[A775]

## Contents

- **[Status](#status)** — Round 8 stopped at its head: 8x8/2if's THE TRANSMIT figure by the rule would move the Talker's hold-off at two interfaces.
- **[Linked Issue / roles](#linked-issue--roles)** — Public tasks, executor, and independent reviewers.
- **[Rounds 6 to 8](#rounds-6-to-8)** — Each commit since round 5's head and what it answers.
- **[The reviews' findings](#the-reviews-findings)** — R835-3 and R836-3, finding by finding.
- **[The rulings](#the-rulings)** — The rulings on rounds 6 and 7B's stops, item by item.
- **[The 1x1/1if rows at the head](#the-1x11if-rows-at-the-head)** — Every row by every source with its margin, the slice rule, the pace, `tier_grid.py`, the load and the 140 ms per-pass cost.
- **[Every stated cost against the head's legs](#every-stated-cost-against-the-heads-legs)** — The survey at both points, the restatements, the polls' base attributed.
- **[The CPU budget harness](#the-cpu-budget-harness)** — Every arm at both points on the rebuilt image.
- **[Image identity and ROM](#image-identity-and-rom)** — The sync by hash, every point at its entry.
- **[What did not run](#what-did-not-run)** — The gates, the full pass and the sweep, at the stop.
- **[Description](#description)** — The validity gate and the declarations, and each source's stream_id (#905).
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this does not do.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

**STOP** at `f93317cb` (`895-talker-redeclare` -> `dev-soft-core`), round 8 (#895 issuecomment-6892130675's stop list; the stop is issuecomment-6895274375). The decision is the maintainer's.

- **Round 7A** built the slice rule's choice, 950 us; every 1x1/1if row held.
- **Round 7B** merged #902's round-13 head and made the ruling's one behaviour-neutral cut. The last queued notice was then 135.43 ms at 950 us, over 130 at every slice in the ruled range, and the round stopped.
- **Round 8** carries out the ruling on that stop:
  - the bound follows its row to **140 ms**;
  - the slice rule chooses **900 us** there, which the loop is built at;
  - the merge of #902's `b6f5c638` changes no image of this branch, by hash;
  - every leg runs again on the rebuilt image at both points.
- **Every 1x1/1if row holds by every source** at the head, the 1x1/1if survey is UNDER 0, and the bound and the slice settle after the one rebuild.
- **The stop:** with 8x8/2if's costs restated by the rule, its tx row is 104.25 ms. By the rule its `CTRL_LOOP_TX_MS` would be 105, which moves `SRP_REDECLARE_CS` at two interfaces from 2,029 to 2,030 cs: a wire-visible change. It is not restated.
- The gates, the full pass and the sweep did not run.

No rebase, no force, no amend. No RTL, mailbox-contract, tsn-c-stack, lwSRP or donor change. This branch's firmware changes since round 6 are three:
- 7B's one behaviour-neutral cut;
- the bound, `AECP_QUEUED_MS`, 140 at one interface;
- the slice, `CTRL_LOOP_SLICE_US`, 900 at one interface.

## Linked Issue / roles

Relates to #895
Relates to #905 (acceptance 1 to 3 and 5 here; 4 is the bench run)
Relates to #894 (#902 merged here at `b6f5c638`; its names patch carried unchanged)
Relates to #906, #907 (srptx findings, not fixed here)
Relates to #908 (the last queued notice over 125 ms)
Relates to #909 (the code and data placement the merges and the cut move, named, not chased)
Relates to #890 (8x8/2if's share), #872 (the second-hart study, should the last queued notice pass 140 ms)
Relates to #665

Executor: `[A775]`
Internal cleared-context reviewer: `[R835]` (R835-3, started issuecomment-6881026642)
External reviewer: `[R836]` (R836-3, issuecomment-6881271637)

## Rounds 6 to 8

| Commit | Round, item | What |
|---|---|---|
| `df0bc467` | 6, 1 | Merge #902's `9606b3a9` (#894's round 11). |
| `3024e740` | 6, 2 | The polls' base at 1x1/1if 205 -> 215 us and a pass's events' fixed part 30 -> 35 us, both columns. |
| `bf0844f1` | 6 | Section 13, section 5, FR_NFR 3.4.1, READMEs; R836-3-F1 and both RS1s. |
| `ff943513`, `6d79b352` | 7A, 1 | The slice at the rule's 950 us (dropped at 7B's merge for #902's own). |
| `58c99c67`, `4c9757ee` | 7A | 8x8/2if MAAP's timer slot 215 -> 225 us; section 13 "The rule's slice built (#895)". |
| `7e3db6b9` | 7B | Merge #902's `234bc149` (the SET_CONFIGURATION cut, the slice at 950 us, `CTRL_LOOP_SRP_UNIT_US` 280); #902's slice code taken. |
| `f14e56a9`, `1a917cf1` | 7B, 3 | The one behaviour-neutral cut: `srp_mbx_gate` returns at once on the gate and base its last call left; plant `talker-gate-repeat-ignores-its-base`. |
| `2657af21`, `0c93071e` | 7B | The polls' base 215 -> 225 us (`save-held`, 21,094 cycles); section 13 "The composition with #894's SET_CONFIGURATION cut (#895)". |
| `1143e3f5` | 8, sync | Merge #902's `b6f5c638` (`CTRL_LOOP_TX_MS` 99 at two interfaces). |
| `2b7f8428` | 8, 1 | `AECP_QUEUED_MS` at one interface 130 -> 140, the queued rule's figure for its row; FR_NFR 3.4.1 amended, the row against 125, 130 and 140. |
| `73388996` | 8, 4 | The slice at the rule's choice at the 140 ms bound, 900 us. |
| `b69388c7` | 8, 7 | 8x8/2if, reported: the polls' base 325 -> 345, a notice past `AECP_FAN_BYTES` 655 -> 700, a pass's events' fixed part 35 -> 40, AMAP_LIVE_WRITE 25 -> 30 us. |
| `f93317cb` | 8 | Section 13 "The bound and the slice at 140 ms (#895)", FR_NFR 3.4.1, the SRP README. |

## The reviews' findings

| Finding | Severity / lens | Answer at this head |
|---|---|---|
| R835-3-F1: the 1x1/1if polls' base stated at 205 us against 20,456 cycles | MAJOR; Conformance, RTL, Tests, Docs | **Restated, and every stated table surveyed at both points at each image.** The base is now 225 us (21,094 cycles in `save-held` on the cut's image, unchanged on the rebuilt one). The survey is UNDER 0 at both points at the head. Its attribution: on #902's own image the heaviest base is 19,074 cycles; the merges' growth is placement (#909), in AECP's poll and delivery, not in the Talker's polls. |
| R835-3-F2: 8x8/2if AMAP_LIVE_WRITE stated at 25 us | MINOR; Conformance, Tests | **Restated by the rule at this head:** 2,465 cycles on the rebuilt image, 30 us (`b69388c7`). It was 2,367 at round 6's head, within 25 then. |
| R835-3-RS1: the roles lines | RESIDUE; Docs | Taken, as worded (above). |
| R835-3-S1: `maap_mbx_start`'s written mark | SUGGESTION; Robustness | Retained, not taken. |
| R835-3-S2: a cost audit against every table at each re-measure | SUGGESTION; Tests | Taken as evidence: `costs_vs_stated.py` before and after each restatement, at every image (round packets). |
| R835-3-S3: section 5's title against its deltas' base | SUGGESTION; Docs | Taken. |
| R835-2-S2 = R836-3-S5: the INDEX hashed before the scrub | SUGGESTION; Docs | Taken: each round's INDEX is generated after the scrub and checked. |
| R836-3-F1: the closing R4 figure 12.85 ms | MINOR; Docs | Taken: the closing summary is this head's, R4 13.25 ms by every source at 900 us. |
| R836-3-RS1: "move no byte" | RESIDUE; Docs | Taken, as worded. |
| R836-3-S1 to S4 | SUGGESTION | Retained, optional. The cut's plant adds one Talker row, 35 in all. |

## The rulings

| Ruling, item | Answer |
|---|---|
| issuecomment-6886630886 (round 6's stop), 1: the slice as the rule's choice | 7A built 950 us. 7B took #902's 950 us at the merge. Round 8 builds the rule's 900 us at the new bound (`73388996`). |
| same, 2 and 3: the 130 ms bound kept; the one cut if no slice holds | 7B made the one cut (`f14e56a9`). After it no slice in 650 to 1,100 us held at 130, and 7B stopped. |
| same, 6 and 7: 7A and 7B, the order | Done; #902 first. |
| issuecomment-6892130675 (7B's stop), 1: the bound follows its row in #901 | `2b7f8428`: 140 ms for the row's 135.43 at 950 us (136.65 at 900); FR_NFR 3.4.1 amended against 125, 130 and 140. |
| same, 2: #902 untouched | No change to #902's code. Its head keeps 130. |
| same, 3: `CTRL_LOOP_TX_MS` by the rule at both points, `SRP_REDECLARE_CS` unchanged | At 1x1/1if the rule gives the stated 34 (tx 34.00 at 900 us) and the hold-off stays 2,023 cs. **At 8x8/2if the rule gives 105 (tx 104.25), which would move the hold-off to 2,030 cs: the stop.** |
| same, 4: the slice rule chooses again; the pace by its rule | 900 us (+0.0086); pace 9 ms. |
| same, 5: no second cut, no placement chase | None. |
| same, 7: rebuild, every leg, the survey, the full pass, the margins and the 140 ms per-pass cost | Rebuild, legs, survey, margins and the per-pass cost are done (below). The full pass did not run (the stop). |
| same, 8: #902's merged images by hash | 552 of 552 image files identical across the sync (`receipts/identity`); #894's own 332 of 332 `b6f5c638` against `234bc149`. |

## The 1x1/1if rows at the head

By every source, ms (`flip_grade.py --check --point 1x1/1if` at `f93317cb`: PASS), at the built and ruled 900 us, the last queued notice's bound at 140 ms:

| Row | W | Bound | Margin | Relative |
|---|---:|---:|---:|---:|
| R4 | 13.25 | 20 | 6.75 | +0.3375 |
| R5 | 75.84 | 90 | 14.16 | +0.1573 |
| R6 | 73.36 | 90 | 16.64 | +0.1849 |
| first queued notice | 14.72 | 20 | 5.28 | +0.2640 |
| last queued notice | 136.65 | 140 | 3.35 | +0.0239 |
| R4L | 203.57 | 238 | 34.43 | +0.1447 |
| ACMP | 29.63 | 30 | 0.37 | +0.0123 |
| ADP | 27.86 | 30 | 2.14 | +0.0713 |
| MAAP | 27.96 | 30 | 2.04 | +0.0680 |
| tx | 34.00 | 49 (`CTRL_LOOP_TX_MS` 34) | 15.00 | +0.3061 |
| txL | 48.58 | 49 | 0.42 | +0.0086 |

- **The slice rule:** 900 us at +0.0086 (txL binding); 950 us is +0.0076, 1,000 us +0.0065, and 1,050 and 1,100 fail. `ruled` = built = 900. `tier_grid.py`: 6 of 420 hold, CHOSEN the built design.
- **The pace:** 9 ms (txL 49.99 at 8).
- **The load:** 0.517 at the pin, 0.514 with tsn-c-stack#32, 0.696 with every command the largest legal one.
- **The 140 ms per-pass cost:** a pass's own cost is 260 us, a pass's events' fixed part (35) plus its polls' base (225). The last queued notice holds 140 ms up to **278 us** (137.93 ms). At **279 us** it is 141.36 ms and txL 49.02, both over (`per_pass_threshold.py`).
- **Self-tests at the head:** `rows_tiers.py --selftest` 1032 of 1033; the one refusal is "THE TRANSMIT's stated figure under its row", 8x8/2if's 99 against 104.25, the stop. `flip_grade.py --selftest` 585 of 585, `load_grade.py --selftest` 26 of 26.
- **8x8/2if, reported:** R4 45.06, R5 209.00, R6 198.71, first 21.11, last 857.77, R4L 211.08, ACMP 68.94, tx 104.25, txL 466.85; load 0.798 / 0.756.

## Every stated cost against the head's legs

`costs_vs_stated.py` holds every table the rows read by the rule over the legs:
- `load_grade.py`'s two columns, `poll_grade.STATED_US` and `whole_grade.stated_us`;
- `rows_grade.ROW_COSTS`, `rows_tiers.DATAPATH_US`, `LONG_NOTICE_US` and `LONG_RECORD_US`;
- `edit_rows.EDIT_RECORD_US`.

| Point | At the rebuilt image's tables (`73388996`) | At the head |
|---|---|---|
| 1x1/1if | UNDER 0: every cost the cut image's but event counts; the base 21,094 (225), the fixed part 2,715 (within 35) | UNDER 0 |
| 8x8/2if | UNDER 7: the base 32,705 (345; 325), a notice past `AECP_FAN_BYTES` 66,481 (700; 655), the fixed part 3,437 (40; 35), AMAP_LIVE_WRITE 2,465 (30; 25) | UNDER 0 (`b69388c7`) |

## The CPU budget harness

Every group of every arm at both points on a clean clone of `73388996`, whose firmware is the head's:

| Point | Arm | Groups | Refusals | Budget misses | `STATED` | rc |
|---|---|---:|---:|---|---:|---:|
| 1x1/1if | A (5 parts, merged) | 96 | 0 | 7 of 950 | 0 | 0 |
| 1x1/1if | `answering-every-port`, `valid-destinations`, B | 16, 2, 3 | 0 | 0 | 0 | 0 |
| 8x8/2if | A (5 parts, merged) | 94 | 0 | 7 of 994 | 0 | 0 |
| 8x8/2if | `answering-every-port` | 16 | 0 | 0 | 16 (the base) | 1; **0 regraded** at `b69388c7` |
| 8x8/2if | `valid-destinations` | 2 | 0 | 0 | 0 | 0 |
| 8x8/2if | B | 3 | 0 | 0 | 2 (the long notice) | 1; **0 regraded** at `b69388c7` |

- **Joins:** 359 at 1x1/1if (188.102 to 190.121 ms) and 750 at 8x8/2if (185.605 to 190.228), every one within 181 to 239.
- **The misses** are arm A's seven held-egress rows at each point, as before.
- **8x8/2if's share:** two passes of `answering-every-port` (at most 2.018 ms) and two of arm B's `aecp-largest-notice` (2.337 ms) are over the per-pass share. They are reported and belong to #890.

## Image identity and ROM

`image_sha.py` hashes every image `ledger.sh` links: each ELF's loadable bytes and every object.
- **7B's cut head `1a917cf1` against the sync merge `1143e3f5`:** 552 of 552 identical.
- **The merge against `73388996`:** 16 differ, every one a one-interface `ctrl_loop.o` or its ELF. No two-interface image changed.

ROM at the head (`plat_ledger.py` PASS):

| Point | Image | Entry or budget | rom / sram, RAMB36 | Left |
|---|---|---:|---|---:|
| 8x8/2if | platform | 60.5 | 131,752 / 114,224: 60.5 | 1,368 B |
| 8x8/2if | fixture | 59.0 | 126,608 / 113,248: 59.0 | 368 B |
| 8x8/2if | harness `answering-every-port` | 59.0 | 126,916 / 113,312: 59.0 | 60 B |
| 8x8/2if | harness `valid-destinations` | 59.0 | 126,776 / 113,248: 59.0 | 200 B |
| 8x8/1if | platform | 56 | 130,200 / 97,328: 56.0 | 872 B |
| others | | 56 | within | |

## What did not run

At the stop: the gates, the full pass on a clean clone, the four-shard sweep, the firmware campaigns and every hosted job step. Run on clean clones:
- the graders, the self-tests, and the doc and idiom checks at the head (`docs_check.py`: 0 findings);
- the surveys and the ledgers;
- in 7B, the firmware arms for the cut and its plant.

## Description

### Validity and the declarations (rounds 1 and 2, unchanged)

A source declares its MSRP Talker only while its SRP parameters are valid: MAAP holds its destination, and a probe of the last 15 s or a registered Listener asks for it (Milan v1.2 4.3.3.1, 5.3.7.4).
- It declares at once, Talker Advertise with base + n and its TSpec, or Talker Failed (code 1) when its bandwidth does not fit.
- A lapse withdraws it, its licence and TALKER_DECL bit first.
- An unchanged destination is declared again at once. A changed one waits two LeaveAllTime periods after the Leave (IEEE 802.1Q-2018 35.2.2.8, Table 10-7), plus a JoinTime and THE TRANSMIT's MRPDU by every source: `SRP_REDECLARE_CS`, 2,023 cs at one interface and 2,029 at two.
- `srp_mbx_gate` returns at once on the gate and base its last call left (7B's cut).

### Each source's stream_id (#905, unchanged)

The MAAP adapter (`maap_mbx.c`), which owns `DA_GATE`, writes each source's `SRC_SID_HI:SRC_SID_LO` through `mbx_pub_src_sid` while its gate bit is clear (`KL_mbx_pkg.sv:345`).

## Authoritative references

- #895 rulings issuecomment-6892130675 (round 8), 6886630886 (round 7), 6876349305. #894 issuecomment-6888782796 (its round 13), 6872978311, 6867990126, 6845846512, 6862465874 (the queued bound's rule).
- IEEE 1722.1-2021 9.3.2.6; IEEE 802.1Q-2018 10.7.11, 35.2.2.8, Tables 10-5 to 10-7; Milan v1.2 4.2.7.1.1 (Table 4.3), 4.3.2, 4.3.3.1, 5.3.7.4.
- `docs/design/SPLIT_CONTROL_MEMORY.md` section 13 ("The bound and the slice at 140 ms (#895)"); FR_NFR.md 3.4.1; `sw/firmware/ctrl/loop/ctrl_loop.h` (`CTRL_LOOP_SLICE_US`, `CTRL_LOOP_TX_MS`); `sw/firmware/ctrl/aecp/aecp_mbx.h` (`AECP_QUEUED_MS`); `sw/firmware/ctrl/srp/srp_mbx.c` (`SRP_REDECLARE_CS`); `tb/verilator/ctrl_service_budget/queued_bound.py`, `rows_tiers.py`.

## How to validate

```sh
git checkout f93317cb && git submodule update --init --recursive
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if   # rc 0: last 136.65 of 140, ACMP 29.63, txL 48.58
python3 -B tb/verilator/ctrl_service_budget/tier_grid.py --point 1x1/1if            # rc 0: 6 of 420, CHOSEN the built 900 us
python3 -B tb/verilator/ctrl_service_budget/rows_tiers.py --selftest               # rc 1: 1032 of 1033, 8x8/2if's THE TRANSMIT figure
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check                   # rc 0: 0.517 / 0.514
```

## Known limitations / out of scope

- **The stop** (above): 8x8/2if's `CTRL_LOOP_TX_MS` by the rule, and with it the Talker's hold-off at two interfaces.
- **The margins:** ACMP has 0.37 ms and txL 0.42 ms left at 1x1/1if; the last queued notice passes 140 ms at a pass's own cost of 279 us (260 now).
- **Layout sensitivity (#909):** the polls' base and the 8x8/2if costs move with code placement; restated by the rule, not chased.
- **The ROM:** the `answering-every-port` 8x8/2if harness arm has 60 B left at 59.0 (graded in #898's composed check).
- **Found before, for their own issues:** srptx `[TIME]` (#906) and the hold `[TX]` path (#907).
- **8x8/1if** is lane 894b's. The bench run (#895 acceptance 6, #905 acceptance 4) is the bench lane's.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (acceptance 4 composed holds at 1x1/1if; the stop is 8x8/2if's hold-off)
- [ ] Required tests and local gates pass at the exact head (not run: the stop)
- [ ] Current PR head has a successful `rtl-fast` verdict
- [ ] Exact-head `verilator-suites` and `yosys-portability` after ready
- [x] No undocumented requirement/interface change
- [ ] Internal cleared-context review POSITIVE at the exact head
- [ ] External review POSITIVE at the exact head
- [ ] Every review lens covered clean at the merge candidate
- [ ] Candidate merge validated, post-merge containment clean
