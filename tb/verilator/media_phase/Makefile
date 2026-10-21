# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# The media-clock PHASE loop (#632, #764), closed at the silicon 512 ms window:
# media_phase_wrap.sv (the real KL_crf_rx, KL_mmcm_drp_servo,
# KL_media_domain_event and the phased KL_crf_tx) against the behavioural
# MMCM, a free-running local oscillator and a CRF talker on an exact 2 ms
# grid. sim_main.cpp lists the cases; each runs in its own process.
#
#   make          - the three-interface pins, the blend, the offsets, the
#                   detector cases, then every loop case (CASE_JOBS at once)
#   make pins     - the synthetic three-interface shape graded at its pins
#   make blend    - the in-tree I2S + TDM8 blend graded at both interfaces'
#                   pins (sim_blend.cpp)
#   make ofs      - several AAF outputs of one domain, each its own offset,
#                   graded against the CRF timing points (sim_ofs.cpp)
#   make det      - the phase detector alone, every boundary placed exactly
#                   (sim_det.cpp)
#   make cases    - build and run every case
#   make mutants  - THE MUTATION CAMPAIGN, explicit: one planted defect per
#                   loop term and per interface constant, each required to
#                   fail its named check (phase_mutants.py). It rebuilds per
#                   mutant and ran in 751 s at MUTANT_JOBS=4, which
#                   does not fit this suite's sweep budget, so like the other
#                   long campaigns it is a target of its own
#                   (docs/testing/TESTING.md records who runs it)
#   make clean    - remove build artifacts
#
# WALL CLOCK. Each loop case simulates 35 to 100 s of a 3.125 MHz datapath
# clock and a 768 kHz audio clock, one case per process; CASE_JOBS of them run
# at once. Measured locally at the default 3 jobs on a shared host, the whole
# default target, its five builds included: 578 s.

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
PIN_SRCS = $(LATPKG_RTL) \
           $(RTL_DIR)/common/cdc_pair_fifo.sv \
           $(RTL_DIR)/ieee1722/aaf/KL_tdm_capture_master.sv \
           $(DOMEV_RTL) $(CRFTX_RTL) $(PIN_WRAP)

# the detector alone (#632): KL_mmcm_drp_servo with a 32-cycle tick, so a
# window is 16,384 cycles
DET_MDIR ?= obj_det
DET_CASES = inband events meanin balanced unbal129 unbal160 jitter cross afterhold range snap

CASES = engage engage2 edge edge2 step ramp holdover internal mr slew phcstep burst carry
OUT  ?= obj_logs

.PHONY: all run build cases pins pins-build blend blend-build ofs ofs-build det det-build mutants clean
all: run

build:
	$(VERILATOR) $(VFLAGS) --Mdir $(MDIR) --top-module $(TOP) $(SRCS) sim_main.cpp -o Vmedia_phase

run: pins blend ofs det cases

pins-build:
	$(VERILATOR) $(VFLAGS) --Mdir $(PIN_MDIR) --top-module pin_wrap $(PIN_SRCS) sim_pins.cpp -o Vpin_wrap

pins: pins-build
	@echo "======================================================================"
	$(PIN_MDIR)/Vpin_wrap

det-build:
	$(VERILATOR) $(VFLAGS) --Mdir $(DET_MDIR) --top-module KL_mmcm_drp_servo --prefix Vdet_servo \
	  -GTICK_CYC_P=32 $(RTL_DIR)/common/cdc_pulse.sv $(RTL_DIR)/common/cdc_handshake.sv \
	  $(SERVO_RTL) sim_det.cpp -o Vdet

# several AAF outputs of one domain with their own offsets (#632):
# ofs_wrap.sv, sim_ofs.cpp
OFS_WRAP ?= ofs_wrap.sv
OFS_MDIR ?= obj_ofs
MTTR_RTL ?= $(RTL_DIR)/ieee1722/crf/KL_mtt_round.sv
OFS_SRCS = $(MTTR_RTL) $(RTL_DIR)/ieee1722/aaf/KL_aaf_packetizer.sv $(CRFTX_RTL) $(OFS_WRAP)

ofs-build:
	$(VERILATOR) $(VFLAGS) --Mdir $(OFS_MDIR) --top-module ofs_wrap $(OFS_SRCS) sim_ofs.cpp -o Vofs_wrap

ofs: ofs-build
	@echo "======================================================================"
	$(OFS_MDIR)/Vofs_wrap

# the in-tree two-interface shape (#632): the Arty I2S + TDM8
# capture through KL_pair_blend into the capture crossbar's frame bank,
# graded at both interfaces' pins: blend_wrap.sv, sim_blend.cpp
BLEND_WRAP ?= blend_wrap.sv
BLEND_MDIR ?= obj_blend
LATPKG_RTL ?= $(RTL_DIR)/ieee1722/crf/KL_media_if_latency_pkg.sv
CMAP_RTL   ?= $(RTL_DIR)/ieee1722/aaf/KL_chan_map_capture.sv
I2SCAP_RTL ?= $(RTL_DIR)/ieee1722/aaf/KL_aaf_capture_i2s.sv
BLEND_SRCS = $(LATPKG_RTL) $(RTL_DIR)/common/cdc_pair_fifo.sv \
             $(I2SCAP_RTL) \
             $(RTL_DIR)/ieee1722/aaf/KL_tdm_capture_master.sv \
             $(RTL_DIR)/ieee1722/aaf/KL_pair_blend.sv $(DOMEV_RTL) $(CMAP_RTL) $(BLEND_WRAP)

blend-build:
	$(VERILATOR) $(VFLAGS) --Mdir $(BLEND_MDIR) --top-module blend_wrap $(BLEND_SRCS) sim_blend.cpp -o Vblend_wrap

blend: blend-build
	@echo "======================================================================"
	$(BLEND_MDIR)/Vblend_wrap

# every detector case in its own process; the verdict is make's
det: det-build
	@rc=0; for c in $(DET_CASES); do \
	  echo "======================================================================"; \
	  $(DET_MDIR)/Vdet +case=$$c || rc=1; \
	done; exit $$rc

# every case, one process each, CASE_JOBS at once; each case's whole log is
# kept in OUT, and printed here without its per-window trace lines. The
# verdict is make's: any failing case fails the target
CASE_JOBS ?= 3
cases: build
	@mkdir -p $(OUT)
	@printf '%s\n' $(CASES) | xargs -P $(CASE_JOBS) -I{} sh -c \
	  '$(MDIR)/Vmedia_phase +case=$$1 > $(OUT)/$$1.log 2>&1; echo $$? > $(OUT)/$$1.rc' sh {}
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
	rm -rf obj_dir obj_pins obj_blend obj_det obj_ofs obj_logs __pycache__
