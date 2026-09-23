#!/usr/bin/env bash
# rec.sh NAME CMD... : run CMD in the lane, keep its log and one exits.tsv row.
set -uo pipefail
OUT=$REVIEWS/437-a190-packet
LANE=$LANES/437-container-paragraph-scopes
name=$1; shift
start=$(date -u +%Y-%m-%dT%H:%M:%SZ)
head=$(git -C "$LANE" rev-parse HEAD)
(cd "$LANE" && "$@") > "$OUT/receipts/$name.log" 2>&1
rc=$?
printf '%s\t%s\t%s\t%s\t%s\n' "$name" "$rc" "$head" "$start" "$*" >> "$OUT/receipts/exits.tsv"
echo "[$rc] $name :: $(tail -1 "$OUT/receipts/$name.log" | cut -c1-150)"
