#!/usr/bin/env bash
# usage: run_r679_2_probes_only.sh <revision> <out dir>: the probe half of
# R679-2's run_reviewer_probes.sh (s2, repark, repark-mut), the same steps in
# the same order, one build at a time; the control campaign half is not run
set -u
S=<scratch>/r3
. $S/scripts/env.sh
here=$S/probes/r679-2
clone=<lane>; rev=$1; out=$2
rm -rf "$out"; mkdir -p "$out"
export_to() { rm -rf "$1"; mkdir -p "$1"; git -C "$clone" archive "$rev" | tar -x -C "$1"; }
export_to "$out/s2"; export_to "$out/repark"; export_to "$out/repark-mut"
python3 -I "$here/s2_probe.py" "$out/s2/tb/srp_stream_fsms/sim_main.cpp"
python3 -I "$here/repark_probe.py" "$out/repark/tb/srp_stream_fsms/sim_main.cpp"
(cd "$out/repark-mut" && patch -s -p1 < "$here/rv-repark-overwrites-pairs.patch")
python3 -I "$here/repark_probe.py" "$out/repark-mut/tb/srp_stream_fsms/sim_main.cpp"
for n in s2 repark repark-mut; do
  ( cd "$out/$n/tb/srp_stream_fsms" && make RUN_ARGS=suite > "$out/$n.log" 2>&1; echo $? > "$out/$n.rc" )
done
grep -h -E "^PROBE|checks:" "$out/s2.log" "$out/repark.log" "$out/repark-mut.log" > "$out/summary.txt"
echo done > "$out/DONE"
