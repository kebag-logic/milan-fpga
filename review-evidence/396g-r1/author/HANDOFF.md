# HANDOFF: #396 part A (release gate plan, contract and documents), executor [A674]

Status: **REVIEW READY** at `21faa48242e021177a1dc702f28e51347c6a7a57`
(tree `dff7043fb74a2b30bca12bc48fa9e7d6fafd3296`), branch `396-release-gate-plan`,
one local commit on dev `e76a755afc0536453161e3cd33f6f4d2dcd7641f`. Not pushed. No PR operation.

- Assignment: #396 issuecomment-6408079016 (part A). Owner decisions: issuecomment-6408072465.
  Audio signal design: issuecomment-5978644444. `mr`/`tu` rule: issuecomment-5857762351,
  corrected by issuecomment-5857765949 (already merged through #593; unchanged here).
- TAKEN: issuecomment-6408201605. REVIEW READY: issuecomment-6409063728.
- Remote checked: `origin` is `https://github.com/kebag-logic/milan-fpga.git`; merge base with
  `origin/dev` is `e76a755a`. No git command was run inside any submodule; gitlinks unchanged.
- No firmware, RTL, builder, submodule, hardware, bench or flashing action.

## What the lane found, and how it was interpreted (published in TAKEN)

1. PR #586 and #593 had already merged the `soak` and `power` areas and REQ-VER-06 (seven days,
   200 cold cuts at 160/40, binding-only inventory). The lane re-parameterizes them to the
   2026-10-26 decisions rather than adding them again.
2. An `audio` area already existed (channel identity). The release audio-integrity run
   (`audio.integrity`) and its control join that area, so `--areas soak,audio,power` emits the
   gate. The audio identity audit is scoped to the identity steps, so the release step's
   all-index counter targets cannot mask an index-0-only identity loop (new check below).
3. Soft resets: T0 is the host-timestamped reset command, the analogue of the round-3
   power-strip ON origin. The mechanism is bench-declared and recorded per cycle; no power-off
   hold applies. Authority: Milan v1.2 5.5.1.4 ("a power cycle or a simple reset").
4. The eight items are issue #70's inventory (configuration, sampling rate, stream formats,
   presentation time offset, channel mappings, clock source, entity and group names, other
   object names) plus the binding (5.3.8.2/5.3.8.3/5.3.8.7). Milan v1.2 states no
   non-volatile clause for the current configuration; it is cited as #70 item 1.
5. Counter layout (the 2026-10-04 design made concrete): 24-bit sample in bits 31:8 of S32,
   bits 7:0 zero (the #451/#629 layout); sample bits 15:12 = channel index + 1 (no valid word
   is zero); bits 11:0 = sample counter mod 4096. Eight channels peak near -47 dBFS; the wrap is
   11.7 Hz at 48 kHz. Limit stated in code, plan and docs: slips are decided modulo 4096, a
   shift of 2048 or more aliases, an exact multiple of 4096 is invisible to the counter.
