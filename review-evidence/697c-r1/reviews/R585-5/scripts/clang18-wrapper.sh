#!/bin/sh
exec env LD_LIBRARY_PATH=$VALIDATION_TOOLS/clang-18/root/usr/lib/x86_64-linux-gnu $VALIDATION_TOOLS/clang-18/root/usr/bin/clang-18 "$@"
