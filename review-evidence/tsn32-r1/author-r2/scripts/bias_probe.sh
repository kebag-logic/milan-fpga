#!/bin/bash
# Instrumented copy of round 2's draft walk test (probe/walk_probe.cpp: the draft with sink 32 alone on a third
# interface, before the poll bias was added to the test; the biases below are macros): at 33 sinks, count polls that find sink 32's probe at the
# owed queue's head (head) and those that send it while its timer still waits for it (left), per command bias
# (BIAS: 1 in BIAS commands to sink 32, 0 for none), poll bias (POLLB: poll first 1 in POLLB steps while owed) and
# restore bias (RB). usage: bias_probe.sh OUT
set -u
. <scratch>/scripts/env.sh
S=<scratch> O=$1; mkdir -p $O
cd <lanes>/tsn-c-stack-32-walk
gcc -std=c11 -O1 -DACMP_MAX_SINKS=33u -DNDEBUG -DCTRL_REENTRY_ASSERT -Iinclude -c src/acmp.c -o $O/acmp.o
g++ -std=c++20 -O1 $(pkg-config --cflags gtest) -c tests/main.cpp -o $O/main.o
for cfgv in "4 0 1" "0 0 1" "8 0 1" "16 0 1" "4 2 1" "4 4 1" "4 2 0" "8 2 0" "0 2 0" "4 3 0"; do
  set -- $cfgv
  g++ -std=c++20 -O1 -DBIAS=$1u -DPOLLB=$2u -DRB=$3 -DSTEPS=8000u -DACMP_MAX_SINKS=33u -Iinclude -Iexamples -Itests $(pkg-config --cflags gtest) -c $S/probe/walk_probe.cpp -o $O/wp.o
  g++ $O/wp.o $O/acmp.o $O/main.o $(pkg-config --libs gmock gtest) -o $O/wp
  echo "BIAS=$1 POLLB=$2 RB=$3 $($O/wp --gtest_filter=*ThirtyThree* 2>&1 | grep sinks=)"
done
rm -f $O/*.o $O/wp
