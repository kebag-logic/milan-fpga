#!/bin/sh
# build_gptp_suite.sh REPO OUTDIR [EXTRA_TEST_CPP] [UBSAN=0|1]
# Builds the gPTP port's GoogleTest suite at REPO (optionally with probe tests appended) into OUTDIR/test_gptp.
set -eu
R=$1; O=$2; X=${3:-}; U=${4:-0}
mkdir -p "$O"
SAN=""; [ "$U" = 1 ] && SAN="-fsanitize=undefined -fno-sanitize-recover=undefined"
INC="-I$R/sw/firmware/ctrl/gptp -I$R/sw/firmware/gtest -I$R/sw/firmware/ctrl -I$R/sw/firmware/ctrl/mbx"
cp "$R/sw/firmware/ctrl/test/test_gptp.cpp" "$O/suite.cpp"
[ -n "$X" ] && cat "$X" >> "$O/suite.cpp"
gcc -std=c11 -O2 -DNDEBUG -Wall -Wextra -Werror -pedantic $SAN $INC -c "$R/sw/firmware/ctrl/gptp/gptp.c" -o "$O/gptp.o"
g++ -std=c++20 -O1 -g -Wall -Wextra $SAN $INC -I"$R/sw/firmware/ctrl/test" -c "$O/suite.cpp" -o "$O/suite.o"
g++ -std=c++20 -O1 $SAN $INC -c "$R/sw/firmware/gtest/fw_gtest_main.cpp" -o "$O/main.o"
g++ -std=c++20 -O1 $SAN $INC -DFW_TALLY_LABEL='"probe"' -c "$R/sw/firmware/gtest/fw_gtest_label.cpp" -o "$O/label.o" 2>/dev/null || true
g++ $SAN "$O"/*.o -o "$O/test_gptp" -lgmock -lgtest -pthread
