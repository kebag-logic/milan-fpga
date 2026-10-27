[R699] NEGATIVE - exact head b206d88b937257ca5ccf1753c5fa211605c9f7e6

# R699-6: internal cleared-context delta review, issue #396 part A, PR #786

Head `b206d88b937257ca5ccf1753c5fa211605c9f7e6`, tree `d8140361159b60b52adba7bed317f7e009f49494`. The source base is `e76a755a`. The previously reviewed head is `910d4b94` (R699-5). The delta is three commits: `6c9d566d`, `9c20c08e` and `b206d88b`. They touch six files: `REQUIREMENTS.md`, `docs/testing/TESTING.md`, `tb/tools/torture_campaign.py`, the two release-mutant tables and `tests/steps/torture_release_steps.py`.

## Scope reconstructed

- Issue #396 acceptance 1, 2 and 5, and the desk half of 4. This is part A, per the 2026-10-26 assignment. Items 3 and 4 need the bench (part B) and stay open, so the PR body correctly says "Relates to #396".
- Owner decisions:
  - 2026-10-04 audio design: a bit-exact counter. Item 1: "every discontinuity is classified exactly at its sample". Item 4: "per-event record, to localize the source".
  - 2026-10-26 four decisions: 24 h, 200 cycles (150 cold, 50 at commit, 50 soft resets), the stricter criteria, both documents.
  - 2026-10-26 follow-ups: AECP REBOOT, and the analog limits set at baseline + 6 dB.
- Manager round-6 ruling (issuecomment-6432123822):
  - Item 1, the property: "a capture with any DUT event never grades PASS, and every DUT event is listed at its sample". Exact classification holds only inside a documented scope.
  - Item 2: a seeded fuzz that gates the property.
  - Item 3: H1 and H2 stated outside the scope, and pinned.
  - Item 4: S1.
- The delta's new normative text:
  - REQ-VER-06 (`REQUIREMENTS.md:408-425`);
  - TESTING 6d (`docs/testing/TESTING.md:1294`, rule 4 `:1342-1343`, `:1350`, `:1374-1382`, `:1466-1518`);
  - `AUDIO_COUNTER_LIMITS` (`tb/tools/torture_campaign.py:3747-3804`);
  - the `audio.counter-classified` and planted-arm assertion texts (`:3338-3374`).

## Verdict

**NEGATIVE.** One MINOR finding is open (F1). There are also three SUGGESTIONs and no RESIDUE. There is no BLOCKER or MAJOR.

- The fail-safe half of the new property holds in every probe:
  - 60,000 fresh fuzz seeds, at 16384 and at 8192 frames;
  - a 6,720-case excursion grid;
  - 60,000 isolated single-event cases.
  - Across all of these, no capture with a DUT event grades PASS. The 3 fuzz PASS outcomes are byte-identical to a clean run, as the in-tree check requires.
- The first exactness-scope shape (one event, at least 64 clean samples from everything else) is exact in 60,000 isolated cases. The only deviations are the rule-3 neighbour-word limit and the stated channel-number-clear exception.
- The listing half fails, and the property is universal ("Every capture meets one property"). A constant-mask excursion that a DUT slip interrupts, far from every planted arm, is listed only from the slip on. That lands 1,673 to 3,947 samples after the excursion's first word in my grid, and the gap grows with the excursion. The new gate does not reach this shape at its seeds.
- All R699-5 findings are resolved at this head (table below). The three delta commits are one line each, with no trailers.

## Findings

### F1 MINOR: Conformance, Robustness, Tests, Docs. A constant-mask excursion interrupted by a DUT slip is listed only from the slip, not within 63 samples of its first word

