#!/usr/bin/env python3
"""List which `owner_stated_seconds` listings each named mutant breaks, without stopping at the first.

Usage: python3 -I per_listing.py <clone root> <scratch dir> <mutant name>...  ("none" = unmutated)
Copies scripts/, applies the mutant from MUTANTS, makes `kept`'s assert record instead of raise.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

root, scratch, names = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:]
ASSERT = '        assert events == stated, f"{words}\'s stated seconds were not kept on the owner\'s clock: {events}"\n'
RECORD = '        print("LISTING", "RED" if events != stated else "GREEN", words, flush=True)\n'
status = 0
for name in names:
    tree = scratch / name
    shutil.rmtree(tree, ignore_errors=True)
    shutil.copytree(root / "scripts", tree / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    test = tree / "scripts/test_suite_cancellation.py"
    text = test.read_text()
    assert text.count(ASSERT) == 1
    test.write_text(text.replace(ASSERT, RECORD))
    if name != "none":
        sys.path.insert(0, str(tree / "scripts"))
        import process_test_support  # noqa: E402  (the copy's own table)
        product = tree / "scripts/owned_process.py"
        body = product.read_text()
        for old, new in process_test_support.MUTANTS[name][2:]:
            assert body.count(old) == 1
            body = body.replace(old, new)
        product.write_text(body)
    env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
    out = subprocess.run([sys.executable, "-B", str(test), "--control", "owner_stated_seconds"], cwd=tree, env=env,
                         capture_output=True, text=True, timeout=150, stdin=subprocess.DEVNULL).stdout
    rows = [line for line in out.splitlines() if line.startswith("LISTING ")]
    red = [line[len("LISTING RED "):] for line in rows if line.startswith("LISTING RED ")]
    print(f"{name}: {len(rows)} listings kept, {len(red)} red: {red}")
    if name == "none" and red:
        status = 1
sys.exit(status)
