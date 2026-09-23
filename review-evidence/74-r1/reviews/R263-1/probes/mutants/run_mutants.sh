#!/bin/bash
# Reviewer mutation probes (R263-1, #74 item 2). Each mutant is one textual
# substitution in a disposable copy of the head tree; a substitution that
# changes nothing is refused. For every mutant both touched suites' main
# harnesses are built and run, and their [FAIL] lines are recorded.
#   run_mutants.sh <head_tree> <scratch_dir> <out_dir>
set -eu
HEAD=$1; SCR=$2; OUT=$3
V=${VERILATOR:-verilator}
mkdir -p "$SCR" "$OUT"
CAP=hdl/ieee1722/aaf/KL_chan_map_capture.sv
MGA=hdl/ieee1722/crf/KL_media_grid_align.sv
# name|file|perl substitution
MUTANTS=(
  "coin_old|$CAP|s/tdm_frame_pend_r <= tdm_frame_pend_r;/tdm_frame_pend_r <= 1'b0;/"
  "coin_set|$CAP|s/tdm_frame_pend_r <= tdm_frame_pend_r;/tdm_frame_pend_r <= 1'b1;/"
  "coin_tickfirst|$CAP|s/tdm_frame_pend_r <= tdm_frame_pend_r;/tdm_frame_pend_r <= 1'b1; if (tdm_fed_r && !tdm_frame_pend_r && tdm_dup_cnt_o != 16'hFFFF) tdm_dup_cnt_o <= tdm_dup_cnt_o + 16'd1;/"
  "keep_no_hi|$MGA|s/KEEP_HI_C = TSTW_C'\\(DIV_C - LOCK_KEEPOFF_CYC_P\\);/KEEP_HI_C = TSTW_C'(DIV_C);/"
  "keep_no_lo|$MGA|s/KEEP_LO_C = TSTW_C'\\(LOCK_KEEPOFF_CYC_P\\);/KEEP_LO_C = TSTW_C'(0);/"
  "keep_small|$MGA|s/\\(CLK_FREQ_HZ_P \\/ FS_HZ_P\\) \\/ 128/(CLK_FREQ_HZ_P \\/ FS_HZ_P) \\/ 512/"
  "keep_cross|$MGA|s/ref_keep_w = \\(tst_next_w < KEEP_LO_C\\) \\? KEEP_LO_C/ref_keep_w = (tst_next_w < KEEP_LO_C) ? KEEP_HI_C/"
  "keep_raw|$MGA|s/if \\(frame_ev_i\\) ref_r <= ref_keep_w;/if (frame_ev_i) ref_r <= tst_next_w;/"
)
run_one() {
  local spec=$1
  local name=${spec%%|*}; local rest=${spec#*|}
  local file=${rest%%|*}; local sub=${rest#*|}
  local T="$SCR/mut_$name"
  rm -rf "$T"; mkdir -p "$T"; cp -r "$HEAD/hdl" "$HEAD/tb" "$T/"
  # never reuse a build product copied from another tree
  find "$T/tb" -maxdepth 3 -type d -name 'obj_*' -prune -exec rm -rf {} +
  perl -pi -e "$sub" "$T/$file"
  if cmp -s "$HEAD/$file" "$T/$file"; then echo "MUTANT $name: SUBSTITUTION FAILED" > "$OUT/$name.txt"; return 0; fi
  diff "$HEAD/$file" "$T/$file" > "$OUT/$name.diff" || true
  (
    cd "$T/tb/verilator/media_grid_align"
    "$V" --cc --exe --build -j 2 --top-module media_grid_align_wrap -Wno-fatal -Wno-lint -Wno-style \
      -Wno-PINCONNECTEMPTY +incdir+../../../hdl/common -CFLAGS "-std=c++17 -O2 -I$PWD" \
      media_grid_align_wrap.sv ../../../hdl/ieee1722/crf/KL_media_grid_align.sv \
      ../../../hdl/ieee1722/crf/KL_media_nco.sv ../../../hdl/ieee1722/aaf/KL_chan_map_capture.sv \
      sim_main.cpp -o Vmedia_grid_align_sim > build.log 2>&1
    ./obj_dir/Vmedia_grid_align_sim > run.log 2>&1 || true
  )
  (
    cd "$T/tb/verilator/chmap_capture"
    make VERILATOR="$V" obj_dir/Vchmap_wrap > build.log 2>&1
    ./obj_dir/Vchmap_wrap > run.log 2>&1 || true
  )
  {
    echo "MUTANT $name ($file)"
    sed 's/^/  diff: /' "$OUT/$name.diff"
    echo "  media_grid_align: $(grep -E 'checks, [0-9]+ failures' "$T/tb/verilator/media_grid_align/run.log")"
    grep '\[FAIL\]' "$T/tb/verilator/media_grid_align/run.log" | sed 's/^/    mga /' || true
    grep -E 'acquisition:|window [0-9]:' "$T/tb/verilator/media_grid_align/run.log" | sed 's/^/    mga /' | head -12 || true
    echo "  chmap_capture: $(grep -E 'checks, [0-9]+ failures' "$T/tb/verilator/chmap_capture/run.log")"
    grep '\[FAIL\]' "$T/tb/verilator/chmap_capture/run.log" | sed 's/^/    chmap /' || true
  } > "$OUT/$name.txt"
}
export -f run_one
export HEAD SCR OUT V
printf '%s\0' "${MUTANTS[@]}" | xargs -0 -P 8 -I{} bash -c 'run_one "$@"' _ {}
cat "$OUT"/*.txt
