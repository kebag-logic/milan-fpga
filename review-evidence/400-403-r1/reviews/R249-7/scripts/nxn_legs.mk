# Extra targets layered over tb/verilator/milan_dp/Makefile (make -f Makefile -f <this>):
# the `run` recipe's obj_nxn (arty_4x4) and obj_nxn8 (ax7101_8x8) legs, verbatim, on their own.
r249-nxn: ltn_rom.hex ucode.hex gptp_ucode.hex $(GEN_ALL)
	$(VERILATOR) $(SHAPE_4x4) $(DP_VFLAGS) --Mdir obj_nxn -GN_STREAMS=4 $(SRCS) sim_nxn.cpp -o Vmilan_dp_nxn
	./obj_nxn/Vmilan_dp_nxn
r249-nxn8: ltn_rom.hex ucode.hex gptp_ucode.hex $(GEN_ALL)
	$(VERILATOR) $(SHAPE_8x8) $(DP_VFLAGS) --Mdir obj_nxn8 -GN_STREAMS=8 -GLOOPBACK_P=1 -CFLAGS "-DNSTREAMS_TB=8 -DAX8X8_TB=1 -DLOOPBACK_TB=1 -DLB_SEQ_FIXED=1 -Wall -Wextra" $(SRCS) sim_nxn.cpp -o Vmilan_dp_nxn8
	./obj_nxn8/Vmilan_dp_nxn8
