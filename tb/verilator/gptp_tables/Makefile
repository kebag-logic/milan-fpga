# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Per-table lockstep bench for the fabric gPTP plane (issue #640, lane M7):
# the real plane inside the `gptp_shadow` slice bench, each converted table
# compared every cycle with the storage form it had before.
VERILATOR ?= verilator
VERILATOR_JOBS ?= 0
RTL_DIR    = ../../../hdl
GPTP_DIR   = ../../../gptp-processor
AXIS_DIR   = ../../../third_party/verilog-axis/rtl
SLICE_DIR  = ../gptp_shadow
UCODE_GEN  = $(GPTP_DIR)/hdl/ucode/gen_gptp_ucode.py
TOP        = gptp_tables_wrap

#: the slice bench's engine image shape: two megahertz is the floor the
#: engine's microsecond divider allows, and both gPTP slice suites use it
ENGINE_CLK_HZ = 2000000

VFLAGS = --cc --exe --build -j $(VERILATOR_JOBS) \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -Wno-TIMESCALEMOD -Wno-GENUNNAMED -Wno-PROCASSINIT -Wno-SELRANGE \
         -Wno-PINCONNECTEMPTY -Wno-PINMISSING \
         -GUCODE_HEX_P='"gptp_ucode.hex"' -GCLK_HZ_P=$(ENGINE_CLK_HZ) \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"
SRCS = gptp_tables_wrap.sv \
       $(SLICE_DIR)/gptp_shadow_wrap.sv \
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

.PHONY: all run mutants print-inputs clean

all: mutants

run: gptp_ucode.hex
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vgptp_tables_sim
	./obj_dir/Vgptp_tables_sim

#: A lockstep that cannot go red proves nothing. `mutants.py` plants, one at
#: a time in private copies of the sources, a wrong depth, a wrong read
#: latency and an index alias in each converted table, and requires the
#: table's own named check to fail.
mutants: run
	python3 mutants.py

gptp_ucode.hex: $(UCODE_GEN)
	python3 $< --clk-hz $(ENGINE_CLK_HZ) --cease-ms 3000 -o $@

#: The tracked files `run` reads, relative to this directory, for the
#: mutation driver's private copies.
print-inputs:
	@echo Makefile $(SRCS) $(CPP) $(UCODE_GEN)

clean:
	rm -rf obj_dir gptp_ucode.hex
