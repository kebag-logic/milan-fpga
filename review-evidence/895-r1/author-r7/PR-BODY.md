[A775]

## Contents

- **[Status](#status)** — Round 7B stopped: after the one cut no slice from 650 to 1,100 us holds every 1x1/1if row.
- **[Linked Issue / roles](#linked-issue--roles)** — Public tasks, executor, and independent reviewers.
- **[Rounds 6 and 7](#rounds-6-and-7)** — Each commit since round 5's head and what it answers.
- **[The reviews' findings](#the-reviews-findings)** — R835-3 and R836-3, finding by finding.
- **[Every stated cost against this head's legs](#every-stated-cost-against-this-heads-legs)** — The survey at both points, the restatements, and the polls' base attributed.
- **[The 1x1/1if flip check](#the-1x11if-flip-check)** — Every row by every source at 950 us, the slice rule, the pace, `tier_grid.py` and the load.
- **[The CPU budget harness](#the-cpu-budget-harness)** — Every arm at both points on the image with the rule's slice.
- **[ROM ledger](#rom-ledger)** — Every point, at its entry.
- **[What did not run](#what-did-not-run)** — The gates, the full pass and the sweep, which are 7B's.
- **[Description](#description)** — The validity gate and the declarations, and each source's stream_id (#905).
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this does not do.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

**STOP** at `0c93071e` (`895-talker-redeclare` -> `dev-soft-core`), round 7B (#895 issuecomment-6886630886's stop list; the stop is #895 issuecomment-6892087027): after the ruling's one cut, no slice from 650 to 1,100 us holds every 1x1/1if row. The decision is the maintainer's.

- **Round 6** merged #902's `9606b3a9`, restated two costs by the rule, and stopped: at 900 us the last queued notice was 134.94 ms.
- **Round 7A** built the slice rule's choice, 950 us. Every 1x1/1if row held on the rebuilt image, with the last queued notice at 127.83.
- **Round 7B** merged #902's round-13 review head `234bc149`, taking #902's slice code for this branch's own. At the composed tables no slice in the ruled range holds every row: the last queued notice is 134.74 ms at 950 us.
  - The polls' base is 20,453 cycles on the merge's image against 19,074 on #902's own. The growth is in AECP's poll and delivery (placement, #909), not in the Talker's polls.
  - The ruling's one behaviour-neutral cut (item 3) took 717 cycles from that pass. On the cut's image `save-held`'s base is 21,094 cycles, 225 us by the rule.
  - At the final tables the last queued notice is 135.43 ms at 950 us, and over 130 at every slice from 650 to 1,100.
- The gates, the full pass and the sweep did not run (the stop).

No rebase, no force, no amend. No RTL, mailbox-contract, tsn-c-stack, lwSRP or donor change; the one firmware change of this branch's own in round 7 is the cut, behaviour-neutral. No bound, ceiling, pace or the every-source rule moves.

## Linked Issue / roles

Relates to #895
Relates to #905 (acceptance 1 to 3 and 5 here; 4 is the bench run)
Relates to #894 (#902 merged here at `234bc149`; its names patch carried unchanged)
Relates to #906, #907 (srptx findings, not fixed here)
Relates to #909 (the code and data placement the merges move, named, not chased)
Relates to #890 (8x8/2if's share)
Relates to #896
Relates to #665

Executor: `[A775]`
Internal cleared-context reviewer: `[R835]` (R835-3, started issuecomment-6881026642)
External reviewer: `[R836]` (R836-3, issuecomment-6881271637)

## Rounds 6 and 7

| Commit | Round, item | What |
|---|---|---|
| `df0bc467` | 6, item 1 | Merge #902's `9606b3a9` (#894's round 11: the one-row map edit's cut, its edits a class of their own at 260 / 325 us). In `load_grade.py` each cost is the side's that moved it from the merge base `7398ec0a`, the larger where both did; FR_NFR 3.4.1, the SRP README and section 13 carry both sides' text. |
| `3024e740` | 6, item 2 | The polls' base at 1x1/1if goes 205 -> 215 us (`poll_grade.STATED_US`, `load_grade.STATED_US_DONOR`), and a pass's events' fixed part 30 -> 35 us (both columns), each its measurement by the rule. |
| `bf0844f1` | 6, items 2-4 | Section 13 "The composition measured again (#895)", section 5's plan with the cut's 208 to 224 B, FR_NFR 3.4.1, the READMEs, R836-3-RS1's wording. |
| `ff943513` | 7A, item 1 | The built 1x1/1if slice is the slice rule's choice at the restated tables: `CTRL_LOOP_SLICE_US` 900 -> **950 us**. `ctrl_loop.h` states the rule. The self-tests hold the figure: `rows_tiers.py`'s tree control refuses the 900 us header ("the built design's slice not the rule's"), and `selftest_round.py` holds 950 / 1,300. |
| `6d79b352` | 7A | `rows_tiers.py` back within the 1,000-line module ratchet (a comment on two lines). |
| `58c99c67` | 7A, item 2 | MAAP's timer slot at 8x8/2if goes 215 -> 225 us in both columns: 21,120 CPU cycles in arm A's `save` group, by the rule. |
| `4c9757ee` | 7A | Section 13 "The rule's slice built (#895)", the tiers table, the tx paragraph, the pace table and the closing summary at 950 us; FR_NFR 3.4.1; the SRP README. |
| `7e3db6b9` | 7B, item 1 | Merge #902's `234bc149` (#894's SET_CONFIGURATION cut, the slice at the rule's 950 us, `CTRL_LOOP_SRP_UNIT_US` 280, a build of one 735). #902's slice code is taken for this branch's (#894 issuecomment-6888782796, item 2), so `ff943513`'s and `6d79b352`'s duplicates are dropped; each cost is the side's that moved it from `9606b3a9`, the larger where both did; the pace stays 9, the rule's at the composed tables. |
| `f14e56a9` | 7B, item 3 | The one cut: `srp_mbx_gate` returns at once on the gate and base its last call left (`gate_seen`, `gate_base`), exactly behaviour-neutral, with plant `talker-gate-repeat-ignores-its-base` (35 Talker plants) and the SRP README. |
| `1a917cf1` | 7B | `rows_tiers.py`'s control comment back to #902's: the file equals #902's. |
| `2657af21` | 7B, item 2 | The polls' base at 1x1/1if 215 -> 225 us, both tables: 21,094 cycles in `save-held` on the cut's image, by the rule. |
| `0c93071e` | 7B | Section 13 "The composition with #894's SET_CONFIGURATION cut (#895)", the tiers and pace tables, the closing summary; FR_NFR 3.4.1; the SRP README. |

## The reviews' findings

| Finding | Severity / lens | Answer at this head |
|---|---|---|
| R835-3-F1: the 1x1/1if polls' base stated at 205 us against 20,456 cycles (215 by the rule) | MAJOR; Conformance, RTL, Tests, Docs | **Restated, and every stated table surveyed at both points** ([below](#every-stated-cost-against-this-heads-legs)). The base (20,282 cycles, 215 us) and a pass's events' fixed part (3,041 cycles, 35 us) at 1x1/1if, and MAAP's timer slot at 8x8/2if (21,120 cycles, 225 us), are restated in both columns; the survey is UNDER 0 at both points. The base over 205 is this lane's Talker work: #894's own image measures 18,843 cycles (200 us). At the restated tables the slice rule took 950 us; by the ruling on round 6's stop the loop is built at it (7A: every row held). 7B's composition with #894's SET_CONFIGURATION cut moves the base again (215, then 225 after the one cut, `save-held`), and no slice in the ruled range holds every row: the stop. |
| R835-3-F2: 8x8/2if AMAP_LIVE_WRITE stated at 25 us against 2,426 cycles (30 by the rule) | MINOR; Conformance, Tests | **Shown within.** The `datapath-events` group at 8x8/2if measures its take and sinks at 2,367 cycles, 23.67 us, within the 23.80 that 25 holds, by `eventcost.py`, the measure #894 states `DATAPATH_US` by (#894 issuecomment-6872978311); both interfaces at this head. |
| R835-3-RS1: the roles lines | RESIDUE; Docs | Taken, as worded (above); the external line names R836-3. |
| R835-3-S1: `maap_mbx_start`'s written mark before a first opening | SUGGESTION; Robustness | Retained, not taken: no SRP or MAAP code change. |
| R835-3-S2: a cost audit against every table at each re-measure | SUGGESTION; Tests | Taken as evidence: `costs_vs_stated.py` over each round's legs against every table the rows read, before and after each restatement. Not added to the tree. |
| R835-3-S3: section 5's table title against its deltas' base | SUGGESTION; Docs | Taken: each delta names its base. |
| R835-2-S2 = R836-3-S5: the INDEX hashed before the scrub | SUGGESTION; Docs | Taken: the INDEX is generated after the scrub and checked (a second scrub changes nothing; every hash is its file's). |
| R836-3-F1: the closing R4 figure 12.85 ms | MINOR; Docs | Taken: the closing summary is this head's, R4 13.30 ms by every source at 950 us and the last queued notice 135.43 (`flip_grade.py --check --point 1x1/1if`); the present-tense references that pointed at the tiers table name their heads. |
| R836-3-RS1: "move no byte" | RESIDUE; Docs | Taken, as worded: "The pace and THE TRANSMIT restatements leave every image's linked ROM and SRAM sizes unchanged" in sections 13 and 5. |
| R836-3-S1 to S4 (= R836-1-S2, S3; R835-1-S1 = R835-2-S3; R835-2-S1) | SUGGESTION | Retained, optional: no SRP code change. |

## Every stated cost against this head's legs

The survey (`costs_vs_stated.py`) reads each table from the tree and holds each key by the rule to the most measured over the legs. The measures are round 1's parsers, the harness's own heaviest and `record_classes.py`'s classes. The tables are `load_grade.py`'s two columns, `poll_grade.STATED_US`, `whole_grade.stated_us`, `rows_grade.ROW_COSTS`, `rows_tiers.DATAPATH_US`, `LONG_NOTICE_US` and `LONG_RECORD_US`, and `edit_rows.EDIT_RECORD_US`.

| Cost | Most measured, CPU cycles | Rule | Before | Now |
|---|---:|---:|---:|---:|
| 1x1/1if the polls' base | 20,282 (`acmp-cmd`, round 6) / 21,094 (`save-held`, the cut's image) | 215 / 225 | 205 | **225** (`2657af21`) |
| 1x1/1if a pass's events' fixed part (`notice-burst-0`) | 3,041 (round 6) | 35 | 30 | 35 (round 6; 2,449 on the cut's image) |
| 8x8/2if MAAP's timer slot (`save`) | 21,120 (7A) | 225 | 215 | 225 (7A) |

- **At the cut's image, 1x1/1if: UNDER 2 before `2657af21`** (the base, both tables) **and UNDER 0 after.** 8x8/2if was last surveyed at 7A (UNDER 0); its legs were not run on the cut's image.
- **The polls' base, attributed** (`acmp-cmd`):
  - #894's `234bc149`: 19,074 cycles (205 by the rule). The merge: 20,453 (215).
  - The +1,379 cycles are AECP's poll (+625) and delivery (+840); the Talker's MAAP poll (−6) and SRP delivery (−290) are cheaper. The pass has +82 instructions and 17 refills fewer: placement (#909).
  - The cut: 19,736 in `acmp-cmd`. But `save-held` is 21,094 (19,793 at 7A), with 262 instructions fewer and 49 more refills.

## The 1x1/1if flip check

By every source, ms (`flip_grade.py --check --point 1x1/1if`):

| Row | Bound | 7A `4c9757ee` (950 us) | 7B composed tables (950 us) | Head `0c93071e` (950 us) |
|---|---:|---:|---:|---:|
| R4 | 20 | 13.16 | 13.25 | 13.30 |
| R5 / R6 | 90 | 74.52 / 72.58 | 74.98 / 73.04 | 75.89 / 73.41 |
| first queued notice | 20 | 14.70 | 14.75 | 14.77 |
| last queued notice | 130 | 127.83 | **134.74** | **135.43** |
| R4L | 238 | 203.58 | 203.59 | 203.62 |
| ACMP / ADP / MAAP | 30 | 29.34 / 27.61 / 27.70 | 29.51 / 27.78 / 27.88 | 29.68 / 27.91 / 28.01 |
| tx | 49 (`CTRL_LOOP_TX_MS` 34) | 33.69 | 33.88 | 34.05 |
| txL | 49 | 48.37 | 48.40 | 48.63 |
| result | | PASS | FAIL | **FAIL** |

- **The slice rule at the head:** no grid slice from 650 to 1,100 us holds every row.
  - The best in that range is 950 us at −0.0418, the last queued notice 135.43 to 167.39 ms across the range.
  - The rule's overall best is 1,200 us at −0.0043, where txL is 49.21.
  - `rows_tiers.ruled` gives 800 (its fallback). `tier_grid.py`: 0 of 420 hold.
- **The pace rule:** 9 ms (txL 52.34 at 8).
- **The load:** 0.517 / 0.514, 0.696 with every notice the largest legal one.
- **The sensitivity** at the composed tables: every row holds at 950 us once the polls' base and a pass's events' fixed part come to 240 us together, and not at 245.
- **Self-tests at the head** (the tree's own controls report the stop):
  - `rows_tiers.py --selftest` 1031/1033: the built slice not the rule's; THE TRANSMIT's stated figure under its row, 34 against 34.05 (98 against 98.99 at 8x8/2if).
  - `flip_grade.py --selftest` 584/585: the queued bound.
  - `load_grade.py --selftest` 26/26.

## The CPU budget harness

| Image | Point | Arm | Groups | Refusals | Budget misses | `STATED` | rc |
|---|---|---|---:|---:|---|---:|---:|
| 7A `6d79b352` | 1x1/1if | A (merged), `answering-every-port`, `valid-destinations`, B | 96, 16, 2, 3 | 0 | 7 of 950 (A) | 0 | 0 |
| 7A `6d79b352` | 8x8/2if | A (merged), `answering-every-port`, `valid-destinations`, B | 94, 16, 2, 3 | 0 | 7 of 994 (A) | 0 | 0 |
| the cut `1a917cf1` | 1x1/1if | A (merged), `answering-every-port`, `valid-destinations`, B | 96, 16, 2, 3 | 0 | 7 of 950 (A) | 0 | 0 |

- **The merge's image `7e3db6b9`:** arm B (rc 0) and `acmp-cmd` alone ran to their end, as did `acmp-cmd` on #902's `234bc149`. The merge's other legs were stopped once the cut superseded them (receipts' `.stopped` files).
- **Joins:** every interval measured is within 181 to 239 ms. 7A: 1,109, 182.679 to 190.642. The cut's image: 359, 188.102 to 190.121.
- **The misses** are arm A's seven `backlog-owed` held-egress rows, as before.
- **7A's 8x8/2if arm B:** `aecp-largest-notice` has two passes over the share, the longest 2.237 ms. It is reported, and belongs to #890.
- **The cut's arms:** talker, srp-acmp-if1/if2, port, portable and unit PASS. Its plant is caught at one interface and two.

## ROM ledger

`plat_ledger.py` PASS (0 findings) and `ctrl_srp_image.py` at the cut's head `1a917cf1`. rom / sram need in B, then RAMB36:

| Point | Image | Entry or budget | 7A `6d79b352` | The cut's head | Left |
|---|---|---:|---|---|---:|
| 1x1/1if | fixture | 56 | 112,152 / 55,184: 41.0 | 112,424 / 55,200: 41.0 | |
| 1x1/2if | fixture | 56 | 113,696 / 57,360: 42.5 | 113,984 / 57,376: 42.5 | |
| 8x8/1if | fixture | 56 | 124,816 / 96,288: 54.5 | 125,088 / 96,304: 55.0 | |
| 8x8/2if | fixture | 59.0 | 126,320 / 113,232: 59.0 | 126,608 / 113,248: 59.0 | 368 B |
| 8x8/2if | harness `answering-every-port` | 59.0 | 126,628 / 113,296: 59.0 | 126,916 / 113,312: 59.0 | 60 B |
| 8x8/2if | harness `valid-destinations` | 59.0 | 126,488 / 113,232: 59.0 | 126,776 / 113,248: 59.0 | 200 B |
| 1x1/1if | platform | 56 | 117,216 / 56,224: 43.0 | 117,488 / 56,224: 43.0 | |
| 1x1/2if | platform | 56 | 118,784 / 58,400: 43.5 | 119,072 / 58,400: 44.0 | |
| 8x8/1if | platform | 56 | 129,928 / 97,264: 56.0 | 130,200 / 97,328: 56.0 | 872 B |
| 8x8/2if | platform | 60.5 | 131,464 / 114,224: 60.5 | 131,752 / 114,224: 60.5 | 1,368 B |

## What did not run

At the stop: the gates, the full pass on a clean clone, the four-shard sweep, the firmware campaigns, and 8x8/2if's legs on the cut's image. Run on clean clones: the graders and the doc and idiom checks at the head (`docs_check.py` 0 findings), the firmware arms on the cut, and the ledgers at the merge and at the cut.

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

- #895 rulings issuecomment-6886630886 (round 7: the slice as the rule's choice, 7A and 7B), 6876349305, 6864645058, 6857334948. #894 issuecomment-6878532871 (round 11's class split), 6872978311 (`DATAPATH_US` by `eventcost.py`), rulings 6867990126 (the egress bounds), 6870437042, 6845846512 (the slice rule), 6844175391.
- IEEE 1722.1-2021 9.3.2.6; IEEE 802.1Q-2018 10.7.11, 35.2.2.8, Tables 10-5 to 10-7; Milan v1.2 4.2.7.1.1 (Table 4.3), 4.3.2, 4.3.3.1, 5.3.7.4.
- `docs/design/SPLIT_CONTROL_MEMORY.md` sections 5 and 13 ("The composition measured again (#895)", "The rule's slice built (#895)"); FR_NFR.md 3.4.1; `sw/firmware/ctrl/loop/ctrl_loop.h` (`CTRL_LOOP_SLICE_US`); `tb/verilator/ctrl_service_budget/rows_tiers.py`, `poll_grade.py`, `load_grade.py`.

## How to validate

```sh
git checkout 0c93071e && git submodule update --init --recursive
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if   # rc 1: last 135.43 over 130 at 950 us
python3 -B tb/verilator/ctrl_service_budget/tier_grid.py --point 1x1/1if            # rc 1: 0 of 420 hold
python3 -B tb/verilator/ctrl_service_budget/rows_tiers.py --selftest               # rc 1: 1031 of 1033
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check                   # rc 0: 0.517 / 0.514
```

## Known limitations / out of scope

- **The stop** (above): no slice in the ruled range holds every 1x1/1if row after the one cut; the maintainer decides.
- **Layout sensitivity (#909):** the polls' base at 1x1/1if (`acmp-cmd`, then `save-held`), a pass's events' fixed part and MAAP's timer slot at 8x8/2if moved with the merges' and the cut's placement, restated by the rule.
- **8x8/2if's share** in arm B's `aecp-largest-notice` (above) is #890's.
- **The ROM:** the harness's `answering-every-port` 8x8/2if arm has 60 B left at 59.0; the platform's 8x8/2if image has 1,368 B at its 60.5 cap.
- **Found before, for their own issues:** srptx `[TIME]` (#906) and the hold `[TX]` path (#907).
- **8x8/1if** is lane 894b's. The bench run (#895 acceptance 6, #905 acceptance 4) is the bench lane's.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (acceptance 4 composed fails at this head: the stop)
- [ ] Required tests and local gates pass at the exact head (not run: the stop)
- [ ] Current PR head has a successful `rtl-fast` verdict
- [ ] Exact-head `verilator-suites` and `yosys-portability` after ready
- [x] No undocumented requirement/interface change
- [ ] Internal cleared-context review POSITIVE at the exact head
- [ ] External review POSITIVE at the exact head
- [ ] Every review lens covered clean at the merge candidate
- [ ] Candidate merge validated, post-merge containment clean
