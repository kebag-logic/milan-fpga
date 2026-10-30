"""#817: planted mutants against the constraint-presence check (sw/builder/test_clock_constraints.py).

Each mutant edits one tracked file in a scratch clone, runs the whole check with the LiteX interpreter,
records its exit status and the failure line, restores the file with git and requires a clean tree.
A mutant is KILLED when the check exits non-zero and its output carries the expected words.
usage: python3 mutants.py <clone> <out-dir> <litex-python>
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

clone, out, python = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
out.mkdir(parents=True, exist_ok=True)

MUTANTS = [
    ("M1-hook-call-removed", "sw/litex/milan_soc.py",
     "                    add_servo_reset_constraints(platform, self.crg)\n",
     "                    pass\n",
     "shipping servo reset synchronizer hook missing, duplicated or renamed: []"),
    ("M2-cut-removed", "sw/litex/clock_constraints.tcl",
     "    set_false_path -from $src -to $pin\n",
     "",
     "servo cut missing or widened: "),
    ("M3-cut-widened-to-every-clock", "sw/litex/clock_constraints.tcl",
     "    set_false_path -from $src -to $pin\n",
     "    set_false_path -to $pin\n",
     "servo cut missing or widened: "),
    ("M4-attribute-check-dropped", "sw/litex/clock_constraints.tcl",
     "        if {![string is true -strict [get_property ASYNC_REG $cell]]} {\n",
     "        if {0} {\n",
     "accepted: *lacks ASYNC_REG*"),
    ("M5-hook-skipped-with-servo-present", "sw/litex/milan_soc.py",
     '                if (optional_blocks or {}).get("media_clock_servo", True):\n',
     '                if not (optional_blocks or {}).get("media_clock_servo", True):\n',
     "shipping servo reset synchronizer hook missing, duplicated or renamed: []"),
]

results = []
for name, rel, old, new, words in MUTANTS:
    path = clone / rel
    text = path.read_text()
    assert text.count(old) == 1, f"{name}: anchor not unique in {rel}"
    path.write_text(text.replace(old, new))
    start = time.time()
    run = subprocess.run([python, "sw/builder/test_clock_constraints.py"], cwd=clone,
                         capture_output=True, text=True, timeout=3000,
                         env=dict(os.environ, PYTHONHASHSEED="0", TMPDIR=str(out.parent / "tmp")))
    seconds = round(time.time() - start)
    log = run.stdout + run.stderr
    (out / f"{name}.log").write_text(log)
    subprocess.run(["git", "checkout", "--", rel], cwd=clone, check=True)
    status = subprocess.run(["git", "status", "--short", "--untracked-files=no"], cwd=clone,
                            capture_output=True, text=True, check=True).stdout
    assert not status.strip(), f"{name}: clone not restored: {status}"
    found = words in log
    lines = [line for line in log.splitlines() if words.rstrip() in line]
    results.append({"mutant": name, "file": rel, "rc": run.returncode, "seconds": seconds,
                    "expected_words": words, "found": found,
                    "verdict": "KILLED" if run.returncode != 0 and found else "SURVIVED",
                    "failing_line": lines[0][:400] if lines else None})
    print(json.dumps(results[-1]), flush=True)

(out / "mutants.json").write_text(json.dumps(results, indent=2) + "\n")
survived = [r["mutant"] for r in results if r["verdict"] != "KILLED"]
print("MUTANTS:", "all killed" if not survived else "SURVIVED " + " ".join(survived))
sys.exit(1 if survived else 0)
