#!/usr/bin/env bash
# Run census_extra.sh over every case in receipts/census_extra_cases.txt, 4 at a time.
P="${PACKET_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
xargs -P 4 -I{} "$P/scripts/census_extra.sh" "$P/scratch/head-tree" "$P/scratch/extra/{}" {} < "$P/receipts/census_extra_cases.txt"
