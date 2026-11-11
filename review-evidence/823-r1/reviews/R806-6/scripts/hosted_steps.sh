#!/bin/sh
# Usage: hosted_steps.sh <out.tsv> <run-id>...
# Every job step of each workflow run, one TSV row per step:
# run, job, job conclusion, job head, step number, step name, step conclusion.
# Pages of 10 jobs are fetched one by one, each retried up to five times.
out=$1; shift
: > "$out"
for id in "$@"; do
  page=1
  while :; do
    ok=
    for try in 1 2 3 4 5; do
      body=$(gh api "repos/kebag-logic/milan-fpga/actions/runs/$id/jobs?per_page=10&page=$page" 2>/dev/null) && ok=1 && break
      sleep 4
    done
    [ -n "$ok" ] || { echo "FETCH-FAILED run $id page $page" >&2; exit 1; }
    n=$(printf '%s' "$body" | jq '.jobs | length')
    [ "$n" -gt 0 ] || break
    printf '%s' "$body" | jq -r --arg id "$id" '.jobs[] | . as $j | .steps[] |
      [$id, $j.name, $j.conclusion, $j.head_sha[:8], .number, .name, .conclusion] | @tsv' >> "$out"
    page=$((page + 1))
  done
  printf '%s' "$body" | jq -r '"run total_count \(.total_count)"' >&2
done
