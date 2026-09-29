#!/bin/sh
# Build one scratch parent: a clone of the read-only parent checkout at a given
# dev commit, gptp-processor and third_party/verilog-axis at their gitlinks
# from the pin lane (the recipe of processor #131, 5868716919), and
# protocol-processor cloned from the processor lane at a given commit, with the
# gitlink staged. Nothing is committed; `external` is not fetched.
# Usage: mk_parent.sh <dest> <parent checkout> <parent rev> <processor lane> <processor rev> <pin lane>
set -eu
DEST=$1 PARENT=$2 PREV=$3 PP=$4 PPREV=$5 PIN=$6
rm -rf "$DEST"
git clone -q --no-checkout "$PARENT" "$DEST"
cd "$DEST"
git checkout -q --detach "$PREV"
git config submodule.gptp-processor.url "$PIN/gptp-processor"
git config submodule.third_party/verilog-axis.url "$PIN/third_party/verilog-axis"
git config submodule.protocol-processor.url "$PP"
git -c protocol.file.allow=always submodule -q update --init gptp-processor third_party/verilog-axis protocol-processor
git -C protocol-processor checkout -q --detach "$PPREV"
git add protocol-processor
echo "scratch parent $(git rev-parse HEAD) processor $(git -C protocol-processor rev-parse HEAD)"
git submodule status gptp-processor third_party/verilog-axis protocol-processor
