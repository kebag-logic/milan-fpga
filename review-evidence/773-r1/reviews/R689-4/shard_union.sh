#!/usr/bin/env bash
# List every --ci-pieces shard i/N of the repo and prove each piece is owned exactly once
# and the union equals the unsharded 0/1 selection.
set -u
REPO=${1:?repo}; OUT=${2:?outdir}; N=${3:-17}
mkdir -p "$OUT"; cd "$REPO" || exit 2
: >"$OUT/all_shards.txt"
for i in $(seq 0 $((N-1))); do
  bash scripts/run_all_suites.sh --ci-pieces --shard "$i/$N" --list >"$OUT/shard_$i.txt" 2>"$OUT/shard_$i.err" || { echo "shard $i rc=$?"; exit 1; }
  sed "s|^|$i |" "$OUT/shard_$i.txt" >>"$OUT/all_shards.txt"
done
bash scripts/run_all_suites.sh --ci-pieces --shard 0/1 --list >"$OUT/unsharded.txt" 2>"$OUT/unsharded.err" || exit 1
awk '{print $2}' "$OUT/all_shards.txt" | sort >"$OUT/union_sorted.txt"
sort "$OUT/unsharded.txt" >"$OUT/unsharded_sorted.txt"
dups=$(uniq -d "$OUT/union_sorted.txt" | wc -l)
echo "pieces_total=$(wc -l <"$OUT/union_sorted.txt") unsharded=$(wc -l <"$OUT/unsharded_sorted.txt") duplicates=$dups"
if diff -q "$OUT/union_sorted.txt" "$OUT/unsharded_sorted.txt" >/dev/null && [ "$dups" = 0 ]; then echo "UNION_EXACT_ONCE=ok"; else echo "UNION_EXACT_ONCE=FAIL"; diff "$OUT/union_sorted.txt" "$OUT/unsharded_sorted.txt" | head; exit 1; fi
