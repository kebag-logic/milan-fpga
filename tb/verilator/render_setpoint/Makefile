# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# KL_render_setpoint verification: the listener render path's setpoint stage
# (#386). Drives the depacketizer clone with encoded per-sample ramps on two
# streams at the class-A frame shape (6 events per PDU) against a media tick,
# and asserts the law: prefill to the setpoint, the fill sawtooth, the
# first-event delay of every PDU at the setpoint, byte-exact beats for 8, 3,
# 1 and 12 wire channels, the pop schedule and the delayed render tick, the
# underrun gap, both reset rails, the overrun drop, convergence, the one-shot
# recentre (counted once), a flush, and a tick queued inside the schedule.
#   make        - build and run the harness, then the mutation arm
#   make run    - the harness alone
#   make clean  - remove build artifacts
VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = KL_render_setpoint

# ONE statement of the elaborated shape: every value feeds BOTH the -G that
# builds the stage and the -D that tells the harness what it drives.
N_STREAMS   = 2
N_CH        = 8
DEPTH_LOG2  = 5
PDU_EVENTS  = 6
SETPOINT    = 8
CONV_BAND   = 3
RESET_BAND  = 6
# the observer's clock: 100 kHz makes one observer period 100 cycles, so the
# 100-period convergence dwell is reachable in a short run
CLK_HZ      = 100000

GFLAGS = -GN_STREAMS_P=$(N_STREAMS) -GN_CH_P=$(N_CH) -GDEPTH_LOG2_P=$(DEPTH_LOG2) \
         -GPDU_EVENTS_P=$(PDU_EVENTS) -GSETPOINT_EVT_P=$(SETPOINT) \
         -GCONV_BAND_EVT_P=$(CONV_BAND) -GRESET_BAND_EVT_P=$(RESET_BAND) \
         -GCLK_FREQ_HZ_P=$(CLK_HZ)
DFLAGS = -DN_STREAMS_TB=$(N_STREAMS) -DN_CH_TB=$(N_CH) -DDEPTH_LOG2_TB=$(DEPTH_LOG2) \
         -DPDU_EVENTS_TB=$(PDU_EVENTS) -DSETPOINT_TB=$(SETPOINT) \
         -DCONV_BAND_TB=$(CONV_BAND) -DRESET_BAND_TB=$(RESET_BAND) -DCLK_HZ_TB=$(CLK_HZ)

VFLAGS = --cc --exe --build -j 0 --top-module $(TOP) $(GFLAGS) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-EOFNEWLINE \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra $(DFLAGS)"
# SRCS and MDIR are overridable so the mutation arm builds a MUTATED COPY of
# the stage with this exact flag set, into its own directory, through the same
# recipe - one statement of how the harness is built.
SRCS ?= $(RTL_DIR)/ieee1722/aaf/KL_render_setpoint.sv
MDIR ?= obj_dir
EXE   = VKL_render_setpoint_sim
CPP   = sim_main.cpp

.PHONY: all run build mutants clean
.DEFAULT_GOAL := all
all: run mutants

build:
	$(VERILATOR) $(VFLAGS) --Mdir $(MDIR) $(SRCS) $(CPP) -o $(EXE)

run: build
	@echo "======================================================================"
	./$(MDIR)/$(EXE)

# Rule 8: the harness above is load-bearing only if it can fail. Seven defects
# are injected into the real RTL, one at a time, and each must make the SAME
# harness fail by its own verdict; the unmutated build must still pass.
# Mutants build in a temporary directory, nothing is written into the tree.
mutants:
	@echo "======================================================================"
	python3 mutants.py

clean:
	rm -rf obj_dir
