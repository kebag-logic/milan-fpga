#!/usr/bin/env python3
"""Two questions about the round-4 generative test's oracle (violations()).

Usage: probe_r4_oracle.py <repo checkout> <scratch dir>
1. Strict oracle at the head: add "check-baseline never exits 1" and "check exits 1 only with
   RESULT: MATERIAL REGRESSION" to violations(), in process, and run the fixtures' generated cases at
   two seeds. The head should keep both (0 failures), which shows the stricter oracle is sound.
2. The same strict oracle against the mutant "check-baseline problems exit 1", which the shipped oracle
   misses: the strict oracle should detect it.
3. Double mutant: the barrier narrowed to Refusal AND record()'s handler narrowed to OSError. Neither
   inner handler nor the barrier is left for a ValueError from a report: the shipped oracle should detect it.
Runs on copies of the three modules; never writes inside the checkout.
"""
from pathlib import Path
import shutil
import subprocess
import sys

repo, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
here = repo / "syn/ooc"
MODULES = ("pp_resource_gate.py", "pp_baseline_rank.py", "pp_resource_gate_selftest.py")
STRICT = '''
import sys, pp_resource_gate as g
shipped = g.violations
def strict(runs, broken):
    problems = shipped(runs, broken)
    for command, status, lines in runs:
        if command == "check-baseline" and status == 1:
            problems.append("check-baseline exit 1")
        if command == "check" and status == 1 and "RESULT: MATERIAL REGRESSION" not in lines:
            problems.append("check exit 1 without RESULT: MATERIAL REGRESSION")
    return problems
g.violations = strict
sys.exit(g.fuzz(int(sys.argv[1]), int(sys.argv[2])))
'''
SHIPPED = "import sys, pp_resource_gate as g; sys.exit(g.fuzz(int(sys.argv[1]), int(sys.argv[2])))"


def tree(name, edits):
    folder = scratch / name
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    for module in MODULES:
        shutil.copy(here / module, folder / module)
    for module, old, new in edits:
        text = (folder / module).read_text()
        assert text.count(old) == 1, (name, old)
        (folder / module).write_text(text.replace(old, new))
    return folder


def run(label, folder, code, cases, seed):
    result = subprocess.run([sys.executable, "-B", "-c", code, str(cases), str(seed)], cwd=folder,
                            capture_output=True, text=True, timeout=1800)
    lines = (result.stdout + result.stderr).strip().splitlines()
    first = next((line for line in lines if "FAILURE" in line), "")
    print(f"{label}: rc {result.returncode} :: {lines[-1] if lines else ''}")
    if first:
        print(f"    first failure: {first[:260]}")


head = tree("head", [])
run("1a head, strict oracle, 5000 @ 234", head, STRICT, 5000, 234)
run("1b head, strict oracle, 5000 @ 4474", head, STRICT, 5000, 4474)
cb1 = tree("cb1", [("pp_resource_gate.py", "            return 2 if problems else 0",
                    "            return 1 if problems else 0")])
run("2a check-baseline exit 1 mutant, shipped oracle, 2000 @ 234", cb1, SHIPPED, 2000, 234)
run("2b check-baseline exit 1 mutant, strict oracle, 2000 @ 234", cb1, STRICT, 2000, 234)
both = tree("both", [("pp_resource_gate.py", "    except Exception as error:  # the barrier",
                      "    except Refusal as error:  # the barrier"),
                     ("pp_resource_gate.py",
                      "    except (OSError, ValueError, KeyError, IndexError, TypeError, RecursionError) as error:",
                      "    except OSError as error:")])
run("3 barrier and record handler both narrowed, shipped oracle, 500 @ 234", both, SHIPPED, 500, 234)
