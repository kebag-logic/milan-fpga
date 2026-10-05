#!/usr/bin/env bash
# Regenerate the two processor ROMs at the checkout's pin, outside the tree, and compare with rom_digests.tsv.
# Usage: rom_digests_check.sh <checkout-root> <scratch-dir>
set -eu
root=$1; out=$2; mkdir -p "$out"
pin=$(git -C "$root" ls-tree HEAD protocol-processor | awk '{print $3}')
python3 "$root/protocol-processor/hdl/acmp/rom/gen_ltn_rom.py" -o "$out/ltn_rom.hex" >/dev/null
python3 "$root/protocol-processor/hdl/aecp/ucode/gen_ucode.py" -o "$out/ucode.hex" >/dev/null
rc=0
for img in ltn_rom.hex ucode.hex; do
  got=$(sha256sum < "$out/$img" | awk '{print $1}')
  rec=$(awk -F'\t' -v p="$pin" -v i="$img" '$1==p && $2==i {print $3}' "$root/syn/yosys/rom_digests.tsv")
  if [ "$got" = "$rec" ]; then echo "MATCH $pin $img $got"; else echo "MISMATCH $pin $img got=$got recorded=$rec"; rc=1; fi
done
exit $rc
