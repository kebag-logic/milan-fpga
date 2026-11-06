#!/bin/bash
# Copy the final head's gate logs into receipts/gates, scratch and home paths replaced; a log over 200 KB keeps its
# first 40 and last 120 lines, with the whole log's sha256 and size beside it.
# usage: collect_gates16.sh HEAD [RECEIPTS_GATES_DIR]
set -u
H=$1
T=$VALIDATION_STORAGE/665s2b-a683u
S=$MANAGEMENT/2026-09-23/665s2b-a683u/scripts
G=${2:-$MANAGEMENT/2026-09-23/665s2b-a683u/receipts/gates}
scrub() { sed -e "s#$T#<scratch>#g" -e "s#$VALIDATION_STORAGE#<tmp>#g" -e "s#$LANES/#<lanes>/#g" \
  -e "s#$VALIDATION_TOOLS#<tools>#g" -e "s#$VALIDATION_STORAGE/scratch#<tools>#g" -e "s#$WORKSPACE_HOME#\$HOME#g" \
  -e "s#/tmp/<session>-[0-9]*#<tmp>#g"; }
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
for f in "$T/lane-logs-final2"/*; do keep "$f" "$G/lane/$(basename "$f")"; done
for f in "$T/docs-$H/logs"/*; do keep "$f" "$G/docs/logs/$(basename "$f")"; done
for f in "$T/docs-$H"/*.driver.log "$T/docs-$H/jobs.txt" "$T/docs-$H/verify.log"; do keep "$f" "$G/docs/$(basename "$f")"; done
for k in 0 1 2 3; do
    src=$T/sweep-final/shard-$k
    for f in "$src/spec"/* "$src/spec.json"; do [ -f "$f" ] && keep "$f" "$G/sweep/shard-$k/$(basename "$f")"; done
    for f in "$src/logs"/*.log "$src/logs/preflight"/*.log; do
        [ -f "$f" ] && keep "$f" "$G/sweep/shard-$k/logs/${f#$src/logs/}"
    done
    keep "$T/logs/fwshard-$k.log" "$G/firmware/fwshard-$k.log"
done
for leg in G-A1 G-A8; do
    for f in "$T/logs/$leg.log" "$T/logs/${leg}h.log" "$T/logs/${leg}h2.log" "$T/logs/$leg-finish.log" "$T/logs/$leg-regrade.log"; do
        [ -f "$f" ] || continue
        grep -v '^[│├└ ]' "$f" > "$T/logs/receipt.tmp"
        keep "$T/logs/receipt.tmp" "$G/harness/$leg/$(basename "$f" | sed "s/^$leg-//; s/^$leg\.log$/run.log/")"
    done
    keep "$T/builds/$leg/results/table.md" "$G/harness/$leg/table.md"
    keep "$T/builds/$leg/build.json" "$G/harness/$leg/build.json"
    echo "ctrl_app.elf sha256 $(sha256sum < "$T/builds/$leg/image/ctrl_app.elf" | cut -c1-64) $(stat -c %s "$T/builds/$leg/image/ctrl_app.elf") B" > "$G/harness/$leg/image.txt"
done
keep "$T/logs/imgcheck.log" "$G/image-identity.log"
# the runs a host reset cut (2026-11-05 13:10): docs.yml's job list and the sweep's shard specs, kept for the record
keep "$T/docs-$H-killed/jobs.txt" "$G/killed/docs-jobs.txt"
for k in 0 1 2 3; do keep "$T/sweep-d930ea98-killed/shard-$k/spec.json" "$G/killed/sweep-shard-$k-spec.json"; \
    ls "$T/sweep-d930ea98-killed/shard-$k/logs" > "$T/logs/receipt.tmp"; keep "$T/logs/receipt.tmp" "$G/killed/sweep-shard-$k-logs.txt"; done
keep "$T/logs/dispatch.txt" "$G/dispatch.txt"
# docs.yml's first docs-gates-0 at the head, gate_13 rc 1 on a venv without wavedrom, and that run's verifier
for f in "$T/docs-$H/first-run/logs/docs-gates-0__gate_13.log" "$T/docs-$H/first-run/logs/docs-gates-0__gate_13.rc" \
         "$T/docs-$H/first-run/verify.log" "$T/docs-$H/first-run/docs-gates-0.driver.log"; do
    keep "$f" "$G/docs/first-run/$(basename "$f")"; done
du -sh "$G"
