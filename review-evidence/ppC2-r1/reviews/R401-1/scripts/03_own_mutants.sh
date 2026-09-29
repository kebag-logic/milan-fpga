#!/bin/sh
# Reviewer-owned mutants against the Release! fix (KL_pp_maap.sv W_ADDR exit).
# Each patch is planted in a scratch copy of the head export; the unmodified
# tb/maap suite must finish red with a named U17b failure.
set -u
. "$(dirname "$0")/00_env.sh"
S="$PKT/scratch/head"
R="$PKT/receipts/own-mutants"
mkdir -p "$R"; : > "$R/summary.txt"
for p in "$PKT"/scripts/mutations/*.patch; do
  m=$(basename "$p" .patch)
  T="$PKT/scratch/mut/$m"
  rm -rf "$T"; mkdir -p "$T/tb"
  cp -r "$S/hdl" "$T/hdl"; cp -r "$S/tb/maap" "$S/tb/common" "$T/tb/"
  rm -rf "$T/tb/maap/obj_dir"
  (cd "$T" && git apply "$p") || { echo "$m APPLY-FAILED" >> "$R/summary.txt"; continue; }
  make -C "$T/tb/maap" VERILATOR="$VLT" run > "$R/$m.log" 2>&1
  rc=$?
  tally=$(grep -E '^[0-9]+ checks:' "$R/$m.log" | tail -1)
  named=$(grep -c '^FAIL: U17b:' "$R/$m.log")
  if [ "$rc" -ne 0 ] && [ -n "$tally" ] && [ "$named" -gt 0 ]; then v=KILLED; else v=UNPROVEN; fi
  echo "$m rc=$rc tally=[$tally] U17b-fails=$named $v" >> "$R/summary.txt"
  grep '^FAIL:' "$R/$m.log" | head -6 | sed 's/^/    /' >> "$R/summary.txt"
done
cat "$R/summary.txt"
