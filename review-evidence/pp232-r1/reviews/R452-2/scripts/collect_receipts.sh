#!/usr/bin/env bash
# Copy round 2's raw run outputs from scratch/ into receipts/, replacing local absolute
# paths with neutral placeholders, then write MANIFEST.sha256 (every file under
# receipts/ and scripts/, paths relative to the packet).
# Usage: collect_receipts.sh PACKET CLONE
set -euo pipefail
pk=$1; clone=$2
s=$pk/scratch; r=$pk/receipts
rm -rf "$r"; mkdir -p "$r/runs" "$r/probe" "$r/campaigns" "$r/parent"
clean() {  # src dst
  sed -e "s#$pk#\$PACKET#g" -e "s#$clone#\$CLONE#g" -e "s#$HOME#\$HOME#g" "$1" >"$2"
}
for f in "$s"/runs/*; do clean "$f" "$r/runs/$(basename "$f")"; done
for f in "$s"/clearprobe/*.log; do clean "$f" "$r/probe/clearprobe-$(basename "$f")"; done
clean "$s/r1-scripts.sha256" "$r/runs/r1-scripts.sha256"
clean "$s/out-notify/results.json" "$r/campaigns/notify-results.json"
for f in "$s"/out-notify/*.log; do [ -f "$f" ] && clean "$f" "$r/campaigns/notify-$(basename "$f")"; done
git -C "$s/parent" diff --cached -- scripts/xvlog.budget >"$r/parent/xvlog.budget.cumulative.diff"
cp "$s/parent/scripts/xvlog.budget" "$r/parent/xvlog.budget.after-four-patches"
cd "$pk"
find receipts scripts -type f ! -name '*.pyc' | LC_ALL=C sort | xargs sha256sum >MANIFEST.sha256
echo "manifest: $(wc -l <MANIFEST.sha256) files"
