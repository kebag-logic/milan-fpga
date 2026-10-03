[R447] NEGATIVE - exact head 0feff20fa228d0cb91d507943e6d39495b28b880

# R447-2 external review: issue #234 / PR #638, round 2

- Head `0feff20fa228d0cb91d507943e6d39495b28b880`, tree `60ca338523e54df51c26b7efe471df1690218da9`, source base dev `1269cdafb4bb964c757baae0f0c5a932d43f540b`.
- 8 commits, 14 files. Round 2 is `2a765a6c..0feff20f`: 3 one-line commits, 9 files. No `hdl/` change, no gitlink move, and `pp_resource_baseline.json` is unchanged in round 2.
- Verdict NEGATIVE: two MINOR findings are open, F1 and F2. Both concern the new gate's refusal surface.
  - RTL is covered clean.
  - Conformance, Robustness and Tests are unclean under F1 and F2. Docs is unclean under F1.
- Every prior finding is judged below. Of the 20 prior items (R446-1: 3 MINOR, 4 RESIDUE, 5 SUGGESTION; R447-1: 4 MINOR, 2 RESIDUE, 2 SUGGESTION), 19 are resolved. R447-1 MINOR 1 is retained in a narrower form as F1. F2 is a new defect in the round-2 route-status reader.
- My verdict and ledger were written before I read any other reviewer's report: `receipts/draft_verdict.md`, with its digest and UTC time in `receipts/draft_verdict.sha256`. Reading the reports afterwards changed neither.

## Inputs, in order

1. AGENTS.md, CONTRIBUTING.md and docs/README.md.
2. Issue #234's body and its comments:
   - the lane assignment (5966260488) and the takeover (5966304381);
   - round-1 REVIEW READY (5967818534);
   - the manager rulings (5967852698) and the owner decision (5967924270);
   - the round-2 assignment (5968015720) and round-2 REVIEW READY (5968531831).
