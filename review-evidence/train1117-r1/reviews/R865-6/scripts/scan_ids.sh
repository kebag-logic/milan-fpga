#!/bin/sh
# Scan the added lines of BASE..HEAD in non-markdown, non-svg/png/drawio files for
# issue-comment / review / reviewer-finding IDs and session labels.
# Usage: scan_ids.sh <repo> <base> <head>   ; prints hits, rc 1 if any.
set -eu
repo=$1 base=$2 head=$3
cd "$repo"
git diff --name-only "$base" "$head" | grep -vE '\.(md|svg|png|drawio)$' > /tmp/scan_ids.$$ || true
pat='issuecomment|pullrequestreview|discussion_r[0-9]|#issue-[0-9]|\bR[0-9]{3,4}-[0-9]+(-[A-Za-z]*[0-9]+)?\b|\bR[0-9]{3,4}-[0-9]+\b|\[[AR][0-9]+(-[ab])?\]|\b[AR][0-9]{3,4}\b|author-r[0-9]|-F[0-9]+\b'
hits=0
while IFS= read -r f; do
  git diff -U0 "$base" "$head" -- "$f" | grep -E '^\+' | grep -vE '^\+\+\+' | grep -nE "$pat" | sed "s|^|$f: |" && hits=1 || true
done < /tmp/scan_ids.$$
rm -f /tmp/scan_ids.$$
exit $hits
