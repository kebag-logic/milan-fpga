#!/bin/sh
# Regenerate the processor's two ROM images at each pin from that pin's own
# generator (exported read-only from a clone) and print their SHA-256.
# usage: rom_regen.sh <processor-clone> <out-dir> <pin>...
set -eu
clone=$1; out=$2; shift 2
for pin in "$@"; do
  d="$out/rom_$pin"; mkdir -p "$d/src"
  git -C "$clone" archive "$pin" hdl | tar -x -C "$d/src"
  python3 "$d/src/hdl/aecp/ucode/gen_ucode.py" -o "$d/ucode.hex" >/dev/null
  python3 "$d/src/hdl/acmp/rom/gen_ltn_rom.py" -o "$d/ltn_rom.hex" >/dev/null
  printf '%s\tucode.hex\t%s\n' "$pin" "$(sha256sum "$d/ucode.hex" | cut -d' ' -f1)"
  printf '%s\tltn_rom.hex\t%s\n' "$pin" "$(sha256sum "$d/ltn_rom.hex" | cut -d' ' -f1)"
done
