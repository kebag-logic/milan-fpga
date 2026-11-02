#!/bin/sh
# Disposable probes on an exported copy of the head: the clean copy must check fresh; re-planting a vanished
# D0-001/D0-033 spelling must make --check fail and bring the row (and the page's stale status) back after --write.
set -u
SRC=$1; WORK=$2
run() { name=$1; shift
  rm -rf "$WORK/$name"; mkdir -p "$WORK/$name"; git -C "$SRC" archive HEAD | tar -x -C "$WORK/$name"
  "$@" "$WORK/$name"
  (cd "$WORK/$name" && python3 -I scripts/docs_inventory.py --check >/dev/null 2>&1; echo "$name: --check rc=$?")
  (cd "$WORK/$name" && python3 -I scripts/docs_inventory.py --write >/dev/null 2>&1 && python3 -I scripts/docs_inventory.py --check >/dev/null 2>&1; echo "$name: --write then --check rc=$?")
  grep -E '^\| D0-00(1|33) ' "$WORK/$name/docs/DOCUMENTATION_AUDIT.md" | cut -d'|' -f2-4 | sed "s/^/$name row:/"
  grep -E '^\| \[(README.md|docs/fpga/DATAPLANE_WALKTHROUGH.md)\]' "$WORK/$name/docs/DOCUMENTATION_AUDIT.md" | awk -F' [|] ' -v n="$name" '{print n" status: "$1" "$6" "$7}'
}
clean() { :; }
readme_back() { printf '\nADP, ACMP, AECP, MAAP and SRP default to bare-metal firmware.\n' >> "$1/README.md"; }
d033_copy() { printf '\nIts default is _bare-metal_ control; all-fabric remains supported\n' >> "$1/docs/fpga/DATAPLANE_WALKTHROUGH.md"; }
run clean clean
run readme_back readme_back
run d033_copy d033_copy
