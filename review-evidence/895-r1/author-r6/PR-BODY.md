[A775]

## Contents

- **[Status](#status)** — Round 6 stopped at its head: the slice rule leaves the built design at the restated tables, and the built design's last queued notice is over 130 ms.
- **[Linked Issue / roles](#linked-issue--roles)** — Public tasks, executor, and independent reviewers.
- **[Round 6](#round-6)** — Each item of the round's assignment and the commit that answers it.
- **[The reviews' findings](#the-reviews-findings)** — R835-3 and R836-3, finding by finding.
- **[Every stated cost against this head's legs](#every-stated-cost-against-this-heads-legs)** — The survey, the two restatements, and the polls' base attributed.
- **[The 1x1/1if flip check at the restated tables](#the-1x11if-flip-check-at-the-restated-tables)** — Every row by every source at the built 900 us slice and at the rule's 950 us, the pace, `tier_grid.py` and the load.
- **[The CPU budget harness](#the-cpu-budget-harness)** — The legs at 1x1/1if on the merge's image, and the 8x8/2if `datapath-events` group.
- **[ROM ledger](#rom-ledger)** — Every point at the merge, the cut's 208 to 224 B.
- **[What did not run](#what-did-not-run)** — The gates, the full pass and the 8x8/2if legs, left at the stop.
- **[Description](#description)** — The validity gate and the declarations (rounds 1 and 2), and each source's stream_id (#905).
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this does not do.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

**STOP** at `bf0844f19374bfbf7091271dfb50fad7a1f1835d` (`895-talker-redeclare` -> `dev-soft-core`), round 6: the decision is the maintainer's (#895 issuecomment-6886561084).

- Round 5 ended at `62298ab5` (REVIEW READY, issuecomment-6880958086); its two delta reviews were NEGATIVE: R835-3 (issuecomment-6881281833: F1 MAJOR, F2 MINOR) and R836-3 (issuecomment-6881271637: F1 MINOR).
- Round 6 merged #902's `9606b3a9` (#894's round 11) and measured the composition again. Two stated costs were under their rule figure at 1x1/1if and are restated: the polls' base 205 -> 215 us and a pass's events' fixed part 30 -> 35 us.
- At the restated tables the built design's last queued notice at 1x1/1if is **134.94 ms, over its 130**, and the slice rule (`rows_tiers.ruled`, `tier_grid.py`) takes **950 us**, not the built 900. Both are stops of the ruling issuecomment-6876349305, so the round stops for a decision; no slice is chosen here.
- The gates, the full pass, the sweep and the 8x8/2if legs did not run (below).

No rebase, no force, no amend. No RTL, mailbox-contract, firmware-code, tsn-c-stack, lwSRP or donor change in this round's own commits (the merge brings #902's `aecp_maps.c` cut). No bound, ceiling or the every-source rule moves; the two figures moved are the rule's restatements.

## Linked Issue / roles

Relates to #895
Relates to #905 (acceptance 1 to 3 and 5 here; 4 is the bench run)
Relates to #894 (#902 merged here at `9606b3a9`; its names patch carried unchanged)
Relates to #906, #907 (srptx findings, not fixed here)
Relates to #909 (the code and data placement the merges move, named, not chased)
Relates to #896
Relates to #665

Executor: `[A775]`
Internal cleared-context reviewer: `[R835]` (R835-3, started issuecomment-6881026642)
External reviewer: `[R836]` (R836-3, issuecomment-6881271637)

## Round 6

| Commit | Item | What |
|---|---|---|
| `df0bc467` | 1 | Merge #902's `9606b3a9` (#894's round 11: the one-row map edit's cut, its edits a class of their own at 260 / 325 us). Conflicts: `load_grade.py`, each cost the side's that moved it from the merge base `7398ec0a`, the larger where both did (AECP's timer slot, the 8x8/2if TICK and MAAP's record #895's; ACMP's owed frame #894's 55 / 70 us; the 1x1/1if TICK and the 8x8/2if fixed part both sides' 50 / 35); FR_NFR 3.4.1's pace sentence, the SRP README's tx sentence and section 13, each both sides' text at the merge's figures. At the merged tables, before any re-measure, the slice rule already takes 950 us (+0.0200 against the built 900's +0.0175) and `rows_tiers.py --selftest` refuses the tree. |
| `3024e740` | 2 | The polls' base at 1x1/1if 205 -> 215 us (`poll_grade.STATED_US`, `load_grade.STATED_US_DONOR`) and a pass's events' fixed part 30 -> 35 us (`load_grade.STATED_US`, both columns), each its measurement on the merge's image by the rule. |
| `bf0844f1` | 2-4 | Section 13's new subsection "The composition measured again (#895)" (the survey, the attribution, the datapath events, the classes, the rows at both slices, the stop); the tiers table, the tx paragraph, the pace table and the closing summary at this head's figures (R4 13.11 ms); section 5's plan at this head (the cut's 208 to 224 B); FR_NFR 3.4.1, the SRP and platform READMEs; R836-3-RS1's wording. |

## The reviews' findings

| Finding | Severity / lens | Answer at this head |
|---|---|---|
| R835-3-F1: the 1x1/1if polls' base stated at 205 us against 20,456 cycles (215 by the rule) | MAJOR; Conformance, RTL, Tests, Docs | **Restated, and it stops the round.** Every stated table the rows read was surveyed against this head's legs by the rule ([below](#every-stated-cost-against-this-heads-legs)); two were under, the base (20,282 cycles at the merge, 215 us) and a pass's events' fixed part (3,041 cycles, 35 us), both restated in both columns (`3024e740`). The base over 205 is this lane's Talker work: #894's own image measures 18,843 cycles (200 us). At the restated tables the flip check, the pace rule, `tier_grid.py` and `rows_tiers.py --selftest` ran: the slice rule takes 950 us and the built design's last queued notice is 134.94 ms, the ruling's stop. |
| R835-3-F2: 8x8/2if AMAP_LIVE_WRITE stated at 25 us against 2,426 cycles (30 by the rule) | MINOR; Conformance, Tests | **Shown within at this head.** The `datapath-events` group on the merge's image at 8x8/2if measures its take and sinks at 2,367 cycles, 23.67 us, within the 23.80 that 25 holds, by `eventcost.py`, the measure #894 states `DATAPATH_US` by (#894 issuecomment-6872978311); section 13 states it. The 8x8/2if rows are unchanged. |
| R835-3-RS1: the roles lines | RESIDUE; Docs | Taken, as worded (above); the external line names R836-3. |
| R835-3-S1: `maap_mbx_start`'s written mark before a first opening | SUGGESTION; Robustness | Retained, not taken: no code change this round. |
| R835-3-S2: a cost audit against every table at each re-measure | SUGGESTION; Tests | Taken as evidence: `costs_vs_stated.py` over this round's legs, against every table the rows read, before and after the restatement (the round's receipts). Not added to the tree. |
| R835-3-S3: section 5's table title against its deltas' base | SUGGESTION; Docs | Taken: the table is this head's, and each delta names its base (round 4's against `5b264bf2`, the cut's against `62298ab5`). |
| R835-2-S2 = R836-3-S5: the INDEX of the evidence packet hashed before the scrub | SUGGESTION; Docs | Taken: this round's INDEX is generated after the scrub. |
| R836-3-F1: the closing R4 figure 12.85 ms | MINOR; Docs | Taken: the closing summary is this head's, R4 13.11 ms by every source (`flip_grade.py --check --point 1x1/1if` at `bf0844f1`), with the last queued notice's 134.94; the two other present-tense references that pointed at the tiers table now name their heads. |
| R836-3-RS1: "move no byte" | RESIDUE; Docs | Taken, as worded: "The pace and THE TRANSMIT restatements leave every image's linked ROM and SRAM sizes unchanged" in section 13 and section 5; the PR's ROM bullet below. |
| R836-3-S1 to S4 (= R836-1-S2, S3; R835-1-S1 = R835-2-S3; R835-2-S1) | SUGGESTION | Retained, optional: no code change this round. |

## Every stated cost against this head's legs

The survey (`costs_vs_stated.py`) reads each table from the tree and holds each key to the most measured over the 1x1/1if legs on the merge's image `df0bc467` by the rule. The measures are round 1's parsers, the harness's own heaviest (`poll_grade.held`, `whole_grade.held`) and `record_classes.py`'s classes. The tables are `load_grade.py`'s two columns, `poll_grade.STATED_US`, `whole_grade.stated_us` (`ctrl_loop.h`'s passes given whole), `rows_grade.ROW_COSTS`, `rows_tiers.DATAPATH_US`, `LONG_NOTICE_US` and `LONG_RECORD_US`, and `edit_rows.EDIT_RECORD_US`.

| Cost (1x1/1if) | Most measured, CPU cycles | Rule | Stated before | Stated now |
|---|---:|---:|---:|---:|
| the polls' base (`acmp-cmd`) | 20,282 | 215 | 205 | **215** (both tables) |
| a pass's events' fixed part (`notice-burst-0`) | 3,041 | 35 | 30 | **35** (both columns) |
| every other key | | | | within its rule figure (`UNDER 0` at the restated tables) |

- **At the merge's tables `UNDER 4`** (the two keys in both of their tables); **at the restated tables `UNDER 0`**. The ruled AECP record (item 3) is within too: every other record is at most 20,525 cycles, 220 us against 235.
- **AECP's classes** (`record_classes.py`): a paced edit at most 23,306 cycles (245 us, 260 stated), the largest legal command's 86,762 (915, 975), every other record 20,525 (220, 235). Arm B's SET_CONFIGURATION, 33,304 cycles (350 us), is reported, not held, as #894 records.
- **The polls' base, attributed.** At #894's own head `9606b3a9` the same group's heaviest base is 18,843 cycles, 200 us by the rule. At the merge it is 20,282, 1,439 more. The pass runs 79 instructions more with 4 instruction refills fewer, so the growth is code. It falls in the polls: MAAP's +407 and SRP's delivery's +378, which carry the Talker's declarations and each source's stream_id (#905), and ACMP's, ADP's and AECP's +320, +198 and +161. It was 20,456 at round 5's head.
- **A pass's events' fixed part** rose from 2,623 to 3,041 cycles with the cut's placement (#909), not traced.

## The 1x1/1if flip check at the restated tables

By every source, ms (`flip_grade.py --check --point 1x1/1if` at `bf0844f1`, and the same rows at 950 us on a scratch export of it):

| Row | Bound | Round 5 `62298ab5` | The merge's tables | Restated, the built 900 us | Restated, 950 us (the rule's) |
|---|---:|---:|---:|---:|---:|
| R4 | 20 | 12.96 | 13.03 | 13.11 | 13.16 |
| R5 / R6 | 90 | 73.46 / 69.35 | 73.88 / 69.73 | 74.47 / 72.53 | 74.52 / 72.58 |
| first queued notice | 20 | 14.59 | 14.62 | 14.65 | 14.70 |
| last queued notice | 130 | 127.08 | 127.73 | **134.94** | 127.83 |
| R4L | 238 | 203.48 | 203.49 | 203.53 | 203.58 |
| ACMP / ADP / MAAP | 30 | 28.85 / 27.20 / 27.29 | 29.03 / 27.36 / 27.46 | 29.29 / 27.56 / 27.65 | 29.34 / 27.61 / 27.70 |
| tx | 49 (`CTRL_LOOP_TX_MS` 34) | 33.20 | 33.39 | 33.64 | 33.69 |
| txL | 49 | 47.86 | 47.97 | 48.32 | 48.37 |
| result | | PASS | PASS | **FAIL** | every row holds |

- **The slice rule** (`rows_tiers.slice_choice`, `ruled`): 950 us, least margin +0.0129 (txL binding); the built 900 us is -0.038 (the last queued notice). At the merge's tables it was 950 already (+0.0200 against +0.0175).
- **`tier_grid.py --point 1x1/1if`**: 12 of 420 designs hold every row and the load; CHOSEN 950 us, AECP first, SRP first, the AECP queue, cap 2, +0.0129.
- **`rows_tiers.py --selftest`**: 1031 of 1032; "ESCAPED the built design's slice not the rule's".
- **The pace rule**: 9 ms (txL 49.94 at 8, 48.32 at 9); the built design's last queued notice is over 130 at every pace from 7 to 13 ms (135.04 to 134.81).
- **Each restatement alone** puts it over: the base alone 133.91 ms, the fixed part alone 132.72.
- **The load** (`load_grade.py --check`, PASS): 0.517 at the pin and 0.513 with tsn-c-stack#32, 0.696 with every notice the largest legal one.
- **8x8/2if** (reported, its tables unchanged): R4 42.85, R4L 210.91, tx 89.98 under the 98 stated, txL 399.86; load 0.798 / 0.756.
- Self-tests at the head: `load_grade.py --selftest` 25 of 25; `flip_grade.py --selftest` **584 of 585**: "ESCAPED AECP_QUEUED_MS not the bound the last queued notice's row rules", which `queued_bound.controls` reports while the tree's own statement is not its rule's: the amendment's rule (#894's contingent ruling of 2026-11-13, item 2) rounds the 134.94 ms row up to 135 ms, within its 140, against the 130 `aecp_mbx.h` states. It was 585 of 585 at the merge.

## The CPU budget harness

At 1x1/1if, every group of every arm on a clean clone of the merge `df0bc467`, whose firmware is the head's (the later commits change Python tables and docs). `run.py --record-budget-findings --record-share-findings`; arm A in five parts, merged and regraded as one leg.

| Point | Arm | Groups | Refusals | Budget misses | Passes over the share | `STATED` | rc |
|---|---|---:|---:|---|---|---:|---:|
| 1x1/1if | A (5 parts, merged) | 96 | 0 | 7 of 950 | 0 of 133,506 | 0 | 0 |
| 1x1/1if | `answering-every-port` | 16 | 0 | 0 of 280 | 0 of 20,434 | 0 | 0 |
| 1x1/1if | `valid-destinations` | 2 | 0 | 0 of 5 | 0 of 2,668 | 0 | 0 |
| 1x1/1if | B (`aecp`, `aecp-largest-notice`, `aecp-fanout`) | 3 | 0 | 0 of 44 | 0 of 339 | 0 | 0 |
| 8x8/2if | A, `datapath-events` alone | 1 | 0 | 0 of 0 | 0 of 163 | 0 | 0 |

- **The misses** are arm A's seven `backlog-owed` held-egress rows (ruling 6871343905 (a)), as before.
- **Join intervals: 365 in 117 group runs at this head, 187.779 to 190.109 ms, every one within 181.0 to 239.0.**
- **The attribution leg**: `acmp-cmd` and `aecp-fanout` at 1x1/1if on #902's `9606b3a9`, rc 0.
- Arm B now runs `aecp-largest-notice` and `aecp-fanout` beside `aecp`, the groups `record_classes.py` holds there.

## ROM ledger

The merge's images (`plat_ledger.py` PASS, 0 findings; `ctrl_srp_image.py` for the size fixture and the two 8x8/2if harness arms). rom / sram need in B, then RAMB36:

| Point | Image | Entry or budget | Round 5 `62298ab5` | This head | Left |
|---|---|---:|---|---|---:|
| 1x1/1if | fixture | 56 | 111,928 / 55,184: 41.0 | 112,152 / 55,184: 41.0 | |
| 1x1/2if | fixture | 56 | 113,472 / 57,360: 42.5 | 113,696 / 57,360: 42.5 | |
| 8x8/1if | fixture | 56 | 124,608 / 96,288: 54.5 | 124,816 / 96,288: 54.5 | |
| 8x8/2if | fixture | 59.0 | 126,112 / 113,232: 59.0 | 126,320 / 113,232: 59.0 | 656 B |
| 8x8/2if | harness `answering-every-port` | 59.0 | 126,420 / 113,296: 59.0 | 126,628 / 113,296: 59.0 | 348 B |
| 8x8/2if | harness `valid-destinations` | 59.0 | 126,280 / 113,232: 59.0 | 126,488 / 113,232: 59.0 | 488 B |
| 1x1/1if | platform | 56 | 116,992 / 56,224: 43.0 | 117,216 / 56,224: 43.0 | |
| 1x1/2if | platform | 56 | 118,560 / 58,400: 43.5 | 118,784 / 58,400: 43.5 | |
| 8x8/1if | platform | 56 | 129,720 / 97,264: 56.0 | 129,928 / 97,264: 56.0 | 1,144 B |
| 8x8/2if | platform | 60.5 | 131,256 / 114,224: 60.5 | 131,464 / 114,224: 60.5 | 1,656 B |

- #894's cut adds 224 B of rom to each 1x1 image and 208 B to each 8x8 one, no sram; no image moves to another granule.
- The pace and THE TRANSMIT restatements of round 5 left every image's linked ROM and SRAM sizes unchanged; this round's own commits change no firmware.

## What did not run

At the stop, by the assignment's stop rule:
- the gates and the full pass at the head, every hosted job step locally, and the Verilator sweep;
- the CPU budget harness at the final head (its firmware is the merge's, measured above);
- 8x8/2if's arm A, `answering-every-port`, `valid-destinations` and arm B legs. Arm A's first part was stopped after the stop's two triggers were settled at 1x1/1if: restating can only raise a cost, and the rows only grow with their costs. Only `datapath-events` ran at 8x8/2if, for R835-3-F2.

Run at the merge: the workflows' check scripts that a sync can break (`check_py_idiom.py`, `check_cpp_idiom.py`, doc paths and style, hygiene, solution docs, feature status), and `docs_check.py` at the head (0 findings).

## Description

### Validity and the declarations (rounds 1 and 2, unchanged)

A source declares its MSRP Talker only while its SRP parameters are valid: MAAP holds its destination, and a probe of the last 15 s or a registered Listener asks for it (Milan v1.2 4.3.3.1, 5.3.7.4).
- It declares at once, Talker Advertise with base + n and its TSpec, or Talker Failed (code 1) when its bandwidth does not fit.
- A lapse withdraws it, its licence and TALKER_DECL bit first. A Leave lwSRP refuses stays owed until lwSRP takes it.
- An unchanged destination is declared again at once. A changed one waits two LeaveAllTime periods after the Leave (IEEE 802.1Q-2018 35.2.2.8, Table 10-7), plus a JoinTime and THE TRANSMIT's MRPDU by every source (`SRP_REDECLARE_CS`, 2,023 cs at one interface, 2,029 at two).

Under THE TIERS, the declarations ride THE TRANSMIT's slices; the Talker's licence still waits for the MVRP commit (Milan v1.2 4.3.2).

### Each source's stream_id (#905, unchanged)

The MAAP adapter (`maap_mbx.c`), which owns `DA_GATE`, writes each source's `SRC_SID_HI:SRC_SID_LO` through `mbx_pub_src_sid` while its gate bit is clear (`KL_mbx_pkg.sv:345`): every source's at its start, and again before each reopening.

## Authoritative references

- #895 rulings issuecomment-6876349305 (rounds 5 and 6, its stops), 6864645058, 6857334948. #894 issuecomment-6878532871 (round 11's class split), 6872978311 (`DATAPATH_US` by `eventcost.py`), rulings 6867990126 (the egress bounds), 6870437042, 6845846512 (the slice rule), 6844175391.
- IEEE 1722.1-2021 9.3.2.6; IEEE 802.1Q-2018 10.7.11, 35.2.2.8, Tables 10-5 to 10-7; Milan v1.2 4.2.7.1.1 (Table 4.3), 4.3.2, 4.3.3.1, 5.3.7.4.
- `docs/design/SPLIT_CONTROL_MEMORY.md` sections 5 and 13 ("The composition measured again (#895)"); FR_NFR.md 3.4.1; `tb/verilator/ctrl_service_budget/poll_grade.py`, `load_grade.py`, `rows_tiers.py`; `sw/firmware/ctrl/loop/ctrl_loop.h` (`CTRL_LOOP_SLICE_US`).

## How to validate

```sh
git checkout bf0844f1 && git submodule update --init --recursive
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if   # rc 1: last 134.94 over 130 (R4 13.11, txL 48.32, tx 33.64)
python3 -B tb/verilator/ctrl_service_budget/tier_grid.py --point 1x1/1if            # rc 0: 12 of 420, CHOSEN 950 us
python3 -B tb/verilator/ctrl_service_budget/rows_tiers.py --selftest               # rc 1: 1031 of 1032, the built slice not the rule's
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check                   # rc 0: 0.517 / 0.513
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --selftest                # rc 1: 584 of 585, AECP_QUEUED_MS not its row's rule
```

## Known limitations / out of scope

- **The slice at 1x1/1if** is the maintainer's: the built 900 us holds every row but the last queued notice (134.94 ms of 130); the rule's 950 us holds every row (+0.0129). No slice is chosen here.
- **Layout sensitivity (#909):** a pass's events' fixed part rose with the cut's placement, restated by the rule, not chased.
- **The platform's 8x8/2if image** has 1,656 B of rom at its 60.5 cap.
- **Found before, for their own issues:** srptx `[TIME]` (#906) and the hold `[TX]` path (#907).
- **8x8/1if** is lane 894b's. The bench run (#895 acceptance 6, #905 acceptance 4) is the bench lane's.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (acceptance 4 composed fails at the restated tables: the stop)
- [ ] Required tests and local gates pass at the exact head (not run: the stop)
- [ ] Current PR head has a successful `rtl-fast` verdict
- [ ] Exact-head `verilator-suites` and `yosys-portability` after ready
- [x] No undocumented requirement/interface change
- [ ] Internal cleared-context review POSITIVE at the exact head
- [ ] External review POSITIVE at the exact head
- [ ] Every review lens covered clean at the merge candidate
- [ ] Candidate merge validated, post-merge containment clean
