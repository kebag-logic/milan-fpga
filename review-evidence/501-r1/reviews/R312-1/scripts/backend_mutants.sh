#!/bin/sh
# [R312] probe: plant defects in copies of KL_nvm_backend.sv / sim_main.cpp
# under $SCR and grade them with the head 8x8 fixture. Run from repo root with
# the pinned Verilator first on PATH. Never edits the tree.
set -u
REPO=$(pwd); SCR=${SCR:?}; mkdir -p "$SCR"
TB=$REPO/tb/verilator/nvm_backend; RTL=$REPO/hdl/milan/KL_nvm_backend.sv
N=$(sed -n 's/.*AEM_NAME_ENTRIES_C = \([0-9]*\);.*/\1/p' configs/generated/endstation_ax7101_8x8/gen/adp_shape_defaults.svh)
SHAPE="-GCLK_HZ_P=10000 -GT_ALIVE_MS_P=4 -GT_COMMIT_MS_P=6 -GT_HOLD_MS_P=2 -GN_STREAM_IN_P=9 -GN_STREAM_OUT_P=9 -GN_SPORT_IN_P=8 -GN_SPORT_OUT_P=8 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=$N"
mut() { # name harness(with|without) python-replace-old python-replace-new
  d=$SCR/$1; mkdir -p $d
  python3 - "$RTL" "$d/KL_nvm_backend.sv" "$3" "$4" <<'PY'
import sys; s=open(sys.argv[1]).read(); o,n=sys.argv[3],sys.argv[4]
assert o=="" or s.count(o)==1, ("anchor count", s.count(o)); open(sys.argv[2],"w").write(s.replace(o,n) if o else s)
PY
  cp $TB/sim_main.cpp $d/sim_main.cpp
  if [ "$2" = without ]; then python3 - "$d/sim_main.cpp" <<'PY'
import sys; p=sys.argv[1]; s=open(p).read(); a="  test_output_boundaries();\n\n  printf"; assert s.count(a)==1; open(p,"w").write(s.replace(a,"  printf"))
PY
  fi
  verilator --cc --exe --build -j 8 --prefix Vnvm -Wall -CFLAGS "-std=c++17 -O2 -Wall -Wextra -I$TB" --Mdir $d/obj --top-module KL_nvm_backend $SHAPE $d/KL_nvm_backend.sv $d/sim_main.cpp -o Vnvm > $d/build.log 2>&1 || { echo "$1: BUILD FAILED"; return; }
  $d/obj/Vnvm $TB/records_endstation_ax7101_8x8.txt > $d/run.log 2>&1; rc=$?
  echo "$1 [harness $2]: rc=$rc $(grep 'checks:' $d/run.log) ; distinct FAIL kinds:"
  grep '^FAIL:' $d/run.log | sed 's/port [0-9]*/port N/; s/0x7[0-7]/0x7N/g' | cut -c1-150 | sort | uniq -c | head -8
}
OB="&& ({16'd0, dev_offset_i} + {16'd0, eff_len_w} <= 32'(rec_len_w))"
OBM="&& ({16'd0, dev_offset_i} + {16'd0, eff_len_w} <= 32'(rec_len_w) + 32'd1)"
ER="? 16'(rec_len_w) : dev_len_i;"; ERM="? 16'(rec_len_w) - 16'd1 : dev_len_i;"
TL="rec_len_w  = 12'(mapo_len_r[mapo_idx_w]);"; TLM="rec_len_w  = 12'(mapo_len_r[mapo_idx_w][8:0]);"
mut control with "" ""
mut over_by_one with "$OB" "$OBM"
mut over_by_one_old without "$OB" "$OBM"
mut erase_short with "$ER" "$ERM"
mut erase_short_old without "$ER" "$ERM"
mut len9 with "$TL" "$TLM"
mut len9_old without "$TL" "$TLM"
