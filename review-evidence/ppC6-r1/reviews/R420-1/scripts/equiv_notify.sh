#!/usr/bin/env bash
# KL_aecp_notify: head at EN_IDENTIFY_NOTIF_P = 0 vs main 0451d83d (yosys equiv_*),
# then a negative control that must FAIL (one planted constant change).
set -euo pipefail
PKT="$(cd "$(dirname "$0")/.." && pwd)"; S="$PKT/scratch"; W="$S/equiv"; mkdir -p "$W/neg"; cd "$W"
sv2v "$S/base/hdl/common/pp_pkg.sv" "$S/base/hdl/aecp/KL_aecp_notify.sv" | sed 's/^module KL_aecp_notify (/module notify_gold (/' > notify_gold.v
sv2v "$S/head/hdl/common/pp_pkg.sv" "$S/head/hdl/aecp/KL_aecp_notify.sv" | sed 's/^module KL_aecp_notify (/module notify_gate (/' > notify_gate.v
yosys -q -l "$PKT/receipts/equiv_notify.log" -s "$PKT/scripts/equiv_notify.ys" >/dev/null && echo "equiv: PROVEN"
cp notify_gold.v neg/; sed "0,/32'd1000/s//32'd999/" notify_gate.v > neg/notify_gate.v
cd neg; if yosys -q -l "$PKT/receipts/equiv_notify_negctl.log" -s "$PKT/scripts/equiv_notify.ys" >/dev/null 2>&1; then echo "negative control: WRONGLY PROVEN"; exit 1; else echo "negative control: fails as it must"; fi
