#!/bin/bash
# The recipe's Yosys loop body for one shape ($1 = ax7101 | ax8x8).
set -u
shape=$1
case "$shape" in
  ax7101) config=endstation_ax7101_1x1_tdm8 ;;
  ax8x8) config=endstation_ax7101_8x8 ;;
esac
export OOC_CHPARAM="$(cat "$WORK/$shape-ooc/baseline_chparam.txt")"
export OOC_SHAPE="$REPO/configs/generated/$config"
export OOC_TMP="$WORK/$shape-yosys"
export YOSYS_MALLOC=none
bash syn/yosys/ooc.sh KL_pp_shadow
