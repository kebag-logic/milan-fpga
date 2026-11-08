#!/bin/sh
# SPDX-License-Identifier: MIT
# usage: run_gates6.sh GATES_CLONE RV32_CLONE WORK TOOLS JOBS
# Starts, each detached with its own log and rc file: the full gate kit with --graphs (which runs the
# full mutation campaign) on one clean clone, and the RV32 gate (Debug and Release) on another.
# Returns at once; poll WORK/val.rc and WORK/rv32.rc. clang-18 (the comment lexer) and clang-tidy 18 come first on PATH; the hosted
# clang arm uses the host clang, as in the author's run. The gtest variables point at TOOLS/gtest-1.14.0.
set -u
g=$1; r=$2; w=$3; t=$4; j=$5; mkdir -p "$w"
export PATH=$t/clang-18/bin:$t/clang-tidy-18/bin:$PATH PKG_CONFIG_PATH=$t/gtest-1.14.0/lib/pkgconfig CMAKE_PREFIX_PATH=$t/gtest-1.14.0 LD_LIBRARY_PATH=$t/gtest-1.14.0/lib
(cd "$g" && nohup python3 scripts/validate.py --graphs --work "$w/val" --jobs "$j" > "$w/val.log" 2>&1; echo $? > "$w/val.rc") > /dev/null 2>&1 &
(cd "$r" && nohup python3 scripts/baremetal.py --work "$w/rv32" --jobs 2 > "$w/rv32.log" 2>&1; echo $? > "$w/rv32.rc") > /dev/null 2>&1 &
