#!/usr/bin/env python3
"""Probe: on the composed tree, put back the pre-#711 single-vector MVRP walk in
srp_latency.cpp (keeping the new EndMark assertion) and require the
srp_latency arm to FAIL at IF=1 and IF=2; then restore the file's exact bytes
and require the unmodified arm to PASS. Prints PROBE OK or PROBE BAD.

usage: probe_latency_walk.py <repo> <build-dir>
"""
import hashlib
import sys
from pathlib import Path

repo, build = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
import ctrl_arms  # noqa: E402
import fw_gtest  # noqa: E402
import srp_arms  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

target = repo / "sw/firmware/ctrl/test/srp_latency.cpp"
original = target.read_bytes()
digest = hashlib.sha256(original).hexdigest()
NEW = """                else { // 802.1Q-2018 10.8.1.2: a Message holds vectors up to its EndMark.
                       while(off+2<=f->len && (f->bytes[off] || f->bytes[off+1])) {
                           const unsigned n=wire_be16(f->bytes+off)&8191u;
                           off+=2+width+(n+2)/3;
                       }
                       off+=2; }
"""
OLD = """                else { const unsigned n=wire_be16(f->bytes+off)&8191u;
                       off+=2+width+(n+2)/3+2; }
"""
text = original.decode()
if text.count(NEW) != 1:
    sys.exit("PROBE BAD: the grouped walk is not present exactly once")
lwsrp = (repo / "third_party/lwSRP").resolve()


def arms(tag):
    tree = Tree(CTRL, build / tag / "checkout", build / tag / "reuse", fw_gtest.Build(jobs=4))
    cut_reuse(tree.reuse)
    return [srp_arms.arm_srp(tree, lwsrp, i, test="srp_latency.cpp") for i in (1, 2)]


ok = True
try:
    target.write_text(text.replace(NEW, OLD))
    for o in arms("old-walk"):
        print(f"old walk: arm {o.arm} rc {o.rc}")
        print(o.log[-1500:])
        ok = ok and o.rc != 0
finally:
    target.write_bytes(original)
restored = hashlib.sha256(target.read_bytes()).hexdigest() == digest
print(f"restored exact bytes: {restored}")
for o in arms("head"):
    print(f"head walk: arm {o.arm} rc {o.rc}")
    ok = ok and o.rc == 0
print("PROBE OK" if ok and restored else "PROBE BAD")
sys.exit(0 if ok and restored else 1)
