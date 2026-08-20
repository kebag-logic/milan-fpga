# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# IEEE 1722.1 / 1722 field-validation campaign, tsn-gen driven.
#
#   make            build the DUT, run the campaign and the traceability check
#   make build      build only
#   make aaf        run the AAF campaign (the only one left)
#   make matrix-check   the module<->spec<->test no-drift contract
#
# Each campaign target also gates the freshness of the TEST_RESULTS.md it
# writes: the committed copy must match a fresh run, timestamp aside. See the
# FRESH block below.
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

# THE COMMITTED EVIDENCE FILE MUST SAY WHAT THE CAMPAIGN PRODUCES. Each
# campaign writes a TEST_RESULTS.md into the folder of the RTL it validates,
# and until this gate existed nothing compared the committed copy against a
# fresh run. On 2026-08-19 the gPTP artifact came to claim 355 pass while a
# fresh run at the CI-pinned tsn-gen rev produced 353, and every gate in the
# repository stayed green: the tsn-gen field oracle had unpinned two model
# fields for good spec reasons, grade_tx() skips a field with no constraint,
# and so two checks stopped being graded. Nothing went red because nothing
# failed - the file simply went on asserting a number that had stopped being
# true, which is the worst shape for a document a reader trusts to answer
# "is this block verified".
#
# It is the same contract matrix-check enforces below for MODULE_MATRIX.md,
# and it is deliberately built the same way. Two differences are forced by
# what this artifact is:
#
#   * it carries a generation timestamp, so the comparison is on SUBSTANCE
#     with the stamp normalised away on both sides - a byte comparison would
#     be red on every run for a reason that means nothing, and the AAF
#     artifact was in exactly that state the day this was written;
#   * the campaigns SKIP without tsn-gen, so there is no fresh result to
#     compare. That is reported as a SUITE-SKIP naming the reason, never as a
#     pass. The suite stays countable there through matrix-check's floor of 2,
#     not through this gate pretending it checked something.
#
# It runs inside each campaign target rather than as a target of its own, so
# the campaign cannot be run without it, and it is chained with && after the
# campaign guard so neither check can swallow the other's failure.
FRESH = ../../../scripts/check_results_fresh.py

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

# ---- gPTP fabric slice (wrapper lives with the gptp_shadow TB) -------------
# The same slice the datapath splice instantiates: KL_gptp_shadow (tap +
# engine + lane) + the real timestamp_counter + KL_gptp_txstamp as the MAC
# boundary. Bench scaling (2 MHz, cease resume 3 s) so the campaign's timer
# waits stay affordable.
GPTP_DIR  = ../../../gptp-processor
PTP_SRCS = ../gptp_shadow/gptp_shadow_wrap.sv \
           $(RTL)/ieee8021as/ptp_timestamp/timestamp_counter.sv \
           $(RTL)/ieee8021as/gptp_plane/KL_gptp_shadow.sv \
           $(RTL)/ieee8021as/gptp_plane/KL_gptp_txstamp.sv \
           $(TP)/verilog-axis/rtl/axis_fifo.v \
           $(GPTP_DIR)/hdl/ucpu/gptp_ucpu_pkg.sv \
           $(GPTP_DIR)/hdl/ucpu/KL_gptp_ucpu.sv \
           $(GPTP_DIR)/hdl/wire/KL_gptp_rx_parser.sv \
           $(GPTP_DIR)/hdl/wire/KL_gptp_tx_slot.sv \
           $(GPTP_DIR)/hdl/common/KL_gptp_timer.sv \
           $(GPTP_DIR)/hdl/top/KL_gptp_engine.sv
PTP_FLAGS = --top-module gptp_shadow_wrap \
            -Wno-TIMESCALEMOD -Wno-GENUNNAMED -Wno-PROCASSINIT -Wno-SELRANGE \
            -Wno-PINCONNECTEMPTY \
            -GUCODE_HEX_P='"gptp_ucode.hex"' -GCLK_HZ_P=2000000 --Mdir obj_ptp

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

.PHONY: all build run graderself aaf ptp matrix matrix-check clean

