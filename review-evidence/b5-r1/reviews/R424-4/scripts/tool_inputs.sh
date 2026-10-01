#!/usr/bin/env bash
# Which packet files does each published figures command open? An openat
# system-call trace of each command over the pinned packets (after step 1).
# usage: tool_inputs.sh <extracted review-evidence/b5-r1 at the pin, after step 1> <scratch-dir>
set -euo pipefail
r=$1 tmp=$2
mkdir -p "$tmp"
echo "# packet files opened by each figures command (openat system-call trace; .py files omitted)"
echo "## b5_attrib.py figures <lane packet> <round 2 receipts>"
strace -f -e trace=openat -o "$tmp/st1.txt" python3 "$r/author-r2/tools/b5_attrib.py" figures "$r/author" "$r/author-r2/receipts" > /dev/null
grep -o '"[^"]*b5-r1/[^"]*"' "$tmp/st1.txt" | sed 's#.*b5-r1/##; s#"##' | grep -v '\.py$' | sort -u
echo "## b5_round3.py figures <lane packet> <round 2 receipts>"
strace -f -e trace=openat -o "$tmp/st2.txt" python3 "$r/author-r3/tools/b5_round3.py" figures "$r/author" "$r/author-r2/receipts" > /dev/null
grep -o '"[^"]*b5-r1/[^"]*"' "$tmp/st2.txt" | sed 's#.*b5-r1/##; s#"##' | grep -v '\.py$' | sort -u
echo "## events.jsonl opened by either: $(grep -c 'events.jsonl' "$tmp/st1.txt" "$tmp/st2.txt" | tr '\n' ' ')"
