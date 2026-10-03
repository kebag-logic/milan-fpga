#!/usr/bin/env bash
# R448-3: one probe of the round-3 census (yosys's own module list).
# Copies a pristine tree, applies one edit, runs the tree's syn/yosys/run.sh.
# usage: r3_probe.sh <tree> <scratch> <out> <case>
# Writes <out>/<case>.log and <out>/<case>.rc.
set -uo pipefail
here=$(cd "$(dirname "$0")" && pwd)
src=$1 scr=$2 out=$3 case=$4
t="$scr/r3-$case"; rm -rf "$t"; mkdir -p "$t" "$out"; cp -a "$src/." "$t/"
run="$t/syn/yosys/run.sh"
newmod() { # <name> <header-prefix> <fault:yes|no>
  local body=""
  [ "$3" = yes ] && body="  r448_absent_module u_r448_planted ();"
  printf '// SPDX-License-Identifier: CERN-OHL-W-2.0\n%smodule %s (input logic a_i);\n%s\nendmodule\n' \
    "$2" "$1" "$body" > "$t/hdl/top/$1.sv"
}
addtop() { sed -i "s/protocol_processor_top)/protocol_processor_top $1)/" "$run"; }
mut() { # <python-replace-old> <new>: exact one-occurrence replacement in run.sh
  python3 - "$run" "$1" "$2" <<'PY' || exit 9
import sys
p, old, new = sys.argv[1:]
s = open(p).read()
assert s.count(old) == 1, (old, s.count(old))
open(p, "w").write(s.replace(old, new))
PY
}
{
  case "$case" in
    pristine) ;;
    bbox)            newmod KL_r448_bbox '(* blackbox *) ' no ;;
    bbox-top)        newmod KL_r448_bbox '(* blackbox *) ' no; addtop KL_r448_bbox ;;
    bbox-fault)      newmod KL_r448_bboxf '(* blackbox *) ' yes ;;
    wbox)            newmod KL_r448_wbox '(* whitebox *) ' no ;;
    wbox-top)        newmod KL_r448_wbox '(* whitebox *) ' no; addtop KL_r448_wbox ;;
    static-split)    printf 'module static\n  KL_r448_static (input logic a_i);\nendmodule\n' > "$t/hdl/top/KL_r448_static.sv" ;;
    # the first top fails elaboration AND an uncovered module exists: the
    # census must still run on run 1's list, before any verdict line
    first-top-red-plus-uncovered)
      python3 "$here/r448-2/plant.py" "$t" absent KL_aecp_desc_mem_guard || exit 9
      newmod KL_r448_plain '' yes ;;
    # mutants of the round-3 change; each must be killed by some probe
    m-select-no-boxes+bbox) mut 'declared.txt select -list =*' 'declared.txt select -list *'; newmod KL_r448_bbox '(* blackbox *) ' no ;;
    m-ls+bbox)        mut 'tee -q -o declared.txt select -list =*' 'tee -q -o declared.txt ls'; newmod KL_r448_bbox '(* blackbox *) ' no ;;
    m-ls)             mut 'tee -q -o declared.txt select -list =*' 'tee -q -o declared.txt ls' ;;
    m-no-census+attr) mut '|| census
' '|| true
'; newmod KL_r448_attrs '(* keep_hierarchy = "yes" *) ' yes ;;
    m-no-list)        mut 'tee -q -o declared.txt select -list =*\n' '' ;;
    m-sed-pattern)    mut "s/^\\\$abstract\\\\//p" "s/^\\\\//p" ;;
    m-census-every-run+allv) mut "[ \"\$parses\" -gt 1 ] || ! grep -q '^@@begin ' gate.log || census" '[ "$parses" -gt 1 ] || census'
                      python3 "$here/r448-2/plant.py" "$t" allv-syntax KL_srp_top || exit 9 ;;
    m-list-cmd-unsupported) mut 'declared.txt select -list =*' 'declared.txt select -r448-no-such-option =*' ;;
    *) echo "unknown case $case"; exit 9 ;;
  esac
  "$run"
} >"$out/$case.log" 2>&1
echo $? >"$out/$case.rc"
rm -rf "$t"
echo "$case rc=$(cat "$out/$case.rc")"
