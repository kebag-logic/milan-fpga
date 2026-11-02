#!/bin/sh
# Probe trees for run_probes.sh. Usage: setup_trees.sh <head-clone> <packet-dir>
set -u
C=$1; P=$2; S=$P/scratch; R=$P/receipts
PATHS="scripts hdl/common/csr configs/generated/endstation_ax7101_1x1_tdm8 configs/generated/endstation_arty_4x4 docs/reference"
for n in head m1 m2 m4 m5; do rm -rf "$S/t/$n"; mkdir -p "$S/t/$n"; git -C "$C" archive 2c500d0a9c3eb0ef0c764db6978bf8d0ab217ea2 $PATHS | tar -x -C "$S/t/$n"; done
rm -rf "$S/t/prev" "$S/t/prev_m4"; mkdir -p "$S/t/prev"; git -C "$C" archive ef7dc985 $PATHS | tar -x -C "$S/t/prev"
for m in m1 m2 m4 m5; do (cd "$S/t/$m" && patch -p1 < "$R/patches/$m.rtl.diff"); done
cp -r "$S/t/prev" "$S/t/prev_m4"; (cd "$S/t/prev_m4" && patch -p1 < "$R/patches/m4.rtl.diff")
git -C "$C" show 79fdea05:docs/reference/REGISTER_MAP.md > "$S/page_round4_wording.md"
