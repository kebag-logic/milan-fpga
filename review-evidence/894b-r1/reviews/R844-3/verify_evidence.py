#!/usr/bin/env python3
"""Check the published archive's hashes and cross-receipt claims without rebuilding."""
import hashlib, json, pathlib, re, sys
root = pathlib.Path(sys.argv[1])
manifest = json.loads((root / "MANIFEST.json").read_text())
selected = [r for r in manifest if r["file"].startswith(("author-r5/", "author-r6/"))]
for r in selected:
 data = (root / r["file"]).read_bytes()
 assert hashlib.sha256(data).hexdigest() == r["published_sha256"], r["file"]
print(f"Published manifest: {len(selected)} files verified; {sum(r['path_redacted'] for r in selected)} path-redacted.")
for round_ in (5, 6):
 directory = root / f"author-r{round_}"
 entries = re.findall(r"^\| `([^`]+)` \| ([\d,]+) \| `([a-f0-9]{64})` \|", (directory / "INDEX.md").read_text(), re.M)
 matches, redactions = 0, 0
 for name, size, sha in entries:
  actual = (directory / name).read_bytes()
  if hashlib.sha256(actual).hexdigest() == sha:
   assert len(actual) == int(size.replace(",", ""))
   matches += 1
  else:
   rec = next(r for r in selected if r["file"] == f"author-r{round_}/{name}")
   assert rec["path_redacted"] and rec["original_sha256"] == sha, name
   redactions += 1
 print(f"Round {round_} index: {matches} matching files, {redactions} explained redactions.")
def read(name): return (root / name).read_text()
def images(name):
 result = {}
 for line in read(name).splitlines():
  m = re.match(r"((?:fixture|platform)-\S+):.*?sha256 ([a-f0-9]{64}), loadable sha256 ([a-f0-9]{64})", line)
  if m: result[m[1]] = (m[2],m[3])
 assert len(result) == 8, (name,len(result))
 return result
r5 = images("author-r5/receipts/images/raw-a15345f7.txt")
merge = images("author-r6/receipts/images/raw-5aadbc8c.txt")
head = images("author-r6/receipts/images/raw-af2c4d7a.txt")
upstream = images("author-r6/receipts/images/raw-902-4ae887a1.txt")
assert r5 == merge == head
print("All 8 image ELF and loadable SHA-256 pairs match a15345f7 -> 5aadbc8c -> af2c4d7a.")
fixed = [k for k in head if "8x8-1if" not in k]
assert len(fixed)==6 and all(head[k] == upstream[k] for k in fixed)
print("All 6 fixed-image pairs equal upstream 4ae887a1.")
budget = re.compile(r"^BUDGET .*", re.M)
measured = budget.findall(read("author-r5/receipts/harness/leg-M-A0-a15345f7.txt"))
bare = budget.findall(read("author-r5/receipts/harness/attribution-backlog-owed-647d5c4a.txt"))
assert measured == bare and len(bare) == 7
print("Bare merge attribution: all 7 BUDGET lines equal measured-image lines (microsecond resolution).")
for line in bare: print(line)
suites = checks = 0
for shard in range(4):
 t=read(f"author-r6/receipts/gates/sweep-shard{shard}-af2c4d7a.txt")
 s,p,f,to=map(int,re.search(r"suites: (\d+) +passed: (\d+) +failed: (\d+) +timed out: (\d+)",t).groups())
 c,fail=map(int,re.search(r"checks: (\d+) +in-suite failures: (\d+)",t).groups())
 assert s==p and f==to==fail==0 and "SKIPPED lines 0" in t
 suites+=s; checks+=c
print(f"Published sweep: {suites} suites, {checks} checks, no failure, timeout or skip.")
wf=read("author-r6/receipts/gates/workflows-verify-af2c4d7a.md")
rcs=[line.split("|")[5].strip() for line in wf.splitlines() if line.startswith("| ") and len(line.split("|"))==8][1:]
assert set(rcs)=={"0","NOT RUN"},set(rcs)
print(f"Published local workflow execution: {rcs.count('0')} steps rc 0; {rcs.count('NOT RUN')} NOT RUN.")
lane=read("author-r6/receipts/gates/lane-gates-af2c4d7a.txt")
gates=re.findall(r"^(\S+) rc=(\d+):",lane,re.M)
assert len(gates)==65
assert all(int(rc)==int("_exits_1" in name) for name,rc in gates)
print(f"Published lane gates: {len(gates)} expected return codes.")
plat=read("author-r6/receipts/gates/plat-ledger-af2c4d7a.txt")
for line in plat.splitlines():
 if line.startswith(("POINT ", "plat_ledger controls:", "plat_ledger:")): print(line)
print("Evidence consistency: PASS. Hash receipts authenticate content consistency, not execution independently.")

