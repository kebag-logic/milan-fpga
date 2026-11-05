#!/usr/bin/env bash
# A fresh --shared clone of the lane at <head>, its submodules at that commit's gitlinks,
# objects taken from the lane's own submodule clones. Usage: clone_at.sh <head> <dir>
set -eu
head=$1; dir=$2; lane=$LANES/840-identity-link
test ! -e "$dir"
git clone -q --shared --no-checkout "$lane" "$dir"
git -C "$dir" -c advice.detachedHead=false checkout -q --detach "$head"
git -C "$dir" remote set-url origin https://github.com/kebag-logic/milan-fpga.git
for d in third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP; do
  git -C "$dir" config "submodule.$d.url" "$lane/$d"
done
git -C "$dir" -c protocol.file.allow=always submodule update -q --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP
test "$(git -C "$dir" rev-parse HEAD)" = "$head"
test -z "$(git -C "$dir" status --porcelain)"
git -C "$dir" submodule status
