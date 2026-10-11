#!/bin/sh
# usage: run_bg.sh <name> <workdir> <command...>
# Runs a command detached, logging to receipts/<name>.log and its exit
# status to receipts/<name>.rc. PACKET and VERILATOR come from the caller.
name=$1; dir=$2; shift 2
log="$PACKET/receipts/$name.log"; rc="$PACKET/receipts/$name.rc"
rm -f "$rc"
( cd "$dir" && { date -u +"start %FT%TZ"; "$@"; } > "$log" 2>&1; echo $? > "$rc"; date -u +"end %FT%TZ" >> "$log" ) &
