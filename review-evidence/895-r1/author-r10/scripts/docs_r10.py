#!/usr/bin/env python3
"""docs_r10.py TREE: round 10's documentation pass (lane 895): R836-4-F1 and R835-4-F2, every superseded figure the
inventory found stated as this head's, each either restated as this head's or given its historical subject (#894's
head, or the round of this branch that measured it), and section 5's and 13's provenance; R835-4-S1 and S2. Markdown
only. Each replacement asserted unique."""
import sys
from pathlib import Path

tree = Path(sys.argv[1])
R9 = 'https://github.com/kebag-logic/milan-fpga/issues/895#issuecomment-6895331865'
B = '#the-bound-and-the-slice-at-140-ms-895'
X = '#the-transmits-figure-at-two-interfaces-895'


def edit(path, pairs):
    p = tree / path
    t = p.read_text()
    for old, new in pairs:
        assert t.count(old) == 1, (path, t.count(old), old[:100])
        t = t.replace(old, new)
    p.write_text(t)


SCM = 'docs/design/SPLIT_CONTROL_MEMORY.md'
final_table = (
    "\n**At this head** (its images identical by sha256 to round 9's `449d29d2`, [section 13](" + X + ")), planned the "
    "same way (`ledger.sh` on a clean clone; `plat_ledger.py` passes at every point):\n\n"
    "| Point | Fixture `rom` / `sram` need, B | Fixture RAMB36 | Platform `rom` / `sram` need, B | Platform RAMB36 | "
    "Platform `ctrl_plat`, B |\n"
    "|---|---:|---:|---:|---:|---:|\n"
    "| 1x1, one interface (shipping) | 112,424 / 55,200 | 41.0 | 117,488 / 56,224 | 43.0 | 17,536 |\n"
    "| 1x1, two interfaces | 113,984 / 57,376 | 42.5 | 119,072 / 58,400 | 44.0 | 19,072 |\n"
    "| 8x8, one interface | 125,088 / 96,304 | 55.0 | 130,200 / 97,328 | 56.0, accepted | 18,240 |\n"
    "| 8x8, two interfaces (largest) | 126,608 / 113,248 | 59.0, its ledger's | 131,752 / 114,224 | 60.5, its "
    "ledger's cap | 20,352 |\n\n"
    "The platform's 8x8 image with two interfaces holds 131,752 B of `rom` in 133,120, 1,368 B left at 60.5 RAMB36, "
    "its debt of 4.5 RAMB36 owed to S14. The size fixture's 8x8 image with two interfaces holds 126,608 B in 126,976 "
    "(368 B to spare), the harness's `answering-every-port` arm 126,916 B (60 B) and its `valid-destinations` arm "
    "126,776 B (200 B), each 59.0. The platform's 8x8 one-interface image holds 130,200 B in 131,072 at 56.0 (872 B), "
    "its `ctrl_plat` 18,240 B since the gate's kept gate and base (#895's one cut). Every other point of both images "
    "is within 56.\n")
