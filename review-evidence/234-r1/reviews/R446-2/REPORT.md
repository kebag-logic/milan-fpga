[R446] NEGATIVE - exact head 0feff20fa228d0cb91d507943e6d39495b28b880

# R446-2 internal review: issue #234 / PR #638, round 2

- Head `0feff20fa228d0cb91d507943e6d39495b28b880`, tree `60ca338523e54df51c26b7efe471df1690218da9`, source base dev `1269cdafb4bb964c757baae0f0c5a932d43f540b`. The round-2 delta is `2a765a6c..0feff20f`: three one-line commits, 9 files.
- Rebuilt from public state, in this order:
  - AGENTS.md and CONTRIBUTING.md;
  - the issue body, then the lane assignment (5966260488), the takeover (5966304381), REVIEW READY round 1 (5967818534), the manager rulings (5967852698), the owner decision (5967924270), the round-2 assignment (5968015720) and REVIEW READY round 2 (5968531831);
  - milestones 10 and 12, issues #233, #639 and #640;
  - the full diff `1269cdaf..0feff20f` and its history;
  - the public evidence tree `43ad8362:review-evidence/234-r1`;
  - the live PR body;
  - hosted check runs at the exact head.
- The real A and B measurement directories were read for the gate's own inputs only: the reports, the cell census and the route status report.
- The author's adapted `reconcile-r2.py` and its diff were judged, as the assignment asks. No other author material was read.
- Prior public findings (R446-1, 5968004900; R447-1, 5968008794) were read only after the independent pass over the diff. Each one is resolved or retained in the table below.
- The rulings and the owner decision were applied as given. The gate policy values are accepted, criterion 1 is judged at 50 MHz, and the gate runs in both places. NFR-RES-01 stays at 60 %, to be met by the #640 redesign in milestone 12, "Optimisations Mark II", which starts after milestone 10, "Instrument verification". None of these is counted as a defect.

Verdict: **NEGATIVE**. Three MINOR findings are open (F1, F2, F3), with one RESIDUE and three SUGGESTIONs. All three findings sit in the new exit-code and route-completion code. Every measured figure, the partition, the policy pin, the CI wiring and the docs gates hold.

## Prior findings at this head

