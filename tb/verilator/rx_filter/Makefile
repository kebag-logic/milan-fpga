# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Verilator verification of rx_mac_filter.sv (TCAM-driven RX dest-MAC filter).
# Pure RTL (tcam.sv), no Xilinx tools needed.
#   make        - run the clean harness, then prove a missing, swapped, tied-off
#                 and direction-wrong binding of the real TCAM seam is rejected
#   make clean  - remove build artifacts

VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = rx_mac_filter

# -Wno-fatal keeps the waived lint categories non-fatal - and on its own it
# also demotes an elaboration $error to a warning, so an illegal shield shape
# BUILDS and simulates (review built -GTDATA_WIDTH=52 here, rc 0).
# -Werror-USERERROR restores the contract: a $error is a failed verilate, the
# same discipline the integrated milan_dp suite carries.
# -Werror-PINMISSING / -Werror-UNDRIVEN: a missing binding or a port with the
# wrong direction is refused BY NAME even under -Wno-fatal. Verilator inlines
# the child, so no harness check can see a direction error; these two are what
# let binding_mutant.py tell "direction-wrong" from "did not compile".
VFLAGS = --cc --exe --build -j 0 \
         --top-module $(TOP) \
         -Wall -Wno-fatal -Werror-USERERROR -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
         -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY \
         -Werror-PINMISSING -Werror-UNDRIVEN \
         -CFLAGS "-std=c++17 -O2"

SRCS = $(RTL_DIR)/ieee8021q/filtering/tcam.sv $(RTL_DIR)/ieee8021q/filtering/rx_mac_filter.sv
CPP  = sim_main.cpp

# Rule 6: the module's elaboration contract, graded by MUTATION. Each case is
# a parameter set the module declares impossible; elaboration must REFUSE it
# WITH THE MODULE'S OWN DIAGNOSTIC. The exit status alone proves nothing:
# review deleted the whole $error chain and three of the four refusals still
# printed [PASS], refused by an accidental SELRANGE/ASCRANGE/ZEROREPL warning
# in tcam.sv rather than by the contract. So each arm captures stderr to a
# file and requires a USERERROR line carrying `rx_mac_filter: <PARAM>=<value> `
# - grep's status on that FILE is the assertion, and nothing goes through a
# pipe (a pipeline returns its LAST command's status, which is how a refused
# build reads as a pass). The legal default must still elaborate: that last
# arm is what makes the contract a guard and not a ban.
NEG_LINT  = $(VERILATOR) --lint-only -Werror-USERERROR --top-module $(TOP) $(SRCS)
NEG_CASES = TDATA_WIDTH=32 TDATA_WIDTH=52 NUM_ENTRIES=0 ACTION_WIDTH=0

.PHONY: all run binding-negative negative print-vflags clean
all: binding-negative negative

run:
	$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vrx_filter_sim
	@echo "======================================================================"
	./obj_dir/Vrx_filter_sim

# Rule 5: the TCAM lookup key is a real production seam, not an internal
# observation backdoor. binding_mutant.py applies one mutation at a time -
# missing, swapped, tied-off, direction-wrong - to a COPY of the RTL, builds it
# with the recipe below and requires the named refusal or the SAME harness's
# own FAIL. The run prerequisite is the positive control: the unmodified
# boundary must pass before a deliberate misbinding is meaningful.
binding-negative: run
	@echo "======================================================================"
	python3 binding_mutant.py

# Rule 3: the seam arms build with THIS recipe, read through this target, never
# a copy of it. One word per line so the shell's quoting of -CFLAGS survives.
print-vflags:
	@printf '%s\n' $(VERILATOR) $(VFLAGS)

negative:
	@echo "======================================================================"
	@mkdir -p obj_dir; pass=0; fail=0; \
	for c in $(NEG_CASES); do \
	  log=obj_dir/neg_$${c%%=*}_$${c##*=}.log; \
	  if $(NEG_LINT) -G$$c >/dev/null 2>$$log; then \
	    echo "[FAIL] elaboration ACCEPTED illegal $$c"; fail=$$((fail+1)); \
	  elif grep -q "USERERROR.*rx_mac_filter: $$c " $$log; then \
	    echo "[PASS] elaboration refused $$c with the contract's own diagnostic"; \
	    pass=$$((pass+1)); \
	  else \
	    echo "[FAIL] elaboration refused $$c, but NOT by the contract (see $$log)"; \
	    fail=$$((fail+1)); \
	  fi; \
	done; \
	if $(NEG_LINT) -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM \
	     >/dev/null 2>&1; then \
	  echo "[PASS] elaboration accepted the legal default shape"; pass=$$((pass+1)); \
	else \
	  echo "[FAIL] elaboration REFUSED the legal default shape"; fail=$$((fail+1)); \
	fi; \
	echo ""; \
	echo "$$((pass+fail)) checks: $$pass PASS, $$fail FAIL"; \
	test $$fail -eq 0

clean:
	rm -rf obj_dir
