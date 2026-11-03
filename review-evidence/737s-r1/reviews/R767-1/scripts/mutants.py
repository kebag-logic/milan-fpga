#!/usr/bin/env python3
"""Reviewer mutation campaign for the LiteX leg split (PR #836, issue #737).

Usage: mutants.py <disposable clone at the reviewed head> <receipt dir>

Each mutant is one exact-text replacement (its anchor must occur exactly once).
After applying it the workflow is regenerated with the mutant generator (so a
generator mutant is judged by the self-tests, not merely by --check against the
committed file), then the self-tests that guard this change run:
  scripts/run_litex_sims.sh --selftest, scripts/ci_litex_legs_selftest.py,
  scripts/ci_gate_workflows_selftest.py, scripts/ci_gate_workflows.py --check
  (against the regenerated file), and a stub-interpreter end-to-end leg run
  (scripts/e2e_legs.py) that runs the real runner through ci_litex_legs.py and
  judges the union and the aggregate verifier.
A mutant is KILLED when any of them exits non-zero. Tracked files are restored
with `git checkout -- .` and `git clean -fdq` after each mutant.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

CLONE = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
HERE = Path(__file__).resolve().parent

M = [
    # id, file, old, new, what it breaks
    ("S1", "scripts/run_litex_sims.sh",
     '    SELECTED+=("$t"); unset \'asked[$t]\'',
     '    SELECTED+=("$t"); unset \'asked[$t]\'; [ "${#SELECTED[@]}" -ge 2 ] && break',
     "--only silently runs at most two members"),
    ("S2", "scripts/run_litex_sims.sh",
     '  select_members "$ONLY" || exit 2',
     '  select_members "$ONLY" || exit 2; SELECTED=("${INVENTORY[@]}")',
     "--only ignored: every leg runs the whole inventory"),
    ("S3", "scripts/run_litex_sims.sh",
     '  for t in "${INVENTORY[@]}"; do\n    if [ ! -f "$SIM_DIR/$t.py" ]; then',
     '  for t in "${SELECTED[@]}"; do\n    if [ ! -f "$SIM_DIR/$t.py" ]; then',
     "MISSING reconciliation narrowed to the selection"),
    ("S4", "scripts/run_litex_sims.sh",
     "    printf '%s\\t%s\\t%s\\n' \"$t\" \"$verdict\" \"$((SECONDS - start))\" >> \"$out/verdicts.tsv\"",
     "    [ \"$verdict\" = FAIL ] || printf '%s\\t%s\\t%s\\n' \"$t\" \"$verdict\" \"$((SECONDS - start))\" >> \"$out/verdicts.tsv\"",
     "a failing member writes no verdict row"),
    ("S5", "scripts/run_litex_sims.sh",
     "      0)   verdict=PASS ;; 94) verdict=SKIP ;; 124|137) verdict=TIMEOUT ;; *) verdict=FAIL ;;",
     "      *)   verdict=PASS ;;",
     "every verdict row says PASS"),
    ("S6", "scripts/ci_litex_legs.py",
     "    return [[name for name in names if owner[name] == leg] for leg in range(legs)]",
     "    owner[names[-1]] = -1\n    return [[name for name in names if owner[name] == leg] for leg in range(legs)]",
     "partition drops the last inventory member from every leg"),
    ("S7", "scripts/ci_litex_legs.py",
     "    return [[name for name in names if owner[name] == leg] for leg in range(legs)]",
     "    return [[name for name in names if owner[name] == leg or (leg == owner[names[-1]] and name == names[0])] for leg in range(legs)]",
     "partition places one member in two legs"),
    ("S8", "scripts/ci_litex_legs.py",
     "    if absent:\n        raise",
     "    if False:\n        raise",
     "union no longer refuses a simulation in no leg"),
    ("S9", "scripts/ci_litex_legs.py",
     "        if executed != legs[leg]:",
     "        if False:",
     "union no longer requires each leg's rows to equal its selection"),
    ("S10", "scripts/ci_litex_legs.py",
     "        if receipt[\"exit\"] != 0:",
     "        if False:",
     "union ignores a red runner exit"),
    ("S11", "scripts/ci_litex_legs.py",
     "            if row[\"verdict\"] != \"PASS\":",
     "            if row[\"verdict\"] not in (\"PASS\", \"SKIP\"):",
     "union accepts a SKIP"),
    ("S12", "scripts/ci_gate_receipts.py",
     "    if any(simulated):\n        from ci_litex_legs import union as litex_union",
     "    if False:\n        from ci_litex_legs import union as litex_union",
     "aggregate never checks the LiteX union"),
    ("S13", "scripts/ci_gate_receipts.py",
     "    elif litex:\n        raise ValueError(\"LiteX leg receipts without an executed LiteX division\")",
     "    elif False:\n        raise ValueError(\"LiteX leg receipts without an executed LiteX division\")",
     "aggregate accepts LiteX receipts from a skipped division"),
    ("S14", "scripts/ci_gate_workflows.py",
     "                   + \"python3 scripts/ci_litex_legs.py run \" + str(case[\"litex\"])",
     "                   + \"python3 scripts/ci_litex_legs.py run \" + str(min(case[\"litex\"], 1))",
     "generator runs leg 1 on both worker 3 and worker 4 (leg 2 unrun)"),
    ("S15", "scripts/ci_gate_workflows.py",
     "and leg not in LITEX_WORKERS[name]:",
     "and leg in LITEX_WORKERS[name]:",
     "Verilator set up on the builder workers instead of the LiteX workers"),
    ("S16", "scripts/ci_gate_workflows.py",
     "        retained += \"\\n${{ runner.temp }}/gate-results/litex-leg-*.json\\n\"",
     "        pass",
     "LiteX workers do not upload their leg receipt"),
    ("S17", "scripts/ci_litex_legs.py",
     "    table.unlink(missing_ok=True)",
     "    pass",
     "leg runner keeps a stale verdict table"),
    ("S18", "scripts/run_litex_sims.sh",
     "  rm -f \"$out\"/*.log \"$out/verdicts.tsv\"   # a stale log is not evidence\n  : > \"$out/verdicts.tsv\"",
     "  rm -f \"$out\"/*.log   # a stale log is not evidence\n  touch \"$out/verdicts.tsv\"",
     "runner appends to a stale verdict table"),
    ("S19", "scripts/ci_litex_legs.py",
     "    if max(loads) > LEG_BUDGET:",
     "    if False:",
     "leg budget refusal removed"),
    ("S20", "scripts/ci_gate_workflows.py",
     "    kept[\"run\"] = (\"\".join(line + \"\\n\" for line in preparation)\n                   + \"python3 scripts/ci_litex_legs.py run \"",
     "    kept[\"run\"] = (\"\"\n                   + \"python3 scripts/ci_litex_legs.py run \"",
     "LiteX legs drop the runner --selftest preparation line"),
    ("S21", "scripts/ci_litex_legs.py",
     "    rc = subprocess.run([*command, \"--only\", \",\".join(legs[leg])], cwd=ROOT, check=False).returncode",
     "    rc = subprocess.run([*command, \"--only\", \",\".join(legs[leg])], cwd=ROOT, check=False).returncode and 0",
     "leg runner records exit 0 whatever the runner returned"),
    ("S22", "scripts/ci_litex_legs.py",
     "        if receipt[\"selected\"] != legs[leg]:",
     "        if False:",
     "union trusts each receipt's own selection"),
    ("S23", "scripts/ci_gate_workflows.py",
     "LITEX_WORKERS = {\"elaborate\": (2, 3, 4)}",
     "LITEX_WORKERS = {\"elaborate\": (2, 3, 1)}",
     "leg 2 placed on builder worker 1 again"),
]


def run(cmd: list[str], log: Path, timeout: int = 900) -> int:
    with log.open("w") as fh:
        try:
            return subprocess.run(cmd, cwd=CLONE, stdout=fh, stderr=subprocess.STDOUT, timeout=timeout).returncode
        except subprocess.TimeoutExpired:
            fh.write("TIMEOUT\n")
            return 124


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    results = []
    wanted = set(os.environ.get("MUTANTS", "").split(",")) - {""}
    for mid, path, old, new, what in [("S0", None, None, None, "no mutation (baseline)"), *M]:
        if wanted and mid not in wanted:
            continue
        subprocess.run(["git", "checkout", "-q", "--", "."], cwd=CLONE, check=True)
        subprocess.run(["git", "clean", "-fdq"], cwd=CLONE, check=True)
        if path:
            target = CLONE / path
            text = target.read_text()
            assert text.count(old) == 1, (mid, text.count(old))
            target.write_text(text.replace(old, new))
        d = OUT / mid
        d.mkdir(exist_ok=True)
        gates = {}
        gates["regenerate"] = run([sys.executable, "scripts/ci_gate_workflows.py"], d / "regenerate.log")
        gates["gen_check"] = run([sys.executable, "scripts/ci_gate_workflows.py", "--check"], d / "gen_check.log")
        gates["runner_selftest"] = run(["bash", "scripts/run_litex_sims.sh", "--selftest"], d / "runner_selftest.log")
        gates["legs_selftest"] = run([sys.executable, "scripts/ci_litex_legs_selftest.py"], d / "legs_selftest.log")
        gates["gate_selftest"] = run([sys.executable, "scripts/ci_gate_workflows_selftest.py"], d / "gate_selftest.log")
        gates["scope_selftest"] = run([sys.executable, "scripts/ci_scope.py", "--selftest"], d / "scope_selftest.log") if mid in ("S0", "S23") else 0
        gates["e2e"] = run([sys.executable, str(HERE / "e2e_legs.py"), str(CLONE), str(d / "e2e")], d / "e2e.log")
        killers = [k for k, v in gates.items() if v != 0 and k != "regenerate"]
        results.append({"id": mid, "file": path, "breaks": what, "rc": gates,
                        "verdict": ("BASELINE-GREEN" if not killers else "BASELINE-RED") if mid == "S0"
                        else ("KILLED by " + ",".join(killers) if killers else "SURVIVED")})
        print(f"{mid:4} {results[-1]['verdict']:60} {what}", flush=True)
    subprocess.run(["git", "checkout", "-q", "--", "."], cwd=CLONE, check=True)
    subprocess.run(["git", "clean", "-fdq"], cwd=CLONE, check=True)
    (OUT / ("mutants-" + os.environ.get("MUTANTS_TAG", "all") + ".json")).write_text(json.dumps(results, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
