#!/bin/bash
# usage: jobdur.sh RUNID... -> tsv: run workflow job conclusion seconds runner
for r in "$@"; do
  gh api "repos/kebag-logic/milan-fpga/actions/runs/$r/jobs?per_page=100&filter=latest" --paginate \
    -q '.jobs[] | select(.conclusion=="success") | [env.R, .name, .conclusion, ((.completed_at|fromdate)-(.started_at|fromdate)), .runner_name] | @tsv' 2>/dev/null | sed "s/^/$r\t/"
done
