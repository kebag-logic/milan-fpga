#!/usr/bin/env bash
# Disposable probes that show the checks this review relies on can fail.
# Usage: mutation_probe.sh <review-clone> <python> <repro-root> <scratch>
set -uo pipefail
clone=$1 py=$2 repro=$3 scratch=$4
b5="$repro/review-evidence/b5-r1"
echo "--- P1: one flipped byte in the restored read record must break step 2"
cp "$b5/author-r2/receipts/a-long-reads.u16" "$scratch/u16.bak"
printf '\xff' | dd of="$b5/author-r2/receipts/a-long-reads.u16" bs=1 seek=65536 count=1 conv=notrunc status=none
(cd "$b5" && python3 author-r2/tools/b5_attrib.py figures author author-r2/receipts 2>/dev/null | cmp -s - author-r2/receipts/attribution.txt); echo "mutated cmp rc=$? (non-zero expected)"
cp "$scratch/u16.bak" "$b5/author-r2/receipts/a-long-reads.u16"
(cd "$b5" && python3 author-r2/tools/b5_attrib.py figures author author-r2/receipts 2>/dev/null | cmp -s - author-r2/receipts/attribution.txt); echo "restored cmp rc=$? (0 expected)"
echo "--- P2: the masked-by-step-1 copy (gunzip without -f) must not reproduce"
git --git-dir="$scratch/ev.git" show 9006c78e354d5a2f244fd606c55790a825304bd3:review-evidence/b5-r1/author-r2/receipts/a-long-reads.u16 > "$b5/author-r2/receipts/a-long-reads.u16"
echo "published masked copy sha256 prefix: $(sha256sum "$b5/author-r2/receipts/a-long-reads.u16" | cut -c1-8)"
(cd "$b5" && python3 author-r2/tools/b5_attrib.py figures author author-r2/receipts 2>/dev/null | cmp -s - author-r2/receipts/attribution.txt); echo "masked-copy cmp rc=$? (non-zero expected)"
cp "$scratch/u16.bak" "$b5/author-r2/receipts/a-long-reads.u16"
echo "restored sha256 prefix: $(sha256sum "$b5/author-r2/receipts/a-long-reads.u16" | cut -c1-8)"
echo "--- P3: a broken intra-page anchor, then a broken cross-page link, on the page (probe clone)"
probe="$scratch/probe"; rm -rf "$probe"
git clone -q --shared --no-checkout "$clone" "$probe" && git -C "$probe" checkout -q --detach e5ad118783c2ff96e13f1d794f10bf2b63741282
sed -i 's|(#artifact-hashes)\.|(#artifact-hashes-missing).|' "$probe/docs/findings/117_AUDIO_CONTINUITY.md"
echo "probe lines changed: $(git -C "$probe" diff --numstat | awk '{print $1}')"
(cd "$probe" && "$py" -B scripts/docs_check.py >/dev/null 2>&1); echo "docs_check on broken intra-page anchor rc=$? (recorded: 0 means the gate does not judge intra-page anchors)"
(cd "$probe" && "$py" -B scripts/gen_toc.py --verify-anchors >/dev/null 2>&1); echo "gen_toc --verify-anchors on mutated page rc=$?"
git -C "$probe" checkout -q -- docs/findings/117_AUDIO_CONTINUITY.md
sed -i 's|(451_TDM8_FIRST_LIGHT.md#method)|(451_TDM8_FIRST_LIGHT_MISSING.md#method)|' "$probe/docs/findings/117_AUDIO_CONTINUITY.md"
echo "probe lines changed: $(git -C "$probe" diff --numstat | awk '{print $1}')"
(cd "$probe" && "$py" -B scripts/docs_check.py >/dev/null 2>&1); echo "docs_check on broken cross-page link rc=$? (non-zero expected)"
git -C "$probe" checkout -q -- docs/findings/117_AUDIO_CONTINUITY.md
(cd "$probe" && "$py" -B scripts/docs_check.py >/dev/null 2>&1); echo "docs_check on restored probe rc=$? (0 expected)"
echo "--- P4: a withheld size planted back into a copy of the head page must hit the size scan"
cp "$clone/docs/findings/117_AUDIO_CONTINUITY.md" "$scratch/p4.md"
old="$scratch/scan/page_e216dfe4.md"
"$py" - "$old" "$scratch/p4.md" <<'PY'
import re, sys
old, new = sys.argv[1:3]
row = re.search(r"^\| `diag1` every channel, 25 s \| ([0-9]+) \|", open(old).read(), re.M).group(1)
t = open(new).read().replace("| `diag1` every channel, 25 s | withheld |", "| `diag1` every channel, 25 s | %s |" % row, 1)
open(new, "w").write(t)
PY
"$py" "$(dirname "$0")/size_scan.py" "$old" "$scratch/p4.md" | sed -n '/p4.md/,$p'
rm -f "$scratch/p4.md"
