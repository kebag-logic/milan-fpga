#!/bin/sh
# Regenerate every tracked ROM image with the arguments its own producer uses
# and compare it byte-for-byte with the tracked file. Prints the SHA-256 of
# both and exits nonzero on any mismatch. Writes only under a temp directory.
#   rom_parity.sh              -> working-tree files vs working-tree generator
#   REF=<commit> rom_parity.sh -> files and generator both read from <commit>
#                                 with git show (no checkout)
set -u
cd "${A188_LANE:-$LANES/gptp68-step-policy}" || exit 2
GEN=hdl/ucode/gen_gptp_ucode.py
T=$(mktemp -d)
if [ -n "${REF:-}" ]; then
  git show "$REF:$GEN" > "$T/gen.py" || exit 2
  echo "# ref: $REF ($(git rev-parse "$REF"))"
else
  cp "$GEN" "$T/gen.py"
  echo "# ref: working tree at HEAD $(git rev-parse HEAD)"
fi
rc=0
check() {  # tracked-path  generator-args...
  f=$1; shift
  if [ -n "${REF:-}" ]; then git show "$REF:$f" > "$T/tracked.hex"; else cp "$f" "$T/tracked.hex"; fi
  python3 "$T/gen.py" "$@" -o "$T/out.hex" >/dev/null || { echo "GENFAIL $f"; rc=1; return; }
  a=$(sha256sum "$T/tracked.hex" | cut -d' ' -f1); b=$(sha256sum "$T/out.hex" | cut -d' ' -f1)
  if [ "$a" = "$b" ]; then echo "MATCH  $a  $f  (args: $*)"; else echo "DIFFER tracked=$a generated=$b  $f  (args: $*)"; rc=1; fi
}
check tb/verilator/engine/gptp_ucode.hex --clk-hz 2000000 --cease-ms 3000
check tb/tsngen/gptp_ucode.hex --clk-hz 2000000
check tb/verilator/ucpu/gptp_ucode.hex
check syn/ooc/work/gptp_ucode.hex
rm -rf "$T"
exit $rc
