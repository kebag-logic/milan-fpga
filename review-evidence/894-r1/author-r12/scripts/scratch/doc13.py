from pathlib import Path
import sys
p=Path('docs/design/SPLIT_CONTROL_MEMORY.md'); t=p.read_text()
def sub(old,new):
    global t
    assert t.count(old)==1,(t.count(old),old[:80]); t=t.replace(old,new)
old="""| The one-row edit's record cut, the edits a class of their own, a TICK at 50 us and ACMP's owed frame at 55: an 8 ms pace ([below](#the-one-row-edit)) | 12.93 | 188.41, within 238 | 28.64 | 27.01 | 27.13 | 14.56 | 73.39 | 69.24 | 127.22, within 130, **over 125** | 33.01, within 49 | 48.23, within 49, **over 40** |"""
sub(old, old+"""
| SET_CONFIGURATION's record cut and paced, the paced class at 300 us: an 8 ms pace ([below](#set_configurations-record)) | 13.01 | 188.41, within 238 | 28.80 | 27.17 | 27.29 | 14.59 | 73.80 | 69.60 | 127.86, within 130, **over 125** | 33.21, within 49 | 48.23, within 49, **over 40** |""")
sub("""| 1x1/1if | 900 us | 12.93 | 73.39 | 69.24 | 14.56 | 127.22, within 130 (over 125) |
| 8x8/2if | 1,300 us | 42.62 | 194.54 | 179.22 | 20.38 | 665.47 |""",
"""| 1x1/1if | 900 us | 13.01 | 73.80 | 69.60 | 14.59 | 127.86, within 130 (over 125) |
| 8x8/2if | 1,300 us | 44.24 | 206.45 | 196.31 | 20.93 | 806.60 |""")
old=t[t.index("- **Not the formal measurement.** In the answering-ports arm, labelled"):]
old=old[:old.index("\n- **The images.**")]
sub(old, """- **Not the formal measurement.** In the answering-ports arm, labelled and never the formal measurement but for its `aecp` group and the edits ([the harness](../../tb/verilator/ctrl_service_budget/README.md)), `aecp-fanout`'s SET_CONFIGURATION, which arm A's fixture refuses, was 33,724 cycles at 1x1/1if under the cut (355 us by the rule; 33,692 at `7398ec0a`, 33,533 at `12180198`) and 78,332 on the 8x8 shape (825 us); no stated cost covered it, and [SET_CONFIGURATION's record](#set_configurations-record) below is its cut.""")
old=t[t.index("- **The images.** The cut adds 220 B of rom to every image"):]
old=old[:old.index("\n")]
sub(old, """- **The images.** The cut added code to every image, its rom by alignment 224 B in each 1x1 image (the 1x1/1if size fixture 110,576 to 110,800 B, taking its next granule, 41.0 RAMB36, within 56) and 208 B in each 8x8 image (the 8x8/2if platform 130,496 to 130,704 B of 131,072, 60.0 RAMB36; the 8x8/1if platform at 56.0). Sram is unchanged.

### SET_CONFIGURATION's record
""" + Path(sys.argv[1]).read_text().rstrip('\n'))
sub("- **The margins at this head** (round 30's legs,", "- **The margins in round 30's measurements** (round 30's legs,")
sub("with arm A's least margin at this head an AECP record's, by round 30's legs", "with arm A's least margin an AECP record's, by round 30's legs")
sub("under the tiers every 1x1/1if row holds by every source, R4 12.85 ms ([THE TIERS](#the-tiers))", "under the tiers every 1x1/1if row holds by every source, R4 13.01 ms ([THE TIERS](#the-tiers))")
p.write_text(t)
print('ok')
