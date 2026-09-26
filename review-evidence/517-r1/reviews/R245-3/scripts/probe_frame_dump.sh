#!/bin/bash
# Real-leg MILAN_COUNTER_FRAME_OUT probe (#517). usage: probe_frame_dump.sh TREE OUTDIR
# Runs the ten non-aclk ordinary legs (a) directly, one after another in recipe
# order, and (b) through sim_pool.py --jobs=2 with the same argv, each with the
# variable naming a fresh file. Records exit codes, the final file hash, the
# runner's note, and 0.2 s samples of live legs in the suite directory.
set -u
TREE=$1 OUT=$2; mkdir -p "$OUT"; cd "$TREE/tb/verilator/milan_dp" || exit 90
LEGS="./obj_dir/Vmilan_dp_sim ./obj_notify/Vmilan_dp_notify ./obj_crflic/Vmilan_dp_crflic ./obj_nxn/Vmilan_dp_nxn ./obj_nxndv/Vmilan_dp_nxndv ./obj_nxn8/Vmilan_dp_nxn8 ./obj_nxn4c/Vmilan_dp_nxn4c ./obj_nolpf/Vmilan_dp_nolpf ./obj_prune/Vmilan_dp_prune ./obj_ax1x1/Vmilan_dp_ax1x1"
sample() { while :; do n=0; for p in $(pgrep -f '^\./obj_[a-z0-9]+/Vmilan_dp_'); do c=$(readlink /proc/$p/cwd 2>/dev/null); [ "$c" = "$PWD" ] && n=$((n+1)); done; echo "$n"; sleep 0.2; done; }
# (a) direct sequential
sample > "$OUT/seq-samples.txt" & S=$!
rc=0; for l in $LEGS; do MILAN_COUNTER_FRAME_OUT="$OUT/frame-seq.bin" taskset -c 0-5 $l > "$OUT/seq-$(basename $l).log" 2>&1 || { rc=$?; echo "FAIL $l $rc"; break; }; done
kill $S; echo "seq_exit=$rc" > "$OUT/summary.txt"
# (b) pool with the variable present
sample > "$OUT/pool-samples.txt" & S=$!
MILAN_COUNTER_FRAME_OUT="$OUT/frame-pool.bin" taskset -c 0-5 python3 sim_pool.py --jobs=2 \
  $(for l in $LEGS; do case $l in *notify*|*/obj_nxn/*|*nxndv*|*nxn8*|*nxn4c*) printf -- '--exclusive %s ' $l;; *) printf '%s ' $l;; esac; done) > "$OUT/pool.out" 2>&1
prc=$?; kill $S
{ echo "pool_exit=$prc"; echo "frame_seq=$(sha256sum < "$OUT/frame-seq.bin" 2>/dev/null | cut -c1-64) bytes=$(stat -c %s "$OUT/frame-seq.bin" 2>/dev/null)";
  echo "frame_pool=$(sha256sum < "$OUT/frame-pool.bin" 2>/dev/null | cut -c1-64) bytes=$(stat -c %s "$OUT/frame-pool.bin" 2>/dev/null)";
  echo "max_live_seq=$(sort -n "$OUT/seq-samples.txt" | tail -1) max_live_pool=$(sort -n "$OUT/pool-samples.txt" | tail -1)";
  echo "pool_note=$(grep -c '^sim_pool: MILAN_COUNTER_FRAME_OUT is set, so the legs run one at a time in recipe order' "$OUT/pool.out")";
  for l in $LEGS; do b=$(basename $l); a=$(sha256sum < "$OUT/seq-$b.log" | cut -c1-16); p=$(ls obj_legs/*-$b.log); q=$(sha256sum < $p | cut -c1-16); echo "leg $b seq=$a pool=$q $([ $a = $q ] && echo IDENTICAL || echo DIFFERENT)"; done; } >> "$OUT/summary.txt"
cat "$OUT/summary.txt"
