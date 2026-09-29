#!/bin/sh
# Usage: prior_findings_at_head.sh REV  -- re-checks the anchors of prior public findings at REV
R=${1:?rev}; P=docs/findings/451_TDM8_FIRST_LIGHT.md; I=docs/findings/README.md
s(){ git show "$R:$1"; }
echo "page blob: $(git rev-parse $R:$P) (R392-3 reviewed cb7dd0aa...)"
echo "-- #617 links in page (R392-1 F2 = R393-1 F1):"; s $P | grep -n 'issues/617' | cut -d: -f1 | tr '\n' ' '; echo
echo "-- #617 link in index row (R393-1 F2, R392-1 F2):"; s $I | grep -c '451_TDM8_FIRST_LIGHT.md.*issues/617'
echo "-- owner report 5872564358 cites (R393-1 F3):"; s $P | grep -n '5872564358' | cut -d: -f1 | tr '\n' ' '; echo
echo "-- seven conductors (R393-1 F3):"; s $P | grep -n -i 'seven conductors' | cut -c1-80
echo "-- removed idle-high claim absent (R392-1 F1):"; s $P | grep -c -i 'could not have come from the pin'
echo "-- line 3 session identity (R393-2 S8, retained):"; s $P | sed -n 3p
echo "-- index State wording (R393-2 S7, R392-2 S2, retained):"; s $I | grep '451_TDM8' | awk -F'|' '{print $4}'
echo "-- CLOCK_DOMAINS:140 cites #617? (R392-3 S2, retained):"; s docs/litex/CLOCK_DOMAINS.md | sed -n 140p | grep -c 617
echo "-- scripts/ subtree changed since R392-3's head (R392-3 S1 gate blind spots):"; [ "$(git rev-parse $R:scripts)" = "$(git rev-parse 0e5ae9c82bbdb5abc3feba84f07d0e6481254906:scripts)" ] && echo unchanged || git diff --stat 0e5ae9c82bbdb5abc3feba84f07d0e6481254906 $R -- scripts
