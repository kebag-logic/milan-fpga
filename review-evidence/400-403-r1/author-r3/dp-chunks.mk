.PHONY: a316-prereq
a316-prereq: ltn_rom.hex ucode.hex gptp_ucode.hex $(GEN_ALL) $(SHAPE_DV_F) gptp gptp-lat gmstep

.PHONY: a316-step-01
a316-step-01:
	$(VERILATOR) $(SHAPE_1x1) $(DP_VFLAGS) $(SRCS) $(CPP) -o Vmilan_dp_sim

.PHONY: a316-step-02
a316-step-02:
	$(VERILATOR) $(SHAPE_4x4) $(DP_VFLAGS) --Mdir obj_nxn -GN_STREAMS=4 $(SRCS) sim_nxn.cpp -o Vmilan_dp_nxn

.PHONY: a316-step-03
a316-step-03:
	$(VERILATOR) $(SHAPE_DV) $(DP_VFLAGS) --Mdir obj_nxndv -GN_STREAMS=4 -CFLAGS "-DNSTREAMS_TB=4 -DDIVERGENT_TB=1 -I$(CURDIR)/gen_divergent -Wall -Wextra" $(SRCS) sim_nxn.cpp -o Vmilan_dp_nxndv

.PHONY: a316-step-04
a316-step-04:
	$(VERILATOR) $(SHAPE_8x8) $(DP_VFLAGS) --Mdir obj_nxn8 -GN_STREAMS=8 -GLOOPBACK_P=1 -CFLAGS "-DNSTREAMS_TB=8 -DAX8X8_TB=1 -DLOOPBACK_TB=1 -DLB_SEQ_FIXED=1 -Wall -Wextra" $(SRCS) sim_nxn.cpp -o Vmilan_dp_nxn8

.PHONY: a316-step-05
a316-step-05:
	$(VERILATOR) $(SHAPE_4x4) $(DP_VFLAGS) --Mdir obj_nxn4c -GN_STREAMS=4 \
	  -GTALKER_WIRE_CHANS_P=4 -GAUDIO_IF_SLOTS_P=8 -GAUDIO_IF_MASTER_P=1 \
	  -GAUDIO_IF_I2S_PAIR_P=1 $(SRCS) sim_nxn.cpp -o Vmilan_dp_nxn4c

.PHONY: a316-step-06
a316-step-06:
	$(VERILATOR) $(SHAPE_1x1) $(DP_VFLAGS) --Mdir obj_nolpf -GLPF_P=0 $(SRCS) $(CPP) -o Vmilan_dp_nolpf

.PHONY: a316-step-07
a316-step-07:
	$(VERILATOR) $(SHAPE_1x1) $(DP_VFLAGS) --Mdir obj_prune $(PRUNE_G) $(SRCS) sim_prune.cpp -o Vmilan_dp_prune

.PHONY: a316-step-08
a316-step-08:
	$(AX1X1_BUILD)

.PHONY: a316-step-09
a316-step-09:
	$(ACLK_BUILD)

.PHONY: a316-step-10
a316-step-10:
	@echo "======================================================================"

.PHONY: a316-step-11
a316-step-11:
	$(NOTIFY_BUILD)

.PHONY: a316-step-12
a316-step-12:
	$(CRFLIC_BUILD)

.PHONY: a316-step-13
a316-step-13:
	./obj_dir/Vmilan_dp_sim

.PHONY: a316-step-14
a316-step-14:
	@echo "---- Milan 5.4.5 notifications and the #508 GET_STREAM_INFO seam, TIMED on the compressed processor timebase ----"

.PHONY: a316-step-15
a316-step-15:
	./$(NOTIFY_MDIR)/Vmilan_dp_notify

.PHONY: a316-step-16
a316-step-16:
	@echo "---- #530 CRF talker licence and per-type LeaveAll, TIMED on one compressed grid ----"

.PHONY: a316-step-17
a316-step-17:
	./$(CRFLIC_MDIR)/Vmilan_dp_crflic

.PHONY: a316-step-18
a316-step-18:
	./obj_nxn/Vmilan_dp_nxn

.PHONY: a316-step-19
a316-step-19:
	@echo "---- the DIVERGENT shape: input row 1 declares the 96 kHz base ----"

.PHONY: a316-step-20
a316-step-20:
	./obj_nxndv/Vmilan_dp_nxndv

.PHONY: a316-step-21
a316-step-21:
	./obj_nxn8/Vmilan_dp_nxn8

.PHONY: a316-step-22
a316-step-22:
	@echo "---- the shipping Arty shape: 4 streams x 4 wire channels ----"

.PHONY: a316-step-23
a316-step-23:
	./obj_nxn4c/Vmilan_dp_nxn4c

.PHONY: a316-step-24
a316-step-24:
	@echo "---- LPF_P=0 (pruned render tap, the ax7101 shipping shape) ----"

.PHONY: a316-step-25
a316-step-25:
	./obj_nolpf/Vmilan_dp_nolpf

.PHONY: a316-step-26
a316-step-26:
	@echo "---- all six tier-1 blocks pruned ----"

.PHONY: a316-step-27
a316-step-27:
	./obj_prune/Vmilan_dp_prune

.PHONY: a316-step-28
a316-step-28:
	@echo "---- THE SHIPPING ALINX SHAPE: 1 stream x 8 wire channels, TDM8 master ----"

.PHONY: a316-step-29
a316-step-29:
	./obj_ax1x1/Vmilan_dp_ax1x1

.PHONY: a316-step-30
a316-step-30:
	@echo "---- the same shape at the TRUE clk_audio ratio (391/1591) ----"

.PHONY: a316-step-31
a316-step-31:
	./obj_aclk/Vmilan_dp_aclk

.PHONY: a316-step-32
a316-step-32:
	@echo "---- #386 render law: the same leg against mutated setpoint stages and datapath ----"

.PHONY: a316-step-33
a316-step-33:
	python3 render_mutants.py

.PHONY: a316-step-34
a316-step-34:
	@echo "---- #387 GM step re-base: the gmstep leg against the acceptance's controls ----"

.PHONY: a316-step-35
a316-step-35:
	python3 gmstep_mutants.py
