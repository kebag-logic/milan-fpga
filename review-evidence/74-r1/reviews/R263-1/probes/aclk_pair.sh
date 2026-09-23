#!/bin/bash
# Build and run tb/verilator/milan_dp `aclk` on two full trees (head RTL and
# base RTL, everything else identical), 4 Verilator jobs each, then diff the
# two run logs.   aclk_pair.sh <head_root> <base_root> <out_dir>
set -u
H=$(cd "$1" && pwd); B=$(cd "$2" && pwd); mkdir -p "$3"; OUT=$(cd "$3" && pwd)
V=${VERILATOR:-verilator}
mkdir -p "$OUT"
run() {
  local root=$1 tag=$2
  ( cd "$root/tb/verilator/milan_dp" &&
    make aclk VERILATOR="$V" VERILATOR_JOBS=4 > "$OUT/aclk_$tag.full.log" 2>&1
    echo "make exit $?" >> "$OUT/aclk_$tag.full.log" )
}
start=$(date +%s)
run "$H" head &
run "$B" base &
wait
echo "elapsed $(( $(date +%s) - start )) s"
for t in head base; do
  # the run log proper: from the first harness line on (the build noise differs by path only)
  awk '/^== |^\[|^  \[|checks|RESULT|MEASURED|A_MCSRV|SLIP_|TDM junction|make exit/' "$OUT/aclk_$t.full.log" > "$OUT/aclk_$t.run.log"
  tail -n 4 "$OUT/aclk_$t.full.log"
done
if cmp -s "$OUT/aclk_head.run.log" "$OUT/aclk_base.run.log"; then
  echo "ACLK run logs byte-identical ($(wc -l < "$OUT/aclk_head.run.log") lines)"
else
  echo "ACLK run logs DIFFER"; diff "$OUT/aclk_base.run.log" "$OUT/aclk_head.run.log" | head -40
fi
