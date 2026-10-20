#!/usr/bin/env bash
# The bench's own GSI campaign at the extracted head, with its temporary
# trees under the packet scratch. usage: gsi_campaign.sh <tree> <out> <jobs>
set -uo pipefail
tree=$1; out=$2; jobs=$3
P="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$out" "$P/scratch/tmp"
export TMPDIR="$P/scratch/tmp"
s=$(date +%s)
python3 "$tree/tb/pp_top/gsi_mutants.py" --output "$out/out" \
  --verilator "$P/scratch/bin/verilator" --jobs "$jobs" > "$out/gsi.log" 2>&1
echo $? > "$out/gsi.rc"; echo $(( $(date +%s) - s )) > "$out/gsi.secs"
