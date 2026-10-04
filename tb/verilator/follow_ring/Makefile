# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# The media-clock plane and the two listener rings it paces, through a source
# change and through an INTERNAL aligner pull-in (#645, #647):
# follow_ring_wrap.sv binds the real meter, CRF receiver, servo, NCO, aligner,
# capture crossbar LOOP bucket and render setpoint stage, with
# milan_datapath's own glue between them copied verbatim by dp_glue.py.
#   make         - the standing legs, then the mutation arm (mutants.py)
#   make build   - build the harness (MDIR, default obj_dir)
#   make b8      - lane B8's INTERNAL-to-AAF set, then AAF to CRF and back
#   make pullin  - one serial-clock hold under a running stream at INTERNAL
#   make mutants - every planted defect must fail its named check
#   make sweep-b8 / sweep-pullin - the #645 / #647 reproductions across their
#                  phase sweeps (sweep.py; SWEEP_JOBS at a time). They record
#                  the defects; they grade nothing, and exit 0 once every run
#                  completed
#   make clean   - remove build artifacts
#
# CLK_HZ is the ONE value for the wrapper's axis clock and the harness's
# wheel: derive, never mirror. The aligner's gains scale with it (the
# wrapper's banner): at an eighth of the shipping 50 MHz they are 2 + 3 and
# 12 - 3.

VERILATOR ?= verilator
VERILATOR_JOBS ?= 0
RTL_DIR = ../../../hdl
DP_SRC ?= $(RTL_DIR)/milan/milan_datapath.sv
SHAPE  ?= ../../../configs/generated/endstation_ax7101_1x1_tdm8
CLK_HZ ?= 6250000
MDIR   ?= obj_dir
MUT_DEFS ?=
SWEEP_JOBS ?= 4

SRCS = $(RTL_DIR)/ieee1722/avtp/avtp_subtype_pkg.sv \
       $(RTL_DIR)/common/cdc_pulse.sv $(RTL_DIR)/common/cdc_handshake.sv \
       $(RTL_DIR)/ieee1722/crf/KL_aaf_clock_meter.sv \
       $(RTL_DIR)/ieee1722/crf/KL_crf_rx.sv \
       $(RTL_DIR)/ieee1722/crf/KL_mmcm_drp_servo.sv \
       $(RTL_DIR)/ieee1722/crf/KL_media_nco.sv \
       $(RTL_DIR)/ieee1722/crf/KL_media_grid_align.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_chan_map_capture.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_render_setpoint.sv \
       follow_ring_wrap.sv

# --public-flat-rw: the harness reads the servo's window registers and the
# loopback ring's pair pointers; it writes nothing through them.
VFLAGS = --cc --exe --build -j $(VERILATOR_JOBS) --top-module follow_ring_wrap \
         --public-flat-rw -GCLK_HZ_P=$(CLK_HZ) +incdir+$(SHAPE) +incdir+$(MDIR) $(MUT_DEFS) \
         -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY \
         -Wno-EOFNEWLINE \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra -DCLK_HZ_TB=$(CLK_HZ)"

.PHONY: all run build b8 pullin mutants sweep-b8 sweep-pullin clean
all: run mutants
run: b8 pullin

build:
	mkdir -p $(MDIR)
	python3 dp_glue.py $(DP_SRC) $(MDIR)/dp_glue.svh
	$(VERILATOR) $(VFLAGS) -Mdir $(MDIR) $(SRCS) sim_main.cpp -o Vfollow_ring

# The standing legs. b8 sets AAF where the loopback ring is left within a
# tenth of a tick of its empty edge (set phase 0.5), so any walk a
# stream-to-stream switch leaves slips it: the declared "no frame slip" of
# those switches is graded at its most sensitive place.
b8: build
	./$(MDIR)/Vfollow_ring --case b8 --dwell-s 1.0 --set-phase 0.5 --hold-s 20 --switch-hold-s 15

pullin: build
	./$(MDIR)/Vfollow_ring --case pullin

mutants:
	python3 mutants.py

sweep-b8: build
	python3 sweep.py b8 --exe $(MDIR)/Vfollow_ring --out $(MDIR)/sweep --jobs $(SWEEP_JOBS) \
	  --jitter-us 0 5 --extra --dwell-s 1.0

sweep-pullin: build
	python3 sweep.py pullin --exe $(MDIR)/Vfollow_ring --out $(MDIR)/sweep --jobs $(SWEEP_JOBS) \
	  --hold-us 52 56

clean:
	rm -rf obj_dir obj_mut __pycache__
