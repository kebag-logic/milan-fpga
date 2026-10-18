r648-default: ltn_rom.hex ucode.hex
	@rm -f obj_dir/build_tally.txt
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vpp_top_sim
	./obj_dir/Vpp_top_sim
