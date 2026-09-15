# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# THE SHIPPING TDM8 MASTER RENDER LANE (issue #447), from a dynamic
# AUDIO_MAP command to the decoded serial pins, on the elaborated
# milan_datapath. Two elaborations: the shipping AX7101 1x1 TDM8 shape, and a
# generated TWO-STREAM shape where the epoch's stream-qualified bind-fall mask
# and the nonphysical in-range cluster key are observable at all.
#
#   make          - build and run both legs, then the leg's own defect arms
#   make tdm8render        - the shipping-shape leg alone
#   make tdm8render-multi  - the two-stream leg alone
#   make tdm8render-mutants
#                 - THE FULL MUTATION CAMPAIGN. Explicit, not part of the
#                   default target: it rebuilds the elaborated leg once per
#                   mutant and costs tens of minutes, which does not fit a PR
#                   shard's per-suite wall clock. #367/PR #385 settled the
#                   rule - nothing is shortened and no check is dropped, the
#                   long campaign becomes an opt-in target - and
#                   docs/testing/TESTING.md records who runs it.
#   make clean    - remove build artifacts
#
# WHY THIS IS ITS OWN SUITE DIRECTORY. These legs lived in tb/verilator/
# milan_dp, whose default target already carries the whole integration bank
# and measured 1037.7 s uncontended on a 16-CPU set - a 1.73x headroom under
# scripts/run_all_suites.sh's 1800 s per-suite guard, against a hosted
# slowdown that docs/testing/TESTING.md measures at up to 1.58x. The two legs
# add about 137 s, which takes that headroom to 1.53x and puts the suite over
# the hosted bar. Splitting them out is the milan_dp_gptp move of #367: every
# check stays, nothing is shortened, and the sweep discovers and shards this
# directory on its own with the default 1800 s budget.

VERILATOR ?= verilator
VERILATOR_JOBS ?= 0
RTL_DIR    = ../../../hdl
PP_DIR     = ../../../protocol-processor/hdl
CFG_DIR    = ../../../configs/generated
DP         = ../milan_dp

# ONE SOURCE LIST AND ONE FLAG SET, BOTH TAKEN FROM THE SUITE THAT OWNS THEM.
# tb/verilator/milan_dp exports the datapath source list (`print-srcs`, which
# tb/verilator/pp_shadow already consumes) and the elaboration flag set
# (`print-dp-vflags`). Copying either here would be a second hand-maintained
# statement of how this datapath is built, and the whole point of this leg is
# that it elaborates the SAME gateware the shipping shape's other legs do. The
# relative paths inside both are relative to a tb/verilator/<suite>/
# directory, which this is.
#
# TDMRM_SRC and DP_SRC are passed through EXPLICITLY rather than left to
# MAKEFLAGS: tdm8_render_mutants.py overrides them on the command line to
# elaborate a mutated copy through this same recipe, and a mutant that
# silently fell back to the tracked source would be a control that controls
# nothing.
TDMRM_SRC ?= $(RTL_DIR)/ieee1722/aaf/KL_tdm_render_master.sv
DP_SRC    ?= $(RTL_DIR)/milan/milan_datapath.sv
SRCS := $(shell $(MAKE) -s -C $(DP) print-srcs \
                TDMRM_SRC='$(TDMRM_SRC)' DP_SRC='$(DP_SRC)')
ifneq ($(.SHELLSTATUS),0)
$(error $(DP) print-srcs failed; the datapath source list could not be derived)
endif
DP_VFLAGS := $(shell $(MAKE) -s -C $(DP) print-dp-vflags)
ifneq ($(.SHELLSTATUS),0)
$(error $(DP) print-dp-vflags failed; the elaboration flag set could not be derived)
endif

