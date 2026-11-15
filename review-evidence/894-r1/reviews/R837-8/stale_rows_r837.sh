#!/bin/sh
# Reviewer's grep of every superseded 1x1/1if row figure from section 13's rows-history table (rows before the head's
# 950 us row), outside table lines, in section 13, FR_NFR, READMEs and source comments. Run from the repository root.
toks='12\.85 28\.44 26\.83 26\.95 14\.51 72\.91 68\.80 126\.46 29\.86 48\.09 188\.39 12\.93 28\.64 27\.01 27\.13 14\.56 73\.39 69\.24 127\.22 33\.01 48\.23 188\.41 13\.01 28\.80 27\.17 27\.29 14\.59 73\.80 69\.60 127\.86 33\.21 13\.05 188\.43 28\.90 27\.25 27\.37 14\.61 74\.02 69\.81 132\.71 33\.33 48\.38'
for t in $toks; do
  git grep -nP "(?<![0-9.])$t(?![0-9])" -- docs/design/SPLIT_CONTROL_MEMORY.md docs/reference/FR_NFR.md docs/design/MAILBOX_SPLIT.md '*README*' '*.c' '*.h' '*.py' '*.cpp' | grep -v ':|' | awk -F: -v t="$t" '{print t"\t"$1":"$2}'
done
