#!/bin/sh
# Round-3 driver: the round-2 campaign (r329_campaign.sh) with the same
# per-mutant scripts and mutant lists, split into parts and run at -P 8.
# Usage: r329_3_campaign.sh <tree> <outdir> unchanged|adapter|dp|report
#   (PATH must carry the pinned verilator)
set -u
T=$1; O=$2; S=$(cd "$(dirname "$0")" && pwd)
case $3 in
unchanged)
  mkdir -p "$O/unchanged"
  printf '%s\n' control M1_drop_map M2_drop_name M3_delay_one_cycle M4_wrong_phase_2 \
    M5_early_phase_4 M6_add_only M7_no_sticky M8_input_ports_only M9_any_phase M10_late_mark |
    xargs -P 8 -I{} python3 "$S/r329_mutants.py" "$T" "$O/unchanged/{}" {} > /dev/null ;;
adapter)
  mkdir -p "$O/adapter"
  printf '%s\n' M1_drop_map M2_drop_name M4_wrong_phase_2 M5_early_phase_4 M6_add_only \
    M8_input_ports_only M9_any_phase M10_late_mark U1_drop_map U5_refused_live \
    U6_add_only U8_input_only U11_unqualified_p5 |
    xargs -P 8 -I{} python3 "$S/r329_mutants_adapter.py" "$T" "$O/adapter/{}" {} > /dev/null ;;
dp)
  mkdir -p "$O/dp"
  printf '%s\n' D1_pulse_no_out_change D2_pulse_no_in_change D3_pulse_any_phase5_record |
    xargs -P 3 -I{} python3 "$S/r329_dp_mutants.py" "$T" "$O/dp/{}" {} > /dev/null ;;
report)
  for d in unchanged adapter dp; do
    echo "## $d"; for f in "$O/$d"/*/RESULTS.txt; do cat "$f"; done
  done ;;
esac
