#!/bin/sh
# Static receipts for R380-1. Run from the repository root of a checkout at
# 6029890c8ba6fd35fac3d3210b8f3a7b30bb1769 with protocol-processor at 16be6768.
# Usage: sh static_receipts.sh <receipt-dir>
set -u
R=$1
D3=docs/design/SAVED_STATE_MATERIALIZATION.md
FC=docs/design/SAVED_STATE_FASTCONNECT.md
PP=protocol-processor
{
  echo "## lane sections: DR3a / DR4 / negative controls / physical"
  for n in 1 2 3 4 5; do
    sec=$(awk -v n="$n" '$0 ~ "^### 18\\."n" " {f=1; print; next} f && /^#{2,3} / {exit} f' "$D3")
    printf 'lane %s: ratif=%s DR4=%s 8x8_open_blocked=%s negctl=%s physical=%s\n' "$n" \
      "$(printf '%s' "$sec" | grep -c -E 'ratif|DR3a')" \
      "$(printf '%s' "$sec" | grep -c -E 'DR4|1x1 TDM8')" \
      "$(printf '%s' "$sec" | grep -c -E 'open.{0,12}blocked|blocked post-place|not waived')" \
      "$(printf '%s' "$sec" | grep -c '^\*\*Negative controls')" \
      "$(printf '%s' "$sec" | grep -c -i -E 'physical|cold-cycle|cold cycle|cold cuts')"
  done
  echo "## section 18 preamble (applies to all lanes)"
  awk '/^## 18\. /{f=1} f && /^### 18\.1/{exit} f' "$D3" | grep -n -E 'DR3a|DR4|8x8|DR2'
} > "$R/50_lane_contract_carry.txt" 2>&1
{
  echo "## F07.9 edit-table rows (file column)"
  awk '/^### 15\.2/{f=1} f && /^## 16\./{exit} f' "$D3" | grep -o -E '\[docs/[a-z0-9_./-]+\]' | sort | uniq -c
  echo "## processor doc text at 16be6768 that states the superseded contract, absent from the table"
  grep -n -E 'OR it with `aecp_dyn_dirty_o`|Nothing in the processor writes a record for 6 or 7' $PP/docs/guides/integrator.md
  grep -n -E '^\| `NVM_RS_TMO_CYC_P`' $PP/docs/guides/integrator.md | cut -c1-160
  grep -n -E 'compares this table and diagram 21' $PP/docs/guides/integrator.md
  grep -n -E 'restore_blank_o. is the third pin|a failed\s*$|walk included' $PP/docs/guides/operator.md
  grep -n -E '^\| P-NVM-RS-TMO-CYC' $PP/docs/architecture/01_overview.md | cut -c1-200
  grep -n -o 'NVM_RS_TMO_CYC_P' $PP/docs/diagrams/21-integration-faces.svg | head -1
} > "$R/51_f079_table_coverage.txt" 2>&1
{
  echo "## ruled debounce vs remaining 'open/provisional' statements"
  grep -n -E 'DR2a settles|DR2a rules both|Debounce policy is ruled' $FC docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md
  grep -n -E 'T-NVM-DEBOUNCE. is a different quantity and is still open' $FC
  grep -n -E 'provisional value section 14 leaves open' docs/integration/BAREMETAL_FIRMWARE.md sw/firmware/milan_baremetal/milan_baremetal.c
  grep -n -E 'T-NVM-DEBOUNCE is not decided there' scripts/nvm_shape.py
  grep -n -E 'its provisional 1,000 ms debounce' "$D3"
} > "$R/52_debounce_consistency.txt" 2>&1
{
  echo "## DR2c ruling vs D3 writer state machine"
  grep -n -E '^\| DR2c' "$D3" | cut -c1-400
  grep -n -E 'ACQUIRE again \(a fresh latch\)|giveup += port err|RETRY_MAX_P. failed writes' "$D3"
  echo "## any backoff/spacing state in sections 6.1-6.3:"
  awk '/^### 6\.1/{f=1} f && /^### 6\.4/{exit} f' "$D3" | grep -n -i -E 'backoff|500 ms|apart|DR2c' || echo "none"
} > "$R/53_retry_fsm_vs_dr2c.txt" 2>&1
