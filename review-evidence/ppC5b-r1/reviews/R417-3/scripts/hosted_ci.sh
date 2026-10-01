#!/usr/bin/env bash
# Read-only: records every hosted workflow run at the exact head, with each job's and
# step's status, conclusion and times (GitHub REST, GET only). usage: hosted_ci.sh <repo> <sha>
R=$1; SHA=$2; echo "queried (UTC): $(date -u +%FT%TZ)"
for id in $(gh api "repos/$R/actions/runs?head_sha=$SHA&per_page=50" --jq '.workflow_runs[].id'); do
  gh api "repos/$R/actions/runs/$id" --jq '"run \(.id) \(.name) event=\(.event) status=\(.status) conclusion=\(.conclusion) head=\(.head_sha)"'
  gh api "repos/$R/actions/runs/$id/jobs" --jq '.jobs[] | "  job \(.name): \(.status) \(.conclusion) \(.started_at) -> \(.completed_at)", (.steps[] | "    step \(.number) \(.name): \(.status) \(.conclusion) \(.started_at) -> \(.completed_at)")'
done
