[R748] POSITIVE - exact head 50e5d08dda6e89cf010a740cea5cf4539807db01

External cleared-context review, round R748-2, of kebag-logic/milan-fpga PR #820 for issue #818. This is a delta review over the round-1 head `32f0d9b5425a8526ac9d39e5913c01944c36e4d0`.
Head `50e5d08dda6e89cf010a740cea5cf4539807db01`, tree `3a555c98c488102e1ef4c62f06f2acc1a27445b7`, source base dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`.
The delta is two commits (`fda977a3`, `50e5d08d`) and six files: `syn/ooc/pp_resource_gate.py`, `pp_resource_gate_mutants.py`, `pp_resource_gate_set_selftest.py`, `docs/design/AREA_BUDGET.md`, `docs/design/MARK_II_AREA_PLAN.md` and `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`.
Authority, unchanged from round 1:
- the #818 body (frozen acceptance) and rule 1 of the ruling at #814 issuecomment-6522621984: "The fall from the record is still computed and published, but as a warning";
- the build floor in `docs/integration/BUILDING.md` section 5;
- the recipe's comparison snippet.

Verdict: POSITIVE. All four round-1 findings (F1, F2, F3 and R1) are resolved at their cause, and each was verified by execution at this head.
This round raises no BLOCKER, MAJOR or MINOR. It records one RESIDUE in the PR body (R2) and retains one optional SUGGESTION (S1).
Every lens is covered clean at this head.

## Round-1 findings, resolved at this head

### F1 (MINOR Docs, RTL): RESOLVED. The Mark II mapping record now exits 0

The fix is at `docs/design/MARK_II_AREA_PLAN.md:1340-1346`. The `record` line (1345-1346) now carries `--shipping-selection`. Line 1341 gives the reason: the map reads one routed checkpoint.
The probe extracts the `cp` and `record` lines verbatim from the doc's fenced block, from the file at head (`receipts/r2-probes/f1-documented-lines.txt`). It runs them from the clone root with `$WORK` set to a byte-verified copy of dev `1e80128f`'s recorded route set:
- the record exits 0 and stores ExtraPostPlacementOpt at WNS 0.303 (`f1-mark2-record.log`);
- a marked check against that scratch record exits 0 (`f1-mark2-recheck.log`);
- the same record without the mark still exits 2 (`f1-mark2-unmarked-refused.log`), so the doc fix and not a relaxed interface is what makes it pass.

Every other gate invocation in the tree names a set or the mark. That covers the recipe at `PP_SHADOW_BASELINE_RECIPE.md:573-574` and `:626-627`, and the usage text at `pp_resource_gate.py:63`. `MARK_II_AREA_PLAN.md` lines 173 and 1459 cite historical runs.

### F2 (MINOR Conformance, Docs, Tests): RESOLVED. The fall WARNING now prints beside a floor failure

`verdict_for()` at `syn/ooc/pp_resource_gate.py:566-581` builds the floor note and then appends the fall note independently.
- It returns `"; ".join(notes) or "ok", not missed`, so the exit status still depends on the floor alone.
- `judge()` at `:537` keys the summary line on `"WARNING: fell"`, so the summary line also follows a combined verdict.

Real-route plants on dev's recorded set (`receipts/r2-probes/`), each with exit 1:

| Plant | Printed |
|---|---|
| every route's WNS below the 0.03 floor at Slow_0C and Slow_85C, with a fall of 0.42 ns (`f2-wns-floor-and-fall.log`) | `WNS_ns 0.44 0.02 -0.42 REGRESSION: below the floor 0.03 at Slow_0C, Slow_85C; WARNING: fell by more than 0.25 from the record`, then `WARNING: WNS_ns fell from the record ...` and `RESULT: MATERIAL REGRESSION` |
| the round-1 reproduction, one corner only (`f2-wns-one-corner.log`) | `at Slow_85C; WARNING: ...` and the summary WARNING. Round 1 printed 0 WARNING lines on this plant |
| WHS -0.300 at the fast corners, a fall of 0.336 ns (`f2-whs-floor-and-fall.log`) | both notes for WHS and the summary line |
| WHS -0.010, a fall of 0.046 ns, within the timing fall (`f2-whs-floor-no-fall.log`) | the REGRESSION and no WARNING, the negative case |
| the same notes on a marked single route (`f2-wns-marked-alone.log`, `f2-whs-marked-alone.log`) | the same notes, exit 1 |

The fall alone still never fails:
- arm `WNS fell more than the timing fall: a warning, never a failure`;
- campaign mutant `a fall never fails`, rewritten to `not notes`, is killed by that arm;
- round 1's `large-fall` real-route probe passes (exit 0, WARNING; `receipts/route-probes/large-fall.log`).

The docs now say so:
- `AREA_BUDGET.md:442`: "prints a WARNING, also beside a floor failure, and never fails";
- `PP_SHADOW_BASELINE_RECIPE.md:588`: "also beside a floor failure; the fall alone never fails".

`BUILDING.md:578` ("A fall from the gate's record is printed as a warning, never a failure") was unconditional in round 1 and is now true without qualification, so it needed no change.

The new arms are at `pp_resource_gate_set_selftest.py:73-79` and `:95-99`: WNS and WHS, each with a fall beyond the timing fall and one within it.
- `fall warned beside a floor miss` is killed by the WNS "both reported" arm.
- `fall warning summarized beside a floor miss` is killed by the same arm.

### F3 (MINOR Tests): RESOLVED. The safety direction of the corner-agreement guard is now pinned

The guard at `pp_resource_gate.py:401` (`if worst != figures[figure]`, in `corners()` at `:387-404`) is unchanged and already two-way. The new arms at `pp_resource_gate_set_selftest.py:106-109` plant a timing summary below every corner report and under the floor: WNS 0.01 and WHS -0.05. Both require exit 2 with the exact disagreement text.

Campaign mutants:
- `corners agree in both directions` (`worst < figures[figure]`, round 1's X5) is killed by the arm "the summary's WNS below every corner's, under the floor";
- `corners agree in the other direction` is killed by the round-1 arm "a corner's WNS below the summary's".

Two extra mutants of mine pin the WHS arm separately. Each weakens the guard to one way for one slack only:
- Y1 (WHS) is killed by the arm "the summary's WHS below every corner's";
- Y2 (WNS) is killed by the WNS arm.

So each slack's safety direction has its own killing arm.

Real routes, all exit 2 with `the reports are not of one run` (`receipts/r2-probes/f3-*.log`):
- every summary at WNS 0.010 beside the recorded corners: "worst WNS_ns is 0.303 and the timing summary's 0.01";
- the shipping summary at WHS -0.050: "0.028 ... -0.05", in a set and on a marked route;
- a corner below the summary, for WNS and for WHS.

### R1 (RESIDUE, PR body): RESOLVED

The Status bullet reads: of 44 new and 11 rewritten mutants (9 changed edits; `timing fall` and `timing fall boundary` under rewritten arms), 54 are killed by a named arm or check and `every corner model read` by the fixture record's refusal. Both halves were checked against the code:
- Against dev `1e80128f`, the mutant table delta is 192 to 236: 44 added, 0 removed, 9 changed edits (`receipts/mutant-delta-dev.json`).
- Attribution of all 55 at head (`receipts/mutant-attribution-pr.tsv`): 54 are killed by a named `AssertionError` arm. `every corner model read` is killed by `Refusal: the signoff corners' worst WHS_ns is 0.2 and the timing summary's 0.1`, before the arms run.
- `a single route selected alone` is killed by the command-line arm `check reads the kind from a standalone directory`. Its assertion message spans two lines. This round's attribution script reads the `AssertionError` line itself, where round 1's classifier read the last error-looking line.

## New findings at this head

### R2 RESIDUE - PR #820 body, the file table under "Description": stale arm and mutant counts

Evidence:
- The row for `syn/ooc/pp_resource_gate_set_selftest.py (new)` says "21 timing arms ... 29 route-set arms". At head, `timing_arms()` returns 27 and `set_arms_table()` returns 31. The round-1 head had 21 and 29; round 2 added 4 F2 arms, 2 F3 arms and 2 S1 arms.
- The row for `syn/ooc/pp_resource_gate_mutants.py` says "38 new mutants, 11 rewritten to the new code". Against dev it is 44 new and 9 changed edits.

The Status section of the same body carries the correct totals (312 arms, 236 mutants, 44 new and 11 rewritten). The self-test, the campaign and every verdict are unaffected, so the defect is wording only.

Exact fix:
- the first row: "27 timing arms on one route's corners, 31 route-set arms through `main()` (the issue's four cases among them), 2 standalone refusals and the set's re-record";
- the second row: "44 new mutants; 9 existing edits rewritten to the new code (`timing fall` and `timing fall boundary` keep their edits under rewritten arms)".

### S1 SUGGESTION Tests - syn/ooc/pp_resource_gate.py `bound()` shipping-script precondition - four sub-conditions without an arm (retained from R748-1)

The ceiling half of round-1 S1 is done:
- the set arms "a selected comparison is judged on the BRAM tile ceiling" and "a route not selected is not judged on the BRAM tile ceiling" (`pp_resource_gate_set_selftest.py:156-160`);
- mutants `ceiling judged on the selected route` and `ceiling not judged on a route not selected`, each killed by its arm;
- my extra ceiling-boundary mutant Y8 (`>=`), killed by `BRAM tiles at the ceiling`;
- real routes: BRAM tile 130 on the selected AltSpreadLogic_high route exits 1 with `BRAM_TILE  REGRESSION: 130 exceeds the ceiling 121.5`. On the non-selected shipping route it exits 0 with no ceiling line (`receipts/r2-probes/s1-*.log`).

The four `bound()` sub-conditions stay unarmed, as the PR's Known limitations states. Each is redundant with a later check. This stays optional.

## Checks of the brief

1. **Mark II record command on a recorded set:** exit 0, see F1.
2. **Floor miss with a fall beyond tolerance:** both notes print, the summary WARNING prints and the exit is 1, for WNS and WHS, in a set and on a marked route. See F2.
3. **Summary worst corner disagreeing with the corner reports, both directions:** exit 2 for WNS and WHS in each direction, see F3.
4. **Self-test and mutant runner** (`scripts/run_gate_suites.sh`, `receipts/suites/`):
   - `--selftest`: rc 0, `resource gate selftest: 312 arms and 500 generated cases PASS`, and the placement controls PASS;
   - `check-baseline`: rc 0, `baseline PASS: 3 endpoints`;
   - campaign at 16 workers: rc 0, `resource gate mutants: control passes, all 236 mutants fail`;
   - the 9 round-2 mutants (6 added, 3 changed; `receipts/mutant-delta-round1.json`) and `timing fall`/`timing fall boundary` are each killed by a named arm (`receipts/mutant-attribution-r2.tsv`).

   Nine extra mutants Y1-Y9 aimed at the delta (`scripts/r2_extra_mutants.json`): 8 are killed by named arms. Y6 survives and is an equivalent mutant: it keys the summary on any `"WARNING"` in a verdict, and the fall note is the only WARNING a verdict can hold.

   The extras cover:
   - each slack's guard weakened to one way (Y1, Y2);
   - the hold-only guard loop (Y3);
   - the floor note dropped beside a fall (Y4);
   - the notes in the other order (Y5);
   - a floor miss passing when it also fell (Y7);
   - the ceiling boundary (Y8);
   - the warning only beside a floor miss (Y9).
5. **Recorded route sets: verdicts unchanged from round 1.** `scripts/recorded_sets.sh` ran the round-1 gate (`32f0d9b5`, extracted by `git archive`) and the head gate on six recorded sets, 28 runs each:
   - #814's dev, head and control sets;
   - #806 `cf3ef596`, with its comparisons in the sibling `806-a701b`, which open the shipping checkpoint;
   - #787 `a0e555a7`;
   - #817, whose shipping route alone was recorded and is judged marked.

   All 28 head logs are byte-identical to the round-1 head's (`receipts/recorded-head-50e5d08d/`, `receipts/recorded-32f0d9b5/`). The 15 logs for the #814 sets are also byte-identical to my R748-1 receipts. After path normalisation they match the author's 15 published round-2 logs (`receipts/author-after-compare.txt`). The 93 #814 route report files match the author's `route-reports.tsv` (`receipts/routes/verify.txt`).

   | Set | Exit | Selected | Notes |
   |---|---|---|---|
   | dev `1e80128f` | 0 | ExtraPostPlacementOpt, +0.303 ns | no WARNING |
   | #814 head `8b28ebaf` | 0 | ExtraPostPlacementOpt, +0.128 | WARNING (fell 0.312) |
   | #814 control | 0 | AltSpreadLogic_high, +0.342 | |
   | #806 `cf3ef596` | 0 | AltSpreadLogic_high, +0.235 | |
   | #787 `a0e555a7` | 0 | AltSpreadLogic_high, +0.193 | |
   | #817 (marked) | 0 | shipping route | WARNING (fell 0.274) |

   In every set, the unmarked lone route exits 2 and the set record names the selected directive.
6. **Round 1's 28 real-route probes at head:** 28 PASS (`receipts/route-probes/results.json`). This round's 16 probes: 16 PASS (`receipts/r2-probes/results.json`).
7. **Comment rule and style:** the only comment added in the delta is `# The fall is published whatever the floor verdict.` (`pp_resource_gate.py:576`). It states the behaviour, sits under the existing `#818` reason line and has no lane label, round, reviewer ID or comment ID. The delta adds no em-dash. Docs and idiom gates all rc 0 (`receipts/docs/`):
   - `docs_check.py`: 0 findings;
   - `check_doc_style.py`: OK;
   - `check_doc_paths.py`: 1071 paths resolve;
   - `check_py_idiom.py`: within every ratchet.
