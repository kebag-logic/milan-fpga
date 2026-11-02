#!/usr/bin/env python3
"""Reviewer probes for #833: mutants that condition on whether a new descendant is live.

Usage: python3 -I r764_8_live_probes.py <repo-root> <scratch-dir> [name ...]
Each probe copies scripts/ to <scratch-dir>/<name>, applies its edit, runs the WHOLE
test_suite_cancellation.py (every control) and prints red/green with the last line.
"""
import concurrent.futures
import shutil
import subprocess
import sys
from pathlib import Path

NEW = "                    if (pid, start) not in initial:\n                        continue\n"
PROBES = {
    # Rows 2 and 6: a live descendant new since the first census gets SIGTERM in grace.
    "sigterm-to-live-new": ((NEW, NEW.replace("not in initial:", "not in initial and pid not in live:")),),
    # Row 8: a live trap command loses the shell's window after a resume inside grace.
    "live-trap-command-unspared-after-in-grace-resume": (
        ("if (pid, start) not in initial and resumed is not None:",
         "if (pid, start) not in initial and resumed is not None and (pid not in live or resumed >= deadline):"),),
    # Row 8: a live trap command never shares the window.
    "live-trap-command-unspared": (
        ("if (pid, start) not in initial and resumed is not None:",
         "if (pid, start) not in initial and resumed is not None and pid not in live:"),),
}


def run(root: Path, scratch: Path, name: str) -> str:
    tree = scratch / name
    shutil.rmtree(tree, ignore_errors=True)
    shutil.copytree(root / "scripts", tree / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    product = tree / "scripts/owned_process.py"
    text = product.read_text()
    for old, new in PROBES[name]:
        assert text.count(old) == 1, f"{name}: edit does not apply once: {old!r}"
        text = text.replace(old, new)
    product.write_text(text)
    with open(scratch / f"{name}.out", "w") as out:
        status = subprocess.run([sys.executable, "-B", str(tree / "scripts/test_suite_cancellation.py")], cwd=tree,
                                stdin=subprocess.DEVNULL, stdout=out, stderr=subprocess.STDOUT, timeout=500,
                                start_new_session=True).returncode
    lines = [line for line in (scratch / f"{name}.out").read_text(errors="replace").splitlines() if line.strip()]
    errors = [line for line in lines if "Error" in line]
    return f"{name}: {'red' if status else 'green'} rc {status}: {(errors or lines or [''])[-1][:300]}"


def main() -> int:
    root, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    scratch.mkdir(parents=True, exist_ok=True)
    names = sys.argv[3:] or list(PROBES)
    with concurrent.futures.ThreadPoolExecutor(len(names)) as pool:
        for line in pool.map(lambda name: run(root, scratch, name), names):
            print(line, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
