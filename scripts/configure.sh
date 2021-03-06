#!/bin/bash
#
# This script's CWD should be /gdb/build

../src/configure \
  --disable-binutils \
  --disable-ld \
  --disable-gold \
  --disable-gas \
  --disable-gprof \
  --disable-nls \
  --with-system-readline \
  --with-system-zlib \
  --enable-unit-tests \
  --enable-maintainer-mode
