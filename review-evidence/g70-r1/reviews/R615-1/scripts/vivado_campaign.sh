#!/bin/sh
# Reviewer Vivado campaign for #70 / PR #79, run once under the exclusive
# Vivado lock, one Vivado session at a time.
#   usage: vivado_campaign.sh PACKET
# PACKET/scratch/head  = git archive of 26622e27 (constrained flow)
# PACKET/scratch/main  = git archive of 5dce647a (unconstrained flow)
# PACKET/scratch/plant-usedinsynth = head copy with the XDC excluded from
#   synthesis by property (a plant the static gate cannot see).
# Receipts land in PACKET/receipts/vivado/<arm>/.
set -u
P=$1
S=$P/scratch
R=$P/receipts/vivado
VIVADO_SETTINGS=${VIVADO_SETTINGS:-$HOME/Xilinx/2026.1/Vivado/settings64.sh}
export VIVADO_SETTINGS
mkdir -p "$R"
exec 9>$VIVADO_LOCK
date -u +%FT%TZ > "$R/lock-wait-start.txt"
flock -w 3600 9 || { echo "lock timeout" > "$R/lock-timeout.txt"; exit 9; }
date -u +%FT%TZ > "$R/lock-acquired.txt"

keep() { # arm dir
  mkdir -p "$R/$1"
  for f in ucpu_ooc.log engine_ooc.log ucpu_util.rpt ucpu_util_hier.rpt \
           ucpu_timing.rpt engine_util.rpt engine_util_hier.rpt engine_timing.rpt; do
    [ -f "$2/syn/ooc/work/$f" ] && cp "$2/syn/ooc/work/$f" "$R/$1/$f"
  done
}

for arm in head main; do
  rm -rf "$S/$arm/syn/ooc/work/"*.log "$S/$arm/syn/ooc/work/"*.rpt
  ( cd "$S/$arm" && date -u +%FT%TZ && make ooc; echo "rc=$?" ) > "$R/make-ooc-$arm.txt" 2>&1
  keep "$arm" "$S/$arm"
done

# Plant the static gate cannot see: the XDC is read before synth_design but
# excluded from synthesis. Only the log check can catch it. ucpu only.
D=$S/plant-usedinsynth
mkdir -p "$D/syn/ooc/work"
(
  cd "$D/syn/ooc/work" &&
  python3 "$D/syn/ooc/check_ooc_clock.py"; echo "static rc=$?"
  python3 "$D/hdl/ucode/gen_gptp_ucode.py" -o gptp_ucode.hex &&
  . "$VIVADO_SETTINGS" &&
  vivado -mode batch -source "$D/syn/ooc/ucpu_ooc.tcl" -nojournal -log ucpu_ooc.log
  echo "vivado rc=$?"
  python3 "$D/syn/ooc/check_ooc_clock.py" --log ucpu_ooc.log; echo "log rc=$?"
) > "$R/plant-usedinsynth.txt" 2>&1
mkdir -p "$R/plant-usedinsynth"
for f in ucpu_ooc.log ucpu_util.rpt ucpu_timing.rpt; do
  [ -f "$D/syn/ooc/work/$f" ] && cp "$D/syn/ooc/work/$f" "$R/plant-usedinsynth/$f"
done
date -u +%FT%TZ > "$R/lock-released.txt"
