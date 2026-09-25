#!/usr/bin/env bash
# Independent release-tail probe (#545). Wraps the REAL ptp_csr_sync and
# timestamp_counter RTL at the head, a one-register addend latch equal to
# KL_gptp_shadow.sv phc_adj_o (latched on the engine addend pulse), and the
# slew_rate_alignment block extracted verbatim from milan_datapath.sv. The
# engine is modelled per KL_gptp_engine.sv: phc_addend_we_o and
# phc_slew_active_o are registered and change on the same edge.
# Ground truth is the counter's own per-cycle integer increment: every
# PHC sample whose preceding increment used the slew addend must be staged
# with the level high. Variant TAIL=3 must violate it (tightness control).
set -u
REPO=${REPO:-$REVIEWS/r301-2-545}
PKT=${PKT:-$REVIEWS/545-r301-2-packet}
HEAD=b94f53cc4e5dbfd9527ba666922a55804515165c
VERILATOR=${VERILATOR:-$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator}
HERE=$(cd "$(dirname "$0")" && pwd)
W="$PKT/scratch/tail_probe"; rm -rf "$W"; mkdir -p "$W"
git -C "$REPO" show "$HEAD:hdl/ieee8021as/ptp_timestamp/ptp_csr_sync.sv" > "$W/ptp_csr_sync.sv"
git -C "$REPO" show "$HEAD:hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv" > "$W/timestamp_counter.sv"
git -C "$REPO" show "$HEAD:hdl/milan/milan_datapath.sv" > "$W/dp.sv"
BLOCK=$(awk '/logic \[3:0\] gptp_slew_tail_r;/{f=1} f{print} /end : slew_rate_alignment/{if(f) exit}' "$W/dp.sv")
[ "$(printf '%s\n' "$BLOCK" | wc -l)" -eq 6 ] || { echo "FAIL: alignment block not found verbatim"; exit 2; }
printf '%s\n' "$BLOCK" > "$W/block_extracted.txt"
rc=0
for TAIL in 4 3; do
  B="$BLOCK"
  if [ "$TAIL" = 3 ]; then
    B=$(printf '%s\n' "$BLOCK" | sed -e 's/logic \[3:0\] gptp_slew_tail_r/logic [2:0] gptp_slew_tail_r/' -e 's/{gptp_slew_tail_r\[2:0\], gptp_slew_active_w}/{gptp_slew_tail_r[1:0], gptp_slew_active_w}/')
  fi
  D="$W/tail$TAIL"; mkdir -p "$D"
  { sed -n '1,/^\/\/ BLOCK$/p' "$HERE/probe_top.sv.in" | sed '$d'; printf '%s\n' "$B"; sed -n '/^\/\/ BLOCK$/,$p' "$HERE/probe_top.sv.in" | sed '1d'; } > "$D/probe_top.sv"
  "$VERILATOR" --cc --exe --build -j 4 -Wno-fatal -Wno-lint -Wno-style --public-flat-rw \
     --top-module probe_top -Mdir "$D/obj" "$D/probe_top.sv" "$W/ptp_csr_sync.sv" \
     "$W/timestamp_counter.sv" "$HERE/probe_main.cpp" -o Vprobe >"$D/build.log" 2>&1 || { echo "BUILD FAIL tail$TAIL"; tail -20 "$D/build.log"; exit 2; }
  echo "== tail stages = $TAIL"
  "$D/obj/Vprobe"; r=$?
  if [ "$TAIL" = 4 ] && [ $r -ne 0 ]; then echo "UNEXPECTED: shipped tail violates"; rc=1; fi
  if [ "$TAIL" = 3 ] && [ $r -eq 0 ]; then echo "UNEXPECTED: 3-stage control not rejected"; rc=1; fi
done
echo "probe rc=$rc"
exit $rc
