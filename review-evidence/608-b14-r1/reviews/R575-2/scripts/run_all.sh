#!/usr/bin/env bash
# R575-2 receipts. usage: run_all.sh <archive root: review-evidence/608-b14-r1 extracted from c848925d> <out dir>
set -eu
A=$1; O=$2; S=$(cd "$(dirname "$0")" && pwd); mkdir -p "$O"
python3 -I "$S/check_evidence_identity.py" "$A" > "$O/evidence-identity.txt"
python3 -I "$S/check_item3_withdrawals.py" "$A/author/item3" > "$O/item3-withdrawals.txt"
python3 -I "$S/check_slip_lb_ledger.py" "$A/author" > "$O/slip-lb-ledger.txt"
python3 -I "$S/check_soak_records.py" "$A/author" > "$O/soak-records.txt"
python3 -I "$S/check_restore_rows.py" "$A/author" > "$O/restore-rows.txt"
python3 -I "$S/check_item2_counters.py" "$A/author" > "$O/item2-counters.txt"
python3 -I "$S/check_item2_phase_times.py" "$A/author" > "$O/item2-phase-times.txt"
grep -h 'NVM:' "$A/author/item2/setup/dut-before.txt" "$A/author/restore/console-final.txt" > "$O/nvm-lines.txt"
echo ok
