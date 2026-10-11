#!/bin/sh
# Reviewer probe (R593-2): extract the dev-base slice sources with every
# changed module (and its parents up to the slice wrapper) suffixed `_dev`,
# for make_dual.py and make_shadow_dual.py.
# Usage: prep_dev.sh <clone at the exact head> <out dir>
set -eu
CLONE=$1; OUT=$2
BASE=e8454e2751d05b02ee8e5a571857589ab358ab86
DONOR_BASE=5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d
mkdir -p "$OUT"
git -C "$CLONE" show $BASE:hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv > "$OUT/KL_gptp_shadow_dev.sv"
git -C "$CLONE" show $BASE:hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv > "$OUT/KL_gptp_txret_dev.sv"
git -C "$CLONE" show $BASE:tb/verilator/gptp_shadow/gptp_shadow_wrap.sv > "$OUT/gptp_shadow_wrap_dev.sv"
git -C "$CLONE/gptp-processor" show $DONOR_BASE:hdl/common/KL_gptp_timer.sv > "$OUT/KL_gptp_timer_dev.sv"
git -C "$CLONE/gptp-processor" show $DONOR_BASE:hdl/top/KL_gptp_engine.sv > "$OUT/KL_gptp_engine_dev.sv"
# the engine RTL is unchanged at the head pin; it is copied only to rename its timer
git -C "$CLONE/gptp-processor" diff --quiet $DONOR_BASE HEAD -- hdl/top/KL_gptp_engine.sv
for f in "$OUT"/*.sv; do
  sed -i -E 's/\bKL_gptp_shadow\b/KL_gptp_shadow_dev/g; s/\bKL_gptp_txret\b/KL_gptp_txret_dev/g; s/\bKL_gptp_engine\b/KL_gptp_engine_dev/g; s/\bKL_gptp_timer\b/KL_gptp_timer_dev/g; s/\bgptp_shadow_wrap\b/gptp_shadow_wrap_dev/g' "$f"
done
sha256sum "$OUT"/*.sv
