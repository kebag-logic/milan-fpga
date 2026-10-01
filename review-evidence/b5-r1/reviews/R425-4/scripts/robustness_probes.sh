#!/usr/bin/env bash
# Fault probes on the page's reproduction steps, on a fresh copy of the pinned dirs.
# usage: robustness_probes.sh <git-repo-holding-8e6be432> <work-dir>
set -uo pipefail
repo=$(realpath "$1") work=$(realpath -m "$2")
rm -rf "$work"; mkdir -p "$work"
git -C "$repo" archive 8e6be4329008137a152f9171638e48a43e549fb7 review-evidence/b5-r1/author \
  review-evidence/b5-r1/author-r2 review-evidence/b5-r1/author-r3 | tar -x -C "$work"
b=$work/review-evidence/b5-r1; r=$b/author-r2/receipts
echo "## P1: gunzip -k without -f beside the masked copy"
(cd "$r" && gunzip -k a-long-reads.u16.gz </dev/null >/dev/null 2>&1); echo "rc=$?"
echo "## P2: step 2 on the MASKED copy (reader skipped step 1)"
python3 -I "$b/author-r2/tools/b5_attrib.py" figures "$b/author" "$r" > "$work/p2.out" 2> "$work/p2.err"; echo "rc=$?"
cmp -s "$work/p2.out" "$r/attribution.txt" && echo "output equals attribution.txt" || echo "output differs from attribution.txt ($(diff "$work/p2.out" "$r/attribution.txt" | grep -c '^[<>]') differing lines); stderr: $(tail -1 "$work/p2.err")"
echo "## P3: step 3 on the MASKED copy"
python3 -I "$b/author-r3/tools/b5_round3.py" figures "$b/author" "$r" > "$work/p3.out" 2> "$work/p3.err"; echo "rc=$?"
cmp -s "$work/p3.out" "$b/author-r3/receipts/round3_figures.txt" && echo "output equals round3_figures.txt" || echo "output differs ($(diff "$work/p3.out" "$b/author-r3/receipts/round3_figures.txt" | grep -c '^[<>]') differing lines); stderr: $(tail -1 "$work/p3.err")"
echo "## P4: steps 1-3 run from an unrelated working directory"
(cd "$r" && gunzip -kf a-long-reads.u16.gz)
(cd / && python3 -I "$b/author-r2/tools/b5_attrib.py" figures "$b/author" "$r" | cmp -s - "$r/attribution.txt"); echo "attribution identical rc=$?"
(cd / && python3 -I "$b/author-r3/tools/b5_round3.py" figures "$b/author" "$r" | cmp -s - "$b/author-r3/receipts/round3_figures.txt"); echo "round3 identical rc=$?"
echo "## P5: a one-byte change to the restored record is detected by the receipts"
python3 - "$r/a-long-reads.u16" <<'PY'
import sys; p=sys.argv[1]; b=bytearray(open(p,'rb').read()); b[1000]^=1; open(p,'wb').write(b)
PY
python3 -I "$b/author-r2/tools/b5_attrib.py" figures "$b/author" "$r" 2>/dev/null | cmp -s - "$r/attribution.txt"; echo "attribution identical after a 1-bit flip rc=$? (nonzero = detected)"
echo "## P6: the unmasked-figure inputs the tools read, masked in the archive?"
python3 - "$b" <<'PY'
import json,sys
b=sys.argv[1]
s=json.load(open(b+"/author/summary/a-long/summary.json"))
print("summary.json channel_identification:", s["channel_identification"])
PY
