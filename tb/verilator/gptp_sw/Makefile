# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# gPTP in firmware against modelled peers (#884, #665 F6): the firmware's ports, adapter, loop and mailbox driver on
# the host mailbox model at two interfaces, each interface's PHC, launch observer, timestamp unit and control tap in
# Verilator. `make` builds and runs every run (slave, master, flood); `make run RUN=slave` one of them;
# `make mutants` plants each defect of gptp_sw_mutants.py and requires its check to fail.
VERILATOR ?= verilator
ROOT = ../../..
FW ?= $(ROOT)/sw/firmware/ctrl
HDL = $(ROOT)/hdl
MDIR ?= ./obj_dir
GEN = $(abspath $(MDIR))/gen
RTL = $(HDL)/ieee8021as/ptp_timestamp/timestamp_counter.sv $(HDL)/common/cdc_handshake.sv $(HDL)/common/cdc_pulse.sv \
      $(HDL)/ieee8021as/gptp_plane/KL_gptp_gmii_launch.sv $(HDL)/ieee8021as/gptp_tsu/KL_gptp_tsu.sv \
      $(HDL)/milan/KL_ctrl_split.sv $(ROOT)/third_party/verilog-axis/rtl/axis_fifo.v tb_gptp_sw.sv
# the mailbox driver from a copy of its directory holding the two-interface contract (gen_mailbox.py
# --variant-interfaces 2): its own quoted include of mbx_contract.h finds that one, not the tracked one-interface header
MBX = $(GEN)/mbx
FW_SRC = $(FW)/gptp/gptp.c $(FW)/gptp/gptp_mbx.c $(FW)/loop/ctrl_loop.c $(MBX)/mbx.c $(FW)/host/mbx_model.c \
         $(FW)/host/mbx_plat_host.c
INC = -I$(MBX) -I$(abspath $(FW))/gptp -I$(abspath $(FW))/loop -I$(abspath $(FW))/host \
      -I$(abspath $(FW))/port -I$(abspath $(ROOT))/third_party/tsn-c-stack/include
VFLAGS = --cc --exe --build -j 0 -Wall -Wno-fatal -Werror-USERERROR -Werror-PINMISSING -Wno-DECLFILENAME \
         -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY -Wno-GENUNNAMED -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC \
         -Wno-PROCASSINIT -CFLAGS "-std=c++17 -O2 -Wall -Wextra $(INC)"
RUN ?=

FW_OBJ = $(patsubst %.c,$(MDIR)/fw/%.o,$(notdir $(FW_SRC)))

all: run

$(MBX)/mbx_contract.h:
	python3 -B $(ROOT)/sw/mailbox/gen_mailbox.py --variant-interfaces 2 --out $(GEN)
	rm -rf $(MBX) && cp -r $(abspath $(FW))/mbx $(MBX) && cp $(GEN)/mbx_contract.h $(MBX)/mbx_contract.h

# the firmware is C11: built by the C compiler, as the firmware gates build it, and linked into the bench
$(MDIR)/fw/%.o: $(MBX)/mbx_contract.h $(filter-out $(MBX)/%,$(FW_SRC)) $(wildcard $(FW)/*/*.h)
	@mkdir -p $(MDIR)/fw
	$(CC) -std=c11 -O2 -Wall -Wextra -Werror -pedantic $(INC) -c $(filter %/$*.c,$(abspath $(FW_SRC))) -o $@

build: $(FW_OBJ)
	$(VERILATOR) $(VFLAGS) --top-module tb_gptp_sw --Mdir $(MDIR) -I$(HDL)/common $(RTL) sim_main.cpp \
	  -LDFLAGS "$(abspath $(FW_OBJ))" -o Vtb_gptp_sw

run: build
	$(MDIR)/Vtb_gptp_sw $(RUN)

mutants:
	python3 -B gptp_sw_mutants.py

clean:
	rm -rf obj_dir obj_mut_*

.PHONY: all build run mutants clean
