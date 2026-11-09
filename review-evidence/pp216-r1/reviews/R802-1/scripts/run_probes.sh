#!/usr/bin/env bash
# run_probes.sh [JOBS]: every row of probes/probes.tsv through probe.sh, JOBS at once
PKT=${PKT:-$(cd "$(dirname "$0")/.." && pwd)}; export PKT
J=${1:-4}
tr '\t' '\037' < "$PKT/probes/probes.tsv" | xargs -d '\n' -P "$J" -I{} bash -c 'IFS=$'"'"'\037'"'"' read -r n f l o w <<< "$1"; "$PKT/scripts/probe.sh" "$n" "$f" "$l" "$o" "$w"' _ {}
