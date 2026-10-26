[A674b]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Round 2](#round-2)** — Each R699-1 and R700-1 finding, its fix and the test that proves it.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN at the desk, head `a3e24ac5ef984cb92458f1728f2c275349ae9854`:

- planner self-test 103/103;
- release mutation controls 219/219 killed;
- behave 469 scenarios, the plan feature 150;
- every documentation gate rc 0.

`396-release-gate-plan` -> `dev`: two commits on dev `e76a755a`, round 1 `21faa482` and round 2 `a3e24ac5`.
The bench runs (acceptance items 3 and 4) are #396 part B and remain open.

## Linked Issue / roles

Relates to #396

This is part A of #396 (the plan, the assertion contract and the documents).
Acceptance items 3 and 4 need the bench, so this PR must not close the Issue.

Executor: `[A674]` (round 1), `[A674b]` (round 2)
Internal cleared-context reviewer: `[R699]`
External reviewer: `[R700]`

## Description

The [owner decisions of 2026-10-26](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-6408072465)
replace the seven-day soak and the 160/40 cold-cut mix that PR #586 merged.
This PR applies them to the plan, its offline graders and the documents.

| Piece | Change |
|---|---|
| `soak` | 24 h by default (`--soak-duration-s 86400`), interval 60 s. Zero `SEQ_NUM_MISMATCH`, `STREAM_INTERRUPTED`, `LATE_TIMESTAMP` and `EARLY_TIMESTAMP` growth on every Stream Input, CRF included. Zero `MEDIA_UNLOCKED` growth outside a recorded planted event, explained or not. An increment is excused only between two reads inside the planted window, so the runner reads the input at the window's edges. Oracle `check_release_soak_counters`. The merged `mr`/`tu`, `asCapable`, `AVTPRX_TSD` and uptime rules are unchanged. |
| `audio` | The identity area gains `audio.integrity`, the [2026-10-04 signal design](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5978644444), run inside the soak window. A bit-exact counter rides on every digital path and every bound AAF channel, in both directions. The counter never repeats within a run (below). The grader `grade_audio_counter_capture` classifies each event at its sample: n dropped, n repeated, n samples of silence (replaced or inserted), a bit-flip mask, or a channel swap. Planted drop, repeat and flip arms run in the first and the last tenth; a missed arm voids the run. Capture-side losses are attributed apart but advance the clocks. Each event carries its capture and acquisition indices, its words, and anchored wall and gPTP times. The analog sine pair (997 Hz, 9,973 Hz) is planned, with its limits undecided. |
| `power` | 200 cycles: `power.idle` 100 and `power.journal_commit` 50 cold cuts, and `power.soft_reset` 50 resets with power held on. A soft reset's T0 is its host-timestamped reset command. Every cycle restores the eight Milan items of #70's inventory and the binding, as data (`RELEASE_PERSISTED_ITEMS`). `check_release_state_restored` refuses a pre-cycle or pending value equal to its default. A commit cut passes only with a `ReleaseCommitCut` placing its cut inside the recorded commit window. The ADP, automatic-restore and #75 reconnect bounds are unchanged. |
| Negative controls | `power.control.first-boot-restart` (#366) must fail `power.single-boot`. `power.control.persistence-disabled` must fail `power.state-restored`. `audio.control.planted-drop` must fail `audio.zero-dut-glitches` and classify the drop exactly, graded offline on a synthetic capture. |
| Audit | The per-area audit refuses a missing index, direction or CRF sink in any release repeat. It also refuses a dropped or downgraded required assertion, a missing phase, a cycle mix that does not sum to the total, and a missing control. |
| Docs | REQ-VER-06 and REQ-VER-05's blocker sentence; CONTRIBUTING section 3's gate for release PRs; TESTING 6d's inputs, rules, limits, verdicts, controls and retention per 6b; the README roadmap (24 h); the persistence design's restated numbers. |

Counter layout: S32 words, with the 24-bit sample in bits 31:8 and bits 7:0 zero (the #451 and #629 layout).

| Sample bits | Content |
|---|---|
| 15:12 | The channel number, the channel index plus one |
| 11:1 | The absolute sample position `n`, modulo 2048 |
| 0 | Bit `n mod 32` of block `n div 2048`'s code, the block number times `0x9E3779B1` modulo 2^32 |

Thirty-two consecutive samples of one block give its number, so the counter repeats only after 2^43 samples.
That is about 530 days at 192 kHz, the highest Milan v1.2 6.2 (Table 6.1) rate; a 24-hour run is 1.66e10 samples there.
Eight channels peak near -47 dBFS, and the 2048-sample wrap is a 23.4 Hz sawtooth at 48 kHz.
The grader reads headerless interleaved S32 in either byte order and streams a 24-hour file in chunks.
It grades about 4.7 capture-minutes per second for eight channels, about 5 minutes per 24 h, with or without an offset channel.

## Round 2

Round 2 answers [R699-1](https://github.com/kebag-logic/milan-fpga/pull/786#issuecomment-6409756577) and
[R700-1](https://github.com/kebag-logic/milan-fpga/pull/786#issuecomment-6409757802), both NEGATIVE at `21faa482`,
under the [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-6409763644).
Round 1 is not rewritten. Lines are at `a3e24ac5` in `tb/tools/torture_campaign.py` unless named.
Every listed test fails on round 1's code: the round-2 test class transplanted onto the round-1 planner
fails all 14 new or changed arms.

| Finding | Fix | Test that proves it |
|---|---|---|
| R700 F1 (MAJOR): the repeating payload cannot prove zero glitches; a 4096-sample drop passed | Non-repeating counter, `audio_counter_word` `:3699`, `_audio_decode` `:3752`; windows close at 64 clean samples whose decoded position sizes every slip (`_CounterWindow` `:4047`, `_CounterScan._close` `:4164`) | `test_audio_counter_word_layout` `:7454`, `test_audio_block_slips_are_sized_exactly` `:7613` (drops and repeats of 2048, 4096, 8192 and 409600 samples, both byte orders, chunked, near the end of a 24 h run at 192 kHz); scenario "the audio grader sizes a slip of whole blocks exactly" |
| R699 F3 (MINOR): the 4096-multiple backstop did not hold | The blind spot is gone; the backstop claim is removed from TESTING 6d and the limits restated (`docs/testing/TESTING.md:1335`-`:1345`) | `test_audio_block_slips_are_sized_exactly`; R700's probe `drop-4096` now FAILs as `dropped 4096` |
| R699 F1 (MINOR): compound and edge events misclassified; a static swap voided the run | `_audio_duplicate` `:3911`, `_audio_excursion` `:3920`, `_audio_window_events` `:4000`; channel numbers acquired at capture start and identities graded in `finish` `:4199`; arms follow their counter (`carriers` `:4222`) | `test_audio_compound_and_edge_events` `:7533`, `test_audio_static_swap_fails_with_every_arm_found` `:7601`; scenarios "a one-sample hold reads as one repeated and then one dropped sample" and "a channel swap from the first frame fails as a swap with every arm found" |
| R700 F2 (MAJOR): tag corruption read as a swap | Tag integrity decides first: `_partner` `:4152` admits only a reciprocal exchange, `_audio_labels` `:3854`; a copied word names its source in `matches_channel` (`_audio_extend` `:3965`) | `test_audio_tag_integrity_decides_first` `:7570` (a flip of each of the 32 container bits, against an independent expectation; reciprocal swaps; copies; consecutive corruptions); scenario "a channel-number flip on one channel is corruption, not a swap" |
| R700 F3 (MAJOR): pending defaults satisfied the commit-cut vacuity guard | `ReleaseCommitCut` `:3566`, `_release_cut_refusal` `:3578`, `_release_commit_restored` `:3628`: a pending value at its default is NOT RUN; a cut outside its commit window is NOT RUN as "the cut hit no journal commit"; a bare pending snapshot can FAIL but never PASS | `test_release_commit_cut_evidence` `:7356`; scenario outline "a journal-commit cut passes only with placed, non-vacuous evidence" |
| R700 F4 (MAJOR): planted exceptions covered whole read intervals | `check_release_soak_counters` `:3507`, rule `:3554`: an increment is excused only between two reads inside its input's planted window; plan `planted_event_reads` `:4749` | `test_release_soak_media_unlocked_planted` `:7265` (R700's unlock 25 s after the window FAILs); example "one MEDIA_UNLOCKED beside a planted event" |
| R700 F5 (MAJOR): capture losses did not advance the event clocks | `_audio_timing` `:4320`: the acquisition index adds every logged loss; times are interpolated between the capture tool's `anchors`, never extrapolated, and gPTP time never across a recorded discontinuity (`CounterCapture` `:4364`) | `test_audio_capture_losses_advance_the_clocks` `:7636` (108.7 s and 208.7 s after R700's 409600-frame loss; null without an anchor; gPTP null across a step); scenario "a capture loss is time that ran" |
| R699 F2 (MINOR): mutants G07, G12, R03 survived | Anchors kept, behaviour pinned | `test_audio_capture_loss_needs_every_channel` `:7697` (G07), `test_audio_tag_integrity_decides_first` (G12), `test_release_commit_cut_evidence` (R03). R699's mutant script, rerun unchanged: 22 KILLED including G07, G12 and R03, 0 SURVIVED, 6 INVALID. The six INVALID anchor removed round-1 code; each re-anchored equivalent is KILLED through the same runner. |
| R699 R1, R700 R1 (RESIDUE) | Issue-comment IDs removed from `:3321` and `:3652`; `tests/steps/torture_release_steps.py:239` reworded | Inspection |
| R699 S1 (SUGGESTION): adopted | "At the start and at the end" is the first and the last tenth (`AUDIO_ARM_EDGE_DIVISOR` `:3690`) | `test_audio_arms_run_at_both_edges` `:7705`; scenario "arms planted only in the middle of the capture void the run" |
| R699 S2 (SUGGESTION): adopted | The fast path runs per channel (`_CounterScan.frames` `:4123`) | `test_audio_offset_channel_and_mixed_capture` `:7740`; throughput unchanged with an offset channel (round 1: 0.08 capture-minutes per second) |
| R699 S3 (SUGGESTION): declined | Tables 4.1/4.2 holds lie outside the decided criteria | A candidate for its own Issue |

Patterns the signal cannot tell apart are stated limits, each pinned by a self-test arm (TESTING 6d):

- A flip of position bit 0 can make a word equal to its neighbour; it then reads as that slip pair.
- A slip pair whose displaced words share one XOR mask with the track reads as a `bit-flip`.
- A slip of whole 2048-sample blocks is found within 63 samples, sized exactly, with `located_within`.
- Between events under 64 samples apart, intermediate slips take the smallest sizes the positions allow; the total is exact.
- A slip in a capture's last 63 samples carries `unresolved`.

Citation note: the assignment cites Milan v1.2 4.4.2.1 for the sample rate.
In Milan v1.2, 4.4.2.1 is the Listener's 2.126 ms presentation-time buffering.
The sample-rate set is in 6.2, Table 6.1, so the period is stated against that clause.

Reviewer evidence rerun at `a3e24ac5`:

- R699's probes, ported by changing their word generator only, report the design class for every case in the F1 table.
- R700's probes, ported to the layout with the verification's larger multiples, both directions, an anchored row and a gPTP-step row, return every expected verdict, and their count mutant is killed.
- Thirteen planner defects planted at feature level each fail a named plan scenario.
- 36 planted defects added or re-anchored in `tb/tools/torture_release_mutants.py` each fail a named self-test arm.

## Authoritative references

- #396 owner decisions issuecomment-6408072465; assignments issuecomment-6408079016 and issuecomment-6409763644;
  audio design issuecomment-5978644444; `mr`/`tu` rule issuecomment-5857765949 (unchanged).
- Milan v1.2 5.3.8.10 with Table 5.6 (counters, reset on not-bound to bound); 5.3.5.1, 5.3.7.1,
  5.3.7.6, 5.3.8.1-5.3.8.3, 5.3.8.7, 5.3.9.1, 5.3.10.1, 5.3.11.1, 5.3.13 (saved state);
  5.5.1.4 ("a power cycle or a simple reset"); 5.5.2.4/5.5.2.6; 5.6.2/5.6.3; 6.2 Table 6.1 (sampling rates); Annex B.1.1.
- IEEE 1722-2016 4.4.4.3, 4.4.4.6, 4.4.4.7, 7.3.5. IEEE 1722.1-2021 6.2.2.5, 7.4.43.
- REQUIREMENTS.md section 8; CONTRIBUTING.md section 3; docs/testing/TESTING.md sections 6, 6b, 6d;
  docs/testing/methodology.md (R2: every new check ships a control that fails it).

## How to get into the same state

```sh
git fetch origin
git switch 396-release-gate-plan
git submodule update --init protocol-processor gptp-processor
python3 -m pip install behave
python3 -m pip install -r tools/markdown/requirements.txt
```

## How to validate

```sh
python3 -B tb/tools/torture_campaign.py --self-test
python3 -B tb/tools/torture_release_mutants.py
python3 -B tb/tools/torture_campaign.py --coverage-by-area --areas soak,audio,power
python3 -B tb/tools/torture_campaign.py --plan --areas soak,audio,power --json
cd tests && behave --no-capture -f plain && cd ..
python3 -B scripts/docs_check.py
python3 -B scripts/gen_toc.py --check
python3 -B scripts/gen_toc.py --verify-anchors
python3 -B scripts/check_em_dash.py --base origin/dev
python3 -B scripts/check_doc_style.py
python3 -B scripts/check_doc_paths.py
python3 -B scripts/check_py_idiom.py
git diff --check origin/dev HEAD
```

Expected result / pass criteria: every command exits 0. The self-test runs 103 tests OK.
The mutation driver prints `PASS: 219 mutations killed; source unchanged` (about 13 minutes).
Behave reports 469 scenarios passed, the plan feature 150.
The coverage audit reports `soak`, `audio` and `power` complete.
The docs gates report zero findings.

## Known limitations / out of scope

- The bench runs on the shipping image, and the two power controls on their known-defect images,
  are #396 part B (acceptance items 3 and 4). Nothing here touches hardware.
- The bench source must implement the counter layout above.
  The capture tool must record its anchors at least every `audio_context_s` and at the capture's end.
  The power runner must record each commit cut's window and cut instant.
  The plan states all three.
- No limit is decided yet for the analog sine pair's THD+N or predictor residual.
  `audio.analog-sine-pair` stays NOT RUN, so no release can qualify, until a recorded decision sets them.
- `restore_bound_s = 30` stays provisional, pending ratification from #397 and #75.
- The soft-reset mechanism is bench-declared and recorded per cycle; AECP REBOOT is not
  implemented by the processor and cannot serve.
- The counter's wrap is 23.4 Hz at 48 kHz, no longer infrasonic as the 2026-10-04 design described; its level is unchanged.
- The bit-identical limits above are properties of any finite-alphabet signal, stated rather than hidden.
- No firmware, RTL, builder or submodule change.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (part A: items 1, 2, 5 and the desk half of 4; items 3 and 4 open)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
