#!/bin/sh
# Compare the CI command table's sha256 declarations for the resource-gate scripts
# with the files' content at each named commit. Usage: command_table_pins.sh <clone> <commit>...
set -u
cd "$1" || exit 2; shift
for c in "$@"; do
  for f in syn/ooc/pp_placement_selftest.py syn/ooc/pp_resource_gate_mutants.py syn/ooc/pp_resource_gate_selftest.py; do
    pin=$(git show "$c:ci/image/command-table.json" | python3 -I -c 'import json,sys; print(json.load(sys.stdin)["scripts"][sys.argv[1]]["sha256"])' "$f")
    act=$(git show "$c:$f" | sha256sum | cut -c1-64)
    [ "$pin" = "$act" ] && s=match || s=STALE
    echo "$c $f declared=$pin content=$act $s"
  done
done
