gdb-scripts
-----------

This repository contains scripts/commands used to develop/build/test GDB.

GDB is fairly hard to get built and tested so I containerized the build to make
it easier to reproduce on my machines.

# Usage

Run `./x.py` to see help menu:

```
usage: x [-h] [-s SOURCE_DIR] [-b BUILD_DIR] {conf,build,run,shell,help} ...

positional arguments:
  {conf,build,run,shell,help}
                        subcommands
    conf                configure and build gdb container image
    build               build gdb
    run                 run gdb
    shell               open shell
    help                print help

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE_DIR, --source-dir SOURCE_DIR
                        source code directory
  -b BUILD_DIR, --build-dir BUILD_DIR
                        build directory

```

# Notes

You'll need [`podman`](https://podman.io/) installed on your system for these
scripts to work. The default file paths are also built around my preferences
but I've left command line options to override the the defaults.
