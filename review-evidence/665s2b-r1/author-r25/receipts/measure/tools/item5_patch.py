"""Item 5 of the round 25 ruling (#665 issuecomment-6751196896): the 8x8/2if answering-every-port arm's rom margin
in the ledger (SPLIT_CONTROL_MEMORY.md section 5). usage: python3 -I item5_patch.py LANE"""
import sys
from pathlib import Path

p = Path(sys.argv[1]) / 'docs/design/SPLIT_CONTROL_MEMORY.md'
t = p.read_text()
anchor = "The figures by part below are `b8628704`'s.\n"
assert t.count(anchor) == 1
note = (
    "The CPU budget harness's 8x8/2if `answering-every-port` arm, the size fixture with a test port that answers every "
    "notice ([section 13](#the-polls-by-source)), is the image nearest its ledger: its build is refused once its `rom` "
    "passes 122,880 B, the granule past which the plan would take 58.0 tiles against the 57.5 ledgered "
    "([section 3](#3-named-refusals)) (#665, the "
    "[round 25 ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6751196896), item 5).\n"
    "\n"
    "| Image | Arm's `rom`, B | Margin to the granule, B |\n"
    "|---|---:|---:|\n"
    "| `a30c9986` (the merge of `dev-soft-core` `1d6bf555`, the arm's readers sharing its path reader) | 122,868 | 12 |\n"
    "| This head (SRP's retry bounded by its source, `struct srp_mbx`'s two frame buffers last) | 122,556 | 324 |\n"
    "| This head with tsn-c-stack #32 at the pin (a scratch build) | 123,012 | 132 over |\n"
    "\n"
    "The retry's rule added about 104 B of code, and with the two 1.5 KB buffers last every other field of the adapter "
    "is within a load's reach of its address, which takes 348 B of address arithmetic off `srp_mbx.o` (11,916 to "
    "11,568 B of `.text`). The other arms at this head: `answering-later` 122,400 B, `answering-ports` 122,416 B, arm A "
    "122,248 B. tsn-c-stack #32 grows the core's `acmp.o` from 12,748 to 13,300 B of `.text`, so the pin move that "
    "carries it owes this arm 132 B of `rom`, or its next granule.\n"
    "\n")
t = t.replace(anchor, note + anchor)
p.write_text(t)
print('item 5 applied')
