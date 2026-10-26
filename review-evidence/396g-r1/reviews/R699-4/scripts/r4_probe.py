#!/usr/bin/env python3
"""Round-4 independent probe of the #396 audio counter grader.

Usage: python3 -I r4_probe.py <path-to-tb/tools> <dir holding r3_probe.py> [jobs]

Words come from r3_probe.py's own encoder (TESTING.md 6d layout), never the
planner's synthesizer. Arms are r3_probe's standard log (tolerance 2).

Groups:
  X  byte identity of every residual round-3 probe deviation with the reading
     the grader gave (the stated limits), and that reading's located_within.
  R  seeded fuzz: 1 to 3 DUT events (one-word corruptions with assorted masks,
     slips of assorted sizes, all channels or one) clustered within 64 samples,
     near a planted arm or in the open. Oracle:
       - PASS only when the bytes equal the arms-only capture;
       - NOT RUN only when a DUT slip lands on a slip arm's own sample;
       - every arm found when FAIL;
       - per channel, the signed sum of DUT slip sizes equals the true net DUT
         shift, unless an unresolved event is on that channel;
       - every DUT event's sample lies inside some reported DUT event on its
         channel (located_within or capture_index, +-2 tolerance) - INFO only,
         byte-identical alternatives are allowed by the stated limits.
  C  constant-mask excursions (64..2049 words, assorted masks) with a one-word
     corruption or a short slip beside one or both ends, 1..64 samples away.
     Oracle: one bit-flip of the excursion's length and mask at its start, and
     the neighbour graded at its own sample in its own class.
One line per case: <group>-<id> <OK|DEVIATION|INFO> <observed>; a summary per group.
Exit status is 0.
"""
import json
import random
import sys
from multiprocessing import get_context

TOOLS, HERE = sys.argv[1], sys.argv[2]
JOBS = int(sys.argv[3]) if len(sys.argv) > 3 else 8
sys.path.insert(0, HERE)
sys.argv = [sys.argv[0], TOOLS]
import r3_probe as p  # noqa: E402

C = p.C


def bytes_of(frames, ops, planted=True):
    aops = p.arms(frames)[0] if planted else []
    return p.build(frames, aops + list(ops))


def brief(e):
    return p.brief(e)


def span(e):
    lo, hi = e.get("located_within", (e["capture_index"],) * 2)
    if e["class"] in ("bit-flip", "unresolved", "swap"):
        hi = max(hi, e["capture_index"] + e.get("n", 1) - 1)
    return lo, hi


# ---- X: residual round-3 deviations are byte-identical stated limits ---------------
def x_cases():
    F = 8192
    out = []
    # FB residuals: 0x100 at 3000 on ch2, then a whole-block slip at 3000+k on all channels.
    for n, k in ((2048, 1), (-2048, 1), (-4096, 1), (2048, 2), (2048, 3), (2048, 4)):
        ops = [("xor", 3000, 2, 0x100), ("shift", 3000 + k, n)]
        alt = [("shift", 3000, n, 2)] + [("shift", 3000 + k, n, c) for c in (0, 1, 3)]
        out.append((f"FB-0x100-then-{n}-at+{k}", F, ops, alt, {2: 3000}, 3000 + k))
    # SB residuals: drop 3 at 3000 then 4096 at 3000+k reads as one drop of 4099 at 3000.
    for k in (1, 2):
        ops = [("shift", 3000, 3), ("shift", 3000 + k, 4096)]
        alt = [("shift", 3000, 4099)]
        out.append((f"SB-3-then-4096-at+{k}", F, ops, alt, {c: 3000 for c in range(C)}, None))
    # A NOT RUN residuals: a DUT slip on a slip arm's own sample (stated limit).
    for at, n in ((300, 1024), (500, 1024)):
        out.append((f"A-own-sample-{at}-{n}", 16384, [("shift", at, n)], None, None, at))
    return out


