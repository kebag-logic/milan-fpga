#!/bin/sh
# Refined probe: an OFF row becomes the slowest 8x8 capture; the arm summary is
# recomputed with the harness's own grader so only the published `maxima`
# entry is stale. The gate must refuse. Restores the HEAD blob afterwards.
# Usage: probe_capture_maxima.sh <repo>
set -u
cd "$1"
rc_json=tb/verilator/nvm_capture_cpu/measurements.json
python3 - "$rc_json" <<'PY'
import json, sys
sys.path.insert(0, 'tb/verilator/nvm_capture_cpu')
import run
p = sys.argv[1]; d = json.load(open(p))
off = d['measurements'][1]
off['rows'][0]['sys_cycles'] = 2_440_000
summary = run.grade_rows(off['rows'], off)
off.update({k: summary[k] for k in ('minimum_ms', 'maximum_ms', 'margin')})
open(p, 'w').write(json.dumps(d, indent=2) + '\n')
PY
python3 scripts/check_nvm_capture.py > /tmp/probe.$$ 2>&1; echo "probe=off-slowest-maxima-stale rc=$? msg=$(grep -E '^(FAIL|PASS)' /tmp/probe.$$)"; rm -f /tmp/probe.$$
git show "HEAD:$rc_json" > "$rc_json"
git diff --quiet HEAD -- "$rc_json" && echo "restored: tracked bytes equal HEAD"
