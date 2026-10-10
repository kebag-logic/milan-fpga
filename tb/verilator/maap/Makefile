# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# KL_maap verification against IEEE 1722-2016 Annex B (#686): golden frames,
# the Table B.7 walk and conflict cells, strict B.3.4 timer intervals.
#   make          - build and run the harness, then the mutation campaign
#   make run      - the harness only
#   make mutants  - every planted defect must fail its named check (mutants.py)
#   make coverage - line coverage, gated at 95 %
# 10 kHz scaled clock: 1 ms tick = 10 cycles (probe 500 ms ~ 5k cycles).
VERILATOR ?= verilator
VERILATOR_JOBS ?= 0
RTL_DIR    = ../../../hdl
TOP        = KL_maap
MAAP_RTL  ?= $(RTL_DIR)/ieee1722/maap/KL_maap.sv
MDIR      ?= obj_dir
COV_MDIR  ?= obj_cov
VFLAGS = --cc --exe --build -j $(VERILATOR_JOBS) --top-module $(TOP) \
         -GCLK_FREQ_HZ_P=10000 --public-flat-rw \
         -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
         -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-IMPORTSTAR -Wno-CASEINCOMPLETE \
         -Wno-EOFNEWLINE -CFLAGS "-std=c++17 -O2 -Wall -Wextra"
SRCS = $(MAAP_RTL)
.PHONY: all run build mutants clean coverage integration-build
all: run mutants

# #696: the real CSR-to-MAAP path, using the datapath suite's source authority.
DP_MDIR ?= obj_integration
integration-build:
	$(MAKE) -f integration.mk build DP_MDIR=$(DP_MDIR) MAAP_RTL=$(abspath $(MAAP_RTL))

build:
	$(VERILATOR) $(VFLAGS) -Mdir $(MDIR) $(SRCS) sim_main.cpp -o VKL_maap_sim

run: build
	$(abspath $(MDIR))/VKL_maap_sim

mutants:
	python3 mutants.py

# Line coverage, gated at 95 % (defensive arms carry coverage_off pragmas)
coverage:
	mkdir -p $(COV_MDIR)
	$(VERILATOR) $(VFLAGS) --coverage --Mdir $(COV_MDIR) $(SRCS) sim_main.cpp \
	    -o VKL_maap_cov
	cd $(COV_MDIR) && ./VKL_maap_cov
	verilator_coverage --annotate $(COV_MDIR)/annotated --annotate-min 1 $(COV_MDIR)/coverage.dat
	python3 ../avtp_rxmon/cov_gate.py $(COV_MDIR)/annotated 95 KL_maap.sv
clean:
	rm -rf obj_dir obj_cov obj_mut_* coverage.dat cov_annotated
