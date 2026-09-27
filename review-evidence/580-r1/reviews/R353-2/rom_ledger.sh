#!/bin/sh
# Regenerate the three ledgered control-plane ROMs from the initialized pinned
# submodules and compare each sha256 with its row in syn/yosys/rom_digests.tsv.
# Usage: rom_ledger.sh <repo> <out-dir>
set -eu
R=$1; O=$2
PP=$(git -C "$R" rev-parse :protocol-processor); GP=$(git -C "$R" rev-parse :gptp-processor)
[ "$(git -C "$R/protocol-processor" rev-parse HEAD)" = "$PP" ]
[ "$(git -C "$R/gptp-processor" rev-parse HEAD)" = "$GP" ]
rc=0
for spec in "ltn_rom.hex|protocol-processor/hdl/acmp/rom/gen_ltn_rom.py|$PP" \
            "ucode.hex|protocol-processor/hdl/aecp/ucode/gen_ucode.py|$PP" \
            "gptp_ucode.hex|gptp-processor/hdl/ucode/gen_gptp_ucode.py|$GP"; do
  img=${spec%%|*}; rest=${spec#*|}; gen=${rest%%|*}; pin=${rest#*|}
  PYTHONDONTWRITEBYTECODE=1 python3 "$R/$gen" -o "$O/$img" >/dev/null
  got=$(sha256sum < "$O/$img"); got=${got%% *}
  rec=$(awk -v p="$pin" -v i="$img" '$1 == p && $2 == i { print $3 }' "$R/syn/yosys/rom_digests.tsv")
  n=$(printf '%s\n' "$rec" | grep -c . || true)
  if [ "$n" = 1 ] && [ "$rec" = "$got" ]; then s=MATCH; else s=MISMATCH; rc=1; fi
  echo "$s $pin $img generated=$got ledger=$rec rows=$n"
done
exit $rc
