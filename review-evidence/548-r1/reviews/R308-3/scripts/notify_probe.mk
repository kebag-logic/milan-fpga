# Used as `make -f Makefile -f notify_probe.mk notify-probe` inside
# tb/verilator/milan_dp of an extracted candidate tree. The recipe is the
# milan_dp Makefile's own timed-notification build (the `run` target's
# obj_notify line), with only --Mdir made overridable so a mutated datapath
# (DP_SRC, which that Makefile already exposes) builds beside the positive one.
NOTIFY_MDIR ?= obj_notify

.PHONY: notify-probe
notify-probe: ltn_rom.hex ucode.hex gptp_ucode.hex
	$(VERILATOR) $(SHAPE_AX1x1) $(GPTP_OFF_VFLAGS) --Mdir $(NOTIFY_MDIR) \
	  -GPP_TIM_DIV_US_P=1 -GPP_TIM_DIV_MS_P=100 \
	  -CFLAGS "-DNSTREAMS_TB=1 -DNOTIFY_TIMED_TB=1 -DMS_CYC_TB=100 -Wall -Wextra" \
	  $(SRCS) sim_nxn.cpp -o Vmilan_dp_notify
