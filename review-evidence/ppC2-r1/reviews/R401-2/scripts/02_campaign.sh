#!/bin/sh
# The PR's own MAAP mutation campaign on the head export. Its three controls are
# tb/maap run, tb/rx_validator run and tb/pp_top maap-internal, unmutated.
set -u
. "$(dirname "$0")/00_env.sh"
H="$PKT/scratch/head"; R="$PKT/receipts"
cd "$H" && python3 tb/maap/mutants.py --output "$R/head-mutants" > "$R/head-mutants.txt" 2>&1
echo "rc=$?" | tee -a "$R/head-mutants.txt"
