#!/usr/bin/env python3
"""Render a named set of probe pages on GitHub and score base and head walks.

Usage: probe.py <head-scripts> <base-scripts> <probes.json> <out.json>
probes.json: list of {"name", "page"}. Prints one line per probe.
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gfm  # noqa: E402


def walk(scripts: str, rows: list, out: Path) -> list:
    src = out.with_suffix(".in.json")
    src.write_text(json.dumps(rows))
    subprocess.run([sys.executable, str(Path(__file__).with_name("walk.py")), scripts,
                    str(src), str(out)], check=True)
    src.unlink()
    rows = json.loads(out.read_text())
    out.unlink()
    return rows


def main() -> int:
    head, base, probes, out = sys.argv[1], sys.argv[2], sys.argv[3], Path(sys.argv[4])
    rows = json.loads(Path(probes).read_text())
    hw = walk(head, rows, out.with_name(out.stem + ".head.json"))
    bw = walk(base, rows, out.with_name(out.stem + ".base.json"))
    receipts = gfm.render_all([r["page"] for r in rows], jobs=1)
    result = []
    for r, h, b, rc in zip(rows, hw, bw, receipts):
        gh = rc["headings"]
        row = {"name": r["name"], "page": r["page"], "github": gh, "head": h["walk"],
               "base": b["walk"], "head_agrees": h["walk"] == gh, "base_agrees": b["walk"] == gh,
               "head_blocks": h["blocks"], "request_sha256": rc["request_sha256"],
               "response_sha256": rc["response_sha256"], "response_bytes": rc["response_bytes"]}
        result.append(row)
        print(f"{r['name']}: github={[x[1] for x in gh]} head={[x[1] for x in h['walk']]} "
              f"base={[x[1] for x in b['walk']]} head_agrees={row['head_agrees']} "
              f"base_agrees={row['base_agrees']}")
    out.write_text(json.dumps(result, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
