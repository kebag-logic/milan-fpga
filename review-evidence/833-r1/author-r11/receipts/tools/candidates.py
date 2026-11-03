"""Candidate mutants for round 9: the reviewers' round 8 edits, read from their published scripts, and edge mutants."""
import ast
import runpy
from pathlib import Path

PROBES = Path("$VALIDATION_STORAGE/833-a726j/probes")


def published_r763_8() -> dict:
    """R763-8's MINE, by running only its constants and MINE assignment from r8_mutants.py."""
    tree = ast.parse((PROBES / "r763-8/r8_mutants.py").read_text())
    keep = [node for node in tree.body if isinstance(node, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id in ("RESUME", "NEW_TERM", "MINE") for t in node.targets)]
    scope = {}
    exec(compile(ast.Module(body=keep, type_ignores=[]), "r8_mutants.py", "exec"), scope)
    return {name: (edit,) for name, edit in scope["MINE"].items()}


R763_8 = published_r763_8()
R764_8_LIVE = runpy.run_path(str(PROBES / "r764-8/probes/r764_8_live_probes.py"))["PROBES"]
R764_8_EDGE = {name: edits for name, edits in
               runpy.run_path(str(PROBES / "r764-8/probes/r764_8_probes.py"))["PROBES"].items() if edits}

NEW_TERM = "                    if (pid, start) not in initial:\n                        continue\n                elif"
WINDOW = "if (pid, start) not in initial and resumed is not None:"
LATE = (("passes = 0\n", "passes = late = 0\n"),
        ("            last = now\n", "            last = now\n            late += clock >= deadline\n"))


def term(condition: str) -> tuple:
    """New descendants get SIGTERM unless the condition holds."""
    return (NEW_TERM, "                    if (pid, start) not in initial and " + condition + ":\n"
                      "                        continue\n                elif")


EDGES = {
    "first-pass-live-trap-command-sigtermed": (
        ("resumed = clock\n", "resumed, edge = clock, passes == 1\n"),
        term("not (resumed is not None and edge and pid in live)")),
    "second-pass-live-trap-command-sigtermed": (
        ("resumed = clock\n", "resumed, edge = clock, passes == 2\n"),
        term("not (resumed is not None and edge and pid in live)")),
    "last-in-grace-live-trap-command-unspared": (
        ("passes = 0\n", "passes = 0\n        early = set()\n"),
        ("            signum = signal.SIGKILL if clock >= deadline else signal.SIGTERM\n",
         "            signum = signal.SIGKILL if clock >= deadline else signal.SIGTERM\n"
         "            early |= set(owned) if clock < deadline else set()\n"),
        (WINDOW, WINDOW[:-1] + " and not (pid in live and resumed < deadline and pid not in early):")),
    "first-past-grace-live-trap-command-unspared": (
        *LATE, ("resumed = clock\n", "resumed, edge = clock, late == 1\n"),
        (WINDOW, WINDOW[:-1] + " and not (edge and pid in live):")),
    "second-past-grace-live-trap-command-unspared": (
        *LATE, ("resumed = clock\n", "resumed, edge = clock, late == 2\n"),
        (WINDOW, WINDOW[:-1] + " and not (edge and pid in live):")),
    "last-pass-live-trap-command-unspared": (
        ("resumed = clock\n", "resumed, edge = clock, clock + MAX_PASS_SECONDS >= kill_all + REAP_SECONDS\n"),
        (WINDOW, WINDOW[:-1] + " and not (edge and pid in live):")),
    "resume-past-grace-beside-live-new": (
        ("and root_pid in owned and not (live - {root_pid}):",
         "and root_pid in owned and not ({p for p in live if (p, owned[p][1]) in initial or clock < deadline}"
         " - {root_pid}):"),),
    "live-new-sigtermed-beside-stopped-shell": (
        term("not (pid in live and resumed is None and self.root_notified)"),),
    "live-new-sigtermed-with-no-shell": (
        term("not (pid in live and not self.root_notified)"),),
    "next-to-last-in-grace-live-trap-command-sigtermed": (
        term("not (pid in live and resumed is not None and resumed >= deadline - MAX_PASS_SECONDS)"),),
    "next-to-last-in-grace-trap-command-sigtermed": (
        term("not (pid not in live and resumed is not None and resumed >= deadline - MAX_PASS_SECONDS)"),),
}

CANDIDATES = {"none": (), **R763_8, **R764_8_LIVE, **R764_8_EDGE, **EDGES}
