#!/bin/bash
# SPDX-License-Identifier: MIT
# usage: rv32_plants3.sh HEAD_TREE WORK OUT JOBS PLANT...
# For each registered plant (or "unplanted"): copies HEAD_TREE, applies the plant from tests/mutations.json,
# runs scripts/baremetal.py, then runs each smoke ELF directly under QEMU and records its exit code
# (the smoke exits with the number of the first failing check). HEAD_TREE is never modified.
set -u
src=$1; work=$2; out=$3; jobs=$4; shift 4
: > "$out"
for name in "$@"; do
  w=$work/$name; rm -rf "$w"; mkdir -p "$w"; cp -a "$src" "$w/tree"
  if [ "$name" != unplanted ]; then
    python3 -I - "$w/tree" "$name" <<'PY' || { echo "$name APPLY FAILED" >> "$out"; continue; }
import json, sys
from pathlib import Path
root, name = Path(sys.argv[1]), sys.argv[2]
p = {x['name']: x for x in json.loads((root / 'tests/mutations.json').read_text())}[name]
f = root / p['path']; t = f.read_text(); assert t.count(p['old']) == 1
f.write_text(t.replace(p['old'], p['new']))
PY
  fi
  (cd "$w/tree" && python3 scripts/baremetal.py --work "$w/rv32" --jobs "$jobs" > "$w/baremetal.log" 2>&1)
  line="$name baremetal_rc=$?"
  for kind in debug release; do
    elf=$w/rv32/$kind/rv32_smoke.elf
    if [ -f "$elf" ]; then
      timeout 60 qemu-system-riscv32 -machine virt -nographic -bios none -kernel "$elf" -no-reboot > /dev/null 2>&1
      line="$line $kind=$?"
    else
      line="$line $kind=no_elf"
    fi
  done
  echo "$line" >> "$out"
done
