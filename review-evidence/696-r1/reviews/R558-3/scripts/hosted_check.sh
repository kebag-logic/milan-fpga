#!/bin/sh
# Usage: hosted_check.sh <outdir> <head-sha>
# Read-only: records every workflow run and job conclusion at <head-sha>, and the
# maap lines of the Verilator shard 1/5 log once that job has completed.
set -u
OUT=$1; SHA=$2; R=kebag-logic/milan-fpga
{
  echo "queried=$(date -u +%FT%TZ) head=$SHA"
  gh api "repos/$R/actions/runs?head_sha=$SHA&per_page=50" \
    --jq '.workflow_runs[] | [.id,.name,.event,.status,(.conclusion//"-"),.run_attempt,.head_sha] | @tsv'
  for run in $(gh api "repos/$R/actions/runs?head_sha=$SHA&per_page=50" --jq '.workflow_runs[].id'); do
    gh api "repos/$R/actions/runs/$run/jobs?per_page=100" \
      --jq ".jobs[] | [\"$run\",.id,.name,.status,(.conclusion//\"-\"),(.started_at//\"-\"),(.completed_at//\"-\")] | @tsv"
  done
} > "$OUT/hosted-status.tsv"
job=$(awk -F'\t' '$3=="Verilator shard 1/5"{print $2}' "$OUT/hosted-status.tsv" | head -1)
st=$(awk -F'\t' '$3=="Verilator shard 1/5"{print $4}' "$OUT/hosted-status.tsv" | head -1)
if [ -n "$job" ] && [ "$st" = completed ]; then
  gh run view --repo "$R" --job "$job" --log 2>/dev/null \
    | grep -E 'shard: 1/5|PASS +maap|FAIL +maap|PASS |FAIL |suites: |checks: |failing suites|TIMEOUT' \
    > "$OUT/hosted-shard1-summary.log"
fi
cat "$OUT/hosted-status.tsv" | grep -E 'Verilator shard 1/5|rtl-full|rtl-fast|docs|elaborate'
