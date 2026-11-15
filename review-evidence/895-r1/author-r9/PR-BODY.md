[A775]

## Contents

- **[Status](#status)** — Round 9 is review-ready at its head: THE TRANSMIT's figure at two interfaces by the rule, the hold-off following it, #902's round 20 synced, one full pass.
- **[Linked Issue / roles](#linked-issue--roles)** — Public tasks, executor, and independent reviewers.
- **[Rounds 6 to 9](#rounds-6-to-9)** — Each commit since round 5's head and what it answers.
- **[The findings](#the-findings)** — R835-3 and R836-3 finding by finding, and the one this round found in this branch's own evidence.
- **[The rulings](#the-rulings)** — The rulings on rounds 6, 7B and 8's stops, item by item.
- **[The 1x1/1if rows at the head](#the-1x11if-rows-at-the-head)** — Every row by every source with its margin, the per-pass headroom, the slice rule, the pace, the load and the self-tests.
- **[THE TRANSMIT's figure at two interfaces](#the-transmits-figure-at-two-interfaces)** — The figure, the hold-off, the images by hash, the arms and the leg run again.
- **[Every stated cost against the legs](#every-stated-cost-against-the-legs)** — The survey at both points.
- **[The CPU budget harness](#the-cpu-budget-harness)** — Every arm at both points, and why the legs carry.
- **[Image identity and ROM](#image-identity-and-rom)** — Each sync and change by hash, every point at its entry.
- **[The full pass](#the-full-pass)** — Every hosted job step, the campaigns, the lane gates and the sweep at the exact head.
- **[Description](#description)** — The validity gate and the declarations, and each source's stream_id (#905).
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this does not do.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

**REVIEW READY** at `056d619d` (`895-talker-redeclare` -> `dev-soft-core`), round 9 (#895 issuecomment-6895331865, the ruling on round 8's stop issuecomment-6895274375; the REVIEW READY is issuecomment-6899637516).

- **Round 7A** built the slice rule's choice, 950 us; every 1x1/1if row held.
- **Round 7B** merged #902's round-13 head and made the ruling's one behaviour-neutral cut; the last queued notice was then 135.43 ms, over 130 at every slice in the ruled range, and the round stopped.
- **Round 8** moved the bound to its row's **140 ms**, built the slice rule's **900 us** there, and measured every leg again on the rebuilt image. With 8x8/2if's costs restated its tx row is 104.25 ms, and the rule's 105 would move the Talker's hold-off at two interfaces: the round stopped.
- **Round 9** carries out the ruling on that stop:
  - `CTRL_LOOP_TX_MS` at two interfaces is **105 ms**, and `SRP_REDECLARE_CS` there follows to **2,030 cs** (2,029 at 99 ms); one interface keeps 34 ms and 2,023 cs;
  - by sha256 **no one-interface image changes**, and each of the six two-interface images differs from the merge **in one instruction only**, `li a3,2029` to `li a3,2030`, so every leg carries;
  - the two-interface Talker arms and the 8x8/2if `valid-destinations` leg ran again and pass;
  - #902's round-20 heads `41ca9f87` and, as #902 moved during the round, `07ed787e` (docs only) are merged, the images identical by hash;
  - **one full pass** on clean clones of the exact head: every hosted job step (139 ran, 226 not run with a reason, 0 bad), the firmware campaigns (control 716 of 716, AECP 299 and SRP 415 rows, 0 escaped), `fw_coverage.py --check` PASS, every lane gate, and the sweep's 65 suites on four shards, 0 failed. The pass's first run, one head earlier, found the harness self-test's stale bound; it ran again in full at the final head.
- **Found in this branch's own evidence:**
  - `plat_ledger.py` refused 8x8/1if's `ctrl_plat` (18,240 B against the recorded 18,176) since 7B's cut, and round 8's body called it PASS. Fixed (`449d29d2`); no image changes.
  - The full pass's first run, at `c772b1e5`, failed one lane gate: the harness self-test pinned the last queued notice's bound at 130 ms, stale since round 8 moved it to 140 (round 8 ran no gate). Fixed (`249a3823`): the pin is (140, 62) and its over-bound probe 141 ms, as tight as before. The pass then ran again, in full, at the final head.

No rebase, no force, no amend. No RTL, mailbox-contract, tsn-c-stack, lwSRP or donor change. This branch's firmware changes since round 6 are four: 7B's one behaviour-neutral cut; the bound, `AECP_QUEUED_MS`, 140 at one interface; the slice, `CTRL_LOOP_SLICE_US`, 900 at one interface; and THE TRANSMIT's figure, `CTRL_LOOP_TX_MS`, 105 at two interfaces, the one wire change the ruling allows.

## Linked Issue / roles

Relates to #895
Relates to #905 (acceptance 1 to 3 and 5 here; 4 is the bench run)
Relates to #894 (#902, merged into `dev-soft-core` as `659d7687` during round 9, its tree `07ed787e`'s, which this branch merged at `056d619d`; its names patch carried unchanged; `dev-soft-core` states `CTRL_LOOP_TX_MS` 99 and `AECP_QUEUED_MS` 130, which this PR moves to 105 and 140)
Relates to #906, #907 (srptx findings, not fixed here)
Relates to #908 (the last queued notice over 125 ms)
Relates to #909 (the code and data placement the merges and the cut move, named, not chased)
Relates to #890 (8x8/2if's share), #872 (the second-hart study, should the last queued notice pass 140 ms)
Relates to #665

Executor: `[A775]`
Internal cleared-context reviewer: `[R835]` (R835-3, started issuecomment-6881026642)
External reviewer: `[R836]` (R836-3, issuecomment-6881271637)

The ruling asks for two delta reviews from round 5's head `62298ab5`.

## Rounds 6 to 9

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
| `663b519b` | 9, sync | Merge #902's `41ca9f87` (#894's round 20: section 13's history in the past, `aecp_mbx.h` comments, `rows_grade.py`'s docstring). Section 13's three conflicting hunks taken word by word: #902's change wherever this branch left those words unchanged. |
| `845364b6` | 9, 1 | `CTRL_LOOP_TX_MS` at two interfaces 99 -> 105, `SRP_REDECLARE_CS` there 2,029 -> 2,030 cs; the two self-test controls' figure and plants (34/105, under each row 33/104); FR_NFR 3.4.1, section 13 "THE TRANSMIT's figure at two interfaces (#895)", the SRP README, the harness README. |
| `449d29d2` | 9 | `ctrl_memory_ledger.PLAT_8X8_1` 18,176 -> 18,240 B, the 64 B 7B's cut adds at 8x8/1if; section 3. |
| `c772b1e5` | 9 | Section 13: the images by hash, the sync's, the Talker arms, the rows and the ledger. |
| `249a3823` | 9 | The harness self-test's queued bound at 140 ms at one interface (`selftest_notice.py`: the pin (140, 62), the over-bound probe 141 ms), and `ctrl_loop.h`'s comment of it. |
| `056d619d` | 9, sync | Merge #902's `07ed787e` (#894's round 20: sections 5 and 13's image sizes as its head's), docs only; where #902 states its head's sizes this branch states its own (126,608 and 131,752 B). |

## The findings

| Finding | Severity / lens | Answer at this head |
|---|---|---|
| R835-3-F1: the 1x1/1if polls' base stated at 205 us against 20,456 cycles | MAJOR; Conformance, RTL, Tests, Docs | **Restated, and every stated table surveyed at both points at each image.** The base is 225 us (21,094 cycles in `save-held` on the cut's image, unchanged on the rebuilt one). The survey is UNDER 0 at both points at round 8's head, and no measured image and no table has moved since. Its attribution: on #902's own image the heaviest base is 19,074 cycles; the merges' growth is placement (#909), in AECP's poll and delivery, not in the Talker's polls. |
| R835-3-F2: 8x8/2if AMAP_LIVE_WRITE stated at 25 us | MINOR; Conformance, Tests | **Restated by the rule:** 2,465 cycles on the rebuilt image, 30 us (`b69388c7`). It was 2,367 at round 6's head, within 25 then. |
| R835-3-RS1: the roles lines | RESIDUE; Docs | Taken, as worded (above). |
| R835-3-S1: `maap_mbx_start`'s written mark | SUGGESTION; Robustness | Retained, not taken. |
| R835-3-S2: a cost audit against every table at each re-measure | SUGGESTION; Tests | Taken as evidence: `costs_vs_stated.py` before and after each restatement, at every image (round packets). |
| R835-3-S3: section 5's title against its deltas' base | SUGGESTION; Docs | Taken. |
| R835-2-S2 = R836-3-S5: the INDEX hashed before the scrub | SUGGESTION; Docs | Taken: each round's INDEX is generated after the scrub and checked. |
| R836-3-F1: the closing R4 figure 12.85 ms | MINOR; Docs | Taken: the closing summary is the head's, R4 13.25 ms by every source at 900 us. |
| R836-3-RS1: "move no byte" | RESIDUE; Docs | Taken, as worded. |
| R836-3-S1 to S4 | SUGGESTION | Retained, optional. The cut's plant adds one Talker row, 35 in all. |
| Found in round 9 by the executor: `plat_ledger.py` FAIL at 8x8/1if since 7B's cut (`ctrl_plat` 18,240 B, recorded 18,176), reported in round 8's body as PASS | for the reviewers' lens | **Fixed** (`449d29d2`): the record is 18,240. `plat_ledger.py` passes at every point at the head and `test_ctrl_memory.py` passes. The record is read only by those two, so no image changes. Round 8's body was wrong on this line. |
| Found in round 9's first full pass: `tb/verilator/ctrl_service_budget/run.py --self-test` 2 failures at `c772b1e5`, `selftest_notice.queue_checks` pinning the bound at (130, 62) and probing 131 ms as a miss, stale since round 8's `2b7f8428` | for the reviewers' lens | **Fixed** (`249a3823`): the pin (140, 62) and the probe 141 ms, one over the bound as before; 0 failures at the final head. |

## The rulings

| Ruling, item | Answer |
|---|---|
| issuecomment-6886630886 (round 6's stop), 1: the slice as the rule's choice | 7A built 950 us. 7B took #902's 950 us at the merge. Round 8 builds the rule's 900 us at the new bound (`73388996`). |
| same, 2 and 3: the 130 ms bound kept; the one cut if no slice holds | 7B made the one cut (`f14e56a9`). After it no slice in 650 to 1,100 us held at 130, and 7B stopped. |
| same, 6 and 7: 7A and 7B, the order | Done; #902 first. |
| issuecomment-6892130675 (7B's stop), 1: the bound follows its row in #901 | `2b7f8428`: 140 ms for the row's 135.43 at 950 us (136.65 at 900); FR_NFR 3.4.1 amended against 125, 130 and 140. |
| same, 2: #902 untouched | No change to #902's code. Its head keeps 130. |
| same, 3: `CTRL_LOOP_TX_MS` by the rule at both points | At 1x1/1if the rule gives the stated 34 (tx 34.00 at 900 us), the hold-off 2,023 cs. At 8x8/2if it gave 105, which moved the hold-off: round 8's stop, ruled in round 9. |
| same, 4: the slice rule chooses again; the pace by its rule | 900 us (+0.0086); pace 9 ms. |
| same, 5: no second cut, no placement chase | None. |
| same, 7: rebuild, every leg, the survey, the margins and the 140 ms per-pass cost | Done in round 8 (below). The full pass ran in round 9. |
| same, 8: #902's merged images by hash | 552 of 552 image files identical across that sync; #894's own 332 of 332 `b6f5c638` against `234bc149`. |
| **issuecomment-6895331865 (round 8's stop), 1 and 2: (a), the hold-off follows the tx row** | `845364b6`: `CTRL_LOOP_TX_MS` at two interfaces 105, `SRP_REDECLARE_CS` there 2,030 cs; IEEE 802.1Q-2018 35.2.2.8 sets only the least, 2,000 cs, so a changed destination is declared 10 ms later at two interfaces. |
| same, 3: (b) and (c) refused | Neither taken. |
| same, 4: own commit, FR_NFR 3.4.1, section 13, the SRP README; #902 keeps 99 | `845364b6` carries all three; #902 untouched. |
| same, 5: no one-interface image changes, the two-interface ones only in that constant | 0 one-interface files differ; 12 two-interface files, each one instruction ([below](#the-transmits-figure-at-two-interfaces)). |
| same, 5: the two-interface Talker arms and the 8x8/2if `valid-destinations` leg again | PASS (below). |
| same, 5: sync onto #902's current head, image identity | `663b519b` (`41ca9f87`) and `056d619d` (`07ed787e`); 552 of 552 identical across each. |
| same, 5: one full pass on a clean clone | [The full pass](#the-full-pass). |
| same, 5: two delta reviews from round 5's head | For the reviewers, from `62298ab5`. |

## The 1x1/1if rows at the head

By every source, ms (`flip_grade.py --check --point 1x1/1if` at the head: PASS), at the built and ruled 900 us, the last queued notice's bound at 140 ms (`per_pass_threshold.py` on an export of the head):

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

- **The per-pass headroom:** a pass's own cost is **260 us**, a pass's events' fixed part (35) plus its polls' base (225). Every row holds up to **278 us** (the last queued notice 137.93 ms). At **279 us** the last queued notice is 141.36 ms and txL 49.02 ms, both over: 18 us of headroom.
- **The slice rule:** 900 us at +0.0086 (txL binding); 950 us is +0.0076, 1,000 us +0.0065, and 1,050 and 1,100 fail. `ruled` = built = 900. `tier_grid.py`: 6 of 420 hold, CHOSEN the built design.
- **The pace:** 9 ms (txL 49.99 at 8).
- **The load:** 0.517 at the pin, 0.514 with tsn-c-stack#32, 0.696 with every command the largest legal one.
- **Self-tests at the head:** `rows_tiers.py --selftest` **1033 of 1033** (round 8: 1032, the one escape THE TRANSMIT's figure at 8x8/2if); `flip_grade.py --selftest` 585 of 585; `load_grade.py --selftest` 26 of 26.
- **8x8/2if, reported:** R4 45.06, R5 209.00, R6 198.71, first 21.11, last 857.77, R4L 211.08, ACMP 68.94, tx 104.25 (105 stated), txL 466.85; load 0.798 / 0.756.

## THE TRANSMIT's figure at two interfaces

- **The figure.** `CTRL_LOOP_TX_MS` is the built design's tx row by every source rounded up to the ms: 34 ms at one interface (34.00) and **105 ms** at two (104.25). `rows_tiers.tx_statements` holds both at or over their rows.
- **The hold-off.** `SRP_REDECLARE_CS` = 2 x 1,000 + `SRP_JOIN_CS` (19) + (`CTRL_LOOP_TX_MS` + 9) / 10: **2,030 cs** at two interfaces (2,029 at 99) and 2,023 at one. A withdrawn Talker's changed destination waits 10 ms longer at two interfaces, on the safe side of 35.2.2.8's least, 2,000 cs.
- **The images, by sha256** (`image_sha.py`: each ELF's loadable bytes and every linked object of every image `ledger.sh` links, 552 files; `compare_images.py`):
  - one-interface: **0 differ**;
  - two-interface: **12 differ**, `srp_mbx.o` and the ELF of each of the platform's and the size fixture's 1x1 and 8x8 images and the harness's two 8x8/2if arms. Each differs in **one instruction**, `li a3,2029` to `li a3,2030` (`7ed00693` to `7ee00693`), and in no other instruction or section byte (`objdump -d` and `objdump -s`).
- **Run again at two interfaces:**
  - `srp_talker.cpp` at 8x8/2if, 11 tests, and at 1x1/1if, 11; the composition's `SrpGate` at 8x8/2if, 7; the SRP and ACMP arm at two interfaces, 76: **PASS**;
  - the 8x8/2if `valid-destinations` leg (R9-W8, on a clean clone of `449d29d2`): 2 groups, 0 refusals, 0 budget misses, 0 of 3,052 passes over the share, no `STATED` line, 49 joins from 185.605 to 190.228 ms. Both groups' measured logs are **byte-identical** to round 8's leg on the image before; the results differ only in the head's stated tables and the build's hash.
- **The campaigns** hold the hold-off's terms: SRP's campaign plants each (`talker-hold-off-one-leaveall`, `talker-hold-off-skipped`, ...), 70 Talker rows (35 at each interface count), every one caught ([below](#the-full-pass)).

## Every stated cost against the legs

No measured image and no stated table has changed since round 8's survey (one-interface images identical by hash; two-interface images in the hold-off's constant alone, which no cost reads). The survey (`costs_vs_stated.py`, every table the rows read, by the rule over the legs):

| Point | At round 8's rebuilt image's tables (`73388996`) | At round 8's head and this one |
|---|---|---|
| 1x1/1if | UNDER 0 | UNDER 0 |
| 8x8/2if | UNDER 7: the base 32,705 (345; 325), a notice past `AECP_FAN_BYTES` 66,481 (700; 655), the fixed part 3,437 (40; 35), AMAP_LIVE_WRITE 2,465 (30; 25) | UNDER 0 (`b69388c7`) |

## The CPU budget harness

Every group of every arm at both points on a clean clone of round 8's `73388996`, whose image is the head's at one interface by hash and at two interfaces but for the hold-off's constant:

| Point | Arm | Groups | Refusals | Budget misses | `STATED` | rc |
|---|---|---:|---:|---|---:|---:|
| 1x1/1if | A (5 parts, merged) | 96 | 0 | 7 of 950 | 0 | 0 |
| 1x1/1if | `answering-every-port`, `valid-destinations`, B | 16, 2, 3 | 0 | 0 | 0 | 0 |
| 8x8/2if | A (5 parts, merged) | 94 | 0 | 7 of 994 | 0 | 0 |
| 8x8/2if | `answering-every-port` | 16 | 0 | 0 | 16 (the base) | 1; **0 regraded** at `b69388c7` |
| 8x8/2if | `valid-destinations` | 2 | 0 | 0 | 0 | 0; **again at this head's image: 0**, logs identical |
| 8x8/2if | B | 3 | 0 | 0 | 2 (the long notice) | 1; **0 regraded** at `b69388c7` |

- **Joins:** 359 at 1x1/1if (188.102 to 190.121 ms) and 750 at 8x8/2if (185.605 to 190.228), every one within 181 to 239.
- **The misses** are arm A's seven held-egress rows at each point, as before.
- **8x8/2if's share:** two passes of `answering-every-port` (at most 2.018 ms) and two of arm B's `aecp-largest-notice` (2.337 ms) are over the per-pass share. They are reported and belong to #890.

## Image identity and ROM

`image_sha.py` hashes every image `ledger.sh` links: each ELF's loadable bytes and every object, 552 files.
- **7B's cut head `1a917cf1` against round 8's sync merge `1143e3f5`:** 552 of 552 identical.
- **That merge against `73388996`** (the bound and the slice): 16 differ, every one a one-interface `ctrl_loop.o` or its ELF.
- **`73388996` against round 9's sync merge `663b519b`:** 552 of 552 identical.
- **That merge against `449d29d2`** (THE TRANSMIT's figure): 0 one-interface; 12 two-interface, each one instruction (above).
- **`449d29d2` against the final head `056d619d`** (the self-test fix, a comment, the second sync): 552 of 552 identical.

ROM at the head (`plat_ledger.py` rc 0, PASS at every point, `ledger.sh` on clean clones of `449d29d2` and of the final head):

| Point | Image | Entry or budget | rom / sram, RAMB36 | Left |
|---|---|---:|---|---:|
| 8x8/2if | platform | 60.5 | 131,752 / 114,224: 60.5 | 1,368 B |
| 8x8/2if | fixture | 59.0 | 126,608 / 113,248: 59.0 | 368 B |
| 8x8/2if | harness `answering-every-port` | 59.0 | 126,916 / 113,312: 59.0 | 60 B |
| 8x8/2if | harness `valid-destinations` | 59.0 | 126,776 / 113,248: 59.0 | 200 B |
| 8x8/1if | platform | 56 | 130,200 / 97,328: 56.0 (`ctrl_plat` 18,240 B, as recorded) | 872 B |
| others | | 56 | within | |

## The full pass

Both runs on clean clones; the second at the final head `056d619d` is the evidence, the first at `c772b1e5` found one failure ([the findings](#the-findings)) and is kept (`receipts/pass1-c772b1e5`).

| Gate | Command | Result at `056d619d` | Receipt |
|---|---|---|---|
| every `run:` step of rtl-fast, rtl, docs, elaborate | `run_wf.py` per job, each on its own fresh clone (`gate_queue.sh`, 18 units on `cpu_ranges.py` pick8 ranges, or the session pool while a release hold took every pick) | every job failed 0. docs-check-no-git's 3 steps rc 0; its driver's after-run `git status` fails since the job's own step removes `.git` (a driver artifact, as before) | `gates/workflows` |
| verify | `verify_wf.py <head> rtl-fast.yml rtl.yml docs.yml elaborate.yml --matrix=yosys-shards=shard:0-4,1-4,2-4,3-4` | rc 0: 139 steps ran, 226 not run with a reason, 0 bad (round 5: the same) | `gates/verify-table.md` |
| firmware campaigns (in those jobs) | firmware-{control,aecp,srp}-mutants | control 716 of 716 caught; AECP 299 rows, SRP 415 rows (70 `talker-`, 35 at each interface count, among them `talker-hold-off-skipped`, `-one-leaveall` and `-never-ends`), all caught, 0 escaped | `gates/campaigns.txt` |
| firmware coverage | firmware-unit's `fw_coverage.py --selftest` and `--check` | PASS (39 files) | `gates/workflows` |
| job trees after | `run_wf.py` tree-after | clean, but firmware-unit and the three mutant jobs leave `?? dispatch-build/` (#902's shard-dispatch self-test, for #894, as before) | `gates/workflows/*tree-after.txt` |
| lane gates a | `lane_gates.sh a` | all rc 0 but `flip_check` and `flip_check_8x8` (rc 1 by design: 8x8/2if); `flip_check_1x1` rc 0; **`harness_selftest` 0 failures** (1 at `c772b1e5`: 2 failures); behave rc 0 | `gates/lane` |
| lane gates b, c | `lane_gates.sh b` / `c` | `test_builder.py --require-rv32` rc 0; `nvm_selftest`, `boot_1x1`, `boot_8x8`, `boot_native`, `boot_plants` rc 0 | `gates/lane` |
| full Verilator sweep | `run_all_suites.sh --shard k/4`, each shard its own clone and its own `cpu_ranges.pick8()` range, with CI's `MAKEFLAGS=-j4` and the hosted job's `TSN_GEN_ROOT` in the env | 65 suites (15 + 17 + 17 + 16), 0 failed, 2,713,040 checks, 0 in-suite failures, each shard exit 0; `tsn_fuzz`'s field campaigns 164 and 675 pass, freshness PASS; shard trees clean after but shard 3's two `TEST_RESULTS.md` date stamps, restored | `sweep/` |
| graders at the head | `flip_grade.py --check --point 1x1/1if`, `rows_tiers.py --selftest`, `tier_grid.py`, `load_grade.py --check`, the slice rule | PASS; 1033 of 1033; 6 of 420, CHOSEN the built 900 us; 0.517 / 0.514; `slice_choice` (900, +0.0086) = `ruled` = built; `tx_statements` [] | `graders/g-final` |
| the ROM ledger | `ledger.sh` on a clean clone of the head | `plat_ledger.py` rc 0, PASS at every point; 552 of 552 image files identical to `449d29d2`'s | `ledger-final`, `identity/` |

## Description

### Validity and the declarations (rounds 1 and 2; the hold-off's figure at two interfaces in round 9)

A source declares its MSRP Talker only while its SRP parameters are valid: MAAP holds its destination, and a probe of the last 15 s or a registered Listener asks for it (Milan v1.2 4.3.3.1, 5.3.7.4).
- It declares at once, Talker Advertise with base + n and its TSpec, or Talker Failed (code 1) when its bandwidth does not fit.
- A lapse withdraws it, its licence and TALKER_DECL bit first.
- An unchanged destination is declared again at once. A changed one waits two LeaveAllTime periods after the Leave (IEEE 802.1Q-2018 35.2.2.8, Table 10-7), plus a JoinTime and THE TRANSMIT's MRPDU by every source: `SRP_REDECLARE_CS`, 2,023 cs at one interface and **2,030 at two**.
- `srp_mbx_gate` returns at once on the gate and base its last call left (7B's cut).

### Each source's stream_id (#905, unchanged)

The MAAP adapter (`maap_mbx.c`), which owns `DA_GATE`, writes each source's `SRC_SID_HI:SRC_SID_LO` through `mbx_pub_src_sid` while its gate bit is clear (`KL_mbx_pkg.sv:345`).

## Authoritative references

- #895 rulings issuecomment-6895331865 (round 9), 6892130675 (round 8), 6886630886 (round 7), 6876349305. #894 issuecomment-6888782796 (its round 13), 6872978311, 6867990126, 6845846512, 6862465874 (the queued bound's rule).
- IEEE 1722.1-2021 9.3.2.6; IEEE 802.1Q-2018 10.7.11, 35.2.2.8, Tables 10-5 to 10-7; Milan v1.2 4.2.7.1.1 (Table 4.3), 4.3.2, 4.3.3.1, 5.3.7.4.
- `docs/design/SPLIT_CONTROL_MEMORY.md` section 13 ("The bound and the slice at 140 ms (#895)", "THE TRANSMIT's figure at two interfaces (#895)"); FR_NFR.md 3.4.1; `sw/firmware/ctrl/loop/ctrl_loop.h` (`CTRL_LOOP_SLICE_US`, `CTRL_LOOP_TX_MS`); `sw/firmware/ctrl/aecp/aecp_mbx.h` (`AECP_QUEUED_MS`); `sw/firmware/ctrl/srp/srp_mbx.c` (`SRP_REDECLARE_CS`); `sw/litex/ctrl_memory_ledger.py`; `tb/verilator/ctrl_service_budget/queued_bound.py`, `rows_tiers.py`.

## How to validate

```sh
git checkout 056d619d && git submodule update --init --recursive
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if   # rc 0: last 136.65 of 140, ACMP 29.63, txL 48.58
python3 -B tb/verilator/ctrl_service_budget/rows_tiers.py --selftest               # rc 0: 1033 of 1033
python3 -B tb/verilator/ctrl_service_budget/tier_grid.py --point 1x1/1if            # rc 0: 6 of 420, CHOSEN the built 900 us
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check                   # rc 0: 0.517 / 0.514
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir /tmp/plat        # rc 0: every point PASS
```

## Known limitations / out of scope

- **The margins:** ACMP has 0.37 ms and txL 0.42 ms left at 1x1/1if; a pass's own cost has 18 us of headroom (279 us against 260).
- **Layout sensitivity (#909):** the polls' base and the 8x8/2if costs move with code placement; restated by the rule, not chased.
- **The ROM:** the `answering-every-port` 8x8/2if harness arm has 60 B left at 59.0 (graded in #898's composed check).
- **Found before, for their own issues:** srptx `[TIME]` (#906) and the hold `[TX]` path (#907).
- **8x8/1if** is lane 894b's. The bench run (#895 acceptance 6, #905 acceptance 4) is the bench lane's.
- **`dev-soft-core`** (with #902 merged) states `CTRL_LOOP_TX_MS` 99 and `AECP_QUEUED_MS` 130; this PR's head states 105 and 140, its own image's by the rulings. The candidate merge with `dev-soft-core` at `659d7687` has this head's tree, since `659d7687`'s tree is `07ed787e`'s.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (acceptance 4 composed holds at 1x1/1if; 8x8/2if reported)
- [x] Required tests and local gates pass at the exact head (the full pass at `056d619d`, [above](#the-full-pass))
- [ ] Current PR head has a successful `rtl-fast` verdict
- [ ] Exact-head `verilator-suites` and `yosys-portability` after ready
- [x] No undocumented requirement/interface change
- [ ] Internal cleared-context review POSITIVE at the exact head
- [ ] External review POSITIVE at the exact head
- [ ] Every review lens covered clean at the merge candidate
- [ ] Candidate merge validated, post-merge containment clean
