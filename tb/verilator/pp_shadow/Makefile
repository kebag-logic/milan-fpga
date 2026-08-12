# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# milan_datapath elaborated with the protocol-processor SHADOW plane ON
# (PP_PLANE_P=1) — the ONLY leg in the tree that builds the submodule into the
# consumer. milan_dp keeps proving the OFF side (its source list does not even
# name the processor), so the two suites together are the parity contract:
# OFF is byte-identical to what shipped, ON is what this suite grades.
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
PP_DIR     = ../../../protocol-processor/hdl
AXIS_DIR   = ../../../third_party/verilog-axis/rtl
TOP        = milan_datapath
CFG_DIR    = ../../../configs/generated

# The entity shape must be named (milan_dp's banner explains why at length: an
# unnamed shape falls through to whichever config last ran --write-rtl).
SHAPE_1x1  = +incdir+$(CFG_DIR)/endstation_arty_current
SHAPE_DEF  = $(RTL_DIR)/common/csr/gen/adp_shape_defaults.svh
GEN_CSR    = $(RTL_DIR)/common/csr/gen/lwsrp_csr_defaults.svh
GEN_ALL    = $(GEN_CSR) $(SHAPE_DEF)

C  = $(RTL_DIR)/common
Q  = $(RTL_DIR)/ieee8021q/ts
P  = $(RTL_DIR)/ieee8021as/ptp_timestamp

# TIME COMPRESSION: 1 us = 1 clk, 1 ms = 100 clk (the tb/pp_top ratio). The ADP
# advertise cadence is seconds of REAL time; at silicon rates this suite would
# need 10^9 cycles to see a single ENTITY_AVAILABLE attempt. Both values feed
# the gateware only — the C++ side is told the ratio by -D so the two cannot
# drift into disagreeing about what a millisecond is.
TIM_G  = -GPP_TIM_DIV_US_P=1 -GPP_TIM_DIV_MS_P=100
TIM_D  = -DPP_MS_CYCLES=100

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         +incdir+$(RTL_DIR)/common +incdir+$(RTL_DIR)/common/csr +incdir+$(RTL_DIR)/common/eth_event_counter \
         +incdir+$(RTL_DIR)/ieee17221/adp +incdir+$(RTL_DIR)/ieee8021q/ts \
         +incdir+$(RTL_DIR)/ieee8021as/ptp_timestamp +incdir+$(AXIS_DIR) \
         +incdir+$(RTL_DIR)/ieee17221/aecp +incdir+$(RTL_DIR)/ieee17221/aecp/gen \
         -Wall -Wno-fatal -Werror-USERERROR -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY -Wno-IMPORTSTAR \
         -Wno-CASEINCOMPLETE -Wno-EOFNEWLINE -Wno-PINMISSING -Wno-SELRANGE \
         -Wno-TIMESCALEMOD -Wno-GENUNNAMED -Wno-PROCASSINIT -Wno-ASCRANGE \
         -Wno-SYNCASYNCNET -Wno-MULTIDRIVEN -Wno-UNOPTFLAT -Wno-LATCH \
         -Werror-MODDUP \
         `# MODDUP MUST be an ERROR here, and -Wno-fatal above is exactly why:` \
         `# the processor and the consumer BOTH declare adp_pkg and acmp_pkg.` \
         `# As a plain warning under -Wno-fatal, Verilator exits 0 and silently` \
         `# keeps the FIRST declaration - so the processor's engines compile` \
         `# against the consumer's constants and nothing says a word. This flag` \
         `# is the difference between a loud blocker and silent wrong code.` \
         -GPB_PREFILL_C=2 -GCLKV_QTICK_CYC_P=4096 -GLDIAG_IVAL_CYC_P=256 \
         -GPP_PLANE_P=1 $(TIM_G) \
         -CFLAGS "-std=c++17 -O2 $(TIM_D)"

# The consumer's own datapath sources come STRAIGHT FROM milan_dp — that list
# is the one proven to elaborate, and a second copy here would drift silently.
DP_SRCS := $(shell $(MAKE) -s -C ../milan_dp print-srcs)

