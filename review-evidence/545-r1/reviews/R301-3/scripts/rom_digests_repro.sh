#!/usr/bin/env bash
# Regenerates the three control-plane ROM images at the checked-out pins with
# the same generators syn/yosys/ooc.sh uses, into a scratch directory, and
# compares each sha256 against the syn/yosys/rom_digests.tsv row for the pin.
set -eu
R=$(git rev-parse --show-toplevel)
OUT=${1:?scratch dir}
mkdir -p "$OUT"
PP=$(git -C "$R" rev-parse :protocol-processor)
GP=$(git -C "$R" rev-parse :gptp-processor)
[ "$(git -C "$R/protocol-processor" rev-parse HEAD)" = "$PP" ] || { echo "pp checkout != gitlink"; exit 2; }
[ "$(git -C "$R/gptp-processor" rev-parse HEAD)" = "$GP" ] || { echo "gptp checkout != gitlink"; exit 2; }
fail=0
for spec in "ltn_rom.hex|protocol-processor/hdl/acmp/rom/gen_ltn_rom.py|$PP" \
            "ucode.hex|protocol-processor/hdl/aecp/ucode/gen_ucode.py|$PP" \
            "gptp_ucode.hex|gptp-processor/hdl/ucode/gen_gptp_ucode.py|$GP"; do
  IFS='|' read -r img gen pin <<< "$spec"
  python3 "$R/$gen" -o "$OUT/$img" >/dev/null
  got=$(sha256sum < "$OUT/$img"); got=${got%% *}
  rec=$(awk -v p="$pin" -v i="$img" '$1==p && $2==i {print $3; exit}' "$R/syn/yosys/rom_digests.tsv")
  if [ "$got" = "$rec" ]; then v=MATCH; else v=MISMATCH; fail=1; fi
  echo "$v $img pin=$pin generated=$got recorded=${rec:-NONE}"
done
exit $fail
