# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# avtp_stream_parser verification (stream id/PT extraction + match table).
VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
C          = $(RTL_DIR)/common
A          = $(RTL_DIR)/ieee1722/avtp
TOP        = avtp_stream_parser
VFLAGS = --cc --exe --build -j 0 --top-module $(TOP) \
         +incdir+$(C) +incdir+$(A) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-IMPORTSTAR -Wno-CASEINCOMPLETE \
         -Wno-EOFNEWLINE -CFLAGS "-std=c++17 -O2"
SRCS = $(C)/ethernet_packet_pkg.sv $(A)/avtp_subtype_pkg.sv $(A)/avtp_stream_parser.sv
# stream-table harness (NXN_ARCHITECTURE §1.1 / P1): table authority + parser
TBLFLAGS = --cc --exe --build -j 0 --top-module stream_table_wrap \
         +incdir+$(C) +incdir+$(A) \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-IMPORTSTAR -Wno-CASEINCOMPLETE \
         -Wno-EOFNEWLINE -Wno-PINCONNECTEMPTY -CFLAGS "-std=c++17 -O2"
TBLSRCS = $(C)/ethernet_packet_pkg.sv $(A)/avtp_subtype_pkg.sv \
          $(A)/avtp_stream_parser.sv $(A)/KL_stream_table.sv stream_table_wrap.sv
.PHONY: all run clean
all: run
run:
	$(VERILATOR) $(VFLAGS) $(SRCS) sim_main.cpp -o Vavtp_stream_parser_sim
	./obj_dir/Vavtp_stream_parser_sim
	$(VERILATOR) $(TBLFLAGS) --Mdir obj_tbl $(TBLSRCS) sim_table.cpp -o Vstream_table_sim
	./obj_tbl/Vstream_table_sim
clean:
	rm -rf obj_dir obj_tbl
