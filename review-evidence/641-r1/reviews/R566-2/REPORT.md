[R566] POSITIVE - exact head 614b4aa5f408d75673b546ce6efb6ef126437be2

# R566-2: internal independent review of PR #699 (Closes #641, #651), round 2

- **Head:** `614b4aa5f408d75673b546ce6efb6ef126437be2`, tree `6bdddb24ad611a450350c00131f64468631b889b`. Source base and live dev: `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.
- **Delta under review:** `759d1d24..614b4aa5`, three commits (`2aa74ab9`, `0c9d8589`, `614b4aa5`), 12 files. This answers assignment #641 comment 6084524982 and REVIEW READY 6085568861.
- **Reconstruction order:** AGENTS.md and CONTRIBUTING.md; docs/README.md; issue #641 and #651 bodies; the manager's scope comments 6081334020 and 6084524982; the PR body; the full diff from base to head and the round-2 delta; the public round-1 evidence tree `2f7a3d63:review-evidence/641-r1`; hosted check runs at the head.
- **Prior findings:** the R566-1 and R567-1 findings were read only after this round's independent pass.

## Verdict summary

No BLOCKER, MAJOR, MINOR or RESIDUE is open at this head. The only MINOR from round 1 (R566-1-F1 / R567-1-F1) is resolved, both round-1 RESIDUEs are resolved, and adopted suggestions S1 and S3 are implemented and proved. Three SUGGESTIONs are recorded. They are optional and leave no lens unclean. All five lenses are covered clean at this exact head.

## Prior public findings: status at this head

| ID | Round-1 severity | Status at 614b4aa5 | Evidence at this head |
|---|---|---|---|
| R566-1-F1 / R567-1-F1 | MINOR (Docs) | **RESOLVED** | See the item 1 table below. Every named authority now states that both flows refuse an active guard. A tree-wide grep finds no remaining contrary claim about `run.sh`/`ooc.sh`. The documented example returns rc 1 at width 52 and rc 0 at width 64 under both converters (`receipts/ooc_width_probe.log`). |
| R566-1-R1 | RESIDUE | **RESOLVED** | `syn/yosys/README.md:44` and `syn/yosys/enforce_elaboration.py:4` now carry the exact replacement text. The `ooc.sh:563` comment was aligned too. |
| R567-1-R1 | RESIDUE | **RESOLVED** | `tb/verilator/fw_service_budget/README.md:84-85` now reads "Two full 64 KiB slots bound WIP at 14.56 seconds. This remains below the 30-second guard." That is the exact fix, and its quantities are unchanged. |
| R566-1-S1 | SUGGESTION | **ADOPTED** (its optional half is retained as R566-2-S1) | `rtl-fast.yml:225-226` sits next to `ooc_selftest.py` and `cache_selftest.py`. Contract pins are at `ci_events.py:1252,2341,6382`. Removal, `\|\| true` and `continue-on-error` mutants are each refused (`receipts/s1_ci_mutants.log`). Hosted `yosys-elaboration` step 11 succeeded at this head. |
| R566-1-S2 | SUGGESTION | **NOT ADOPTED; retained as SUGGESTION** (it was optional) | The limitation is now documented at `syn/yosys/README.md:45-46`. The refusal of a converted guard still reads `Can't resolve task name '$error'` (`receipts/ooc_width_probe.log`, sv2v 0.0.13 rows). |
| R566-1-S3 | SUGGESTION | **ADOPTED** | `tb/verilator/pp_shadow/Makefile:108-110` follows the sibling pattern (`milan_dp_render`, `milan_dp_mclk`). The new control `scripts/entity_shape_selftest.py:426-438` passes under both Make versions. Deleting the assertion makes `MAKE=false` succeed silently (rc 0) under both, so the control can fail (`receipts/s3_assertion_mutant.log`). |

### Item 1: each current authority, re-read and checked against execution