all: run

build: obj_aaf/Vaaf_cosim obj_ptp/Vptp_cosim

obj_aaf/Vaaf_cosim: cosim_aaf.cpp cosim_axis.h $(AAF_SRCS)
	$(VERILATOR) $(VCOMMON) $(AAF_FLAGS) $(AAF_SRCS) cosim_aaf.cpp -o Vaaf_cosim

gptp_ucode.hex: $(GPTP_DIR)/hdl/ucode/gen_gptp_ucode.py
	python3 $< --clk-hz 2000000 --cease-ms 3000 -o $@

obj_ptp/Vptp_cosim: cosim_ptp.cpp cosim_axis.h $(PTP_SRCS) gptp_ucode.hex
	$(VERILATOR) $(VCOMMON) $(PTP_FLAGS) $(PTP_SRCS) cosim_ptp.cpp -o Vptp_cosim

run: graderself build aaf ptp matrix-check
	@echo "== tsn_fuzz: all campaigns passed =="

# The field grader's own self-test. Deliberately FIRST and deliberately free of
# Verilator and tsn-gen: it guards a defect the campaigns cannot see, because a
# constraint kind grade_tx does not know produces no check to fail. It therefore
# has to run even where the campaigns skip.
graderself:
	@$(PY) test_grade_tx.py

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
# green.
#
# THE CHECK IS DELEGATED, NOT REIMPLEMENTED. suite_tally.py --campaign-guard
# applies the same recognisers the sweep applies, because a second matcher
# written here is how the two come to disagree — a first cut of this rule was a
# hand-rolled grep, and a review found it rejected four tally shapes the sweep
# reads perfectly well while ACCEPTING "0 pass, 0 fail", the one outcome it most
# needed to reject.
#
# tee, not `> file`: run_all_suites.sh treats a timeout as UNKNOWN rather than
# failure, and with a plain redirect a timed-out campaign leaves nothing in the
# suite log to read. The exit code travels in a sidecar because pipefail is not
# portable to every /bin/sh.
#
# BOTH scratch files are removed first. tee's exit status is discarded (that is
# the price of not having pipefail), so if it cannot open aaf.out the previous
# run's log survives and the guard reads THAT -- a reworded summary would then
# be waved through by a stale copy of the old one. Contrived, but the fix is a
# filename.
aaf: obj_aaf/Vaaf_cosim
	@rm -f obj_aaf/aaf.rc obj_aaf/aaf.out; \
	 { $(PY) fuzz_aaf.py 2>&1; echo $$? > obj_aaf/aaf.rc; } | tee obj_aaf/aaf.out; \
	 rc=$$(cat obj_aaf/aaf.rc); \
	 if [ "$$rc" -ne 0 ]; then exit "$$rc"; fi; \
	 $(PY) ../../../scripts/suite_tally.py --campaign-guard obj_aaf/aaf.out && \
	 $(PY) $(FRESH) --log obj_aaf/aaf.out \
	     --artifact $(RTL)/ieee1722/avtp/doc/TEST_RESULTS.md \
	     --label hdl/ieee1722/avtp/doc/TEST_RESULTS.md

# same tee/rc/guard discipline as aaf — see the block comment above it
ptp: obj_ptp/Vptp_cosim
	@rm -f obj_ptp/ptp.rc obj_ptp/ptp.out; \
	 { $(PY) fuzz_ptp.py 2>&1; echo $$? > obj_ptp/ptp.rc; } | tee obj_ptp/ptp.out; \
	 rc=$$(cat obj_ptp/ptp.rc); \
	 if [ "$$rc" -ne 0 ]; then exit "$$rc"; fi; \
	 $(PY) ../../../scripts/suite_tally.py --campaign-guard obj_ptp/ptp.out && \
	 $(PY) $(FRESH) --log obj_ptp/ptp.out \
	     --artifact $(RTL)/ieee8021as/gptp_plane/doc/TEST_RESULTS.md \
	     --label hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md

clean:
	rm -rf obj_aaf obj_ptp gptp_ucode.hex __pycache__