**Where:**
- The claims the delta adds:
  - `REQUIREMENTS.md:408-411` ("Every capture meets one property ... Each such event is listed within 63 samples of its sample, on each channel it changes");
  - `docs/testing/TESTING.md:1486-1490`;
  - `AUDIO_COUNTER_LIMITS[0]` at `tb/tools/torture_campaign.py:3748`;
  - the `audio.counter-classified` text at `:3338` ("each is listed within 63 samples of its sample unless it masks a planted arm");
  - the PR body, Round 6 item 1.
- The gate that claims to prove it: `test_audio_compositions_never_pass_and_list_every_event` (`:9461`), with its generator `_fuzz_units` at `:9378`.
- The reading is made in `_CounterScan`'s window reading. This location is inferred from the outputs; I did not trace the cause in the code.

**Authority:**
- Owner audio design, 2026-10-04:
  - item 1, "Every discontinuity is classified exactly at its sample";
  - item 4, the per-event record "to localize the source", with its wall and gPTP times and a counter walk either side of the event.
- Manager round-6 ruling, item 1: "every DUT event is listed at its sample". The delta implements this with a 63-sample tolerance.
- The delta's own REQ-VER-06 sentence at `REQUIREMENTS.md:409`.

**Evidence** (`scripts/probe_case.py`, `scripts/probe_gap.py`, `scripts/probe_fuzz.py`, `scripts/probe_seed.py`; receipts named below):
- Minimal case. It uses the sweep's six planted arms at 16384 frames, with tolerance 2 (`_sweep_grade`).
  - The events are XOR `0x80100` over channel 0's words 4424 to 6149 (1,726 words) and a DUT repeat of 3 at 6097 on every channel. The nearest arm is 700, more than 3,700 samples away.
  - The verdict is `FAIL`.
  - Channel 0's DUT events start at 6097 (`dropped 1021`, then `bit-flip 0x100` pieces, then `repeated 1024` at 6150).
  - Nothing is listed on channel 0 from 4424 to 6096, so the excursion's first 1,673 words are not located (`receipts/case_reach.txt`, row `0x00080100` at 4424; `receipts/case_4424.txt`).
  - Two controls behave as stated:
    - The same excursion without the slip is one `bit-flip 1726 0x00080100` at 4424, as the in-scope isolated rule says (`receipts/case_4424_no_slip.txt`).
    - The same excursion with its slip, started at 900, is listed at 900 (`receipts/case_reach.txt`).
- Grid (`receipts/gap_16384.json`). The grid has 6,720 cases:
  - excursions of 300 to 4,000 words, from 21 start positions;
  - a drop or repeat of 3 or 17, placed 53 or 300 words before the excursion's end;
  - eight masks, all away from the arms.
  - Results:
    - 48 cases list channel 0's first DUT event more than 63 samples after the excursion starts.
    - The largest gap is 3,947: a 4,000-word excursion with the slip 53 words before its end.
    - The masks are `0x00080100` (27 cases) and `0x00040000` (21 cases), and both are composition-sweep mask classes.
    - Every case grades `FAIL`; none passes.
- Its own generator reaches the shape. `_fuzz_units` and `_fuzz_check`, unchanged, were run over seeds 2,000,000 to 2,019,999 at 8192 frames, the sweeps' other capture length (`receipts/fuzz_8192_2M.json`, `receipts/fuzz_8192_violations_detail.txt`).
  - 2 of 20,000 seeds violate the check.
  - Seed 2007597 is this shape. Its excursion is 1,726 words under `0x80100` at 4424, and the DUT repeat of 3 at 6097 falls inside it. The run is void for an unrelated arm (a DUT drop of 17 on the 7492 drop arm), and the excursion has no listing within 63 samples.
  - The other violating seed is S1 below.
  - At 16384 frames, 40,000 fresh seeds (1,000,000 to 1,039,999) show 0 violations (`receipts/fuzz_16384_1M.json`). This agrees with the author's 70,000 seeds at 16384. The shape is rare there because the generator puts an excursion beside an arm or near an earlier event, and rarely brackets a later slip.
