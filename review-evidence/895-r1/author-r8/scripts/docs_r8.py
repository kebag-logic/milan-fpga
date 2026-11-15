#!/usr/bin/env python3
"""docs_r8.py TREE FIG.json: round 8's documentation at the head, the figures from FIG.json (the 8x8/2if rows and load
after its survey; the 1x1/1if figures are the head's, measured). Edits section 13 of SPLIT_CONTROL_MEMORY.md, FR_NFR
3.4.1 and the SRP README in TREE, each replacement asserted unique."""
import json
import sys
from pathlib import Path

tree, fig = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text())
R8 = 'https://github.com/kebag-logic/milan-fpga/issues/895#issuecomment-6892130675'
A = '#the-bound-and-the-slice-at-140-ms-895'


def edit(path, pairs):
    p = tree / path
    t = p.read_text()
    for old, new in pairs:
        assert t.count(old) == 1, (path, old[:90])
        t = t.replace(old, new)
    p.write_text(t)


e = fig['8x8']
section = ("\n### The bound and the slice at 140 ms (#895)\n\n"
 f"[#895's ruling of 2026-11-15 on round 7B's stop]({R8}) moves the last queued notice's bound to its row in #895 alone, and lets the slice rule choose again there:\n\n"
 "- **The bound** (item 1). `queued_bound.py` rules the built design's row rounded up to the next 5 ms, never over 140 ms. The row was 135.43 ms at 950 us, 10.43 over decision D's 125, 5.43 over #894's amended 130 and 4.57 within 140, so `AECP_QUEUED_MS` at one interface is 140 ms (`aecp_mbx.h`). #894's head keeps 130, and #908 stays open.\n"
 "- **The slice** (item 4). At the 140 ms bound the slice rule takes 900 us (least margin +0.0086, txL binding; 950 us +0.0076, 1,000 us +0.0065), and `rows_tiers.ruled` agrees. The loop is built there (`CTRL_LOOP_SLICE_US`), and at 900 us the row is 136.65 ms, which rules the same 140. A 900 us slice holds one MRPDU's build, as 950 did.\n"
 f"- **THE TRANSMIT's figure** (item 3). By the rule `CTRL_LOOP_TX_MS` is the built design's tx row rounded up to the ms: 34.00 ms at 1x1/1if at 900 us, so it stays 34 (the 35 of 950 us is not taken), and `SRP_REDECLARE_CS` stays 2,023 cs at one interface. At 8x8/2if see below.\n"
 "- **The sync.** The merge of #902's `b6f5c638` changes no image of this branch: every image `ledger.sh` links has its loadable bytes and objects identical to those at round 7B's cut head, 552 of 552 by sha256, and #894 shows its own images identical to `234bc149`'s. The bound and the slice change only the one-interface images, in `ctrl_loop.o` and the ELF. Every two-interface image is identical.\n"
 "- **Measured again on the rebuilt image,** every group of arm A, the `answering-every-port` and `valid-destinations` arms and arm B's three groups at 1x1/1if, and the same at 8x8/2if.\n"
 "  - At 1x1/1if every cost equals its measurement on the cut's image but for event counts. The polls' base is 21,094 cycles in `save-held`, 225 us, and a pass's events' fixed part 2,715 cycles, within its 35. No stated cost is under its rule figure, so the bound and the slice settle after the one rebuild.\n"
 f"  - At 8x8/2if, reported: {e['survey']}\n"
 "- **The rows** (`flip_grade.py --check --point 1x1/1if`, by every source, ms, with each margin): R4 13.25 (6.75), R5 75.84 (14.16), R6 73.36 (16.64), the first queued notice 14.72 (5.28), the last 136.65 (3.35 of 140), R4L 203.57 (34.43), ACMP 29.63 (0.37), ADP 27.86 (2.14), MAAP 27.96 (2.04), tx 34.00 (15.00) and txL 48.58 (0.42). Every row holds by every source.\n"
 "  - `tier_grid.py` holds 6 of its 420 designs and chooses the built one. The pace by #894's rule is 9 ms (txL 49.99 at 8).\n"
 "  - The load is 0.517 at the pin and 0.514 with tsn-c-stack #32, and 0.696 with every command the largest legal one.\n"
 "  - Every join interval is within 181 to 239 ms: 359 at 1x1/1if, 188.102 to 190.121 ms.\n"
 "- **The 140 ms limit.** A pass's own cost at 1x1/1if, a pass's events' fixed part and its polls' base, is 260 us. The last queued notice holds 140 ms up to 278 us, and at 279 us it is 141.36 ms and txL 49.02 ms, each over its bound (`per_pass_threshold.py` in the round's receipts). The placement that moves the base by a thousand cycles a group is #909's.\n"
 "- **The ROM** is round 7B's cut head's to the byte in size: the platform's 8x8/2if image at 60.5 RAMB36 with 1,368 B left, the size fixture and the harness's two 8x8/2if arms at 59.0 with 368, 60 and 200 B, every other point within 56.\n\n"
 f"- **THE TRANSMIT's figure at 8x8/2if.** With 8x8/2if's costs restated, its tx row is {e['tx']} ms, over the 99 `CTRL_LOOP_TX_MS` states there, and `rows_tiers.tx_statements` holds each interface count's figure at or over its row. By the rule the figure would be {e['txrule']} ms, and `SRP_REDECLARE_CS` at two interfaces, two LeaveAllTime periods, a JoinTime and (`CTRL_LOOP_TX_MS` + 9) / 10, would move from 2,029 to {e['redeclare']} cs: a withdrawn Talker's changed destination declared {e['delta_ms']} ms later at 8x8/2if, a wire-visible change. So the figure is not restated here, and it is the maintainer's under [the ruling]({R8}).\n\n"
 f"So at this head every 1x1/1if row holds by every source at the built slice, the slice rule's 900 us, with the last queued notice's bound at its row's 140 ms; the load is within 0.70 in both columns, and each image is within its entry. 8x8/2if's THE TRANSMIT figure waits for the maintainer. 8x8/2if is reported: R4 {e['R4']} ms, R4L {e['R4L']}, tx {e['tx']}, txL {e['txL']}, and the load {e['load']} at the pin and {e['load32']} with tsn-c-stack #32.\n")
