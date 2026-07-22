run:
	verilator --cc --exe --build -j 8 --top-module KL_lwsrp_rx \
	  -Wno-fatal -CFLAGS "-std=c++17 -O2" \
	  ../../../third_party/verilog-axis/rtl/axis_fifo.v ../../../hdl/ieee8021q/srp/lwsrp_pkg.sv ../../../hdl/ieee8021q/srp/KL_lwsrp_walker.sv \
	  ../../../hdl/ieee8021q/srp/KL_lwsrp_ingress.sv ../../../hdl/ieee8021q/srp/KL_lwsrp_registrar.sv \
	  ../../../hdl/ieee8021q/srp/KL_lwsrp_ta_registrar.sv ../../../hdl/ieee8021q/srp/KL_lwsrp_rx.sv \
	  sim_main.cpp -o Vswpdu
	./obj_dir/Vswpdu
