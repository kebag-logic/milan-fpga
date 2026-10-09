#!/usr/bin/env bash
# rx_filter suite at the reviewed head with the pinned Verilator: positive run,
# binding mutants and the four elaboration-contract negatives plus legal default.
# Arg 1: pinned Verilator directory (holding the `verilator` wrapper).
set -u
export PATH="$1:$PATH" PYTHONDONTWRITEBYTECODE=1
verilator --version
make -C tb/verilator/rx_filter clean >/dev/null
make -C tb/verilator/rx_filter all VERILATOR="$1/verilator"
rc=$?
make -C tb/verilator/rx_filter clean >/dev/null
exit $rc
