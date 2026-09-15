# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# The gPTP egress timestamp closed loop (issue #360): the real donor engine,
# the real plane and ledger, the real PHC, the real launch observer, the real
# link guard, the real merge arbiter and the SHIPPING MAC TRANSMIT CHAIN
# converted from the product's own migen source.
#
# The generated chain is REGENERATED AND COMPARED before the build, so a
# stale artifact is a red rather than a wrong answer. That needs the pinned
# LiteX interpreter; $MILAN_LITEX_PYTHON names it, as in every other consumer
# of that stack in this tree.
VERILATOR ?= verilator
#: The interpreter that carries the pinned LiteX stack, named the way every
#: other consumer of that stack in this tree names it. Plain `python3` still
#: CHECKS the artifact - against the product source region it was converted
#: from, its pins and its own bytes - and says which level it ran.
MILAN_LITEX_PYTHON ?= python3
RTL_DIR    = ../../../hdl
GPTP_DIR   = ../../../gptp-processor
AXIS_DIR   = ../../../third_party/verilog-axis/rtl
GEN_DIR    = generated
TOP        = gptp_txts_wrap

#: The engine's own timers are generated for a faster second so a protocol
#: run fits in a simulation. The TIMESTAMP arithmetic is unaffected: the
#: plane is told the product's 20 ns PHC tick and 8 ns observation tick, and
#: the correction this bench grades is therefore the product's own 426 ns.
#: Two megahertz is the floor the donor's own microsecond divider sets
#: (US_DIV_C = clk/1e6 must be at least two), and it is what the plane-slice
#: suite already generates, so both suites drive one engine image shape.
ENGINE_CLK_HZ = 2000000

#: migen writes combinational blocks with `<=`, compares a last_be field
#: against a constant that its own generate-time choice made constant, and
#: leaves the RX half of the chain undriven here. None of those is a finding
#: about the converted chain; every warning class that could be one is left
#: on.
VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -Wno-TIMESCALEMOD -Wno-GENUNNAMED -Wno-PROCASSINIT -Wno-SELRANGE \
         -Wno-PINCONNECTEMPTY -Wno-COMBDLY -Wno-CMPCONST -Wno-UNDRIVEN \
         -Wno-SYNCASYNCNET \
         -GUCODE_HEX_P='"gptp_ucode.hex"' -GCLK_HZ_P=$(ENGINE_CLK_HZ) \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"

SRCS = gptp_txts_wrap.sv \
       $(GEN_DIR)/mac_tx_chain.v \
       $(RTL_DIR)/ieee8021as/ptp_timestamp/timestamp_counter.sv \
       $(RTL_DIR)/ieee8021as/gptp_plane/KL_gptp_txticket.sv \
       $(RTL_DIR)/ieee8021as/gptp_plane/KL_gptp_txret.sv \
       $(RTL_DIR)/ieee8021as/gptp_plane/KL_gptp_gmii_launch.sv \
       $(RTL_DIR)/ieee8021as/gptp_plane/KL_gptp_shadow.sv \
       $(RTL_DIR)/ieee17221/adp/adp_tx_arbiter.sv \
       $(RTL_DIR)/common/KL_link_guard.sv \
       $(RTL_DIR)/common/cdc_pulse.sv \
       $(RTL_DIR)/common/cdc_handshake.sv \
       $(AXIS_DIR)/axis_fifo.v \
       $(GPTP_DIR)/hdl/ucpu/gptp_ucpu_pkg.sv \
       $(GPTP_DIR)/hdl/ucpu/KL_gptp_ucpu.sv \
       $(GPTP_DIR)/hdl/wire/KL_gptp_rx_parser.sv \
       $(GPTP_DIR)/hdl/wire/KL_gptp_tx_slot.sv \
       $(GPTP_DIR)/hdl/common/KL_gptp_timer.sv \
       $(GPTP_DIR)/hdl/top/KL_gptp_engine.sv
CPP  = sim_main.cpp

.PHONY: all run model clean

all: mutants

run: gptp_ucode.hex model
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vgptp_txts_sim
	./obj_dir/Vgptp_txts_sim

#: A green suite and a suite that cannot go red look the same from outside.
#: `mutants.py` plants one defect at a time - the observation point, each
#: register-stage term of the correction, the measured cycle distance - and
#: requires this suite to notice, restoring the exact source afterwards.
#: It is part of the default target, so the evidence is produced by the
#: same command the sweep runs.
.PHONY: mutants
mutants: run
	python3 mutants.py

#: A STALE CONVERTED CHAIN IS A RED. The loop is only causal while this
#: artifact is the chain the product builds, so the generator regenerates it
#: and refuses a mismatch before anything is compiled.
model:
	$(MILAN_LITEX_PYTHON) ../../../sw/litex/gen_mac_tx_model.py --check

#: The converted chain ALONE, with one fixed stimulus and no grading, so
#: `sw/litex/test_gptp_tx_timestamp.py` can drive the same stimulus through
#: the migen objects it was converted from and require the two pad traces to
#: agree. That equivalence gate builds this target itself; it is not part of
#: `all`, because it proves nothing on its own.
.PHONY: padtrace
padtrace: obj_pad/Vmac_tx_chain_pads

obj_pad/Vmac_tx_chain_pads: $(GEN_DIR)/mac_tx_chain.v pad_trace_main.cpp
	$(VERILATOR) --cc --exe --build -j 0 --top-module mac_tx_chain \
	  --Mdir obj_pad -Wno-fatal \
	  -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra" \
	  $(GEN_DIR)/mac_tx_chain.v pad_trace_main.cpp -o Vmac_tx_chain_pads

gptp_ucode.hex: $(GPTP_DIR)/hdl/ucode/gen_gptp_ucode.py
	python3 $< --clk-hz $(ENGINE_CLK_HZ) --cease-ms 3000 -o $@

clean:
	rm -rf obj_dir obj_pad gptp_ucode.hex