edit(SCM, [
    # section 5: #894's tables and sentences name #894's head
    ("Its size at each point was measured in the composed build by `ctrl_plat_image.py` at that merge: 17,472, 19,008, "
     "18,112 and 20,288 B (`ctrl_memory_ledger.py`; 17,536, 19,008, 18,176 and 20,288 B at the head, below).",
     "Its size at each point was measured in the composed build by `ctrl_plat_image.py` at that merge: 17,472, 19,008, "
     "18,112 and 20,288 B (`ctrl_memory_ledger.py`; 17,536, 19,008, 18,176 and 20,288 B at #894's head `07ed787e`, "
     "below, and 17,536, 19,072, 18,240 and 20,352 B at this branch's, at this section's end)."),
    ("**With the control loop's tiers** (#894; the [ruling of 2026-11-13]",
     "**With the control loop's tiers** (#894, at #894's head `07ed787e`, which #902 merged into `dev-soft-core`; "
     "this branch's head is planned at this section's end; the [ruling of 2026-11-13]"),
    ("| Point | Fixture `rom` / `sram` need, B, at the head (the ruling's head) | Fixture RAMB36 | Platform `rom` / `sram` "
     "need, B, at the head (the ruling's head) |",
     "| Point | Fixture `rom` / `sram` need, B, at #894's head (the ruling's head) | Fixture RAMB36 | Platform `rom` / "
     "`sram` need, B, at #894's head (the ruling's head) |"),
    ("The size fixture's 8x8 image with two interfaces holds 125,792 B of `rom` in 126,976 at the head (125,200 at the "
     "ruling's head)",
     "The size fixture's 8x8 image with two interfaces holds 125,792 B of `rom` in 126,976 at #894's head (125,200 at "
     "the ruling's head)"),
    ("The platform's image there holds 130,920 B of `rom` in 131,072 at the head, 152 B before",
     "The platform's image there holds 130,920 B of `rom` in 131,072 at #894's head, 152 B before"),
    ("`ctrl_plat` is 17,536, 19,008, 18,176 and 20,288 B at the four points (`ctrl_memory_ledger.py`).",
     "`ctrl_plat` is 17,536, 19,008, 18,176 and 20,288 B at the four points on #894's head (`ctrl_memory_ledger.py` "
     "records this branch's, 17,536, 19,072, 18,240 and 20,352 B)."),
    # section 5: this branch's earlier heads
    ("**At this branch's head, #895 on #810's head `084cf7a8`**, planned the same way",
     "**At this branch's `9e30c2c3`, #895 on #810's head `084cf7a8`**, planned the same way"),
    ("The size fixture's 8x8 image with two interfaces holds 124,568 B of `rom` in 124,928, 360 B to spare, within the "
     "58.5 its entry ledgers;",
     "The size fixture's 8x8 image with two interfaces held 124,568 B of `rom` in 124,928 there, 360 B to spare, within "
     "the 58.5 its entry then ledgered;"),
    ("No entry or cap moves: every other point of both images is within 56, and the platform's largest plans 60.0 with "
     "1,344 B of `rom` to spare in 131,072.",
     "No entry or cap moved: every other point of both images was within 56, and the platform's largest planned 60.0 "
     "with 1,344 B of `rom` to spare in 131,072."),
    ("**At this branch's head, #895 on #894's round 11 `9606b3a9`**, planned the same way",
     "**At round 6's head `bf0844f1`, #895 on #894's round 11 `9606b3a9`**, planned the same way"),
    ("The platform's 8x8 image with two interfaces holds 131,464 B of `rom`, 392 B past the 131,072 that 60.0 holds, "
     "so its entry is 60.5, the cap of the owner's decision: 1,656 B of `rom` left,",
     "The platform's 8x8 image with two interfaces held 131,464 B of `rom` there, 392 B past the 131,072 that 60.0 "
     "holds, so its entry is 60.5, the cap of the owner's decision: 1,656 B of `rom` left then,"),
    ("The size fixture's 8x8 image with two interfaces holds 126,320 B in 126,976 (656 B to spare), the harness's "
     "`answering-every-port` arm 126,628 B (348 B) and its `valid-destinations` arm 126,488 B (488 B), each within the "
     "59.0 #894's entry carries; 58.5 is out of reach, #894's own fixture being 59.0. Every other point of both images "
     "is within 56, the platform's 8x8 one-interface image at 56.0 with 1,144 B of `rom` to spare.\n",
     "The size fixture's 8x8 image with two interfaces held 126,320 B in 126,976 there (656 B to spare), the harness's "
     "`answering-every-port` arm 126,628 B (348 B) and its `valid-destinations` arm 126,488 B (488 B), each within the "
     "59.0 #894's entry carries; 58.5 is out of reach, #894's own fixture being 59.0. Every other point of both images "
     "was within 56, the platform's 8x8 one-interface image at 56.0 with 1,144 B of `rom` to spare.\n" + final_table),
    # section 13's provenance
    ("## 13. The larger fetch L1 and the record mover\n\n",
     "## 13. The larger fetch L1 and the record mover\n\n"
     "This section composes two lanes' text. In #894's passages (PR #902, merged into `dev-soft-core` with "
     "`07ed787e`'s tree) \"the head\" is #894's head and its figures that image's; the subsections marked (#895) "
     "state this branch's at the round each names. This branch's head is [the bound and the slice at 140 ms](" + B + ") "
     "and [THE TRANSMIT's figure at two interfaces](" + X + "): its rows, statements and images are those.\n\n"),
    ("the first queued notice is a tier row, 14.66 ms within 20 at 1x1/1if and 20.93 ms at 8x8/2if, stated 22 and "
     "reported; SRP's R5 and R6 are tier rows held to decision D's 90 ms, 74.07 and 69.86 ms at 1x1/1if;",
     "the first queued notice is a tier row, 14.72 ms within 20 at 1x1/1if and 21.11 ms at 8x8/2if at this head, "
     "stated 22 and reported (14.66 and 20.93 at #894's head); SRP's R5 and R6 are tier rows held to decision D's 90 "
     "ms, 75.84 and 73.36 ms at 1x1/1if at this head (74.07 and 69.86 at #894's);"),
    ("(before THE TIERS; under them it is the tx row's statement, 34 and 99 ms at the head, [below](#the-tiers))",
     "(before THE TIERS; under them it is the tx row's statement, 34 and 105 ms at this head, [below](" + X + "); 34 "
     "and 99 at #894's head)"),
    ("Under THE TIERS the 8x8/2if first queued notice is a tier row, 20.93 ms by every source, stated 22 ms and "
     "reported (#890); the decision and its 185 us stand.",
     "Under THE TIERS the 8x8/2if first queued notice is a tier row, 21.11 ms by every source at this head (20.93 at "
     "#894's), stated 22 ms and reported (#890); the decision and its 185 us stand."),
    ("| the first notice of a queue, from its port's answer (`AECP_QUEUED_FIRST_MS`) | 14.66 ms by every source, held to "
     "20 (14.60 at `12180198`'s 1,200 us slice) | 20.93 ms by every source, stated 22 (20.25 at `12180198`) |",
     "| the first notice of a queue, from its port's answer (`AECP_QUEUED_FIRST_MS`) | 14.72 ms by every source at this "
     "head, held to 20 (14.66 at #894's head; 14.60 at `12180198`'s 1,200 us slice) | 21.11 ms by every source at this "
     "head, stated 22 (20.93 at #894's head; 20.25 at `12180198`) |"),
    ("| every notice queued behind it (`AECP_QUEUED_MS`) | 127.21 ms by every source, held to 130 (91.59, held to 125, "
     "at `12180198`'s 1,200 us slice) | 806.60 ms by every source, stated 62, ceiling 70 (647.23 at `12180198`) |",
     "| every notice queued behind it (`AECP_QUEUED_MS`) | 136.65 ms by every source at this head, held to 140 (127.21, "
     "held to 130, at #894's head; 91.59, held to 125, at `12180198`'s 1,200 us slice) | 857.77 ms by every source at "
     "this head, stated 62, ceiling 70 (806.60 at #894's head; 647.23 at `12180198`) |"),
    ("and the last's is [#894's amendment](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6862465874)"
     "'s 130 ms (`AECP_QUEUED_MS`; decision D's 125 before it);",
     "and the last's is 140 ms at this head (`AECP_QUEUED_MS`), the queued rule's figure for its row ([#895's ruling of "
     "2026-11-15 on round 7B's stop](https://github.com/kebag-logic/milan-fpga/issues/895#issuecomment-6892130675), "
     "item 1), [#894's amendment](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6862465874)'s 130 "
     "ms on #894's head and decision D's 125 before it;"),
    ("Under THE TIERS the built design's last queued notice at 1x1/1if is held to the amendment's 130 ms "
     "(`AECP_QUEUED_MS`, [above](#the-queued-notices-at-stated-costs-and-the-first-notice));",
     "Under THE TIERS the built design's last queued notice at 1x1/1if is held to 140 ms at this head (`AECP_QUEUED_MS`, "
     "[above](#the-queued-notices-at-stated-costs-and-the-first-notice); the amendment's 130 ms on #894's head);"),
    ("the slice rule's choice at one interface, 950 us, and 1,300 us at two;",
     "the slice rule's choice at one interface, 900 us at this head (950 us at #894's), and 1,300 us at two;"),
    ("A 950 us slice holds one MRPDU's build and not both (1,010 us, `CTRL_LOOP_BUILD_PASS_US`)",
     "A 900 us slice, as #894's 950 us, holds one MRPDU's build and not both (1,010 us, `CTRL_LOOP_BUILD_PASS_US`)"),
    ("then at the slice ruling's 800 us (950 us at the head, [below](#the-final-passs-restatements)):",
     "then at the slice ruling's 800 us (900 us at this head, [below](" + B + "); 950 us at #894's, "
     "[below](#the-final-passs-restatements)):"),
    ("| The slice rule's choice, 950 us ([below](#the-final-passs-restatements)): an 8 ms pace |",
     "| On #894's head: the slice rule's choice there, 950 us ([below](#the-final-passs-restatements)), an 8 ms pace |"),
    ("was 125,200 B of rom (125,792 B at the head), 59.0 RAMB36,",
     "was 125,200 B of rom (125,792 B at #894's head, 126,608 at this branch's, [section 5](#5-fit)), 59.0 "
     "RAMB36,"),
    ("At 1x1/1if the size fixture's image is 111,024 B of rom and 55,152 B of sram, 41.0 RAMB36, its 552 B slots "
     "included, since SET_CONFIGURATION's cut",
     "At 1x1/1if the size fixture's image is 111,024 B of rom and 55,152 B of sram on #894's head (112,424 and 55,200 "
     "at this branch's), 41.0 RAMB36, its 552 B slots included, since SET_CONFIGURATION's cut"),
    ("900 us at 1x1/1if (`CTRL_LOOP_SLICE_US`; 950 us since [#894's ruling of 2026-11-15]"
     "(https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6888782796)), txL binding.",
     "900 us at 1x1/1if (`CTRL_LOOP_SLICE_US`; 950 us on #894's head since [#894's ruling of 2026-11-15]"
     "(https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6888782796), and 900 at this branch's, "
     "[below](" + B + ")), txL binding."),
    ("The tx row then took a seventeenth pass, 33.01 ms within its 49 (33.38 ms at the head's 950 us slice), and "
     "`CTRL_LOOP_TX_MS`, THE TRANSMIT's stated figure, is 34 ms (`ctrl_loop.h`), a figure only a static assertion "
     "reads: every image is byte-identical to the one measured.",
     "The tx row then took a seventeenth pass, 33.01 ms within its 49 (33.38 ms at #894's head's 950 us slice, 34.00 "
     "at this branch's 900 us), and `CTRL_LOOP_TX_MS`, THE TRANSMIT's stated figure, was 34 ms (`ctrl_loop.h`), a "
     "figure only a static assertion read on #894's image, every image of which was byte-identical to the one measured. "
     "In this branch a withdrawn Talker's hold-off reads it too (`SRP_REDECLARE_CS`, `srp_mbx.c`), and it is 105 ms at "
     "two interfaces ([below](" + X + "))."),
    ("- **The images.** The cut and the stamp add 216 B of rom to each image but the 1x1/1if size fixture, 224 B there "
     "(111,024 B, 41.0 RAMB36); the 8x8/2if platform holds 130,920 B of 131,072, 60.0 RAMB36, 152 B spare, and the "
     "8x8/1if platform 129,624 B, 56.0.",
     "- **The images.** The cut and the stamp add 216 B of rom to each image but the 1x1/1if size fixture, 224 B there "
     "(111,024 B, 41.0 RAMB36, on #894's head); the 8x8/2if platform there holds 130,920 B of 131,072, 60.0 RAMB36, "
     "152 B spare, and the 8x8/1if platform 129,624 B, 56.0 (this branch's: [section 5](#5-fit))."),
    ("### The final pass's restatements\n\n",
     "### The final pass's restatements\n\n"
     "On #894's head (`07ed787e`): the figures are that image's. This branch's head's are "
     "[below](" + B + ").\n\n"),
    ("### SRP's Talker declarations on THE TIERS\n\n",
     "### SRP's Talker declarations on THE TIERS\n\n"
     "At round 5's head `62298ab5`, superseded by the subsections below: the figures are that image's.\n\n"),
    ("so it is 2,023 cs at one interface (2,022 before) and 2,029 at two,",
     "so it was 2,023 cs at one interface (2,022 before) and 2,029 at two (2,030 since, [below](" + X + ")),"),
    ("### The composition measured again (#895)\n\n",
     "### The composition measured again (#895)\n\n"
     "At round 6's head `bf0844f1`, superseded by the subsections below: the figures are that image's.\n\n"),
    ("### The rule's slice built (#895)\n\n",
     "### The rule's slice built (#895)\n\n"
     "At round 7A's head `4c9757ee`, superseded by the subsections below: the figures are that image's.\n\n"),
    ("### The composition with #894's SET_CONFIGURATION cut (#895)\n\n",
     "### The composition with #894's SET_CONFIGURATION cut (#895)\n\n"
     "At round 7B's head `0c93071e`, superseded by the subsections below: the figures are that image's.\n\n"),
    # R835-4-S1, S2 in round 8's subsection
    ("The last queued notice holds 140 ms up to 278 us, and at 279 us it is 141.36 ms and txL 49.02 ms, each over its "
     "bound (`per_pass_threshold.py` in the round's receipts).",
     "The last queued notice holds 140 ms up to 278 us, and at 279 us it is 141.36 ms and txL 49.02 ms, each over its "
     "bound (`review-evidence/895-r1/author-r8/scripts/per_pass_threshold.py` on the `895-review-evidence` branch). "
     "These 18 us are the bounds' headroom, not the flip check's: `CTRL_LOOP_TX_MS` states the tx row, 34.00 ms, "
     "rounded up with no slack, so any rise in a pass's own cost restates it by the rule (the flip check refuses "
     "the statement from a 226 us base, the tx row 34.02), with no wire change at one interface until it passes 40 ms."),
    # R836-4-F1: What is left
    ("At the head, round 13's legs, on images byte-identical to the head's, gave arm A at 1x1/1if 0 refusals and 0 of "
     "140,032 passes over THE SHARE, the seven held-egress rows recorded misses, and exited 1 at 8x8/2if only on #910's "
     "build of one.",
     "At #894's head, #894's round 13's legs, on images byte-identical to that head's, gave arm A at 1x1/1if 0 refusals "
     "and 0 of 140,032 passes over THE SHARE, the seven held-egress rows recorded misses, and exited 1 at 8x8/2if only "
     "on #910's build of one. At this branch's head, round 8's legs, on images identical by sha256 to this head's at "
     "one interface and differing at two only in the hold-off's one instruction ([section 13](" + X + ")), give arm A "
     "0 refusals and 0 of 130,341 passes over THE SHARE at 1x1/1if and 0 of 218,322 at 8x8/2if, the seven held-egress "
     "rows recorded misses at each point."),
    ("Under them the first queued notice is a tier row: 14.66 ms within 20 at 1x1/1if, and 20.93 ms at 8x8/2if, "
     "stated 22 and reported ([the table above](#the-queued-notices-at-stated-costs-and-the-first-notice)).",
     "Under them the first queued notice is a tier row: 14.72 ms within 20 at 1x1/1if, and 21.11 ms at 8x8/2if, stated "
     "22 and reported, at this head (14.66 and 20.93 at #894's; [the table above]"
     "(#the-queued-notices-at-stated-costs-and-the-first-notice))."),
    ("(under THE TIERS the tx row, 33.38 ms within 49 at 1x1/1if, which `CTRL_LOOP_TX_MS` states as 34 ms, and 99 at "
     "two interfaces)",
     "(under THE TIERS the tx row, 34.00 ms within 49 at 1x1/1if and 104.25 at two interfaces at this head, which "
     "`CTRL_LOOP_TX_MS` states as 34 and 105 ms; 33.38 ms, 34 and 99 at #894's head)"),
])
edit('docs/reference/FR_NFR.md', [
    ("Under THE TIERS the 8x8/2if first queued notice is a tier row, 20.93 ms by every source, stated 22 ms and "
     "reported (#890);",
     "Under THE TIERS the 8x8/2if first queued notice is a tier row, 21.11 ms by every source at this head (20.93 at "
     "#894's), stated 22 ms and reported (#890);"),
])
edit('sw/firmware/ctrl/aecp/README.md', [
    ("and every notice queued behind it within `AECP_QUEUED_MS`, 130 ms at 1x1/1if (decision D's 125 ms, rounded up to "
     "the next 5 ms from the last queued notice's row by every source after #908's cuts, by [#894's amendment of "
     "2026-11-13](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6862465874) to its contingent "
     "ruling, item 2; `queued_bound.py`)",
     "and every notice queued behind it within `AECP_QUEUED_MS`, 140 ms at 1x1/1if (`queued_bound.py`'s rule, the "
     "built design's row rounded up to the next 5 ms and never over 140, for the row's 136.65 ms by every source at the "
     "slice rule's 900 us, [#895's ruling of 2026-11-15](https://github.com/kebag-logic/milan-fpga/issues/895"
     "#issuecomment-6892130675), item 1; 130 ms on #894's head, decision D's 125 ms rounded up from its row after "
     "#908's cuts by [#894's amendment of 2026-11-13](https://github.com/kebag-logic/milan-fpga/issues/894"
     "#issuecomment-6862465874) to its contingent ruling, item 2)"),
])
edit('tb/verilator/ctrl_service_budget/README.md', [
    ("At 1x1/1if the last is held to 130 ms, `AECP_QUEUED_MS` there, by [#894's amendment]"
     "(https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6862465874) to its contingent ruling's item 2: "
     "[`queued_bound.py`](queued_bound.py) derives it, the built design's row after #908's cuts rounded up to the next "
     "5 ms and never over 140 ms,",
     "At 1x1/1if the last is held to 140 ms, `AECP_QUEUED_MS` there, for the built design's row, 136.65 ms by every "
     "source ([#895's ruling of 2026-11-15](https://github.com/kebag-logic/milan-fpga/issues/895#issuecomment-"
     "6892130675), item 1; 130 ms on #894's head by [#894's amendment](https://github.com/kebag-logic/milan-fpga/"
     "issues/894#issuecomment-6862465874) to its contingent ruling's item 2): [`queued_bound.py`](queued_bound.py) "
     "derives it, the built design's row rounded up to the next 5 ms and never over 140 ms,"),
    ("`AECP_QUEUED_MS` planted in a copy of `aecp_mbx.h` past its 130 ms bound (at 1,250 ms) at 1x1/1if;",
     "`AECP_QUEUED_MS` planted in a copy of `aecp_mbx.h` past its 140 ms bound (at 1,250 ms) at 1x1/1if;"),
])
edit('sw/firmware/ctrl/plat/README.md', [
    ("`ctrl_memory.LEDGERED`), with 1,656 B of `rom` left.",
     "`ctrl_memory.LEDGERED`), with 1,368 B of `rom` left at this head (1,656 B at round 6's)."),
])
print('ok')
