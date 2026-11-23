"""Compare the compiled sources of a whole capture with the union of part captures (measurement only, not committed).

A compile's identity: its compiled source and the files its dependency output lists, each path with the builder's
temporary directory replaced by <tmp>. Usage: compare_sets.py FULL_CAPTURE PART_CAPTURE... (only the compiles whose run is the
control gate's)."""
import re, sys
from pathlib import Path
sys.path[:0] = ["$LANES/ci-fbshard/sw/firmware/ctrl/test", "$LANES/ci-fbshard/sw/firmware/gtest"]
import ctrl_capture
from ctrl_configs import COMPILED
TMP = re.compile(r"/tmp/(?:ctrl-fw-|tmp)[^/]+/")
def norm(p): return TMP.sub("<tmp>/", p)
def compiles(where, word):
    cap = ctrl_capture.load(Path(where))
    keep = set(); count = 0
    for inv in cap.invocations:
        if not any(word in r for r in inv.run):
            continue
        count += 1
        for s in inv.sources:
            if s.lang in COMPILED and s.deps is not None:
                keep.add((norm(s.path), frozenset(map(norm, s.deps.files))))
    return keep, count
word = "test_ctrl_firmware.py"
full, nf = compiles(sys.argv[1], word)
union = set(); n = 0
for part in sys.argv[2:]:
    got, k = compiles(part, word); union |= got; n += k
print(f"whole: {nf} invocations, {len(full)} distinct compiles; parts: {n} invocations, {len(union)} distinct compiles")
print(f"in the whole, in no part: {len(full - union)}")
for src, _ in sorted(full - union)[:10]: print("   ", src)
print(f"in a part, not in the whole: {len(union - full)}")
for src, _ in sorted(union - full)[:10]: print("   ", src)
print("UNION PROOF:", "PASS" if not (full - union) else "FAIL")
