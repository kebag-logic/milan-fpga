# -Werror-USERERROR: rx_mac_filter's elaboration contract must fail this
# build too; -Wno-fatal alone demotes a $error to a warning (Rule 6).
run:
	verilator --cc --exe --build -j 8 --top-module tcam_csr_wrap -Wno-fatal -Werror-USERERROR \
	  -CFLAGS "-std=c++17 -O2" \
	  ../../../hdl/ieee8021q/filtering/tcam.sv ../../../hdl/ieee8021q/filtering/rx_mac_filter.sv wrap.sv \
	  sim_main.cpp -o Vtcw
	./obj_dir/Vtcw
