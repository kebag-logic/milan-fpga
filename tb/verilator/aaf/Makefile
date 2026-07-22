VERILATOR ?= verilator
TOP = aaf_talker_i2s
SRCS = ../../../hdl/ieee1722/aaf/aaf_talker_i2s.sv ../../../hdl/common/cdc_pair_fifo.sv
all: run
obj_dir/V$(TOP): $(SRCS) sim_main.cpp
	$(VERILATOR) --cc --exe --build -j 0 --top-module $(TOP) -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -CFLAGS "-std=c++17 -O2" $(SRCS) sim_main.cpp
run: obj_dir/V$(TOP)
	./obj_dir/V$(TOP)
clean: ; rm -rf obj_dir
.PHONY: all run clean
