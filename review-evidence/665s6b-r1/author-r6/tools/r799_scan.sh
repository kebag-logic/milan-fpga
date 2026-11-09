#!/bin/sh
# r799_scan.sh REPO BASE HEAD : R799-1's comment-rule list (receipts/residue_source_lines.txt) re-derived. R799-1
# published the list, not its scan; this is R800-1's comment_rule_scan.sh with one change, `issuecomment-` matched
# with or without digits after it (a comment ID broken over two lines), which reproduces R799-1's 43 lines exactly
# at e69d243a. Prints path:line: text for each added line outside *.md that names an issue comment, a ruling by
# its comment ID, or a lane label (S2b, S6a, S6b, S11, S12, S13).
git -C "$1" --no-pager diff --no-color -U0 "$2..$3" -- . ':(exclude)*.md' | awk '
/^\+\+\+ b\//{f=substr($2,3)} /^@@/{split($3,a,","); n=substr(a[1],2)+0; next}
/^\+/{ if ($0 ~ /issuecomment-|ruling [0-9][0-9][0-9][0-9][0-9][0-9]+|(^|[^A-Za-z0-9])S(2b|6a|6b|11|12|13)([^A-Za-z0-9]|$)/) print f":"n": "substr($0,2,150); n++; next}
/^ /{n++}'
