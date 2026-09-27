#!/usr/bin/env bash
# Usage: gate.sh <name> <cmd...>
# Runs <cmd> in the current directory, stores combined output in
# receipts/<name>.log and appends "<name>\t<rc>\t<seconds>\t<cmd>" to receipts/gates.tsv.
PKT="$(cd "$(dirname "$0")/.." && pwd)"
name="$1"; shift
start=$(date +%s)
"$@" > "$PKT/receipts/$name.log" 2>&1
rc=$?
end=$(date +%s)
printf '%s\t%s\t%s\t%s\n' "$name" "$rc" "$((end-start))" "$*" >> "$PKT/receipts/gates.tsv"
echo "$name rc=$rc ($((end-start))s)"
exit 0
