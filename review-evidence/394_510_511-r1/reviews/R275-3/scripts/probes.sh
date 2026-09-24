#!/usr/bin/env bash
# Disposable fault probes: each seeds one composition-shaped defect in a
# tracked file, runs the gate that should see it, and restores the exact
# head bytes with git checkout. A probe is KILLED when the gate fails.
#   probes.sh <repo> <outdir>
set -u
repo=$1; out=$2
mkdir -p "$out"
cd "$repo" || exit 2
summary="$out/PROBES.tsv"
printf 'probe\tgate_rc\tresult\n' > "$summary"
probe() {
    local name=$1 file=$2 script=$3; shift 3
    local log="$out/$name.log"
    python3 - "$file" "$script" > "$log" 2>&1 <<'EOF'
import sys, re
path, expr = sys.argv[1], sys.argv[2]
old, new = expr.split('\x1f')
text = open(path, encoding='utf-8').read()
if old not in text:
    sys.exit('seed text not found: ' + old)
open(path, 'w', encoding='utf-8').write(text.replace(old, new, 1))
print('seeded', path)
EOF
    local seed=$?
    if [ $seed -ne 0 ]; then
        printf '%s\t-\tSEED-FAILED\n' "$name" >> "$summary"
        git checkout -- "$file"; return
    fi
    { printf '$ %s\n' "$*"; "$@"; } >> "$log" 2>&1
    local rc=$?
    git checkout -- "$file"
    if [ $rc -ne 0 ]; then r=KILLED; else r=SURVIVED; fi
    printf '%s\t%s\t%s\n' "$name" "$rc" "$r" >> "$summary"
}
US=$'\x1f'
old=c1b617435824929a790739ea8585c3fe1a328cc0
new=e5dcea6e351abff18a27a00f8e345f3251bdbd8f
# P1: the pin table reverted to the PR source's own pin.
probe p1_stale_pin_table docs/reference/SUBMODULES.md \
  "| \`gptp-processor\` | \`$new\`${US}| \`gptp-processor\` | \`$old\`" \
  python3 scripts/check_submodule_docs.py
# P2: an engine-guide link in the composed GPTP_PLANE table left at the old pin.
probe p2_stale_engine_link docs/design/GPTP_PLANE.md \
  "FPGA-gPTP/blob/$new/docs/MANAGER.md${US}FPGA-gPTP/blob/$old/docs/MANAGER.md" \
  python3 scripts/check_gptp_docs.py
# P3: the PR's anchored heading renamed, so five inbound links dangle.
probe p3_anchor_rename docs/design/GPTP_PLANE.md \
  "### Propagation asymmetry is not modelled${US}### Propagation asymmetry is not modeled" \
  python3 scripts/check_doc_paths.py
probe p3b_anchor_rename_toc docs/design/GPTP_PLANE.md \
  "### Propagation asymmetry is not modelled${US}### Propagation asymmetry is not modeled" \
  python3 scripts/gen_toc.py --verify-anchors
# P4: an em dash on the PR's added TIME_SYNC line.
probe p4_em_dash docs/design/TIME_SYNC.md \
  "- Link delay asymmetry is not modelled; it is zero (#511).${US}- Link delay asymmetry is not modelled — it is zero (#511)." \
  python3 scripts/check_em_dash.py --base 70da0bcdf7896b26efb4cc3f854c17a02f2c4126
# P5: a recommended MVU command claimed served in the generated fact block.
probe p5_feature_fact docs/reference/MILAN_FEATURE_STATUS.md \
  "- \`GET_MILAN_INFO\`${US}- \`GET_MILAN_INFO\`
- \`GET_SYSTEM_UNIQUE_ID\`" \
  python3 scripts/check_feature_status.py
# P6: the FR_NFR contents entry desynchronised from its heading.
probe p6_toc_label docs/reference/FR_NFR.md \
  "(#5-steps-to-comply-with-milan-v12-procedure)${US}(#5-steps-to-comply-with-milan-v12-procedur)" \
  python3 scripts/gen_toc.py --check
cat "$summary"
