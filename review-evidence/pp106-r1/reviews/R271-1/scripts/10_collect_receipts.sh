#!/usr/bin/env bash
# Collect publishable receipts from the disposable trees: per-mutant FAIL lines
# and the head/base suite logs, with host paths replaced by placeholders.
# Usage: 10_collect_receipts.sh <packet> <review-clone> <validation-storage>
set -uo pipefail
pk=$1; clone=$2; vs=$3; sc=$pk/scratch; out=$pk/receipts
scrub() { sed -e "s#$pk#\$PACKET#g" -e "s#$clone#\$CLONE#g" \
              -e "s#$vs#\$VALIDATION_STORAGE#g" -e "s#$HOME#\$WORKSPACE_HOME#g" \
              -e "s#/tmp/[A-Za-z0-9._/-]*#\$TMP#g"; }
{
  for d in "$sc"/mut-R* "$sc"/plant-X* "$sc"/oldtb-*; do
    [ -d "$d" ] || continue
    echo "== $(basename "$d")"
    for l in "$d"/*.log "$d"/logs/*.log; do
      [ -f "$l" ] || continue
      t=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$l" | tail -1)
      echo "  $(basename "$l" .log): ${t:-NO TALLY}"
      grep -E '^FAIL:' "$l" | sed 's/^/    /'
    done
  done
} | scrub > "$out/03_mutants_detail.txt"
mkdir -p "$out/logs"
for s in srp_decoder srp_encoder srp_stream_fsms srp_top; do
  scrub < "$out/head_suites/$s.log" > "$out/logs/head_$s.log"
  scrub < "$out/base_suites/$s.log" > "$out/logs/base_$s.log"
done
scrub < "$sc/probe-head/probe_srp_decoder.log" > "$out/logs/probe_head_srp_decoder.log"
scrub < "$sc/mut-R1/probe_srp_decoder.log" > "$out/logs/probe_R1_srp_decoder.log"
scrub < "$sc/mut-R8/probe_srp_decoder.log" > "$out/logs/probe_R8_srp_decoder.log"
