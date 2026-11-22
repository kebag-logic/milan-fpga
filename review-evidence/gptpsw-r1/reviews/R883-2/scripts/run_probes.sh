#!/bin/sh
# run_probes.sh CLONE PACKET: the reviewer's firmware probes at the clone's head. Each probe file is appended to a
# scratch copy of test_gptp.cpp (the suite's own Net fixture and step_across_the_link assertions); nothing tracked
# is written. Needs gcc/g++, GoogleTest/GoogleMock. Outputs under PACKET/scratch/gtest/.
set -eu
R=$1; P=$2; B=$P/scratch/gtest
"$P/scripts/build_gptp_suite.sh" "$R" "$B/head"
"$B/head/test_gptp" | tail -3
"$P/scripts/build_gptp_suite.sh" "$R" "$B/ext" "$P/probes/probe_matrix_ext.inc"
"$B/ext/test_gptp" --gtest_filter='Net.Probe*:Net.AStep*:Net.ABackward*' | grep -E 'FAILED|OK \]|Which is: [1-9]' || true
"$P/scripts/build_gptp_suite.sh" "$R" "$B/sweep" "$P/probes/probe_midstep_sweep.inc"
"$B/sweep/test_gptp" --gtest_filter='MidSweep.*' | grep SWEEP
"$P/scripts/build_gptp_suite.sh" "$R" "$B/outage" "$P/probes/r883-1-outage-and-step-adapted-plus-mid.inc"
"$B/outage/test_gptp" --gtest_filter='Net.Outage*:Net.Probe*' | grep -E '^\[(PROBE|OUTAGE)\]'
"$P/scripts/build_gptp_suite.sh" "$R" "$B/ubsan" "$P/probes/probe_matrix_ext.inc" 1
"$B/ubsan/test_gptp" 2>&1 | grep -cE 'runtime error' || true
