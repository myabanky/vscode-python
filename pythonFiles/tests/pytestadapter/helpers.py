# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import http.client
import http.server
import io
import json
import os
import pathlib
import socket
import socketserver
import subprocess
import sys
import threading
import uuid
from typing import Dict, List, Sequence, Union
import ssl

TEST_DATA_PATH = pathlib.Path(__file__).parent / ".data"


# def create_server(host=None, port=0, backlog=socket.SOMAXCONN, timeout=None):
# """Return a local server socket listening on the given port."""

# assert backlog > 0
# if host is None:
#     host = "127.0.0.1"
# if port is None:
#     port = 0

# try:
#     server = _new_sock()
#     if port != 0:
#         if sys.platform == "win32":
#             server.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
#         else:
#             try:
#                 server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#             except (AttributeError, OSError):
#                 pass  # Not available everywhere
#     server.bind((host, port))
#     if timeout is not None:
#         server.settimeout(timeout)
#     server.listen(backlog)
# except Exception:
#     # server.close()
#     raise
# return server

# def create_server(host=None, port=0, backlog=socket.SOMAXCONN, timeout=None):


def create_client():
    """Return a client socket that may be connected to a remote address."""
    return _new_sock()


def _new_sock():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

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
    """
    Process the RPC JSON data and checks to make sure it has a Content-Length header.
    Returns the JSON data as a dictionary.
    """
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
    """
    Helper function that runs the pytest on the given args and returns the JSON data of the result.
    This method uses multithreading to handle both creating a listener and running the pytest command
    as a subprocess.
    """
    process_args = [
        sys.executable,
        "-m",
        "pytest",
        "-p",
        "vscode_pytest",
    ] + args

    server_address = ("", 0)
    Handler = PostHandlerPytest
    httpd = http.server.HTTPServer(server_address, PostHandlerPytest)
    ip, port = httpd.socket.getsockname()

    env = {
        "TEST_UUID": str(uuid.uuid4()),
        "TEST_PORT": str(port),
        "PYTHONPATH": os.fspath(pathlib.Path(__file__).parent.parent.parent),
    }

    result = []
    t1 = threading.Thread(target=listen_on_socket, args=(httpd, result))
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
    """
    Helper function that runs the given process args and env as a subprocess from the test data path.
    """
    subprocess.run(
        process_args,
        env=env,
        cwd=os.fspath(TEST_DATA_PATH),
    )


def listen_on_socket(httpd: http.server.HTTPServer, result: List[str]):
    """
    Helper function that listens on the given socket and appends the result to the given list.
    """
    httpd.serve_forever()

    # response = conn.getresponse()
    print(response.status, response.reason)
    # all_data = ""
    # while True:
    #     data = sock.recv(1024 * 1024)
    #     if not data:
    #         break
    #     all_data = all_data + data.decode("utf-8")
    # result.append(all_data)


class PostHandlerPytest(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = f"Received POST request:\n\n{body}"
        self.wfile.write(response.encode("utf-8"))
