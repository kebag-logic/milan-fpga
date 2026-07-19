run:
	verilator --cc --exe --build -j 8 --top-module tcam_csr_wrap -Wno-fatal \
	  -CFLAGS "-std=c++17 -O2" \
	  ../../../hdl/common/tcam.sv ../../../hdl/common/rx_mac_filter.sv wrap.sv \
	  sim_main.cpp -o Vtcw
	./obj_dir/Vtcw
