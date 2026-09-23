#!/bin/sh
# Reproduce the gPTP ROM content digest the ledger records for the new pin,
# the old pin's recorded digest (control), the donor's own tracked images,
# and the protocol-processor rows at the unchanged pin, without Yosys.
# Usage: rom_digest_check.sh <clone> <scratch dir>
set -u
clone=$1 work=$2
mkdir -p "$work"
cd "$clone" || exit 2
ledger=syn/yosys/rom_digests.tsv
rc=0
gl=$(git rev-parse :gptp-processor)
old=$(git rev-parse 759da623072358afdb0e9d570a7b4b6a788492c9:gptp-processor)
pp=$(git rev-parse :protocol-processor)
echo "gptp gitlink $gl; base gitlink $old; pp gitlink $pp"
for pin in "$gl" "$old"; do
  src="$work/gen_$pin.py"
  git -C gptp-processor show "$pin:hdl/ucode/gen_gptp_ucode.py" > "$src" || exit 2
  python3 -I "$src" -o "$work/gptp_ucode_$pin.hex" > /dev/null || { echo "FAIL generator at $pin"; rc=1; continue; }
  got=$(sha256sum < "$work/gptp_ucode_$pin.hex"); got=${got%% *}
  rec=$(awk -v p="$pin" '$1 == p && $2 == "gptp_ucode.hex" { print $3 }' "$ledger")
  n=$(awk -v p="$pin" '$1 == p && $2 == "gptp_ucode.hex"' "$ledger" | wc -l)
  echo "pin $pin generated $got recorded $rec rows $n"
  [ "$n" = 1 ] && [ "$got" = "$rec" ] || { echo "FAIL ledger row for $pin"; rc=1; }
done
# the pin's own tracked images at the default clock
for img in tb/verilator/ucpu/gptp_ucode.hex syn/ooc/work/gptp_ucode.hex; do
  t=$(git -C gptp-processor show "$gl:$img" | sha256sum); t=${t%% *}
  echo "donor $img $t"
done
# the protocol-processor rows at the unchanged pin still exist
for img in ltn_rom.hex ucode.hex; do
  n=$(awk -v p="$pp" -v i="$img" '$1 == p && $2 == i' "$ledger" | wc -l)
  echo "pp pin $pp $img rows $n"
  [ "$n" = 1 ] || { echo "FAIL pp row $img"; rc=1; }
done
# the ledger diff against the base adds exactly one row and removes none
git diff --numstat 759da623072358afdb0e9d570a7b4b6a788492c9 HEAD -- "$ledger"
git diff -U0 759da623072358afdb0e9d570a7b4b6a788492c9 HEAD -- "$ledger" | grep '^[-+][^-+]'
# rows are sorted and unique, as the recorder writes them
body=$(grep -v '^#' "$ledger")
[ "$(printf '%s\n' "$body" | LC_ALL=C sort -u)" = "$body" ] && echo "ledger body sorted-unique OK" || { echo "FAIL ledger order"; rc=1; }
echo "rom_digest_check rc=$rc"
exit $rc
