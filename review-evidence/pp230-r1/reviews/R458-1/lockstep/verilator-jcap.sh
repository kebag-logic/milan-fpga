#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Cap a bench Makefile's verilator --build -j to 2 so concurrent probe builds
# stay inside the review's 16-job budget. VERILATOR_REAL is the pinned tool.
for a in "$@"; do shift; case "$a" in -j) set -- "$@" "-j"; NEXTJ=1; continue;; esac
  if [ "${NEXTJ:-0}" = 1 ]; then set -- "$@" 2; NEXTJ=0; else set -- "$@" "$a"; fi; done
exec "${VERILATOR_REAL:?}" "$@"
