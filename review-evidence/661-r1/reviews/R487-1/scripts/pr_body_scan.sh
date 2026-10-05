#!/usr/bin/env bash
# Fetch the live PR body and head, and scan the body for host paths, account names, privilege commands,
# stale "local branch" wording and the top-port figure.
# Usage: pr_body_scan.sh <owner/repo> <pr>
set -u
gh pr view "$2" -R "$1" --json headRefOid,updatedAt --jq '"head " + .headRefOid + " updated " + .updatedAt'
body=$(gh pr view "$2" -R "$1" --json body --jq .body)
echo "body sha256 $(printf '%s' "$body" | sha256sum | cut -c1-64)"
for pat in '/data/' '/home/' '/tmp/' 'sudo' ' -u [a-z]' 'is local' 'not been pushed' 'ports are unchanged'; do
  n=$(printf '%s\n' "$body" | grep -c -- "$pat"); echo "pattern '$pat': $n line(s)"
  [ "$pat" = 'ports are unchanged' ] && printf '%s\n' "$body" | grep -- "$pat" | sed 's/^/   /'
done
