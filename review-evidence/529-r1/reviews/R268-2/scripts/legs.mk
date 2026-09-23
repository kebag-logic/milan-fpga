# SPDX-License-Identifier: CERN-OHL-W-2.0
# Loaded AFTER tb/verilator/milan_dp/Makefile (make -f Makefile -f legs.mk):
# one target per sim_nxn leg, the argument lists copied from the `run` recipe
# at the reviewed head, with only --Mdir ($(MDIR)) and the harness file
# ($(HARNESS)) substituted. DP_SRC is the Makefile's own override.
HARNESS ?= sim_nxn.cpp
.PHONY: review-nxn review-nxndv review-nxn8 review-nxn4c review-notify
review-nxn:
	$(VERILATOR) $(SHAPE_4x4) $(DP_VFLAGS) --Mdir $(MDIR) -GN_STREAMS=4 $(SRCS) $(HARNESS) -o Vmilan_dp_nxn
review-nxndv:
	$(VERILATOR) $(SHAPE_DV) $(DP_VFLAGS) --Mdir $(MDIR) -GN_STREAMS=4 -CFLAGS "-DNSTREAMS_TB=4 -DDIVERGENT_TB=1 -I$(CURDIR)/gen_divergent -Wall -Wextra" $(SRCS) $(HARNESS) -o Vmilan_dp_nxndv
review-nxn8:
	$(VERILATOR) $(SHAPE_8x8) $(DP_VFLAGS) --Mdir $(MDIR) -GN_STREAMS=8 -GLOOPBACK_P=1 -CFLAGS "-DNSTREAMS_TB=8 -DAX8X8_TB=1 -DLOOPBACK_TB=1 -DLB_SEQ_FIXED=1 -Wall -Wextra" $(SRCS) $(HARNESS) -o Vmilan_dp_nxn8
review-nxn4c:
	$(VERILATOR) $(SHAPE_4x4) $(DP_VFLAGS) --Mdir $(MDIR) -GN_STREAMS=4 -GTALKER_WIRE_CHANS_P=4 -GAUDIO_IF_SLOTS_P=8 -GAUDIO_IF_MASTER_P=1 -GAUDIO_IF_I2S_PAIR_P=1 $(SRCS) $(HARNESS) -o Vmilan_dp_nxn4c
review-notify:
	$(VERILATOR) $(SHAPE_AX1x1) $(GPTP_OFF_VFLAGS) --Mdir $(MDIR) -GPP_TIM_DIV_US_P=1 -GPP_TIM_DIV_MS_P=100 -CFLAGS "-DNSTREAMS_TB=1 -DNOTIFY_TIMED_TB=1 -DMS_CYC_TB=100 -Wall -Wextra" $(SRCS) $(HARNESS) -o Vmilan_dp_notify
