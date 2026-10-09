#!/bin/sh
# Pinned Verilator with its internal make parallelism capped at 8 (the suites
# pass `-j 0`), so two concurrent top-level builds stay inside a 12 GB unit.
# env: PINNED_VERILATOR = path of the pinned 5.050 launcher
for a; do shift; if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a=8; fi; set -- "$@" "$a"; prev=$a; done
exec "${PINNED_VERILATOR:?}" "$@"
