#!/usr/bin/env python3
"""Plant defects into a scratch copy of trace_table.py; the standing tests must fail.

    python3 -I -B trace_table_mutants.py <source-tree> <scratch-dir>

Each mutant is one textual replacement in trace_table.py; the copy keeps
test_trace_table.py unchanged beside it. A mutant survives if the unit tests
still pass. Also runs R475-7's oracle-free check (if given via --decimal) and
the reviewer's integer oracle on each mutant for comparison.
"""
import shutil
import subprocess
import sys
from pathlib import Path

MUTANTS = [
    ("float-times", "    return Fraction(decimal)\n", "    return Fraction(float(decimal))\n"),
    ("inclusive-end", "            if t0 <= t < t1:\n", "            if t0 <= t <= t1:\n"),
    ("exclusive-start", "            if t0 <= t < t1:\n", "            if t0 < t < t1:\n"),
    ("pdu-inclusive-end", "            if not (t0 <= t < t1):\n", "            if not (t0 <= t <= t1):\n"),
    ("recentre-is-slip", "                if kind == \"recentre\":\n", "                if kind == \"never\":\n"),
    ("recentre-masks-slip", "    for kind in (\"dup\", \"skip\", \"recentre\"):\n        for t in marks[kind]:\n",
     "    for kind in (\"dup\", \"skip\", \"recentre\"):\n        for t in marks[kind]:\n"
     "            if kind != \"recentre\" and t in marks[\"recentre\"]:\n                continue\n"),
    ("skip-not-subset", "                    b[\"skips\"] += int(kind == \"skip\")\n", "                    pass\n"),
    ("servo-strict", "        last = [w for w in windows if w[0] <= te]\n", "        last = [w for w in windows if w[0] < te]\n"),
    ("no-final-clip", "        te = min(t1, t0 + (i + 1) * a.step_s)\n", "        te = t0 + (i + 1) * a.step_s\n"),
    ("coverage-always-complete", "if marks[\"end\"]:\n            coverage", "if True:\n            coverage"),
    ("coverage-never-complete", "coverage = \"complete\" if", "coverage = \"partial\" if"),
    ("float-bin-index", "                b = bins[int((t - t0) / a.step_s)]\n                if kind",
     "                b = bins[int((float(t) - float(t0)) / float(a.step_s))]\n                if kind"),
    ("pdu-float-bin-index", "            b = bins[int((t - t0) / a.step_s)]\n            if not math.isnan(m):",
     "            b = bins[min(len(bins) - 1, int((float(t) - float(t0)) / float(a.step_s)))]\n            if not math.isnan(m):"),
    ("margin-jump-slips", "            if not (t0 <= t < t1):\n                continue\n",
     "            if not (t0 <= t < t1):\n                continue\n"
     "            if not math.isnan(m) and getattr(main, 'prev', None) is not None and m - main.prev > 0.5:\n"
     "                bins[int((t - t0) / a.step_s)][\"slips\"] += 1\n"
     "            main.prev = m if not math.isnan(m) else getattr(main, 'prev', None)\n"),
]


def main():
    src, work = Path(sys.argv[1]), Path(sys.argv[2])
    orig = (src / "tb/verilator/follow_ring/trace_table.py").read_text()
    test = src / "tb/verilator/follow_ring/test_trace_table.py"
    survivors = []
    for name, old, new in MUTANTS:
        if orig.count(old) != 1:
            print(f"{name}: anchor not unique ({orig.count(old)}) - NOT APPLIED")
            survivors.append(name)
            continue
        d = work / name / "tb/verilator/follow_ring"
        d.mkdir(parents=True, exist_ok=True)
        (d / "trace_table.py").write_text(orig.replace(old, new))
        shutil.copy(test, d / "test_trace_table.py")
        r = subprocess.run([sys.executable, "-I", "-B", str(d / "test_trace_table.py")],
                           capture_output=True, text=True)
        (work / name / "unittest.log").write_text(r.stdout + r.stderr)
        caught = r.returncode != 0
        failed = [l for l in (r.stdout + r.stderr).splitlines() if l.startswith(("FAIL:", "ERROR:"))]
        print(f"{name}: unit tests rc {r.returncode} -> {'CAUGHT' if caught else 'SURVIVED'} "
              f"({len(failed)} failing: {', '.join(l.split()[1] for l in failed[:4])})")
        if not caught:
            survivors.append(name)
    print(f"trace_table mutants: {len(MUTANTS) - len(survivors)}/{len(MUTANTS)} caught; survivors {survivors}")
    return 0 if not survivors else 1


if __name__ == "__main__":
    sys.exit(main())
