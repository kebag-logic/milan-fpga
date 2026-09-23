# [A216] probe legs for #529. Included AFTER tb/verilator/milan_dp/Makefile:
#   make -f Makefile -f <this> a_<leg> DP_SRC=<datapath copy> A_MDIR=<dir>
# Each target is the suite's own `run` recipe line for that leg (same SRCS,
# DP_VFLAGS/GPTP_OFF_VFLAGS, shape and -G/-D set); only the Mdir differs, so a
# mutant build never overwrites the positive one.
A_MDIR ?= obj_a
# harness source, relative to the suite directory (a baseline copy may sit there)
A_CPP ?= sim_nxn.cpp
.PHONY: a_prereq a_nxn a_nxndv a_nxn8 a_nxn4c a_notify
a_prereq: ltn_rom.hex ucode.hex gptp_ucode.hex $(GEN_ALL) $(SHAPE_DV_F)
a_nxn: a_prereq
	$(VERILATOR) $(SHAPE_4x4) $(DP_VFLAGS) --Mdir $(A_MDIR) -GN_STREAMS=4 $(SRCS) $(A_CPP) -o Vmilan_dp_nxn
a_nxndv: a_prereq
	$(VERILATOR) $(SHAPE_DV) $(DP_VFLAGS) --Mdir $(A_MDIR) -GN_STREAMS=4 -CFLAGS "-DNSTREAMS_TB=4 -DDIVERGENT_TB=1 -I$(CURDIR)/gen_divergent -Wall -Wextra" $(SRCS) $(A_CPP) -o Vmilan_dp_nxndv
a_nxn8: a_prereq
	$(VERILATOR) $(SHAPE_8x8) $(DP_VFLAGS) --Mdir $(A_MDIR) -GN_STREAMS=8 -GLOOPBACK_P=1 -CFLAGS "-DNSTREAMS_TB=8 -DAX8X8_TB=1 -DLOOPBACK_TB=1 -DLB_SEQ_FIXED=1 -Wall -Wextra" $(SRCS) $(A_CPP) -o Vmilan_dp_nxn8
a_nxn4c: a_prereq
	$(VERILATOR) $(SHAPE_4x4) $(DP_VFLAGS) --Mdir $(A_MDIR) -GN_STREAMS=4 -GTALKER_WIRE_CHANS_P=4 -GAUDIO_IF_SLOTS_P=8 -GAUDIO_IF_MASTER_P=1 -GAUDIO_IF_I2S_PAIR_P=1 $(SRCS) $(A_CPP) -o Vmilan_dp_nxn4c
a_notify: a_prereq
	$(VERILATOR) $(SHAPE_AX1x1) $(GPTP_OFF_VFLAGS) --Mdir $(A_MDIR) -GPP_TIM_DIV_US_P=1 -GPP_TIM_DIV_MS_P=100 -CFLAGS "-DNSTREAMS_TB=1 -DNOTIFY_TIMED_TB=1 -DMS_CYC_TB=100 -Wall -Wextra" $(SRCS) $(A_CPP) -o Vmilan_dp_notify
