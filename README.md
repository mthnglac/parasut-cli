parasut-cli
===========

Parasut CLI for managing workspace

[![oclif](https://img.shields.io/badge/cli-oclif-brightgreen.svg)](https://oclif.io)
[![Version](https://img.shields.io/npm/v/parasut-cli.svg)](https://npmjs.org/package/parasut-cli)
[![Downloads/week](https://img.shields.io/npm/dw/parasut-cli.svg)](https://npmjs.org/package/parasut-cli)
[![License](https://img.shields.io/npm/l/parasut-cli.svg)](https://github.com/mthnglac/parasut-cli/blob/master/package.json)

<!-- toc -->
* [Usage](#usage)
* [Commands](#commands)
<!-- tocstop -->
# Usage
<!-- usage -->
```sh-session
$ npm install -g parasut-cli
$ parasut-cli COMMAND
running command...
$ parasut-cli (-v|--version|version)
parasut-cli/0.0.0 linux-x64 node-v14.15.4
$ parasut-cli --help [COMMAND]
USAGE
  $ parasut-cli COMMAND
...
```
<!-- usagestop -->
# Commands
<!-- commands -->
* [`parasut-cli hello [FILE]`](#parasut-cli-hello-file)
* [`parasut-cli help [COMMAND]`](#parasut-cli-help-command)

## `parasut-cli hello [FILE]`

describe the command here

```
USAGE
  $ parasut-cli hello [FILE]

OPTIONS
  -f, --force
  -h, --help       show CLI help
  -n, --name=name  name to print

EXAMPLE
  $ parasut-cli hello
  hello world from ./src/hello.ts!
```

_See code: [src/commands/hello.ts](https://github.com/mthnglac/parasut-cli/blob/v0.0.0/src/commands/hello.ts)_

## `parasut-cli help [COMMAND]`

display help for parasut-cli

```
USAGE
  $ parasut-cli help [COMMAND]

ARGUMENTS
  COMMAND  command to show help for

OPTIONS
  --all  see all commands in CLI
```

_See code: [@oclif/plugin-help](https://github.com/oclif/plugin-help/blob/v3.2.2/src/commands/help.ts)_
<!-- commandsstop -->
