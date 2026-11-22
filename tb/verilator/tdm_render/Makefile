# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# KL_tdm_render verification: TDM8 output serializer (item-4 audio front-end,
# OUTPUT side). The TB drives bclk/fsync per the frame geometry, writes known
# slot samples on clk_i, and de-serializes tdm_dout_o with a golden model that
# samples exactly like KL_tdm_capture (rising edge, Philips-heritage delay-1) -
# asserting bit-exact slots, frame alignment, double-buffer latching, pad-zero,
# 24-bit sign preservation, a multi-frame run and stale-frame repeat.
VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
C          = $(RTL_DIR)/common
AAF        = $(RTL_DIR)/ieee1722/aaf
TOP        = KL_tdm_render
VFLAGS = --cc --exe --build -j 0 --top-module $(TOP) \
         +incdir+$(C) +incdir+$(AAF) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-IMPORTSTAR -Wno-CASEINCOMPLETE \
         -Wno-EOFNEWLINE -CFLAGS "-std=c++17 -O2 -Wall -Wextra"
SRCS = $(C)/cdc_pair_fifo.sv $(AAF)/KL_tdm_render.sv

# KL_tdm_render_master's LANE WIDTH (#584): the first SLOTS_P slots of a bus
# frame of BUS_SLOTS_P slots are rendered and the rest serialize zero. Four
# legs: the 8x8's lane (1 of 32 slots, the first TDM render channel only) on a
# modelled timing owner, a two-slot lane on an 8-slot bus, the shipping 1x1's
# full TDM8 lane through the DEFAULT BUS_SLOTS_P (which elaborates as before
# #584), and the 8x8's lane on its REAL timing owner, KL_tdm_capture_master's
# TDM32 bus, decoded from the bclk, fsync and dout pins alone.
#   make master-mutants - the planted defects (master_mutants.py), explicit
RM_SRC  ?= $(AAF)/KL_tdm_render_master.sv
CM_SRC  ?= $(AAF)/KL_tdm_capture_master.sv
RM_SRCS  = $(C)/cdc_pair_fifo.sv $(RM_SRC)
RM_FLAGS = --cc --exe --build -j 0 +incdir+$(C) +incdir+$(AAF) \
           -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
           -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-IMPORTSTAR -Wno-CASEINCOMPLETE \
           -Wno-EOFNEWLINE -Wno-SELRANGE -Wno-PINCONNECTEMPTY
# lane <name> <slots> <bus slots> <pass BUS_SLOTS_P: 1/0> <frame position width>
define LANE
$(1):
	$(VERILATOR) $(RM_FLAGS) --top-module KL_tdm_render_master --prefix Vtdm_render_master \
	  --Mdir obj_$(1) -GSLOTS_P=$(2) $(if $(filter 1,$(4)),-GBUS_SLOTS_P=$(3),) -GFRAME_POS_W_P=$(5) \
	  -CFLAGS "-std=c++17 -O2 -Wall -Wextra -DLANE_SLOTS=$(2) -DLANE_BUS_SLOTS=$(3)" $(RM_SRCS) sim_master.cpp \
	  -o Vtdm_render_master_$(1)
	./obj_$(1)/Vtdm_render_master_$(1)
endef

.PHONY: all run clean master master-mutants lane1of32 lane2of8 lane8of8 bus1of32
all: run master
run:
	$(VERILATOR) $(VFLAGS) $(SRCS) sim_main.cpp -o VKL_tdm_render_sim
	./obj_dir/VKL_tdm_render_sim
$(eval $(call LANE,lane1of32,1,32,1,10))
$(eval $(call LANE,lane2of8,2,8,1,8))
$(eval $(call LANE,lane8of8,8,8,0,8))
bus1of32:
	$(VERILATOR) $(RM_FLAGS) --top-module bus_wrap --Mdir obj_bus1of32 -CFLAGS "-std=c++17 -O2 -Wall -Wextra" \
	  $(RM_SRCS) $(CM_SRC) master_bus_wrap.sv sim_master_bus.cpp -o Vbus_wrap_1of32
	./obj_bus1of32/Vbus_wrap_1of32
master: lane1of32 lane2of8 lane8of8 bus1of32
master-mutants:
	python3 -B master_mutants.py
clean:
	rm -rf obj_dir obj_lane* obj_bus* obj_mut
