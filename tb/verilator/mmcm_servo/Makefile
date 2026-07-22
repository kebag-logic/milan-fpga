# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# KL_mmcm_drp_servo harnesses:
#   sim_main.cpp  -> VKL_mmcm_drp_servo : unit TB against the behavioral
#     MMCME2 model (DRP verify/repair sequencing, +-100 ppm lock, bounded
#     slew, holdover, no-activity gating)
#   sim_rails.cpp -> Vrails_wrap        : servo-in-loop with KL_i2s_playback
#     (the drift-lottery rails cease with the servo engaged)
#   make        - build and run both
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl

VFLAGS = --cc --exe --build -j 0 \
         -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-EOFNEWLINE \
         -Wno-PINCONNECTEMPTY \
         -CFLAGS "-std=c++17 -O2"

COMMON = $(RTL_DIR)/common/cdc_pulse.sv $(RTL_DIR)/common/cdc_handshake.sv \
         $(RTL_DIR)/ieee1722/crf/KL_mmcm_drp_servo.sv

# sim-compressed unit params: 125 us tick, 4 ms window renormalized to the
# fixed ns/512ms CSR scale; GAIN 7 = the 125 us tick at the silicon VCO
# LOCK_THR is widened to 16 ppm in the compressed TBs: the +-2-clk tick
# sampling jitter is amplified x128 by NORM_SHIFT (silicon windows keep the
# default 2 ppm threshold - there the same jitter is 0.08 ppm)
UNIT_G = -GTICK_CYC_P=3072 -GWIN_LOG2_P=5 "-GNOM_WIN_NS_P=64'd4000000" \
         -GNORM_SHIFT_P=7 -GGAIN_NUM_P=7 -GRELOCK_TOUT_P=20000 \
         -GLOCK_THR_P=8192

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) --top-module KL_mmcm_drp_servo $(UNIT_G) \
	  $(COMMON) sim_main.cpp -o Vservo_sim
	@echo "======================================================================"
	./obj_dir/Vservo_sim
	$(VERILATOR) $(VFLAGS) --top-module rails_wrap -Mdir obj_rails \
	  $(COMMON) $(RTL_DIR)/common/cdc_pair_fifo.sv \
	  $(RTL_DIR)/ieee1722/aaf/KL_i2s_playback.sv rails_wrap.sv \
	  sim_rails.cpp -o Vrails_sim
	@echo "======================================================================"
	./obj_rails/Vrails_sim

clean:
	rm -rf obj_dir obj_rails
