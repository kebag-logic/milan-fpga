# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# KL_tdm_render_master lane width (#584): the first SLOTS_P slots of a bus
# frame of BUS_SLOTS_P slots are rendered and the rest serialize zero.
#
#   make           - the three legs, then the planted defects
#   make legs      - the three legs alone
#   make mutants   - the planted defects alone (mutants.py)
#
# Legs: the 8x8's lane (1 of 32 slots: the first TDM render channel only), a
# two-slot lane on an 8-slot bus, and the shipping 1x1's full TDM8 lane built
# through the DEFAULT BUS_SLOTS_P, which elaborates as it did before #584.
VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
C          = $(RTL_DIR)/common
AAF        = $(RTL_DIR)/ieee1722/aaf
RM_SRC    ?= $(AAF)/KL_tdm_render_master.sv
SRCS       = $(C)/cdc_pair_fifo.sv $(RM_SRC)
VFLAGS = --cc --exe --build -j 0 --top-module KL_tdm_render_master \
         --prefix Vtdm_render_master +incdir+$(C) +incdir+$(AAF) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-IMPORTSTAR -Wno-CASEINCOMPLETE \
         -Wno-EOFNEWLINE -Wno-SELRANGE
CXX_STD = -std=c++17 -O2 -Wall -Wextra

# leg <name> <slots> <bus slots> <pass BUS_SLOTS_P: 1/0>
define LEG
$(1):
	$(VERILATOR) $(VFLAGS) --Mdir obj_$(1) -GSLOTS_P=$(2) \
	  $(if $(filter 1,$(4)),-GBUS_SLOTS_P=$(3),) -GFRAME_POS_W_P=$(5) \
	  -CFLAGS "$(CXX_STD) -DTB_SLOTS=$(2) -DTB_BUS_SLOTS=$(3)" \
	  $(SRCS) sim_main.cpp -o Vtdm_render_master_$(1)
	./obj_$(1)/Vtdm_render_master_$(1)
endef

.PHONY: all legs mutants clean lane1of32 lane2of8 lane8of8
all: legs mutants
legs: lane1of32 lane2of8 lane8of8
$(eval $(call LEG,lane1of32,1,32,1,10))
$(eval $(call LEG,lane2of8,2,8,1,8))
$(eval $(call LEG,lane8of8,8,8,0,8))
mutants:
	python3 -B mutants.py
clean:
	rm -rf obj_lane* obj_mut*
