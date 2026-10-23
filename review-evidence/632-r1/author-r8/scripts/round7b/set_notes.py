#!/usr/bin/env python3
"""Round 7b: write the three endpoints' `measured` notes after record --write.
record --write replaces only each endpoint's `record`; the note is the
endpoint's provenance text, edited here through the same json.dumps(indent=1)
the gate writes, so the file's layout is the gate's own.
usage: set_notes.py <baseline.json>
"""
import json, sys
from pathlib import Path

p = Path(sys.argv[1])
d = json.loads(p.read_text())
B = "https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6309313685"
E = "https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6357449062"
head = ("2026-10-23, issues #632 and #764 (PR #770): RTL inputs at lane head 5282b8b68983b3b5f7d9be4635c8847dbe6c38a1, "
        "the lane's merge of dev e5b480a385841f19420570bbba7c46da101d1303 (merge commit "
        "dc9cda7dfcb4be6e58f11d9c6d1594d81b44c0a6) plus documentation, with processor "
        "93fb0b2d736b36588ea7321e25fba2f8819ea41f and FPGA-gPTP 55680bff3b287b9a7b0c759f51471fa617c17335; "
        "the input digest reproduces at dc9cda7d. ")
pre = ("The preceding #771 record at 8de4b80ba84967e04da38e0eaed68c0b6b5256e0 measures dev e5b480a3's design "
       "(their synthesis inputs differ only in comment lines). ")
tail = ("Every tolerance, floor and ceiling unchanged. docs/findings/234_PP_SHADOW_AREA_BASELINE.md retains the "
        "earlier records and this delta.")
notes = {
    "route-1x1": head + "Explicit synth.maxThreads 1, general.maxThreads 32, synthesis and implementation in one "
    "process. " + pre + "Owner exceptions: against it the route moved by +500 LUT (tolerance +500), +376 FF "
    "(+600), +107 slices (tolerance +80) and +2 RAMB18 (tolerance 0), with DSP -1 and WNS -0.055 ns. The owner "
    f"chose block RAM for the render queue in {B} and accepted this change's LUT, FF and slice growth for now, "
    f"with Mark II (#640) to recover the area, in {E} (2026-10-23); 15 of 15,850 slices remain, so the next "
    "growth needs its own owner decision. Every other figure passed. " + tail,
    "ooc-1x1": head + "Explicit synth.maxThreads 1, general.maxThreads 32; the shipping 20 ns clock. " + pre +
    "Every figure equals it; the input digest moves because the standalone script reads the shipping export's "
    "whole source list, which carries this change's datapath sources, while the wrapper's own sources are "
    f"unchanged. Recorded with the route under the same two owner exceptions, {B} and {E}. " + tail,
    "ooc-8x8": head + "Explicit synth.maxThreads 1, general.maxThreads 32; an RTL elaboration supplies the bound "
    "parameters; the shipping 20 ns clock. " + pre + "Every figure equals it; the input digest moves because the "
    "standalone script reads the shipping export's whole source list, which carries this change's datapath "
    "sources, while the wrapper's own sources are unchanged. Recorded with the route under the same two owner "
    f"exceptions, {B} and {E}. " + tail,
}
for e, text in notes.items():
    assert text.isascii()
    d["endpoints"][e]["measured"] = text
p.write_text(json.dumps(d, indent=1) + "\n")
print("notes written")
