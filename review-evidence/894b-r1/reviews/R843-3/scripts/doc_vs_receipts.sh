#!/bin/sh
# Section 13's 8x8/1if figures at the head beside the author's round-5/6 receipts of the head's image
# (arguments: the clone at the head, the extracted review-evidence/894b-r1 directory).
set -u
C=$1; E=$2
DOC=$C/docs/design/SPLIT_CONTROL_MEMORY.md
echo "# section 13 at $(git -C "$C" rev-parse HEAD), the lines that state 8x8/1if's gate, load and every-source rows"
grep -n "^\*\*The gate at 8x8/1if\*\*\|^- \*\*The load\*\* at 8x8/1if\|^- \*\*8x8/1if's own ADP record\|^- \*\*Every row the CPU decides\|^- \*\*Join intervals:\|^- \*\*THE RETRY's rounds:\|^- \*\*The rows by every source,\|^- \*\*The load with every AECP\|^\*\*The AECP records by class at 8x8/1if" "$DOC" | cut -c1-400
grep -n "^| AECP (20) \|^| The last queued notice (130) " "$DOC"
echo
echo "# the round-6 packet's derivation at the head (model/rows-8x8-1if-af2c4d7a.txt)"
cat "$E/author-r6/receipts/model/rows-8x8-1if-af2c4d7a.txt"
echo
echo "# the round-5/6 regrade of the head's image (harness/gate-8x8-1if-regraded-af2c4d7a.txt): its header and worst rows"
sed -n '1,2p' "$E/author-r6/receipts/harness/gate-8x8-1if-regraded-af2c4d7a.txt"
grep -n "^| aecp | AECP\|^Join intervals\|^THE RETRY's rounds\|Over every group" "$E/author-r6/receipts/harness/gate-8x8-1if-regraded-af2c4d7a.txt" | cut -c1-200
echo
echo "# the head's load gate (load_grade.py --check), 8x8/1if"
grep -n "^| 8x8/1if" "$(dirname "$0")/../receipts/load-grade-check.txt" | cut -c1-80
