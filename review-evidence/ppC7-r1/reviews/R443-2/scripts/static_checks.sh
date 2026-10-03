#!/bin/sh
# Static checks for R443-2. Usage: static_checks.sh <clone at 81edaaa> [round-1 head]
set -u
C=${1:?clone}; R1=${2:-e2c7d97d158a30e44289a06a33f8ff4c5e289b87}
cd "$C" || exit 2
echo "## head"; git rev-parse HEAD HEAD^{tree}
echo "## 1. R443-1-F1 verification grep (expect no output)"
grep -rnE 'avtp\.[A-Z_]+|srp \+ avtp adapters|gptp · avtp · mclk adapters' docs
echo "rc=$?  (1 = no match)"
echo "## 2. removed adapter ops / stream-datapath requests / counter node (docs, hdl, tb sources; expect only the 06 ctr read-face node)"
grep -rnE '(avtp|mclk|gptp)\.[A-Z_]{3,}|INPUT_DISABLE|INPUT_CONFIGURE|OUTPUT_ENABLE|srp \+ avtp|avtp adapter|mclk adapter|gptp adapter|adapters -->|ctrs\[' \
  docs hdl tb --include='*.md' --include='*.sv' --include='*.py' --include='*.hpp' --include='*.cpp'
echo "## 3. 'adapter' in 01/03/05/06, docs/README, guides (srp class-B face only expected)"
grep -rniE 'adapter' docs/architecture/01_overview.md docs/architecture/03_packet_engine.md docs/architecture/05_acmp_engine.md docs/architecture/06_aecp_engine.md docs/README.md docs/guides/README.md docs/guides/integrator.md
echo "## 4. in-processor counter block wording in 01/03/05/06, docs/README, guides/README"
grep -rniE 'counter (bank|block|ram|rom)|counters? (subsystem|engine)|mask rom|counter-mask' docs/architecture/01_overview.md docs/architecture/03_packet_engine.md docs/architecture/05_acmp_engine.md docs/architecture/06_aecp_engine.md docs/README.md docs/guides/README.md
echo "## 5. mask ROM anywhere"
grep -rniE 'mask[_ -]?rom' docs hdl
echo "## 6. GPTP_GM_CHANGED statements"
grep -rn 'GPTP_GM_CHANGED' docs
echo "## 7. RTL lines changed this round that are not comments (expect none)"
git diff -U0 "$R1" HEAD -- hdl | grep '^[+-][^+-]' | grep -vE '^[+-]\s*(//|.*//[!]? )'
echo "## 8. anchors/headings changed this round"
for f in $(git diff --name-only "$R1" HEAD -- '*.md'); do
  a=$(git show "$R1:$f" | grep -oE '<a id="[^"]+"|^#+ .*' | sort); b=$(git show "HEAD:$f" | grep -oE '<a id="[^"]+"|^#+ .*' | sort)
  [ "$a" = "$b" ] || { echo "== $f"; diff <(echo "$a") <(echo "$b"); }
done 2>/dev/null || true
echo "## 9. E_GCTRS / E_GCTRSNS listing"
sed -n '/^place(E_GCTRS, \[/,/^\])/p;/^place(E_GCTRSNS, \[/,/^\])/p' hdl/aecp/ucode/gen_ucode.py
echo "## 10. notify slot decode"
sed -n '/counter_event_map/,/^  end/p' hdl/aecp/KL_aecp_notify.sv
