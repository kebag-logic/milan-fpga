"""R220 independent reading of the AC5 raw act receipts (scratch head) and the
normal-head replica; also checks MANIFEST published hashes of those files."""
import json, hashlib, pathlib, re, sys
root = pathlib.Path(sys.argv[1])
man = json.loads((root / "MANIFEST.json").read_text())
entries = man if isinstance(man, list) else man.get("files", man)
def published_hash(rel):
    items = entries.items() if isinstance(entries, dict) else ((e.get("file") or e.get("path"), e) for e in entries)
    for k, v in items:
        if k and str(k) == rel:
            return v
    return None
for rel in ("ac5-act/01.log", "ac5-act/02.log", "ac5-act/results.json", "act-draft-fast/01.log", "ac5/mutation.diff"):
    h = hashlib.sha256((root / rel).read_bytes()).hexdigest()
    rec = published_hash(rel)
    recs = json.dumps(rec) if rec is not None else "NOT IN MANIFEST"
    print(f"{rel}: sha256={h[:16]}... manifest-match={'yes' if h in recs else 'NO'}")
docs = (root / "ac5-act/01.log").read_text().splitlines()
rtl = (root / "ac5-act/02.log").read_text().splitlines()
def res(lines, job, step):
    pat = re.compile(r"^\[" + re.escape(job) + r"\s*\]\s+(✅|❌)\s+(Success|Failure) - Main " + re.escape(step) + r" \[")
    return [m.group(2) for l in lines for m in [pat.search(l)] if m]
def jobres(lines, job):
    pat = re.compile(r"^\[" + re.escape(job) + r"\s*\]")
    return [l.split("🏁")[1].strip() for l in lines if pat.match(l) and "🏁" in l]
fails = lambda lines, job: [l.split("|",1)[1].strip() for l in lines if re.match(r"^\[" + re.escape(job) + r"\s*\]", l) and "|   FAIL" in l]
print("binding:", [l for l in docs[:3] if "exact head" in l or "validation base" in l])
print("docs: Python idiom gate:", res(docs, "docs/docs-check", "Python idiom gate"))
print("docs: CI event and SHA contract gate:", res(docs, "docs/docs-check", "CI event and SHA contract gate"))
print("docs: contract findings:", fails(docs, "docs/docs-check"))
later = ["Local act runner contract gate", "Doc cited-path gate", "Archive integrity gate", "Per-page contents gate",
         "Sweep/build shape gate", "Deploy shape gate", "Entity shape gate"]
print("docs: later docs-check steps executed after the refusal:", [s for s in later if any(f"Run Main {s}" in l for l in docs)])
for j in ("docs/docs-check", "docs/wire-accountability", "docs/docs-check-no-git"):
    print(f"docs: job {j}:", jobres(docs, j))
print("docs verdict:", [l for l in docs if l.startswith("act-ci: docs")])
print("rtl: gate contract step:", res(rtl, "rtl-full/full-ci-gate", "Hold every workflow file to its contract"))
print("rtl: gate findings:", fails(rtl, "rtl-full/full-ci-gate"))
for j in ("rtl-full/full-ci-gate", "rtl-full/verilator-suites", "rtl-full/yosys-portability"):
    print(f"rtl: job {j}:", jobres(rtl, j), "| FAIL lines:", len(fails(rtl, j)))
workers = sorted({l.split("]")[0][1:].strip() for l in rtl if l.startswith("[rtl-full/") and ("shard" in l.split("]")[0].lower() or "physical" in l.split("]")[0].lower())})
print("rtl: worker/physical jobs that produced any log line:", workers or "none (not run after the failed selector)")
print("rtl: aggregate SHA verifier:", [f for j in ("rtl-full/verilator-suites","rtl-full/yosys-portability") for f in fails(rtl, j) if "expected" in f and "shard" in f])
print("rtl verdict:", [l for l in rtl if l.startswith("act-ci: rtl-full")])
normal = (root / "act-draft-fast/01.log").read_text().splitlines()
print("normal head binding:", [l for l in normal[:3] if "exact head" in l])
print("normal: docs-check contract gate:", res(normal, "docs/docs-check", "CI event and SHA contract gate"), "| Python idiom:", res(normal, "docs/docs-check", "Python idiom gate"))
print("normal verdicts:", [l for l in normal if re.match(r"act-ci: (docs|rtl-fast|elaborate):", l)])
