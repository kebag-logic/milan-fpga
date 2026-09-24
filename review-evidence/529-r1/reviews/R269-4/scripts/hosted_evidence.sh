#!/usr/bin/env bash
# Read-only record of the hosted evidence relevant to a merge-train candidate
# tree: the PR head's check runs (executed vs skipped), GitHub's pull-request
# test merge commit and its tree, and, for each job listed, the commit the job
# checked out and the per-suite verdict lines it printed. Nothing is written
# to GitHub. Requires an authenticated `gh`.
# Usage: hosted_evidence.sh <owner/repo> <pr-head-sha> <test-merge-sha> <job-id>...
set -euo pipefail
repo=$1 head=$2 tmerge=$3; shift 3
echo "## check runs on PR head $head (name, status, conclusion)"
gh api "repos/$repo/commits/$head/check-runs?per_page=100" \
  --jq '.check_runs[] | [.name, .status, (.conclusion // "-")] | @tsv' | sort
echo
echo "## GitHub test merge $tmerge"
gh api "repos/$repo/git/commits/$tmerge" --jq '"tree " + .tree.sha, "parents " + ([.parents[].sha]|join(" ")), "date " + .committer.date, "message " + .message'
echo
for job in "$@"; do
  log=$(mktemp)
  gh api --allow-escape-sequences "repos/$repo/actions/jobs/$job/logs" > "$log"
  name=$(gh api "repos/$repo/actions/jobs/$job" --jq '.name + " (" + .conclusion + ")"')
  echo "## job $job: $name"
  grep -a -m1 -oE 'HEAD is now at [0-9a-f]+' "$log" || echo "no checkout line"
  sed 's/\x1b\[[0-9;]*m//g' "$log" | grep -a -E '^[0-9TZ:.-]+ (PASS|FAIL|SKIP|TIMEOUT) +[a-z_0-9]+' | cut -c30- || true
  rm -f "$log"
done
