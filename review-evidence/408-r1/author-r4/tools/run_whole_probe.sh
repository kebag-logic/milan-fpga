#!/usr/bin/env bash
# One whole-gate probe job: <kind> <name> <mode> <arg> [patch]
#   r273   the round-three external reviewer's probe.py on a JSON case file
#   r273m  the same probe.py at the mutation-table anchor, only the entries
#          named in $A254_LABELS (arg is unused)
#   r272   the round-one internal reviewer's probe_gate1b.py on a case module
#   split  the round-two internal reviewer's split-digraph probe (SDK only;
#          its redacted repository path set to the lane, nothing else changed)
# mode is sdk (the verified disposable SDK mapped) or absent (cross hidden).
set -u
kind=$1 name=$2 mode=$3 arg=$4 patch=${5:-}
R=${A254_REVIEWS:?} LANE=${A254_LANE:?} SDK=${A254_SDK:?} out=${A254_DEST:?}
cd /tmp/a254/scratch
flag=(--absent); [ "$mode" = sdk ] && flag=(--sdk "$SDK")
pflag=(); [ -n "$patch" ] && pflag=(--patch "$patch")
case $kind in
  r273) R273_LANE=$LANE python3 -B "$R/R273-5/probes/probe.py" --cases "$arg" \
          --out "$out/$name.json" "${flag[@]}" "${pflag[@]}" > "$out/$name.log" 2>&1 ;;
  r273m) R273_LANE=$LANE python3 -B "$R/R273-5/probes/probe.py" --anchor mutations \
          --labels "${A254_LABELS:?}" --out "$out/$name.json" "${flag[@]}" \
          "${pflag[@]}" > "$out/$name.log" 2>&1 ;;
  r272) python3 -B "$R/R272-1/scripts/probe_gate1b.py" --tree "$LANE" --cases "$arg" \
          --out "$out/$name.json" "${flag[@]}" "${pflag[@]}" > "$out/$name.log" 2>&1 ;;
  split) python3 -B /tmp/a254/probes-r272-2/probe_split_digraph.py "$SDK" "$arg" \
          > "$out/$name.log" 2>&1 ;;
esac
echo "$name rc=$?"
