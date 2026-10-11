# Reviewer probe: build and run ONE sim_nxn leg through milan_dp's own recipe.
# Usage: make -C tb/verilator/milan_dp -f <this> nxnonly NXN_MDIR=... [DP_SRC=...] [NXN_SHAPE=4|8]
include Makefile
NXN_MDIR ?= obj_r600_nxn
NXN_SHAPE ?= 4
ifeq ($(NXN_SHAPE),8)
NXN_G = $(SHAPE_8x8) $(DP_VFLAGS) --Mdir $(NXN_MDIR) -GN_STREAMS=8 -GLOOPBACK_P=1 -CFLAGS "-DNSTREAMS_TB=8 -DAX8X8_TB=1 -DLOOPBACK_TB=1 -DLB_SEQ_FIXED=1 -Wall -Wextra"
else
NXN_G = $(SHAPE_4x4) $(DP_VFLAGS) --Mdir $(NXN_MDIR) -GN_STREAMS=4
endif
nxnprereq: ltn_rom.hex ucode.hex gptp_ucode.hex $(GEN_ALL)
nxnbuild:
	$(VERILATOR) $(NXN_G) $(SRCS) sim_nxn.cpp -o Vmilan_dp_nxn
nxnonly: nxnbuild
	./$(NXN_MDIR)/Vmilan_dp_nxn
