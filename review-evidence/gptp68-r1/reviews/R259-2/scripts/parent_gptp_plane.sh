#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Focused parent consumer probe: the parent's tb/verilator/gptp_plane suite at
# a parent revision, with gptp-processor populated by the exact donor tree of
# a given donor revision (the parent gitlink content, not a checkout). Only
# the files the suite reads are fetched, each verified against the blob id
# the parent tree records. Usage: parent_gptp_plane.sh <parent-rev> <donor-rev>
set -eu
. "$(dirname "$0")/env.sh"
prev=$1; drev=$2
w="$SCRATCH/parent_plane_${prev%${prev#????????}}_${drev%${drev#????????}}"
rm -rf "$w"; mkdir -p "$w/gptp-processor"
gh api "repos/kebag-logic/milan-fpga/git/trees/$prev?recursive=1" \
  --jq '.tree[] | select(.type=="blob") | select(.path|test("^tb/verilator/gptp_plane/|^tb/common/(verilator_harness|gptp_tx_flags)\\.hpp$|^hdl/ieee8021as/ptp_timestamp/timestamp_counter\\.sv$")) | .sha + " " + .path' > "$w/inputs.txt"
while read -r sha path; do
  mkdir -p "$w/$(dirname "$path")"
  gh api "repos/kebag-logic/milan-fpga/git/blobs/$sha" --jq .content | base64 -d > "$w/$path"
  test "$(git hash-object "$w/$path")" = "$sha"
done < "$w/inputs.txt"
git -C "$CLONE" archive "$drev" | tar -x -C "$w/gptp-processor"
echo "# parent $prev, $(wc -l < "$w/inputs.txt") input blobs verified; gptp-processor = donor $drev tree $(git -C "$CLONE" rev-parse "$drev^{tree}")"
echo "# verilator: $(verilator --version)"
cd "$w/tb/verilator/gptp_plane"
rc=0
make run VFLAGS="--cc --exe --build -j 8 --top-module gptp_plane_wrap -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -GUCODE_HEX_P='\"gptp_ucode.hex\"' -GCLK_HZ_P=2000000 -CFLAGS \"-std=c++17 -O2 -I$w/tb/verilator/gptp_plane -Wall -Wextra\"" > "$w/make.log" 2>&1 || rc=$?
grep -vE '^%Warning|^ +[0-9]+ \||^ +\||^ +\.\.\.|^ +\^|Location of port|For warning|lint_off|^- V e r i|^- Verilator|make\[1\]|^verilator |^g\+\+|^ccache|^echo|^rm -f|^ar |^Archive' "$w/make.log" | sed "s|$w|<probe>|g"
echo "# make exit status: $rc"
exit "$rc"
