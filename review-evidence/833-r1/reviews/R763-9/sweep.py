"""Reviewer mutant sweep for #833: each stated row's behaviour, perturbed in one cell at a time.

Usage: python3 -I sweep.py <clean-tree> <scratch-dir> <jobs> [name-filter]
Cells: resume class (by the resume's clock, or the clock at the event before any resume) x liveness of a
descendant new since the first census (none, not live, live, any) x with or without a cancelled shell.
For each mutant: apply its edits to a copy of scripts/ (each edit must match once), run probe_cells.py
(does the mutant change a stated behaviour in some cell?), then the repository's owner_stated_seconds and,
if that is green, every other owner control. A survivor is a mutant red on the probe and green on every
owner control. Prints one line per mutant and a summary.
"""
import concurrent.futures
import os
import shutil
import subprocess
import sys
from pathlib import Path

CLEAN, SCRATCH, JOBS = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), int(sys.argv[3])
FILTER = sys.argv[4] if len(sys.argv) > 4 else ""
PROBE = Path(__file__).resolve().parent / "probe_cells.py"
CONTROLS = ("owner_stated_seconds", "owner_report", "owner_reparented", "owner_late_exit", "owner_stall",
            "owner_shell_window", "owner_survivor", "owner_vanishing", "owner_late_cancel", "owner_reused_identity")

# Classes of time X, X being the resume's clock ("resumed") or the clock at the event ("clock").
CLASSES = {
    "first": "{x} < 5e-7", "second": "5e-7 <= {x} < 0.25", "half": "0.25 <= {x} < 0.75",
    "one": "0.75 <= {x} < 1.25", "one-half": "1.25 <= {x} < 1.9", "next-to-last-in-grace": "1.9 <= {x} < 2 - 1.4e-6",
    "last-in-grace": "2 - 1.4e-6 <= {x} < 2", "first-past": "{x} == 2.0", "second-past": "2 < {x} < 2.25",
    "two-half": "2.25 <= {x} < 2.75", "three": "2.75 <= {x} < 3.25", "four": "3.25 <= {x} < 4.75",
    "five-half": "4.75 <= {x} < 7.5", "ten": "7.5 <= {x} < 13.9", "last-pass": "13.9 <= {x} < 14",
}
NEW = "((_p, _e[1]) not in initial for _p, _e in owned.items())"
LIVENESS = {
    "none": f"not any{NEW}",
    "fake": "any((_p, _e[1]) not in initial and not owned_process_live(_p) for _p, _e in owned.items())",
    "live": "any((_p, _e[1]) not in initial and owned_process_live(_p) for _p, _e in owned.items())",
    "any": "True",
}
SHELLS = {"shell": "self.root_notified", "noshell": "not self.root_notified"}

L_TERM_NEW = "                    if (pid, start) not in initial:\n                        continue\n"
L_RESUME = "if self.root_notified and resumed is None and root_pid in owned and not (live - {root_pid}):"
L_WINDOW = "                kill_all = max(kill_all, clock + TRAP_SECONDS)\n"
L_SIGNUM = "            signum = signal.SIGKILL if clock >= deadline else signal.SIGTERM\n"
L_SHELL = "if pid == root_pid and self.root_notified and (resumed is None or clock < kill_all):"
L_PARENT = "if any(parent == pid and child in live for child, (parent, _start) in owned.items()):"
L_TRAP = "if (pid, start) not in initial and resumed is not None:"
L_LIMIT = "            limit = kill_all + REAP_SECONDS\n"
L_KILLALL = "                elif clock < kill_all:\n"
HELPER = ("def _live(pid: int) -> bool:\n",
          "def owned_process_live(pid: int) -> bool:\n    return _live(pid)\n\n\ndef _live(pid: int) -> bool:\n")


def cond(x, cls, liv, sh):
    parts = [f"({CLASSES[cls].format(x=x)})"] if cls else []
    if x == "resumed" and cls:
        parts.insert(0, "resumed is not None")
    parts += [f"({LIVENESS[liv]})", SHELLS[sh]] if sh else [f"({LIVENESS[liv]})"]
    return "(" + " and ".join(parts) + ")"


