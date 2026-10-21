# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# The media-clock plane and the two listener paths it paces, through a source
# change and through an INTERNAL aligner pull-in (#645, #647):
# follow_ring_wrap.sv binds the real meter, CRF receiver, servo, NCO, aligner,
# capture crossbar LOOP bucket, domain media event and render presentation
# stage (#632), with milan_datapath's own glue between them, the #645 settle
# recentre included, copied verbatim by dp_glue.py.
#   make         - the five standing legs (run)
#   make build   - build the harness (MDIR, default obj_dir)
#   make b8      - lane B8's INTERNAL-to-AAF set, then AAF to CRF and back,
#                  each graded on its settle recentre
#   make pullin  - one serial-clock hold under a running stream at INTERNAL,
#                  graded on its settle recentre
#   make bind    - bench lane B17's binds at INTERNAL, each graded on its
#                  settle recentre, then one under CRF following
#   make mutants - every planted defect must fail its named check
#   make sweep-b8 / sweep-pullin / sweep-bind - the #645 / #647 / B17
#                  campaigns across their phase sweeps (sweep.py; SWEEP_JOBS
#                  at a time), every run graded on the settle law; exit 0
#                  only when every run passed
#   make clean   - remove build artifacts
#
# DEFAULT WALL CLOCK (#645, 2026-10-09): measured at 8e4b1e53 on the
# hosted ubuntu-latest runner, run 37892515345, shard 0/5 job 113696564335.
# Sequential make -C, successive verdict timestamps including build time:
# 1114.2 s PASS, leaving 325.8 s to 1440 s and 685.8 s to the 1800 s guard.
# Cold replica: env -u MAKEFLAGS taskset -c 32-35 make -C
# tb/verilator/follow_ring; serial outer make, 437.204 s. The standing
# legs run in a bounded four-job sub-make with one shared b8/pullin/bind build.
# Historical ratio: 1422.5 / 800.2 rounded up to 1.78, from 1e79ebdc
# (run 37882435947, job 113665137864). Its replica projection was 778.2 s,
# not a hosted measurement: margins 661.8 s to 1440 s and 1021.8 s to 1800 s.
# The replica meets 708 s; the measured hosted window meets 1260 s.
# Later heads still require hosted acceptance. TESTING.md links all receipts.
# The fifteen rebuilt controls remain in make mutants, owned by the manager
# merge bank in TESTING.md; the five default legs retain all their checks.
# #645's bind round added the fifth leg, bind: cold on one four-CPU set of
# a slower host, the five legs took 857.6 s and the four earlier legs
# 800.9 s, so it costs 7.1 % and projects the hosted window to 1193.2 s
# (TESTING.md). That is a projection; hosted acceptance is still owed.
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
       $(RTL_DIR)/ieee1722/crf/KL_media_domain_event.sv \
       $(RTL_DIR)/ieee1722/aaf/KL_render_queue.sv \
       follow_ring_wrap.sv

# --public-flat-rw: the harness reads the servo's window registers and the
# loopback ring's pair pointers; it writes nothing through them.
VFLAGS = --cc --exe --build -j $(VERILATOR_JOBS) --top-module follow_ring_wrap \
         --public-flat-rw -GCLK_HZ_P=$(CLK_HZ) -GFRAME_DIV_P=$(FRAME_DIV) -GTICK_CYC_P=$(AUDIO_TICK_CYC) +incdir+$(SHAPE) +incdir+$(MDIR) $(MUT_DEFS) \
         -Wall -Wno-fatal -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY \
         -Wno-EOFNEWLINE \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra -DCLK_HZ_TB=$(CLK_HZ) -DFRAME_DIV_TB=$(FRAME_DIV)"

.PHONY: all run build b8 pullin bind small-pullin settle-control mutants sweep-b8 sweep-pullin sweep-bind clean
all: run
# The sweep invokes serial outer make. Give these five independent legs a
# bounded pool even there; b8, pullin and bind share one build in this
# sub-make. An outer -jN cannot expand the pool past four leg jobs.
run:
	+$(MAKE) -j4 b8 pullin bind small-pullin settle-control

build:
	mkdir -p $(MDIR)
	python3 dp_glue.py $(DP_SRC) $(MDIR)/dp_glue.svh
	$(VERILATOR) $(VFLAGS) -Mdir $(MDIR) $(SRCS) sim_main.cpp -o Vfollow_ring

# The standing legs. b8 sets AAF at the set phase (0.0) where the servo's
# pull-in leaves the loopback ring half a tick from its empty edge; each hold
# runs past its settle recentre, and the presentation stage is graded on its
# law after each. pullin feeds at the latency whose 52 us hold moved the
# retired setpoint stage off its law (#647), and the presentation stage must
# hold its law across it.
b8: build
	$(abspath $(MDIR))/Vfollow_ring --case b8 --dwell-s 1.0 --set-phase 0.0 --hold-s 16 --switch-hold-s 15

pullin: build
	$(abspath $(MDIR))/Vfollow_ring --case pullin --latency-us 210.42 --after-s 1.5

# bind (#645, bench lane B17): three of B17's ten bind cycles as measured -
# 5 (its burst 94 ms after the first PDU, the earliest and the smallest that
# slipped, then the largest later one), 4 (the largest first burst) and 9
# (the latest first PDU, 161 ms after the bind) - with the first PDU at the
# phase that primes the ring mid B17's window and uniform 0 to 5 us lateness
# (B17's p99.9 was 4.4 to 6.1 us); then cycle 5 under CRF following.
bind: build
	$(abspath $(MDIR))/Vfollow_ring --case bind --b17-cycles 5,4,9 --bind-phase 0.125 --jitter-us 5 \
	  --dwell-s 0.5 --follow-binds 1

# The review's sub-arm pulls at 25 MHz: audio edges resolve 1/64 sample,
# with the real 1 ms servo tick.
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

# sweep-bind: all ten B17 cycles as measured, the first PDU at 16 phases of
# a media tick, without lateness and with B17's 0 to 5 us envelope
sweep-bind: build
	python3 sweep.py bind --exe $(MDIR)/Vfollow_ring --out $(MDIR)/sweep --jobs $(SWEEP_JOBS) \
	  --jitter-us 0 5 --extra --dwell-s 0.5

clean:
	rm -rf obj_dir obj_mut __pycache__