def case_x(args):
    name, F, ops, alt, alt_at, true_at = args
    v, d, dut = p.grade(F, ops)
    obs = [brief(e) for e in dut]
    if alt is None:
        ok = v == "NOT RUN" and [a["index"] for a in d["planted_missed"]] == [true_at]
        return f"X-{name}", ok, [v, d.get("why"), d["planted_missed"], obs]
    same = bytes_of(F, ops) == bytes_of(F, alt)
    ok = same and v == "FAIL" and not d["planted_missed"]
    # The reading given must be the alternative's: no bit-flip, each alt slip inside its event.
    ok = ok and not any(e["class"] == "bit-flip" for e in dut)
    for c, at in alt_at.items():
        es = [e for e in dut if e["channel"] == c and e["class"] in ("dropped", "repeated")]
        ok = ok and any(span(e)[0] <= at <= span(e)[1] for e in es)
    return f"X-{name}", ok, ["bytes-identical" if same else "bytes-DIFFER", v, obs]


# ---- R: seeded fuzz ----------------------------------------------------------------
MASKS = (0x100, 0x80000, 0x40000, 0x80100, 0x00F00F00, 0x01000000, 0x100000, 0x200, 0x1E00)
SIZES = (1, -1, 2, -2, 3, 5, -5, 100, -100, 1024, -1024, 2047, 2048, -2048, 2049, 4096, -4096, 8192, 6291456)
F_R = 16384
ARM_AT = (300, 500, 700, F_R - 700, F_R - 450, F_R - 200)
SLIP_ARMS = {300: 3, 500: -2, F_R - 700: 3, F_R - 450: -2}


def r_cases(count, seed):
    rnd = random.Random(seed)
    for i in range(count):
        base = rnd.choice(ARM_AT + (2000, 6000, 9000)) + rnd.randint(-66, 66)
        ops = []
        for _ in range(rnd.choice((1, 2, 2, 3))):
            at = base + rnd.randint(0, 64)
            if rnd.random() < 0.5:
                ops.append(("xor", at, rnd.randrange(C), rnd.choice(MASKS)))
            else:
                n = rnd.choice(SIZES)
                ops.append(("shift", at, n) if rnd.random() < 0.6 else ("shift", at, n, rnd.randrange(C)))
        yield f"{i}", ops


def case_r(args):
    name, ops = args
    v, d, dut = p.grade(F_R, ops)
    obs = [brief(e) for e in dut]
    problems = []
    clean = bytes_of(F_R, ops) == bytes_of(F_R, [])
    if v == "PASS" and not clean:
        problems.append("FALSE-PASS")
    if v == "NOT RUN":
        own = any(o[0] == "shift" and SLIP_ARMS.get(o[1]) is not None and (o[2] - 0) % 2048 != 0 for o in ops)
        own_any = any(o[0] == "shift" and o[1] in SLIP_ARMS for o in ops)
        own_flip = any(o[0] == "xor" and o[1] in (700, F_R - 200) and o[2] == 1 for o in ops)
        if own_flip and not own_any:
            return f"R-{name}", "LIMIT-own-flip-sample", [v, d.get("why"), [list(o) for o in ops], obs[:12]]
        if own and not problems:
            return f"R-{name}", "LIMIT-own-slip-sample", [v, d.get("why"), [list(o) for o in ops], obs[:12]]
        if not own_any:
            problems.append("VOID:" + str(d.get("why")))
        elif not own:
            problems.append("VOID-own-sample-whole-block:" + str(d.get("why")))
    if v == "FAIL" and d.get("planted_missed"):
        problems.append("FAIL-with-missed-arm")
    info = []
    if v in ("FAIL",):
        for c in range(C):
            net = sum(o[2] for o in ops if o[0] == "shift" and (len(o) < 4 or o[3] == c))
            got = sum((e["n"] if e["class"] == "dropped" else -e["n"]) for e in dut
                      if e["channel"] == c and e["class"] in ("dropped", "repeated"))
            if any(e["channel"] == c and e["class"] == "unresolved" for e in dut):
                continue
            if net != got:
                problems.append(f"NET-ch{c}:{net}!={got}")
        for o in ops:
            chans = [o[2]] if o[0] == "xor" else ([o[3]] if len(o) > 3 else range(C))
            at = o[1]
            for c in chans:
                if not any(e["channel"] == c and span(e)[0] - 2 <= at <= span(e)[1] + 2 for e in dut):
                    info.append(f"uncovered:{o}@ch{c}")
    status = "DEVIATION" if problems else ("INFO" if info else "OK")
    return f"R-{name}", status, [v, d.get("why"), problems, info, [list(o) for o in ops], obs[:12]]


