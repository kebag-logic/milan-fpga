#!/usr/bin/env python3
"""Write disposable driver variants next to the engine mutation driver.

usage: make_variants.py <engine_dir>

<engine_dir> is tb/verilator/engine of a disposable extraction of the
reviewed head, holding mutants.py (head) and mutants_base.py (the base
commit's driver). Every variant is a new file in that directory, so the
driver's own relative paths (the RTL, the generator, the helper arms)
resolve exactly as for the real driver. The tracked files are not touched.

Variants:
  stub_*     the real driver with build/generate_image/run_harness replaced
             by fast fakes (random 0-30 ms delays, deterministic output),
             over the FULL mutant list, plus one planted fault each
  sub_*      the real driver restricted to a 5-mutant subset, with the
             real toolchain
"""
import sys
from pathlib import Path

ENG = Path(sys.argv[1]).resolve()
HEAD = (ENG / "mutants.py").read_text(encoding="utf-8")
BASE = (ENG / "mutants_base.py").read_text(encoding="utf-8")
MAIN_GUARD = 'if __name__ == "__main__":\n'

#: list indices of the real-toolchain subset: RTL mutants (slow: they build) at 0 and 3
#: and three generator mutants (fast: they
#: reuse the clean build), so completion order differs from list order
SUBSET = [0, 1, 2, 11, 12]

STUB = r'''
# ---- reviewer probe: fake toolchain -------------------------------------
import os
import json as _json, random as _random, threading as _threading, time as _time
_LOCK = _threading.Lock()
_BY_TAG = {"".join(c if c.isalnum() else "_" for c in _m[0]): _m
           for _m in MUTATIONS}
_RECORD = os.environ.get("PROBE_RECORD")

def _note(kind, path):
    if _RECORD:
        with _LOCK, open(_RECORD, "a") as _f:
            _f.write(_json.dumps([kind, str(path),
                                  _threading.get_ident()]) + "\n")

def build(srcdir, work, tag):
    mdir = work / f"obj_{tag}"
    mdir.mkdir(parents=True, exist_ok=False)   # a shared dir would collide
    _note("build", mdir)
    _time.sleep(_random.random() * 0.03)
    (mdir / "exe").write_text("fake")
    return mdir / "exe"

def generate_image(srcdir, rundir):
    rundir.mkdir(parents=True, exist_ok=True)
    _note("image", rundir)
    _time.sleep(_random.random() * 0.01)
    (rundir / "gptp_ucode.hex").write_text("fake")
    return True

def run_harness(exe, rundir):
    _note("run", rundir)
    _time.sleep(_random.random() * float(os.environ.get("PROBE_SLEEP", "0.03")))
    if not (rundir / "gptp_ucode.hex").is_file():
        raise RuntimeError(f"run dir vanished under a running task: {rundir}")
    tag = rundir.name.removeprefix("run_")
    if os.environ.get("PROBE_RAISE") == tag:
        raise OSError(f"planted harness crash in {tag}")
    if tag == "clean":
        return 0, "1 checks: 1 PASS, 0 FAIL\n"
    breaks = _BY_TAG[tag][4]
    wants = breaks.split(" | ")
    fails = "".join(f"FAIL {w} got 0 exp 1\n" for w in wants)
    return 1, fails + f"{len(wants) + 1} checks: 1 PASS, {len(wants)} FAIL\n"
# ---- end of reviewer probe ----------------------------------------------

'''

SUB = ("\n# ---- reviewer probe: a 5-mutant subset ----\n"
       f"MUTATIONS = [MUTATIONS[i] for i in {SUBSET!r}]\n\n")

# planted faults: (name, [(old, new), ...]); each old appears exactly once
FAULTS = {
    "none": [],
    # results yielded in completion order instead of list order
    "order": [("        for future in futures:\n            yield future.result()\n",
               "        from concurrent.futures import as_completed\n"
               "        for future in as_completed(futures):\n"
               "            yield future.result()\n")],
    # worker threads print their own lines as they go
    "print": [("run_mutant(work, clean_exe, mutation, lines.append), lines",
               "run_mutant(work, clean_exe, mutation, print), lines")],
    # the concurrent path silently drops the last task
    "droplast": [("        futures = [pool.submit(task) for task in tasks]\n",
                  "        futures = [pool.submit(task) for task in tasks[:-1]]\n")],
    # both modes abort right after the control (identical output)
    "abort": [("            # -- each mutant must be caught ----------------------------------\n",
               "            return 1\n")],
    # both modes skip the last mutant consistently (identical output)
    "short": [("args.jobs, [control, *map(planted, MUTATIONS)])",
               "args.jobs, [control, *map(planted, MUTATIONS[:-1])])")],
    # every mutant shares one directory (as one tag, so they collide)
    "shared": [('    own = Path(tempfile.mkdtemp(prefix="mutant-", dir=work))\n'
                '    srcdir = stage(own, tag, (fname, edits))\n',
                '    own = work\n'
                '    srcdir = stage(own, tag, (fname, edits))\n')],
}


def patched(text: str, edits) -> str:
    for old, new in edits:
        n = text.count(old)
        if n != 1:
            sys.exit(f"pattern appears {n} times: {old!r}")
        text = text.replace(old, new)
    return text


def insert(text: str, block: str) -> str:
    assert text.count(MAIN_GUARD) == 1
    return text.replace(MAIN_GUARD, block + MAIN_GUARD)


for name, edits in FAULTS.items():
    (ENG / f"stub_{name}.py").write_text(insert(patched(HEAD, edits), STUB))
(ENG / "stub_base.py").write_text(insert(BASE, STUB))
for name in ("none", "order"):
    (ENG / f"sub_{name}.py").write_text(insert(patched(HEAD, FAULTS[name]), SUB))
(ENG / "sub_base.py").write_text(insert(BASE, SUB))
#: the smallest real-toolchain subset that fits one foreground call on a
#: loaded host: the control and one generator mutant (no mutant build)
SUB1 = ("\n# ---- reviewer probe: a 1-mutant subset ----\n"
        "MUTATIONS = [MUTATIONS[1]]\n\n")
(ENG / "sub1_none.py").write_text(insert(HEAD, SUB1))
(ENG / "sub1_base.py").write_text(insert(BASE, SUB1))
print("variants:", sorted(p.name for p in ENG.glob("st*_*.py")) +
      sorted(p.name for p in ENG.glob("sub_*.py")))
