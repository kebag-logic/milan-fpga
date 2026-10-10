[R573] POSITIVE - exact head 89464a9b2dbcc6ef2f8beb10a1cb3ee942ef2e54

# R573-2: external independent review of processor PR #172 (issue #170, saved-state lane 3: every user name), round 2

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #172, branch `pp170-names`.
- Exact head `89464a9b2dbcc6ef2f8beb10a1cb3ee942ef2e54`, tree `2949350d820ad16cda288abb624f4cea7a021e70`. The PR head matches it (`receipts/hosted-check-runs.txt`).
- Source base and merge-base: `09e357fb4bf3d35c8a9deba9a787e13f74d08c83`. Processor `main` is now at `336e9f36`, which this PR does not include. The parent's live dev is `aef7ac66`. I did not build the manager's merge-turn candidate.
- Review start: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/172#issuecomment-6092647336
- Round-2 assignment: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/170#issuecomment-6091582915
- Delta reviewed: `c3864686..89464a9b`, five commits on top of `c3864686`. History is linear, with no rebase and no amend (`receipts/scope-and-design-inputs.txt`).

## Reconstruction

I read the sources in this order:

1. The repository README and `docs/README.md`. The repository has no AGENTS.md or CONTRIBUTING.md.
2. The issue #170 body (frozen acceptance items 1–6) and every issue comment: the assignment, the STOP, the manager's ruling on adoption patches and the vendor lock, the round-1 REVIEW READY, the round-2 assignment, and the round-2 REVIEW READY.
3. The PR body at the head, and the D3 §18.3 contract the issue quotes.
4. `git diff 09e357fb..89464a9b` and its history, then the delta `c3864686..89464a9b`.
5. The public author packet at milan-fpga `00db2c38/review-evidence/pp170-r1`. I used it for the round-1 timing logs and `parent-name-evidence.patch`.

I read the prior public review reports (R573-1, R572-1) only after my own pass over the diff and my own probes. I did not read any concurrent reviewer material.

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open. All four round-2 items are resolved at this head, each verified by execution.

- **R573-1-F1 = R572-1-F2 (shipping capacity): resolved.**
  - Every population now builds at its bound capacity, 39 and 107, and again at 128.
  - The new `name_table_last_entry_dropped` control is KILLED at `N3 saved ordinal 38` (39 entries) and at `N3 saved ordinal 106` (107 entries).
  - My round-1 `capacity_probe.sh`, rerun unmodified, now fails the boundary defect in the PR's own suite (`cap128-boundary-synth`: rc 1, at N3/N5 38 and 106). It was rc 0 in round 1.
  - An independent replay-side boundary control I wrote this round fails only at the bound capacity, at N5 38 and 106, and survives at 128. So the new geometry adds real detection.
- **R572-1-F1 (debt protection on names): resolved.**
  - The N9 arm passes at both bound capacities.
  - `rollback_ignores_debt` is KILLED at `N9 debt names:`.
  - Two independent debt defects I wrote are also caught by N9: the debt left unwired at the top, and the guard forgiving the debt at the first beat.
  - A bench edit that removes the late burst fails N9's premise check, so N9 is not vacuous.
- **R573-1-R1 and R572-1 RS1: applied.**
  - The README now carries the round-1 reviewer's exact sentence. That sentence is itself slightly imprecise, so I record a corrected exact fix as a new RESIDUE, R573-2-R1. RESIDUE does not affect the verdict.
  - In 09 §8.2, the heading and the intro edit are verbatim. The closing sentence carries this round's correct counts.

One wording RESIDUE (R573-2-R1) and four suggestions are recorded. None of them affects the verdict.

## Scope and design inputs (tests and docs only)

`receipts/scope-and-design-inputs.txt`:

