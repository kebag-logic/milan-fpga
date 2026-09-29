#!/bin/sh
# Export the exact head (git archive, never the clone) and run the focused suite.
set -u
. "$(dirname "$0")/00_env.sh"
H="$PKT/scratch/head"; R="$PKT/receipts"
rm -rf "$H"; mkdir -p "$H" "$R"
git -C "$CLONE" archive "$HEAD_SHA" | tar -x -C "$H"
{ "$VLT" --version; } > "$R/verilator-version.txt" 2>&1
make -C "$H/tb/maap" VERILATOR="$VLT" run > "$R/head-tb-maap.log" 2>&1
echo "tb/maap rc=$? $(grep -E '^[0-9]+ checks:' "$R/head-tb-maap.log")" | tee "$R/head-suites.txt"
