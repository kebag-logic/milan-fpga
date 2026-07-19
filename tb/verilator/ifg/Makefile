run:
	verilator --cc --exe --build -j 8 --top-module tx_ifg_gasket -Wno-fatal \
	  -CFLAGS "-std=c++17 -O2" ../../../hdl/common/tx_ifg_gasket.sv sim_main.cpp -o Vifg
	./obj_dir/Vifg
