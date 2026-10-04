#!/usr/bin/env python3
"""Campaign 2: planted defects in the round-2 code, each run IN MEMORY so the
tree is never written.

Resmap mutants go through the published R478-1 tool scripts/mutate_module.py
(sha256 e0a4c996...dde, copied unchanged into this packet): it reads one
module, replaces exactly one occurrence of OLD by NEW and runs that module's
own selftest(). Check-14 mutants go through check14_mutant.py (this packet),
which preloads a mutated nvm_allocation_table into sys.modules and then runs
check_nvm_record_space.py --self-test.

Usage: c2_mutations.py <head tree> <receipt dir> [jobs]
Writes <receipt dir>/c2_mutations.json and one log per mutant."""
import concurrent.futures
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TREE, OUT = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
JOBS = int(sys.argv[3]) if len(sys.argv) > 3 else 8
OUT.mkdir(parents=True, exist_ok=True)
YS, RM = "syn/resmap/yosys_sweep.py", "syn/resmap/resmap_models.py"
AT = "scripts/nvm_allocation_table.py"

# (id, tool, module, OLD, NEW, expectation) ; expectation red|green|info
MUTANTS = [
    ("ctl_ys", "mm", YS, "failures += outcome != expected", "failures += outcome != expected", "green"),
    ("ctl_rm", "mm", RM, 'result["guards"]["by_builder"] = builder', 'result["guards"]["by_builder"] = builder',
     "green"),
    ("ctl_at", "at", AT, "if len(row) != len(head):", "if len(row) != len(head):", "green"),
    # the round-1 survivors, as R478-1's required outcome spells them
    ("r3", "mm", YS, "failures += outcome != expected", 'failures += outcome == "failed"', "red"),
    ("r11", "mm", RM, 'result["guards"]["by_builder"] = builder', "pass", "red"),
    # the round-2 cause pin
    ("y_foreign_not_counted", "mm", YS, "failures += foreign", "failures += 0", "red"),
    ("y_foreign_false", "mm", YS, 'foreign = outcome == expected == "refused" and cause not in line',
     "foreign = False", "red"),
    ("y_cause_ignored_case", "mm", YS, 'foreign = outcome == expected == "refused" and cause not in line',
     'foreign = outcome == expected == "refused" and cause.upper() not in line.upper()', "info"),
    ("y_plan_cause_optional", "mm", YS,
     'raise PlanError(f"{name}: an expected refusal must pin its cause, a text of the refusal line")', "pass",
     "red"),
    ("y_plan_cause_on_built", "mm", YS,
     'raise PlanError(f"{name}: a cause is pinned on a variant the plan expects to build")', "pass", "red"),
    ("y_plan_expect_any", "mm", YS,
     "raise PlanError(f\"{name}: expect must be built or refused, not {spec['expect']!a}\")", "pass", "red"),
    ("y_crash_is_built", "mm", YS, 'return "failed", f"exit', 'return "built", f"exit', "red"),
    ("y_shapes_rc0", "mm", YS, "failures += outcome != expected\n        failures += foreign",
     "failures += 0", "red"),
    # the by_builder producer
    ("m_by_builder_every_point", "mm", RM,
     'builder = sorted(name for name, entry in summary.items() if "builder" in entry)',
     "builder = sorted(summary)", "red"),
    ("m_by_builder_always_written", "mm", RM,
     'if builder:\n        result["guards"]["by_builder"] = builder',
     'result["guards"]["by_builder"] = builder', "red"),
    ("m_build_ignores_plan_path", "mm", RM, "plan = yosys_sweep.load_plan(plan_path)",
     "plan = yosys_sweep.load_plan(yosys_sweep.PLAN)", "info"),
    # check 14's width rule (R479-1 F1)
    ("a_width_check_off", "at", AT, "if len(row) != len(head):", "if False:", "red"),
    ("a_width_off_nonstrict", "at", AT, "if len(row) != len(head):", "if False:", "red", "strict=True",
     "strict=False"),
    ("a_short_only", "at", AT, "if len(row) != len(head):", "if len(row) < len(head):", "red"),
    ("a_long_only", "at", AT, "if len(row) != len(head):", "if len(row) > len(head):", "red"),
    ("a_strict_off", "at", AT, "strict=True", "strict=False", "info"),
    ("a_width_no_continue", "at", AT,
     "findings.append(_allocation_width(where, head, row))\n            continue",
     "findings.append(_allocation_width(where, head, row))", "info"),
]


def run(m):
    ident, tool, module, old, new, want, *extra = m
    log = OUT / f"{ident}.log"
    if tool == "mm":
        argv = [sys.executable, str(HERE / "mutate_module.py"), str(TREE / module), old, new]
    else:
        argv = [sys.executable, str(HERE / "check14_mutant.py"), str(TREE), old, new, *extra]
    proc = subprocess.run(argv, cwd=TREE, capture_output=True, text=True, timeout=1200)
    text = proc.stdout + proc.stderr
    log.write_text(text)
    if tool == "mm":
        line = next((ln for ln in text.splitlines() if ln.startswith("SELFTEST rc=")), "")
        selftest_rc = int(line.split("=")[1]) if line else None
    else:
        selftest_rc = proc.returncode
    red = selftest_rc not in (0, None) or (selftest_rc is None and proc.returncode != 0)
    if "anchor occurs" in text:
        red, verdict = None, "ANCHOR-NOT-UNIQUE"
    else:
        verdict = "red" if red else "green"
    failures = [ln for ln in text.splitlines() if "FAILED" in ln or "SELF-TEST" in ln or "control" in ln.lower()]
    return {"id": ident, "module": module, "old": old, "new": new, "extra": extra, "expect": want,
            "verdict": verdict, "proc_rc": proc.returncode, "selftest_rc": selftest_rc,
            "as_expected": (want == "info") or (verdict == want), "evidence": failures[:6]}


with concurrent.futures.ThreadPoolExecutor(JOBS) as pool:
    results = list(pool.map(run, MUTANTS))
(OUT / "c2_mutations.json").write_text(json.dumps(results, indent=1) + "\n")
for r in results:
    print(f"{r['id']:32s} expect={r['expect']:5s} verdict={r['verdict']:6s} ok={r['as_expected']}")
print("ALL AS EXPECTED" if all(r["as_expected"] for r in results) else "SOME NOT AS EXPECTED")
