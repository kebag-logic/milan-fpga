#!/usr/bin/env bash
# Build and run pp_top from an exported, probe-patched processor tree.
# Usage: run_pp_top.sh <exported-pp-root> <verilator> <log>
# Same flags as tb/pp_top/Makefile except the build parallelism is capped at 8.
set -u
root=$1
verilator=$2
log=$3
cd "$root/tb/pp_top" || exit 2
vflags='--cc --exe --build -j 8 --top-module pp_top_wrap -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"'
{
  printf 'verilator: %s\n' "$("$verilator" --version)"
  timeout 3000 make run VERILATOR="$verilator" VFLAGS="$vflags"
  printf 'exit=%s\n' "$?"
} > "$log" 2>&1
tail -n 5 "$log"
