#!/usr/bin/env bash
# usage: campaigns2.sh <tree> <label>  -- the two campaigns that refuse an existing output directory
tree=$1; label=$2
out=<data>/tmp/pp181-a635/camp/$label
mkdir -p "$out"
. <data>/tmp/pp181-a635/env.sh
export TMPDIR=<data>/tmp/pp181-a635/tmp; mkdir -p "$TMPDIR"
cd "$tree" || exit 9
run() {
  local name=$1; shift
  local t0=$SECONDS rc=0
  rm -rf "$out/$name"
  "$@" > "$out/$name.log" 2>&1 || rc=$?
  echo "$name rc=$rc ($((SECONDS - t0))s)" >> "$out/rc-c.txt"
}
: > "$out/rc-c.txt"
run name_state make -C tb/name_state mutants OUTPUT="$out/name_state"
run elab_guards make -C tb/elab_guards mutants MUTANT_OUTPUT="$out/elab_guards"
echo DONE >> "$out/rc-c.txt"
