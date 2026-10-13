#!/usr/bin/env bash
# Apply one textual mutation to a disposable copy of the reviewed tree and run
# the scope selftest and the CI-events contract check on it.
# Usage: run_mutation.sh <readonly-tree> <work-root> <mutations.json> <id>
set -uo pipefail
tree="$1"; work="$2"; muts="$3"; id="$4"
d="$work/$id"; rm -rf "$d"; mkdir -p "$d"; cp -a "$tree/." "$d/"; chmod -R u+w "$d"
python3 -I - "$muts" "$id" "$d" <<'PY' || { echo "$id APPLY-FAILED"; exit 0; }
import json, sys, pathlib
muts, ident, root = sys.argv[1:4]
for i, path, old, new in json.load(open(muts)):
    if i == ident:
        p = pathlib.Path(root, path); s = p.read_text()
        assert s.count(old) == 1, f"anchor count {s.count(old)}"
        p.write_text(s.replace(old, new, 1))
PY
cd "$d"
timeout 600 env PYTHONDONTWRITEBYTECODE=1 python3 scripts/ci_scope.py --selftest > "$d.scope.log" 2>&1; s=$?
timeout 600 env PYTHONDONTWRITEBYTECODE=1 python3 scripts/ci_events.py --check > "$d.events.log" 2>&1; e=$?
echo "$id scope_selftest_rc=$s ci_events_check_rc=$e scope_FAIL_lines=$(grep -c FAIL "$d.scope.log")"
