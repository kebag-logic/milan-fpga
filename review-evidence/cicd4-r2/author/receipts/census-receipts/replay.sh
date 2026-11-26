#!/bin/bash
# Replay the census judge over the five retained receipts, then the seven planted faults, at the receipts' head.
# Usage: replay.sh <clean clone at 530149b5dd1a94cc5011b17c9bb28af54bc79be3, submodules initialised> <scratch dir>
set -u
here=$(cd "$(dirname "$0")" && pwd); clone=$1; scratch=$2
cd "$here" && sha256sum -c SHA256SUMS || exit 1
test "$(git -C "$clone" rev-parse HEAD)" = 530149b5dd1a94cc5011b17c9bb28af54bc79be3 || exit 1
rm -rf "$scratch/union"; mkdir -p "$scratch/union"
for f in "$here"/census-leg-*.json; do n=$(basename "$f" .json); mkdir -p "$scratch/union/$n"; cp "$f" "$scratch/union/$n/"; done
(cd "$clone" && python3 sw/mailbox/census_legs.py union --root "$scratch/union") > "$here/replay-union.log" 2>&1
echo "union rc=$?"
python3 "$here/plant_census.py" "$clone" "$scratch/union" "$scratch/plant"
