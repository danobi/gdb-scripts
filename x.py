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

    sh(f"podman run -it -v={src}:/gdb/src -v={build}:/gdb/build localhost/{IMAGE_NAME} /bin/bash -c 'cd build && ../configure.sh'")

def cmd_build(args):
    build_image()

    src = os.path.expanduser(args.source_dir)
    build = os.path.expanduser(args.build_dir)

    sh(f"podman run -v={src}:/gdb/src -v={build}:/gdb/build localhost/{IMAGE_NAME} make -C build -j4")

def main():
    parser = argparse.ArgumentParser(prog='x')
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
            default='~/dev/gdb/build',
            help='build directory')

    subparsers = parser.add_subparsers(help='subcommands')

    configure = subparsers.add_parser(
            'conf',
            help='configure and build gdb container image')
    configure.set_defaults(func=cmd_configure)

    build = subparsers.add_parser('build', help='build gdb')
    build.set_defaults(func=cmd_build)

    help = subparsers.add_parser(
            'help',
            help='print help')
    help.set_defaults(func=lambda _: parser.print_help())


    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()