#!/bin/bash
# Builds receipts/ from the round-5 work directory alone, replacing host paths with placeholders,
# then writes receipts/INDEX.md from the files present (name, size, sha256, first line).
# receipts/ is rebuilt from scratch: an existing one is moved aside first. Round 4's script, re-pointed.
#   $1 the work directory   $2 the output directory
set -u
W=$1 O=$2 R=$2/receipts
[ -e "$R" ] && mv "$R" "$R.previous-$(date +%s)"
mkdir -p "$R"
failed=0
scrub() {  # $1 source, $2 destination (its directory is made)
    mkdir -p "$(dirname "$2")"
    if ! sed -e "s#$W#<work>#g" -e 's#$LANES/665-s1-faces#<tree>#g' \
            -e 's#$LANES/665s1-a680e-shard#<shard-clone>#g' \
            -e 's#$VALIDATION_STORAGE/scratch/a680b-work#<round2-work>#g' -e 's#$VALIDATION_STORAGE/scratch/665s1-a680d-work#<round4-work>#g' \
            -e 's#$REVIEWS#<reviews>#g' -e 's#$VALIDATION_TOOLS#<tools>#g' \
            -e "s#$O#<out>#g" -e 's#$MANAGEMENT#<management>#g' -e 's#$WORKSPACE_HOME#~#g' \
            -e 's#^\(| Host *: \).*#\1<host>#' "$1" > "$2"; then
        echo "scrub failed: $1"; failed=$((failed + 1))
    fi
}
need() {  # $1 source, $2 destination: a receipt that must exist
    if [ -f "$1" ]; then scrub "$1" "$2"; else echo "missing: $1"; failed=$((failed + 1)); fi
}
copy_tree() {  # $1 source directory, $2 destination under receipts, $3 find name pattern, $4 depth
    [ -d "$1" ] || return 0
    find "$1" -maxdepth "${4:-3}" -type f -name "$3" -size -200k | while read -r f; do scrub "$f" "$R/$2/${f#"$1"/}"; done
}
copy_tree "$W/gates" gates '*.txt' 1
# the firmware self-test: the final run at 4e3aab32, and the first at 0cce1525 with its two escapes
copy_tree "$W/fw2" fw '*.txt' 1
for k in 0 1 2 3; do need "$W/fw/shard-$k.txt" "$R/fw/first-run-0cce1525/shard-$k.txt"; done
need "$W/fw/head.txt" "$R/fw/first-run-0cce1525/head.txt"
# the AECP arms at the final head, and the standalone campaign
for n in 1 2; do need "$W/arm-final$n.log" "$R/gates/aecp-arms-app-if$n.txt"; done
for k in 0 1 2 3; do
    need "$W/aecp-mutants/shard-$k.log" "$R/aecp-mutants/shard-$k.log"
    need "$W/aecp-mutants/shard-$k/results.json" "$R/aecp-mutants/shard-$k-results.json"
done
# the scratch runs of the new plants (probes/subset_mutants.py), escapes included
for s in mut-sub1 mut-sub2 mut-sub3 mut-sub4; do need "$W/$s.log" "$R/aecp-mutants/scratch/$s.log"; done
for n in waiting-undo-misses-a-byte face-publishes-while-a-change-waits; do
    need "$W/mut-sub2/$n.log" "$R/aecp-mutants/scratch/escaped-in-mut-sub2-$n.log"
done
# the reviewers' probes, unmodified, at the final head
P=$W/probes/final
need "$P/head.txt" "$R/probes/head.txt"
need "$P/late-ack.log" "$R/probes/r701-4-late-ack-notify-probe.log"
need "$P/response.log" "$R/probes/r701-3-response-probe.log"
need "$P/r702-3/run.out" "$R/probes/r702-3-probe-ack.log"
need "$P/r702-4/run.out" "$R/probes/r702-4-delta-probes.out"
for n in 1 2; do need "$P/r702-4/pk/scratch/delta-probes/if$n.log" "$R/probes/r702-4-delta-probes-if$n.log"; done
sha256sum "$W/probes/r701-4/late_ack_notify_probe.py" "$W/probes/r701-4/response_probe.py" \
    "$P/r702-3/probe_ack.py" "$P/r702-4/delta_probes.py" \
    $REVIEWS/665s1-r701-4-packet/scripts/late_ack_notify_probe.py \
    $REVIEWS/665s1-r701-4-packet/scripts/response_probe.py \
    $REVIEWS/665s1-r702-4-packet/probe_ack.py \
    $REVIEWS/665s1-r702-4-packet/delta_probes.py > "$W/probes/hashes.txt"
scrub "$W/probes/hashes.txt" "$R/probes/probe-hashes.txt"
# the linked images: the final head's and the first measurement at bd0b7ff1
copy_tree "$W/img-4e3a/images" images '*.txt' 1
need "$W/img-4e3a/linked-images.txt" "$R/images/linked-images.txt"
need "$W/img-4e3a/image-points.txt" "$R/images/image-points.txt"
copy_tree "$W/img-bd0b/images" images-bd0b7ff1 '*.txt' 1
# two compactions measured on throwaway edits of the final head (restored), each still 57.5
copy_tree "$W/img-4e3a" images 'compaction-*.log' 1
# the sweep
for s in "$W"/sweep-*/; do
    s=${s%/}
    for pat in 'spec.json' 'results.json' 'complete.json' '*.log'; do copy_tree "$s" "sweep/$(basename "$s")" "$pat"; done
done
{
    echo "Files over 200 KB left out of receipts/ (size in bytes, sha256), from the work directory:"
    find "$W"/gates "$W"/fw "$W"/fw2 "$W"/sweep-* "$W"/aecp-mutants "$W"/probes/final -maxdepth 4 -type f -size +200k 2>/dev/null \
        | sort | while read -r f; do
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
