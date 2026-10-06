[R525] POSITIVE - exact head 6c94e9f5f496ac25f8c4e31f9e3685c725de29f3

R525-2 resolves the two shared MINOR findings. All five lenses are CLEAN for this delta review. No source change occurred; the other R525-1 verdicts stand. No open finding or RESIDUE remains in this assigned delta. This is a source-review verdict, not merge authorization.

Tree: `25b32c793bd4bb6d959640094a44fb2b5c9d7a45`. Source base: `6714181d0c8a16e2983f85b724f4d688f5111835`. The final public snapshot and local byte checks on 2026-10-06 at 20:29 UTC still identify the assigned head.

Reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README.md, [#677 acceptance and public scope decision](https://github.com/kebag-logic/milan-fpga/issues/677#issuecomment-6021510152), [#678 ruling](https://github.com/kebag-logic/milan-fpga/issues/678), REQUIREMENTS.md, saved-state sections 6.1-6.2, the mailbox design and public headers, then the complete one-commit diff and public executable evidence. Prior findings were read after that independent diff pass. The independent verdict and ledger were written before reading the other reviewer's report; `receipts/independent-decision-order.json` records that order.

**R525-1-F1 / R524-1-F1 | MINOR, RESOLVED | Conformance, Docs | PR #684 body, Authoritative references, adp.h bullet**

Authority/evidence: The [current PR body](https://github.com/kebag-logic/milan-fpga/pull/684) now attributes the Advertise state machine to Milan v1.2 section 5.6.3 and the ADPDU to IEEE 1722.1-2021 section 6.2. This matches `sw/firmware/ctrl/adp/adp.h:9` and `docs/design/MAILBOX_SPLIT.md:279`; the no-callback reference remains.

Impact of the original defect: the authority bullet directed readers to the wrong specification clause. Required outcome: correct both attributions without changing the source contract. Verification: direct comparison and the executable citation check pass (`receipts/pr-684.json`, `receipts/delta-check.log`). No required change remains. This closes a clause error, without reclassifying it as wording residue.

**R525-1-F2 / R524-1-F2 | MINOR, RESOLVED | Tests, Docs | #677 comments 6024328677 and 6024757146; sw/firmware/gtest/README.md:283**

Authority/evidence: The [manager correction](https://github.com/kebag-logic/milan-fpga/issues/677#issuecomment-6024757146) states 14 exclusion data rows, unchanged from the source base, including five ADP rows. An independent census finds 14 rows and five `adp.c` rows at both base and head. Every file/function/statement/excluded-item coordinate is identical; only the five ADP explanations gained the header-rule justification in the original source change. The source README correctly says fourteen at line 218.

Impact of the original defect: the evidence comment overstated the exclusion population. Required outcome: publish the accurate census while preserving the original comment. Verification: the [original comment](https://github.com/kebag-logic/milan-fpga/issues/677#issuecomment-6024328677) remains present with its original 15-row statement and equal creation/update timestamps; the separate correction names it explicitly. `receipts/comment-6024328677.json`, `receipts/comment-6024757146.json` and `receipts/delta-check.log` record the result. No required change remains.

Both prior public finding sets are reconciled in `receipts/prior-findings.json`. Their original severity and all assigned lenses are retained. The conversation, submitted-review and inline-comment index contains no additional finding set requiring disposition.

[R525] PASS Conformance - PR #684 authority bullet; `sw/firmware/ctrl/adp/adp.h:9,130`; `docs/design/MAILBOX_SPLIT.md:279`; `sw/firmware/ctrl_nvm/nvm_klj2.c:298` - the corrected citations agree with the authorities. The source still checks loaded payload bounds before reading and documents the single-event-loop rule. The correction alters neither acceptance contract nor reviewed behavior.

[R525] PASS RTL - `receipts/source.diff`, `receipts/source-name-status.txt`, `sw/firmware/ctrl/adp/adp.c:24` and `receipts/integrity-final.log` - the complete 26-path source delta remains confined to firmware, tests and documentation. The six guarded port calls and entry checks remain as reviewed. No RTL, clock/reset/CDC, configuration, workflow or gitlink change accompanies either public correction.

[R525] PASS Robustness - `sw/firmware/ctrl_nvm/test/test_nvm_prefix.cpp:18`; `sw/firmware/ctrl/test/test_adp_reentry.cpp:147,174,201`; supplied prefix-failure and control logs - the exact-sized prefix boundaries, inline-expiry cases and same/cross-instance matrix remain unchanged. The public corrections change no negative-path handling, timer behavior, assertion behavior or failure verdict. R525-1 execution coverage remains applicable at this identical head.

[R525] PASS Tests - `sw/firmware/gtest/README.md:283`; `coverage.ratchet`; `ctrl_arms.py:36`; `nvm_bench.py:82`; `receipts/delta-check.log` and supplied coverage log - independently counted both exclusion tables and compared their excluded-item identities. The census correction now matches the evidence. Default/coverage test wiring and instrumentation remain unchanged. Three in-memory negative controls reject a wrong clause, a wrong count and a widened exclusion; none modifies source.

[R525] PASS Docs - current PR authority bullet, original and correction comments, `sw/firmware/ctrl/adp/adp.h:9,130`, changed READMEs and port-header hunks in `receipts/source.diff` - public authority and evidence claims now agree with the source. The preserved historical error has an explicit linked correction, as the public assignment requires.

The reviewer-owned completion ledger is:

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | PR authority bullet; adp.h:9,130; MAILBOX_SPLIT.md:279; nvm_klj2.c:298; #677/#678 | R525-2 correction closure; R525-1 source verdict retained | 6c94e9f5f496ac25f8c4e31f9e3685c725de29f3 |
| RTL | CLEAN | Complete source.diff; adp.c:24; source-name-status.txt; integrity-final.log | R525-1 coverage retained; R525-2 delta applied | 6c94e9f5f496ac25f8c4e31f9e3685c725de29f3 |
| Robustness | CLEAN | test_nvm_prefix.cpp:18; test_adp_reentry.cpp:147,174,201; supplied control/failure logs | R525-1 coverage retained; R525-2 delta applied | 6c94e9f5f496ac25f8c4e31f9e3685c725de29f3 |
| Tests | CLEAN | gtest/README.md:283; base/head census; coverage.ratchet; correction 6024757146; delta-check.log | R525-2 census closure; R525-1 execution retained | 6c94e9f5f496ac25f8c4e31f9e3685c725de29f3 |
| Docs | CLEAN | PR body; both issue comments; adp.h:9,130; README:218,283; header/doc diff | R525-2 | 6c94e9f5f496ac25f8c4e31f9e3685c725de29f3 |

Reproduce the focused checks from the packet:

```sh
python3 scripts/run_delta_checks.py <source-checkout> <packet-directory>
```

Every recorded foreground command returned 0. `receipts/commands.json` records arguments, completion times and status; adjacent `.log` and `.rc` files retain raw results. The count/citation checks, three negative controls, source whitespace check and byte-integrity checks passed. This round ran no fresh firmware campaign or heavy build.

Six selected executable-evidence files from [public commit 412c0f10](https://github.com/kebag-logic/milan-fpga/tree/412c0f10e12755a47f79ec3f90e08ef5d2ecaa47/review-evidence/677-r1) match the published SHA-256 manifest. They include control results, coverage, the old-bound failure witness and NVM results. The supplied evidence record identifies this head and 75 successful gate records; its NVM campaign has 109 unique caught defects. Coverage reports 14 files at 100% after exclusions. These are audited supplied receipts, distinct from this round's fresh census and integrity checks.

Limits and pending manager duties:

- Complete the other independent round and all merge prerequisites. This report closes the shared findings for this reviewer; it does not publish or impersonate another reviewer's verdict.
- Source validation remains distinct from the final current-dev candidate. The assignment identifies live dev `6a05347d4e2ec1dcb37d4e5806c7767537de3ce0`. The manager must construct and validate the actual candidate at merge time, handle the publicly identified #679 / PR #683 integration dependency, and obtain renewed coverage for any changed artifacts.
- The assignment reports full manager source-bank passes. This delta review retains that supplied evidence and samples the public packet; it does not independently repeat those banks. The manager owns complete source/candidate receipts, hosted acceptance and local-replica acceptance. No new hosted-job snapshot was taken here; skipped contexts establish no executed test result.
- Physical calibration was NOT RUN. Field and resource-calibration skips are not hardware proof. Host evidence does not establish board timing, power-cut recovery or physical release qualification. The event-loop guard is not a concurrency lock; freestanding object checks do not establish a linked target assertion handler.
- Initial and final raw proofs match: 1,142 superproject blobs, 558 protocol-processor blobs, 104 gPTP-processor blobs and 214 axis-library blobs. Bytes, file kinds, executable modes and index entries match the immutable trees. Required registered gitlinks match `ead8036035affd53ef4b29979190f2f4f67084c0`, `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` and `48ff7a7e2ef782cf778d47910cf85835c64b1bce`, respectively. The optional external gitlink is unchanged. The detached checkout is clean; no source restoration was necessary.
- No source edit, commit, push, GitHub write, hardware operation or merge occurred. After an explicitly authorized merge, the manager still owes containment, current public evidence, issue closure and workflow completion.
- Publish REPORT.md and only files listed in MANIFEST.sha256. The entire scratch directory is excluded.

R525-2 FINISHED
