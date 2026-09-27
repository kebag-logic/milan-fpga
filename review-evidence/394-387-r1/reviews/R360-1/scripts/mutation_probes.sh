#!/bin/sh
# Plant single-cell and single-hash mutations in a copy of the findings page and
# show that recompute_table.py and check_hash_table.py each report them.
# usage: mutation_probes.sh <page.md> <packet author dir> <scratch dir>
set -u
PAGE=$1; PK=$2; T=$3; D=$(dirname "$0")
mkdir -p "$T"
run() {
  cp "$PAGE" "$T/page.md"; sed -i "$1" "$T/page.md"
  echo "mutant: $1"
  cmp -s "$PAGE" "$T/page.md" && echo "  mutant not applied"
  python3 "$D/recompute_table.py" "$T/page.md" "$PK" | grep -E 'DIFF|table rows differing' | cut -c1-90
}
run 's/| 39.92 \/ 39.77-40.05 | 0.63 |/| 39.92 \/ 39.77-40.05 | 0.73 |/'
run 's/| 12.25-12.54 |/| 12.25-12.55 |/'
run 's/| 2 \/ 0 | 1 > 2 > 1 |$/| 2 \/ 0 | 1 > 2 > 0 > 1 |/'
cp "$PAGE" "$T/page.md"
sed -i 's/9ae8fa4f84afe9da7afbca6466d66b106263669b8b96eae1f7d684ba4c6487fa/9ae8fa4f84afe9da7afbca6466d66b106263669b8b96eae1f7d684ba4c6487fb/' "$T/page.md"
echo "mutant: cycle 3 tap.pcap hash, last nibble"
python3 "$D/check_hash_table.py" "$T/page.md" "$PK" | grep -E 'MISMATCH|mismatches' | cut -c1-90
