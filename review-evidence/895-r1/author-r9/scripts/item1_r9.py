#!/usr/bin/env python3
"""item1_r9.py TREE: round 9's item 1 in TREE (#895's ruling of 2026-11-15 on round 8's stop): CTRL_LOOP_TX_MS at two
interfaces 99 -> 105 ms, the built design's tx row there, 104.25 ms, rounded up, so SRP_REDECLARE_CS at two
interfaces moves from 2,029 to 2,030 cs; the two self-test controls that plant the figure under its row; the test's
comment; FR_NFR 3.4.1, section 13, the SRP README and the harness README. Each replacement asserted unique."""
import sys
from pathlib import Path

tree = Path(sys.argv[1])
R9 = 'https://github.com/kebag-logic/milan-fpga/issues/895#issuecomment-6895331865'
A = '#the-transmits-figure-at-two-interfaces-895'


def edit(path, pairs):
    p = tree / path
    t = p.read_text()
    for old, new in pairs:
        assert t.count(old) == 1, (path, old[:90])
        t = t.replace(old, new)
    p.write_text(t)


edit('sw/firmware/ctrl/loop/ctrl_loop.h', [(
    "// THE TRANSMIT's MRPDU by every source at the built design, in ms rounded up\n"
    "// (tb/verilator/ctrl_service_budget/rows_tiers.py, the tx row, which refuses a\n"
    "// tree whose row passes this). At 8x8/2if, whose rows by every source are\n"
    "// reported and not held (#894, the owner's decision of 2026-11-12, owed to\n"
    "// #872), it is over the bound, and ctrl_loop.c holds 1x1/1if alone to it.\n"
    "#define CTRL_LOOP_TX_MS (MBX_N_IF == 1u ? 34u : 99u)\n",
    "// THE TRANSMIT's MRPDU by every source at the built design, in ms rounded up\n"
    "// (tb/verilator/ctrl_service_budget/rows_tiers.py, the tx row, which refuses a\n"
    "// tree whose row passes this). A withdrawn Talker's hold-off adds it\n"
    "// (srp_mbx.c, SRP_REDECLARE_CS), so the hold-off follows the row: 105 ms at\n"
    "// 8x8/2if for its 104.25 there (#895's ruling of 2026-11-15 on that figure,\n"
    "// item 1). At 8x8/2if, whose rows by every source are\n"
    "// reported and not held (#894, the owner's decision of 2026-11-12, owed to\n"
    "// #872), it is over the bound, and ctrl_loop.c holds 1x1/1if alone to it.\n"
    "#define CTRL_LOOP_TX_MS (MBX_N_IF == 1u ? 34u : 105u)\n")])

edit('sw/firmware/ctrl/test/srp_talker.cpp', [(
    "(ctrl_loop.h, CTRL_LOOP_JOIN_CS and CTRL_LOOP_TX_MS): 20,230 ms at one interface, 20,290 at two.",
    "(ctrl_loop.h, CTRL_LOOP_JOIN_CS and CTRL_LOOP_TX_MS): 20,230 ms at one interface, 20,300 at two.")])

edit('tb/verilator/ctrl_service_budget/flip_grade.py', [
    ("    figure = '#define CTRL_LOOP_TX_MS (MBX_N_IF == 1u ? 34u : 99u)'\n",
     "    figure = '#define CTRL_LOOP_TX_MS (MBX_N_IF == 1u ? 34u : 105u)'\n"),
    ("    for leg, point, said in (('33u : 99u', '1x1/1if', 33), ('34u : 98u', '8x8/2if', 98)):\n"
     "        under = {loop: text.replace(figure, figure.replace('34u : 99u', leg))}\n",
     "    for leg, point, said in (('33u : 105u', '1x1/1if', 33), ('34u : 104u', '8x8/2if', 104)):\n"
     "        under = {loop: text.replace(figure, figure.replace('34u : 105u', leg))}\n")])

edit('tb/verilator/ctrl_service_budget/rows_tiers.py', [
    ("    figure = '#define CTRL_LOOP_TX_MS (MBX_N_IF == 1u ? 34u : 99u)'\n",
     "    figure = '#define CTRL_LOOP_TX_MS (MBX_N_IF == 1u ? 34u : 105u)'\n"),
    ("    under = {loop: header.replace(figure, '#define CTRL_LOOP_TX_MS (MBX_N_IF == 1u ? 33u : 98u)')}\n",
     "    under = {loop: header.replace(figure, '#define CTRL_LOOP_TX_MS (MBX_N_IF == 1u ? 33u : 104u)')}\n")])

edit('tb/verilator/ctrl_service_budget/README.md', [(
    "(`tx_statements`; 34 ms at 1x1/1if and 99 at 8x8/2if, whose rows are reported).",
    "(`tx_statements`; 34 ms at 1x1/1if and 105 at 8x8/2if, whose rows are reported, for its tx row's 104.25; 99 "
    "before SRP's Talker declarations' costs were restated there, #895).")])

edit('sw/firmware/ctrl/srp/README.md', [(
    "declares at once, while a changed destination waits `SRP_REDECLARE_CS` after\n"
    "the Leave's request (two LeaveAllTime periods, Table 10-7, with a JoinTime and\n"
    "THE TRANSMIT's bound); a destination that changes while valid withdraws the old\n"
    "one first.",
    "declares at once, while a changed destination waits `SRP_REDECLARE_CS` after\n"
    "the Leave's request (two LeaveAllTime periods, Table 10-7, with a JoinTime and\n"
    "THE TRANSMIT's MRPDU by every source, `CTRL_LOOP_TX_MS`, the latest the Leave\n"
    "departs: 2,023 cs at one interface and 2,030 at two, where the figure is 105 ms\n"
    "for the tx row's 104.25, [#895's ruling of 2026-11-15 on that figure](" + R9 + "),\n"
    "items 1 and 2; 35.2.2.8 sets only the least, 2,000 cs); a destination that\n"
    "changes while valid withdraws the old one first.")])

