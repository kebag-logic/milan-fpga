#!/bin/sh
# Build and run tb/verilator/avtp_rxmon's NxN suite (the Makefile's NXFLAGS and
# NXSRCS, with -j 8 in place of -j 0). $1 = tree exported with
# `git archive HEAD hdl tb/verilator/avtp_rxmon` plus the gitlinked
# third_party/verilog-axis/rtl/axis_fifo.v; $2 = verilator.
set -eu
cd "$1/tb/verilator/avtp_rxmon"
R=../../../hdl; C=$R/common; A=$R/ieee1722/avtp
"$2" --cc --exe --build -j 8 --top-module avtp_rxmon_nx_wrap -GCLK_FREQ_HZ_P=100000 \
  +incdir+$C +incdir+$A -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
  -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-IMPORTSTAR -Wno-CASEINCOMPLETE -Wno-EOFNEWLINE \
  -Wno-PINCONNECTEMPTY -CFLAGS "-std=c++17 -O2 -Wall -Wextra" --Mdir obj_nx \
  $C/ethernet_packet_pkg.sv $A/avtp_subtype_pkg.sv $A/avtp_stream_parser.sv $A/KL_stream_table.sv \
  $A/KL_avtp_rx_monitor_ctx.sv $R/ieee1722/aaf/KL_aaf_rx_depacketizer.sv $R/ieee1722/aaf/KL_pcm_route.sv \
  ../../../third_party/verilog-axis/rtl/axis_fifo.v avtp_rxmon_nx_wrap.sv sim_main_nx.cpp \
  -o Vavtp_rxmon_nx_sim > build.log 2>&1
./obj_nx/Vavtp_rxmon_nx_sim
