# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of the full AECP/AEM listener subsystem (KL_aecp_top):
# drives real AECP command Ethernet frames into the RX monitor tap and checks
# the response frames byte-for-byte. Pure RTL, no Xilinx tools.
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL        = ../../../hdl
GEN        = $(RTL)/aecp/gen/aecp_aem_rom.svh
TOP        = KL_aecp_top

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -I$(RTL)/aecp -I$(RTL)/common \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-CASEINCOMPLETE \
         -CFLAGS "-std=c++17 -O2 -I.."

SRCS = $(RTL)/aecp/aecp_pkg.sv \
       $(RTL)/adp/adp_pkg.sv \
       $(RTL)/common/axi_stream_if.sv \
       ../../../third_party/verilog-axis/rtl/axis_fifo.v \
       $(RTL)/aecp/KL_aecp_ingress.sv \
       $(RTL)/aecp/KL_aecp_packet_validator.sv \
       $(RTL)/aecp/KL_aecp_common_parser.sv \
       $(RTL)/aecp/KL_aecp_l0_state.sv \
       $(RTL)/aecp/KL_aecp_timers.sv \
       $(RTL)/aecp/KL_aecp_accessor.sv \
       $(RTL)/aecp/KL_aecp_aem_store.sv \
       $(RTL)/aecp/KL_aecp_aem_dyn_mux.sv \
       $(RTL)/aecp/KL_aecp_response_builder.sv \
       $(RTL)/aecp/KL_aecp_top.sv
CPP  = sim_main.cpp

.PHONY: all run clean
all: run

run: $(GEN)
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vaecp_sim
	@echo "======================================================================"
	./obj_dir/Vaecp_sim

$(GEN):
	cd ../../.. && python3 avdecc/gen_aem_store.py

# tsn-gen <-> Verilator co-sim harness: a UNIX-socket AECP responder DUT.
COSIM_FLAGS = --cc --exe --build -j 0 --top-module $(TOP) \
              -I$(RTL)/aecp -I$(RTL)/common \
              -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
              -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-CASEINCOMPLETE \
              -CFLAGS "-std=c++17 -O2"
cosim: $(GEN)
	$(VERILATOR) $(COSIM_FLAGS) $(SRCS) cosim_main.cpp -o Vaecp_cosim

clean:
	rm -rf obj_dir
