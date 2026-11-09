#!/usr/bin/env bash
# run_escalate.sh JOBS: the probes of probes/escalate.tsv against every other srp_top group
PKT=${PKT:-$(cd "$(dirname "$0")/.." && pwd)}; export PKT
export PROBE_GROUPS="armdelay phases edge peer congestion guards restart timers lvleave lvcoll share link"
tr '\t' '\037' < "$PKT/probes/escalate.tsv" | xargs -d '\n' -P "${1:-3}" -I{} bash -c 'IFS=$'"'"'\037'"'"' read -r n f l o w <<< "$1"; "$PKT/scripts/probe.sh" "$n" "$f" "$l" "$o" "$w"' _ {}
