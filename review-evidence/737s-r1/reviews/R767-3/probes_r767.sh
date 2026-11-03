#!/usr/bin/env bash
# Reviewer mutation probes for #737 at the reviewed head. Usage: probes_r767.sh <clone> <receipt-dir>
# Each probe edits one tracked file, runs the named checks, and restores the file from HEAD.
set -u
clone=$1; out=$2; mkdir -p "$out"; cd "$clone" || exit 2
restore() { git checkout -- scripts/ci_litex_legs.py scripts/ci_gate_workflows.py; }
probe() {  # name, file, python-replace-old, python-replace-new, commands...
  local name=$1 file=$2 old=$3 new=$4; shift 4
  python3 -I - "$file" "$old" "$new" <<'EOF' || { echo "$name: mutation did not apply" > "$out/$name.txt"; return; }
import sys, pathlib
p = pathlib.Path(sys.argv[1]); s = p.read_text()
assert s.count(sys.argv[2]) == 1, "pattern not unique"
p.write_text(s.replace(sys.argv[2], sys.argv[3]))
EOF
  { echo "probe $name: $file: '$old' -> '$new'"; git diff --stat | cat
    for cmd in "$@"; do bash -c "$cmd" > "$out/$name.cmd.log" 2>&1; rc=$?
      echo "rc=$rc :: $cmd"; tail -n 2 "$out/$name.cmd.log"; done; } > "$out/$name.txt"
  restore
}
probe p1-job-limit-2640 scripts/ci_litex_legs.py 'JOB_LIMIT = 2700' 'JOB_LIMIT = 2640' \
  'python3 scripts/ci_litex_legs_selftest.py' 'python3 scripts/ci_gate_workflows_selftest.py'
probe p2-soc-897-fits scripts/ci_litex_legs.py '"test_soc_timing_cuts": 510,' '"test_soc_timing_cuts": 897,' \
  'python3 scripts/ci_litex_legs.py legs'
probe p3-soc-898-refused scripts/ci_litex_legs.py '"test_soc_timing_cuts": 510,' '"test_soc_timing_cuts": 898,' \
  'python3 scripts/ci_litex_legs.py legs'
probe p4-setup-873-budget-793-refused scripts/ci_litex_legs.py 'SETUP = 485' 'SETUP = 873' \
  'python3 scripts/ci_litex_legs.py legs'
probe p5-full-history-aggregate scripts/ci_gate_workflows.py 'HEAD_ONLY_AGGREGATES = {"elaborate"}' 'HEAD_ONLY_AGGREGATES = set()' \
  'python3 scripts/ci_gate_workflows.py --check' 'python3 scripts/ci_gate_workflows_selftest.py'
probe p6-metadata-everywhere scripts/ci_gate_workflows.py '        if leg != generator:' '        if False:' \
  'python3 scripts/ci_gate_workflows.py --check' 'python3 scripts/ci_gate_workflows_selftest.py'
restore
git status --short > "$out/post-probe-status.txt"