| Prior finding | Status | Evidence at `0feff20f` |
|---|---|---|
| R446-1 F1: non-finite slack passes | **Resolved** | `pp_resource_gate.py:128-132`. My unchanged `probe_gate_cli.py` gives WNS `nan` rc 2, and `inf` with 0 endpoints rc 2. Its one `BAD` line is that inf case: round 1 wrote 1, and both F1 ("refused with exit 2 ... or failed with exit 1") and assignment item 1 allow or require 2. The other 116 of 117 cases are as expected. Arms run at `_selftest.py:157-160`. The shipped mutants `finite slack` and `timed endpoints` are killed. One related test gap, the absent endpoint columns, is in F2. |
| R446-1 F2: claimed refusals without arms | **Resolved** | `probe_gate_mutants.py`, unchanged: 23/23 KILLED, control passes (`receipts/r1-probes/probe-gate-mutants.log`). |
| R446-1 F3: partition mix | **Resolved** | `partition_rederive.py` re-derives the following from the published A and B `ooc-1x1` records: 51 terms; net +79 LUT / +93 FF; absolute 391 / 121; processor top's own logic -23 / +107; `u_nvm_port` +83 / +33. The identity wrapper +162/+126 = 83/33 + 79/93 holds. All 10 sentences in both pages match. The unchanged `reconcile.py` reports exactly its 2 hard-coded round-1 sentences and nothing else. |
| R446-1 R1-R3 (RESIDUE) | **Resolved** | `AREA_BUDGET.md:114`, `:201`, `:204`, findings `:337`, `:338`, `:341`. They use R447-1's per-line wording, which carries R1's and R2's content. |
| R446-1 R4 (RESIDUE) | **Resolved** | The live PR body's decisions 1-5 and its limitations bullet state the rulings and the owner decision. |
| R446-1 S1 (exit-1 tracebacks) | **Partly taken; retained in F3** | The four cases listed in round 1 now exit 2. Wrong-typed fields inside a record still exit 1 through a traceback. |
| R446-1 S2-S5 | **Taken** | S2: `probe_policy_pin.py` passes 105/105. S3: arms at `_selftest.py:161-165`. S4: `docs/findings/README.md:23-24`. S5: the shipped mutants `header uniqueness`, `one generated top` and `count format decimals` are killed. |
| R447-1 MINOR 1 (malformed baseline exits 1) | **Resolved for its listed cases; class retained in F3** | The listed cases exit 2 through `main()`: the 13 `check` and 20 `check-baseline` arms, and my policy and malformed probes. Malformed record fields still exit 1 by traceback (F3). |
| R447-1 MINOR 2 (disabled checks undetected) | **Resolved** | Shipped mutants `standalone RAMB36`, `standalone DSP`, `refusal exit status`, `kind from the directory`, `timing floor boundary`, `ceiling boundary` and `timing fall boundary` are all killed (`receipts/gates/gate-mutants.log`, 84/84). |
| R447-1 MINOR 3 (no route completion) | **Resolved as required; new gap F1** | The 37-unrouted-nets case exits 1 and the clean case 0 on a copy of A's real directory. The new reader accepts a report without its routable rows (F1). |
| R447-1 MINOR 4 (partition) | **Resolved** | As R446-1 F3. |
| R447-1 RESIDUE 1 and 2 | **Resolved** | `AREA_BUDGET.md:114`, `:201`, `:204`. In the PR body, item 1 states the later owner decision, which supersedes "needs the owner's ruling". |
| R447-1 suggestions 1 and 2 | **Taken** | Policy pin: 105/105. Parser and identity guard arms: the shipped mutants `design identity`, `design state identity`, `one timing summary` and `timing value row` are killed. |

## Findings

### F1 - MINOR - Conformance, Robustness, Tests - `syn/ooc/pp_resource_gate.py:268-277`; `syn/ooc/pp_resource_gate_selftest.py:179-180` - a route status report without its routable-net rows reads "complete" and passes

- **Requirement/evidence:**
  - Assignment item 3 (5968015720) asks that a missing or unreadable route status report exit 2.
  - The gate's docstring (`:22-24`) and `AREA_BUDGET.md:190` say an unreadable measurement exits 2.
  - REVIEW READY round 2 states that "routable nets not fully routed exit 1".
  - `routing()` requires exactly one `nets with routing errors` row. It only requires the `routable nets` and `fully routed nets` rows to occur *equally often*, and zero times is equal. So the completeness comparison `sum(routed) != sum(routable)` becomes `0 != 0`.
  - `receipts/probe-route-status.log` used a symlink copy of A's real route directory with the route status report replaced. Each case went through the gate's CLI against the real `route-1x1` baseline:
    - both rows removed: **rc 0**, "route status: complete, no unrouted net and no routing error";
    - both rows relabelled: **rc 0**, the same line.
  - The other 13 planted cases behave as required:
    - clean: 0;
    - routing errors with unrouted pins, overlaps only, an unrouted-nets row, or one net short of fully routed: 1;
    - missing, duplicated, empty, directory, not UTF-8, repeated error row, negative count, or only the routable row removed: 2.
  - The self-test's only arm for these rows removes the routable row alone (`_selftest.py:179-180`), so it cannot tell "equal count" from "present".
- **Impact:**
  - The primary signal, the error row, is still required, so a real report from today's tool fails closed.
  - A report whose net-count rows are absent or renamed is still printed as a proven complete route and exits 0. The gate prints a completeness claim it did not check.
  - This is the one parser in the gate that accepts a missing row. `utilization()` refuses any absent label.
- **Required outcome:**
  - A route status report that lacks exactly one `routable nets` row and one `fully routed nets` row exits 2 with a named reason.
  - An arm removes both rows.
  - A mutant that relaxes the presence requirement is killed.
