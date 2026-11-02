#!/bin/bash
# Copy the final gates' logs into receipts/gates, scratch and home paths replaced; a log over 200 KB keeps its first
# 40 and last 120 lines, with the whole log's sha256 and size beside it.
# usage: collect_gates.sh HEAD
set -u
H=$1
T=$VALIDATION_STORAGE/665s2b-a683p
S=$MANAGEMENT/2026-09-23/665s2b-a683p/scripts
G=$MANAGEMENT/2026-09-23/665s2b-a683p/receipts/gates
scrub() { sed -e "s#$T#<scratch>#g" -e "s#$LANES/#<lanes>/#g" -e "s#$VALIDATION_TOOLS#<tools>#g" \
  -e "s#$VALIDATION_STORAGE/scratch#<tools>#g" -e "s#$WORKSPACE_HOME#\$HOME#g"; }
keep() {  # SRC DEST
    mkdir -p "$(dirname "$2")"
    if [ "$(stat -c %s "$1")" -gt 200000 ]; then
        { echo "# cut: the first 40 and last 120 lines of $(basename "$1"); whole: $(stat -c %s "$1") bytes, sha256 $(sha256sum < "$1" | cut -c1-64)"
          head -40 "$1"; echo "# ..."; tail -120 "$1"; } | scrub > "$2"
    else
        scrub < "$1" > "$2"
    fi
}
rm -rf "$G/lane" "$G/docs" "$G/sweep" "$G/firmware"
for f in "$T/lane-logs-final3"/*; do keep "$f" "$G/lane/$(basename "$f")"; done
for f in "$T/docs-final3/logs"/*; do keep "$f" "$G/docs/logs/$(basename "$f")"; done
for f in "$T/docs-final3"/*.driver.log "$T/docs-final3/jobs.txt"; do keep "$f" "$G/docs/$(basename "$f")"; done
$VALIDATION_STORAGE/665s2b-a683o/gates/venv/bin/python3 "$S/verify_docs_yml.py" "$H" "$T/docs-final3" > "$G/docs/verify.md" 2>&1
echo "verify_docs_yml rc=$?" >> "$G/docs/verify.md"
for k in 0 1 2 3; do
    for f in "$T/sweep6/shard-$k/spec"/* "$T/sweep6/shard-$k/spec.json"; do keep "$f" "$G/sweep/shard-$k/$(basename "$f")"; done
    for f in "$T/sweep6/shard-$k/logs"/*.log "$T/sweep6/shard-$k/logs/preflight"/*.log; do
        [ -f "$f" ] && keep "$f" "$G/sweep/shard-$k/logs/${f#$T/sweep6/shard-$k/logs/}"
    done
    keep "$T/logs/fwshard-$k.log" "$G/firmware/fwshard-$k.log"
done
keep "$T/logs/nvmself.log" "$G/firmware/nvmself.log"
keep "$T/logs/imgcheck.log" "$G/image-identity.log"
du -sh "$G"
