#!/bin/sh
# Caps the pinned Verilator's build parallelism at 8 jobs (the suite Makefile passes -j 0;
# the last -j given wins). Set PINNED_VERILATOR to the pinned 5.050 wrapper.
exec "${PINNED_VERILATOR:?}" "$@" -j 8
