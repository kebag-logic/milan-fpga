#!/usr/bin/env bash
# Produce the build outputs that matter in one checkout into <outdir>: both ROM
# images, the generated module matrix, F06.14 as the command gate rewrites it,
# and Verilator's C++ for protocol_processor_top; then hash them.
# usage: build_outputs.sh <checkout> <outdir>   (pinned verilator on PATH)
set -eu
tree=$(cd "$1" && pwd); out=$2; rm -rf "$out"; mkdir -p "$out"; cd "$tree"
python3 hdl/aecp/ucode/gen_ucode.py -o "$out/ucode.hex" >/dev/null
python3 hdl/acmp/rom/gen_ltn_rom.py -o "$out/ltn_rom.hex" >/dev/null
w=$(mktemp -d); git archive HEAD | tar -x -C "$w"
( cd "$w" && python3 -B scripts/check_aecp_commands.py --write >/dev/null && cp docs/architecture/06_aecp_engine.md "$out/06_after_write.md" )
( cd "$w" && python3 scripts/gen_matrix.py >/dev/null 2>&1 || true; cp docs/traceability/MODULE_MATRIX.md "$out/MODULE_MATRIX.md" )
( cd "$w" && pkgs=$(find hdl -name '*_pkg.sv' | sort); all=$(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort)
  verilator --cc -Wno-fatal -Wno-lint -Wno-style --top-module protocol_processor_top -Mdir "$out/vcc" $pkgs $all >"$out/verilate.log" 2>&1 )
rm -rf "$w"
( cd "$out" && find . -type f ! -name verilate.log ! -name '*.d' ! -name '*.dat' -print0 | sort -z | xargs -0 sha256sum ) >"$out.sha256"