8. **Author evidence:** `review-evidence/818-r1/MANIFEST.json` at `75d730df` checks out:
   - 465 entries, every published sha256 matches its blob, and no tree file is unlisted (`receipts/evidence-manifest-verify.txt`);
   - the archive commit itself carries no signature (`%G?` = N), so the integrity check is the manifest;
   - the author's gate receipts end on the same lines as mine (312 arms, 236 mutants, 3 endpoints);
   - the docs replica `all.rc` is 0, and the rtl-fast replica table reports rc 0 for `changes`, `bdd-conformance` and `yosys-elaboration` over base `1e80128f`. Those replicas are the author's, not mine.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `syn/ooc/pp_resource_gate.py:502-581` (`judge()`, `verdict_for()`) against #818 and #814 rule 1 (fall published as a WARNING, never failing; floors per corner); real-route verdicts `receipts/r2-probes/f2-*.log`, `receipts/route-probes/large-fall.log`; six recorded sets `receipts/recorded-head-50e5d08d/*` | R748-2 | 50e5d08dda6e89cf010a740cea5cf4539807db01 |
| RTL | CLEAN | no HDL in the PR; the gate's CLI and record interface (`pp_resource_gate.py:57-66`) against every invocation in the tree: recipe `:573-574`, `:626-627`; `MARK_II_AREA_PLAN.md:1344-1346` run verbatim (`receipts/r2-probes/f1-*.log`); the delta does not touch `.github/workflows/rtl-fast.yml` or `scripts/ci_events.py` (covered in R748-1) | R748-2 | 50e5d08dda6e89cf010a740cea5cf4539807db01 |
| Robustness | CLEAN | `corners()` guard `pp_resource_gate.py:387-404` in both directions for both slacks on real-route copies (`receipts/r2-probes/f3-*.log`); combined floor-and-fall verdict on sets and marked routes; ceiling on selected vs not-selected route (`s1-*.log`); round 1's 28 refusal and selection probes re-run (`receipts/route-probes/`) | R748-2 | 50e5d08dda6e89cf010a740cea5cf4539807db01 |
| Tests | CLEAN | `syn/ooc/pp_resource_gate_set_selftest.py:73-79,95-109,156-160`; the round-2 entries of `pp_resource_gate_mutants.py`; `receipts/suites/*` (312 arms, 236 of 236 mutants killed); `receipts/mutant-attribution-r2.tsv` (11 delta mutants and 9 extras), `receipts/mutant-attribution-pr.tsv` (all 55 PR mutants) | R748-2 | 50e5d08dda6e89cf010a740cea5cf4539807db01 |
| Docs | CLEAN (R2 RESIDUE carried) | `docs/design/AREA_BUDGET.md:436-446`, `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:572-592,625-628`, `docs/design/MARK_II_AREA_PLAN.md:1336-1352`, `docs/integration/BUILDING.md:578`; PR #820 body; docs gates `receipts/docs/*` | R748-2 | 50e5d08dda6e89cf010a740cea5cf4539807db01 |

