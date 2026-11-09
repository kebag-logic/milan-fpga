#!/bin/bash
# (recovering: reports each UB and continues, to show the behaviour) Build and run the 33-sink owed-mask probe against a tsn-c-stack checkout. usage: acmp_mask_probe.sh STACK OUTDIR [SINKS]
set -u
T=$1 O=$2 N=${3:-33}
G=${GTEST:-$DATA/tools/gtest-1.14.0}
mkdir -p "$O"
sed "s/ACMP_MAX_SINKS == 33u/ACMP_MAX_SINKS == ${N}u/" "$(dirname "$0")/acmp_mask_probe.cpp" > "$O/probe.cpp"
gcc -std=c11 -O2 -fsanitize=shift -DACMP_MAX_SINKS=${N}u -I"$T/include" -c "$T/src/acmp.c" -o "$O/acmp.o" &&
g++ -std=c++17 -O2 -fsanitize=shift -DACMP_MAX_SINKS=${N}u -I"$T/include" -I"$T/tests" -I"$G/include" \
    "$O/probe.cpp" "$O/acmp.o" "$G/lib/libgtest.a" "$G/lib/libgtest_main.a" -lpthread -o "$O/probe" && "$O/probe"
