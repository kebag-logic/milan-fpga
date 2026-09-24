#!/usr/bin/env bash
# Read-only listing of hosted check runs at one commit: name, status, conclusion, start, end.
set -eu
sha=${1:-b71061d7fbc1119b02eb430f293672ff8b3f85b8}
gh api "repos/kebag-logic/milan-fpga/commits/$sha/check-runs?per_page=100" \
  --jq '.check_runs[] | "\(.name)\t\(.status)\t\(.conclusion)\t\(.started_at)\t\(.completed_at)"' | sort
