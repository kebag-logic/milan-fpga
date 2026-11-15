#!/bin/sh
# Reviewer's own grep of the round-12/13 moved figures at the checked-out head.
# Usage: run from the repository root; prints file:line:token for each hit.
for t in '\b725\b' '33\.01' '\b900 ?us' '900-us' '0\.515' '0\.511' '0\.513' '13\.05' '132\.71' '127\.86' '48\.23' '48\.38' '33\.21' '33\.33' '28\.80' '28\.90' '125\.84' '\b0\.509\b'; do
  git grep -nP "$t" -- docs/design/SPLIT_CONTROL_MEMORY.md docs/reference/FR_NFR.md '*README*' '*.c' '*.h' '*.cpp' '*.hpp' '*.py' '*.sv' '*.svh' '*.v' '*.yml' '*.md' | awk -v t="$t" -F: '{print t"\t"$1":"$2}'
done
