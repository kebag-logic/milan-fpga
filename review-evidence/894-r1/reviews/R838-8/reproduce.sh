#!/usr/bin/env bash
# Run from the exact source checkout; write receipts to the supplied directory.
set -euo pipefail
packet_dir="$(cd "$(dirname "$0")" && pwd)"
receipt_dir="${1:?usage: reproduce.sh OUTPUT_DIRECTORY}"
mkdir -p "$receipt_dir"
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if > "$receipt_dir/flip-check.txt" 2>&1
printf '0\n' > "$receipt_dir/flip-check.rc"
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check > "$receipt_dir/load-check.txt" 2>&1
printf '0\n' > "$receipt_dir/load-check.rc"
python3 -B "$packet_dir/verify_evidence.py" . "$receipt_dir" > "$receipt_dir/evidence-check.txt" 2>&1
python3 -B "$packet_dir/verify_source.py" . > "$receipt_dir/source-integrity.txt" 2>&1
