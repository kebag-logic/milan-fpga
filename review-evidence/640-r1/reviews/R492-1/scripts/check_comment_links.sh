#!/usr/bin/env bash
# For every issue-comment URL a diff adds, confirm the comment exists on the issue the URL names (read-only API).
# Usage: check_comment_links.sh <repo> <base> <head>
cd "$1" || exit 2
git diff "$2" "$3" | grep '^+' | grep -oE 'https://github.com/kebag-logic/milan-fpga/(issues|pull)/[0-9]+#issuecomment-[0-9]+' | sort -u |
while read -r u; do
  id=${u##*-}; num=$(printf '%s' "$u" | sed -E 's|.*/(issues\|pull)/([0-9]+)#.*|\2|')
  got=$(gh api "repos/kebag-logic/milan-fpga/issues/comments/$id" --jq '.issue_url' 2>/dev/null | sed 's|.*/||')
  if [ "$got" = "$num" ]; then echo "OK $u"; else echo "FAIL $u (comment on issue '$got')"; fi
done
