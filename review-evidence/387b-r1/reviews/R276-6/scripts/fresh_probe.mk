# SPDX-License-Identifier: CERN-OHL-W-2.0
# R276-6 reviewer probe: loaded beside the suite's own Makefile
# (make -C <milan_dp> -f Makefile -f fresh_probe.mk fresh-probe), so the
# probe runs inside a recipe of the real parent make, as `run` runs
# gmstep_mutants.py. PROBE_PY, RUNNER and LABEL come from the command line.
.PHONY: fresh-probe
fresh-probe:
	python3 $(PROBE_PY) $(CURDIR) $(RUNNER) $(LABEL)
