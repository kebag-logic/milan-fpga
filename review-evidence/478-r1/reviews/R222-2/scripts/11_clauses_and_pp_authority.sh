#!/usr/bin/env bash
# Clause text and pinned processor authority used by the Conformance and RTL
# lenses. Standards are read from local copies under $STANDARDS_DIR (default
# the reviewer's standards directory); the processor is read from the scratch
# clone's protocol-processor submodule at the parent gitlink. Read-only.
set -euo pipefail
STANDARDS_DIR=${STANDARDS_DIR:-$HOME/standards}
SC=${SCRATCH:-/tmp/r222-478-r2-scratch}
P="$SC/git-sub/protocol-processor"
PIN=424c688fa2205b934a7689a58f2aa766420f2326
pdftotext -layout "$STANDARDS_DIR/Milan_Specification_Consolidated_v1.2_Final_Approved 20231130.pdf" "$SC/milan12.txt" 2>/dev/null
pdftotext -layout "$STANDARDS_DIR/1722.1-2021.pdf" "$SC/17221_2021.txt" 2>/dev/null
echo '## Milan v1.2 (Consolidated, 2023-11-30) Section 5.3.3.3 and 5.3.5.1'
awk '/^5\.3\.3\.3 AUDIO_UNIT/{f=1} /^5\.3\.3\.4 /{f=0} f' "$SC/milan12.txt" | sed '/^$/d'
awk '/^5\.3\.5\.1 Sampling rate/{f=1} /^Note: the sampling rate/{f=0} f' "$SC/milan12.txt" | sed '/^$/d'
echo '## IEEE Std 1722.1-2021 Table 7-5 (AUDIO_UNIT), offsets 136-144'
grep -n -A1 -E '^ +(136|140|142|144) +[24]' "$SC/17221_2021.txt" | sed -n '1,12p'
echo "## protocol-processor @ $PIN"
echo "HEAD of scratch submodule: $(git -C "$P" rev-parse HEAD)"
for f in docs/architecture/07_memory_maps.md docs/architecture/06_aecp_engine.md hdl/aecp/ucode/gen_ucode.py; do
  echo "$f blob $(git -C "$P" rev-parse "$PIN:$f")"
done
echo '-- 07_memory_maps.md L10 row'
git -C "$P" show "$PIN:docs/architecture/07_memory_maps.md" | grep -n '^| L10 |'
echo '-- gen_ucode.py SSR constants and walk loop'
git -C "$P" show "$PIN:hdl/aecp/ucode/gen_ucode.py" | grep -n -E '^SSR_LIST_OFF|^SSR_WALK_MAX|^for k in range\(0, SSR_WALK_MAX, 2\)|past the bound: refused'
echo '-- builder constant and refusal at the head'
git -C "$SC/git-sub" show HEAD:sw/builder/endstation_builder.py | grep -n -E '^BASE_RATE_HZ|^MAX_AUDIO_UNIT_RATES|section 3.1, L10|if len\(rates\) > MAX_AUDIO_UNIT_RATES|if len\(set\(rates\)\) != len\(rates\)|if rate not in rates'
