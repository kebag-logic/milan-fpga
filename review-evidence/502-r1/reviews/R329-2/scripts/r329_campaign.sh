#!/bin/sh
# Round-2 driver: the UNCHANGED round-1 campaign, then the anchor adapter.
# Usage: r329_campaign.sh <tree> <outdir>   (PATH must carry the pinned verilator)
set -u
T=$1; O=$2; S=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$O/unchanged" "$O/adapter"
# 1. unchanged script, every round-1 mutant (stale anchors are REFUSED, not kills)
printf '%s\n' control M1_drop_map M2_drop_name M3_delay_one_cycle M4_wrong_phase_2 \
  M5_early_phase_4 M6_add_only M7_no_sticky M8_input_ports_only M9_any_phase M10_late_mark |
  xargs -P 4 -I{} python3 "$S/r329_mutants.py" "$T" "$O/unchanged/{}" {} > /dev/null
# 2. anchor adapter for the refused ones, plus round-2 variants
printf '%s\n' M1_drop_map M2_drop_name M4_wrong_phase_2 M5_early_phase_4 M6_add_only \
  M8_input_ports_only M9_any_phase M10_late_mark U1_drop_map U5_refused_live \
  U6_add_only U8_input_only U11_unqualified_p5 |
  xargs -P 4 -I{} python3 "$S/r329_mutants_adapter.py" "$T" "$O/adapter/{}" {} > /dev/null
for d in unchanged adapter; do
  echo "## $d"; for f in "$O/$d"/*/RESULTS.txt; do cat "$f"; done
done
