#!/usr/bin/env python3
"""A long module heading, and one carrying only an unfit label, must fail the memory-map --check in a scratch copy."""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path
root, py = Path(sys.argv[1]), sys.argv[2]
def run(change, name):
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        (t / "docs/diagrams").mkdir(parents=True)
        shutil.copy(root / "docs/diagrams/memory_map.gen.py", t / "docs/diagrams/")
        shutil.copy(root / "docs/diagrams/memory_map.svg", t / "docs/diagrams/")
        shutil.copy(root / "docs/diagrams/memory_map.drawio", t / "docs/diagrams/")
        shutil.copytree(root / "scripts", t / "scripts", ignore=shutil.ignore_patterns("__pycache__", "*.budget"))
        p = t / "scripts/register_descriptions.json"
        d = json.loads(p.read_text())
        change(d)
        p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
        r = subprocess.run([py, "-B", str(t / "docs/diagrams/memory_map.gen.py"), "--check"], capture_output=True, text=True)
        print(f"{name}: rc={r.returncode} {' / '.join(r.stdout.strip().splitlines())[:220]}")
def long_name(d): d["modules"][0]["heading"] = "0x000  -  " + "very long module name " * 4
def glyph(d): d["modules"][0]["heading"] = "0x000  -  Identification \U0001F534"
def none(d): pass
run(none, "control")
run(long_name, "label overprints the address")
run(glyph, "label carries a glyph")
