"""Merge-round checks on the FPGA-gPTP merge head, printed as one receipt.

usage: merge_checks.py <head tree> <main tree> <round-2 tree> <head engine gate log>

1. The ROM images: the head generator rebuilds each committed image, and
   each equals main's.
2. The engine mutation arm at head is main's arm and round 2's arm, less
   the entries one side deleted on purpose.
3. Every arm entry whose `breaks` carries a strict prefix printed every
   check it names as FAIL before its verdict, in the head engine gate log.
4. The SOURCE_EVIDENCE anchors resolve at head.
"""
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

HEAD, MAIN, R2, LOG = (Path(a) for a in sys.argv[1:5])
GEN = "hdl/ucode/gen_gptp_ucode.py"
IMAGES = {"tb/verilator/ucpu/gptp_ucode.hex": [],
          "syn/ooc/work/gptp_ucode.hex": [],
          "tb/verilator/engine/gptp_ucode.hex": ["--clk-hz", "2000000",
                                                 "--cease-ms", "3000"],
          "tb/tsngen/gptp_ucode.hex": ["--clk-hz", "2000000"]}


def arm(root: Path):
    for k in ("receipt_mutants", "mutation_verdict"):
        sys.modules.pop(k, None)
    sys.path[:0] = [str(root / "tb"), str(root / "tb/verilator/engine")]
    spec = importlib.util.spec_from_file_location(
        f"m{abs(hash(root))}", root / "tb/verilator/engine/mutants.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    del sys.path[:2]
    return mod


print("1. ROM images")
for image, args in IMAGES.items():
    out = HEAD / ".merge-check.hex"
    subprocess.run(["python3", str(HEAD / GEN), *args, "-o", str(out)],
                   check=True, capture_output=True)
    rebuilt = out.read_bytes() == (HEAD / image).read_bytes()
    out.unlink()
    same = (HEAD / image).read_bytes() == (MAIN / image).read_bytes()
    print(f"   {image}: regenerated identical {rebuilt}; equal to main {same}")

print("2. engine arm")
h, b, r = arm(HEAD), arm(MAIN), arm(R2)
H = {e[0]: e[-1] for e in h.MUTATIONS}
B = {e[0]: e[-1] for e in b.MUTATIONS}
R = {e[0]: e[-1] for e in r.MUTATIONS}
print(f"   head {len(H)}, main {len(B)}, round 2 {len(R)}, shared {len(B.keys() & R.keys())}")
print(f"   head adds none: {not (H.keys() - B.keys() - R.keys())}")
print(f"   main entries not at head (deleted by round 2): {sorted(B.keys() - H.keys())}")
print(f"   round-2 entries not at head (deleted by main): {sorted(R.keys() - H.keys())}")
same_b = all(H[n] == B[n] for n in B.keys() & H.keys() - R.keys())
same_r = all(H[n] == R[n] for n in R.keys() & H.keys() - B.keys())
print(f"   each side's own entries keep their breaks: main {same_b}, round 2 {same_r}")

print("3. strict named checks in the head engine gate log")
pref = ("#82 ", "#84 ", "#85 ", "#87 ", "#88 ", "#89 ", "#90 ", "#91 ",
        h.P1_PREFIX)
segs, seg = {}, []
text = LOG.read_text()
for line in text.splitlines():
    m = re.match(r"\[(PASS|FAIL)\] mutant (?:caught: )?(.*?) - ", line)
    if m:
        segs[m.group(2)] = (m.group(1), seg)
        seg = []
    elif line.startswith("FAIL "):
        seg.append(line)
print(f"   verdicts {len(segs)}; [FAIL] verdicts "
      f"{sum(v[0] == 'FAIL' for v in segs.values())}; "
      f"'missed its named' {text.count('missed its named')}")
tally = {}
for e in h.MUTATIONS:
    name, breaks = e[0], e[-1]
    if not breaks.startswith(pref):
        continue
    key = "p1 255" if breaks.startswith(h.P1_PREFIX) else breaks.split(" ")[0]
    verdict, fails = segs.get(name, ("missing", []))
    wants = breaks.split(" | ")
    hit = sum(any(w in f for f in fails) for w in wants)
    t = tally.setdefault(key, [0, 0, 0, 0])
    t[0] += 1
    t[1] += verdict == "PASS" and hit == len(wants)
    t[2] += len(wants)
    t[3] += hit
for key, (n, ok, want, hit) in sorted(tally.items()):
    print(f"   {key}: {ok}/{n} mutants caught on every named check; "
          f"{hit}/{want} named checks printed FAIL")

print("4. SOURCE_EVIDENCE")
r4 = subprocess.run(["python3", "scripts/check_source_evidence.py"], cwd=HEAD,
                    capture_output=True, text=True)
print("   " + r4.stdout.strip().splitlines()[-1] + f" (rc {r4.returncode})")
