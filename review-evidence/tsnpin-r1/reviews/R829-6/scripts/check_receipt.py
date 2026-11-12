"""Check the corrected round-4 coverage receipt against the repository and the coverage-write log.
Usage: python3 -I check_receipt.py <repo dir> <extracted review-evidence/tsnpin-r1 dir>
Applies the receipt's diff to 0fb66211's committed coverage.ratchet, checks the post-image blob id the diff names,
and compares every row of the result with the covered counts in fw_coverage-write-at-0fb66211.log."""
import hashlib, os, re, subprocess, sys, tempfile
repo, ev = sys.argv[1], sys.argv[2]
R = "sw/firmware/gtest/coverage.ratchet"
rc4 = os.path.join(ev, "author-r4/receipts/round4/fw_coverage-write-at-0fb66211-diff.txt")
rc5 = os.path.join(ev, "author-r5/receipts/round5/fw_coverage-write-at-0fb66211-diff.txt")
log = os.path.join(ev, "author-r4/receipts/round4/fw_coverage-write-at-0fb66211.log")
g = lambda *a: subprocess.run(["git", "-C", repo, *a], check=True, capture_output=True, text=True).stdout
txt = open(rc4).read()
print("round4 == round5 copy:", open(rc4, "rb").read() == open(rc5, "rb").read())
print("sha256:", hashlib.sha256(open(rc4, "rb").read()).hexdigest())
hdr = [l for l in txt.splitlines() if l.startswith("#")]
print("header lines:", len(hdr), "| mentions 'Corrected':", any("Corrected" in l for l in hdr))
m = re.search(r"^index ([0-9a-f]+)\.\.([0-9a-f]+)", txt, re.M)
pre_full = g("rev-parse", "0fb66211b7:" + R).strip()
print("pre-image named", m.group(1), "| 0fb66211 blob", pre_full, "| match:", pre_full.startswith(m.group(1)))
body = txt[txt.index("diff --git"):]
with tempfile.TemporaryDirectory() as d:
    open(os.path.join(d, "r"), "w").write(g("show", "0fb66211b7:" + R))
    open(os.path.join(d, "p"), "w").write(body.replace("a/" + R, "a/r").replace("b/" + R, "b/r"))
    subprocess.run(["patch", "-s", "r", "p"], cwd=d, check=True)
    applied = open(os.path.join(d, "r")).read()
post = subprocess.run(["git", "hash-object", "--stdin"], input=applied, capture_output=True, text=True).stdout.strip()
print("post-image named", m.group(2), "| applied blob", post, "| match:", post.startswith(m.group(2)))
rat = {l.split()[0]: l.split() for l in applied.splitlines() if l and not l.startswith("#")}
meas = {}
for l in open(log):
    f = l.split()
    if len(f) >= 3 and (f[0].startswith("sw/") or f[0].startswith("third_party/")) and "/" in f[1]:
        meas[f[0]] = (f[1].split("/")[0], f[2].split("/")[0])
bad = []
for k, (lc, bc) in meas.items():
    r = rat.get(k)
    if r is None or r[2] != f"{lc}/{lc}" or r[4] != f"{bc}/{bc}":
        bad.append((k, (lc, bc), r))
print(f"log rows {len(meas)} | ratchet rows {len(rat)} | rows disagreeing {len(bad)} | rows only in ratchet {sorted(set(rat)-set(meas))}")
for b in bad: print("  ", b)
for k in ("sw/firmware/ctrl/app/ctrl_app_aecp.c", "sw/firmware/ctrl_nvm/nvm_store.c"):
    old = [l for l in g("show", "0fb66211b7:" + R).splitlines() if l.startswith(k + " ")]
    head = [l for l in g("show", "6eacd76d5f596a88a537dcb4fb5b39a5a2284c3c:" + R).splitlines() if l.startswith(k + " ")]
    print(f"{k}: 0fb66211 {old[0].split()[2]} | receipt/log {rat[k][2]} | head {head[0].split()[2]}")
