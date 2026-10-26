#!/usr/bin/env python3
"""Check each remaining deviation of R699-3's unmodified probes against its stated limit.

Usage: python3 -I limit_proofs.py <tb/tools dir> <dir holding the reviewer's r3_probe.py>

Every capture is built with the reviewer's own encoder (r3_probe.build and
its arm set), never the planner's. One line per case:
    <id> <PROVED|NOT PROVED> <claim> <evidence>
FB and SB: the bytes equal the stated alternative capture, and the grader
reads that alternative. A over-strict: FAIL, every arm found, and each DUT
slip's located_within holds the planted sample. A same-sample: the DUT slip
sits at a planted slip arm's own sample and is not whole blocks; the run is
void with that arm missed. A spans: FAIL with every arm found, read as the
slips its words show. E: FAIL, the slip inside the interval and fewer than
64 captured samples after its first differing word, read as unresolved with
located_within holding it. Exit status 0.
"""
import sys

sys.path.insert(0, sys.argv[2])
sys.argv = [sys.argv[0], sys.argv[1]]
import r3_probe as p  # noqa: E402

F = 16384


def capture(frames: int, ops: list) -> list:
    """The reviewer's frames for `ops` with the reviewer's arms."""
    arm_ops, _ = p.arms(frames)
    return p.build(frames, arm_ops + ops)


def located(event: dict) -> tuple:
    return tuple(event.get("located_within", (event["capture_index"],) * 2))


def line(pid: str, ok: bool, claim: str, evidence: object) -> None:
    print(f"{pid} {'PROVED' if ok else 'NOT PROVED'} {claim} {evidence}", flush=True)


# FB: a code-bit corruption at 3000 that equals the new track's word, every word up to the slip on both tracks.
for n, k in ((2048, 1), (-2048, 1), (-4096, 1), (2048, 2), (2048, 3), (2048, 4)):
    ops = [("xor", 3000, 2, 0x100), ("shift", 3000 + k, n)]
    alone = [("shift", 3000, n, 2)] + [("shift", 3000 + k, n, c) for c in (0, 1, 3)]
    v, d, dut = p.grade(F, ops)
    ch2 = [e for e in dut if e["channel"] == 2]
    ok = (capture(F, ops) == capture(F, alone) and v == "FAIL" and not d["planted_missed"]
          and [e["class"] for e in ch2] == ["dropped" if n > 0 else "repeated"] and ch2[0]["capture_index"] == 3000)
    line(f"FB-0x100-then-{n}-at+{k}", ok, "bytes equal the slip alone at the corrupted word on channel 2",
         [p.brief(e) for e in ch2])
# SB: a 3-sample drop at 3000 whose words all fit both tracks up to the slip of whole blocks.
for k in (1, 2):
    ops = [("shift", 3000, 3), ("shift", 3000 + k, 4096)]
    v, d, dut = p.grade(F, ops)
    ok = (capture(F, ops) == capture(F, [("shift", 3000, 4099)]) and v == "FAIL"
          and {(e["class"], e["n"], e["capture_index"]) for e in dut} == {("dropped", 4099, 3000)})
    line(f"SB-3-then-4096-at+{k}", ok, "bytes equal one slip of the sum at 3000", sorted({p.brief(e)["n"] for e in dut}))
# A, over-strict: the probe compares capture_index; located_within holds the planted sample.
for name, at in (("drop4096-5-after-repeat", 505), ("drop4096-5-after-flip", 705), ("drop4096-40-after-flip", 740),
                 ("drop4096-900-after-repeat", 1400)):
    v, d, dut = p.grade(F, [("shift", at, 4096)])
    ok = (v == "FAIL" and not d["planted_missed"] and len(dut) == 4
          and all(e["n"] == 4096 and located(e)[0] <= at <= located(e)[1] for e in dut))
    line(f"A-{name}", ok, f"every arm found and each slip located around {at}", [located(e) for e in dut])
# A, same sample: the DUT slip of 1024 sits at the drop arm (300) or the repeat arm (500).
for name, at, arm in (("drop1024-200-before-repeat", 300, 3), ("drop1024-200-before-flip", 500, -2)):
    v, d, dut = p.grade(F, [("shift", at, 1024)])
    ok = (v == "NOT RUN" and [a["index"] for a in d["planted_missed"]] == [at]
          and {e["n"] for e in dut} == {abs(1024 + arm)})
    line(f"A-{name}", ok, f"one slip of the sum {1024 + arm} at the arm's own sample; the arm is missed",
         sorted({e["n"] for e in dut}))
# A, spans: a constant-mask corruption that the planted repeat at 500 interrupts.
for ch in (0, 1):
    v, d, dut = p.grade(F, [("xor", 450 + k, ch, 0x80000) for k in range(100)])
    ok = v == "FAIL" and not d["planted_missed"] and {e["class"] for e in dut} == {"dropped", "repeated"}
    line(f"A-ch{ch}-0x80000x100-spans-repeat", ok, "every arm found; read as the slips its words show",
         [p.brief(e) for e in dut])
# E: inside the interval, fewer than 64 captured samples after the first differing word.
for n, back in ((-2048, 64), (-4096, 64), (6291456, 64), (-2048, 65), (6291456, 65), (6291456, 66)):
    frames = 8192
    at = frames - back
    v, d, dut = p.grade(frames, [("shift", at, n)])
    q = d["qualified"]
    ok = (v == "FAIL" and at < q["end"] and len(dut) == 4
          and all(e["class"] == "unresolved" and located(e)[0] <= at <= located(e)[1]
                  and frames - e["capture_index"] < 64 for e in dut))
    line(f"E-{n}-at-F-{back}", ok, "unresolved, located around the slip, under 64 samples from the end",
         sorted({(e["capture_index"], located(e)) for e in dut}))