## Executed evidence (this review, at the exact head)

The scripts are in `scripts/` and the receipts in `receipts/`:
- `run_gate_suites.sh`: self-test, check-baseline and the mutant campaign capped at 16 workers;
- `recorded_sets.sh`: six recorded sets under the round-1 and head gates, at most 8 concurrent runs;
- `route_probes.py`: round 1's 28 probes;
- `r2_probes.py`: this round's 16 F1, F2, F3 and S1 probes on byte-verified copies of real routes;
- `mutant_delta.py` and `mutant_attrib.py`: mutant tables and attribution, with `r2_delta.json` and `r2_extra_mutants.json`;
- `verify_routes.py`: the route bytes.

Clone state after the probes (`receipts/clone-state.txt`):
- HEAD is `50e5d08d`, with a clean worktree and index, and `git ls-files -s` equals the head tree's blobs and modes;
- the gitlinks are protocol-processor `f65c8ff7`, gptp-processor `f97c1803` and third_party/verilog-axis `48ff7a7e`, all checked out clean;
- an ignored `syn/ooc/__pycache__` created by this review's imports was removed, leaving 0 untracked or ignored entries.

## Real limits

- No Vivado route was run. The verdicts use the routes that #814, #806, #787 and #817 recorded. The Mark II map step (Vivado) was not run, only its `cp` and `record` lines.
- L1 and L2 from R748-1 stand unchanged: a stale comparison directory, and a trust-based `--shipping-selection`. The delta does not touch either.
- `gen_toc.py --verify-anchors` and `--check` did not run here, because the pinned Markdown renderer is not installed. The author's docs replica reports them green.
- Hosted contexts were not inspected. No act or Docker run, no manager source bank. Physical calibration NOT RUN; no hardware claim.

