[R747] POSITIVE - exact head 50e5d08dda6e89cf010a740cea5cf4539807db01

# R747-2: internal cleared-context review of PR #820 (#818), round 2

- **Head:** `50e5d08dda6e89cf010a740cea5cf4539807db01`, tree `3a555c98c488102e1ef4c62f06f2acc1a27445b7`.
- **Bases:** round-1 head `32f0d9b5425a8526ac9d39e5913c01944c36e4d0`; source base `1e80128f0a467b58bf884b7d9bf62e013a2fb141`.
- **PR metadata** (`receipts/pr820.json`): this head, base `dev` at `1e80128f`, four commits.
- **Scope:** a delta review, `git diff 32f0d9b5..50e5d08d` (`receipts/delta.diff`). It covers 6 files, +49/-12, in two commits:
  - `fda977a3`, the gate, the arms and the mutants;
  - `50e5d08d`, three doc sentences.

  Code the delta does not touch keeps its round-1 verdict (R747-1 at `32f0d9b5`, all five lenses CLEAN), unless the delta changes something it depends on. I checked that dependency with the route-set, fuzz and campaign reruns below.
- **Findings resolved here:** R748-1 F1, F2, F3 and R1, plus S1, which the author chose to address.
- **Authorities:**
  - the #818 body (`receipts/issue818.json`);
  - rule 1 of the #814 ruling, as read in R747-1;
  - the round-2 instruction on #818 (issuecomment-6529748129), and the author's TAKEN and REVIEW READY for round 2 (`receipts/issue818-comments.json`);
  - `docs/integration/BUILDING.md` section 5, `docs/design/AREA_BUDGET.md` "The resource gate", the recipe, and `syn/resmap/resmap_map.py` (the mapper's tie to the record).
- **Public evidence read:** the author's round-2 receipts index at `75d730df` `review-evidence/818-r1/author-r2/` (`INDEX.md` and `route-reports.tsv`; the digest matches the index). I read it as evidence, not proof. I re-ran every claim I rely on.
- **Isolation:** until this verdict and ledger were on disk, I fetched PR data only through the two allowed calls, and read only my own round-1 report and the R748-1 findings named in the brief. I read no other reviewer's packet or report.

## Verdict basis

1. **F2: a fall WARNING now prints beside a floor failure, and the exit stays 1. RESOLVED.**
   - Code: `verdict_for()` (`syn/ooc/pp_resource_gate.py:566-581`) builds the floor note and the fall note independently and joins them. Its `ok` is `not missed`, so the fall still never decides the status. `judge()` (`:537`) now collects a warned figure by `"WARNING: fell" in verdict`, so the summary WARNING line follows a joined verdict.
   - Real-route probes on a copy of dev `1e80128f`'s recorded set (`receipts/probes/round2-probes.tsv`, `logs/`):

     | Probe | Exit | Output |
     |---|---|---|
     | Every route below the setup floor; selected ExtraPostPlacementOpt at 0.020, a 0.42 fall | 1 | `REGRESSION: below the floor 0.03 at Slow_0C; WARNING: fell by more than 0.25 from the record`, then `WARNING: WNS_ns fell from the record ...`, then `RESULT: MATERIAL REGRESSION` |
     | Selected WHS -0.300 at Fast_85C, a 0.336 fall | 1 | the WHS REGRESSION and the WARNING together, and the WHS summary WARNING |
     | Selected WHS -0.005, a 0.041 fall within the 0.25 column | 1 | the REGRESSION only, no WARNING |

   - The same probes against the round-1 gate print the REGRESSION only (`receipts/probes-r1/`). The probe tells the two gates apart.
2. **F3: the corner-agreement guard is now tested in its safety direction. RESOLVED.**
   - New arms, both exit 2 naming the disagreement:
     - `the summary's WNS below every corner's, under the floor` (`pp_resource_gate_set_selftest.py:106`);
     - `the summary's WHS below every corner's, under the floor` (`:108`).
   - The one-way mutant `corners agree in both directions` (`worst < summary`) is killed by the WNS arm (`receipts/named-kills.tsv`).
   - My own split mutants are killed by the matching arm (`receipts/extra-mutants.tsv`):
     - Y6, one-way for WHS only, by the WHS arm. That arm is not vacuous.
     - Y7, one-way for WNS only, by the WNS arm.
   - Real-route probes, each exit 2 with `the reports are not of one run`:
     - all three summaries at WNS 0.010 (F3-a);
     - only the selected route's summary (F3-b);
     - the selected summary at WHS -0.050 (F3-c);
     - a comparison's summary (F3-f);
     - the other direction, a corner below the summary, for WNS and for WHS (F3-d, F3-e).
3. **F1: the documented Mark II record command runs. RESOLVED.**
   - Commands: the `cp` and `record` lines, extracted verbatim from `docs/design/MARK_II_AREA_PLAN.md:1343-1346` (`receipts/f1/documented-lines.sh`), with `$WORK/ax7101` pointing at dev's recorded shipping route.
   - Results (`receipts/f1/`):
     - the documented lines exit 0;
     - a check against the scratch record exits 0;
     - the round-1 documented form exits 2 at this head;
     - the tracked baseline is byte-unchanged.
   - Why the mark is right here, though #818's round-2 instruction said "route-set form": `resmap_map.py map` ties the map of `$WORK/ax7101/gateware/alinx_ax7101_route.dcp` to the record's figures (`resmap_map.py:42-45,489-499`). A set record stores the selected directive's figures. When that directive is not the shipping one, the map's tie would fail.
   - So the one-route mark is the form that keeps the map tied to its checkpoint. That is one of the two outcomes R748-1 F1 allowed, and the new sentence at `:1341` gives the reason. The PR body publishes this choice, so I raise no finding.
4. **R1: the PR body's mutant claim is now exact. RESOLVED.**
   - Counted by `scripts/mutant_delta.py` (`receipts/mutant-delta-dev-head.txt`): dev has 192 mutants and this head 236, so 44 were added and none removed, with 9 edits changed. That matches "44 new and 11 rewritten (9 changed edits; `timing fall` and `timing fall boundary` keep their edits under rewritten arms)".
   - Every SET_MUTANTS and MUTANTS entry is killed (209 of 209 rc=1, `receipts/named-kills.tsv`). `every corner model read` is killed by the fixture record's refusal, as the body says.
   - One new attribution sentence is inexact; it is RS1 below.
5. **S1 (optional in R748-1): the BRAM tile ceiling is pinned to the selected route.**
   - `ceiling judged on the selected route` is killed by `a selected comparison is judged on the BRAM tile ceiling` (`:156`).
   - `ceiling not judged on a route not selected` is killed by `a route not selected is not judged on the BRAM tile ceiling` (`:159`).
   - The `bound()` sub-conditions stay unarmed. The PR body says so, with the redundancy argument.
6. **Mutant kills: every mutant is killed, and each round-2 mutant by the arm written for it.**
   - Campaign at head: `control passes, all 236 mutants fail`, rc 0 (`receipts/gates/mutants.log`).
   - Round-2 and rewritten mutants, by killing arm (`receipts/named-kills.tsv`):
     - `fall warned beside a floor miss` and `fall warning summarized beside a floor miss`: the WNS "both reported" arm;
     - `timing floor`: `WNS below the floor`;
     - `floor names its corners`: `WNS below the floor`;
     - `a fall never fails`: the fall-warning arm;
     - `corners agree in the other direction`: the pre-existing `a corner's WNS below the summary's` (RS1).
   - Eight reviewer mutants of the delta are all killed by the intended arm (`receipts/extra-mutants.tsv`):
     - Y1 and Y2, the warning suppressed for one figure only;
     - Y3, the warning printed for any floor miss, killed by `... within the timing fall: no warning`;
     - Y4, the notes reversed;
     - Y5, the summary line dropping a figure warned beside a floor miss;
     - Y6 and Y7, the one-way guards per figure;
     - Y8, a floor miss passing when a fall is also warned.
7. **The recorded routes' verdicts are unchanged.**
   - Bytes: the 93 recorded report files of the dev, #814 head and #814 control sets match the author's published `route-reports.tsv`, before and after the probes (`receipts/routes-verify*.txt`).
   - Runs: the round-1 gate (`32f0d9b5`) and this head's gate, each extracted by `git archive`, on six recorded sets (`scripts/run_routes.sh`), 33 runs per gate:
     - for each set: set check, reversed order, set record, marked, unmarked, marked record;
     - for the #817 route, which has no comparisons: marked, unmarked, marked record.
   - The two gates' exit codes match on all 33 runs, and every log is byte-identical between them (`receipts/routes-r1/`, `receipts/routes-head/`). Every set check exits 0 and every unmarked route exits 2:

     | Set | Selected directive | Worst-corner WNS | Note |
     |---|---|---|---|
     | dev | ExtraPostPlacementOpt | +0.303 | |
     | #814 head | ExtraPostPlacementOpt | +0.128 | WARNING, 0.312 fall |
     | #814 control | AltSpreadLogic_high | +0.342 | |
     | #806 | AltSpreadLogic_high | +0.235 | |
     | #787 | AltSpreadLogic_high | +0.193 | |
     | #817, marked | (one route) | +0.166 | WARNING, 0.274 fall |

   - The generated exit-code campaign on dev's real route, 400 cases at seed 747, gives 0 failures. Its log is byte-identical to the round-1 receipt (`receipts/fuzz-dev-400.log`).
8. **Self-test and audit.**
   - `--selftest` rc 0: `312 arms and 500 generated cases PASS`, placement gate PASS. All 8 new arms PASS (`receipts/gates/selftest.log`).
   - `check-baseline` rc 0: `baseline PASS: 3 endpoints`.

## Findings

No BLOCKER, MAJOR or MINOR.

**RS1 RESIDUE (Docs) - PR #820 body, "Round 2 mutants, each killed by the arm written for it" - one attribution is to a pre-existing arm**
- Evidence: `corners agree in the other direction` (`worst > summary`) is killed by the round-1 arm `a corner's WNS below the summary's`, not by a round-2 arm (`receipts/named-kills.tsv`). The kill is real. Only the sentence is loose, and it changes no test, figure or verdict.
- Exact fix: "... each killed by the arm written for it, except `corners agree in the other direction`, which the existing arm `a corner's WNS below the summary's` kills".

**Retained SUGGESTIONs (optional, unchanged by the delta):**
- R747-1, Tests, `syn/ooc/pp_resource_gate.py` `run_case`: generated cases cover only a marked single route.
- R747-1, Robustness and Docs, `AREA_BUDGET.md`: one sentence that hold does not enter the selection.
- R747-1, Robustness and Docs, the recipe: the fresh-directory sentence could name the comparison directories.
- R748-1 S1 remainder: the four `bound()` sub-conditions have no arm of their own, each redundant with a later check. The PR body states this.

## Lens results (clean lenses in findings format)

- **[R747] PASS Conformance** - `syn/ooc/pp_resource_gate.py:537,566-581`; `receipts/probes/round2-probes.tsv`; `receipts/routes-head/*`.
  - Checked against #818 ("the fall ... printed as `WARNING`, with no failure") and rule 1: the fall is published whatever the floor verdict, and the status follows the floors only.
  - Checked that the recorded sets' verdicts and the issue's acceptance are unchanged: dev selects ExtraPostPlacementOpt at +0.303 and exits 0.
- **[R747] PASS RTL** - artifacts:
  - the gate's CLI and record interface, against every live invocation in the tree: the recipe `:219,573,626` and `MARK_II_AREA_PLAN.md:1344-1346` (now marked);
  - `resmap_map.py:489-499`, for the tie of record to checkpoint;
  - `receipts/f1/`.

  No HDL is in the diff. The interface contract the mapper depends on holds.
- **[R747] PASS Robustness** - `receipts/probes/` (10 probes, all as expected); `receipts/fuzz-dev-400.log` (0 failures, identical to round 1); `receipts/routes-head/` (33 runs). Probed:
  - a floor miss with a fall beyond and within the column, for WNS and WHS;
  - a summary disagreeing with the corners in both directions, on the selected route, a comparison and all routes;
  - reversed order, marked, unmarked and record.
- **[R747] PASS Tests** - `syn/ooc/pp_resource_gate_set_selftest.py:73-80,95-100,106-109,156-160`; `syn/ooc/pp_resource_gate_mutants.py:31,306-321,370-375`; `receipts/gates/{selftest,mutants}.log`; `receipts/named-kills.tsv`; `receipts/extra-mutants.tsv`.
  - Each new arm is non-vacuous: a mutant exists that it alone kills, or that it is the first to kill.
  - The rewritten mutants `timing floor`, `floor names its corners` and `a fall never fails` target the new spans, and each is killed.
- **[R747] PASS Docs** - `docs/design/AREA_BUDGET.md:442`; `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:588`; `docs/design/MARK_II_AREA_PLAN.md:1340-1347`. Also re-read: `docs/integration/BUILDING.md:578` and the gate docstring `:32`, both unconditional statements that stay true.
  - Docs gates at head, all rc 0 (`receipts/docs/`):
    - `docs_check`, `check_doc_style`, `check_doc_paths`, `check_py_idiom`;
    - `measure_fail_fast`, `measure_test_evidence`, `check_hygiene`, `measure_naming`;
    - `check_todo_ownership`, `check_feature_status`;
    - in the pinned markdown environment: `check_em_dash` against `1e80128f` (64 added lines, 0 findings) and `32f0d9b5` (5 lines, 0 findings), and `gen_toc --verify-anchors` and `--check`.
  - Comment rule: the added source lines hold no lane label, round, reviewer ID or issue-comment ID. The one new comment, `# The fall is published whatever the floor verdict.`, states behaviour only.
  - The PR body's one loose sentence is RS1, RESIDUE.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #818 body and #814 rule 1 against `pp_resource_gate.py:537,566-581`; real-route F2 probes; 6 recorded sets, round-1 vs head gate | R747-2 | `50e5d08dda6e89cf010a740cea5cf4539807db01` |
| RTL | CLEAN | no HDL; CLI/record interface vs every live invocation; `resmap_map.py:489-499`; `receipts/f1/` | R747-2 | `50e5d08dda6e89cf010a740cea5cf4539807db01` |
| Robustness | CLEAN | `receipts/probes/` (10), `fuzz-dev-400.log`, `routes-head/` (33 runs) | R747-2 | `50e5d08dda6e89cf010a740cea5cf4539807db01` |
| Tests | CLEAN | set_selftest arms `:73-109,156-160`; mutants `:31,306-375`; selftest/mutants logs; `named-kills.tsv` (209/209); `extra-mutants.tsv` (8/8) | R747-2 | `50e5d08dda6e89cf010a740cea5cf4539807db01` |
| Docs | CLEAN (RS1 RESIDUE carried) | AREA_BUDGET:442, recipe:588, MARK_II:1340-1347, BUILDING:578, docstring:32; `receipts/docs/` | R747-2 | `50e5d08dda6e89cf010a740cea5cf4539807db01` |

## Real limits

- **No new route.** There was no Vivado run and the Mark II map step was not run. Probes plant report text in disposable copies under `scratch/`, without `.dcp`, so they show the gate's reading, not Vivado's behaviour.
- **Coverage of the six sets.** The #806, #787 and #817 sets were identified by their comparison scripts' checkpoint paths. Their bytes are not in the author's `route-reports.tsv`, so "unchanged" for them means the round-1 gate and this head's gate give byte-identical output. My round-1 receipts covered only the dev and #814 sets.
- **Hosted state, a snapshot only** (`receipts/hosted-check-runs.json`, 2026-10-30T20:11Z, 51 runs):
  - 14 success, 1 skipped, the rest queued or in progress;
  - `changes` and `bdd-conformance` succeeded;
  - `yosys-elaboration` (the step that runs the gate), `docs-check`, `elaborate`, and the Verilator and Yosys shards were still queued or running.

  No hosted acceptance is claimed. I ran no act or Docker.
- No manager source bank ran at this head, and I claim none. Physical calibration was NOT RUN, and no hardware was used.
- The clone is byte-identical to the head (`receipts/restore-check.txt`):
  - clean worktree and index;
  - `ls-files -s` equal to the head tree's blobs and modes;
  - gitlinks gptp-processor `f97c1803`, protocol-processor `f65c8ff7` and third_party/verilog-axis `48ff7a7e`, checked out clean.

## Pending manager duties

- Validate the current-dev merge candidate against live dev `56df0894` (builder and native banks) at the merge turn.
- Own hosted and act acceptance at this exact head, including `yosys-elaboration` and the shards still queued in the snapshot.
- Carry RS1 to the residue checklist.
- The external review's re-check of F1 to F3 at this head is its own.

## Prior public review findings

I read these after the verdict and ledger above were on disk:
- PR #820's issue comments (`receipts/pr820-comments.json`, 5 comments): three review-start notices, R747-1 (POSITIVE at `32f0d9b5`) and R748-1 (NEGATIVE at `32f0d9b5`).
- PR #820's reviews and review comments: none.

No other public finding exists. Each prior finding is resolved or retained at this head:

| Prior finding | Status at `50e5d08d` | Evidence |
|---|---|---|
| R748-1 F1 MINOR, Docs and RTL: the Mark II `record` exits 2 | RESOLVED | The documented lines exit 0 and the re-check exits 0; the tracked baseline is unchanged (`receipts/f1/`); basis item 3 |
| R748-1 F2 MINOR, Conformance, Docs and Tests: no WARNING beside a floor miss | RESOLVED | `verdict_for()` `:566-581`; four arms; real-route probes print both, exit 1; the docs say so; basis item 1 |
| R748-1 F3 MINOR, Tests: the guard's safety direction untested | RESOLVED | Two arms; the one-way mutant is killed by its arm; real-route F3-a to F3-f exit 2; basis item 2 |
| R748-1 R1 RESIDUE: the PR body's mutant claim | RESOLVED | The counts are reproduced exactly; basis item 4. A new loose sentence is RS1 |
| R748-1 S1 SUGGESTION: the ceiling and `bound()` sub-conditions | Ceiling part RESOLVED; `bound()` part RETAINED as optional | Basis item 5 |
| R747-1 three SUGGESTIONs | RETAINED, optional | Unchanged by the delta |
| R748-1 limits L1 and L2 (stale comparison directory; the mark is trust-based) | Unchanged limits, not findings | Same class as the R747-1 suggestion on the recipe |

R748-1 noted that `gen_toc.py --verify-anchors` and `--check` were not run. Both ran in this round, rc 0 (`receipts/docs/`).

With every prior finding resolved or retained as optional, the verdict above stands unchanged.

R747-2 FINISHED
