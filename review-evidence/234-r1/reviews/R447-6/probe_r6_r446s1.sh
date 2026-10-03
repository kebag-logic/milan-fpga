#!/usr/bin/env bash
# This reviewer's own mutants for the three class widenings R446-5 S1 names, run against the head's --selftest,
# gate.fuzz(5000, 447) and check-baseline in a copy (never inside the checkout).
# Usage: probe_r6_r446s1.sh <repo checkout> <scratch dir>
set -u
repo=$1 scratch=$2
rm -rf "$scratch"; mkdir -p "$scratch"
python3 - "$repo" "$scratch" <<'PY'
import sys, shutil
from pathlib import Path
repo, scratch = Path(sys.argv[1]), Path(sys.argv[2])
S = r'SCOPE_NAME = re.compile(r"[A-Za-z0-9_.:/\[\]-]{1,128}")'
M = {"scope name admits a space": (S, r'SCOPE_NAME = re.compile(r"[A-Za-z0-9_.:/\[\] -]{1,128}")'),
     "scope name admits an empty key": (S, r'SCOPE_NAME = re.compile(r"[A-Za-z0-9_.:/\[\]-]{0,128}")'),
     "SCOPES first element wildcarded": ('SCOPES = ("endpoints", None, "record", "scopes")',
                                         'SCOPES = (None, None, "record", "scopes")')}
for name, (old, new) in M.items():
    folder = scratch / "".join(c if c.isalnum() else "_" for c in name)
    folder.mkdir()
    for m in ("pp_resource_gate.py", "pp_baseline_rank.py", "pp_resource_gate_selftest.py", "pp_resource_baseline.json"):
        shutil.copy(repo / "syn/ooc" / m, folder / m)
    text = (folder / "pp_resource_gate.py").read_text()
    assert text.count(old) == 1, name
    (folder / "pp_resource_gate.py").write_text(text.replace(old, new))
PY
for f in "$scratch"/*/; do
  ( cd "$f"
    python3 -B pp_resource_gate.py --selftest > selftest.log 2>&1; s=$?
    python3 -B -c "import sys, pp_resource_gate as g; sys.exit(g.fuzz(5000, 447))" > fuzz.log 2>&1; z=$?
    python3 -B pp_resource_gate.py check-baseline --baseline pp_resource_baseline.json --budget "$repo/docs/design/AREA_BUDGET.md" > cb.log 2>&1; c=$?
    printf '%s: selftest rc=%s (%s); fuzz5k rc=%s (%s); check-baseline rc=%s\n' "$(basename "$f")" $s "$(grep -h "Error\|selftest:" selftest.log | tail -n 1 | cut -c1-150)" $z "$(grep -o '[0-9]* failures' fuzz.log)" $c ) &
done
wait
