#!/usr/bin/env bash
# capture_coherence again, uncontended: the suite's default target exactly as
# scripts/run_all_suites.sh invokes it (make -C tb/verilator/capture_coherence),
# on the two CPUs and with the job knobs the sweep gives its shard, without the
# runner's wall clock, then graded by the runner's own tally (suite_tally.py).
# usage: cc_rerun.sh <clone> <out>
set -u
repo=$1; out=$2
export PATH=$VALIDATION_STORAGE/scratch/632-a659/r3/bin:$VALIDATION_STORAGE/scratch/632-a659/r2/venv31213/bin:$PATH
export TSN_GEN_ROOT=$VALIDATION_STORAGE/scratch/632-a659/tsn-gen
export VERILATOR_JOBS=2 START_JOBS=2 SIM_JOBS=2 JOBS=2 POOL=2 CENSUS_JOBS=2
mkdir -p "$out"
cd "$repo" || exit 2
git rev-parse HEAD > "$out/HEAD.txt"
mapfile -t own < <(python3 -c 'import os; print(*sorted(os.sched_getaffinity(0)), sep="\n")')
cpus="${own[6]}-${own[7]}"
echo "taskset -c <2 CPUs> make -C tb/verilator/capture_coherence" > "$out/command.txt"
date -Is > "$out/start"
taskset -c "$cpus" make -C tb/verilator/capture_coherence > "$out/capture_coherence.log" 2>&1
echo $? > "$out/rc"
date -Is > "$out/end"
python3 scripts/suite_tally.py --verdict "$out/capture_coherence.log" > "$out/tally.txt" 2>&1
echo $? >> "$out/tally.txt"
