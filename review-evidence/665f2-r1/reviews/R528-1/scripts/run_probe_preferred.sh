#!/bin/sh
# Build and run the reviewer probe for IEEE 1722-2016 Table B.7 note a.
# Usage: run_probe_preferred.sh REPO OUTDIR   (expects gcc, g++, GoogleTest)
set -eu
R=$1/sw/firmware/ctrl; O=$2; H=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$O"
gcc -std=c11 -O2 -DNDEBUG -I"$R/maap" -I"$R/wire" -c "$R/maap/maap.c" -o "$O/maap.o"
g++ -std=c++17 -I"$R/maap" "$H/probes/probe_preferred.cpp" "$O/maap.o" -lgtest -lgtest_main -pthread -o "$O/probe_preferred"
"$O/probe_preferred"
