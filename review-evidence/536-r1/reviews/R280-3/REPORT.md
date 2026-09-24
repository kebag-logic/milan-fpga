[R280] POSITIVE - exact head 639fc41a41bda896cf7316d5e27d39575727efb0

# R280-3: composition review of issue #536 / PR #543 on the merge-train candidate

- Candidate: `639fc41a41bda896cf7316d5e27d39575727efb0`, tree `e4cd9ffb49baebd5add305f62f6f42892fb42d58`.
  - First parent: `8b7be584da62657f9767ad07e294d278144869c5`, the queued train (#117, #387, #394/#510/#511).
  - Second parent: PR source head `fb84de54ee9c1e3a2b51d2a239efbc04e4a22bad`.
- Source base: `26d855a9176d63625e6635a029a0c44e3d57ce9a`.
- The train's first stage `5c51569b` has the same tree as live dev `615b5a5d` (`ad69eb9f`). The candidate is therefore live dev's content, plus the queued predecessors, plus this PR (`composition.txt`).
- Scope: composition acceptance only. The source head carries two independent POSITIVE source rounds, R280-2 and R281-2, both at `fb84de54`.
- Verdict meaning: the composed tree introduces no defect beyond the reviewed sources.
- All five lenses were applied. No BLOCKER, MAJOR or MINOR is open. One new SUGGESTION is recorded.

## Reconstruction order

1. `AGENTS.md`, and `CONTRIBUTING.md` sections 2.1, 3 and 6.
2. `docs/README.md`.
3. Issue #536:
   - the body and its three acceptance criteria;
   - the [A10] assignment;
   - the [A223] and [A230] TAKEN and REVIEW READY comments;
   - the #510 decision it cites.
4. The PR #543 body and the review-start notice.
5. The linked authorities:
   - the pinned engine at `424c688`: `hdl/aecp/KL_aecp_engine.sv`, `hdl/aecp/ucode/gen_ucode.py` and `hdl/packet_engine/KL_pp_rx_validator.sv`;
   - `docs/reference/MILAN_FEATURE_STATUS.md` and `milan_feature_status.json`;
   - the compliance matrix;
   - `FR_NFR.md` FR-MVU-01 to 03.
6. `git diff 8b7be584..639fc41a` and the history of both sides.
7. The public evidence tree `review-evidence/536-r1` at `765cb958`, and the exact-head hosted check runs.

I wrote my verdict and ledger before reading any prior review finding (`ledger_before_prior_findings.md`, stamped 07:23:41 +02:00). I read R280-1, R281-1, R280-2 and R281-2 only after that.

## Composition analysis

| Question | Result | Receipt |
|---|---|---|
| Files this PR changes | `docs/MILAN_V12_ROADMAP.md`, `tests/README.md`, `tests/features/aecp_response_contract.feature`, `tests/steps/aecp_engine_model.py`, `tests/steps/aecp_engine_steps.py` | `composition.txt` |
| Files a queued predecessor also changed | **One path: `docs/MILAN_V12_ROADMAP.md`.** #394/#510/#511 edits Section 5: the CRF paragraph at :437-439 and the not-SHALL table at :471-476. This PR edits Section 6, row :541. The hunks are disjoint. | `composition.txt` |
| Composed patch against the PR patch | Identical, except for the roadmap blob ids and a hunk offset of +2 lines | `composition.txt` |
| Candidate tree against a clean merge | `git merge-tree --write-tree 8b7be584 fb84de54` returns `e4cd9ffb`, the candidate tree. No conflict was resolved by hand. | `composition.txt` |
| Suite inputs, source against candidate | Byte-identical: the `tests/` subtree (`9264168a`), the `protocol-processor` gitlink (`424c688`), `milan_feature_status.json` and `check_feature_status.py`. The train moves only the gptp-processor gitlink (`c1b61743` to `e5dcea6e`). That is a predecessor's change, and this PR's steps do not read it. | `composition.txt` |
| Semantic interaction: MVU wording | The predecessor's text says MVU `0x0001` to `0x0004` "answer NOT_IMPLEMENTED with the command echoed", in roadmap :471-472, compliance matrix :136-137, FR-MVU-02 and the feature-status note. This PR's rows `aecp_response_contract.feature:134-139` assert exactly that, each at its own figure's length. The ledger's `served_mvu_operations` is `["GET_MILAN_INFO"]`, and `SERVED_MVU` (`aecp_engine_steps.py:276`) is `{0x0000: GET_MILAN_INFO}`. They agree. | `gates_candidate.log` (feature_status, behave) |
| Semantic interaction: shared registries and gates | The ledger's `fact_documents` list the roadmap for `served_mvu_operations`. `check_feature_status.py` AST-parses `SERVED` out of this PR's step module and reports 0 findings; its self-test passes 46/46. `pp_srcs.py --check` keeps the step module under its existing `PROSE_OK` entry. Neither side changes a ratchet budget, and every ratchet holds on the combined tree. | `gates_candidate.log` |
| TOC, anchors and docs tables | `gen_toc.py --verify-anchors` and `--check` pass. The T1 row `tests/README.md:90` says 59, and the run gives 59 scenarios and 435 steps. The dated total of 312 at `tests/README.md:80,128` predates this PR (R280-O2). | `gates_candidate.log` |
| Workflow and record pins | Neither side touches `.github/workflows` or any pin record. `ci_events.py --check` exits 0. | `gates_candidate.log` |

## Gates run on the candidate

`gates.sh` ran 27 gates in the foreground at `639fc41a`. Every one exited 0 (`gates_candidate.log`):

- `git diff --check 8b7be584 HEAD`.
- `docs_check.py`: 0 findings over 165 md files and 850 scrubbed files.
- `check_em_dash.py`:
  - `--base 8b7be584`, the parent: 0 findings over 2 added lines.
  - `--base 26d855a9`: 0 findings over 1227 added lines on 24 pages.
  - `--selftest`.
- `check_doc_style.py`, `check_doc_paths.py`, `gen_toc.py --verify-anchors` and `gen_toc.py --check`.
- `check_feature_status.py`, and the same script with `--self-test`.
- `check_solution_docs.py`, `check_submodule_docs.py`, `check_gptp_docs.py`, `check_gptp_docs.py --with-submodule` and `gen_module_matrix.py --check`.
- `check_py_idiom.py`, `measure_naming.py --check`, `measure_fail_fast.py --check`, `check_todo_ownership.py`, `measure_test_evidence.py --check`, `check_hygiene.py --check` and `check_port_contracts.py`.
- `pp_srcs.py --check` and `ci_events.py --check`.
- behave on the contract feature: 59 scenarios and 435 steps passed.
- behave on the full suite: 14 features, 343 scenarios and 1736 steps passed. This equals the tally published at the source head.

## Disposable probes on the candidate

`probes.py` ran each arm on a scratch copy; the results are in `probes.log`. The behave arms copy `tests/` and `protocol-processor/hdl` and link the rest of the tree read-only. The em-dash arm uses a scratch shared clone. All 6 arms were exact:

| Arm | Expected failing lines | Result |
|---|---|---|
| Control, unmodified | none (59/59) | exact |
| `SERVED_MVU` also declares `0x0002` | feature :137 (row `0x0002`) and :233 (RTL gate) | exact |
| MVU dispatch arm made unreachable | :131, :150, :196, :197, :198 | exact |
| Engine copy declares `MVU_GET_SYSTEM_UNIQUE_ID_C` | :233 | exact |
| Em-dash control on the composed roadmap | `check_em_dash --base 8b7be584` exits 0 | exact |
| An em dash inserted into composed row :541 | exits 1 with 1 finding | exact |

These arms show two things. The composed tree keeps the source's failing arms for acceptance criteria 1 and 2. The docs gate judges the one composed line against the train parent.

## Findings

No BLOCKER, MAJOR or MINOR finding is open.

- **R280-3-S1: SUGGESTION, Docs, `docs/reference/MILAN_COMPLIANCE_MATRIX.md:136-137`.**
  - The predecessor's rows cite only `pp_top M4` as evidence for `0x0002`, and say "no per-command PP arm yet" for `0x0003` and `0x0004`.
  - In the composed tree, `aecp_response_contract.feature:134-139` grades all four RECOMMENDED commands, each in its own figure.
  - Impact: none on correctness. The rows are still true; they just do not point at the offline evidence that now exists.
  - Optional outcome: a later docs change could cite the feature rows beside pp_top. This does not affect coverage.

## Prior public review findings on this PR

I read these only after writing my ledger. The test files are byte-identical between `fb84de54` and `639fc41a`, so every resolution recorded at the source head still holds here. I spot-checked each one against the candidate's lines.

| Finding | Severity; lenses | Status at `639fc41a` | Evidence at this head |
|---|---|---|---|
| R280-F1 = R281-F1: the sub-decode outline pinned only 3 of its guards | MINOR; Tests, Robustness | RESOLVED | Feature :181-191 has one row per octet @22 to @27, both @26 nibbles, the one-bit @27 row, r = 1, and cdl 19. Over-length commands are served at cdl 24 and 112 (:197-198). Message types 0, 2, 4, 8, 10, 12 and 14 have rows (:219-225). The probe arm "dispatch unreachable" fails the served guard rows. |
| R280-F2 = R281-F2: rows `0x0001` and `0x0003` sent a truncated Figure 5.3 frame | MINOR; Conformance, Tests, Robustness | RESOLVED | `MVU_COMMAND_FORMS` is at `aecp_engine_model.py:688`. The rows assert cdl 28, 20, 92 and 20 (feature :136-139). The step refuses a row whose figure does not match (`aecp_engine_steps.py:392`). |
| R280-F3(a): IEEE 9.3.5.3.3 was cited for the MVU echo | MINOR; Conformance, Docs | RESOLVED | Feature :105-110 and the steps header :88-97 cite Milan Table 5.19 and IEEE 9.6 (Table 9-6, 9.6.5.3.1), and limit 9.3.5.3.3 to AEM. |
| R280-F3(b) = R281-F3: a Section 4.2.4 quotation sat under a 5.4.4.1 heading | MINOR; Docs, Conformance | RESOLVED | `aecp_engine_model.py:82-85` quotes 5.4.4.1's own sentence and attributes the SHALL to Section 4.2.4. |
| R280-S1 = R281-2 S4: the MVU gate regex parses only `[15:0]` / `16'h` | SUGGESTION; Tests | RETAINED as a suggestion | `aecp_engine_steps.py:895` is unchanged. It is equivalent at pin `424c688`. |
| R280-S2 = R281-2 S5: `SERVED_MVU` is not tied to the ledger | SUGGESTION; Tests, Docs | RETAINED as a suggestion | Both sides still hold only `GET_MILAN_INFO` in the composed tree. |
| R281-2 S1: the over-length rows stop at cdl 112 | SUGGESTION; Tests, Robustness | RETAINED as a suggestion | Unchanged, and the composition does not affect it. |
| R281-2 S2: the model answers frames larger than the 576-octet RX slot | SUGGESTION; Robustness, Tests | RETAINED; predates this PR | Unchanged. |
| R280-O1 = R281-1 S1 = R281-2 S3: the "NOTE ON THE DECODE" is stale | SUGGESTION; out of scope | RETAINED; predates this PR | Feature :32-36 is unchanged. |
| R280-O2, R280-O3 and R281-2 O4 | out of scope | Agreed | Unchanged, and the composition does not affect them. |

No prior BLOCKER, MAJOR or MINOR is open. No finding was moved to another Issue in place of a fix.

## Clean-lens results at `639fc41a`

```text
[R280] PASS Conformance - tests/features/aecp_response_contract.feature:116-160 with tests/steps/aecp_engine_model.py:448-460,542-552, against issue #536 AC1-3, the #510 decision and the predecessor's composed statements (docs/MILAN_V12_ROADMAP.md:471-472, docs/reference/MILAN_COMPLIANCE_MATRIX.md:135-137, docs/reference/FR_NFR.md FR-MVU-02, docs/reference/milan_feature_status.json served_mvu_operations) - GET_MILAN_INFO is served with the Figure 5.4 body and 0x0001-0x0004 draw NOT_IMPLEMENTED echoes; every document in the composed tree states the same MVU position; check_feature_status reports 0 findings
[R280] PASS RTL - composition.txt (protocol-processor gitlink 424c688 at base, source, parent and candidate; the PR changes no hdl/ path); pinned KL_aecp_engine.sv:702-713,1290-1296,2822-2825, gen_ucode.py:98-118,699-718, KL_pp_rx_validator.sv:545-548 - the model's sub-decode terms and E_MVUINFO constants still mirror the pin the candidate carries; the predecessors' RTL (milan_datapath.sv, KL_crf_rx.sv, gptp gitlink e5dcea6e) is outside every path this PR's steps read
[R280] PASS Robustness - the tests/ subtree 9264168a is identical in source and candidate (composition.txt); feature guard rows :179-198 and message-type rows :217-225 pass on the candidate (gates_candidate.log behave_contract); the dispatch-unreachable arm in probes.log fails exactly the served guard rows
[R280] PASS Tests - gates_candidate.log: behave_full 14/343/1736 and behave_contract 59/435 on the composed tree; probes.log: 6/6 arms exact (served-set widening, dispatch removal, engine-constant staleness gate, control); the measure_test_evidence and check_py_idiom ratchets hold on the combined tree
[R280] PASS Docs - docs/MILAN_V12_ROADMAP.md:541 (the only composed file) and tests/README.md:90 checked against the run; docs_check, check_em_dash (against the parent and against the source base), gen_toc --verify-anchors and --check, check_doc_style, check_doc_paths and check_feature_status all report 0 findings (gates_candidate.log); the em-dash arm in probes.log shows the gate judges the composed row
```

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Composition touches the lens scope? | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|---|
| Conformance | CLEAN | Yes: the predecessor's docs state the MVU position and this PR's rows assert it | feature :116-160; model :448-552; roadmap :471-472 and :541; matrix :135-137; FR-MVU-02; the feature ledger JSON | R280-3 | `639fc41a41bda896cf7316d5e27d39575727efb0` |
| RTL | CLEAN | No: the PR changes no hdl/ path and the protocol-processor pin is unchanged | gitlinks in `composition.txt`; the pinned engine, ucode and validator lines above | R280-3 for the composition; R280-2 and R281-2 for the source scope | `639fc41a41bda896cf7316d5e27d39575727efb0`; source rounds at `fb84de54` |
| Robustness | CLEAN | No: `tests/` is byte-identical | `composition.txt`; the behave contract run; the probe arm | R280-3 for the composition; R280-2 and R281-2 for the source scope | `639fc41a41bda896cf7316d5e27d39575727efb0`; source rounds at `fb84de54` |
| Tests | CLEAN | Yes: the suite runs on the composed inputs and ratchets | behave and ratchets in `gates_candidate.log`; `probes.log` | R280-3 | `639fc41a41bda896cf7316d5e27d39575727efb0` |
| Docs | CLEAN | Yes: the shared roadmap page and the docs gates | roadmap :541; `tests/README.md:90`; docs gates in `gates_candidate.log`; the em-dash probe | R280-3 | `639fc41a41bda896cf7316d5e27d39575727efb0` |

## Real limits

- **This is a composition round.** The composition cannot change the source-scope content: the test files and the processor pin are byte-identical. For that content I rely on the two POSITIVE source rounds at `fb84de54`, including their clause readings against the Milan v1.2 and IEEE 1722.1-2021 texts and their executed RTL probes.
- **What I did not run.** I did not re-read the specification texts. I did not build or run Verilator, pp_top, milan_dp, Yosys, the builder bank, xvlog or `run_all_suites.sh`. I ran no hosted, act or Docker job.
- **Which candidate this is.** The candidate is the manager's merge-train candidate: `8b7be584` plus this PR. It is not yet the final current-dev candidate. It is not on GitHub, so it has no hosted check runs.
- **Hosted evidence, inspected at the source head `fb84de54`** (`hosted_check_runs_fb84de54.tsv`):
  - Every required context concluded with success: `rtl-fast`, `docs-check`, `docs-check-no-git`, `wire-accountability`, `elaborate`, `verilator-suites` and `yosys-portability`.
  - All 5 Verilator shards and all 4 Yosys shards concluded with success. Their completion times spread over about 35 minutes, which is consistent with jobs that actually executed.
  - "Physical gPTP (nightly and manual)" was skipped and is not evidence.
- **Manager banks not verified.** I found no public comment on PR #543 or Issue #536 that records the manager's source static/builder and native banks at this candidate head. I did not verify them; I rely on the manager's statement.
- **No hardware proof.** Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Probe coverage.** The probe set is small and aimed at the composition. I did not re-run the source rounds' 40 author arms or their review arms.
- **Clone restoration.** My runs created ignored `__pycache__` directories, and I removed them afterwards. The final check in `integrity.log` shows:
  - HEAD is `639fc41a` and the index tree is `e4cd9ffb`.
  - The worktree equals HEAD. A hash-object sweep over every tracked blob finds no byte, mode or link difference.
  - No file is flagged `assume-unchanged` or `skip-worktree`.
  - The protocol-processor (`424c688`) and gptp-processor (`e5dcea6e`) checkouts match their gitlinks and are clean.

## Pending manager duties

- At the merge turn, build the final current-dev candidate: live dev (`615b5a5d` at review time) plus the train. Run the full local bar on it. If dev has moved past `615b5a5d`, redo the overlap check for this PR's five paths.
- Complete hosted and act acceptance of the exact merge head.
- Obtain explicit maintainer merge authorization.
- After the merge, run post-merge containment (`check_merge_containment.py`, `check_merge_review_integrity.py`) and move the card.
- Optionally, route R280-3-S1 and the retained suggestions (R280-S1 and S2; R281-2 S1, S2 and S3; O4) to Issues.

## Receipts (listed in `MANIFEST.sha256`)

- `composition.txt`
- `gates.sh` and `gates_candidate.log`
- `probes.py` and `probes.log`
- `integrity.log`
- `hosted_check_runs_fb84de54.tsv`
- `ledger_before_prior_findings.md`

R280-3 FINISHED
