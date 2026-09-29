# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# AAF column coherence at the TDM capture junction (#617). The real TDM8
# master front end, media NCO, grid aligner, capture crossbar and packetizer,
# bound as milan_datapath binds them on the shipping AX7101 1x1 TDM8 shape,
# with the #451 pattern shifted into the TDM data pin and every AAF column
# the talker emits decoded. INTERNAL drift sweeps on the true 391/1591 plan
# (one whole beat) and on +/-1000 ppm plans, then CRF: locks at sixteen
# phases on the true plan and at four on +/-50 ppm plans, and the aligner's
# engagement PLACED against the capture walk's crossing - every cycle across
# +/-32 of it and every 16 round the frame on the true plan, every 4 across
# the +/-50 ppm acquisition band, every quarter cycle at 64 sub-step phases
# across the crossing at -50 ppm, and the approach to the settled lock at
# +/-80 and +/-100 ppm (sim_main.cpp's header lists them). A second leg runs
# the same bench against the whole milan_datapath on the shipping shape, with
# its own placed band.
#   make         - both legs, then the mutation arm (in parallel, one build
#                  per CPU: mutants.py)
#   make run     - the junction harness alone
#   make dp      - the milan_datapath leg alone
#   make mutants - the mutation arm alone (mutants.py)
#   make clean   - remove build artifacts
VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
AAF        = $(RTL_DIR)/ieee1722/aaf
CRF        = $(RTL_DIR)/ieee1722/crf
TOP        = coherence_wrap

# THE SHIPPING 1x1 TDM8 SHAPE, stated once: every value feeds BOTH the -G
# that builds the wrapper and the -D that tells the harness what it drives.
# The axis clock is the shape's milan_clk_hz (configs/
# endstation_ax7101_1x1_tdm8.yaml), and the LOOP bucket is its backed
# loopback lane (one stream of eight channels).
CLK_HZ      = 50000000
N_TALKERS   = 1
WIRE_CHANS  = 8
TDM_SLOTS   = 8
LB_STREAMS  = 1
LB_CH       = 8

GFLAGS = -GCLK_HZ_P=$(CLK_HZ) -GN_TALKERS_P=$(N_TALKERS) -GWIRE_CHANS_P=$(WIRE_CHANS) \
         -GTDM_SLOTS_P=$(TDM_SLOTS) -GLB_STREAMS_P=$(LB_STREAMS) -GLB_CH_P=$(LB_CH)
DFLAGS = -DCLK_HZ_TB=$(CLK_HZ) -DWIRE_CHANS_TB=$(WIRE_CHANS) -DTDM_SLOTS_TB=$(TDM_SLOTS)

VFLAGS = --cc --exe --build -j 0 --top-module $(TOP) $(GFLAGS) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra $(DFLAGS)"
# CMAP_SRC, NCO_SRC, WRAP_SRC and MDIR are overridable so the mutation arm
# builds a MUTATED COPY of the crossbar, of the media NCO, or of the wrapper's
# aligner binding, with this exact flag set, into its own directory, through
# the same recipe - one statement of how the harness is built.
CMAP_SRC ?= $(AAF)/KL_chan_map_capture.sv
NCO_SRC  ?= $(CRF)/KL_media_nco.sv
WRAP_SRC ?= coherence_wrap.sv
MDIR     ?= obj_dir
SRCS = $(RTL_DIR)/common/cdc_pair_fifo.sv \
       $(AAF)/KL_tdm_capture_master.sv \
       $(NCO_SRC) \
       $(CRF)/KL_media_grid_align.sv \
       $(CMAP_SRC) \
       $(AAF)/KL_aaf_packetizer.sv \
       $(WRAP_SRC)
EXE  = Vcoherence_sim
CPP  = sim_main.cpp

.PHONY: all run build dp dp-build mutants clean
.DEFAULT_GOAL := all
all: run dp mutants

