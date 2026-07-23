# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Digital audio loop: KL_aaf_packetizer (talker) -> parser -> KL_avtp_rx_monitor
# -> KL_aaf_rx_depacketizer (listener). Proves the recovered payload is
# bit-exact to the injected 1 kHz tone and measures its THD+N. Offline.
VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
C          = $(RTL_DIR)/common
A          = $(RTL_DIR)/ieee1722/avtp
F          = $(RTL_DIR)/ieee1722/aaf
TOP        = aaf_audio_loop_wrap

VFLAGS = --cc --exe --build -j 0 --top-module $(TOP) \
         +incdir+$(C) +incdir+$(A) +incdir+$(F) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-IMPORTSTAR -Wno-CASEINCOMPLETE \
         -Wno-EOFNEWLINE -Wno-PINCONNECTEMPTY -CFLAGS "-std=c++17 -O2"

SRCS = $(C)/ethernet_packet_pkg.sv $(A)/avtp_subtype_pkg.sv \
       $(F)/KL_aaf_packetizer.sv \
       $(A)/avtp_stream_parser.sv $(A)/KL_avtp_rx_monitor.sv \
       $(F)/KL_aaf_rx_depacketizer.sv \
       ../../../third_party/verilog-axis/rtl/axis_fifo.v \
       aaf_audio_loop_wrap.sv

.PHONY: all run clean
all: run
run:
	$(VERILATOR) $(VFLAGS) $(SRCS) sim_main.cpp -o Vaaf_audio_loop_sim
	./obj_dir/Vaaf_audio_loop_sim

clean:
	rm -rf obj_dir
