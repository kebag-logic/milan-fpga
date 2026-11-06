#!/usr/bin/env python3
"""List every selftest needle that the --findings-dir text alone can satisfy.

Usage: needle_sources.py SCRIPT. Loads the script as a module and wraps gate() so
each control's rendered page and lane files can be compared with its needles.
"""
import importlib.util
import sys
import tempfile
from pathlib import Path

spec = importlib.util.spec_from_file_location("inv", sys.argv[1])
inv = importlib.util.module_from_spec(spec)
sys.modules["inv"] = inv
spec.loader.exec_module(inv)
real_control = inv.control
rows = []


def control(name, mutate, want, needle="", says="", absent=""):
    captured = {}
    real_tmp = tempfile.TemporaryDirectory

    class Keep(real_tmp):
        def __exit__(self, *a):
            root = Path(self.name)
            page = root / inv.OUTPUT
            captured["rendered"] = page.read_text(encoding="utf-8") if page.is_file() else ""
            lanes = root / "lanes"
            captured["listed"] = "".join(p.read_text(encoding="utf-8") for p in lanes.glob("*.md")) if lanes.is_dir() else ""
            return super().__exit__(*a)

    inv.tempfile.TemporaryDirectory = Keep
    try:
        result = real_control(name, mutate, want, needle, says, absent)
    finally:
        inv.tempfile.TemporaryDirectory = real_tmp
    for text in (needle,) if isinstance(needle, str) else needle:
        if not text:
            continue
        on_page = text in captured.get("rendered", "")
        in_lanes = text in captured.get("listed", "")
        rows.append((name, text, on_page, in_lanes))
    return result


inv.control = control
code = inv.selftest()
print("selftest rc", code)
both = [r for r in rows if r[2] and r[3]]
lanes_only = [r for r in rows if r[3] and not r[2]]
page_only = [r for r in rows if r[2] and not r[3]]
print(f"needles: {len(rows)}; page only {len(page_only)}; lane file only {len(lanes_only)}; both {len(both)}")
print("-- needles satisfiable from the lane file even if the page lost them:")
for name, text, _, _ in both:
    print(f"   [{name}] {text!r}")
print("-- needles only in the lane file:")
for name, text, _, _ in lanes_only:
    print(f"   [{name}] {text!r}")
