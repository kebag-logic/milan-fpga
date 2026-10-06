[R525] NEGATIVE - exact head 6c94e9f5f496ac25f8c4e31f9e3685c725de29f3

Round R525-1 applied all five lenses. The firmware fixes and executable checks pass. Two public documentation/evidence errors remain MINOR, leaving Conformance, Tests and Docs UNCLEAN. Neither qualifies as RESIDUE: one changes a clause attribution, the other an exclusion figure. No source fix is requested by this review.

Tree: `25b32c793bd4bb6d959640094a44fb2b5c9d7a45`. Source base: `6714181d0c8a16e2983f85b724f4d688f5111835`. The published head was rechecked at 2026-10-06T20:18:34Z and still matched. This verdict covers that source head and the captured public artifacts.

Reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README.md, [#677 acceptance and assignment 6021510152](https://github.com/kebag-logic/milan-fpga/issues/677#issuecomment-6021510152), [#678 ruling](https://github.com/kebag-logic/milan-fpga/issues/678), REQUIREMENTS.md sections 1 and 8, the architecture and mailbox contract, SAVED_STATE_FASTCONNECT.md sections 6.1-6.2 and firmware headers, then the complete one-commit diff and public executable evidence. The independent verdict and ledger were written before reading another review.

**R525-1-F1 | MINOR | Conformance, Docs | PR #684 body, Authoritative references, adp.h bullet**

Authority/evidence: The [PR body](https://github.com/kebag-logic/milan-fpga/pull/684) attributes the state-machine reference to `IEEE 1722.1-2021 section 5.6.3`. `sw/firmware/ctrl/adp/adp.h:9` correctly assigns the advertiser to Milan v1.2 5.6.3 and the ADPDU to IEEE 1722.1-2021 6.2. `docs/design/MAILBOX_SPLIT.md:277` uses the same separation. [The final public snapshot](receipts/final-pr-reference.json) retains the erroneous bullet.

Impact: A cold reviewer is directed to the wrong specification clause. The source header and examined behavior are correct.

Required outcome: Replace that PR-body bullet with: `sw/firmware/ctrl/adp/adp.h: Milan v1.2 Section 5.6.3 advertiser, IEEE 1722.1-2021 Section 6.2 ADPDU, and the no-callback port contract from #678.`

Verification: Re-read the corrected public bullet against the header and mailbox design. A public-text correction needs reviewer disposition; it does not require another firmware build.

**R525-1-F2 | MINOR | Tests, Docs | issue #677, REVIEW READY comment 6024328677, coverage evidence bullet**

Authority/evidence: The [review-ready comment](https://github.com/kebag-logic/milan-fpga/issues/677#issuecomment-6024328677) says `Exclusion table unchanged (15 rows)`. The table at `sw/firmware/gtest/README.md:283` contains 14 data rows, including five ADP rows. The independent [static audit](receipts/static-audit.json) proves the same 14 file/function/statement/excluded-item identities at base and head. [The public claim receipt](receipts/issue-exclusion-claim.json) records the discrepancy.

Impact: The public evidence census gives the wrong exclusion population. The actual no-new-exclusions claim and coverage ratchet hold.

Required outcome: Publish a follow-up correction: `The coverage exclusion table has 14 data rows, unchanged from the source base; five are ADP rows.` Preserve the existing comment, as assignment 6021510152 requires. Keep the correct source table and ratchet unchanged.

Verification: Run `python3 scripts/static_audit.py <source>` from this packet and compare its 14-row result with the public correction. No coverage-measurement change is required.

Conformance was applied to both acceptance contracts. `sw/firmware/ctrl_nvm/nvm_klj2.c:298` refuses a payload beyond `loaded` before scanning it; the enclosing walker bounds the header first. The earlier container-end check preserves VD_LEN precedence, while a short loaded record returns VD_REC, matching `nvm_klj2.h:106`. Validated container sizes and shape-derived payload lengths keep the sums bounded. `sw/firmware/ctrl/adp/adp.h:130` states the same/cross-instance prohibition, zero-delay deferral, interrupt deferral, assertion/release modes, lifetime count and F2-F5 inheritance. The source acceptance behavior passes; F1 leaves the lens UNCLEAN.

[R525] PASS RTL - `receipts/source.diff`, `sw/firmware/ctrl/adp/adp.c:24`, `sw/firmware/ctrl/adp/adp_mbx.c:16`, `sw/firmware/ctrl/loop/ctrl_loop.h:8`, `sw/firmware/milan_baremetal/Makefile:5` - architecture and integration checked against the single-event-loop contract. All six port calls are bracketed and all public ADP entries check the guard before using arguments. The adapter delivers inputs through later handlers. The 26-path diff changes firmware, tests and documentation; RTL, CDC/reset logic, gitlinks, configurations, workflows and shipping build inputs have no delta. The shipping library's object list remains `milan_baremetal.o`.

[R525] PASS Robustness - `sw/firmware/ctrl_nvm/test/test_nvm_prefix.cpp:18`, `sw/firmware/ctrl/test/test_adp_reentry.cpp:147`, `:174`, `:201`, and the campaign receipts - exact 40-, 47- and 48-byte allocations and both final-payload boundaries pass. Restoring the old end bound produces a one-byte heap read immediately beyond the 48-byte allocation. The early-bound mutant wrongly rejects the valid end; the late-bound mutant overreads. Both are caught. The two timer probes and 120 port/entry/instance combinations pass in each build mode. Release cases check counting, unchanged state/output, running timers and subsequent valid calls. Debug cases require the assertion diagnostic and child termination; their valid-transition checks run afterward in the unaffected parent, not in a resumed asserted process. Existing suites retain malformed-frame, restart, stale-expiry, backpressure, store-failure and configuration coverage.

Tests were applied to `ctrl_arms.py:36`, `test_ctrl_firmware.py:100`, `nvm_bench.py:82`, `fw_gtest.py:84`, `fw_coverage.py:419` and `.github/workflows/rtl-fast.yml:246`. The new cases enter default execution and coverage; both the prefix test and codec receive sanitizer instrumentation. Guard removal must fail both named timer probes in both modes. All 76 base control mutants and 106 base NVM mutants remain definition-identical; each catalogue adds three. The full independent campaigns catch every registered mutant, encompassing the requested older 102 store defects. F2 leaves Tests UNCLEAN for the public census.

Docs was applied to all three changed READMEs, the ADP header and the nine other rule-bearing headers: `adp_mbx.h`, `mbx.h`, `mbx_hal.h`, `ctrl_debug.h`, `ctrl_pool.h`, `shlan_port.h`, `nvm_flash.h`, `nvm_state.h` and `nvm_flash_litespi.h`. The five ADP exclusion rows at `sw/firmware/gtest/README.md:285` cite the header rule. Guard scope, diagnostic lifetime, deferred dispatch and host-only sanitizer use are documented. F1/F2 concern the public authority/evidence text.

The following independent execution receipts belong to this round. Each command's full argument vector, return code and elapsed time is in its adjacent JSON receipt. Commands remained foreground processes; independent campaigns ran concurrently, with at most 16 compilation jobs. Disposable builds and mutations stayed under `scratch/`.

| Check | Result | Receipts |
|---|---|---|
| Control firmware, `--require-rv32 --self-test --jobs 4` | 423 host checks, 122 re-entry tests per mode, RV32 object/symbol check, 79/79 mutants; rc 0 | [log](receipts/ctrl-campaign.log), [command/status](receipts/ctrl-campaign.json) |
| NVM default gate, `--self-test --jobs 8` | 435 tests and five RV32 shape builds passed; 48 mutants graded before the 580-second limit, rc 124 | [log](receipts/nvm-campaign.log), [command/status](receipts/nvm-campaign.json) |
| NVM remaining disjoint batches, `--jobs 4` each | 16 + 15 + 15 + 15 mutants caught; all four rc 0 | [plan](receipts/nvm-resume-plan.json), `receipts/nvm-part-{0,1,2,3}.{log,json,rc}` |
| Combined NVM campaign audit | 109/109 registered mutants, exactly one completed grade each, no gaps; no unnamed checks in the suite inventory | [summary](receipts/campaign-summary.json), [portable aggregator](scripts/aggregate_receipts.py) |
| Focused prefix control and three mutants | Control passed; all three defects failed the named test, with sanitizer overflow diagnostics for old/late bounds; probe rc 0 | [raw output](receipts/prefix-probe.log), [script](scripts/prefix_probe.py) |
| Coverage `--check --jobs 4` | All 14 files at 100% lines/branches after unchanged exclusions; rc 0 | [log](receipts/coverage.log), [command/status](receipts/coverage.json) |
| Coverage and tally controls | 28/28 coverage controls; 18/18 listener mutants; rc 0 | [log](receipts/small-checks.log), [script](scripts/small_checks.py) |
| Source scope and whitespace | All prior mutant definitions and 14 exclusions preserved; whitespace check passed | [audit](receipts/static-audit.json), [script](scripts/static_audit.py) |

The initial NVM timeout is retained as rc 124, not represented as a successful full command. The frozen continuation plan excludes its 48 completed grades; the aggregate checks every registered name and all continuation statuses. All campaign processes have finished.

Public executable evidence was read from [commit 412c0f10, review-evidence/677-r1](https://github.com/kebag-logic/milan-fpga/tree/412c0f10e12755a47f79ec3f90e08ef5d2ecaa47/review-evidence/677-r1). Thirteen selected receipts match the published SHA-256 manifest, including all six public NVM batches, control results, coverage and the sanitizer witness. Its evidence record identifies this exact source head and 75 successful gate records. [The audit](receipts/public-evidence-audit.json) distinguishes those supplied records from the independent execution above.

The reviewer-owned completion ledger is:

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #677/#678; `sw/firmware/ctrl_nvm/nvm_klj2.h:106`; `nvm_klj2.c:298`; `sw/firmware/ctrl/adp/adp.h:130`; PR authority bullet | R525-1 applied, not clean | 6c94e9f5f496ac25f8c4e31f9e3685c725de29f3 |
| RTL | CLEAN | Complete `receipts/source.diff`; `sw/firmware/ctrl/adp/adp.c:24`; `adp_mbx.c:16`; shipping Makefile:5; control receipts | R525-1 | 6c94e9f5f496ac25f8c4e31f9e3685c725de29f3 |
| Robustness | CLEAN | `sw/firmware/ctrl_nvm/test/test_nvm_prefix.cpp:18`; `sw/firmware/ctrl/test/test_adp_reentry.cpp:147`; both campaigns and prefix receipts | R525-1 | 6c94e9f5f496ac25f8c4e31f9e3685c725de29f3 |
| Tests | UNCLEAN (F2) | Default/coverage wiring, mutant catalogues, `receipts/campaign-summary.json`, exclusion audit, review-ready comment 6024328677 | R525-1 applied, not clean | 6c94e9f5f496ac25f8c4e31f9e3685c725de29f3 |
| Docs | UNCLEAN (F1, F2) | Three changed READMEs, ten rule-bearing headers, PR authority and Issue evidence snapshots | R525-1 applied, not clean | 6c94e9f5f496ac25f8c4e31f9e3685c725de29f3 |

Prior-public-finding disposition: the first query, after the independent verdict and ledger were written, contained no submitted reviews or inline findings and only the two review-start notices. A final query found the subsequently published [R524-1 findings](https://github.com/kebag-logic/milan-fpga/pull/684#issuecomment-6024636464). R524-1-F1 is retained as the independently recorded F1 above. R524-1-F2 is retained as F2 after checking it against this round's own 14-row audit and the original public comment. Their assigned lenses are preserved. Neither is resolved at this head. [The disposition receipt](receipts/prior-findings.json) records both queries.

Limits and pending manager duties:

- Correct both public inaccuracies and obtain reviewer closure. Finish all independent review rounds before considering merge.
- This is source review, not validation of the final current-dev candidate. The assignment identified live dev `6a05347d4e2ec1dcb37d4e5806c7767537de3ce0`. Land #679 / PR #683 first, resolve its `test_ctrl_firmware.py` conflict semantically, review the resulting delta and validate the actual current-dev candidate. Preserve both lanes' cases and job limits; re-cover affected lenses.
- The manager owns full static/builder/native banks and hosted/local-replica acceptance. Those full banks were not rerun here. Link the manager's exact-head source results and final-candidate results in the public task record; the captured comments do not contain a separate manager native-bank receipt.
- [The hosted snapshot](receipts/hosted-checks.json) contains successful jobs and jobs still running, including firmware-unit and exhaustive shards. Physical gPTP is explicitly skipped. It establishes neither completed hosted acceptance nor executed physical testing.
- RV32 results prove freestanding objects and symbol inventories, not a linked target assertion handler. The optional lwSRP arm and mailbox co-simulation were not independently repeated. The guard enforces the one-event-loop contract; it is not a concurrency lock. Future F2-F5 implementations are not certified here.
- Physical calibration was NOT RUN. Field and resource-calibration skips are not hardware proof. Host/model results do not establish board timing, physical power-cut recovery or release qualification.
- [Initial](receipts/initial-tree.json) and [final](receipts/final-tree.json) proofs match: 1,142 superproject blobs, 558 protocol-processor blobs, 104 gPTP-processor blobs and 214 axis-library blobs, with pinned modes, kinds and index entries. All three required registered gitlinks match. [Index flags](receipts/final-index-flags.json) are normal; the [checkout is clean](receipts/final-status.log). The optional `external` gitlink remains unchanged and uninitialized. No source was edited.
- [Recorded peak memory](receipts/resource-limits.json) was 11,850,264,576 bytes, below the 12 GiB cap, with no out-of-memory events. No hardware, full RTL/native bank, shared installation, publication or merge operation was performed.
- After an explicitly authorized merge, the manager still owes containment, current documentation/evidence, Issue closure and workflow completion. Publish only REPORT.md and files listed in MANIFEST.sha256. The entire `scratch/` directory is excluded.

R525-1 FINISHED
