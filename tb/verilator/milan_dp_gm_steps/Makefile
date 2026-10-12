# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# THE GM STEP LEG (#387, #602, #621) AND ITS DEFAULT CONTROLS, split out of
# tb/verilator/milan_dp for wall clock. ../milan_dp keeps the leg's one
# recipe, its harness (sim_gmstep.cpp) and the generated images it reads;
# this suite runs them on its own worker, and owns their control driver.
#
#   make                - the clean leg with every phase, then the five
#                         acceptance controls; those run the leg without its
#                         #621 small-step phase, which holds none of their
#                         named checks
#   make gmstep-mutants - the whole control inventory, every control on the
#                         whole leg: an explicit campaign, outside the sweep's
#                         deadline (docs/testing/TESTING.md)
#
# WHY THIS IS ITS OWN SUITE DIRECTORY (#621 runtime round). The #621 phase
# took the leg from 48 s to 253 s of CPU, and the sweep ran the leg seven
# times: the clean leg, the driver's positive control and five controls. On
# hosted run 38048622822 milan_dp then hit its 4800 s limit. Without this
# change dev's own milan_dp already took 2973-3520 s on hosted pushes, over
# 60% of that limit. Moving the leg and its controls here takes its whole
# share off milan_dp's worker. Every check and control still runs on every
# PR; only the controls skip the phase none of them names. Native per-leg
# times and the hosted projection are in this suite's README.

.PHONY: all run gmstep-mutants
all: run

run:
	$(MAKE) -C ../milan_dp gmstep
	python3 gmstep_mutants.py --no-small-steps

gmstep-mutants:
	$(MAKE) -C ../milan_dp gmstep
	python3 gmstep_mutants.py --all
