#!/bin/sh
# Reproduce the evidence for findings F1 and F2 from a checkout of
# kebag-logic/milan-fpga at 6029890c8ba6fd35fac3d3210b8f3a7b30bb1769 with the
# protocol-processor submodule at 16be6768f710e79450aace277abacd6c2c3336e5.
# Usage: finding_evidence.sh <repo-root>
set -u
R=$1
P=$R/protocol-processor
D3=$R/docs/design/SAVED_STATE_MATERIALIZATION.md
FC=$R/docs/design/SAVED_STATE_FASTCONNECT.md
echo "== processor pin"; git -C "$P" rev-parse HEAD
echo "== F1: files and sections the D3 section 15.2 table names"
sed -n '/^### 15.2 Processor F07.9 edit table/,/^## 16/p' "$D3" | grep '^| \[' | sed 's/](https[^)]*)//' | cut -d'|' -f2,3
echo "== F1: superseded statements at the pin outside those rows"
echo "-- 02_interfaces.md section 8 boot paragraph (table cites only 8.1/8.2, lines 538-572)"
sed -n '532,536p' "$P/docs/architecture/02_interfaces.md"
echo "-- guides/integrator.md (not in the table)"
grep -n 'OR it with `aecp_dyn_dirty_o`\|Nothing in the processor writes a record for 6 or 7' "$P/docs/guides/integrator.md"
echo "-- guides/operator.md (not in the table)"
grep -n 'restore_fail_o` means the whole boot restore\|Every sink then' "$P/docs/guides/operator.md"
echo "-- 01_overview.md F01.5 parameter row (not in the table)"
grep -n '^| P-NVM-RS-TMO-CYC' "$P/docs/architecture/01_overview.md" | cut -c1-160
echo "-- D3 contract statements these contradict"
grep -n 'restore_fail_o` and `restore_blank_o` become both walks\|aecp_dyn_dirty_o` stays exported for diagnosis but leaves\|CLOSED | an image not proven\|Preserve completed bindings on D3 rollback\|RETRY_MAX_P`, `RS_TMO_CYC_P` (the restore' "$D3" | cut -c1-200
echo "== F2: FASTCONNECT section 1 present-tense pin/line claims"
grep -n 'The processor pin is\|ONLY manager wired to the port today' "$FC" | cut -c1-220
echo "-- D3 reconciliation baseline"
grep -n 'Its processor pin is' "$D3"
echo "-- lines FASTCONNECT cites at the actual pin"
sed -n '2261p;2278p' "$P/hdl/top/protocol_processor_top.sv"
grep -n 'KL_pp_nvm_mgr_arb u_nvm_arb\|m1_req_i' "$P/hdl/top/protocol_processor_top.sv"
echo "-- ancestry"; git -C "$P" merge-base --is-ancestor 2faa5af8889d97616bda1369e4739a546da7b0f1 HEAD && echo "2faa5af8 is an ancestor, $(git -C "$P" rev-list --count 2faa5af8889d97616bda1369e4739a546da7b0f1..HEAD) commits behind"
echo "-- sentence added by this change"
grep -n 'Implementation and historical evidence remain explicitly distinguished below' "$FC"