# THE SHAPE THE AX7101 ACTUALLY FLASHES, named rather than inherited: an
# unnamed shape falls through to whichever config last ran --write-rtl (the
# milan_dp banner explains the cost at length).
SHAPE_AX1x1 = +incdir+$(CFG_DIR)/endstation_ax7101_1x1_tdm8
SHAPE_AX1_F = $(CFG_DIR)/endstation_ax7101_1x1_tdm8/gen/adp_shape_defaults.svh
GEN_CSR     = $(RTL_DIR)/common/csr/gen/lwsrp_csr_defaults.svh

# the shipping argv's own numbers (sw/litex/build.sh cfg_ax7101), and the
# render width that turns the parked lane into a live one - the shipping
# config's audio_interface.physical_channels.render.
AX_CHANS  = 8
AX_SLOTS  = 8
AX_I2SPB  = 0
AX_RENDER = 8

TDM8R_MDIR  ?= obj_tdm8r
TDM8R_SHAPE ?= $(SHAPE_AX1x1)
define TDM8R_BUILD
$(VERILATOR) $(TDM8R_SHAPE) $(DP_VFLAGS) --Mdir $(TDM8R_MDIR) \
  -GN_STREAMS=1 -GTALKER_WIRE_CHANS_P=$(AX_CHANS) \
  -GAUDIO_IF_SLOTS_P=$(AX_SLOTS) -GAUDIO_IF_MASTER_P=1 \
  -GAUDIO_IF_RENDER_SLOTS_P=$(AX_RENDER) \
  -GLOOPBACK_P=1 -GI2SPB_P=$(AX_I2SPB) -GLPF_P=0 \
  $(SRCS) sim_tdm8_render.cpp -o Vmilan_dp_tdm8r
endef

# THE SAME RENDER LANE ON A MULTI-STREAM SHAPE. gen_tdm8r_multi_shape.py
# writes a second end-station config (a second listener, the wire-truth
# cluster policy) and the REAL builder derives the shape header and the served
# entity image from it, exactly as for the shipping one. Same leg source, its
# multi-stream phase selected by -DTDM8R_MULTI_TB.
TDM8RM_GEN   = obj_tdm8rm_aem/endstation_tdm8r_multi
TDM8RM_MDIR  ?= obj_tdm8rm
TDM8RM_SHAPE ?= +incdir+$(TDM8RM_GEN)
define TDM8RM_BUILD
$(VERILATOR) $(TDM8RM_SHAPE) $(DP_VFLAGS) --Mdir $(TDM8RM_MDIR) \
  -GN_STREAMS=2 -GTALKER_WIRE_CHANS_P=$(AX_CHANS) \
  -GAUDIO_IF_SLOTS_P=$(AX_SLOTS) -GAUDIO_IF_MASTER_P=1 \
  -GAUDIO_IF_RENDER_SLOTS_P=$(AX_RENDER) \
  -GLOOPBACK_P=1 -GI2SPB_P=$(AX_I2SPB) -GLPF_P=0 \
  -CFLAGS "-DTDM8R_MULTI_TB=1 -Wall -Wextra" \
  $(SRCS) sim_tdm8_render.cpp -o Vmilan_dp_tdm8rm
endef

.PHONY: all run tdm8render tdm8render-build tdm8render-multi \
        tdm8render-multi-build tdm8render-mutants clean
.DEFAULT_GOAL := all
all: run

# The ACMP listener transition ROM and the AECP uCPU microcode are GENERATED,
# and the processor $$readmemh's them by the relative names below - so they
# must exist in the RUN directory, not just the build one.
ltn_rom.hex: $(PP_DIR)/acmp/rom/gen_ltn_rom.py
	python3 $< -o $@

ucode.hex: $(PP_DIR)/aecp/ucode/gen_ucode.py
	python3 $< -o $@

