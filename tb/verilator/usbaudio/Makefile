# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
RTL_SIMULATOR ?= verilator
JOBS ?= 2
MDIR ?= obj_dir
RTL ?= ../../../hdl/milan/usbaudio
SOURCES = $(RTL)/KL_usbaudio_record.sv $(RTL)/KL_usbaudio_status.sv \
          $(RTL)/KL_usbaudio_feedback.sv protocol_tb.sv
.PHONY: all build run duplex-build duplex
all: check
check:
	python3 -B check.py --engine "$(RTL_SIMULATOR)" --out "$(abspath $(MDIR))" --jobs $(JOBS) \
	  $(if $(CLEANUP_LEDGER),--cleanup-ledger "$(CLEANUP_LEDGER)",)
build:
	$(RTL_SIMULATOR) --binary --timing --top-module protocol_tb -Wall \
	  -Wno-TIMESCALEMOD --build-jobs $(JOBS) --Mdir $(abspath $(MDIR)) $(SOURCES)
run: build
	$(abspath $(MDIR))/Vprotocol_tb

WINDOW_LOG2 ?= 13
duplex-build:
	$(RTL_SIMULATOR) --cc --exe --build --top-module KL_usbaudio_bridge \
	  -Wall -Wno-fatal -Wno-TIMESCALEMOD --build-jobs $(JOBS) \
	  -GWINDOW_LOG2_P=$(WINDOW_LOG2) -CFLAGS "-O3 -std=c++17 -Wall -Wextra -DWINDOW_LOG2_TB=$(WINDOW_LOG2)" \
	  --Mdir $(abspath $(MDIR)) \
	  $(wildcard $(RTL)/*.sv) ../../../third_party/verilog-axis/rtl/axis_async_fifo.v \
	  $(abspath duplex.cpp)
duplex: duplex-build
	$(abspath $(MDIR))/VKL_usbaudio_bridge

reference-build:
	$(RTL_SIMULATOR) --binary --timing --top-module reference_tb -Wall \
	  -Wno-fatal -Wno-TIMESCALEMOD --build-jobs $(JOBS) --Mdir $(abspath $(MDIR)) \
	  $(RTL)/KL_usbaudio_record.sv $(RTL)/KL_usbaudio_ingress.sv \
	  $(RTL)/KL_usbaudio_reference.sv $(RTL)/KL_usbaudio_feedback.sv reference_tb.sv
reference: reference-build
	$(abspath $(MDIR))/Vreference_tb

STORAGE_BITS ?= 32
storage-build:
	$(RTL_SIMULATOR) --binary --timing --top-module storage_tb -GWIDTH_P=$(STORAGE_BITS) \
	  -Wall -Wno-fatal -Wno-TIMESCALEMOD --build-jobs $(JOBS) --Mdir $(abspath $(MDIR)) \
	  ../../../hdl/ieee1722/aaf/KL_chan_map_capture.sv \
	  ../../../hdl/ieee1722/aaf/KL_aaf_packetizer.sv storage_tb.sv
storage: storage-build
	$(abspath $(MDIR))/Vstorage_tb

packet-build:
	$(RTL_SIMULATOR) --binary --timing --top-module packet_tb -Wall \
	  -Wno-fatal -Wno-TIMESCALEMOD --build-jobs $(JOBS) --Mdir $(abspath $(MDIR)) \
	  $(RTL)/KL_usbaudio_packet.sv packet_tb.sv
packet: packet-build
	$(abspath $(MDIR))/Vpacket_tb

gpif-build:
	$(RTL_SIMULATOR) --binary --timing --top-module gpif_tb -Wall \
	  -Wno-fatal -Wno-TIMESCALEMOD --build-jobs $(JOBS) --Mdir $(abspath $(MDIR)) \
	  $(RTL)/KL_usbaudio_gpif.sv $(RTL)/KL_usbaudio_reset.sv gpif_tb.sv
gpif: gpif-build
	$(abspath $(MDIR))/Vgpif_tb

media-build:
	$(RTL_SIMULATOR) --binary --timing --top-module media_tb -Wall \
	  -Wno-fatal -Wno-TIMESCALEMOD --build-jobs $(JOBS) --Mdir $(abspath $(MDIR)) \
	  $(RTL)/KL_usbaudio_media.sv media_tb.sv
media: media-build
	$(abspath $(MDIR))/Vmedia_tb
