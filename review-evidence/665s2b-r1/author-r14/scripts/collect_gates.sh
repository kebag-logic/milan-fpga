#!/bin/bash
# Copy the final head's gate logs into receipts/gates, scratch and home paths replaced; a log over 200 KB keeps its
# first 40 and last 120 lines, with the whole log's sha256 and size beside it.
# usage: collect_gates.sh HEAD [RECEIPTS_GATES_DIR]
set -u
H=$1
T=$VALIDATION_STORAGE/665s2b-a683q
S=$MANAGEMENT/2026-09-23/665s2b-a683q/scripts
G=${2:-$MANAGEMENT/2026-09-23/665s2b-a683q/receipts/gates}
scrub() { sed -e "s#$T#<scratch>#g" -e "s#$VALIDATION_STORAGE#<tmp>#g" -e "s#$LANES/#<lanes>/#g" \
  -e "s#$VALIDATION_TOOLS#<tools>#g" -e "s#$VALIDATION_STORAGE/scratch#<tools>#g" -e "s#$WORKSPACE_HOME#\$HOME#g" \
  -e "s#/tmp/[session]-[0-9]*#<tmp>#g"; }
keep() {  # SRC DEST
    mkdir -p "$(dirname "$2")"
    if [ "$(stat -c %s "$1")" -gt 200000 ]; then
        { echo "# cut: the first 40 and last 120 lines of $(basename "$1"); whole: $(stat -c %s "$1") bytes, sha256 $(sha256sum < "$1" | cut -c1-64)"
          head -40 "$1"; echo "# ..."; tail -120 "$1"; } | scrub > "$2"
    else
        scrub < "$1" > "$2"
    fi
}
rm -rf "$G"
for f in "$T/lane-logs-q2"/*; do keep "$f" "$G/lane/$(basename "$f")"; done
for f in "$T/gates/docs-q2/logs"/*; do keep "$f" "$G/docs/logs/$(basename "$f")"; done
for f in "$T/gates/docs-q2"/*.driver.log "$T/gates/docs-q2/jobs.txt"; do keep "$f" "$G/docs/$(basename "$f")"; done
$VALIDATION_STORAGE/665s2b-a683o/gates/venv/bin/python3 "$S/verify_docs_yml.py" "$H" "$T/gates/docs-q2" > "$G/docs/verify.md" 2>&1
echo "verify_docs_yml rc=$?" >> "$G/docs/verify.md"
for k in 0 1 2 3; do
    for f in "$T/sweep2/shard-$k/spec"/* "$T/sweep2/shard-$k/logs/preflight"/*.log; do
        keep "$f" "$G/sweep-first-attempt/shard-$k/${f#$T/sweep2/shard-$k/}"
    done
    # shard 2's result is its run alone on four CPUs (sweep3-s2b); its two OOM-killed runs are kept beside it
    src=$T/sweep3/shard-$k
    [ "$k" = 2 ] && src=$T/sweep3-s2b
    for f in "$src/spec"/* "$src/spec.json"; do keep "$f" "$G/sweep/shard-$k/$(basename "$f")"; done
    for f in "$src/logs"/*.log "$src/logs/preflight"/*.log; do
        [ -f "$f" ] && keep "$f" "$G/sweep/shard-$k/logs/${f#$src/logs/}"
    done
    keep "$T/logs/fwshard-$k.log" "$G/firmware/fwshard-$k.log"
done
for run in "sweep3/shard-2:8cpu-10G" "sweep3-s2-oom24:16cpu-24G"; do
    d=$T/${run%%:*} n=${run##*:}
    for f in "$d/spec"/* "$d/spec.json" "$d/logs"/*.log; do
        [ -f "$f" ] && keep "$f" "$G/sweep-shard2-killed/$n/${f#$d/}"
    done
done
keep "$T/logs/sweep-shard2-units.txt" "$G/sweep-shard2-killed/units.txt"
for leg in G-A1 G-A8; do
    grep -v '^[│├└ ]' "$T/logs/$leg.log" > "$T/logs/$leg.receipt.log"
    keep "$T/logs/$leg.receipt.log" "$G/harness/$leg/run.log"
    keep "$T/builds/$leg/results/table.md" "$G/harness/$leg/table.md"
    keep "$T/builds/$leg/build.json" "$G/harness/$leg/build.json"
    echo "ctrl_app.elf sha256 $(sha256sum < "$T/builds/$leg/image/ctrl_app.elf" | cut -c1-64) $(stat -c %s "$T/builds/$leg/image/ctrl_app.elf") B" > "$G/harness/$leg/image.txt"
done
keep "$T/logs/imgcheck-a3f23bba.log" "$G/image-identity.log"
du -sh "$G"
