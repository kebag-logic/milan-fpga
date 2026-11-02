#!/usr/bin/env python3
"""Reviewer probe mutants of scripts/owned_process.py for #833, run on owner_stated_seconds.

Usage: python3 -I r764_8_probes.py <repo-root> <scratch-dir>
Each probe copies scripts/ to <scratch-dir>/<name>, applies its edit (each old text must occur once),
runs `test_suite_cancellation.py --control owner_stated_seconds`, and prints red/green with the
failing listing's words. 'none' must be green.
"""
import shutil
import subprocess
import sys
from pathlib import Path

PROBES = {
    "none": (),
    # Row 6/7/8 hole in the interior of the later-past-grace class (7 s to 13 s): no window there.
    "interior-past-grace-no-window": (
        ("kill_all = max(kill_all, clock + TRAP_SECONDS)",
         "kill_all = max(kill_all, clock + TRAP_SECONDS) if not (7.0 <= clock < 13.0) else kill_all"),),
    # Row 7 hole for a lone shell resumed in the interior of the later-in-grace class.
    "interior-in-grace-lone-shell-killed": (
        ("(resumed is None or clock < kill_all):",
         "(resumed is None or clock < kill_all and not (0.5 <= resumed < 1.5 and clock > resumed"
         " and not any(parent == pid for _c, (parent, _s) in owned.items()))):"),),
    # Grace read as strictly past 2 s: the first SIGKILL pass would be the one after 2 s.
    "grace-strictly-past": (
        ("signum = signal.SIGKILL if clock >= deadline else signal.SIGTERM",
         "signum = signal.SIGKILL if clock > deadline else signal.SIGTERM"),),
    # A resume exactly at the grace deadline opens no window (first past-grace cell edge).
    "no-window-at-grace-edge": (
        ("kill_all = max(kill_all, clock + TRAP_SECONDS)",
         "kill_all = max(kill_all, clock + TRAP_SECONDS) if clock != deadline else kill_all"),),
    # The trap command loses the window only when it is first listed after the resume pass, past grace.
    "trap-command-spared-only-in-resume-pass-past-grace": (
        ("if (pid, start) not in initial and resumed is not None:",
         "if (pid, start) not in initial and resumed is not None and (resumed < deadline or clock == resumed):"),),
    # A new descendant beside a stopped shell gets SIGTERM only from the third pass on (in grace).
    "sigterm-new-beside-stopped-shell-late": (
        ("                    if (pid, start) not in initial:\n                        continue\n",
         "                    if (pid, start) not in initial and (resumed is not None or clock < 0.75):\n"
         "                        continue\n"),),
    # The resume is held one pass when the shell's last child left in the pass at 2 s exactly.
    "resume-held-at-grace-edge": (
        ("and root_pid in owned and not (live - {root_pid}):",
         "and root_pid in owned and not (live - {root_pid}) and clock != deadline:"),),
    # The verdict after a resume in grace comes 10 s after the window, from the grace deadline instead.
    "verdict-from-grace-after-in-grace-resume": (
        ("limit = kill_all + REAP_SECONDS",
         "limit = (max(kill_all, deadline + TRAP_SECONDS) if resumed is not None and resumed < deadline"
         " else kill_all) + REAP_SECONDS"),),
}


def main() -> int:
    root, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    for name, edits in PROBES.items():
        tree = scratch / name
        shutil.rmtree(tree, ignore_errors=True)
        shutil.copytree(root / "scripts", tree / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
        product = tree / "scripts/owned_process.py"
        text = product.read_text()
        for old, new in edits:
            assert text.count(old) == 1, f"{name}: edit does not apply once: {old!r}"
            text = text.replace(old, new)
        product.write_text(text)
        run = subprocess.run([sys.executable, "-B", str(tree / "scripts/test_suite_cancellation.py"), "--control",
                              "owner_stated_seconds"], cwd=tree, stdin=subprocess.DEVNULL, capture_output=True,
                             text=True, timeout=300)
        lines = [line for line in (run.stdout + run.stderr).splitlines() if line.strip()]
        print(f"{name}: {'red' if run.returncode else 'green'} rc {run.returncode}: {lines[-1][:260] if lines else ''}",
              flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