6. Capture format: headerless interleaved S32, big-endian (`tb/tools/thdn.py`, external capture)
   or little-endian (#451 TDM capture). The tracked planner synthesizes it offline, so the
   assignment's STOP condition does not apply.
7. Analog sine pair: no THD+N or residual limit is decided. `audio.analog-sine-pair` is NOT RUN
   until a recorded decision sets them; flagged as an open decision.
8. "Planted event" (MEDIA_UNLOCKED rule): a runner-logged deliberate disturbance with target,
   kind and window; each excuses at most one increment per input whose read interval it meets.
9. `audio_context_s` = 5 s, from the design's "a few seconds either side". Planted-arm defaults:
   3-sample drop, 2-sample repeat, mask `0x00000100`.
10. CONTRIBUTING had no "release PR" notion; the new bullet defines it (a PR promoting a shipping
    candidate toward `main`) and sets the gate for it.

## Changes (file:line at the head, reason)

| File:line | Change | Reason |
|---|---|---|
| `tb/tools/torture_campaign.py:3120` | `RELEASE_SOAK_DURATION_S = 86400` | Decision 1: 24 h soak |
| `tb/tools/torture_campaign.py:3123` | `RELEASE_POWER_PHASES` 100/50/50 | Decision 2: 150 cold (50 in commit), 50 soft resets |
| `tb/tools/torture_campaign.py:3128` | `RELEASE_PERSISTED_ITEMS`, clause per item | Decision 3: eight Milan items and the binding, as data |
| `tb/tools/torture_campaign.py:3143` | `ReleaseSettings`: new defaults, `reset_cycles`, `audio_duration_s`, `audio_context_s`, validation | Parameters for every area; audio must fit inside the soak |
| `tb/tools/torture_campaign.py:3199`, `:3209` | soak duration text 86400 s; stricter counter text | Decision 3: zero SEQ/INTERRUPTED/LATE/EARLY, zero unplanted MEDIA_UNLOCKED |
| `tb/tools/torture_campaign.py:3269` | `power.cycle-count-and-phase` (renamed from cold-count) | 200 cycles incl. soft resets; reset never counts as a cut |
| `tb/tools/torture_campaign.py:3276`, `:3286`, `:3306` | state-restored (eight items, vacuity), ADP T0 for resets, single-boot after cut and reset | Decision 3; soft-reset origin |
| `tb/tools/torture_campaign.py:3320` | `AUDIO_RELEASE_ASSERTS` (8 audio assertions + complete evidence) | Audio design, each with its clause |
| `tb/tools/torture_campaign.py:3361`, `:3368`, `:3372` | `RELEASE_REQUIRED_ASSERTS`, `RELEASE_CONTROLS`, `A_RELEASE_CONTROL` | "No step may skip a required assertion"; acceptance 4 |
| `tb/tools/torture_campaign.py:3426` | eligibility requires the full inventory | Decision 3 (was binding only) |
| `tb/tools/torture_campaign.py:3464`, `:3492` | `check_release_soak_counters` | Offline oracle for the stricter counter rules |
| `tb/tools/torture_campaign.py:3549` | `check_release_state_restored` | Offline oracle; vacuity trap; commit old-or-new |
| `tb/tools/torture_campaign.py:3598`-`:3680` | counter layout constants, `audio_counter_word`, `synthesize_counter_capture` | Signal contract and the offline synthetic capture |
| `tb/tools/torture_campaign.py:3681` | `_CounterScan` | Per-sample classifier: dropped, repeated, silence (replaced/inserted), bit-flip mask, swap |
| `tb/tools/torture_campaign.py:3867`, `:3907`, `:3925`, `:3938` | attribution, `CounterCapture`, `CounterRunLog`, `grade_audio_counter_capture` | Planted arms (void on miss, both ends), capture losses apart, streamed fast path |
| `tb/tools/torture_campaign.py:4261` | `plan_soak` args: counter oracle, zero-growth list, planted-event log | Decision 3 evidence |
| `tb/tools/torture_campaign.py:4315`, `:4335` | `_audio_control_fixture`, `_audio_release_steps` | `audio.integrity` inside the soak window; `audio.control.planted-drop` |
| `tb/tools/torture_campaign.py:4400` | `plan_power`: idle, journal_commit, soft_reset phases | Decision 2; reset T0, no hold, reset evidence |
| `tb/tools/torture_campaign.py:4494`, `:4535` | `_power_controls`, `run_release_control` | #366 and persistence-disabled controls with desk fixtures; one runner for all three controls |
| `tb/tools/torture_campaign.py:2429` | `plan_audio(dut, peer, settings)` = identity + release steps | Audio area gains the release run |
| `tb/tools/torture_campaign.py:4776`, `:4790` | identity audit scoped; `_release_area_defects` | Per-area audit: coverage, required SHALL assertions, phases, cycle mix, controls |
| `tb/tools/torture_campaign.py:4617`, `:7428`-`:7434`, `:7451`, `:7484` | build_plan passes settings to audio; CLI `--reset-cycles`, `--audio-duration-s`, `--audio-context-s`; table prints release args | Parameters reachable from the CLI |
| `tb/tools/torture_campaign.py:5736`-`:6226` | existing release arms updated to the new decisions | Same controls, new values |
| `tb/tools/torture_campaign.py:6738` | `_ReleaseGateChecks` (14 new arms) | New checks below |
| `tb/tools/torture_release_mutants.py:43`, `:613` | one anchor follows "next cycle"; 60 new planted defects | Each must fail a named arm |
| `tests/features/torture_campaign_plan.feature:304`-`:493` | audio rows; 24 h/100-50-50 defaults; cycle-mix, required-assertion, counter, control, grader scenarios | Assignment item 2 |
| `tests/steps/torture_release_steps.py:24`, `:41`, `:52`, `:377` | independent required-assertion table and inventory; repeat filter; new steps | Oracles stated apart from the planner |
| `REQUIREMENTS.md:322`-`:484` | REQ-VER-06: 24 h, stricter counters, audio row, 200-cycle mix, eight items, reset T0, controls; REQ-VER-05 blocker sentence names both campaigns | Decisions 1-4 |
| `CONTRIBUTING.md:420`-`:439` | release campaigns bullet; new "release gate for release PRs" bullet | Decision 4 |
| `docs/testing/TESTING.md:1021`-`:1455` (6d) | values, command, inventory, eligibility, soak counter oracle, audio-integrity section, soft resets, state oracle, negative-control table, retention per 6b | Assignment item 4 |
| `README.md:349` | "week-long soak" -> "24 h soak" (column-aligned) | Assignment item 4 |
| `docs/design/SAVED_STATE_MATERIALIZATION.md:2950`, `:2952`, `:2956` | restated REQ-VER-06 numbers and T0 | Consistency: the page restates REQ-VER-06's values |

## New checks (planted mutant, failing words)

All 60 defects below were added to `tb/tools/torture_release_mutants.py`; the unchanged self-test
fails the named arm with these words (`receipts/mutant_failing_words.log`):

| Check (self-test arm) | Planted mutant | Failing words |
|---|---|---|
| `test_release_defaults_and_assertions` | soak returns to seven days | `Tuples differ: (604800, 60) != (86400, 60)` |
| `test_release_eligibility_boundaries` | cycle minimums return to 160/40 | eligibility dict differs (`power.*: False != True`) |
| `test_release_eligibility_boundaries` | soft-reset minimum dropped | eligibility dict differs (`True != False`) |
| `test_release_defaults_and_assertions` | soft resets planned as cold cuts | `Lists differ: [True, True, True] != [True, True, False]` |
| `test_release_timing_and_snapshot_contract` | soft reset T0 taken from the power strip | `'T0: power-strip ON command, ...' != 'T0: reset command, ...'` |
| `test_release_defaults_and_assertions` | inventory loses the clock source | `Lists differ: [...] != [..., 'clock_source', ...]` |
| `test_release_eligibility_boundaries` | eligibility accepts the binding alone | `{'soak.continuous': True, ...} != {'soak.continuous': False, ...}` |
| `test_release_eligibility_boundaries` | audio duration eligibility dropped | `'audio.integrity': True != False` |
| `test_release_settings_validation` | audio run may outlast the soak | `ValueError not raised` |
| `test_release_soak_counter_growth` | zero-growth counters may grow; LATE / EARLY removed from the set | `'PASS' != 'FAIL'` |
| `test_release_soak_counter_growth` | soak counter decrease accepted | `'reset' not found in 'zero-growth counter grew'` |
| `test_release_soak_media_unlocked_planted` | MEDIA_UNLOCKED needs no planted event; one event excuses many; another input's event accepted | `'PASS' != 'FAIL'` |
| `test_release_soak_media_unlocked_planted` | planted window excludes the read edge | `'FAIL' != 'PASS'` |
| `test_release_soak_counter_evidence` | missing evidence accepted; endpoint read optional | `'PASS' != 'NOT RUN'` |
| `test_release_state_restored` | vacuity check removed | `'FAIL' != 'NOT RUN'` |
| `test_release_state_restored` | reverted state accepted; missing readback accepted | `'PASS' != 'FAIL'`; `'PASS' != 'NOT RUN'` |
| `test_release_state_commit_cut` | mixed commit state accepted; vacuous commit accepted | `'PASS' != 'FAIL'`; `'PASS' != 'NOT RUN'` |
| `test_release_controls_fail_as_planted` | #366 fixture healthy; persistence fixture restored; audio drop removed | `'PASS' != 'FAIL'` |
| `test_release_area_audit_refuses_each_defect` | control verdict / failing assertion / presence not audited; assertions or severity not audited | `True is not false` |
| `test_release_area_audit_refuses_each_defect` | power phases not audited | `'phases' not found in {'cycle_mix': ...}` |
| `test_release_area_audit_refuses_each_defect` | cycle mix not audited | `Tuples differ: (True, False) != (False, True)` |
| `test_release_audio_does_not_mask_identity` | release audio masks the identity audit | `True is not false : {'area': 'audio', ...}` |
| `test_audio_grader_classes` | isolated flip read as a slip; slip direction inverted; fast path compares the capture with itself | `'NOT RUN' != 'FAIL'` |
| `test_audio_grader_classes` | slip alias boundary moved | `'dropped' != 'repeated'` |
| `test_audio_grader_classes` | inserted silence not told apart | `8 != 4 : [...]` |
| `test_audio_grader_classes` | swap read as corruption | `'bit-flip' != 'swap'` |
| `test_audio_grader_classes` | DUT audio events pass | `'PASS' != 'FAIL'` |
| `test_audio_grader_attribution` | capture loss counted against the DUT | `Tuples differ: ('FAIL', [...]) != ('PASS', [])` |
| `test_audio_grader_attribution` | logged loss trusted without the capture; missed arm accepted; arm position, size or mask ignored | `'PASS' != 'NOT RUN'` |
| `test_audio_grader_attribution` | arms need not bracket the run | `'FAIL' != 'NOT RUN'` |
| `test_audio_grader_evidence` | torn final frame accepted | `'PASS' != 'NOT RUN'` |
| `test_audio_grader_evidence` | event overflow passes | `'NOT RUN' != 'FAIL'` |
| `test_release_defaults_and_assertions` | soak counter oracle unnamed; audio run outside the soak window; planted-event log not retained | dict / tuple differ; `'planted_event_log' not found in [...]` |
| `test_release_assertion_text` | six text mutants (unlock wording, 160/40, seven days, eight items, reset T0, timestamp counters) | `'<decided phrase>' not found in '<clause>'` |

Feature-level controls (`receipts/feature_mutants.py`, run on a scratch copy of the committed
`tests/` and `tb/tools/`): 15 planner defects, each fails at least one plan-feature scenario,
for example "soak returns to seven days" fails
`torture_campaign_plan.feature:342 release defaults encode the decided soak, audio run and cycle mix`,
"missed arm accepted" fails `:438 a missed planted arm voids the audio run`
(`receipts/feature_mutants.log`). Pristine copy: 133 scenarios pass.

Grader throughput (`receipts/grader_throughput.log`): the clean fast path grades about
36 capture-minutes per second for eight channels (24 h in about 40 s, plus I/O).

## Gate table (all at the head above, foreground, never piped; receipts in `receipts/`)

| Command | rc | Result |
|---|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | 0 | 94 tests OK (80 before) |
| `python3 -B tb/tools/torture_release_mutants.py` | 0 | 192 mutations killed (132 before + 60); source unchanged |
| `cd tests && behave --no-capture -f plain` (rtl-fast bdd-conformance) | 0 | 14 features, 452 scenarios, 2154 steps passed (406 scenarios before) |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | 0 | 133 scenarios, 533 steps |
| `docs_check.py` (pinned renderer) | 0 | 0 findings, 210 md + 1418 scrubbed files |
| `gen_toc.py --check` (pinned) | 0 | OK, 149 pages |
| `gen_toc.py --verify-anchors` (pinned) | 0 | 537 fragment links |
| `check_em_dash.py --base origin/dev` (pinned) | 0 | 0 findings over 222 added lines in 5 pages, arms 339/339 |
| `check_doc_style.py` (pinned) | 0 | OK, 23 documents |
| `check_doc_paths.py` (pinned) | 0 | 1065 cited paths resolve |
| `python3 -B scripts/check_py_idiom.py` | 0 | at ratchets; new Python complies (Rule 12) |
| `python3 -B scripts/check_feature_status.py` and `--self-test` | 0, 0 | 0 findings; 46/46 |
| `python3 -B tb/tools/torture_campaign.py --coverage-by-area --areas soak,audio,power` | 0 | all three areas complete |
| `git diff --check origin/dev HEAD`; `git diff --check` | 0, 0 | clean |
| feature-level planted defects (`receipts/feature_mutants.py`) | 0 | 15/15 killed; baseline 133 pass |

## Acceptance status (issue #396)

1. Met at the desk: decisions recorded on the issue (6408072465); REQ-VER-06 carries 24 h,
   200 cycles and the criteria; REQ-VER-05's blocker sentence names both campaigns.
2. Met: `--plan` emits `soak`, `audio` (release step) and `power` with interval and duration
   parameters; the feature asserts every index, both directions, the CRF sink, the 200-cycle mix
   and the required assertions; `--self-test` passes.
3. Open (part B): the bench runs on the shipping image.
4. Desk half met (three plan entries with failing assertions and desk fixtures; the audio drop is
   graded offline); the two power controls still need bench runs on the known-defect images.
5. Met: TESTING 6d and CONTRIBUTING name the gate and its artifacts; docs gates and behave pass.

So the PR body says "Relates to #396", not "Closes".

## Open items and risks

- **Decision needed:** THD+N and predictor-residual limits for the analog sine pair. Until set,
  `audio.analog-sine-pair` is NOT RUN and no release can qualify.
- `restore_bound_s = 30` stays provisional (ratification from #397/#75), unchanged.
- Soft-reset mechanism is bench-declared; the plan records but does not choose it. The pinned
  processor answers AECP REBOOT (1722.1-2021 7.4.43) with the NOT_IMPLEMENTED echo (its
  REQ-FWX-001), so REBOOT cannot be the mechanism.
- The counter cannot see slips that are exact multiples of 4096 samples; stated in code and docs.
- If the shipping image still shows #366, the first cold cut after any flash fails
  `power.single-boot` by design; part B must start the campaign accordingly or fix #366 first.
- The power controls' desk fixtures prove the oracles can fail; physical detection is part B.

## Receipts

`receipts/INDEX.md` is generated from the files present (name, size, SHA-256).
