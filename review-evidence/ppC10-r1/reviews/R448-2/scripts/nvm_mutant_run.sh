#!/usr/bin/env bash
# One elab_bounds.sh mutant: copy the tree, mutate, run the bench with the
# pinned Verilator. "-nopath" mutants run with sv2v and yosys off PATH.
# usage: nvm_mutant_run.sh <tree> <scratch> <out> <verilator> <mutant>
set -uo pipefail
here=$(cd "$(dirname "$0")" && pwd)
src=$1 scr=$2 out=$3 vl=$4 m=$5
t="$scr/nvm-$m"; rm -rf "$t"; mkdir -p "$t" "$out"; cp -a "$src/." "$t/"
path=$PATH
if [[ $m == *-nopath ]]; then
  nb="$scr/nopath-bin-$m"; rm -rf "$nb"; mkdir -p "$nb"
  for x in /usr/bin/*; do case ${x##*/} in yosys*|sv2v*) ;; *) ln -s "$x" "$nb/" ;; esac; done
  path=$nb
fi
{
  python3 "$here/nvm_mutants.py" "$t" "$m" || exit 9
  echo "sv2v on PATH: $(PATH=$path command -v sv2v || echo none); yosys on PATH: $(PATH=$path command -v yosys || echo none)"
  PATH=$path VERILATOR=$vl "$t/tb/nvm_port/elab_bounds.sh"
} >"$out/$m.log" 2>&1
echo $? >"$out/$m.rc"
rm -rf "$t"
echo "$m rc=$(cat "$out/$m.rc")"
