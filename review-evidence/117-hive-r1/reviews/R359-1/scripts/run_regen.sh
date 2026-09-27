#!/bin/sh
# Regenerate the shipping 1x1 TDM8 AEM image from the product-image commit and
# check the published packet against it (reviewer R359-1, issue 117 / PR 598).
#
# usage: run_regen.sh <milan-fpga clone> <work dir> <published packet author dir>
# The clone must contain commit 9e9954e9 and initialised protocol-processor and
# gptp-processor submodules at the gitlinks that commit records. Nothing in the
# clone is written; the source is exported into <work dir>/tree.
set -eu
mkdir -p "$2"
repo=$(cd "$1" && pwd) work=$(cd "$2" && pwd) pkt=$(cd "$3" && pwd)
img=9e9954e96bf55181edb9949ae94c9abd4ab6aaf5
here=$(cd "$(dirname "$0")" && pwd)
rm -rf "$work/tree" "$work/bout" && mkdir -p "$work/tree"
git -C "$repo" archive "$img" | tar -x -C "$work/tree"
for sm in protocol-processor gptp-processor; do
    want=$(git -C "$repo" ls-tree "$img" "$sm" | awk '{print $3}')
    git -C "$repo/$sm" archive "$want" | tar -x -C "$work/tree/$sm"
    echo "submodule $sm $want"
done
cd "$work/tree"
python3 sw/builder/endstation_builder.py configs/endstation_ax7101_1x1_tdm8.yaml -o ../bout | head -1
python3 avdecc/gen_aemi_image.py --overlay ../bout/endstation_ax7101_1x1_tdm8/aem_overlay.json \
    -o ../aem_desc.bin -m ../aem_desc.map > /dev/null
sha256sum ../aem_desc.bin
python3 "$here/verify_packet.py" "$pkt" ../aem_desc.bin ../aem_desc.map
