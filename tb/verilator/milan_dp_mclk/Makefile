# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# MEDIA-CLOCK FOLLOWING AT THE ROOT (#629): the milan_datapath rows of
# docs/design/MEDIA_CLOCK_FOLLOWING.md's test plan, on the elaborated
# datapath at the TRUE audio clock ratio with the MMCM's fine phase shift
# modelled, so the servo closes its loop through the real decode, reference
# mux, AAF clock meter, restart request and counters.
#
#   make          - build the leg and its mutant schemata, then run the leg
#                   and every named mutant (mclk_mutants.py)
#   make mclk     - the leg alone
#   make clean    - remove build artifacts
#
# WHY ITS OWN SUITE DIRECTORY. tb/verilator/milan_dp's default target already
# runs most of its 3600 s guard on hosted runners (docs/testing/
# CI_WORKFLOWS.md), and this leg follows talkers for tens of simulated
# seconds. The milan_dp_render move of #447 applies: one more directory the
# sweep discovers and shards with the default 1800 s budget.
#
# THE CLOCKS. The fabric runs at MCLK_HZ = 4 MHz (PTP_INCR 250 ns, the
# smallest whole-ns tick Q8.24 holds is 255 ns), the audio clock at the
# shipping plan, 100 MHz x 391/1591, so the TDM frame and the packet grid
# keep their real 48 kHz relation. Everything the media plane derives from
# the fabric clock is derived from MILAN_CLK_FREQ_HZ, never restated.

VERILATOR ?= verilator
VERILATOR_JOBS ?= 0
RTL_DIR = ../../../hdl
PP_DIR  = ../../../protocol-processor/hdl
DP      = ../milan_dp

MCLK_HZ = 4000000

# ONE SOURCE LIST AND ONE FLAG SET, taken from the suite that owns them (the
# milan_dp_render rule). Three files are substituted in the exported list:
#   * KL_ptp_clock_validity by clkv_double.sv, the tu test double (its
#     banner says why);
#   * the datapath, the AAF clock meter and milan_csr by MUT_DP_SRC,
#     MUT_AAFM_SRC and MUT_CSR_SRC when mclk_mutants.py elaborates its
#     mutant schemata through this same recipe. A mutant that silently fell
#     back to the tracked source would be a control that controls nothing,
#     so the overrides are substituted, never appended.
# --no-print-directory: both lists are the nested make's stdout, and a print-
# directory flag it inherits would write "Entering directory" into them. GNU
# make 4.3 hands a `make -C` recipe MAKEFLAGS=w, which reaches the nested
# `make mclk-build` mclk_mutants.py runs: on the hosted runner the schemata
# then failed to elaborate and the campaign never ran (#629 R432-1 F2, the
# defect #617 R394-3 F1 fixed in tb/verilator/capture_coherence).
# MAKEFLAGS= for the same reason, wider: GNU make 4.4 also exports its own
# flags to $(shell), so `make -pqrR` (scripts/shape_consumer_inventory.py's
# database read) ran the nested make in question mode, print-srcs failed
# and the parse stopped at the $(error) below with no rule read (#629
# R433-2 F1). The nested make takes no flag from this one.
DP_RTL   = $(RTL_DIR)/milan/milan_datapath.sv
AAFM_RTL = $(RTL_DIR)/ieee1722/crf/KL_aaf_clock_meter.sv
CSR_RTL  = $(RTL_DIR)/common/csr/milan_csr.sv
CLKV_RTL = $(RTL_DIR)/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv
MUT_DP_SRC   ?= $(DP_RTL)
MUT_AAFM_SRC ?= $(AAFM_RTL)
MUT_CSR_SRC  ?= $(CSR_RTL)
SRCS_DP := $(shell MAKEFLAGS= $(MAKE) -s --no-print-directory -C $(DP) print-srcs)
ifneq ($(.SHELLSTATUS),0)
$(error $(DP) print-srcs failed; the datapath source list could not be derived)
endif
SRCS := $(patsubst $(CLKV_RTL),clkv_double.sv,\
        $(patsubst $(DP_RTL),$(MUT_DP_SRC),\
        $(patsubst $(AAFM_RTL),$(MUT_AAFM_SRC),\
        $(patsubst $(CSR_RTL),$(MUT_CSR_SRC),$(SRCS_DP)))))