| Authority | Now states | Checked against |
|---|---|---|
| `docs/development/CODE_QUALITY.md:1252-1268` | Both flows refuse active guards (#651). sv2v 0.0.12 preserves native `$error`, which Yosys honours. sv2v 0.0.13 emits `initial $display`, which the helper restores. Width 52 fails and width 64 passes. | `receipts/ooc_width_probe.log`. Under 0.0.12, `$error` is preserved and width 52 fails with the guard's own message. Under 0.0.13, `initial $display("Error [elaboration] ...")` appears and width 52 fails with `Can't resolve task name '$error'`. Width 64 returns rc 0 under both. `receipts/yosys_error_mechanism.log` shows that a native generate-scope `$error` prints its own message and an inactive branch passes. |
| `docs/findings/README.md:26` | "At the measurement revision, Yosys ignored converted elaboration guards. Since #651, both synthesis flows refuse active guards." | The same receipts. The historical finding is kept and framed as past. |
| `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:25,30-33,104-112` | The summary bullet is scoped to "the measured flows", with a dated note "Update 2026-10-09 (#651)". The method note is in the past tense, and the measurements are unchanged. | The historical finding is retained as instructed. Line 608 is about the sweep's own measured pipeline, so it stays accurate as history. |
| `hdl/ieee8021q/filtering/rx_mac_filter.sv:145-151` | A comment-only correction, consistent with the documents above. | `receipts/rtl_comment_only_vs_r1.log` and `_vs_base.log` show that the code bytes are identical after stripping comments, the file stays at 277 lines (line anchors unchanged), and only lines 145-151 changed. Neither the 6 tracked `.patch` files nor any exact-text table holds a removed or added comment line or a line-number reference into that span. `receipts/rx_filter_suite.log` (pinned Verilator 5.050) passes 5/5 binding-mutant anchors, 4/4 contract negatives and the legal default. |

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE.

### R566-2-S1 - SUGGESTION - Tests - `syn/yosys/guard_selftest.py:23-30,68,77` - the "native" arm does not plant the form the pinned converter emits

- **Evidence:** every fixture puts the guard inside `initial` (`guard_selftest.py:30`), so the "native" arm plants a procedural `initial $error(...)`. The CI-pinned sv2v 0.0.12 instead emits a generate-scope `$error(...)` with no `initial` (`receipts/ooc_width_probe.log`, 0.0.12 lowering lines 64-73). That is the form every hosted worker sends to Yosys. Yosys refuses it with the guard's own message, not with a message naming `$error` (`receipts/yosys_error_mechanism.log`). So the pinned path's refusal is proved by reviewer and author probes, not by a committed control. The self-test never runs the installed converter. The assertion text at `:77` still says "the fatal task" for what is `$error`.
- **Impact:** none today; every documented behaviour holds. A later change that stopped Yosys refusing the generate-scope form, or one that made the helper rewrite it, would be caught by no CI step.
- **Suggested outcome (optional):** add a generate-scope `$error` arm that requires the guard's own message. Optionally add one arm that lowers a planted guard with the installed `sv2v`. Optionally reword the `:77` message to name `$error`.
- **Verification:** the new arm passes at the head and fails when that form escapes refusal.

### R566-1-S2 (retained) - SUGGESTION - Robustness - `syn/yosys/enforce_elaboration.py:14,19` - converted refusals rely on Yosys rejecting a procedural `$error`

- The restored task is still refused through the unsupported-construct error `Can't resolve task name '$error'`, and the guard's own message is lost. This round documents the limitation (`syn/yosys/README.md:45-46`) and names the Yosys version. The original suggestion is unchanged and optional.

### R566-2-S2 - SUGGESTION - Docs - `syn/resmap/yosys_sweep.py:47-49,535-536` - the sweep driver's help text calls the conversion unenforcing without naming a version

- **Evidence:** the help text says guards are ones "that the sv2v conversion leaves unenforced". The driver runs its own sv2v-to-Yosys path (`yosys_sweep.py:441`), not `run.sh`/`ooc.sh`. So this statement does not contradict "both Yosys flows refuse active guards". It is accurate for the sv2v 0.0.13 the #649 sweep documents. Under the 0.0.12 pin, native `$error` is refused by Yosys (`receipts/yosys_error_mechanism.log`).
- **Suggested outcome (optional):** scope the sentence to the converter version, for example "that sv2v 0.0.13's conversion leaves unenforced".

## Lens results at this exact head

```text
[R566] PASS Conformance - #641 items 1-3, #651 items 1-3 at 614b4aa5 - receipts/shape_selftest_make441.log and receipts/shape_selftest_make43.log (228/228 each, stopped-parse controls and pp_shadow nested controls included), receipts/shape_gate_make441.log and _make43.log (real gate rc 0); receipts/guard_selftest.log (36 controls, both flows); receipts/ooc_width_probe.log (TDATA_WIDTH 52 refused / 64 accepted under sv2v 0.0.12 and 0.0.13); receipts/nvm_names_probe.log (KL_nvm_backend N_NAME_P 235 and 129 refused, 128 accepted, pinned converter); receipts/hosted_yosys_elaboration_steps.tsv (CI inherits: step 11 success at the head); receipts/fw_service_budget_selftest.log (55 oracle + 14 flash checks; fixture unchanged in round 2)
[R566] PASS RTL - hdl/ieee8021q/filtering/rx_mac_filter.sv:145-151, tb/verilator/pp_shadow/Makefile:107-110, syn/yosys/ooc.sh:562-563, syn/yosys/enforce_elaboration.py:4 - RTL edit comment-only with code bytes and line count identical to 759d1d24 and to base (receipts/rtl_comment_only_vs_*.log); rx_filter suite incl. binding mutants and contract negatives green on pinned Verilator 5.050 (receipts/rx_filter_suite.log); Makefile assertion matches the sibling .SHELLSTATUS pattern and is evaluated immediately after the := expansion it guards; ooc.sh/enforce deltas are comment/docstring-only
[R566] PASS Robustness - tb/verilator/pp_shadow/Makefile:108-110, syn/yosys/enforce_elaboration.py:14-19 - failed nested derivation (MAKE=false) stops the parse rc 2 with the named diagnostic under GNU Make 4.4.1 and 4.3, clean derivation rc 0 (receipts/s3_assertion_mutant.log); inactive generate branches pass and active ones refuse for native, converted-error and converted-fatal forms incl. chparam overrides (receipts/guard_selftest.log, ooc_width_probe.log, yosys_error_mechanism.log); boundary 128 accepted / 129 refused (nvm_names_probe.log)
[R566] PASS Tests - scripts/entity_shape_selftest.py:426-438,766, .github/workflows/rtl-fast.yml:225-226, scripts/ci_events.py:1252,2341,6382 - new nested-status control fails when the assertion is deleted (s3_assertion_mutant.log, both makes); CI contract 1749 items / 2374 arms pass and refuse removed, neutralised and continue-on-error variants of the new step (docs_gates.log, s1_ci_mutants.log); hosted yosys-elaboration ran the step at this head; R566-2-S1 recorded as optional
[R566] PASS Docs - docs/development/CODE_QUALITY.md:1252-1268, docs/findings/README.md:26, docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:25,30-33,104-112, syn/yosys/README.md:43-60, tb/verilator/fw_service_budget/README.md:84-85 - every sentence checked against execution receipts (table above); tree-wide grep for contrary enforcement claims clean apart from R566-2-S2 (a different pipeline, accurate for its documented converter); 25/25 documentation and CI-contract commands rc 0 incl. docs_check, em-dash --base 5603c353, doc_style, gen_toc --check/--verify-anchors, DOC_MAP (receipts/docs_gates.log, docs_gates.json)
```

## Reviewer-owned coverage ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #641/#651 acceptance; shape gate and self-test under both Make versions; guard self-test; width and N_NAME_P probes; hosted step 11; fixture self-test | R566-2 | `614b4aa5f408d75673b546ce6efb6ef126437be2` |
| RTL | CLEAN | `rx_mac_filter.sv` comment-only proof and anchors; rx_filter suite; `pp_shadow/Makefile` assertion; `ooc.sh` and `enforce_elaboration.py` deltas | R566-2 | `614b4aa5f408d75673b546ce6efb6ef126437be2` |
| Robustness | CLEAN | failed-derivation path under both Make versions; inactive/active, native/converted/fatal and override paths; name-count boundary | R566-2 | `614b4aa5f408d75673b546ce6efb6ef126437be2` |
| Tests | CLEAN | new nested-status control and its deletion mutant; CI step and contract arms with three mutants; hosted step result | R566-2 | `614b4aa5f408d75673b546ce6efb6ef126437be2` |
| Docs | CLEAN | four F1 authorities, both residues, yosys README, tree-wide grep, 25 documentation/contract gates | R566-2 | `614b4aa5f408d75673b546ce6efb6ef126437be2` |

The merge candidate must contain this head unchanged in each lens's scope. A later commit that touches any examined artifact un-covers that lens.

## Author's builder NOT RUN arm and memory peak

- **Builder arm NOT RUN: acceptable.**
  - The arm is gate 11 (`sw/builder/test_builder.py:19268-19274`). It calibrates the resource estimate against an archived place report that is not on disk.
  - It is a registered NOT RUN, not coverage, and its subject is untouched: no `sw/builder` file is in the PR diff.
  - The hosted `docs-check` job at this exact head registers the same gate 11 NOT RUN, among 17, and still passes (`receipts/hosted_builder_not_run_extract.txt`). So the gap is environmental and existed before this PR. Under the review constraints this review did not run the builder bank.
- **Memory peak of 10.08 GB against the 9 GB ceiling: a process exception, not a product or evidence defect.**
  - No OOM occurred, and the author re-ran lint with four workers to a pass.
  - Every functional result this review relies on was re-executed here, independently of the author's runs.
  - The manager should keep the incident on the lane record. It does not affect the verdict.

## Hosted CI at the exact head (read-only; executed and skipped jobs kept apart)

- **Snapshot:** taken 2026-10-09T17:26Z (`receipts/check_runs_at_head.tsv`, `receipts/gh_pr_checks.txt`).
- **Executed and successful:** `changes`, `bdd-conformance`, `verilator-lint`, `yosys-elaboration` (all steps, including the new step 11; `receipts/hosted_yosys_elaboration_steps.tsv`), `Yosys shard 0/4` to `3/4` (each running "Run this weighted portability shard"), `Verilator shard 3/5`, `docs-check`, `docs-check-no-git`, `wire-accountability` and `full-ci-gate`.
- **Skipped:** `Physical gPTP (nightly and manual)`. A skip is not evidence.
- **In progress at the snapshot:** `Verilator shard 0/5`, `1/5`, `2/5` and `4/5`, `elaborate` and `firmware-unit`.
- **Not yet created:** the aggregates `verilator-suites` and `yosys-portability`. `yosys-portability` depends on `verilator-suites`.
- This review makes no claim about the hosted `yosys-portability` verdict at this head.

## Real limits

- **Not run (by assignment):** the full builder, parent, PP, gPTP and Yosys banks, and the native or builder banks of the current-dev candidate. No manager source bank exists at this head and none is inferred.
- **Not re-run in round 2:** the full `run.sh` portability over all tops, the full OOC flow, the six-arm #649 sweep replay and the fixture rebuild. Their round-2 inputs are comment-only or unchanged, and this review reran the targeted examples instead.
- **Toolchain:** local Yosys 0.66 is a distribution build with external ABC, so byte equality with the hosted bundled-ABC build is not claimed. The GNU Make 4.3 binary came from a local container image layer, and the sv2v 0.0.12 binary is a local install; identities are in `receipts/toolchain.txt`. Neither was checked against the CI release-zip digest.
- **Hosted result cache:** the hosted Yosys shards finished in under a minute each. That suggests result-cache reuse, which is expected because comment-only RTL edits do not change converter output. This review does not judge the cached evidence's acceptability.
- **Process:** probes ran sequentially in this session, not concurrently. All mutation probes ran in disposable copies under `scratch/`.
- **Clone integrity:** the reviewed clone was verified afterwards. It is at the exact head with a clean worktree and index, the index's mode/blob/path digest equals HEAD's, and the three required submodule gitlinks match and are clean (`receipts/exact_head_restore.txt`).
- **Hardware:** no physical calibration or hardware claim is made.

## Pending manager duties

- **Hosted acceptance at this head:** collect `verilator-suites`, `yosys-portability`, `elaborate`, `firmware-unit` and the remaining Verilator shards, plus the act replica.
- **Current-dev candidate:** validate the merge candidate (builder and native banks) at the merge turn and link the receipts on the PR.
- **External round:** the external R567-2 verdict is still required.
- **Suggestions:** decide whether to carry the optional suggestions R566-2-S1, R566-2-S2 and R566-1-S2 to follow-up issues.
- **Incident:** keep the 10.08 GB memory incident on the lane record.
- **Publication:** publish this report and the MANIFEST-listed receipts. Receipts had host-specific path prefixes replaced with placeholders by `scripts/sanitize_paths.py`; only path text changed.

## Packet

`REPORT.md`, `MANIFEST.sha256`, `scripts/` (portable drivers: `run_job.sh`, `shape_make43.sh`, `shape_gate.sh`, `guard_selftest.sh`, `ooc_width_probe.sh`, `nvm_names_probe.sh`, `yosys_error_mechanism.sh`, `s3_assertion_mutant.sh`, `s1_ci_mutants.py`, `rtl_comment_only.py`, `rx_filter_suite.sh`, `docs_gates.py`, `sanitize_paths.py`), and `receipts/` (logs, rc files, JSON, hosted extracts).

R566-2 FINISHED
