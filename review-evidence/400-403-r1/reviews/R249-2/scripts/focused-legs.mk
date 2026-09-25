# Focused legs reusing tb/verilator/milan_dp/Makefile variables verbatim.
# usage: make -C tb/verilator/milan_dp -f Makefile -f <this> nxn-only
nxn-only: ltn_rom.hex ucode.hex gptp_ucode.hex $(GEN_ALL)
	$(VERILATOR) $(SHAPE_4x4) $(DP_VFLAGS) --Mdir obj_nxn -GN_STREAMS=4 $(SRCS) sim_nxn.cpp -o Vmilan_dp_nxn
	./obj_nxn/Vmilan_dp_nxn
nxn8-only: ltn_rom.hex ucode.hex gptp_ucode.hex $(GEN_ALL)
	$(VERILATOR) $(SHAPE_8x8) $(DP_VFLAGS) --Mdir obj_nxn8 -GN_STREAMS=8 -GLOOPBACK_P=1 -CFLAGS "-DNSTREAMS_TB=8 -DAX8X8_TB=1 -DLOOPBACK_TB=1 -DLB_SEQ_FIXED=1 -Wall -Wextra" $(SRCS) sim_nxn.cpp -o Vmilan_dp_nxn8
	./obj_nxn8/Vmilan_dp_nxn8
ax1x1-only: ltn_rom.hex ucode.hex $(GEN_CSR) $(SHAPE_AX1_F)
	$(AX1X1_BUILD)
	./obj_ax1x1/Vmilan_dp_ax1x1
