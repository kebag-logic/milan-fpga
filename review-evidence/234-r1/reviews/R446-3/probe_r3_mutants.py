#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe (round 3): validator and parser mutants that differ from the shipped list.

Each mutant edits one unique span of syn/ooc/pp_resource_gate.py (or of
pp_baseline_rank.py) in a temporary copy of the three modules and runs
`--selftest`. KILLED means the self-test exited non-zero; the first error line
is shown as the reason. These are variants the shipped campaign does not
spell: partial relaxations (a superset or subset accepted instead of the
whole check removed) and validator bypasses.

Usage: probe_r3_mutants.py <checkout> [--jobs N]; exit 0 when the control
passes and every mutant applies and is killed.
"""

import ast
import concurrent.futures
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(sys.argv[1]).resolve() / "syn/ooc"
JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 8
GATE, RANK = "pp_resource_gate.py", "pp_baseline_rank.py"
MUTANTS = {
    "control": (GATE, None),
    "identity: extra key accepted": (GATE, ("sorted(identity) != sorted(IDENTITY)",
                                            "not set(IDENTITY) <= set(identity)")),
    "identity: missing key accepted": (GATE, ("sorted(identity) != sorted(IDENTITY)",
                                              "not set(identity) <= set(IDENTITY)")),
    "figures: extra figure accepted": (GATE, ("sorted(figures) != held", "not set(held) <= set(figures)")),
    "figures: missing figure accepted": (GATE, ("sorted(figures) != held", "not set(figures) <= set(held)")),
    "scopes: extra count accepted": (GATE, ("sorted(counts) == sorted(SCOPE)", "set(SCOPE) <= set(counts)")),
    "scopes: missing count accepted": (GATE, ("sorted(counts) == sorted(SCOPE)", "set(counts) <= set(SCOPE)")),
    "digest: any hex length": (GATE, ('r"[0-9a-f]{64}"', 'r"[0-9a-f]+"')),
    "digest: upper-case hex": (GATE, ('r"[0-9a-f]{64}"', 'r"[0-9a-fA-F]{64}"')),
    "digest: type test dropped": (GATE, ('not isinstance(base["inputs_sha256"], str) or ', "")),
    "kind: type test dropped": (GATE, ("    if not isinstance(kind, str) or kind not in GATED:\n",
                                       "    if kind not in GATED:\n")),
    "number(): text accepted": (GATE, ("isinstance(value, (int, float)) and not", "isinstance(value, (int, float, str)) and not")),
    "load(): only the first endpoint validated": (
        GATE, ("for name, entry in baseline[\"endpoints\"].items() for problem in shape_problems(name, entry)]",
               "for name, entry in list(baseline[\"endpoints\"].items())[:1] for problem in shape_problems(name, entry)]")),
    "check-baseline bypasses load()": (
        GATE, ('        baseline = {"endpoints": {}} if printing else load(args.baseline)\n',
               '        baseline = {"endpoints": {}} if printing else (json.loads(args.baseline.read_text()) '
               'if args.command == "check-baseline" else load(args.baseline))\n')),
    "check bypasses load()": (
        GATE, ('        baseline = {"endpoints": {}} if printing else load(args.baseline)\n',
               '        baseline = {"endpoints": {}} if printing else (json.loads(args.baseline.read_text()) '
               'if args.command == "check" else load(args.baseline))\n')),
    "routing-errors row: duplicates accepted": (
        GATE, ('    if len(counts.get("nets with routing errors", [])) != 1:\n',
               '    if len(counts.get("nets with routing errors", [])) < 1:\n')),
    "routing-errors row: may be absent": (
        GATE, ('    if len(counts.get("nets with routing errors", [])) != 1:\n',
               '    if len(counts.get("nets with routing errors", [])) > 1:\n')),
    "slack: integer accepted without fraction": (GATE, ('r"-?[0-9]+\\.[0-9]+"', 'r"-?[0-9]+(?:\\.[0-9]+)?"')),
    "utilization: any fraction accepted": (GATE, ('r"[0-9]+(\\.5)?"', 'r"[0-9]+(\\.[0-9]+)?"')),
    "hierarchy: first count cell unchecked": (RANK, ("for value in fields[2:]):\n", "for value in fields[3:]):\n")),
    "hierarchy: last count cell unchecked": (RANK, ("for value in fields[2:]):\n", "for value in fields[2:-1]):\n")),
}


def run(name: str, target: str, change) -> tuple[bool, str]:
    text = (HERE / target).read_text()
    if change is not None:
        old, new = change
        if text.count(old) != 1:
            return False, f"{'NOT-APPL':<9} {name:<46} | span occurs {text.count(old)} times"
        text = text.replace(old, new)
    ast.parse(text)
    with tempfile.TemporaryDirectory(prefix="r446-r3-mutant-") as tmp:
        for sibling in (GATE, RANK, "pp_resource_gate_selftest.py"):
            shutil.copy2(HERE / sibling, Path(tmp) / sibling)
        (Path(tmp) / target).write_text(text)
        result = subprocess.run([sys.executable, "-B", str(Path(tmp) / GATE), "--selftest"],
                                capture_output=True, text=True, timeout=600)
    out = (result.stdout + result.stderr).splitlines()
    reason = next((line.strip() for line in out if "AssertionError" in line or "Error:" in line),
                  out[-1] if out else "")
    if name == "control":
        ok = result.returncode == 0
        return ok, f"{'CONTROL' if ok else 'CTRL-BAD':<9} {name:<46} | {reason[:170]}"
    ok = result.returncode != 0
    return ok, f"{'KILLED' if ok else 'SURVIVED':<9} {name:<46} | {reason[:170]}"


def main() -> int:
    with concurrent.futures.ThreadPoolExecutor(JOBS) as pool:
        results = list(pool.map(lambda item: run(item[0], *item[1]), MUTANTS.items()))
    for _, line in results:
        print(line)
    bad = sum(not ok for ok, _ in results)
    print(f"round-3 mutant probe: {len(results) - 1} mutants, {bad} not killed or not applied (control included)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
