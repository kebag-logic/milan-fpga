# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# KL_chan_map_capture lane: the per-pair-slot TX source mux feeding the shared
# KL_aaf_packetizer. Lane A (N=2) checks per-slot routing / remap / disabled-
# slot absence + the map readback; lane B (N=8 all-8ch) exercises the widened
# pair_slot up to slot 31.
VERILATOR ?= verilator
TOP = chmap_wrap
SRCS = ../../../hdl/ieee1722/aaf/KL_chan_map_capture.sv \
       ../../../hdl/ieee1722/aaf/KL_aaf_packetizer.sv \
       ../../../hdl/ieee1722/aaf/KL_tone_gen.sv \
       chmap_wrap.sv
all: run
obj_dir/V$(TOP): $(SRCS) sim_main.cpp
	$(VERILATOR) --cc --exe --build -j 0 --top-module $(TOP) \
	  -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC \
	  -Wno-PINCONNECTEMPTY -Wno-UNUSEDPARAM -CFLAGS "-std=c++17 -O2" \
	  $(SRCS) sim_main.cpp
run: obj_dir/V$(TOP)
	./obj_dir/V$(TOP)
	$(MAKE) netcheck

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
NETLIST = obj_net/chmap_netlist.v
LOWERED = obj_net/chmap_lowered.v
$(NETLIST): ../../../hdl/ieee1722/aaf/KL_chan_map_capture.sv
	mkdir -p obj_net
	$(SV2V) --top=KL_chan_map_capture $< > $(LOWERED)
	$(YOSYS) -q -p "read_verilog $(LOWERED); hierarchy -top KL_chan_map_capture; \
	  proc; opt; memory; opt -full; write_verilog -noattr $(NETLIST)"
obj_net/Vchmap_netcheck: $(NETLIST) sim_netcheck.cpp
	$(VERILATOR) --cc --exe --build -j 0 --top-module KL_chan_map_capture \
	  --Mdir obj_net/obj_dir -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
	  -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-DECLFILENAME \
	  -CFLAGS "-std=c++17 -O2" \
	  $(NETLIST) sim_netcheck.cpp -o ../Vchmap_netcheck
netcheck: obj_net/Vchmap_netcheck
	./obj_net/Vchmap_netcheck

clean: ; rm -rf obj_dir obj_net
.PHONY: all run clean netcheck