3. NFR-RES-01, BUILDING.md section 5, and the milestone list (`receipts/milestones.tsv`: "Instrument verification (2027)" and "Optimisations Mark II" exist; #640 is in the latter).
4. `git diff 1269cdaf..0feff20f` and `2a765a6c..0feff20f`, with their history.
5. The public evidence:
   - `43ad8362:review-evidence/234-r1`, the round-1 records and receipts;
   - `b228a4cb:review-evidence/234-r1/author-r2`, the round-2 receipts and `reconcile-r2.diff`;
   - the existing A and B measurement directories, read only.
6. The exact-head hosted check runs.
7. Only after the draft verdict: the R446-1 and R447-1 reports and their published probes.

## Findings

```text
[R447] MINOR Conformance, Robustness, Tests, Docs - syn/ooc/pp_resource_gate.py:368-369, :289-290, :299-306, :339-347, :265-267; docs/testing/PP_SHADOW_BASELINE_RECIPE.md:462; docs/design/AREA_BUDGET.md:190; PR #638 body (Description, gate row) - the exit-code contract is not total: malformed baseline record fields exit 1 by traceback or pass silently, and a non-ASCII digit in the route status escapes as a traceback
Requirement/evidence: round-2 assignment item 2 (5968015720): "Every malformed or missing baseline entry and every unreadable measurement exits 2 with a named reason, never through a traceback ... Exit 1 stays reserved for a material regression." The docs repeat it: the recipe says "A missing, non-JSON or incomplete baseline gives 2, never 1"; AREA_BUDGET.md:190 says "exit 1 means a material regression only"; the PR body says "always with its reason and never through a traceback". receipts/probe_contract.log runs the real CLI as a subprocess. The candidate is a symlink mirror of the real A route with +1000 LUT and one image digest changed, and the control exits 1 (MATERIAL REGRESSION). Each case edits one field of the route-1x1 entry:
  - record.kind [] or {}: check rc 1 TRACEBACK (TypeError, unhashable, :368 sits outside entry_problems' try); check-baseline rc 1 TRACEBACK too.
  - record.figures.LUT "50128" or null: check rc 1 TRACEBACK (TypeError at :302); check-baseline rc 0 "baseline PASS".
  - record.figures.LUT NaN: check rc 0 "RESULT: PASS" on the +1000-LUT candidate (nan comparisons are false); check-baseline rc 0. This fails open.
  - record.identity "x": check rc 1 TRACEBACK (:290); check-baseline rc 0.
  - record.scopes []: check rc 1 TRACEBACK (AttributeError, :343); check-baseline rc 0.
  - record.identity [] and record.figures.WNS_ns NaN are accepted without a refusal (rc 1 only because of the planted LUT growth); check-baseline rc 0.
  - A route status count "²" (str.isdigit() is true, int() raises): rc 1 TRACEBACK (receipts/probe_route_real_A.log).
  Tolerance, floor and ceiling of Infinity or NaN are caught by check-baseline's table pin (rc 2) but not at `check`; that half is covered by the hosted check-baseline, so it is not part of this finding. The enumerated cases of item 2 (non-JSON, missing file, no endpoints, no record, missing tolerance, unknown ceiling figure, wrong-shape manifest) all exit 2 correctly (probe_cli 54/54).
Impact: a hand-edited or merge-damaged baseline that hosted check-baseline accepts makes the bank's `check` exit 1, read as a material regression of the candidate, or exit 0 on a real growth (NaN). That is the 1-versus-2 misrouting R447-1 MINOR 1 was about, in fields the round-2 guard does not reach. It fails closed except for the NaN case.
Required change: a baseline record whose kind, identity, figures (type and finiteness of every gated figure), digest or scope table is not of the recorded shape is refused with exit 2 and a named reason, by `check` and by check-baseline. A route status count is read as ASCII digits or refused with 2. No path reaches a traceback. Self-test arms drive these through main(), each with a killed mutant. Alternatively, narrow the documented contract, but the assignment wording makes that a manager decision.
Verification: probe_contract.py reports rc 2 with no TRACEBACK for every edited case in both columns, and rc 1 for the control. probe_route_real.py's superscript case gives rc 2.
```

```text
[R447] MINOR Conformance, Robustness, Tests - syn/ooc/pp_resource_gate.py:268-276 - a route status report without its routable and fully-routed rows reads as a complete route
Requirement/evidence: round-2 assignment item 3: the route endpoint reads `*_route_status.rpt`; unrouted nets or routing errors exit 1; "a missing or unreadable report: exit 2". The reader requires exactly one routing-errors row (:268) and equally many routable and fully-routed rows (:271). Zero of each satisfies that, and `sum(routed) == sum(routable) == 0` (:275), so the route is declared complete. receipts/probe_route_real_A.log mirrors the real A route and keeps the real report with only its "routable nets" and "fully routed nets" rows removed: rc 0, "route status: complete, no unrouted net and no routing error", RESULT: PASS. Removing either row alone is refused with rc 2, as are a missing, duplicated, empty, non-UTF-8 or directory report. On B the same planted report prints "route status: complete", and B exits 1 only for its +625 LUT (receipts/probe_route_real_B.log). The shipped arms (pp_resource_gate_selftest.py:179-180) remove only the routable row, so the mutant campaign cannot see this gap.
Impact: a report that names no routable-net count is not evidence of a complete route, yet the gate prints "route status: complete" and can pass. Real Vivado reports always carry both rows, and a truncated file loses the last row, the error row, first. So this is a fail-open on an incomplete report rather than a likely field failure, but it is the completeness check this round added.
Required change: the route-status reader requires a routable-nets row and a fully-routed-nets row (at least one each, or exactly one each, as the report layout is read), and refuses otherwise with exit 2 and a named reason. A self-test arm removes both rows, and a mutant relaxing the guard is killed.
Verification: probe_route_real.py "both routable rows missing" gives rc 2, and every other case is unchanged (13 of 15 as wanted today, 15 of 15 after both fixes).
```

```text
[R447] SUGGESTION Robustness - syn/ooc/pp_resource_gate.py:252-258 - the route status report is not bound to the measured run
Requirement/evidence: report_route_status writes no tool or design header (the real A and B reports are 11 lines: counts only), and the gate reads it by glob, independent of the identity and input digest. A stale report left from an earlier run in the same directory is read as this run's.
Suggested change: require the report to be no older than baseline_utilization.rpt, or record its digest in the run receipts the bank keeps.
```

## Prior findings at this head

R446-1 is the internal round-1 report at `2a765a6c`. R447-1 is my own round-1 report.

| Prior finding | State at 0feff20f | Evidence (this round) |
|---|---|---|
| R446-1 F1 non-finite slack passes | RESOLVED | `pp_resource_gate.py:128-132`. R446 `probe_gate_cli.py` unchanged: `nan` gives rc 2, and `inf` with 0 endpoints gives rc 2 (the one "BAD" is the probe's literal want of 1; F1 allowed 2 and the assignment required 2). Arms `WNS not a number`, `WNS and WHS infinite`, `no timed endpoint`. Mutants `finite slack` and `timed endpoints` are killed (`receipts/classify_mutants.log`). |
| R446-1 F2 claimed refusals without an arm | RESOLVED | R446 `probe_gate_mutants.py` unchanged: 23 of 23 killed, control passes (`receipts/r446probes/`). |
| R446-1 F3 mixed partitions | RESOLVED | `receipts/partition_r2.log`, re-derived from the published A/B `ooc-1x1` records: 51 terms (52 listed instances minus `u_pp/u_nvm_port`, which has no listed descendant); net +79 LUT / +93 FF; absolute 391 / 121; `u_pp` own logic -23 / +107; wrapper minus `u_nvm_port` = +79 / +93. All equal findings :137-142 and AREA_BUDGET :166-170. `armq_r` flops counted by name in the real cell censuses: A 1,153, B 1,260, so +107 (`receipts/armq_count.log`), matching findings :142. The cited RTL `protocol_processor_top.sv:2921` declares `armq_r` at pin `631eeb34`. |
| R446-1 R1, R2 | RESOLVED | AREA_BUDGET :114, :201, :204 carry the ruled wording, R447-1 RESIDUE 1's form. |
| R446-1 R3 | RESOLVED | Findings :336-341: lever 2 is "#230 (joins its scope)", and levers 3 and 6 are "#639". |
| R446-1 R4 | RESOLVED | The PR body's "Decisions" 1 to 5 state the rulings and the owner decision. |
| R446-1 S1 to S5 | RESOLVED | S2: policy pin, 107/107 below. S3: arms `LUT improvement beyond the tolerance` and `WNS rise beyond the tolerance`, with mutants. S4: findings README :23-24. S5: header-uniqueness, generated-top and decimal-format mutants are killed. S1 is resolved for its listed cases; its class continues as F1. |
| R446-1 `reconcile.py` | Unchanged copy: 2 mismatches, the expected result. Adapted copy: SOUND, 0 mismatches. | The unchanged script asserts the round-1 sentences, so it cannot pass any corrected prose. Its second check needs FF +95 on a partition whose records give -12. The published `reconcile-r2.diff` touches only those two checks. It recomputes the partition from the records (the own logic of every instance except `u_pp/u_nvm_port`, which is my partition), asserts the round-2 sentences ("a net +79 LUTs and +93 FFs", "sum to 391 LUTs and 121 FFs", "51 terms", "-23 LUTs and +107 FFs") in both pages, and hard-codes no figure. I rebuilt the copy from R446-1's published script plus that diff (`patch` rc 0; `receipts/r446probes/reconcile-r2.reconstructed.py`); it reports 0 mismatches. |
| R447-1 MINOR 1 malformed baseline exits 1 by traceback | RETAINED, narrowed, as F1 | The six listed cases now exit 2 (`probe_cli.py` unchanged: 54 of 54 as documented). The same class remains for record field shapes and a non-ASCII route count. |
| R447-1 MINOR 2 disabled checks undetected | RESOLVED | `extra_mutants.py` unchanged: 18 of 18 killed, control 113 arms PASS. |
| R447-1 MINOR 3 route completion never read | RESOLVED as asked | `probe_route_status.py` unchanged: clean exit 0, 37 unrouted nets exit 1. On the real A/B routes, unrouted, some-unrouted-pins, errored and partly-routed reports exit 1; missing, duplicated, empty and unreadable reports exit 2. New gap: F2. |
| R447-1 MINOR 4 mixed partitions | RESOLVED | As R446-1 F3. `partition_check.py` unchanged prints the complete-partition line (+79, 391, +93) and the `u_pp` line (-23, +107) that the prose now uses. Its trailing "documented:" line is a fixed round-1 string, not a check. |
| R447-1 RESIDUE 1 | RESOLVED | AREA_BUDGET :114, :201, :204 carry the exact fix text. |
| R447-1 RESIDUE 2 | RESOLVED | PR body items 2 and 3 and the limitations bullet carry the exact text. Item 1 now states the owner decision 5967924270, which supersedes "needs the owner's ruling"; this is correct. |
| R447-1 SUGGESTION 1 policy unpinned | RESOLVED | `receipts/probe_policy.log`: 107 of 107 perturbations refused, rc 2 naming the endpoint, with the control rc 0. That covers each of the 21 JSON policy values moved two ways and removed, an added JSON field per endpoint, and every table cell altered (a value moved; a dash replaced with a value). |
| R447-1 SUGGESTION 2 guards without arms | RESOLVED | Design, design state, header uniqueness, one timing summary, timing value row and one generated top each have an arm, and their mutants are killed. |

## Clean lens

```text
[R447] PASS RTL - git diff --name-status 1269cdaf..0feff20f (14 files, none under hdl/; gitlinks 631eeb34 / 5dce647a / 48ff7a7e unchanged, receipts/restore_check.log); protocol-processor@631eeb34 hdl/top/protocol_processor_top.sv:2916-2922 (armq_r [8][4][ARM_W_C]); real A/B ax7101-ooc baseline_cells.tsv (armq_r 1,153 / 1,260 FD cells, receipts/armq_count.log); syn/ooc/pp_baseline.py standalone_clock (bound CLK_HZ_P 50 MHz to 20.000 ns, 10 ns default) with the pp_baseline self-test and 32/32 mutants - no RTL or interface change to judge; the one new RTL claim of round 2 (the processor top's +107 FF are its timer-arm queues) is true at the pinned source and in both measured netlists; the clock derivation matches the records' standalone_clock_ns 20.000.
```

## Lens coverage beyond the findings

These checks found nothing wrong.

- **Conformance:**
  - Criterion 1 as ruled: A +0.063 / +0.036 ns and B +0.101 / +0.036 ns at 20 ns.
  - Criterion 3 cites the owner decision at AREA_BUDGET :133-136.
  - Criterion 4's hosted half executed at the exact head: hosted job `yosys-elaboration`, step 9 "Prove the OOC read sets..." success, logging "resource gate selftest: 113 arms PASS", "control passes, all 84 mutants fail" and "baseline PASS: 3 endpoints" (`receipts/hosted_*`).
  - Real data through the head's CLI (`receipts/real/`): A route, 1x1 and 8x8 each rc 0, with the route "route status: complete". B route rc 1 (+625 LUT over 500), with route status complete. B 1x1 and 8x8 rc 0. A 10 ns control rc 2 (standalone_clock_ns).
  - The real reports read clean: A 105,566 of 105,566 and B 105,559 of 105,559 routable nets fully routed, with 0 routing errors, as findings :83-84 say.
  - `replay_records.py` unchanged gives A 0/0/0, B 1/0/0 and 10 ns 2.
  - `check_tables.py` unchanged: 49 groups, 0 mismatches.
  - The ooc-1x1 baseline record equals the published A record.
- **Robustness:**
  - The policy pin is total: 107 of 107 (above).
  - Route status reading: 13 of 15 planted cases as wanted on A. The two misses are F1 and F2.
  - Finite and non-finite timing and zero endpoints behave as documented (R446 probe, 117 cases, one expectation mismatch explained above).
- **Tests:**
  - Self-test: 113 arms.
  - Shipped mutants: 84 of 84 fail, control passes. `receipts/classify_mutants.log` classifies each kill by its final exception. 74 are killed by an arm assertion on a wrong status or text. 10 are killed by an arm assertion whose report is an exception the mutated gate let escape. 0 by a harness crash, 0 survived. Each of the 10 removes a refusal guard (or, for `Slice row`, a figure the comparator then cannot find), so the escaped traceback is the defect the arm's exit-2 contract detects.
  - R446's reason probe agrees: 84 of 84 ARM.
  - Round-1 probes rerun unchanged: `extra_mutants` 18/18 killed, and R446 `probe_gate_mutants` 23/23 killed.
- **Docs:**
  - Policy table re-layout: every value equals the round-1 table. Route: +500 / +600 / +80 / +0 x3 / +0.030 ns / 0 ns / 0.25 ns / 121.5. ooc-1x1: +250 / +250 / +0 x3. ooc-8x8: +316 / +339 / +0 x3. The parsed table equals the JSON.
  - The owner-decision citation, the #639/#640 mapping, the README index and the partition prose are correct.
  - CI_WORKFLOWS :58 "Five pages" now lists AREA_BUDGET with its reader (:69-71), consistent with `ci_scope.py` `GATE_READ_DOCS` and with the classifier, which files `docs/design/AREA_BUDGET.md` alone as RTL-relevant (`receipts/gates/ci_scope_budget_only.log` "true"). Its self-test derives the page from `pp_resource_gate.py:48` and kills both table mutations (`ci_scope.log`).
  - The only Docs defect is the "never 1" claim covered by F1.

## Touched gates (this head, GNU Make 4.3 first on PATH, built from the verified release tarball, sha256 e05fdde4...)

All 31 gate jobs rc 0 (`receipts/gates/*.rc`, run by `run_gates.sh`; several jobs chain two commands):

- gate: self-test (113 arms), mutants (84), check-baseline;
- pp_baseline: self-test and 32 mutants; the reports self-test;
- dp_srcs: self-test and tops; ooc_tcl;
- ci_events: `--check` and `--selftest`;
- ci_scope: `--selftest`, the diff classification, and AREA_BUDGET alone;
- pp_srcs: `--check` and `--selftest`;
- docs_check and its `--selftest`; em-dash over 580 added lines;
- doc style, DOC_MAP, solution docs, feature status, module matrix, doc paths, archive, TOC and anchors;
- Python idiom, hygiene, TODO, fail-fast and test evidence;
- `git diff --check`;
- `make -C gptp-processor docs` under GNU Make 4.3.

One runner-script slip: the first pass named a nonexistent `docs_check.py --no-git` option. It was replaced by `--selftest`, which was run alone, and that log is the one kept.

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | Issue #234 criteria with rulings 5967852698 and owner decision 5967924270; round-2 assignment items 1-8; `pp_resource_gate.py`; real A/B directories through the CLI (`receipts/real/`); `probe_contract.log`; `probe_route_real_{A,B}.log`; hosted job step 9 | R447-2 | `0feff20fa228d0cb91d507943e6d39495b28b880` |
| RTL | CLEAN | Diff name list and gitlinks; `protocol_processor_top.sv:2916-2922` at `631eeb34`; A/B `baseline_cells.tsv` `armq_r` counts; `pp_baseline.py` standalone clock | R447-2 | `0feff20fa228d0cb91d507943e6d39495b28b880` |
| Robustness | UNCLEAN (F1, F2) | `pp_resource_gate.py:111-133, 252-277, 352-438, 441-483` under the contract, route, policy and R446/R447 CLI probes | R447-2 | `0feff20fa228d0cb91d507943e6d39495b28b880` |
| Tests | UNCLEAN (F1, F2) | `pp_resource_gate_selftest.py` (113 arms); `pp_resource_gate_mutants.py` (84, classified); R446 `probe_gate_mutants.py` 23/23 and `probe_pr_mutant_reasons.py`; R447-1 `extra_mutants.py` 18/18 | R447-2 | `0feff20fa228d0cb91d507943e6d39495b28b880` |
| Docs | UNCLEAN (F1) | `AREA_BUDGET.md` (round-2 diff, table parse); findings page :80-142, :336-353; recipe :453-477; findings README :23-24; CI_WORKFLOWS :58-71; `ci_scope.py:50-61, 269-274`; PR body; R446 `reconcile.py` and the adapted copy; R447-1 `partition_check.py` and `check_tables.py` | R447-2 | `0feff20fa228d0cb91d507943e6d39495b28b880` |

## Real limits

- No Vivado or Yosys run in this review. Records were not re-derived from new measurements. The real A/B directories were read only: through the gate, through symlink mirrors with one planted file, and by counting the cell census.
- The A/B measurement directories are the author's run storage, not public evidence. Their route status reports and cell censuses are therefore cited by the content quoted here, not by a published digest.
- The planted route status variants use counts and labels copied from the real report. The "some unrouted pins" and "unrouted nets" rows are written in the report's layout from the vendor's documented labels, not captured from a failing run.
- Not run, as instructed: the full suites, `run_all_suites.sh`, `syn/yosys/run.sh`, lint, xvlog, the builder bank, act and `act_ci --selftest`. The docs job's no-git variant was not reproduced; docs-check-no-git succeeded on the hosted head.
- Hosted contexts as read (`receipts/hosted_check_runs.tsv`, read at the time in `hosted_check_runs.read_at`): rtl-fast, yosys-elaboration, docs-check, docs-check-no-git, wire-accountability, full-ci-gate, all four Yosys shards and Verilator shards 0 and 3 succeeded. `elaborate` and Verilator shards 1, 2 and 4 were in progress. The `verilator-suites` and `yosys-portability` aggregates were not yet listed. "Physical gPTP" was skipped, and a skip is not hardware proof.
- Physical calibration was NOT RUN. No bitstream, hardware or bench result.

## Pending manager duties

- Hosted and act acceptance of the exact head, including the two long aggregates once emitted.
- The Vivado comparison in the merge bank for any candidate that changes RTL, the processor pin or the build recipe, per ruling (b).
- Final current-dev candidate validation at the merge turn: source base `1269cdaf`, live dev `bbf704ec`.
- After a fix round, re-review F1 and F2 at the new head. Every lens whose scope the fix touches must be covered again there.

## Probe hygiene

After all probes the clone is at the exact head and tree; the index tree is `60ca3385`. There are 0 untracked or ignored entries (the gates' `__pycache__` was removed) and 0 assume-unchanged or skip-worktree flags. All 985 regular tracked blobs rehash to their index ids with matching modes. The three required gitlinks are at their pins and clean (`receipts/restore_check.log`). The evidence branch was fetched as objects only. No GitHub write was made.

R447-2 FINISHED
