#!/usr/bin/env bash
# R356-1 probe: elaborate KL_pp_shadow (top) at the base and head trees with
# the parameters milan_datapath passes for a shape (read from that shape's
# tracked generated header), and compare Verilator post-elaboration stats.
# Also: liveness legs (a non-default count must reach u_pp at head only) and
# zero-count legs (what the processor does if a count were 0).
# Usage: probe_elab.sh <scratch dir with base/ head/> <verilator> <outdir> <pp_srcs.txt from scripts/pp_srcs.py>
set -u
S=${1:?scratch}; V=${2:?verilator}; O=${3:?outdir}; PPSRCS=${4:?pp source list}
mkdir -p "$O"
val() { sed -n "s/.*localparam int $1 *= *\([0-9]*\);.*/\1/p" "$2" | head -1; }
elab() {  # side tag extra-G...
  local side=$1 tag=$2; shift 2
  local T="$S/$side" M="$O/$side-$tag"
  mkdir -p "$M"
  ( cd "$T" && "$V" --lint-only --stats -Wno-fatal -Wno-lint -Wno-style \
      --top-module KL_pp_shadow -Mdir "$M" \
      $(cat "$PPSRCS") hdl/milan/KL_pp_shadow.sv \
      -y hdl/milan -y hdl/common -y protocol-processor/hdl/top -y third_party/verilog-axis/rtl -Wno-TIMESCALEMOD \
      -Ihdl/common "$@" > "$M/elaborate.log" 2>&1 ; echo "rc=$?" >> "$M/elaborate.log" )
  printf '%-6s %-28s %s  stats=%s\n' "$side" "$tag" "$(tail -1 "$M/elaborate.log")" \
    "$( [ -f "$M/VKL_pp_shadow__stats.txt" ] && echo present || echo absent)"
}
shape_args() {  # shape side -> -G list as milan_datapath binds them
  local h="$S/$2/configs/generated/$1/gen/adp_shape_defaults.svh" g
  g="-GN_STREAM_IN_P=$(val ADP_LISTENER_SINK_C "$h") -GN_STREAM_OUT_P=$(val ADP_TALKER_SRC_C "$h")"
  g="$g -GDESC_NAME_ENTRIES_P=$(val AEM_NAME_ENTRIES_C "$h")"
  g="$g -GN_SPORT_IN_P=$(val ADP_DMAP_IN_NPORTS_C "$h") -GN_SPORT_OUT_P=$(val ADP_DMAP_OUT_NPORTS_C "$h")"
  g="$g -GN_AUDIO_UNIT_P=$(val AEM_N_AUDIO_UNIT_C "$h") -GN_CLK_DOM_P=$(val AEM_N_CLKDOM_C "$h")"
  [ "$2" = head ] && g="$g -GN_CONTROL_P=$(val AEM_N_CONTROL_C "$h")"
  echo "$g"
}
for shape in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
  for side in base head; do
    a=$(shape_args $shape $side); echo "$side $shape args: $a"
    elab $side $shape $a
  done
done
# Liveness: at the 1x1 shape, raise one count to 2. At base only the NVM
# backend sees it; at head u_pp (processor dyn-state rows) must see it too.
b=$(shape_args endstation_ax7101_1x1_tdm8 base | sed 's/-GN_AUDIO_UNIT_P=1/-GN_AUDIO_UNIT_P=2/')
h=$(shape_args endstation_ax7101_1x1_tdm8 head | sed 's/-GN_AUDIO_UNIT_P=1/-GN_AUDIO_UNIT_P=2/')
elab base au2 $b; elab head au2 $h
h=$(shape_args endstation_ax7101_1x1_tdm8 head | sed 's/-GN_CONTROL_P=1/-GN_CONTROL_P=3/')
elab head ctl3 $h
h=$(shape_args endstation_ax7101_1x1_tdm8 head | sed 's/-GN_CLK_DOM_P=1/-GN_CLK_DOM_P=2/')
elab head cd2 $h
# Zero legs at head: what the processor does if a count reached 0.
for p in N_AUDIO_UNIT_P N_CLK_DOM_P N_CONTROL_P; do
  h=$(shape_args endstation_ax7101_1x1_tdm8 head | sed "s/-G$p=1/-G$p=0/")
  elab head zero-$p $h
done
