#!/usr/bin/env python3
"""Is the surviving "cat failure ignored" budget mutant outcome-equivalent?

Usage: python3 budget_equivalence_probe.py <checkout> <python>
Two spellings of the mutant are written into the generator in place; for each, the generator
self-test runs and the emitted shell is run over a mode-000 limit, and whether it exported
CI_CENSUS_JOBS and what it printed are recorded. The exact original bytes are restored.
"""
import pathlib
import subprocess
import sys

checkout = pathlib.Path(sys.argv[1])
python = sys.argv[2]
generator = checkout / "scripts" / "ci_runtime_workflows.py"
original = generator.read_bytes()
OLD = ('  if [ -e "$cgroup/memory.max" ]; then\n'
       '    if ! limit="$(cat "$cgroup/memory.max")"; then\n'
       '      echo "unreadable memory limit in $cgroup" >&2; exit 1\n'
       '    fi\n')
MUTANTS = {
    "cat failure swallowed (|| true)":
        '  if [ -e "$cgroup/memory.max" ]; then\n    limit="$(cat "$cgroup/memory.max" 2>/dev/null || true)"\n',
    "cat failure unguarded (errexit only)":
        '  if [ -e "$cgroup/memory.max" ]; then\n    limit="$(cat "$cgroup/memory.max")"\n',
}
PLANT = r'''
import pathlib, sys, tempfile
sys.path.insert(0, "scripts")
import ci_gate_workflows_selftest as t
gib = 1024 * 1024
with tempfile.TemporaryDirectory() as d:
    root = pathlib.Path(d)
    for name, cgroup, limits, denied in (("mode-000 limit", "/", {"": str(8 * 2**30)}, {"": "limit"}),
                                         ("limit is a directory", "/", {"": str(8 * 2**30)}, {"": "non-file"})):
        print(name, "->", t.census_budget(pathlib.Path(tempfile.mkdtemp(dir=root)), 16, 61 * gib, cgroup, limits, denied))
'''
try:
    text = original.decode()
    assert text.count(OLD) == 1
    for name, new in MUTANTS.items():
        generator.write_text(text.replace(OLD, new))
        selftest = subprocess.run([python, "scripts/ci_gate_workflows_selftest.py"], cwd=checkout,
                                  capture_output=True, text=True, check=False)
        planted = subprocess.run([python, "-c", PLANT], cwd=checkout, capture_output=True, text=True, check=False)
        print(f"== {name}: generator self-test rc {selftest.returncode}")
        print("  " + planted.stdout.strip().replace("\n", "\n  "), planted.stderr.strip()[-300:])
finally:
    generator.write_bytes(original)
print("restored:", generator.read_bytes() == original)
