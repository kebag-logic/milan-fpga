"""set_measured.py <baseline> <before>: round 2 (the merge e44a4d20). the three endpoints' `measured` notes, the one field the gate's record --write
leaves alone (written by hand on every earlier re-record). Touches no record, tolerance, floor or ceiling; writes the
file in the gate's own format (json indent 1), and refuses unless only the notes differ from the recorder's output."""
import json
import sys
from pathlib import Path

path, before = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text())
text = path.read_text()
b = json.loads(text)
assert json.dumps(b, indent=1) + "\n" == text, "the file is not in the recorder's format"
P = "044cb25f4ed2187bd238490650e73d5d189855d1"
G = "1616fc8f062fbf58c35ad31674b5b233207bbdb8"
DEV = "0a75aa774b89ac89351700f63dd8cbb89694af6c"
L = "e44a4d20d95858124b83048c0db4980b3e05a238"
URL = "https://github.com/kebag-logic/milan-fpga/issues/845#issuecomment-6689114981"
HEAD = (f"2026-11-08, issue #851 (processor pin {P}, processor #214, PR #215) with FPGA-gPTP pin {G} (issue #843, PR #846): "
        f"RTL inputs at lane commit {L}, the lane's merge of dev {DEV}; the lane's later commits change no synthesis input. "
        "Explicit synth.maxThreads 1, general.maxThreads 32")
TAIL = ("Every tolerance, floor and ceiling unchanged. docs/findings/234_PP_SHADOW_AREA_BASELINE.md retains the earlier "
        "records and this delta.")
OOC = ("The figures equal the measurement at lane commit a566d4f9 on dev 1eb5289d; the input digest differs because the "
       "export's read set also holds FPGA-gPTP sources and images, which KL_pp_shadow does not instantiate. "
       "It is re-recorded with the route so that the record measures one tree. ")


def delta(ep, k):
    return b["endpoints"][ep]["record"]["figures"][k] - before["endpoints"][ep]["record"]["figures"][k]


r = b["endpoints"]["route-1x1"]["record"]["figures"]
notes = {
    "route-1x1": HEAD + "; the first route with all four lab fixes; the recipe's three placement directives from one synthesis "
    "checkpoint, AltSpreadLogic_high selected by the gate at WNS +0.210 ns over ExtraPostPlacementOpt +0.112 ns and "
    f"ExtraTimingOpt +0.018 ns. {15850 - r['SLICE']} of 15,850 slices remain. Against the fourteenth record (#843's route, "
    f"which measures dev {DEV[:8]}'s synthesis inputs) the route moved by +{delta('route-1x1', 'LUT')} LUT (tolerance +500), "
    f"+{delta('route-1x1', 'FF')} FF (+600) and {delta('route-1x1', 'SLICE')} slices (80), with RAMB36, RAMB18 and DSP "
    f"unchanged, WNS {delta('route-1x1', 'WNS_ns'):+.3f} ns and WHS {delta('route-1x1', 'WHS_ns'):+.3f} ns: the gate passed "
    "it, and that movement is this adoption's alone. It is re-recorded so that the record measures the merged tree; the "
    f"lab fixes' growth up to the fourteenth record is under the maintainer decision of 2026-11-06, {URL}. " + TAIL,
    "ooc-1x1": HEAD + "; the shipping 20 ns clock. Against the fourteenth record, whose standalone records are #845's "
    f"(processor 92100657), the wrapper moved by +{delta('ooc-1x1', 'LUT')} LUT and +{delta('ooc-1x1', 'FF')} FF "
    "(tolerances 250 and 250), RAMB36, RAMB18 and DSP unchanged; the gate passed it. " + OOC + TAIL,
    "ooc-8x8": HEAD + "; out of context only, not routed; an RTL elaboration supplies the bound parameters; the shipping 20 ns "
    "clock. Against the fourteenth record, whose standalone records are #845's (processor 92100657), the wrapper moved by "
    f"+{delta('ooc-8x8', 'LUT')} LUT and +{delta('ooc-8x8', 'FF')} FF (tolerances 316 and 339), RAMB36, RAMB18 and DSP "
    "unchanged; the gate passed it. " + OOC + TAIL,
}
for name, note in notes.items():
    assert note.isascii()
    b["endpoints"][name]["measured"] = note
path.write_text(json.dumps(b, indent=1) + "\n")
after = json.loads(path.read_text())
for ep in after["endpoints"]:
    x, y = dict(after["endpoints"][ep]), dict(json.loads(text)["endpoints"][ep])
    x.pop("measured"); y.pop("measured")
    assert x == y
print("notes set")
