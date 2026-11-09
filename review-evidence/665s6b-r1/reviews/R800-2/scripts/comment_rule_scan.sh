#!/bin/sh
# comment_rule_scan.sh REPO BASE HEAD : every added line outside *.md in BASE..HEAD that names an issue comment
# (issuecomment-N), a ruling by its comment ID (ruling N), or a lane label (S2b, S6a, S6b, S11, S12, S13), as
# path:line: text, the line number in HEAD.
git -C "$1" --no-pager diff --no-color -U0 "$2..$3" -- . ':(exclude)*.md' | awk '
/^\+\+\+ b\//{f=substr($2,3)} /^@@/{split($3,a,","); n=substr(a[1],2)+0; next}
/^\+/{ if ($0 ~ /issuecomment-[0-9]+|ruling [0-9][0-9][0-9][0-9][0-9][0-9]+|(^|[^A-Za-z0-9])S(2b|6a|6b|11|12|13)([^A-Za-z0-9]|$)/) print f":"n": "substr($0,2,150); n++; next}
/^ /{n++}'
