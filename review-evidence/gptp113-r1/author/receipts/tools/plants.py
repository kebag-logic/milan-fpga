#!/usr/bin/env python3
"""PR #112's thirteen planted defects, each against the engine passes test at two layouts.

usage: python3 -I plants.py REPO OLD_REV NEW_REV SCRATCH [WORKERS]

For each layout (OLD_REV: the test beside the Makefile in tb/verilator/engine/; NEW_REV: the test in tb/),
stages the test, the engine Makefile and pass_run.py from that revision into SCRATCH/<arm>-<n>/ at their
repository paths, applies one plant (every anchor must occur exactly once), and runs the test from there.
A control with no plant runs per layout too and must pass. Prints CAUGHT/MISSED per plant and layout,
with the test's [FAIL] lines, and exits 0 only when every plant is caught at both layouts and both controls
pass.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

MK = "tb/verilator/engine/Makefile"
RUN = "tb/verilator/engine/pass_run.py"
TESTS = {"old": "tb/verilator/engine/passes_test.py", "new": "tb/engine_passes_test.py"}


def _pass_line(n: int) -> str:
    """Pass n's recipe line in the Makefile under test."""
    if n == 0:
        return "\t@$(PASS) run 0 -- ./obj_dir/Vengine_sim\n"
    d, g, tail = [("seedrun", "--seq-seed 0x200000", ""), ("syncseedrun", "--sync-seq-seed 0x10000", ""),
                  ("p1run", "--p1 255 --clock-accuracy 0xFE", " +not-gm-capable")][n - 1]
    return (f"\t@$(PASS) run {n} --mkdir {d} --gen 'python3 $(GEN) $(GENARGS) {g} -o {d}/gptp_ucode.hex' \\\n"
            f"\t  --shell 'cd {d} && ../obj_dir/Vengine_sim{tail}'\n")


ALL_AT_ONCE = [(_pass_line(0), "\t@" + " & ".join(_pass_line(n).strip().lstrip("@").replace("\\\n\t  ", "")
                                                  for n in range(4)) + " & wait\n")] + [
    (_pass_line(n), "\t@:\n") for n in (1, 2, 3)]

#: name -> [(file, old, new), ...]
PLANTS: dict[str, list[tuple[str, str, str]]] = {
    "the four passes in one job": [(MK, o, n) for o, n in ALL_AT_ONCE],
    "the pass-0 echo printed under -s": [(
        MK, "$(if $(findstring s,$(firstword -$(MAKEFLAGS))),,--banner ./obj_dir/Vengine_sim)",
        "--banner ./obj_dir/Vengine_sim")],
    "-i not passed to the passes": [(
        MK, "PASS = python3 pass_run.py $(if $(findstring i,$(firstword -$(MAKEFLAGS))),--ignore-errors)",
        "PASS = python3 pass_run.py")],
    "the -k suppression removed (a replay after a failure prints)": [(
        RUN, '    """Pass N\'s banner, what it printed, then its own ending."""\n    if not ignoring and failed_before(n):',
        '    """Pass N\'s banner, what it printed, then its own ending."""\n    if False:')],
    "a simulator's signal death replayed as status 128+n": [(
        RUN, '        reraise(record["signal"], record.get("core", False))',
        '        return 128 + record["signal"]')],
    "no fail-fast stop": [(
        RUN, '    """Pass N failed: mark it, then stop every later pass still running."""\n',
        '    """Pass N failed: mark it, then stop every later pass still running."""\n    return\n')],
    "a print failure ignored": [(
        RUN, "        print(f\"engine pass {n}: its transcript could not be printed ({exc})\", file=sys.stderr)\n"
             "        (STATE / f\"{n}.stop\").touch()\n        return 1\n",
        "        pass\n")],
    "signals not forwarded": [(
        RUN, "FORWARDED = (signal.SIGINT, signal.SIGTERM, signal.SIGQUIT, signal.SIGHUP)", "FORWARDED = ()")],
    "standard error merged into standard output": [(
        RUN, "selector.register(proc.stderr, selectors.EVENT_READ, 2)",
        "selector.register(proc.stderr, selectors.EVENT_READ, 1)")],
    "the generator without the serial redirection, its signal death replayed as 256-n": [
        (RUN, 'generate + " >/dev/null"', "generate"),
        (RUN, '            record.update(gen_signal=os.WTERMSIG(status), gen_core=os.WCOREDUMP(status))\n'
              '        record["gen"] = os.WEXITSTATUS(status) if os.WIFEXITED(status) else 0\n',
              '            pass\n        record["gen"] = gen.returncode % 256\n')],
    "a generator's own signal death not re-raised at replay": [(
        RUN, '    if record.get("gen_signal"):\n        reraise(record["gen_signal"], record.get("gen_core", False))\n',
        '')],
    "the replay re-raising in make's directory": [(
        RUN, "    os.chdir(STATE)  # a relative file core_pattern", "    pass  # a relative file core_pattern")],
    "a no-core replay left dumpable": [(
        RUN, "        ctypes.CDLL(None, use_errno=True).prctl(PR_SET_DUMPABLE, 0, 0, 0, 0)\n", "        pass\n")],
}


