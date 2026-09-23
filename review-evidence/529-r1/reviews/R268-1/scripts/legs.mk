# Reviewer probe legs. Included AFTER tb/verilator/milan_dp/Makefile with
#   make -f Makefile -f <this> <target> DP_SRC=<copy> R_MDIR=<dir>
# so every build reuses the suite's own SRCS / DP_VFLAGS / SHAPE_* variables.
# Only the Mdir differs, so a mutant never overwrites the positive build.
R_MDIR ?= obj_r
# harness source; a reviewer probe may point this at a copy in the suite dir
R_CPP ?= sim_nxn.cpp
.PHONY: r_prereq r_nxn r_nxndv r_nxn8 r_nxn4c r_notify
r_prereq: ltn_rom.hex ucode.hex gptp_ucode.hex $(GEN_ALL) $(SHAPE_DV_F)
r_nxn: r_prereq
	$(VERILATOR) $(SHAPE_4x4) $(DP_VFLAGS) --Mdir $(R_MDIR) -GN_STREAMS=4 $(SRCS) $(R_CPP) -o Vmilan_dp_nxn
r_nxndv: r_prereq
	$(VERILATOR) $(SHAPE_DV) $(DP_VFLAGS) --Mdir $(R_MDIR) -GN_STREAMS=4 -CFLAGS "-DNSTREAMS_TB=4 -DDIVERGENT_TB=1 -I$(CURDIR)/gen_divergent -Wall -Wextra" $(SRCS) $(R_CPP) -o Vmilan_dp_nxndv
r_nxn8: r_prereq
	$(VERILATOR) $(SHAPE_8x8) $(DP_VFLAGS) --Mdir $(R_MDIR) -GN_STREAMS=8 -GLOOPBACK_P=1 -CFLAGS "-DNSTREAMS_TB=8 -DAX8X8_TB=1 -DLOOPBACK_TB=1 -DLB_SEQ_FIXED=1 -Wall -Wextra" $(SRCS) $(R_CPP) -o Vmilan_dp_nxn8
r_nxn4c: r_prereq
	$(VERILATOR) $(SHAPE_4x4) $(DP_VFLAGS) --Mdir $(R_MDIR) -GN_STREAMS=4 -GTALKER_WIRE_CHANS_P=4 -GAUDIO_IF_SLOTS_P=8 -GAUDIO_IF_MASTER_P=1 -GAUDIO_IF_I2S_PAIR_P=1 $(SRCS) $(R_CPP) -o Vmilan_dp_nxn4c
r_notify: r_prereq
	$(VERILATOR) $(SHAPE_AX1x1) $(GPTP_OFF_VFLAGS) --Mdir $(R_MDIR) -GPP_TIM_DIV_US_P=1 -GPP_TIM_DIV_MS_P=100 -CFLAGS "-DNSTREAMS_TB=1 -DNOTIFY_TIMED_TB=1 -DMS_CYC_TB=100 -Wall -Wextra" $(SRCS) $(R_CPP) -o Vmilan_dp_notify
