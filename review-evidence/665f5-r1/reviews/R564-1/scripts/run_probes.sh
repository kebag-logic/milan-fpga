#!/usr/bin/env bash
# Reviewer probes for R564-1. Builds the candidate's own AECP core fixture
# (first 157 lines of test_aecp.cpp at the reviewed head) plus the probe tests,
# in a DISPOSABLE export, and runs them through the candidate's aecp_arms.py.
# Usage: run_probes.sh <disposable-export-root> <probe-dir> <output-dir>
# The export must carry gptp-processor and protocol-processor at their pins.
set -eu
root=$1; probes=$2; out=$3
t="$root/sw/firmware/ctrl/test/test_aecp.cpp"
head -n 157 "$t" > "$out.fixture.cpp"
cat "$out.fixture.cpp" "$probes/probe_tests.cpp" "$probes/probe_tests_p6.cpp" > "$t"
cd "$root/sw/firmware/ctrl/test"
PYTHONDONTWRITEBYTECODE=1 python3 -B aecp_arms.py --core --output "$out" --filter 'Core.P*'
