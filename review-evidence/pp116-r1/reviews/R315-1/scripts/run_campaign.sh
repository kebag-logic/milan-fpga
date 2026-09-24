#!/bin/sh
# Run one of the three processor mutation campaigns touched by PR #117 in a
# disposable processor checkout, recording rc and wall seconds.
#   usage: run_campaign.sh <pp-checkout> <label> <desc|srp|gsi> <outdir> <verilator-dir>
# <verilator-dir> holds a `verilator` for PATH (the pinned 5.050 wrapper).
# The campaigns pin or cap their own build parallelism at <= 8 jobs.
set -u
tree=$1; label=$2; which=$3; out=$4; vdir=$5
mkdir -p "$out"
PATH="$vdir:$PATH"; export PATH
cd "$tree" || exit 2
case $which in
  desc) cmd="python3 tb/desc_mem_guard/mutate.py --output $out/$label-desc" ;;
  srp)  cmd="python3 tb/srp_admission/mutants.py --output $out/$label-srp" ;;
  gsi)  cmd="python3 tb/pp_top/gsi_mutants.py --output $out/$label-gsi --verilator $vdir/verilator" ;;
  *) echo "unknown campaign $which"; exit 2 ;;
esac
start=$(date +%s)
$cmd > "$out/$label-$which.stdout" 2>&1
rc=$?
end=$(date +%s)
echo "tree=$(git rev-parse HEAD) campaign=$which rc=$rc seconds=$((end - start)) verilator=$(verilator --version)" \
  | tee "$out/$label-$which.status"
