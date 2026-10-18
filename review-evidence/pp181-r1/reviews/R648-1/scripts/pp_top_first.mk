# Included after tb/pp_top/Makefile: the suite's first build only (every
# section, default parameters), with the build's thread count capped so
# several builds can share the host.  usage:
#   make -C <tree>/tb/pp_top -f Makefile -f pp_top_first.mk VERILATOR=... BJ=4 first
BJ ?= 4
first: ltn_rom.hex ucode.hex
	@rm -f obj_dir/build_tally.txt
	$(VERILATOR) $(subst -j 0,-j $(BJ),$(VFLAGS)) $(SRCS) $(CPP) -o Vpp_top_sim
	./obj_dir/Vpp_top_sim

# the same build without running it
first-build: ltn_rom.hex ucode.hex
	$(VERILATOR) $(subst -j 0,-j $(BJ),$(VFLAGS)) $(SRCS) $(CPP) -o Vpp_top_sim
