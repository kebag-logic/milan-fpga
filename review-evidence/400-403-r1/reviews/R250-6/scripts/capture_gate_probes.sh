#!/usr/bin/env bash
# Disposable probes of scripts/check_nvm_capture.py in a scratch copy of the head.
# 1. dev's pre-refresh receipt against this head's firmware must FAIL (R249-4 F1).
# 2. the refreshed receipt must PASS.
# 3. a one-byte firmware comment edit must FAIL.
# 4. a harness edit must FAIL.
# 5. a receipt row raised past the 24.5 ms bar must FAIL.
# Every probe restores the tracked bytes and the script checks git status at the end.
# Usage: capture_gate_probes.sh <scratch-tree> <dev-rev>
set -uo pipefail
tree=$1 dev=$2
: "${PYVENV:=$VALIDATION_TOOLS/md-venv-40cdefe08ebd}"
export PATH="$PYVENV/bin:$PATH"
cd "$tree" || exit 2
R=tb/verilator/nvm_capture_cpu/measurements.json
FW=sw/firmware/milan_baremetal/milan_baremetal.c
gate() { python3 scripts/check_nvm_capture.py > /tmp/probe.$$ 2>&1; local rc=$?; grep -E '^(PASS|FAIL)' /tmp/probe.$$ | tail -1 | cut -c1-160; return $rc; }
expect() { local want=$1 name=$2; gate; local rc=$?
  if { [ "$want" = pass ] && [ $rc -eq 0 ]; } || { [ "$want" = fail ] && [ $rc -ne 0 ]; }; then
    echo "PROBE $name: expected $want, rc=$rc OK"; else echo "PROBE $name: expected $want, rc=$rc WRONG"; fi; }
git show "$dev:$R" > "$R"; expect fail dev-receipt-on-head-firmware; git checkout -q -- "$R"
expect pass refreshed-receipt
printf '\n/* probe */\n' >> "$FW"; expect fail firmware-edit; git checkout -q -- "$FW"
printf '\n# probe\n' >> tb/verilator/nvm_capture_cpu/probe.py; expect fail harness-edit
git checkout -q -- tb/verilator/nvm_capture_cpu/probe.py
python3 - "$R" <<'EOF'
import json, sys
p = sys.argv[1]; m = json.load(open(p))
for arm in m['measurements']:
    if arm['cpu_hz'] == 50_000_000 and arm['shape'].endswith('8x8') and arm['traffic'] == 'off':
        arm['rows'][5]['sys_cycles'] = 2_450_001
json.dump(m, open(p, 'w'), indent=2)
EOF
expect fail off-row-over-bar; git checkout -q -- "$R"
expect pass restored
echo "STATUS: $(git status --porcelain | wc -l) changed tracked/untracked entries"
rm -f /tmp/probe.$$