- The grader's behaviour here is likely unchanged since `910d4b94`: the delta changed only the void reason's text in the grader. The universal listing claim, and the gate presented as its proof, are new in this delta.

**Impact:**
- The release verdict is still `FAIL`, so no defective image passes.
- The per-event record is wrong for the very case it exists for. The record names the slip, not the corruption that began up to 3,947 samples (82 ms at 48 kHz) earlier in my grid. Without a slip, the same excursion is recorded at its first word. The gap grows with the excursion length: an investigator is pointed at the wrong sample and the wrong wall and gPTP time.
- A normative REQ-VER-06 sentence is false, and the gate described as proving the property does not test this composition.

**Required outcome:** either of these.
- The grader lists, on every channel it changes, a DUT event within 63 samples of the first word of a constant-mask excursion that a slip interrupts. The class may be any class: outside the scope, the ruling allows another class.
  - The shape is pinned by a self-test arm that fails at `b206d88b`.
  - The gate's generator reaches it: for example, a placement that puts a slip inside an earlier long excursion, or the 8192-frame length.
- Or, if that is not a contained change, publish the limit and get a decision first. Stating it narrows the ruling's property ("every DUT event is listed at its sample"), so it needs a public manager decision before it is written. After that decision:
  - REQ-VER-06 `:409`, TESTING `:1488`, `counter_limits[0]`, the assertion text at `:3338` and the PR body each state the shape and its listing gap;
  - the shape is pinned.

**Verification:**
- `scripts/probe_gap.py`, unchanged, reports `gap_over_63: 0`, or only cases inside a newly stated and decided shape.
- `scripts/probe_fuzz.py <head> 8192 2000000 2020000 ...` no longer reports seed 2007597.
- The new self-test arm fails at `b206d88b`.

### S1 SUGGESTION: Tests. Define "its sample" for overlapping events, and widen the oracle's cancellation allowance

- Seed 2017152 at 8192 frames is the second violation in `receipts/fuzz_8192_2M.json`. It is an oracle artefact, not a grader defect.
  - Two excursions under the same mask `0x80100`, 96 and 1,571 words, both start at 2773 on channel 2.
  - Their first 96 words cancel, so the bytes change only from 2869, and the grader lists `bit-flip 1475` exactly there.
  - `_fuzz_check` measures from the 1,571-word unit's nominal sample, 2773. Its cancellation allowance removes only whole units, so the case is flagged.
- The self-test's fixed seeds do not hit this. A change of seeds, frames or generator could produce a spurious failure, though.
- Measuring each unit from the first word it changes in the composed capture, or keeping same-channel corruptions from overlapping, would make the oracle match the property's text ("a DUT event the bytes show").

### S2 SUGGESTION: Tests. The masked allowance is wider than the stated exception

- In a void run, `_fuzz_check` (`tb/tools/torture_campaign.py:9446-9449`) excuses an unlisted unit when any missed arm lies within that unit's span ±2 and matches its channel. That holds even when another unit caused the miss.
- The stated exception is narrower: "a DUT event that masks a planted arm at its sample" (`TESTING.md:1490`).
- A void blocks the release, so this cannot hide a release defect. Tying the allowance to the unit whose removal restores the arm would make the gate check the sentence as written.

### S3 SUGGESTION: Docs. A dated timeout figure in the PR body's history

- The PR body's mutant-timing paragraph still reads "against the driver's 600". That paragraph is about `910d4b94`, so it is accurate for that head.
- A clause such as "(1200 from `9c20c08e`)" would keep a cold reader from taking 600 as current.
- This is optional, because the sentence is dated by its head.

## Prior findings at this head (R699-5 and earlier R699 rounds)

