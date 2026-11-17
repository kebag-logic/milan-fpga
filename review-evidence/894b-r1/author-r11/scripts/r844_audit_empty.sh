#!/bin/bash
# R844-1's source_comment_audit.py (published on 894-review-evidence, reviews/R844-1) over this checkout: it prints each
# added comment, docstring or check-description line of 7398ec0a..HEAD that shows an issue-comment ID. Prints its
# lines and their count; exits 1 when it printed any. usage: r844_audit_empty.sh AUDIT_SCRIPT (from the checkout)
set -u
out=$(python3 -I "$1" "$PWD") || { echo "the audit exited $?"; exit 2; }
n=$(printf '%s' "$out" | grep -c .)
echo "R844-1 source_comment_audit.py over $(git rev-parse HEAD): $n line(s)"
[ -n "$out" ] && printf '%s\n' "$out"
[ "$n" = 0 ]