- **Base to head:** `docs/architecture/09_verification.md` is modified, and six files under `tb/name_state/` are added.
- **Round-2 delta:** `09_verification.md`, `tb/name_state/{README.md,mutants.py,run.py,sim_main.cpp}`.
- **Identical tree objects at base and head:**
  - `hdl` `4d21ab65…`, `syn` `a5e560a6…`, `scripts` `316cdbc8…`;
  - `tb/pp_top` `4c9d4c49…`, `tb/common` `118f4454…`, `tb/acmp_nvm` `6178d41c…`;
  - `.github` `33d4660d…` and the root `Makefile`.
- **Consequence:** RTL, the shared harness, registers, ports, parameters and the 128-record name allocation are byte-identical to the base. That is the design-input identity the DR4 no-re-measure ruling rests on.
- **Gitlinks:** this repository has none.

## Lens 1: Conformance (CLEAN)

Authorities: issue #170 items 1–6; D3 §18.3; Milan v1.2 §5.3.13 (user names persist) and §5.3.12 (IDENTIFY is volatile); IEEE 1722.1-2021 §7.4.17.1 and §7.4.18.2 (SET_NAME/GET_NAME, 64-byte values).

- **Bound geometry (items 1 and 4).**
  - I regenerated both parent images at milan-fpga `5603c353` with the parent builder overlay and `avdecc/gen_aemi_image.py`, using the reviewed packer. Both match the README's identities: 1x1 is 7,512 B, `4fc8d615…396d`; 8x8 is 19,520 B, `d8296833…a7bc` (`receipts/parent-images.log`).
  - The image headers carry `n_names` 39 and 107. The parent's generated `AEM_NAME_ENTRIES_C` is 39 (`endstation_ax7101_1x1_tdm8`) and 107 (`endstation_ax7101_8x8`), which are the values `run.py` `NAMES = {1: 39, 8: 107}` binds.
  - My independent image parser (`scripts/inventory_check.py`) still maps every ordinal identically to the bench oracle: 39 of 39 and 107 of 107 (`receipts/inventory-check.log`).
- **Debt protection (items 3 and 5, "omit descriptor rollback or debt protection").** The debt half now fails a named name-value assertion inside this lane's suite, and the rollback half still fails D3N5. The N9 arm grades exactly what the round-2 assignment required:
  - every entry and GET_NAME at the image default;
  - READ_DESCRIPTOR serving both image ENTITY names;
  - a later SET_NAME of the last ordinal saved and read back.
- **Negative controls (item 5).** The campaign gives golden PASS at both bound capacities and 16 of 16 KILLED. The assignment's "15 of 15" counted the 14 round-1 controls plus the debt control, but the same assignment also required the boundary control, so 16 is the correct total. The author explained this in the REVIEW READY.
- **Measurement (item 6).** DR3a was re-executed at the bound geometry (RTL lens). DR4 rests on the identical design inputs.
- **Limit.** Physical cold-cycle evidence stays outside items 1–6 and is NOT RUN. Nothing here is hardware proof.

## Lens 2: RTL (CLEAN)

- **No RTL change.** The `hdl` tree object is identical (above).
- **The controls' RTL edits match their stated defects:**
  - `name_table_last_entry_dropped` edits `KL_aecp_nvm_writer.sv:1006` to `< N_NAME_P - 1`, which drops only the record of the table's last entry;
  - `rollback_ignores_debt` removes `!desc_debt_i` from the `W_RB` exit at `:870`.
  - Each anchor occurs exactly once.
- **The N9 premise is consistent with the RTL.**
  - `KL_aecp_desc_mem_guard.sv` holds `owed_r` from an accepted request to its terminal beat. The guard's debt survives the store's local reset, and the writer stays in `W_RB` while it is owed (`KL_aecp_nvm_writer.sv:599,869-870`).
  - The instrumented intact run shows cause 6, 11,921 owed cycles inside the roll-back, the restore ending rolled back with the image valid, and all 39 / 107 entries and GETs at the defaults (`receipts/debt-probe.log`).
