#!/usr/bin/env bash
# #787 round 4: #70's dynmap-mutants campaign alone at <rev>, in the campaigns clone, after the first start was stopped
# by hand for memory (the unit reached 14.9 GB beside rtl-fast's publication census). The make target as TESTING.md
# names it; MAKEFLAGS=-j4 for the three prerequisite legs.
# usage: dynmap_run.sh <rev>
set -u
rev=$1; X=$VALIDATION_STORAGE/787-a700e; C=$X/clone-campaigns-${rev:0:8}; O=$X/r/campaigns-${rev:0:8}; D=$(cd "$(dirname "$0")" && pwd)
cd "$C" || exit 2
[ "$(git rev-parse HEAD)" = "$rev" ] || exit 2
source "$D/env.sh"; source "$D/fw_env.sh"; export VERILATOR_JOBS=4 MAKEFLAGS=-j4
s=$(date +%s)
make -C tb/verilator/milan_dp dynmap-mutants DYNMAP_MUTANT_JOBS=4 > "$O/dynmap_mutants-rerun.log" 2>&1; rc=$?
echo "$rc $(( $(date +%s)-s ))s dynmap_mutants-rerun: make -C tb/verilator/milan_dp dynmap-mutants DYNMAP_MUTANT_JOBS=4" >> "$O/table-dynmap.txt"
git status --porcelain --untracked-files=no > "$O/clone-status-after-dynmap.txt"
echo DYNMAP-DONE >> "$O/table-dynmap.txt"
