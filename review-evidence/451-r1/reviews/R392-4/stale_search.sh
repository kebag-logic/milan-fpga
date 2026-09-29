#!/bin/sh
# Usage: stale_search.sh REV  -- pattern families over tracked first-party text at REV,
# excluding docs/history, the #451 page and submodules. Prints family, path:line.
REV=$1
for fam in \
  'render-status:not clocked on any shipping build|no physical TDM|not physical TDM render|capture, not physical|TDM render(ing)? (is|remains) (unclocked|untested|unvalidated)|render serializer had no' \
  'first-light:first light|first-light|#451|issues/451' \
  'bench-link:PocketBeagle|McASP|J11 header|TDM8 link|serial-audio validation|#448\b' \
  'din-coherence:DIN frame|frame coherence|#617|issues/617' \
  'slip-rate:SLIP_TDM|10\.64 ppm|-10\.64|47,999' \
  'tdm-hw:TDM (on|in) (silicon|hardware)|physical TDM|TDM8 .*(silicon|hardware|bench)'
do
  name=${fam%%:*}; pat=${fam#*:}
  git grep -n -I -E -i "$pat" "$REV" -- . ':!docs/history' ':!docs/findings/451_TDM8_FIRST_LIGHT.md' \
    ':!protocol-processor' ':!gptp-processor' ':!external' ':!third_party' \
    | sed "s/^$REV:/$name\t/"
done
