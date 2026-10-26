#!/bin/bash
# Builds receipts/ from the round-3 work directory alone, replacing host paths with placeholders,
# then writes receipts/INDEX.md from the files present (name, size, sha256, first line).
# receipts/ must not exist yet.
#   $1 the work directory   $2 the output directory
set -u
W=$1 O=$2 R=$2/receipts
[ -e "$R" ] && { echo "$R exists"; exit 2; }
mkdir -p "$R"
failed=0
scrub() {  # $1 source, $2 destination (its directory is made)
    mkdir -p "$(dirname "$2")"
    if ! sed -e "s#$W#<work>#g" -e 's#$LANES/665-s1-faces#<tree>#g' \
            -e 's#$LANES/665s1-a680c-shard#<shard-clone>#g' -e 's#$VALIDATION_STORAGE/scratch/a680b-base#<base-tree>#g' \
            -e 's#$VALIDATION_STORAGE/scratch/a680b-work#<round2-work>#g' -e 's#$VALIDATION_TOOLS#<tools>#g' \
            -e "s#$O#<out>#g" -e 's#$MANAGEMENT#<management>#g' -e 's#$WORKSPACE_HOME#~#g' \
            -e 's#^\(| Host *: \).*#\1<host>#' "$1" > "$2"; then
        echo "scrub failed: $1"; failed=$((failed + 1))
    fi
}
copy_tree() {  # $1 source directory, $2 destination under receipts, $3 find name pattern
    [ -d "$1" ] || return 0
    find "$1" -maxdepth 3 -type f -name "$3" -size -200k | while read -r f; do scrub "$f" "$R/$2/${f#"$1"/}"; done
}
copy_tree "$W/gates" gates '*.txt'
copy_tree "$W/fw" fw/final-44d95625 '*.txt'
copy_tree "$W/fw-b6e35903" fw/at-b6e35903 '*.txt'
copy_tree "$W/fw-7464b876-d9-escaped" fw/at-7464b876-d9-escaped '*.txt'
for s in "$W"/sweep-*/; do
    s=${s%/}
    for pat in 'spec.json' '01.log' 'results.json' 'complete.json' '*.log'; do copy_tree "$s" "sweep/$(basename "$s")" "$pat"; done
done
for d in ooc-bd3f5d94 ooc-e76a755a; do
    for f in util_hier.rpt util.rpt route.rpt sources.sha256 ooc.tcl; do scrub "$W/$d/$f" "$R/ooc/$d-$f"; done
    sed -n '/WNS(ns)/,+2p' "$W/$d/timing.rpt" | head -3 > "$R/ooc/$d-timing-summary.txt"
done
scrub "$W/ooc.log" "$R/ooc/ooc-runs.log"
copy_tree "$W/images" images-at-80aa0372 '*.txt'
copy_tree "$W/final/images" images-final '*.txt'
copy_tree "$W/export-receipts" export '*'
scrub "$W/export.log" "$R/export/export-run.log"
scrub "$W/export-attempt1-wrongsha.log" "$R/export/export-attempt1-wrongsha.log"
for f in linked-images.txt:linked-images-at-80aa0372.txt linked-images-final.txt:linked-images-final.txt \
         ledger-mutants.txt:ledger-mutants-at-80aa0372.txt ledger-mutants-2.txt:ledger-mutants-b48db8fa.txt \
         d9-mutants.txt:d9-mutants.txt test-ctrl-memory-4.txt:test-ctrl-memory-b48db8fa.txt \
         hang/run-lb.txt:wb-address-shifted-before-fix.txt; do
    scrub "$W/${f%%:*}" "$R/${f#*:}"
done
{
    echo "Files over 200 KB left out of receipts/ (size in bytes, sha256), from the work directory:"
    find "$W"/gates "$W"/fw "$W"/sweep-* "$W"/ooc-* -type f -size +200k 2>/dev/null | sort | while read -r f; do
        echo "${f#"$W"/} $(stat -c %s "$f") $(sha256sum "$f" | cut -d' ' -f1)"
    done
} > "$R/large-files.txt"
empty=$(find "$R" -type f -size 0)
[ -z "$empty" ] || { echo "empty: $empty"; failed=$((failed + 1)); }
big=$(find "$R" -type f -size +200k)
[ -z "$big" ] || { echo "over 200 KB: $big"; failed=$((failed + 1)); }
{
    echo "# Receipts index (generated from the files present)"
    echo
    echo "| File | Bytes | sha256 (first 16) | First line |"
    echo "|---|---:|---|---|"
    (cd "$R" && find . -type f ! -name INDEX.md | sort) | while read -r f; do
        p="$R/${f#./}"
        first=$(head -c 300 "$p" | head -1 | tr -d '|`' | cut -c1-90)
        echo "| \`${f#./}\` | $(stat -c %s "$p") | $(sha256sum "$p" | cut -c1-16) | $first |"
    done
} > "$R/INDEX.md"
echo "receipts: $(find "$R" -type f | wc -l) files, $(du -sh "$R" | cut -f1), $failed problem(s)"
exit $((failed > 0))
