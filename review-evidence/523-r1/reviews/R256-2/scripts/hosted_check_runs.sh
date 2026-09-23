#!/usr/bin/env bash
# Reviewer receipt: read-only listing of exact-head hosted check runs.
# Usage: hosted_check_runs.sh HEAD_SHA > hosted-check-runs.tsv
set -eu
gh api "repos/kebag-logic/milan-fpga/commits/$1/check-runs?per_page=100" --paginate \
  --jq '.check_runs[] | [.name, .status, (.conclusion // "-"), (.started_at // "-"), (.completed_at // "-")] | @tsv' | sort
