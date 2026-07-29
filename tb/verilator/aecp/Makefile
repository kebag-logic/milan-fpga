# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of the full AECP/AEM listener subsystem (KL_aecp_top):
# drives real AECP command Ethernet frames into the RX monitor tap and checks
# the response frames byte-for-byte. Pure RTL, no Xilinx tools.
# Three executables:
#   sim_main.cpp   -> deployed shape (tracked gen/aecp_aem_rom.svh)
#   sim_fmt2.cpp   -> 2-AAF-input shape (gen_fmt2_shape.py -> fmt2_inc/, which
#     SHADOWS gen/ via include order) exercising the per-stream
#     `AEM_PER_STREAM_FMT format tables per descriptor.
#   sim_amap.cpp   -> 8x8 ship shape, GET_AUDIO_MAP port-relative bounds
#     (defect A: the served map came from a hardcoded AUDIO_MAP index with a
#     hardcoded length, which only coincides with the right one at 1x1).
#   sim_dynmap.cpp -> dynamic-audio-map shape (gen_dynmap_shape.py ->
#     dynmap_inc/, same shadowing) exercising the `AEM_DYNMAP
#     ADD/REMOVE/GET_AUDIO_MAP engine (Milan 5.4.2.26-28).
#   sim_pools.cpp  -> D8 ROLE-POOL shape (gen_pools_shape.py -> pools_inc/,
#     same shadowing): host/pilot/loopback cluster pools on a board that
#     routes NO audio pins, role-derived AUDIO_CLUSTER object_names, and
#     the 1722.1-2021 7.2.19 port-relative AUDIO_MAP offsets that let two
#     talker ports carry IDENTICAL offsets onto DIFFERENT clusters.
#   sim_dynmap2.cpp -> MULTI-PORT dynamic shape (gen_dynmap2_shape.py ->
#     dynmap2_inc/): two dynamic STREAM_PORT_INPUTs + three stream inputs,
#     i.e. `AEM_DYNMAP and `AEM_PER_STREAM_FMT together, which is what a
#     4x4 / 8x8 listener build compiles (Milan 5.3.3.9 dynamic on ALL
#     Stream Port Inputs).
#   make        - build and run all self-checking harnesses
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL        = ../../../hdl
GEN        = $(RTL)/ieee17221/aecp/gen/aecp_aem_rom.svh
TOP        = KL_aecp_top

# This suite asserts DESCRIPTOR CONTENT, so it must name the entity whose
# descriptors it expects. gen/aecp_aem_rom.svh under hdl/ieee17221/aecp/ is
# whichever config was last written with --write-rtl; regenerating the tree
# for the 8x8 ship shape pointed this 1x1 harness at an 8x8 descriptor set
# (NO_SUCH_DESCRIPTOR, wrong current_format). The config dir comes FIRST so
# its gen/ wins the include search.
CFG_DIR    = ../../../configs/generated
SHAPE_1x1  = -I$(CFG_DIR)/endstation_arty_current
# The SHIP shape, tracked: 9 STREAM_INPUT + 9 STREAM_OUTPUT, exactly the
# descriptor set the AX7101 gateware carries. sim_nxn.cpp needs it because
# the 1x1 and 1x3 harnesses structurally cannot see an index-coverage defect.
SHAPE_8x8  = -I$(CFG_DIR)/endstation_ax7101_8x8

VBASE  = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -I$(RTL)/ieee17221/aecp -I$(RTL)/common \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-CASEINCOMPLETE \
         -CFLAGS "-std=c++17 -O2 -I.."
VFLAGS     = $(SHAPE_1x1) $(VBASE)
VFLAGS_NXN = $(SHAPE_8x8) $(VBASE)

