"""set_measured.py <baseline> <before>: the three endpoints' `measured` notes, the one field the gate's record --write
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
G = "135afd043309369a87ddbc8d6550aff8ec52a157"
DEV = "1eb5289db8fc9d139ce90cad2e380b4515793806"
L = "a566d4f9706fcbe03594c8f03034130a8da3ff07"
URL = "https://github.com/kebag-logic/milan-fpga/issues/845#issuecomment-6689114981"
HEAD = (f"2026-11-07, issue #851 (processor pin {P}, processor #214, PR #215): RTL inputs at lane commit {L} on dev {DEV}, "
        f"with FPGA-gPTP {G}; the lane's later commits change no synthesis input. Explicit synth.maxThreads 1, general.maxThreads 32")
TAIL = (f"The maintainer accepted the area growth of the mandatory lab fixes on 2026-11-06, with a re-baselined budget, in {URL}. "
        "The differences include dev's movement since the thirteenth record (87e9d03a): PRs #841 and #842. "
        "Every tolerance, floor and ceiling unchanged. docs/findings/234_PP_SHADOW_AREA_BASELINE.md retains the earlier records and this delta.")


def delta(ep, k):
    return b["endpoints"][ep]["record"]["figures"][k] - before["endpoints"][ep]["record"]["figures"][k]


r = b["endpoints"]["route-1x1"]["record"]["figures"]
notes = {
    "route-1x1": HEAD + "; the recipe's three placement directives from one synthesis checkpoint, ExtraTimingOpt selected by the gate "
    "at WNS +0.258 ns over ExtraPostPlacementOpt +0.044 ns and AltSpreadLogic_high +0.028 ns. "
    f"{15850 - r['SLICE']} of 15,850 slices remain. Maintainer decision: against the thirteenth record the route moved by "
    f"+{delta('route-1x1', 'LUT')} LUT (tolerance +500), +{delta('route-1x1', 'FF')} FF (+600) and {delta('route-1x1', 'SLICE')} slices (80), "
    f"with RAMB36, RAMB18 and DSP unchanged, WNS {delta('route-1x1', 'WNS_ns'):+.3f} ns and WHS {delta('route-1x1', 'WHS_ns'):+.3f} ns; "
    "the gate refused the LUT growth. " + TAIL,
    "ooc-1x1": HEAD + "; the shipping 20 ns clock. Against the thirteenth record the wrapper moved by "
    f"+{delta('ooc-1x1', 'LUT')} LUT and +{delta('ooc-1x1', 'FF')} FF (tolerances 250 and 250), RAMB36, RAMB18 and DSP unchanged; "
    "the gate passed it, and it is re-recorded with the route so that the record holds one processor pin. " + TAIL,
    "ooc-8x8": HEAD + "; out of context only, not routed; an RTL elaboration supplies the bound parameters; the shipping 20 ns clock. "
    f"Against the thirteenth record the wrapper moved by +{delta('ooc-8x8', 'LUT')} LUT and +{delta('ooc-8x8', 'FF')} FF "
    "(tolerances 316 and 339), RAMB36, RAMB18 and DSP unchanged; the gate passed it, and it is re-recorded with the route "
    "so that the record holds one processor pin. " + TAIL,
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
