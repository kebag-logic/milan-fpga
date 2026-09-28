#!/bin/sh
# Evidence for R380-2 F1: processor statements at 16be6768 that describe the
# AECP commit mark (NVM_MARK) as the persistence trigger or mechanism, the D3
# statements they contradict, whether D3 section 15.2 has a row for the file,
# and whether D3's named contract-sweep pattern matches the line.
# Run from the parent repository root.
set -u
D3=docs/design/SAVED_STATE_MATERIALIZATION.md
FC=docs/design/SAVED_STATE_FASTCONNECT.md
PP=protocol-processor
SWEEP='COMMIT.*NVM_MARK|aecp_dyn_dirty_o|nvm_unflushed_o|d3_unflushed_o|restore_(done|fail|blank)_o|T-NVM|RETRY_MAX_P|DEB_TICKS_P|entity_enable|Nothing in the processor|groups 6 and 7|integrating platform'
echo "## processor pin: $(git -C $PP rev-parse HEAD)"
echo "## D3 / FASTCONNECT statements (head $(git rev-parse HEAD))"
grep -n -E 'Triggers are the live writes, never the commit marks|Command-completion marks remain notification effects|Selector 7 and an out-of-range index set nothing|Live writes select records; marks retain command-completion meaning' "$D3" "$FC"
echo "## section 15.2 rows naming gen_ucode.py:"
awk '/^### 15\.2/{f=1;next} f&&/^## 16\./{exit} f' "$D3" | grep -c 'gen_ucode' 
echo "## section 15.2 06_aecp_engine row:"
awk '/^### 15\.2/{f=1;next} f&&/^## 16\./{exit} f' "$D3" | grep '06_aecp_engine' | sed -E 's/\(https[^)]*\)//g'
for spec in \
  hdl/aecp/ucode/gen_ucode.py:1364 hdl/aecp/ucode/gen_ucode.py:1439 hdl/aecp/ucode/gen_ucode.py:1582 \
  hdl/aecp/ucode/gen_ucode.py:1583 hdl/aecp/ucode/gen_ucode.py:1675 hdl/aecp/ucode/gen_ucode.py:1791 \
  hdl/aecp/ucode/gen_ucode.py:1925 hdl/aecp/ucode/gen_ucode.py:2002 hdl/aecp/ucode/gen_ucode.py:2091 \
  docs/architecture/06_aecp_engine.md:342 docs/architecture/06_aecp_engine.md:343 \
  docs/architecture/06_aecp_engine.md:344 docs/architecture/06_aecp_engine.md:423 \
  docs/architecture/06_aecp_engine.md:424 docs/00_MILAN_COMPLIANCE_REVIEW.md:208; do
  f=${spec%%:*}; n=${spec##*:}
  line=$(sed -n "${n}p" "$PP/$f")
  if printf '%s\n' "$line" | grep -q -E "$SWEEP"; then m=SWEEP-MATCH; else m=sweep-miss; fi
  printf '%s  %s  %s\n' "$m" "$spec" "$(printf '%s' "$line" | sed -E 's/^ +//' | cut -c1-150)"
done
