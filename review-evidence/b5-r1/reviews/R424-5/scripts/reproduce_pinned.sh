#!/usr/bin/env bash
# Reproduce the page's steps 1-3 from the three packet directories at the
# pinned archive commit alone, and trace which packet files each tool opens.
# Usage: reproduce_pinned.sh <evidence-git-dir> <scratch-dir> <archive-commit>
set -euo pipefail
ev=$1 out=$2 pin=$3
rm -rf "$out" && mkdir -p "$out"
git --git-dir="$ev" archive "$pin" review-evidence/b5-r1/author \
  review-evidence/b5-r1/author-r2 review-evidence/b5-r1/author-r3 | tar -x -C "$out"
git --git-dir="$ev" show "$pin:review-evidence/b5-r1/MANIFEST.json" > "$out/MANIFEST.json"
cd "$out/review-evidence/b5-r1"
echo "pin: $pin"
echo "files extracted: $(find author author-r2 author-r3 -type f | wc -l)"
python3 - "$out/MANIFEST.json" <<'PY'
import hashlib, json, os, sys
m = {e["file"]: e for e in json.load(open(sys.argv[1]))}
n = bad = missing = 0
for top in ("author", "author-r2", "author-r3"):
    for d, _, fs in os.walk(top):
        for f in fs:
            p = os.path.join(d, f)
            n += 1
            e = m.get(p)
            if e is None:
                missing += 1; print("not in manifest:", p); continue
            if hashlib.sha256(open(p, "rb").read()).hexdigest() != e["published_sha256"]:
                bad += 1; print("published_sha256 mismatch:", p)
print(f"manifest check: {n} files, {bad} mismatches, {missing} unlisted")
red = sorted(k for k, e in m.items() if e["path_redacted"] and k.split("/")[0] in ("author", "author-r2", "author-r3"))
print(f"path_redacted files in the three directories: {len(red)}")
for k in red: print("  redacted:", k)
PY
echo "--- step 1"
(cd author-r2/receipts && gunzip -kf a-long-reads.u16.gz; echo "gunzip rc=$?"; sha256sum a-long-reads.u16; stat -c 'bytes=%s' a-long-reads.u16)
echo "--- step 2"
set +e
strace -f -qq -e trace=openat -o "$out/trace_attrib.txt" python3 author-r2/tools/b5_attrib.py figures author author-r2/receipts > "$out/attrib.out" 2> "$out/attrib.err"; echo "b5_attrib rc=$? stderr_bytes=$(stat -c %s "$out/attrib.err")"
cmp "$out/attrib.out" author-r2/receipts/attribution.txt; echo "cmp attribution.txt rc=$?"
sha256sum "$out/attrib.out" | cut -c1-64
echo "--- step 3"
strace -f -qq -e trace=openat -o "$out/trace_round3.txt" python3 author-r3/tools/b5_round3.py figures author author-r2/receipts > "$out/round3.out" 2> "$out/round3.err"; echo "b5_round3 rc=$? stderr_bytes=$(stat -c %s "$out/round3.err")"
cmp "$out/round3.out" author-r3/receipts/round3_figures.txt; echo "cmp round3_figures.txt rc=$?"
sha256sum "$out/round3.out" | cut -c1-64
set -e
echo "--- packet files opened (successful openat, relative to the archive root)"
for t in attrib round3; do
  echo "[$t]"
  grep -v ENOENT "$out/trace_$t.txt" | grep -o '"[^"]*"' | tr -d '"' \
    | grep -E '^(author|author-r2|author-r3)/' | grep -v '__pycache__' | sort -u | sed 's/^/  /'
done
