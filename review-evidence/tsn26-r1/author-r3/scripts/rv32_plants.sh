#!/bin/bash
# usage: rv32_plants.sh TREE WORK OUT PLANT...
# Applies each registered plant to a disposable copy of TREE, runs scripts/baremetal.py on it, then runs the
# Debug and Release smoke ELFs under QEMU and records each exit code. TREE itself is never modified.
set -u
src=$1; work=$2; out=$3; shift 3
: > "$out"
for name in unplanted "$@"; do
  w=$work/$name; rm -rf "$w"; mkdir -p "$w"; cp -a "$src" "$w/tree"
  if [ "$name" != unplanted ]; then
    python3 -I - "$w/tree" "$name" <<'PY'
import json, sys
from pathlib import Path
root, name = Path(sys.argv[1]), sys.argv[2]
p = {x['name']: x for x in json.loads((root / 'tests/mutations.json').read_text())}[name]
f = root / p['path']; t = f.read_text(); assert t.count(p['old']) == 1
f.write_text(t.replace(p['old'], p['new']))
PY
  fi
  (cd "$w/tree" && python3 scripts/baremetal.py --work "$w/rv32" --jobs 8 > "$w/baremetal.log" 2>&1; echo "$name baremetal_rc=$?" >> "$out")
  for kind in debug release; do
    elf=$w/rv32/$kind/rv32_smoke.elf
    if [ -f "$elf" ]; then
      timeout 60 qemu-system-riscv32 -machine virt -nographic -bios none -kernel "$elf" -no-reboot > /dev/null 2>&1
      echo "$name $kind qemu_rc=$?" >> "$out"
    else
      echo "$name $kind no_elf" >> "$out"
    fi
  done
done
