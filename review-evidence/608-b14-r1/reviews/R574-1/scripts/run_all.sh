#!/bin/sh
# Re-create the R574-1 receipts. Usage: run_all.sh <evidence-root> <findings-page> <out-dir>
# <evidence-root> is review-evidence/608-b14-r1 extracted from the published evidence commit
# c848925d2e88a98e7f31b663e5dd4f342b765487; <findings-page> is docs/findings/B14_BENCH_5603C353.md
# at head 6ec1a3a9a827575a84fb60d42ad3b085ecb70f19.
set -eu
R=$1; PAGE=$2; O=$3; D=$(cd "$(dirname "$0")" && pwd); A=$R/author
mkdir -p "$O"
python3 -I "$D/check_manifests.py" "$R" > "$O/manifest-check.txt"
python3 -I "$D/check_item2_table.py" "$A" "$PAGE" > "$O/item2-table-check.txt"
python3 -I "$D/check_item2_counters.py" "$A" > "$O/item2-counters-check.txt"
python3 -I "$D/check_item3.py" "$A" "$PAGE" > "$O/item3-check.txt"
python3 -I "$D/check_item4.py" "$A" "$PAGE" > "$O/item4-check.txt"
python3 -I "$D/slip_timeline.py" "$A" > "$O/slip-timeline.txt"
python3 -I "$D/check_soak_maap_restore.py" "$A" > "$O/soak-maap-restore-check.txt"
