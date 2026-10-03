#!/usr/bin/env bash
# Run tb/pp_top mutation campaigns one after another from a source copy at the
# reviewed head. Usage: run_campaigns.sh TREE OUTDIR RECEIPTS JOBS NAME...
# NAME is a driver stem under tb/pp_top (ctr_mutants, aecp_mutants, ...).
# Each campaign writes RECEIPTS/<name>.log and RECEIPTS/<name>.rc.
set -u
tree=$1 out=$2 rec=$3 jobs=$4; shift 4
cd "$tree" || exit 1
for name in "$@"; do
  args=(--output "$out/$name")
  case $name in name_wr_mutant) ;; *) args+=(--jobs "$jobs");; esac
  start=$(date +%s)
  python3 "tb/pp_top/$name.py" "${args[@]}" > "$rec/$name.log" 2>&1
  rc=$?
  echo "$rc" > "$rec/$name.rc"
  echo "$name rc=$rc seconds=$(( $(date +%s) - start ))" >> "$rec/campaign_times.txt"
done
