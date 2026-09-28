#!/usr/bin/env bash
# Reviewer probe R395-1: CRF lock phases around the walk-snapshot crossing.
# usage: run_zone.sh <clone> junction|junction-base|dp [D0 D1 DS]
#   junction       head crossbar, sim_main_zone.cpp, phases D0..D1 step DS
#   junction-base  the same harness against <base-rtl>/KL_chan_map_capture.sv
#                  (BASE_RTL env var), the wrapper's TDM_FRAME_PAIRS_P line dropped
#   dp             whole milan_datapath, sim_dp_zone.cpp (64 phases)
# Works in an untracked copy tb/verilator/r395_probe_zone, removed on exit.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
clone="$1"; mode="$2"; d0="${3:-4050}"; d1="${4:-4140}"; ds="${5:-2}"
w="$clone/tb/verilator/r395_probe_zone"
trap 'rm -rf "$w"' EXIT
rm -rf "$w"; cp -r "$clone/tb/verilator/capture_coherence" "$w"; rm -rf "$w/obj_dir" "$w/obj_dp"
cp "$here/sim_main_zone.cpp" "$w/sim_main.cpp"; cp "$here/sim_dp_zone.cpp" "$w/sim_dp.cpp"
cd "$w"
V="--cc --exe --build -j 0 --top-module coherence_wrap -GCLK_HZ_P=50000000 -GN_TALKERS_P=1 -GWIRE_CHANS_P=8 -GTDM_SLOTS_P=8 -GLB_STREAMS_P=1 -GLB_CH_P=8 -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY"
C="-std=c++17 -O2 -DCLK_HZ_TB=50000000 -DWIRE_CHANS_TB=8 -DTDM_SLOTS_TB=8 -DR395_D0=$d0 -DR395_D1=$d1 -DR395_DS=$ds"
case "$mode" in
  junction)
    make -s build VFLAGS="$V -CFLAGS \"$C\"" >/dev/null; ./obj_dir/Vcoherence_sim || true ;;
  junction-base)
    sed -i '/\.TDM_FRAME_PAIRS_P (TDM_SLOTS_P \/ 2),/d' coherence_wrap.sv
    make -s build CMAP_SRC="${BASE_RTL:?}/KL_chan_map_capture.sv" VFLAGS="$V -CFLAGS \"$C\"" >/dev/null
    ./obj_dir/Vcoherence_sim || true ;;
  dp)
    make -s dp-build DP_MDIR=obj_dp >/dev/null; ./obj_dp/Vcoherence_dp || true ;;
esac
