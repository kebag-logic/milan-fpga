probe-nxn:
	$(VERILATOR) $(SHAPE_4x4) $(DP_VFLAGS) --Mdir $REVIEWS/640-m6-r601-1-packet/receipts/dpprobe/DP-0-clean/obj -GN_STREAMS=4 $(SRCS) sim_nxn.cpp -o Vmilan_dp_nxn
	$REVIEWS/640-m6-r601-1-packet/receipts/dpprobe/DP-0-clean/obj/Vmilan_dp_nxn
