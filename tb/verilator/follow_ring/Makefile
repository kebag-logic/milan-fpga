# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# The media-clock plane and the two listener rings it paces, through a source
# change and through an INTERNAL aligner pull-in (#645, #647):
# follow_ring_wrap.sv binds the real meter, CRF receiver, servo, NCO, aligner,
# capture crossbar LOOP bucket and render setpoint stage, with
# milan_datapath's own glue between them, the #645 settle recentre included,
# copied verbatim by dp_glue.py.
#   make         - the four standing legs (run)
#   make build   - build the harness (MDIR, default obj_dir)
#   make b8      - lane B8's INTERNAL-to-AAF set, then AAF to CRF and back,
#                  each graded on its settle recentre
#   make pullin  - one serial-clock hold under a running stream at INTERNAL,
#                  graded on its settle recentre
#   make mutants - every planted defect must fail its named check
#   make sweep-b8 / sweep-pullin - the #645 / #647 campaigns across their
#                  phase sweeps (sweep.py; SWEEP_JOBS at a time), every run
#                  graded on the settle law; exit 0 only when every run passed
#   make clean   - remove build artifacts
#
# DEFAULT WALL CLOCK (#645, 2026-10-09): the previous 1e79ebdc hosted
# window was 1422.5 s (run 37882435947, job 113665137864, dev-class runner),
# leaving 17.5 s to 1440 s and 377.5 s to the unchanged 1800 s guard.
# New cold replica: env -u MAKEFLAGS taskset -c 32-35 make -C
# tb/verilator/follow_ring; serial outer make, 437.204 s. The four standing
# legs run in a bounded four-job sub-make with one shared b8/pullin build.
# At this suite's measured ratio, 1422.5 / 800.2 rounded up to 1.78,
# the projection is 778.2 s: margins 661.8 s to 1440 s and 1021.8 s to
# 1800 s. It meets the 708 s replica bar; exact-head hosted acceptance
# still requires <=1260 s. See docs/testing/TESTING.md for source receipts.
# The twelve rebuilt controls remain in make mutants, owned by the manager
# merge bank in TESTING.md; the four default legs retain all their checks.
#
# CLK_HZ is the ONE value for the wrapper's axis clock and the harness's
# wheel: derive, never mirror. The aligner's gains scale with it (the
# wrapper's banner): at an eighth of the shipping 50 MHz they are 2 + 3 and
# 12 - 3.

VERILATOR ?= verilator
VERILATOR_JOBS ?= 16
RTL_DIR = ../../../hdl
# traceability-text-input: milan_datapath.sv
DP_SRC ?= $(RTL_DIR)/milan/milan_datapath.sv
# mutants.py builds a planted COPY of the capture crossbar through this
CMAP_SRC ?= $(RTL_DIR)/ieee1722/aaf/KL_chan_map_capture.sv
SHAPE  ?= ../../../configs/generated/endstation_ax7101_1x1_tdm8
CLK_HZ ?= 6250000
# Sub-sample holds resolve 1/64 sample; keep the servo tick exactly 1 ms.
FRAME_DIV ?= 64
AUDIO_TICK_CYC = $(shell expr $(FRAME_DIV) \* 48)
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
       $(CMAP_SRC) \
       $(RTL_DIR)/ieee1722/aaf/KL_render_setpoint.sv \
       follow_ring_wrap.sv

# --public-flat-rw: the harness reads the servo's window registers and the
# loopback ring's pair pointers; it writes nothing through them.
VFLAGS = --cc --exe --build -j $(VERILATOR_JOBS) --top-module follow_ring_wrap \
         --public-flat-rw -GCLK_HZ_P=$(CLK_HZ) -GFRAME_DIV_P=$(FRAME_DIV) -GTICK_CYC_P=$(AUDIO_TICK_CYC) +incdir+$(SHAPE) +incdir+$(MDIR) $(MUT_DEFS) \
         -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY \
         -Wno-EOFNEWLINE \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra -DCLK_HZ_TB=$(CLK_HZ) -DFRAME_DIV_TB=$(FRAME_DIV)"

.PHONY: all run build b8 pullin small-pullin settle-control mutants sweep-b8 sweep-pullin clean
all: run
# The sweep invokes serial outer make. Give these four independent legs a
# bounded pool even there; b8 and pullin share one build in this sub-make.
# An outer -jN cannot expand the pool past four leg jobs.
run:
	+$(MAKE) -j4 b8 pullin small-pullin settle-control

build:
	mkdir -p $(MDIR)
	python3 dp_glue.py $(DP_SRC) $(MDIR)/dp_glue.svh
	$(VERILATOR) $(VFLAGS) -Mdir $(MDIR) $(SRCS) sim_main.cpp -o Vfollow_ring

# The standing legs. b8 sets AAF at the set phase (0.0) where the servo's
# pull-in leaves the loopback ring half a tick from its empty edge and the
# render stage a tick and a half off its law, and where every settle's
# render window stays clear of #643's ambiguity window, so all three are
# graded; each hold runs past its settle recentre. pullin feeds at the phase
# the 52 us hold's pull moves off the law.
b8: build
	$(abspath $(MDIR))/Vfollow_ring --case b8 --dwell-s 1.0 --set-phase 0.0 --hold-s 16 --switch-hold-s 15

pullin: build
	$(abspath $(MDIR))/Vfollow_ring --case pullin --latency-us 210.42 --after-s 1.5

# The review's sub-arm pull is gradable on both sides of the law boundary
# at 25 MHz. Audio edges resolve 1/64 sample, with the real 1 ms servo tick.
small-pullin:
	$(MAKE) build CLK_HZ=25000000 FRAME_DIV=64 MDIR=$(abspath $(MDIR))_fine
	python3 small_pulls.py --exe $(abspath $(MDIR))_fine/Vfollow_ring \
	  --out $(abspath $(MDIR))_fine/results --jobs $(SWEEP_JOBS)

settle-control:
	python3 settle_control.py --sim $(VERILATOR) \
	  --out $(abspath $(MDIR))_control --jobs $(SWEEP_JOBS)

mutants:
	python3 mutants.py --jobs $(SWEEP_JOBS)

# sweep-b8: no lateness and uniform lateness through the ruled 60 us
# envelope; the rare tail is a separate run (--jitter-us 2 --tail-us 24 --tail-p 1e-4)
sweep-b8: build
	python3 sweep.py b8 --exe $(MDIR)/Vfollow_ring --out $(MDIR)/sweep --jobs $(SWEEP_JOBS) \
	  --jitter-us 0 5 60 --hold-s 40 --switch-hold-s 20 --extra --dwell-s 1.0

sweep-pullin: build
	python3 sweep.py pullin --exe $(MDIR)/Vfollow_ring --out $(MDIR)/sweep --jobs $(SWEEP_JOBS) \
	  --hold-us 52 56

clean:
	rm -rf obj_dir obj_mut __pycache__