def show(repo: Path, rev: str, path: str) -> str:
    """`path`'s text at `rev`."""
    return subprocess.run(["git", "show", f"{rev}:{path}"], cwd=repo, capture_output=True, text=True,
                          check=True).stdout


def one(job: tuple[Path, str, str, Path, str, list[tuple[str, str, str]]]) -> tuple[str, str, bool]:
    """Stage one arm, plant it, run its test; (arm, report, caught-or-passed as required)."""
    repo, arm, rev, work, name, edits = job
    shutil.rmtree(work, ignore_errors=True)
    texts = {p: show(repo, rev, p) for p in (MK, RUN, TESTS[arm])}
    for target, old, new in edits:
        if texts[target].count(old) != 1:
            return arm, f"BAD-ANCHOR [{arm}] {name}: {old[:70]!r}", False
        texts[target] = texts[target].replace(old, new)
    for p, text in texts.items():
        (work / p).parent.mkdir(parents=True, exist_ok=True)
        (work / p).write_text(text)
    run = subprocess.run([sys.executable, "-u", str(work / TESTS[arm])], capture_output=True, text=True,
                         timeout=1800)
    fails = [line[:160] for line in run.stdout.splitlines() if line.startswith("[FAIL]")]
    passes = sum(line.startswith("[PASS]") for line in run.stdout.splitlines())
    shutil.rmtree(work, ignore_errors=True)
    if not edits:
        ok = run.returncode == 0 and not fails
        head = f"{'PASS' if ok else 'FAIL'} [{arm}] control, no plant: rc={run.returncode}, {passes} PASS, {len(fails)} FAIL"
    else:
        ok = run.returncode != 0
        head = f"{'CAUGHT' if ok else 'MISSED'} [{arm}] {name}: rc={run.returncode}, {len(fails)} failing checks"
    return arm, head + "\n" + "".join(f"    {line}\n" for line in fails[:3]), ok


def main() -> int:
    """Every plant at both layouts, plus a control per layout."""
    repo, old, new, scratch = Path(sys.argv[1]), sys.argv[2], sys.argv[3], Path(sys.argv[4]).resolve()
    workers = int(sys.argv[5]) if len(sys.argv) > 5 else 3
    #: optional: only these "arm:n" jobs (n a plant index or "control"), to finish an interrupted matrix
    only = set(sys.argv[6].split(",")) if len(sys.argv) > 6 else None
    jobs = []
    for arm, rev in (("old", old), ("new", new)):
        jobs.append((repo, arm, rev, scratch / f"{arm}-control", "control", []))
        for n, (name, edits) in enumerate(PLANTS.items()):
            jobs.append((repo, arm, rev, scratch / f"{arm}-{n}", name, edits))
    if only is not None:
        jobs = [j for j in jobs if j[3].name.replace("-", ":", 1) in only]
    results = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for result in pool.map(one, jobs):  # printed as each finishes, in job order
            results.append(result)
            print(result[1], end="", flush=True)
    for arm in ("old", "new"):
        planted = [ok for a, r, ok in results if a == arm and "control" not in r.split("\n")[0]]
        print(f"[{arm}] {sum(planted)}/{len(planted)} plants caught")
    return 0 if all(ok for _a, _r, ok in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
