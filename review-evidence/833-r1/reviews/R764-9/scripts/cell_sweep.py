#!/usr/bin/env python3
"""Reviewer per-cell mutant sweep for owner_stated_seconds (#833, PR #834).

usage: cell_sweep.py CLONE SCRATCH OUT.json [--author] [--jobs N]

Each mutant of scripts/owned_process.py is applied to a copy of CLONE/scripts. The copy's
owner_stated_seconds control is put in record mode: every listing ("cell") prints CELL or
FAILCELL with its words instead of stopping at the first failure, so the result is the
exact set of cells each mutant turns red. A mutant red on no cell is a survivor of this
control; survivors are then run, unmodified test, on every owner control and the whole test.
With --author, the published MUTANTS are mapped the same way.
"""
import concurrent.futures
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

CLONE, SCRATCH, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
AUTHOR = "--author" in sys.argv
JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 16
sys.path.insert(0, str(CLONE / "scripts"))
import process_test_support  # noqa: E402

TERM = "                    if (pid, start) not in initial:\n                        continue\n                elif"
SPARE = "if (pid, start) not in initial and resumed is not None:"
RESUME = "and root_pid in owned and not (live - {root_pid}):"
PARENT = "if any(parent == pid and child in live for child, (parent, _start) in owned.items()):"
VERDICT = "            if clock >= limit and (owned or clock >= limit + REAP_SECONDS):"
SHELL = "(resumed is None or clock < kill_all):"
H = "5e-7"  # half a tick of the control's clock
RES = {  # resume classes, by the clock at the resume
    "R1-first-pass": f"resumed is not None and resumed < {H}",
    "R2-early-grace": f"resumed is not None and {H} <= resumed < 0.25",
    "R3-interior-grace": "resumed is not None and 0.25 <= resumed < 1.75",
    "R4-late-grace": "resumed is not None and 1.75 <= resumed < deadline",
    "R5-first-past": f"resumed is not None and deadline <= resumed < deadline + {H}",
    "R6-early-past": f"resumed is not None and deadline + {H} <= resumed < deadline + 0.25",
    "R7-interior-past": "resumed is not None and deadline + 0.25 <= resumed < 13.75",
    "R8-late-past": "resumed is not None and resumed >= 13.75",
}
CLK = {  # pass classes, by the clock of the pass
    "C1-first-pass": f"clock < {H}",
    "C2-early-grace": f"{H} <= clock < 0.25",
    "C3-interior-grace": "0.25 <= clock < 1.75",
    "C4-late-grace": "1.75 <= clock < deadline",
    "C5-first-past": f"deadline <= clock < deadline + {H}",
    "C6-early-past": f"deadline + {H} <= clock < deadline + 0.25",
    "C7-interior-past": "deadline + 0.25 <= clock < 13.75",
    "C8-late-past": "clock >= 13.75",
}
LIVE = {"live": "pid in live", "notlive": "pid not in live"}
SH = {"shell": "self.root_notified", "noshell": "not self.root_notified"}
NEWLIVE = "any((p, e[1]) not in initial and {} for p, e in owned.items())"


