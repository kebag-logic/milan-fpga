#!/bin/sh
# Regenerate every tracked ROM image from the generator at a given clone and
# compare it with the committed bytes. Usage: rom_regen_check.sh <clone> <outdir>
set -eu
clone=$1; out=$2
mkdir -p "$out"
gen="$clone/hdl/ucode/gen_gptp_ucode.py"
check() { # <tracked path> <generator args...>
  t=$1; shift
  python3 -B "$gen" "$@" -o "$out/$(echo "$t" | tr / _)" >"$out/$(echo "$t" | tr / _).log"
  a=$(sha256sum "$clone/$t" | cut -d' ' -f1)
  b=$(sha256sum "$out/$(echo "$t" | tr / _)" | cut -d' ' -f1)
  if [ "$a" = "$b" ]; then v=EQUAL; else v=DIFFER; fi
  echo "$t tracked=$a regenerated=$b $v | $(head -1 "$out/$(echo "$t" | tr / _).log")"
}
check tb/verilator/engine/gptp_ucode.hex --clk-hz 2000000 --cease-ms 3000
check tb/tsngen/gptp_ucode.hex --clk-hz 2000000
check tb/verilator/ucpu/gptp_ucode.hex
check syn/ooc/work/gptp_ucode.hex