old_close = "for the maintainer. The 8x8/2if legs were not run on the cut's image, so its rows are the composed tables' and reported: R4 44.55 ms, R4L 210.93, and the load 0.798 at the pin and 0.756 with tsn-c-stack #32.\n"
new_close = ("for the maintainer, which [#895's ruling of 2026-11-15 on that stop](" + R8 + ") answers ([below](" + A + ")). The 8x8/2if legs were not run on the cut's image, so its rows were the composed tables' then.\n" + section)
edit('docs/design/SPLIT_CONTROL_MEMORY.md', [
 ("So after the ruling's one cut no slice within 650 to 1,100 us holds every 1x1/1if row: the stop of", "So after the ruling's one cut no slice within 650 to 1,100 us held every 1x1/1if row at the 130 ms bound: the stop of"),
 (old_close, new_close),
 ("| 1x1/1if | 950 us | 13.30 | 75.89 | 73.41 | 14.77 | **135.43, over 130** ([below](#the-composition-with-894s-set_configuration-cut-895)) |",
  "| 1x1/1if | 900 us | 13.25 | 75.84 | 73.36 | 14.72 | 136.65, within 140 (over 125; [below](" + A + ")) |"),
 ("| 8x8/2if | 1,300 us | 44.55 | 207.11 | 196.61 | 21.04 | 797.94 |",
  f"| 8x8/2if | 1,300 us | {e['R4']} | {e['R5']} | {e['R6']} | {e['first']} | {e['last']} |"),
 ("| 34.05, within 49 | 48.63, within 49, **over 40** |\n",
  "| 34.05, within 49 | 48.63, within 49, **over 40** |\n| The last queued notice's bound at its row's 140 ms and the slice rule's 900 us: the 9 ms pace ([below](" + A + ")) | 13.25 | 203.57, within 238 | 29.63 | 27.86 | 27.96 | 14.72 | 75.84 | 73.36 | 136.65, within 140, **over 125** | 34.00, within 49 | 48.58, within 49, **over 40** |\n"),
 ("by every source 33.69 ms at 1x1/1if at the rule's 950 us slice and 94.99 ms at 8x8/2if (the tx row of `rows_tiers.py`, at the costs of SRP's Talker declarations composed with #894's round 11 and measured again on the image with that slice, [below](#the-rules-slice-built-895);",
  f"by every source 34.00 ms at 1x1/1if at the rule's 900 us slice and {e['tx']} ms at 8x8/2if, over the 99 stated there (the tx row of `rows_tiers.py`, at the head's costs, [below](" + A + "); 34.05 at 950 us after the one cut, 33.69 at the rule's 950 us before #894's SET_CONFIGURATION cut and 94.99 at 8x8/2if then, [above](#the-rules-slice-built-895);"),
 ("under the tiers, composed with #894's SET_CONFIGURATION cut and measured again after the one cut, R4 by every source is 13.30 ms at 1x1/1if and every 1x1/1if row holds but the last queued notice, 135.43 ms at 950 us, over its 130 at every slice from 650 to 1,100 us ([THE TIERS](#the-tiers), [that composition](#the-composition-with-894s-set_configuration-cut-895));",
  "under the tiers every 1x1/1if row holds by every source at the slice rule's 900 us, the last queued notice's bound at its row's 140 ms, R4 13.25 ms ([THE TIERS](#the-tiers), [the bound and the slice](" + A + "));"),
])
edit('docs/reference/FR_NFR.md', [
 ("the last queued notice 135.43 ms at 950 us, over its 130 at every slice from 650 to 1,100 us, the ruling's stop, for the maintainer (#895).",
  "the last queued notice 135.43 ms at 950 us, over its 130 at every slice from 650 to 1,100 us, the ruling's stop. By [#895's ruling of 2026-11-15 on that stop](" + R8 + ") the bound follows the row to 140 ms and the slice rule takes 900 us there, where 9 ms holds txL, 48.58 ms, and R4L, 203.57, and every 1x1/1if row holds by every source, the last queued notice 136.65 ms (#895)."),
 ("So by [#895's ruling of 2026-11-15 on that composition](" + R8 + "), item 1, the bound follows its row in #895 alone, 140 ms at one interface, and #894's head keeps 130.",
  "So by [#895's ruling of 2026-11-15 on that composition](" + R8 + "), item 1, the bound follows its row in #895 alone, 140 ms at one interface, and #894's head keeps 130; at the slice rule's 900 us there the row is 136.65 ms, which rules the same 140."),
 ("(33.69 ms with SRP's Talker declarations composed with #894's round 11 and measured again, at the slice rule's 950 us,",
  "(34.00 ms with SRP's Talker declarations composed with #894's SET_CONFIGURATION cut and measured again, at the slice rule's 900 us,"),
])
edit('sw/firmware/ctrl/srp/README.md', [
 ("By every source it is 34.05 ms there at 950 us at the Talker declarations' costs composed with #894's SET_CONFIGURATION cut and measured again, over the 34 ms `CTRL_LOOP_TX_MS` states, which waits with the slice for the maintainer's decision (33.88 at the composed tables,",
  "By every source it is 34.00 ms there at the slice rule's 900 us, the last queued notice's bound at 140 ms, at the Talker declarations' costs composed with #894's SET_CONFIGURATION cut and measured again, which `CTRL_LOOP_TX_MS` states as 34 ms (34.05 at 950 us after the one cut, 33.88 at the composed tables,"),
])
print('ok')
