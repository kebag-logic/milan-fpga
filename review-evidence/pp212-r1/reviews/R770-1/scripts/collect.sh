#!/usr/bin/env bash
# Copy the reviewer's raw receipts from scratch/ into receipts/ and write
# MANIFEST.sha256 (paths relative to the packet root). Usage: collect.sh PACKET
set -euo pipefail
P=$(cd "$1" && pwd); S=$P/scratch; R=$P/receipts
rm -rf "$R"; mkdir -p "$R"/{suites,campaigns/srp-head,campaigns/srp-base,campaigns/acmp-head,probes,area/independent-flow,area/author-flow,logs}
cp "$S"/logs/*.log "$S"/logs/*.rc "$R/logs/" 2>/dev/null || true
cp "$S"/logs/J1_streamfsms_head.log "$R/suites/srp_stream_fsms-head.log"
cp "$S"/logs/J9_makecheck_head.log "$R/suites/make-check-head.log"
cp "$S"/logs/J12_lint_head.log "$R/suites/lint_hdl-head-verilator5050.log"
cp "$S"/srp_campaign_head/*.log "$R/campaigns/srp-head/"
cp "$S"/srp_campaign_base/*.log "$R/campaigns/srp-base/"
cp "$S"/acmp_campaign_head/* "$R/campaigns/acmp-head/"
cp "$S"/probes/*.log "$R/probes/"
for t in base head; do
  for f in "$S"/area/${t}_top_2x2/stat.txt; do [ -f "$f" ] && cp "$f" "$R/area/independent-flow/${t}_srp_top_2x2.stat"; done
  for n in srp_top_2x2 srp_top_8x8; do
    [ -f "$S/area_af/$t/$n.stat" ] && cp "$S/area_af/$t/$n.stat" "$R/area/author-flow/${t}_$n.stat"
  done
done
cp "$S"/env.txt "$R/env.txt"
cp "$S"/clone-integrity.txt "$R/clone-integrity.txt"
cd "$P"
find REPORT.md scripts receipts -type f ! -name MANIFEST.sha256 | sort | grep -v '^REPORT.md$' | xargs sha256sum > MANIFEST.sha256
wc -l MANIFEST.sha256
