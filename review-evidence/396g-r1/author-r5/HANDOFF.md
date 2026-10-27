# HANDOFF: #396 part A round 5 (release gate plan), executor [A674e]

Status: **REVIEW READY** at `910d4b94c4d5334b1869f42e9653c308a15d0dba`
(tree `07ce568e5a407531407917c5e8f81d524cd09947`), branch `396-release-gate-plan`.
Three round-5 commits sit on the round-4 head `85da3e4595871c1573c28b4d040b9e98463a41c9`, which is not rewritten.
Base dev is `e76a755afc0536453161e3cd33f6f4d2dcd7641f`. Nothing is pushed, and no PR operation ran.

- Round-5 assignment: #396 issuecomment-6424374359. Findings answered: R699-4 (PR #786 issuecomment-6424363636)
  G1 to G4 (MINOR), residue R1 and suggestions S1 to S3. R700-3 stays POSITIVE.
- TAKEN: issuecomment-6424440613. REVIEW READY: issuecomment-6431708324.
- Remote checked: `origin` is `https://github.com/kebag-logic/milan-fpga.git`; merge base `e76a755a`.
  In protocol-processor and gptp-processor, `rev-parse --show-toplevel` is the directory and origin is the processor
  repository. Read-only checks only; the gitlinks are unchanged (`receipts/head.txt`). No RTL, firmware, builder,
  hardware, bench or flashing action ran.
- Commits, one line, no body, no trailer:
  - `4a460fc3`: `Balance every audio reading against its decoded shift, hold excursions at the offset in force, grade
    one-word events beside them and sweep each planted arm's neighbours (#396)`;
  - `17a43ef2`: `Pin the interrupted constant-mask excursion with a DUT slip as well as a planted one (#396)`;
  - `910d4b94`: `Stop the composition sweeps at their first failing case, after a clean-capture check, so a broken
    grader fails them at once (#396)`.
- Why the third commit: the first serial driver run, at `17a43ef2`, stopped at its 196th control. The mutated
  self-test of `block code bit dropped from the word` passed the driver's 600-second limit, because under it every
  sweep case failed slowly (about 420 seconds for the two sweeps). The driver treats a timeout as no kill. The
  sweeps now check a clean capture first and stop at their first failing case, which they name; under that
  control they fail in about a second. The driver was restarted at `910d4b94`.

## How the ruling was applied

1. G3 by an invariant. The only source of an unbalanced reading was the hold: it built its image against offset 0
   while the reading had recorded a slip before the masked run. The hold now sits at the offset in force and re-reads
   what it must; the invariant is explicit in `_read` (ranking) and `_close` (a per-channel ledger and a guard whose
   fallback is one `unresolved` event). The 44 near-boundary regressions had a second cause (a coincident word kept a
   code-bit excursion's offset), fixed in `_audio_return`. `r4_net_sweep.py`: 0 unbalanced. `r4_regress_sweep.py`:
   0 regressions, 0 deviations.
2. G1 and G2. G2's slip-before shape is resolved by item 1's construction; its adjacent shapes needed the excursion's
   ends read as one-word events, which also resolves the flip-arm adjacency of G1. What remains of G1 would need an
   arm-led heuristic, so it is stated exactly (two voids, one bit-identical limit) and pinned by the sweep.
3. The composition sweep and the slip-before sweep are self-test arms, each case checked against the class its bytes
   put it in.
4. W03 and W07 are killed by a release-tolerance arm.
5. R1 as written.

STOP condition: not met. Against the round-4 head, the seeded fuzz changes five verdicts, all NOT RUN to FAIL, all a
corruption on channel 1 one sample beside the flip arm (a swept shape). Every other earlier probe gives the same
output, timing aside. One attempt that would have met it was reverted before commit: limiting the offset-before
candidate to that exact offset fixed R-4857 but flipped R-5869 from FAIL to NOT RUN, a cluster outside the swept shapes.
R-4857 is instead inside the stated own-sample void.

## Changes (file:line at `910d4b94`, `tb/tools/torture_campaign.py` unless named)

| Change | Where | Reason |
|---|---|---|
| Hold at the offset in force where the masked run begins | `_hold` `:4732` | G3 and G2: the image was judged against offset 0 while the reading had moved |
| Re-read the recorded part to end on that offset; hold only where a slip may lie in the masked run | `_split` `:4772` | G3: the recorded slips must sum to the image's offset; R-1624: a half-block slip is the old track under 0x80000 |
| A reading that does not balance ranks behind every one that does | `ranked` in `_read` `:4672` | Ruling item 1: an unbalanced reading is rejected |
| Per-channel ledger and guard; fallback event | `_close` `:4839`, `:4857`, `:4863`; `_record` `:4890`; `_unbalanced` `:4873`; `AUDIO_UNBALANCED_REASON` `:3717`; `_CounterSlot` `shift`, `reported` | Ruling item 1: no slip that did not happen is ever reported |
| `_audio_net` | `:4266` | The signed shift of events, inserted silence included |
| Excursion end after a constant-mask lead no single whole-block offset explains | `_audio_return` `:4181` | G3's 44 regressions: a coincident word carried the excursion into its neighbour |
| One word off the mask at either end, and each word of a two-word excursion under two masks, is its own event | `_audio_corruption` `:4211`, `:4232`; `_audio_extend` `:4310` | G2 adjacency; G1 flip-arm adjacency |
| A constant-mask excursion ending in a slip is one bit-flip and that slip | `_audio_excursion` `:4162` | G2: 30 near-boundary slip-at-return shapes read as three slips |
| `_audio_excursion` split into `_audio_excursion`, `_audio_return`, `_audio_corruption` | `:4125`-`:4263` | The 100-line function ratchet; checked behaviour-preserving (every probe log byte-identical before and after) |
| R1 wording; balance sentence | `_read` docstring `:4647` | R1 |
| `counter_limits` and assertion texts | `AUDIO_COUNTER_LIMITS` `:3738`; `audio.counter-classified` `:3338`; `audio.planted-arms-found` `:3360` | Invariant, limits, voids, narrowed claims |
| Docs | `REQUIREMENTS.md:412`-`:419`; `docs/testing/TESTING.md:1340`-`:1393`, `:1445`-`:1478` | Each rule, limit and void stated; "either order", "never hides" and "beside any one-word event" narrowed or made true |
| Release controls | `tb/tools/torture_release_audio_mutants.py:20`-`:23`, `:157`-`:202` (18 new, 289 in all); re-anchored `:72`, `:110`, `:139`, `:152`, `tb/tools/torture_release_mutants.py:740`, `:838`-`:843`; `:129` compares only the arms found, the third part of the score | Each new rule has a planted defect; seven anchors moved with the rewrite |

## New checks (each fails on `85da3e45`, `receipts/transplant_round5_arms_final.log`, except the interplay arm,
which targets mutants)

