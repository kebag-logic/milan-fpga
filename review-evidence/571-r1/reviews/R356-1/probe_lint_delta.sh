#!/usr/bin/env bash
# R356-1 probe: Verilator -Wall lint of KL_pp_shadow (top) at base and head
# with the AX 1x1 shape's generated parameters; compare the warning sets with
# line numbers removed, so only new or lost warning kinds/sites show.
# Usage: probe_lint_delta.sh <scratch dir with base/ head/> <verilator> <outdir> <pp_srcs.txt>
set -u
S=${1:?}; V=${2:?}; O=${3:?}; PPSRCS=${4:?}
mkdir -p "$O"
G="-GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GDESC_NAME_ENTRIES_P=38 -GN_SPORT_IN_P=1 -GN_SPORT_OUT_P=1 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1"
for side in base head; do
  g="$G"; [ $side = head ] && g="$g -GN_CONTROL_P=1"
  ( cd "$S/$side" && "$V" --lint-only -Wall -Wno-fatal -Wno-TIMESCALEMOD --top-module KL_pp_shadow \
      -Mdir "$O/lint-$side" $(cat "$PPSRCS") hdl/milan/KL_pp_shadow.sv \
      -y hdl/milan -y hdl/common -y protocol-processor/hdl/top -y third_party/verilog-axis/rtl \
      -Ihdl/common $g > "$O/lint-$side.log" 2>&1; echo "rc=$?" >> "$O/lint-$side.log" )
  grep -E '^%(Warning|Error)' "$O/lint-$side.log" | sed -E 's/:[0-9]+:[0-9]+:/:L:C:/' | sort > "$O/lint-$side.norm"
  echo "$side: $(tail -1 "$O/lint-$side.log") warnings=$(wc -l < "$O/lint-$side.norm")"
done
echo "== normalized warning delta (base -> head) =="
diff "$O/lint-base.norm" "$O/lint-head.norm" && echo "no warning delta"
