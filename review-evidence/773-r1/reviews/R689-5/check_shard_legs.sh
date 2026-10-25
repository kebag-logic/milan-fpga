#!/usr/bin/env bash
# Usage: check_shard_legs.sh <repo-clone-at-candidate> <jobs.json> <log-dir> <out-dir>
# For each hosted "Verilator shard i/17" job: fetch its log (read-only API), confirm
# the checked-out commit and the --shard argument, and compare the pieces the leg
# printed with the candidate's own `run_all_suites.sh --ci-pieces --shard i/17 --list`.
set -u
repo=$1 jobs=$2 logs=$3 out=$4
mkdir -p "$logs" "$out"
want_sha=0e5cb60a15ca08b9d7096702d45d34860806d348
python3 -I -c 'import json,sys
for j in json.load(open(sys.argv[1])):
    if j["name"].startswith("Verilator shard "): print(j["id"], j["name"].split()[-1])' "$jobs" > "$out/legs.txt"
: > "$out/summary.tsv"
fail=0
while read -r id sel; do
  i=${sel%/*}
  [ -s "$logs/$id.log" ] || gh api --allow-escape-sequences "repos/kebag-logic/milan-fpga/actions/jobs/$id/logs" > "$logs/$id.log"
  clean=$(tr -d '\033' < "$logs/$id.log")
  fetched=$(grep -a -c "origin +$want_sha:refs/remotes/pull/779/merge" <<<"$clean")
  target=$(grep -a -c "target_sha=$want_sha" <<<"$clean")
  shardarg=$(grep -a -c -- "--shard \"$i/17\"" <<<"$clean")
  (cd "$repo" && scripts/run_all_suites.sh --ci-pieces --shard "$i/17" --list) | sort > "$out/local_$i.txt"
  # the leg prints "Shard <i> owns:" followed by one indented piece per line
  awk -v hdr="Shard $i owns:" '
    { sub(/^[0-9T:.Z-]+ /, "") }
    $0 == hdr { on = 1; next }
    on && /^  [A-Za-z0-9_]+$/ { sub(/^  /, ""); print; next }
    on { exit }' <<<"$clean" | sort > "$out/hosted_$i.txt"
  n=$(wc -l < "$out/local_$i.txt")
  same=$(cmp -s "$out/local_$i.txt" "$out/hosted_$i.txt" && echo yes || echo no)
  ok=1; [ "$fetched" -ge 1 ] && [ "$target" -ge 1 ] && [ "$shardarg" -ge 1 ] && [ "$n" -ge 1 ] && [ "$same" = yes ] || ok=0
  [ $ok -eq 1 ] || fail=1
  printf '%s\t%s\tfetch=%s\ttarget=%s\tshardarg=%s\tlocal_pieces=%s\thosted_list_equal=%s\tok=%s\n' "$id" "$sel" "$fetched" "$target" "$shardarg" "$n" "$same" "$ok" >> "$out/summary.tsv"
done < "$out/legs.txt"
cat "$out"/hosted_*.txt | sort > "$out/union.txt"
(cd "$repo" && scripts/run_all_suites.sh --ci-pieces --shard 0/1 --list) | sort > "$out/unsharded.txt"
printf 'legs=%s union=%s unique=%s unsharded=%s union_equals_unsharded=%s\n' \
  "$(wc -l < "$out/legs.txt")" "$(wc -l < "$out/union.txt")" "$(sort -u "$out/union.txt" | wc -l)" \
  "$(wc -l < "$out/unsharded.txt")" "$(cmp -s "$out/union.txt" "$out/unsharded.txt" && echo yes || echo no)" >> "$out/summary.tsv"
cat "$out/summary.tsv"
exit $fail
