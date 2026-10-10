#!/usr/bin/env bash
# Reproduce the R574-2 recompute receipts from the archived packet.
# Usage: run_all.sh <archive-author-dir> <out-dir>
# <archive-author-dir> is review-evidence/608-b14-r1/author extracted from
# archive commit c848925d2e88a98e7f31b663e5dd4f342b765487.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
a=$1 out=$2
mkdir -p "$out"
python3 -I "$here/item3_hold.py" "$a" > "$out/item3_hold.txt"
python3 -I "$here/soak_counters.py" "$a" > "$out/soak_counters.txt"
python3 -I "$here/slip_lb_ledger.py" "$a" > "$out/slip_lb_ledger.txt"
python3 -I "$here/item6_console.py" "$a" > "$out/item6_console.txt"
