#!/usr/bin/env bash
# Run R449-2's census_probe.sh forms (unchanged, via census_batch_one.sh) at
# this head, 4 at a time. PACKET is a staging dir whose scripts/ is the
# verbatim round-2 copy and whose scratch/head-tree is a real head export.
P="${PACKET_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
export PACKET=$P/scratch/r449pk
xargs -P 4 -L 1 "$PACKET/scripts/census_batch_one.sh" < "$P/receipts/r449_census_cases.txt"
