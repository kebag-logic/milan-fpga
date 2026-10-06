#!/usr/bin/env bash
# Focused structural-equivalence probe: sv2v over the derived source list of one
# exported tree, then yosys `hierarchy; proc; opt_clean; stat -json` for one top.
# Usage (the pp_top ROM images are generated in the export first): yosys_stat.sh <export_root> <top> <out.json>
set -euo pipefail
exp=$(readlink -f "$1"); top=$2; out=$(readlink -f "$3")
cd "$exp"
pkgs=$(grep -lE '^\s*package\s+\w+\s*;' $(find hdl -name '*.sv' | sort) | sort)
rest=$(for f in $(find hdl -name '*.sv' | sort); do grep -qE '^\s*package\s+\w+\s*;' "$f" || echo "$f"; done)
tmp=$(mktemp -d)
# shellcheck disable=SC2086
sv2v -DSYNTHESIS $pkgs $rest > "$tmp/all.v"
# the uCPU ROMs are read by $readmemh at elaboration: generate them as the
# pp_top suite does and run yosys where they live
make -s -C tb/pp_top ltn_rom.hex ucode.hex > "$tmp/gen.log" 2>&1
cd tb/pp_top
yosys -q -p "read_verilog $tmp/all.v; hierarchy -top $top; proc; opt_clean; tee -q -o $out stat -json" > "$tmp/yosys.log" 2>&1 || { tail -5 "$tmp/yosys.log"; exit 1; }
rm -rf "$tmp"
sha256sum "$out"
