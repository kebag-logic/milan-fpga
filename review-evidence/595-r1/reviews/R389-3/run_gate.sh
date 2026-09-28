#!/usr/bin/env bash
# Usage: run_gate.sh <name> <cwd> <cmd...>
# Runs one gate, writing receipts/<name>.log and appending a line to receipts/gates.tsv:
# name  rc  seconds  head  cwd-label  log-sha256  argv
set -u
PKT="$(cd "$(dirname "$0")" && pwd)"
name="$1"; cwd="$2"; shift 2
log="$PKT/receipts/$name.log"
head="$(git -C "$cwd" rev-parse HEAD 2>/dev/null)"
start=$(date +%s.%N)
( cd "$cwd" && "$@" ) > "$log" 2>&1
rc=$?
end=$(date +%s.%N)
secs=$(python3 -c "print(round($end-$start,2))")
sha=$(sha256sum "$log" | cut -d' ' -f1)
label="$(basename "$cwd")"
printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$name" "$rc" "$secs" "$head" "$label" "$sha" "$*" >> "$PKT/receipts/gates.tsv"
echo "$name rc=$rc ${secs}s"
exit $rc
