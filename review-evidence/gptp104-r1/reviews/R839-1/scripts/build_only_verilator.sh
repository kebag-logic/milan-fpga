#!/bin/sh
# Stand-in for $(VERILATOR) in the engine Makefile's real `run` recipe: runs
# the pinned Verilator with the recipe's own arguments and environment (so
# the suite model is really built through whatever OBJCACHE/CCACHE_* the
# Makefile set), then exits 3 so the recipe stops before the simulations.
$REVIEWS/gptp104-r839-1-packet/scratch/bin/verilator "$@" || exit $?
exit 3
