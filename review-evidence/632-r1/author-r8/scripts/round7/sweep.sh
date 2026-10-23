#!/usr/bin/env bash
# The full Verilator sweep (scripts/run_all_suites.sh) at the lane head, in a
# clean clone, one shard at a time, with CI's CPython 3.12.3, the pinned
# Verilator 5.050 and tsn-gen at CI's TSN_GEN_REV. At most two Verilator
# builds at once: every suite job knob is capped at 2 through make's ?=, and
# the shard holding capture_coherence (whose mutation arm sizes itself by CPU
# affinity) runs on two CPUs. No nohup: the runner's own preflight sends a
# real HUP to its children and refuses a sweep whose children ignore it.
# usage: sweep.sh <repo> <out> <shard>...
set -u
repo=$1; out=$2; shift 2
export PATH=$VALIDATION_STORAGE/scratch/632-a659/r3/bin:$VALIDATION_STORAGE/scratch/632-a659/r2/venv31213/bin:$PATH
export TSN_GEN_ROOT=$VALIDATION_STORAGE/scratch/632-a659/tsn-gen
export VERILATOR_JOBS=2 START_JOBS=2 SIM_JOBS=2 JOBS=2 POOL=2 CENSUS_JOBS=2
mkdir -p "$out"
cd "$repo"
git rev-parse HEAD > "$out/HEAD.txt"
# the CPUs this session is booked on (its affinity), never another lane's:
# the first six for a shard, the next two for the capture_coherence shard
# (CPU_OFS shifts both, for a second sweep running beside the first)
mapfile -t own < <(python3 -c 'import os; print(*sorted(os.sched_getaffinity(0)), sep="\n")')
ofs=${CPU_OFS:-0}
for i in "$@"; do
  cpus="${own[$ofs]}-${own[$((ofs + 5))]}"
  [ "$i" = 2 ] && cpus="${own[$((ofs + 6))]}-${own[$((ofs + 7))]}"
  date -Is > "$out/shard$i.start"
  taskset -c "$cpus" bash scripts/run_all_suites.sh "$out/shard$i" --shard "$i/4" > "$out/shard$i.summary" 2>&1
  echo $? > "$out/shard$i.rc"
  date -Is > "$out/shard$i.end"
done
echo SWEEP-DONE > "$out/DONE"
