#!/usr/bin/env bash
# For every issuecomment link on the pages, confirm (read-only API GET) that
# the comment exists and belongs to the issue the URL names.
# Usage: comment_link_probe.sh <repo> <page>...
set -u
repo=$1; shift
cd "$repo" || exit 2
bad=0; n=0
for url in $(grep -ohE 'https://github.com/[^/]+/[^/]+/(issues|pull)/[0-9]+#issuecomment-[0-9]+' "$@" | sort -u); do
  n=$((n+1))
  slug=$(echo "$url" | sed -E 's#https://github.com/([^/]+/[^/]+)/.*#\1#')
  num=$(echo "$url" | sed -E 's@.*/(issues|pull)/([0-9]+)#.*@\2@')
  cid=${url##*-}
  got=$(gh api "repos/$slug/issues/comments/$cid" --jq '.issue_url' 2>/dev/null | sed -E 's#.*/##')
  if [ "$got" = "$num" ]; then echo "OK   $url"; else echo "BAD  $url (comment belongs to: ${got:-missing})"; bad=$((bad+1)); fi
done
echo "comment links checked=$n bad=$bad"
exit $bad
