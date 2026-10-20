# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# The media-clock PHASE loop (#632, #764), closed at the silicon 512 ms window:
# media_phase_wrap.sv (the real KL_crf_rx, KL_mmcm_drp_servo,
# KL_media_domain_event and the phased KL_crf_tx) against the behavioural
# MMCM, a free-running local oscillator and a CRF talker on an exact 2 ms
# grid. sim_main.cpp lists the cases; each runs in its own process.
#
#   make          - the two-interface pins, every case, then the mutants
#   make pins     - the synthetic two-interface shape graded at its pins
#   make cases    - build and run every case
#   make mutants  - the planted mutants alone (phase_mutants.py)
#   make clean    - remove build artifacts

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

# the synthetic two-interface shape (#632): pin_wrap.sv, sim_pins.cpp
PIN_WRAP ?= pin_wrap.sv
PIN_MDIR ?= obj_pins
PIN_SRCS = $(RTL_DIR)/ieee1722/crf/KL_media_if_latency_pkg.sv \
           $(RTL_DIR)/common/cdc_pair_fifo.sv \
           $(RTL_DIR)/ieee1722/aaf/KL_tdm_capture_master.sv \
           $(DOMEV_RTL) $(CRFTX_RTL) $(PIN_WRAP)

CASES = engage engage2 step ramp holdover internal mr carry
OUT  ?= obj_logs

.PHONY: all run build cases pins pins-build mutants clean
all: run

build:
	$(VERILATOR) $(VFLAGS) --Mdir $(MDIR) --top-module $(TOP) $(SRCS) sim_main.cpp -o Vmedia_phase

run: pins cases mutants

pins-build:
	$(VERILATOR) $(VFLAGS) --Mdir $(PIN_MDIR) --top-module pin_wrap $(PIN_SRCS) sim_pins.cpp -o Vpin_wrap

pins: pins-build
	@echo "======================================================================"
	./$(PIN_MDIR)/Vpin_wrap

# every case, one process each; a case's log is kept whole, and the verdict
# is make's own: the first failing case fails the target
cases: build
	@mkdir -p $(OUT)
	@set -e; for c in $(CASES); do \
	  echo "======================================================================"; \
	  ./$(MDIR)/Vmedia_phase +case=$$c | tee $(OUT)/$$c.log | grep -v '^  t=' ; \
	  test "$${PIPESTATUS[0]}" = 0 || { echo "CASE $$c FAILED"; exit 1; }; \
	done

mutants:
	@echo "======================================================================"
	@echo "---- #632/#764 phase loop: one planted defect per loop term ----------"
	python3 phase_mutants.py

clean:
	rm -rf obj_dir obj_pins obj_logs __pycache__
