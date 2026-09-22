[R254] POSITIVE - exact head f01f237d4b48c7b1ed59c80aca51430901791624

R254-1 is an internal source review of issue #439 / PR #525. Tree: `ff1c54c52cbb196db754ce6999c661730a3d0e94`; sole parent and actual source base: `483a133ed08867ea0d300d2b4a027b5b48a4282f`. All five lenses were independently applied. There are no open BLOCKER, MAJOR or MINOR findings against this source scope. One previously optional diagnostic SUGGESTION remains optional. This verdict does not approve a later #504 composition or authorize merge.

The public [assignment](https://github.com/kebag-logic/milan-fpga/pull/525#issuecomment-5783912293), [frozen issue](https://github.com/kebag-logic/milan-fpga/issues/439), [SHA scope decision](https://github.com/kebag-logic/milan-fpga/issues/439#issuecomment-5772547851), and [source-lane decision](https://github.com/kebag-logic/milan-fpga/issues/439#issuecomment-5782501927) establish the task. I read RTK.md, AGENTS.md, CONTRIBUTING.md, docs/README.md, REQ-VER-01/02/04, CI_WORKFLOWS items 4/7/11/12 and One authoritative SHA, and the submodule boundary authority before evaluating the diff and executable evidence. Public metadata, decisions, the linked R220 review and the PR521 diff are saved in `public/`. PR525 has no submitted or inline reviews in the captured APIs. No private transcript, scratchpad, author contact or other agent supplied evidence.

[R254] PASS Conformance - `REQUIREMENTS.md:215`; `docs/testing/CI_WORKFLOWS.md:333`, `:417`, `:635`, `:717`, `:768`, `:939`; `scripts/ci_events.py:2034`, `:3738`, `:3816` - every frozen content-pin acceptance criterion is met at this head.

The scope was fixed from issue439 and policy before inspecting the records: four full-workflow jobs, three fast-workflow jobs, and only the named SHA publisher in full-ci-gate. My own YAML enumeration and shell-whitespace normalization compared every actual scoped run body with its literal record. No expected record was generated from a candidate workflow during checking. Shared constants are existing specialized literals or newly written fixed tuples, not reads from workflows. [inventory.json](receipts/inventory.json) retains all raw scripts, literal normalized records and identities.

| Job | Actual 1-based run-step positions | Bodies | Normalized lines |
|---|---|---:|---:|
| verilator-shards | 2, 3, 5, 6, 7, 9, 10, 11, 12, 13 | 10 | 70 |
| verilator-suites | 3, 4, 5 | 3 | 15 |
| yosys-shards | 2, 3, 5, 6, 7, 9 | 6 | 40 |
| yosys-portability | 3, 4, 5 | 3 | 17 |
| verilator-lint | 2, 4, 5, 6 | 4 | 15 |
| bdd-conformance | 2, 3, 4 | 3 | 3 |
| yosys-elaboration | 2, 4, 5, 6, 7, 8, 9, 10 | 8 | 40 |
| full-ci-gate | 2 | 1 | 8 |
| Total | | 38 | 208 |

Acceptance disposition:

| Frozen criterion | Result and evidence |
|---|---|
| AC1: every seven-job body and sibling SHA body uses the #407 form | All 38 tuples equal independently normalized actual scripts; shared `check_carrier_script` is called through real sequence coverage. |
| AC2: changed command refused by job/step | All 208 lines independently swallowed, deleted and replaced; exact first-difference diagnostic required, plus 190 whole-body/append/prepend/empty controls. |
| AC3: nonvacuous records | All 38 records tested through full `check`: missing, empty, blank, space-only, raw string, list, dict, mixed-type tuple and stale tuple. Each refuses through its own record or content diagnostic. |
| AC4: pristine green; prior arms preserved | Source CLI `--check`: 1589 items, exit 0. Default `--selftest`: 2135 arms, exit 0. Exact base: 1513 items / 1150 arms. All 1051 original mutation names, edits and required reasons are identical and still detected. |
| AC5: SHA negatives, every-line swallowing, maintenance and truthful policy | Both SHA escapes reproduce green at base and refuse at source; all eight SHA lines tested; matching script/record CLI maintenance passes; changed documentation describes executed scope. |

The on-disk CLI SHA receipts name `full-ci-gate`, step 2, and the actual first differing normalized line:

- Entire mismatch block removed: exit 1; line 4 must be `if [ "$head" != "$GITHUB_SHA" ]; then`; found the target_sha publication. Base CLI exits 0.
- Mismatch `exit 1` replaced by `true`: exit 1; line 6 must be `exit 1`; found `true`. Base CLI exits 0.

See [disk-results.json](receipts/disk-results.json), `source-drop-block--check.stdout` and `source-exit-true--check.stdout`. The full checker produces the new comparison refusal for both, without relying on an unrelated refusal.

[R254] PASS RTL - [scope-preservation.json](receipts/scope-preservation.json), `scripts/ci_events.py:2350`, `:3190`, `:3966`, and [probe-summary.json](receipts/probe-summary.json) - workflow execution, product RTL/interfaces, processor populations, existing specialized pins and membership authority are preserved.

Only `scripts/ci_events.py` and `docs/testing/CI_WORKFLOWS.md` differ across all 855 tracked entries. The four workflow blobs, act_ci.py, every budget and every gitlink are unchanged. Carrier records equal base by value. Removing only newly added `run` fields from the RTL tables reproduces the old tables exactly, including the physical-leg records. The comparison also proves 325 existing function bodies unchanged after excluding docstrings. Only `check_carrier_steps`, `_mutations` and `selftest` change; five new helpers are test-only. Of 172 pre-existing module assignments, only the two RTL record-table ASTs change. The normalizer, specialized comparisons, CLI and return-code interface are unchanged. Membership continues to read live jobs independently of these records. Product clocks, resets, CDC, wire behavior and backpressure are inapplicable to this diff; the complete tree comparison, unchanged workflows and gitlinks are the artifacts establishing that scope.

[R254] PASS Robustness - `scripts/ci_events.py:3190`, `:3738`, `:3796`, `:8091`; [independent-probes.json](receipts/independent-probes.json) and [disk-results.json](receipts/disk-results.json) - malformed inputs and records fail closed; normal maintenance and supported whitespace remain accepted.

The independent sweep has 1280 cases, including 624 per-line edits, 342 malformed/stale-record cases, 38 sequence-maintenance positives and whitespace checks on all 38 bodies. Missing/non-string live run bodies refuse through identity checks. NBSP, CR and U+2028 refuse. Blank lines, indentation and tabs pass for every actual body. Continuations normalize identically; splitting the first command word retains two pre-existing specialized full-check refusals (`yosys-shards` step 9 and `yosys-elaboration` step 2), identically at base and head, while sequence content comparison accepts. This is an existing full-check limit, not evidence of changed normalization.

Matching additions to a worker fetch script and to the sibling SHA script pass both real CLI modes (2140 and 2138 maintenance selftest arms respectively); either side edited alone fails. Separately specialized contracts still constrain maintenance, as the policy states.

[R254] SUGGESTION Robustness - `scripts/ci_events.py:7606`, `:7643`; [malformed-results.json](receipts/malformed-results.json) - retain R220's optional malformed-pristine selftest diagnostic improvement.

Authority/evidence: the [linked R220-2 review](https://github.com/kebag-logic/milan-fpga/pull/505#issuecomment-5772521129) classified this as SUGGESTION Robustness. I reproduced a blank carrier body and a carrier missing its name at this exact head. `--check` refuses each with exit 1; default `--selftest` fails with IndexError / KeyError respectively. Impact: a traceback replaces a structured selftest explanation; no false pass occurs. Required outcome for approval: none; optional improvement is a named malformed-pristine selftest refusal. Verification of a future improvement: both saved malformed controls must remain nonzero and print the intended structured diagnostic. This retained SUGGESTION does not prevent clean lens coverage.

[R254] PASS Tests - `scripts/ci_events.py:7658`, `:7675`, `:7693`, `:8091`, `:8208`, `:8271`; [prior-arms.json](receipts/prior-arms.json), [new-arms.json](receipts/new-arms.json), [cli-results.json](receipts/cli-results.json) - normal default selftest owns the new controls, old reasons remain intact, and independent weak validators are detected.

I compared every prior mutation's edited world and required reason against base and required the same reason from the candidate checker. For each of the 756 new mutations, I independently identified the single changed actual script and computed the first difference; its required reason exactly equals that result. Default selftest adds 756 content mutations, 228 record/maintenance controls and one whitespace control. All 1150 prior arms remain; all 1151 original emitted success markers remain after normalizing only the vacuity marker's larger population count. Exact-base input files were reconstructed from Git, and their CLI output matches the baseline comparison receipts.

Nine independently selected checker weakenings ran through the real CLI, on disposable Python copies. The table counts failures naming new `rtl-script-439` controls, rather than unrelated legacy failures:

| Weakening | Pristine check exit | Default selftest exit | New-control failures |
|---|---:|---:|---:|
| accept-truncation | 0 | 1 | 63 |
| accept-extension | 0 | 1 | 38 |
| only-line-count | 0 | 1 | 510 |
| unordered-lines | 0 | 1 | 25 |
| ignore-comments | 0 | 1 | 6 |
| ignore-interior-swallow | 0 | 1 | 170 |
| disconnect-seven | 0 | 1 | 911 |
| disconnect-sha | 0 | 1 | 35 |
| missing-record-accepted | 0 | 1 | 114 |

The disconnect-seven and disconnect-sha variants remove the respective call conditions. Other variants test length, order, comments, interior swallowing and missing-record enforcement. Every expected mutant exit 1 is detector evidence, not a passing source gate. Specialized findings cannot satisfy the new mutation reasons. No workflow command, compiler bank, native bank or host orchestrator was executed by these probes.

[R254] PASS Docs - `docs/testing/CI_WORKFLOWS.md:768`, `:927`, `:947`, `:1070`; [gate-results.json](receipts/gate-results.json), [inventory.json](receipts/inventory.json) - every changed coverage and maintenance statement agrees with executed inventory and controls.

Both changed documentation hunks accurately describe the seven jobs plus sibling SHA step, existing normalization, independent specialized pins, record failures, first-line diagnostics, default control ownership and matching maintenance. Six focused reviewer gates pass: docs_check, gen_toc --check, gen_toc --verify-anchors, check_py_idiom without unsupported flags, check_em_dash against the exact base, and git diff --check. No new budget, exception, obsolete authority or hardware claim is introduced.

Prior public finding disposition at this exact head:

| Earlier finding | Original severity / lenses | Disposition at f01f237d4b48c7b1ed59c80aca51430901791624 |
|---|---|---|
| Issue439 recognized RTL content gap and added sibling SHA escapes | Frozen task defect | Resolved by the 38 records and the independent per-line, record and SHA CLI probes. |
| R219/R220 F1, old shape-gate paragraph said scripts were not pinned | MINOR / Docs | Remains resolved: CI_WORKFLOWS:1070 names recorded shape gates and their content/maintenance policy; focused docs gates pass. |
| R220 F2, only last-line swallowing tested | MINOR / Tests, Conformance | Remains resolved: unchanged `_carrier_script_edits` covers non-last lines; all old arms/reasons preserved. New RTL coverage includes every line; interior-swallow weakening produces 170 new failures. |
| R220 F3, inaccurate residue omitted sibling SHA gap | MINOR / Docs | Resolved here: CI_WORKFLOWS:768 explicitly names sibling content coverage, and both originally escaping assertions now refuse. No relabeling of its original Docs attribution. |
| Earlier append/reorder, coverage-list and maintenance suggestions | SUGGESTION / Tests or Docs as originally filed | Adopted behavior remains: preserved old controls, explicit coverage and matching-update remedy; append/order CLI weakenings fail. |
| R220 malformed-pristine traceback suggestion | SUGGESTION / Robustness | Retained optional, reproduced and described above. |

Public full-source evidence was read from immutable [ff790f6a review-evidence/439-r1](https://github.com/kebag-logic/milan-fpga/tree/ff790f6a12e40b1cd855800ae99a527495d57eb7/review-evidence/439-r1). All 133 downloaded files were checked against their Git blob IDs; see [public-downloads.json](receipts/public-downloads.json). The manager's result arrays bind 48 static/builder commands and five native commands to this source and dev483, all with process exit 0. I read their raw logs and integrity records rather than rerunning those banks. The native evidence records 55 parent suites, 14903 protocol checks with no failures, gPTP make completion, uncached Yosys results and 316 passing BDD scenarios. Scoped Verilator 5.050 identity is manager evidence; this Python/document review did not invoke Verilator.

These results preserve their limits: builder gate 11 physical calibration is NOT RUN; four parent field/freshness skips contribute no hardware proof. The xvlog result retains four pre-existing processor findings at its unchanged ratchet. These are neither newly resolved defects nor a physical acceptance claim. All original author setup/control failures and the review harness's own four unsuccessful attempts retain attribution in [FAILURES.md](FAILURES.md), with raw stderr and archived scripts. No setup failure is credited as a successful detector.

The only #504 conflict evidence used is the public PR521 diff saved in `public/pr521.diff`: its shared-file hunks concern non-RTL SDK records/controls and SDK documentation. That supports a distinct source lane; it proves no later semantic composition. After #504 lands, the actual current-dev candidate requires fresh affected-artifact review and validation. External R255 Opus remains pending availability and is not waived. Trusted replica, hosted contexts, final current-dev candidate, authorized merge and containment remain manager work. No Actions/run/check/status APIs, gh run, gh pr checks, Docker/act, candidate act_ci execution or selftest, privilege, shared installation, hardware, source fix, commit, push, other checkout edit, public write or metadata mutation was performed.

Reviewer-owned completion ledger (source coverage only):

| Lens | Covering round | Exact covered head | Status |
|---|---|---|---|
| Conformance | R254-1 | f01f237d4b48c7b1ed59c80aca51430901791624 | CLEAN |
| RTL | R254-1 | f01f237d4b48c7b1ed59c80aca51430901791624 | CLEAN |
| Robustness | R254-1 | f01f237d4b48c7b1ed59c80aca51430901791624 | CLEAN |
| Tests | R254-1 | f01f237d4b48c7b1ed59c80aca51430901791624 | CLEAN |
| Docs | R254-1 | f01f237d4b48c7b1ed59c80aca51430901791624 | CLEAN |

These five source rows do not preapprove any changed artifact at a later head. The overall issue/merge bar remains incomplete for the pending work above.

Final direct integrity verifies all 855 parent entries (851 blob entries plus four gitlinks), file bytes, regular/symlink kind, executable modes, exact stage-0 index tuples and the three required submodule populations. The independently checked pins are protocol-processor `424c688fa2205b934a7689a58f2aa766420f2326` (222 files), gptp-processor `c1b617435824929a790739ea8585c3fe1a328cc0` (103), and verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce` (214). Source tracked status is clean; head/tree remain the assigned objects. The optional external gitlink is unchanged and uninitialized. See [initial-integrity.json](receipts/initial-integrity.json), [final-integrity.json](receipts/final-integrity.json), and final explicit-field PR metadata. Reproduction commands and bounded scripts are in [COMMANDS.md](COMMANDS.md). Maximum probe concurrency was four; total concurrent focused child jobs remained below eight.

R254-1 FINISHED
