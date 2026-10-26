#!/bin/bash
# Builds receipts/ from this round's raw receipts in the work directory, replacing host paths with
# placeholders, then writes receipts/INDEX.md from the files present (name, size, sha256, first line).
# Files over 200 KB are listed in receipts/large-files.txt with size and sha256, never copied.
#   $1 the work directory   $2 the output directory   $3 the final head's short id   $4 the images directory
set -u
W=$1 O=$2 H=$3 I=$4 R=$2/receipts
[ -e "$R" ] && mv "$R" "$R.previous-$(date +%s)"
mkdir -p "$R"
failed=0
large=()
scrub() {  # $1 source, $2 destination (its directory is made)
    if [ "$(stat -c %s "$1")" -gt 204800 ]; then large+=("$2 $(stat -c %s "$1") $(sha256sum "$1" | cut -d' ' -f1)"); return; fi
    mkdir -p "$(dirname "$2")"
    if ! sed -e "s#$W#<work>#g" -e 's#$LANES/665s1-a680g-shard#<shard-clone>#g' \
            -e 's#$LANES/665-s1-faces#<tree>#g' \
            -e 's#$VALIDATION_STORAGE/scratch/a680b-work#<round2-work>#g' -e 's#$VALIDATION_STORAGE/scratch/665s1-a680d-work#<round4-work>#g' \
            -e 's#$VALIDATION_STORAGE/scratch/665s1-a680f-work#<round5-work>#g' -e 's#$VALIDATION_TOOLS#<tools>#g' \
            -e 's#$REVIEWS#<reviews>#g' -e "s#$O#<out>#g" \
            -e 's#$MANAGEMENT#<management>#g' -e 's#$WORKSPACE_HOME#~#g' "$1" > "$2"; then
        echo "scrub failed: $1"; failed=$((failed + 1))
    fi
}
for f in "$W"/gates/*; do scrub "$f" "$R/gates/$(basename "$f")"; done
for f in "$W"/fw/*; do scrub "$f" "$R/fw/$(basename "$f")"; done
for f in "$W"/aecp-mutants/head.txt "$W"/aecp-mutants/shard-*.log; do scrub "$f" "$R/aecp-mutants/$(basename "$f")"; done
for k in 0 1 2 3; do scrub "$W/aecp-mutants/out-$k/results.json" "$R/aecp-mutants/results-shard-$k.json"; done
while read -r f; do scrub "$f" "$R/probes/${f#"$W"/probes/}"; done < <(find "$W/probes" -path "$W/probes/scratch" -prune -o -type f -print | sort)
for f in "$I"/image-points.txt "$I"/linked-images.txt "$I"/elf-sha256.txt "$I"/images/head-*.txt; do
    scrub "$f" "$R/images/$(basename "$f")"
done
# the new plants graded before the first commit, with the escape found and closed there
for s in sub1 sub2; do
    scrub "$W/$s/results.json" "$R/plants-before-commit/$s-results.json"
done
scrub "$W/sub1/expired-lock-not-held-against-others.log" "$R/plants-before-commit/sub1-expired-lock-not-held-against-others.log"
# the C++ idiom ratchet's failure at 168ae33d that the third commit answers
scrub "$W/gates-168ae33d/docs-gates.txt" "$R/superseded/docs-gates-168ae33d.txt"
# the four-shard sweep at the final head
S=$W/sweep-$H
if [ -d "$S" ]; then
    while read -r f; do scrub "$f" "$R/sweep/sweep-$H/${f#"$S"/}"; done < <(find "$S" -type f | sort)
    for f in "$W"/sweep-spec/sweep-"$H".json; do scrub "$f" "$R/sweep/$(basename "$f")"; done
fi
{
    echo "Files over 200 KB left out of receipts/ (destination, size in bytes, sha256):"
    for l in "${large[@]}"; do echo "${l#"$R"/}"; done
} > "$R/large-files.txt"
empty=$(find "$R" -type f -size 0)
[ -z "$empty" ] || { echo "empty: $empty"; failed=$((failed + 1)); }
big=$(find "$R" -type f -size +200k)
[ -z "$big" ] || { echo "over 200 KB: $big"; failed=$((failed + 1)); }
left=$(grep -rlE '$WORKSPACE_HOME|$VALIDATION_STORAGE|/srv/act' "$R" || true)
[ -z "$left" ] || { echo "host paths left: $left"; failed=$((failed + 1)); }
{
    echo "# Receipts index (generated from the files present)"
    echo
    echo "| File | Bytes | sha256 | First line |"
    echo "|---|---:|---|---|"
    find "$R" -type f ! -name INDEX.md | sort | while read -r f; do
        first=$(head -n 1 "$f" | cut -c1-100 | tr '|' '/')
        echo "| ${f#"$R"/} | $(stat -c %s "$f") | $(sha256sum "$f" | cut -d' ' -f1) | $first |"
    done
} > "$R/INDEX.md"
echo "receipts: $(find "$R" -type f | wc -l) files, failed=$failed"
exit $((failed > 0))
