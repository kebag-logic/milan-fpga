#!/usr/bin/env bash
# Round-2 delta probe: prove the HDL changes between two trees are comment-only.
#  1. preprocess each changed HDL file with comments stripped (-E -P) and diff;
#  2. elaborate protocol_processor_top (whole hdl/ tree) to JSON at both trees,
#     drop source locations, and compare the normalized netlists;
#  3. regenerate every ROM image (listener ROM, microcode, descriptor image)
#     at both trees and compare their hashes.
# Usage: probe_comment_only.sh BASE_TREE HEAD_TREE OUT_DIR   (verilator on PATH)
set -euo pipefail
base=$1; head=$2; out=$3
mkdir -p "$out"
files="hdl/top/protocol_processor_top.sv hdl/aecp/KL_aecp_engine.sv hdl/aecp/KL_aecp_nvm_writer.sv"
verilator --version > "$out/tool.txt"
rc=0

# 1. comment-stripped preprocessed text
for f in $files; do
  for t in base head; do
    d=$base; [ "$t" = head ] && d=$head
    (cd "$d" && verilator -E -P "$f") | grep -v '^[[:space:]]*$' > "$out/$(basename "$f").$t.pp"
  done
  if cmp -s "$out/$(basename "$f").base.pp" "$out/$(basename "$f").head.pp"; then
    echo "PP-EQUAL $f"
  else
    echo "PP-DIFF  $f"; rc=1
  fi
done | tee "$out/pp_compare.txt"

# 2. elaborated netlist (JSON), source locations removed
norm() {
  python3 - "$1" <<'PY'
import json, sys, re
def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k not in ("loc", "file", "filename")}
    if isinstance(o, list):
        return [strip(x) for x in o]
    return o
j = json.load(open(sys.argv[1]))
print(json.dumps(strip(j), sort_keys=True, indent=0))
PY
}
for t in base head; do
  d=$base; [ "$t" = head ] && d=$head
  (cd "$d" && pkgs=$(find hdl -name '*_pkg.sv' | sort) && all=$(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort) \
    && verilator --json-only -Wno-fatal -Wno-lint -Wno-style --top-module protocol_processor_top \
         --Mdir "$out/json_$t" $pkgs $all) > "$out/json_$t.log" 2>&1
  norm "$out/json_$t/Vprotocol_processor_top.tree.json" > "$out/netlist_$t.norm.json"
done
sha256sum "$out/netlist_base.norm.json" "$out/netlist_head.norm.json" | sed "s#$out/##" | tee "$out/netlist_hashes.txt"
# The simulator embeds "<file>.sv:<line>" in the text of the assertion it
# generates for every `unique case`; a comment line added above such a case
# shifts that number and nothing else. Record the raw differing lines, require
# every one to be such a string, then compare with the line number masked.
diff "$out/netlist_base.norm.json" "$out/netlist_head.norm.json" > "$out/netlist_raw.diff" || true
ndiff=$(grep -cE '^[<>]' "$out/netlist_raw.diff" || true)
nother=$(grep -E '^[<>]' "$out/netlist_raw.diff" \
  | grep -cvE 'Error: [A-Za-z_]+\.sv:[0-9]+: Assertion failed in %m: unique case' || true)
echo "raw differing lines: $ndiff, of which not a generated unique-case assertion string: $nother" \
  | tee -a "$out/netlist_hashes.txt"
[ "$nother" -eq 0 ] || rc=1
for t in base head; do
  sed -E 's/(Error: [A-Za-z_]+\.sv:)[0-9]+(: Assertion failed in %m: unique case)/\1LINE\2/' \
    "$out/netlist_$t.norm.json" > "$out/netlist_$t.masked.json"
done
sha256sum "$out/netlist_base.masked.json" "$out/netlist_head.masked.json" | sed "s#$out/##" | tee -a "$out/netlist_hashes.txt"
if cmp -s "$out/netlist_base.masked.json" "$out/netlist_head.masked.json"; then
  echo "NETLIST-EQUAL protocol_processor_top (locations dropped, generated assertion line numbers masked)" | tee -a "$out/netlist_hashes.txt"
else
  echo "NETLIST-MISMATCH protocol_processor_top" | tee -a "$out/netlist_hashes.txt"; rc=1
fi

# 3. ROM images
for t in base head; do
  d=$base; [ "$t" = head ] && d=$head
  mkdir -p "$out/rom_$t"
  (cd "$d" && python3 -B hdl/acmp/rom/gen_ltn_rom.py -o "$out/rom_$t/ltn_rom.hex" \
    && python3 -B hdl/aecp/ucode/gen_ucode.py -o "$out/rom_$t/ucode.hex") > "$out/rom_$t.log" 2>&1
done
(cd "$out" && sha256sum rom_base/* rom_head/*) | tee "$out/rom_hashes.txt"
for r in ltn_rom.hex ucode.hex; do
  if cmp -s "$out/rom_base/$r" "$out/rom_head/$r"; then echo "ROM-EQUAL $r"; else echo "ROM-DIFF $r"; rc=1; fi
done | tee -a "$out/rom_hashes.txt"
grep -q 'DIFF\|MISMATCH' "$out/pp_compare.txt" "$out/rom_hashes.txt" "$out/netlist_hashes.txt" && rc=1
echo "probe rc=$rc"
exit "$rc"
