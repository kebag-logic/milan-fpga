#!/usr/bin/env bash
# Reviewer probes (R883-1, PR #966 at f15b3a7d2bf1ba84d14140a4cda8a193d2e6b1c9), portable.
# Usage: run_probes.sh <repo checkout at the head> <scratch out dir>
# Needs g++/gcc with -fsanitize=undefined,address, GoogleTest/GoogleMock (-lgtest -lgmock).
#  1. the port's own 34 GoogleTests under UBSan/ASan (unmodified sources);
#  2. the same suite plus the step probes (probe_step_nrr.inc, probe_outage.inc) on a scratch copy of
#     test_gptp.cpp whose simulated peer answers a Pdelay_Req after g_turn_ns (make_turn_probe.py).
# No tracked file is modified: every copy and object is written under <scratch out dir>.
set -euo pipefail
repo=$(cd "$1" && pwd)
out=$(mkdir -p "$2" && cd "$2" && pwd)
here=$(cd "$(dirname "$0")" && pwd)
fw="$repo/sw/firmware"
gcc -std=c11 -O1 -g -fsanitize=undefined,address -I"$fw/ctrl/gptp" -c "$fw/ctrl/gptp/gptp.c" -o "$out/gptp_san.o"
g++ -std=c++17 -O1 -g -fsanitize=undefined,address -I"$fw/ctrl/gptp" -I"$fw/gtest" "$out/gptp_san.o" \
    "$fw/ctrl/test/test_gptp.cpp" "$fw/gtest/fw_gtest_main.cpp" -o "$out/test_gptp_san" -lgtest -lgmock -pthread
"$out/test_gptp_san" > "$out/ubsan_suite.log" 2>&1 || true
grep "runtime error" "$out/ubsan_suite.log" | sort | uniq -c || true
grep -E "PASSED|FAILED" "$out/ubsan_suite.log" || true
gcc -std=c11 -O2 -I"$fw/ctrl/gptp" -c "$fw/ctrl/gptp/gptp.c" -o "$out/gptp_o2.o"
cat "$here/probe_step_nrr.inc" "$here/probe_outage.inc" > "$out/all.inc"
python3 -I "$here/make_turn_probe.py" "$fw/ctrl/test/test_gptp.cpp" "$out/all.inc" "$out/test_probe.cpp"
g++ -std=c++17 -O1 -I"$fw/ctrl/gptp" -I"$fw/gtest" "$out/gptp_o2.o" "$out/test_probe.cpp" \
    "$fw/gtest/fw_gtest_main.cpp" -o "$out/test_probe" -lgtest -lgmock -pthread
"$out/test_probe" 2>&1 | grep -E "^\[(PROBE|OUTAGE)\]|PASSED|FAILED"
