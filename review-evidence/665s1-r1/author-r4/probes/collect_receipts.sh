#!/bin/bash
# Builds receipts/ from the round-4 work directory alone, replacing host paths with placeholders,
# then writes receipts/INDEX.md from the files present (name, size, sha256, first line).
# receipts/ is rebuilt from scratch: an existing one is moved aside first.
#   $1 the work directory   $2 the output directory
set -u
W=$1 O=$2 R=$2/receipts
[ -e "$R" ] && mv "$R" "$R.previous-$(date +%s)"
mkdir -p "$R"
failed=0
scrub() {  # $1 source, $2 destination (its directory is made)
    mkdir -p "$(dirname "$2")"
    if ! sed -e "s#$W#<work>#g" -e 's#$LANES/665-s1-faces#<tree>#g' \
            -e 's#$LANES/665s1-a680d-shard#<shard-clone>#g' \
            -e 's#$VALIDATION_STORAGE/scratch/a680b-work#<round2-work>#g' -e 's#$VALIDATION_STORAGE/scratch/a680c-work#<round3-work>#g' \
            -e 's#$REVIEWS#<reviews>#g' -e 's#$VALIDATION_TOOLS#<tools>#g' \
            -e "s#$O#<out>#g" -e 's#$MANAGEMENT#<management>#g' -e 's#$WORKSPACE_HOME#~#g' \
            -e 's#^\(| Host *: \).*#\1<host>#' "$1" > "$2"; then
        echo "scrub failed: $1"; failed=$((failed + 1))
    fi
}
copy_tree() {  # $1 source directory, $2 destination under receipts, $3 find name pattern, $4 depth
    [ -d "$1" ] || return 0
    find "$1" -maxdepth "${4:-3}" -type f -name "$3" -size -200k | while read -r f; do scrub "$f" "$R/$2/${f#"$1"/}"; done
}
copy_tree "$W/gates" gates '*.txt' 1
copy_tree "$W/fw" fw '*.txt' 1
# the probes: R701-3's through its driver, R702-3's as published; each at the reviewed head (control) and the final head
scrub "$W/probes/r701/final.log" "$R/probes/r701-response-probe-final.log"
scrub "$W/probes/r701/control-44d95625.log" "$R/probes/r701-response-probe-control-44d95625.log"
scrub "$W/probes/r702-final/run.log" "$R/probes/r702-probe-ack-final.log"
scrub "$W/probes/r702-control/run.log" "$R/probes/r702-probe-ack-control-44d95625.log"
scrub "$W/probes/final-head.txt" "$R/probes/final-head.txt"
sha256sum "$W/probes/r701/response_probe.py" "$W/probes/r702-final/probe_ack.py" \
    $REVIEWS/665s1-r701-3-packet/scripts/response_probe.py \
    $REVIEWS/665s1-r702-3-packet/probe_ack.py > "$W/probes/hashes.txt"
scrub "$W/probes/hashes.txt" "$R/probes/probe-hashes.txt"
# the AECP campaign: the final run whole, and the first run's one escape
for k in 0 1 2 3; do
    scrub "$W/aecp-mut-final/s$k.log" "$R/aecp-mutants/final-shard-$k.log"
    scrub "$W/aecp-mut-final/s$k/results.json" "$R/aecp-mutants/final-shard-$k-results.json"
done
for n in unapplied-earlier-change-admits-the-next unapplied-change-claims-success unapplied-lock-release-notified \
         held-face-admits-lock-entity held-face-admits-add-audio-mappings held-face-refuses-get-control \
         face-never-unapplied face-owed-interface-counted-applied face-held-commit-counted-applied \
         face-publish-writes-a-held-block face-open-claims-its-acknowledgement \
         aecp-opens-before-its-publication-is-acknowledged; do
    f=$(ls "$W"/aecp-mut-final/s*/"$n".log 2>/dev/null | head -1)
    if [ -n "$f" ]; then scrub "$f" "$R/aecp-mutants/new-defects/$n.log"; else echo "missing defect log: $n"; failed=$((failed + 1)); fi
done
for k in 0 1 2 3; do scrub "$W/aecp-mut/s$k.log" "$R/aecp-mutants/first-run-shard-$k.log"; done
f=$(ls "$W"/aecp-mut/s*/face-poll-writes-a-held-block.log 2>/dev/null | head -1)
[ -n "$f" ] && scrub "$f" "$R/aecp-mutants/first-run-escaped-face-poll-writes-a-held-block.log"
# the linked images and the export
copy_tree "$W/final/images" images '*.txt' 1
scrub "$W/final/linked-images.txt" "$R/images/linked-images.txt"
scrub "$W/final/image-points.txt" "$R/images/image-points.txt"
copy_tree "$W/img-wip1/images" images-working-tree '*.txt' 1
copy_tree "$W/exp-receipts" export '*' 1
scrub "$W/exp/export.log" "$R/export/export-run.log"
# the sweep
for s in "$W"/sweep-*/; do
    s=${s%/}
    for pat in 'spec.json' 'results.json' 'complete.json' '*.log'; do copy_tree "$s" "sweep/$(basename "$s")" "$pat"; done
done
{
    echo "Files over 200 KB left out of receipts/ (size in bytes, sha256), from the work directory:"
    find "$W"/gates "$W"/fw "$W"/sweep-* "$W"/aecp-mut-final -maxdepth 3 -type f -size +200k 2>/dev/null | sort | while read -r f; do
        echo "${f#"$W"/} $(stat -c %s "$f") $(sha256sum "$f" | cut -d' ' -f1)"
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
