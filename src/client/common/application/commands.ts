// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

'use strict';

import { CancellationToken, Position, TextDocument, Uri } from 'vscode';
import { Commands as LSCommands } from '../../activation/commands';
import { TensorBoardEntrypoint, TensorBoardEntrypointTrigger } from '../../tensorBoard/constants';
import { Channel, Commands, CommandSource } from '../constants';

export type CommandsWithoutArgs = keyof ICommandNameWithoutArgumentTypeMapping;

/**
 * Mapping between commands and list or arguments.
 * These commands do NOT have any arguments.
 * @interface ICommandNameWithoutArgumentTypeMapping
 */
interface ICommandNameWithoutArgumentTypeMapping {
    [Commands.InstallPythonOnMac]: [];
    [Commands.InstallJupyter]: [];
    [Commands.InstallPythonOnLinux]: [];
    [Commands.InstallPython]: [];
    [Commands.ClearWorkspaceInterpreter]: [];
    [Commands.Set_Interpreter]: [];
    [Commands.Set_ShebangInterpreter]: [];
    [Commands.Run_Linter]: [];
    [Commands.Enable_Linter]: [];
    ['workbench.action.showCommands']: [];
    ['workbench.action.debug.continue']: [];
    ['workbench.action.debug.stepOver']: [];
    ['workbench.action.debug.stop']: [];
    ['workbench.action.reloadWindow']: [];
    ['workbench.action.closeActiveEditor']: [];
    ['workbench.action.terminal.focus']: [];
    ['editor.action.formatDocument']: [];
    ['editor.action.rename']: [];
    [Commands.ViewOutput]: [];
    [Commands.Set_Linter]: [];
    [Commands.Start_REPL]: [];
    [Commands.Enable_SourceMap_Support]: [];
    [Commands.Exec_Selection_In_Terminal]: [];
    [Commands.Exec_Selection_In_Django_Shell]: [];
    [Commands.Create_Terminal]: [];
    [Commands.PickLocalProcess]: [];
    [Commands.ClearStorage]: [];
    [Commands.CreateNewFile]: [];
    [Commands.ReportIssue]: [];
    [Commands.RefreshTensorBoard]: [];
    [LSCommands.RestartLS]: [];
}

export type AllCommands = keyof ICommandNameArgumentTypeMapping;

/**
 * Mapping between commands and list of arguments.
 * Used to provide strong typing for command & args.
 * @export
 * @interface ICommandNameArgumentTypeMapping
 * @extends {ICommandNameWithoutArgumentTypeMapping}
 */
export interface ICommandNameArgumentTypeMapping extends ICommandNameWithoutArgumentTypeMapping {
    ['vscode.openWith']: [Uri, string];
    ['workbench.action.quickOpen']: [string];
    ['workbench.action.openWalkthrough']: [string | { category: string; step: string }, boolean | undefined];
    ['workbench.extensions.installExtension']: [
        Uri | string,
        (
            | {
                  installOnlyNewlyAddedFromExtensionPackVSIX?: boolean;
                  installPreReleaseVersion?: boolean;
                  donotSync?: boolean;
              }
            | undefined
        ),
    ];
    ['workbench.action.files.openFolder']: [];
    ['workbench.action.openWorkspace']: [];
    ['setContext']: [string, boolean] | ['python.vscode.channel', Channel];
    ['python.reloadVSCode']: [string];
    ['revealLine']: [{ lineNumber: number; at: 'top' | 'center' | 'bottom' }];
    ['python._loadLanguageServerExtension']: [];
    ['python.SelectAndInsertDebugConfiguration']: [TextDocument, Position, CancellationToken];
    ['vscode.open']: [Uri];
    ['notebook.execute']: [];
    ['notebook.cell.execute']: [];
    ['notebook.cell.insertCodeCellBelow']: [];
    ['notebook.undo']: [];
    ['notebook.redo']: [];
    ['python.viewLanguageServerOutput']: [];
    ['vscode.open']: [Uri];
    ['workbench.action.files.saveAs']: [Uri];
    ['workbench.action.files.save']: [Uri];
    ['jupyter.opennotebook']: [undefined | Uri, undefined | CommandSource];
    ['jupyter.runallcells']: [Uri];
    ['extension.open']: [string];
    ['workbench.action.openIssueReporter']: [{ extensionId: string; issueBody: string }];
    [Commands.GetSelectedInterpreterPath]: [{ workspaceFolder: string } | string[]];
    [Commands.TriggerEnvironmentSelection]: [undefined | Uri];
    [Commands.Sort_Imports]: [undefined, Uri];
    [Commands.Exec_In_Terminal]: [undefined, Uri];
    [Commands.Exec_In_Terminal_Icon]: [undefined, Uri];
    [Commands.Debug_In_Terminal]: [Uri];
    [Commands.Tests_Configure]: [undefined, undefined | CommandSource, undefined | Uri];
    [Commands.LaunchTensorBoard]: [TensorBoardEntrypoint, TensorBoardEntrypointTrigger];
    ['workbench.view.testing.focus']: [];
}
