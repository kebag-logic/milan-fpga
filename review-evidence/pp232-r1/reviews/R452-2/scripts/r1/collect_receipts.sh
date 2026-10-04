#!/usr/bin/env bash
# Copy the review's raw run outputs from scratch/ into receipts/, replacing
# local absolute paths with neutral placeholders, then write MANIFEST.sha256.
# Usage: collect_receipts.sh PACKET CLONE
set -euo pipefail
pk=$1; clone=$2
s=$pk/scratch; r=$pk/receipts
rm -rf "$r"; mkdir -p "$r/runs" "$r/probe" "$r/yosys" "$r/campaigns"
clean() {  # src dst
  sed -e "s#$pk#\$PACKET#g" -e "s#$clone#\$CLONE#g" -e "s#$HOME#\$HOME#g" "$1" >"$2"
}
for f in "$s"/runs/*.log "$s"/runs/*.rc "$s"/runs/*-compare.txt; do
  case "$(basename "$f")" in ls-smoke.log) continue ;; esac
  clean "$f" "$r/runs/$(basename "$f")"
done
for f in "$s"/probe/*.log; do clean "$f" "$r/probe/$(basename "$f")"; done
for f in "$s"/clearprobe/*.log; do clean "$f" "$r/probe/clearprobe-$(basename "$f")"; done
for k in head main; do
  clean "$s/yosys-$k/stat.txt" "$r/yosys/$k-stat.txt"
done
for c in notify d3 acmp; do
  [ -f "$s/out-$c/results.json" ] && clean "$s/out-$c/results.json" "$r/campaigns/$c-results.json"
done
cd "$pk"
find receipts scripts -type f ! -name '*.pyc' | LC_ALL=C sort | xargs sha256sum >MANIFEST.sha256
echo "manifest: $(wc -l <MANIFEST.sha256) files"
