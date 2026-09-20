# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator CO-SIMULATION of the saved-state snapshot-ownership contract
# (docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md), graded against the
# SHIPPING hdl/milan/KL_nvm_backend.sv and the SHIPPING writer
# sw/firmware/milan_baremetal/milan_baremetal.c compiled for the host.
#
# What makes this suite different from tb/verilator/nvm_backend, which grades
# the same module: the FIRMWARE IS IN THE LOOP, and so is the REAL donor
# producer path at the pinned revision (KL_acmp_nvm_shadow driving
# KL_pp_nvm_port, and KL_aecp_dyn_state). nvm_backend grades the module's byte
# pump, its region decode and its section 9 status against a harness; this one
# grades the pair against the ORDERINGS of the contract page's section 9 --
# the acknowledgement race of issue #418, the ERASE-error counterexample, the
# one-pulse re-arm failure of issue #420, the capture hold, the window load and
# the writer's restart.
#
#   run        every executed case of section 9 at BOTH shipped shapes, then
#              the identity control, the identity-wrap arm and every mutant
#              the page names, each of which MUST be killed by the ONE check
#              the page names for it.
#   quick      the shipping builds at 1x1 only, no mutants: the local loop.
#   wrap       the identity-wrap arm alone: the same cases at 1, 2 and 16
#              identity bits, where the writer's report must not move with
#              the width (issue #484 round 2).
#   control    additionally builds a backend and a writer from BEFORE the
#              contract (LEGACY_DIR) and requires the three historical defects
#              to reproduce there. That is the non-vacuity proof in the
#              direction a mutant cannot give: the checks fail on the source
#              the defects were reported against and pass on this one.
#   lint       Verilator lint of the wrapper against the shipping backend.
#
# The model's limits are stated in README.md and are not small: no CPU
# instruction time, no bus latency, no clock-domain crossings, no real flash
# timing. The backend clock is 1 MHz of MODEL time.

PYTHON  ?= python3
JOBS    ?= 8
POOL    ?= 8
SHAPES  ?= 1x1,8x8
# a checkout of hdl/milan/KL_nvm_backend.sv and
# sw/firmware/milan_baremetal/milan_baremetal.c from before the contract
LEGACY_DIR ?=

RTL     = ../../../hdl/milan
BACKEND = $(RTL)/KL_nvm_backend.sv
PP      = ../../../protocol-processor/hdl
DONOR   = $(PP)/acmp/pp_acmp_pkg.sv $(PP)/aecp/KL_aecp_dyn_state.sv \
          $(PP)/acmp/KL_acmp_nvm_shadow.sv $(PP)/packet_engine/KL_pp_nvm_port.sv

.PHONY: all run quick wrap control lint clean
all: run

run:
	$(PYTHON) -B run_cases.py --shapes $(SHAPES) --jobs $(JOBS) --pool $(POOL)

quick:
	$(PYTHON) -B run_cases.py --shapes 1x1 --jobs $(JOBS) --pool $(POOL) --skip-mutants

wrap:
	$(PYTHON) -B run_cases.py --shapes 1x1 --jobs $(JOBS) --pool $(POOL) --wrap-only

control:
	@test -n "$(LEGACY_DIR)" || { echo "control needs LEGACY_DIR=<dir with the"\
	  " pre-contract KL_nvm_backend.sv and milan_baremetal.c>"; exit 2; }
	$(PYTHON) -B run_cases.py --shapes 1x1 --jobs $(JOBS) --pool $(POOL) \
	  --skip-mutants --legacy-dir $(LEGACY_DIR)

# `-Wall` with NO `-Wno-fatal` on the shipping module: a Verilator warning on
# it stops this build. The wrapper and the donor carry -Wno-fatal, because
# neither is this suite's subject.
#
# `-Werror-USERERROR` on EVERY invocation here, including the one that would
# already be fatal: the backend states its legal parameter ranges as
# elaboration $errors (KL_nvm_backend.sv g_refuse_* guards), and -Wno-fatal
# on its own demotes a $error to a warning nothing reads, so an out-of-range
# build would elaborate, simulate and be graded. The rule, and the review
# that found a suite grading an illegal shape with rc 0 before the flag was
# added there, are in docs/development/CODE_QUALITY.md under rule 6, "Where
# the contract is enforced, and where it is not".
lint:
	verilator --lint-only -Wall -Werror-USERERROR --top-module KL_nvm_backend \
	  -GCLK_HZ_P=1000000 -GN_STREAM_IN_P=9 -GN_STREAM_OUT_P=9 \
	  -GN_SPORT_IN_P=8 -GN_SPORT_OUT_P=8 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 \
	  -GN_NAME_P=99 -GT_HOLD_MS_P=50 -GCAP_ID_W_P=16 $(BACKEND)
	verilator --lint-only -Wall -Wno-fatal -Werror-USERERROR --top-module cosim_top \
	  +define+NVM_CONTRACT_3 \
	  -GCLK_HZ_P=1000000 -GN_STREAM_IN_P=9 -GN_STREAM_OUT_P=9 \
	  -GN_SPORT_IN_P=8 -GN_SPORT_OUT_P=8 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 \
	  -GN_NAME_P=99 $(DONOR) $(BACKEND) cosim_top.sv

clean:
	rm -rf build runs
