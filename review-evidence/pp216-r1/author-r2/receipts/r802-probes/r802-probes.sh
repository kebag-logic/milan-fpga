#!/usr/bin/env bash
# r802-probes.sh <tree> <probes-dir> <out>: apply each of the second review's three surviving Applicant probes
# (its patch files as published, unchanged) to a scratch copy of <tree>, run tb/srp_encoder, and keep the log;
# then apply its link-bounce testbench probe (patch -p1, which takes the moved lines of sim_main.cpp) and run
# its r802link group of tb/srp_top. Each run's rc is in <out>/<name>.rc.
set -u
tree=$(cd "$1" && pwd); pd=$(cd "$2" && pwd); out=$3; mkdir -p "$out"; out=$(cd "$out" && pwd)
for p in p09-note4-inverted p12-txla-vp-stays p19-txla-vp-sends-sj; do
  w=$(mktemp -d); mkdir -p "$w/tb"; cp -r "$tree/hdl" "$w/"; for n in common srp_encoder; do rsync -a --exclude 'obj_*' "$tree/tb/$n" "$w/tb/"; done
  (cd "$w" && git apply "$pd/$p.patch" && make -C tb/srp_encoder) > "$out/$p.srp_encoder.log" 2>&1; echo $? > "$out/$p.rc"
  rm -rf "$w"
done
w=$(mktemp -d); mkdir -p "$w/tb"; cp -r "$tree/hdl" "$w/"; for n in common srp_top; do rsync -a --exclude 'obj_*' "$tree/tb/$n" "$w/tb/"; done
(cd "$w" && patch -p1 < "$pd/r802-link-bounce.tb.patch" && make -C tb/srp_top run RUN_ARGS=r802link) > "$out/r802-link-bounce.log" 2>&1; echo $? > "$out/r802-link-bounce.rc"
rm -rf "$w"