# ---- C: constant-mask excursions beside one-word events ---------------------------
def c_cases():
    for mask in (0x80000, 0x40000, 0x100, 0x00F00F00, 0x80100):
        for length in (64, 65, 100, 300, 2049):
            for begin in (3000, 4096 - 7, 6143):
                for gap in (1, 2, 17, 63, 64):
                    for side in ("before", "after", "both"):
                        for nb in ("flip", "slip3", "slip-2"):
                            yield mask, length, begin, gap, side, nb


def case_c(args):
    mask, length, begin, gap, side, nb = args
    F = 16384
    ch = 2
    ops = [("xor", begin + k, ch, mask) for k in range(length)]
    nmask = 0x100 if mask != 0x100 else 0x80000
    sites = []
    if side in ("before", "both"):
        sites.append(begin - gap)
    if side in ("after", "both"):
        sites.append(begin + length - 1 + gap)
    expect_slips = []
    for s in sites:
        if nb == "flip":
            ops.append(("xor", s, ch, nmask))
        else:
            n = 3 if nb == "slip3" else -2
            ops.append(("shift", s, n))
            expect_slips.append((s, n))
    v, d, dut = p.grade(F, ops)
    obs = [brief(e) for e in dut]
    ok = v == "FAIL" and not d["planted_missed"]
    flips = [e for e in dut if e["class"] == "bit-flip" and e["channel"] == ch and e.get("n", 1) > 1]
    ok = ok and len(flips) == 1 and flips[0]["capture_index"] == begin and flips[0]["n"] == length \
        and flips[0]["mask"] == f"0x{mask:08X}"
    if nb == "flip":
        for s in sites:
            ok = ok and any(e["class"] == "bit-flip" and e["channel"] == ch and e["capture_index"] == s
                            and e["n"] == 1 and e["mask"] == f"0x{nmask:08X}" for e in dut)
        ok = ok and not any(e["class"] in ("dropped", "repeated", "unresolved") for e in dut)
    else:
        for s, n in expect_slips:
            for c in range(C):
                ok = ok and any(e["channel"] == c and e["class"] == ("dropped" if n > 0 else "repeated")
                                and e["n"] == abs(n) and span(e)[0] <= s <= span(e)[1] for e in dut)
        slips = [e for e in dut if e["class"] in ("dropped", "repeated")]
        ok = ok and len(slips) == C * len(expect_slips) and not any(e["class"] == "unresolved" for e in dut)
    return f"C-0x{mask:X}-L{length}-b{begin}-g{gap}-{side}-{nb}", ok, [v, obs[:10]]


def run(group, fn, cases):
    with get_context("fork").Pool(JOBS) as pool:
        res = pool.map(fn, list(cases), chunksize=4)
    counts = {}
    for name, ok, obs in res:
        status = ok if isinstance(ok, str) else ("OK" if ok else "DEVIATION")
        counts[status] = counts.get(status, 0) + 1
        print(name, status, json.dumps(obs), flush=True)
    print("SUMMARY", group, " ".join(f"{k}={v}" for k, v in sorted(counts.items())), flush=True)


def main():
    run("X", case_x, x_cases())
    run("C", case_c, c_cases())
    run("R", case_r, r_cases(6000, 396004))


if __name__ == "__main__":
    main()
