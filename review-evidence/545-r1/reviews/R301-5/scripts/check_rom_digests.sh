#!/usr/bin/env bash
# Independently regenerate the three control-plane ROM images at the
# superproject's recorded pins and compare each sha256 with the ledger row
# syn/yosys/rom_digests.tsv keys by that pin. Then run the repository gate
# itself (syn/yosys/ooc.sh) on its smallest top, which validates all three
# images against the ledger before pricing anything.
#
# usage: check_rom_digests.sh <repo> <scratch-dir>
set -uo pipefail
repo=$(cd "$1" && pwd)
work=$(mkdir -p "$2" && cd "$2" && pwd)
cd "$repo" || exit 2
status=0
pp=$(git rev-parse :protocol-processor)
gp=$(git rev-parse :gptp-processor)
echo "gitlink protocol-processor $pp (checkout $(git -C protocol-processor rev-parse HEAD))"
echo "gitlink gptp-processor     $gp (checkout $(git -C gptp-processor rev-parse HEAD))"
for spec in \
    "ltn_rom.hex|protocol-processor/hdl/acmp/rom/gen_ltn_rom.py|$pp" \
    "ucode.hex|protocol-processor/hdl/aecp/ucode/gen_ucode.py|$pp" \
    "gptp_ucode.hex|gptp-processor/hdl/ucode/gen_gptp_ucode.py|$gp"; do
  IFS='|' read -r img gen pin <<< "$spec"
  python3 "$gen" -o "$work/$img" > /dev/null || { echo "FAIL generator $gen"; status=1; continue; }
  got=$(sha256sum < "$work/$img"); got=${got%% *}
  rec=$(awk -v p="$pin" -v i="$img" '$1 == p && $2 == i { print $3 }' syn/yosys/rom_digests.tsv)
  n=$(printf '%s\n' "$rec" | grep -c .)
  if [ "$n" -eq 1 ] && [ "$got" = "$rec" ]; then
    echo "PASS $img at $pin: $got (one ledger row)"
  else
    echo "FAIL $img at $pin: generated $got, ledger rows ($n): $rec"; status=1
  fi
done
echo "--- syn/yosys/ooc.sh tcam"
( cd syn/yosys && ./ooc.sh tcam ); rc=$?
echo "ooc.sh tcam exit $rc"
[ "$rc" -eq 0 ] || status=1
echo "overall $status"
exit $status
