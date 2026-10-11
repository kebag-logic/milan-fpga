#!/usr/bin/env bash
# Run the srp_latency arm (IF=1 and IF=2) for each probe: name checkout lwSRP-checkout.
P=${R597_PACKET:-$(cd "$(dirname "$0")/.." && pwd)}; S=$P/scratch; . $P/scripts/r597_env.sh
out=$P/receipts/walk
while read -r name tree lw; do
  rm -rf "$S/wb/$name"; mkdir -p "$S/wb/$name"
  python3 -B $P/scripts/r597_latency_arm.py "$S/$tree" "$S/wb/$name" "$S/$lw" > "$out/$name.log" 2>&1
  echo "$name rc=$?" >> "$out/summary.txt"
done <<LIST
exact-head-newpin r597-1-711-exact lw-new
newwalk-oldpin w-newwalk-pinold lw-old
base-oldwalk-oldpin base-full lw-old
oldwalk-assert-newpin walk-oldwalk lw-new
oldwalk-assert-oldpin w-oldwalk-pinold lw-old
oldwalk-noassert-newpin w-noassert-new lw-new
mut-vecsize-newpin w-vecsize lw-new
mut-noendskip-newpin w-noendskip lw-new
LIST
echo done >> "$out/summary.txt"
