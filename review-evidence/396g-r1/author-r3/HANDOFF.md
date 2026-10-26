# HANDOFF: #396 part A round 3 (release gate plan), executor [A674c]

Status: **REVIEW READY** at `4d69e1923ce8209029af6e084336f13cca834c29`
(tree `55e22fe10172e2965687b6fbab734cab19fe183d`), branch `396-release-gate-plan`.
Two round-3 commits sit on the round-2 head `a3e24ac5ef984cb92458f1728f2c275349ae9854`, which is not rewritten:
`9da26126a6a87af19f654f47cdb373172cc6026e` and `4d69e1923ce8209029af6e084336f13cca834c29`.
Base dev is `e76a755afc0536453161e3cd33f6f4d2dcd7641f`. Nothing is pushed, and no PR operation ran.

- Round-3 assignment: #396 issuecomment-6413452035. Findings answered: R700-2 (PR #786 issuecomment-6413374622)
  F1 MAJOR and F2 MINOR; R699-2 (issuecomment-6413444899) F1, F2 and F3 MINOR, and S1 to S4.
- TAKEN: issuecomment-6413676533. REVIEW READY - round 3: issuecomment-6415178051.
- Remote checked: `origin` is `https://github.com/kebag-logic/milan-fpga.git`; merge base `e76a755a`.
  No git command ran inside any submodule, and the gitlinks are unchanged.
  No RTL, firmware, builder, hardware, bench or flashing action ran.
- Commits, one line each, no body, no trailer:
  - `9da26126`: `Qualify only the observed audio interval, grade boundary block slips unresolved and one constant
    mask at every length (#396)`.
  - `4d69e192`: `Grade the invalid-anchor arm against its capture's qualified length so each anchor defect decides
    the verdict (#396)`.

## Findings and fixes (file:line at `4d69e192`, `tb/tools/torture_campaign.py` unless named)

