[A482] Design media-clock following of one selected AAF or CRF source (#629, lane M1)

## Contents

- **[Status](#status)**: design only, three docs commits, `629-media-clock-follow` -> `dev`, round 2 answered, awaiting the D1 and D5 decisions and re-review.
- **[Linked Issue / roles](#linked-issue--roles)**: relates to #629; executors and reviewers.
- **[Description](#description)**: the design page, its index row, and the decisions it records.
- **[Round 2](#round-2)**: what round 2 changed, finding by finding.
- **[Authoritative references](#authoritative-references)**: the Milan, IEEE 1722.1 and IEEE 1722 clauses read.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: the branch and the pinned Markdown environment.
- **[How to validate](#how-to-validate)**: the gates, and the one area measurement the page quotes.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what the page does not establish.
- **[Definition of Done](#definition-of-done)**: the merge bar.

## Status

Design only. Three commits on dev `d4dd742679b902b2bc5eedf89d525066d59aafbb`, `629-media-clock-follow` -> `dev`:

- round 1: `78d4fef220c0ad4873a89b138828c0543c2bcad0`;
- round 2: `4845f158c487827c7b331f79545c4abeed18dec6`, then `49899572741b732563bdca0bff03cefb69aea867`, the head.

Documentation only: no RTL, builder, generator, configuration or processor change. Every gate below rc 0 at `49899572`. D1 and D5 are re-opened for decision, and D4 is with the owner.

## Linked Issue / roles

Relates to #629 (lane M1, the design item of its body; the implementation, simulation and bench items stay open). The lane's assignments are [#629 comment 5935051587](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5935051587) (round 1) and [#629 comment 5935864862](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5935864862) (round 2).

Executor: `[A482]` (round 1), `[A483]` (round 2)
Internal cleared-context reviewer: `[R428]`
External reviewer: `[R429]`

## Description

| File | Change |
|---|---|
| `docs/design/MEDIA_CLOCK_FOLLOWING.md` (new) | The design for following one selected AAF or CRF talker's media clock |
| `docs/README.md` | Its row in the design index (the "Architecture and integration" table) |

The page holds:

- **Clause findings**, by question. (a) Milan v1.2 5.3.3.6 is a minimum set: its "exactly one" binds CRF-capable inputs and the single AAF input of a Configuration without CRF, and no clause sets a count for an AAF input beside a CRF input or any order; IEEE 1722.1-2021 7.2.32 caps the list at 216. (b) What the clauses require on a lost stream (a listed source in use and saved, Milan v1.2 5.3.11.1; no non-ATDECC change while locked, 5.4.2.15; the 5.3.11.2 counters), what they permit (an entity-initiated change while unlocked, 5.3.11.1; free-wheel, IEEE 1722-2016 10.6 and the 4.4.4.7 NOTE), and what this design chooses (no fallback at any time). (c) The 4.4.4.3 disruption and echo shalls name CRF only; acting on them for a followed AAF stream is permitted, and PICS AAF-5 supports it. (d) Eight places where the current reading is wrong.
- **A map of the current state**, every fact at `path:line` on dev `d4dd7426` (processor paths at its pin `b2db3a97`).
- **The design**: an AAF clock meter for the 48 kHz base format that keeps the mean of each 16-PDU group (96 samples, the CRF spacing) and feeds the existing servo in its own units, with a 4,096 ns jump bound derived from IEEE 1722-2016 10.8; one widened selection decode; the source switch, with one `mr` request per switch by construction; lock loss and holdover; the CRF output and A2; the CLOCK_DOMAIN counters; area.
- **The change lists**: every parent-visible change, and the cross-repository plan for the protocol processor, filed as protocol-processor #141 (no processor RTL change; its documentation and tests change).
- **The test plan**: simulation cases each with a failing mutant, and bench cases by B6's method (PR #630).

Decisions, with the page's recommendation and their state:

| ID | Question | Recommendation | State |
|---|---|---|---|
| D1 | Source order | L1: INTERNAL 0, CRF 1, AAF input k at 2 + k (class order on every shape), so CRF's index does not depend on the listener count | Re-opened in round 2, for decision |
| D2 | AAF measurement | M1: one meter on the selected input; round 2 adds the format restriction, the group-mean pick and the 4,096 ns bound | Ruled M1 |
| D3 | Switching between two followed sources | W2: hold over and re-acquire, no trim reset | Ruled W2 |
| D4 | A2 at INTERNAL | A2-a: engage the grid aligner at INTERNAL too; reverses the recorded INTERNAL free-run rule | With the owner |
| D5 | CLOCK_DOMAIN LOCKED and UNLOCKED | C1: unlocked while a followed source's servo is not LOCKED; reverses the recorded LOCKED-equals-`~tu` rule while following, stated | Re-opened in round 2, for decision |
| D6 | Shipping configurations | All five, in one regeneration; every unit loses its saved state once at that update | Ruled all five |
| D7 | Phase alignment (IEEE 1722-2016 10.8, 4.3.5) | A new issue | Filed as #632 |

## Round 2

Round 2 is two commits on `78d4fef2`, answering [R428-1](https://github.com/kebag-logic/milan-fpga/pull/631#issuecomment-5935858741) and [R429-1](https://github.com/kebag-logic/milan-fpga/pull/631#issuecomment-5935860128) under the round 2 assignment. `4845f158` carries the answers below. `49899572` makes three statements precise before publication: the jump bound as a spacing deviation, the rate offset inside the deviation measurement, and which lock option C2 counts, with its counter-test line. Together they change only `docs/design/MEDIA_CLOCK_FOLLOWING.md` (+494 / -187 against `78d4fef2`). The index row is unchanged.

| Assignment item | Findings | Answer, by page section |
|---|---|---|
| 1. The AAF meter | R428-1 F2; R429-1 F2, F3 | "Measuring an AAF stream's media clock". The fields the meter reads, with their nets. The supported format: Milan v1.2 6.2's 48 kHz base format only, with samples per PDU derived from `stream_data_length` = 24 x `channels_per_frame`, because AAF has no such field and the RX monitor's family compare does not check it. The pick: groups of 16 by `sequence_num` modulo 16, which stay aligned across the 8-bit wrap; the six divisors that break at the wrap, and the five that would not, are all refused as non-base formats. The kept value is the group mean (P2, over P1). The timestamp-quality assumption with its basis: IEEE 1722-2016 10.8 Equation (15) plus the CRF timing points' own error, about +/-1,426 ns; Equation (16) for what a CRF listener accepts; no clause for a talker on its own clock; the bench measures the reference peer. The jump bound re-derived: 4,096 ns (B2, over B1 2,048 ns and B3 16,384 ns), still catching a one-sample step. A desk model table of B1/B2 and P1/P2 under group-shaped and independent error. |
| 2. `mr` on a source switch | R429-1 F4 | "History, lock, era and outputs": a meter era starts at every change of the followed listener and at entry into AAF following, clearing the lock without a disruption trigger and re-seeding the received `mr` silently. "`mr`": one request per switch by construction, and why the merge window (at most 125 us per AAF output) cannot absorb a second. Test rows: the meter's seed row, and the `milan_dp` switch row with the two talkers at opposite `mr` levels and a no-re-seed mutant. |
| 3. The test plan | R428-1 F4 (a) to (e); R429-1 F5 (1) to (4) | A root W2 row with a presentation-removed mutant; a D5 counter row with the other option's level as mutant, and the bench lock-loss row reads the counters; a CSR row with a missing read-window mutant; the decimation-by-1 symptom corrected (`rate_valid` never rises), and `rate_valid` asserted wherever a rate is compared; a real AECP-walk mutant (a stale decode table); the true-ratio leg with AAF and CRF talkers at different offsets and a mux-stuck-on-CRF mutant; meter rows for error at and beyond the bound, refused formats and the sequence wrap, each with a mutant. |
| 4. The clause wording | R428-1 F5; R429-1 F1 | (a): the "at most one per Stream Input" sentence removed; 7.6 recorded as a recommendation whose model covers CRF only, and 7.6.2's one-domain consequence restated as a fact of this model. (b): split into what the clauses require, what they permit and what this design chooses; no fallback stated as this design's choice with its reasons; 10.6 and the 4.4.4.7 NOTE cited for free-wheel. The two IEEE 1722-2016 quotations moved to (c), the received-toggle case they describe. Holdover item 2 no longer says "as (b) requires". |
| 5. Current with the rulings | R428-1 F6 | The header's "Where the decisions stand"; the Decisions table's state column; #632 and protocol-processor #141 linked where the page proposes them; D4 marked with the owner. |
| Re-opened D1 | R428-1 F1 | "Source list and order": the saved-state rationale withdrawn, with the KLJ2 refusal across a model change cited; what the update does to saved state; L1 re-argued on index stability; the class order on shapes without INTERNAL or CRF. |
| Re-opened D5 | R428-1 F3 | "CLOCK_DOMAIN LOCKED and UNLOCKED": the recorded rule and its history (written 2026-08-14, before live CRF selection on 2026-09-02); options C0, C1, C2, C3; C1 recommended with the reversal stated and its cost; the banner rewrite in the root change list. |
| 6. Suggestions | R428-1 S1 to S4, O1; R429-1 S1 to S4 | All taken. R428-1 S1: (c) and (d) item 5 read PICS AAF-5. S2: A2 under following holds while the TDM feed is live. S3: the restore compare at `KL_aecp_nvm_writer.sv:501-503`, the MMCM-plan comment at `:3937`, the servo at 871 LUT / 792 FF, `_load_names`, the servo harnesses, and the three 7.4.23.1 credit sites. S4 and R429-1 S4: the class order on every shape. O1: (d) item 8 records the flag value for the model lane; filing it as an issue stays the manager's. R429-1 S1: the stale comment at `:3112`, `_load_names`, `CLOCK_SOURCE_NAMES` at `:141`. S2: the AAF `tu` wiring trap and the read-window terms. S3: the 7.6 row, and C1 stated as superseding the recorded rationale. |

Also changed in round 2: the area estimate (the meter grows by the group mean, total about 380 to 560 LUT, 290 to 440 FF, 1 RAMB18), the parent-visible list (the builder test, the gate-pinned compare text, the servo harnesses, the saved-state release note), and a bench switch case.

Round 2 evidence: the Markdown gates below at `49899572`; the desk model of the meter rules (`meter_rules_model.py`, standard library only, deterministic, rc 0), with its output, in the round 2 packet. The model is of the rules, not of any talker.

Round 2b, under [#629 comment 5936355573](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5936355573), executor `[A484]`: `c554ae51b1dcc2285863f0f0117cb025971a594c`, the new head, replaces the glob in the page's "Generated" change-list row with the five tracked `configs/generated/<config>/gen/` shape-header paths, so that `scripts/check_entity_shape.py` arm I resolves it (`checks: 166 failures: 0`, rc 0; rc 1 at `49899572`, and the same reference is in the round-1 page at `78d4fef2`); the meaning is unchanged, and every gate under "How to validate" except the area run is rc 0 at this head.

## Authoritative references

- Milan v1.2: 5.3.3.6, 5.3.8.7, 5.3.11.1, 5.3.11.2 (Tables 5.7, 5.15), 5.4.2.15, 5.4.2.16, Table 5.4, Table 5.6, 6.2 (Table 6.1), 7.1, 7.2.2, 7.2.3, 7.3.2, 7.4, 7.6, 7.6.2.
- IEEE 1722.1-2021: 6.2.2.8, 7.2.6 (Table 7-8), 7.2.9, 7.2.9.1 (Table 7-16), 7.2.9.2 (Table 7-17), 7.2.32 (Table 7-61), 7.4.23, 7.4.23.1, 7.4.24, Table 7-141.
- IEEE 1722-2016: 4.3.2, 4.3.5, 4.4.4.3, 4.4.4.5, 4.4.4.6, 4.4.4.7, 7.2.4, 7.3 (7.3.3, 7.3.5), 7.5, 10.4.3, 10.6, 10.8 (Equations 15 and 16), PICS Table F.7 (AAF-5, AAF-6).
- #629 (the decision in its body, both lane M1 assignments, the [rulings](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5935520588)), #389 (option (a), reversed for AAF), #74 (A2 and its ledger), #632 (phase alignment), protocol-processor #141 (the processor part), PR #630 (bench lane B6, the baseline).
- `docs/design/TIME_SYNC.md`, `docs/reference/FR_NFR.md` (FR-CLK-03, FR-CLK-04), `docs/reference/MILAN_COMPLIANCE_MATRIX.md`, `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` (L6), `docs/design/AREA_BUDGET.md`, `docs/design/SAVED_STATE_FASTCONNECT.md`, `docs/design/SAVED_STATE_MATERIALIZATION.md`; the protocol processor's `docs/architecture/07_memory_maps.md` (L6) and `docs/00_MILAN_COMPLIANCE_REVIEW.md` (REQ-AEM-013, REQ-MDL-005).

## How to get into the same state

```sh
git fetch origin
git checkout 629-media-clock-follow
git submodule update --init protocol-processor
python3 -m venv .md-venv
.md-venv/bin/python -m pip install --require-hashes -r tools/markdown/requirements.txt
```

## How to validate

```sh
.md-venv/bin/python scripts/docs_check.py
.md-venv/bin/python scripts/check_doc_style.py
.md-venv/bin/python scripts/gen_toc.py --check
.md-venv/bin/python scripts/gen_toc.py --verify-anchors
.md-venv/bin/python scripts/check_em_dash.py --base d4dd7426
.md-venv/bin/python scripts/check_doc_paths.py
git diff --check d4dd7426 HEAD
# the one measurement the page quotes (Yosys estimate, out of context):
OOC_SHAPE="$PWD/configs/generated/endstation_ax7101_1x1_tdm8" syn/yosys/ooc.sh KL_crf_rx
```

Expected result / pass criteria: every command exits 0. `docs_check` reports 0 findings; `check_em_dash` reports 0 findings over 885 added lines in 2 pages; the TOC gate and the anchor check pass; `check_doc_paths` resolves every cited path. The area run prints `KL_crf_rx` at 433 LUT, 544 FF, 1 RAMB18 and 147 CARRY4, the figures in the page's "Area estimate".

Results at `49899572`, each run unpiped with its output to a file: all rc 0. The same gates were also rc 0 at `4845f158`.

- `docs_check`: 0 findings across 184 Markdown files and 955 scrubbed text files.
- `check_doc_style`: OK, 22 current documents.
- `gen_toc --check`: OK. `gen_toc --verify-anchors`: 292 links reproduced.
- `check_em_dash --base d4dd7426`: 0 findings over 885 added lines.
- `check_doc_paths`: OK, 874 cited paths resolve.
- `git diff --check` and `git diff --check d4dd7426 HEAD`: clean.

Round 1's results at `78d4fef2` were the same gates, all rc 0, with `check_feature_status --self-test` also rc 0.

## Known limitations / out of scope

- Design only: no simulation was run, and nothing in the page is implemented. The area figures are estimates scaled from one out-of-context run. The meter's figures come from a desk model of its rules, not of any talker.
- No measurement of a real AAF talker's timestamp regularity exists in the repository. The meter is designed for the IEEE 1722-2016 10.8 talker bound; the bench lane measures the reference peer's through the meter's status word.
- The baseline findings page (B6) is cited through PR #630, which is still open.
- Out of scope, by the assignments: every RTL, builder, generator, configuration and processor change, and the requirement amendments themselves (FR-CLK-03, FR-CLK-04 and the #389 record). The page lists each of them as a change for the implementation lanes.
- IEEE 1722-2016 10.8 and 4.3.5 phase alignment is filed as #632 (D7), not designed here.
- The RX monitor's unused external-clock media-lock rule stays #74's ledger item 3.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (this PR covers #629's design step only; it relates to #629 and does not close it)
- [ ] New or changed behavior has self-checking tests (no behavior changes; the test plan is in the page)
- [x] Required local verification bar passes (the Markdown gates above, rc 0)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains (none is made; the proposed ones are listed in the page)
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
