# HANDOFF: #396 part A round 4 (release gate plan), executor [A674d]

Status: **REVIEW READY** at `85da3e4595871c1573c28b4d040b9e98463a41c9`
(tree `9ed9c6f592675f0e9bf59858b80a77c6255ccb22`), branch `396-release-gate-plan`.
One round-4 commit sits on the round-3 head `4d69e1923ce8209029af6e084336f13cca834c29`, which is not rewritten.
Base dev is `e76a755afc0536453161e3cd33f6f4d2dcd7641f`. Nothing is pushed, and no PR operation ran.

- Round-4 assignment: #396 issuecomment-6417665116. Findings answered: R699-3 (PR #786 issuecomment-6417659353)
  F1 and F2 (MINOR), and suggestions S1 and S2. R700-3 (issuecomment-6416855079) is POSITIVE.
- TAKEN: issuecomment-6418516955. REVIEW READY - round 4: issuecomment-6422609857.
- Remote checked: `origin` is `https://github.com/kebag-logic/milan-fpga.git`; merge base `e76a755a`.
  Read-only checks inside the initialised submodules confirmed each top-level directory and origin;
  the gitlinks are unchanged (`receipts/head.txt`). No RTL, firmware, builder, hardware, bench or flashing action ran.
- Commit, one line, no body, no trailer: `85da3e45`: `Grade a whole-block slip after a one-word corruption, let the
  arm log decide bit-identical readings and keep constant-mask excursions whole beside one-word events (#396)`.

## Findings and fixes (file:line at `85da3e45`, `tb/tools/torture_campaign.py` unless named)

