#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Focused parent consumer probe: the parent's tb/verilator/gptp_shadow `run`
# target (real KL_gptp_txret) at a parent revision, gptp-processor populated
# by the exact tree of a donor revision, verilog-axis axis_fifo.v at the
# parent's pin. Every fetched file is verified against the blob id its tree
# records. An optional patch (a prior review's or the author's public probe)
# is applied to the harness copy. Build parallelism is capped at 8.
# Usage: parent_shadow_probe.sh <parent-rev> <donor-rev> [patch]
set -eu
. "$(dirname "$0")/env.sh"
prev=$1; drev=$2; patch=${3:-}
if [ -n "$patch" ]; then patch=$(cd "$(dirname "$patch")" && pwd)/$(basename "$patch"); fi
tag=$(basename "${patch:-none}" .patch)
w="$SCRATCH/parent_shadow_$(echo "$drev" | cut -c1-7)_$tag"
rm -rf "$w"; mkdir -p "$w/gptp-processor" "$w/third_party/verilog-axis/rtl"
gh api "repos/kebag-logic/milan-fpga/git/trees/$prev?recursive=1" \
  --jq '.tree[] | select(.type=="blob") | select(.path|test("^tb/verilator/gptp_shadow/(Makefile|gptp_shadow_wrap\\.sv|sim_main\\.cpp)$|^tb/common/(verilator_harness|gptp_tx_flags)\\.hpp$|^hdl/ieee8021as/ptp_timestamp/(timestamp_counter|KL_ptp_clock_validity)\\.sv$|^hdl/ieee8021as/gptp_plane/KL_gptp_(txticket|txret|gmii_launch|shadow)\\.sv$|^hdl/common/(KL_link_guard|cdc_pulse|cdc_handshake)\\.sv$")) | .sha + " " + .path' > "$w/inputs.txt"
axis=$(gh api "repos/kebag-logic/milan-fpga/git/trees/$prev?recursive=1" --jq '.tree[] | select(.path=="third_party/verilog-axis") | .sha')
asha=$(gh api "repos/alexforencich/verilog-axis/git/trees/$axis?recursive=1" --jq '.tree[] | select(.path=="rtl/axis_fifo.v") | .sha')
echo "$asha third_party/verilog-axis/rtl/axis_fifo.v" >> "$w/inputs.txt"
while read -r sha path; do
  mkdir -p "$w/$(dirname "$path")"
  case $path in
    third_party/*) gh api "repos/alexforencich/verilog-axis/git/blobs/$sha" --jq .content | base64 -d > "$w/$path" ;;
    *) gh api "repos/kebag-logic/milan-fpga/git/blobs/$sha" --jq .content | base64 -d > "$w/$path" ;;
  esac
  test "$(git hash-object "$w/$path")" = "$sha"
done < "$w/inputs.txt"
git -C "$CLONE" archive "$drev" | tar -x -C "$w/gptp-processor"
echo "# parent $prev ($(wc -l < "$w/inputs.txt") input blobs verified, verilog-axis $axis); gptp-processor = donor $drev tree $(git -C "$CLONE" rev-parse "$drev^{tree}"); probe: $(basename "${patch:-none}")"
if [ -n "$patch" ]; then
  (cd "$w" && patch -p1 -s < "$patch")
fi
echo "# verilator: $(verilator --version)"
cd "$w/tb/verilator/gptp_shadow"
rc=0
make run > "$w/make.log" 2>"$w/probe.log" || rc=$?
grep -E 'checks:|^FAIL|Error' "$w/make.log" | sed "s|$w|<probe>|g" | head -20 || true
if grep -q '^WEDGE' "$w/probe.log"; then
  n=$(grep -c '^WEDGE k=' "$w/probe.log")
  echo "# probe pairs: $n"
  grep '^WEDGE k=' "$w/probe.log" | awk '
    { for (i = 1; i <= NF; i++) { split($i, kv, "="); v[kv[1]] = kv[2] }
      a = v["adj"] + 0; if (a < 0) a = -a; if (a > amax) amax = a
      if (v["flags"] != 13) bad++
      last = $0 }
    END { printf "# max |adj| %d (envelope 1677722); pairs with flags other than 13: %d\n# last: %s\n", amax, bad, last }'
  grep '^WEDGE k=' "$w/probe.log" | sed -n '1,3p;58,60p'
fi
echo "# make exit status: $rc"
exit "$rc"
