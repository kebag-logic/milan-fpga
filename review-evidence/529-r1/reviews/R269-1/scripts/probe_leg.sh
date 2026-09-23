#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Build and run one milan_dp sim_nxn leg against a chosen milan_datapath source
# (the exact-head file or a mutated copy), inside a disposable copy of the
# exact-head tree. Mirrors the leg recipes in tb/verilator/milan_dp/Makefile
# (targets `run` obj_nxn / obj_notify / obj_nxn8) with the source list and the
# DP flag set exported by that Makefile's print-srcs / print-dp-vflags.
#
# usage: probe_leg.sh <leg:nxn|notify|nxn8|main> <dp_src.sv> <tag> [jobs]
# env:   VERILATOR   pinned simulator (5.050)
#        PACKET      packet root (default: this script's parent directory)
set -euo pipefail
leg=$1; dp_src=$(readlink -f "$2"); tag=$3; jobs=${4:-8}
PACKET=${PACKET:-$(cd "$(dirname "$0")/.." && pwd)}
S=$PACKET/scratch
TREE=$S/tree
RUN=$TREE/tb/verilator/milan_dp
: "${VERILATOR:?set VERILATOR to the pinned simulator}"
LOG=$PACKET/receipts/leg_${tag}.log
mkdir -p "$PACKET/receipts" "$S/obj"
cd "$RUN"
[ -f ltn_rom.hex ] || python3 ../../../protocol-processor/hdl/acmp/rom/gen_ltn_rom.py -o ltn_rom.hex
[ -f ucode.hex ]   || python3 ../../../protocol-processor/hdl/aecp/ucode/gen_ucode.py -o ucode.hex
# the Makefile's source list, with its DP_SRC default replaced by the probe's
srcs=$(sed "s#\.\./\.\./\.\./hdl/milan/milan_datapath\.sv#${dp_src}#" "$S/srcs.txt")
grep -q "$dp_src" <<<"$srcs"
# the Makefile's DP flag set (GPTP_OFF_VFLAGS), job count bounded
vflags=$(sed "s/--build -j 0/--build -j ${jobs}/" "$S/dpvflags.txt")
MDIR=$S/obj/$tag
cpp=sim_nxn.cpp
rm -rf "$MDIR"
case $leg in
  nxn)    shape="+incdir+../../../configs/generated/endstation_arty_4x4"
          extra=(-GN_STREAMS=4); cfl=(); bin=Vmilan_dp_nxn ;;
  main)   shape="+incdir+../../../configs/generated/endstation_arty_current"
          extra=(); cfl=(); bin=Vmilan_dp_sim; cpp=sim_main.cpp ;;
  nxn8)   shape="+incdir+../../../configs/generated/endstation_ax7101_8x8"
          extra=(-GN_STREAMS=8 -GLOOPBACK_P=1)
          cfl=(-CFLAGS "-DNSTREAMS_TB=8 -DAX8X8_TB=1 -DLOOPBACK_TB=1 -DLB_SEQ_FIXED=1 -Wall -Wextra")
          bin=Vmilan_dp_nxn8 ;;
  notify) shape="+incdir+../../../configs/generated/endstation_ax7101_1x1_tdm8"
          extra=(-GPP_TIM_DIV_US_P=1 -GPP_TIM_DIV_MS_P=100)
          cfl=(-CFLAGS "-DNSTREAMS_TB=1 -DNOTIFY_TIMED_TB=1 -DMS_CYC_TB=100 -Wall -Wextra")
          bin=Vmilan_dp_notify ;;
  *) echo "unknown leg $leg" >&2; exit 2 ;;
esac
{
  echo "# leg=$leg tag=$tag dp_src_sha256=$(sha256sum "$dp_src" | cut -d' ' -f1)"
  echo "# simulator: $("$VERILATOR" --version)"
  echo "# build start $(date -u +%FT%TZ)"
} > "$LOG"
set +e
# shellcheck disable=SC2086
eval "\"$VERILATOR\" $shape $vflags --Mdir \"$MDIR\" ${extra[*]} \"\${cfl[@]}\" $srcs $cpp -o $bin" \
  > "$MDIR.build.log" 2>&1
brc=$?
echo "# build exit $brc $(date -u +%FT%TZ)" >> "$LOG"
if [ $brc -ne 0 ]; then
  echo "# BUILD FAILED; last 40 lines of the build log follow" >> "$LOG"
  tail -40 "$MDIR.build.log" | sed -e "s#$PACKET#<packet>#g" -e "s#$HOME#\$HOME#g" >> "$LOG"
  echo "leg $tag: BUILD FAILED ($brc)"; exit 0
fi
export TMPDIR=$S/tmp; mkdir -p "$TMPDIR"
"$MDIR/$bin" > "$MDIR.run.log" 2>&1
rrc=$?
set -e
echo "# run exit $rrc $(date -u +%FT%TZ)" >> "$LOG"
# keep the CRF sections and the tally lines in the receipt, full log in scratch
grep -E 'CTRS-CRF|NOTIFY-CRF|CRF row pushes|^\s*(PASS|FAIL)\b.*\[CTRS\]|RESULT|passed|failed|checks|FAIL' "$MDIR.run.log" \
  | sed -e "s#$PACKET#<packet>#g" -e "s#$HOME#\$HOME#g" >> "$LOG" || true
echo "# FAIL lines: $(grep -c 'FAIL' "$MDIR.run.log" || true)" >> "$LOG"
tail -5 "$MDIR.run.log" | sed -e "s#$PACKET#<packet>#g" -e "s#$HOME#\$HOME#g" >> "$LOG"
echo "leg $tag: run exit $rrc"