def perturbations(c, cr):
    """Each stated behaviour broken under condition c (clock classes) or cr (resume classes)."""
    return {
        # Row 2: a new descendant gets SIGTERM / a first-census one does not / grace boundary.
        "r2-sigterm-new": [(L_TERM_NEW, f"                    if (pid, start) not in initial and not {c}:\n"
                                        "                        continue\n")],
        "r2-sigterm-new-after-resume": [(L_TERM_NEW, f"                    if (pid, start) not in initial and not {cr}:\n"
                                                     "                        continue\n")],
        "r2-skip-initial-term": [(L_TERM_NEW, f"                    if (pid, start) not in initial or {c}:\n"
                                              "                        continue\n")],
        "r2-grace-early": [(L_SIGNUM, "            signum = signal.SIGKILL if clock >= deadline or "
                                      f"{c} else signal.SIGTERM\n")],
        "r2-sigterm-resumed-shell": [(L_SHELL, L_SHELL[:-1] + f" and not ({cr} and clock == resumed):")],
        # Row 3: a parent of a live child is killed before 4 s / anything not windowed is spared past 4 s.
        "r3-parent-unspared": [(L_PARENT, L_PARENT[:-1] + f" and not {c}:")],
        "r3-kill-all-late": [(L_KILLALL, f"                elif clock < kill_all + (0.25 if {c} else 0):\n")],
        "r3-kill-all-late-r": [(L_KILLALL, f"                elif clock < kill_all + (0.25 if {cr} else 0):\n")],
        # Row 4: the verdict a pass late or early.
        "r4-verdict-late": [(L_LIMIT, f"            limit = kill_all + REAP_SECONDS + (0.25 if {c} else 0)\n")],
        "r4-verdict-early": [(L_LIMIT, f"            limit = kill_all + REAP_SECONDS - (0.25 if {c} else 0)\n")],
        "r4-verdict-late-r": [(L_LIMIT, f"            limit = kill_all + REAP_SECONDS + (0.25 if {cr} else 0)\n")],
        "r4-verdict-early-r": [(L_LIMIT, f"            limit = kill_all + REAP_SECONDS - (0.25 if {cr} else 0)\n")],
        # Row 5: the resume held a pass / taken while another lives.
        "r5-resume-held": [(L_RESUME, L_RESUME[:-1] + f" and not {c}:")],
        "r5-resume-early": [(L_RESUME, "if self.root_notified and resumed is None and root_pid in owned and "
                                       f"(not (live - {{root_pid}}) or {c}):")],
        # Row 6: the window shorter or longer, set at the resume or later.
        "r6-window-short": [(L_WINDOW, f"                kill_all = max(kill_all, clock + TRAP_SECONDS - "
                                       f"(0.25 if {cr} else 0))\n")],
        "r6-window-long": [(L_WINDOW, f"                kill_all = max(kill_all, clock + TRAP_SECONDS + "
                                      f"(0.25 if {cr} else 0))\n")],
        "r6-window-cut-later": [(L_SIGNUM, f"            kill_all = resumed + TRAP_SECONDS - 0.25 if {cr} else "
                                           "kill_all\n" + L_SIGNUM)],
        # Row 7: the shell killed inside its window.
        "r7-shell-killed-early": [(L_SHELL, L_SHELL[:-1] + f" and not ({cr} and clock >= resumed + 9.75):")],
        "r7-shell-killed-in-resume-pass": [(L_SHELL, L_SHELL[:-1] + f" and not ({cr} and clock == resumed "
                                                                    "and clock >= deadline):")],
        # Row 8: the trap's command killed inside the window / given none.
        "r8-trap-no-window": [(L_TRAP, L_TRAP[:-1] + f" and not {cr}:")],
        "r8-trap-killed-early": [(L_TRAP, L_TRAP[:-1] + f" and not ({cr} and clock >= resumed + 9.75):")],
        "r8-trap-no-window-c": [(L_TRAP, L_TRAP[:-1] + f" and not {c}:")],
    }


def mutants():
    out = {}
    for liv in LIVENESS:
        for sh in (*SHELLS, None):
            for cls in (*CLASSES, None):
                c = cond("clock", cls, liv, sh)
                cr = cond("resumed", cls, liv, sh) if cls else "(resumed is not None and " + cond("clock", None, liv, sh) + ")"
                for pname, edits in perturbations(c, cr).items():
                    out[f"{pname}|{cls or 'all'}|{liv}|{sh or 'either'}"] = [HELPER, *edits]
    return out


def apply(name, edits):
    root = SCRATCH / name.replace("|", "__")
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(CLEAN / "scripts", root / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    product = root / "scripts/owned_process.py"
    text = product.read_text()
    for old, new in edits:
        assert text.count(old) == 1, (name, old)
        text = text.replace(old, new)
    product.write_text(text)
    return root


def run(argv, cwd, timeout):
    env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
    try:
        p = subprocess.run(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                           timeout=timeout, start_new_session=True)
        return p.returncode, (p.stdout + p.stderr)
    except subprocess.TimeoutExpired:
        return None, "timeout"


def one(item):
    name, edits = item
    root = apply(name, edits)
    rc, out = run([sys.executable, "-I", str(PROBE), str(root)], root, 120)
    probe = "red" if rc else "green"
    cells = [line.split(":")[0][5:] for line in out.splitlines() if line.startswith("CELL ")]
    if rc is None or (rc and not cells):
        probe = f"probe-error {out.strip().splitlines()[-1:] if out.strip() else ''}"
    caught = None
    if probe == "red":
        for control in CONTROLS:
            crc, cout = run([sys.executable, "-B", str(root / "scripts/test_suite_cancellation.py"), "--control",
                             control], root, 150)
            if crc != 0:
                caught = control
                break
    shutil.rmtree(root, ignore_errors=True)
    verdict = ("equivalent" if probe == "green" else "SURVIVOR" if probe == "red" and caught is None
               else f"killed by {caught}" if probe == "red" else probe)
    return name, verdict, cells


def main():
    SCRATCH.mkdir(parents=True, exist_ok=True)
    items = [(n, e) for n, e in mutants().items() if FILTER in n]
    with concurrent.futures.ThreadPoolExecutor(JOBS) as pool:
        results = list(pool.map(one, items))
    survivors = 0
    for name, verdict, cells in results:
        survivors += verdict == "SURVIVOR"
        print(f"{name}: {verdict}" + (f" cells={cells}" if verdict == "SURVIVOR" else f" ncells={len(cells)}"), flush=True)
    counts = {}
    for _n, v, _c in results:
        key = "killed" if v.startswith("killed") else v
        counts[key] = counts.get(key, 0) + 1
    print(f"sweep: {len(results)} mutants {counts} survivors={survivors}")


main()