def mine() -> dict:
    """Every reviewer mutant: name -> list of (old, new) edits."""
    m = {}
    # A: SIGTERM a new descendant inside grace when P (product: never).
    for lk, lv in LIVE.items():
        for sk, sv in SH.items():
            m[f"A-sigterm-new/{lk}/{sk}/unresumed"] = [(TERM, TERM.replace(
                "not in initial:", f"not in initial and not ({lv} and {sv} and resumed is None):"))]
        for rk, rv in list(RES.items())[:4]:
            m[f"A-sigterm-new/{lk}/shell/{rk}"] = [(TERM, TERM.replace(
                "not in initial:", f"not in initial and not ({lv} and {rv}):"))]
    # B: SIGKILL a trap's command inside the shell's window when P (product: spared to kill_all).
    for lk, lv in LIVE.items():
        for rk, rv in RES.items():
            m[f"B-trap-command-unspared/{lk}/shell/{rk}"] = [(SPARE, SPARE.replace(
                ":", f" and not ({lv} and {rv}):"))]
    # C: spare a new descendant past 2 s with no resume when P (product: SIGKILL at 2 s).
    for lk, lv in LIVE.items():
        for sk, sv in SH.items():
            m[f"C-new-spared-unresumed/{lk}/{sk}"] = [(SPARE, SPARE.replace(
                "and resumed is not None:", f"and (resumed is not None or ({lv} and {sv} and clock < 3.0)):"))]
    # D: parent sparing by a new child (product: a live child, new or not, spares its parent to 4 s).
    for sk, sv in SH.items():
        m[f"D-live-new-child-spares-nothing/{sk}"] = [(PARENT, PARENT.replace(
            "child in live", f"child in live and not ((child, _start) not in initial and {sv})"))]
        m[f"D-notlive-new-child-spares/{sk}"] = [(PARENT, PARENT.replace(
            "child in live", f"(child in live or ((child, _start) not in initial and {sv}))"))]
    # E: a live new descendant does not hold the resume in pass class Q.
    for ck, cv in CLK.items():
        m[f"E-resume-ignores-live-new/{ck}"] = [(RESUME, RESUME.replace(
            "not (live - {root_pid})", f"not ({{p for p in live if (p, owned[p][1]) in initial or not ({cv})}}"
                                       " - {root_pid})"))]
    # F: a not-live descendant holds the resume in pass class Q: new, or from the first census.
    for origin, test in (("new", "not in initial"), ("initial", "in initial")):
        for ck, cv in CLK.items():
            m[f"F-resume-held-by-notlive-{origin}/{ck}"] = [(RESUME, RESUME.replace(
                "not (live - {root_pid})", f"not ((live | {{p for p in owned if (p, owned[p][1]) {test}"
                                           f" and p not in live and ({cv})}}) - {{root_pid}})"))]
    # G: a live new descendant postpones the verdict, or hastens it a pass, with or without the shell.
    newlive = "any((p, e[1]) not in initial and _live(p) for p, e in owned.items())"
    for key, cond in [("noshell", "not self.root_notified"), ("shell-unresumed", "self.root_notified and resumed is None"),
                      *[(f"shell-{rk}", rv) for rk, rv in RES.items()]]:
        m[f"G-verdict-postponed-by-live-new/{key}"] = [(VERDICT, VERDICT.replace(
            "):", f") and not ({cond} and {newlive}):"))]
        m[f"G-verdict-hastened-by-live-new/{key}"] = [(VERDICT, VERDICT.replace(
            "if clock >= limit and", f"if (clock >= limit or clock >= limit - 0.75 and {cond} and {newlive}) and"))]
    # H: the shell loses its window while its trap's command, live or not, is listed after a resume in class R.
    for lk, lv in LIVE.items():
        for rk, rv in RES.items():
            m[f"H-shell-unspared-beside-trap-command/{lk}/{rk}"] = [(SHELL, SHELL.replace(
                ":", f" and not ({rv} and clock > resumed and "
                     f"{NEWLIVE.format(lv.replace('pid', 'p'))}):"))]
    # X: contrived edges inside the late-in-grace cell (outside listed resumes; residue probes).
    m["X-sigterm-live-new-late-resume-gap-over-1us"] = [(TERM, TERM.replace(
        "not in initial:", "not in initial and not (pid in live and resumed is not None and resumed >= 1.5"
                           " and clock - resumed > 1e-6):"))]
    m["X-sigterm-live-new-late-resume-no-zombie"] = [(TERM, TERM.replace(
        "not in initial:", "not in initial and not (pid in live and resumed is not None and resumed >= 1.5"
                           " and all(p in live for p in owned)):"))]
    m["X-sigterm-notlive-new-late-resume-gap-over-1us"] = [(TERM, TERM.replace(
        "not in initial:", "not in initial and not (pid not in live and resumed is not None and resumed >= 1.5"
                           " and clock - resumed > 1e-6):"))]
    return m


