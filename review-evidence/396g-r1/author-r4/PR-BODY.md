[A674d]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Round 4](#round-4)** — Each R699-3 finding, its fix and the test that proves it.
- **[Round 3](#round-3)** — Each R700-2 and R699-2 finding, its fix and the test that proves it.
- **[Round 2](#round-2)** — Each R699-1 and R700-1 finding, its fix and the test that proves it.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN at the desk, head `85da3e4595871c1573c28b4d040b9e98463a41c9`:

- planner self-test 112/112;
- release mutation controls 271/271 killed;
- behave 495 scenarios, the plan feature 176;
- every documentation gate rc 0.

`396-release-gate-plan` -> `dev`: five commits on dev `e76a755a`.
They are round 1 `21faa482`, round 2 `a3e24ac5`, round 3 `9da26126` and `4d69e192`, and round 4 `85da3e45`.
The bench runs (acceptance items 3 and 4) are #396 part B and remain open.

## Linked Issue / roles

Relates to #396

This is part A of #396 (the plan, the assertion contract and the documents).
Acceptance items 3 and 4 need the bench, so this PR must not close the Issue.

Executor: `[A674]` (round 1), `[A674b]` (round 2), `[A674c]` (round 3), `[A674d]` (round 4)
Internal cleared-context reviewer: `[R699]`
External reviewer: `[R700]`

## Description

The [owner decisions of 2026-10-26](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-6408072465)
replace the seven-day soak and the 160/40 cold-cut mix that PR #586 merged.
This PR applies them to the plan, its offline graders and the documents.

| Piece | Change |
|---|---|
| `soak` | 24 h by default (`--soak-duration-s 86400`), interval 60 s. Zero `SEQ_NUM_MISMATCH`, `STREAM_INTERRUPTED`, `LATE_TIMESTAMP` and `EARLY_TIMESTAMP` growth on every Stream Input, CRF included. Zero `MEDIA_UNLOCKED` growth outside a recorded planted event, explained or not. An increment is excused only between two reads inside the planted window, so the runner reads the input at the window's edges. Oracle `check_release_soak_counters`. The merged `mr`/`tu`, `asCapable`, `AVTPRX_TSD` and uptime rules are unchanged. |
| `audio` | The identity area gains `audio.integrity`, the [2026-10-04 signal design](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5978644444), run inside the soak window. A bit-exact counter rides on every digital path and every bound AAF channel, in both directions. The counter never repeats within a run (below). The grader `grade_audio_counter_capture` classifies each event at its sample: n dropped, n repeated, n samples of silence (replaced or inserted), a bit-flip mask, a channel swap, or an `unresolved` stretch at a capture's end. Each verdict states the qualified interval it proves. `PASS` needs 24 hours of observed samples in that interval. Planted drop, repeat and flip arms run in the first and the last tenth, inside the qualified interval; a missed arm voids the run. Where the capture's bytes allow two readings, the planted-arm log decides at a logged arm, never at the cost of a DUT event. Capture-side losses are attributed apart and advance the clocks, but are not observed time. Each event carries its capture and acquisition indices, its words, and anchored wall and gPTP times. The analog sine pair (997 Hz, 9,973 Hz) is planned, with its limits not yet set (below). |
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

## Round 4

Round 4 answers [R699-3](https://github.com/kebag-logic/milan-fpga/pull/786#issuecomment-6417659353), NEGATIVE at `4d69e192`
with two MINOR findings, under the [round-4 assignment](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-6417665116).
[R700-3](https://github.com/kebag-logic/milan-fpga/pull/786#issuecomment-6416855079) is POSITIVE. Rounds 1 to 3 are not rewritten.
Lines are at `85da3e45` in `tb/tools/torture_campaign.py` unless named. Every listed self-test arm fails on `4d69e192`.

| Finding | Fix | Test that proves it |
|---|---|---|
| R699-3 F1 (MINOR): a one-word corruption followed within 64 samples by a whole-block slip was misgraded, and after the planted flip arm it voided the run | The cause was the window's labelling. Once a corrupted word fitted the closing track, the offset in force before it stopped being a candidate, and the longest run won. Now the offset in force before the last change stays a candidate (`_audio_labels` `:3960`, `:3989`). The offset nearest the one in force is kept while it fits, so each slip takes the smallest size and a slip of whole blocks sits at the first word that shows it; half a block away, the twin nearer the offset before comes first (`_audio_fit` `:4017`, `_audio_candidates` `:3995`). A departure ends at the first word from which every word up to its return fits the offset in force (`_audio_excursion` `:4127`). A one-word departure that returns a whole number of blocks away is a corruption beside that slip (`:4135`), judged against whichever track gives its mask fewer bits set (`:4144`). A whole-block slip's `located_within` runs on to the first word that shows it, the resync included (`_audio_slip` `:4173`, `_audio_upto` `:4183`); a corrupted word bounds it only where the tracks differ (`:4318`). Where the bytes allow two readings, the planted-arm log decides (`_read` `:4546`, `_cut` `:4591`, `_score` `:4618`, `_AudioSteer` `:4083`). A missed flip arm is tried as the corrupted word, judged against the offset in force or the closing one, the window opened before its start where the word was followed. A missed slip arm keeps the excursion it enters or leaves (`:4148`). A slip that differs from a slip arm by whole blocks is split into the arm and a slip beside it (`slip` `:4272`). Another reading is taken only with no more DUT events and more arms found, so the log never hides a DUT event | `test_audio_block_slip_after_a_corruption_or_a_slip` `:8661` (0x100 and 0x80000 corruptions, then ±2048, ±4096 and 8192 slips 1 to 64 samples later; 3-sample drops and 2-sample repeats then ±4096; a half-block corruption just after a slip). `test_audio_planted_arms_beside_block_slips` `:8731`: slips 1, 2, 3 and 9 samples either side of both flip arms and two slip arms, on every channel and on the arm's channel, FAIL with every arm found. Also a slip that undoes a slip arm at the next sample, and logged arms the capture does not show staying missed. The tie pin in `test_audio_slip_and_corruption_share_a_window` `:8612`. Scenarios `tests/features/torture_campaign_plan.feature:514` and `:525` |
| R699-3 F2 (MINOR): the constant-mask rule changed beside a one-word corruption, and at a code-bit corruption ending on a block boundary | Only the window's trailing words under the closing mask start a hold, so an event before them is graded on its own (`_hold` `:4624`). A followed word on the old track is a possible return, never a release; a masked word after it parts the masks (`_AudioImage.keeps` `:4426`, `clean` `:4420`, `holds` `:4434`, `:4502`). A held excursion returns when the content resumes nearer the old track than the held one (`_close` `:4688`). `_returned` `:4522` ends the bit-flip where the old track's words began and grades the rest of the window against the old track, so an event beside the excursion is its own | `test_audio_constant_mask_beside_one_word_events` `:8791`: 0x80000 and 0x40000 over 100 words with a 0x100 word 1 to 64 samples before or after, the planted flip arm as the neighbour, and a planted drop at the return. `test_audio_code_bit_corruption_ending_on_a_block` `:8814`: 0x100 from 5000, 6143 and 6144 to 8191 through 12288. Scenarios `:538` and `:549` |

Bit-identical shapes are stated exactly in TESTING 6d (`docs/testing/TESTING.md:1390`-`:1417`), REQ-VER-06 (`REQUIREMENTS.md:412`-`:414`) and `counter_limits` (`AUDIO_COUNTER_LIMITS` `:3731`).
A self-test arm pins each one by comparing the bytes:

- A code-bit corruption less than 64 samples before a slip of whole blocks may make its word the new track's. When every word between them fits both tracks, the bytes are that slip alone at the corrupted word.
- A slip of whole blocks and a code-bit corruption can give the same bytes in either order: the corrupted word is the other track's and only one word between them differs. The corruption reads first, and the slip is located after it.
- A slip followed, within the words that fit both tracks, by a slip of whole blocks gives the bytes of one slip of their sum.
- A slip pair whose total is whole blocks and whose displaced words share one mask reads as that bit-flip and a slip of whole blocks beside it.
- A DUT slip at a planted slip arm's own sample is one slip of their sum; unless the DUT slip is whole blocks, the arm is missed and the run is void.
- A constant-mask corruption that a slip interrupts reads as the slips its words show.

Suggestions, each a choice:

- R699-3 S1 adopted: the interval decides what is proved clean, not the class of a slip near its end (`docs/testing/TESTING.md:1380`; self-test comment `:8507`).
- R699-3 S2 adopted: both void reasons for an unacquired channel name the DUT not driving the counter on it (`:5049`, `:5074`; `docs/testing/TESTING.md:1434`).

R699-3's probes, rerun unmodified at `85da3e45`, every script byte-identical to its published manifest:

- `r3_arm_void_probe.py`: no NOT RUN line; 0 of 256 not FAIL at every size.
- `r3_cluster_probe.py`: FB 654 OK, 6 DEVIATION (433 before); SB 258 OK, 2 (89 before); CF 32 OK, 0 (28 before); CB 40 OK, 0 (12 before).
- `r3_probe.py`: E 642/6, S 1170/0, M 273/0 (3 before), A 21/8.
- Every remaining deviation is shown, with the reviewer's own encoder, to be its stated limit:
  - the 6 FB and 2 SB lines give bytes equal to the slip alone, or to one slip of the sum;
  - 4 A lines are FAIL with every arm found, and `located_within` holds the slip; the probe compares `capture_index` exactly;
  - 2 A lines put the DUT slip at a planted slip arm's own sample;
  - 2 A lines are a constant-mask corruption that the planted repeat interrupts;
  - the 6 E lines are S1's case.
- Round-2 probes, unmodified:
  - compound 30/30 OK;
  - the arm probe A2 to A5 FAIL, and A1 is NOT RUN only by the 24-hour rule;
  - `grader_probe_r2` has the same OK and DEVIATION per case as at `4d69e192`;
  - the `required_s` port is 110 OK, with P5 void as in the reviewer's own receipt;
  - N07 at 8214.
- `reviewer_mutants_r2.py`: 31 KILLED, 0 SURVIVED, 1 INVALID. N15's line changed; ported to it, N15 is killed.
- `r3_reviewer_mutants.py`: 13 KILLED, 0 SURVIVED, 3 INVALID. V07, V09 and V13's lines changed; ported to them, all three are killed.

R700-3's probes, rerun as byte-identical copies, since they write beside themselves:

- `delta_probes.py`, `qualified_probes.py` and `compound_ambiguity.py` give byte-identical output at `4d69e192` and at `85da3e45`.
- In `boundary_matrix.py`, `compound-4096-1-80000` now meets R700-3's compound rule.
- `compound-4096-5-100` no longer meets it: it is the stated code-bit tie, read corruption first, and the self-test pins its bytes.

Two wider sweeps with the reviewer's encoder FAIL with every arm found in all 39936 placements. They place DUT slips 1 to 64 samples either side of all six arms, on every channel or on one.
The sizes are 1, 2, 3, 5, 7, 100, 1023, 1024, 1025, 2047, 2048, 2049, 3000, 4096, 6143, 6145 and 8192 samples, most in both directions (`receipts/arm_sweep.log`, `receipts/arm_sweep_odd.log`).
Twenty-two new planted defects in `tb/tools/torture_release_audio_mutants.py` each fail a named round-4 arm.

## Round 3

Round 3 answers [R700-2](https://github.com/kebag-logic/milan-fpga/pull/786#issuecomment-6413374622) and
[R699-2](https://github.com/kebag-logic/milan-fpga/pull/786#issuecomment-6413444899), both NEGATIVE at `a3e24ac5`,
under the [round-3 assignment](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-6413452035).
Rounds 1 and 2 are not rewritten.
Lines are at `4d69e192` in `tb/tools/torture_campaign.py` unless named.

| Finding | Fix | Test that proves it |
|---|---|---|
| R700-2 F1 (MAJOR): a slip of whole blocks at a capture's boundary could earn PASS | Every verdict states its qualified interval (`_CounterScan.qualified` `:4461`, `_audio_qualified` `:4676`). It runs from 63 samples after the last channel's acquisition to 63 samples before the capture's end. `grade_audio_counter_capture` `:4709` takes `required_s`, 86400 by default. `PASS` needs that many observed seconds in the interval; a shorter one is NOT RUN (`:4799`). Logged losses are not observed time. A channel that never acquires, or an arm or logged loss outside the interval, is NOT RUN by name (`:4776`). At either end, words that differ from the track only in the code bit are one `unresolved` event with `located_within` (`_audio_boundary` `:3993`, `_audio_open` `:4081`), never an exact class | `test_audio_qualified_interval_is_stated_and_required` `:8105`. `test_audio_boundary_block_slips_are_unresolved` `:8169` keeps the reviewer's byte-identical endpoint pairs, pinned by the published capture SHA-256. They cover whole-block drops and repeats 1 to 65 samples from the end and 10 to 62 from the start, both byte orders, 113-byte chunks, and with and without guard samples. Scenarios `tests/features/torture_campaign_plan.feature:477` and `:484` |
| R700-2 F2 (MINOR): the constant-mask rule changed silently at 64 samples | One rule at every length. Sixty-four corrupted words that decode as another track are held as `_AudioImage` (`:4263`, `_audio_image_mask` `:4250`), not adopted. If the words return to the old track, the whole excursion is one `bit-flip` (`_close` `:4389`). A word off the mask releases the held events as the slips they are (`:4329`, `_release` `:4353`). Past the 65536-word bound, a constant-mask stretch stays a `bit-flip` in each piece (`_audio_excursion` `:4049`) | `test_audio_constant_mask_at_every_length` `:8249`: masks `0x100`, `0x80000`, `0x40000` and `0x200` over 2, 63, 64, 65, 100 and 2000 words, across block boundaries and chunked. Genuine slips that are images for a while are released exactly. A half-block repeat and drop is the stated bit-identical limit. An excursion the capture ends inside carries `unresolved`. Scenario `:496` |
| R699-2 F1 (MINOR): a slip and a one-word corruption in one 64-sample window were misgraded and could void a run | A run of positions is cut at each word no offset explains (`_audio_fit` `:3980`, `_audio_candidates` `:3960`, in `_audio_labels` `:3905`). Each departure is judged against the offset in force, again after every slip (`:4170`) | `test_audio_slip_and_corruption_share_a_window` `:8299` covers drop 3, repeat 2 and drop 4096. Each is followed 5, 40 or 100 samples later by a `0x80000`, `0x40000` or `0x100` flip or a two-word burst. A DUT drop beside the flip arm FAILs with the arm found, and arms 10, 40 or 63 samples apart PASS. Scenario `:509` |
| R699-2 F2 (MINOR): a whole-block slip in the last 63 samples read as a code-bit corruption | The same boundary rule: an `unresolved` event, as TESTING 6d states (`docs/testing/TESTING.md:1382`). A logged loss there is outside the qualified interval, so it is NOT RUN by name (`TESTING.md:1431`) | `test_audio_boundary_block_slips_are_unresolved`. The reviewer's edge probe, unmodified, reports `unresolved` at every `F-20` to `F-63` row |
| R699-2 F3 (MINOR): the "at or before" acquisition boundary was untested; mutant N07 survived | Test added; the code was right | `test_audio_capture_losses_advance_the_clocks` (`:8014`) checks a loss logged at an event's own index. Scenario `:514`. The reviewer's mutant runner, unchanged, kills N07 |

A round-3 regression was caught before review: the 24-hour default made a clean short capture NOT RUN.
So the invalid-anchor arm stopped depending on its anchors, and the reviewer's N30 and N31 survived.
That arm now grades against its capture's qualified length, with a valid-anchor control that must PASS (`:8038`, commit `4d69e192`).
N30 and N31 are killed again.

Suggestions, each a choice:

- R699-2 S1 adopted as documentation: a capture starts once the counter flows; leading silence fails (`TESTING.md:1394`, plan `capture_start` `:5162`).
- R699-2 S2 adopted: every verdict lists `anchor_gaps` (`_audio_anchor_gaps` `:4690`), verdict unchanged; `test_audio_anchor_gaps_are_reported` `:8337`.
- R699-2 S3 adopted: a channel that has not acquired within 65536 frames voids the run at once (`:4752`); the reviewer's misuse probe now stops in under a second.
- R699-2 S4 adopted: the window bound is documented, and its pieces keep one rule (`TESTING.md:1388`).

Bit-identical limits, each pinned by a self-test arm (TESTING 6d):

- A flip of position bit 0 can make a word equal to its neighbour; it then reads as that slip pair.
- A slip pair whose displaced words share one XOR mask reads as a `bit-flip`, at any length.
- A slip of whole blocks is found within 63 samples, sized exactly, with `located_within`.
- A slip that is the old track under one mask is held until the masks part, at most one block later.
- Between events under 64 samples apart, slips take the smallest sizes; a code bit they leave unexplained reads as a code-bit `bit-flip`.
- At either end of a capture, a code-bit-only stretch is one `unresolved` event; other unconfirmed slips carry `unresolved`.
- Nothing outside the qualified interval is proved clean.

Reviewer evidence rerun at `4d69e192`, every script byte-identical to its published manifest:

- R700-2 `delta_probes.py`, unmodified. Interior rows are unchanged. The byte-identical tail pairs and the clean control are NOT RUN, since a 0.17 s capture cannot meet the 24-hour rule. `tail-slip-8191-4096`, `tail-slip-with-64-more-frames` and `initial-slip` are `unresolved`. `constant-code-xor-64`, `-65`, `-100` and `-chunked` are one `bit-flip` each.
- The same probe ported to pass `required_s` only, with the interval recorded. The clean control and both byte-identical pairs PASS with the interval `[63, 8129)`, so the slips lie outside what is proved. `initial-slip` starts it at 73.
- R699-2 probes, unmodified:
  - the compound probe is 30/30 OK;
  - the arm probe's A2 to A5 FAIL;
  - the edge probe's X1 is `unresolved` from `F-20` to `F-63`;
  - the N07 probe gives acquisition index 8214;
  - every other DEVIATION is a clean capture NOT RUN by the 24-hour rule.
- Ported to pass `required_s` only, every line is OK except P5. P5 plants no arms, so it is void, as in the reviewer's own receipt.
- R699-2 `reviewer_mutants_r2.py`, unchanged: 32 KILLED, 0 SURVIVED, 0 INVALID. The round-1 runner, unchanged: 22 KILLED, 6 INVALID on code round 2 removed.
- The round-3 test class transplanted onto round 2's grader fails every new boundary, mask, window, interval and anchor-gap arm. A shim accepts the new keyword there, so each arm fails on behaviour.
- Nine planner defects planted at feature level each fail a named scenario.
- 30 planted defects added in `tb/tools/torture_release_mutants.py` each fail a named self-test arm.

## Round 2

Round 2 answers [R699-1](https://github.com/kebag-logic/milan-fpga/pull/786#issuecomment-6409756577) and
[R700-1](https://github.com/kebag-logic/milan-fpga/pull/786#issuecomment-6409757802), both NEGATIVE at `21faa482`,
under the [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-6409763644).
Every listed test failed on round 1's code. Line numbers below are at `a3e24ac5`.

| Finding | Fix | Test that proves it |
|---|---|---|
| R700 F1 (MAJOR): the repeating payload cannot prove zero glitches | Non-repeating counter, `audio_counter_word` `:3699`, `_audio_decode` `:3752`; windows close at 64 clean samples whose decoded position sizes every slip | `test_audio_counter_word_layout`, `test_audio_block_slips_are_sized_exactly` |
| R699 F3 (MINOR): the 4096-multiple backstop did not hold | The blind spot is gone; the backstop claim is removed | `test_audio_block_slips_are_sized_exactly` |
| R699 F1 (MINOR): compound and edge events; a static swap voided the run | Neighbour repeats, constant-mask excursions, identities acquired at capture start | `test_audio_compound_and_edge_events`, `test_audio_static_swap_fails_with_every_arm_found` |
| R700 F2 (MAJOR): tag corruption read as a swap | Tag integrity decides first; only a reciprocal exchange is a swap | `test_audio_tag_integrity_decides_first` |
| R700 F3 (MAJOR): pending defaults satisfied the commit-cut vacuity guard | `ReleaseCommitCut`; a pending default or a cut outside its window is NOT RUN | `test_release_commit_cut_evidence` |
| R700 F4 (MAJOR): planted exceptions covered whole read intervals | An increment is excused only between two reads inside its planted window | `test_release_soak_media_unlocked_planted` |
| R700 F5 (MAJOR): capture losses did not advance the event clocks | Acquisition index adds every logged loss; times interpolated between anchors | `test_audio_capture_losses_advance_the_clocks` |
| R699 F2 (MINOR): mutants G07, G12, R03 survived | Anchors kept, behaviour pinned | Killed by named arms |
| Residues; S1 and S2 adopted; S3 declined | Comment IDs removed; arms in the first and last tenth; per-channel fast path | `test_audio_arms_run_at_both_edges`, `test_audio_offset_channel_and_mixed_capture` |

Citation note: the round-2 assignment cites Milan v1.2 4.4.2.1 for the sample rate.
In Milan v1.2, 4.4.2.1 is the Listener's 2.126 ms presentation-time buffering.
The sample-rate set is in 6.2, Table 6.1, so the period is stated against that clause.

## Authoritative references

- #396 owner decisions issuecomment-6408072465 and issuecomment-6409128703; assignments issuecomment-6408079016,
  issuecomment-6409763644, issuecomment-6413452035 and issuecomment-6417665116; audio design issuecomment-5978644444;
  `mr`/`tu` rule issuecomment-5857765949 (unchanged).
- Milan v1.2 5.3.8.10 with Table 5.6 (counters, reset on not-bound to bound); 5.3.5.1, 5.3.7.1,
  5.3.7.6, 5.3.8.1-5.3.8.3, 5.3.8.7, 5.3.9.1, 5.3.10.1, 5.3.11.1, 5.3.13 (saved state);
  5.5.1.4 ("a power cycle or a simple reset"); 5.5.2.4/5.5.2.6; 5.6.2/5.6.3; 6.2 Table 6.1 (sampling rates); Annex B.1.1.
- IEEE 1722-2016 4.4.4.3, 4.4.4.6, 4.4.4.7, 7.3.5. IEEE 1722.1-2021 6.2.2.5, 7.4.43.
- REQUIREMENTS.md section 8 (REQ-VER-06); CONTRIBUTING.md section 3; docs/testing/TESTING.md sections 6, 6b, 6d;
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
python3 -B scripts/check_feature_status.py
git diff --check origin/dev HEAD
```

Expected result / pass criteria: every command exits 0.

- The self-test runs 112 tests OK.
- The mutation driver prints `PASS: 271 mutations killed; source unchanged`, after about 90 minutes.
- Behave reports 495 scenarios passed, the plan feature 176.
- The coverage audit reports `soak`, `audio` and `power` complete.
- The docs gates report zero findings.

## Known limitations / out of scope

- The bench runs on the shipping image, and the two power controls on their known-defect images,
  are #396 part B (acceptance items 3 and 4). Nothing here touches hardware.
- The bench source must implement the counter layout above.
  The capture tool must record its anchors at least every `audio_context_s` and at the capture's end.
  The power runner must record each commit cut's window and cut instant.
- Each audio capture must run past the 24 hours at both ends.
  It needs at least 63 guard samples at each end, plus any logged loss.
  The soak window outlasts 24 hours by as much. The plan states this.
- Logged capture losses are not counted as observed time, so a run with losses must capture longer. This is the strict reading of "the qualified interval covers the full 24 h".
- Owner decision issuecomment-6409128703 sets two things this plan text does not yet carry:
  - AECP REBOOT for the 50 soft resets, NOT RUN until REBOOT lands;
  - sine-pair limits at the first-hour baseline plus 6 dB.
  Both lie outside the round-4 assignment and are for the manager to route.
  Until the limits are recorded, `audio.analog-sine-pair` stays NOT RUN, so no release can qualify.
- `restore_bound_s = 30` stays provisional, pending ratification from #397 and #75.
- The counter's wrap is 23.4 Hz at 48 kHz, no longer infrasonic as the 2026-10-04 design described; its level is unchanged.
- The bit-identical limits in TESTING 6d are properties of any finite-alphabet signal, stated rather than hidden.
  Where two readings tie, the grader takes a stated convention, and the planted-arm log decides at a logged arm.
- The release mutation driver runs the whole self-test once per defect, so it now takes about 90 minutes.
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
