# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
GPTP_DIR   = ../../../gptp-processor
AXIS_DIR   = ../../../third_party/verilog-axis/rtl
TOP        = gptp_shadow_wrap
VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -Wno-TIMESCALEMOD -Wno-GENUNNAMED -Wno-PROCASSINIT -Wno-SELRANGE \
         -Wno-PINCONNECTEMPTY \
         -GUCODE_HEX_P='"gptp_ucode.hex"' -GCLK_HZ_P=2000000 \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"
SRCS = gptp_shadow_wrap.sv \
       $(RTL_DIR)/ieee8021as/ptp_timestamp/timestamp_counter.sv \
       $(RTL_DIR)/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv \
       $(RTL_DIR)/ieee8021as/gptp_plane/KL_gptp_txticket.sv \
       $(RTL_DIR)/ieee8021as/gptp_plane/KL_gptp_txret.sv \
       $(RTL_DIR)/ieee8021as/gptp_plane/KL_gptp_gmii_launch.sv \
       $(RTL_DIR)/ieee8021as/gptp_plane/KL_gptp_shadow.sv \
       $(RTL_DIR)/common/KL_link_guard.sv \
       $(RTL_DIR)/common/cdc_pulse.sv \
       $(RTL_DIR)/common/cdc_handshake.sv \
       $(AXIS_DIR)/axis_fifo.v \
       $(GPTP_DIR)/hdl/ucpu/gptp_ucpu_pkg.sv \
       $(GPTP_DIR)/hdl/ucpu/KL_gptp_ucpu.sv \
       $(GPTP_DIR)/hdl/wire/KL_gptp_rx_parser.sv \
       $(GPTP_DIR)/hdl/wire/KL_gptp_tx_slot.sv \
       $(GPTP_DIR)/hdl/common/KL_gptp_timer.sv \
       $(GPTP_DIR)/hdl/top/KL_gptp_engine.sv
CPP  = sim_main.cpp

.PHONY: all run mutants clean

all: mutants

run: gptp_ucode.hex
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vgptp_shadow_sim
	./obj_dir/Vgptp_shadow_sim

#: A green suite and a suite that cannot go red look the same from outside.
#: `mutants.py` plants one plane defect at a time - what a ledger entry is,
#: when it may resolve, what a barrier destroys, what discharges a recovery
#: demand, and which measured terms the reconstruction is made of - and
#: requires this suite to notice, restoring the exact source afterwards. It
#: is the default target, so the evidence comes from the command the sweep
#: already runs.
mutants: run
	python3 mutants.py

gptp_ucode.hex: $(GPTP_DIR)/hdl/ucode/gen_gptp_ucode.py
	python3 $< --clk-hz 2000000 --cease-ms 3000 -o $@

clean:
	rm -rf obj_dir gptp_ucode.hex
