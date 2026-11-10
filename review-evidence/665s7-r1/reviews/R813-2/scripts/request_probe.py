"""request_probe.py MILAN_DP WORK OFFSET...: the licence scenario with the peer's MSRP LeaveAll moved from ms 16000
(on lwSRP's periodic grid) to 16000 + OFFSET, one build per OFFSET through srptx_mutants.build() into WORK; each run
graded in full. srptx.hpp is edited in place for each build and restored byte for byte afterwards (checked by
sha256); nothing else in the checkout is written. Prints the MSRP egress around the move, the grade's cause for the
frame after it, and every [TIME] finding."""
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
import srptx_grade as g  # noqa: E402
import srptx_mutants as m  # noqa: E402

hpp = Path(sys.argv[1]) / "srptx.hpp"
work = Path(sys.argv[2])
orig = hpp.read_bytes()
digest = hashlib.sha256(orig).hexdigest()
anchor = b"constexpr std::uint32_t kPeerLeaveAllMs = 16000;"
assert orig.count(anchor) == 1
try:
    for off in (int(x) for x in sys.argv[3:]):
        hpp.write_bytes(orig.replace(anchor, f"constexpr std::uint32_t kPeerLeaveAllMs = {16000 + off};".encode()))
        arm = work / f"la{off}"
        arm.mkdir(parents=True, exist_ok=True)
        ok, out = m.build(arm, None, None)
        hpp.write_bytes(orig)
        if not ok:
            print(f"offset {off}: BUILD FAILED\n{out}")
            continue
        rc, found, _ = m.run(arm, "licence", 0)
        cap = g.load(arm / "licence-0.json")
        frames = [f for f in cap.mrpdus if f.proto == "MSRP" and not f.error and not cap.queued(f)]
        cause = g.causes(cap, "MSRP", frames)
        near = [(round(f.us / 1000, 3), c[0] if c else None, round(c[1]["us"] / 1000, 3) if c else None)
                for f, c in zip(frames, cause) if 15900 <= f.us / 1000 <= 16700]
        full = g.grade(cap)[0]
        print(f"== peer MSRP LeaveAll at ms {16000 + off}: binary rc {rc}; applied at ms "
              f"{g.applied_ms(cap, 'MSRP LeaveAll, the peer, no re-declaration')}")
        print(f"   MSRP egress 15900..16700 ms as (egress ms, grade's cause, that expiry's ms): {near}")
        print(f"   {len(full)} finding(s)")
        for f in full:
            print(f"     {f}")
finally:
    hpp.write_bytes(orig)
    assert hashlib.sha256(hpp.read_bytes()).hexdigest() == digest
    print(f"srptx.hpp restored, sha256 {digest}")
