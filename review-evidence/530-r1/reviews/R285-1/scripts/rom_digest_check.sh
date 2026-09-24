#!/usr/bin/env bash
# Regenerate the two protocol-processor ROM images at the checked-out pin into
# a scratch directory and print their sha256 beside the rom_digests.tsv rows.
set -euo pipefail
repo=${1:?usage: rom_digest_check.sh <repo> <scratch>}
scratch=${2:?}
mkdir -p "$scratch"
pin=$(git -C "$repo" rev-parse :protocol-processor)
echo "pin $pin checkout $(git -C "$repo/protocol-processor" rev-parse HEAD)"
python3 "$repo/protocol-processor/hdl/acmp/rom/gen_ltn_rom.py" -o "$scratch/ltn_rom.hex" >/dev/null
python3 "$repo/protocol-processor/hdl/aecp/ucode/gen_ucode.py" -o "$scratch/ucode.hex" >/dev/null
for img in ltn_rom.hex ucode.hex; do
  got=$(sha256sum < "$scratch/$img"); got=${got%% *}
  rec=$(awk -v p="$pin" -v i="$img" '$1==p && $2==i {print $3}' "$repo/syn/yosys/rom_digests.tsv")
  if [ "$got" = "$rec" ]; then v=MATCH; else v=MISMATCH; fi
  echo "$img generated=$got recorded=$rec $v"
done
