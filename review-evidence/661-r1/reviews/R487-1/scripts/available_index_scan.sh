#!/usr/bin/env bash
# Show the processor's available_index rule at the pin and every parent statement of that rule outside history.
# Usage: available_index_scan.sh <repo>
set -eu
cd "$1"
echo "## processor rule at $(git ls-tree HEAD protocol-processor | awk '{print $3}')"
grep -n 'DOC RULE' -A3 protocol-processor/hdl/adp/KL_adp_engine.sv
grep -n 'bld_done_avail_w)\|bld_done_dep_w)' -A1 protocol-processor/hdl/adp/KL_adp_engine.sv
echo "## parent statements (history excluded)"
for spec in "docs/reference/REGISTER_MAP.md:1032-1037" "docs/design/SAVED_STATE_MATERIALIZATION.md:1036-1038" \
            "avdecc/gen_aemi_image.py:105-106" "tb/tools/avtp_wire_truth_checks.py:553-559" \
            "tb/tools/avtp_wire_truth_checks.py:586-589" "docs/reference/MILAN_COMPLIANCE_MATRIX.md:154-154"; do
  f=${spec%%:*}; r=${spec#*:}; echo "-- $f:$r"; sed -n "${r%-*},${r#*-}p" "$f" | cut -c1-330
done
