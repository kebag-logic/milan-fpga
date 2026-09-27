#!/usr/bin/env bash
# Fresh 8x8 export (recipe "Before measuring" + "Export the shipping builds", ax8x8 only; no synthesis).
# usage: REPO=<clean checkout at head> WORK=<empty external dir> PKT=<packet> VIVADO_BIN=<.../Vivado/bin>
#        LITEX_PYTHON=<litex venv python3> SDK=<verified sdk> bash fresh_export.sh
set -euo pipefail
: "${REPO:?}" "${WORK:?}" "${PKT:?}"
. "$PKT/scripts/env.sh"
cd "$REPO"
mkdir -p "$WORK/builder" "$WORK/roms"
python3 scripts/ci_rv32_sdk.py --destination "$SDK" --verify-only >/dev/null
test ! -e sw/builder/out
ln -s "$WORK/builder" sw/builder/out
test ! -e configs/generated/ltn_rom.hex
test ! -e configs/generated/ucode.hex
ln -s "$WORK/roms/ltn_rom.hex" configs/generated/ltn_rom.hex
ln -s "$WORK/roms/ucode.hex" configs/generated/ucode.hex
bash sw/litex/build.sh ax8x8 --dry-run > "$WORK/ax8x8-dry-run.log"
python3 "$PKT/scripts/export_8x8.py"
# Remove the recipe's three redirect symlinks so the checkout returns to exact head bytes.
rm sw/builder/out configs/generated/ltn_rom.hex configs/generated/ucode.hex
