#!/bin/bash
# Mutation probes for syn/ooc/pp_baseline.py image checks on a copied export.
# usage: probe_helper.sh <repo> <gateware-source> <scratch>
set -u
R=$1; G=$2; S=$3
run() {  # name, mutate-command
  d=$S/$1; rm -rf "$d"; cp -a "$G" "$d"; mkdir -p "$d/roms"
  cp "$R/configs/generated/ucode.hex" "$d/roms/ucode.hex"
  cp "$R/configs/generated/ltn_rom.hex" "$d/roms/ltn_rom.hex"
  sed -i "s#$R/configs/generated/ucode.hex#$d/roms/ucode.hex#; s#$R/configs/generated/ltn_rom.hex#$d/roms/ltn_rom.hex#" "$d/alinx_ax7101.v"
  (cd "$d" && eval "$2")
  out=$(python3 -B "$R/syn/ooc/pp_baseline.py" "$d" 2>&1); rc=$?
  printf '%-22s rc=%s %s\n' "$1" "$rc" "$(printf '%s' "$out" | tail -1 | cut -c1-120)"
}
run control-unmodified "true"
run ucode-short "sed -i '\$d' roms/ucode.hex"
run ucode-long "tail -1 roms/ucode.hex >> roms/ucode.hex"
run ucode-narrow "sed -i '1s/^.//' roms/ucode.hex"
run ucode-nonhex "sed -i '5s/^./g/' roms/ucode.hex"
run ucode-missing "rm roms/ucode.hex"
run trom-empty ": > roms/ltn_rom.hex"
run litex-rom-missing "rm alinx_ax7101_rom.init"
run litex-mem-short "sed -i '\$d' alinx_ax7101_mem.init"
run sram-nonempty "echo 00000000 > alinx_ax7101_sram.init"
run gptp-dup-param "sed -i 's#^\(\s*\.GPTP_UCODE_HEX_P.*\)\$#\1\n\1#' alinx_ax7101.v"
