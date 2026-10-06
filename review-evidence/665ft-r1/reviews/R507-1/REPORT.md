[R507] NEGATIVE - exact head 27433e47c6d7805376547a91b418cf6aa9d95d2a

External independent review, round R507-1, issue #665 / PR #675, lane FT. Tree: `b8eed7686df2a3a1980ac68f3667da45451e5e3b`. Source base: `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`.

Two independently found MAJOR findings and three subsequently published MINOR findings remain open. The two MAJOR findings concern the claimed coverage guarantee. The existing suites and coverage gate pass, but a reachable public error return is excluded and an exclusion can transfer to a different uncovered branch. Conformance, Robustness, Tests and Docs are UNCLEAN. RTL is CLEAN for this head and this lane's scope. Neither finding requires changing firmware behavior.

**Scope and independence**

Reconstruction used AGENTS.md and CONTRIBUTING.md, docs/README.md, the issue's public scope and decisions, the linked requirements and interfaces, then the exact base-to-head diff and seven-commit history. The principal scope authorities are the [unit-test directive](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6008744385), [FT assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6009234414), and [later lane acceptance decisions](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6009661573). Their text is retained in `scope-decisions.json`.

The independent diff pass, verdict and five-lens ledger were written before consulting prior PR review findings. At the initial subsequent public-thread snapshot, PR #675 had only two review-start comments and no review findings. The final thread check found the newly published R506-1 findings (comment 6011948437); they were read only after the independent verdict and ledger had been written, and are explicitly retained below. `public-evidence.json` records both snapshots. No other reviewer's report informed the independent pass. No source fixes, commits, pushes, GitHub writes, author contact or merges were performed.

