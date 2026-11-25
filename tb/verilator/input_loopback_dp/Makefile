# SPDX-License-Identifier: CERN-OHL-W-2.0
WORK ?= $(CURDIR)/obj_tests
VERILATOR ?= verilator
VERILATOR_JOBS ?= 4
export VERILATOR VERILATOR_JOBS
.PHONY: all one eight
all: one eight
one:
	python3 run.py --shape 1 --work $(WORK)/one
eight:
	python3 run.py --shape 8 --work $(WORK)/eight
