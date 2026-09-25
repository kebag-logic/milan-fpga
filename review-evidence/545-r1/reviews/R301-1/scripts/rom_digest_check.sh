#!/usr/bin/env bash
# Regenerate gptp_ucode.hex with the pinned processor's own generator (the
# same invocation ooc.sh uses) and compare with the ledger row for the pin.
set -u
REPO=${REPO:-$REVIEWS/r301-1-545}
PKT=${PKT:-$REVIEWS/545-r301-1-packet}
cd "$REPO" || exit 2
PIN=$(git ls-files -s gptp-processor | awk '{print $2}')
echo "gitlink $PIN; checkout $(git -C gptp-processor rev-parse HEAD)"
python3 gptp-processor/hdl/ucode/gen_gptp_ucode.py -o "$PKT/scratch/gptp_ucode.hex" >/dev/null || exit 2
GOT=$(sha256sum < "$PKT/scratch/gptp_ucode.hex" | cut -d' ' -f1)
WANT=$(awk -v p="$PIN" '$1==p && $2=="gptp_ucode.hex"{print $3}' syn/yosys/rom_digests.tsv)
echo "regenerated $GOT"; echo "ledger      $WANT"
[ -n "$WANT" ] && [ "$GOT" = "$WANT" ] && echo MATCH || { echo MISMATCH; exit 1; }