- **Verification:** rerun `probe_route_status.py <checkout> <A route dir> <scratch>`. The two `CONTRACT both ...` cases must give rc 2. The shipped self-test and mutant campaign must still pass.

### F2 - MINOR - Tests - `syn/ooc/pp_resource_gate_selftest.py:31-35`, `:269-300`; `syn/ooc/pp_resource_gate_mutants.py` - the budget-table pin is proven only for tolerance cells, and the timed-endpoint column guard has no arm

- **Requirement/evidence:**
  - Assignment item 4: "Every claimed refusal has an arm and a killed mutant".
  - `AREA_BUDGET.md:155` claims `check-baseline` "refuses a baseline whose policy differs from it in any cell".
  - The self-test docstring says it plants "every regression and refusal the resource gate claims".
  - `receipts/probe-extra-mutants.log` ran each mutant against the shipped 113-arm self-test. The control passes and these four mutants **survive**:
    - `check-baseline compares tolerances only`: `for field in ("tolerance",)` at `pp_resource_gate.py:432`, so floor and ceiling cells are never compared;
    - `check-baseline compares table figures only`: drops `set(held)` at `:434`, so a JSON policy figure the table lacks is never reported;
    - `budget floors read as zero`: survives because the fixture's floors are both 0 (`_selftest.py:34`);
    - `timed endpoint columns optional`: drops `not paths` at `:129`, so a timing summary with no `Total Endpoints` column is accepted.
  - The shipped gate is correct at all four points:
    - `receipts/probe-policy-pin.log` shows every floor and ceiling cell bump, dash and JSON change refused, and an added JSON ceiling, floor or tolerance figure refused;
    - the code at `:129` refuses absent columns.
  - Every audit arm that edits the table or the JSON changes a tolerance (`_selftest.py:287-290`).
- **Impact:**
  - The hosted self-test, mutants and `check-baseline` are the only automated protection of the policy pin.
  - An edit narrowing the comparison to tolerances stays green. After such an edit, the accepted 121.5-tile ceiling or the +0.030 ns WNS floor could be loosened in the JSON alone.
  - That is exactly the R446-1 S2 / R447-1 suggestion 1 hole the round was asked to close mechanically.
- **Required outcome:** audit arms and matching shipped mutants for each of these:
  - a floor cell differing between table and JSON, with a non-zero fixture floor;
  - a ceiling cell differing;
  - a JSON policy figure the table lacks;
  - a timing summary without its `Total Endpoints` columns.
- **Verification:** rerun `probe_extra_mutants.py <checkout> --jobs 12`. All four must be KILLED and the control must pass.

### F3 - MINOR - Conformance, Robustness, Tests, Docs - `syn/ooc/pp_resource_gate.py:289-290`, `:299-306`, `:339-349`, `:363-370`, `:481`; `docs/design/AREA_BUDGET.md:190`; PR body "Description" - malformed fields inside a baseline record exit 1 through a traceback, and `check-baseline` passes them

