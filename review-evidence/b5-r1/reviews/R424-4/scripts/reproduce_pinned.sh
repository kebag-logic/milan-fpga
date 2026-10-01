#!/usr/bin/env bash
# Re-run the reproduction steps of docs/findings/117_AUDIO_CONTINUITY.md
# ("Artifact hashes", steps 1 to 3) from the three packet directories at the
# pinned archive commit alone.
#
# usage: reproduce_pinned.sh <git-dir holding the archive commit> <work-dir>
# The work dir must not exist; it receives a fresh extraction.
set -euo pipefail

readonly PIN=8e6be4329008137a152f9171638e48a43e549fb7
readonly RECORD_SHA=2183d57f0646cf94405b95aea5547b83f5ff0b9190ac0bd1bdcc87760c919961

git_dir=$1
work=$2
[[ -e $work ]] && { echo "refusing: $work exists" >&2; exit 2; }
mkdir -p "$work"

git --git-dir="$git_dir" cat-file -e "${PIN}^{commit}"
git --git-dir="$git_dir" archive "$PIN" \
    review-evidence/b5-r1/author review-evidence/b5-r1/author-r2 \
    review-evidence/b5-r1/author-r3 review-evidence/b5-r1/MANIFEST.json |
    tar -x -C "$work"
root=$work/review-evidence/b5-r1
echo "pin: $PIN"
echo "extracted files: $(find "$root" -type f | wc -l)"

# Every extracted packet file must match its published_sha256 in the manifest.
python3 - "$root" <<'EOF'
import hashlib, json, os, sys
root = sys.argv[1]
man = {e["file"]: e for e in json.load(open(os.path.join(root, "MANIFEST.json")))}
bad = checked = 0
for d in ("author", "author-r2", "author-r3"):
    for dp, _, fs in os.walk(os.path.join(root, d)):
        for f in fs:
            rel = os.path.relpath(os.path.join(dp, f), root)
            h = hashlib.sha256(open(os.path.join(dp, f), "rb").read()).hexdigest()
            e = man.get(rel)
            checked += 1
            if e is None or e["published_sha256"] != h:
                bad += 1
                print("MISMATCH", rel)
print(f"manifest published_sha256 check: {checked} files, {bad} mismatches")
sys.exit(1 if bad else 0)
EOF

lane=$root/author
rec=$root/author-r2/receipts
r3=$root/author-r3

# Step 1: restore the read record and check its hash.
masked_sha=$(sha256sum "$rec/a-long-reads.u16" | cut -d' ' -f1)
echo "published (masked) a-long-reads.u16 before gunzip: $masked_sha"
(cd "$rec" && gunzip -kf a-long-reads.u16.gz)
got=$(sha256sum "$rec/a-long-reads.u16" | cut -d' ' -f1)
echo "step 1 a-long-reads.u16 after gunzip: $got bytes=$(stat -c %s "$rec/a-long-reads.u16")"
[[ $got == "$RECORD_SHA" ]] && echo "step 1: PASS" || { echo "step 1: FAIL"; exit 1; }

# Step 2: b5_attrib.py figures equals attribution.txt.
python3 "$root/author-r2/tools/b5_attrib.py" figures "$lane" "$rec" > "$work/attribution.out"
if cmp "$work/attribution.out" "$rec/attribution.txt"; then
    echo "step 2: PASS $(sha256sum < "$work/attribution.out" | cut -d' ' -f1)"
else
    echo "step 2: FAIL"; diff "$work/attribution.out" "$rec/attribution.txt" | head; exit 1
fi

# Step 3: b5_round3.py figures equals round3_figures.txt.
python3 "$r3/tools/b5_round3.py" figures "$lane" "$rec" > "$work/round3.out"
if cmp "$work/round3.out" "$r3/receipts/round3_figures.txt"; then
    echo "step 3: PASS $(sha256sum < "$work/round3.out" | cut -d' ' -f1)"
else
    echo "step 3: FAIL"; diff "$work/round3.out" "$r3/receipts/round3_figures.txt" | head; exit 1
fi

# The tools must have read the masked inputs: show they are the path_redacted copies.
python3 - "$root" <<'EOF'
import json, os, sys
root = sys.argv[1]
man = {e["file"]: e for e in json.load(open(os.path.join(root, "MANIFEST.json")))}
for f in ("author/summary/a-long/summary.json", "author/runs/a-long/events.jsonl",
          "author/summary/a-long/continuity-events.csv", "author/restore/peer-descs-2.jsonl"):
    e = man[f]
    print(f, "path_redacted" if e["path_redacted"] else "unmasked",
          "original==published" if e["original_sha256"] == e["published_sha256"] else "original!=published")
EOF
echo "reproduction: ALL PASS"
