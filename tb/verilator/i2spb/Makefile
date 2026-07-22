run:
	verilator --cc --exe --build -j 8 --top-module KL_i2s_playback \
	  -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
	  -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-EOFNEWLINE \
	  -CFLAGS "-std=c++17 -O2" \
	  ../../../hdl/common/cdc_pair_fifo.sv ../../../hdl/common/cdc_pulse.sv \
	  ../../../hdl/ieee1722/aaf/KL_i2s_playback.sv \
	  sim_main.cpp -o Vi2spb_sim
	./obj_dir/Vi2spb_sim
