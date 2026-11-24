#!/bin/bash
# mkclone.sh NAME REV: a --shared clone of the lane at REV in r3/wt/NAME, its submodules from the lane's own
# checkouts (no network, the lane's config untouched). Prints the clone path.
set -euo pipefail
LANE=/data-2/milan/lanes/cicd-1
W=/data-2/milan/tmp/cicd-a839/r3/wt/$1
REV=$2
mkdir -p "$(dirname "$W")"
[ -e "$W" ] || git clone -q --shared --no-checkout "$LANE" "$W"
git -C "$W" fetch -q "$LANE" "$REV" 2>/dev/null || true
git -C "$W" -c advice.detachedHead=false checkout -q -f --detach "$REV"
for d in third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack; do
  git -C "$W" config "submodule.$d.url" "$LANE/$d"
done
git -C "$W" -c protocol.file.allow=always submodule update -q --init --force \
  third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack
# the receipts' source identity reads each dependency's origin: keep .gitmodules' own URL there
for d in third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack; do
  git -C "$W/$d" remote set-url origin "$(git -C "$W" config -f .gitmodules "submodule.$d.url")"
done
echo "$W $(git -C "$W" rev-parse HEAD)"
