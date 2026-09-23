#!/usr/bin/env python3
"""Compare walks against renders already in the cache, sending nothing.

Usage: offline_compare.py <pages.json> <out-prefix> <tree>=<scripts> ...
Same verdicts as compare.py, over the pages whose render is cached.
"""
import collections
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from compare import verdict  # noqa: E402
from render_gfm import rendered_headings  # noqa: E402

CACHE = HERE.parent / "receipts" / "renders"


def main() -> None:
    pages_path, prefix = sys.argv[1:3]
    trees = dict(arg.split("=", 1) for arg in sys.argv[3:])
    pages = json.load(open(pages_path))
    rendered = {}
    for key, text in pages.items():
        req = json.dumps({"text": text, "mode": "gfm"}, sort_keys=True).encode()
        sha = hashlib.sha256(req).hexdigest()
        path = CACHE / f"{sha}.html"
        if path.exists():
            body = path.read_text()
            rendered[key] = {"request_sha256": sha,
                             "response_sha256": hashlib.sha256(body.encode()).hexdigest(),
                             "headings": rendered_headings(body)}
    walks = {}
    for name, scripts in trees.items():
        out = f"{prefix}.{name}.json"
        subprocess.run([sys.executable, "-B", str(HERE / "walk_headings.py"),
                        scripts, pages_path, out], check=True)
        walks[name] = json.load(open(out))
    result, lines = {}, []
    for key in rendered:
        row = dict(rendered[key], rendered=rendered[key]["headings"])
        del row["headings"]
        for name in trees:
            listed = walks[name][key]["headings"]
            row[name] = {"listed": listed, "verdict": verdict(listed, row["rendered"])}
        result[key] = row
        lines.append("%-16s %s rendered=%s %s" % (
            key, " ".join("%s=%s" % (n, row[n]["verdict"]) for n in trees),
            [h[1] for h in row["rendered"]],
            " ".join("%s=%s" % (n, [h[1] for h in row[n]["listed"]]) for n in trees)))
    json.dump(result, open(f"{prefix}.json", "w"), indent=1, sort_keys=True)
    Path(f"{prefix}.txt").write_text("\n".join(lines) + "\n")
    tally = collections.Counter(tuple(result[k][n]["verdict"] for n in trees) for k in result)
    print("rendered pages:", len(result), "of", len(pages))
    for combo, count in sorted(tally.items()):
        print(" ", dict(zip(trees, combo)), count)


if __name__ == "__main__":
    main()
