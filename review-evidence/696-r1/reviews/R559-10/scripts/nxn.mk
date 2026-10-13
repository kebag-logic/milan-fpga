# Focus the unchanged 4x4 recipe from milan_dp's run target.
# Load after that suite's Makefile; all sources, flags and shape are its own.
REVIEW_MDIR ?= obj_review_nxn
.PHONY: reviewer-nxn
reviewer-nxn: ltn_rom.hex ucode.hex $(GEN_ALL)
	$(VERILATOR) $(SHAPE_4x4) $(DP_VFLAGS) --Mdir $(REVIEW_MDIR) -GN_STREAMS=4 $(SRCS) sim_nxn.cpp -o Vmilan_dp_nxn
	$(abspath $(REVIEW_MDIR))/Vmilan_dp_nxn
