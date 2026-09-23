#!/usr/bin/env python3
"""Re-send every committed fixture shape's exact recorded request bytes to
GitHub's Markdown API and compare the fresh response with the recorded one,
then compare the recorded headings with what the walk at <walk-root> lists.

Usage: rerender_fixtures.py <clone> <walk-root> <out.jsonl> [start end]
Rows are appended and flushed one by one, so a run can be split into chunks.
"""
import hashlib
import json
import subprocess
import sys
import time

sys.path.insert(0, sys.argv[0].rsplit("/", 1)[0])
from probe import rendered_headings  # noqa: E402

FIXTURES = ("gen_toc_family_one.json", "gen_toc_comment_shapes.json", "gen_toc_container_walk.json")
HELPER = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
import gen_toc
json.dump([[[l, r] for l, r, _ in gen_toc.headings(p)] for p in json.load(sys.stdin)], sys.stdout)
'''
clone, root, out_path = sys.argv[1:4]
start, end = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (0, None)
shapes = []
for fixture in FIXTURES:
    for shape in json.load(open(f"{clone}/scripts/{fixture}", encoding="ascii"))["shapes"]:
        shapes.append((fixture, shape))
walk = json.loads(subprocess.run([sys.executable, "-B", "-c", HELPER, root + "/scripts"],
                                 input=json.dumps([s["page"] for _, s in shapes]).encode(),
                                 capture_output=True, check=True).stdout)
tally = {}
with open(out_path, "a", encoding="utf-8") as out:
    for (fixture, shape), listed in list(zip(shapes, walk))[start:end]:
        time.sleep(1)
        request = shape["request_bytes"].encode()
        for _ in range(4):
            proc = subprocess.run(["gh", "api", "markdown", "--input", "-"], input=request,
                                  capture_output=True, check=False)
            if proc.returncode == 0:
                break
            time.sleep(20)
        fresh = proc.stdout
        row = {"fixture": fixture, "name": shape["name"], "exit": proc.returncode,
               "request_sha256_ok": hashlib.sha256(request).hexdigest() == shape["request_sha256"],
               "recorded_sha256_ok": hashlib.sha256(shape["response_bytes"].encode()).hexdigest()
               == shape["response_sha256"],
               "fresh_sha256": hashlib.sha256(fresh).hexdigest(),
               "fresh_identical": fresh == shape["response_bytes"].encode(),
               "recorded_headings_ok": rendered_headings(shape["response_bytes"]) == shape["headings"],
               "walk_agrees": listed == shape["headings"]}
        key = tuple(sorted(k for k, v in row.items() if v is False))
        tally[str(key)] = tally.get(str(key), 0) + 1
        out.write(json.dumps(row, sort_keys=True) + "\n")
        out.flush()
print(len(shapes), json.dumps(tally, sort_keys=True))
