/* eslint-disable @typescript-eslint/no-explicit-any */
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.
import * as assert from 'assert';
import { Uri } from 'vscode';
import * as typeMoq from 'typemoq';
import { IConfigurationService } from '../../../../client/common/types';
import { PytestTestDiscoveryAdapter } from '../../../../client/testing/testController/pytest/pytestDiscoveryAdapter';
import { ITestServer } from '../../../../client/testing/testController/common/types';
import { IPythonExecutionFactory, IPythonExecutionService } from '../../../../client/common/process/types';
import { createDeferred, Deferred } from '../../../../client/common/utils/async';

suite('pytest test discovery adapter', () => {
    let testServer: typeMoq.IMock<ITestServer>;
    let configService: IConfigurationService;
    let execFactory = typeMoq.Mock.ofType<IPythonExecutionFactory>();
    let adapter: PytestTestDiscoveryAdapter;
    let execService: typeMoq.IMock<IPythonExecutionService>;
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    let deferred: Deferred<void>;
    setup(() => {
        testServer = typeMoq.Mock.ofType<ITestServer>();
        testServer.setup((t) => t.createUUID(typeMoq.It.isAny())).returns(() => 'uuid123');
        testServer.setup((t) => t.getPort()).returns(() => 12345);
        testServer
            .setup((t) => t.onDataReceived(typeMoq.It.isAny(), typeMoq.It.isAny()))
            .returns(() => ({
                dispose: () => {
                    /* no-body */
                },
            }));
        configService = ({
            getSettings: () => ({
                testing: { pytestArgs: ['.'] },
            }),
        } as unknown) as IConfigurationService;
        execFactory = typeMoq.Mock.ofType<IPythonExecutionFactory>();
        execService = typeMoq.Mock.ofType<IPythonExecutionService>();
        execFactory
            .setup((x) => x.createActivatedEnvironment(typeMoq.It.isAny()))
            .returns(() => Promise.resolve(execService.object));
        deferred = createDeferred();
        let arg;
        execService
            .setup((x) => x.exec(typeMoq.It.isAny(), typeMoq.It.isAny()))
            .returns(() => {
                deferred.resolve();
                arg = typeMoq.It.isAny();
                return Promise.resolve({ stdout: '{}' });
            });
        execFactory.setup((p) => ((p as unknown) as any).then).returns(() => undefined);
        execService.setup((p) => ((p as unknown) as any).then).returns(() => undefined);
        console.log(arg);
    });
    test("onDataReceivedHandler should parse only if cwd matches the test adapter's cwd", async () => {
        const uri = Uri.file('/my/test/path/');
        const data = { status: 'success' };
        const eventData = {
            cwd: uri.fsPath,
            data: JSON.stringify(data),
        };

        adapter = new PytestTestDiscoveryAdapter(testServer.object, configService);
        const promise = adapter.discoverTests(uri, execFactory.object);
        await deferred.promise;
        adapter.onDataReceivedHandler(eventData);
        const result = await promise;
        assert.deepStrictEqual(result, data);
    });
    test("onDataReceivedHandler should not parse if cwd doesn't match the test adapter's cwd", async () => {
        const uri = Uri.file('/my/test/path/');
        let data = { status: 'error' };
        const wrongUriEventData = {
            cwd: Uri.file('/other/path').fsPath,
            data: JSON.stringify(data),
        };
        adapter = new PytestTestDiscoveryAdapter(testServer.object, configService);
        const promise = adapter.discoverTests(uri, execFactory.object);
        adapter.onDataReceivedHandler(wrongUriEventData);

        data = { status: 'success' };
        const correctUriEventData = {
            cwd: uri.fsPath,
            data: JSON.stringify(data),
        };
        adapter.onDataReceivedHandler(correctUriEventData);
        const result = await promise;
        assert.deepStrictEqual(result, data);
        // goal to have the right cwd?
    });
    // test('correct args for discover options', async () => {
    //     // eslint-disable-next-line @typescript-eslint/no-unused-vars

    //     let options: TestCommandOptions | undefined;
    //     const stubConfigSettings = ({
    //         getSettings: () => ({
    //             testing: { unittestArgs: ['-v', '-s', '.', '-p', 'test*'] },
    //         }),
    //     } as unknown) as IConfigurationService;
    //     // testServer
    //     const stubTestServer = ({
    //         sendCommand(opt: TestCommandOptions): Promise<void> {
    //             options = opt;
    //             return Promise.resolve();
    //         },
    //         onDataReceived: () => {
    //             // no body
    //         },
    //     } as unknown) as ITestServer;
    //     const adapter2 = new PytestTestDiscoveryAdapter(stubTestServer, stubConfigSettings);
    //     adapter2.discoverTests(Uri.file('/my/test/path/'), execFactory.object);
    //     assert.deepStrictEqual(options, {
    //         args: ['.'],
    //         cwd: '/my/test/path/',
    //     });
    // });
});