| Finding | Change | Reason |
|---|---|---|
| R700-2 F1 (assignment 1) | `AUDIO_GUARD_FRAMES` `:3696`; `_CounterSlot.acquired` (set in `_close` `:4373`, at `:4414`); `_CounterScan.qualified` `:4461`; `_audio_qualified` `:4676`; `grade_audio_counter_capture` `:4709` with `required_s` (default `RELEASE_SOAK_DURATION_S`), verdict order `:4776`-`:4801` | A slip of whole blocks shows only within 63 samples, so only samples with 63 acquired samples before and 63 captured after are proved. Every verdict states `qualified` (start, end, frames, seconds, acquisition indices, logged losses inside). PASS needs `required_s` observed seconds; losses are not observed. A short interval is NOT RUN. Never-acquired channels, and arms or losses outside the interval, are NOT RUN by name. |
| R700-2 F1, R699-2 F2 (assignments 1, 4) | `AUDIO_CLASSES` adds `unresolved` `:3703`; `_audio_labels` `:3905` routes end and pre-acquisition runs to `_audio_boundary` `:3993`; `_audio_open` `:4081`; `_audio_window_events` `:4139` | At either end, words that differ from the track only in the code bit are one `unresolved` event. Its `located_within` bounds the slip, and its reason names both readings, so it is never an exact class. |
| R700-2 F2 (assignment 2) | `_audio_image_mask` `:4250`, `_AudioImage` `:4263`; held in `_close` (`mask = ...` `:4405`); merged on return `:4389`; released off-mask on the fast path `:4329` and per word, and by `_release` `:4353`; released `unresolved` at the end `:4436`; bound pieces in `_audio_excursion` `:4049` | Sixty-four corrupted words under one mask decode as another track. Holding that track until it returns or leaves the mask makes rule 4 hold at every length, and genuine image slips still come out exact. |
| R699-2 F1 (assignment 3) | `_audio_candidates` `:3960`, `_audio_fit` `:3980` (longest exact run, cut at unexplained words); re-judging after every slip `:4170` | One corrupted word no longer turns its whole run of positions into corruption. Departures are judged against the offset in force. |
| R699-2 F3 (assignment 5) | Test only: `test_audio_capture_losses_advance_the_clocks` `:8014` block | The code was right; the boundary is now pinned, and N07 fails it. |
| Regression in `9da26126`, fixed in `4d69e192` | `test_audio_capture_losses_advance_the_clocks` `:8038` block | The 24 h default made the clean capture NOT RUN whatever its anchors, so N30/N31 survived; the arm now grades against the clean qualified length, with a valid-anchor PASS control and exact refusal reasons. |
| S1 adopted (docs) | `docs/testing/TESTING.md:1394`; plan `capture_start` `:5162` | Leading words are graded against the acquired track; leading silence fails. |
| S2 adopted | `_audio_anchor_gaps` `:4690`, `anchor_gaps` in every verdict | Gaps shown, verdict unchanged. |
| S3 adopted | `:4752` | A channel not acquired within 65536 frames voids the run at once. |
| S4 adopted | `TESTING.md:1388`; `_audio_excursion` `:4049` | The bound is documented, and pieces keep the constant-mask class. |
| Plan contract | `AUDIO_QUALIFICATION` `:3716`, `AUDIO_COUNTER_LIMITS` `:3726`; `counter_grader_required_s` `:5153`; `qualification` `:5155`; `planted_placement` `:5158`; control fixture `required_s` `:5113`, passed by `run_release_control` `:5366` | The emitted plan states the interval, the requirement and the capture rule. |
| Assertion texts | `audio.inside-soak-window` `:3326`, `audio.counter-classified` `:3338`, `audio.planted-arms-found` `:3354`, `audio.capture-losses-apart` `:3360`, `audio.zero-dut-glitches` `:3380` | Each states the new rule and its limits. |
| Docs | `REQUIREMENTS.md:412`, `:415`-`:420`, `:430`; `docs/testing/TESTING.md:1275`, `:1322`, `:1343`-`:1364`, `:1382`-`:1398`, `:1408`, `:1417`, `:1431`-`:1434` | REQ-VER-06 and TESTING 6d follow every change. |
| Steps and feature | `tests/steps/torture_release_steps.py:582` (`_qualified_s`), `:819`-`:928`; `tests/features/torture_campaign_plan.feature:477`-`:516` | Feature-level scenarios for each item, on the steps' own encoder. |
| Driver | `tb/tools/torture_release_mutants.py`: 30 defects added (`:889`-`:965`), one re-anchored (`inserted silence not told apart`) | Each fails a named arm. |

## New checks (planted defect, failing words; `receipts/mutant_failing_words.log`)

New arms: `test_audio_qualified_interval_is_stated_and_required` `:8105`, `test_audio_boundary_block_slips_are_unresolved`
`:8169`, `test_audio_constant_mask_at_every_length` `:8249`, `test_audio_slip_and_corruption_share_a_window` `:8299`,
`test_audio_anchor_gaps_are_reported` `:8337`. Extended: `test_audio_capture_losses_advance_the_clocks`,
`test_release_audio_control_classifies_exactly`, `test_release_defaults_and_assertions`. `_independent_bytes` `:7831`
builds captures from the restated layout (`_word`); its empty, `F-1`/2048 and `F-2`/8192 captures reproduce the
reviewer's published SHA-256 `f395a643...`, which the boundary arm pins.

