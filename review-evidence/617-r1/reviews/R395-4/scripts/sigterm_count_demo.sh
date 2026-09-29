#!/usr/bin/env bash
# How many SIGTERMs a recipe's process receives when timeout(1) kills
# `make -C <dir>` (scripts/run_all_suites.sh's guard): timeout signals the make
# and its process group, and make then also forwards SIGTERM to its running child.
# Usage: sigterm_count_demo.sh <make binary> <demo dir with Makefile + count.py>
set -u
for m in "$1" /usr/bin/make; do echo "== $($m --version | head -1)"; timeout 1 "$m" -s -C "$2" all; echo "timeout rc=$?"; timeout 5 tail -f /dev/null; done 2>&1
