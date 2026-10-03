#!/usr/bin/env python3
"""Perturb every policy value of the baseline JSON and every cell of the budget table, one at a time.

Usage: probe_policy.py <repo checkout> <scratch dir>
Each perturbation is written to a scratch copy and judged by
`pp_resource_gate.py check-baseline --baseline <copy> --budget <copy>` as a
subprocess. Every perturbation must exit 2 naming the endpoint; the unperturbed
pair must exit 0. Also prints the policy the head's table parses to.
"""
import json
from pathlib import Path
import re
import subprocess
import sys

repo, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
scratch.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(repo / "syn/ooc"))
import pp_resource_gate as gate  # noqa: E402

GATE = repo / "syn/ooc/pp_resource_gate.py"
BASE = json.loads((repo / "syn/ooc/pp_resource_baseline.json").read_text())
PAGE = (repo / "docs/design/AREA_BUDGET.md").read_text()


def judge(baseline: dict, page: str) -> tuple[int, str]:
    (scratch / "b.json").write_text(json.dumps(baseline))
    (scratch / "budget.md").write_text(page)
    run = subprocess.run([sys.executable, "-B", str(GATE), "check-baseline", "--baseline", str(scratch / "b.json"),
                          "--budget", str(scratch / "budget.md")], capture_output=True, text=True, timeout=120)
    out = (run.stdout + run.stderr).strip().replace("\n", " | ")
    return run.returncode, ("TRACEBACK " if "Traceback" in out else "") + out[:220]


print("parsed table:", json.dumps(gate.policy_table(PAGE), sort_keys=True))
results = []
status, out = judge(BASE, PAGE)
results.append(("control", 0, status, out))
for name, entry in BASE["endpoints"].items():
    for field in gate.POLICY:
        for figure, value in entry.get(field, {}).items():
            for new in (value + 1, value - 0.001 if isinstance(value, float) else value + 0.5):
                data = json.loads(json.dumps(BASE))
                data["endpoints"][name][field][figure] = new
                results.append((f"JSON {name} {field} {figure} {value} -> {new}", 2, *judge(data, PAGE)))
            data = json.loads(json.dumps(BASE))
            del data["endpoints"][name][field][figure]
            results.append((f"JSON {name} {field} {figure} removed", 2, *judge(data, PAGE)))
    data = json.loads(json.dumps(BASE))
    data["endpoints"][name].setdefault("floor", {})["LUT"] = 1
    results.append((f"JSON {name} floor LUT added", 2, *judge(data, PAGE)))
lines = PAGE.splitlines(keepends=True)
head = [i for i, line in enumerate(lines) if line.startswith("| Endpoint | LUT | FF | Slice | RAMB36")]
assert len(head) == 1
for index in range(head[0] + 2, head[0] + 5):
    cells = lines[index].rstrip("\n").split("|")
    for column in range(2, len(cells) - 1):
        cell = cells[column].strip()
        number = re.fullmatch(r"([+-]?)(\d+(?:\.\d+)?)( ns)?", cell)
        if number:
            options = [f"{number[1]}{float(number[2]) + 1:g}{number[3] or ''}"]
        else:
            options = ["+0", "5"]
        for new in options:
            changed = cells[:]
            changed[column] = f" {new} "
            page = "".join(lines[:index]) + "|".join(changed) + "\n" + "".join(lines[index + 1:])
            results.append((f"table {cells[1].strip()} column {column - 1} {cell!r} -> {new!r}", 2, *judge(BASE, page)))
bad = 0
for label, wanted, got, out in results:
    verdict = "OK" if got == wanted and "TRACEBACK" not in out else "BAD"
    bad += verdict == "BAD"
    print(f"{verdict} {label}: wanted {wanted}, got {got}: {out}")
print(f"{len(results) - bad}/{len(results)} as wanted")
