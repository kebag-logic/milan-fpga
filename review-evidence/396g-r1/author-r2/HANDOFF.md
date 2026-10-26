# HANDOFF: #396 part A round 2 (release gate plan), executor [A674b]

Status: **REVIEW READY** at `a3e24ac5ef984cb92458f1728f2c275349ae9854`
(tree `0b14ef1a593071516d72535e62bce90537c6364e`), branch `396-release-gate-plan`.
One round-2 commit on top of the round-1 head `21faa48242e021177a1dc702f28e51347c6a7a57`, which is
not rewritten; base dev `e76a755afc0536453161e3cd33f6f4d2dcd7641f`. Not pushed. No PR operation.

- Round-2 assignment: #396 issuecomment-6409763644. Findings answered: R699-1 (PR #786
  issuecomment-6409756577) and R700-1 (issuecomment-6409757802), with their published probes and mutants.
- TAKEN: issuecomment-6410118618. REVIEW READY - round 2: issuecomment-6411596557.
- Remote checked: `origin` is `https://github.com/kebag-logic/milan-fpga.git`; merge base `e76a755a`.
  No git command ran inside any submodule; gitlinks unchanged. No RTL, firmware, builder, hardware,
  bench or flashing action.
- Commit: `Make the audio counter non-repeating and grade tags, holds, commit cuts, planted windows and
  capture-loss clocks exactly (#396)`: one line, no body, no trailer.

## Citation note (published in TAKEN)

The assignment cites Milan v1.2 4.4.2.1 for the sample rate. In the Milan v1.2 text, 4.4.2.1 is
"Presentation Time supported by Listener" (buffer up to 2.126 ms). The sample-rate set {48, 96, 192 kHz}
is 6.2, Table 6.1. The counter's period is stated against 6.2's 192 kHz maximum.

## Findings and fixes (file:line at `a3e24ac5`)

| Finding | Fix | Reason |
|---|---|---|
| R700 F1, R699 F3 (assignment 1, 6): a repeating payload cannot prove zero glitches; the 4096-multiple backstop was untrue | `tb/tools/torture_campaign.py:3651`-`:3764`: sample bits 15:12 keep the channel number, bits 11:1 carry the position modulo 2048, bit 0 one bit of a 32-bit block code (block x `0x9E3779B1` mod 2^32), `audio_counter_word` `:3699`, `_audio_decode` `:3752` | Non-repeating for 2^43 samples (530 days at 192 kHz, Milan v1.2 6.2) inside the decided -47 dBFS envelope; 64 clean samples fix the absolute position, so every slip is sized exactly, and the backstop claim is gone |
| Same | `_CounterWindow` `:4047`, `_CounterScan` `:4107`, `_close` `:4164`: a mismatch opens a window that closes at the next 64 clean samples, whose decoded position sizes every slip | Exact sizes; a slip of whole 2048-sample blocks carries `located_within` (`_audio_slip` `:3948`) |
| R700 F2 (assignment 2): tag corruption read as a swap | `_partner` `:4152` (reciprocal exchange only), `_audio_labels` `:3854` (tag first), `_audio_extend` `:3965` (`matches_channel`) | A flipped or copied channel number is a `bit-flip` with its exact mask; only a reciprocal exchange is a `swap` |
| R699 F1 (assignment 1): compound and edge events, static swap voids the run | `_audio_duplicate` `:3911`, `_audio_excursion` `:3920`, `_audio_window_events` `:4000`, identities in `finish` `:4199`, `carriers` `:4222` | A word equal to a received neighbour is a repeat (hold = 1 repeated then 1 dropped); a net-zero excursion with one XOR mask is one corruption; numbers acquired at capture start, so a static swap FAILs as a swap with its arms found |
| R700 F3 (assignment 3): pending defaults defeat the vacuity guard; a cut that hit no commit | `ReleaseCommitCut` `:3566`, `_release_cut_refusal` `:3578`, `check_release_state_restored` `:3589`, `_release_commit_restored` `:3628`; plan `cut_evidence`/`pending_values` `:4944` | A pending value at its default is NOT RUN; a cut instant outside `[start, end)` is NOT RUN as "the cut hit no journal commit"; a bare pending dict can FAIL but never PASS; idle and soft-reset cycles ignore a pending snapshot |
| R700 F4 (assignment 4): planted exceptions widened to the read interval | `check_release_soak_counters` `:3507`, match rule `:3554`; assertion text `:3209`; plan `planted_event_reads` `:4749` | An increment is excused only between two reads inside the planted window |
| R700 F5 (assignment 5): capture losses did not advance the clocks | `_audio_timing` `:4320`, `_audio_anchors_valid` `:4305`, `CounterCapture.anchors`/`gptp_steps_wall_s` `:4364`, `acquired_frames`/`duration_s` in `grade_audio_counter_capture` `:4422` | Acquisition index = stored index + every loss logged at or before it; times interpolated between the capture tool's anchors, never extrapolated, gPTP never across a recorded discontinuity; unsupported times are null with a reason |
| R699 F2 (assignment 7): G07, G12, R03 survive | G07 anchor kept in `_audio_attribute` `:4270`; G12 anchor kept in `_audio_extend` `:3965`; R03 anchor kept in `check_release_state_restored` `:3589` | Each now fails a named arm (below); the reviewer's script, rerun unchanged, reports all three KILLED |
| R699 R1, R700 R1 (assignment 8): residues | `torture_campaign.py:3321` and `:3652` comments; `tests/steps/torture_release_steps.py:239` docstring | No issue-comment ID or review word in source comments |
| R699 S1: adopted | `AUDIO_ARM_EDGE_DIVISOR` `:3690`; edges in `grade_audio_counter_capture` | "At the start and at the end" is the first and the last tenth of the capture |
| R699 S2: adopted | `_CounterScan.frames` `:4123` | The fast path runs per channel; an offset channel or a channel without the counter no longer falls to the slow path |
| R699 S3: declined | none | Tables 4.1/4.2 holds are outside the decided criteria; recommend the manager files its own Issue |
| Assertion texts | `:3336`, `:3347`, `:3352`, `:3358`, `:3278` | Each assertion states the new rule and its limits |
| Plan contract | `counter_layout` `:4827`, `counter_limits` `:4837`, `capture_timing` `:4853`, `event_record`; control fixture `:4785` | The emitted plan carries the layout, period, limits and timing rule |
| Docs | `REQUIREMENTS.md:336`, `:402`-`:419`, `:442`-`:444`; `docs/testing/TESTING.md:1102`, `:1115`-`:1120`, `:1281`-`:1380`, `:1410`-`:1418`, `:1506`-`:1508` | REQ-VER-06 and TESTING 6d follow every change, with the bit-identical limits stated |

