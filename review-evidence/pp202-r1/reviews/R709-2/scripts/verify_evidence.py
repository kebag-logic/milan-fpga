"""Verify the published evidence tree against its MANIFEST.json and pull the
figures this review checks. Usage: python3 -I verify_evidence.py <pp202-r1 dir>"""
import hashlib, json, os, re, sys
root = sys.argv[1]
man = json.load(open(os.path.join(root, "MANIFEST.json")))
listed = {e["file"]: e for e in man}
ok = bad = 0
for f, e in listed.items():
    if not f.startswith("author-r3/"):
        continue
    h = hashlib.sha256(open(os.path.join(root, f), "rb").read()).hexdigest()
    if h == e["published_sha256"]:
        ok += 1
    else:
        bad += 1
        print("MISMATCH", f)
present = [os.path.relpath(os.path.join(d, x), root) for d, _, fs in os.walk(os.path.join(root, "author-r3")) for x in fs]
print(f"author-r3: {ok} files match MANIFEST.json, {bad} mismatch, {len([p for p in present if p not in listed])} unlisted")
gs = json.load(open(os.path.join(root, "author-r3/receipts/gate-status.json")))
print("gate-status: all accepted rc 0:", all(r["rc"] == 0 for r in gs["accepted_return_codes"]),
      "| full_processor_checks", gs["full_processor_checks"])
for leg in ("sidmove-ax1x1-head.txt", "sidmove8-8x8-head.txt", "control-no-wiring-sidmove.txt",
            "control-round2-precedence-sidmove8.txt"):
    t = open(os.path.join(root, "author-r3/receipts/parent", leg)).read()
    ms = sorted(set(re.findall(r"declaration under 2 s \((\d+) ms\)", t)))
    res = re.findall(r"^checks: (\d+)\s+failures: (\d+)", t, re.M)
    print(f"parent {leg}: conflict-to-declaration ms {ms}; checks/failures {res}")
pr = open(os.path.join(root, "author-r3/PR-BODY.md")).read()
m = re.search(r"under 2 s \(([^)]*)\)", pr)
print("PR-BODY parent timing claim:", m.group(1) if m else None)