- **N9's AUDIO_UNIT locator** (`sim_main.cpp:30-37`) reads the image's own index map at the offsets `gen_desc_image.py` documents: `n_entries` @0x08, `index_off` @0x0C, `descriptor_type` @+2, `elem_off` @+8. The premise check requires the locator to be non-zero, cause 6 and debt at roll-back start.
- **DR4: no re-measure, by ruling.** The design inputs are byte-identical, so the recorded 1x1 TDM8 delta stands: +0 LUT / +0 FF / 0 BRAM / 0 DSP against +750 / +400 / 0 / 0, with WNS +3.203 ns. I re-measured nothing and did not recompute the parent OOC digest; the evidence is tree-object identity. The 8x8 post-place obligation stays open and blocked.
- **DR3a, re-executed on the regenerated images** (`receipts/gen-*-measure.log`, `receipts/dr3a-summary.txt`):

  | Shape | Name entries | Worst terminal (clocks) | Worst D3 wait (clocks) |
  |---|---:|---:|---:|
  | 1x1 | 39 | 14,418 | 1,220 |
  | 1x1 | 128 | 15,919 | 1,220 |
  | 8x8 | 107 | 28,714 | 1,908 |
  | 8x8 | 128 | 29,008 | 1,908 |

  - The aggregate budget is 1,000,001 clocks and the per-wait budget is 20,001.
  - The longest record operation is 87 clocks.
  - These figures match the author's 28,714 and 1,908.
  - The 128-entry rows are byte-identical to the round-1 published `name-restore-{1,8}-timing.log`.
  - These are model figures, not hardware latency.

## Lens 3: Robustness (CLEAN)

- **Existing output directory refused.** Pointing `mutants.py` at an existing directory now exits 2 with "output directory already exists", before anything runs. The directory stays empty (`receipts/refuse-existing.log`).
- **Exact-ordinal grading.** `mutants.py` matches `re.escape(assertion) + (?!\d)`, so "N3 saved ordinal 38" can no longer match 380, and "N5 restored ordinal 1" no longer matches 10–19.
- **A crash cannot count as a kill.** A build failure returns BUILD_FAILED. A kill needs rc 1, a printed tally and the named FAIL line. For a control graded in two populations, every run must kill.
- **`run.py`** builds each distinct capacity once (`entries-N/`), runs each population at its bound capacity and then at 128, and keeps the round-1 failure paths: a missing tally, or a crash with zero FAILs, is non-zero.
- **The capacity rebind is exercised.** The unmodified external probe rebinds the `EXTRA` line text. Its `grep -c` guard requires exactly one match, and it still works (`receipts/capacity-probe.log`).
- **Concurrency.** The campaign ran with `--jobs 3` alongside three other reviewer workloads without interference.
- **Reviewer process note.** My first background launch survived a shell reset that I had believed killed it. It then wrote a stale rc and a stale `results.json` into recreated directories. I discarded every artifact that launch could have touched and reran those workloads into new directories. Every receipt cited here comes from a single clean run.
- **Suggestion S1** below covers a new retained-work-directory behaviour.

## Lens 4: Tests (CLEAN)

I verified the pinned simulation compiler 5.050 before use: `--version` gives `5.050 2026-07-01 rev v5.050`, and the wrapper and binary sha256 values are in `receipts/verilator-identity.txt`.

