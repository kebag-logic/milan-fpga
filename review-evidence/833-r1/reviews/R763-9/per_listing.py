"""For each named MUTANTS entry, which owner_stated_seconds listings turn red (every listing run, none stops).

Usage: python3 -I per_listing.py <clean-tree> <scratch> name...
"""
import shutil, subprocess, sys, os, concurrent.futures
from pathlib import Path
CLEAN, SCRATCH = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(CLEAN / "scripts"))
from process_test_support import MUTANTS
ASSERT = "        assert events == stated, f\"{words}'s stated seconds were not kept on the owner's clock: {events}\"\n"
def one(name):
    root = SCRATCH / name
    shutil.rmtree(root, ignore_errors=True)
    shutil.copytree(CLEAN / "scripts", root / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    p = root / "scripts/owned_process.py"; t = p.read_text()
    for old, new in MUTANTS[name][2:]:
        assert t.count(old) == 1; t = t.replace(old, new)
    p.write_text(t)
    q = root / "scripts/test_suite_cancellation.py"; s = q.read_text()
    assert s.count(ASSERT) == 1
    q.write_text(s.replace(ASSERT, "        print('LISTING', repr(words), 'RED' if events != stated else 'green', flush=True)\n"))
    out = subprocess.run([sys.executable, "-B", str(q), "--control", "owner_stated_seconds"], cwd=root, capture_output=True,
                         text=True, timeout=120, env={k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}).stdout
    lines = [l for l in out.splitlines() if l.startswith("LISTING")]
    red = [l.split(" ", 1)[1].rsplit(" ", 1)[0] for l in lines if l.endswith("RED")]
    shutil.rmtree(root, ignore_errors=True)
    return name, len(lines), red
with concurrent.futures.ThreadPoolExecutor(16) as pool:
    for name, total, red in pool.map(one, sys.argv[3:]):
        print(f"{name}: red on {len(red)} of {total}: {red}")
