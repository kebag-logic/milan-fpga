[R524] POSITIVE - exact head 6c94e9f5f496ac25f8c4e31f9e3685c725de29f3

R524-2, internal independent delta review of issue #677 / PR #684, including the public #678 scope decision. Both shared MINOR findings are resolved. No open finding or residue remains in this delta. The other R524-1 verdicts stand at this unchanged source head.

Tree: `25b32c793bd4bb6d959640094a44fb2b5c9d7a45`. Source base: `6714181d0c8a16e2983f85b724f4d688f5111835`. This verdict covers the published source and corrected public artifacts; it does not validate a later merge candidate.

Reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README.md, [#677 acceptance](https://github.com/kebag-logic/milan-fpga/issues/677) and [frozen lane scope](https://github.com/kebag-logic/milan-fpga/issues/677#issuecomment-6021510152), [#678 ruling](https://github.com/kebag-logic/milan-fpga/issues/678), requirements and interface authorities, then the complete one-commit diff/history and public executable evidence. The prior internal findings were read only after the independent diff pass. No private author material or another reviewer's report informed this verdict or ledger.

**Resolved findings**

**R524-1-F1 / R525-1-F1 | MINOR | Conformance, Docs | RESOLVED | PR #684 body, Authoritative references, adp.h bullet**

- Authority/evidence: `sw/firmware/ctrl/adp/adp.h:9`, `docs/design/MAILBOX_SPLIT.md:279` and `REQUIREMENTS.md:410` distinguish the Milan advertiser from the IEEE ADPDU. The [current PR body](https://github.com/kebag-logic/milan-fpga/pull/684) now cites Milan v1.2 section 5.6.3 for the Advertise state machine and IEEE 1722.1-2021 section 6.2 for the ADPDU, retaining the no-callback contract reference. Snapshot: `receipts/pr-body.json`.
- Impact of the former defect: incorrect public attribution directed reviewers to the wrong standard/clause; source behavior was unaffected.
- Required outcome: both authorities correctly attributed in the public bullet. Met.
- Verification: direct comparison with the exact-head header and interface document; executable assertions in `scripts/audit_delta.py`, recorded in `receipts/delta-audit.json`, exit 0.

**R524-1-F2 / R525-1-F2 | MINOR | Tests, Docs | RESOLVED | issue #677, coverage evidence in comment 6024328677 and correction 6024757146**

- Authority/evidence: `sw/firmware/gtest/README.md:218` and its table at line 284 contain 14 exclusion data rows, five for `adp.c`. The audit independently counts 14 at both base and head and compares every row's file, function, statement and excluded items: all unchanged. The five ADP proof explanations add the header rule without widening exclusions.
- Impact of the former defect: the original public census said 15, disagreeing with the actual exclusion population. It did not change the coverage measurement.
- Required outcome: publish the accurate count while preserving the original comment, as the frozen scope requires. Met by the [manager's correction](https://github.com/kebag-logic/milan-fpga/issues/677#issuecomment-6024757146): 14 data rows, unchanged from the source base; five ADP rows.
- Verification: `receipts/delta-audit.json` records both counts and unchanged exclusion identities/items. `receipts/comment-6024328677.json` retains the original 15-row text; its creation and update timestamps are identical. `receipts/comment-6024757146.json` records the explicit correction. Exit 0.

These findings remain classified MINOR and are closed by verified corrections. They have not been downgraded to RESIDUE.

**Five-lens application**

[R524] PASS Conformance - `sw/firmware/ctrl/adp/adp.h:9`, `docs/design/MAILBOX_SPLIT.md:279`, PR authority bullet; `sw/firmware/ctrl_nvm/nvm_klj2.h:106`, `sw/firmware/ctrl_nvm/nvm_klj2.c:285` - F1 attribution now matches the source authorities. The independent diff pass confirms the erased-payload check still preserves container-end precedence and checks loaded bytes before scanning. The stated no-callback rule remains the public #678 ruling. No requirement, clause meaning or protocol behavior changed in the correction.

[R524] PASS RTL - `receipts/changed-files.txt`, `receipts/source.diff`, `sw/firmware/ctrl/adp/adp.c:21`, `sw/firmware/ctrl/adp/adp_mbx.c:16`, `sw/firmware/milan_baremetal/Makefile:6` - checked delta applicability and retained R524-1 coverage. All 26 source-diff paths are under firmware; no RTL, gitlink, configuration, workflow or shipping build input changes. The guard remains a single-event-loop contract. The two public corrections change no architecture, timing, reset or crossing. No new build was needed for this delta.

[R524] PASS Robustness - `sw/firmware/ctrl_nvm/test/test_nvm_prefix.cpp:19`, `sw/firmware/ctrl/test/test_adp_reentry.cpp:146`, `receipts/source-evidence/erased-end-asan.log` - checked unchanged boundary and callback evidence, retaining R524-1 coverage. Exact 40/47/48-byte buffers and the final payload boundary remain the test inputs. Both callback modes and same/other-instance cases remain unchanged. The public failure receipt still detects the restored old bound. This round ran no new firmware or mutation campaign.

[R524] PASS Tests - `sw/firmware/gtest/README.md:284`, `receipts/delta-audit.json`, `sw/firmware/ctrl/test/ctrl_arms.py:36`, `sw/firmware/ctrl_nvm/test/nvm_bench.py:78`, `sw/firmware/gtest/fw_gtest.py:80`, `.github/workflows/rtl-fast.yml:266` - F2's corrected count agrees with an independent base/head row comparison. Default test wiring, instrumentation and ratchet are unchanged from R524-1. The public coverage receipt reports 14 measured files at 100% after exclusions; this file count is distinct from the independently counted 14 exclusion rows.

[R524] PASS Docs - `receipts/pr-body.json`, both issue-comment snapshots, `sw/firmware/ctrl/adp/adp.h:9`, `sw/firmware/gtest/README.md:218` and line 284 - both requested corrections accurately describe the authorities and exclusion population. The original comment remains preserved with an explicit follow-up correction. The reviewed source documentation needs no change for F1/F2.

**Reviewer-owned completion ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `sw/firmware/ctrl/adp/adp.h:9`; `docs/design/MAILBOX_SPLIT.md:279`; PR authority bullet; `receipts/delta-audit.json`; unchanged codec contract/diff | R524-2 closes F1; R524-1 behavior retained | 6c94e9f5f496ac25f8c4e31f9e3685c725de29f3 |
| RTL | CLEAN | Complete source diff/path list; `sw/firmware/ctrl/adp/adp.c:21`; `sw/firmware/ctrl/adp/adp_mbx.c:16`; `sw/firmware/milan_baremetal/Makefile:6`; integrity receipts | R524-1 retained; R524-2 delta applicability checked | 6c94e9f5f496ac25f8c4e31f9e3685c725de29f3 |
| Robustness | CLEAN | `sw/firmware/ctrl_nvm/test/test_nvm_prefix.cpp:19`; `sw/firmware/ctrl/test/test_adp_reentry.cpp:146`; published failure/control receipts; unchanged source tree | R524-1 retained; R524-2 delta applicability checked | 6c94e9f5f496ac25f8c4e31f9e3685c725de29f3 |
| Tests | CLEAN | Base/head exclusion table; `receipts/delta-audit.json`; test wiring; published coverage and campaign receipts; correction comment | R524-2 closes F2; R524-1 execution retained | 6c94e9f5f496ac25f8c4e31f9e3685c725de29f3 |
| Docs | CLEAN | PR authority bullet; original/corrected issue evidence; exact-head header and exclusion table | R524-2 | 6c94e9f5f496ac25f8c4e31f9e3685c725de29f3 |

**Prior public finding disposition**

After this verdict and ledger were written, a read-only audit found the two published first-round reviews, no submitted review bodies and no inline comments. R525-1-F1 duplicates R524-1-F1 with the same Conformance/Docs lenses and is RESOLVED by the verified PR-body correction. R525-1-F2 duplicates R524-1-F2 with the same Tests/Docs lenses and is RESOLVED by the verified 14-row audit and preserved-comment correction. No additional prior public finding remains to retain. `receipts/prior-findings-audit.json` records the public inventory and the report hash captured before reading the external findings. The external reviewer still owns its independent second-round verdict.

**Receipts and real limits**

`scripts/audit_delta.py <checkout> <packet>` checks both corrections, row identities/counts and source scope. `scripts/check_integrity.py <checkout>` hashes the tracked working bytes against the pinned trees, checks kinds/modes, index entries/flags and the three required registered submodule gitlinks. Both return 0. Before/after integrity receipts cover 1,142 superproject blobs, 558 protocol-processor blobs, 104 gPTP-processor blobs and 214 axis-library blobs. No source edits or disposable fault probes occurred; no restoration was necessary.

Selected [public executable evidence at 412c0f10](https://github.com/kebag-logic/milan-fpga/tree/412c0f10e12755a47f79ec3f90e08ef5d2ecaa47/review-evidence/677-r1) was fetched as data and checked against Git blob IDs and the published SHA-256 manifest. `receipts/evidence-fetch.json` records six verified artifacts. The source-head record contains 75 successful gate entries. Selected receipts show the unchanged coverage result, control campaign result, store controls and 109 caught store defects, plus the old-bound failure. These are published prior execution, not fresh execution by this round. No full bank or hosted run was executed or polled here.

The assignment states that the manager's full source static/builder and native banks passed at this head. The current Issue/PR snapshot contains no separate manager native-bank receipt; the manager retains responsibility for publishing/linking that source evidence and for hosted/local-replica acceptance. Source validation at base `6714181d0c8a16e2983f85b724f4d688f5111835` is distinct from the final candidate built against current dev; the assignment identifies live dev as `6a05347d4e2ec1dcb37d4e5806c7767537de3ce0`. Any source merge/resolution must receive the required validation and review of affected lenses. This report does not authorize merging.

Physical calibration is NOT RUN; field and calibration skips provide no hardware proof. Existing host results do not establish physical timing, target service budgets or power-cut behavior. The ADP guard is not a concurrency lock; freestanding object evidence does not prove a linked target assertion handler.

Pending manager duties: publish this report and receipts, complete the independent external review and all outstanding rounds, establish the full source and exact-current-dev candidate gates, distinguish executed hosted jobs from skipped contexts, obtain merge authorization, and perform post-merge containment and Issue/workflow completion. Source evidence cannot substitute for final-candidate evidence.

Only REPORT.md and files listed in MANIFEST.sha256 are publishable. Scratch contents are excluded.

R524-2 FINISHED
