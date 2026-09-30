#!/bin/sh
# Grade a probe set of the round-4 internal review inside gate 1b, with that
# review's scripts unchanged: make_probes.py (or make_probes_r3shapes.py) writes
# the set, patch_probe_hook.py inserts its hook into a byte copy of the clone,
# and run_gate.sh runs test_baremetal_profile_contract() with R412_PROBES set,
# so every probe is graded through the same census_take() and
# assert_resolved_boot_flow(source=...) path as the planted breaks. The log
# starts with the head it ran at; the copy is deleted after the run.
# usage: r412_probe_run.sh <clone> <review> <work> <make-script> <name>
set -eu
clone=$1; review=$2; work=$3; make=$4; name=$5
tree=$work/scratch/probe_$name
mkdir -p "$work/probes" "$work/scratch"
rm -rf "$tree"; mkdir -p "$tree"; cp -a "$clone/." "$tree/"
json=$work/probes/$name.json
log=$work/probes/$name.log
python3 -B "$review/scripts/$make" "$json"
python3 -B "$review/scripts/patch_probe_hook.py" "$tree"
status=$(R412_PROBES=$json "$review/scripts/run_gate.sh" "$tree" "$log.run")
{ echo "probes=$name head=$(git -C "$clone" rev-parse HEAD)"; cat "$log.run"; echo "$status"; } > "$log"
rm -f "$log.run"
rm -rf "$tree"