SRCS = $(RTL)/ieee17221/aecp/aecp_pkg.sv \
       $(RTL)/ieee17221/adp/adp_pkg.sv \
       $(RTL)/common/axi_stream_if.sv \
       ../../../third_party/verilog-axis/rtl/axis_fifo.v \
       $(RTL)/ieee17221/aecp/KL_aecp_ingress.sv \
       $(RTL)/ieee17221/aecp/KL_aecp_packet_validator.sv \
       $(RTL)/ieee17221/aecp/KL_aecp_common_parser.sv \
       $(RTL)/ieee17221/aecp/KL_aecp_l0_state.sv \
       $(RTL)/ieee17221/aecp/KL_aecp_timers.sv \
       $(RTL)/ieee17221/aecp/KL_aecp_accessor.sv \
       $(RTL)/ieee17221/aecp/KL_aecp_aem_store.sv \
       $(RTL)/ieee17221/aecp/KL_aecp_aem_dyn_mux.sv \
       $(RTL)/ieee17221/aecp/KL_aecp_response_builder.sv \
       $(RTL)/ieee17221/aecp/KL_aecp_top.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run: $(GEN)
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vaecp_sim
	python3 gen_fmt2_shape.py fmt2_inc
	$(VERILATOR) -Ifmt2_inc $(VFLAGS) --Mdir obj_fmt2 \
	  $(SRCS) sim_fmt2.cpp -o Vaecp_fmt2   # -Ifmt2_inc FIRST: shadows gen/
	python3 gen_dynmap_shape.py dynmap_inc
	$(VERILATOR) -Idynmap_inc $(VFLAGS) --Mdir obj_dynmap \
	  $(SRCS) sim_dynmap.cpp -o Vaecp_dynmap   # -Idynmap_inc shadows gen/
	$(VERILATOR) $(VFLAGS_NXN) --Mdir obj_nxn \
	  $(SRCS) sim_nxn.cpp -o Vaecp_nxn         # 8x8 ship shape (D1/D2)
	$(VERILATOR) $(VFLAGS_NXN) --Mdir obj_amap \
	  $(SRCS) sim_amap.cpp -o Vaecp_amap       # 8x8 ship shape (defect A)
	python3 gen_pools_shape.py pools_inc
	$(VERILATOR) -Ipools_inc $(VFLAGS) --Mdir obj_pools \
	  $(SRCS) sim_pools.cpp -o Vaecp_pools     # -Ipools_inc shadows gen/
	python3 gen_dynmap2_shape.py dynmap2_inc
	$(VERILATOR) -Idynmap2_inc $(VFLAGS) --Mdir obj_dynmap2 \
	  $(SRCS) sim_dynmap2.cpp -o Vaecp_dynmap2 # -Idynmap2_inc shadows gen/
	@echo "======================================================================"
	./obj_dir/Vaecp_sim
	./obj_fmt2/Vaecp_fmt2
	./obj_dynmap/Vaecp_dynmap
	./obj_nxn/Vaecp_nxn
	./obj_amap/Vaecp_amap
	./obj_pools/Vaecp_pools
	./obj_dynmap2/Vaecp_dynmap2

$(GEN):
	cd ../../.. && python3 avdecc/gen_aem_store.py

# tsn-gen <-> Verilator co-sim harness: a UNIX-socket AECP responder DUT.
COSIM_FLAGS = --cc --exe --build -j 0 --top-module $(TOP) \
              -I$(RTL)/ieee17221/aecp -I$(RTL)/common \
              -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
              -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-CASEINCOMPLETE \
              -CFLAGS "-std=c++17 -O2"
cosim: $(GEN)
	$(VERILATOR) $(COSIM_FLAGS) $(SRCS) cosim_main.cpp -o Vaecp_cosim

clean:
	rm -rf obj_dir obj_fmt2 fmt2_inc obj_dynmap dynmap_inc obj_nxn obj_amap
	rm -rf obj_dir obj_fmt2 fmt2_inc obj_dynmap dynmap_inc obj_pools pools_inc
	rm -rf obj_dir obj_fmt2 fmt2_inc obj_dynmap dynmap_inc \
	       obj_dynmap2 dynmap2_inc
