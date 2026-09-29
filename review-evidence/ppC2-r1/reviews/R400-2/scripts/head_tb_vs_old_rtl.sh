#!/bin/sh
# usage: head_tb_vs_old_rtl.sh CLONE HEAD OLD WORKDIR VERILATOR LOG
# Runs HEAD's tb/maap against OLD's hdl/maap/KL_pp_maap.sv (failing-arm check).
set -eu
clone=$1 head=$2 old=$3 work=$4 vl=$5 log=$6
rm -rf "$work"; mkdir -p "$work"
git -C "$clone" archive "$head" | tar -x -C "$work"
git -C "$clone" show "$old:hdl/maap/KL_pp_maap.sv" > "$work/hdl/maap/KL_pp_maap.sv"
set +e
make -C "$work/tb/maap" run VERILATOR="$vl" > "$log" 2>&1
echo "rc=$?" >> "$log"