| Finding | Status at `b206d88b` | Evidence |
|---|---|---|
| R699-5 H1 (MINOR): a multi-word excursion over a slip arm voids the run | **Resolved under ruling item 3, second option.**<br>Stated outside the exactness scope:<br>- `REQUIREMENTS.md:422-423`;<br>- `TESTING.md:1379-1382`, `:1512-1515`;<br>- `counter_limits` `:3800-3801`.<br>The void reason now names a possible DUT cause, and the shape is pinned by `test_audio_excursion_over_a_slip_arm_may_void`. | Self-test OK. The control "a missed arm's void reason without its possible DUT cause" is killed by that test (`receipts/mutants_delta.json`). |
| R699-5 H2 (MINOR): a channel-number-clearing excursion splits at zero words | **Resolved under ruling item 3, second option.**<br>Stated:<br>- `TESTING.md:1294`, rule 4 `:1342-1343`, `:1516-1518`;<br>- `counter_limits` `:3802-3803`;<br>- the scope exception at `REQUIREMENTS.md:419`.<br>Pinned by `test_audio_excursion_clearing_its_channel_number_is_split`. My isolated probe classes every other isolated excursion exactly (457 + 246 channel-clear cases are counted as out of scope). | `receipts/iso_16384.json`, `receipts/iso_8192.json`. The control "a zero word after a stored word kept as data" is killed. |
| R699-5 R1 (RESIDUE): "no slip that did not happen" | **Resolved:** `TESTING.md:1374`, `REQUIREMENTS.md:421`, `counter_limits` `:3760`, the `_unbalanced` docstring `:4902` and the balance arm's docstring `:9259`. | Read at head |
| R699-5 S1 (SUGGESTION): the mutant timeout margin | **Adopted:** `tb/tools/torture_release_mutants.py:909`, 1200 s per control. A `TimeoutExpired` escapes `main`, so a timeout exits non-zero and never counts as a kill. The pristine baseline keeps 600 s. | Read at head |
| R699-5 S2 (SUGGESTION): widen the two sweeps | Not adopted; it is optional. The new fuzz covers both shapes for the property. | PR body |
| R699-5 S3 (SUGGESTION): name a DUT cause in the void reason | **Adopted:** `AUDIO_ARM_MISSED_REASON` `:3725`, returned at `:5295`. The re-anchored control "missed arm accepted" is killed. | `receipts/mutants_delta.json` |
| R699-1 to R699-4 findings | Resolved as R699-5 recorded. The delta changes none of the code they depend on: the grader's only change is the void reason's text. | `git diff 910d4b94..b206d88b -- tb/tools/torture_campaign.py` |

## Prior findings of the external review (read after the verdict and ledger above were written)

| Finding | Status at `b206d88b` | Basis |
|---|---|---|
| R700-1 F1 to F5 (MAJOR) and R1 (RESIDUE) | **Resolved**, as R700-2 recorded at `a3e24ac5`. R700-1 F1 was retained there as R700-2 F1. | Their causes are untouched by `910d4b94..b206d88b`:<br>- the counter layout and its period;<br>- tag integrity (rule 1);<br>- commit-cut snapshots;<br>- planted-exception windows;<br>- capture-loss clocks.<br>The grader's only delta change is the void reason's text. The power-area and soak checks are unchanged. My isolated probe grades 6,631 swaps and 6,653 copies exactly. |
| R700-2 F1 (MAJOR): capture-boundary slips earn PASS | **Resolved**, as R700-3 recorded at `4d69e192`. It is unaffected by the delta: the qualified interval and `_audio_qualified` are unchanged. | The code is unchanged, so R700-3's resolution stands. My fuzz places events at 200 to `frames - 160`, so it does not re-test the capture boundary itself; it found no PASS with a DUT event. |
| R700-2 F2 (MINOR): the constant-mask rule at 64 samples | **Resolved**, as R700-3 recorded. The delta only scopes the rule's text. | Isolated excursions of 2 to 2,100 words read as one `bit-flip` with their mask in 12,717 in-scope cases. |
| R700-3 S1 (SUGGESTION): pin two compound ambiguities | Optional, and still not pinned. The new exactness scope now puts such compound shapes outside exact classification, which covers the concern in text. | `TESTING.md:1500-1511` |

