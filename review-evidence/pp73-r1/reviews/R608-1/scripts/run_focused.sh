#!/usr/bin/env bash
# Focused source checks for one checkout: make check, the uPC/M9 preambles,
# and the two suites that consume the generated ucode.hex (tb/ucpu, tb/pp_top).
# usage: run_focused.sh <checkout> <label> <outdir> <verilator-dir> [jobs]
# Writes <outdir>/<label>.<step>.log and .rc; never edits the checkout's
# tracked files (suite build products are ignored build outputs).
set -u
tree=$1; label=$2; out=$3; vdir=$4; jobs=${5:-6}
export PATH="$vdir:$PATH"
mkdir -p "$out"
step() {  # step <name> <dir> <cmd...>
  local name=$1 dir=$2; shift 2
  (cd "$dir" && "$@") >"$out/$label.$name.log" 2>&1
  echo $? >"$out/$label.$name.rc"
}
step verilator-version "$tree" verilator --version
step make-check "$tree" make check
step upc-map "$tree" python3 scripts/check_upc_map.py
step m9 "$tree" python3 scripts/check_m9_opcodes.py
step ucpu "$tree/tb/ucpu" make VFLAGS="--cc --exe --build -j $jobs --top-module KL_aecp_ucpu -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -CFLAGS -std=c++17\ -O2\ -I$tree/tb/ucpu\ -Wall\ -Wextra"
step pp_top "$tree/tb/pp_top" make VFLAGS="--cc --exe --build -j $jobs --top-module pp_top_wrap -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -CFLAGS -std=c++17\ -O2\ -I$tree/tb/pp_top\ -Wall\ -Wextra"
echo done >"$out/$label.DONE"
