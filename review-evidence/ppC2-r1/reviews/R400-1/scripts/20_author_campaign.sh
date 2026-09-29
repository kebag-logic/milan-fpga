#!/usr/bin/env bash
# Re-run the PR's own `make -C tb/maap mutants` on a pristine export of the head.
# Receipts: receipts/author-campaign/*.log and receipts/author-campaign.log
source "$(dirname "$0")/common.sh"
T=$SCRATCH/campaign
export_tree "$T"
OUT=$RECEIPTS/author-campaign
rm -rf "$OUT"; mkdir -p "$OUT"
set +e
( cd "$T/tb/maap" && TMPDIR=$SCRATCH taskset -c "$CPUSET" make VERILATOR="$VERILATOR" MUTANT_OUTPUT="$OUT" mutants ) \
  >"$RECEIPTS/author-campaign.log" 2>&1
rc=$?
set -e
echo "rc=$rc" >>"$RECEIPTS/author-campaign.log"
grep -E 'control|KILLED|UNPROVEN|checks:|^rc=' "$RECEIPTS/author-campaign.log"