## Gates and probes at this head (my receipts; rc 0 unless stated)

**Gates:**
- `python3 -B tb/tools/torture_campaign.py --self-test`: 119 tests OK in 31 s (`receipts/selftest.log`).
- `python3 -B -m behave tests/features/torture_campaign_plan.feature`: 176 scenarios. `cd tests && behave`: 14 features, 495 scenarios, 2286 steps.
- `docs_check.py`: 0 findings. `check_doc_paths.py`: OK. `check_doc_style.py`: OK. `check_py_idiom.py`: at ratchets. `check_feature_status.py` and `--self-test`: 0 findings, 46/46.
- `gen_toc.py --check`, `--verify-anchors` and `check_em_dash.py --base e76a755a`: 0 findings, under the pinned renderer in a scratch virtual environment. Without the renderer these exit 2, "renderer not installed", and those runs are not counted.
- `--coverage-by-area --areas soak,audio,power`: complete, `missing` empty. `git diff --check e76a755a HEAD`: clean.

**Delta controls:**
- Run in parallel with the driver's criteria (`scripts/probe_mutants.py`, `receipts/mutants_delta.json`).
- The five added controls and the re-anchored "missed arm accepted" are each killed by their named test, in 27 to 34 s each.
- The author's serial driver run at this head, `PASS: 294 mutations killed; source unchanged` (03:17 to 06:01 UTC), was hash-verified and not rerun.

**Property probes:**
- `scripts/probe_fuzz.py`, the in-tree `_fuzz_units` and `_fuzz_check`, unchanged:
  - 40,000 seeds at 16384 frames: 0 violations, 1 PASS (clean);
  - 20,000 seeds at 8192 frames: 2 violations (F1 and S1), 2 PASS (clean).
  - It reproduces the self-test's 288 seeds with 0 violations (`receipts/fuzz_repro_0_288.json`).
- `scripts/probe_isolated.py` (one event, at least 70 samples from every arm, exact class, size and sample): 40,000 seeds at 16384 and 20,000 at 8192, 0 violations.
- `scripts/probe_gap.py`: F1's grid.

**Author evidence, spot-checked** (commit `61320df0`, unsigned at the git level, like the head):
- 26 files under `review-evidence/396g-r1/author-r6/` were downloaded and their sha256 checked against the packet's `MANIFEST.json`. All match (`receipts/author_evidence.sha256`, `receipts/author_evidence_check.log`).
- `head.txt` names this head and tree. The serial driver log ends `PASS: 294 mutations killed`. The self-test log reads 119 OK. `fuzz_range/summary.txt` reports 69,994 non-PASS, 6 PASS and maximum reach 62, all at 16384 frames, which agrees with my 16384 run.

**Hosted, inspected only** (`receipts/hosted_check_runs.tsv`, 56 runs when read):
- 45 completed successfully, among them `rtl-fast`, `docs-check`, `elaborate`, four Yosys shards and `yosys-elaboration`.
- 10 Verilator shards were still in progress.
- 1 was skipped.
- The manager owns hosted and act acceptance.

**Clone restored:** the clone was never modified. Probes ran on a copy. The checks below are in `receipts/restore_check.log`:
- the porcelain and ignored lists are empty;
- the index matches the tree (same `ls-files -s` digest);
- all four gitlinks are unchanged.

## Documents and the comment rule

- No line the delta adds names a lane label, review round, reviewer ID or comment ID. `L3` is the repository's test-level tag. The new mutant names and docstrings describe behaviour only. There is no new RESIDUE of this kind.
- R1's fix is in. The scope sentences match the code for the three in-scope shapes, apart from F1's listing claim. I probed shape 1. Shapes 2 and 3 are the in-tree sweeps, and they pass.

