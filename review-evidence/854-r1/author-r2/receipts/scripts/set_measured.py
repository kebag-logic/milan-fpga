"""set_measured.py <baseline> <before> <route-check-log>: #854 round 2, the head's re-record. The three endpoints'
`measured` notes, the one field the gate's record --write leaves alone (written by hand on every earlier re-record).
Touches no record, tolerance, floor or ceiling; writes the file in the gate's own format (json indent 1), and refuses
unless only the notes differ from the recorder's output. <before> is the fifteenth record (dev ac0a01e3's file);
<route-check-log> is the route set's check against it, whose route-set lines give each directive's worst-corner WNS."""
import json
import re
import sys
from pathlib import Path

path, before = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text())
routes = dict(re.findall(r"^  (\w+)\s+(-?[0-9.]+)\s+-?[0-9.]+\s", Path(sys.argv[3]).read_text(), re.M))
text = path.read_text()
b = json.loads(text)
assert json.dumps(b, indent=1) + "\n" == text, "the file is not in the recorder's format"
assert set(routes) == {"ExtraPostPlacementOpt", "AltSpreadLogic_high", "ExtraTimingOpt"}, routes
P = "044cb25f4ed2187bd238490650e73d5d189855d1"
G = "1616fc8f062fbf58c35ad31674b5b233207bbdb8"
DEV = "ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36"
L = "7a19f62b4e622d1d7d563184363a42e2644776c1"
HEAD = (f"2026-11-09, issue #854 (the all-fabric tap's control-frame drop count, read from the FIFO's own overflow "
        f"indication) on processor pin {P} and FPGA-gPTP pin {G}, both unchanged: RTL inputs at lane commit {L} on dev "
        f"{DEV}, the live dev tip, so the lane is its own merge result; the lane's later commits change no synthesis "
        "input. Explicit synth.maxThreads 1, general.maxThreads 32")
WHY = ("on dev the count is constant 0 and synthesis removes it with the FIFO's overflow register; it now exists, "
       "with the register of the last beat's classification. It is re-recorded because the change moves the shipping "
       "image (docs/design/AREA_BUDGET.md, the re-baseline rule). ")
SAME = (f"From the fifteenth record's measured commit e44a4d20 to dev {DEV[:8]} no synthesis input moves, so the "
        "movement is this change's: " + WHY)
#: the fifteenth record's own ExtraPostPlacementOpt route, docs/findings/234_PP_SHADOW_AREA_BASELINE.md (its notes
#: give that route's WNS, +0.112 ns)
EPPO15 = {"LUT": 53383, "FF": 54837, "SLICE": 15848, "WNS_ns": 0.112, "WHS_ns": 0.036}
TAIL = ("Every tolerance, floor and ceiling unchanged. docs/findings/234_PP_SHADOW_AREA_BASELINE.md retains the earlier "
        "records and this delta.")


def fig(ep, k, rec=None):
    return (rec or b)["endpoints"][ep]["record"]["figures"][k]


def delta(ep, k):
    return fig(ep, k) - fig(ep, k, before)


def flow_directive(rec):
    flow = rec["endpoints"]["route-1x1"]["record"]["identity"]["flow"]
    return next(x.split()[-1] for x in flow if x.startswith("place_design -directive "))


sel = flow_directive(b)
assert sel == "ExtraPostPlacementOpt", "the same-directive sentence assumes the shipping directive was selected"
others = [d for d in ("AltSpreadLogic_high", "ExtraPostPlacementOpt", "ExtraTimingOpt") if d != sel]
wns = {d: float(v) for d, v in routes.items()}
notes = {
    "route-1x1": HEAD + "; the recipe's three placement directives from one synthesis checkpoint, "
    f"{sel} selected by the gate at WNS {wns[sel]:+.3f} ns over {others[0]} {wns[others[0]]:+.3f} ns and "
    f"{others[1]} {wns[others[1]]:+.3f} ns. {15850 - fig('route-1x1', 'SLICE')} of 15,850 slices remain. Against the "
    f"fifteenth record (#851's route, {flow_directive(before)}) the route moved by {delta('route-1x1', 'LUT'):+d} LUT "
    f"(tolerance +500), {delta('route-1x1', 'FF'):+d} FF (+600) and {delta('route-1x1', 'SLICE'):+d} slices (80), with "
    f"RAMB36 {delta('route-1x1', 'RAMB36'):+d}, RAMB18 {delta('route-1x1', 'RAMB18'):+d} and DSP "
    f"{delta('route-1x1', 'DSP'):+d}, WNS {delta('route-1x1', 'WNS_ns'):+.3f} ns and WHS "
    f"{delta('route-1x1', 'WHS_ns'):+.3f} ns: the gate passed it. From the fifteenth record's measured commit "
    f"e44a4d20 to dev {DEV[:8]} no synthesis input moves, so the difference is this change's and the selected "
    "directive's. At one directive, against the fifteenth record's own ExtraPostPlacementOpt route "
    f"({EPPO15['LUT']:,} LUT, {EPPO15['FF']:,} FF, {EPPO15['SLICE']:,} slices, WNS +{EPPO15['WNS_ns']:.3f} ns), this "
    f"route at ExtraPostPlacementOpt moved by {fig('route-1x1', 'LUT') - EPPO15['LUT']:+d} LUT, "
    f"{fig('route-1x1', 'FF') - EPPO15['FF']:+d} FF and {fig('route-1x1', 'SLICE') - EPPO15['SLICE']:+d} slices, WNS "
    f"{fig('route-1x1', 'WNS_ns') - EPPO15['WNS_ns']:+.3f} ns and WHS {fig('route-1x1', 'WHS_ns') - EPPO15['WHS_ns']:+.3f} "
    "ns: the WNS fall against the record is the directive's, not this change's; " + WHY + TAIL,
    "ooc-1x1": HEAD + "; the shipping 20 ns clock. Against the fifteenth record (#851's) the wrapper moved by "
    f"{delta('ooc-1x1', 'LUT'):+d} LUT and {delta('ooc-1x1', 'FF'):+d} FF (tolerances 250 and 250), RAMB36 "
    f"{delta('ooc-1x1', 'RAMB36'):+d}, RAMB18 {delta('ooc-1x1', 'RAMB18'):+d} and DSP {delta('ooc-1x1', 'DSP'):+d}; "
    "the gate passed it. " + SAME + TAIL,
    "ooc-8x8": HEAD + "; out of context only, not routed; an RTL elaboration supplies the bound parameters; the "
    f"shipping 20 ns clock. Against the fifteenth record (#851's) the wrapper moved by {delta('ooc-8x8', 'LUT'):+d} LUT "
    f"and {delta('ooc-8x8', 'FF'):+d} FF (tolerances 316 and 339), RAMB36 {delta('ooc-8x8', 'RAMB36'):+d}, RAMB18 "
    f"{delta('ooc-8x8', 'RAMB18'):+d} and DSP {delta('ooc-8x8', 'DSP'):+d}; the gate passed it. " + SAME + TAIL,
}
for name, note in notes.items():
    assert note.isascii()
    b["endpoints"][name]["measured"] = note
path.write_text(json.dumps(b, indent=1) + "\n")
after = json.loads(path.read_text())
for ep in after["endpoints"]:
    x, y = dict(after["endpoints"][ep]), dict(json.loads(text)["endpoints"][ep])
    x.pop("measured")
    y.pop("measured")
    assert x == y
for name, note in notes.items():
    print(f"{name}: {note}\n")
print("notes set")
