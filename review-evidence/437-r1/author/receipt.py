#!/usr/bin/env python3
"""Reproducible #437 author receipts; synthetic renderer inputs only."""
import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = "88e9276b2a220c716f64a843f7e1eb8f9265e896"


def command(args):
    return subprocess.run(["rtk", "proxy", *args], capture_output=True, text=True)


def identity():
    return {"head": command(["git", "rev-parse", "HEAD"]).stdout.strip(),
            "tree": command(["git", "rev-parse", "HEAD^{tree}"]).stdout.strip(),
            "status": command(["git", "status", "--porcelain"]).stdout,
            "utc": datetime.now(timezone.utc).isoformat()}


def parser(path):
    spec = importlib.util.spec_from_file_location("receipt_toc", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def snapshot(module, inputs):
    return {name: {"blocks": module.blocks(text), "headings": module.headings(text),
                   "generated_block": module.generated_block(text, name),
                   "line_kinds": module.line_kinds(text), "refusals": module.refusals(text)}
            for name, text in inputs.items()}


def corpus(stage):
    old = parser(HERE / "base-scripts/gen_toc.py")
    new = parser(Path.cwd() / "scripts/gen_toc.py")
    paths = command(["git", "ls-files", "-z", "--", "*.md"]).stdout.split("\0")
    inputs = {p: Path(p).read_text() for p in paths if p}
    baseline, current = snapshot(old, inputs), snapshot(new, inputs)
    (HERE / f"corpus-{stage}-base.json").write_text(json.dumps(baseline, indent=2) + "\n")
    (HERE / f"corpus-{stage}-head.json").write_text(json.dumps(current, indent=2) + "\n")
    changed = [p for p in inputs if baseline[p] != current[p]]
    original_inputs = {}
    for name in inputs:
        result = command(["git", "show", f"{BASE}:{name}"])
        assert result.returncode == 0, name
        original_inputs[name] = result.stdout
    original_base, original_head = snapshot(old, original_inputs), snapshot(new, original_inputs)
    original_changed = [p for p in original_inputs if original_base[p] != original_head[p]]
    (HERE / f"corpus-{stage}-original-base.json").write_text(json.dumps(original_base, indent=2) + "\n")
    (HERE / f"corpus-{stage}-original-head.json").write_text(json.dumps(original_head, indent=2) + "\n")
    report = {**identity(), "input_pages": len(inputs), "differences": changed,
              "original_input_differences": original_changed,
              "original_inputs_sha256": hashlib.sha256(json.dumps(original_inputs, sort_keys=True).encode()).hexdigest(),
              "inputs_sha256": hashlib.sha256(json.dumps(inputs, sort_keys=True).encode()).hexdigest()}
    (HERE / f"corpus-{stage}.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return bool(changed or original_changed)


def render(stage):
    old = parser(HERE / "base-scripts/gen_toc.py")
    new = parser(Path.cwd() / "scripts/gen_toc.py")
    fixtures = json.loads((HERE / "fixtures.json").read_text())
    cache_path = HERE / "renderer-cache.json"
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    from html.parser import HTMLParser

    class Headings(HTMLParser):
        def __init__(self):
            super().__init__()
            self.items = []
            self.current = None
        def handle_starttag(self, tag, attrs):
            if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
                self.current = ""
        def handle_data(self, data):
            if self.current is not None:
                self.current += data
        def handle_endtag(self, tag):
            if tag in ("h1", "h2", "h3", "h4", "h5", "h6") and self.current is not None:
                self.items.append(self.current)
                self.current = None

    rows = []
    for fixture in fixtures:
        page = fixture["page"]
        if page not in cache:
            payload = {"text": page, "mode": "gfm", "context": "kebag-logic/milan-fpga"}
            result = subprocess.run(["rtk", "proxy", "gh", "api", "markdown", "--input", "-"],
                                    input=json.dumps(payload), capture_output=True, text=True)
            if result.returncode:
                raise RuntimeError(result.stderr)
            cache[page] = {"request": payload, "html": result.stdout,
                           "utc": datetime.now(timezone.utc).isoformat(), "exit": 0}
            cache_path.write_text(json.dumps(cache, indent=2) + "\n")
        reader = Headings()
        reader.feed(cache[page]["html"])
        row = {**fixture, "github": reader.items,
               "base": [h[1] for h in old.headings(page)],
               "head": [h[1] for h in new.headings(page)]}
        rows.append(row)
        print(f'{row["id"]}: github={row["github"]} base={row["base"]} head={row["head"]}', flush=True)
    report = {**identity(), "rows": rows}
    (HERE / f"renderer-{stage}.json").write_text(json.dumps(report, indent=2) + "\n")
    return 0


def run(stage, args):
    result = command(args)
    record = {**identity(), "command": ["rtk", "proxy", *args], "exit": result.returncode}
    (HERE / f"{stage}.log").write_text(result.stdout + result.stderr)
    (HERE / f"{stage}.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record))
    print((result.stdout + result.stderr)[-2500:])
    return result.returncode


if __name__ == "__main__":
    action, stage, *args = sys.argv[1:]
    sys.exit({"corpus": lambda: corpus(stage), "render": lambda: render(stage),
              "run": lambda: run(stage, args)}[action]())
