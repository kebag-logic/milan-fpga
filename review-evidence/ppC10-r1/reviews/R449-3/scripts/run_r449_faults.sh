#!/usr/bin/env bash
# Run R449-2's yosys_fault.sh (unchanged, via fault_batch_one.sh) over
# receipts/r449_fault_cases.txt, 4 at a time.
P="${PACKET_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
export PACKET=$P/scratch/r449pk
xargs -P 4 -L 1 "$PACKET/scripts/fault_batch_one.sh" < "$P/receipts/r449_fault_cases.txt"
