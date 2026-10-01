#!/bin/sh
# R425-5: reproduce the page's steps 1-3 from the three packet directories at
# the pinned archive commit alone, and check every packet file against the
# archive MANIFEST.json published_sha256.
# Usage: r425_5_repro.sh <archive-git-dir> <commit> <outdir>
set -eu
G=$1; C=$2; O=$3
rm -rf "$O"; mkdir -p "$O"
git -C "$G" archive "$C" review-evidence/b5-r1/author review-evidence/b5-r1/author-r2 review-evidence/b5-r1/author-r3 | tar -x -C "$O"
git -C "$G" show "$C:review-evidence/b5-r1/MANIFEST.json" > "$O/MANIFEST.json"
cd "$O/review-evidence/b5-r1"
echo "files: $(find author author-r2 author-r3 -type f | wc -l)"
python3 - "$O/MANIFEST.json" <<'EOF'
import json, hashlib, os, sys
m = {e['file']: e for e in json.load(open(sys.argv[1]))}
bad = n = 0
for d in ('author', 'author-r2', 'author-r3'):
    for r, _, fs in os.walk(d):
        for f in fs:
            p = os.path.join(r, f); n += 1
            h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
            e = m.get(p)
            if e is None or e['published_sha256'] != h:
                bad += 1; print('MISMATCH', p)
print(f'manifest check: {n} files, {bad} mismatches')
EOF
(cd author-r2/receipts && gunzip -kf a-long-reads.u16.gz && sha256sum a-long-reads.u16 && wc -c < a-long-reads.u16)
python3 -B author-r2/tools/b5_attrib.py figures author author-r2/receipts > "$O/attribution.out" 2> "$O/attribution.err"; echo "b5_attrib rc=$?"
cmp "$O/attribution.out" author-r2/receipts/attribution.txt && echo "attribution.txt: byte-identical"
python3 -B author-r3/tools/b5_round3.py figures author author-r2/receipts > "$O/round3.out" 2> "$O/round3.err"; echo "b5_round3 rc=$?"
cmp "$O/round3.out" author-r3/receipts/round3_figures.txt && echo "round3_figures.txt: byte-identical"
echo "stderr bytes: $(cat "$O/attribution.err" "$O/round3.err" | wc -c)"
sha256sum author-r2/receipts/attribution.txt author-r3/receipts/round3_figures.txt
