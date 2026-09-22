# SPDX-License-Identifier: CERN-OHL-W-2.0
# KL_aecp_desc_store suite — exit 0 = PASS.
VERILATOR ?= verilator
HDL        = ../../hdl
TOP        = KL_aecp_desc_store

# MEM_TIMEOUT_CYC_P is compressed from its 4096 default so the "no bridge at
# all" arm runs in a few hundred clocks instead of tens of thousands; the BFM's
# 24-clock first-word latency stays well inside it.
VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -GMEM_TIMEOUT_CYC_P=64 \
         -GNAME_ENTRIES_P=256 \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
         -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"

SRCS = $(HDL)/aecp/KL_aecp_desc_store.sv
CPP  = sim_main.cpp

run: image.bin
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vdesc_store_sim
	./obj_dir/Vdesc_store_sim

# the generator's own worked example — proves generator and RTL agree on the
# documented format, not merely on each other
image.bin: $(HDL)/aecp/desc/gen_desc_image.py $(HDL)/aecp/desc/example_milan_8.json
	python3 $(HDL)/aecp/desc/gen_desc_image.py \
	  -i $(HDL)/aecp/desc/example_milan_8.json -o $@ -m image.map >/dev/null

clean:
	rm -rf obj_dir image.bin image.map

.PHONY: run clean
