#!/usr/bin/env bash
# One Yosys-gate fault probe: copy a pristine tree, plant fault(s), run the gate.
# usage: gate_probe.sh <pristine-tree> <scratch-root> <out-dir> <case> [ENV=VAL ...] -- <kind> <arg> [<kind> <arg> ...]
# Writes <out-dir>/<case>.log (gate stdout+stderr) and <out-dir>/<case>.rc.
set -uo pipefail
here=$(cd "$(dirname "$0")" && pwd)
src=$1 scr=$2 out=$3 case=$4; shift 4
envs=()
while [ "$#" -gt 0 ] && [ "$1" != "--" ]; do envs+=("$1"); shift; done
[ "${1-}" = "--" ] && shift
t="$scr/probe-$case"; rm -rf "$t"; mkdir -p "$t" "$out"
cp -a "$src/." "$t/"
{
  while [ "$#" -gt 0 ]; do python3 "$here/plant.py" "$t" "$1" "$2" || exit 9; shift 2; done
  env "${envs[@]}" "$t/syn/yosys/run.sh"
} >"$out/$case.log" 2>&1
echo $? >"$out/$case.rc"
rm -rf "$t"
echo "$case rc=$(cat "$out/$case.rc")"
