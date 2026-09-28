#!/bin/sh
# Re-check every round-1 finding (R380-1 F1-F3, R381-1 F1-F2, taken
# suggestions R381-1 S1/S2) at the checked-out head.
# Run from the parent repository root.
set -u
D3=docs/design/SAVED_STATE_MATERIALIZATION.md
FC=docs/design/SAVED_STATE_FASTCONNECT.md
SN=docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md
BF=docs/integration/BAREMETAL_FIRMWARE.md
T=$(mktemp)
awk '/^### 15\.2/{f=1;next} f&&/^## 16\./{exit} f' "$D3" | sed -E 's/\(https[^)]*\)//g' > "$T"
row() { printf '%-58s ' "$1"; grep -F "$2" "$T" | grep -c -E "$3" ; }
echo "## head $(git rev-parse HEAD)"
echo "## F1 (R380-1 F1 / R381-1 F1): named locations -> matching 15.2 rows (count)"
row "integrator.md:334 pending composition"        'docs/guides/integrator.md' 'lines 334-336.*d3_unflushed_o'
row "integrator.md:336 groups 6/7 writer"          'docs/guides/integrator.md' 'groups 6/7 have no processor writer'
row "integrator.md params table / check script"    'docs/guides/integrator.md' 'lines 47-105.*check-integrator-params'
row "diagram 21 parameter inventory"               'docs/diagrams/21-integration-faces.svg' 'parameter inventory'
row "operator.md restore table / unbound claim"    'docs/guides/operator.md' 'lines 197-227.*every-sink-unbound'
row "01_overview.md:170 F01.5 P-NVM-RS-TMO-CYC"    'docs/architecture/01_overview.md' 'line 170'
row "02_interfaces.md:532-536 boot paragraph"      'docs/architecture/02_interfaces.md' '8 boot paragraph.*lines 532-572'
row "KL_acmp_nvm_shadow immediate retry (DR2c)"    'hdl/acmp/KL_acmp_nvm_shadow.sv' 'immediately return to H_FL_RD.*500 ms backoff'
echo "## F2 (R381-1 F2): FASTCONNECT pin/wiring lines"
grep -n -E 'Which donor commit|The processor pin is|ONLY manager wired to the port today|lines 2261 and 2278' "$FC" || echo "  stale present-tense pin/wiring text: none"
grep -n -E 'Reconciliation pin|Historical completion repair|manager 1 is tied idle at lines 2540-2546' "$FC"
echo "## F2 (R380-1 F2): debounce presented as open"
grep -n -E 'is still open; section 14|provisional value section 14 leaves open|its provisional 1,000 ms debounce' "$FC" "$D3" "$SN" "$BF" || echo "  none in the four pages"
grep -n -E 'milan_baremetal.c:340|nvm_shape.py:146' "$D3"
echo "## F3 (R380-1 F3): writer FSM vs DR2c"
grep -n -E 'ACQUIRE again \(a fresh latch\), or RUN with the alarm|giveup += port err AND retries' "$D3" || echo "  unspaced retry rows: none"
grep -n -E '^\| BACKOFF|attempt 1 or 2 ends with port err|the third attempt ends with err|^retry_ready|^giveup|^attempts|DR2c permits at most three attempts' "$D3"
echo "## R381-1 S1 / S2"
grep -n -E 'Every lost change was reported at the cut|Its reporter was producer pending' "$FC"
grep -n -E 'lines 1450 and 1220-1221 at parent|calls at lines 1453-1454' "$D3"
rm -f "$T"
