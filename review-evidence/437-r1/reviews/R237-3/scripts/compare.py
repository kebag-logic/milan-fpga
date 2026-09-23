#!/usr/bin/env python3
"""Compare walks against GitHub's rendering on a set of synthetic pages.

Usage: compare.py <pages.json> <out-prefix> <tree-name>=<scripts-dir> ...
Renders every page (render_gfm.py, cached under <packet>/receipts/renders),
runs every named walk (walk_headings.py, each in its own process), and
writes <out-prefix>.json and a text table <out-prefix>.txt.

Per page and walk the verdict is AGREE, ESCAPE (the walk lists a heading
GitHub does not render) or WITHHOLD (GitHub renders a heading the walk
does not list), or ESCAPE+WITHHOLD. Headings compare as (level, text).
"""
import collections
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent


def verdict(listed: list, rendered: list) -> str:
    want = collections.Counter(map(tuple, rendered))
    have = collections.Counter(map(tuple, listed))
    escape, withhold = have - want, want - have
    parts = (["ESCAPE"] if escape else []) + (["WITHHOLD"] if withhold else [])
    return "+".join(parts) or "AGREE"


def main() -> None:
    pages_path, prefix = sys.argv[1:3]
    trees = dict(arg.split("=", 1) for arg in sys.argv[3:])
    pages = json.load(open(pages_path))
    rendered_path = f"{prefix}.rendered.json"
    subprocess.run([sys.executable, "-B", str(HERE / "render_gfm.py"),
                    pages_path, str(PACKET / "receipts" / "renders"),
                    rendered_path], check=True)
    rendered = json.load(open(rendered_path))
    walks = {}
    for name, scripts in trees.items():
        path = f"{prefix}.{name}.json"
        subprocess.run([sys.executable, "-B", str(HERE / "walk_headings.py"),
                        scripts, pages_path, path], check=True)
        walks[name] = json.load(open(path))
    result, lines = {}, []
    pages = {k: v for k, v in pages.items() if k in rendered}
    for key in pages:
        row = {"request_sha256": rendered[key]["request_sha256"],
               "response_sha256": rendered[key]["response_sha256"],
               "rendered": rendered[key]["headings"]}
        for name in trees:
            listed = walks[name][key]["headings"]
            row[name] = {"listed": listed,
                         "verdict": verdict(listed, rendered[key]["headings"])}
        result[key] = row
        lines.append("%-40s %s  rendered=%s  %s" % (
            key, " ".join("%s=%s" % (n, row[n]["verdict"]) for n in trees),
            [h[1] for h in row["rendered"]],
            " ".join("%s=%s" % (n, [h[1] for h in row[n]["listed"]])
                     for n in trees)))
    json.dump(result, open(f"{prefix}.json", "w"), indent=1, sort_keys=True)
    Path(f"{prefix}.txt").write_text("\n".join(lines) + "\n")
    tally = collections.Counter(
        tuple(result[k][n]["verdict"] for n in trees) for k in pages)
    print("pages:", len(pages))
    for combo, count in sorted(tally.items()):
        print(" ", dict(zip(trees, combo)), count)


if __name__ == "__main__":
    main()