DP_VFLAGS := $(shell MAKEFLAGS= $(MAKE) -s --no-print-directory -C $(DP) print-dp-vflags)
ifneq ($(.SHELLSTATUS),0)
$(error $(DP) print-dp-vflags failed; the elaboration flag set could not be derived)
endif

# THE TWO-LISTENER SHAPE (gen_mclk_shape.py): the shipping AX7101 TDM8 config
# with a second listener, through the real builder. The shipping argv's own
# numbers otherwise (sw/litex/build.sh cfg_ax7101).
MCLK_GEN = obj_mclk_aem/endstation_mclk
MCLK_HDR = $(MCLK_GEN)/gen/adp_shape_defaults.svh
GEN_CSR  = $(RTL_DIR)/common/csr/gen/lwsrp_csr_defaults.svh
AX_CHANS = 8
AX_SLOTS = 8

MCLK_MDIR ?= obj_mclk
MCLK_CFLAGS ?= -O3
define MCLK_BUILD
$(VERILATOR) +incdir+$(MCLK_GEN) $(DP_VFLAGS) --Mdir $(MCLK_MDIR) \
  -GMILAN_CLK_FREQ_HZ=$(MCLK_HZ) \
  -GN_STREAMS=2 -GTALKER_WIRE_CHANS_P=$(AX_CHANS) \
  -GAUDIO_IF_SLOTS_P=$(AX_SLOTS) -GAUDIO_IF_MASTER_P=1 \
  -GLOOPBACK_P=1 -GI2SPB_P=0 -GLPF_P=0 \
  -CFLAGS "-DMCLK_HZ_TB=$(MCLK_HZ) $(MCLK_CFLAGS) -Wall -Wextra" \
  $(SRCS) sim_mclk.cpp -o Vmilan_dp_mclk
endef

.PHONY: all run mclk mclk-build clean
.DEFAULT_GOAL := all
all: run

# The ACMP listener transition ROM and the AECP uCPU microcode are GENERATED,
# and the processor $$readmemh's them by the relative names below, so they
# must exist in the RUN directory.
ltn_rom.hex: $(PP_DIR)/acmp/rom/gen_ltn_rom.py
	python3 $< -o $@

ucode.hex: $(PP_DIR)/aecp/ucode/gen_ucode.py
	python3 $< -o $@

gen_mclk/endstation_mclk.yaml: gen_mclk_shape.py \
                ../milan_dp_render/gen_tdm8r_multi_shape.py \
                ../../../configs/endstation_ax7101_1x1_tdm8.yaml \
                ../../../sw/builder/endstation_builder.py
	python3 gen_mclk_shape.py

$(MCLK_HDR): gen_mclk/endstation_mclk.yaml
	python3 ../../../sw/builder/endstation_builder.py gen_mclk/endstation_mclk.yaml -o obj_mclk_aem
	python3 gen_mclk_shape.py --check-header $@

mclk-build: ltn_rom.hex ucode.hex $(MCLK_HDR) $(GEN_CSR)
	$(MCLK_BUILD)

mclk: mclk-build
	./$(MCLK_MDIR)/Vmilan_dp_mclk

# THE DEFAULT TARGET: the leg and the campaign together. mclk_mutants.py runs
# the clean leg's full sequence and every mutant's short leg as one pool, so
# the campaign shares the suite's wall clock instead of following it.
run: mclk-build
	python3 mclk_mutants.py

clean:
	rm -rf ltn_rom.hex ucode.hex gen_mclk obj_mclk_aem obj_mclk obj_mclk_mut \
	       __pycache__
