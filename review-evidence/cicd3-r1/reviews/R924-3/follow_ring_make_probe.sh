#!/bin/sh
# usage: follow_ring_make_probe.sh REPO OUTDIR
# Extracts tb/verilator/follow_ring (with hdl and the shape headers) at the pre-delta head
# 13e6d869 and at b0f2bc1a into OUTDIR, then (1) compares `make -n run`, and (2) runs
# `make -j4 --jobserver-style=pipe small-pullin` with VERILATOR=true (no model is built; the
# small_pulls step then fails on the missing model, which is expected) and greps for make's
# jobserver warning. The pipe style is GNU make 4.3's only jobserver and 4.4's optional one.
set -u
repo=$1; out=$2; mkdir -p "$out"
for v in ${PROBE_REVS:-base:13e6d869d8 head:b0f2bc1a78}; do
  n=${v%%:*}; c=${v#*:}; d="$out/fr-$n"; rm -rf "$d"; mkdir -p "$d"
  git -C "$repo" archive "$c" hdl configs/generated/endstation_ax7101_1x1_tdm8 tb/verilator/follow_ring | tar -x -C "$d"
  (cd "$d/tb/verilator/follow_ring" && make -n run 2>&1 | sed "s#$d#ROOT#g") > "$out/make-n-run.$n.txt"
  (cd "$d/tb/verilator/follow_ring" && rm -rf obj_dir_fine && make -j4 --jobserver-style=pipe small-pullin VERILATOR=true SWEEP_JOBS=1 2>&1 | sed "s#$d#ROOT#g") > "$out/small-pullin-pipe.$n.txt"
  printf '%s: jobserver warnings: %s\n' "$n" "$(grep -c 'jobserver unavailable' "$out/small-pullin-pipe.$n.txt")"
done
if cmp -s "$out/make-n-run.base.txt" "$out/make-n-run.head.txt"; then echo "make -n run: IDENTICAL"; else echo "make -n run: DIFFERS"; diff "$out/make-n-run.base.txt" "$out/make-n-run.head.txt" | cut -c1-160 | head -12; fi
