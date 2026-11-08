#!/bin/sh
# Usage: escape_without_round3.sh <mutation work dir> <plant>...
# Runs each plant's ACMP test binary twice: on the whole suite, and with the three round 3 tests excluded.
# A plant the round 2 suite would have missed fails the first run and passes the second.
set -u
W=$1; shift
X='-AcmpOwed.ProbesFallingDueInTheDrainWaitForTheDeferredBind:AcmpOwed.DeferredBindAtTheDocumentedMarginMeetsItsTimeout:AcmpOwed.HoldEndsWithTheLastHeldProbe'
for m in "$@"; do
  b=$W/$m/acmp
  env -u GTEST_FILTER "$b" >/dev/null 2>&1; full=$?
  n=$(env -u GTEST_FILTER "$b" --gtest_filter="$X" 2>&1 | sed -n 's/^\[==========\] \([0-9]*\) tests.*ran.*/\1/p')
  env -u GTEST_FILTER "$b" --gtest_filter="$X" >/dev/null 2>&1; without=$?
  echo "$m full_suite_rc=$full without_round3_rc=$without tests_without=$n"
done
