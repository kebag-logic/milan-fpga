#!/usr/bin/env bash
# Recipe "Yosys comparison" for one shape, detached; caller polls <OOC_TMP>/run_rc.txt.
# Usage: run_yosys_flat_detached.sh <clean-clone> <work> <shape: ax7101|ax8x8>
set -euo pipefail
repo="$1"; work="$2"; shape="$3"
case "$shape" in
  ax7101) config=endstation_ax7101_1x1_tdm8 ;;
  ax8x8) config=endstation_ax7101_8x8 ;;
esac
out="$work/$shape-yosys"; mkdir -p "$out"; rm -f "$out/run_rc.txt"
cd "$repo"
setsid nohup env OOC_CHPARAM="$(cat "$work/$shape-ooc/baseline_chparam.txt")" \
  OOC_SHAPE="$repo/configs/generated/$config" OOC_TMP="$out" YOSYS_MALLOC=none \
  bash -c 'bash syn/yosys/ooc.sh KL_pp_shadow > "$OOC_TMP/ooc_sh_stdout.txt" 2>&1; echo $? > "$OOC_TMP/run_rc.txt"' \
  < /dev/null > /dev/null 2>&1 &
echo "launched pid $!"
