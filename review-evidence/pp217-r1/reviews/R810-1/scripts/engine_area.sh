#!/usr/bin/env bash
# engine_area.sh <tree> <outdir>: sv2v of every hdl/ source, then synth_xilinx -family xc7 -flatten of
# KL_adp_engine and KL_aecp_engine alone (the processor's yosys flow, engines only); one stat per run.
set -euo pipefail
tree=$(cd "$1" && pwd); mkdir -p "$2"; out=$(cd "$2" && pwd)
work=$(mktemp -d -p "$out"); trap 'rm -rf "$work"' EXIT
cd "$tree"
sv2v $(find hdl -name '*_pkg.sv' | sort) $(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort) > "$work/all.v"
( cd hdl/aecp/ucode && python3 -B gen_ucode.py -o "$work/ucode.hex" >/dev/null )
( cd hdl/acmp/rom && python3 -B gen_ltn_rom.py -o "$work/ltn_rom.hex" >/dev/null )
sha256sum "$work/all.v" "$work/ucode.hex" "$work/ltn_rom.hex" | sed "s#$work/##" > "$out/inputs.sha256"
cd "$work"
for top in KL_adp_engine KL_aecp_engine; do
  yosys -q -l "$out/$top.log" -p "read_verilog all.v; hierarchy -check -top $top; synth_xilinx -family xc7 -flatten -top $top; tee -o $out/$top.stat stat" >/dev/null &
  pids="${pids:-} $!"
done
for p in $pids; do wait "$p"; done
for top in KL_adp_engine KL_aecp_engine; do
  printf '%s FF=%s LUT=%s MUXF=%s\n' "$top" \
    "$(grep -E '^\s+[0-9]+\s+.*FD[CPRS]E?\b' "$out/$top.stat" | awk '{s+=$1} END{print s+0}')" \
    "$(grep -E '^\s+[0-9]+\s+.*LUT[1-6]\b' "$out/$top.stat" | awk '{s+=$1} END{print s+0}')" \
    "$(grep -E '^\s+[0-9]+\s+.*MUXF[78]\b' "$out/$top.stat" | awk '{s+=$1} END{print s+0}')"
done | tee "$out/SUMMARY.txt"