## Pending manager duties

- Build and validate the current-dev merge candidate (live dev `56df0894`) with the builder and native banks at the merge turn, and own hosted/act acceptance of this exact head.
- Carry R2 to the residue checklist.

## Prior public review findings (read after the verdict and ledger above were on disk)

What was read:
- PR #820's issue comments: the review-start notices, R747-1 (POSITIVE at `32f0d9b5`, issuecomment-6526254031), my own R748-1 (NEGATIVE at `32f0d9b5`) and R747-2 (POSITIVE at this head, issuecomment-6532577953);
- the PR's reviews and review comments: none;
- #818's comments: the executor's TAKEN and REVIEW READY for both rounds, and the manager's round-2 brief (issuecomment-6529748129).

None of them records a decision that changes the warning rule or the scope of the interface.

| Prior finding | At this head | Basis |
|---|---|---|
| R748-1 F1 MINOR, Docs and RTL | RESOLVED | F1 above. The manager's brief asked for "the route-set form". The author used `--shipping-selection` instead, which was the other outcome R748-1 accepted. The PR's Known limitations gives the reason publicly: the map reads one routed checkpoint. |
| R748-1 F2 MINOR, Conformance, Docs and Tests | RESOLVED | F2 above |
| R748-1 F3 MINOR, Tests | RESOLVED | F3 above |
| R748-1 R1 RESIDUE | RESOLVED | R1 above |
| R748-1 S1 SUGGESTION | ceiling part RESOLVED; the `bound()` part RETAINED, optional | S1 above |
| R747-1 three SUGGESTIONs: fuzz on marked routes only; hold not in the selection; fresh comparison directories | RETAINED, optional | The delta does not touch `run_case`, `best()` or the recipe's fresh-directory text |
| R747-2 RS1 RESIDUE: the PR body sentence "Round 2 mutants, each killed by the arm written for it" | RETAINED as RESIDUE (concur) | My own attribution (F3 above, `receipts/mutant-attribution-r2.tsv`) shows `corners agree in the other direction` is killed by the round-1 arm `a corner's WNS below the summary's`. Only the sentence is loose; R747-2's exact fix stands. |

R747-2 and this round agree at this head: both are POSITIVE, with no BLOCKER, MAJOR or MINOR. The residue they each carry is in the PR body and does not overlap:
- R2 here: stale counts in the file table;
- RS1 there: the attribution sentence.

Residue checklist for the manager: R2 (this report) and RS1 (R747-2).

R748-2 FINISHED
