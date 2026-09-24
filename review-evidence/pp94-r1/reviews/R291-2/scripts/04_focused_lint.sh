#!/usr/bin/env bash
# Focused Verilator lint (repository flags) of the three touched RTL tops, plus the
# guard alone under full -Wall (no UNUSED waivers).
source "$(dirname "$0")/00_env.sh"
cd "$TREE"
pkgs=$(find hdl -name '*_pkg.sv' | sort); all=$(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort)
for top in KL_aecp_desc_mem_guard KL_aecp_desc_store protocol_processor_top; do
  set +e; out=$(verilator --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM --top-module $top $pkgs $all 2>&1); rc=$?; set -e
  n=$(grep -cE '%(Warning|Error)' <<<"$out" || true); echo "$top rc=$rc findings=$n"; grep -E '%(Warning|Error)' <<<"$out" | head -5 || true
done
set +e; out=$(verilator --lint-only -Wall hdl/aecp/KL_aecp_desc_mem_guard.sv 2>&1); rc=$?; set -e
echo "guard-alone-Wall rc=$rc findings=$(grep -cE '%(Warning|Error)' <<<"$out" || true)"; grep -E '%(Warning|Error)' <<<"$out" | head || true
