#!/usr/bin/env bash
# Round 8: the milan_dp Verilator legs whose source changed, built and run one
# at a time in a clean clone at <rev> (pinned Verilator 5.050, env.sh): the
# gptp leg (sim_gptp.cpp) and the ax1x1gptp leg (sim_ax1x1gptp.cpp), each its
# own make target as the sweep invokes it, with its own log and rc.
# usage: legs.sh <rev>
set -u
rev=$1; h=${rev:0:8}
R7=$MANAGEMENT/2026-09-23/632-a659/scripts/round7
C=$VALIDATION_STORAGE/scratch/632-a659/r8/clone-legs-$h
O=$VALIDATION_STORAGE/scratch/632-a659/r8/legs-$h
mkdir -p "$O"
[ -d "$C" ] || bash "$R7/make_clone.sh" "$C" "$rev" > "$O/clone.log" 2>&1
source "$R7/env.sh"
export TSN_GEN_ROOT=$VALIDATION_STORAGE/scratch/632-a659/tsn-gen
cd "$C/tb/verilator/milan_dp" || exit 2
git rev-parse HEAD > "$O/HEAD.txt"
git status --short > "$O/status.txt"
verilator --version > "$O/verilator.txt" 2>&1
date -Is > "$O/start"
for t in gptp ax1x1gptp; do
  s=$(date +%s)
  printf 'make -C tb/verilator/milan_dp %s VERILATOR_JOBS=2\n' "$t" > "$O/$t.command"
  make --no-print-directory "$t" VERILATOR_JOBS=2 > "$O/$t.log" 2>&1; echo $? > "$O/$t.rc"
  echo "$t rc=$(cat "$O/$t.rc") $(( $(date +%s) - s ))s" >> "$O/summary.txt"
done
date -Is > "$O/end"
