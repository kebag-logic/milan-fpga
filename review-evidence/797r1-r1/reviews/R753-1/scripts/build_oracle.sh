#!/bin/sh
# Build and run the milan_csr behavioural oracle at the shipping parameters.
# build_oracle.sh <repo-root> <work-dir> <verilator> <out-log> [extra -G ...]
set -eu
R=$1; W=$2; V=$3; L=$4; shift 4
HERE=$(dirname "$0")
python3 "$HERE/gen_oracle.py" "$R" "$W/sim.cpp"
"$V" --cc --exe --build -j 16 -Wno-fatal -Wno-lint --top-module milan_csr -Mdir "$W/obj" \
  +incdir+"$R/configs/generated/endstation_ax7101_1x1_tdm8" +incdir+"$R/hdl/common/csr" \
  -GNUM_QUEUES=5 -GADDR_WIDTH=16 -GN_LISTENERS_P=1 -GN_TALKERS_P=1 -GSRP_LSN0_ROW_P=2 -GGPTP_PLANE_EN_P=1 \
  -GMILAN_CLK_FREQ_HZ_P=50000000 -GCHMAP_RDBK_P=3 -GPPS_P=0 -GPPS_WIDTH_CYC_P=50000 "$@" \
  "$R/hdl/common/csr/milan_csr.sv" "$W/sim.cpp" -o Vor >"$W/build.log" 2>&1
"$W/obj/Vor" > "$L"