- **Requirement/evidence:**
  - Assignment item 2: "Every malformed or missing baseline entry ... exits 2 with a named reason, never through a traceback". Exit 1 is reserved for a material regression.
  - `AREA_BUDGET.md:190`: "exit 1 means a material regression only".
  - The PR body: "always with its reason and never through a traceback".
  - `entry_problems()` checks that `kind`, `identity`, `inputs_sha256`, `figures` and `scopes` are present, and that the gated figure keys exist. It checks neither their types nor that the figures are numbers. `judge()` (`:281` onward) runs outside the `try` in `main()`.
  - `receipts/probe-malformed-record.log` used the self-test's own fixture and baseline, with one field changed, through the CLI:

    | Record field | `check` | `check-baseline` |
    |---|---|---|
    | `identity` is a list or a string | rc 1, TRACEBACK `TypeError` | rc 0, "baseline PASS" |
    | `scopes` is a list | rc 1, TRACEBACK `AttributeError` | rc 0 |
    | gated figure `LUT` is the string `"1000"` | rc 1, TRACEBACK `TypeError` | rc 0 |
    | `kind` is a list | rc 1, TRACEBACK | rc 1, TRACEBACK |
    | floor `WNS_ns` is `NaN` (Python's JSON reads `NaN`) | rc 0, `RESULT: PASS` (the floor is disabled) | rc 2 (the table differs) |

    A string tolerance and a null figure are refused with exit 2.
- **Impact:**
  - The class R447-1 MINOR 1 raised survives inside the record: a broken baseline is reported with the regression status.
  - `check-baseline`, the hosted guard, passes most of these, so they reach the merge bank's `check` as exit 1.
  - The NaN floor is caught only because hosted CI runs `check-baseline` on the committed file.
  - The record is normally written by `record --write`, so the trigger is a hand edit or a corrupted file.
- **Required outcome:**
  - In both `check` and `check-baseline`, a record field of the wrong type, a non-numeric or non-finite gated figure, and a non-finite policy value each exit 2 with a named reason, never through a traceback.
  - Self-test arms drive these through `main()`, with killed mutants.
  - The docs and the PR body then state the contract as it holds.
- **Verification:** rerun `probe_malformed_record.py <checkout>`. It must report 0 cases not exit 2.

### RESIDUE (wording only; for the residue checklist)

- **R1** - `docs/design/AREA_BUDGET.md:170`. It changes no figure.
  - Now: "The processor top's own logic is one of those terms: -23 LUTs and +107 FFs, its timer-arm queues."
  - Fix: "The processor top's own logic is one of those terms: -23 LUTs and +107 FFs; the 107 FFs are its timer-arm queues." The findings page (`:141-142`) already attributes only the FFs to `armq_r`.

### SUGGESTION

- **S1** - `pp_resource_gate.py:271-272`.
  - The tool's layout for a wholly unrouted route was not verified here. If it prints `routable nets` with no `fully routed nets` row, the gate gives exit 2 ("unequally often") where the contract says 1.
  - A planted case of that layout gives 2 (`probe-route-status.log`, the last line). It fails closed.
  - Reading the counts before the pairing check, or treating an absent `fully routed` row as 0 when `routable` is present, would give 1.
- **S2** - The route status report has no header, so the gate cannot bind it to the run it judges.
  - In A and B it was written by the same `baseline_integrated.tcl` (`:313`) within that run's window: A at 09:16:55 between `route.dcp` and `baseline_utilization.rpt`, B at 10:06:02.
  - A note in the recipe that a stale report from an earlier build in the same directory would be read would make that assumption visible.
- **S3** - "`armq_r`, 1,260 flops in B against A's 1,153" (findings `:142`) is not reproducible from the public evidence. Only A's cone TSV is published.
  - I re-derived 1,153 / 1,260 `FD*` cells named `armq_r` from the two runs' `baseline_cells.tsv`.
  - Publishing B's census or cone row would let a cold reviewer check it.

## Verified clean, with evidence

- **Gates the change touches, rc 0** (`receipts/gates/summary.txt`, 31 commands, run concurrently, GNU Make 4.3 first on PATH, built in scratch from the release tarball, sha256 `e05fdde4...e19`):
  - gate self-test, **113 arms**; gate mutants, control plus **84/84** failing; `check-baseline`, "baseline PASS: 3 endpoints";
  - `pp_baseline` self-test, 32 mutants and reports self-test;
  - `ci_scope --selftest`, which rejects AREA_BUDGET.md filed as docs-only and finds it named at `pp_resource_gate.py:48`; `ci_events --check` and `--selftest`;
  - docs_check, doc style and its self-test, gPTP docs with and without the submodule, `make -C gptp-processor docs` under Make 4.3, DOC_MAP, solution docs, feature status and its self-test, module matrix, doc paths, archive, bare-metal;
  - em-dash (580 added lines, 5 pages), TOC anchors and TOC check, all under the pinned Markdown environment;
  - Python idiom, fail-fast, hygiene, TODO ownership, test evidence;
  - `git diff --check 1269cdaf HEAD` is clean, and the three commits are one line with no trailers.
- **Real data through the gate at this head** (`receipts/real/`):

  | Run | rc | Result |
  |---|---|---|
  | A route | 0 | "route status: complete" (105,566 of 105,566 nets, 0 errors) |
  | A 1x1 | 0 | |
  | A 8x8 | 0 | |
  | A 1x1 at 10 ns | 2 | `standalone_clock_ns` |
  | B route | 1 | +625 LUT over 500; route status complete (105,559 of 105,559) |
  | B 1x1 | 0 | +162 |
  | B 8x8 | 0 | -172 |

  Each route status report was written by the same run script inside that run's window (S2). Findings page `:83-85` is exact.
- **No mutant is killed only by a crash.** `probe_pr_mutant_reasons.py`, unchanged, classifies 84/84 as ARM, killed by a named arm assertion.
  - 74 are wrong verdicts.
  - 10 are an escaped exception that an arm names (exit -1). In 9 of the 10 the escaped exception is the mutant's own defect: an unreadable baseline, budget or status leaks a traceback instead of exiting 2.
  - The 10th, `Slice row`, crashes `judge()`. A coherent variant that also removes `SLICE` from `GATED` is killed by the `missing Slice row` arm's assertion (`probe-extra-mutants.log`).
- **Policy pin** (`receipts/probe-policy-pin.log`, 105/105):
  - The JSON baseline is byte-unchanged since round 1.
  - The round-2 table parses to exactly the JSON policy.
  - The round-1 prose table, read by hand, carries the same values (+500/+600/+80/+0, floors +0.030 and 0, fall 0.25, ceiling 121.5; ooc-1x1 +250/+250; ooc-8x8 +316/+339; +0 RAMB/DSP), so the re-layout changed no value.
  - Every table cell bumped or set to a dash, every dash given a value, every JSON value bumped or removed, and each added JSON figure was refused with exit 2 and a named cell.
- **Partition** (`receipts/partition-rederive.log`): re-derived as in the R446-1 F3 row of the table above, 0 mismatches. The adapted `reconcile-r2.py` (sha256 `7b169df2...`, diff `b7fb8b03...`) differs from my published round-1 script only in the hunk replacing the two round-1 checks, as its diff shows. It computes the same own-logic partition and reports 0 mismatches. Its other 30 OK lines are identical to my unchanged run (`receipts/adapted-reconcile-r2.log`).
- **CI scope:**
  - `GATE_READ_DOCS` now has 5 pages (`ci_scope.py:56-62`) and `CI_WORKFLOWS.md:58-71` says "Five pages". The fifth is check-baseline in `yosys-elaboration`.
  - That is where `rtl-fast.yml:212-214` runs it; the pin is at `ci_events.py:2328-2330`.
  - The classifier gives `AREA_BUDGET.md` alone `true`, the findings page alone `false`, and the PR's file list `true`.
- **Docs** (`AREA_BUDGET.md:97-210`, findings `:80-85`, `:134-145`, `:334-353`, recipe `:441-477`, `docs/findings/README.md:23-24`, the PR body):
  - The owner decision is cited where "needs an owner decision" stood, with the link 5967924270, and milestone 12's description matches.
  - The lever Issue column reads #230 and #639. #639 and #640 exist, and #640 and #233 are in "Optimisations Mark II".
  - Both baseline findings are indexed, with accurate revisions (`7eb3b0d4`, #587 at 50 MHz, three placement directives).
  - Apart from F3's contract sentence and R1, every round-2 sentence matches the code or the records.
- **RTL:**
  - `1269cdaf..0feff20f` touches no file under `hdl/`.
  - The gitlinks are identical at base and head: `631eeb34`, `5dce647a` and `48ff7a7e`.
  - The round-2 prose adds one RTL-derived figure, the `armq_r` census (S3), which reproduces.
- **Hosted, exact head, 11:16Z** (`receipts/hosted-check-runs.txt`, `receipts/hosted-yosys-elaboration-steps.txt`):
  - `rtl-fast`, `yosys-elaboration`, `verilator-lint`, `bdd-conformance`, `changes`, `full-ci-gate`, `docs-check-no-git`, `wire-accountability`, Yosys shards 0-3 and Verilator shard 3 succeeded.
  - `yosys-elaboration` step 9, the gate step, executed with success.
  - `docs-check`, `elaborate` and Verilator shards 0, 1, 2 and 4 were in progress.
  - `Physical gPTP` was skipped. That is not evidence.
- **Probe hygiene** (`receipts/final-tree-verify.log`):
  - HEAD and the tree are exact, and the index tree equals `60ca3385`.
  - `git ls-files -s` equals `ls-tree -r HEAD` for blob, mode and path.
  - Nothing is untracked or ignored, and the three submodules are clean at their gitlinks.
  - Host paths in the receipts are redacted to `<clone>`, `<packet>`, `<run-root>` and `<tools>`.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F3) | #234 criteria under 5967852698 and 5967924270; assignment items 1-8 of 5968015720; `pp_resource_gate.py:111-133,252-321,363-483`; `AREA_BUDGET.md:97-210` vs JSON (policy probe); real A/B gate runs | R446-2 | `0feff20fa228d0cb91d507943e6d39495b28b880` |
| RTL | CLEAN | `git diff --name-status 1269cdaf..0feff20f` (14 files, none under `hdl/`); gitlinks `631eeb34`/`5dce647a`/`48ff7a7e` unchanged; `armq_r` 1,153/1,260 from A/B `baseline_cells.tsv` | R446-2 | `0feff20fa228d0cb91d507943e6d39495b28b880` |
| Robustness | UNCLEAN (F1, F3) | `routing()`, `load()`, `entry_problems()`, `judge()`, `main()` under 16 route-status cases on A's real directory, 16 malformed-record CLI cases, 105 policy-pin cases, 117 round-1 CLI cases | R446-2 | `0feff20fa228d0cb91d507943e6d39495b28b880` |
| Tests | UNCLEAN (F1, F2, F3) | `pp_resource_gate_selftest.py` (113 arms), `pp_resource_gate_mutants.py` (84); 23 round-1 mutants; 84-mutant reason classification; 11 supplementary mutants | R446-2 | `0feff20fa228d0cb91d507943e6d39495b28b880` |
| Docs | UNCLEAN (F3) | `AREA_BUDGET.md:97-210`, findings `:80-85,134-145,334-353`, recipe `:441-477`, `CI_WORKFLOWS.md:58-71`, `docs/findings/README.md:23-24`, live PR body; 31 gates | R446-2 | `0feff20fa228d0cb91d507943e6d39495b28b880` |

## Real limits

- No Vivado run, so the tool's own layouts were not observed:
  - a route status report for an unrouted or partly routed route (F1, S1);
  - a timing summary with no constrained path.
  - The planted layouts follow the real clean report and the round-1 probe's model.
- The raw A and B reports were read from the retained run directories, not from public evidence. The route status contents and the `armq_r` census rest on those directories.
- R447-1's own probes were not rerun. Their claims were checked through the shipped mutant names and my own probes.
- Not run: the full parent, PP, gPTP, Yosys and builder banks; `act_ci` and its self-test; Docker; hardware. The manager reports the source static, builder and native banks passed at this head.
- Physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Accept or reject the hosted contexts still in progress at 11:16Z: `docs-check`, `elaborate`, and Verilator shards 0, 1, 2 and 4.
- Re-review the fix head under every lens the fix touches. A gate change un-covers Conformance, Robustness and Tests; a docs or PR-body change un-covers Docs.
- Carry R1 to the residue checklist if no later round takes it.
- Run the Vivado comparison in the merge bank (ruling (b)), and validate the final current-dev candidate at the merge turn (live dev `bbf704ec`).
- Publish B's `armq_r` census (S3) and the raw route status reports, so a cold reviewer can re-derive them.

R446-2 FINISHED
