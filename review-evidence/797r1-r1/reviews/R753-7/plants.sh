#!/usr/bin/env bash
# Reviewer plants for the register reference freshness gate at one head.
# Usage: plants.sh <probe-tree (a git-initialised export of the head)> <python> <out-dir> <dev-commit-repo> <dev-sha>
# Each plant edits the probe tree, runs the gate, records rc and log, then restores with git checkout.
set -u
T=$1; PY=$2; OUT=$3; REPO=$4; DEV=$5
mkdir -p "$OUT"
cd "$T" || exit 9
CSR=hdl/common/csr/milan_csr.sv
gate() { # name, gate args...
  local n=$1; shift
  /usr/bin/git diff > "$OUT/$n.diff"
  "$PY" scripts/gen_register_reference.py "$@" > "$OUT/$n.log" 2>&1; echo $? > "$OUT/$n.rc"
  /usr/bin/git checkout -q -- . ; /usr/bin/git clean -qfd
  /usr/bin/git diff --quiet || echo "RESTORE FAILED after $n" >> "$OUT/restore.txt"
}
gate p0_control --check
# P1: dev's hand-written page (the conflict taken to dev's side)
/usr/bin/git -C "$REPO" show "$DEV:docs/reference/REGISTER_MAP.md" > docs/reference/REGISTER_MAP.md
gate p1_dev_page --check
# P2: MAC_CTRL reset 0x13 -> 0x17 in both the flop reset and the defaults ROM
sed -i '1576s/mac_ctrl <= 32'"'"'h13;/mac_ctrl <= 32'"'"'h17;/' $CSR
sed -i '2002s/csr_default = 32'"'"'h13;/csr_default = 32'"'"'h17;/' $CSR
gate p2_reset_both --check
# P3: flop reset changed but the defaults ROM left alone (expected refusal, rc 2)
sed -i '1576s/mac_ctrl <= 32'"'"'h13;/mac_ctrl <= 32'"'"'h17;/' $CSR
gate p3_reset_flop_only --check
# P4: register rename A_MAC_IFG -> A_MAC_GAP everywhere in the CSR block
sed -i 's/\bA_MAC_IFG\b/A_MAC_GAP/g' $CSR
gate p4_register_rename --check
# P5: field signal rename mac_ifg -> mac_gap everywhere in the CSR block
sed -i 's/\bmac_ifg\b/mac_gap/g' $CSR
gate p5_signal_rename --check
# P6: comment-only edit on a line that carries a // comment
L=$(grep -n '//' $CSR | head -1 | cut -d: -f1)
sed -i "${L}s|//|// reviewer plant:|" $CSR
gate p6_comment_only --check
# P7: rendered SoC fact tampered in the extract (a memory-region origin)
"$PY" - <<'EOF'
import json; p="scripts/register_map_soc.json"; d=json.load(open(p))
d["memory_regions"][0]["origin"] += 0x1000
open(p,"w").write(json.dumps(d, indent=2, sort_keys=True)+"\n")
EOF
gate p7_soc_rendered_fact --check
# P8: unrendered SoC constant tampered (station MAC back to the pre-#842 value)
"$PY" - <<'EOF'
import json; p="scripts/register_map_soc.json"; d=json.load(open(p))
d["constants"]["milan_station_mac_hi"]=256; d["constants"]["milan_station_mac_lo"]=2
open(p,"w").write(json.dumps(d, indent=2, sort_keys=True)+"\n")
EOF
gate p8_soc_unrendered_constant --check
# P9: the extract reverted wholesale to the round-6 head (pre-refresh) content
/usr/bin/git -C "$REPO" show 2c500d0a:scripts/register_map_soc.json > scripts/register_map_soc.json
gate p9_soc_pre_refresh --check
# P10: the 1de759d3 count reverted (53 -> 52, found 52 -> found 51) in the CI event selftest
sed -i 's/must carry exactly 53 steps/must carry exactly 52 steps/; s/(found 52)/(found 51)/; s/("docs-check", 53)/("docs-check", 52)/' scripts/ci_events.py
/usr/bin/git diff > "$OUT/p10_ci_events_revert.diff"
"$PY" scripts/ci_events.py --selftest > "$OUT/p10_ci_events_revert.log" 2>&1; echo $? > "$OUT/p10_ci_events_revert.rc"
/usr/bin/git checkout -q -- .
/usr/bin/git diff --quiet && echo clean > "$OUT/final_restore.txt"