After the independent pass, the review examined the [published evidence tree](https://github.com/kebag-logic/milan-fpga/tree/b7eb2edc01e87810ff3e01629af0c9bc4a9438f1/review-evidence/665ft-r1) and the public REVIEW READY comment. That tree supplies the published handoff and PR-body evidence, rather than a complete raw gate-log bank. Broad source-bank results remain reported manager/executor evidence; the focused results below were reproduced independently. Source validation is separate from the eventual current-dev merge candidate.

**R507-1-F1 - MAJOR - Conformance, Robustness, Tests, Docs**

Artifact: `sw/firmware/gtest/README.md:208`, excluding `sw/firmware/ctrl_nvm/nvm_klj2.c:350` and its return at line 351; public contract `sw/firmware/ctrl_nvm/nvm_klj2.h:106`; test caller `sw/firmware/ctrl_nvm/test/test_nvm_codec.cpp:26`.

Title: The short-loaded record-header refusal is reachable through the public codec API.

Authority/evidence: The owner directive requires tests of every public function, including every error return, and the README states that none of its exclusions is a gap a test could close. The header documents `nvm_klj2_check_body(img, img_len, loaded)` as operating on a CRC-closed container whose first `loaded` bytes are present; it imposes neither whole-image nor `NVM_STAGE_BYTES` minimum loading. The exclusion proof only considers those two callers' loading sizes.

`coverage_probes.py` compiles the unchanged C11 codec. It creates and validates a complete blank container (`nvm_klj2_check` returns OK), copies its valid 40-byte header into a 40-byte array, and calls `nvm_klj2_check_body(header, 3336, 40)`. The public function returns `NVM_VD_REC` (7). Real gcov data records both arcs of line 350 and one execution of line 351. This satisfies the CRC-closed premise without reading beyond the supplied buffer. See `coverage-probes.log`.

Impact: The reported 100% result removes a real, directly testable public error path. The existing whole-container and staged-container cases do not exercise this refusal, contrary to the lane's error-return and exclusion requirements. This is a test/measurement defect; the existing firmware correctly refuses the short prefix.

Required outcome: Add a direct public-API test for a prefix shorter than the next record header, remove this exclusion, and update the measured ratchet and coverage claims. Preserve the public contract and refusal behavior. Any intended narrowing of the public contract would need an explicit scope decision, not an implicit restriction inferred from current callers.

Verification: A valid CRC-closed image with a 40-byte loaded prefix must return REC; exercise the adjacent header boundary too. The guard's refusal must appear in actual coverage, and a planted defect that removes or misreports this refusal must fail the named test. Rerun both firmware suites, coverage and affected documentation checks.

**R507-1-F2 - MAJOR - Conformance, Robustness, Tests, Docs**

Artifact: `sw/firmware/gtest/fw_coverage.py:222`, especially lines 249-258; `sw/firmware/gtest/fw_coverage_selftest.py:106`; promise in `sw/firmware/gtest/README.md:187`.

Title: Function-wide exclusion counts can conceal loss of coverage at a different branch.

Authority/evidence: The FT assignment requires a gate refusing any coverage drop. The README additionally says a row fails when its branch becomes reachable or something else in the function goes uncovered. `apply_exclusions` checks that the fragment occurs once, but then compares only the total uncovered arcs/lines across the function and removes every zero arc and unexecuted line in that function. It never associates the removed items with the named statement.

The second part of `coverage_probes.py` uses the real compiler and gcov reader on a function with two independent conditions, `x == 7` and `x == 9`. The unchanged exclusion names only the first, with one arc and one line. The control calls 0 and 9, leaving the named condition uncovered. The second measurement calls 0 and 7: the excluded condition is now covered, while the previously covered `x == 9` branch and return are untested. Both `apply_exclusions` and the ratchet comparison return no findings; both report 5/5 lines and 3/3 branches. `coverage-probes.log` records the uncovered line moving from 3 to 5 and the uncovered arc moving from line 2 to line 4.

Impact: A newly untested reachable branch can inherit another branch's exclusion while every recorded percentage remains 100%. The existing stale-exclusion selftest changes only the named gap, so the function totals change and it cannot detect this compensating swap. CI's green measurement therefore does not enforce the documented guarantee.

Required outcome: Bind each exclusion to the actual excluded statement/condition and its permitted uncovered items, with a representation that remains correct for the supported compiler versions. Reject a change in the identity of those uncovered items even when the function's totals are unchanged. Update the documentation to match the enforced guarantee.

Verification: Add a real-gcov or equivalently faithful planted compensating-swap case. The unchanged control must pass, and the swapped gap must be refused. Also retain the existing multiline-condition, shorter-arc-vector, stale-row, missing-file and per-file-drop checks on both recorded compiler families.

**All sixteen exclusions examined**

Rows refer to the table at `sw/firmware/gtest/README.md:197` through line 212. Source paths in this table are relative to `sw/firmware/`. An accepted row below means its construction argument was checked against the named source and supported configuration, not that F2's mechanical enforcement is adequate. The state arguments assume objects maintained through their APIs, rather than arbitrary memory corruption.

| Row | Source/function and excluded condition | Judgment and examined construction |
|---|---|---|
| 1 | `ctrl/adp/adp.c`, `adp_link_change`, up while outside DOWN | Supported: initialization, enable and link-loss paths keep a recorded-down enabled instance in DOWN; only `enter_delay` exits it. |
| 2 | Same function, down while already DOWN | Supported: shutdown disables; an enabled recorded-up instance is outside DOWN before the link transition. |
| 3 | `adp_timer_expired`, DELAY with ADVERTISE timer | Supported: `enter_delay` starts DELAY; `advertise` starts ADVERTISE and enters WAITING. |
| 4 | Same function, DOWN with a timer or WAITING with DELAY | Supported: all DOWN entries stop the timer; WAITING is paired with ADVERTISE; NONE returns earlier. |
| 5 | `adp_poll`, owed AVAILABLE outside enabled DELAY | Supported: only `advertise` creates the debt; shutdown/link loss clear it; a successful send clears it before WAITING. |
| 6 | `ctrl/adp/adp_mbx.c`, `on_poll`, already-true accumulated `owed` | Supported for the present generated one-interface contract: the loop's sole initial accumulation starts false. A future interface-count change must revisit it. |
| 7 | `adp_mbx_attach`, fixed ADP receive bind fails | Supported: the generated channel is in range and the callback is non-null; poll/sink exhaustion is separately exercised. |
| 8 | `ctrl/app/ctrl_app.c`, `ctrl_app_start`, adapter initialization/attach fails | Supported: slot zero plus one interface fits sixteen timers; the app has just initialized empty loop tables. |
| 9 | `ctrl/port/ctrl_pool.c`, `ctrl_pool_alloc`, positive count with empty list | REJECTED after public-finding follow-up: the internal API invariant is preserved, but a write into a released block breaks it and reaches this documented corruption guard. R506-1-F1 is retained and independently reproduced. |
| 10 | `ctrl_nvm/nvm_klj2.c`, `nvm_shape_consistent`, order/offset/payload checks | Supported: fixed ordered blocks and static ID-range assertions, matching offset sums, and generated maximum payload constrain the iterator. The doctored-size build exercises the separate consistency refusal. |
| 11 | Same function, final record count | Supported: the iterator and `NVM_N_REC` use the same group-count constants. |
| 12 | `nvm_klj2_check_body`, header beyond `loaded` | REJECTED: F1 reproduces this through the public loaded-prefix API. |
| 13 | `ctrl_nvm/nvm_store.c`, `nvm_idle`, armed dirty window but no dirty bit | Supported: change arms with a bit; capture closes the window before clearing bits; behind-cursor changes retain their bit. |
| 14 | `nvm_framed_as`, malformed staged frame after matching first magic byte | Supported: stage spans come from blank construction, a validated boot container, or `nvm_rec_frame`; the erased case differs at its first byte. |
| 15 | `nvm_erase_start`, target equals authoritative slot | Supported: `nvm_target_slot` selects the other slot while authority exists; -1 authority cannot equal a slot. |
| 16 | `ctrl_nvm/plat/nvm_flash_litespi.c`, `ls_in_journal`, length exceeds journal | Supported: the only callers pass a checked page or one erase block, each within the two-slot journal. |

**Other lens results and port evidence**

Conformance was applied to the public acceptance, REQUIREMENTS.md, mailbox ownership/order and latency contracts in `docs/design/MAILBOX_SPLIT.md` and `adp_mbx.h`, the four existing seam headers, KLJ2 acceptance in `docs/design/SAVED_STATE_FASTCONNECT.md:685`, and DR2a/DR2b/DR2c/DR3b/DR5 in `docs/design/SAVED_STATE_MATERIALIZATION.md:2301`. No new protocol or shipping behavior is introduced. F1 and F2 prevent the coverage acceptance from being met.

[R507] PASS RTL - `tb/verilator/mbx/suite.hpp:54`, `sw/firmware/ctrl/test/ctrl_build.py:36`, `sw/firmware/ctrl_nvm/test/nvm_bench.py:182`, and the complete base-to-head path diff - No HDL, shipping source behavior, default build, reset/CDC contract, or firmware interface changes. The only production-header edits rename a test file in three comments. C firmware remains separately compiled as C11; mocks substitute the existing `mbx_hal.h`, `shlan_port.h`, `nvm_flash.h` and LiteSPI accessor seams. The shared mailbox suite retains the original assertion bodies, 14-group order and default RTL checker; the bus/co-simulation rerun corroborates that preservation. C++ allocation is confined to host test equipment; the freestanding build checks remain active locally.

Robustness was applied to abnormal tally exits, skips and disabled tests; malformed/truncated frames and records; pool overflow and invalid frees; stale timer tags, deadline wrap, owed frames and full queues; NVM boot/refusal/rollback, changed media, retries and power cuts; LiteSPI range and timeout cases; and the coverage gate's failure paths. Those paths are present in `test_adp.cpp`, `test_port_loop.cpp`, `test_unit_driver.cpp`, `test_nvm_boot.cpp`, `test_nvm_write.cpp`, `test_nvm_flashmock.cpp` and `test_nvm_litespi.cpp`. F1 and F2 remain open under this lens.

Tests were compared with the retired sources and the PR's per-check table. `port_inventory.py` records all 81 old port labels, 121 static ADP labels, 13 lwSRP labels, 125 static mailbox check labels and all 42 old NVM check names, with no missing match. This static inventory supplements examination of predicates, setup/reset order, generated fixture oracles and mutant grading; matching words alone is not semantic proof. Runtime counts intentionally change from assertions to tests: the model's 134 checks become 14 groups; the port's 81 become 29 tests including additions; ADP's 163 runtime checks become 26 tests including additions; the 320-check walk becomes 41 parameterized steps; entity fields remain 45 tests over five shapes; lwSRP's 13 checks become two tests. The NVM port preserves the 42 named checks, generally parameterized over both media paths, and adds codec, mock and shape tests. The old check framework has no live source users; the independent RTL checker remains because the RTL suites use it. Both coverage findings remain test deficiencies despite the passing mutation results.

Docs were checked against the code, PR mapping, module READMEs, new gtest README, docs index and CI policy changes. Tally counting and local-only CI arms are disclosed. The exclusion/unreachability and stale-row guarantees are measurement claims, so F1/F2 are findings rather than wording-only RESIDUE. The later public review's suggestions and wording residue are retained in the disposition below.

**Focused executable evidence**

All commands ran to completion through foreground invocations, with independent campaigns and checks concurrent where resources allowed. Every disposable build and probe was confined to packet `scratch/`. The named logs are invocation output, each paired with its `.rc` receipt; the mailbox receipt is an explicitly selected result excerpt described below. The local versions are gcc/gcov 16.2.1 and GoogleTest/GoogleMock 1.18.0 (`versions.log`).

Commands below are relative to the reviewed repository, except packet scripts. `PACKET` denotes this packet directory; set `TMPDIR=PACKET/scratch` and `PYTHONDONTWRITEBYTECODE=1`, as `run_receipt.py` does. The wrapper syntax is `python3 PACKET/run_receipt.py --repo REPO NAME -- COMMAND...`.

| Command / receipt | Result |
|---|---|
| `python3 sw/firmware/gtest/tally_selftest.py`; `tally.log` | rc 0; 11/11 intended outcomes: one passing control and ten red/refused cases, including crash, abort, early exits, skip, throw, disabled, setup failure and empty selection. |
| `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --build-dir PACKET/scratch/ctrl`; `ctrl.log` | rc 0; all requested arms pass, local RV32I build passes, 74/74 mutants killed by their named checks. lwSRP was not requested in this independent run. |
| `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 4`; `nvm.log` | rc 0; five shapes, 429 tests, required RV32 builds and all 100 planted defects pass their expected verdicts. |
| `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 8 --keep PACKET/scratch/coverage`; `coverage.log` | rc 0; all 14 files reported 100% after exclusions. This reproduces the result, not the validity of F1/F2's exclusions. |
| `python3 sw/firmware/gtest/fw_coverage.py --selftest`; `coverage-selftest.log` | rc 0; 18/18 planted cases. |
| `python3 scripts/ci_scope.py --selftest`; `ci-scope.log` | rc 0, including firmware source/test/README/ratchet paths and mutations misclassifying firmware as documentation. |
| `python3 scripts/ci_events.py --check`; `ci-events-check.log` | rc 0; 1,741 contract items. |
| `python3 scripts/ci_events.py --selftest`; `ci-events-selftest.log` | rc 0; 2,352 arms over 1,741 contract items. |
| `python3 PACKET/mailbox_review.py REPO PINNED_VERILATOR`; `mailbox-results.log`, `mailbox.rc` | rc 0; identity 5.050 verified before use; `make -j16` scoped bus and co-simulation builds, nested compilation limited to four; quick campaign `--jobs 1`; 134/179/13 checks pass and 4/4 mutants killed. |
| `python3 PACKET/coverage_probes.py REPO`; `coverage-probes.log` | rc 0 means both independent reproductions succeeded, not that the candidate is clean. |
| `python3 PACKET/public_findings_probes.py REPO`; `public-findings-probes.log` | rc 0; reproduced the published pool-guard case and the skipped-test tally defect surviving all eleven self-test cases. |
| `python3 PACKET/port_inventory.py REPO`; `port-inventory.log` | rc 0; named port inventory preserved. |
| `git diff --check BASE..HEAD`; `diff-check.log` | rc 0; no whitespace errors. |
| `python3 PACKET/verify_tree.py REPO`; `tree-before.log`, `tree-after.log` | rc 0 before and after; candidate/required submodule blob bytes, Git modes, index trees and gitlinks match. |

The mailbox result excerpt preserves raw identity, command labels, tallies, verdicts and mutant results. Build-command lines containing local installation paths remain only in scratch. The hosted result excerpt removes ANSI CSI sequences and selects version, tally and result lines; its exact selection and original log digest are in `public-evidence.json`. No omitted build output is used as a separate proof claim.

**CI evidence and limits**

The new job at `.github/workflows/rtl-fast.yml:246` installs the two distribution packages, prints their versions, runs the tally and both firmware gates, verifies the pinned RV32 SDK for NVM, and runs the coverage selftest/check. `scripts/ci_events.py` pins its steps and aggregate dependency; `scripts/ci_scope.py` covers all firmware paths. The hosted [firmware-unit job](https://github.com/kebag-logic/milan-fpga/actions/runs/37429204550/job/112155948905) ran at this exact head and completed successfully; all its listed steps executed successfully, rather than being skipped. The [rtl-fast run](https://github.com/kebag-logic/milan-fpga/actions/runs/37429204550) also completed successfully. Raw API receipts are `hosted-firmware-job.json` and `hosted-runs.json`.

The hosted log confirms gcc/gcov 13.3.0, GoogleTest/GoogleMock 1.14.0, distribution packages 1.14.0-1, passing firmware tallies and the 14-file coverage result. It explicitly skips the ctrl RV32 arm before SDK installation; NVM's required RV32 build executes. lwSRP and the two full mutation campaigns are local-only arms, as documented. No local hosted-workflow replica was executed or accepted by this review; the manager owns that evidence and hosted acceptance. At the receipt snapshot, other hosted workflows were still in progress, so no exhaustive-context success is inferred from the fast job.

The full parent, processor, timing, synthesis and builder banks were not rerun. The lwSRP adapter was read and its port checked statically, but its opt-in execution relies on public source evidence. Physical calibration was NOT RUN; field skips and model timing are not hardware proof. This lane neither closes the broader issue #665 nor establishes a new shipping image or physical performance result.

**Disposition of findings published during this review**

The source is [R506-1's public review](https://github.com/kebag-logic/milan-fpga/pull/675#issuecomment-6011948437), published at 2026-10-06 07:57:15 UTC. Its findings text is preserved in `prior-public-findings.json`. None of the following is resolved at this unchanged head. The three MINOR findings remain blocking to clean lens coverage; they are not reclassified as wording residue.

**R506-1-F1 - retained MINOR - Conformance, Robustness, Tests, Docs.** Artifact: `sw/firmware/gtest/README.md:205`, `sw/firmware/ctrl/port/ctrl_pool.c:114`. Authority/evidence: the blanket unreachable-exclusion claim and required defensive/error-return tests. The independent follow-up allocates two blocks, frees both, writes a null next pointer into the released head block, then allocates twice. The second allocation takes the excluded refusal with `free_count=1`, `refused=1`; a disposable copy with the guard removed exits on SIGSEGV. This corrects the initial assessment's limited assumption of clients preserving released storage. Impact: the measurement excludes a deliberately defensive path, and a dropped guard is untested. Required outcome: test the corruption refusal and count, kill a guard-removal mutant, remove the exclusion, and update totals/claims. Verification: `public_findings_probes.py`, the added named unit/mutant, and the coverage gate without this row. The firmware guard itself works correctly at this head.

**R506-1-F2 - retained MINOR - Conformance, Tests, Robustness, Docs.** Artifact: `sw/firmware/gtest/tally_selftest.py:95`, `fw_gtest_main.cpp:159`, `README.md:50`. The original public labels were Conformance and Tests; this review also records the overlapping abnormal-exit proof and documentation claims. Authority/evidence: assignment item 2 requires the tally itself to fail. The selftest checks the combined grade, marker and verdict command, which can all fail solely because of `[FAIL]`. The independent follow-up removes skipped-test counting in a disposable listener: it prints `checks: 1 failures: 0` and `RESULT: PASS`, yet the unchanged selftest accepts all eleven cases. The public review additionally reports surviving setup/crash-count mutants; those two variants were not independently rerun here. Impact: false failure totals can pass the supposed proof. Required outcome: assert the expected tally counts and FAIL result independently of marker/exit refusal, and kill the published listener mutants. Verification: the strengthened selftest must pass the original listener and reject all named defects; retain NOCOUNT behavior for exits that cannot print a tally.

**R506-1-F3 - retained MINOR - Docs.** Artifact: `sw/firmware/gtest/README.md:166` and `:231`, `fw_coverage.py:326`, `ctrl_nvm/test/test_ctrl_nvm.py:252`. Authority/evidence: the page says the coverage gate and each gate print the versions behind their measurements; the actual `ctrl.log` and `coverage.log` do not. Only the store gate invokes `fw_gtest.toolchain()`, and the coverage wrapper truncates away that line. Impact: the claimed local measurement provenance is absent, although the hosted install step records its versions. Required outcome: emit the versions in those gates, or correct the two sentences to identify the actual version records. Verification: inspect their output or the corrected provenance claims. This concerns measurement evidence, so the public MINOR classification remains.

| Public ID | Severity and lenses | Disposition, artifact and required outcome |
|---|---|---|
| R506-1-S1 | SUGGESTION; Tests, Docs | Retained; same function-wide exclusion swap as independently found R507-1-F2 (`fw_coverage.py:222`). The independent finding has its own MAJOR severity and additional lenses. Its evidence, impact, required outcome and verification apply; the public suggestion is not marked fixed. |
| R506-1-S2 | SUGGESTION; Robustness | Retained; `fw_gtest.py:85` and `:180` inherit `GTEST_*`, allowing a shell filter to select fewer tests with a nonempty passing tally. Optional outcome: clear or report these controls; verify a negative filter cannot silently narrow a full gate. No additional execution probe was run here. |
| R506-1-R1 | RESIDUE; Docs | Retained; PR body status/limitation still says no hosted run exists. Exact fix from the public review: replace the status sentence with “Hosted `rtl-fast` at this head: `firmware-unit` passed (run 37429204550); act replay pending.” Replace the limitation with “Hosted evidence: `rtl-fast` run 37429204550 at `27433e47`; the act replay is the manager's.” Verify the edited PR text against the linked hosted receipt. This does not change the recorded job result. |

**Reviewer-owned completion ledger**

Every lens was applied independently. CLEAN below is confined to the artifacts and exact head named; it does not approve subsequent fixes or authorize a merge.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: R507 F1/F2; R506 F1/F2 | Issue #665 directives 6008744385/6009234414/6009661573; REQUIREMENTS.md; MAILBOX_SPLIT.md; SAVED_STATE_FASTCONNECT.md:685; SAVED_STATE_MATERIALIZATION.md:2301; nvm_klj2.h:106; gtest README:178-212; port diff; prior-public-findings.json; public-findings-probes.log | R507-1 applied; no clean covering round | 27433e47c6d7805376547a91b418cf6aa9d95d2a |
| RTL | CLEAN | Full changed-path diff; adp_mbx.h comment diff; ctrl_build.py:36; nvm_bench.py:182; four mock seam implementations; tb/verilator/mbx/suite.hpp:54; mailbox-results.log; local RV32 receipts | R507-1 | 27433e47c6d7805376547a91b418cf6aa9d95d2a |
| Robustness | UNCLEAN: R507 F1/F2; R506 F1/F2 | tally_cases.cpp; tally.log; ADP/port/NVM negative and boundary tests; nvm_klj2.c:327; fw_coverage.py:222; coverage-probes.log; public-findings-probes.log | R507-1 applied; no clean covering round | 27433e47c6d7805376547a91b418cf6aa9d95d2a |
| Tests | UNCLEAN: R507 F1/F2; R506 F1/F2 | Retired-to-new test diff; PR per-check table; port-inventory.log; nvm_fixture.py; nvm_suite.cpp; both mutant graders and campaign logs; fw_coverage_selftest.py; ci_scope/ci_events receipts; public-findings-probes.log | R507-1 applied; no clean covering round | 27433e47c6d7805376547a91b418cf6aa9d95d2a |
| Docs | UNCLEAN: R507 F1/F2; R506 F1/F2/F3 | gtest README:153-212; ctrl/ctrl_nvm README diffs; docs/README.md; docs/testing/CI_WORKFLOWS.md; PR mapping and published handoff; prior-public-findings.json; ctrl.log/coverage.log version provenance | R507-1 applied; no clean covering round | 27433e47c6d7805376547a91b418cf6aa9d95d2a |

The manager must publish this packet, obtain fixes and independent re-review for R507-1-F1/F2 and the retained R506-1-F1/F2/F3, carry the residue to its checklist, reconcile the complete reviewer-owned ledger at the corrected head, and complete hosted/local-replica acceptance. Any eventual authorized merge additionally requires the current-dev candidate validation, no reviews in flight, both independent positive reviews, and post-merge containment under CONTRIBUTING.md. None is supplied by this source-head review.

Final containment: all 1,135 candidate tracked blobs and modes match the published tree; the index and detached HEAD match it too. Required submodules remain at protocol-processor `ead8036035affd53ef4b29979190f2f4f67084c0`, gptp-processor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, and verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`, with their complete tracked bytes/modes/indexes verified. `git status --porcelain=v1 --untracked-files=all` is empty (`status-after.log`). No candidate restoration was needed because probes only changed disposable copies. The optional external submodule was not initialized or used.

Only REPORT.md and entries in MANIFEST.sha256 are publishable. Scratch is disposable and excluded.

R507-1 FINISHED
