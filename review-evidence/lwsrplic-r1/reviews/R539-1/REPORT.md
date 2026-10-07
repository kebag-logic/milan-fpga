[R539] NEGATIVE - exact head 375dbe132c6f1498f2f3e714ce5905d34456c9d5

The licensing change passes its mechanical and executable checks, but the public-release gate remains open. Two findings require resolution: historical disclosure and shifted documentation evidence.

Reviewed tree: `942f26fe59d72990af8ddc5ac6937921b5e401ec`. Scope: [issue #8](https://github.com/kebag-logic/lwSRP/issues/8), [PR #9](https://github.com/kebag-logic/lwSRP/pull/9), and the [public review assignment](https://github.com/kebag-logic/lwSRP/pull/9#issuecomment-6031460658). The owner's release decision is dated 2026-10-07. This review also applies the assignment's explicit history-wide hygiene requirement.

Reconstruction covers repository guidance and documentation, public acceptance, linked authorities, the independent diff/history pass, and public executable evidence. No repository AGENTS.md exists; the supplied command guidance and CONTRIBUTING.md were applied. The independent verdict and ledger were written before querying prior review findings. No other reviewer's report was read. Private author material, other checkouts, and management storage were not inspected.

**R539-1-01 — MAJOR — Conformance, Robustness, Docs — OPEN**

Artifact: historical root guidance blob `21654351bd62a20125f6c9209b55bdf9a8ce7f57`, lines 1 and 3; historical `doc/architecture.md` blob `396d6fe887b6fb807a1939e14eb6f144b95c6e9c`, line 36. Restricted provenance identifiers remain in both objects. They are absent from the current tree but present in five reachable ancestors, including `fed1a0d0a08e1f9682ce1fca3bb4b9985d846e5b` and `19f5796b63652eb1151906de73cb827d4980a53f`. Sensitive strings are intentionally not repeated here.

Authority/evidence: the review assignment requires public-release hygiene across the whole tree **and history**. [Reachability receipts](receipts/history-reachability.json) identify the ancestor commits; [the history audit](receipts/history-scan.json) covers all 13 reachable commits and 109 unique blobs. The [release scope](https://github.com/kebag-logic/lwSRP/issues/1) also excludes private provenance from the public release.

Impact: publishing the current history exposes the removed identifiers. Deletion at the tip does not satisfy the history-wide gate. This is a privacy-rule violation, so it cannot be classified as wording residue.

Required outcome: the manager must establish a publication history that removes the prohibited material from every ref intended for public release. Preserve required attribution and the reviewed source behavior. This reviewer performed no history rewrite or source fix.

Verification: audit a fresh clone of the proposed publication refs, including ancestor blobs and commit messages. Confirm that both cited objects and every equivalent occurrence are no longer publicly reachable, and revalidate the resulting release head.

**R539-1-02 — MINOR — Conformance, Docs — OPEN**

Location: [doc/integrator.md:147](https://github.com/kebag-logic/lwSRP/blob/375dbe132c6f1498f2f3e714ce5905d34456c9d5/doc/integrator.md#L147), with additional affected citations in the developer, manager and tester guides.

Authority/evidence: this PR inserts source-header lines while preserving main's documentation byte-for-byte. The integration guide's “Leave interval” link still selects `src/include/shish_lan/mrp.h#L118`. At the reviewed head, line 118 defines the **Join** interval as 20; the intended **Leave** interval of 60 is at line 119. In `doc/developer.md:161`, the selected range `mrp_mad.c#L161-L162` now includes the QA row and an LA comment, omitting the LA transition at line 163. The stream-address citations at `doc/integrator.md:101` and `doc/manager.md:32` omit the initializer at `msrp.c:354`. [The citation receipt](receipts/shifted-citations.json) lists all 68 shifted occurrences and their corrected fragments.

Impact: numerical and conformance statements link to incorrect or incomplete implementation evidence. The link checker only validates existence and line bounds, so its successful result does not detect this defect. This is not pure wording residue: it affects the evidence supporting measurements and clause comparisons.

Required outcome: update all affected fragments for the added headers. Specifically, change the Leave link to `#L119`, the LA range to `#L162-L163`, and the stream-address range to `#L353-L354`. Review the complete receipt rather than changing only these examples.

Verification: inspect each resulting selected range against its surrounding statement, then rerun local link validation. The cited Leave line must contain `MRP_LEAVE_TIME_CS` with value 60, and the LA/address selections must include their executable initializers.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
| --- | --- | --- | --- | --- |
| Conformance | UNCLEAN | Frozen issue acceptance; official licence; NOTICE; 43 headers; both-parent merge; history; clause-evidence citations. Findings 01 and 02. | R539-1 | 375dbe132c6f1498f2f3e714ce5905d34456c9d5 |
| RTL | CLEAN — not applicable | All 45 tracked files and both merge deltas; no RTL, HDL interface, or RTL change. | R539-1 | 375dbe132c6f1498f2f3e714ce5905d34456c9d5 |
| Robustness | UNCLEAN | Historical disclosure, executable-byte preservation, shell execution, Python syntax, YAML/Kconfig parsing, scenario parsing. Finding 01. | R539-1 | 375dbe132c6f1498f2f3e714ce5905d34456c9d5 |
| Tests | CLEAN | Host build, nine tests/1690 assertions, three scenarios/ten steps, direct unit run, excluded queue syntax, preserved harness. | R539-1 | 375dbe132c6f1498f2f3e714ce5905d34456c9d5 |
| Docs | UNCLEAN | Retained README; all 290 local links; eight licence/notice links; sentence/reference checks; source citation semantics; historical guidance. Findings 01 and 02. | R539-1 | 375dbe132c6f1498f2f3e714ce5905d34456c9d5 |

**Positive evidence and limits**

[LICENSE](https://github.com/kebag-logic/lwSRP/blob/375dbe132c6f1498f2f3e714ce5905d34456c9d5/LICENSE) is exactly equal to the [official Apache text](https://www.apache.org/licenses/LICENSE-2.0.txt): 11,358 bytes, SHA-256 `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`. No whitespace normalization was needed. NOTICE names the project and copyright holder, with informational licence attribution and no additional conditions; this is appropriate for section 4(d). [Static receipts](receipts/static-audit.json) cover both files and every header. The shell script correctly preserves its shebang, followed immediately by SPDX.

Against `02700d9ead0a29dd5d53c1d85e163ea392b79ab0`, the change is LICENSE, NOTICE, and 27 single-line comment additions. Removing those added comments restores every changed pre-existing file byte-for-byte. The README equals main's version. The placeholder unit file remains deleted. LICENSE and NOTICE equal the first parent's copies. The tests and documentation brought in by the main merge survive; the shifted citations are the integration defect recorded above.

History and content inspection found no competing licence, vendored third-party implementation, credential, private host path, private device identifier, or account reference outside permitted commit identities. The history-provenance exception is Finding 01. Issue #8 supplies the owner's authorship declaration. The queue credits an external algorithm, without a third-party code copyright or competing licence notice. Repository inspection cannot independently establish original authorship beyond the available record.

| Executed check | Result | Receipt |
| --- | --- | --- |
| Host configure and `make -j16` | Exit 0 | [configure](receipts/configure.log), [build](receipts/build.log) |
| Verbose ctest and direct unit run | Exit 0; nine tests, 1690 passing assertions | [ctest](receipts/ctest.log), [direct](receipts/unit-direct.log) |
| Scenario execution | Exit 0; three scenarios, ten steps, none skipped | [scenarios](receipts/scenarios.log) |
| Scenario parsing; Python syntax; shell parse and execution | All exit 0 | [validation index](receipts/validation-index.json) |
| Kconfig and module YAML | Exit 0; boolean selection and referenced paths checked | [Kconfig](receipts/kconfig-parse.log), [module](receipts/module-parse.log) |
| Queue source omitted by the normal build | Syntax check exit 0 | [exit receipt](receipts/queue-syntax.rc) |
| Local documentation links | Exit 0; 290 links, including all eight licence/notice links | [links](receipts/local-links.log), [licence links](receipts/license-links.json) |
| Sentence/reference checks and reference self-test | Exit 0 | [sentences](receipts/sentences.log), [references](receipts/references.log), [self-test](receipts/reference-self-test.log) |
| External links | Exit 1; 17 pass, standards publisher returns HTTP 403 | [external links](receipts/external-links.log) |

The initial host configure failed because the unit dependency was absent. That receipt is retained. A public release of the dependency was built solely under disposable scratch storage; completed suites then passed. No shared installation was changed. Six repository URLs passed with authenticated access; public anonymous access remains unverified. No diagrams changed against main, so full graph rendering was not repeated; invoking the renderer's help is only Python-entrypoint evidence.

The [public evidence packet](https://github.com/kebag-logic/milan-fpga/tree/9d6a0632c73f5a2c6fd61dc827f97f6014b60a85/review-evidence/lwsrplic-r1) was read after the independent diff pass. All seven author artifacts matched the archive's manifest and their Git blob identifiers. [Verification receipt](receipts/public-evidence-verification.json). The earlier checkpoint explicitly reports a placeholder suite and scenario setup failure at `fed1a0d`; these are not exact-head passing evidence. The merge validation logs report 1690 assertions and three scenarios, consistent with this reviewer's rerun.

At observation, issue #8 had no comments. PR #9 had two review-start announcements, no formal reviews, and no inline review comments. There were no prior public FINDINGS to resolve or retain. [Reconciliation receipt](receipts/prior-review-check.json). Exact-head hosted queries returned zero workflow runs, zero check runs, and zero commit statuses; the aggregate status was pending. No executed or skipped hosted context is counted as a pass. [Hosted receipt](receipts/hosted-state.json).

**Real limits and manager duties**

The manager's passing full source static/builder and native banks are stated in the assignment; this reviewer did not rerun prohibited parent banks. No manager bank-result comments were present on issue #8 or PR #9 at observation. The archived author packet does not substitute for final candidate acceptance.

The manager owns the final current-dev candidate, using source base `02700d9ead0a29dd5d53c1d85e163ea392b79ab0` and live dev `09f1841bd2c6a9dea8eb1994d887f7386ca4f62d`. Its merge-turn build and hosted/local-runner acceptance remain separate duties. Physical calibration: **NOT RUN**. Field skips provide no hardware proof. No target hardware, full parent banks, or interoperability campaign was run.

Passing codec assertions do not establish protocol conformance. The scenario state-observation weakness remains documented in issue #4 and was not introduced by this PR. This review checks licensing and preservation of the existing behavior; it does not close those protocol or coverage gaps.

The manager must resolve Findings 01 and 02, obtain clean reviews at the resulting candidate, complete the final acceptance duties, and verify anonymous access after publication. No RESIDUE or SUGGESTION is recorded. No publication or GitHub write was performed.

[Final integrity evidence](receipts/integrity.json) verifies all 45 tracked blob bytes and modes, the index, reviewed head/tree, and the disposable validation source. The checkout is clean. There are no submodule gitlinks or .gitmodules at this head. Scripts and reproduction guidance are in [REPRODUCE.md](REPRODUCE.md). Independent jobs were joined within foreground orchestrators; no job remains running. Publish only REPORT.md and files listed in MANIFEST.sha256. Scratch storage contains unpublished raw logs, dependency sources and builds.

R539-1 FINISHED
