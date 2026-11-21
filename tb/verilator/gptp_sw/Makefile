# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# gPTP in firmware against a modelled peer (#884, #665 F6): the firmware's port, adapter, loop and mailbox driver
# on the host mailbox model, the fabric's PHC, launch observer and timestamp unit in Verilator. `make` builds and
# runs both arms (the firmware as slave, then as grandmaster).
VERILATOR ?= verilator
ROOT = ../../..
FW = $(ROOT)/sw/firmware/ctrl
HDL = $(ROOT)/hdl
MDIR ?= ./obj_dir
RTL = $(HDL)/ieee8021as/ptp_timestamp/timestamp_counter.sv $(HDL)/common/cdc_handshake.sv $(HDL)/common/cdc_pulse.sv \
      $(HDL)/ieee8021as/gptp_plane/KL_gptp_gmii_launch.sv $(HDL)/ieee8021as/gptp_tsu/KL_gptp_tsu.sv tb_gptp_sw.sv
FW_SRC = $(FW)/gptp/gptp.c $(FW)/gptp/gptp_mbx.c $(FW)/loop/ctrl_loop.c $(FW)/mbx/mbx.c $(FW)/host/mbx_model.c \
         $(FW)/host/mbx_plat_host.c
INC = -I$(abspath $(FW))/gptp -I$(abspath $(FW))/mbx -I$(abspath $(FW))/loop -I$(abspath $(FW))/host \
      -I$(abspath $(FW))/port -I$(abspath $(ROOT))/third_party/tsn-c-stack/include
VFLAGS = --cc --exe --build -j 0 -Wall -Wno-fatal -Werror-USERERROR -Werror-PINMISSING -Wno-DECLFILENAME \
         -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY -Wno-GENUNNAMED \
         -CFLAGS "-std=c++17 -O2 -Wall -Wextra $(INC)"

FW_OBJ = $(patsubst %.c,$(MDIR)/fw/%.o,$(notdir $(FW_SRC)))

all: run

# the firmware is C11: built by the C compiler, as the firmware gates build it, and linked into the bench
$(MDIR)/fw/%.o:
	@mkdir -p $(MDIR)/fw
	$(CC) -std=c11 -O2 -Wall -Wextra -Werror -pedantic $(INC) -c $(filter %/$*.c,$(abspath $(FW_SRC))) -o $@

build: $(FW_OBJ)
	$(VERILATOR) $(VFLAGS) --top-module tb_gptp_sw --Mdir $(MDIR) -I$(HDL)/common $(RTL) sim_main.cpp \
	  -LDFLAGS "$(abspath $(FW_OBJ))" -o Vtb_gptp_sw

run: build
	$(MDIR)/Vtb_gptp_sw

clean:
	rm -rf obj_dir

.PHONY: all build run clean
