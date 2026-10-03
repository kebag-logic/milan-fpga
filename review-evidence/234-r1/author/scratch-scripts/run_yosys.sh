#!/usr/bin/env bash
# Scratch (never committed): the recipe's Yosys comparison for one combination
# and shape, recording rc and times.   run_yosys.sh <A|B> <ax7101|ax8x8>
set -u
combo=$1; shape=$2
S=$VALIDATION_STORAGE/234-a516
case "$shape" in
  ax7101) config=endstation_ax7101_1x1_tdm8 ;;
  ax8x8) config=endstation_ax7101_8x8 ;;
esac
out=$S/$combo/work/$shape-yosys
mkdir -p "$out"
log=$out/ooc.sh.log
date -Is > "$log.start"
rc=0
OOC_CHPARAM="$(cat "$S/$combo/work/$shape-ooc/baseline_chparam.txt")" \
OOC_SHAPE="$S/$combo/repo/configs/generated/$config" \
OOC_TMP="$out" \
  bash "$S/$combo/repo/syn/yosys/ooc.sh" KL_pp_shadow > "$log" 2>&1 || rc=$?
date -Is > "$log.end"
echo "$rc" > "$log.rc"
