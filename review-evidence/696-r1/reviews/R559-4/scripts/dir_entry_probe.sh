#!/bin/sh
# Usage: dir_entry_probe.sh <clone> <scratchdir> <make>...
# Fake ../milan_dp whose print-srcs names a directory (alone, and beside a real file);
# HEAD integration.mk copied into a disposable tree. Does the guard refuse it?
set -u
C=$1; S=$2; shift 2; G=$S/g; rm -rf "$S"; mkdir -p "$G/tb/verilator/maap" "$G/tb/verilator/milan_dp" "$G/tb/verilator/maap/adir"
cp "$C/tb/verilator/maap/integration.mk" "$G/tb/verilator/maap/integration.mk"; : > "$G/tb/verilator/maap/real.sv"
for m in "$@"; do
  for srcs in "adir" "real.sv adir" "../milan_dp"; do
    printf 'print-srcs:\n\t@echo %s\nprint-dp-vflags:\n\t@echo x\n' "$srcs" > "$G/tb/verilator/milan_dp/Makefile"
    out=$(cd "$G/tb/verilator/maap" && "$m" -s -f integration.mk build VERILATOR=echo DP_MDIR="$S/o" 2>&1 | grep -vE '^python3|^mkdir|Traceback|File |^ ' | tail -2 | cut -c1-160 | tr '\n' ' ')
    echo "$($m --version | head -1) srcs='$srcs' :: $out"
  done
done
