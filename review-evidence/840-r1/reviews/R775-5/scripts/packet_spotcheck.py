#!/usr/bin/env python3
"""Check the archived evidence packet at one commit: fetch the git tree once,
then compare every manifest row's published_sha256 with the bytes served for
that path, on a sample spread across the manifest.
usage: packet_spotcheck.py <MANIFEST.json> <commit> <sample count>"""
import concurrent.futures as cf
import hashlib, json, subprocess, sys
m = json.load(open(sys.argv[1])); ref = sys.argv[2]; want_n = int(sys.argv[3])
print("rows:", len(m), "row keys:", sorted(m[0]))
print("signature field in the manifest:", any("sig" in k.lower() for r in m for k in r))
print("rows whose published differs from original (redaction):",
      sum(r["published_sha256"] != r["original_sha256"] for r in m),
      "path_redacted rows:", sum(bool(r.get("path_redacted")) for r in m))
step = max(1, len(m) // want_n)
sample = m[::step][:want_n]
def one(r):
    url = f"repos/kebag-logic/milan-fpga/contents/review-evidence/840-r1/{r['file']}?ref={ref}"
    got = subprocess.run(["gh", "api", "-H", "Accept: application/vnd.github.raw", url], capture_output=True)
    if got.returncode: return r["file"], "fetch-failed", len(got.stdout)
    return r["file"], hashlib.sha256(got.stdout).hexdigest() == r["published_sha256"], len(got.stdout)
with cf.ThreadPoolExecutor(6) as pool:
    res = list(pool.map(one, sample))
print("sampled:", len(res), "match:", sum(x[1] is True for x in res),
      "differ:", sum(x[1] is False for x in res), "fetch-failed:", sum(x[1] == "fetch-failed" for x in res))
for f, ok, n in res:
    if ok is not True: print("  NOT-MATCHED", str(ok), f[:90], n)