| Arm | What it pins | Fails on `85da3e45` |
|---|---|---|
| `test_audio_slip_totals_balance_the_bytes` `:9232` | G3 shapes; the guard; the ranking | 6 shapes and the guard |
| `test_audio_composition_sweep` `:9179` (helpers `:9044`-`:9178`) | G1: 3456 arm-adjacent cases, class from bytes | its first case (28 of 288 captures in the subtest form of `4a460fc3`) |
| `test_audio_slip_before_a_constant_mask` `:9207` | G2: the reviewer's 750-case grid | its first case (100 of 150 captures in the subtest form of `4a460fc3`) |
| `test_audio_constant_mask_beside_one_word_events` `:8976` (extended `:8994`, `:9007`) | G2 adjacency, slip at return; S3 | 8 subtests |
| `test_audio_arm_interplay_at_the_release_tolerance` `:9293` | G4: W03, W07 | passes (kills the mutants) |

Planted defect, the arm that fails, and its first failing words (`receipts/quick_named_mutants_final.log`, run on the
exact-head export; the 18 new entries and the 8 changed ones):

| Planted defect | Arm that fails | First failing words |
|---|---|---|
| lone corrupted word kept as a slip pair | `test_audio_tag_integrity_decides_first` | `Diff is 2319 characters long. Set self.maxDiff to None to see it.` |
| constant-mask excursion kept as slips | `test_audio_compound_and_edge_events` | `-  (3, 3002, 'repeated', 4, None, None)]` |
| hold read as corruption | `test_audio_compound_and_edge_events` | `+  (3, 3001, 'dropped', 1)]` |
| constant-mask track adopted as a slip | `test_audio_constant_mask_at_every_length` | `-   (2, 3064, 'dropped', 499717412864, None, None)])` |
| a return at the next word not cut from the excursion | `test_audio_block_slip_after_a_corruption_or_a_slip` | `?         ^` |
| arm-led reading taken whatever its DUT events | `test_audio_planted_arms_beside_block_slips` | `+ ('NOT RUN', [3001]) : 3001` |
| hold judged over the whole window | `test_audio_constant_mask_beside_one_word_events` | `-  (2, 3100, 'dropped', 1024, None, None)]` |
| a slip arm never keeps the excursion it enters or leaves | `test_audio_planted_arms_beside_block_slips` | `+ ('FAIL', []) : (299, 'void: a planted arm was missed')` |
| hold judged only against the window's opening offset | `test_audio_slip_before_a_constant_mask` | `-  (3064, 'repeated', 1024, '')]` |
| hold tried at its shortest masked run first | `test_audio_slip_before_a_constant_mask` | `-  (4189, 'repeated', 1024, '')]` |
| recorded part of a hold never read again | `test_audio_slip_totals_balance_the_bytes` | `?       ^     ^^^^^ ^^    ++        ^` |
| a hold made where no slip may lie in the masked words | `test_audio_arm_interplay_at_the_release_tolerance` | `+ ('FAIL', []) : void: a planted arm was missed` |
| unbalanced readings ranked with balanced ones | `test_audio_slip_totals_balance_the_bytes` | `AssertionError: "an unclassified corruption: no reading's slips sum to the shift the by...` |
| the balance guard never fires | `test_audio_slip_totals_balance_the_bytes` | `+  (3, 3000, 'unresolved', 1, '0x00080000', None)]` |
| unbalanced window recorded as its reading | `test_audio_slip_totals_balance_the_bytes` | `+  (3, 3000, 'unresolved', 1, '0x00080000', None)]` |
| unbalanced window reported at its resync | `test_audio_slip_totals_balance_the_bytes` | `(3, 3000, 'unresolved', 1, '0x00080000', None)]` |
| slips recorded outside the ledger | `test_audio_slip_totals_balance_the_bytes` | `-   {'class': 'repeated', 'index': 7742, 'n': 2}]) : void: a planted arm was missed` |
| an excursion's lead never returns at a word that fits | `test_audio_slip_totals_balance_the_bytes` | `Diff is 1323 characters long. Set self.maxDiff to None to see it.` |
| coincident words after a return keep the other offset | `test_audio_slip_totals_balance_the_bytes` | `(2, 4146, 'bit-flip', 1, '0x00080000', None)]` |
| no word beside a constant-mask excursion split off | `test_audio_constant_mask_beside_one_word_events` | `Diff is 1289 characters long. Set self.maxDiff to None to see it.` |
| a two-word excursion under two masks kept whole | `test_audio_composition_sweep` | `AssertionError: 0 != 1 : [{'capture_index': 699, 'class': 'bit-flip', 'n': 2, 'expected...` |
| a word beside a constant-mask excursion merged into it | `test_audio_constant_mask_beside_one_word_events` | `+  (2, 4080, 'bit-flip', 64, '0x00000100', None)]` |
| a constant-mask excursion before a slip read as slips | `test_audio_constant_mask_beside_one_word_events` | `(3, 4153, 'dropped', 3, None, None)]` |
| an excursion already on the slip's track read as one corruption | `test_audio_composition_sweep` | `: [{'capture_index': 15934, 'class': 'bit-flip', 'n': 2, 'expected': '0x001C8500', 'rec...` |
| a flip arm found in a run of any length | `test_audio_arm_interplay_at_the_release_tolerance` | `+ ('FAIL', []) : void: a planted arm was missed` |
| a slip arm split only at its exact index | `test_audio_arm_interplay_at_the_release_tolerance` | `+ ('FAIL', []) : void: a planted arm was missed` |

## Reviewer evidence rerun at `910d4b94` (scripts byte-identical to R699-4's manifest, 34 of 34)

The grader is the same at `4a460fc3`, `17a43ef2` and `910d4b94`; the later commits change self-test arms only.
The grader-only receipts below were run at the `4a460fc3` export and rerun at `910d4b94` byte-identical, timing
values aside (`receipts/final_head_identical.log`; `receipts/r699-4/final_head_identical.log` is the same check at
`17a43ef2`). The self-test-dependent ones were rerun at `910d4b94`: `transplant_round5_arms_final.log`,
`quick_named_mutants_final.log`, `r699-4/r4_reviewer_mutants_final.log` and `tripwire_final/`. The gate receipts
at the root of `receipts/` are from `910d4b94`.

R699-4 (`receipts/r699-4/`):

- `r4_net_sweep.py`: 7011 cases, 0 unbalanced (270 at `85da3e45`).
- `r4_regress_sweep.py`: 3744 cases, 0 deviations; against `4d69e192`, 0 regressed, 2579 improved.
- `r4_cf_full.py`: 256 cases, 0 deviations.
- `r4_probe.py`:
  - X 10/10, C 3375/3375 (924 deviations at `85da3e45`);
  - R: 22 deviations (27 at `85da3e45`), none new; one case moves from OK to INFO (R-3626, two -4096 slips 20 samples
    apart, still FAIL, inside the cluster limit).
- `r4_arm_corruption_sweep.py`: 156 placements not FAIL (175 before). `check_reviewer_voids.py` shows that they are
  exactly the two stated voids predicted from the bytes, each NOT RUN with only its arm missed.
- `r4_reviewer_mutants.py`: W03 and W07 killed; W02, W06, W08, W10 and W11 survive (S2, not adopted).

Earlier probes, unmodified:

- R699-3's and the round-2 probes (`receipts/r699-3/`, `receipts/r699-3_compare.log`) give logs byte-identical to
  R699-4's at `85da3e45`, apart from timing fields.
- R700-3's four probes give byte-identical JSON at `85da3e45` and `4a460fc3` (`receipts/r700-3/compare.log`), and
  at `910d4b94` (`receipts/final_head_identical.log`).

My sweeps (`receipts/sweeps/`):

- `arm_d4.py`: 3456 cases, 739 not exact against 795 at `85da3e45`, none new.
- `classify_arm.py`: every case's outcome matches its byte-predicted class (0 mismatches). Its labels map to the
  self-test's: X2 void-flip (40), X1 void-position (272), L1 neighbour (299), L2 first (352), E exact (2493).
- `located_after_arm.py`: identical to `85da3e45`. Its 28 slips located away from their sample are all the stated
  limit by bytes (`check_mirrored.py`).

Tripwire copy (`receipts/tripwire/`): no unbalanced reading and no guard firing in any of the above. The self-test trips only at
the balance arm, as designed (`selftest_check.log`).

## Gate table (exact head, never piped; `receipts/`)

| Command | rc | Result |
|---|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | 0 | 116 tests OK |
| `python3 -B tb/tools/torture_release_mutants.py` (background, polled) | 0 | `PASS: 289 mutations killed; source unchanged`, in 2 h 23 min with other jobs on the host (`receipts/release_mutants.log`) |
| `scripts/release_mutants_timed.py` on the `910d4b94` export (the driver's criteria, timed) | 0 | 289 killed, 0 survived, 0 invalid; slowest 288 s under six jobs; source unchanged. Run alone, that control takes 262 s at `85da3e45` and 272 s here (`receipts/slowest_control_old_vs_new.log`) |
| R699-4's `release_mutants_parallel.py` on the `17a43ef2` export (the driver's criteria) | 0 | 289 killed, 0 survived, 0 invalid; source unchanged |
| `cd tests && behave --no-capture -f plain` (rtl-fast bdd-conformance) | 0 | 14 features, 495 scenarios, 2286 steps (log hashed) |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | 0 | 176 scenarios, 665 steps |
| `docs_check.py` (pinned renderer) | 0 | 0 findings, 210 md + 1420 scrubbed files |
| `gen_toc.py --check` / `--verify-anchors` (pinned) | 0 / 0 | 149 pages / 538 fragment links |
| `check_em_dash.py --base origin/dev` (pinned) | 0 | 0 findings over 458 added lines in 5 pages |
| `check_doc_style.py` (pinned) | 0 | 23 documents OK |
| `check_doc_paths.py` (pinned) | 0 | 1065 cited paths resolve |
| `python3 -B scripts/check_py_idiom.py` | 0 | at every ratchet (514 modules) |
| `python3 -B scripts/check_feature_status.py` and `--self-test` | 0, 0 | 0 findings |
| `torture_campaign.py --coverage-by-area --areas soak,audio,power` | 0 | three areas complete |
| `torture_campaign.py --plan --areas soak,audio,power --json` | 0 | 17 steps (`receipts/plan.json`) |
| `git diff --check origin/dev HEAD`; `git diff --check`; porcelain | 0, 0, 0 | clean; porcelain empty |

The gates ran with `PYTHONDONTWRITEBYTECODE=1`, so no bytecode was written into the tree.

## Acceptance status (issue #396)

Unchanged from rounds 1 to 4. Items 1, 2 and 5 are met at the desk, and so is the desk half of item 4. Items 3 and 4
need the bench (part B), so the PR body says "Relates to #396".

## Open items and risks

- Two G1 shapes stay voids by design, stated exactly; a void blocks the release.
- Beside a planted flip arm, a slip of whole blocks may be read on the other side of the arm (28 of 7680 placements
  within 4 samples, unchanged from round 4). This is stated as a limit and pinned by bytes.
- The self-test now takes about 25 seconds idle (17 before); the release driver runs it once per control.
- Owner decision issuecomment-6409128703 (AECP REBOOT for the soft resets; sine-pair limits at baseline + 6 dB) is
  still not in the plan text, for the manager to route. `restore_bound_s = 30` stays provisional.
- Scratch outside the tree: the stopped mutant runs' temporary copies were removed. Older `release-controls-*`
  directories predate this session and were left alone.

## Receipts

`receipts/INDEX.md` is generated from the files present (name, bytes, SHA-256). The scripts that produced receipts
are in `scripts/`. Logs over 200 KB are replaced by their SHA-256 and a summary.
