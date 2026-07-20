run:
	verilator --cc --exe --build -j 8 --top-module KL_pcm_lpf -Wno-fatal \
	  -CFLAGS "-std=c++17 -O2" ../../../hdl/avtp/KL_pcm_lpf.sv sim_main.cpp -o Vpcmlpf
	./obj_dir/Vpcmlpf
