#!/bin/bash
# Builds receipts/ from this continuation's raw receipts and the files of the
# round-5 head 4e3aab32 that this round cites (probes and compactions), replacing
# host paths with placeholders, then writes receipts/INDEX.md from the files
# present (name, size, sha256, first line). An existing receipts/ is moved aside.
#   $1 the raw receipts   $2 the output directory   $3 the previous executor's output directory
set -u
RAW=$1 O=$2 PREV=$3 R=$2/receipts
[ -e "$R" ] && mv "$R" "$R.previous-$(date +%s)"
mkdir -p "$R"
failed=0
scrub() {  # $1 source, $2 destination (its directory is made)
    mkdir -p "$(dirname "$2")"
    if ! sed -e 's#$VALIDATION_STORAGE/scratch/665s1-a680f-work#<work>#g' -e 's#$LANES/665-s1-faces#<tree>#g' \
            -e 's#$VALIDATION_STORAGE/scratch/a680b-work#<round2-work>#g' -e 's#$VALIDATION_STORAGE/scratch/665s1-a680d-work#<round4-work>#g' \
            -e 's#$VALIDATION_TOOLS#<tools>#g' -e "s#$O#<out>#g" \
            -e 's#$MANAGEMENT#<management>#g' -e 's#$WORKSPACE_HOME#~#g' "$1" > "$2"; then
        echo "scrub failed: $1"; failed=$((failed + 1))
    fi
}
while read -r f; do scrub "$f" "$R/${f#"$RAW"/}"; done < <(find "$RAW" -type f -size -200k | sort)
# cited from the round-5 head 4e3aab32 (already scrubbed by its own collector): the
# reviewers' probes, unmodified, and the two compactions measured on throwaway edits
for f in "$PREV"/receipts/probes/* "$PREV"/receipts/images/compaction-*.log; do
    scrub "$f" "$R/at-4e3aab32/$(basename "$(dirname "$f")")/$(basename "$f")"
done
{
    echo "Files over 200 KB left out of receipts/ (size in bytes, sha256):"
    find "$RAW" -type f -size +200k | sort | while read -r f; do
        echo "${f#"$RAW"/} $(stat -c %s "$f") $(sha256sum "$f" | cut -d' ' -f1)"
    done
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
