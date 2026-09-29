#!/usr/bin/env bash
# P10: attribute every path that differs between the R368-4 head (1f039cfe) and
# this head: equal to dev b5c0f69d's copy (came from dev), or otherwise named.
# Also: every path that differs between dev and this head must equal the
# R368-4 head's copy (the lane's reviewed content) or be one of the delta's own edits.
set -u
PREV=1f039cfe86d5337f5c9b7248696dba1c4bdda67e; DEV=b5c0f69d5d11f0ec4bc847a2cfdd13e89e199a8a
HEAD_=4c2a30debb031595b81c5c4bfc53b601a0fec528
oid() { git rev-parse -q --verify "$1:$2" 2>/dev/null || echo absent; }
echo "== paths differing PREV..HEAD"
git diff --name-only $PREV $HEAD_ | while read -r p; do
  h=$(oid $HEAD_ "$p"); d=$(oid $DEV "$p")
  if [ "$h" = "$d" ]; then echo "from-dev   $p"; else echo "NOT-DEV    $p"; fi
done
echo "== paths differing DEV..HEAD"
git diff --name-only $DEV $HEAD_ | while read -r p; do
  h=$(oid $HEAD_ "$p"); q=$(oid $PREV "$p")
  if [ "$h" = "$q" ]; then echo "lane-R368-4 $p"; else echo "CHANGED-IN-DELTA $p"; fi
done
echo "== hdl/, syn/, protocol-processor, sw/firmware, sw/litex changes in the delta beyond dev:"
git diff --name-only $DEV $HEAD_ -- hdl syn protocol-processor gptp-processor sw/firmware sw/litex | while read -r p; do
  [ "$(oid $HEAD_ "$p")" = "$(oid $PREV "$p")" ] || echo "  $p"; done
echo "(end)"
