[R699] NEGATIVE - exact head a3e24ac5ef984cb92458f1728f2c275349ae9854

# R699-2: internal cleared-context delta review of PR #786 (issue #396 part A)

- **Head:** `a3e24ac5ef984cb92458f1728f2c275349ae9854`, tree `0b14ef1a593071516d72535e62bce90537c6364e`.
- **Delta reviewed:** `21faa482..a3e24ac5`, one commit by the round-2 executor, six files (REQUIREMENTS.md, TESTING.md, the planner, the release mutant driver, the plan feature and its steps). No RTL, firmware, builder or submodule change. Source base is dev `e76a755a`.
- **Reconstructed from:** AGENTS.md and CONTRIBUTING.md; the round-2 assignment (issue #396 comment 6409763644); REQUIREMENTS.md section 8 (REQ-VER-06); Milan v1.2 6.2 and Table 6.1 (extracted text); the diff; the author's round-2 receipts at `33f88334` `review-evidence/396g-r1/author-r2`; the exact-head hosted check runs. After my own pass I read the prior public findings: my round-1 report (R699-1) and the external round-1 report (R700-1, PR comment 6409757802).
- **Scope rule:** my round-1 ledger stands for code this delta does not touch.

The verdict is **NEGATIVE**. Three MINOR findings are open:

- F1 under Conformance, Robustness, Tests and Docs. Round-1 F1 is retained in part.
- F2 under Conformance, Robustness, Tests and Docs.
- F3 under Tests.

There is no BLOCKER or MAJOR, and no RESIDUE in the delta. Four SUGGESTIONs are recorded. All five R700-1 MAJOR findings and both round-1 residues are resolved at this head. So are R699-1 F2 and F3. RTL is clean.

## Findings

### F1 MINOR: Conformance, Robustness, Tests, Docs. A slip and a one-word corruption in one 64-sample window are misgraded; this can void a run whose arms are all present

This retains round-1 F1 in part.

**Where:**
- `tb/tools/torture_campaign.py:4015-4018`, the `k >= excursion` guard in `_audio_window_events`.
- `:3920-3945`, `_audio_excursion`, which only tests for a return to the offset the window opened on.
- Docs: `docs/testing/TESTING.md:1328-1333` (rules 3 and 4) and `:1365` (arm placement, with no spacing rule). Also `planted_placement` at `tb/tools/torture_campaign.py:4848` and the PR body's limit list.

**Authority:**
- REQ-VER-06 (REQUIREMENTS.md:408): every discontinuity is classified at its sample.
- TESTING 6d rule 3: "One word that leaves the track and returns at once is a `bit-flip`".
- Round-1 F1's required outcome: "a DUT defect with every planted arm present must not void the run".
- The round-2 assignment's item 1: grade compound and edge events exactly.

**Evidence:** `receipts/compound_probe_r2.log` and `receipts/arm_interaction_probe_r2.log`. Both use my independent encoder, not the planner's synthesizer.

When a slip (drop 3, repeat 2 or drop 4096) comes 5 or 40 samples before a one-word corruption on the same channel, three things go wrong:
- **A position-bit flip** (masks `0x80000` and `0x40000`) is reported as a phantom slip pair. For example: `dropped 1024` then `repeated 1024`, with no `bit-flip`.
- **A code-bit flip** (mask `0x100`, the planted arm's own mask) absorbs the slip. The output is `bit-flip n=6 mask 0x00003F00` at the slip's sample, with `dropped 3` moved to just after the flip.
- **A two-word burst** with one mask becomes `dropped 1024` / `repeated 1024`.

At a gap of 100 samples, and with the flip alone, every case is exact.

These are consequences for the release run:

| Probe | Input | Result | Owed |
|---|---|---|---|
| `A2-*-at-440/470/495/498`, `A3` | Standard arms 200 samples apart; one DUT `drop 1` on every channel 2 to 60 samples before the flip arm at 500, or 5 after it | **NOT RUN, "void: a planted arm was missed"** | FAIL |
| `A2-...-at-430` | The same drop 70 samples before | FAIL | FAIL |
| `A1-arms-10/40/63-apart-clean` | A clean capture whose drop, repeat and flip arms are 10, 40 or 63 samples apart | **NOT RUN** (the repeat and flip arms missed) | PASS |
| `A1` at 64 or more apart | The same, wider | PASS | PASS |

The documented limit "Between events less than 64 samples apart, each slip takes the smallest size the positions allow" (`TESTING.md:1343`) is about slip sizes. It does not cover:
- a corruption reclassified as slips;
- a slip moved to another index;
- an arm being lost.

Nothing in TESTING 6d or the plan tells the source to space its arms at least 64 samples apart.

**Impact:**
- An investigation is pointed at the wrong mechanism, and an event is reported at the wrong sample.
- A DUT slip near a planted flip arm makes the run void. That is a broken measurement to re-run, not a failure, so a DUT defect is hidden.
- A source that plants its three arms close together, which the documented schedule permits, voids every run. This direction is fail-safe, but no release could qualify.

**Required outcome:**
- Rules 3 and 4 apply to an excursion inside a window after a slip, measured against the offset in force before that excursion.
- A slip next to a planted arm leaves both events in their classes, at their samples, with the arm found.
- Then one of these for arm spacing:
  - arms closer than 64 samples are graded correctly;
  - or a minimum arm spacing is stated in TESTING 6d and `planted_placement`, and refused by name in `_audio_logs_valid`, rather than discovered as a void run.

**Verification:**
- Rerun `scripts/compound_probe_r2.py` and `scripts/arm_interaction_probe_r2.py` unchanged. Every `K-*` line reads OK, and `A2`/`A3` return FAIL. `A1` at under 64 apart returns PASS, or the documented refusal.
- A new self-test arm fails at this head.

### F2 MINOR: Conformance, Robustness, Tests, Docs. A whole-block slip in the capture's last 63 samples is reported as a code-bit corruption, not as an unresolved slip

**Where:**
- `tb/tools/torture_campaign.py:4199-4203`. `finish` closes the open window with no resync, so `_audio_offset` (`:3892`) has no anchor that fits, and the words are labelled `bad`.
- Claims:
  - `docs/testing/TESTING.md:1345`: "A slip in a capture's last 63 samples cannot be confirmed, so it carries `unresolved`".
  - `counter_limits` at `tb/tools/torture_campaign.py:4846`: "a slip in the last 63 samples of a capture is unresolved".
  - The PR body limit list: "A slip in a capture's last 63 samples carries `unresolved`".

**Evidence:** `receipts/edge_probe_r2.log` (X1, X4) and `receipts/grader_probe_r2.log` (E3).
- A 4096-sample drop at `F-20` to `F-63` is reported on every channel as `bit-flip`, n of 18 to 63, mask `0x00000100`. There is no `unresolved` and no slip class.
- At `F-64` and earlier, the slip is reported as `dropped 4096`, which is exact.
- A non-block drop of 3 in the same span correctly carries `unresolved` (X2).
- A logged capture loss of 4096 frames at `F-30` is NOT RUN, because the loss is not found (X4).

**Judgement:** fewer than 32 or 64 words cannot fix the block, so the signal cannot size this slip. That part is a genuine limit. But the documents state a different behaviour (`unresolved` on a slip) from what the grader does (a code-bit `bit-flip`). And TESTING 6d says "a self-test arm pins each one"; none pins this case. The verdict is still FAIL, so nothing passes falsely. This is MINOR rather than RESIDUE because the fix needs a test, or a code change, not only words.

**Required outcome:** one of these.
- Report an own-tag stretch to the capture's end, whose only mismatch is the code bit, as an `unresolved` slip.
- Or state this limit exactly in TESTING 6d, `counter_limits` and the PR body, including the capture-loss case, and pin it with a self-test arm.

**Verification:** rerun `scripts/edge_probe_r2.py`. X1 at `F-20` to `F-63` reports the documented class, and a self-test arm fails if the behaviour changes.

### F3 MINOR: Tests. The "at or before" boundary of the acquisition index is untested; reviewer mutant N07 survives

**Where:** `tb/tools/torture_campaign.py:4334`, `return index + sum(frames for at, frames in lost if at <= index)`.

**Authority:** `docs/testing/TESTING.md:1379`, "The acquisition index adds every loss logged at or before an event".

**Evidence:**
- `receipts/reviewer_mutants_r2.log`: N07 (`at <= index` changed to `at < index`) SURVIVED. Both the self-test and the plan feature returned rc 0, against a passing pristine control.
- `receipts/n07_probe.log` shows the mutant is not equivalent. Events at the loss index report `acquisition_index` 8214 at the head and 8205 under the mutant, and their `wall_s` moves by 9 frames.

**Impact:** the documented boundary can regress unnoticed. The capture-loss events themselves, and any DUT event at the loss index, would carry the wrong acquisition index and time.

**Required outcome:** a self-test arm or scenario pins the acquisition index and time of an event at a logged loss's own index.

**Verification:** rerun `scripts/reviewer_mutants_r2.py` unchanged. N07 is KILLED with the control still passing.

### S1 SUGGESTION: Robustness. Leading silence

A capture that starts before the stream flows reports its leading zeros as a DUT `silence` event, so the run FAILs (`E1-leading-silence`). Consider stating in TESTING 6d that each capture starts once the counter flows, or how a leading run before acquisition is treated.

### S2 SUGGESTION: Robustness, Docs. The anchor cadence is documented but not checked

TESTING.md:1352 asks for an anchor at least every `audio_context_s` and one at the capture's end. The grader accepts any anchor set, including none. Events then carry null times, the reason, and a count in `timing_unsupported` (`L3`). Verdicts are unaffected. Consider reporting cadence gaps in the detail, so that missing context is visible at grading time.

### S3 SUGGESTION: Robustness. Wrong byte order grades slowly

With a wrong stated byte order, no channel ever acquires. The grader then runs at about 1.6x real time on this host, about 15 h for a 24 h capture, before a verdict (`receipts/throughput_misuse_r2.log`). Consider an early named refusal when no counter channel acquires within a bounded number of frames.

### S4 SUGGESTION: Docs. The window bound is not documented

The 65536-word window bound ("more than 65536 words without 64 clean samples", `tb/tools/torture_campaign.py:4150`) is not described in TESTING 6d. It means a long corrupted stretch is graded in pieces with `unresolved` slips.

## Prior findings at this head

| Finding | Status at `a3e24ac5` | Evidence |
|---|---|---|
| R699-1 F1 (MINOR) | **Retained in part, as F1.** Every round-1 case now classifies by the documented rules: hold, skip then hold, dup then skip at 5, tag-bit flip as `bit-flip` with `matches_channel`, bursts of `0x100`/`0x200` as one `bit-flip`, and static swaps as FAIL `swap` with every arm found. Outside the new patterns of F1, no DUT event voids the run. | `receipts/grader_probe_r2.log` P1 to P8, Q-* (all OK) |
| R699-1 F2 (MINOR) | **Resolved.** G07, G12 and R03 are KILLED, by `test_audio_capture_loss_needs_every_channel`, `test_audio_tag_integrity_decides_first` and `test_release_commit_cut_evidence`. The unmodified round-1 driver: 22 killed, 0 survived, 6 invalid because their anchors were rewritten. Ported equivalents of those six are killed. | `receipts/r1_reviewer_mutants_unmodified.log`, `receipts/reviewer_mutants_r2.log` (G08, G09, N10, N13, N16, N25), `receipts/mutants.log` |
| R699-1 F3 (MINOR) | **Resolved.** The counter now repeats only after 2^43 samples, so a 2048, 4096, 8192, 75776 or 4096000-sample slip is FAIL and exactly sized on every counter path, in both directions and from a late start. The backstop sentence is gone. The end-of-capture edge is F2. | B1, B2 and B3 in `receipts/grader_probe_r2.log` |
| R699-1 R1, R700-1 R1 (RESIDUE) | **Resolved.** No `issuecomment` remains in the planner, steps, feature or mutant driver. `tests/steps/torture_release_steps.py:239` is reworded. The other "round" docstrings there predate the PR (#746). The delta adds no new label, round, reviewer ID or comment ID. | grep of the added lines |
| R699-1 S1, S2 | Adopted: the arms rule is now the first and last tenth (E5 boundary 1637 PASS, 1638 NOT RUN), and the fast path runs per channel (one-channel offset: 281x real time on this host). | `receipts/grader_probe_r2.log` E5, P9 |
| R699-1 S3 | Declined by the executor. That is acceptable, because it is optional. | PR body |
| R700-1 F1 (MAJOR) | **Resolved.** A 4096-sample drop now FAILs. A 3000-sample slip is sized exactly (`test_audio_block_slips_are_sized_exactly`). The whole release fails a 4096 slip with clean AVTP counters. | B1; self-test |
| R700-1 F2 (MAJOR) | **Resolved.** A tag-bit flip or a copied word is `bit-flip`, with mask and `matches_channel`. Only a reciprocal exchange is `swap`. Every container bit is tested. | T1 to T5, P3/P4; N10, N32 killed |
| R700-1 F3 (MAJOR) | **Resolved.** A pending value at its default, all or one, is NOT RUN. A cut outside `[start, end)` is NOT RUN, "the cut hit no journal commit". A bare pending dict never passes. Soft and idle cuts ignore a supplied cut. | R3 to R9; N01 to N04 and R03 killed |
| R700-1 F4 (MAJOR) | **Resolved.** An increment is excused only between two reads inside the input's window. Reads at 0 and 60 s around a 10 to 20 s window FAIL. Edge reads PASS. Before, after and twice-in-one-event all FAIL. | S4 to S4e; N05 and N26 killed |
| R700-1 F5 (MAJOR) | **Resolved.** The acquisition index adds the losses. Times are interpolated between anchors, never extrapolated, and gPTP time never across a recorded step. Unsupported times are null with a reason. The boundary test gap is F3. | L1 to L7; N06, N08, N09 and N24 killed |

## The brief's items

1. **Non-repeating counter.** The period is 2^43 samples. That is 530.2 days at 192 kHz, the highest Milan v1.2 6.2 (Table 6.1) rate, against a 24 h run of 1.66e10 samples at 192 kHz and 4.15e9 at 48 kHz (`B3`).
   - The documents cite 6.2 Table 6.1, which is the clause that lists 48/96/192 kHz. The assignment's pointer, 4.4.2.1, is the Listener presentation-time clause, so the documents' citation is the correct one.
   - A dropped period is detectable (B1).
   - Static swap: FAIL as `swap`, with every arm found.
   - Compound and edge events: exact for every round-1 case, but F1 and F2 at this head.
2. **Tag integrity decides first.** Yes (T1 to T5).
3. **Commit-cut vacuity guard.** Yes (R5 to R7b).
4. **Planted exceptions are local.** Yes (S4 to S4e).
5. **Losses advance the clocks and stay apart from DUT counts.** Yes (L1, L2). See F3 for the boundary test.
6. **4096-multiple slips.** The blind spot is closed on every counter path rather than backstopped. The edge is F2.
7. **Round-1 surviving mutants.** All three fail a named check. One new reviewer mutant survives (F3).
8. **Comment IDs.** None remain.

**Nothing weaker slipped in.** These changes were examined:
- `repeat 2048` moved from the class table to the block-slip test, where it is sized exactly with `located_within`.
- A logged 4096-frame loss that the capture does not show was PASS and is now NOT RUN.
- Start times are still required. Anchors replace invented times.

Every change is equal or stricter. The documents (REQ-VER-06, TESTING 6d, plan args, assertion text, PR body) follow every change, except F1's spacing rule and F2's limit.

## Gates (exact head, this clone, all rc 0)

| Gate | Result |
|---|---|
| `torture_campaign.py --self-test` | 103 OK |
| `torture_release_mutants.py` | 219 killed, source unchanged |
| `cd tests && behave` | 14 features, 469 scenarios, 2206 steps passed |
| Plan feature | 150 scenarios, 585 steps |
| `docs_check.py` | 0 findings over 210 md files |
| `check_doc_paths.py` | 1065 paths |
| `gen_toc.py --check` | Pass |
| `gen_toc.py --verify-anchors` | 538 anchors |
| `check_em_dash.py --base e76a755a` | 0 findings over 296 lines |
| `check_em_dash.py --base 21faa482` | 0 findings over 101 lines |
| `check_doc_style.py` | Pass |
| `check_py_idiom.py` | Within budget |
| `check_feature_status.py` and `--self-test` | Pass |
| `--coverage-by-area --areas soak,audio,power` | Missing `{}` for all three |
| `--plan ... --json` | rc 0 |
| `git diff --check e76a755a HEAD` | Clean |

The Markdown gates ran under the pinned renderer, cmarkgfm 2025.10.22 and html5lib 1.1, in a private venv.

**Author evidence, spot-checked.** The evidence commit `33f88334` is unsigned at the git level. Four receipts were fetched and match the published `MANIFEST.json` sha256 (`receipts/author_r2_spotcheck.sha256`):
- `head.txt` names this head and tree;
- `rc.txt` is all 0;
- `selftest.log` reads 103 OK;
- `round1_head_vs_new_tests.log` shows the new tests failing on round 1's code (55 failures, 6 errors).

**Round-1 probes, unmodified** (`receipts/r1_grader_probe*_unmodified.log`). They encode the superseded 4096-sample counter, so at this head every capture is a non-counter signal. The grader refuses it: no acquisition, and NOT RUN or FAIL. That is the correct response to a wrong layout. The same cases, with only the word encoder ported to the documented layout, are in `scripts/grader_probe_r2.py`.

## Lens coverage

[R699] PASS RTL - `git diff --stat e76a755a..a3e24ac5 -- hdl sw protocol-processor gptp-processor external third_party` (empty); top-level gitlinks `ed211803`/`55680bff`/`efeb541a` equal to base and all six index gitlinks match HEAD (`receipts/restore_check.log`); plan `event_context.csr` SLIP_LB 0x8D4 / SLIP_TDM 0x8D8 unchanged against docs/reference/REGISTER_MAP.md - no RTL in the delta; S32 layout bits 31:8 and pad unchanged.

- **Conformance: UNCLEAN (F1, F2).** Examined:
  - REQUIREMENTS.md:333-445 against Milan v1.2 6.2/Table 6.1;
  - assertion texts `tb/tools/torture_campaign.py:3213-3365`;
  - `check_release_soak_counters` `:3507`;
  - `ReleaseCommitCut` and the commit checks `:3566-3648`;
  - the grader `:3651-4487`.
- **Robustness: UNCLEAN (F1, F2).** Examined: edge, compound, tag, loss, anchor, byte-order and throughput probes (`receipts/*_r2.log`).
- **Tests: UNCLEAN (F1, F2, F3).** Examined:
  - `_ReleaseGateChecks` `:7233-7955`;
  - the plan feature, its diff and the steps diff;
  - author mutants (219);
  - reviewer mutants (31 of 32 killed).
- **Docs: UNCLEAN (F1, F2).** Examined:
  - REQUIREMENTS.md REQ-VER-06;
  - TESTING.md 6d (:1099-1510);
  - plan args `:4826-4870`;
  - the PR body.

### Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | REQUIREMENTS.md:333-445; `tb/tools/torture_campaign.py:3213-3365, 3507-4487`; Milan v1.2 6.2/Table 6.1 text; `receipts/grader_probe_r2.log`, `compound_probe_r2.log`, `arm_interaction_probe_r2.log`, `edge_probe_r2.log` | R699-2 | `a3e24ac5ef984cb92458f1728f2c275349ae9854` |
| RTL | CLEAN | Empty RTL/firmware/submodule diff; gitlinks; REGISTER_MAP SLIP words; S32 layout | R699-2 (delta); R699-1 for the rest | `a3e24ac5ef984cb92458f1728f2c275349ae9854` |
| Robustness | UNCLEAN (F1, F2) | Grader edge, compound, tag, loss and anchor probes; misuse throughput; soak and commit oracle probes | R699-2 | `a3e24ac5ef984cb92458f1728f2c275349ae9854` |
| Tests | UNCLEAN (F1, F2, F3) | Self-test `:7233-7955`; plan feature and steps; `receipts/mutants.log`; `receipts/reviewer_mutants_r2.log`; `receipts/r1_reviewer_mutants_unmodified.log` | R699-2 | `a3e24ac5ef984cb92458f1728f2c275349ae9854` |
| Docs | UNCLEAN (F1, F2) | REQ-VER-06; TESTING 6d; plan `counter_limits`/`planted_placement`; PR body | R699-2 | `a3e24ac5ef984cb92458f1728f2c275349ae9854` |

## Real limits

- **Source validation only.** Gates and probes ran in an isolated clone at the exact head. No manager source bank ran at this head, and none is claimed or inferred. The current-dev merge candidate (base `e76a755a`, live dev `a8594bb9`) is not validated here.
- **No physical evidence.** Physical calibration was NOT RUN. The bench soak, the audio run, the power campaign and the power controls on known-defect images are part B. Desk controls are not hardware proof.
- **Hosted contexts were inspected, not accepted** (`receipts/hosted_checks.log`).
  - Executed and green: `bdd-conformance`, `verilator-lint`, `docs-check-no-git`.
  - Failed, cancelled or skipped: the other contexts, including `rtl-fast` (cancelled), `docs-gates-*`, `docs-check`, `firmware-*`, `verilator-suites`, `yosys-portability` and `full-ci-gate`.
  - The same pattern was recorded at round 1, where install steps failed before any gate ran. This review did not re-diagnose them.
- **Synthetic captures only.** All classification probes use synthetic captures built with an independent encoder. No real capture was graded.

## Pending manager duties

- Route F1 to F3 to the executor.
- Build and validate the current-dev merge candidate (builder and native banks), and link the receipts.
- Hosted and replica acceptance at the final head.
- Carried from round 1: decide the analog sine-pair limits, ratify `restore_bound_s = 30`, and complete the external review at the final head.

## Receipts

Every publishable file is listed in `MANIFEST.sha256`:
- the scripts under `scripts/`, including the round-1 scripts reused unchanged;
- the raw logs and return codes under `receipts/`.

Probes and mutants ran on `git archive` exports of the head. The export's `tb/tools/torture_campaign.py` blob is `c260eb1432`, the same as `HEAD:tb/tools/torture_campaign.py`. The review clone was never modified, and `receipts/restore_check.log` confirms it: HEAD, tree and index tree match, the gitlinks are intact, and porcelain and diff-index are empty.

R699-2 FINISHED
