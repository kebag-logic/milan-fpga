#!/bin/sh
# R608-4 campaign launcher: each campaign runs in its own exported tree with its
# own log and rc file under receipts/. Usage: run_campaigns.sh PACKET VERILATOR
P=$1; V=$2; S=$P/scratch; R=$P/receipts
mkdir -p "$R"
( cd "$S/head" && python3 -B scripts/check_aecp_commands.py --selftest > "$R/head-selftest.log" 2>&1; echo $? > "$R/head-selftest.rc" ) &
( cd "$S/head" && python3 -B scripts/check_aecp_commands.py > "$R/head-gate.log" 2>&1; echo $? > "$R/head-gate.rc" ) &
( cd "$S/head-sweep/tb/aecp_cmds" && make VERILATOR="$V" run > "$R/head-aecp_cmds-run.log" 2>&1; echo $? > "$R/head-aecp_cmds-run.rc" ) &
( cd "$S/head-mut/tb/aecp_cmds" && python3 -B mutants.py --output "$S/mutout" --verilator "$V" --jobs 6 > "$R/head-aecp_cmds-mutants.log" 2>&1; echo $? > "$R/head-aecp_cmds-mutants.rc" ) &
wait
