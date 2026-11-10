#!/bin/bash
# Re-run one sweep suite killed by the wall clock, as run_all_suites.sh runs it (timeout BUDGET make -C the suite's
# directory, its log asked by suite_tally.py --verdict), in its shard's clone at the head with the sweep spec's
# environment, on four CPUs (capture_coherence builds one datapath a CPU). usage: cc_rerun.sh SUITE BUDGET_S OUT
set -u
S=$1 TMO=$2 O=$3
T=<scratch>
C=<lanes>/665s2b-a683ze-sweep-shard2
mkdir -p "$O" $T/tmp-cc-rerun
cd "$C" || exit 3
H=$(git rev-parse HEAD)
{ echo "head $H dirty $(git status --porcelain --untracked-files=no | wc -l) suite $S budget ${TMO}s cpus $(nproc) start $(date +%T)"
  echo "cleaned: $(git clean -fdxn tb/verilator/$S | wc -l) generated paths under tb/verilator/$S"; } > "$O/rerun.txt"
git clean -q -fdx "tb/verilator/$S"
export PATH=<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:<data>/scratch/a662/make43/bin:<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export VERILATOR=<tools>/pinned-verilator-5.050/verilator TSN_GEN_ROOT=<management>/tools/tsn-gen-deca300c
export TMPDIR=$T/tmp-cc-rerun MAKEFLAGS="-j4 --no-print-directory"
start=$(date +%s)
timeout "$TMO" make -C "$C/tb/verilator/$S" > "$O/$S.log" 2>&1
rc=$?
echo "make rc=$rc elapsed=$(( $(date +%s) - start ))s end $(date +%T)" >> "$O/rerun.txt"
python3 "$C/scripts/suite_tally.py" --verdict "$O/$S.log" >> "$O/rerun.txt" 2>&1
echo "verdict rc=$?" >> "$O/rerun.txt"
python3 "$C/scripts/suite_tally.py" "$O" >> "$O/rerun.txt" 2>&1
echo "tally rc=$?" >> "$O/rerun.txt"
echo "dirty after $(git status --porcelain --untracked-files=no | wc -l)" >> "$O/rerun.txt"
