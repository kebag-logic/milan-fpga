#!/usr/bin/env bash
set -uo pipefail
repo=$(cd "$1" && pwd)
packet=$(cd "$2" && pwd)
export TMPDIR="$packet/scratch/tmp"
export PYTHONDONTWRITEBYTECODE=1
mkdir -p "$TMPDIR"
case "$3" in
  focused) python3 "$packet/scripts/focused_controls.py" "$repo" "$packet/scratch/focused" "$packet/receipts/focused" ;;
  differential) cd "$repo"; python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep "$packet/scratch/differential" ;;
  *) exit 2 ;;
esac
