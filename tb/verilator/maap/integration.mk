# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# #696 M4: source list and elaboration flags come from the datapath suite.
VERILATOR ?= verilator
VERILATOR_JOBS ?= 2
DP_MDIR ?= obj_integration
MAAP_RTL ?= ../../../hdl/ieee1722/maap/KL_maap.sv
# MAKEFLAGS= : GNU make 4.3 (the hosted runner) leaks "Entering directory" lines into a
# $(shell) capture under an inherited w flag inside a recursive -j parent, even with
# --no-print-directory; the sibling suites (milan_dp_mclk, milan_dp_render, pp_shadow)
# clear the inherited flags the same way. The job bound is passed explicitly.
DP_SRCS := $(shell MAKEFLAGS= $(MAKE) -s --no-print-directory -C ../milan_dp print-srcs)
ifneq ($(.SHELLSTATUS),0)
$(error datapath source derivation failed)
endif
ifeq ($(strip $(DP_SRCS)),)
$(error datapath source list is empty)
endif
ifneq ($(filter-out $(wildcard $(DP_SRCS)),$(DP_SRCS)),)
$(error datapath source list names non-files: $(firstword $(filter-out $(wildcard $(DP_SRCS)),$(DP_SRCS))))
endif
DP_FLAGS := $(shell MAKEFLAGS= $(MAKE) -s --no-print-directory -C ../milan_dp print-dp-vflags VERILATOR_JOBS=$(VERILATOR_JOBS))
ifneq ($(.SHELLSTATUS),0)
$(error datapath flag derivation failed)
endif
SRCS = $(subst ../../../hdl/ieee1722/maap/KL_maap.sv,$(MAAP_RTL),$(DP_SRCS))
.PHONY: build
build:
	mkdir -p $(DP_MDIR)
	python3 ../../../protocol-processor/hdl/acmp/rom/gen_ltn_rom.py -o $(DP_MDIR)/ltn_rom.hex
	python3 ../../../protocol-processor/hdl/aecp/ucode/gen_ucode.py -o $(DP_MDIR)/ucode.hex
	$(VERILATOR) +incdir+../../../configs/generated/endstation_ax7101_1x1_tdm8 \
	  $(DP_FLAGS) --Mdir $(DP_MDIR) -GMAAP_CLK_HZ_P=10000 \
	  -GN_STREAMS=1 -GTALKER_WIRE_CHANS_P=8 -GAUDIO_IF_SLOTS_P=8 \
	  -GAUDIO_IF_MASTER_P=1 -GLOOPBACK_P=1 -GI2SPB_P=0 -GLPF_P=0 \
	  $(SRCS) sim_integration.cpp -o maap_integration