| Planted defect | Named arm | Failing words |
|---|---|---|
| qualified interval runs to the capture's end | boundary | `8192 not less than 8191` |
| qualified interval starts at acquisition | qualified | `{'start': 0, ...} != {'start': 63, ...}` |
| acquisition index not recorded | qualified | `('FAIL', 63, 8129) != ('FAIL', 73, 8129)` |
| required duration not enforced / defaults to 0.1 s | qualified | `('PASS', [], ...) != ('NOT RUN', [], 'the qualified interval is ...')` |
| capture losses counted as observed time | qualified | `'PASS' != 'NOT RUN'` |
| arm / loss outside the qualified interval accepted | qualified | `('NOT RUN', '<other reason>') != ('NOT RUN', '<named reason>')` |
| unacquired channel passes | qualified | `('PASS', [2], None) != ('NOT RUN', [2], None)` |
| unacquired channel graded to the end | qualified | `262144 not less than or equal to 66048` |
| capture-end stretch graded exactly / open words reported as a corruption | boundary | `'bit-flip' not found in ('unresolved', 'dropped')` |
| pre-acquisition stretch graded exactly | boundary | `12 != 4 : [{... 'class': 'bit-flip' ...` |
| open stretch bound widened at the end / before acquisition | boundary | `False is not true : {...}` / `1 not less than 0` |
| half-block alternative dropped | boundary | `Items in the first set but not the second:` |
| open stretch never closes an excursion | boundary | `[(2, 8172, 'repeated', 1024 ...)] != [(2, 8172, 'bit-flip', 2, '0x00080000' ...` |
| a run fits whole or not at all | window | `[(2, 3000, 'bit-flip', 6, '0x0000FF00')] != [(2, 3005, 'bit-flip', 1, '0x00000100')]` |
| departures after a slip not judged again | window | `[] != [(2, 3005, 'bit-flip', 1, '0x00080000')]` |
| constant-mask track adopted / held excursion never returns | mask | `('FAIL', [(2, 3000, 'repeated', 499717412864 ...` |
| held excursion not carried across a region | mask | same words, 2000-word case |
| held excursion kept off its mask (fast block / per word) | mask | `'unresolved' unexpectedly found in {...}` |
| excursion open at the end / cut by the end window released as exact | mask | set differs / `None unexpectedly found` |
| window-bound pieces lose their corruption | mask | `Items in the first set but not the second:` |
| anchor gap after the last anchor not reported / measured over stored frames | anchors | `('PASS', []) != ('PASS', [[0, 8192]])` / `[[0, 4000]]` |
| a loss at the event's own index not counted (N07) | clocks | `7000 != 10000` |
| inserted silence not told apart (re-anchored) | classes | `8 != 4` |

Feature level (`receipts/feature_mutants.log`): nine planner defects each fail a named round-3 scenario; the pristine
copy passes all 162.

Against round 2's code (`receipts/round2_head_vs_new_tests*.log`): the round-3 test class transplanted onto the round-2
planner errors on the new keyword. With a shim that accepts and drops `required_s`, it fails on behaviour. The
boundary, mask, window, interval, anchor-gap and control arms fail there. The loss-index and anchor arms pass,
as they should: F3 was a missing test, and N07's kill is its proof.

## Reviewer evidence rerun at `4d69e192` (scripts byte-identical to the published manifests)

- R700-2 `delta_probes.py` unmodified (`receipts/r700_delta_probes_unmodified.*`):
  - interior rows are unchanged;
  - the clean control and the byte-identical tail pairs are NOT RUN, since sub-second captures cannot meet the 24 h rule;
  - `tail-slip-8191-4096`, `tail-slip-with-64-more-frames` and `initial-slip` are `unresolved`;
  - `constant-code-xor-64`, `-65`, `-100` and `-chunked` are one `bit-flip`.
- Ported by `scripts/make_ports.py`, which adds `required_s` and records `qualified` (`receipts/r700_delta_probes.port.diff`).
  The clean control and both byte-identical pairs PASS with `[63, 8129)`. `initial-slip` starts the interval at 73.
- R699-2 probes unmodified (`receipts/r699_*_unmodified.log`):
  - compound 30/30 OK;
  - arm A2 to A5 FAIL as owed;
  - edge X1 `unresolved` at `F-20` to `F-63`, and X4 NOT RUN by name;
  - N07 probe at 8214;
  - misuse refused within 65536 frames;
  - the other DEVIATION lines are clean captures NOT RUN by the 24 h rule.