edit('docs/reference/FR_NFR.md', [(
    "and `CTRL_LOOP_TX_MS`, that row rounded up to 34 ms, held to it at compile time in `ctrl_loop.c`.",
    "and `CTRL_LOOP_TX_MS`, that row rounded up to 34 ms, held to it at compile time in `ctrl_loop.c`. At 8x8/2if, "
    "whose rows are reported, `CTRL_LOOP_TX_MS` is 105 ms, its tx row's 104.25 with SRP's Talker declarations' costs "
    "restated there rounded up, and a withdrawn Talker's hold-off, `SRP_REDECLARE_CS`, which adds it to two "
    "LeaveAllTime periods and a JoinTime, follows it: 2,030 cs at two interfaces (2,029 at 99 ms) and 2,023 at one. "
    "IEEE 802.1Q-2018 35.2.2.8 sets only the least, 2,000 cs, and the terms above it cover the Leave's latest "
    "departure, so a changed destination is declared 10 ms later at two interfaces, on the safe side "
    "([#895's ruling of 2026-11-15 on that figure](" + R9 + "), items 1 to 3; #894's head keeps 99).")])

section = (
    "\n### THE TRANSMIT's figure at two interfaces (#895)\n\n"
    f"[#895's ruling of 2026-11-15 on round 8's stop]({R9}) takes the rule's figure at 8x8/2if:\n\n"
    "- **The figure** (item 1). `CTRL_LOOP_TX_MS` at two interfaces is the built design's tx row by every source "
    "rounded up to the ms, 105 ms for its 104.25 at the restated costs ([above](#the-bound-and-the-slice-at-140-ms-895)), "
    "so `rows_tiers.tx_statements` holds both interface counts' figures at or over their rows. #894's head keeps 99.\n"
    "- **The hold-off follows it** (items 1 and 2). `SRP_REDECLARE_CS` (`srp_mbx.c`) is two LeaveAllTime periods, a "
    "JoinTime and (`CTRL_LOOP_TX_MS` + 9) / 10, the latest the Leave departs after its request: 2,030 cs at two "
    "interfaces, 2,029 at 99 ms, and 2,023 at one, unchanged. IEEE 802.1Q-2018 35.2.2.8 sets only the least, 2,000 "
    "cs, so the terms above it must follow the tx row, and a withdrawn Talker's changed destination is declared 10 ms "
    "later at two interfaces, on the safe side.\n"
    "- **Refused** (item 3): a statement under its row, and a second source for the hold-off's term.\n"
)
edit('docs/design/SPLIT_CONTROL_MEMORY.md', [
    ("by every source 34.00 ms at 1x1/1if at the rule's 900 us slice and 104.25 ms at 8x8/2if, over the 99 stated "
     "there (the tx row of `rows_tiers.py`, at the head's costs, [below](#the-bound-and-the-slice-at-140-ms-895);",
     "by every source 34.00 ms at 1x1/1if at the rule's 900 us slice and 104.25 ms at 8x8/2if (the tx row of "
     "`rows_tiers.py`, at the head's costs, [below](#the-bound-and-the-slice-at-140-ms-895);"),
    ("which `CTRL_LOOP_TX_MS` states as 34 and 99 ms (30 at 1x1/1if before SRP's Talker declarations' merge with THE "
     "TIERS and #894's round 11; 99 at two interfaces since #894's tx row there reached 98.49 ms,",
     "which `CTRL_LOOP_TX_MS` states as 34 and 105 ms (30 at 1x1/1if before SRP's Talker declarations' merge with THE "
     "TIERS and #894's round 11; 99 at two interfaces since #894's tx row there reached 98.49 ms, and 105 since this "
     f"branch's reached 104.25, [below]({A});"),
    ("- **THE TRANSMIT's figure at 8x8/2if.** With 8x8/2if's costs restated, its tx row is 104.25 ms, over the 99 "
     "`CTRL_LOOP_TX_MS` states there,",
     "- **THE TRANSMIT's figure at 8x8/2if.** With 8x8/2if's costs restated, its tx row is 104.25 ms, over the 99 "
     "`CTRL_LOOP_TX_MS` stated there then,"),
    ("So the figure is not restated here, and it is the maintainer's under [the ruling]"
     "(https://github.com/kebag-logic/milan-fpga/issues/895#issuecomment-6892130675).",
     "So the figure was not restated in that round; it was the maintainer's under [the ruling]"
     f"(https://github.com/kebag-logic/milan-fpga/issues/895#issuecomment-6892130675), and is 105 ms by the next "
     f"([below]({A}))."),
    ("8x8/2if's THE TRANSMIT figure waits for the maintainer. 8x8/2if is reported:",
     f"8x8/2if's THE TRANSMIT figure waited for the maintainer, and is 105 ms ([below]({A})). 8x8/2if is reported:"),
])
p = tree / 'docs/design/SPLIT_CONTROL_MEMORY.md'
t = p.read_text()
anchor = "tx 104.25, txL 466.85, and the load 0.798 at the pin and 0.756 with tsn-c-stack #32.\n"
assert t.count(anchor) == 1
p.write_text(t.replace(anchor, anchor + section))
print('ok')
