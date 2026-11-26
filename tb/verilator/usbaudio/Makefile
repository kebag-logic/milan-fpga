# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
ifndef RTL_SIMULATOR
$(error Set RTL_SIMULATOR to the installed RTL simulation executable)
endif
JOBS ?= 2
MDIR ?= obj_dir
RTL ?= ../../../hdl/milan/usbaudio
SOURCES = $(RTL)/KL_usbaudio_record.sv $(RTL)/KL_usbaudio_status.sv \
          $(RTL)/KL_usbaudio_feedback.sv protocol_tb.sv
.PHONY: all build run
all: run
build:
	$(RTL_SIMULATOR) --binary --timing --top-module protocol_tb -Wall \
	  -Wno-TIMESCALEMOD --build-jobs $(JOBS) --Mdir $(abspath $(MDIR)) $(SOURCES)
run: build
	$(abspath $(MDIR))/Vprotocol_tb