| Run | Result | Receipt |
|---|---|---|
| Normal suite (`run.py`, synthetic): 1x1 at 39 and 128, 8x8 at 107 and 128 | rc 0; 173 + 445 + 173 + 445 = 1,236 checks, 0 FAIL | `receipts/head-normal.*` |
| Generated images, functional | rc 0 / rc 0; 346 (1x1) and 890 (8x8) checks | `receipts/gen-{1x1,8x8}-plain.*` |
| Generated images, `--measure` | rc 0; DR3a as in the RTL lens | `receipts/gen-*-measure.*` |
| Author campaign (`mutants.py --jobs 3`) | rc 0; golden PASS at 39 and 107; 16/16 KILLED, each on its named assertion | `receipts/author-campaign*` |
| `capacity_probe.sh` (round 1, unmodified; sha256 `a6f13785…`) | cap39-1x1 rc 0 (346); cap107-8x8 rc 0 (890); **cap128-boundary-synth rc 1** (N3/N5 38 at 39 entries and 106 at 107; the 128 runs pass); cap39-boundary rc 1 | `receipts/capacity-probe.*`, `receipts/probe-*` |
| Reviewer debt probe (`scripts/debt_probe.py`, N9 alone, instrumented) | intact: 4/4 at 39 and 107; `rollback_ignores_debt`: N9 names, entity and SET fail | `receipts/debt-probe.*` |
| Reviewer controls, round 2 (`scripts/reviewer_controls_r2.py`, full normal entry point) | golden PASS; see below | `receipts/reviewer-controls-r2*` |
| Supplementary boundary control (`scripts/reviewer_controls_r2b.py`) | KILLED: N5 38 (39 entries) and N5 106 (107 entries); 128 runs pass | `receipts/reviewer-controls-r2b*` |
| `make check`, `scripts/gen_matrix.py --check` | rc 0 / rc 0 | `receipts/make-check.*`, `receipts/gen-matrix.*` |

**Author campaign, named assertions (`receipts/author-campaign-summary.txt`):**

- **N3 saved ordinal:** `TRG_name` and `name_record_id_shifted`.
- **N5 restored ordinal:** `RPL_name` and `name_entry_shifted`; `name_empty_refused` (ordinal 2); `name_lanes_partial` (ordinal 1).
- **Arm-level assertions:** `latch_ignores_program` (N7), `name_taint_ignored` (D3N6), `names_before_the_image` (D3N7), `store_not_rolled_back` (D3N5), `identify_survives_reset` (N8), `pending_clears_other_name` (N6).
- **New debt control:** `rollback_ignores_debt` (N9 debt names).
- **Image defaults and live lanes:** `image_names_zeroed` (N1), `live_name_lane_dropped` (N2).
- **New boundary control:** `name_table_last_entry_dropped` (N3 saved ordinal 38 at 39 entries, and N3 saved ordinal 106 at 107 entries).

**Reviewer controls, round 2.** Each plant is written independently of the author's tables. A kill needs a completed run and every required pattern.

- **Round-1 controls, rerun at the new geometry:**
  - KILLED: `R_trigger_odd_dropped` (N3 at ordinal 1), `R_record_id_neighbour` (N3), `R_empty_replay_skipped` (N5 at ordinal 2), `R_pending_clears_higher` (N6) and `R_latch_lane_alias` (N3).
  - `R_replay_skips_locate_wait` again fails N4 ("every name reset to image default before replay", rc 1) instead of the D3N7 I predicted. That is identical to round 1. N4 is a name-value assertion, so the defect is caught. My prediction was wrong; the suite has no gap here.
