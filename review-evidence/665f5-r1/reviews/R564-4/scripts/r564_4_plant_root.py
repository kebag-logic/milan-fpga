#!/usr/bin/env python3
"""R564-4: make a disposable root whose sw/firmware/ctrl is a real copy carrying
one plant, every other entry a symlink into the unmodified scratch root.

Usage: r564_4_plant_root.py SOURCE_ROOT NEW_ROOT PLANT
"""
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r564_4_plant import PLANTS  # noqa: E402

src, dst, plant = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
chain = ["sw", "firmware", "ctrl"]
here_src, here_dst = src, dst
for depth, name in enumerate(chain):
    here_dst.mkdir(parents=True, exist_ok=True)
    for entry in here_src.iterdir():
        if entry.name in (name, ".git"):
            continue
        link = here_dst / entry.name
        if not link.exists():
            link.symlink_to(entry)
    here_src, here_dst = here_src / name, here_dst / name
shutil.copytree(here_src, here_dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
path, old, new, _ = PLANTS[plant]
target = here_dst / path
text = target.read_text()
assert text.count(old) == 1, f"plant site count {text.count(old)}"
target.write_text(text.replace(old, new))
print(f"planted {plant} in {target}")
