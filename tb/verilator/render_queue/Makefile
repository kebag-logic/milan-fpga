# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# KL_render_queue verification: the listener render path's presentation
# stage (#632). The harness plays the depacketizer's read side (each PDU's
# header, then its payload beats) and the domain's media event on an exact
# frame grid, and grades every event the stage presents to every interface,
# byte-exact, against a reference model of the law: each event in the frame
# its timestamp names (rounded to the nearest), each interface reading the
# frame its out-lead names, the late, too-early and untimed rules with their
# counters, a frame read once a lap, a flush, the slips, the 32-bit timestamp
# wrap, the observability taps, and channel counts of 8, 6, 3, 2, 1 and 12 -
# run once on a two-stream, two-interface, 8-lane shape and once on the
# shipping one-stream, one-interface shape at 7 lanes (an odd N_CH_P: the pad
# lane must be a virtual channel).
#   make        - build and run the harness on both shapes, then the mutation arm
#   make run    - the two-interface harness alone
#   make odd    - the one-interface 7-lane harness alone
#   make clean  - remove build artifacts
VERILATOR ?= verilator
VERILATOR_JOBS ?= 0
RTL_DIR    = ../../../hdl
TOP        = KL_render_queue

# ONE statement of the elaborated shape: every value feeds BOTH the -G that
# builds the stage and the -D that tells the harness what it drives.
N_STREAMS = 2
N_CH      = 8
N_IF      = 2
LEAD0     = 2
LEAD1     = 3
EV_LAT    = 20964
MAX_HOLD  = 2126000
PAY_LEAD  = 16
# the observer's clock: 1 MHz makes one observer period 1,000 cycles, so the
# 100-period convergence dwell is 1,000 frames of the harness's 100 cycles
CLK_HZ    = 1000000

GFLAGS = -GN_STREAMS_P=$(N_STREAMS) -GN_CH_P=$(N_CH) -GN_IF_P=$(N_IF) \
         -GIF_LEAD_P=$$(( $(LEAD0) + 256 * $(LEAD1) )) -GEV_LAT_NS_P=$(EV_LAT) \
         -GMAX_HOLD_NS_P=$(MAX_HOLD) -GPAY_LEAD_CYC_P=$(PAY_LEAD) -GCLK_FREQ_HZ_P=$(CLK_HZ)
DFLAGS = -DN_STREAMS_TB=$(N_STREAMS) -DN_CH_TB=$(N_CH) -DN_IF_TB=$(N_IF) \
         -DLEAD0_TB=$(LEAD0) -DLEAD1_TB=$(LEAD1) -DEV_LAT_TB=$(EV_LAT) \
         -DMAX_HOLD_TB=$(MAX_HOLD) -DPAY_LEAD_TB=$(PAY_LEAD) -DCLK_HZ_TB=$(CLK_HZ)

VFLAGS = --cc --exe --build -j $(VERILATOR_JOBS) --top-module $(TOP) $(GFLAGS) \
         -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-EOFNEWLINE \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra $(DFLAGS)"
# SRCS and MDIR are overridable so the mutation arm builds a MUTATED COPY of
# the stage with this exact flag set, into its own directory, through the same
# recipe - one statement of how the harness is built.
SRCS ?= $(RTL_DIR)/ieee1722/aaf/KL_render_queue.sv
MDIR ?= obj_dir
EXE   = VKL_render_queue_sim
CPP   = sim_main.cpp

.PHONY: all run build odd mutants clean
.DEFAULT_GOAL := all
all: run odd mutants

build:
	$(VERILATOR) $(VFLAGS) --Mdir $(MDIR) $(SRCS) $(CPP) -o $(EXE)

run: build
	@echo "======================================================================"
	./$(MDIR)/$(EXE)

# The shipping geometry through the same recipe: one stream, one interface
# at an out-lead of two frames, and an ODD lane count (N_CH_P = 7), so the
# crossbar's channel view carries a pad lane, which an even count cannot
# exercise.
odd:
	@echo "======================================================================"
	$(MAKE) -s run N_STREAMS=1 N_CH=7 N_IF=1 LEAD1=0 MDIR=obj_odd

# Rule 8: the harness above is load-bearing only if it can fail. Defects are
# injected into the real RTL, one at a time, and each must make the SAME
# harness fail by its own named check; the unmutated build must still pass on
# every shape a mutant uses. Mutants build in a temporary directory, nothing
# is written into the tree.
mutants:
	@echo "======================================================================"
	python3 mutants.py

clean:
	rm -rf obj_dir obj_odd __pycache__
