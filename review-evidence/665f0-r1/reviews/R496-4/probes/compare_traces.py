#!/usr/bin/env python3
"""R496-4 reviewer probe: compare a head trace with an unbounded-queue
reference trace of probe_coalesce_diff.c in drain mode.

FAIL lines (the probe's head invariants) are not compared: the reference
exceeds the head's cap by design, and the head's own FAIL lines are graded by
its exit code in run_probes.sh.

Pass when (a) every state line agrees and (b) the wires agree once runs of
back-to-back identical ENTITY_DEPARTING frames are collapsed to one, i.e. the
head drops only back-to-back repeats of a DEPARTING. Also reports how many
frames the reference sent that the head did not, and that each was such a
repeat.

Usage: compare_traces.py HEAD_TRACE REF_TRACE
"""
import sys


def load(path):
    wire, states = [], []
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            if ln.startswith("W "):
                wire.append(tuple(ln.split()[1:]))
            elif ln.startswith("S "):
                states.append(ln.strip())
    return wire, states


def collapse(wire):
    out = []
    for f in wire:
        if out and f[0] == "DE" and out[-1] == f:
            continue
        out.append(f)
    return out


def main():
    hw, hs = load(sys.argv[1])
    rw, rs = load(sys.argv[2])
    ok = True
    if hs != rs:
        ok = False
        for i, (a, b) in enumerate(zip(hs, rs)):
            if a != b:
                print(f"STATE DIFF at line {i}: head {a!r} ref {b!r}")
                break
        else:
            print(f"STATE LENGTH DIFF {len(hs)} vs {len(rs)}")
    if collapse(hw) != collapse(rw):
        ok = False
        print("WIRE DIFF after collapsing back-to-back identical DEPARTINGs")
    dropped = len(rw) - len(hw)
    head_repeats = len(hw) - len(collapse(hw))
    print(f"head frames {len(hw)}, reference frames {len(rw)}, reference-only frames {dropped}, "
          f"head back-to-back identical DEPARTINGs kept {head_repeats}")
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