# ...and the entity image the leg's AECP face serves. The AECP uCPU validates
# this image before it enables the entity, so the leg cannot answer a map
# command without it. Built by the SAME two tools sw/litex loads at
# PP_DESC_BASE_P, from the tracked shipping config, so the map face under test
# is the one a board would serve. It sits in the RUN directory, shared by the
# clean leg and every mutant run.
tdm8r_aemi.bin: ../../../configs/endstation_ax7101_1x1_tdm8.yaml \
                ../../../sw/builder/endstation_builder.py \
                ../../../avdecc/gen_aemi_image.py
	python3 ../../../sw/builder/endstation_builder.py ../../../configs/endstation_ax7101_1x1_tdm8.yaml -o obj_tdm8r_aem
	python3 ../../../avdecc/gen_aemi_image.py --overlay obj_tdm8r_aem/endstation_ax7101_1x1_tdm8/aem_overlay.json --line-bytes 576 -o $@

# ...and the MULTI-STREAM shape's config, header and entity image. One builder
# invocation writes both the include directory the leg elaborates and the
# overlay its AECP face serves, so the two cannot describe different entities.
gen_tdm8r_multi/endstation_tdm8r_multi.yaml: gen_tdm8r_multi_shape.py \
                ../../../configs/endstation_ax7101_1x1_tdm8.yaml \
                ../../../sw/builder/endstation_builder.py
	python3 gen_tdm8r_multi_shape.py

tdm8rm_aemi.bin: gen_tdm8r_multi/endstation_tdm8r_multi.yaml \
                ../../../avdecc/gen_aemi_image.py
	python3 ../../../sw/builder/endstation_builder.py gen_tdm8r_multi/endstation_tdm8r_multi.yaml -o obj_tdm8rm_aem
	python3 ../../../avdecc/gen_aemi_image.py --overlay $(TDM8RM_GEN)/aem_overlay.json --line-bytes 576 -o $@

tdm8render: ltn_rom.hex ucode.hex tdm8r_aemi.bin $(GEN_CSR) $(SHAPE_AX1_F)
	$(TDM8R_BUILD)
	./$(TDM8R_MDIR)/Vmilan_dp_tdm8r

tdm8render-build: ltn_rom.hex ucode.hex tdm8r_aemi.bin $(GEN_CSR) $(SHAPE_AX1_F)
	$(TDM8R_BUILD)

tdm8render-multi: ltn_rom.hex ucode.hex tdm8rm_aemi.bin $(GEN_CSR)
	$(TDM8RM_BUILD)
	./$(TDM8RM_MDIR)/Vmilan_dp_tdm8rm

tdm8render-multi-build: ltn_rom.hex ucode.hex tdm8rm_aemi.bin $(GEN_CSR)
	$(TDM8RM_BUILD)

# THE DEFAULT TARGET. Both legs clean - which is the campaign's own positive
# control, taken here and immediately before it - and then the LEG-SIDE defect
# arms, which are the part of the campaign that needs no rebuild: each runs
# the clean binary in a mode that plants a defect in the STIMULUS rather than
# the gateware (a stopped render clock, one changed sample, a clock-source
# selection that names INTERNAL) and requires the leg to fail by a named
# check. That is an executable negative arm inside the sweep's wall clock; the
# gateware and generated-shape mutants, which each need their own
# elaboration, are the explicit tdm8render-mutants target below.
run: tdm8render tdm8render-multi
	@echo "======================================================================"
	python3 tdm8_render_mutants.py --leg-defects

# THE FULL CAMPAIGN, explicit. The two build prerequisites put the clean
# positive controls on disk first, where the runner's LEGS table looks for
# them, so an explicit invocation grades against the same binaries this suite
# built rather than rebuilding them a second time.
tdm8render-mutants: tdm8render-build tdm8render-multi-build
	@echo "======================================================================"
	@echo "---- #447 render lane: the same legs against mutated gateware and shape ----"
	python3 tdm8_render_mutants.py

clean:
	rm -rf ltn_rom.hex ucode.hex tdm8r_aemi.bin obj_tdm8r_aem tdm8rm_aemi.bin \
	       obj_tdm8rm_aem gen_tdm8r_multi obj_tdm8r obj_tdm8rm __pycache__
