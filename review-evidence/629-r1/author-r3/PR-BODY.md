[A482] Design media-clock following of one selected AAF or CRF source (#629, lane M1)

## Contents

- **[Status](#status)**: design only, five docs commits, `629-media-clock-follow` -> `dev`, round 3 answered, awaiting the D1, D5 and D8 decisions and re-review.
- **[Linked Issue / roles](#linked-issue--roles)**: relates to #629; executors and reviewers.
- **[Description](#description)**: the design page, its index row, and the decisions it records.
- **[Round 2](#round-2)**: what round 2 changed, finding by finding.
- **[Round 3](#round-3)**: what round 3 changed, item by item, with its evidence.
- **[Authoritative references](#authoritative-references)**: the Milan, IEEE 1722.1 and IEEE 1722 clauses read.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: the branch and the pinned Markdown environment.
- **[How to validate](#how-to-validate)**: the gates, the shape check, and the one area measurement the page quotes.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what the page does not establish.
- **[Definition of Done](#definition-of-done)**: the merge bar.

## Status

Design only. Five commits on dev `d4dd742679b902b2bc5eedf89d525066d59aafbb`, `629-media-clock-follow` -> `dev`:

- round 1: `78d4fef220c0ad4873a89b138828c0543c2bcad0`;
- round 2: `4845f158c487827c7b331f79545c4abeed18dec6`, then `49899572741b732563bdca0bff03cefb69aea867`;
- round 2b: `c554ae51b1dcc2285863f0f0117cb025971a594c`;
- round 3: `a463a1deb9d63614e8bd2134ccd7b2cd541c72ed`, the head.

Documentation only: no RTL, builder, generator, configuration or processor change. Every gate below rc 0 at `a463a1de`. D1 and D5 are open for decision, D8 is new and open for decision, and D4 is with the owner.

## Linked Issue / roles

Relates to #629 (lane M1, the design item of its body; the implementation, simulation and bench items stay open). The lane's assignments are [#629 comment 5935051587](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5935051587) (round 1), [#629 comment 5935864862](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5935864862) (round 2), [#629 comment 5936355573](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5936355573) (round 2b) and [#629 comment 5936791368](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5936791368) (round 3).

Executor: `[A482]` (round 1), `[A483]` (round 2), `[A484]` (round 2b), `[A486]` (round 3)
Internal cleared-context reviewer: `[R428]`
External reviewer: `[R429]`

## Description

| File | Change |
|---|---|
| `docs/design/MEDIA_CLOCK_FOLLOWING.md` (new) | The design for following one selected AAF or CRF talker's media clock |
| `docs/README.md` | Its row in the design index (the "Architecture and integration" table) |

The page holds:

- **Clause findings**, by question. (a) Milan v1.2 5.3.3.6 is a minimum set: its "exactly one" binds CRF-capable inputs and the single AAF input of a Configuration without CRF, and no clause sets a count for an AAF input beside a CRF input or any order; IEEE 1722.1-2021 7.2.32 caps the list at 216. (b) What the clauses require on a lost stream (a listed source in use and saved, Milan v1.2 5.3.11.1; no non-ATDECC change while locked, 5.4.2.15; the 5.3.11.2 counters), what they permit (an entity-initiated change while unlocked, since no clause forbids one outside 5.4.2.15; free-wheel on CRF packet loss, IEEE 1722-2016 10.6, and the 4.4.4.7 NOTE), and what this design chooses (no fallback at any time). (c) The 4.4.4.3 disruption and echo shalls name CRF only; acting on them for a followed AAF stream is permitted, and PICS AAF-5 supports it. (d) Eight places where the current reading is wrong.
- **A map of the current state**, every fact at `path:line` on dev `d4dd7426` (processor paths at its pin `b2db3a97`).
- **The design**: an AAF clock meter for the 48 kHz base format that keeps the mean of each 16-PDU group (96 samples, the CRF spacing) and gives the existing servo a rate in its own units from a two-point difference over 4.096 s (D8), with a 4,096 ns jump bound derived from IEEE 1722-2016 10.8; one widened selection decode; the source switch, with one `mr` request per switch by construction; lock loss and holdover; the CRF output and A2; the CLOCK_DOMAIN counters; area.
- **The change lists**: every parent-visible change, and the cross-repository plan for the protocol processor, filed as protocol-processor #141 (no processor RTL change; its documentation and tests change).
- **The test plan**: simulation cases each with a failing mutant, and bench cases by B6's method (PR #630).

Decisions, with the page's recommendation and their state:

| ID | Question | Recommendation | State |
|---|---|---|---|
| D1 | Source order | L1: INTERNAL 0, CRF 1, AAF input k at 2 + k (class order on every shape), so CRF's index does not depend on the listener count | Re-opened in round 2, for decision |
| D2 | AAF measurement | M1: one meter on the selected input; round 2 adds the format restriction, the group-mean pick and the 4,096 ns bound; its estimator is D8. The ruling's "keeps one AAF timestamp in 16" becomes "keeps the mean of each 16" | Ruled M1; the wording changes for the manager to confirm |
| D3 | Switching between two followed sources | W2: hold over and re-acquire, no trim reset | Ruled W2 |
| D4 | A2 at INTERNAL | A2-a: engage the grid aligner at INTERNAL too; reverses the recorded INTERNAL free-run rule | With the owner |
| D5 | CLOCK_DOMAIN LOCKED and UNLOCKED | C1 with E8: unlocked while a followed source's servo is not LOCKED; reverses the recorded LOCKED-equals-`~tu` rule while following, stated. C2 if D8 keeps E1 | Re-opened in round 2, restated in round 3, for decision |
| D6 | Shipping configurations | All five, in one regeneration; every unit loses its saved state once at that update | Ruled all five |
| D7 | Phase alignment (IEEE 1722-2016 10.8, 4.3.5) | A new issue | Filed as #632 |
| D8 | The AAF meter's rate estimator | E8: a two-point difference over 4.096 s from an 8-entry snapshot ring; meets the servo's lock test under every error shape of 10.8 size; one RAMB18 fewer; rate valid 4.096 s after a history restart | New in round 3, for decision |

## Round 2

Round 2 is two commits on `78d4fef2`, answering [R428-1](https://github.com/kebag-logic/milan-fpga/pull/631#issuecomment-5935858741) and [R429-1](https://github.com/kebag-logic/milan-fpga/pull/631#issuecomment-5935860128) under the round 2 assignment. `4845f158` carries the answers below. `49899572` makes three statements precise before publication: the jump bound as a spacing deviation, the rate offset inside the deviation measurement, and which lock option C2 counts, with its counter-test line. Together they change only `docs/design/MEDIA_CLOCK_FOLLOWING.md` (+494 / -187 against `78d4fef2`). The index row is unchanged.

| Assignment item | Findings | Answer, by page section |
|---|---|---|
| 1. The AAF meter | R428-1 F2; R429-1 F2, F3 | "Measuring an AAF stream's media clock". The fields the meter reads, with their nets. The supported format: Milan v1.2 6.2's 48 kHz base format only, with samples per PDU derived from `stream_data_length` = 24 x `channels_per_frame`, because AAF has no such field and the RX monitor's family compare does not check it. The pick: groups of 16 by `sequence_num` modulo 16, which stay aligned across the 8-bit wrap; the six divisors that break at the wrap, and the five that would not, are all refused as non-base formats. The kept value is the group mean (P2, over P1). The timestamp-quality assumption with its basis: IEEE 1722-2016 10.8 Equation (15) plus the CRF timing points' own error, about +/-1,426 ns; Equation (16) for what a CRF listener accepts; no clause for a talker on its own clock; the bench measures the reference peer. The jump bound re-derived: 4,096 ns (B2, over B1 2,048 ns and B3 16,384 ns), still catching a one-sample step. A desk model table of B1/B2 and P1/P2 under group-shaped and independent error (superseded in round 3). |
| 2. `mr` on a source switch | R429-1 F4 | "History, lock, era and outputs": a meter era starts at every change of the followed listener and at entry into AAF following, clearing the lock without a disruption trigger and re-seeding the received `mr` silently. "`mr`": one request per switch by construction. Test rows: the meter's seed row, and the `milan_dp` switch row with the two talkers at opposite `mr` levels and a no-re-seed mutant (both reworked in round 3). |
| 3. The test plan | R428-1 F4 (a) to (e); R429-1 F5 (1) to (4) | A root W2 row with a presentation-removed mutant; a D5 counter row with the other option's level as mutant, and the bench lock-loss row reads the counters; a CSR row with a missing read-window mutant; the decimation-by-1 symptom corrected (`rate_valid` never rises), and `rate_valid` asserted wherever a rate is compared; a real AECP-walk mutant (a stale decode table); the true-ratio leg with AAF and CRF talkers at different offsets and a mux-stuck-on-CRF mutant; meter rows for error at and beyond the bound, refused formats and the sequence wrap, each with a mutant. |
| 4. The clause wording | R428-1 F5; R429-1 F1 | (a): the "at most one per Stream Input" sentence removed; 7.6 recorded as a recommendation whose model covers CRF only, and 7.6.2's one-domain consequence restated as a fact of this model. (b): split into what the clauses require, what they permit and what this design chooses; no fallback stated as this design's choice with its reasons; 10.6 and the 4.4.4.7 NOTE cited for free-wheel. The two IEEE 1722-2016 quotations moved to (c), the received-toggle case they describe. Holdover item 2 no longer says "as (b) requires". |
| 5. Current with the rulings | R428-1 F6 | The header's "Where the decisions stand"; the Decisions table's state column; #632 and protocol-processor #141 linked where the page proposes them; D4 marked with the owner. |
| Re-opened D1 | R428-1 F1 | "Source list and order": the saved-state rationale withdrawn, with the KLJ2 refusal across a model change cited; what the update does to saved state; L1 re-argued on index stability; the class order on shapes without INTERNAL or CRF. |
| Re-opened D5 | R428-1 F3 | "CLOCK_DOMAIN LOCKED and UNLOCKED": the recorded rule and its history (written 2026-08-14, before live CRF selection on 2026-09-02); options C0, C1, C2, C3; C1 recommended with the reversal stated and its cost; the banner rewrite in the root change list. |
| 6. Suggestions | R428-1 S1 to S4, O1; R429-1 S1 to S4 | All taken. R428-1 S1: (c) and (d) item 5 read PICS AAF-5. S2: A2 under following holds while the TDM feed is live. S3: the restore compare at `KL_aecp_nvm_writer.sv:501-503`, the MMCM-plan comment at `:3937`, the servo at 871 LUT / 792 FF, `_load_names`, the servo harnesses, and the three 7.4.23.1 credit sites. S4 and R429-1 S4: the class order on every shape. O1: (d) item 8 records the flag value for the model lane; filing it as an issue stays the manager's. R429-1 S1: the stale comment at `:3112`, `_load_names`, `CLOCK_SOURCE_NAMES` at `:141`. S2: the AAF `tu` wiring trap and the read-window terms. S3: the 7.6 row, and C1 stated as superseding the recorded rationale. |

Also changed in round 2: the area estimate, the parent-visible list (the builder test, the gate-pinned compare text, the servo harnesses, the saved-state release note), and a bench switch case.

Round 2 evidence: the Markdown gates at `49899572`; the desk model of the meter rules (`meter_rules_model.py`, standard library only, deterministic, rc 0), with its output, in the round 2 packet. Round 3's model supersedes it: it adds the within-group void rule and the closed loop.

Round 2b, under [#629 comment 5936355573](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5936355573), executor `[A484]`: `c554ae51` replaces the glob in the page's "Generated" change-list row with the five tracked `configs/generated/<config>/gen/` shape-header paths, so that `scripts/check_entity_shape.py` arm I resolves it (`checks: 166 failures: 0`, rc 0; rc 1 at `49899572`); the meaning is unchanged.

## Round 3

Round 3 is one commit, `a463a1de` on `c554ae51`, answering [R428-2](https://github.com/kebag-logic/milan-fpga/pull/631#issuecomment-5936781329) and [R429-2](https://github.com/kebag-logic/milan-fpga/pull/631#issuecomment-5936790644) under the [round 3 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5936791368). It changes only `docs/design/MEDIA_CLOCK_FOLLOWING.md` (+322 / -101 against `c554ae51`). The index row is unchanged.

| Assignment item | Findings | Answer, by page section |
|---|---|---|
| 1. The error-shape claim: fix the design | R428-2 F2; R429-2 N1 | New subsection "The rate estimator" (D8). No estimator over 512 ms can meet the servo's 2 ppm lock test against every error shape of 10.8 size: a 2J ramp over a span T is a rate of 2J / T, 4.07 ppm at +/-1,042 ns over 512 ms; every unbiased linear estimator has a worst case of at least 2J / T, the two-point difference attains it, and a least-squares slope reaches 3J / T. The servo's PI amplifies estimator error by up to 2.125 (worst-case gain). E8, a two-point difference over 8 x 512 ms from an 8-entry snapshot ring, bounds the window error at 753 ns at +/-1,426 ns for every shape (890 ns at a plant gain of 1.2). Area: one RAMB18 fewer than round 2's meter, about 10 to 30 LUT and under 10 FF more. Latency: the rate is valid 4.096 s after a history restart instead of 512 ms; LOCKED 7.3 s after an ideal talker's first PDU in the model, against 3.7 s. The desk-model table against independent, alternating, random-sign and uniform per-group, 10 ms / 1 s / 2 s periodic and worst-case error, and the one-sample step at all 16 group positions, which is still rejected. Options E1, LS1, E4, E8 and a servo lock-rule change, with E8 recommended. The "two shapes bound the cases" sentence is gone. |
| 2. The desk model's void rule | R428-2 F1; R429-2 N2 | The round-3 model applies the within-group void. The +/-2,500 ns row now reads "never valid" (about 120 groups voided per second); round 2's 0.996 came from a model without the rule. New paragraph "The tolerance the two rules give": +/-1,748 ns per timestamp at 300 ppm (correlated error, spacing rule), +/-1,766 ns (independent error, in-group rule) and +/-2,048 ns at 0 ppm, matched by the model's first restarts. No other round-2 row survives unchanged: the table is replaced. |
| 3. The switch test | R428-2 F3; R429-2 N3 | The meter now owns the classification: only its own 100 ms timeout pulses `disrupt_p`; an era start by a listener change, entry or exit clears the lock silently; its enable is the one selection gate. A new meter row counts `disrupt_p` and `mr_toggle_p` at the meter's ports, killing the no-re-seed and era-start mutants at every switch. The `milan_dp` switch row now has three checks: (i) requests counted at a `public_flat_rd` tap on the restart request (no port or register), killing both mutants at every switch; (ii) a pinned stimulus, the new talker starting 5 ms after the switch, which puts the no-re-seed mutant's second toggle on every output; (iii) an INTERNAL dwell for the enable mutant. The `mr` rationale now says which second request lands inside each output's merge window (a lock clear at the switch: never on the wire) and which after it (a late-starting talker's stale-seed echo; a 100 ms timeout), per output. Checked against the unmodified `KL_media_clock_restart.sv` in the pinned HDL simulator. |
| 4. D5 restated | R429-2 (D5 on corrected evidence) | "CLOCK_DOMAIN LOCKED and UNLOCKED": C1 stays recommended, with E8, since under E8 a talker inside the design assumption never drops the servo out of LOCKED, so C1's counters move only at a loss, a return and a switch. The round-2 cost "one pair per about 2.5 s" is withdrawn. C2 is recommended instead if D8 keeps E1. |
| 5. Suggestions | R428-2 S1 to S4; R429-2 S1 to S4 | All taken. 10.6 now reads "lost due to network packet loss" (R428-2 S3). The 96 / count per-format pick separated from the fixed 16-PDU pick (R428-2 S1). The floor of the group-mean division stated as at most 1 ns in a rate (R428-2 S2). D2's ruled wording quoted, with both changes to it, in "Measuring an AAF stream's media clock" and in the Decisions table (R428-2 S4, R429-2 S2). The entity-initiated change rests on the absence of a prohibition outside 5.4.2.15, and 5.3.11.1's "is able to" reads as a capability (R429-2 S1). The merge window stated per output: 125 us AAF, 2 ms CRF (R429-2 S3). `hdl/common/gen/adp_shape_defaults.svh` added to the Generated row's Where cell (R429-2 S4). |

Also changed in round 3: the area table (the meter, E8: 340 to 510 LUT, 270 to 410 FF, 0 RAMB18; total about 390 to 590 LUT, 290 to 450 FF, 0 RAMB18), the switching and restart latencies, the parent-visible RTL rows (the estimator, the enable, the two pulses, the request tap), a servo-with-meter simulation row, the bench B AAF lock criterion, and three Limits: the closed-loop model's scope, and the same worst-case property on the CRF path's own 512 ms rate (about 255 ns per timestamp in closed loop against the 384 ns `KL_crf_rx` assumes), proposed as a separate issue because the ruling keeps `KL_crf_rx` unchanged.

Round 3 evidence, in the round 3 packet:

- `meter_rules_model_r3.py` (standard library only, deterministic seeds, rc 0) with its output: the loop's worst-case gain per estimator and plant gain, a talker frequency step, latency, the sequence wrap and its mutant, the tolerance sweep, the +/-2,500 ns row with the void on and off, the step sweep at 16 group positions, and the shape table for E1, E4, E8 and LS1 with P1 and P2, open loop and closed loop. A second run is byte-identical.
- `mcr_switch_probe/` (`sim_switch.cpp`, `run_probe.sh`, receipt rc 0): the unmodified `KL_media_clock_restart.sv` (sha256 `5891b12a...465f`) built with `N_TALKERS_P=2` in the pinned HDL simulator 5.050. The switch alone: one toggle per output at every phase (1,600 of 1,600 at cycle resolution on a scaled clock; 32 of 32 at 100 MHz). The no-re-seed mutant with the new talker starting 5 ms after the switch: a second toggle on both outputs at every phase (1,600 of 1,600 at two report latencies; 32 of 32 at 100 MHz at two latencies). The same mutant with the new talker streaming: 17 % of trials scaled, 27 % at 100 MHz. A request 1 to 4 cycles after the switch: on the wire in 0 of 13,056 trials.

## Authoritative references

- Milan v1.2: 5.3.3.6, 5.3.8.7, 5.3.11.1, 5.3.11.2 (Tables 5.7, 5.15), 5.4.2.15, 5.4.2.16, Table 5.4, Table 5.6, 6.2 (Table 6.1), 7.1, 7.2.2, 7.2.3, 7.3.2, 7.4, 7.6, 7.6.2.
- IEEE 1722.1-2021: 6.2.2.8, 7.2.6 (Table 7-8), 7.2.9, 7.2.9.1 (Table 7-16), 7.2.9.2 (Table 7-17), 7.2.32 (Table 7-61), 7.4.23, 7.4.23.1, 7.4.24, Table 7-141.
- IEEE 1722-2016: 4.3.2, 4.3.5, 4.4.4.3, 4.4.4.5, 4.4.4.6, 4.4.4.7, 7.2.4, 7.3 (7.3.3, 7.3.5), 7.5, 10.4.3, 10.6, 10.8 (Equations 15 and 16), PICS Table F.7 (AAF-5, AAF-6).
- #629 (the decision in its body, the lane M1 assignments, the [rulings](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5935520588)), #389 (option (a), reversed for AAF), #74 (A2 and its ledger), #632 (phase alignment), protocol-processor #141 (the processor part), PR #630 (bench lane B6, the baseline).
- `docs/design/TIME_SYNC.md`, `docs/reference/FR_NFR.md` (FR-CLK-03, FR-CLK-04), `docs/reference/MILAN_COMPLIANCE_MATRIX.md`, `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` (L6), `docs/design/AREA_BUDGET.md`, `docs/design/SAVED_STATE_FASTCONNECT.md`, `docs/design/SAVED_STATE_MATERIALIZATION.md`; the protocol processor's `docs/architecture/07_memory_maps.md` (L6) and `docs/00_MILAN_COMPLIANCE_REVIEW.md` (REQ-AEM-013, REQ-MDL-005).
- The RTL the round-3 analysis rests on: `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv` (the PI gains, lock rule and rate sampling), `hdl/ieee1722/crf/KL_crf_rx.sv` (the ring, timeout and bind edge), `hdl/ieee1722/avtp/KL_media_clock_restart.sv` (the #387 merge).

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
python3 scripts/check_entity_shape.py
git diff --check d4dd7426 HEAD
# the one measurement the page quotes (Yosys estimate, out of context):
OOC_SHAPE="$PWD/configs/generated/endstation_ax7101_1x1_tdm8" syn/yosys/ooc.sh KL_crf_rx
```

Expected result / pass criteria: every command exits 0. `docs_check` reports 0 findings; `check_em_dash` reports 0 findings over 1,106 added lines in 2 pages; the TOC gate and the anchor check pass; `check_doc_paths` resolves every cited path; `check_entity_shape` reports `checks: 166 failures: 0`. The area run prints `KL_crf_rx` at 433 LUT, 544 FF, 1 RAMB18 and 147 CARRY4, the figures in the page's "Area estimate".

Results at `a463a1de`, each run unpiped with its output to a file: all rc 0.

- `docs_check`: 0 findings across 184 Markdown files and 955 scrubbed text files.
- `check_doc_style`: OK, 22 current documents.
- `gen_toc --check`: OK. `gen_toc --verify-anchors`: 292 links reproduced.
- `check_em_dash --base d4dd7426`: 0 findings over 1,106 added lines.
- `check_doc_paths`: OK, 875 cited paths resolve.
- `check_entity_shape`: `checks: 166 failures: 0`, RESULT: PASS.
- `git diff --check` and `git diff --check d4dd7426 HEAD`: clean.

The area run was not repeated in round 3; round 1 ran it and both round-1 reviews reproduced it.

## Known limitations / out of scope

- Design only: nothing in the page is implemented, and no RTL of this design was simulated. The area figures are estimates scaled from one out-of-context run. The meter's figures come from a desk model of its rules and of the servo's PI, not of any talker or of the servo's RTL; the switch-test figures come from the unmodified restart engine in the pinned HDL simulator.
- No measurement of a real AAF talker's timestamp regularity exists in the repository. The meter is designed for the IEEE 1722-2016 10.8 talker bound plus the CRF timing points' error; the bench lane measures the reference peer's through the meter's status word.
- The CRF path's own 512 ms rate has the same worst-case property under correlated error; it is recorded in the page's Limits and proposed as a separate issue, not designed here.
- The baseline findings page (B6) is cited through PR #630, which is still open.
- Out of scope, by the assignments: every RTL, builder, generator, configuration and processor change, and the requirement amendments themselves (FR-CLK-03, FR-CLK-04 and the #389 record). The page lists each of them as a change for the implementation lanes.
- IEEE 1722-2016 10.8 and 4.3.5 phase alignment is filed as #632 (D7), not designed here.
- The RX monitor's unused external-clock media-lock rule stays #74's ledger item 3.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (this PR covers #629's design step only; it relates to #629 and does not close it)
- [ ] New or changed behavior has self-checking tests (no behavior changes; the test plan is in the page)
- [x] Required local verification bar passes (the Markdown gates and the shape check above, rc 0)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains (none is made; the proposed ones are listed in the page)
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
