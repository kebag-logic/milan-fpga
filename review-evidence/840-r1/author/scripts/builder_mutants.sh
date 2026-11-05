#!/usr/bin/env bash
# Plant each builder-gate 28b defect into a scratch clone at <head>, run gate 28b
# alone, record its rc and the words it failed with, then restore the file.
# Usage: builder_mutants.sh <head> <scratch-clone> <out-dir>
set -u
head=$1; w=$2; out=$3
mkdir -p "$out"
cd "$w" || exit 2
test "$(git rev-parse HEAD)" = "$head" || exit 3
plant() {
  local name=$1 file=$2 old=$3 new=$4
  python3 - "$file" "$old" "$new" <<'PY'
import sys
from pathlib import Path
p, old, new = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
t = p.read_text()
assert t.count(old) == 1, ("anchor", old)
p.write_text(t.replace(old, new))
PY
  python3 sw/builder/test_builder.py --gates test_station_mac_ul_bit_warns > "$out/$name.log" 2>&1
  echo "$name rc=$? words: $(grep -m1 -o 'gate 28b[^\"]*' "$out/$name.log" | cut -c1-160)"
  git checkout -q -- "$file"
}
plant ul-bit-is-ig sw/builder/endstation_builder.py 'MAC48_UL_BIT = 1 << 41' 'MAC48_UL_BIT = 1 << 40'
plant always-warns sw/builder/endstation_builder.py '    if not _mac48(mac, "platform.mac_address") & MAC48_UL_BIT:
        return []' '    if False:
        return []'
plant warning-on-stdout sw/builder/endstation_builder.py '        print(f"[endstation_builder] WARNING: {warning}", file=sys.stderr)' '        print(f"[endstation_builder] NOTE: {warning}")'
plant warning-refuses sw/builder/endstation_builder.py '    for warning in r["warnings"]:' '    if r["warnings"]:
        sys.exit("CONFIG ERROR: " + r["warnings"][0])
    for warning in r["warnings"]:'
plant arty-keeps-old-mac configs/endstation_arty_4x4.yaml 'mac_address: "02:4b:4c:00:00:02"' 'mac_address: "02:00:00:00:00:02"'
git status --short > "$out/tree-after.txt"
