#!/usr/bin/env python3
"""Re-send every committed fixture shape's exact recorded request bytes to
GitHub's Markdown API and compare the fresh response with the recorded one;
then run the base and head walks on each page against the recorded headings.

Usage: rerender_fixtures.py <head-scripts> <base-scripts> <render-dir> <out.json>
"""
import concurrent.futures
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURES = ("gen_toc_family_one.json", "gen_toc_comment_shapes.json",
            "gen_toc_container_walk.json")


def send(req: bytes, cache: Path) -> bytes:
    key = hashlib.sha256(req).hexdigest()
    path = cache / f"{key}.fixture.html"
    if not path.exists():
        (cache / f"{key}.fixture.req.json").write_bytes(req)
        res = subprocess.run(["gh", "api", "-X", "POST", "/markdown", "--input",
                              str(cache / f"{key}.fixture.req.json")],
                             capture_output=True, check=True)
        path.write_bytes(res.stdout)
    return path.read_bytes()


def main() -> None:
    head, base, cache_dir, out_path = sys.argv[1:5]
    cache = Path(cache_dir)
    cache.mkdir(parents=True, exist_ok=True)
    shapes = []
    for fixture in FIXTURES:
        data = json.loads((Path(head) / fixture).read_text(encoding="ascii"))
        shapes += [(fixture, s) for s in data["shapes"]]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        fresh = list(pool.map(lambda fs: send(fs[1]["request_bytes"].encode(), cache), shapes))
    pages = {f"{f}::{s['name']}": s["page"] for f, s in shapes}
    with tempfile.TemporaryDirectory() as tmp:
        pages_path = Path(tmp) / "pages.json"
        pages_path.write_text(json.dumps(pages))
        walks = {}
        for name, tree in (("head", head), ("base", base)):
            out = Path(tmp) / f"{name}.json"
            subprocess.run([sys.executable, "-B", str(HERE / "walk_headings.py"),
                            tree, str(pages_path), str(out)], check=True)
            walks[name] = json.loads(out.read_text())
    rows, tally = [], {}
    for (fixture, shape), body in zip(shapes, fresh):
        key = f"{fixture}::{shape['name']}"
        req_ok = hashlib.sha256(shape["request_bytes"].encode()).hexdigest() == shape["request_sha256"]
        request = json.loads(shape["request_bytes"])
        row = {
            "fixture": fixture, "name": shape["name"],
            "request_sha256_matches": req_ok,
            "request_page_matches": request.get("text") == shape["page"] and request.get("mode") == "gfm",
            "fresh_response_sha256": hashlib.sha256(body).hexdigest(),
            "fresh_identical": body == shape["response_bytes"].encode(),
            "recorded_headings": shape["headings"],
            "head_listed": walks["head"][key]["headings"],
            "base_listed": walks["base"][key]["headings"],
        }
        row["head_agrees"] = row["head_listed"] == shape["headings"]
        row["base_agrees"] = row["base_listed"] == shape["headings"]
        rows.append(row)
        combo = (fixture, row["fresh_identical"], row["base_agrees"], row["head_agrees"])
        tally[str(combo)] = tally.get(str(combo), 0) + 1
    json.dump({"rows": rows, "tally": tally}, open(out_path, "w"), indent=1)
    for combo, n in sorted(tally.items()):
        print(combo, n)
    bad = [r["name"] for r in rows if not (r["request_sha256_matches"] and r["request_page_matches"])]
    print("request mismatches:", bad)
    print("regressions (base agrees, head does not):",
          [r["name"] for r in rows if r["base_agrees"] and not r["head_agrees"]])
    print("head disagrees:", [r["name"] for r in rows if not r["head_agrees"]])


if __name__ == "__main__":
    main()