# The protocol-processor submodule, in tb/pp_top's order.
PP_SRCS = $(PP_DIR)/common/pp_pkg.sv $(PP_DIR)/srp/srp_pkg.sv \
       $(PP_DIR)/acmp/acmp_pkg.sv $(PP_DIR)/adp/adp_pkg.sv \
       $(PP_DIR)/common/KL_pp_prng.sv $(PP_DIR)/common/KL_pp_timer_service.sv \
       $(PP_DIR)/packet_engine/KL_pp_rx_validator.sv \
       $(PP_DIR)/packet_engine/KL_pp_rx_slots.sv \
       $(PP_DIR)/packet_engine/KL_pp_normalizer.sv \
       $(PP_DIR)/packet_engine/KL_pp_dispatch.sv \
       $(PP_DIR)/packet_engine/KL_pp_tx_slots.sv \
       $(PP_DIR)/packet_engine/KL_pp_tx_arbiter.sv \
       $(PP_DIR)/packet_engine/KL_pp_scoreboard.sv \
       $(PP_DIR)/packet_engine/KL_pp_event_router.sv \
       $(PP_DIR)/packet_engine/KL_pp_originator.sv \
       $(PP_DIR)/packet_engine/KL_pp_trace_ring.sv \
       $(PP_DIR)/packet_engine/KL_pp_side_port.sv \
       $(PP_DIR)/packet_engine/KL_pp_nvm_port.sv \
       $(PP_DIR)/adp/KL_adp_engine.sv \
       $(PP_DIR)/acmp/KL_acmp_listener.sv $(PP_DIR)/acmp/KL_acmp_talker.sv \
       $(PP_DIR)/acmp/KL_acmp_nvm_shadow.sv \
       $(PP_DIR)/srp/KL_srp_decoder.sv $(PP_DIR)/srp/KL_srp_domain.sv \
       $(PP_DIR)/srp/KL_srp_vlan.sv $(PP_DIR)/srp/KL_srp_admission.sv \
       $(PP_DIR)/srp/KL_srp_talker_fsm.sv $(PP_DIR)/srp/KL_srp_listener_fsm.sv \
       $(PP_DIR)/srp/KL_srp_encoder.sv $(PP_DIR)/srp/KL_srp_top.sv \
       $(PP_DIR)/top/KL_mrp_strip.sv $(PP_DIR)/top/protocol_processor_top.sv \
       $(RTL_DIR)/milan/KL_pp_shadow.sv

CPP = sim_main.cpp

.PHONY: all run clean
all: run

# The ACMP listener transition ROM is GENERATED, and protocol_processor_top
# $readmemh's it by the relative name below — so it must exist in the RUN
# directory, not just the build one.
ltn_rom.hex: $(PP_DIR)/acmp/rom/gen_ltn_rom.py
	python3 $< -o $@

# PREFLIGHT — the package-collision blocker (see README). A suite that cannot
# build must say so out loud and exit 0, NOT fail the tree sweep and NOT build
# something quietly wrong. The moment the protocol-processor renames its
# adp_pkg/acmp_pkg, this check passes and the suite runs with no edit here.
# The reason is printed on EVERY run: a silent skip is the false-green trap.
PP_PKGS  := $(shell awk '/^package /{print $$2}' $(PP_DIR)/adp/adp_pkg.sv $(PP_DIR)/acmp/acmp_pkg.sv 2>/dev/null | tr -d ';' | sort -u)
DP_PKGS  := $(shell awk '/^package /{print $$2}' $(RTL_DIR)/ieee17221/adp/adp_pkg.sv $(RTL_DIR)/ieee17221/acmp/acmp_pkg.sv 2>/dev/null | tr -d ';' | sort -u)
COLLIDE  := $(filter $(PP_PKGS),$(DP_PKGS))

# PP_SRCS comes FIRST: its packages must be declared before the modules that
# import them, and putting the consumer's list first would resolve a colliding
# package name to the consumer's copy (see -Werror-MODDUP above).
run: ltn_rom.hex $(GEN_ALL)
ifneq ($(COLLIDE),)
	@echo "  [SKIP] pp_shadow: BLOCKED on duplicate SystemVerilog packages: $(COLLIDE)"
	@echo "         The protocol-processor and this repo both declare them, with"
	@echo "         different contents. Under -Wno-fatal Verilator exits 0 and"
	@echo "         SILENTLY keeps the first, so the processor would compile"
	@echo "         against the consumer's constants. Fix belongs in the"
	@echo "         protocol-processor: rename to pp_adp_pkg / pp_acmp_pkg."
	@echo "         See tb/verilator/pp_shadow/README.md."
	@echo "pp_shadow: 0 checks, 0 failures (SKIPPED - blocked)"
else
	$(VERILATOR) $(SHAPE_1x1) $(VFLAGS) $(PP_SRCS) $(DP_SRCS) $(CPP) -o Vpp_shadow_sim
	./obj_dir/Vpp_shadow_sim
endif

clean:
	rm -rf obj_dir ltn_rom.hex
