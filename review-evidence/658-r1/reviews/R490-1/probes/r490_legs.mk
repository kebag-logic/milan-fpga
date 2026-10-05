# R490-1: focused sim_nxn legs of tb/verilator/milan_dp, built with the
# suite's own recipe lines (included after the suite Makefile).
# make -C tb/verilator/milan_dp -f Makefile -f <this> r490-nxn|r490-nxndv|r490-nxn8
r490-nxn: ltn_rom.hex ucode.hex $(GEN_ALL)
	$(VERILATOR) $(SHAPE_4x4) $(DP_VFLAGS) --Mdir obj_nxn -GN_STREAMS=4 $(SRCS) sim_nxn.cpp -o Vmilan_dp_nxn
	./obj_nxn/Vmilan_dp_nxn
r490-nxndv: ltn_rom.hex ucode.hex $(GEN_ALL) $(SHAPE_DV_F)
	$(VERILATOR) $(SHAPE_DV) $(DP_VFLAGS) --Mdir obj_nxndv -GN_STREAMS=4 -CFLAGS "-DNSTREAMS_TB=4 -DDIVERGENT_TB=1 -I$(CURDIR)/gen_divergent -Wall -Wextra" $(SRCS) sim_nxn.cpp -o Vmilan_dp_nxndv
	./obj_nxndv/Vmilan_dp_nxndv
r490-nxn8: ltn_rom.hex ucode.hex $(GEN_ALL)
	$(VERILATOR) $(SHAPE_8x8) $(DP_VFLAGS) --Mdir obj_nxn8 -GN_STREAMS=8 -GLOOPBACK_P=1 -CFLAGS "-DNSTREAMS_TB=8 -DAX8X8_TB=1 -DLOOPBACK_TB=1 -DLB_SEQ_FIXED=1 -Wall -Wextra" $(SRCS) sim_nxn.cpp -o Vmilan_dp_nxn8
	./obj_nxn8/Vmilan_dp_nxn8
