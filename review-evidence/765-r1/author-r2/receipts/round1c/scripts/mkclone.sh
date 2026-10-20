#!/usr/bin/env bash
# Clean clone of the lane at a commit, with the four gate submodules from the lane's own modules.
set -euo pipefail
DEST=$1; COMMIT=$2; LANE=<lane>
git clone -q "$LANE" "$DEST"
git -C "$DEST" checkout -q "$COMMIT"
for m in third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack; do
  git -C "$DEST" config "submodule.$m.url" "$LANE/.git/modules/$m"
done
git -C "$DEST" -c protocol.file.allow=always submodule update --init -q \
  third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack
git -C "$DEST" submodule status
