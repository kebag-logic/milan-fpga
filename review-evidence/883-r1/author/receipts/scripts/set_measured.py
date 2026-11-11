"""set_measured.py <baseline> <before>: the three endpoints' `measured` notes for #883's record, the one field the
gate's record --write leaves alone (written by hand on every earlier re-record). Touches no record, tolerance, floor or
ceiling; writes the file in the gate's own format (json indent 1), and refuses unless only the notes differ."""
import json
import sys
from pathlib import Path

path, before = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text())
text = path.read_text()
b = json.loads(text)
assert json.dumps(b, indent=1) + "\n" == text, "the file is not in the recorder's format"
P = "801ef2283ec793e35a2590fc6593c90313a64041"
G = "a64be73de32f3ec5084cf908a530218e9006453e"
G_KEPT = "1616fc8f062fbf58c35ad31674b5b233207bbdb8"
REVERT = "8edfae9957c99233007255a3f62f26a5706879e2"
DEV = "46c971fa0a09e2c8ca21acb95769defdc06c3068"
L = "a89802c8dc278fabeff06fd2a79070611187a8f7"
HEAD = (f"2026-11-11, issue #883 (processor pin {P}, processor #216 and #217, PRs #218 and #219; FPGA-gPTP pin {G_KEPT} "
        f"unchanged): RTL inputs at lane commit {L} on dev {DEV}, the live dev tip, so the lane is its own merge result. "
        f"That commit carried FPGA-gPTP pin {G} (FPGA-gPTP #102, PR #103, no RTL, synthesis or ROM change), which lane "
        f"commit {REVERT} reverts to {G_KEPT[:8]} (#883 ruling); an export at the final pins reads the same synthesis "
        "inputs, and the lane's other later commits change none. Explicit synth.maxThreads 1, general.maxThreads 32")
TAIL = ("It is re-recorded because the change moves the shipping image (docs/design/AREA_BUDGET.md, the re-baseline "
        "rule). Every tolerance, floor and ceiling unchanged. docs/findings/234_PP_SHADOW_AREA_BASELINE.md retains the "
        "earlier records and this delta.")


def delta(ep, k):
    return b["endpoints"][ep]["record"]["figures"][k] - before["endpoints"][ep]["record"]["figures"][k]


r = b["endpoints"]["route-1x1"]["record"]["figures"]
notes = {
    "route-1x1": HEAD + "; the recipe's three placement directives from one synthesis checkpoint, ExtraPostPlacementOpt "
    "selected by the gate at WNS +0.334 ns over ExtraTimingOpt +0.218 ns and AltSpreadLogic_high +0.162 ns. "
    f"{15850 - r['SLICE']} of 15,850 slices remain. Against the sixteenth record (#854's route, ExtraPostPlacementOpt, "
    f"which measures dev {DEV[:8]}'s synthesis inputs) the route moved by {delta('route-1x1', 'LUT'):+d} LUT (tolerance "
    f"+500), {delta('route-1x1', 'FF'):+d} FF (+600) and {delta('route-1x1', 'SLICE'):+d} slices (80), with RAMB36, "
    f"RAMB18 and DSP unchanged, WNS {delta('route-1x1', 'WNS_ns'):+.3f} ns and WHS {delta('route-1x1', 'WHS_ns'):+.3f} "
    "ns: the gate passed it, and the movement is this adoption's alone, at the same directive. " + TAIL,
    "ooc-1x1": HEAD + "; the shipping 20 ns clock. Against the sixteenth record (#854's) the wrapper moved by "
    f"{delta('ooc-1x1', 'LUT'):+d} LUT and {delta('ooc-1x1', 'FF'):+d} FF (tolerances 250 and 250), RAMB36, RAMB18 and "
    "DSP unchanged; the gate passed it. " + TAIL,
    "ooc-8x8": HEAD + "; out of context only, not routed; an RTL elaboration supplies the bound parameters; the shipping "
    f"20 ns clock. Against the sixteenth record (#854's) the wrapper moved by {delta('ooc-8x8', 'LUT'):+d} LUT and "
    f"{delta('ooc-8x8', 'FF'):+d} FF (tolerances 316 and 339), RAMB36, RAMB18 and DSP unchanged; the gate passed it. "
    + TAIL,
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
print("notes set")
