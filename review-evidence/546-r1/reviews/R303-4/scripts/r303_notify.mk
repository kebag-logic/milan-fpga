# Wrapper: the milan_dp suite Makefile plus the timed notification build,
# recipe copied verbatim from that Makefile's `run` target (obj_notify).
include Makefile
R303_MDIR ?= obj_notify
r303-notify: ltn_rom.hex ucode.hex $(GEN_CSR) $(SHAPE_AX1_F)
	$(VERILATOR) $(SHAPE_AX1x1) $(GPTP_OFF_VFLAGS) --Mdir $(R303_MDIR) \
	  -GPP_TIM_DIV_US_P=1 -GPP_TIM_DIV_MS_P=100 \
	  -CFLAGS "-DNSTREAMS_TB=1 -DNOTIFY_TIMED_TB=1 -DMS_CYC_TB=100 -Wall -Wextra" \
	  $(SRCS) sim_nxn.cpp -o Vmilan_dp_notify
