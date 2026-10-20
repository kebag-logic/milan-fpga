#!/bin/sh
# Build and run the clean dynmap leg of tb/verilator/milan_dp at the reviewed head.
# Usage: run_clean_dynmap.sh <clone> <pinned-verilator> <receipt-dir>
set -u
C=$1; V=$2; R=$3
cd "$C/tb/verilator/milan_dp" || exit 9
VERILATOR=$V make -s -j16 VERILATOR=$V dynmap > "$R/dynmap_clean.log" 2>&1
echo $? > "$R/dynmap_clean.rc"
