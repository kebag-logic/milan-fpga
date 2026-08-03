# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# E4 — the AEM dynamic-state ingest port (CSR 0x7C8-0x7D4).
#
# Gates the master that closes Milan v1.2 persistence: a descriptor-addressed
# patch port into KL_aecp_aem_store that is accepted ONLY while the ADP
# advertiser is down, so "replay before you advertise" is structural. The
# suite's central leg is a ROUND TRIP — restore over CSR, advertise, read the
# value back over a normal GET_STREAM_FORMAT — because storing a byte is not
# the clause; answering with it is.
#
# SHAPE IS PINNED ON PURPOSE. gen/aecp_aem_rom.svh under hdl/ieee17221/aecp/
# is whichever config was last written with `--write-rtl`, so a harness that
# relies on it silently re-targets itself when another lane regenerates the
# tree. The config dir comes FIRST on the include path so its gen/ wins the
# search, exactly as tb/verilator/aecp does.

VERILATOR ?= verilator
RTL        = ../../../hdl
GEN        = $(RTL)/ieee17221/aecp/gen/aecp_aem_rom.svh
TOP        = aempatch_wrap

CFG_DIR    = ../../../configs/generated
SHAPE_8x8  = -I$(CFG_DIR)/endstation_ax7101_8x8

VFLAGS = $(SHAPE_8x8) --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -I$(RTL)/ieee17221/aecp -I$(RTL)/common \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-CASEINCOMPLETE -Wno-GENUNNAMED \
         -CFLAGS "-std=c++17 -O2"

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
       $(RTL)/ieee17221/aecp/KL_aem_patch.sv \
       $(RTL)/ieee17221/aecp/KL_aecp_response_builder.sv \
       $(RTL)/ieee17221/aecp/KL_aecp_top.sv \
       aempatch_wrap.sv

#! The store's write-port arbiter cannot be collided from the frame level —
#! the patch port is closed exactly when the AECP engine is live — so it gets
#! its own tiny executable against the RAM directly. A mutation campaign is
#! why: flipping the arbitration priority left the frame-level suite green.
STORE_SRCS = $(RTL)/ieee17221/aecp/aecp_pkg.sv \
             $(RTL)/ieee17221/aecp/KL_aecp_aem_store.sv

all: run

$(GEN):
	cd ../../.. && python3 avdecc/gen_aem_store.py

obj_dir/V$(TOP): $(GEN) $(SRCS) sim_main.cpp
	$(VERILATOR) $(VFLAGS) $(SRCS) sim_main.cpp

obj_store/VKL_aecp_aem_store: $(GEN) $(STORE_SRCS) sim_store.cpp
	$(VERILATOR) $(SHAPE_8x8) --cc --exe --build -j 0 \
	  --top-module KL_aecp_aem_store --Mdir obj_store \
	  -I$(RTL)/ieee17221/aecp -I$(RTL)/common \
	  -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
	  -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-GENUNNAMED \
	  -CFLAGS "-std=c++17 -O2" \
	  $(STORE_SRCS) sim_store.cpp

run: obj_dir/V$(TOP) obj_store/VKL_aecp_aem_store
	./obj_dir/V$(TOP)
	./obj_store/VKL_aecp_aem_store

clean:
	rm -rf obj_dir obj_store

.PHONY: all run clean
