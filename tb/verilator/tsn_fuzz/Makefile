# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# IEEE 1722.1 / 1722 field-validation campaign, tsn-gen driven.
#
#   make            build the co-simulation DUTs and run every campaign
#   make build      build only
#   make aaf                 run the AAF campaign (the only one left)
#   make clean
#
# Each campaign is a Python driver talking to a Verilator server built from
# the REAL RTL over a UNIX socket (see cosim_axis.h for the session protocol).
# tsn-gen supplies the spec field model; exit code is the gate.
#
# tsn-gen location: $TSN_GEN_ROOT (default ~/tsn-gen). When it is absent the
# campaigns SKIP cleanly (exit 0) rather than fail — the suite must stay
# runnable on a machine without the generator installed.
VERILATOR ?= verilator
RTL        = ../../../hdl
TP         = ../../../third_party
PY        ?= python3

VCOMMON = --cc --exe --build -j 0 \
          -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
          -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-CASEINCOMPLETE \
          -CFLAGS "-std=c++17 -O2 -I.."

# ---- ACMP / ADP / AECP campaigns: DELETED with the RTL they fuzzed --------
# fuzz_acmp, fuzz_adp, fuzz_aecp and the legacy 14-command smoke driver all
# drove hdl/ieee17221/{acmp,adp,aecp} engines that no longer exist: the
# protocol processor is this device's 1722.1 plane now, and its own campaign
# lives with the submodule. The AAF campaign below is untouched - it fuzzes
# hdl/ieee1722, which is data plane and was not replaced.
#
# THIS IS A COVERAGE LOSS AND IT IS NOT PAPERED OVER: 1722.1 field fuzzing
# against THIS repository's RTL is gone because THIS repository no longer has
# any 1722.1 RTL to fuzz.

# ---- AVTP/AAF receive stack (wrapper lives with the avtp_rxmon TB) ---------
AAF_SRCS = $(RTL)/common/ethernet_packet_pkg.sv \
           $(RTL)/ieee1722/avtp/avtp_subtype_pkg.sv \
           $(RTL)/ieee1722/avtp/avtp_stream_parser.sv \
           $(RTL)/ieee1722/avtp/KL_avtp_rx_monitor.sv \
           $(RTL)/ieee1722/aaf/KL_aaf_rx_depacketizer.sv \
           $(TP)/verilog-axis/rtl/axis_fifo.v \
           ../avtp_rxmon/avtp_rxmon_wrap.sv
AAF_FLAGS = --top-module avtp_rxmon_wrap -GCLK_FREQ_HZ_P=10000 \
            +incdir+$(RTL)/common +incdir+$(RTL)/ieee1722/avtp --Mdir obj_aaf

.PHONY: all build run aaf matrix matrix-check clean

all: run

build: obj_aaf/Vaaf_cosim

obj_aaf/Vaaf_cosim: cosim_aaf.cpp cosim_axis.h $(AAF_SRCS)
	$(VERILATOR) $(VCOMMON) $(AAF_FLAGS) $(AAF_SRCS) cosim_aaf.cpp -o Vaaf_cosim

run: build aaf matrix-check
	@echo "== tsn_fuzz: all campaigns passed =="

# regenerate the module<->spec<->test traceability matrix from the tree
matrix:
	$(PY) ../../../docs/traceability/gen_module_matrix.py

# fail if the committed matrix is stale (the no-drift contract)
#
# The echo is this suite's ONLY unconditional tally. gen_module_matrix.py
# prints prose, not a count shape, so before this line the whole suite reported
# nothing at all whenever the optional campaign skipped -- a NOCOUNT, and the
# sweep could not go green on a machine without tsn-gen.
#
# TWO is the number, and it is worth being exact about because a first cut said
# one. --check gates two INDEPENDENT contracts under a single exit code (see
# gen_module_matrix.py's two `rc = 1` sites): that the 13 generated artifacts
# are not stale, and that the untested-module ratchet has not slipped. Either
# can fail while the other holds, so they are two assertions.
#
# It is deliberately NOT 63, the module count: the ratchet inspects 63 modules
# to reach one verdict, and billing the sweep's headline 63 checks for two
# assertions would inflate it with work this suite did not do. Understating is
# the safe direction here; overstating is what the headline exists to prevent.
#
# The echo runs only when the check above exits 0, so a stale matrix or a
# slipped ratchet stays a failure with NO tally, never a passing 2.
matrix-check:
	$(PY) ../../../docs/traceability/gen_module_matrix.py --check
	@echo "traceability contracts (drift + ratchet): 2 checks: 2 PASS, 0 FAIL"


# THE CAMPAIGN MUST ACCOUNT FOR ITSELF, and this check is here because giving
# the suite an unconditional 2-check floor (see matrix-check) took away the
# backstop it used to have. Before that floor, a campaign whose summary line was
# reworded printed no shape suite_tally.py knew, the suite fell to NOCOUNT and
# the sweep stopped. Now the floor clears NOCOUNT on its own, so the same
# rewording would silently drop 164 checks from the headline with everything
# green. UNPARSED still catches a reword that stays tally-shaped; it does not
# catch "164 ok / 0 bad".
#
# So: exactly two outcomes are valid, a tally or a declared skip. Anything else
# fails here, where it is loud, instead of vanishing into the total.
aaf: obj_aaf/Vaaf_cosim
	@$(PY) fuzz_aaf.py > obj_aaf/aaf.out 2>&1; rc=$$?; cat obj_aaf/aaf.out; \
	 if [ $$rc -ne 0 ]; then exit $$rc; fi; \
	 grep -qE '^(==.*: [0-9]+ pass, [0-9]+ fail|SUITE-SKIP:)' obj_aaf/aaf.out || { \
	   echo "tsn_fuzz: the campaign printed NEITHER a tally suite_tally.py can"; \
	   echo "  read NOR a declared skip. Its checks would be counted as zero"; \
	   echo "  with the sweep still green. Restore one of the two shapes."; \
	   exit 1; }

clean:
	rm -rf obj_aaf __pycache__
