#!/usr/bin/env bash
# gsi_mutants.py, every mutant, on the clean notify build notify.sh made in the
# same clone (the campaign re-runs that clean leg first).
# usage: gsi.sh <clone> <out>
set -u
here=$(cd "$(dirname "$0")" && pwd)
source "$here/env.sh"
export TSN_GEN_ROOT=$VALIDATION_STORAGE/scratch/632-a659/tsn-gen
C=$1; O=$2; mkdir -p "$O"
cd "$C/tb/verilator/milan_dp" || exit 2
git rev-parse HEAD > "$O/HEAD.txt"
date -Is > "$O/start"
python3 gsi_mutants.py > "$O/gsi_mutants.log" 2>&1
echo $? > "$O/rc"
date -Is > "$O/end"