# THE ALIGNER KEEP-OFF IS THE DATAPATH'S, NOT A RESTATEMENT: mga_keepoff.py
# copies milan_datapath's MGA_* declarations out of DP_SRC (below) into the
# build directory, where the wrapper `include-s them. So a datapath mutant
# (the mutation arm's band50 leg) reaches this leg as well. It refuses a
# DP_SRC whose aligner instance binds its keep-off to anything else, so a
# literal there cannot pass unseen (RM9).
build:
	mkdir -p $(MDIR)
	python3 mga_keepoff.py $(DP_SRC) $(MDIR)/mga_keepoff.svh
	$(VERILATOR) $(VFLAGS) +incdir+$(MDIR) --Mdir $(MDIR) $(SRCS) $(CPP) -o $(EXE)

run: build
	@echo "======================================================================"
	$(abspath $(MDIR))/$(EXE)

# THE WHOLE DATAPATH, on the shape the AX7101 flashes. Its source list and
# elaboration flag set are tb/verilator/milan_dp's own (print-srcs,
# print-dp-vflags), so this leg elaborates the same gateware that suite does;
# DP_SRC passes through so the mutation arm can elaborate a mutated datapath
# through this same recipe. The shape values are sw/litex/build.sh
# cfg_ax7101's, and the milan clock is the shape's 50 MHz.
# --no-print-directory: both lists are the nested make's stdout, and a print-
# directory flag it inherits (GNU make 4.3 hands a `make -C` recipe
# MAKEFLAGS=w, which reached the mutation arm's builds on the hosted runner)
# would write "Entering directory" into them (#617 R394-3 F1).
DP_DIR   = ../milan_dp
PP_DIR   = ../../../protocol-processor/hdl
DP_SRC  ?= $(RTL_DIR)/milan/milan_datapath.sv
DP_MDIR ?= obj_dp
DP_SRCS  := $(shell $(MAKE) -s --no-print-directory -C $(DP_DIR) print-srcs DP_SRC='$(DP_SRC)')
ifneq ($(.SHELLSTATUS),0)
$(error $(DP_DIR) print-srcs failed; the datapath source list could not be derived)
endif
DP_VFLAGS := $(shell $(MAKE) -s --no-print-directory -C $(DP_DIR) print-dp-vflags)
ifneq ($(.SHELLSTATUS),0)
$(error $(DP_DIR) print-dp-vflags failed; the elaboration flag set could not be derived)
endif
SHAPE_AX1x1 = +incdir+../../../configs/generated/endstation_ax7101_1x1_tdm8
DP_GFLAGS = -GMILAN_CLK_FREQ_HZ=$(CLK_HZ) -GN_STREAMS=$(N_TALKERS) \
            -GTALKER_WIRE_CHANS_P=$(WIRE_CHANS) -GAUDIO_IF_SLOTS_P=$(TDM_SLOTS) \
            -GAUDIO_IF_MASTER_P=1 -GAUDIO_IF_RENDER_SLOTS_P=$(TDM_SLOTS) \
            -GLOOPBACK_P=1 -GI2SPB_P=0 -GLPF_P=0

# The ACMP listener transition ROM and the AECP uCPU microcode are GENERATED,
# and the processor $$readmemh's them by these relative names - so they must
# exist in the RUN directory.
ltn_rom.hex: $(PP_DIR)/acmp/rom/gen_ltn_rom.py
	python3 $< -o $@

ucode.hex: $(PP_DIR)/aecp/ucode/gen_ucode.py
	python3 $< -o $@

dp-build: ltn_rom.hex ucode.hex
	$(VERILATOR) $(SHAPE_AX1x1) $(DP_VFLAGS) --Mdir $(DP_MDIR) $(DP_GFLAGS) \
	  -CFLAGS "$(DFLAGS) -Wall -Wextra" $(DP_SRCS) sim_dp.cpp -o Vcoherence_dp

dp: dp-build
	@echo "======================================================================"
	$(abspath $(DP_MDIR))/Vcoherence_dp

# Rule 8: the harness is load-bearing only if it can fail. Defects are
# planted in a copy of the real crossbar, one at a time, and each must make
# the SAME harness fail by its own verdict and by the check it names; the
# unmutated build must still pass. Mutants build in a temporary directory,
# in parallel, one per CPU this process may use; nothing is written into the
# tree.
mutants:
	@echo "======================================================================"
	python3 mutants.py

clean:
	rm -rf obj_dir obj_dp ltn_rom.hex ucode.hex
