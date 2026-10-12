#!/usr/bin/env bash
# Does tb/aecp_cmds' suite target (now through check_observed.py) fail on an
# engine drift, and does any existing control notice a wrapper that drops the
# gate's exit status? Disposable clone at the exact head; restored after.
# usage: wrapper_probe.sh CLONE
set -u
C=$1; cd "$C" || exit 99
[ "$(git rev-parse HEAD)" = 4bee75b2e647507a71ece50359fceb135c334757 ] || exit 98
restore() { git checkout -q -- . && git clean -qfdx >/dev/null; }
q1() { python3 - <<'EOF'
import pathlib
p = pathlib.Path("hdl/aecp/KL_aecp_engine.sv"); t = p.read_text()
old = "else                                    upc_r <= UPC_SCLKS_C;"
assert t.count(old) == 1
p.write_text(t.replace(old, "else                                    upc_r <= UPC_GCLKS_C;"))
EOF
}
run_suite() { # label
  rm -f "$C/../wrapper-tags.txt"
  out=$( (cd tb/aecp_cmds && REQ_TAG_LOG="$C/../wrapper-tags.txt" make) 2>&1 ); rc=$?
  echo "SUITE $1: make rc=$rc"
  printf '%s\n' "$out" | grep -E '^FAIL:|checks: ' | head -4 | sed 's/^/    /'
  echo "    evidence: $(cat "$C/../wrapper-tags.txt" 2>/dev/null)"
}
restore
q1; run_suite "q1 engine drift, wrapper as published"
restore
q1
sed -i 's/                               "--observed", str(observation)\], check=False).returncode/                               "--observed", str(observation)], check=False).returncode and 0/' tb/aecp_cmds/check_observed.py
git diff --stat | sed 's/^/    /'
run_suite "q1 engine drift, wrapper planted to drop the status"
restore
echo "restored: $(git status --porcelain | wc -l) changes"
