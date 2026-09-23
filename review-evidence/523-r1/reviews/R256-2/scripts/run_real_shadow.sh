#!/usr/bin/env bash
# Reviewer receipt: the complete real gptp_shadow make in a disposable copy.
# Usage: run_real_shadow.sh COPY VERILATOR_WRAPPER RECEIPT_DIR TMPDIR
set -u
copy="$1"; verilator="$2"; out="$3"; tmp="$4"
python3 "$(dirname "$0")/integrity.py" "$copy" b5ce20eca8b59709ec5bc6115e5e15bfc312f283 > "$out/real-shadow-integrity-before.txt" 2>&1
start=$(date +%s)
env TMPDIR="$tmp" PYTHONDONTWRITEBYTECODE=1 VERILATOR="$verilator" VERILATOR_JOBS=8 \
  make -C "$copy/tb/verilator/gptp_shadow" > "$out/real-shadow-make.log" 2>&1
rc=$?
end=$(date +%s)
echo "exit $rc seconds $((end - start))" > "$out/real-shadow-exit.txt"
python3 "$(dirname "$0")/integrity.py" "$copy" b5ce20eca8b59709ec5bc6115e5e15bfc312f283 > "$out/real-shadow-integrity-after.txt" 2>&1
ls -A "$tmp" > "$out/real-shadow-tmp-after.txt"
