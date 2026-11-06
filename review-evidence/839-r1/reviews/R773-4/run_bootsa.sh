#!/bin/sh
# Usage: run_bootsa.sh <repo> <receipt-dir> <tmpdir> <verilator>
set -u
repo=$1; out=$2; export TMPDIR=$3; V=$4
cd "$repo/tb/verilator/milan_dp" || exit 2
"$V" --version > "$out/bootsa.verilator_version.txt" 2>&1
make -j16 VERILATOR="$V" bootsa > "$out/bootsa.log" 2>&1; echo $? > "$out/bootsa.rc"
PATH="$(dirname "$V"):$PATH" make VERILATOR="$V" bootsa-mutants > "$out/bootsa_mutants.log" 2>&1; echo $? > "$out/bootsa_mutants.rc"