- **New debt controls:** `R_debt_unwired` (the top ties `d3_desc_debt_i` to 0) is KILLED at N9 debt names in both populations. `R_guard_first_beat` (the guard forgives the debt at the first response beat, an informational control) is also caught at N9.
- **N9 premise:** `R_n9_no_late_burst` (the bench's late burst removed) fails N9's premise check (cause 0, 0 owed cycles), which shows the arm is not vacuous.
- **Excluded control:** `R_name_walk_one_short` edited the `default` branch of `sel_cnt_f`. That function bounds only the scalar groups, and sel 0..5 each have an explicit case, so the edit is an equivalent mutant: rc 0, as it must be. I excluded it and replaced it with `R_restore_walk_one_short`, where `W_NEXT` ends the walk one record early. That control is KILLED only at the bound capacities, at N5 38 and N5 106.

**Mechanism under the debt defects (from `receipts/debt-probe.log`):**

- The store's table entries stay at the image defaults: 0 of 39 and 0 of 107 entries differ.
- The restore ends CLOSED, not rolled back.
- GET_NAME stops answering with the defaults (39 of 39 and 107 of 107 differ), READ_DESCRIPTOR fails, and the later SET_NAME is not saved.
- N9 therefore catches the defect through the served name values, which is the controller-visible consequence. The table-entry conjunct alone would not catch it (see S4).

**Informational merge-tree probe (`receipts/merge-tree-probe.*`).** This is NOT the manager's merge candidate.

- `git merge-tree` of the head with processor `main` `336e9f36` is clean.
- `tb/pp_top/sim_main.cpp`, which the name bench `#include`s, changed on `main`. The normal name suite on the merged tree still gives 1,236 / 1,236, rc 0.

## Lens 5: Docs (CLEAN; RESIDUE R573-2-R1 and suggestions only)

- **README geometry paragraph** (`tb/name_state/README.md:46-52`): it matches `run.py` (bound capacity first, then 128). The image-production note (lines 38-45) matches my regenerated images byte for byte.
- **README counts:** 173 per 1x1 run, 445 per 8x8 run and 1,236 total match the receipts. "Twelve reused … four further controls" matches `mutants.py:31-67`: 12 reused plus `pending_clears_other_name`, `image_names_zeroed`, `live_name_lane_dropped` and `name_table_last_entry_dropped`.
- **README N9 row and paragraph:** they match `sim_main.cpp:152-197`: the 16,000-clock late burst, cause 6, and the three graded properties.
- **09 §8.2:**
  - The heading now ends "(issues #131, #61, #83, #170)", and the intro inserts "the complete name populations in `tb/name_state`". Both are verbatim from R572-1 RS1.
  - The closing sentence (`:233`) reads "16 controls … twelve reused from `d3_mutants.py` and four of its own". That is the RS1 sentence with this round's correct counts; the verbatim 14/eleven/three would now be false.
  - The row at `:204` states the geometry, the debt arm and 16 controls.
  - `make check` passes.
- **R573-1-R1:** applied with the exact sentence from round 1 (`README.md:74-78`). See R573-2-R1 for a precision fix to that sentence.
- **PR body:** its claims (16 controls, 1,236 / 346 / 890 checks, 28,714 clocks, the boundary at 38 and 106, the N9 properties) match my receipts.

## Findings

### R573-2-R1 (RESIDUE): the README's period-90 sentence says all of ordinals 90–106 repeat ordinals 0–16

- **Lens:** Docs.
- **Where:** `tb/name_state/README.md:74-78`. This is the sentence the round-1 review (R573-1-R1) supplied, applied verbatim.
- **Evidence:** values are `33 + (ordinal*11 + byte*7) % 90`, except that every ordinal with `ordinal % 7 == 2` is all-zero (`sim_main.cpp:24-25`).
  - Ordinals 90, 91, 94–98 and 101–105 repeat their o−90 partner: twelve full-length pairs.
  - Ordinals 92, 93, 99, 100 and 106 do not repeat. Either the ordinal itself is empty (93, 100) or its partner is (2, 9, 16).
  - My `inventory_check.py` independently reports 12 non-empty duplicate pairs (`receipts/inventory-check.log`).
- **Impact:** wording only. No test, figure, verdict or claim changes. The sentence's conclusion, that only record ID and CRC separate the repeating pairs, still holds for the twelve.
- **Exact fix:** replace "so in the 8x8 diagnostic ordinals 90–106 repeat the values of ordinals 0–16, and only each saved frame's record ID and CRC distinguish them." with "so in the 8x8 diagnostic twelve of ordinals 90–106 repeat the full-length value of the ordinal 90 below them (all but 92, 93, 99, 100 and 106, where one of the pair is empty), and only each saved frame's record ID and CRC distinguish those pairs."
- **Verification:** the README reads as above. No rerun is needed.

### Suggestions (do not affect the verdict)

- **S1 (Robustness, new in this delta).** With a retained `--work` directory, `tb/name_state/run.py:77-79` reuses an existing `names-<population>.bin` instead of regenerating it. A rerun into the same `--work` after a `fixture.py` or packer change would therefore test the stale synthetic image. Round 1 regenerated the image on every invocation. The default temporary directory, the campaign and every probe here use fresh directories, so no evidence is affected. Suggested change: regenerate once per invocation, for example by keeping the generated path in memory, or refuse a non-empty `--work`.
- **S2 (Robustness; retained R573-1-S4 = R572-1-S5).** `--measure` still asserts nothing ("0 checks", rc 0). CHECKs of terminal ≤ AGG and every wait ≤ RS_TMO would turn a DR3a regression into a failure.
- **S3 (Tests; retained R572-1-S2).** The value pattern still has period 90, so at 8x8 an o↔o+90 replay mapping is invisible to N5 for the twelve pairs. A pattern injective over 128 ordinals would close this.
- **S4 (Docs or Tests).** Under every debt defect tried, the table entries stay at the image defaults, and the N9 kill comes from the served values after a CLOSED restore. The README could say so: "without the debt hold the restore ends CLOSED and the names are no longer served". Alternatively, N9 could add a separate `restore_rb_o` / not-closed check, so the cause is named directly.

## Prior public review findings, resolved or retained at this head

| ID | Severity | Status at 89464a9b | Evidence |
|---|---|---|---|
| R573-1-F1 = R572-1-F2 | MINOR | **Resolved** | bound-capacity runs; campaign KILLED at N3 38 and 106; unmodified probe now rc 1; independent replay-side control fails only at the bound |
| R572-1-F1 | MINOR | **Resolved** | N9 arm; `rollback_ignores_debt` KILLED at N9 debt names; two independent debt controls also fail N9; premise not vacuous |
| R573-1-R1 | RESIDUE | **Applied verbatim** | `README.md:74-78`; precision follow-up in R573-2-R1 |
| R572-1 RS1 | RESIDUE | **Applied** | heading and intro verbatim; closing sentence with correct round-2 counts (`09_verification.md:233`) |
| R573-1-S1 / R572-1-S3 (image production) | SUGGESTION | Taken | `README.md:38-45`, hashes verified |
| R573-1-S2 / R572-1-S4 (existing output directory) | SUGGESTION | Taken | `receipts/refuse-existing.log` |
| R573-1-S3 (prefix grading) | SUGGESTION | Taken | exact-ordinal regex in `mutants.py` |
| R573-1-S4 / R572-1-S5 (`--measure` asserts nothing) | SUGGESTION | Retained (S2 above) | |
| R572-1-S2 (period-90 pattern) | SUGGESTION | Retained (S3 above) | |
| R572-1-S1 (name pending-export check), R572-1-S6 (compliance-matrix citation) | SUGGESTION | Retained, not taken | unchanged files |

## Parent consumer input (`parent-name-evidence.patch`, an adoption input, not part of this PR)

I composed a disposable copy of milan-fpga `5603c353`, with `gptp-processor` at its pin `5dce647a` and the processor gitlink staged at `89464a9b`. It was never committed.

- Without the patch, `scripts/measure_test_evidence.py --check` returns rc 1: "1 unexplained DUT-source reader(s)", namely `protocol-processor/tb/name_state/mutants.py`.
- With the patch, which applies cleanly, the gate returns rc 0: 71 ≤ 77 suites without an arm, 0 ≤ 0 unexplained readers (`receipts/parent-evidence-{unpatched,patched}.log`).
- The disposition text ("name capture, replay and pending defects") predates the debt and boundary controls. The adoption lane may extend the wording. This does not affect the gate.
- I ran no other parent gate. Full parent banks are not allowed in this review.

## Hosted evidence at the exact head (queried 2026-10-10T02:49Z, `receipts/hosted-check-runs.txt`)

- `docs-gates` ×2 and `portability` ×2: completed, success.
- `suites` ×2: still in progress, with no conclusion.
- Combined status: pending.

The manager owns hosted and act acceptance. There is no manager source bank at this exact head, and I neither claim nor infer one. At query time, the public evidence branch held only the round-1 author packet (`00db2c38`). The round-2 gate receipts the REVIEW READY cites (all five processor gates and seventeen parent gates) were not yet archived publicly. I re-executed the name-suite, campaign, DR3a, docs and matrix claims myself. The rest stay the author's claims until they are archived.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #170 items 1–6 and rulings; round-2 assignment; D3 §18.3; regenerated parent images and `AEM_NAME_ENTRIES_C` 39/107; independent ordinal parser; N1–N9, D3N5–D3N7; campaign 16/16 | R573-2 (delta); R573-1 for unchanged files | 89464a9b2dbcc6ef2f8beb10a1cb3ee942ef2e54 |
| RTL | CLEAN | base/head tree identity (hdl, syn, scripts, tb/pp_top, tb/common, tb/acmp_nvm, .github, Makefile); control anchors in `KL_aecp_nvm_writer.sv`; debt guard and `W_RB`; N9 locator against the `gen_desc_image.py` layout; DR3a re-executed at bound and 128; DR4 by design-input identity | R573-2 | 89464a9b2dbcc6ef2f8beb10a1cb3ee942ef2e54 |
| Robustness | CLEAN (S1, S2) | `run.py` geometry loop and failure paths; `mutants.py` refusal, exact-ordinal grading, multi-population verdicts; unmodified external probe rebind; concurrency | R573-2 | 89464a9b2dbcc6ef2f8beb10a1cb3ee942ef2e54 |
| Tests | CLEAN (S3) | normal suite (1,236); generated images (346/890); author campaign; capacity probe; debt probe; 10+1 reviewer controls; `make check`; matrix; informational merge-tree run | R573-2 | 89464a9b2dbcc6ef2f8beb10a1cb3ee942ef2e54 |
| Docs | CLEAN (RESIDUE R573-2-R1; S4) | `tb/name_state/README.md`; `09_verification.md` §8.2 (heading, intro, `:204` row, `:233`); PR body; R573-1-R1 / RS1 application | R573-2 | 89464a9b2dbcc6ef2f8beb10a1cb3ee942ef2e54 |

## Real limits

- **Not run:**
  - the full processor suite bank (1,029,529 checks claimed), HDL lint and the portable synthesis flow;
  - any vendor synthesis. DR4 was not re-measured, by ruling; its evidence is design-input tree identity;
  - all parent gates except the single evidence-reader gate;
  - the merge-turn current-dev candidate.
- **Model figures:** DR3a numbers come from the simulation model with a byte-per-cycle NVM model.
- **No hardware proof:** physical calibration and cold-cycle are NOT RUN, and field skips are not hardware proof.
- **Informational only:** the merge-tree probe against processor `main` `336e9f36` is not manager validation.
- **Clone restored and verified** after all probes (`receipts/clone-restore-verify.txt`):
  - HEAD `89464a9b`, tree `2949350d`, and the index writes the same tree;
  - the worktree and index equal HEAD;
  - zero untracked or ignored entries (the ignored `.venv-wavedrom/` that `make check` creates was removed);
  - all 587 tracked blobs are byte-identical with matching modes;
  - there are no gitlinks.

  The merge-tree probe added unreachable loose objects to the clone's object store. No ref, index entry or tracked file changed. Every probe tree lived under the packet's `scratch/`.

## Pending manager duties

- Hosted acceptance at the exact head, including the two `suites` contexts still in progress.
- Archiving the author's round-2 receipts publicly: the five processor gates, the seventeen parent gates and the design-input digests.
- The merge-turn current-dev candidate (builder and native banks) against processor `main` `336e9f36` and parent dev `aef7ac66`, with its receipts.
- Carrying RESIDUE R573-2-R1 to the residue checklist.
- Making sure the parent adoption lane carries `parent-name-evidence.patch`, or an equivalent entry.
- The separate acceptance of physical cold-cycle and lane 5's combined fault campaign. The 8x8 post-place obligation stays open.

R573-2 FINISHED
