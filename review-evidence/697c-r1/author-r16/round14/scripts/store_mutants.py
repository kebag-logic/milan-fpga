"""Each round-14 fix removed in turn from a disposable clone, then that clone's object-store and inherited controls
run (store_subset.py): which controls escape. usage: store_mutants.py <disposable clone> <work> <scripts dir>"""
import subprocess
import sys
from pathlib import Path

clone, work, scripts = (Path(a).resolve() for a in sys.argv[1:4])
build = clone / "sw/firmware/ctrl/test/ctrl_build.py"
MUTANTS = {
    "M0 none": [],
    "M1 no object hashed against its id": [("    if held != oid:\n", "    if False:\n")],
    "M2 the helper without core.fsmonitor=false": [('"git", "-c", "core.fsmonitor=false", "-C"', '"git", "-C"')],
}
original = build.read_text(encoding="utf-8")
for name, edits in MUTANTS.items():
    text = original
    for old, new in edits:
        assert text.count(old) == 1, (name, old)
        text = text.replace(old, new)
    build.write_text(text, encoding="utf-8")
    res = subprocess.run([sys.executable, "-I", str(scripts / "store_subset.py"), str(clone), str(work / name[:2])],
                         capture_output=True, text=True)
    lines = res.stdout.splitlines()
    print(f"== {name}: {lines[-1] if lines else res.stderr[-300:]}")
    for line in lines:
        if line.startswith("[ESCAPED]"):
            print("  " + line[:260])
build.write_text(original, encoding="utf-8")
print("restored:", build.read_text(encoding="utf-8") == original)
