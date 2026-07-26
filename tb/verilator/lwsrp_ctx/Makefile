# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of KL_lwsrp_top.sv with N_CTX_P = 4 — the
# N-attribute context table (docs/MILAN_COMPLIANCE_GAPS.md §3 closure):
#   - N=1-shape golden equivalence: with zero extra rows provisioned the
#     declare pair is BYTE-IDENTICAL to the legacy engine's frames
#   - CRF-listener row: provision -> Listener attr on the wire, Ready
#     follows the TA registration, TalkerFailed capture + readback
#   - extra talker row: full 25-byte TalkerAdvertise FirstValue from the
#     record RAM, bridge Listener Ready via +k vector
#   - multi-attribute MRPDU packing (TalkerAdv + 2-vector Listener msg)
#   - one bridge vector covering MULTIPLE contexts at different +k
#   - add/remove mid-stream (LV withdraw), LeaveAll aging across contexts
# and sim_rowmap.cpp at the REAL 0x800 window shape (N_CTX_P = L+T-1 = 7,
# L = T = 4):
#   - talker t's admission gate reads ctx row (L-1)+t, and three provisioned
#     LISTENER rows (the rows the gate used to read) move NO talker gate
#   - per-row TSpec: three geometries, each row's own MaxFrameSize in its own
#     TalkerAdvertise vector and its own slope in the Sigma
#   - out-of-range rows are LOUD: 0xDEAD readback instead of aliasing row 0,
#     sticky ctx_oor_o, in-range rows unharmed
#   make        - build and run the self-checking harness
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
AXIS_DIR   = ../../../third_party/verilog-axis/rtl
TOP        = KL_lwsrp_top

VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -GCLK_FREQ_HZ_P=10000 -GN_CTX_P=4 \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY \
         -CFLAGS "-std=c++17 -O2"

SRCS = $(RTL_DIR)/ieee8021q/srp/lwsrp_pkg.sv \
       $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_timers.sv \
       $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_tx.sv \
       $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_ingress.sv \
       $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_walker.sv \
       $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_registrar.sv $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_ta_registrar.sv \
       $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_rx.sv \
       $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_bw_gate.sv \
       $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_ctx.sv \
       $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_ctx_tx.sv \
       $(RTL_DIR)/ieee8021q/srp/KL_lwsrp_top.sv \
       $(AXIS_DIR)/axis_fifo.v
CPP  = sim_main.cpp

# Second shape: the REAL 0x800 window row map at L = T = 4 (arty 4x4), i.e.
# N_CTX_P = L+T-1 = 7 attribute rows with talker t at ctx row (L-1)+t. This
# is the build the row-map / per-row-TSpec / out-of-range gates run on.
RMFLAGS = --cc --exe --build -j 0 \
          --top-module $(TOP) \
          -GCLK_FREQ_HZ_P=10000 -GN_CTX_P=7 -GN_LISTENERS_P=4 -GN_TALKERS_P=4 \
          -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
          -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY \
          -CFLAGS "-std=c++17 -O2"

.PHONY: all run clean
all: run

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vlwsrp_ctx_sim
	$(VERILATOR) $(RMFLAGS) --Mdir obj_rowmap $(SRCS) sim_rowmap.cpp -o Vlwsrp_rowmap_sim
	@echo "======================================================================"
	./obj_dir/Vlwsrp_ctx_sim
	./obj_rowmap/Vlwsrp_rowmap_sim

clean:
	rm -rf obj_dir obj_rowmap
