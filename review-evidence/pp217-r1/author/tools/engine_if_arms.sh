#!/usr/bin/env bash
# engine_if_arms.sh <tree> <runs>: a one-off measurement, not a campaign: the control and the two issue #217 engine
# arms (last-index-is-next, last-index-kept-after-departing) against tb/adp_engine's two-interface build
# (`make interfaces`, IF1 to IF9), each in a scratch copy made as tb/adp_engine/mutants.py makes its own (hdl and
# the three suites, generated files left out, the patch planted with git apply --check then git apply).
set -u
T=$(cd "$1" && pwd); R=$2
. "$(dirname "$0")/common.sh"
CAP=$(cd "$(dirname "$0")" && pwd)/vl-cap
mkdir -p "$R" "$S/tmp/engine-if"
for arm in control last-index-is-next last-index-kept-after-departing; do
  w=$(mktemp -d "$S/tmp/engine-if/$arm.XXXX")
  cp -r "$T/hdl" "$w/hdl"; mkdir -p "$w/tb"
  for s in common adp_engine pp_top; do
    rsync -a --exclude 'obj_*' --exclude '*.hex' --exclude '__pycache__' "$T/tb/$s/" "$w/tb/$s/"
  done
  if [ "$arm" != control ]; then
    (cd "$w" && git apply --check "$T/tb/adp_engine/mutations/$arm.patch" && git apply "$T/tb/adp_engine/mutations/$arm.patch") \
      > "$R/$arm.plant.log" 2>&1 || { echo "plant failed" >> "$R/$arm.plant.log"; echo 99 > "$R/$arm.rc"; continue; }
  fi
  g "$R" "$w" "$CAP:$SV:$BASE" "$arm" make -C tb/adp_engine interfaces
  rm -rf "$w"
done
echo done > "$R/ALL.done"
