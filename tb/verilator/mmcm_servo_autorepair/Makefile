# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# KL_mmcm_drp_servo auto_repair REPAIR-path harness (roadmap 6 tail):
#   sim_autorepair.cpp -> VKL_mmcm_drp_servo : plants a WRONG CLKOUT0 divider
#     in the DRP-slave model (drp_model.h) and proves the exact XAPP888
#     read-modify-write repair sequence when auto_repair_i=1, and ZERO DRP
#     writes when auto_repair_i=0 (the silicon-safe tied-off default).
#   make        - build and run
#   make clean  - remove build artifacts
#
# This dir is standalone: it does NOT touch tb/verilator/mmcm_servo (the
# shared PS-lock / rails harnesses).

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl

VFLAGS = --cc --exe --build -j 0 \
         -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-EOFNEWLINE \
         -CFLAGS "-std=c++17 -O2"

COMMON = $(RTL_DIR)/common/cdc_pulse.sv $(RTL_DIR)/common/cdc_handshake.sv \
         $(RTL_DIR)/ieee1722/crf/KL_mmcm_drp_servo.sv

# sim-compressed unit params (same scale as tb/verilator/mmcm_servo): 125 us
# tick, 4 ms window renormalized to the fixed ns/512ms CSR scale. The DRP
# repair sequence is timing-independent of these; they only keep activation
# fast. RELOCK_TOUT_P(20000) > the model relock_lat(500) so relock completes.
UNIT_G = -GTICK_CYC_P=3072 -GWIN_LOG2_P=5 "-GNOM_WIN_NS_P=64'd4000000" \
         -GNORM_SHIFT_P=7 -GGAIN_NUM_P=7 -GRELOCK_TOUT_P=20000 \
         -GLOCK_THR_P=8192

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) --top-module KL_mmcm_drp_servo $(UNIT_G) \
	  $(COMMON) sim_autorepair.cpp -o Vautorepair_sim
	@echo "======================================================================"
	./obj_dir/Vautorepair_sim

clean:
	rm -rf obj_dir
