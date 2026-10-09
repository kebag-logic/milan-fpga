# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# #696 M4: source list and elaboration flags come from the datapath suite.
VERILATOR ?= verilator
VERILATOR_JOBS ?= 2
DP_MDIR ?= obj_integration
MAAP_RTL ?= ../../../hdl/ieee1722/maap/KL_maap.sv
DP_SRCS := $(shell $(MAKE) -s -C ../milan_dp print-srcs)
ifneq ($(.SHELLSTATUS),0)
$(error datapath source derivation failed)
endif
DP_FLAGS := $(shell $(MAKE) -s -C ../milan_dp print-dp-vflags)
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
