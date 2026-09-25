# Extra target, loaded after the suite Makefile (make -f Makefile -f nxn4.mk nxn4):
# the 4x4 sim_nxn leg exactly as `run` builds it, built and run alone.
.PHONY: nxn4
nxn4: ltn_rom.hex ucode.hex gptp_ucode.hex $(GEN_ALL)
	$(VERILATOR) $(SHAPE_4x4) $(DP_VFLAGS) --Mdir obj_nxn -GN_STREAMS=4 $(SRCS) sim_nxn.cpp -o Vmilan_dp_nxn
	./obj_nxn/Vmilan_dp_nxn
