# SPDX-License-Identifier: CERN-OHL-W-2.0
VERILATOR ?= verilator
VERILATOR_JOBS ?= 4
RTL = ../../../hdl
F = $(RTL)/ieee1722/aaf
A = $(RTL)/ieee1722/avtp
QUEUE_SRC ?= $(F)/KL_render_queue.sv
CAPTURE_SRC ?= $(F)/KL_chan_map_capture.sv
MDIR ?= obj_dir
STREAMS ?= 8
FIRST ?= 1
CHANNELS ?= 63
LEAD ?= 1
SRCS = $(RTL)/common/ethernet_packet_pkg.sv $(A)/avtp_subtype_pkg.sv \
 $(F)/KL_aaf_packetizer.sv $(A)/avtp_stream_parser.sv $(A)/KL_avtp_rx_monitor.sv \
 $(F)/KL_aaf_rx_depacketizer.sv $(QUEUE_SRC) $(CAPTURE_SRC) \
 ../../../third_party/verilog-axis/rtl/axis_fifo.v loopback_wrap.sv
.PHONY: all run one bounds clean
all: run one
one:
	$(MAKE) run STREAMS=1 FIRST=8 CHANNELS=8 LEAD=2 MDIR=$(MDIR)_one
clean:
	rm -rf $(MDIR) $(MDIR)_one
run:
	$(VERILATOR) --cc --exe --build -j $(VERILATOR_JOBS) --top-module loopback_wrap \
	 +incdir+$(RTL)/common +incdir+$(A) +incdir+$(F) --Mdir $(MDIR) -Wall -Wno-fatal -Werror-USERERROR -Wno-PINMISSING -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM \
	 -Wno-DECLFILENAME -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-IMPORTSTAR \
	 -GN_STREAMS_P=$(STREAMS) -GINPUT_FIRST_P=$(FIRST) -GINPUT_CH_P=$(CHANNELS) -GLEAD_P=$(LEAD) \
	 -CFLAGS "-std=c++17 -O2 -Wall -Wextra -DNSTREAMS=$(STREAMS) -DFIRST=$(FIRST) -DCHANNELS=$(CHANNELS) -DLEAD=$(LEAD)" \
	 $(SRCS) sim_main.cpp -o Vinput_loopback
	$(MDIR)/Vinput_loopback

bounds:
	python3 bounds.py --output $(MDIR)_bounds
