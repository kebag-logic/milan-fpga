#!/usr/bin/env python3
"""Plant earlier multi-declarator patterns into a copy of check_cpp_idiom.py
and run its --selftest, expecting a FAIL on the brace arms.

Usage: python3 -I mutate_multidecl.py <checkout> <scratch-dir>

The checkout is only read; each mutant is a copy under <scratch-dir> placed
at scripts/check_cpp_idiom.py of a minimal mirror that symlinks the rest of
the checkout's top level, so the selftest sees the same tree.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
scratch = Path(sys.argv[2]).resolve()
src = (root / "scripts" / "check_cpp_idiom.py").read_text()

HEAD_TEXT = '_DECL_TEXT = r"(?:[^;(){}\\n]|\\{(?:[^{}\\n]|\\{(?:[^{}\\n]|\\{[^{}\\n]*\\})*\\})*\\})*"'
assert HEAD_TEXT in src, "head _DECL_TEXT not found"

MUTANTS = {
    # the pattern the delta replaced (prior head e18c8225): one brace level
    "one-level-brace": '_DECL_TEXT = r"(?:[^;(){}\\n]|\\{[^{}\\n]*\\})*"',
    # two levels only: the three-deep arms must catch it
    "two-level-brace": '_DECL_TEXT = r"(?:[^;(){}\\n]|\\{(?:[^{}\\n]|\\{[^{}\\n]*\\})*\\})*"',
    # base 46c971fa shape: braces are ordinary text, commas inside count
    "base-no-brace": '_DECL_TEXT = r"[^;()\\n]*"',
}

for name, text in MUTANTS.items():
    d = scratch / name
    if d.exists():
        shutil.rmtree(d)
    (d / "scripts").mkdir(parents=True)
    for entry in root.iterdir():
        if entry.name in ("scripts", ".git"):
            continue
        os.symlink(entry, d / entry.name)
    for entry in (root / "scripts").iterdir():
        if entry.name != "check_cpp_idiom.py":
            os.symlink(entry, d / "scripts" / entry.name)
    (d / "scripts" / "check_cpp_idiom.py").write_text(src.replace(HEAD_TEXT, text))
    r = subprocess.run([sys.executable, "-I", "scripts/check_cpp_idiom.py", "--selftest"],
                       cwd=d, capture_output=True, text=True)
    fails = [l for l in r.stdout.splitlines() if l.startswith("[FAIL]")]
    summary = [l for l in r.stdout.splitlines() if "checks:" in l]
    print(f"== mutant {name}: rc={r.returncode} {summary[-1] if summary else r.stderr.strip()[-200:]}")
    for l in fails:
        print("   " + l)
    print(f"   verdict: {'KILLED' if r.returncode != 0 and fails else 'SURVIVED'}")
