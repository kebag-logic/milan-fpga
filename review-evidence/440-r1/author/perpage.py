"""Dump every tracked Markdown page using either engine and either population."""
import argparse
import hashlib
import importlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("--scripts", type=Path, required=True)
ap.add_argument("--revision", required=True)
ap.add_argument("--label", required=True)
args = ap.parse_args()
sys.path.insert(0, str(args.scripts.resolve()))
toc = importlib.import_module("gen_toc")
paths = subprocess.check_output(["git", "ls-files", "-z", "*.md"]).decode().split("\0")[:-1]
rows = {}
for path in paths:
    if args.revision == "worktree":
        raw = Path(path).read_bytes()
    else:
        raw = subprocess.check_output(["git", "show", args.revision + ":" + path])
    text = raw.decode().replace("\r\n", "\n").replace("\r", "\n")
    rows[path] = dict(content_sha256=hashlib.sha256(raw).hexdigest(),
                      blocks=toc.blocks(text), kinds=toc.line_kinds(text),
                      headings=toc.headings(text), generated=toc.generated_block(text, path),
                      owns=toc.owns(path, text), refusals=toc.refusals(text))
target = root / (args.label + ".json")
target.write_text(json.dumps(rows, indent=2, ensure_ascii=True) + "\n")
print(f"{len(rows)} tracked pages; {sum(r['generated'] is not None for r in rows.values())} carry provenance")
print(hashlib.sha256(target.read_bytes()).hexdigest(), target.name)
