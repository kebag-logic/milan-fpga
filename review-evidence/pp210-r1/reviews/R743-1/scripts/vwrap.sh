#!/usr/bin/env bash
# The pinned Verilator ($PINNED_VERILATOR, default `verilator` on PATH) with each
# build's "-j 0" capped at 2 jobs, so several suites can build side by side
# inside a memory cap.
args=(); prev=""
for a in "$@"; do if [ "$prev" = "-j" ] && [ "$a" = "0" ]; then a=2; fi; args+=("$a"); prev=$a; done
exec "${PINNED_VERILATOR:-verilator}" "${args[@]}"
