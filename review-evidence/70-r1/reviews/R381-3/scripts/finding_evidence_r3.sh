#!/usr/bin/env bash
# R381-3: re-check R381-2 F1/F2 at the exact round-3 head.
# Usage: finding_evidence_r3.sh <parent-clone>
# Read-only: git show at fixed commits; rg over the processor submodule
# checkout, which must be clean at the pin.
set -u
C="$1"; PIN=16be6768f710e79450aace277abacd6c2c3336e5; HEAD=816c3b742940b9ac8d160ff03e05553a47e5e66d
PP="$C/protocol-processor"
D3=$(git -C "$C" show "$HEAD:docs/design/SAVED_STATE_MATERIALIZATION.md")
echo "processor HEAD $(git -C "$PP" rev-parse HEAD) (pin $PIN); porcelain $(git -C "$PP" status --porcelain | wc -l)"
# The named sweep, extracted verbatim from the head's section 15.2 code block.
SWEEPLINE=$(printf '%s\n' "$D3" | grep -E "^rg -n -U -i -C 2 '")
PAT=$(printf '%s\n' "$SWEEPLINE" | sed -E "s/^rg -n -U -i -C 2 '(.*)' docs hdl tb$/\1/")
echo "named sweep (verbatim from D3 at head): $SWEEPLINE"
OUT=$(cd "$PP" && rg -n -U -i -C 2 "$PAT" docs hdl tb)
echo "sweep output lines: $(printf '%s\n' "$OUT" | wc -l); match lines: $(printf '%s\n' "$OUT" | grep -cE '^[^:]+:[0-9]+:')"
echo
echo "== F1: every cited statement: 15.2 row for the file, location cited in a row, sweep match (':') or context ('-')"
fail=0
for spec in \
  "hdl/aecp/ucode/gen_ucode.py:1364" "hdl/aecp/ucode/gen_ucode.py:1439" "hdl/aecp/ucode/gen_ucode.py:1675" \
  "hdl/aecp/ucode/gen_ucode.py:1791" "hdl/aecp/ucode/gen_ucode.py:1925" "hdl/aecp/ucode/gen_ucode.py:2002" \
  "hdl/aecp/ucode/gen_ucode.py:2091" "hdl/aecp/ucode/gen_ucode.py:1582" "hdl/aecp/ucode/gen_ucode.py:1583" \
  "hdl/aecp/ucode/gen_ucode.py:1584" \
  "docs/architecture/06_aecp_engine.md:342" "docs/architecture/06_aecp_engine.md:343" \
  "docs/architecture/06_aecp_engine.md:365" "docs/architecture/06_aecp_engine.md:423" "docs/architecture/06_aecp_engine.md:424" \
  "docs/00_MILAN_COMPLIANCE_REVIEW.md:208" \
  "docs/architecture/03_packet_engine.md:236" \
  "docs/architecture/02_interfaces.md:492" "docs/architecture/02_interfaces.md:493" \
  "hdl/top/protocol_processor_top.sv:2450" "hdl/top/protocol_processor_top.sv:2451" \
  "tb/acmp_nvm/README.md:15" \
  "hdl/packet_engine/KL_pp_nvm_mgr_arb.sv:15" "hdl/packet_engine/KL_pp_nvm_mgr_arb.sv:16" ; do
  f=${spec%%:*}; l=${spec##*:}
  txt=$(git -C "$PP" show "$PIN:$f" | sed -n "${l}p" | sed -E 's/^[[:space:]]+//' | cut -c1-110)
  rows=$(printf '%s\n' "$D3" | grep -c "blob/$PIN/$f)")
  # Does any row for this file cite a line range containing l?
  cited=$(printf '%s\n' "$D3" | grep "blob/$PIN/$f)" | awk -F'|' '{print $3}' | python3 -c "
import re,sys
l=int(sys.argv[1]); hit=0
# Only numbers introduced by 'line'/'lines', including lists such as
# 'lines 1364, 1439 and 2091'; section numbers like '6.4' are not lines.
for cell in sys.stdin:
    for run in re.findall(r'lines? ((?:\d+(?:-\d+)?(?:, | and |,? and )?)+)', cell):
        for a,b in re.findall(r'(\d+)(?:-(\d+))?', run):
            a=int(a); b=int(b) if b else a
            if a<=l<=b: hit=1
print(hit)" "$l")
  if printf '%s\n' "$OUT" | grep -qE "^$f:$l:"; then sw=MATCH; elif printf '%s\n' "$OUT" | grep -qE "^$f-$l-"; then sw=context; else sw=ABSENT; fi
  [ "$rows" -gt 0 ] && [ "$cited" = 1 ] && [ "$sw" != ABSENT ] || fail=1
  echo "$f:$l | rows $rows | line cited $cited | sweep $sw | $txt"
done
echo "F1 location check: $([ $fail = 0 ] && echo ALL COVERED || echo GAP)"
echo
echo "-- R381-3 independent residuals (not in either round-2 list): row for file, sweep status"
for spec in "tb/acmp_nvm/acmp_nvm_wrap.sv:12" "tb/acmp_nvm/acmp_nvm_wrap.sv:13" \
  "hdl/aecp/ucode/gen_ucode.py:472" "docs/architecture/06_aecp_engine.md:874" \
  "hdl/packet_engine/KL_pp_nvm_port.sv:25"; do
  f=${spec%%:*}; l=${spec##*:}
  txt=$(git -C "$PP" show "$PIN:$f" | sed -n "${l}p" | sed -E 's/^[[:space:]]+//' | cut -c1-110)
  rows=$(printf '%s\n' "$D3" | grep -c "blob/$PIN/$f)")
  if printf '%s\n' "$OUT" | grep -qE "^$f:$l:"; then sw=MATCH; elif printf '%s\n' "$OUT" | grep -qE "^$f-$l-"; then sw=context; else sw=ABSENT; fi
  echo "$f:$l | rows $rows | sweep $sw | $txt"
done
echo
echo "-- gen_ucode.py: every NVM_MARK site at the pin versus the row's cited list"
git -C "$PP" show "$PIN:hdl/aecp/ucode/gen_ucode.py" | grep -n "u('NVM_MARK'" | sed -E 's/  +/ /g'
echo
echo "-- mark rows: 'stay' and 'never/stop being persistence triggers' wording"
printf '%s\n' "$D3" | grep -n -E 'stop being persistence triggers|never persistence triggers' | sed -E 's/\]\([^)]*\)/]/g' | cut -c1-200
echo
echo "-- exemption text at head (must not cover trigger-describing comments)"
printf '%s\n' "$D3" | grep -n -E 'Microprogram mark|exemption never covers|Every omitted match|microprogram marks stay valid|do not need rewriting'
echo
echo "== F2: DR2c-carrier on all four pages"
for f in docs/design/SAVED_STATE_FASTCONNECT.md docs/design/SAVED_STATE_MATERIALIZATION.md docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md docs/integration/BAREMETAL_FIRMWARE.md; do
  t=$(git -C "$C" show "$HEAD:$f")
  echo "$f: ruling link $(printf '%s\n' "$t" | grep -c 'issuecomment-5863247772') | 9.2 anchor links $(printf '%s\n' "$t" | grep -c '#92-when-it-sets-when-it-is-revoked-and-when-the-loss-is-forgiven') | 'only reset-sticky' $(printf '%s\n' "$t" | grep -ciE 'only (the port.s )?(`nvm_alarm` is )?reset-sticky|only reset-sticky') | never clears nvm_alarm $(printf '%s\n' "$t" | grep -cE 'never clears? `nvm_alarm`|cannot clear it|never clear `nvm_alarm`') | stale-clears-on-success $(printf '%s\n' "$t" | grep -cE 'clears `nvm_stale`|clear `nvm_stale`')"
done
echo "-- residual un-carried alarm wording (expect none):"
for f in docs/design/SAVED_STATE_FASTCONNECT.md docs/design/SAVED_STATE_MATERIALIZATION.md docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md docs/integration/BAREMETAL_FIRMWARE.md; do
  git -C "$C" show "$HEAD:$f" | grep -n -E 'Exhaustion keeps the alarm|The alarm remains until reset|reset-only alarm|Clear an exhausted alarm|firmware alarm' | sed "s|^|$f:|"
done
echo "-- lane-2 negative control and required recovery (D3 18.2):"
printf '%s\n' "$D3" | grep -n -E 'Clear `nvm_alarm` on heartbeat|Drive producer exhaustion|For firmware loss alone|That required recovery is not a negative control'
echo "-- FASTCONNECT 9.2 recovery rule and section 16 Recovery line (unchanged normative oracle):"
git -C "$C" show "$HEAD:docs/design/SAVED_STATE_FASTCONNECT.md" | grep -n -E "^stale' |^backed' |^\*\*Clears\*\* on any of|Recovery|A healed outage" | cut -c1-200
exit $fail
