# HANDOFF, round 4: the cut, attempt 1 (#665), [A794]

**STOP: attempt 1 does not pass.** The work cut holds on its own terms: wire behaviour is unchanged (the control
campaign 797 of 797 and the two-placement comparison pass on it and at the tip), and the largest legal record is
within its statement at every point, with margin (870 of 975 us at 1x1/1if, 1,610 of 1,715 at 8x8/1if, and 1,565
of 1,650 at 8x8/2if, the variant's). The attempt fails on these, each with figures below:

1. **A design conflict at 8x8/2if (the relearn).** The ruled procedure (three windows at 1x1/1if, nothing placed
   by hand) learns `aecp owe` and `aecp owed_drain`, the owed-notice queue's functions, which the third window runs.
   The size fixture compiles that queue out at two interfaces by design (`AECP_MBX_OWED_SLOTS` is 0 there, #894,
   `aecp_mbx.h`), so `ctrl_hot.py`'s LINKED rule refuses every 8x8/2if fixture image. No 8x8/2if leg of the tip
   builds. Any way past it (drop the entries, give the fixture the queue's code, change the gate) needs a ruling.
   None was chosen. A scratch variant without just those two entries was measured for the decision.
2. **Measured costs over their statements.** Each was traced to the head that brings it (the table "Where each miss
   comes from"):
   - since step 9, before round 4: the 1x1/1if paced edit record (a one-row REMOVE, 320 us at step 9, 310 at the
     tip, against 305) and the 8x8/2if AECP notice item (27,899 cycles at step 9, 28,596 in the variant, against
     27,500);
   - since #936 (step 10): at 8x8/1if the SRP record (380 us at the tip against 365), its apply item (375 against
     345) and a pass's polls base (315 against 280). The relearn lowers them but does not bring them back. Ruling
     item 3 lets MSRP's receive path leave the hot region only if the SRP record holds at every point, and it does not
     at 8x8/1if;
   - from the relearn: at 8x8/2if `record.maap`, 160 us against 155 (155 with the old list);
   - from the cut's code placement: at 8x8/1if event.MAAP, 240 us against 225 (210 at step 9, 215 at step 10, 240 with
     the cut on the old list and at the tip). The cut changes no MAAP code; it moves what is linked after
     `aecp_maps.c`, and the fetch L1's conflicts with it;
   - not traced to a head: the variant's 8x8/2if event.AECP, 120 us against 115.

Attempt 2 (a deeper work cut, same procedure) waits for the manager's go. Finding 1 needs a ruling before any head
can measure 8x8/2if with the ruled list. Most of finding 2 is not on the largest record's path, so a work cut there
does not reach it.

## Heads

| Head | Branch | What |
|---|---|---|
| `ed5855fe` | `flip-train-1117` (the step-9 branch) | step 9 `4a5bfb32` and the cut: `ab4bc245` (the cut), `d7c8cd95` (its account), `dccca6ec` (round 3's missed contents-list fix), `ed5855fe` (the fixture at its measured 60.5, S14 debt) |
| `25299527` | `flip-train-1117-p10` | the p10 tip: #944 `7cfb8a04` (`5ff15cbc`), its idiom fix `9a91c39b`, the step-9 branch carried by merge (`547c0b1e`, `45af90b3`, `25299527`), the relearned hot list `febbfc4b`, the platform's 8x8/1if image at its measured 58.0 `25b2a5b7` |
| `febbfc4b` | (p10) | the measured tip: everything after it changes only the planner's caps and documentation, no image the harness builds |

Nothing is pushed or posted. Both branches are local; the gitlinks are `gptp-processor` `1616fc8f` and
`protocol-processor` `801ef228` on both.

## Provisional step 10: #944 at `7cfb8a04`

#944's review head `7cfb8a04` (GitHub head checked before the merge) is merged `--no-ff` on `flip-train-1117-p10`
(branched from the step-9 tip `4a5bfb32`) as `5ff15cbc`. 9 of its 22 files conflicted; RESOLUTIONS.md has each. It
moves no submodule, and the index kept the train's gitlinks (staged by path, never `git add -A`). Two points need the
reader:

- **The ROM ledger, restated to the composed images' measurement in the merge.** The fixture's `answering-ports` arm
  needs 131,216 B of `rom`, 144 B past the 131,072 B that 60.0 holds, so its entry is **60.5, ledgered as S14 debt**
  (RULING-1117b: "a fixture at 60.5 is S14 debt"); the other five arms need 130,720 to 131,036 B. `ctrl_plat` is 64 B
  more at 1x1/1if and at 8x8/2if (18,048 and 21,568 B; #936's own head grows the 1x1 two-interface point instead), and
  the platform's 8x8 two-interface image holds 138,816 B within its 62.5. Its 8x8 one-interface image has 8 B of `rom`
  left at its 57.5.
- **The twin's strings**: #936 fixes the notice the train owed (`stream-output-0-notices`) and owes a new row
  (`stream-output-0-dest-mac`) with a plant. Its strings were taken, and the twin's own run confirmed them.

| Check at step 10 (`5ff15cbc`; the fix `9a91c39b`) | Result |
|---|---|
| Firmware shards 0 to 3 | all PASS; the control campaign (shard 1) 797 of 797 |
| Two-placement simulation | `make twin`, `twin-plants` (16 plants, each refused by its own words), `twin-maps`, `twin-maps-plants`: all PASS |
| ROM ledger | `plat_ledger.py --self-test` PASS at all four points, 9 of 9 controls; the fixture in six arms (60.0, `answering-ports` 60.5); `test_ctrl_memory` PASS |
| Harness self-tests | `run.py --self-test` 0 failures; `rows_tiers`, `record_classes`, the load gate and its self-test, the flip self-test, `shape_costs`, `egress_ledger`, `mailbox_margins`: PASS; `flip_check` at 1x1/1if PASS, and at all points the base's same eleven 8x8/2if findings |
| `py_idiom` | FAIL at the merge: `aecp_mutants.py` at 1,009 lines (#936 took it to 1,000, the train adds 22). Fixed at `9a91c39b` (#936's four notice mutants in `aecp_notice_mutants.py` in place, the 365-row table identical); PASS |
| Docs, hygiene, C++ idioms, `fw_coverage --check` | PASS. `gen_toc.py --check` was not in the list here; the drift it finds came from step 9 (below) and is fixed on the step-9 branch |

## Attempt 1, part 1: the work cut

Composition commits on the step-9 branch `flip-train-1117`: the cut `ab4bc245` (`aecp_maps.c` only), its account
`d7c8cd95` (`SPLIT_CONTROL_MEMORY.md`, after #923's subsection), `dccca6ec`, a step-9 contents-list fix (below), and
`ed5855fe`, the fixture's ledger at its measured 60.5. The cut adds 128 B of `rom` to the `answering-ports` arm at
8x8/2if, 131,128 B, past step 9's 60.0, so that image's build was refused until the restatement. They are carried
to p10 by `git merge --no-ff` (`547c0b1e`, `45af90b3`, `25299527`), with no rebase.

**Attributed before it was chosen.** The step-9 record (arm A's `aecp-largest-notice`, REMOVE_AUDIO_MAPPINGS of 63
identical mappings at an input port, 95,482 cycles, 1,005 us) was traced by committed PC and split by function
(receipts/cut/s9.perfunc.txt): 16,135 of 22,202 instructions are `aecp_maps.c`'s. The two changes remove work every
mapping of every edit does, whatever the mappings:

- the stream format's channel count read from its three bytes (`format_channels`, equal to `channels(wire_be64(p))`
  for every byte pattern), not the 64-bit word;
- the port's geometry read once an edit (`struct geometry`), not once a mapping.

No check, result or response moves, and no line a mutant or plant patches is touched.

| The record at 1x1/1if, arm A, the step-9 placement | Cycles | Instructions | By the rule | Margin to 975 us |
|---|---:|---:|---:|---:|
| step 9 | 95,482 | 22,202 | 1,005 us | -30 us |
| **the cut** | **84,389** | **18,577** | **890 us** | **85 us** |
| not taken: the cut plus `wire_be16` written as a sum | 80,097 | | 845 us | 130 us |

By function, instructions / cycles: `legal` 5,418 / 16,127 against 4,158 / 11,469; `wire_be64` 819 / 2,036 against
none; `wire_be32` 2,772 / 7,721 against 1,386 / 3,941; `aecp_map_command` 6,649 / 26,751 against 6,489 / 26,629;
`aecp_find` unchanged (2,432). The sum variant was not taken: GCC 16 turns the OR form of a 16-bit read into a byte-swap
of a halfword (ten instructions for five), so its further 45 us rests on the compiler's choice, not on work removed.
Margin was sized against the hot list's reorder (the rehearsal moved the record by about 2,000 cycles) and the
frozen #936 head.

| Gate on the cut (`ab4bc245`) | Result |
|---|---|
| Firmware shards 0 to 3 (the control campaign is shard 1) | all PASS; the control campaign 797 of 797, unchanged |
| Two-placement simulation | `twin`, `twin-plants`, `twin-maps`, `twin-maps-plants`: all PASS |
| ROM ledger at the step-9 branch's tip (`ed5855fe`) | PASS: the platform at four points, 9 of 9 controls (`rom` 124,496 / 126,104 / 137,144 / 138,720 B, 72 B left at 8x8/1if's 57.5); the fixture's six arms 130,624 to 131,128 B (`answering-ports` 60.5); `test_ctrl_memory` |
| Quick list at `dccca6ec` (with `gen_toc.py --check` and `--verify-anchors`) | PASS but the base's same eleven 8x8/2if flip findings: `run.py --self-test` 0 failures, `fw_coverage --check` PASS (the ratchet holds with the cut), `py_idiom`, the docs gates, `gen_toc.py --check` and `--verify-anchors` |

**A step-9 miss of round 3, fixed (`dccca6ec`).** The merge of #934 left the two-placement README's contents list with
the boot leg's entry twice and without the split control path's and the twin's. The docs workflow's `gen_toc.py
--check` reports that drift at `8f6fbb84`. Round 3's quick list ran only `--selftest`, so it was not seen there. The
list is regenerated by `gen_toc.py --write`, and the two descriptions are restored at step 9's counts. Round 4's quick
list runs `--check` and `--verify-anchors` at every head.

## Attempt 1, part 2: the relearn

`febbfc4b` on p10, by the recorded procedure and the ruled third window, traced at `547c0b1e` (the cut on step 10;
only documentation changed before the commit). Windows: `backlog` 162,156 committed PCs (its run ends inside),
`backlog-adp` 900,000, `aecp-largest-notice` 776,535. The list has **269 entries** against 206: 93 added, 30 gone,
nothing placed by hand. The header records the three windows as standing procedure, and that a fourth window or a
window for one head needs a ruling. The traces are named by sha256 there and in receipts/hot/. `ctrl_hot.py --check
--map` and `--self-test` pass.

- The third window's entries are the map edit's and the `EDIT` window's, as in round 3's rehearsal (`hot-rec`), but
  for `wire_be64`, which the cut removed.
- **MSRP's receive path leaves the hot region** (`mrp_rx`, `mrpdu_parse`, `msrp_decode_attr`, `msrp_join_ind` and
  the rest), as do `mrp_transmit`, MAAP's `enqueue` and `send_frame`, and the fan-out's `fan` and `fan_end`, which
  the old list had placed by hand. Under ruling item 3 that stands only if the SRP record and the SRP rows and the
  last queued notice hold at every point (the survey below).
- **The conflict (finding 1).** The third window ran `aecp owe` and `aecp owed_drain`, the owed-notice queue, which
  the size fixture compiles out at two interfaces. LINKED refuses every 8x8/2if fixture image, in all four arms of
  the measurement and in the ledger's six. The platform's images link at all four points, since `ctrl_plat.c`
  always gives the queue. Round 3's rehearsal linked only 1x1/1if.

| Gate at the p10 tip `25299527` | Result |
|---|---|
| Firmware shards 0 to 3 | all PASS; the control campaign 797 of 797 |
| Two-placement simulation | `twin`, `twin-plants` (16 plants), `twin-maps`, `twin-maps-plants`: all PASS |
| Quick list (with the TOC gates) | PASS but the base's same eleven 8x8/2if flip findings |
| ROM ledger | the platform PASS at four points, 9 of 9 controls; the fixture's 8x8/2if arms refused by LINKED (finding 1) |

## The measurement at the p10 tip

Three heads were measured: **the tip as ruled** (`febbfc4b`; the later `25299527` builds the same images, byte for
byte), at 1x1/1if and 8x8/1if, since it builds no 8x8/2if image; **the scratch variant** (the tip's list without
the two entries the 8x8/2if fixture compiles out, not committed), at 8x8/2if; and, for the record classes only,
**the cut with the old list** (`45af90b3`, no relearn). The rule throughout: cycles plus 5 %, rounded up to 5 us.
Cells give us by the rule, then the margin to the statement (negative means over).

**The largest legal record** (the long class, `record_classes.py`; arm A's and the answering-ports arm's
`aecp-largest-notice`):

| Point (statement) | The tip | The variant | The cut, old list | Step 9 (round 3) |
|---|---:|---:|---:|---:|
| 1x1/1if (975 us) | 82,619 c, **870, 105** | 82,628 c, 870, 105 | 84,044 c, 885, 90 | 95,482 c, 1,005, -30 |
| 8x8/1if (1,715 us) | 152,869 c, **1,610, 105** | 152,811 c, 1,605, 110 | 154,637 c, 1,625, 90 | |
| 8x8/2if (1,650 us) | does not link | 148,711 c, **1,565, 85** | 150,340 c, 1,580, 70 | |

**The record classes and the fan-out item that miss somewhere**, at the heads before the tip:

| Cost (point, statement) | Step 9 `4a5bfb32` | Step 9 and the cut `ed5855fe` | Step 10 `9a91c39b` | Cut, old list `45af90b3` | The tip / the variant |
|---|---:|---:|---:|---:|---:|
| paced record, a one-row REMOVE, arm B `aecp-fanout` (1x1/1if, 305 us) | **320** | **315** | **325** | **315** | **310** / **315** |
| paced record, SET_CONFIGURATION, arm B (8x8/2if, 595 us) | 580 | 580 | **605** | **600** | - / 585 |
| `aecp` poll item, arm B `aecp-fanout` (8x8/2if, 27,500 cycles) | **27,899** (5 over) | **27,839** (5) | **28,689** (20) | **28,802** (20) | - / **28,596** (10) |
| the same item (1x1/1if, 21,000; 8x8/1if, 14,500) | | | | 15,735; 13,865 | 15,718; 13,640 / 15,779; 13,617 |

**Every statement the survey holds** (`survey_point.py` over every leg of the point, the datapath events by
`eventcost_dp.py`; `record_classes.py` for the record classes), us by the rule against the statement, the tip at
1x1/1if and 8x8/1if, the variant at 8x8/2if; **bold** is over:

| Statement | 1x1/1if (tip) | 8x8/1if (tip) | 8x8/2if (variant) |
|---|---:|---:|---:|
| the largest legal record (long) | 870 / 975 | 1,610 / 1,715 | 1,565 / 1,650 |
| a paced record | **310 / 305** | 590 / 685 | 585 / 595 |
| an ordinary record (held other) | 220 / 245 | 200 / 265 | 200 / 265 |
| event.AECP | 60 / 75 | 70 / 115 | **120 / 115** |
| event.MAAP | 150 / 165 | **240 / 225** | 200 / 225 |
| AS_PATH_CHANGED / AVB_INFO_CHANGED | 25 / 35, 25 / 35 | 25 / 40, 25 / 40 | 30 / 40, 30 / 40 |
| the SRP record (`record.srp`) | 245 / 285 | **380 / 365** | 325 / 365 |
| the SRP record's apply (`item.record`) | 245 / 285 | **375 / 345** | 320 / 365 |
| a pass's polls base | 205 / 225 | **315 / 280** | 305 / 345 |
| `record.maap` | 110 / 115 | 175 / 175 | **160 / 155** |
| `record.adp` | 100 / 100 | 130 / 130 | 125 / 125 |
| the AECP notice item (`item.aecp`) | 170 / 210 | 145 / 145 | **305 / 275** |
| the long notice item (`aecp_long`) | 345 / 365 | 320 / 320 | 675 / 700 |
| survey result | 0 exceeded | 4 statements over | 3 statements over |

The answering-every-port arm (the queued notices) passes at both points of the tip, and every arm's budget rows
are within their budgets but for the command behind the owed input (63 to 65 ms against 20 ms at every point, as in
round 1). That row is one of the three no CPU lever moves (tsn-c-stack #26).

**Where each miss comes from**, by the same group run alone at earlier heads (cycles; receipts/measure/):

| Miss | Step 9 `4a5bfb32` | Step 9 and the cut `ed5855fe` | Step 10 `9a91c39b` | The cut, old list `45af90b3` | Attempt 1 |
|---|---:|---:|---:|---:|---:|
| 1x1/1if paced record (305 us) | **320 us** | **315** | **325** | **315** | **310** (tip) |
| 8x8/1if polls base (28,000) | 26,866 | | **29,427** | **30,937** | **29,933** (tip) |
| 8x8/1if SRP record's apply (34,500) | 33,974 | | **34,529** | **36,086** | **35,506** (tip) |
| 8x8/2if `aecp` item (27,500) | **27,899** | **27,839** | **28,689** | **28,802** | **28,596** (variant) |
| 8x8/2if `record.maap` (155 us) | | | | 155 | **160** (variant) |
| 8x8/1if event.MAAP (225 us), the `srp-talker-loss` group | 19,530 (210 us) | | 20,339 (215) | **22,428 (240)** | **22,778 (240)** (tip) |

So the 1x1/1if paced record and the 8x8/2if notice item have been over since step 9. #936 takes the 8x8/1if SRP
record and polls base over. The relearn improves those three, but per ruling item 3 the SRP record must hold at every
point with MSRP's receive path out of the hot region, and at 8x8/1if it does not. The relearn takes the 8x8/2if MAAP
record over (MAAP's `enqueue` and `send_frame` left the hot region). The 8x8/1if MAAP event moves with the cut's
placement alone: the code after `aecp_maps.c` moves, and the 4 KiB direct-mapped fetch L1's conflicts move with it.
The 8x8/2if event.AECP was not traced to a head.

**Rows**, at the statements (no statement moved, so `flip_grade.py --check` reads the same table as round 3 at every
head): at 1x1/1if every row holds, margins R4 6.58, R5 13.50, R6 16.00, first 5.26, last 2.11, R4L 34.42, ACMP
**0.09**, ADP 1.88, MAAP 1.79, tx 14.72 and txL **0.11** ms. At 8x8/1if THE TRANSMIT's figure holds (74.26 of 75 ms)
and the load is 0.735 of 0.75; its other rows are reported, owed to #872. At 8x8/2if the findings are the base's
same eleven, and no others.

**The ROM ledger** at the tip: the platform at four points, 9 of 9 controls, 124,696 / 126,328 / 137,328 /
138,936 B of `rom`, 44.5 / 45.5 / **58.0** / 62.5 RAMB36 (the 8x8/1if entry raised to 58.0, S14 debt). The size
fixture is 60.5 (S14 debt, as ruled). Its 8x8/2if arms are refused by LINKED at the tip; in the variant they need
130,840 to 131,336 B, two arms at 60.5. `test_ctrl_memory` passes.

## Owed at the final head

- **Fit and the timing floor**, at the final head: owed, not run (no Vivado this round). The release image was not
  exported at either head this round.
- **A ruling on finding 1** before any head can measure 8x8/2if with the ruled hot list. The options, none chosen:
  the variant (drop a traced entry that some split image compiles out, a mechanical rule but not the ruled
  procedure); give the fixture's two-interface image the owed queue's code; or change the gate.
- **Attempt 2's go** (a deeper work cut, same procedure). From these figures, its scope would be the misses of
  finding 2. None is on the largest record's path, which has 105 us of margin at 1x1/1if:
  - the 1x1/1if paced edit record (310 us against 305; since step 9);
  - the 8x8/2if notice fan-out item (28,596 cycles against 27,500; since step 9);
  - the 8x8/1if SRP record, its apply and the polls base (#936's);
  - the 8x8/2if MAAP record (the relearn's) and the 8x8/1if MAAP event (the cut's placement).
  The last two move by code placement alone, so the list relearned at the frozen head can move them either way.
- **At #936's frozen head**: the same cut is re-measured with the list re-traced (RULING-1117b, item 4). The step-9
  branch `ed5855fe` is its base.

## Notes

- No step was pushed or posted; no GitHub state changed. The two-placement simulation, the shards and the quick list
  ran at every committed head they name. The three measured configurations' legs are receipts under
  receipts/measure/.
- **Round 3's measurement scope.** Round 3 attributed only the six groups of the record and events at 1x1/1if, so
  two misses present since step 9 (the 1x1/1if paced record and the 8x8/2if fan-out item) were first seen this round.
  Round 3's quick list also lacked `gen_toc.py --check` (`dccca6ec` fixes the drift it missed). Both are corrected
  in round 4's procedure.
- **CPU.** Every unit ran on the shared session pool (`cpu_ranges.SESSION_POOL`, 64-95) by CPUWeight, never an
  exclusive booking. At 23:40 the cut-only head's and the variant's duplicate arms were stopped by unit to bring the
  decision's survey forward (receipts/measure/STOPPED.txt); their answering-ports arms had finished and are kept.
- Scratch stays under 40 GB (superseded attribution builds of rounds 2 and 3 removed; their figures are in
  round 3's receipts).
