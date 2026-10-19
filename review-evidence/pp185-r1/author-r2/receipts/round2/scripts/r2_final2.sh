#!/usr/bin/env bash
# round 2, final head after the bench split: every processor gate, then the notify
# campaign (the one campaign that builds tb/aecp_notify), serially, through gate.sh
S=<data>/tmp/pp185-a647; T=<data>/lanes/pp185-ctl; F="$S/r2/rec/head-final2"
"$S/scripts/proc_gates.sh" "$T" "$F/gates"
"$S/scripts/campaigns2.sh" "$T" "$F/campaigns" notify
echo ALL-DONE > "$F/final2.done"
