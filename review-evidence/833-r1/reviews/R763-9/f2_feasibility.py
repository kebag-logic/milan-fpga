"""F2 feasibility: one listing added to a copy of the head's stated_liveness; green at head, red under F2's mutants.

Usage: python3 -I f2_feasibility.py <clean-tree> <scratch>
"""
import os, shutil, subprocess, sys
from pathlib import Path
CLEAN, SCRATCH = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
ANCHOR = "        # The survivor's trap starts it, and no shell is cancelled."
LISTING = '''        # Reviewer feasibility: the child's trap starts it beside a shell never resumed; both outlive 14 s.
        kept("a live new descendant beside a shell never resumed",
             lambda clock: {shell: (owner_pid, "2"), child: (shell, "4"), **({live: (child, "8")} if clock else {})},
             [(0, "SIGTERM", "child"), (2, "SIGKILL", "trap command"), (4, "SIGKILL", "child"),
              *[(14, "SIGKILL", name) for name in ("shell", "child", "trap command")], (14, "verdict")], shell)
'''
PARENT = "if any(parent == pid and child in live for child, (parent, _start) in owned.items()):"
LIMIT = "            limit = kill_all + REAP_SECONDS\n"
MUTANTS = {
    "none": [],
    "parent-of-live-new-unspared-beside-shell": [(PARENT, "if any(parent == pid and child in live and not (self.root_notified"
        " and (child, _start) not in initial) for child, (parent, _start) in owned.items()):")],
    "verdict-early-live-new-beside-stopped-shell": [(LIMIT, "            limit = kill_all + REAP_SECONDS - (0.25 if"
        " self.root_notified and resumed is None and any((p, e[1]) not in initial and _live(p) for p, e in owned.items())"
        " else 0)\n")],
}
for name, edits in MUTANTS.items():
    for with_listing in (False, True):
        root = SCRATCH / f"{name}-{int(with_listing)}"
        shutil.rmtree(root, ignore_errors=True)
        shutil.copytree(CLEAN / "scripts", root / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
        p = root / "scripts/owned_process.py"; t = p.read_text()
        for old, new in edits:
            assert t.count(old) == 1; t = t.replace(old, new)
        p.write_text(t)
        if with_listing:
            q = root / "scripts/test_suite_cancellation.py"; s = q.read_text()
            assert s.count(ANCHOR) == 1; q.write_text(s.replace(ANCHOR, LISTING + ANCHOR))
        r = subprocess.run([sys.executable, "-B", "scripts/test_suite_cancellation.py", "--control", "owner_stated_seconds"],
                           cwd=root, capture_output=True, text=True, timeout=120,
                           env={k: v for k, v in os.environ.items() if not k.startswith("PYTHON")})
        last = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()][-1]
        print(f"{name} / {'with' if with_listing else 'without'} the listing: rc {r.returncode}: {last[:160]}")
        shutil.rmtree(root, ignore_errors=True)
