#!/usr/bin/env python3
"""Round-3 focused sweeps: interior clusters the delta claims to grade exactly.

Usage: python3 -I r3_cluster_probe.py <path-to-tb/tools> <dir holding r3_probe.py> [jobs]

Uses r3_probe.py's independent encoder and arm set (arms at 300/500/700 and
F-700/F-450/F-200, flip arms on channel 1). The DUT events go on channel 2
and on every channel, away from the arms. Each line:
    <id> <OK|DEVIATION> <verdict, why, missed arms, DUT events>
Groups:
  FB  a one-word corruption on channel 2, then a whole-block slip k samples later
      (REQ-VER-06; TESTING 6d "one corrupted word never hides the slips beside it")
  SB  a 3-sample drop or 2-sample repeat, then a whole-block slip k samples later
      (the slip's sample must lie inside its stated location)
  CF  a 100-word constant-mask excursion on channel 2 with a one-word code-bit
      corruption g samples before its start or after its end (rule 4 "at any length")
  CB  a code-bit-only corruption [s, e) on channel 2 covering a whole block
"""
import json
import sys
from multiprocessing import get_context

sys.path.insert(0, sys.argv[2])
TOOLS = sys.argv[1]
JOBS = int(sys.argv[3]) if len(sys.argv) > 3 else 8
sys.argv = [sys.argv[0], TOOLS]
import r3_probe as p  # noqa: E402

F = 16384


def located(e):
    return e.get("located_within", (e["capture_index"],) * 2)


def run(args):
    group, name, ops, checker, params = args
    v, d, dut = p.grade(F, ops)
    ok = globals()[checker](*params)(v, d, dut)
    return f"{group}-{name}", ok, [v, d.get("why"), d.get("planted_missed"), [p.brief(e) for e in dut][:6]]


def check_fb(at, n, mask):
    def check(v, d, dut):
        if v != "FAIL" or d["planted_missed"]:
            return False
        flips = [e for e in dut if e["class"] == "bit-flip"]
        slips = [e for e in dut if e["class"] in ("dropped", "repeated")]
        return (flips and [(e["channel"], e["capture_index"], e["n"], e["mask"]) for e in flips]
                == [(2, 3000, 1, f"0x{mask:08X}")]
                and sorted(e["channel"] for e in slips) == [0, 1, 2, 3]
                and all(e["n"] == abs(n) and located(e)[0] <= at <= located(e)[1] for e in slips))
    return check


def check_sb(at, n, first):
    def check(v, d, dut):
        if v != "FAIL" or d["planted_missed"]:
            return False
        big = [e for e in dut if e["n"] == abs(n)]
        small = [e for e in dut if e["n"] == abs(first)]
        return (len(big) == 4 and len(small) == 4 and len(dut) == 8
                and all(located(e)[0] <= at <= located(e)[1] for e in big)
                and all(located(e)[0] <= 3000 <= located(e)[1] for e in small))
    return check


def check_cf(start, flip, mask):
    def check(v, d, dut):
        got = sorted((e["channel"], e["capture_index"], e["class"], e["n"], e.get("mask")) for e in dut)
        return v == "FAIL" and not d["planted_missed"] and got == sorted(
            [(2, start, "bit-flip", 100, f"0x{mask:08X}"), (2, flip, "bit-flip", 1, "0x00000100")])
    return check


def check_cb(s, e):
    def check(v, d, dut):
        got = [(x["channel"], x["capture_index"], x["class"], x["n"], x.get("mask")) for x in dut]
        return v == "FAIL" and not d["planted_missed"] and got == [(2, s, "bit-flip", e - s, "0x00000100")]
    return check


def cases():
    for mask in (0x100, 0x80000):
        for k in list(range(1, 64)) + [64, 70, 100]:
            for n in (2048, -2048, 4096, -4096, 8192):
                at = 3000 + k
                yield ("FB", f"0x{mask:X}-then-{n}-at+{k}", [("xor", 3000, 2, mask), ("shift", at, n)],
                       "check_fb", (at, n, mask))
    for first in (3, -2):
        for k in list(range(1, 64)) + [64, 100]:
            for n in (4096, -4096):
                at = 3000 + k
                yield ("SB", f"{first}-then-{n}-at+{k}", [("shift", 3000, first), ("shift", at, n)],
                       "check_sb", (at, n, first))
    for mask in (0x80000, 0x40000):
        for g in (1, 2, 5, 20, 40, 63, 64, 70):
            yield ("CF", f"0x{mask:X}x100-flip-{g}-before", [("xor", 3000 + k, 2, mask) for k in range(100)]
                   + [("xor", 3000 - g, 2, 0x100)], "check_cf", (3000, 3000 - g, mask))
            yield ("CF", f"0x{mask:X}x100-flip-{g}-after", [("xor", 3000 + k, 2, mask) for k in range(100)]
                   + [("xor", 3100 + g - 1, 2, 0x100)], "check_cf", (3000, 3100 + g - 1, mask))
    for s in (6143, 6144, 6100, 5000):
        for e in (8192, 8193, 8194, 8200, 8300, 9000, 10240, 10241, 12288, 12300):
            yield ("CB", f"{s}-{e}", [("xor", k, 2, 0x100) for k in range(s, e)], "check_cb", (s, e))


def main():
    with get_context("fork").Pool(JOBS) as pool:
        counts = {}
        for pid, good, observed in pool.imap(run, list(cases()), chunksize=4):
            tag = "OK" if good else "DEVIATION"
            group = pid.split("-")[0]
            counts.setdefault(group, [0, 0])[tag == "DEVIATION"] += 1
            print(f"{pid} {tag} {json.dumps(observed, default=str)}", flush=True)
        for group, (ok, dev) in counts.items():
            print(f"SUMMARY {group} OK={ok} DEVIATION={dev}", flush=True)


if __name__ == "__main__":
    main()
