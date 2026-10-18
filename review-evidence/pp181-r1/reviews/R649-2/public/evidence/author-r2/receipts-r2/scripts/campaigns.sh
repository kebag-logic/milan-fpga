#!/usr/bin/env bash
# usage: campaigns.sh <tree> <label>  -- every campaign that builds a changed file (round 2):
# d3 beside the rest; name_state and elab_guards refuse an existing output directory
tree=$1; label=$2
out=<data>/tmp/pp181-a635/r2/camp/$label
mkdir -p "$out"
. <data>/tmp/pp181-a635/env.sh
export TMPDIR=<data>/tmp/pp181-a635/tmp; mkdir -p "$TMPDIR"
cd "$tree" || exit 9
run() {   # run <stream> <name> <fresh|made> <command...>
  local stream=$1 name=$2 dir=$3; shift 3
  local t0=$SECONDS rc=0
  rm -rf "$out/$name"
  [ "$dir" = made ] && mkdir -p "$out/$name"
  "$@" > "$out/$name.log" 2>&1 || rc=$?
  echo "$name rc=$rc ($((SECONDS - t0))s)" >> "$out/rc-$stream.txt"
}
: > "$out/rc-a.txt"; : > "$out/rc-b.txt"
( run a d3 made python3 tb/pp_top/d3_mutants.py --output "$out/d3" --jobs 3; echo DONE >> "$out/rc-a.txt" ) &
(
  run b notify made python3 tb/pp_top/notify_mutants.py --output "$out/notify" --jobs 3
  run b dispatch made make -C tb/pp_top aecp-dispatch-mutants AECP_DISPATCH_MUTANT_OUTPUT="$out/dispatch"
  run b aecp made make -C tb/pp_top aecp-mutants MUTANT_OUTPUT="$out/aecp"
  run b ctr made make -C tb/pp_top ctr-mutants CTR_MUTANT_OUTPUT="$out/ctr"
  run b gsi made python3 tb/pp_top/gsi_mutants.py --output "$out/gsi"
  run b name_wr made python3 tb/pp_top/name_wr_mutant.py --output "$out/name_wr"
  run b acmp made python3 tb/pp_top/acmp_mutants.py --output "$out/acmp" --jobs 3
  run b name_state fresh make -C tb/name_state mutants OUTPUT="$out/name_state"
  run b elab_guards fresh make -C tb/elab_guards mutants MUTANT_OUTPUT="$out/elab_guards"
  echo DONE >> "$out/rc-b.txt"
) &
wait
echo "status-after $(git status --short 2>/dev/null | tr '\n' ';')" > "$out/done.txt"
echo CAMP-DONE >> "$out/done.txt"
