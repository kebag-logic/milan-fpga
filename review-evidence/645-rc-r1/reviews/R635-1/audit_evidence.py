#!/usr/bin/env python3
"""Read immutable public evidence and check review claims. No simulations or writes.

Usage: python3 audit_evidence.py /path/to/review-clone
Requires both evidence commits in that clone's object database.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(sys.argv[1]).resolve()
HEAD = "2639eecf3f94aa1a8be5c922058a05f0a48b1933"
BASE = "f62602531d415d6c1cae1374a3cc2938faf54049"
PACKET = "a86dc902d332e27ce093f5f56ccdaa5e46f9ce90"
B17 = "bdb96b6685751a424fbbdc952726f33efd17282a"
PREFIX = "review-evidence/645-rc-r1/"


def git(*args):
    return subprocess.check_output(["git", "--no-replace-objects", "-C", str(REPO), *args])


def blob(commit, path):
    return git("show", commit + ":" + path)


def receipt(path):
    return blob(PACKET, PREFIX + "author/" + path).decode()


manifest = json.loads(blob(PACKET, PREFIX + "MANIFEST.json"))
excluded = {"HANDOFF.md", "PR-BODY.md", "REVIEW-READY.md", "REVIEW-READY.readback.md", "TAKEN.md"}
verified = 0
for row in manifest:
    if Path(row["file"]).name in excluded:
        continue
    data = blob(PACKET, PREFIX + row["file"])
    assert hashlib.sha256(data).hexdigest() == row["published_sha256"], row["file"]
    verified += 1
print(f"PUBLIC MANIFEST: {verified} executable-evidence files verified against published hashes")
print(f"SOURCE HEAD {HEAD}; BASE {BASE}; EVIDENCE {PACKET}; B17 {B17}")

cpp = blob(HEAD, "tb/verilator/follow_ring/sim_main.cpp").decode()
table = re.search(r"kB17 = \{\{(.*?)\}\};", cpp, re.S).group(1)
constants = [[float(x) for x in line.split(",")] for line in re.findall(r"\{([^{}]+)\}", table)]
slopes = []
quantiles = []
print("B17 PARAMETERS: cycle first_delay_ms burst_after_first_s first_peak_us later_peak_us decay_us/PDU")
for n in range(1, 11):
    path = f"review-evidence/645-b17-r1/author/summary/c{n:02}.json"
    data = blob(B17, path)
    d = json.loads(data)
    late = d["tap"]["late_pdus"]
    first = [late[0]]
    for p in late[1:]:
        if p["s"] - first[-1]["s"] >= 0.0002:
            break
        first.append(p)
    size = len(first)
    mx = (size - 1) / 2
    my = sum(p["late_us"] for p in first) / size
    slope = sum((i - mx) * (p["late_us"] - my) for i, p in enumerate(first)) / sum((i - mx)**2 for i in range(size))
    slopes.append(-slope)
    priming = d["tap"]["priming"]
    quantiles.append(priming["lateness_us"]["p999"])
    expected = [float(n), priming["first_pdu_after_command_ms"],
                round(first[0]["s"] - priming["first_pdu_after_command_ms"] / 1000, 4),
                max(p["late_us"] for p in first),
                max(p["late_us"] for p in late if p["s"] > d["poll"]["slips"][0]["s_hi"])]
    assert constants[n - 1] == expected, (constants[n - 1], expected)
    assert not [p for p in late if p["s"] < first[0]["s"]]
    print(*expected, f"{(-slope):.6f}", "summary_sha256=" + hashlib.sha256(data).hexdigest())
print(f"Mean decay {sum(slopes)/10:.6f}; rounded {sum(slopes)/10:.3f}; p99.9 range {min(quantiles)}..{max(quantiles)} us")
assert round(sum(slopes)/10, 3) == 1.538
ana = blob(B17, "review-evidence/645-b17-r1/author/tools/ana_b17.py").decode()
assert "LATE_US = 10.0" in ana and "pres > LATE_US * 1e3" in ana
print("BOUND AUDIT: B17 late_pdus contains ONLY lateness > 10 us (ana_b17.py:51,333-336).")
print("An empty pre-burst list does not establish an exercised 10-us non-slipping arrival.")
print("The no-second-slip inference for cycle 5 is 30.260 - 1e6/48000 = %.6f us, not >10 us." % (30.260 - 1e6/48000))

pattern = re.compile(
    r"RESULT-645-BIND: B17 cycle (?P<cycle>\d+).*?first PDU \+(?P<first>[\d.]+) ms.*?"
    r"primed margin (?P<lo>[\d.]+)\.\.(?P<hi>[\d.]+) us \((?P<window>inside|OUTSIDE).*?"
    r"arms (?P<arms>\d+).*?settle recentres (?P<settles>\d+) \((?P<ticks>[-\d.]+).*?"
    r"render recentres (?P<renders>\d+), SLIP_LB \+(?P<dups>\d+) dups \+(?P<skips>\d+) skips, slipped frames "
    r"(?P<pre>\d+) before the ring acts and (?P<post>\d+) after.*?"
    r"margin after a recentre \+(?P<after>\d+\.\d+)\.\..*?full side \+(?P<full>\d+\.\d+)")
for variant in ["base", "fix"]:
    rows = []
    rcs = []
    for jitter in [0, 5]:
        for phase in range(16):
            name = f"campaign/{variant}/bind_j{jitter}_p{phase:02}"
            text = receipt(name + ".log")
            rcs.append(int(receipt(name + ".rc")))
            current = [m.groupdict() for m in pattern.finditer(text)]
            assert len(current) == 10, name
            assert sorted(int(r["cycle"]) for r in current) == list(range(1, 11))
            for r in current:
                r["artifact"] = name + ".log"
                for key in ["arms", "settles", "renders", "dups", "skips", "pre", "post"]:
                    r[key] = int(r[key])
                rows.append(r)
            if variant == "base" and jitter == 0 and phase == 9:
                example = next(r for r in current if r["cycle"] == "1")
                assert example["dups"] == 2 and example["pre"] == 0 and example["post"] == 1
                print("BOUND COUNTEREXAMPLE: author/" + name + ".log")
                print(next(line for line in text.splitlines() if line.startswith("RESULT-645-BIND: B17 cycle 1 ")))
    inside = [r for r in rows if r["window"] == "inside"]
    assert len(inside) == 169 and len(rows) == 320
    print(variant.upper(), json.dumps({"runs_rc0": rcs.count(0), "runs": len(rcs), "binds": len(rows),
        "inside": len(inside), "outside": len(rows)-len(inside),
        **{key:sum(r[key] for r in rows) for key in ["arms", "settles", "renders", "dups", "skips", "pre", "post"]}}))
    if variant == "base":
        assert rcs == [1] * 32
        assert all((r["dups"], r["skips"], r["pre"], r["post"]) == (2, 0, 0, 1) for r in inside)
    else:
        assert rcs == [0] * 32
        assert all((r["arms"],r["settles"],r["renders"],r["post"]) == (1,1,1,0) for r in rows)
        assert all(r["dups"] == r["skips"] == 0 for r in inside)
        assert sum(r["pre"] != 0 for r in rows) == 6
        print("FIX EXTREMA ticks %.2f..%.2f empty %.3f full %.3f" % (
            min(float(r["ticks"]) for r in rows), max(float(r["ticks"]) for r in rows),
            min(float(r["after"]) for r in rows), min(float(r["full"]) for r in rows)))
        for r in rows:
            if r["pre"]:
                text = receipt(r["artifact"])
                slip = re.search(r"info: B17 cycle " + r["cycle"] + r": slip \(dup\) \+([\d.]+) s", text)
                delay = float(slip.group(1)) - float(r["first"])/1000
                assert 0 <= delay < .0022
                print("EARLY SLIP",r["artifact"],"cycle",r["cycle"],"after_first_ms",round(delay*1000,3))

mutants = receipt("suites/fr_mutants.log")
assert "follow_ring mutants: 15/15 caught" in mutants
for line in mutants.splitlines():
    if line.startswith("[MUTANT]"):
        print(line)
assert int(receipt("suites/fr_mutants.rc")) == 0
print("AREA OOC (LUT/FF; no whole-image or placement claim)")
for name in ["base_n1", "head_n1", "base_n8", "head_n8", "head_off"]:
    text = receipt("area/" + name + ".vivado.util.txt")
    values = [int(re.search(re.escape(key) + r"\s*\|\s*(\d+)", text).group(1)) for key in ["Slice LUTs*", "Slice Registers"]]
    print(name, *values)
print("WALL CLOCK", receipt("wallclock/result.txt").strip())
ratio = 857.648 / 800.859
print("Fifth leg cost %.6f%%; historical-hosted projection %.6f s" % ((ratio-1)*100,1114.2*ratio))
print("SUITE TALLY\n" + receipt("tally/tally.txt"))
for category in ["suites", "gates"]:
    rcs = {r["file"]:int(blob(PACKET, PREFIX + r["file"])) for r in manifest
           if r["file"].startswith("author/"+category+"/") and r["file"].endswith(".rc")}
    print(category, "receipts",len(rcs),"nonzero", {k:v for k,v in rcs.items() if v})
print("AUDIT COMPLETE: numerical sweep claims reproduced; priming-bound derivation is unsupported as stated.")
