"""Print the offline --dry-run transcript of the shipping rtl-full for slot 0 and slot 3 (128-CPU host).

Usage (inside a disposable boundary, cwd = tree root): python3 -I dryrun_r632_4.py <tree-root>
Uses the runner's own offline harness (dry_run_transcript): the real run_validation
with GitHub, git, the slot daemon and the Docker boundary stood in; nothing starts.
"""
import importlib.util
import pathlib
import sys

tree = pathlib.Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("act_ci_dry", tree / "scripts" / "act_ci.py")
m = importlib.util.module_from_spec(spec)
sys.modules["act_ci_dry"] = m
spec.loader.exec_module(m)
fixture = m.selftest_fixture()
run = m.ValidatedRun(fixture.pr, fixture.repository, fixture.base)
for number in (0, 3):
    rc, text = m.dry_run_transcript(run, "rtl-full", m.ReplaySlot(number), tree)
    print(f"===== slot {number}: rc={rc}")
    for line in text.splitlines():
        if "job container CPUs" in line or "--cpuset-cpus=" in line:
            print(line)
