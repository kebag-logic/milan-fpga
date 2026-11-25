#!/usr/bin/env python3
"""Each planted defect removes one property from the engine's scheduled passes; passes_test.py must fail.

usage: python3 -I passes_plants.py ENGINE_DIR SCRATCH
Copies Makefile, pass_run.py and passes_test.py into SCRATCH/plant-<n>/, applies one substitution (its
anchor must occur exactly once), runs passes_test.py there, four at a time, and prints per plant: CAUGHT
or MISSED, the exit status and the test's [FAIL] lines.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

def _pass_line(n: int) -> str:
    """Pass n's recipe line in the Makefile under test."""
    if n == 0:
        return "\t@$(PASS) run 0 -- ./obj_dir/Vengine_sim\n"
    d, g, tail = [("seedrun", "--seq-seed 0x200000", ""), ("syncseedrun", "--sync-seq-seed 0x10000", ""),
                  ("p1run", "--p1 255 --clock-accuracy 0xFE", " +not-gm-capable")][n - 1]
    return (f"\t@$(PASS) run {n} --mkdir {d} --gen 'python3 $(GEN) $(GENARGS) {g} -o {d}/gptp_ucode.hex' \\\n"
            f"\t  --shell 'cd {d} && ../obj_dir/Vengine_sim{tail}'\n")


# The round-3 shape: one job starts all four passes at once; the other three pass targets do nothing.
ALL_AT_ONCE = [(_pass_line(0), "\t@" + " & ".join(_pass_line(n).strip().lstrip("@").replace("\\\n\t  ", "")
                                                  for n in range(4)) + " & wait\n")] + [
    (_pass_line(n), "\t@:\n") for n in (1, 2, 3)]
PLANTS = {
    "the four passes in one job (the round-3 recipe's shape)": ("Makefile", ALL_AT_ONCE, None),
    "the pass-0 echo printed under -s": (
        "Makefile", "$(if $(findstring s,$(firstword -$(MAKEFLAGS))),,--banner ./obj_dir/Vengine_sim)",
        "--banner ./obj_dir/Vengine_sim"),
    "-i not passed to the passes": (
        "Makefile", "PASS = python3 pass_run.py $(if $(findstring i,$(firstword -$(MAKEFLAGS))),--ignore-errors)",
        "PASS = python3 pass_run.py"),
    "a replay after a failure prints (make -k)": (
        "pass_run.py", '    """Pass N\'s banner, what it printed, then its own ending."""\n    if not ignoring and failed_before(n):',
        '    """Pass N\'s banner, what it printed, then its own ending."""\n    if False:'),
    "a signal death replayed as status 128+n": (
        "pass_run.py", "    if record.get(\"signal\"):\n        if not record.get(\"core\"):",
        "    if record.get(\"signal\"):\n        return 128 + record[\"signal\"]\n        if not record.get(\"core\"):"),
    "no fail-fast stop": (
        "pass_run.py", '    """Pass N failed: mark it, then stop every later pass still running."""\n',
        '    """Pass N failed: mark it, then stop every later pass still running."""\n    return\n'),
    "a transcript that cannot be printed is skipped": (
        "pass_run.py", "        print(f\"engine pass {n}: its transcript could not be printed ({exc})\", file=sys.stderr)\n"
        "        (STATE / f\"{n}.stop\").touch()\n        return 1\n",
        "        pass\n"),
    "signals not passed to the simulator": (
        "pass_run.py", "FORWARDED = (signal.SIGINT, signal.SIGTERM, signal.SIGQUIT, signal.SIGHUP)",
        "FORWARDED = ()"),
    "standard error kept with standard output": (
        "pass_run.py", "selector.register(proc.stderr, selectors.EVENT_READ, 2)",
        "selector.register(proc.stderr, selectors.EVENT_READ, 1)"),
}


def one(engine: Path, scratch: Path, n: int, name: str, plant: tuple[str, str, str]) -> str:
    work = scratch / f"plant-{n}"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    for f in ("Makefile", "pass_run.py", "passes_test.py"):
        shutil.copy(engine / f, work / f)
    target, old, new = plant
    text = (work / target).read_text()
    for o, n_ in (old if new is None else [(old, new)]):
        if text.count(o) != 1:
            return f"BAD-ANCHOR {name}: {o[:60]!r}"
        text = text.replace(o, n_)
    (work / target).write_text(text)
    run = subprocess.run([sys.executable, "-u", str(work / "passes_test.py")], capture_output=True, text=True,
                         timeout=1200)
    fails = [line[:170] for line in run.stdout.splitlines() if line.startswith("[FAIL]")]
    fails.sort(key=lambda line: "at once" not in line and "jobs" not in line)  # budget lines first
    shutil.rmtree(work)
    verdict = "CAUGHT" if run.returncode != 0 else "MISSED"
    return f"{verdict} rc={run.returncode} plant: {name} ({len(fails)} failing checks)\n" + "".join(
        f"    {line}\n" for line in fails[:4]) + (f"    {run.stderr.strip().splitlines()[-1][:170]}\n" if run.stderr.strip() else "")


def main() -> int:
    engine, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda item: one(engine, scratch, *item),
                                [(n, name, plant) for n, (name, plant) in enumerate(PLANTS.items())]))
    for line in results:
        print(line, end="" if line.endswith("\n") else "\n")
    caught = sum(line.startswith("CAUGHT") for line in results)
    print(f"{caught}/{len(PLANTS)} plants caught")
    return 0 if caught == len(PLANTS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
