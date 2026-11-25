#!/usr/bin/env python3
"""Probe the boundary gate's text cross-check and its capture hold on the loopback builder.

usage: registry_probe.py TREE CAPTURE   (CAPTURE: a ctrl_capture.py directory of the two registered commands)
"""
import sys
from pathlib import Path

tree, cap = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(tree / "sw/firmware/ctrl/test"))
import ctrl_capture  # noqa: E402
import ctrl_configs as c  # noqa: E402
import ctrl_runs  # noqa: E402

NAME = "tb/verilator/input_loopback_dp/run.py"


def reasons(capture, scope, known):
    try:
        c.held(capture, scope, known=known)
    except Exception as exc:  # the gate's Refusal
        return [r for r in str(exc).split("; ") if r]
    return []


capture = ctrl_capture.load(cap)
print("capture ran:", sorted(capture.ran), "invocations:", len(capture.invocations))
entry = [b for b in c.BUILDERS if b.path == NAME]
print("entries:", len(entry), "needs:", entry[0].needs)
for argv in entry[0].runs:
    print("  argv:", " ".join(argv))
without = c.Scope(frozenset({"verilator"}))
only = c.Scope(frozenset(), "verilator")
minus = tuple(b for b in c.BUILDERS if b.path != NAME)
for label, scope, known in (("without verilator, entry present", without, c.BUILDERS),
                            ("without verilator, entry REMOVED", without, minus),
                            ("only verilator, entry present, its capture given", only, c.BUILDERS)):
    hit = [r for r in reasons(capture, scope, known) if NAME in r or "input_loopback" in r]
    print(f"[{label}] reasons naming the harness: {len(hit)}")
    for r in hit:
        print("   ", r[:330])
# the capture must be required: judge a capture whose own-run record of the harness is dropped
class Gone:
    def __init__(self, cap): self.__dict__["cap"] = cap
    def __getattr__(self, k):
        v = getattr(self.cap, k)
        return {x for x in v if x != NAME} if k == "ran" else v
hit = [r for r in reasons(Gone(capture), only, c.BUILDERS) if NAME in r]
print("[only verilator, the harness's own capture missing] reasons:", len(hit))
for r in hit:
    print("   ", r[:260])
found = [str(p.relative_to(tree)) for p in c.builder_texts() if "input_loopback" in str(p)]
print("found by text under the two suites:", found)
cands = [str(p.relative_to(tree)) for p in c.candidates() if "input_loopback" in str(p)]
print("candidates under the two suites:", cands)
print("legs:", [ctrl_runs.leg_builders(without, i) for i in range(len(ctrl_runs.LEGS))])
fw = [i for i in capture.invocations if "sw/firmware/ctrl/aecp" in " ".join(map(str, i.args))]
print("captured invocations naming the AECP sources:", len(fw))
