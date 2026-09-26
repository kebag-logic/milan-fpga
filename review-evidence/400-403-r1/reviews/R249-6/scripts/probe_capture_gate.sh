#!/bin/sh
# Disposable fault probes on scripts/check_nvm_capture.py at the checked-out
# head. Each probe perturbs one tracked file, runs the gate, records its exit
# status and message, then restores the exact HEAD blob. Every probe must
# exit nonzero; the final unperturbed run must exit zero.
# Usage: probe_capture_gate.sh <repo>
set -u
cd "$1"
fw=sw/firmware/milan_baremetal/milan_baremetal.c
rc_json=tb/verilator/nvm_capture_cpu/measurements.json
restore() { git show "HEAD:$1" > "$1"; }
run() {
  python3 scripts/check_nvm_capture.py > /tmp/probe.$$ 2>&1; rc=$?
  echo "probe=$1 rc=$rc msg=$(grep -E '^(FAIL|PASS)' /tmp/probe.$$ | head -1)"
  rm -f /tmp/probe.$$
}
# 1. one-byte firmware edit (the R249-4 F1 composition shape)
printf '\n' >> "$fw"; run firmware-byte; restore "$fw"
# 2. one row's sys_cycles raised by one tick, summary left stale
python3 - "$rc_json" <<'EOF'
import json, sys
p = sys.argv[1]; d = json.load(open(p))
d['measurements'][0]['rows'][13]['sys_cycles'] += 1
open(p, 'w').write(json.dumps(d, indent=2) + '\n')
EOF
run row-tamper; restore "$rc_json"
# 3. published 8x8 maximum replaced by the ON-arm-only maximum after an
#    OFF row is made the slowest capture (OFF must set the maximum)
python3 - "$rc_json" <<'EOF'
import json, sys
p = sys.argv[1]; d = json.load(open(p))
off = d['measurements'][1]
off['rows'][0]['sys_cycles'] = 2_440_000
off['maximum_ms'] = 24.4; off['margin'] = 49 / 24.4
open(p, 'w').write(json.dumps(d, indent=2) + '\n')
EOF
run off-slowest-maxima-stale; restore "$rc_json"
# 4. an OFF row carrying traffic counts
python3 - "$rc_json" <<'EOF'
import json, sys
p = sys.argv[1]; d = json.load(open(p))
d['measurements'][1]['rows'][5]['requests'] = 1
open(p, 'w').write(json.dumps(d, indent=2) + '\n')
EOF
run off-row-traffic; restore "$rc_json"
# 5. firmware digest in receipt reverted to the pre-merge (dev) digest
python3 - "$rc_json" <<'EOF'
import json, sys
p = sys.argv[1]; d = json.load(open(p))
d['product_firmware_sha256'] = '7cdc5e68243ff35a4b3b0b13613ba5f937010835dc737b1400c640d6ebce8a64'
open(p, 'w').write(json.dumps(d, indent=2) + '\n')
EOF
run stale-dev-digest; restore "$rc_json"
# 6. an 8x8 50 MHz row one tick over the 24.5 ms limit, summaries recomputed
python3 - "$rc_json" <<'EOF'
import json, sys
p = sys.argv[1]; d = json.load(open(p))
a = d['measurements'][0]; a['rows'][13]['sys_cycles'] = 2_450_001
a['maximum_ms'] = 24.50001; a['margin'] = 49 / 24.50001
open(p, 'w').write(json.dumps(d, indent=2) + '\n')
EOF
run over-limit; restore "$rc_json"
run unperturbed-head
git status --porcelain -- "$fw" "$rc_json"
git diff --quiet HEAD -- "$fw" "$rc_json" && echo "restored: tracked bytes equal HEAD"
