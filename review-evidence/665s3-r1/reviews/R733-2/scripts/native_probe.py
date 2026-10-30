"""Reviewer probe: the split boot driver's NATIVE verdict, with no build.

Usage: python3 -B native_probe.py <checkout> <work-dir>

1. The checkout's own --native-controls (run.py's NATIVE_CONTROLS through its own stand-in), in process.
2. Extra controls of this reviewer's, through the same stand-in and grade: a model killed by a signal
   after a valid boot's observations (exit -11, no tally), a saved status that is not a number, and a
   tally line the sweep cannot read. Each must be NATIVE on its run and on its regrade (the unreadable
   status on its regrade).
3. Disposable copies of run.py, each with one part of the NATIVE check removed; at least one of the
   checkout's own native controls must then be graded WRONG, or the controls do not protect that part.
Exit 0 when all three hold.
"""
from __future__ import annotations

import contextlib
import types
import io
import shutil
import sys
from pathlib import Path

checkout, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
RUN = checkout / "tb/verilator/ctrl_split_boot/run.py"
SHAPE, N_IF = "endstation_ax7101_1x1_tdm8", 1


def load(path: Path, name: str):
    """Import a copy of run.py as a module of its own, its __file__ the checkout's run.py, so every path it
    derives (HERE, ROOT, the firmware tree) is the checkout's."""
    mod = types.ModuleType(name)
    mod.__file__ = str(RUN)
    sys.modules[name] = mod
    sys.path.insert(0, str(checkout / "scripts"))
    exec(compile(path.read_text(), str(path), "exec"), mod.__dict__)
    return mod


def quiet(fn, *args):
    """fn(*args), its stdout kept."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        value = fn(*args)
    return value, buf.getvalue()


def main() -> int:
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    bad = 0
    run = load(RUN, "run_head")
    wrong, text = quiet(run.native_controls, work / "head", SHAPE, N_IF)
    print(text.rstrip())
    print(f"PROBE 1 head native controls: {'as required' if wrong == 0 else 'WRONG'} ({wrong} wrong)")
    bad += wrong != 0

    # 2. extra controls
    C = run.Control
    extra = {
        "probe-killed-by-signal": (C(-11, "", True, "NATIVE", "NATIVE"), None),
        "probe-status-garbage": (C(0, run.PASSED, True, "PASS", "NATIVE"), "zero\n"),
        "probe-tally-unreadable": (C(0, "== ctrl_split_boot: checks: 1   failures: x ==\nRESULT: PASS\n",
                                     True, "NATIVE", "NATIVE"), None),
    }
    for name, (control, status_text) in extra.items():
        where = work / "extra" / name
        where.mkdir(parents=True)
        (ran, _), _ = quiet(run.point, where, SHAPE, N_IF, False, None, run.stand_in(where, SHAPE, N_IF, control))
        if status_text is not None:
            (where / run.STATUS).write_text(status_text)
        (regraded, _), _ = quiet(run.point, where, SHAPE, N_IF, True)
        got = (run.verdict(ran), run.verdict(regraded))
        ok = got == (control.run, control.regrade)
        bad += not ok
        print(f"PROBE 2 {name}: {'as required' if ok else 'WRONG'} (run {got[0]}, regrade {got[1]}; required "
              f"{control.run}, {control.regrade}); findings {ran} / {regraded}")

    # 3. the NATIVE check with one part removed: the shipped controls must notice
    src = RUN.read_text()
    cuts = {
        "status-ignored": ("    elif status != 0:\n        findings.append(f'NATIVE: the model exited {status}')\n",
                           ""),
        "missing-status-ignored": ("    if status is None:\n        findings.append(f'NATIVE: the run saved no exit "
                                   "status ({STATUS}), so how the model ended is unknown')\n    elif",
                                   "    if status is None:\n        pass\n    elif"),
        "nocount-ignored": ("    if suite_tally.is_nocount(checks, failures, matched, skipped):\n",
                            "    if False:\n"),
        "failure-ignored": ("    elif failed:\n", "    elif False:\n"),
        "regrade-reads-returncode-zero": ("        return int((out / STATUS).read_text())\n",
                                          "        return 0\n"),
        "run-not-saved": ("        (out / STATUS).write_text(f'{result.returncode}\\n')\n", ""),
    }
    for name, (old, new) in cuts.items():
        if src.count(old) != 1:
            print(f"PROBE 3 {name}: REFUSED, its anchor occurs {src.count(old)} times")
            bad += 1
            continue
        copy = work / "cuts" / name / "run.py"
        copy.parent.mkdir(parents=True)
        copy.write_text(src.replace(old, new))
        mod = load(copy, f"run_{name.replace('-', '_')}")
        wrong, text = quiet(mod.native_controls, work / "cuts" / name / "out", SHAPE, N_IF)
        caught = wrong > 0
        bad += not caught
        named = [ln.split(":")[0].removeprefix("NATIVE-CONTROL ") for ln in text.splitlines() if "WRONG" in ln]
        print(f"PROBE 3 {name}: {'killed' if caught else 'SURVIVED'} by {wrong} control(s) {named}")
    print(f"native_probe: {'PASS' if bad == 0 else 'FAIL'} ({bad} not as required)")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
