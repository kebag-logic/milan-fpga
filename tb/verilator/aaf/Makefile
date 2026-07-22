VERILATOR ?= verilator
TOP = aaf_talker_i2s
SRCS = ../../../hdl/ieee1722/aaf/aaf_talker_i2s.sv ../../../hdl/common/cdc_pair_fifo.sv
# NxN talker lane (NXN_ARCHITECTURE P4): golden byte-compare (flat talker vs
# capture+packetizer) + two-talker interleave at N=2
NXSRCS = ../../../hdl/ieee1722/aaf/aaf_talker_i2s.sv \
         ../../../hdl/ieee1722/aaf/KL_aaf_capture_i2s.sv \
         ../../../hdl/ieee1722/aaf/KL_aaf_packetizer.sv \
         ../../../hdl/common/cdc_pair_fifo.sv aaf_nx_wrap.sv
all: run
obj_dir/V$(TOP): $(SRCS) sim_main.cpp
	$(VERILATOR) --cc --exe --build -j 0 --top-module $(TOP) -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -CFLAGS "-std=c++17 -O2" $(SRCS) sim_main.cpp
obj_nx/Vaaf_nx_wrap: $(NXSRCS) sim_main_nx.cpp
	$(VERILATOR) --cc --exe --build -j 0 --top-module aaf_nx_wrap --Mdir obj_nx \
	  -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC \
	  -Wno-PINCONNECTEMPTY -Wno-UNUSEDPARAM -CFLAGS "-std=c++17 -O2" \
	  $(NXSRCS) sim_main_nx.cpp -o Vaaf_nx_wrap
run: obj_dir/V$(TOP) obj_nx/Vaaf_nx_wrap
	./obj_dir/V$(TOP)
	./obj_nx/Vaaf_nx_wrap
clean: ; rm -rf obj_dir obj_nx
.PHONY: all run clean
