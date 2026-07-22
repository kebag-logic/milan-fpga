# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of the full AECP/AEM listener subsystem (KL_aecp_top):
# drives real AECP command Ethernet frames into the RX monitor tap and checks
# the response frames byte-for-byte. Pure RTL, no Xilinx tools.
# Two executables:
#   sim_main.cpp -> deployed shape (tracked gen/aecp_aem_rom.svh)
#   sim_fmt2.cpp -> 2-AAF-input shape (gen_fmt2_shape.py -> fmt2_inc/, which
#     SHADOWS gen/ via include order) exercising the per-stream
#     `AEM_PER_STREAM_FMT format tables per descriptor.
#   make        - build and run both self-checking harnesses
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL        = ../../../hdl
GEN        = $(RTL)/ieee17221/aecp/gen/aecp_aem_rom.svh
TOP        = KL_aecp_top

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -I$(RTL)/ieee17221/aecp -I$(RTL)/common \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-CASEINCOMPLETE \
         -CFLAGS "-std=c++17 -O2 -I.."

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
	@echo "======================================================================"
	./obj_dir/Vaecp_sim
	./obj_fmt2/Vaecp_fmt2

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
	rm -rf obj_dir obj_fmt2 fmt2_inc
