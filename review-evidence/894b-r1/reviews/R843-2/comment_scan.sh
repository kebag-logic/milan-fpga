#!/bin/bash
# Added non-Markdown, non-docs lines of BASE..HEAD showing an issue-comment ID, a review round, a reviewer/author ID or a
# lane label. usage (from the checkout): comment_scan.sh BASE HEAD
git -c core.pager=cat diff "$1..$2" -- . ':!docs' ':!*.md' | grep '^+' | grep -v '^+++' |
  grep -nE "issuecomment|[Rr]ound [0-9]+|round-[0-9]|\bR[0-9]{3}\b|\[A[0-9]|\[R[0-9]|\blane\b|\bB[0-9]{1,2}\b|894b|reviewer"
echo "matches: $(git -c core.pager=cat diff "$1..$2" -- . ':!docs' ':!*.md' | grep '^+' | grep -v '^+++' | grep -cE "issuecomment|[Rr]ound [0-9]+|round-[0-9]|\bR[0-9]{3}\b|\[A[0-9]|\[R[0-9]|\blane\b|\bB[0-9]{1,2}\b|894b|reviewer")"
