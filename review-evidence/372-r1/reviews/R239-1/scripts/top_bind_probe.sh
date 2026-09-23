#!/bin/sh
# Reviewer probe: build the ORIGINAL ptp_ts `run` leg (ptp_ts_top + sim_main.cpp) with the
# #372 checker and bind added, --assert, and run it. Usage: run_probe.sh <tree> <verilator> <outdir>
set -u
TREE=$1; VL=$2; OUT=$3
S=$TREE/tb/verilator/ptp_ts
cd "$S" || exit 2
"$VL" --cc --exe --build -j 8 --assert --top-module ptp_ts_top \
  +incdir+../../../hdl/common +incdir+../../../hdl/ieee8021as/ptp_timestamp \
  -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC \
  -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY -Wno-IMPORTSTAR -Wno-CASEINCOMPLETE -Wno-EOFNEWLINE \
  -CFLAGS "-std=c++17 -O2" -Mdir "$OUT/obj" \
  ../../../hdl/common/ethernet_packet_pkg.sv ../../../hdl/common/axi_stream_if.sv \
  ../../../hdl/common/cdc_pulse.sv ../../../hdl/common/cdc_handshake.sv \
  ../../../hdl/common/axis_mux_rr_2in_1out.sv ../../../third_party/verilog-axis/rtl/axis_fifo.v \
  ../../../hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv ../../../hdl/ieee8021as/ptp_timestamp/ptp_csr_sync.sv \
  ../../../hdl/ieee8021as/ptp_timestamp/ptp_ts_core.sv ../../../hdl/ieee8021as/ptp_timestamp/ptp_ts_top.sv \
  ../../common/sva/axis_stream_source_sva.sv ../../common/sva/axis_mux_rr_2in_1out_sva.sv \
  ../../common/sva/axis_mux_rr_2in_1out_bind.sv \
  sim_main.cpp "$OUT/witness_stub.cpp" -o Vptp_ts_sva_probe > "$OUT/build.log" 2>&1
echo "build exit=$?"
"$OUT/obj/Vptp_ts_sva_probe" > "$OUT/run.log" 2>&1
echo "run exit=$?"
