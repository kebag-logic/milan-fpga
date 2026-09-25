# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# KL_mmcm_drp_servo harnesses:
#   sim_main.cpp  -> VKL_mmcm_drp_servo : unit TB against the behavioral
#     MMCME2 model (DRP verify/repair sequencing, +-100 ppm lock, bounded
#     slew, holdover, no-activity gating)
#   sim_rails.cpp -> Vrails_wrap        : servo-in-loop with KL_i2s_playback
#     (the drift-lottery rails cease with the servo engaged)
#   sim_phc_step.cpp -> Vphc_step       : the servo at its SILICON defaults
#     (1 ms tick, 512 ms window, NORM_SHIFT_P = 0) against a PHC step (#539)
#   make        - run unit, rails, step and policy-slew harnesses
#   make slew-mutants - run the explicit policy-slew mutation campaign
#   make trace STEP_NS=<n> - the #539 reproduction record: one n ns step at
#                 mid-window, integrator and written rate traced per window
#                 (sim_phc_step.cpp names the slew and talker-step traces)
#   make clean  - remove build artifacts
#
# #545 round 2, 2026-09-25: clean default 952.797 s on two CPUs
# (taskset -c 10,11 make; Verilator 5.052), within the 1800 s budget.
# Shared-host local measurement; 847.203 s margin. Mutations are explicit.

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl

VFLAGS = --cc --exe --build -j 0 \
         -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-EOFNEWLINE \
         -Wno-PINCONNECTEMPTY \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra"

SERVO_RTL ?= $(RTL_DIR)/ieee1722/crf/KL_mmcm_drp_servo.sv
UNIT_MDIR ?= obj_dir
PHC_MDIR ?= obj_phc

COMMON = $(RTL_DIR)/common/cdc_pulse.sv $(RTL_DIR)/common/cdc_handshake.sv \
         $(SERVO_RTL)

# sim-compressed unit params: 125 us tick, 4 ms window renormalized to the
# fixed ns/512ms CSR scale; GAIN 7 = the 125 us tick at the silicon VCO
# LOCK_THR is widened to 16 ppm in the compressed TBs: the +-2-clk tick
# sampling jitter is amplified x128 by NORM_SHIFT (silicon windows keep the
# default 2 ppm threshold - there the same jitter is 0.08 ppm)
UNIT_G = -GTICK_CYC_P=3072 -GWIN_LOG2_P=5 "-GNOM_WIN_NS_P=64'd4000000" \
         -GNORM_SHIFT_P=7 -GGAIN_NUM_P=7 -GRELOCK_TOUT_P=20000 \
         -GLOCK_THR_P=8192

.PHONY: all run unit-build trace phc_step_build slew slew-mutants mutants clean
all: run

# the step harness reads integ_r / u_cmd_r / ew_r / pp_seq_r / pp_run_r, so it
# is built with --public-flat-rw at the servo's DEFAULT (silicon) parameters
STEP_NS ?= 150000
phc_step_build:
	$(VERILATOR) $(VFLAGS) --public-flat-rw --top-module KL_mmcm_drp_servo \
	  -Mdir $(PHC_MDIR) $(COMMON) sim_phc_step.cpp -o Vphc_step

trace: phc_step_build
	./$(PHC_MDIR)/Vphc_step +trace_step_ns=$(STEP_NS)

unit-build:
	$(VERILATOR) $(VFLAGS) --top-module KL_mmcm_drp_servo $(UNIT_G) \
	  -Mdir $(UNIT_MDIR) $(COMMON) sim_main.cpp -o Vservo_sim

run: unit-build
	@echo "======================================================================"
	./$(UNIT_MDIR)/Vservo_sim
	$(VERILATOR) $(VFLAGS) --top-module rails_wrap -Mdir obj_rails \
	  $(COMMON) $(RTL_DIR)/common/cdc_pair_fifo.sv \
	  $(RTL_DIR)/ieee1722/aaf/KL_i2s_playback.sv rails_wrap.sv \
	  sim_rails.cpp -o Vrails_sim
	@echo "======================================================================"
	./obj_rails/Vrails_sim
	$(MAKE) --no-print-directory phc_step_build
	@echo "======================================================================"
	./$(PHC_MDIR)/Vphc_step
	./$(PHC_MDIR)/Vphc_step +slew_suite

# #545 runs the silicon-scale slew and its boundary cases separately, so
# isolated defects need not repeat every step size in the #539 campaign.
slew: phc_step_build
	./$(PHC_MDIR)/Vphc_step +slew_suite

mutants: slew-mutants

slew-mutants:
	python3 slew_mutants.py

clean:
	rm -rf obj_dir obj_rails obj_phc
