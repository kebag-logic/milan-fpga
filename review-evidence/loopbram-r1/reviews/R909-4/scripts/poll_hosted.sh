#!/usr/bin/env bash
# Read-only poll of hosted workflow runs for one commit, for at most N seconds.
# Usage: poll_hosted.sh <owner/repo> <sha> <max-seconds> <out-file>
# Stops early once every run for the commit has completed. Writes the run table
# and the check-run conclusions to <out-file>.
set -u
repo=$1; sha=$2; max=$3; out=$4
end=$(( $(date +%s) + max ))
while :; do
  runs=$(gh api "repos/$repo/actions/runs?head_sha=$sha&per_page=50" \
         --jq '.workflow_runs[] | "\(.id) \(.name) \(.event) \(.status) \(.conclusion)"')
  pending=$(printf '%s\n' "$runs" | awk '$4 != "completed"' | wc -l)
  [ "$pending" -eq 0 ] || [ "$(date +%s)" -ge "$end" ] && break
  sleep 60
done
{
  echo "polled_at $(date -u +%FT%TZ) sha $sha"
  printf '%s\n' "$runs"
  echo "--- check runs (conclusion or status, name)"
  gh api "repos/$repo/commits/$sha/check-runs?per_page=100" --paginate \
     --jq '.check_runs[] | "\(.conclusion // .status)\t\(.name)\t\(.id)"' | sort
} > "$out"
cat "$out" | awk -F'\t' 'NR<8 || $1 != "success"' | head -80
echo "success count: $(grep -c '^success' "$out")"
