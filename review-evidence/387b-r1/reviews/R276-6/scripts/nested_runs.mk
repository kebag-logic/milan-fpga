# SPDX-License-Identifier: CERN-OHL-W-2.0
# R276-6 reviewer probe: run the head's gmstep runners INSIDE a recipe of the
# suite's own parent make, as `run` and `gmstep-mutants` do. Loaded beside it:
#   make -C <milan_dp> -f Makefile -f nested_runs.mk <target> [CTL_ARGS=...]
# CTL_PY is scripts/run_gmstep_controls.py from this packet.
.PHONY: nested-default nested-ctl
# exactly the last line of the `run` recipe
nested-default:
	python3 gmstep_mutants.py
# chosen controls and positive legs through the head's own runner functions
nested-ctl:
	python3 $(CTL_PY) $(CURDIR) $(CTL_WORK) $(CTL_ARGS)
