#!/bin/sh
# Build the BRANCH harnesses against the BASE RTL (git show of dev ede8d48e,
# extracted under base_rtl/) and run them: the new checks must fail there.
set -u
O=$REVIEWS/74-a197-packet
L=$LANES/74-junction-chatter
B=$O/base_rtl
PATH=$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin:$PATH
export PATH
verilator --version
W="-Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY"
cd $L/tb/verilator/media_grid_align || exit 2
verilator --cc --exe --build -j 8 --Mdir $O/obj_base_mga --top-module media_grid_align_wrap $W \
  +incdir+$B/common -CFLAGS "-std=c++17 -O2 -Wall -Wextra -I$L/tb/verilator/media_grid_align" \
  media_grid_align_wrap.sv $B/ieee1722/crf/KL_media_grid_align.sv $B/ieee1722/crf/KL_media_nco.sv \
  $B/ieee1722/aaf/KL_chan_map_capture.sv sim_main.cpp -o Vmga_base > $O/receipts/base-mga-build.log 2>&1 || exit 2
$O/obj_base_mga/Vmga_base > $O/receipts/base-mga-newharness.log 2>&1
echo "media_grid_align (branch harness, base RTL) exit=$?"
cd $L/tb/verilator/chmap_capture || exit 2
verilator --cc --exe --build -j 8 --Mdir $O/obj_base_cmc --top-module chmap_wrap -Wall -Wno-fatal \
  -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-PINCONNECTEMPTY -Wno-UNUSEDPARAM \
  -CFLAGS "-std=c++17 -O2 -Wall -Wextra" $B/ieee1722/aaf/KL_chan_map_capture.sv \
  $B/ieee1722/aaf/KL_aaf_packetizer.sv $B/ieee1722/aaf/KL_tone_gen.sv chmap_wrap.sv sim_main.cpp \
  -o Vcmc_base > $O/receipts/base-cmc-build.log 2>&1 || exit 2
$O/obj_base_cmc/Vcmc_base > $O/receipts/base-cmc-newharness.log 2>&1
echo "chmap_capture (branch harness, base RTL) exit=$?"