Bit-identical limits, each pinned by a self-test arm (TESTING 6d lists them):

- a flip of position bit 0 can make a word equal to its neighbour; it then reads as that slip pair
  (`test_audio_tag_integrity_decides_first` computes which bits do so independently);
- a slip pair whose displaced words share one XOR mask reads as a `bit-flip`
  (`test_audio_compound_and_edge_events`, searched case);
- a slip of whole blocks is located to an interval under 64 samples (`test_audio_block_slips_are_sized_exactly`);
- between events under 64 samples apart, intermediate slip sizes are the smallest the positions allow;
- a slip in the last 63 samples carries `unresolved` (`test_audio_compound_and_edge_events`).

## New checks (planted mutant, failing words)

New self-test arms (`tb/tools/torture_campaign.py`): `test_release_commit_cut_evidence` `:7356`,
`test_audio_compound_and_edge_events` `:7533`, `test_audio_tag_integrity_decides_first` `:7570`,
`test_audio_static_swap_fails_with_every_arm_found` `:7601`, `test_audio_block_slips_are_sized_exactly` `:7613`,
`test_audio_capture_losses_advance_the_clocks` `:7636`, `test_audio_capture_loss_needs_every_channel` `:7697`,
`test_audio_arms_run_at_both_edges` `:7705`, `test_audio_offset_channel_and_mixed_capture` `:7740`;
rewritten: `test_release_soak_media_unlocked_planted` `:7265`, `test_release_state_commit_cut` `:7338`,
`test_audio_counter_word_layout` `:7454`; adapted: `test_audio_grader_classes` `:7781`,
`test_audio_grader_attribution` `:7823`. `_independent` `:7484` builds captures from `_word` `:7448`, the
documented layout restated, never the planner's synthesizer.

Each arm fails on round 1's code: `receipts/round1_head_vs_new_tests.log` (round-1 planner with the
round-2 test class transplanted) lists all 14 new or changed arms failing, 55 failures and 6 errors.

The 36 planted defects this round adds or re-anchors in `tb/tools/torture_release_mutants.py`
(`:664`-`:885`), with the words the unchanged self-test fails with (`receipts/mutant_failing_words.log`):

