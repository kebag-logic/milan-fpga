# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# milan_datapath graded as a SUBSTITUTION harness: the protocol processor is
# THE control plane and it owns the wire.
#
# THE PREMISE INVERTED (2026-08-13). This suite used to elaborate the processor
# as a SHADOW (PP_PLANE_P=1, tx_drain_i=1) beside a live legacy 1722.1/SRP
# plane, and its safety property was "the processor transmits NOTHING". That
# plane is DELETED: milan_datapath instantiates KL_pp_shadow unconditionally,
# drives tx_drain_i to 0 and merges the processor's packed TX with MAAP through
# ctl_tx_mux. So the property is the OPPOSITE now - the processor's frames MUST
# reach the MAC TX boundary, and they must share the lane with MAAP without
# corrupting either. What is unchanged is the reason the suite exists: it is the
# only place the class-D fabric face is graded as a LIVE face.
#
# The parity story is gone with the option. milan_dp does not prove an "OFF
# side" any more - there is no off side - it elaborates the SAME plane in nine
# shapes and grades the data path around it. This suite grades the control
# plane's own egress and its class-D outputs.
#
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

# TIME COMPRESSION: 1 us = 1 clk, 1 ms = 100 clk (the tb/pp_top ratio). The ADP
# advertise cadence is seconds of REAL time; at silicon rates this suite would
# need 10^9 cycles to see a single ENTITY_AVAILABLE attempt. Both values feed
# the gateware only — the C++ side is told the ratio by -D so the two cannot
# drift into disagreeing about what a millisecond is.
TIM_G  = -GPP_TIM_DIV_US_P=1 -GPP_TIM_DIV_MS_P=100
TIM_D  = -DPP_MS_CYCLES=100

# ONE GRID: KL_maap keeps its own millisecond (CLK_FREQ_HZ_P/1000 cycles), and
# the MAAP claim walk is 3 probes x ~500 ms - 1.5e8 cycles at a real 100 MHz,
# which no harness can run, so addr_valid_o would never assert and the shim
# would never be reachable. MAAP_CLK_HZ_P = 100 kHz makes ONE MAAP millisecond
# 100 cycles, which is EXACTLY the processor's compressed millisecond above
# (TIM_DIV_US_P=1, TIM_DIV_MS_P=100). Two planes on two different compressed
# millisecond scales would be a harness that measures its own arithmetic.
MAAP_G = -GMAAP_CLK_HZ_P=100000
MAAP_D = -DMAAP_MS_CYCLES=100

# THE TALKER SOURCE ENABLE IS NO LONGER A -G. KL_pp_shadow's SRC_EN_MASK_P
# parameter is deleted; milan_datapath drives cfg_src_en_i from the ENTITY
# SHAPE ({ACMP_SRC_C{1'b1}} - every declared STREAM_OUTPUT enabled, and no
# other index). So the maap face and the DA gate are reachable on every build
# of every shape, and there is no "no source enabled" arm left to elaborate.

# NO -Wno-* ANYWHERE, WARNINGS ARE ERRORS (USER 2026-08-12).
#
# There is no global `-Werror` in Verilator (only per-rule `-Werror-<CODE>`),
# and it does not need one: warnings are FATAL BY DEFAULT — `-Wno-fatal` is the
# flag that turns that off. So removing every -Wno-*, `-Wno-fatal` first, IS
# the -Werror build. Any warning here stops the build with
# "Exiting due to N warning(s)" and a non-zero exit.
#
# Waivers for VENDORED and PINNED code live in waivers.vlt, scoped to the one
# rule and the one file that earn them. That is different in kind from a global
# -Wno-X, which would silence the same finding in RTL we wrote.
# This is the control-processor substitution harness, so it states the retained
# gPTP-off comparison shape explicitly. The default-on gPTP lane and its lane-4
# diagnostics are exercised by milan_dp/sim_gptp.cpp.
VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         +incdir+$(RTL_DIR)/common +incdir+$(RTL_DIR)/common/csr +incdir+$(RTL_DIR)/common/eth_event_counter \
         +incdir+$(RTL_DIR)/ieee17221/adp +incdir+$(RTL_DIR)/ieee8021q/ts \
         +incdir+$(RTL_DIR)/ieee8021as/ptp_timestamp +incdir+$(AXIS_DIR) \
         -Wall waivers.vlt \
         -GPB_PREFILL_C=2 -GCLKV_QTICK_CYC_P=4096 -GLDIAG_IVAL_CYC_P=256 \
         -GGPTP_PLANE_EN_P=0 \
         $(TIM_G) $(MAAP_G) \
         -CFLAGS "-std=c++17 -O2 $(TIM_D) $(MAAP_D)"

# ONE SOURCE LIST, AND IT ALREADY CONTAINS THE PROCESSOR. milan_dp's SRCS now
# begins with the protocol-processor sources plus KL_pp_shadow/KL_pp_maap_shim,
# because the processor IS part of the datapath. So this suite must NOT keep a
# PP_SRCS of its own: naming those files twice on one verilator command line is
# a duplicate module definition (MODDUP), and with warnings fatal here that is a
# build failure, not a nuisance.
DP_SRCS := $(shell $(MAKE) -s -C ../milan_dp print-srcs)

CPP = sim_main.cpp

.PHONY: all run clean
all: run

# The ACMP listener transition ROM is GENERATED, and protocol_processor_top
# $readmemh's it by the relative name below — so it must exist in the RUN
# directory, not just the build one.
ltn_rom.hex: $(PP_DIR)/acmp/rom/gen_ltn_rom.py
	python3 $< -o $@

# ...and the AECP uCPU microcode image, same relative-$$readmemh contract
# (KL_aecp_engine's UCODE_HEX_P defaults to the bare name "ucode.hex").
#
# THIS RULE WAS MISSING until 2026-08-13, and the cost was exactly the class of
# false green this suite exists to prevent: Verilated $readmem prints
# "%Warning: ucode.hex:0: $$readmem file not found" and CARRIES ON with an
# all-zero ROM, so the AECP engine ran a microcode image of nothing while the
# suite exited 0. A warning on a suite that carries no -Wno-* is a failure of
# this suite's own posture, and the section [L] checks below cannot mean
# anything without the real image.
ucode.hex: $(PP_DIR)/aecp/ucode/gen_ucode.py
	python3 $< -o $@

# THE PACKAGE-COLLISION PREFLIGHT IS GONE (2026-08-13), and the README says why:
# it guarded against this repository and the protocol-processor both declaring
# adp_pkg / acmp_pkg. hdl/ieee17221/adp/adp_pkg.sv and
# hdl/ieee17221/acmp/acmp_pkg.sv are DELETED with the plane they belonged to, so
# the consumer side of the collision set is permanently empty and the guard can
# never fire again. A check that cannot fail is not a check.
run: ltn_rom.hex ucode.hex $(GEN_ALL)
	$(VERILATOR) $(SHAPE_1x1) $(VFLAGS) $(DP_SRCS) $(CPP) -o Vpp_shadow_sim
	./obj_dir/Vpp_shadow_sim

clean:
	rm -rf obj_dir ltn_rom.hex ucode.hex
