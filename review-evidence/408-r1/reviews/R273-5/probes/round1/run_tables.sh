#!/usr/bin/env bash
# Connected mutation-table audits: base with the SDK and absent, head absent
# (head with the SDK is 30-disconnect/connected-sdk). Usage: run_tables.sh <packet> <sdk>
set -u
packet=$1
sdk=$2
out=$packet/receipts/31-tables
mkdir -p "$out"
run() {  # name side mode
  local name=$1 side=$2 mode=$3 flags=()
  if [ "$mode" = sdk ]; then flags=(--sdk "$sdk"); else flags=(--absent); fi
  (
    cd "$packet/scratch/$side" || exit 2
    python3 -B "$packet/scripts/probe.py" --checkout . "${flags[@]}" \
      --mutation-audit --out "$out/$name.json" > "$out/$name.txt" 2>&1
    echo "exit=$?" >> "$out/$name.txt"
  ) &
}
run base-sdk base sdk
run base-absent base absent
run head-absent head absent
wait
tail -n 2 "$out"/*.txt
