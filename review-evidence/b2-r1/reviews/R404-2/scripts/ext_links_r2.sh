#!/usr/bin/env bash
# Resolve each external GitHub link on the three pages through the read-only API.
# Usage: ext_links_r2.sh <file of URLs>
while read -r u; do
  case "$u" in
    *issuecomment-*) repo=$(echo "$u" | sed -E 's#https://github.com/([^/]+/[^/]+)/.*#\1#'); id=${u##*issuecomment-}
       r=$(gh api "repos/$repo/issues/comments/$id" --jq '.issue_url|split("/")|last' 2>&1) ;;
    */issues/*|*/pull/*) repo=$(echo "$u" | sed -E 's#https://github.com/([^/]+/[^/]+)/.*#\1#'); n=$(echo "$u" | sed -E 's#.*/(issues|pull)/([0-9]+).*#\2#')
       r=$(gh api "repos/$repo/issues/$n" --jq '"#"+(.number|tostring)+" "+.state' 2>&1) ;;
    */blob/*) repo=$(echo "$u" | sed -E 's#https://github.com/([^/]+/[^/]+)/blob/.*#\1#'); ref=$(echo "$u" | sed -E 's#.*/blob/([^/]+)/.*#\1#'); p=$(echo "$u" | sed -E 's#.*/blob/[^/]+/([^#]*).*#\1#')
       r=$(gh api "repos/$repo/contents/$p?ref=$ref" --jq '"blob "+.sha[0:10]' 2>&1) ;;
    *) r="(not checked)";;
  esac
  echo "$u -> $r"
done < "$1"
