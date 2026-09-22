#!/usr/bin/env python3
"""R226-2: what exit code does check_em_dash.main() give when git refuses
inside the I440-E label rows (em_dash_arms), versus inside a planted control?

Usage: python3 -B refusal_in_label_rows.py <tree-root>
Runs main(["--selftest"]) in-process twice with an injected Refusal:
  A) raised by judge_page only while em_dash_arms is running;
  B) raised by judge() only while a planted _controls() arm runs (the path
     the file wraps and promises rc 2 for).
No file is modified; the injection is a monkeypatch in this process.
"""
import sys
import traceback
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "scripts"))
sys.dont_write_bytecode = True
import check_em_dash as gate  # noqa: E402
import gen_toc_closer_cases as closers  # noqa: E402

real_judge_page, real_run_control = gate.judge_page, gate._run_control


def run(label):
    try:
        rc = gate.main(["--selftest"])
        print(f"{label}: main returned rc={rc}")
    except BaseException as exc:  # what the CLI would do: traceback, exit 1
        print(f"{label}: main RAISED {type(exc).__name__}: {exc}")
        traceback.print_exc(limit=2, file=sys.stdout)
        print(f"{label}: an uncaught exception makes `python3 check_em_dash.py` exit 1")


# A) Refusal inside the I440-E rows
state = {"in_rows": False}
real_arms = closers.em_dash_arms


def arms_wrapper(g):
    state["in_rows"] = True
    try:
        return real_arms(g)
    finally:
        state["in_rows"] = False


def judge_page_a(*a, **k):
    if state["in_rows"]:
        raise gate.Refusal("git show: injected failure (probe A)")
    return real_judge_page(*a, **k)


closers.em_dash_arms = arms_wrapper
gate.judge_page = judge_page_a
run("A (Refusal inside em_dash_arms)")
closers.em_dash_arms, gate.judge_page = real_arms, real_judge_page


# B) Refusal inside a planted control
def run_control_b(repo, base, control):
    raise gate.Refusal("git diff: injected failure (probe B)")


gate._run_control = run_control_b
run("B (Refusal inside a planted control)")
gate._run_control = real_run_control