RECORD = [
    ("        assert events == stated, f\"{words}'s stated seconds were not kept on the owner's clock: {events}\"",
     "        print(('FAILCELL ' if events != stated else 'CELL ') + words, flush=True)"),
    ("            events = starved_cleanup(owner, listing, names, stated, reaped)\n",
     "            try:\n                events = starved_cleanup(owner, listing, names, stated, reaped)\n"
     "            except Exception as exc:\n                events = [('raised', repr(exc))]\n"),
]


def tree(name: str, edits: list, record: bool) -> Path:
    root = SCRATCH / ("rec" if record else "raw") / name.replace("/", "__")
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(CLONE / "scripts", root / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    for rel, changes in (("scripts/owned_process.py", edits), ("scripts/test_suite_cancellation.py",
                                                              RECORD if record else [])):
        text = (root / rel).read_text()
        for old, new in changes:
            assert text.count(old) == 1, (name, rel, old)
            text = text.replace(old, new)
        (root / rel).write_text(text)
    return root


def run(root: Path, control: str | None) -> tuple:
    argv = [sys.executable, "-B", str(root / "scripts/test_suite_cancellation.py")]
    argv += ["--control", control] if control else []
    env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
    try:
        p = subprocess.run(argv, cwd=root, env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                           timeout=150 if control else 400, start_new_session=True)
        return p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return None, "cut at bound"


def cells(name: str, edits: list) -> dict:
    rc, out = run(tree(name, edits, True), "owner_stated_seconds")
    lines = out.splitlines()
    return dict(rc=rc, cells=[l[5:] for l in lines if l.startswith("CELL ")],
                red=[l[9:] for l in lines if l.startswith("FAILCELL ")], tail=lines[-1:] if lines else [])


def main() -> None:
    muts = {"none": []}
    if AUTHOR:
        muts.update({k: list(v[2:]) for k, v in process_test_support.MUTANTS.items() if k != "none"})
    else:
        muts.update(mine())
    with concurrent.futures.ThreadPoolExecutor(JOBS) as pool:
        result = dict(zip(muts, pool.map(lambda kv: cells(*kv), muts.items())))
    assert not result["none"]["red"] and result["none"]["rc"] == 0, result["none"]
    survivors = [k for k, v in result.items() if k != "none" and not v["red"]]
    controls = (*process_test_support_controls(), None)
    with concurrent.futures.ThreadPoolExecutor(JOBS) as pool:
        jobs = [(s, c) for s in survivors for c in controls]
        raw = {s: tree(s, muts[s], False) for s in survivors}
        outs = list(pool.map(lambda sc: run(raw[sc[0]], sc[1]), jobs))
    for (s, c), (rc, out) in zip(jobs, outs):
        result[s].setdefault("other", {})[c or "whole"] = [rc, (out.strip().splitlines() or [""])[-1][:200]]
    OUT.write_text(json.dumps(dict(edits={k: v for k, v in muts.items()}, result=result), indent=1))
    ncell = len(result["none"]["cells"])
    print(f"{len(muts) - 1} mutants, {ncell} cells in owner_stated_seconds (none: all pass)")
    for k, v in result.items():
        if k == "none":
            continue
        other = v.get("other")
        flag = "" if v["red"] else (" SURVIVOR-of-stated-seconds; other: " +
                                    ", ".join(f"{c}={o[0]}" for c, o in other.items()))
        print(f"{k}: red on {len(v['red'])} cell(s){flag}: {'; '.join(v['red'][:4])}"
              f"{' ...' if len(v['red']) > 4 else ''}")


def process_test_support_controls() -> tuple:
    src = (CLONE / "scripts/test_suite_cancellation.py").read_text()
    start = src.index("OWNER_CONTROLS = (")
    return tuple(eval(src[start + len("OWNER_CONTROLS = "):src.index(")", start) + 1]))


if __name__ == "__main__":
    main()
