#!/usr/bin/env bash
# usage: campaigns.sh <tree> <label> <stream>   -- the campaigns that build a changed file
# stream a: d3 alone (the longest); stream b: the rest but name_state and elab_guards (campaigns2.sh)
tree=$1; label=$2; stream=$3
out=<data>/tmp/pp181-a635/camp/$label
mkdir -p "$out"
. <data>/tmp/pp181-a635/env.sh
export TMPDIR=<data>/tmp/pp181-a635/tmp; mkdir -p "$TMPDIR"
cd "$tree" || exit 9
run() {
  local name=$1; shift
  local t0=$SECONDS rc=0
  rm -rf "$out/$name"; mkdir -p "$out/$name"
  "$@" > "$out/$name.log" 2>&1 || rc=$?
  echo "$name rc=$rc ($((SECONDS - t0))s)" >> "$out/rc-$stream.txt"
}
: > "$out/rc-$stream.txt"
if [ "$stream" = a ]; then
  run d3 python3 tb/pp_top/d3_mutants.py --output "$out/d3" --jobs 4
else
  run notify python3 tb/pp_top/notify_mutants.py --output "$out/notify" --jobs 4
  run dispatch make -C tb/pp_top aecp-dispatch-mutants AECP_DISPATCH_MUTANT_OUTPUT="$out/dispatch"
  run aecp make -C tb/pp_top aecp-mutants MUTANT_OUTPUT="$out/aecp"
  run ctr make -C tb/pp_top ctr-mutants CTR_MUTANT_OUTPUT="$out/ctr"
  run gsi python3 tb/pp_top/gsi_mutants.py --output "$out/gsi"
  run name_wr python3 tb/pp_top/name_wr_mutant.py --output "$out/name_wr"
  run acmp python3 tb/pp_top/acmp_mutants.py --output "$out/acmp" --jobs 4
fi
echo DONE >> "$out/rc-$stream.txt"