## Lens coverage

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Issue #396 acceptance 1, 2, 4 (desk) and 5. Owner decisions 2026-10-04 and 2026-10-26 (both). Round-6 ruling items 1 to 4. `REQUIREMENTS.md:402-430`. Assertion texts `tb/tools/torture_campaign.py:3338-3374`. `AUDIO_COUNTER_LIMITS` `:3747-3804`. Void reason `:3725` and `:5295`. My fuzz, isolated and gap probes. | R699-6 | `b206d88b937257ca5ccf1753c5fa211605c9f7e6` |
| RTL | CLEAN | No RTL, firmware, builder or submodule change in `e76a755a..b206d88b`. All four gitlinks are identical to the base (`receipts/rtl_scope.log`). The counter word layout is `TESTING.md:1286-1294`. Coverage for the unchanged rest was banked by R699-1 and holds, because nothing in RTL scope has changed since. | R699-6 for the delta; R699-1 for the rest | `b206d88b937257ca5ccf1753c5fa211605c9f7e6` |
| Robustness | UNCLEAN (F1) | 60,000 fuzz compositions at two capture lengths; 60,000 isolated events (slips 1 to 5000 including whole blocks, silences replaced and inserted, swaps, copies, one-word corruptions, excursions to 2100 words); a 6,720-case excursion-plus-slip grid; reach cases up to 60,000-word excursions. | R699-6 | `b206d88b937257ca5ccf1753c5fa211605c9f7e6` |
| Tests | UNCLEAN (F1) | `_fuzz_unit`, `_fuzz_units`, `_fuzz_reach`, `_fuzz_clean`, `_fuzz_check` and the three new arms (`:9353-9519`). `tb/tools/torture_release_audio_mutants.py` (5 added). `tb/tools/torture_release_mutants.py` (1 re-anchored, timeout). `tests/steps/torture_release_steps.py:606`. Six delta controls run. Self-test, behave tier and plan feature. The author's 294-control serial log hash-verified. | R699-6 | `b206d88b937257ca5ccf1753c5fa211605c9f7e6` |
| Docs | UNCLEAN (F1) | REQ-VER-06 `REQUIREMENTS.md:402-430`. TESTING 6d `:1286-1518`. `counter_limits`. The `_read` and `_unbalanced` docstrings. The PR body's Round 6 section and risks. The docs, TOC, anchor, em-dash, style and path gates. | R699-6 | `b206d88b937257ca5ccf1753c5fa211605c9f7e6` |

## Real limits

- My probes are seeded samples and grids, not exhaustive. F1 is a counterexample. The absence of other violations proves nothing beyond the cases run.
- F1's cause in the grader is inferred from outputs, not traced in the code.
- Physical calibration was NOT RUN. Acceptance items 3 and 4 (bench) are not addressed by part A, and field skips are not hardware proof.
- No manager source bank runs at this head, and I claim none. Source-head execution evidence here is my own focused gates and probes plus the author's published receipts.
- I did not rerun the full 294-control serial driver. I ran the six delta controls and hash-checked the author's full run.
- The TOC and em-dash gates ran under a scratch virtual environment holding the pinned renderer's hash-locked requirements, not a shared install.

## Pending manager duties

- Route F1 to the author, deciding first which option applies. Option 2 narrows ruling item 1's property and needs a public decision.
- Build and validate the current-dev merge candidate. The source base is `e76a755a` and live dev is `97aab1d0f28bd753a3e11df6278d5cac54f964dd`. Bank the builder and native receipts, and link them on the PR.
- Hosted and act acceptance at the exact head. Ten Verilator shards were in progress when I read them.
- Carry forward the author's still-open routing items: owner decision issuecomment-6409128703 is outside the plan text, and `restore_bound_s = 30` is provisional.

## Receipts

Listed in `MANIFEST.sha256`. The scripts run with `python3 -I -B <script> <path to a torture_campaign.py> ...` and import only that file.

R699-6 FINISHED
