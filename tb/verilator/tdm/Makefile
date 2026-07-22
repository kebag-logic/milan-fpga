VERILATOR ?= verilator
# Item-4 TDM front-end family: KL_tdm_capture (both fsync modes / data
# delays) + KL_aaf_packetizer multi-channel payload (TCTX chans partition)
TOP = tdm_wrap
SRCS = ../../../hdl/ieee1722/aaf/KL_tdm_capture.sv \
       ../../../hdl/ieee1722/aaf/KL_aaf_packetizer.sv \
       ../../../hdl/common/cdc_pair_fifo.sv tdm_wrap.sv
all: run
obj_dir/V$(TOP): $(SRCS) sim_main.cpp
	$(VERILATOR) --cc --exe --build -j 0 --top-module $(TOP) \
	  -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC \
	  -Wno-PINCONNECTEMPTY -Wno-UNUSEDPARAM -CFLAGS "-std=c++17 -O2" \
	  $(SRCS) sim_main.cpp
run: obj_dir/V$(TOP)
	./obj_dir/V$(TOP)
clean: ; rm -rf obj_dir
.PHONY: all run clean
