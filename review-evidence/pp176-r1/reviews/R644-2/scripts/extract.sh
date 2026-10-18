#!/bin/sh
# extract.sh CLONE REV DEST : disposable extract of REV's tree (no .git)
set -eu
rm -rf "$3"; mkdir -p "$3"
git -C "$1" archive "$2" | tar -x -C "$3"
