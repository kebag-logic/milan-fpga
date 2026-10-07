VERILATOR ?= verilator
VERILATOR_JOBS ?= 16
START_RTL ?= ../../../hdl/ieee1722/aaf/KL_aaf_packetizer.sv
START_MDIR ?= obj_start
START_JOBS ?= 4
TOP = aaf_talker_i2s
SRCS = ../../../hdl/ieee1722/aaf/aaf_talker_i2s.sv ../../../hdl/common/cdc_pair_fifo.sv
# Multi-stream talker lane (docs/overview/ARCHITECTURE.md): golden byte-compare (flat talker vs
# capture+packetizer) + two-talker interleave at N=2
NXSRCS = ../../../hdl/ieee1722/aaf/aaf_talker_i2s.sv \
         ../../../hdl/ieee1722/aaf/KL_aaf_capture_i2s.sv \
         ../../../hdl/ieee1722/aaf/KL_aaf_packetizer.sv \
         ../../../hdl/common/cdc_pair_fifo.sv aaf_nx_wrap.sv
all: run
obj_dir/V$(TOP): $(SRCS) sim_main.cpp
	$(VERILATOR) --cc --exe --build -j 0 --top-module $(TOP) -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -CFLAGS "-std=c++17 -O2 -Wall -Wextra" $(SRCS) sim_main.cpp
obj_nx/Vaaf_nx_wrap: $(NXSRCS) sim_main_nx.cpp
	$(VERILATOR) --cc --exe --build -j 0 --top-module aaf_nx_wrap --Mdir obj_nx \
	  -Wall -Wno-fatal -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC \
	  -Wno-PINCONNECTEMPTY -Wno-UNUSEDPARAM -CFLAGS "-std=c++17 -O2 -Wall -Wextra" \
	  $(NXSRCS) sim_main_nx.cpp -o Vaaf_nx_wrap
startup-build:
	$(VERILATOR) --cc --exe --build -j $(VERILATOR_JOBS) \
	  --top-module KL_aaf_packetizer -GN_TALKERS_P=1 -GWIRE_CHANS_P=8 \
	  --Mdir $(START_MDIR) -Wall -Wno-fatal \
	  -CFLAGS "-std=c++17 -O2 -Wall -Wextra" $(START_RTL) $(abspath sim_start.cpp)
startup: startup-build
	$(abspath $(START_MDIR))/VKL_aaf_packetizer
startup-mutants: startup
	python3 start_mutants.py --jobs $(START_JOBS)
run: obj_dir/V$(TOP) obj_nx/Vaaf_nx_wrap startup-mutants
	./obj_dir/V$(TOP)
	./obj_nx/Vaaf_nx_wrap
clean: ; rm -rf obj_dir obj_nx obj_start
.PHONY: all run clean startup startup-build startup-mutants
