#!/bin/sh
# Reviewer mutant runner (R262-1). Builds the PR's own media_grid_align and
# chmap_capture harnesses over each mutated tree at <scratch>/mut/<name>
# (sequentially, 8 compile jobs each), then runs the simulations with at
# most 6 in parallel. usage: run_mutants.sh <scratch_dir> <receipts_dir> <vwrap>
set -eu
S=$1; R=$2; VW=$3
MUTS="MA1_no_hi_clamp MA2_no_lo_clamp MA3_keepoff4 MC1_coin_pend1 MC2_coin_tickfirst MC3_coin_markfirst"
for m in $MUTS; do
  d=$S/mut/$m/tb/verilator/media_grid_align
  ( cd "$d" && "$VW" --cc --exe --build -j 0 --top-module media_grid_align_wrap \
      -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
      -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY \
      +incdir+../../../hdl/common -CFLAGS "-std=c++17 -O2 -I$d" \
      media_grid_align_wrap.sv ../../../hdl/ieee1722/crf/KL_media_grid_align.sv \
      ../../../hdl/ieee1722/crf/KL_media_nco.sv \
      ../../../hdl/ieee1722/aaf/KL_chan_map_capture.sv sim_main.cpp \
      -o Vmedia_grid_align_sim > build.log 2>&1 ) || { echo "BUILD FAILED $m mga"; exit 1; }
  c=$S/mut/$m/tb/verilator/chmap_capture
  ( cd "$c" && make VERILATOR="$VW" obj_dir/Vchmap_wrap > build.log 2>&1 ) \
    || { echo "BUILD FAILED $m chmap"; exit 1; }
  echo "built $m"
done
for m in $MUTS; do
  echo "$S/mut/$m/tb/verilator/media_grid_align ./obj_dir/Vmedia_grid_align_sim $R/mut_${m}_media_grid_align.log"
  echo "$S/mut/$m/tb/verilator/chmap_capture ./obj_dir/Vchmap_wrap $R/mut_${m}_chmap_capture.log"
done | xargs -P 6 -L 1 sh -c 'cd "$0" && { "$1"; echo "exit=$?"; } > "$2" 2>&1'
for m in $MUTS; do
  for suite in media_grid_align chmap_capture; do
    f=$R/mut_${m}_${suite}.log
    printf '%-20s %-17s %s | %s\n' "$m" "$suite" \
      "$(grep -E '^[0-9]+ checks|: [0-9]+ checks' "$f" | tail -1)" "$(grep -E '^exit=' "$f")"
  done
done
