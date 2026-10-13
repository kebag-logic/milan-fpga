#!/usr/bin/env bash
# Scratch: a clean clone of the lane at its HEAD, its five submodules from the lane's own checkouts, then the
# lane's uncommitted diff applied (empty once committed).
# usage: mkclone.sh <directory>
set -euo pipefail
lane=$LANES/697-consume
dir=$1
rm -rf "$dir"
git clone -q "$lane" "$dir"
cd "$dir"
for sub in third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack; do
  git config "submodule.$sub.url" "$lane/$sub"
done
git -c protocol.file.allow=always submodule update -q --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
git -C "$lane" diff --binary > "$dir.diff"
if [ -s "$dir.diff" ]; then git apply "$dir.diff"; fi
git log --oneline -1
git status --short | head -20
