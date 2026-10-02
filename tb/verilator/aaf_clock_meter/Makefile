# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# KL_aaf_clock_meter (#629, docs/design/MEDIA_CLOCK_FOLLOWING.md): the meter
# rows of the design's test plan, M1 to M14, each with its named mutant.
#   make         - build and run every case, then the mutation campaign
#   make run     - the cases only
#   make mutants - every named mutant must fail its named check (mutants.py)
#   make clean   - remove build artifacts
#
# CLK_HZ is the ONE value for both the RTL's CLK_FREQ_HZ_P (the 100 ms
# timeouts) and the harness's slot length (CLK_HZ / 8000 cycles per 125 us
# PDU): derive, never mirror. Every rate is timestamp arithmetic, so the
# compressed clock changes no rate.

VERILATOR ?= verilator
VERILATOR_JOBS ?= 0
RTL_DIR    = ../../../hdl
CLK_HZ    ?= 200000
METER_RTL ?= $(RTL_DIR)/ieee1722/crf/KL_aaf_clock_meter.sv
MDIR      ?= obj_dir

VFLAGS = --cc --exe --build -j $(VERILATOR_JOBS) --top-module meter_wrap \
         -GCLK_HZ_P=$(CLK_HZ) \
         -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY \
         -Wno-EOFNEWLINE \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra -DCLK_HZ_TB=$(CLK_HZ)"

SRCS = $(RTL_DIR)/ieee1722/avtp/avtp_subtype_pkg.sv $(METER_RTL) \
       $(RTL_DIR)/ieee1722/crf/KL_crf_rx.sv meter_wrap.sv

.PHONY: all run build mutants clean
all: run mutants

build:
	$(VERILATOR) $(VFLAGS) -Mdir $(MDIR) $(SRCS) sim_main.cpp -o Vmeter_sim

run: build
	@echo "======================================================================"
	./$(MDIR)/Vmeter_sim

mutants:
	python3 mutants.py

clean:
	rm -rf obj_dir obj_mut_*
