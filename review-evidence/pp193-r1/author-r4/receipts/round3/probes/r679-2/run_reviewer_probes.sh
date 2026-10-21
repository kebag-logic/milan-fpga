#!/bin/sh
# Re-run this review's own probes on a processor clone, never touching it.
# usage: run_reviewer_probes.sh <clone> <revision> <outdir>
# Needs Verilator 5.050 (the CI pin) as `verilator` on PATH. Exports the
# revision with `git archive` into <outdir>; each run's status is in <name>.rc.
#   s2:          s2_probe.py inserted into tb/srp_stream_fsms (handover into a
#                walked slot, plain tx! and txLA! walks, with two controls each)
#   repark:      repark_probe.py on the revision
#   repark-mut:  repark_probe.py with rv-repark-overwrites-pairs.patch planted
#   campaign:    make_extra_mutants.py arms plus the six round-2 controls,
#                through the revision's own tb/srp_top/mutants.py (--jobs 16)
set -u
clone=$1; rev=$2; out=$3
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$out"
export_to() { rm -rf "$1"; mkdir -p "$1"; git -C "$clone" archive "$rev" | tar -x -C "$1"; }
export_to "$out/s2"; export_to "$out/repark"; export_to "$out/repark-mut"; export_to "$out/camp"
python3 -I "$here/s2_probe.py" "$out/s2/tb/srp_stream_fsms/sim_main.cpp"
python3 -I "$here/repark_probe.py" "$out/repark/tb/srp_stream_fsms/sim_main.cpp"
(cd "$out/repark-mut" && patch -s -p1 < "$here/rv-repark-overwrites-pairs.patch")
python3 -I "$here/repark_probe.py" "$out/repark-mut/tb/srp_stream_fsms/sim_main.cpp"
(cd "$out/camp" && git init -q && python3 -I "$here/make_extra_mutants.py" "$out/camp")
for n in s2 repark repark-mut; do
  ( cd "$out/$n/tb/srp_stream_fsms" && make RUN_ARGS=suite > "$out/$n.log" 2>&1; echo $? > "$out/$n.rc" )
done
( cd "$out/camp" && sed -i "s/'srp_top', '', ':')/'srp_top', 'share', ':')/" tb/srp_top/mutants.py \
  && python3 -I tb/srp_top/mutants.py --output "$out/camp-out" --jobs 1 --only \
listener-parked-outside-groups,listener-settle-skips-leave-copies,listener-merge-keeps-park,\
listener-retire-skips-group-mark,listener-park-drops-matcher-pairs,listener-settle-compare-dropped,\
rv-repark-overwrites-pairs,rv-both-parked-grouped,rv-leave-compare-copy-unwritten,\
rv-take-forgets-walk-mark,rv-parked-uses-matcher-pairs > "$out/camp.log" 2>&1; echo $? > "$out/camp.rc" )
grep -h -E "^PROBE|checks:" "$out/s2.log" "$out/repark.log" "$out/repark-mut.log"
grep -E "^(control|listener|rv-|[0-9]+ checks)" "$out/camp.log"
