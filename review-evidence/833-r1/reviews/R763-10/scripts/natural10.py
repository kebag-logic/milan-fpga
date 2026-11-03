"""Round 10 reviewer mutants for #833: each on a reviewer listing, every owner control and the whole test.

Usage: python3 -I natural10.py <clean-tree> <scratch-dir> <jobs>
The reviewer listing is the head's owner_stated_seconds plus two listings written from row 3 of the cleanup
table: a parent from the first census, whose live child from the first census outlives its own SIGKILL,
beside and under a cancelled shell never resumed. Stated: SIGTERM parent and child at 0, SIGKILL child at 2,
parent at 4, and at 14 SIGKILL shell, parent and child, then the verdict. A survivor is red on the reviewer
listing and green on every owner control and the whole test.
"""
import concurrent.futures, os, shutil, subprocess, sys
from pathlib import Path

CLEAN, SCRATCH, JOBS = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), int(sys.argv[3])
CONTROLS = ("owner_stated_seconds", "owner_report", "owner_reparented", "owner_late_exit", "owner_stall",
            "owner_shell_window", "owner_survivor", "owner_vanishing", "owner_late_cancel", "owner_reused_identity")
PARENT = "if any(parent == pid and child in live for child, (parent, _start) in owned.items()):"
MUTANTS = {
    "none": [],
    # Beside or under a cancelled shell, a parent of a live child from the first census is not spared.
    "first-census-parent-unspared-beside-shell": [
        (PARENT, "if any(parent == pid and child in live and not (self.root_notified and (child, _start) in"
                 " initial) for child, (parent, _start) in owned.items()):")],
    # Control: no parent is spared beside a stopped shell; the head's never-resumed listings must catch it.
    "parent-unspared-beside-stopped-shell": [
        (PARENT, "if any(parent == pid and child in live and not (self.root_notified and resumed is None)"
                 " for child, (parent, _start) in owned.items()):")],
}
ANCHOR = "        stated_liveness(kept, cell, names, (survivor, shell, command, owner_pid, zombie))\n"
EXTRA = '''        for words, under in (("a stubborn parent beside a stopped shell", owner_pid),
                             ("a stubborn parent under a stopped shell", shell)):
            kept(words, lambda _clock, under=under: {shell: (owner_pid, "2"), parent: (under, "5"),
                                                     child: (parent, "4")},
                 [(0, "SIGTERM", "parent"), (0, "SIGTERM", "child"), (2, "SIGKILL", "child"),
                  (4, "SIGKILL", "parent"), *[(14, "SIGKILL", n) for n in ("shell", "parent", "child")],
                  (14, "verdict")], shell)
'''


def apply(name, edits):
    for suffix, extra in (("", False), ("-probe", True)):
        root = SCRATCH / (name + suffix)
        shutil.rmtree(root, ignore_errors=True)
        shutil.copytree(CLEAN / "scripts", root / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
        product = root / "scripts/owned_process.py"
        text = product.read_text()
        for old, new in edits:
            assert text.count(old) == 1, (name, old)
            text = text.replace(old, new)
        product.write_text(text)
        if extra:
            test = root / "scripts/test_suite_cancellation.py"
            body = test.read_text()
            assert body.count(ANCHOR) == 1
            test.write_text(body.replace(ANCHOR, EXTRA + ANCHOR))


def run(argv, cwd, timeout):
    env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
    try:
        p = subprocess.run(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                           timeout=timeout, start_new_session=True)
        return p.returncode, (p.stdout + p.stderr)
    except subprocess.TimeoutExpired:
        return None, "timeout"


def task(item):
    name, target = item
    if target == "probe":
        root = SCRATCH / (name + "-probe")
        rc, out = run([sys.executable, "-B", "scripts/test_suite_cancellation.py", "--control", "owner_stated_seconds"],
                      root, 150)
    else:
        root = SCRATCH / name
        argv = [sys.executable, "-B", "scripts/test_suite_cancellation.py"]
        rc, out = run(argv + (["--control", target] if target != "whole" else []), root, 150 if target != "whole" else 600)
    lines = [l for l in out.splitlines() if l.strip()]
    return name, target, rc, (lines[-1][:240] if lines else "")


def main():
    SCRATCH.mkdir(parents=True, exist_ok=True)
    for name, edits in MUTANTS.items():
        apply(name, edits)
    items = [(n, t) for n in MUTANTS for t in ("probe", *CONTROLS, "whole")]
    with concurrent.futures.ThreadPoolExecutor(JOBS) as pool:
        results = list(pool.map(task, items))
    for name in MUTANTS:
        rows = [r for r in results if r[0] == name]
        probe = next(r for r in rows if r[1] == "probe")
        reds = [r[1] for r in rows if r[1] != "probe" and r[2] != 0]
        verdict = "SURVIVOR" if probe[2] and not reds else "equivalent" if not probe[2] else "killed"
        print(f"{name}: {verdict}; reviewer listing rc {probe[2]}: {probe[3]}; red controls {reds}")
        for r in rows:
            if r[1] != "probe":
                print(f"    {r[1]}: rc {r[2]} {r[3]}")


main()
