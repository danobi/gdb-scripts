#!/bin/python3

import argparse
import os
import pathlib
import subprocess
import sys

IMAGE_NAME = "gdb-builder"

def sh(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(1)

def cwd():
    return pathlib.Path(__file__).parent.absolute()

def build_image():
    sh(f"podman build -t {IMAGE_NAME} {cwd()}")

def cmd_configure(args):
    build_image()

    src = os.path.expanduser(args.source_dir)
    build = os.path.expanduser(args.build_dir)

    a = ['podman run']
    a.append(f"-it")
    a.append(f"-v={src}:/gdb/src")
    a.append(f"-v={build}:/gdb/build")
    a.append(f"localhost/{IMAGE_NAME}")
    a.append(f"/bin/bash -c 'cd build && ../configure.sh'")

    sh(" ".join(a))

def cmd_build(args):
    build_image()

    src = os.path.expanduser(args.source_dir)
    build = os.path.expanduser(args.build_dir)

    a = ['podman run']
    a.append(f"-v={src}:/gdb/src")
    a.append(f"-v={build}:/gdb/build")
    a.append(f"localhost/{IMAGE_NAME}")
    a.append(f"make -C build -j{args.parallel}")

    sh(" ".join(a))

def cmd_run(args):
    build_image()

    src = os.path.expanduser(args.source_dir)
    build = os.path.expanduser(args.build_dir)
    if args.gdb_args:
        gdb_args = " ".join([str(x) for x in args.gdb_args])
    else:
        gdb_args = ""

    a = ['podman run']
    a.append(f"-it")
    a.append(f"-v={src}:/gdb/src")
    a.append(f"-v={build}:/gdb/build")
    a.append(f"--cap-add=SYS_PTRACE ")
    a.append(f"--security-opt seccomp=unconfined")
    a.append(f"localhost/{IMAGE_NAME}")
    a.append(f"./build/gdb/gdb {gdb_args}")

    sh(" ".join(a))

def cmd_shell(args):
    build_image()

    src = os.path.expanduser(args.source_dir)
    build = os.path.expanduser(args.build_dir)

    a = ['podman run']
    a.append(f"-it")
    a.append(f"-v={src}:/gdb/src")
    a.append(f"-v={build}:/gdb/build")
    a.append(f"--cap-add=SYS_PTRACE ")
    a.append(f"--security-opt seccomp=unconfined")
    a.append(f"localhost/{IMAGE_NAME}")
    a.append(f"/bin/bash")

    sh(" ".join(a))

def cmd_test(args):
    build_image()

    src = os.path.expanduser(args.source_dir)
    build = os.path.expanduser(args.build_dir)
    if args.test_args:
        test_args = " ".join([str(x) for x in args.test_args])
    else:
        test_args = ""

    a = ['podman run']
    a.append(f"-it")
    a.append(f"-v={src}:/gdb/src")
    a.append(f"-v={build}:/gdb/build")
    a.append(f"--cap-add=SYS_PTRACE ")
    a.append(f"--security-opt seccomp=unconfined")
    a.append(f"localhost/{IMAGE_NAME}")
    a.append(f"make -C build/gdb/testsuite check RUNTESTFLAGS='{test_args}'")

    sh(" ".join(a))

def main():
    parser = argparse.ArgumentParser(
            prog='x',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
            '-s',
            '--source-dir',
            type=str,
            default='~/dev/gdb',
            help='source code directory')
    parser.add_argument(
            '-b',
            '--build-dir',
            type=str,
            default='/tmp/gdb-build',
            help='build directory')
    parser.set_defaults(func=lambda _: parser.print_help())

    subparsers = parser.add_subparsers(help='subcommands')

    configure = subparsers.add_parser(
            'conf',
            help='configure and build gdb container image')
    configure.set_defaults(func=cmd_configure)

    build = subparsers.add_parser('build', help='build gdb')
    build.add_argument(
            '-j',
            '--parallel',
            type=int,
            default=4,
            help='make -j N')
    build.set_defaults(func=cmd_build)

    run = subparsers.add_parser('run', help='run gdb')
    run.add_argument(
            'gdb_args',
            nargs=argparse.REMAINDER,
            help='additional arguments to gdb')
    run.set_defaults(func=cmd_run)

    shell = subparsers.add_parser('shell', help='open shell')
    shell.set_defaults(func=cmd_shell)

    test = subparsers.add_parser('test', help='run `make check tests`')
    test.add_argument(
            'test_args',
            nargs=argparse.REMAINDER,
            help='additional arguments to `make check RUNTESTFLAGS`')
    test.set_defaults(func=cmd_test)

    help = subparsers.add_parser(
            'help',
            help='print help')
    help.set_defaults(func=lambda _: parser.print_help())


    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
