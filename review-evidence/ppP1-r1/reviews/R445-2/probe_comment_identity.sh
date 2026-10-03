#!/usr/bin/env bash
# R445-2 probe: the round-2 delta (BASE..HEAD) changes no HDL token, no ROM
# and no elaborated netlist. Portable: needs git, python3, jq, sha256sum and a
# Verilator 5.050 binary given as $VERILATOR (default: verilator on PATH).
# Usage: probe_comment_identity.sh <repo> <scratch-dir>
# Writes everything under <scratch-dir>; prints one verdict line per check.
set -euo pipefail
REPO=$1; SCR=$2
BASE=${BASE:-c066dd83a2004f9b3640a933860c4d9e677d017e}
HEAD_SHA=${HEAD_SHA:-5960d8fc7e4f6ef2d7551bb224154ef2c265d894}
V=${VERILATOR:-verilator}
TOP=protocol_processor_top
FILES="hdl/aecp/KL_aecp_engine.sv hdl/aecp/KL_aecp_nvm_writer.sv hdl/top/protocol_processor_top.sv"
rm -rf "$SCR"; mkdir -p "$SCR"

extract() {  # <rev> <dir>
  mkdir -p "$2"; git -C "$REPO" archive "$1" | tar -x -C "$2"
}
roms() {  # <tree> <out-dir>: regenerate every ROM/image from its generator
  local t=$1 o=$2; mkdir -p "$o"
  python3 -B "$t/hdl/aecp/ucode/gen_ucode.py" -o "$o/ucode.hex" >/dev/null
  python3 -B "$t/hdl/acmp/rom/gen_ltn_rom.py" -o "$o/ltn_rom.hex" >/dev/null
  python3 -B "$t/hdl/aecp/desc/gen_desc_image.py" --no-lint \
    -i "$t/hdl/aecp/desc/example_milan_8.json" -o "$o/example_milan_8.bin" -m "$o/example_milan_8.map" >/dev/null
  python3 -B "$t/hdl/aecp/desc/gen_desc_image.py" \
    -i "$t/hdl/aecp/desc/milan_min.json" -o "$o/milan_min.bin" -m "$o/milan_min.map" >/dev/null
  ( cd "$o" && sha256sum ucode.hex ltn_rom.hex example_milan_8.bin example_milan_8.map milan_min.bin milan_min.map )
}
tokens() {  # <tree> <out>: comment-free, line-directive-free, whitespace-normalised token stream
  local t=$1 o=$2; : > "$o"
  for f in $FILES; do
    echo "=== $f" >> "$o"
    "$V" -E -P "$t/$f" | tr -s ' \t' ' ' | sed -e 's/^ //' -e 's/ $//' | grep -v '^$' >> "$o"
  done
}
netlist() {  # <tree> <out>: elaborated top as Verilator JSON, locations stripped
  local t=$1 o=$2 od; od=$(dirname "$o")/obj_$(basename "$o" .json)
  ( cd "$t" && pkgs=$(find hdl -name '*_pkg.sv' | sort) && all=$(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort) &&
    # shellcheck disable=SC2086
    "$V" --json-only -Wno-fatal -Wno-lint -Wno-style --top-module "$TOP" --Mdir "$od" $pkgs $all >/dev/null 2>"$od.log" )
  # Locations are stripped, and so are the source line numbers Verilator bakes
  # into its own generated assertion text ("<file>.sv:<line>: Assertion
  # failed"): a comment that adds a line shifts them without changing logic.
  jq -S 'del(.. | .loc?, .file?) | walk(if type=="object" then del(.fileline?) else . end)
         | walk(if type=="string" then gsub("(?<f>[A-Za-z0-9_]+\\.sv):[0-9]+"; "\(.f):N") else . end)' \
    "$od"/V"$TOP".tree.json > "$o"
  jq -r '[..|strings|select(test("[A-Za-z0-9_]+\\.sv:N"))]|length' "$o" > "$o.linerefs"
}
compare() {  # <label> <a> <b>
  if cmp -s "$2" "$3"; then echo "IDENTICAL $1 ($(sha256sum < "$2" | cut -c1-16))"
  else echo "DIFFERENT $1"; diff "$2" "$3" > "$2.diff" || true; head -20 "$2.diff"; fi
}

extract "$BASE" "$SCR/base"; extract "$HEAD_SHA" "$SCR/head"
roms "$SCR/base" "$SCR/rom_base" > "$SCR/rom_base.sha256"
roms "$SCR/head" "$SCR/rom_head" > "$SCR/rom_head.sha256"
cat "$SCR/rom_head.sha256"
compare roms "$SCR/rom_base.sha256" "$SCR/rom_head.sha256"
tokens "$SCR/base" "$SCR/tok_base.txt"; tokens "$SCR/head" "$SCR/tok_head.txt"
compare tokens "$SCR/tok_base.txt" "$SCR/tok_head.txt"
netlist "$SCR/base" "$SCR/net_base.json"; netlist "$SCR/head" "$SCR/net_head.json"
echo "netlist nodes: $(jq '[..|objects|select(.type?)]|length' "$SCR/net_head.json"), normalised line refs: $(cat "$SCR/net_head.json.linerefs")"
compare netlist "$SCR/net_base.json" "$SCR/net_head.json"

# Control: the same comparisons must see a one-token change (a constant
# changed in the writer's code, not in a comment), else they prove nothing.
cp -a "$SCR/head" "$SCR/ctl"
python3 - "$SCR/ctl/hdl/aecp/KL_aecp_nvm_writer.sv" <<'PY'
import re, sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
m = re.search(r"^(?!\s*//)(.*?)\b1'b1\b", s, re.M)
assert m, "no 1'b1 on a code line"
i = m.end() - 1
open(p, "w", encoding="utf-8").write(s[:i] + "0" + s[i+1:])
print("control: line", s[:i].count("\n") + 1, "1'b1 -> 1'b0")
PY
tokens "$SCR/ctl" "$SCR/tok_ctl.txt"; netlist "$SCR/ctl" "$SCR/net_ctl.json"
if cmp -s "$SCR/tok_head.txt" "$SCR/tok_ctl.txt"; then echo "CONTROL-MISSED tokens"; else echo "CONTROL-CAUGHT tokens"; fi
if cmp -s "$SCR/net_head.json" "$SCR/net_ctl.json"; then echo "CONTROL-MISSED netlist"; else echo "CONTROL-CAUGHT netlist"; fi
