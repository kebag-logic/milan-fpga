# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
VERILATOR ?= verilator
RTL_DIR    = ../../hdl
TOP        = KL_gptp_engine
VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -GUCODE_HEX_P='"gptp_ucode.hex"' -GCLK_HZ_P=2000000 \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra -I$(CURDIR)"
SRCS = $(RTL_DIR)/ucpu/gptp_ucpu_pkg.sv $(RTL_DIR)/ucpu/KL_gptp_ucpu.sv \
       $(RTL_DIR)/wire/KL_gptp_rx_parser.sv $(RTL_DIR)/wire/KL_gptp_tx_slot.sv \
       $(RTL_DIR)/common/KL_gptp_timer.sv $(RTL_DIR)/top/KL_gptp_engine.sv
CPP  = tsngen_main.cpp

.PHONY: all run mutants clean
.DEFAULT_GOAL := all
all: run mutants

run: gptp_ucode.hex
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vtsngen
	python3 run_tsngen.py

# Rule 8: prove the checks above are load-bearing. Three defects are injected
# into the real engine RTL, one at a time, and each must make the SAME harness
# fail; the unmutated build must still pass. The suite is staged into a
# temporary directory, so nothing is written into the tree. This arm skips
# exactly when the suite skips (no tsn-gen checkout).
mutants: gptp_ucode.hex
	python3 mutants.py

gptp_ucode.hex: $(RTL_DIR)/ucode/gen_gptp_ucode.py
	python3 $< --clk-hz 2000000 -o $@

clean:
	rm -rf obj_dir gptp_ucode.hex
