# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# KL_chan_map_capture lane: the per-pair-slot TX source mux feeding the shared
# KL_aaf_packetizer. Lane A (N=2) checks per-slot routing / remap / disabled-
# slot absence + the map readback; lane B (N=8 all-8ch) exercises the widened
# pair_slot up to slot 31.
VERILATOR ?= verilator
VERILATOR_JOBS ?= 16
TOP = chmap_wrap
# CMAP_SRC and MDIR are overridable so tb/verilator/capture_coherence's
# mutation arm builds a MUTATED COPY of the crossbar through this exact recipe
# into its own directory ([F1] is the check it must break).
CMAP_SRC ?= ../../../hdl/ieee1722/aaf/KL_chan_map_capture.sv
MDIR     ?= obj_dir
SRCS = $(CMAP_SRC) \
       ../../../hdl/ieee1722/aaf/KL_aaf_packetizer.sv \
       ../../../hdl/ieee1722/aaf/KL_tone_gen.sv \
       chmap_wrap.sv
all: run
$(MDIR)/V$(TOP): $(SRCS) sim_main.cpp
	$(VERILATOR) --cc --exe --build -j $(VERILATOR_JOBS) --top-module $(TOP) --Mdir $(MDIR) \
	  -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC \
	  -Wno-PINCONNECTEMPTY -Wno-UNUSEDPARAM -CFLAGS "-std=c++17 -O2 -Wall -Wextra" \
	  $(SRCS) sim_main.cpp
build: $(MDIR)/V$(TOP)
run: $(MDIR)/V$(TOP)
	$(abspath $(MDIR))/V$(TOP)
	$(MAKE) netcheck
	$(MAKE) lockstep
	python3 lockstep_mutants.py

# #640 M6 lockstep leg: the shipping crossbar beside the pre-change reference
# (reference/KL_chan_map_capture_ref.sv, dev e8454e27's module with only its
# name changed) at the shipping 1x1 shape (4 pair slots, one loopback
# stream) and the 8x8 shape (32 slots, eight streams). LS_SRC and LS_MDIR are
# overridable so lockstep_mutants.py builds a MUTATED copy of the crossbar
# through this exact recipe.
LS_SRC  ?= ../../../hdl/ieee1722/aaf/KL_chan_map_capture.sv
LS_MDIR ?= obj_ls
LS_SRCS = reference/KL_chan_map_capture_ref.sv $(LS_SRC) chmap_lockstep_wrap.sv
LS_FLAGS = --cc --exe --build -j $(VERILATOR_JOBS) --top-module chmap_lockstep_wrap \
	  -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC \
	  -Wno-UNUSEDPARAM -Wno-DECLFILENAME -CFLAGS "-std=c++17 -O2 -Wall -Wextra"
lockstep-build:
	$(VERILATOR) $(LS_FLAGS) --Mdir $(LS_MDIR)1 -GN_SLOTS_P=4 -GN_LB_STREAMS_P=1 \
	  -CFLAGS "-DSLOTS_TB=4 -DNLB_TB=1 -Wall -Wextra" $(LS_SRCS) sim_lockstep.cpp -o Vchmap_lockstep
	$(VERILATOR) $(LS_FLAGS) --Mdir $(LS_MDIR)8 -GN_SLOTS_P=32 -GN_LB_STREAMS_P=8 \
	  -CFLAGS "-DSLOTS_TB=32 -DNLB_TB=8 -Wall -Wextra" $(LS_SRCS) sim_lockstep.cpp -o Vchmap_lockstep
lockstep: lockstep-build
	./$(LS_MDIR)1/Vchmap_lockstep
	./$(LS_MDIR)8/Vchmap_lockstep

# [NC] NETLIST-level decode pin (t532 silicon 2026-08-09, the VERSION 0x0030
# hazard class): RTL sims were green while synthesized silicon shifted the
# map-write / LOOP-tap indexing, so this leg simulates a SYNTHESIZED form of
# the module. yosys `proc; opt; memory; opt -full` inlines the functions,
# resolves the always_ff-local temporaries and decomposes BOTH RAMs into
# explicit write-decode + read-mux trees - the structures a stale/shifted
# binding lands in - and sim_netcheck.cpp pins the decode by value: a
# runtime-style write {stream 0, channel k, LOOP rx j} must read back at k
# and the walker must emit channel k carrying rx j (never k+1 / j+1).
# yosys' netlist, not Vivado's: a pin of the hazard class, not a bit repro.
#
# The module is lowered to Verilog-2005 by sv2v FIRST, exactly as
# syn/yosys/run.sh does, and yosys then reads plain Verilog. Reading the
# .sv directly with `read_verilog -sv` works only on a recent yosys: this
# file uses SystemVerilog size casts (the `32'(expr)` at
# KL_chan_map_capture.sv:673), and the yosys Ubuntu ships to CI (0.33)
# rejects them with "syntax error, unexpected TOK_INT" while a 0.66 desk
# build accepts them. Going through sv2v removes the parser-version
# dependency entirely rather than pinning a yosys build in CI.
YOSYS ?= yosys
SV2V  ?= sv2v
NETDIR ?= obj_net
NETLIST = $(NETDIR)/chmap_netlist.v
LOWERED = $(NETDIR)/chmap_lowered.v
$(NETLIST): ../../../hdl/ieee1722/aaf/KL_chan_map_capture.sv
	mkdir -p $(NETDIR)
	$(SV2V) --top=KL_chan_map_capture $< > $(LOWERED)
	$(YOSYS) -q -p "read_verilog $(LOWERED); hierarchy -top KL_chan_map_capture; \
	  proc; opt; memory; opt -full; write_verilog -noattr $(NETLIST)"
$(NETDIR)/Vchmap_netcheck: $(NETLIST) sim_netcheck.cpp
	$(VERILATOR) --cc --exe --build -j $(VERILATOR_JOBS) --top-module KL_chan_map_capture \
	  --Mdir $(NETDIR)/obj_dir -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
	  -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-DECLFILENAME \
	  -CFLAGS "-std=c++17 -O2 -Wall -Wextra" \
	  $(NETLIST) sim_netcheck.cpp -o ../Vchmap_netcheck
netcheck: $(NETDIR)/Vchmap_netcheck
	$(abspath $(NETDIR))/Vchmap_netcheck

clean: ; rm -rf obj_dir obj_net obj_ls1 obj_ls8
.PHONY: all build run clean netcheck lockstep-build lockstep
