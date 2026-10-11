# Focused copies of the committed milan_dp run recipes; no source change.
include Makefile
.PHONY: review-nxn review-nxn8
review-nxn: ltn_rom.hex ucode.hex gptp_ucode.hex $(GEN_ALL)
	$(VERILATOR) $(SHAPE_4x4) $(DP_VFLAGS) --Mdir obj_review_nxn -GN_STREAMS=4 $(SRCS) sim_nxn.cpp -o Vmilan_dp_nxn
	./obj_review_nxn/Vmilan_dp_nxn
review-nxn8: ltn_rom.hex ucode.hex gptp_ucode.hex $(GEN_ALL)
	$(VERILATOR) $(SHAPE_8x8) $(DP_VFLAGS) --Mdir obj_review_nxn8 -GN_STREAMS=8 -GLOOPBACK_P=1 -CFLAGS "-DNSTREAMS_TB=8 -DAX8X8_TB=1 -DLOOPBACK_TB=1 -DLB_SEQ_FIXED=1 -Wall -Wextra" $(SRCS) sim_nxn.cpp -o Vmilan_dp_nxn8
	./obj_review_nxn8/Vmilan_dp_nxn8