| Planted defect | Named arm | Failing words |
|---|---|---|
| planted window need only meet the read interval | `test_release_soak_media_unlocked_planted` | `'PASS' != 'FAIL'` |
| planted window excludes its start read / end read | same | `'FAIL' != 'PASS'` |
| audio control drop removed (re-anchored) | `test_release_controls_fail_as_planted` | `'PASS' != 'FAIL'` |
| lone corrupted word kept as a slip pair | `test_audio_tag_integrity_decides_first` | `Lists differ: ... 'dropped' ... != ... 'bit-flip', 1, '0x00000400'` |
| slip size not folded around zero | `test_audio_grader_classes` | `'NOT RUN' != 'FAIL'` |
| inserted silence not told apart | `test_audio_grader_classes` | `8 != 4` |
| swap read as corruption | `test_audio_grader_classes` | `'bit-flip' != 'swap'` |
| arm position ignored | `test_audio_grader_attribution` | `'PASS' != 'NOT RUN'` |
| arms need not bracket the run | `test_audio_grader_attribution` | `'FAIL' != 'NOT RUN'` |
| arm edges widened to the halves | `test_audio_arms_run_at_both_edges` | `'PASS' != 'NOT RUN'` |
| fast path compares the capture with itself | `test_audio_grader_classes` | `'NOT RUN' != 'FAIL'` |
| block code bit dropped from the word | `test_audio_counter_word_layout` | `1048576 != 1048832` |
| counter repeats every 4096 samples | `test_audio_counter_word_layout` | `3152384 != 3152640` |
| decode ignores the block code | `test_audio_counter_word_layout` | `None != 2047` |
| expected words lose the block code | `test_audio_counter_word_layout` | `b'\x00\n\x10...' != b'\x00\x0b\x10...'` |
| planted flip mask leaves the code bit | `test_audio_counter_word_layout` | `512 != 256` |
| block slips not located | `test_audio_block_slips_are_sized_exactly` | `False is not true : {... 'n': 2048 ...}` |
| foreign channel number read as a swap | `test_audio_tag_integrity_decides_first` | `Lists differ: ... 'swap' ... != ... 'bit-flip', 1, '0x00100000'` |
| swap run spans a partner change (R699 G12) | `test_audio_tag_integrity_decides_first` | `Lists differ: [(0, 3000, 'swap', 6, ...` |
| constant-mask excursion kept as slips | `test_audio_compound_and_edge_events` | `Lists differ: [(0, 3000, 'dropped', 4 ...` |
| hold read as corruption | `test_audio_compound_and_edge_events` | `Lists differ: [(0, 3000, 'bit-flip', 1) ...` |
| only the previous word counts as a neighbour | `test_audio_compound_and_edge_events` | `Lists differ: [(0, 3000, 'bit-flip', 1) ...` |
| identity changes not recorded | `test_audio_static_swap_fails_with_every_arm_found` | `('PASS', []) != ('FAIL', [])` |
| arms looked for on the logged channel only | same | `('NOT RUN', [{'class': 'bit-flip' ...}]) != ('FAIL', [])` |
| pending defaults accepted | `test_release_commit_cut_evidence` | `('NOT RUN', None) != ('NOT RUN', ['configuration', ...])` |
| cut outside its commit accepted / window end made inclusive | same | `('PASS', None) != ('NOT RUN', 'the cut hit no journal commit')` |
| missing cut evidence accepted | same | `'PASS' != 'NOT RUN'` |
| soft reset graded as a commit cut (R699 R03) | same | `'NOT RUN' != 'FAIL'` |
| capture losses stop the clocks | `test_audio_capture_losses_advance_the_clocks` | `(8000, 8000) != (8000, 417600)` |
| gPTP interpolated across a recorded discontinuity | same | `(208.7, 'anchored') != (None, 'unsupported gPTP: ...')` |
| times extrapolated past the last anchor | same | `(100.16666666666667, None) != (None, None)` |
| anchor past the capture accepted / anchors may run backwards | same | `'PASS' != 'NOT RUN'` |
| capture loss needs only one channel (R699 G07) | `test_audio_capture_loss_needs_every_channel` | `('PASS', ...) != ('NOT RUN', 'a logged capture loss is not in the capture')` |

The driver's full run (`receipts/release_mutants.log`) kills all 219 (192 before; 9 round-1 grader anchors
replaced, 36 added or re-anchored), source unchanged. A first run caught a test the splice had dropped
(`test_release_soak_counter_evidence`); it was restored verbatim before the commit.

Plan-feature scenarios (`tests/features/torture_campaign_plan.feature:404`, `:439`-`:489`; steps
`tests/steps/torture_release_steps.py:450`, `:635`-`:841`, independent `_counter_word` `:635`): 13 planted
planner defects, each fails a named scenario (`receipts/feature_mutants.log`); pristine 150 scenarios pass.

## Reviewer evidence rerun at the head

- R699 `reviewer_mutants.py`, unchanged (sha256 `d23c7076...` matches its manifest):
  22 KILLED, 0 SURVIVED, 6 INVALID, control passing. G07, G12 and R03 are KILLED.
  The six INVALID anchors are round-1 code the rewrite removed. `receipts/r699_equivalents.log`
  re-anchors each on the same defect and runs it through the reviewer's own runner: 6 of 6 KILLED.
