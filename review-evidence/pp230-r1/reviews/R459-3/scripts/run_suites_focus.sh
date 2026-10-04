#!/usr/bin/env bash
# Run one SRP suite's default `make` in an extracted head tree.
# usage: run_suites_focus.sh <tree> <suite> <logdir>
set -u
T=$1; SU=$2; L=$3
mkdir -p "$L"
export VERILATOR="$(dirname "$(readlink -f "$0")")/verilator-j.sh" VJ=${VJ:-2}
make -C "$T/tb/$SU" VERILATOR="$VERILATOR" > "$L/$SU.log" 2>&1
echo $? > "$L/$SU.rc"
