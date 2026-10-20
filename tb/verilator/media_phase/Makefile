# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# The media-clock PHASE loop (#632, #764), closed at the silicon 512 ms window:
# media_phase_wrap.sv (the real KL_crf_rx, KL_mmcm_drp_servo,
# KL_media_domain_event and the phased KL_crf_tx) against the behavioural
# MMCM, a free-running local oscillator and a CRF talker on an exact 2 ms
# grid. sim_main.cpp lists the cases; each runs in its own process.
#
#   make          - the three-interface pins, then every case (CASE_JOBS at once)
#   make pins     - the synthetic three-interface shape graded at its pins
#   make cases    - build and run every case
#   make mutants  - THE MUTATION CAMPAIGN, explicit: one planted defect per
#                   loop term and per interface constant, each required to
#                   fail its named check (phase_mutants.py). It rebuilds per
#                   mutant and runs about 11 minutes at MUTANT_JOBS=4, which
#                   does not fit this suite's sweep budget, so like the other
#                   long campaigns it is a target of its own
#                   (docs/testing/TESTING.md records who runs it)
#   make clean    - remove build artifacts
#
# WALL CLOCK. Each case simulates 35 to 100 s of a 3.125 MHz datapath clock
# and a 768 kHz audio clock, one case per process; CASE_JOBS of them run at
# once. Measured locally at 3 jobs: about 6 minutes for every case.

VERILATOR ?= verilator
VERILATOR_JOBS ?= 0
RTL_DIR    = ../../../hdl
TOP        = media_phase_wrap
MDIR      ?= obj_dir

# --public-flat-rw: the carry case reads the integrator and the window error
VFLAGS = --cc --exe --build -j $(VERILATOR_JOBS) --public-flat-rw \
         -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-EOFNEWLINE \
         -Wno-PINCONNECTEMPTY \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra"

# the three sources phase_mutants.py plants defects in, overridable
SERVO_RTL ?= $(RTL_DIR)/ieee1722/crf/KL_mmcm_drp_servo.sv
DOMEV_RTL ?= $(RTL_DIR)/ieee1722/crf/KL_media_domain_event.sv
CRFTX_RTL ?= $(RTL_DIR)/ieee1722/crf/KL_crf_tx.sv
SRCS = $(RTL_DIR)/common/cdc_pulse.sv $(RTL_DIR)/common/cdc_handshake.sv \
       $(SERVO_RTL) $(DOMEV_RTL) $(CRFTX_RTL) \
       $(RTL_DIR)/ieee1722/crf/KL_crf_rx.sv \
       media_phase_wrap.sv

# the synthetic three-interface shape (#632): pin_wrap.sv, sim_pins.cpp
PIN_WRAP ?= pin_wrap.sv
PIN_MDIR ?= obj_pins
PIN_SRCS = $(RTL_DIR)/ieee1722/crf/KL_media_if_latency_pkg.sv \
           $(RTL_DIR)/common/cdc_pair_fifo.sv \
           $(RTL_DIR)/ieee1722/aaf/KL_tdm_capture_master.sv \
           $(DOMEV_RTL) $(CRFTX_RTL) $(PIN_WRAP)

CASES = engage engage2 step ramp holdover internal mr slew burst carry
OUT  ?= obj_logs

.PHONY: all run build cases pins pins-build mutants clean
all: run

build:
	$(VERILATOR) $(VFLAGS) --Mdir $(MDIR) --top-module $(TOP) $(SRCS) sim_main.cpp -o Vmedia_phase

run: pins cases

pins-build:
	$(VERILATOR) $(VFLAGS) --Mdir $(PIN_MDIR) --top-module pin_wrap $(PIN_SRCS) sim_pins.cpp -o Vpin_wrap

pins: pins-build
	@echo "======================================================================"
	./$(PIN_MDIR)/Vpin_wrap

# every case, one process each, CASE_JOBS at once; each case's whole log is
# kept in OUT, and printed here without its per-window trace lines. The
# verdict is make's: any failing case fails the target
CASE_JOBS ?= 3
cases: build
	@mkdir -p $(OUT)
	@printf '%s\n' $(CASES) | xargs -P $(CASE_JOBS) -I{} sh -c \
	  './$(MDIR)/Vmedia_phase +case=$$1 > $(OUT)/$$1.log 2>&1; echo $$? > $(OUT)/$$1.rc' sh {}
	@rc=0; for c in $(CASES); do \
	  echo "======================================================================"; \
	  grep -v '^  t=' $(OUT)/$$c.log; \
	  test "$$(cat $(OUT)/$$c.rc)" = 0 || { echo "CASE $$c FAILED"; rc=1; }; \
	done; exit $$rc

MUTANT_JOBS ?= 4
mutants:
	@echo "======================================================================"
	@echo "---- #632/#764 phase loop: one planted defect per loop term ----------"
	python3 phase_mutants.py --jobs $(MUTANT_JOBS)

clean:
	rm -rf obj_dir obj_pins obj_logs __pycache__
