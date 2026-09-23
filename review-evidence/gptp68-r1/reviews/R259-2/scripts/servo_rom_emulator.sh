#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Run scripts/servo_rom_emulator.py on the head's own generator at eight
# clocks (images are generated into scratch; only their hex words execute).
set -eu
. "$(dirname "$0")/env.sh"
w="$SCRATCH/emu"; rm -rf "$w"; mkdir -p "$w"
git -C "$CLONE" show "$HEAD_SHA:hdl/ucode/gen_gptp_ucode.py" > "$w/gen_gptp_ucode.py"
python3 "$PACKET/scripts/servo_rom_emulator.py" "$w/gen_gptp_ucode.py" "$w" \
  2000000 25000000 50000000 62500000 100000000 125000000 156250000 1000000
