#!/bin/sh
# Build the reviewer property probe against a given KL_media_clock_restart.sv
# Usage: run.sh <path/to/KL_media_clock_restart.sv> <build-dir> [seed]
set -eu
here=$(cd "$(dirname "$0")" && pwd)
"${VERILATOR:-verilator}" --cc --exe --build -j 4 -Wno-fatal --Mdir "$2" \
  --top-module KL_media_clock_restart -GN_TALKERS_P=2 "$1" "$here/tb.cpp" -o probe >/dev/null
"$2/probe" "${3:-1}"
