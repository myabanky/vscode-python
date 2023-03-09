# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import io
import json
import os
import pathlib
import socket
import subprocess
import sys
import threading
import uuid
from typing import Dict, List, Sequence, Union

TEST_DATA_PATH = pathlib.Path(__file__).parent / ".data"


def create_server(host=None, port=0, backlog=socket.SOMAXCONN, timeout=None):
    """Return a local server socket listening on the given port."""

    assert backlog > 0
    if host is None:
        host = "127.0.0.1"
    if port is None:
        port = 0

    try:
        server = _new_sock()
        if port != 0:
            # If binding to a specific port, make sure that the user doesn't have
            # to wait until the OS times out the socket to be able to use that port
            # again.if the server or the adapter crash or are force-killed.
            if sys.platform == "win32":
                server.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
            else:
                try:
                    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                except (AttributeError, OSError):
                    pass  # Not available everywhere
        server.bind((host, port))
        if timeout is not None:
            server.settimeout(timeout)
        server.listen(backlog)
    except Exception:
        # server.close()
        raise
    return server


def create_client():
    """Return a client socket that may be connected to a remote address."""
    return _new_sock()


def _new_sock():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

    # Set TCP keepalive on an open socket.
    # It activates after 1 second (TCP_KEEPIDLE,) of idleness,
    # then sends a keepalive ping once every 3 seconds (TCP_KEEPINTVL),
    # and closes the connection after 5 failed ping (TCP_KEEPCNT), or 15 seconds
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    except (AttributeError, OSError):
        pass  # May not be available everywhere.
    try:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 1)  # type: ignore
    except (AttributeError, OSError):
        pass  # May not be available everywhere.
    try:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 3)
    except (AttributeError, OSError):
        pass  # May not be available everywhere.
    try:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)
    except (AttributeError, OSError):
        pass  # May not be available everywhere.
    return sock


def shut_down(sock, how=socket.SHUT_RDWR):
    """Shut down the given socket."""
    sock.shutdown(how)


def close_socket(sock):
    """Shutdown and close the socket."""
    try:
        shut_down(sock)
    except Exception:
        pass
    sock.close()


CONTENT_LENGTH = "Content-Length:"


def process_rpc_json(data: str) -> Dict[str, str]:
    str_stream = io.StringIO(data)

    length = None

    while True:
        line = str_stream.readline()
        if line.startswith(CONTENT_LENGTH):
            length = int(line[len(CONTENT_LENGTH) :])
            break

        if not line or line.strip() == "":
            raise ValueError("Header does not contain Content-Length")

    while True:
        line = str_stream.readline()
        if not line or line.strip() == "":
            break

    raw_json = str_stream.read(length)
    return json.loads(raw_json)


def runner(args: List[str]) -> Union[Dict[str, str], None]:
    process_args = [
        sys.executable,
        "-m",
        "pytest",
        "-p",
        "vscode_pytest",
    ] + args

    listener = create_server()
    _, port = listener.getsockname()
    listener.listen()

    env = {
        "TEST_UUID": str(uuid.uuid4()),
        "TEST_PORT": str(port),
        "PYTHONPATH": os.fspath(pathlib.Path(__file__).parent.parent.parent),
    }

    result = []
    t1 = threading.Thread(target=listen_on_socket, args=(listener, result))
    t1.start()

    t2 = threading.Thread(
        target=subprocess_run_task,
        args=(process_args, env),
    )
    t2.start()

    t1.join()
    t2.join()

    return process_rpc_json(result[0]) if result else None


def subprocess_run_task(process_args: Sequence[str], env: Dict[str, str]):
    subprocess.run(
        process_args,
        env=env,
        cwd=os.fspath(TEST_DATA_PATH),
    )


def listen_on_socket(listener: socket.socket, result: List[str]):
    sock, (other_host, other_port) = listener.accept()
    all_data = ""
    while True:
        data = sock.recv(1024 * 1024)
        if not data:
            break
        all_data = all_data + data.decode("utf-8")
    result.append(all_data)
