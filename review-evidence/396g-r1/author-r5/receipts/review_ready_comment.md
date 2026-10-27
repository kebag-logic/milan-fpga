[A674e] REVIEW READY - round 5
Commit: `910d4b94c4d5334b1869f42e9653c308a15d0dba` (tree `07ce568e5a407531407917c5e8f81d524cd09947`), branch `396-release-gate-plan`.
Three round-5 commits sit on the round-4 head `85da3e4595871c1573c28b4d040b9e98463a41c9`, which is not rewritten:

- `4a460fc3`, the grader, its arms, the controls and the documents;
- `17a43ef2`, one more pin (S3);
- `910d4b94`, the two sweeps fail fast.

The first serial driver run, at `17a43ef2`, timed out on one control whose sweeps failed slowly, about 420 s.
The sweeps now check a clean capture first and stop at their first failing case.

Base is dev `e76a755a`. Not pushed.

Changed (answers R699-4 under issuecomment-6424374359):
- **G3, by the invariant.**
  - The unbalanced readings all came from the hold. It judged the masked run against offset 0 while the reading had already recorded a slip before it.
  - The hold now sits at the offset in force where the masked run begins: the opening offset or one the reading reaches, whichever leaves the longest run.
  - A recorded part that does not end on that offset is read again with the masked words restored.
  - The invariant is explicit. A reading whose slips do not sum to the shift the closing samples decode ranks behind every reading that does.
  - A per-channel ledger checks every window. Where no reading balances, the window is one `unresolved` event at its first sample, never a slip that did not happen.
  - The 44 regressions had a second cause, a coincident word that kept a code-bit excursion's offset. The excursion now returns at the first word that fits the offset in force, after a lead under one mask that no single whole-block offset explains.
- **G2.**
  - The slip before is resolved by item 1's construction.
  - A word at either end, off the mask of an excursion that no single offset explains, is its own one-word event.
  - A constant-mask excursion that ends in a slip is one bit-flip and that slip, where no single offset explains its words.
  - No exception remains.
- **G1.**
  - Fixed where one rule covers it: each word of a two-word excursion under two masks that no single offset explains is its own corruption, so a corruption beside a flip arm is graded beside it.
  - The rest is stated exactly, by the ruling's second option. Two voids remain, and a void blocks the release:
    - a corrupted word on a slip arm's own sample, or the one before it, that is its channel's word at another position at most half a block from the old or the new track's;
    - a corruption of a flip arm's own word on its channel, or of the word beside it under the arm's own mask.
  - One limit is bit-identical: a corruption on a slip arm's own sample or the next one may read first, the slip after it within the tolerance.
  - TESTING 6d, REQ-VER-06 and `counter_limits` state them, and narrow "either order" and "never hides".
- **The sweeps are gates.**
  - `test_audio_composition_sweep`: a corruption 0 to 4 samples from each arm, every channel, eight mask classes, 8192 and 16384 frames, tolerance 2; 3456 cases.
  - `test_audio_slip_before_a_constant_mask`: the reviewer's grid, 750 cases.
  - Each case is checked against the class its bytes decide, and every reading balances.
- **G4:** `test_audio_arm_interplay_at_the_release_tolerance` kills W03 and W07.
- **R1** as written.
- S1 and S2 are not adopted, with reasons in the PR body. S3 is adopted: a DUT slip also pins the interrupted-excursion limit.
- A further limit, found while sweeping and unchanged since round 4, is stated and pinned by bytes. Beside a flip arm, a slip of whole blocks may read on the other side of the arm, with the arm's code bit one sample over: 28 of 7680 placements.

Validation, at this head, foreground except the driver, all rc 0:

| Command | Result |
|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | 116 tests OK (112 before) |
| `python3 -B tb/tools/torture_release_mutants.py` | `PASS: 289 mutations killed; source unchanged` (18 added; 7 re-anchored, 1 adjusted) |
| The same 289 controls in parallel, timed (`scripts/release_mutants_timed.py`) | 289 killed; the slowest self-test takes 288 s under six jobs, against the driver's 600 |
| `cd tests && behave --no-capture -f plain` | 495 scenarios, 2286 steps |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain` | 176 scenarios |
| `docs_check.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base origin/dev`, `check_doc_style.py`, `check_doc_paths.py` under the pinned renderer | 0 findings |
| `check_py_idiom.py`; `check_feature_status.py` and `--self-test` | at ratchets; 0 findings |
| `--coverage-by-area --areas soak,audio,power`; `git diff --check origin/dev HEAD` | complete; clean |

The new arms fail on `85da3e45`, by transplant:

- the composition sweep, at its first case (28 of 288 captures in the subtest form of `4a460fc3`);
- the slip-before sweep, at its first case (100 of 150);
- the balance arm, six shapes and the guard;
- the extended adjacency arm, 8 subtests.

The interplay arm targets the mutants.

R699-4's probes, rerun unmodified (34 scripts byte-identical to its manifest):
- `r4_net_sweep.py`: 0 unbalanced of 7011 (270 before).
- `r4_regress_sweep.py`: 0 deviations of 3744; against `4d69e192`, 0 regressed.
- `r4_cf_full.py`: 0 of 256.
- `r4_probe.py`: X 10/10, C 3375/3375 (924 deviations before), R 22 deviations (27 before, none new).
- `r4_arm_corruption_sweep.py`: 156 not FAIL (175 before). They are exactly the two stated voids predicted from the bytes, each NOT RUN with only its arm missed. R-4857 falls in the first.
- `r4_reviewer_mutants.py`: W03 and W07 killed; W02, W06, W08, W10 and W11 change no verdict in any sweep.

STOP check, not met:
- Against `85da3e45`, the seeded fuzz changes five verdicts, all NOT RUN to FAIL.
- All five are a corruption on channel 1 one sample beside the flip arm, a swept shape.
- R699-3's, round-2 and R700-3's probes give output identical to `85da3e45`, timing fields aside.

A tripwire copy raises on any unbalanced reading or on the guard firing. Every probe and sweep above runs clean against it.

Acceptance criteria: unchanged. Items 1, 2 and 5 and the desk half of item 4 are met. Items 3 and 4 need the bench (part B), so the body says "Relates to #396".

Open risks/questions:
- Two voids beside planted arms stay, stated exactly; a void blocks the release.
- The self-test now takes about 25 seconds idle, and the serial driver about two and a half hours on a shared host.
- Owner decision issuecomment-6409128703 is still outside the plan text, and `restore_bound_s = 30` stays provisional, both for the manager to route.

HANDOFF.md and PR-BODY.md (with a Round 5 section) are in the assigned output directory, with the scripts and the receipts and their generated index. No push, PR operation, merge, hardware or bench action.
