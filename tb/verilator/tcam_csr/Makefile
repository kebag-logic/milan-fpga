run:
	verilator --cc --exe --build -j 8 --top-module tcam_csr_wrap -Wno-fatal \
	  -CFLAGS "-std=c++17 -O2" \
	  ../../../hdl/ieee8021q/filtering/tcam.sv ../../../hdl/ieee8021q/filtering/rx_mac_filter.sv wrap.sv \
	  sim_main.cpp -o Vtcw
	./obj_dir/Vtcw
