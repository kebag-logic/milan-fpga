[R276] POSITIVE - exact head e1333a144115f074f8e3bdcd1de2d3a29d7f9dfd

Round R276-8 is the cleared-context composition review of issue #387 / PR #555. It covers the merge-train candidate `e1333a144115f074f8e3bdcd1de2d3a29d7f9dfd`, tree `8ecccb1dbc1d0607ee3c8f5c7067a65f79532255`. Its scope is composition acceptance only. The verdict means this: the composed tree introduces no defect beyond the reviewed PR source `00db64eb1e6e0c9bdb9f35ec5e37ebe6e00d550b` and its predecessors.

## What the candidate is

The facts are in `receipts/base_facts.txt` and `receipts/merge_tree.txt`.

- **Parents.** The first parent is `44873590`, the validated #408 candidate. The second is the PR head `00db64eb`.
- **The first parent matches live dev.** Live dev `ffcbd33d` (PR #535 merged) has tree `5b0645c8`. That is byte-identical to the first parent's tree. So the candidate tree is exactly live dev plus this PR.
- **The merge is clean.** Running `git merge-tree --write-tree 44873590 00db64eb` independently gives `8ecccb1d` with no conflict, which equals the candidate tree. No hand resolution is present.
- **The PR's merge base with dev** is `57456af9`. Since then, the predecessor side changed 10 files and the PR changed 31 (`receipts/overlap.txt`).

## Files both sides changed

The manager's list is confirmed with `git diff --name-only` (`receipts/overlap.txt`):

| File | Other side | Composition check |
|---|---|---|
| `docs/testing/CI_WORKFLOWS.md` | dev (containment) and #408 | Both sides' hunks are carried byte-exact. The PR's hunk is the `milan_dp` budget table and the samples at :156-192. The predecessors' hunks are at :1154-1155 and :1780-1786. The regions are disjoint and nothing cross-references between them. |
| `docs/testing/RUNNING_TESTS.md` | dev (containment) | Carried byte-exact. Dev's five lines at :76-80 shift the PR's deadline sentence from :79 to :84-85. The paragraph still reads in order. |
| `docs/integration/BAREMETAL_FIRMWARE.md` | #408 | Carried byte-exact. The PR's four constraint rows sit at :1359-1362 inside #408's rewritten refusal table. The PR's control paragraph sits at :1406-1412, before "The listed refusals bound only...". It does not contradict #408's "retired onto instruments" text. |
| `sw/builder/test_builder.py` | #408 | Carried byte-exact. The PR's pins sit in #408's `assert_boot_contract`, at :10527-10552. Its eight mutation entries (seven new, one re-pointed) sit in the `mutations` tuple, which opens at :14393 and is iterated at :15651. The entries are at :14616-14650. |

`receipts/side_preservation.txt` shows, for each of the four files, two equalities:

- diff(other parent to candidate) = diff(merge base to this side);
- the same with the sides swapped.

Hunk bodies are compared with line numbers stripped, so each side's change reaches the candidate unchanged. Two negative controls prove the check can fail: swapping the candidate for either uncomposed parent turns the check to `DIFF`, exit 1 (`receipts/side_preservation_controls.txt`). Two more results are in `receipts/one_side_files.txt`:

- all 27 files only the PR changed equal their `00db64eb` blobs;
- all 6 files only the predecessors changed equal their `44873590` blobs.

## Semantic interactions checked

- **Gate 1b** reads the composed `test_builder.py`, the composed `BAREMETAL_FIRMWARE.md` and the PR's `milan_datapath.sv`. The gate was run alone on the candidate in two modes:
  - **With an RV32 compiler:** `receipts/gate1b.log` reports 287/287 mutations rejected, 53/53 RTL variants elaborated with Verilator 5.050, and 0 arms NOT RUN.
  - **With every cross compiler masked** (the docs job's mode): `receipts/gate1b-no-rv32.log` reports 229/229 mutations rejected, 53/53 elaborated, and the one registered NOT RUN, the compiled census.
  - **The PR's gate text is live.** Both logs print its structural statement, "the exact PHC-net census admits media_rebase_p_w ... never GM identity; restart combines it ungated". So the PR's pins and controls run inside #408's reworked gate. The firmware page's "Their structural checks also run without an RV32 compiler" (:1412) holds on the composed tree.
- **Mutation list.** Each of the PR's eight labels occurs exactly once, inside the iterated tuple (`receipts/pr_mutant_labels.txt`).
- **Workflow and prose pins.** `ci_events.py --check` passes: 1647 contract items across 4 workflow files and `CI_WORKFLOWS.md`. `--selftest` passes with 2188 arms.
- **Runner budget.** `measure_test_evidence.py` passes `--check` (runner contract OK, ratchet PASS) and `--selftest` (101/101). This pins the composed 3600 s `milan_dp` budget.
- **Runner preflight.** `run_all_suites.sh` carries the PR's budget, and its preflight runs dev's changed containment self-test. That self-test and the other preflight gates pass on the candidate: `check_merge_containment.py --selftest`, `suite_tally.py --selftest`, `suite_shards.py --selftest` and `test_suite_cancellation.py`. `--shard 0/5 --list` also runs.
- **Navigation and style.** These all pass on the composed pages:
  - `gen_toc.py --check`: 107 pages;
  - `--verify-anchors`: 167 cross-page fragment links;
  - `--selftest`;
  - `check_em_dash.py --base 44873590`: 0 findings over 181 added lines. That is the same 181 lines the source review counted against `57456af9`, so the composition adds exactly the PR's Markdown lines;
  - `check_em_dash.py --base 57456af9`: 0 findings over 740 lines;
  - `check_em_dash.py --selftest`: 339/339 arms;
  - `check_doc_style`, `check_doc_paths`, `gen_module_matrix --check` and `check_gptp_docs`.
- **Documentation and privacy.** `docs_check.py` passes in both modes: Git, with 0 findings across 165 md and 860 scrubbed files, and no Git, from an archive of the exact head. `check_feature_status.py` passes in both modes. `check_baremetal_only.py` passes `--check` and `--selftest`. `check_py_idiom`, `check_rtl_source_lists` and `git diff --check` pass against both bases.

All 31 gate receipts are in `receipts/gates/`, indexed with exit codes in `receipts/gates/summary.tsv`. Every exit is 0.

## Findings

None at MINOR or above. This round raises no new SUGGESTION.

## Prior public review findings on this PR

I read these after my own pass over the diff. Spot checks at this head are in `receipts/prior_findings_spotcheck.txt`.

| Round | Finding | State at this head |
|---|---|---|
| R276-4 F1 BLOCKER, R277-3 F1 BLOCKER | The builder pinned the pre-#387 render trigger | Resolved. `test_builder.py:10529` and `:10548` pin the decided expressions, and gate 1b passes in both modes on the composed tree |
| R276-4 F2 MINOR, R277-3 F3 MINOR | "Pending" ended at adoption, not at the wire | Resolved. `KL_media_clock_restart.sv:66-84` states the wire boundary. tkdiag runs on the candidate: 96/96 checks, including T17 and T18, and all four planted engine defects are caught (`receipts/tkdiag.log`) |
| R276-4 F3 MINOR, R277-3 F4 MINOR | The render banner and port spec named GM identity | Resolved. See `KL_render_setpoint.sv:82-83`, `:120-121` and `:170-171` |
| R276-4 F4 MINOR, R276-5 F1 MINOR, R277-4 F2 MINOR | The `milan_dp` margin was stale, then under 10% | Resolved by decision 5820240308. `CI_WORKFLOWS.md:159-192`, `run_all_suites.sh:245`, and the runner contract passes |
| R277-3 F2 MINOR | No check for a settime's `mr` toggle | Resolved. `sim_main.cpp:1036-1067`. This file is byte-identical to the source |
| R276-5 F2 MINOR | `FPGA_DESIGN.md` gated `mr` on the selection | Resolved. See `FPGA_DESIGN.md:178` and `MILAN_V12_ROADMAP.md:360` |
| R277-4 F1 MINOR | `is_fresh()` misread nested make output | Resolved. `gmstep_mutants.py:191` passes `--no-print-directory -s` |
| R276-6 F1 MINOR, R277-5 F1 MINOR | The 2700 s budget was still stated as current | Resolved. The only `2700` left in docs, scripts and tb are the two history lines, `CI_WORKFLOWS.md:167` and `:185`, and the planted self-test mutation, all kept by the round-4 assignment. The dev insertion moved the fixed sentence to `RUNNING_TESTS.md:84-85` |
| R276-7 S3 SUGGESTION | `TESTING.md:259` could cite decision 5820240308 | Retained, optional. No predecessor touches `TESTING.md` |
| Earlier S items (R276-4, R276-5, R277-3, R277-4) | Various optional suggestions | Dispositioned by later rounds. I did not re-verify each suggestion individually; none affects coverage |

## Lens results at this head

- `[R276] PASS Conformance - sw/builder/test_builder.py:10527-10552, docs/integration/BAREMETAL_FIRMWARE.md:1359-1362, receipts/gate1b.log, receipts/gate1b-no-rv32.log - the decided #387 trigger set (issue comments 5814963103, 5817362105; decision part b) is still enforced by the composed #408 gate: re-base = adjtime | settime; render = re-base | settled source, no GM term; restart ungated by selection and wired directly. The predecessors change no protocol behaviour (no hdl/, tb/, configs/ or gitlink in 57456af9..44873590).`
- `[R276] PASS RTL - receipts/one_side_files.txt, receipts/gate1b.log (53/53 option-on milan_datapath/milan_csr variants elaborated with Verilator 5.050), receipts/tkdiag.log (96/96, 4/4 mutants caught) - every RTL file is byte-identical to the reviewed source; the one composition contact, #408's RTL-contract gate reading the PR's datapath, elaborates and passes.`
- `[R276] PASS Robustness - receipts/gate1b-no-rv32.log, receipts/gates/merge_containment_selftest.log, receipts/gates/measure_evidence_check.log - the composed builder gate degrades as documented without a cross compiler (229/229, one registered NOT RUN), and the runner preflight carrying dev's containment change plus the PR's 3600 s budget passes; no input, reset or timeout path of the PR changed.`
- `[R276] PASS Tests - receipts/side_preservation.txt and its controls, receipts/pr_mutant_labels.txt, receipts/gate1b*.log, receipts/tkdiag.log, receipts/gates/ci_events_selftest.log, receipts/gates/measure_evidence_selftest.log - no mutation entry of either side was lost (hunks byte-exact, all PR labels in the iterated tuple, every mutation rejected in both modes); the PR's tkdiag arm and its four mutants run and bite on the candidate.`
- `[R276] PASS Docs - docs/testing/CI_WORKFLOWS.md:156-192, :1154-1155 and :1780-1786, docs/testing/RUNNING_TESTS.md:76-85, docs/integration/BAREMETAL_FIRMWARE.md:1354-1451, receipts/gates/ (docs_check git and no-Git, gen_toc --check/--verify-anchors/--selftest, check_em_dash vs 44873590 and 57456af9 and --selftest, doc_style, doc_paths, module matrix, gptp docs) - composed pages read coherently, anchors and TOCs hold, and every documentation gate passes.`

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Composed builder pins and firmware constraint rows against the #387 decisions; gate 1b in both modes | R276-8 (this round). Source content: R276-7 POSITIVE at `00db64eb` (comment 5822155060) | `e1333a144115f074f8e3bdcd1de2d3a29d7f9dfd` |
| RTL | CLEAN | RTL byte-identity to the source; gate 1b's 53 elaborations; tkdiag on the candidate | R276-8. Source RTL: R276-6 at `0f003fab` via R276-7 at `00db64eb` (no hdl/ change since) | `e1333a144115f074f8e3bdcd1de2d3a29d7f9dfd` |
| Robustness | CLEAN | No-compiler gate mode; runner preflight including the containment self-test | R276-8. Source: R276-7 at `00db64eb` | `e1333a144115f074f8e3bdcd1de2d3a29d7f9dfd` |
| Tests | CLEAN | Side preservation plus controls; mutation labels; gate 1b tallies; tkdiag plus mutants; ci_events and measure_test_evidence self-tests | R276-8. Source: R276-7 at `00db64eb` | `e1333a144115f074f8e3bdcd1de2d3a29d7f9dfd` |
| Docs | CLEAN | Four overlapped files, composed; 31 static gates | R276-8. Source: R276-7 at `00db64eb` | `e1333a144115f074f8e3bdcd1de2d3a29d7f9dfd` |

The composition touches every lens's scope in some way, so this round applied all five on the candidate itself. The source reviews cover PR content that is byte-identical here.

## Real limits

- **Not run:** the full builder bank (`test_builder.py` end to end), the `milan_dp` sweep including the `gmstep` leg and its controls, Yosys, and the protocol-processor and gPTP banks. They are excluded by this assignment. Every PR-owned `tb/` and `hdl/` file is byte-identical to the reviewed source, and the predecessors change none of them or their build inputs. So their source evidence carries over, but I did not execute it on this tree.
- **Compiler identity.** The compiler-present gate 1b run used a local Buildroot `riscv32-linux-gcc` 14.3.0. I did not verify its identity against the pinned SDK. The masked run matches the hosted docs job's no-compiler mode.
- **First-parent tally not run.** A gate 1b run on the first-parent tree, meant to compare tallies, stopped for an environmental reason: the submodule copies had no Git metadata (`receipts/gate1b-first-parent.log`). The byte-exact hunk check and the label census replace it.
- **Host compiler observation (outside this PR).** On a host whose only cross compiler is an unpinned newlib `riscv64-elf-gcc`, gate 1b refuses on an `__errno` store in `parse_u64()`, where the declared residual is `__errno_location`. That code and that residual are unchanged by this PR, so this is not a finding against it. It is recorded for triage.
- **No hosted run covers this composition.** The hosted runs on `00db64eb` were created at 20:50:04Z, before #408 merged at 21:23Z. GitHub's merge ref `66972b69` still has parents `573f0052` and `00db64eb`. 21 contexts succeeded; `Physical gPTP (nightly and manual)` was skipped.
- **Manager's bank evidence not found.** I could not find public evidence of the manager's bank at `e1333a14`. The linked tree `9028ea6d` archives the source rounds through `00db64eb`.
- **Second source POSITIVE not yet public.** At review time the only public POSITIVE at `00db64eb` is R276-7. R277-6 started at 21:28:51Z and had not reported.
- **Physical calibration NOT RUN.** Field skips are not hardware proof. #387 acceptance 4 (the bench handover measurement) belongs to #117.

## Pending manager duties

- Publish or confirm the second independent source POSITIVE (R277-6 or equivalent) before merge.
- Hosted and act acceptance on this candidate. No hosted run has covered the composition with #408.
- Rebuild the final current-dev candidate at the merge turn. If dev is still `ffcbd33d`, the tree must equal `8ecccb1d`.
- Post-merge containment and review-integrity audits.
- The bench acceptance under #117.

The clone was restored after the probes, and `receipts/verify_restore.txt` checks it:

- HEAD, tree and index are exact;
- every tracked blob hashes to its index entry, with modes matching;
- there are no untracked or ignored files;
- the `gptp-processor` `e5dcea6e`, `protocol-processor` `09f9bf38` and `third_party/verilog-axis` `48ff7a7e` gitlinks are checked out clean;
- `external` `efeb541a` is uninitialised, as at the start.

R276-8 FINISHED
