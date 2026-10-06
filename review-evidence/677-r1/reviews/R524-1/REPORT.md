[R524] NEGATIVE - exact head 6c94e9f5f496ac25f8c4e31f9e3685c725de29f3

R524-1, internal independent review of #677 / PR #684, including #678. All five lenses were applied. No source behavior defect was found. Two public documentation/evidence inaccuracies remain MINOR under the assigned rule: one changes a clause attribution, the other an exclusion figure. Neither qualifies as RESIDUE.

Tree: `25b32c793bd4bb6d959640094a44fb2b5c9d7a45`. Source base: `6714181d0c8a16e2983f85b724f4d688f5111835`. This reviews the published source head, not a later merge result.

Reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, [#677 acceptance and assignment](https://github.com/kebag-logic/milan-fpga/issues/677#issuecomment-6021510152), [#678 ruling](https://github.com/kebag-logic/milan-fpga/issues/678), REQUIREMENTS.md sections 1 and 8, FR_NFR.md control-service hooks, ARCHITECTURE.md, SAVED_STATE_FASTCONNECT.md sections 6.1-6.2 and firmware headers; then the complete one-commit diff and public executable evidence. No other reviewer report informed this independent verdict or ledger.

Findings

**R524-1-F1 | MINOR | Conformance, Docs | PR #684 body, Authoritative references, adp.h bullet**

- Authority/evidence: The [PR body](https://github.com/kebag-logic/milan-fpga/pull/684) cites “IEEE 1722.1-2021 section 5.6.3” for the state machine. `sw/firmware/ctrl/adp/adp.h:9` correctly identifies **Milan v1.2 5.6.3** as the Advertise state machine and **IEEE 1722.1-2021 6.2** as the ADPDU authority. See the public snapshot `public-pr-684.txt`.
- Impact: The published authority directs a cold reviewer to the wrong standard/clause. The header and reviewed transitions are correct; no wire-behavior defect is alleged.
- Required outcome: Correct that PR-body bullet to cite Milan v1.2 Section 5.6.3 for the state machine and IEEE 1722.1-2021 Section 6.2 for the ADPDU, retaining the no-callback header reference.
- Verification: Re-read the corrected public body against `adp.h:9` and its clause-bearing comments. Public correction and reviewer disposition suffice; another firmware build is unnecessary.

**R524-1-F2 | MINOR | Tests, Docs | issue #677, REVIEW READY comment 6024328677, coverage evidence bullet**

- Authority/evidence: The [review-ready comment](https://github.com/kebag-logic/milan-fpga/issues/677#issuecomment-6024328677) says “Exclusion table unchanged (15 rows)”. The table at `sw/firmware/gtest/README.md:284` has **14 data rows**, including five ADP rows, at both source base and head. `audit_evidence.py` compares every row's file, function, statement and excluded items; `evidence-audit.json` records 14 unchanged rows. The README correctly says fourteen at line 218.
- Impact: The public validation census disagrees with the exclusion population. The no-new-exclusions claim and 100% ratchet actually hold; there is no fifteenth exclusion in this tree.
- Required outcome: Publish a follow-up correction: “The coverage exclusion table has 14 data rows, unchanged from the source base; five are ADP rows.” Preserve the existing comment, as assignment 6021510152 requires. Keep the correct table and ratchet unchanged.
- Verification: Re-run `audit_evidence.py` and compare its 14-row result with the public correction. No behavior or coverage-measurement change is needed.

Applied lenses

**Conformance:** `sw/firmware/ctrl_nvm/nvm_klj2.c:285` checks container `end`, then `loaded`, before the erased-payload scan. The enclosing walker checks the eight-byte header against both bounds. Valid container sizes and bounded record lengths keep these sums within range. `nvm_klj2.h:106` permits the loaded prefix. LEN still takes precedence for container overrun; insufficient loaded record bytes return REC. `adp.h:130` states same/cross-instance prohibition, zero-delay delivery, interrupt deferral, both build modes, lifetime count and F2-F5 inheritance. Acceptance behavior passes. F1 keeps this lens UNCLEAN for the public clause attribution.

**[R524] PASS RTL - `source.diff`, `sw/firmware/ctrl/adp/adp.c:21`, `sw/firmware/ctrl/adp/adp_mbx.c:16`, `sw/firmware/milan_baremetal/Makefile:6` - architecture and integration checked.** The complete 26-path diff changes firmware and its tests/docs only: no RTL, gitlink, configuration, workflow or shipping build input. The shared guard matches the single-event-loop model. All six indirect calls are bracketed; every public ADP entry checks before using arguments. The adapter queues/arms work and later dispatches inputs through its handlers. State, wire, tag, backpressure and owed-frame paths remain covered by the control suite. The shipping library still builds `milan_baremetal.o` alone. No clock/reset/CDC logic changed.

**[R524] PASS Robustness - `sw/firmware/ctrl_nvm/test/test_nvm_prefix.cpp:19`, `sw/firmware/ctrl/test/test_adp_reentry.cpp:146`, `probes.log`, `ctrl.log`, `nvm.log` - boundaries and re-entry checked.** Exact 40-, 47- and 48-byte allocations pass under AddressSanitizer. The final payload's end-minus-one and exact-end distinguish rejection from acceptance. Old-bound and one-byte-late defects produce heap-buffer-overflow; the one-byte-early defect rejects a valid boundary and is caught. Both timer regressions and the 6 ports x 10 entries x 2 instance choices matrix pass in both modes. Release cases check counts, state/output preservation and valid calls after return. Debug cases require the assertion diagnostic and child termination; valid-transition checks then run in the unaffected parent. They do not claim an asserted process resumes. The ordinary suites additionally cover malformed frames, restarts, stale expiry, owed output, store failures and five shapes.

**Tests:** `ctrl_arms.py:36`, `nvm_bench.py:78`, `fw_gtest.py:80`, `fw_gtest.py:164` and `.github/workflows/rtl-fast.yml:266` connect these cases to default execution and coverage. Both the prefix C source and C++ test receive sanitizer instrumentation and the binary links its runtime. Guard removal must fail both named timer probes in both modes. All original 76 control and 106 NVM mutant definitions remain AST-identical; each catalogue adds three. The published raw campaigns catch every baseline NVM defect, encompassing the requested 102. F2 keeps this lens UNCLEAN only for the public exclusion census.

**Docs:** Examined all three changed READMEs, `adp.h`, and the nine other rule-bearing headers: `adp_mbx.h`, `mbx.h`, `mbx_hal.h`, `ctrl_debug.h`, `ctrl_pool.h`, `shlan_port.h`, `nvm_flash.h`, `nvm_state.h`, `nvm_flash_litespi.h`. The five ADP exclusion proofs explicitly cite the header rule; excluded identities/items do not change. Guard scope, lifetime count, deferred dispatch, build modes and host-only sanitizer use are documented. F1/F2 concern public text outside those correct source contracts.

Independent execution

From the pinned checkout, `python3 <packet>/run_review.py` ran four independent workers concurrently and waited for all of them. Each used four compilation jobs, at most 16 total. All returned 0 within 145 seconds. All disposable builds and planted copies stayed under `scratch/`; no source was edited.

| Check | Result | Receipts |
|---|---|---|
| Control firmware, `--require-rv32 --jobs 4` | 423 host tests, including 122 debug and 122 release re-entry cases; RV32I object/symbol check passed | `ctrl.log`, `ctrl.rc` |
| NVM store, `--require-rv32 --jobs 4` | 435 tests over five shapes; five RV32I builds passed | `nvm.log`, `nvm.rc` |
| Coverage self-test and `--check --jobs 4` | 28/28 planted cases; all 14 measured files at 100% lines/branches after unchanged exclusions | `coverage.log`, `coverage.rc` |
| Three ADP and three erased-payload mutants | Every named kill matched; guard removal failed both original timer probes in both modes | `probes.log`, `probes.rc`, individual mutation logs |
| Prefix positive control | Exact-sized allocations passed with sanitizer instrumentation | `prefix-control.log` |
| Public catalogue/receipt audit | 79/79 control and 109/109 NVM names appear exactly once in raw successful grades; baseline definitions preserved | `evidence-audit.json` |
| Whitespace and tree integrity | Whitespace check passed; tracked bytes, modes, kinds, index entries/flags and required gitlinks equal pinned trees | `integrity-before.json`, `integrity-after.json` |

The control worker explicitly selects the available bare-metal RV32 compiler instead of the installed Linux SDK whose ilp32 headers are unsuitable for this arm. It changes only the imported driver's compiler-candidate list in that worker. The open assertion symbol is `__assert_func`; the published compiler's is `__assert_fail`. Neither freestanding-object result proves a linked target assertion handler. The NVM worker uses the existing SDK. Versions appear in the logs. The optional lwSRP arm was not repeated; the independent coverage result nevertheless matches the published run that includes it.

Public evidence came from [commit 412c0f10, review-evidence/677-r1](https://github.com/kebag-logic/milan-fpga/tree/412c0f10e12755a47f79ec3f90e08ef5d2ecaa47/review-evidence/677-r1). Fetched blobs match their Git object IDs and published SHA-256 manifest. Its source-head record has 75 successful gate records, including static/builder batches, firmware campaigns and coverage. The six NVM batches are disjoint and exhaustive. This review audited campaign names/results and repeated the six new defects; it did not rerun full 79/109 campaigns or full static/builder/native banks. Public lwSRP and mailbox co-simulation logs are supporting evidence, not fresh reviewer execution.

Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #677/#678; `nvm_klj2.h:106`; `nvm_klj2.c:285`; `adp.h:130`; PR authority bullet | R524-1 applied, not banked | 6c94e9f5f496ac25f8c4e31f9e3685c725de29f3 |
| RTL | CLEAN | Complete `source.diff`; `adp.c:21`; `adp_mbx.c:16`; shipping Makefile:6; `ctrl.log` | R524-1 | 6c94e9f5f496ac25f8c4e31f9e3685c725de29f3 |
| Robustness | CLEAN | `test_nvm_prefix.cpp:19`; `test_adp_reentry.cpp:146`; mutation logs; `ctrl.log`; `nvm.log` | R524-1 | 6c94e9f5f496ac25f8c4e31f9e3685c725de29f3 |
| Tests | UNCLEAN (F2) | Default/coverage wiring; both mutant catalogues; raw receipts; `evidence-audit.json`; comment 6024328677 | R524-1 applied, not banked | 6c94e9f5f496ac25f8c4e31f9e3685c725de29f3 |
| Docs | UNCLEAN (F1, F2) | Three READMEs; ten headers; public Issue/PR evidence and authority text | R524-1 applied, not banked | 6c94e9f5f496ac25f8c4e31f9e3685c725de29f3 |

Prior-public-finding disposition: after writing this independent verdict and ledger, queried PR review bodies, inline comments and conversation comments. There were zero submitted reviews, zero inline comments and only the two manager review-start comments. No prior public review finding on PR #684 existed to resolve or retain. `prior-review-audit.json` records the query and the already-written report hash. The original defects recorded in #677/#678 were independently reproduced as planted failures and their fixes verified above.

Limits and pending manager duties

- Correct both public inaccuracies and obtain reviewer closure. No source fixes are requested. Open MINOR findings cannot bank their lenses under this assignment.
- Obtain the external verdict independently and finish all review rounds. This report does not authorize merge.
- Source validation differs from final current-dev validation. Observed live dev: `6a05347d4e2ec1dcb37d4e5806c7767537de3ce0`. #679 / PR #683 conflicts in `test_ctrl_firmware.py`: land it first, merge dev, review that delta, then validate the exact final candidate. Preserve both lanes' tests and job limits; re-cover affected lenses.
- The manager owns full source/candidate banks and hosted/local-replica acceptance. At the public query, Issue/PR comments contained assignment, takeover, review-ready evidence and review starts, but no separate manager native-bank evidence comment. The assignment says those source banks passed. Publish/link those exact-head receipts before claiming the full merge bar. This focused review supplies no replacement for them.
- `hosted-checks.json` records one exact-head snapshot at 2026-10-06T20:05:19Z. `firmware-unit` executed successfully; other jobs were running and long aggregates were not yet established. Physical gPTP was **skipped**. No completion polling or replica acceptance was performed here.
- Physical calibration was **NOT RUN**. Field and resource-calibration skips are not hardware proof. Host/model results establish neither target-time service budgets nor board, physical-timing or physical power-cut behavior. The guard is an event-loop re-entry check, not a concurrency lock.
- Before/after checks hashed 1,142 superproject blobs, 558 protocol-processor blobs, 104 gPTP-processor blobs and 214 axis-library blobs, verified modes/kinds/index/flags and the three required registered gitlinks. The unrelated `external` gitlink stayed uninitialized and unchanged. The checkout remains clean.
- After an authorized merge, the manager still owes containment, current public evidence/documentation, Issue closure and workflow completion. Only REPORT.md and files listed in MANIFEST.sha256 are publishable. `scratch/` is excluded.

R524-1 FINISHED
