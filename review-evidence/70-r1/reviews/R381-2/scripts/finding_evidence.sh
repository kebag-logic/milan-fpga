#!/usr/bin/env bash
# Reproduce R381-2 finding evidence. Usage: finding_evidence.sh <parent-clone>
# Read-only: uses git show / git grep at fixed commits only.
set -u
C="$1"; PIN=16be6768f710e79450aace277abacd6c2c3336e5; HEAD=e796c68a460fe6946e28cb9da0349a382c868352
PP="$C/protocol-processor"
SWEEP='COMMIT.*NVM_MARK|aecp_dyn_dirty_o|nvm_unflushed_o|d3_unflushed_o|restore_(done|fail|blank)_o|T-NVM|RETRY_MAX_P|DEB_TICKS_P|entity_enable|Nothing in the processor|groups 6 and 7|integrating platform'
echo "processor HEAD $(git -C "$PP" rev-parse HEAD) (pin $PIN)"
echo "== F1: statements at the pin that D3 falsifies (mark as persistence trigger; manager 1 owned by the platform; NVM never delays responses)"
for spec in \
  "hdl/aecp/ucode/gen_ucode.py:2091" \
  "hdl/aecp/ucode/gen_ucode.py:1364" \
  "hdl/aecp/ucode/gen_ucode.py:1791" \
  "docs/architecture/06_aecp_engine.md:342" \
  "docs/architecture/06_aecp_engine.md:365" \
  "docs/architecture/06_aecp_engine.md:423" \
  "docs/00_MILAN_COMPLIANCE_REVIEW.md:208" \
  "hdl/top/protocol_processor_top.sv:2450" \
  "tb/acmp_nvm/README.md:15" \
  "docs/architecture/03_packet_engine.md:236" ; do
  f=${spec%%:*}; l=${spec##*:}
  txt=$(git -C "$PP" show "$PIN:$f" | sed -n "${l}p")
  inTable=$(git -C "$C" show "$HEAD:docs/design/SAVED_STATE_MATERIALIZATION.md" | grep -c "blob/$PIN/$f)")
  sweep=$(printf '%s\n' "$txt" | grep -cE "$SWEEP")
  echo "$f:$l | rows for file in 15.2: $inTable | matched by the named sweep: $sweep"
  echo "    $txt"
done
echo "-- 15.2 row locations for the files above that do have rows:"
git -C "$C" show "$HEAD:docs/design/SAVED_STATE_MATERIALIZATION.md" | grep -E "blob/$PIN/(docs/architecture/06_aecp_engine.md|docs/00_MILAN_COMPLIANCE_REVIEW.md|hdl/top/protocol_processor_top.sv|tb/acmp_nvm/README.md)\)" | awk -F'|' '{print "   ", $2 "|" $3}' | sed -E 's/\[([^]]+)\]\([^)]*\)/\1/'
echo "-- D3 rule that falsifies them:"
git -C "$C" show "$HEAD:docs/design/SAVED_STATE_MATERIALIZATION.md" | sed -n '292,296p;297,301p;421,424p;1939,1941p'
echo "-- sweep exemption text:"
git -C "$C" show "$HEAD:docs/design/SAVED_STATE_MATERIALIZATION.md" | grep -n -E 'microprogram marks stay valid|do not need rewriting'
echo
echo "== F2: firmware DR2c 'alarm until reset' versus the status contract"
for f in docs/design/SAVED_STATE_MATERIALIZATION.md docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md docs/integration/BAREMETAL_FIRMWARE.md; do
  git -C "$C" show "$HEAD:$f" | grep -n -E 'Exhaustion keeps the alarm|The alarm remains until reset|reset-only alarm|Clear an exhausted alarm' | sed "s|^|$f:|"
done
echo "-- FASTCONNECT 9.2 loss causes and recovery rule (normative status home), unchanged for firmware exhaustion:"
git -C "$C" show "$HEAD:docs/design/SAVED_STATE_FASTCONNECT.md" | grep -n -E "^\*\*Clears\*\* on any of|bounded-retry exhaustion\.|^stale' |^backed' |A healed outage does not contaminate"
echo "-- firmware-exhaustion carrier named anywhere in the four pages or the register map (expect none):"
for f in docs/design/SAVED_STATE_FASTCONNECT.md docs/design/SAVED_STATE_MATERIALIZATION.md docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md docs/integration/BAREMETAL_FIRMWARE.md docs/reference/REGISTER_MAP.md; do
  n=$(git -C "$C" show "$HEAD:$f" | grep -c -i -E 'transaction (exhaustion|alarm)|firmware (exhaustion|alarm)|exhaustion (bit|verdict|flag)')
  echo "$f: $n"
done