| Finding | Change | Reason |
|---|---|---|
| F1: the offset in force is lost | `_audio_labels` keeps `held`, the offset before the last change, as a candidate (`:3960`, `:3989`) | Once a corrupted word fitted the closing track, the old offset stopped being a candidate, so later old-track words read as phantom flips |
| F1: the longest run wins | `_audio_fit` `:4017` keeps the offset nearest the one in force while it fits, else the longest run among the others; `_audio_candidates` `:3995` orders half-block twins toward the offset before | Each slip takes the smallest size the positions allow (the documented cluster rule), and a slip of whole blocks sits at the first word that shows it |
| F1: a corruption absorbed into the slip | `_audio_excursion` `:4127`: a departure ends at the first word from which every word up to its return fits the offset in force | Rule 3's "returns at once" was judged by the labels, not by the words, so coincident words lengthened a one-word corruption into a slip pair |
| F1: a half-block corruption before a whole-block slip | `_audio_excursion` `:4135`: a departure whose positions return a whole number of blocks away is judged as a corruption beside that slip, against whichever track gives its mask fewer bits set (`:4144`) | Either reading is two events; the single-bit mask is the corruption, so R700-3's boundary-matrix case `compound-4096-1-80000` now meets its compound rule |
| F1: a slip placed outside its bounds | `_audio_slip` `:4160` runs `located_within` on to the first word that shows the slip (`:4173`, via `_audio_upto` `:4183`, the resync's 64 words included); a corrupted word no longer bounds it where the tracks coincide (`:4318`) | At the resync, words that fit both tracks put the slip after the reported index (the `A-drop4096-5-after-repeat` case); a corrupted word has the same mask on either side where the tracks coincide |
| F1: the planted flip arm voids the run | `_CounterScan` takes the arm log (`:4471`, `:5033`); `_read` `:4546`, `_cut` `:4591`, `_score` `:4618`, `_AudioSteer` `:4083`, `_audio_arm_found` `:4805` | Where the bytes allow two readings, the log decides: a missed flip arm is tried as the corrupted word, judged against the offset in force or the closing one, and the window opened before its start where the slot followed that word. Taken only with no more DUT events and more arms found, so the log never hides a DUT event |
| F1 (wider sweep): a slip arm absorbed | `slip` in `_audio_window_events` `:4272` splits a slip that differs from a logged slip arm by whole blocks, located both sides; `_audio_excursion` `:4148` keeps an excursion a slip arm enters or leaves as its slips | A DUT slip of any size beside any arm must FAIL with every arm found; 39936 swept placements around six arms now do |
| F2: a one-word event beside a held excursion | `_hold` `:4624` starts the hold at the window's trailing words under the closing mask, recording earlier events | A flip before the excursion made the whole window's mask non-constant, so the excursion was adopted as a slip pair |
| F2: the return after the excursion | `_close` `:4688` returns when the content resumes nearer the old track than the held one; `_returned` `:4522` ends the bit-flip where the old track's words began and grades the rest against the old track | A flip after the excursion, or a planted drop at its return, released the hold as slips |
| F2: a code-bit corruption ending on a block | `_AudioImage.keeps` `:4426`, `clean` `:4420`, `holds` `:4434`, per word `:4502`: an old-track word is a possible return; a masked word after it parts the masks | The first returned words also fitted the held track past the block, so the per-word release fired on the return itself |
| S1 adopted | `docs/testing/TESTING.md:1380`-`:1382`; self-test comment `:8507` | The interval decides what is proved clean, not the class |
| S2 adopted | void reasons `:5049`, `:5074`; `docs/testing/TESTING.md:1434`-`:1435` | A channel the DUT never drives with the counter is named |
| Docs | `REQUIREMENTS.md:412`-`:414`; `docs/testing/TESTING.md:1343`-`:1371`, `:1390`-`:1417`; `AUDIO_COUNTER_LIMITS` `:3731`; `audio.counter-classified` `:3338`; `audio.planted-arms-found` `:3357` | Each rule and each bit-identical limit stated exactly; "one corrupted word never hides the slips beside it" withdrawn |
| Layout | `tb/tools/torture_release_audio_mutants.py` (the audio-grader controls, concatenated at `tb/tools/torture_release_mutants.py:887`); `tests/steps/torture_audio_model.py` (the capture helpers, imported at `tests/steps/torture_release_steps.py:23`) | Both files passed the 1000-line module rule; the split follows the `aecp_engine_model.py` precedent |

## New checks (planted defect, failing words; `receipts/mutant_failing_words.log`)

New arms: `test_audio_block_slip_after_a_corruption_or_a_slip` `:8661`, `test_audio_planted_arms_beside_block_slips`
`:8731`, `test_audio_constant_mask_beside_one_word_events` `:8791`, `test_audio_code_bit_corruption_ending_on_a_block`
`:8814`. Changed: `test_audio_slip_and_corruption_share_a_window` `:8612` pins the code-bit tie by byte identity
(`_corruption_first` `:8596`). All five fail on `4d69e192` (`receipts/transplant_round4_arms.log`). New scenarios
`tests/features/torture_campaign_plan.feature:514`, `:525`, `:538`, `:549`: 11 of their 14 examples fail on `4d69e192`
(`receipts/feature_on_round3.log`); the other three are controls.

| Planted defect (driver entry) | Named arm | Failing words |
|---|---|---|
| offset before the last change not a candidate (250) | after | `+ [(2, 3000, 'bit-flip', 1, '0x00000100', None)]` |
| longest run wins over the offset in force (251) | after | `+ [(0, 2048), (1, 2048), (2, 2048), (3, 2048)]` |
| half-block offsets not ordered toward the offset before (252) | after | same words |
| a return at the next word not cut from the excursion (253) | after | `+ [(2, 3000, 'bit-flip', 1, '0x00000100', None)]` |
| a return a whole number of blocks away not cut (254) | after | `+ [(0, 2048), (1, 2048), ...]` |
| slip of whole blocks not located on past its first word (255) | after | `False is not true : [(0, 2048, 3062, 3064), ...]` |
| a corruption beside a slip judged only against the old track (269) | after | `+ [(2, 3000, 'bit-flip', 1, '0x00080000', None)]` |
| a corrupted word bounds the slip where the tracks coincide (256) | arms | `False is not true : {'capture_index': 501, 'class': 'repeated', ...` |
| slip arm absorbed by a slip of whole blocks (257) | arms | `+ ('FAIL', []) : void: a planted arm was missed` |
| split slip located only after its arm (258) | arms | `False is not true : {'capture_index': 300, ... 'located_within': [300, ...` |
| no reading led by a logged flip arm (259) | arms | `+ ('FAIL', []) : void: a planted arm was missed` |
| arm-led reading taken whatever its DUT events (260) | arms | `+ ('NOT RUN', [3001]) : 3001` |
| arm-led reading never judged against the closing offset (261) | arms | void, as 259 |
| arm-led reading never opened before the window (262) | arms | void, as 259 |
| arm-led reading never cuts a word from the resync (263) | arms | void, as 259 |
| a slip arm never keeps the excursion it enters or leaves (270) | arms | `+ ('FAIL', []) : (299, 'void: a planted arm was missed')` |
| a word on the new track read as its own corruption (271) | arms | void, as 259 |
| hold judged over the whole window (264) | beside | `- (2, 3100, 'dropped', 1024, None, None)]` |
| events beside a returned excursion lost (265) | beside | `+ (2, 3100, 'bit-flip', 1, '0x00000100', None)]` |
| a held excursion returns only onto the old track (266) | beside | `+ ('FAIL', []) : void: a planted arm was missed` |
| the old track's own word releases a hold (267) | ending | `- (2, 8194, 'dropped', 499717421056, None, None)]` |
| returned excursion ends at the window (268) | ending | `+ [(2, 5000, 'bit-flip', 3192, '0x00000100', None)]` |
| re-anchored: half-block alternative dropped (235) | boundary | `('repeated', 1024)` |
| re-anchored: constant-mask track adopted as a slip (239), held excursion never returns (240) | mask | `- (2, 3064, 'dropped', 499717412864, None, None)])` |
| re-anchored: held excursion kept through a word off its mask (243) | mask | `'unresolved' unexpectedly found in {...}` |

The self-test grew from 108 to 112 arms and from about 8 to about 17 seconds.

## Reviewer evidence rerun at `85da3e45` (scripts byte-identical to the published manifest; `receipts/r699-3/`)

- `r3_arm_void_probe.py`: no NOT RUN line; every size 0 of 256 not FAIL.
- `r3_cluster_probe.py`: FB 654/6, SB 258/2, CF 32/0, CB 40/0 (433, 89, 28 and 12 deviations before).
- `r3_probe.py`: E 642/6, S 1170/0, M 273/0, A 21/8.
- `receipts/limit_proofs.log`: every one of the 22 remaining deviations is PROVED as its stated limit, with the reviewer's encoder:
  - FB and SB: the bytes equal the stated alternative;
  - A: located_within holds the slip, or it is a stated limit;
  - E: S1's case.
- Round-2 probes: compound 30/30; the arm probe A2 to A5 FAIL; `grader_probe_r2` has the same OK and DEVIATION per case
  as at `4d69e192`; the port is 110 OK plus P5; N07 at 8214; misuse refused with the S2 wording.
- `reviewer_mutants_r2.py`: 31 KILLED, 0 SURVIVED, 1 INVALID (N15's line changed). `scripts/port_n15.py` ports only
  its anchor: KILLED by five arms.
- `r3_reviewer_mutants.py`: 13 KILLED, 0 SURVIVED, 3 INVALID (V07, V09, V13). `scripts/port_r3_mutants.py` ports each
  to its new line: all KILLED.
- R700-3's probes, byte-identical copies run from scratch (`receipts/r700-3/compare.log`):
  - `delta_probes`, `qualified_probes` and `compound_ambiguity` give byte-identical output at `4d69e192` and here;
  - in the boundary matrix, `compound-4096-1-80000` now meets its compound rule;
  - `compound-4096-5-100` is the stated code-bit tie.
- `receipts/arm_sweep.log` and `receipts/arm_sweep_odd.log` (`scripts/arm_sweep.py`, `scripts/arm_sweep_odd.py`,
  the reviewer's encoder): 21504 and 18432 placements, DUT slips of 1 to 8192 samples 1 to 64 samples either side
  of all six arms, every one FAIL with every arm found.

## Gate table (exact head, foreground except the driver, never piped; receipts in `receipts/`)

| Command | rc | Result |
|---|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | 0 | 112 tests OK |
| `python3 -B tb/tools/torture_release_mutants.py` (background, polled) | 0 | `PASS: 271 mutations killed; source unchanged` |
| `cd tests && behave --no-capture -f plain` (rtl-fast bdd-conformance) | 0 | 14 features, 495 scenarios, 2286 steps (log hashed) |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | 0 | 176 scenarios, 665 steps |
| `docs_check.py` (pinned renderer) | 0 | 0 findings, 210 md + 1418 scrubbed files |
| `gen_toc.py --check` / `--verify-anchors` (pinned) | 0 / 0 | 149 pages / 538 fragment links |
| `check_em_dash.py --base origin/dev` (pinned) | 0 | 0 findings over 400 added lines in 5 pages |
| `check_doc_style.py` (pinned) | 0 | 23 documents OK |
| `check_doc_paths.py` (pinned) | 0 | 1065 cited paths resolve |
| `python3 -B scripts/check_py_idiom.py` | 0 | at ratchets (514 modules) |
| `python3 -B scripts/check_feature_status.py` and `--self-test` | 0, 0 | 0 findings |
| `torture_campaign.py --coverage-by-area --areas soak,audio,power` | 0 | three areas complete |
| `torture_campaign.py --plan --areas soak,audio,power --json` | 0 | 17 steps (`receipts/plan.json`) |
| `git diff --check origin/dev HEAD`; `git diff --check`; porcelain | 0, 0, 0 | clean; porcelain empty |

## Acceptance status (issue #396)

The status is unchanged from rounds 1 to 3. Items 1, 2 and 5 are met at the desk, and so is the desk half of item 4.
Items 3 and 4 need the bench (part B), so the PR body says "Relates to #396".

## Open items and risks

- Ties between bit-identical readings take a stated convention: corruption first for the code-bit tie, the
  single-bit mask for a half-block corruption beside a slip. This changes R700-3's `compound-4096-5-100` and the
  round-3 self-test case it mirrors; the self-test now pins that case's bytes, so the change is explicit.
- Owner decision issuecomment-6409128703 (AECP REBOOT for the soft resets; sine-pair limits at baseline + 6 dB) is
  still not in the plan text, for the manager to route. `restore_bound_s = 30` stays provisional.
- The mutation driver's serial run now takes about 90 minutes.
- Scratch outside the tree: the two driver runs I stopped left temporary planner copies; both were removed. The
  other `release-controls-*` temporary directories predate this session and were left alone.

## Receipts

`receipts/INDEX.md` is generated from the files present (name, bytes, SHA-256). The scripts that produced receipts
are in `scripts/`. The full behave log and the cluster probe log (each over 200 KB) are hashed, not copied.