- Ported with `required_s` only (`receipts/r699_grader_probe_r2.port.diff`): every line OK except P5.
  P5 plants no arms, so it is void, exactly as in the reviewer's round-2 receipt (110 OK, 1 DEVIATION).
- R699-2 `reviewer_mutants_r2.py` unchanged: 32 KILLED, 0 SURVIVED, 0 INVALID (N07, N30, N31 killed).
  The round-1 runner, unchanged: 22 KILLED, 6 INVALID on round-1 code.
- Throughput (`receipts/grader_throughput.log`), 8 channels at 48 kHz, 1 MiB chunks: clean 5.8 capture-minutes per
  second (about 4 min per 24 h); one-channel offset 5.6; a channel without the counter 6.4.

## Gate table (exact head, foreground except the driver, never piped; receipts in `receipts/`)

| Command | rc | Result |
|---|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | 0 | 108 tests OK (103 before) |
| `python3 -B tb/tools/torture_release_mutants.py` (background, polled) | 0 | `PASS: 249 mutations killed; source unchanged` (219 before) |
| `cd tests && behave --no-capture -f plain` (rtl-fast bdd-conformance) | 0 | 14 features, 481 scenarios, 2244 steps (log hashed) |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | 0 | 162 scenarios, 623 steps (150 before) |
| `docs_check.py` (pinned renderer) | 0 | 0 findings, 210 md + 1418 scrubbed files |
| `gen_toc.py --check` / `--verify-anchors` (pinned) | 0 / 0 | 149 pages / 538 fragment links |
| `check_em_dash.py --base origin/dev` (pinned) | 0 | 0 findings over 361 added lines in 5 pages |
| `check_doc_style.py` (pinned) | 0 | 23 documents OK |
| `check_doc_paths.py` (pinned) | 0 | 1065 cited paths resolve |
| `python3 -B scripts/check_py_idiom.py` | 0 | at ratchets (long function 9, long module 10, over-long line 0) |
| `python3 -B scripts/check_feature_status.py` and `--self-test` | 0, 0 | 0 findings |
| `torture_campaign.py --coverage-by-area --areas soak,audio,power` | 0 | three areas complete |
| `torture_campaign.py --plan --areas soak,audio,power --json` | 0 | 17 steps; digest and contract in `plan_audit.json` |
| `git diff --check origin/dev HEAD`; `git diff --check` | 0, 0 | clean; porcelain empty |

## Acceptance status (issue #396)

The status is unchanged from rounds 1 and 2. Items 1, 2 and 5 are met at the desk, and so is the desk half of item 4.
Items 3 and 4 need the bench (part B), so the PR body says "Relates to #396".

## Open items and risks

- Owner decision issuecomment-6409128703 is not yet carried by the plan text. It sets AECP REBOOT for the soft resets
  and the sine-pair limits at baseline + 6 dB. It lies outside this round's assignment, for the manager to route.
- Each capture must run past 24 h at both ends by its guards and any logged loss, and the soak window by as much.
  This follows from "the run passes only if the qualified interval covers the full 24 h" with losses not observed.
- The reviewers' unmodified probes read their clean sub-second captures as NOT RUN under the 24 h default.
  The ports show the classification beneath it.
- `restore_bound_s = 30` stays provisional.
- The 65536-frame early refusal also voids a capture that starts with more than 65536 frames before the counter flows.
  TESTING 6d says to start the capture once the counter flows.

## Receipts

`receipts/INDEX.md` is generated from the files present (name, bytes, SHA-256). The scripts that produced
receipts are in `scripts/`, and reviewer-derived ports state their changes in `make_ports.py`. The full behave log
(over 200 KB) and the plan JSON are hashed, not copied.