- R699 `grader_probe.py` and `grader_probe2.py`, ported by changing `word()` only
  (`scripts/r699_grader_probe_port.py`): every case of the F1 table reports its design class.
  Remaining DEVIATION lines are deliberate:
  - `P1-repeat-2048` is located within `[lo, 8206]`, which holds 8205; a block-multiple slip.
  - `P1-hold-one` gives the F1 table's "1 repeated, then 1 dropped", where the probe's own check
    wants a repeat alone.
  - `P5-swap-from-start` is NOT RUN because that probe plants no arms; its events are now `swap`.
  - `S4-unlock-planted` FAILs by R700 F4.
  - `R3-commit-new` is NOT RUN, since it carries no cut-phase evidence (R700 F3).
  - `P6-arms-only-mid-capture` is NOT RUN under S1.
  - `P9-throughput` is not a measurement: the probe's chunk list `cap[i:i + 1 << 20]` parses as
    `cap[i:(i + 1) << 20]` and feeds overlapping chunks.
- R700 `probes.py`, ported (`scripts/r700_probes_port.py`: layout, output directory, the
  verification's larger multiples and both directions, an anchored and a gPTP-step row):
  - every row returns its expected verdict;
  - drop-4096 FAILs as `dropped 4096`, drop-3000 as `dropped 3000`;
  - the tag-bit flip and the copy are `bit-flip` `0x00200000` with `matches_channel` 2;
  - pending defaults are NOT RUN and the unlock 25 s after the window FAILs;
  - after the 409600-frame loss the event's times are null without an anchor;
  - with the end anchor they are 108.7 / 208.7;
  - its count mutant, re-anchored, is KILLED (`receipts/r700_probes_port.json`).
- Throughput (`receipts/grader_throughput.log`), 8 channels at 48 kHz, 1 MiB chunks:
  - clean: 4.7 capture-minutes per second, about 5 minutes for 24 h;
  - one-channel offset: the same rate (round 1: 0.08);
  - a channel without the counter: 5.4.

## Gate table (exact head, foreground except the driver, never piped; receipts in `receipts/`)

| Command | rc | Result |
|---|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | 0 | 103 tests OK (94 before) |
| `python3 -B tb/tools/torture_release_mutants.py` | 0 | 219 mutations killed; source unchanged |
| `cd tests && behave --no-capture -f plain` (rtl-fast bdd-conformance) | 0 | 14 features, 469 scenarios, 2206 steps (summary; full log hashed) |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | 0 | 150 scenarios, 585 steps (133 before) |
| `docs_check.py` (pinned renderer) | 0 | 0 findings, 210 md + 1418 scrubbed files |
| `gen_toc.py --check` / `--verify-anchors` (pinned) | 0 / 0 | 149 pages / 538 fragment links |
| `check_em_dash.py --base origin/dev` (pinned) | 0 | 0 findings over 296 added lines in 5 pages |
| `check_doc_style.py` (pinned) | 0 | 23 documents OK |
| `check_doc_paths.py` (pinned) | 0 | 1065 cited paths resolve |
| `python3 -B scripts/check_py_idiom.py` | 0 | at ratchets |
| `python3 -B scripts/check_feature_status.py` and `--self-test` | 0, 0 | 0 findings; 46/46 |
| `torture_campaign.py --coverage-by-area --areas soak,audio,power` | 0 | three areas complete |
| `torture_campaign.py --plan --areas soak,audio,power --json` | 0 | 17 steps; digest and contract in `plan_audit.json` |
| `git diff --check origin/dev HEAD`; `git diff --check` | 0, 0 | clean |

## Acceptance status (issue #396)

Unchanged from round 1: items 1, 2 and 5 are met at the desk; item 4's desk half is met; items 3 and 4
need the bench (part B). So the PR body says "Relates to #396".

## Open items and risks

- Decision still needed: THD+N and predictor-residual limits for the analog sine pair (NOT RUN until set).
- `restore_bound_s = 30` stays provisional.
- The bench must implement the new counter layout and record the capture tool's anchors and the commit
  window; the plan states both. The private runner is out of this lane's scope.
- The counter's wrap is now 23.4 Hz at 48 kHz (the 2026-10-04 design called it infrasonic); the level is
  unchanged, near -47 dBFS, bench only.
- S3 (Tables 4.1/4.2 holds over the soak) is a candidate for its own Issue; not filed (only TAKEN /
  REVIEW READY / STOP may be posted from this lane).

## Receipts

`receipts/INDEX.md` is generated from the files present (name, bytes, SHA-256). Scripts that produced
receipts are in `scripts/`; reviewer-derived scripts state their single changes in their headers.
