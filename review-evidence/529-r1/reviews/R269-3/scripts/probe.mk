# R269-3 probe wrapper. Copy into tb/verilator/milan_dp of a DISPOSABLE tree
# and run `make -f probe.mk <target> MDIR=<objdir> [DP_SRC=<rtl copy>]
# [NXN_CPP=<harness copy>] VERILATOR=<pinned 5.050>`. Each target repeats the
# suite Makefile's own `run` recipe line for that leg, through the suite's own
# variables (SRCS, DP_VFLAGS, shapes), with only --Mdir and the harness file
# made overridable.
include Makefile

MDIR    ?= obj_probe
NXN_CPP ?= sim_nxn.cpp

.PHONY: probe-hex probe-nxn probe-nxn8 probe-notify probe-nxndv probe-nxn4c
probe-hex: ltn_rom.hex ucode.hex gptp_ucode.hex

probe-nxn: probe-hex $(GEN_ALL)
	$(VERILATOR) $(SHAPE_4x4) $(DP_VFLAGS) --Mdir $(MDIR) -GN_STREAMS=4 $(SRCS) $(NXN_CPP) -o Vmilan_dp_nxn

probe-nxn8: probe-hex $(GEN_ALL)
	$(VERILATOR) $(SHAPE_8x8) $(DP_VFLAGS) --Mdir $(MDIR) -GN_STREAMS=8 -GLOOPBACK_P=1 -CFLAGS "-DNSTREAMS_TB=8 -DAX8X8_TB=1 -DLOOPBACK_TB=1 -DLB_SEQ_FIXED=1 -Wall -Wextra" $(SRCS) $(NXN_CPP) -o Vmilan_dp_nxn8

probe-nxndv: probe-hex $(GEN_ALL) $(SHAPE_DV_F)
	$(VERILATOR) $(SHAPE_DV) $(DP_VFLAGS) --Mdir $(MDIR) -GN_STREAMS=4 -CFLAGS "-DNSTREAMS_TB=4 -DDIVERGENT_TB=1 -I$(CURDIR)/gen_divergent -Wall -Wextra" $(SRCS) $(NXN_CPP) -o Vmilan_dp_nxndv

probe-nxn4c: probe-hex $(GEN_ALL)
	$(VERILATOR) $(SHAPE_4x4) $(DP_VFLAGS) --Mdir $(MDIR) -GN_STREAMS=4 \
	  -GTALKER_WIRE_CHANS_P=4 -GAUDIO_IF_SLOTS_P=8 -GAUDIO_IF_MASTER_P=1 \
	  -GAUDIO_IF_I2S_PAIR_P=1 $(SRCS) $(NXN_CPP) -o Vmilan_dp_nxn4c

probe-notify: probe-hex $(GEN_ALL)
	$(VERILATOR) $(SHAPE_AX1x1) $(GPTP_OFF_VFLAGS) --Mdir $(MDIR) \
	  -GPP_TIM_DIV_US_P=1 -GPP_TIM_DIV_MS_P=100 \
	  -CFLAGS "-DNSTREAMS_TB=1 -DNOTIFY_TIMED_TB=1 -DMS_CYC_TB=100 -Wall -Wextra" \
	  $(SRCS) $(NXN_CPP) -o Vmilan_dp_notify
