[R535] POSITIVE - exact head cd659eb5e93c4da5e97fcbd6282b1efba16e565d

All five lenses are CLEAN for this documentation change. No open BLOCKER, MAJOR, MINOR, RESIDUE, or SUGGESTION remains.
Every prior finding is resolved at this head. This verdict does not establish protocol conformance or deployment readiness.

Reviewed tree: `e5bb35e6cd2efd707cbedaf5d799b8877a0aab30`.
The full comparison is `19f5796..cd659eb5e93c4da5e97fcbd6282b1efba16e565d`.
The round-3 delta is one commit after `5f9b9d99e1d94485fc00a1b1539baf2ae861cb65`.
The assignment is the [round-3 scope decision](https://github.com/kebag-logic/lwSRP/issues/1#issuecomment-6031053742).
The [public review start](https://github.com/kebag-logic/lwSRP/pull/5#issuecomment-6031210740) identifies this exact head.

Reconstruction followed the requested order: repository guidance and documentation; frozen issue and scope decisions; requirements and interfaces; diff and history; public execution evidence.
No repository instruction file exists at this head.
The [initial assignment](https://github.com/kebag-logic/lwSRP/issues/1#issuecomment-6030336537) separates licence work and prohibits protocol-source changes.
The [round-2 decision](https://github.com/kebag-logic/lwSRP/issues/1#issuecomment-6030706379) authorizes the test-harness merge.
The full PR includes that merge; the final commit changes documentation and the reference checker only.
Production protocol sources, platform sources, embedded module files, and their interfaces are unchanged.
See the [history](receipts/history.txt), [full change inventory](receipts/diff-stat.txt), and [round-3 patch](receipts/round3-diff.patch).

The [independent verdict and ledger](receipts/independent-verdict.md) were written before opening prior review findings or reports.
Only then were the [prior external findings](https://github.com/kebag-logic/lwSRP/pull/5#issuecomment-6031016045) and [prior internal findings](https://github.com/kebag-logic/lwSRP/pull/5#issuecomment-6031046955) reconciled.
No current-round peer report, private author material, or lane scratchpad was used.

The table closes every prior finding. Severity and lenses identify the original defect; none remains open.
The round-3 decision requires the reference corrections regardless of their earlier residue labels.

| Prior item | Severity; attributable lenses | Required outcome, impact removed, and verification at this head | Status |
| --- | --- | --- | --- |
| R534-1-01 | MINOR; Conformance, Docs | The [manager matrix](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/doc/manager.md#L35) assigns propagation to 35.2.4 and states that 35.2.3 service primitives are absent. Checked against the normative headings, propagation policy at `src/modules/msrp.c:132–185`, and public stream interface. The clause-mapping defect is removed. | RESOLVED |
| R534-1-02 | MINOR; Conformance, Docs | The manager matrix and [transmit guidance](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/doc/integrator.md#L101) disclose the incorrect address, cite 35.2.2.1/Table 8-1, and link [issue #6](https://github.com/kebag-logic/lwSRP/issues/6) and `src/modules/msrp.c:352–353`. The [runtime receipt](receipts/receive-probe.log) confirms 91-E0-F0-00-0E-80. Integrators are warned against using it for conforming transmission. | RESOLVED |
| R534-1-03 | MINOR; Conformance, Docs | The [Registrar comparison](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/doc/developer.md#L208), manager matrix, and [receive guidance](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/doc/integrator.md#L118) disclose cross-type delivery to Applicants and Registrars. They link [issue #7](https://github.com/kebag-logic/lwSRP/issues/7), handler lines 835–841, and parser lines 154–155. Checked against 10.7.5.20. The [probe](receipts/receive-probe.log) reproduces a Listener LeaveAll moving a Talker registration IN→LV. The omitted scope limitation is now explicit. | RESOLVED |
| R534-1-04 | MINOR; Tests, Docs | The [tester coverage section](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/doc/tester.md#L103) and [manager evidence section](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/doc/manager.md#L56) explain both repeated-operation assertions and link [issue #4](https://github.com/kebag-logic/lwSRP/issues/4). A planted wrong-disable dispatch [still passes all three scenarios](receipts/wrong-disable-scenarios.log). The pages no longer imply this proves the disabled state. | RESOLVED |
| R534-1-05 and R535-1-01 | MINOR; Conformance, Docs | The [data-structure graph](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/doc/developer.md#L29) places the attribute list before the shortened port-timer node. The attribute-list/value edge is visible and clear of unrelated nodes. Independently rendered at [native size](graphs/doc-developer.md-29-native.png) and [page width](graphs/doc-developer.md-29-page.png), both 697 × 486. All other graphs received the same review. The ownership ambiguity is removed. | RESOLVED |
| R534-1-06 | Previously RESIDUE; Docs, Conformance | Every specified correction is present: the [build-setting link](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/doc/integrator.md#L17) targets its defining documentation; all three C11 references link the ISO page; both prose SPDX references link their authority. The [Registrar range](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/doc/developer.md#L182) ends at 395. The [Leave interval](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/doc/integrator.md#L147) links its arming action and constant. Targets and relevant ranges were checked. | RESOLVED |
| R535-1-02 | Previously RESIDUE; Conformance, Docs | C11 is linked in the [overview](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/README.md#L29), integrator build table, and tester prerequisites. The [79-case self-test](receipts/reference-self-test.log) passes. Planted [bare C11](receipts/bare-c11.log) and [inline C11](receipts/inline-c11.log) each return 1; restored prose returns 0. The [ISO catalogue page](https://www.iso.org/standard/57853.html) was opened and identifies ISO/IEC 9899:2011. | RESOLVED |
| R536-1-01, carried through R535-1 | Previously RESIDUE; Docs | The [architecture test-layout table](https://github.com/kebag-logic/lwSRP/blob/cd659eb5e93c4da5e97fcbd6282b1efba16e565d/doc/architecture.md#L68) links both the actual unit runner and scenario bindings. The obsolete placeholder remains absent. This satisfies the stricter carried outcome from the prior external review. | RESOLVED |

The five prior suggestions are also addressed.
The file-reference pattern detects the module-configuration suffix, confirmed by a [planted bare filename](receipts/bare-kconfig.log).
The integrator guide identifies the contradictory module tick instructions.
The developer code map includes the four test artifacts.
The contribution guide applies brace rules to new and changed lines.
The stream-value matrix cites declaration type, attribute type, and FirstValue authorities.
The checker remains a documented heuristic; deriving every filename from the tree is not a required remaining change.

The owner's four rules were reapplied to the whole PR:

| Rule | Current assessment | Evidence |
| --- | --- | --- |
| Short sentences | PASS: 760 sentences/fragments; zero above 25 words; zero prose exemptions. | [Sentence receipt](receipts/sentences.log), plus manual review of all eight pages. |
| Every reference is linked | PASS for the reviewed prose. Standards, clauses, files, functions, issues, and named development utilities have links. Literal fenced syntax is identified. | [Reference receipt](receipts/references.log), [self-test](receipts/reference-self-test.log), planted-reference receipts, and manual target review. |
| Explain use for each reader | PASS: developer extensions and state comparisons; integrator platform contracts and six sequences; manager implementation limits; tester commands, scenarios, and coverage. | Four guides, overview navigation, contribution rules, and [claim mapping](receipts/code-claims.md). |
| Readable, clean, clear graphs | PASS: all 22 independently rendered; 2–11 named nodes or participants; no edge crosses an unrelated node. | [Render receipt](receipts/graph-render-final.log), [individual visual assessments](receipts/graph-inspection.md), and [geometry](receipts/graph-geometry.json). |

Every graph was inspected at native size and a 760-pixel page width.
Fifteen graphs retain native dimensions; their page images are byte-identical. Seven wider graphs were inspected after reduction.
The widest creation sequence has compact but legible labels at page width, with distinct arrows and no ambiguity.
The [final preview repeat](receipts/graph-repeat.json) confirms that all 44 images match the visually inspected set.
Rendering success alone was not treated as a readability result.

All seven acceptance items have supporting evidence:

| Acceptance | Result |
| --- | --- |
| Small, rendered, readable graphs | PASS as documented per graph above. |
| Resolving links | 290 local occurrences and 18 external URLs checked. Exactly eight expected licence/notice dependencies and one expected automated ISO 403 remain. Six repository URLs pass authenticated checks; eleven other external URLs return 200. [Raw link results](receipts/links.log). The ISO page exists, independently verified. |
| Sentence limit and explicit exceptions | PASS. Fenced syntax exceptions are listed; no prose exemptions. |
| No bare clause, file, or issue references | PASS, with additional standard-name coverage and independent negative controls. |
| Every published command executes with recorded exit code | All 17 occurrences executed, including repeated sequences and the complete compiler here-document. Sixteen return 0. The link check returns 1 for the specified exceptions. [Command ledger](receipts/page-commands.md). |
| Claims checked against code | PASS for the bounded claims. [Independent claim mapping](receipts/code-claims.md) covers six state graphs, the manager matrix, storage, receive behavior, timers, adapters, build choices, and coverage. |
| Public-safe content | PASS: eight pages carry the required licence metadata; obsolete instruction and drawing artifacts are absent. Current prose has no private-path, private-host, or prohibited-assistance identifiers. [Publication audit](receipts/publication-audit.json). |

The execution results independently reproduce the current claims:

| Check or probe | Result |
| --- | --- |
| Both configure/build sequences | Every command returns 0. |
| Both configured unit-suite invocations | Return 0; the configured target passes. |
| Direct configured runner and isolated codec executable | Each returns 0, with nine tests and 1,690 assertions. |
| Both scenario executions | Return 0; one feature, three scenarios, ten steps; none skipped. |
| Scenario dry run | Returns 0 for matching only; no behavior executes. |
| Reference self-test | 79 cases; zero failures. |
| Bare C11, inline C11, ISO and SPDX mutations | Each returns 1; restoration returns 0. |
| Bare module filename, 26-word sentence, missing heading | Each fails its relevant check. The heading fixture adds its explicit error to expected missing licence links. |
| Empty unit suite | Direct runner returns 0 without assertions; configured suite returns 8 and rejects it. Restored executable passes. |
| Wrong-disable dispatch | Build and scenarios return 0, reproducing the documented limitation. Disposable source restored. |
| MSRP address and Listener LeaveAll probe | Returns 0 while confirming both documented deviations. |

The [scripts](scripts/README.md) reproduce these checks using disposable exports and a packet-local dependency prefix.
Independent campaigns ran concurrently inside joined foreground processes.
The dependency build used 16 jobs; no heavy parent build or hardware run was performed.
The [environment receipt](receipts/environment.json) records versions and the pinned dependency identity.

The reviewer-owned ledger covers the complete PR at this exact head:

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | Frozen issue and scope decisions; all acceptance items; normative tables and clauses; manager matrix; code-backed disclosures; graph and reference requirements | R535-2 | cd659eb5e93c4da5e97fcbd6282b1efba16e565d |
| RTL | CLEAN | Complete tree and diff inventory; host/module source lists; switch, queue, and platform boundaries. No RTL/HDL artifact, production-source change, or gitlink exists in scope. | R535-2 | cd659eb5e93c4da5e97fcbd6282b1efba16e565d |
| Robustness | CLEAN | Checker source and negative fixtures; reference restoration; parser/callback delivery; timer lifetime and global ticking; queue contract; receive probe; integration warnings | R535-2 | cd659eb5e93c4da5e97fcbd6282b1efba16e565d |
| Tests | CLEAN | Build definition, runner, codec suite, bindings, lifecycle hook and steps; all 17 commands; wrong-disable and empty-suite probes; public execution receipts | R535-2 | cd659eb5e93c4da5e97fcbd6282b1efba16e565d |
| Docs | CLEAN | Eight pages; 22 graphs; four audiences; current PR description; reference/target review; sentence and privacy checks; every prior finding and suggestion | R535-2 | cd659eb5e93c4da5e97fcbd6282b1efba16e565d |

Clean lenses concern documentation acceptance, not the correctness of every existing implementation path.
The documented address, cross-type delivery, timer lifetime, incomplete transmission, parser, and state-table limitations remain real.
The focused receive probe confirms a limitation; it does not provide general state-machine or parser coverage.
The normative review covers displayed transitions and stated differences, not complete standards certification.
No RTL simulation was necessary or executed.

Public evidence was distinguished by revision and provenance.
All eleven files in the [initial public archive](https://github.com/kebag-logic/milan-fpga/tree/3f31bba3bfade7da27bc45f42080aae9a9887a22/review-evidence/lwsrpdoc-r1) match its published manifest.
All 35 files in the [round-3 author packet](https://github.com/kebag-logic/milan-fpga/tree/21b72908/review-evidence/lwsrpdoc-r1/author-r3) match its published manifest.
See the [initial hashes](receipts/initial-public-evidence-hashes.json) and [round-3 hashes](receipts/public-evidence-hashes.json).
Earlier measurements were treated as historical; current measurements were independently repeated.

The [public snapshot](receipts/public-snapshot.json) returned zero exact-head workflow runs, check runs, and commit-status contexts.
Its empty combined status is pending. This represents neither executed success nor a skipped job.
There were no formal reviews or inline review comments beyond the recorded conversation findings.
No manager execution-evidence comment or manager bank receipt was present in the inspected issue, PR, or cited archive.
The assignment reports passing manager source static/builder and native banks; those banks were not rerun or relabelled as reviewer execution.

The manager retains publication, the two-independent-review requirement, hosted/local workflow acceptance, and the final current-development candidate build at the merge turn.
The reviewed source base `19f5796` is distinct from live development `09f1841bd2c6a9dea8eb1994d887f7386ca4f62d`.
The PR base observed during collection is recorded in the snapshot; it did not change the requested comparison.
Verify separate licence files in the combined release, then repeat anonymous repository-link checks after publication.
No residue item from this review needs carrying forward.

No embedded target, network interoperability, hardware, or physical calibration was executed. Physical calibration is NOT RUN.
Field skips are not hardware proof.
Visual judgment covers the recorded renderer and 760-pixel page width; another renderer or narrower display may produce a different layout.
External-link results are dated observations. The ISO automated 403 and eight licence dependencies are expected, not findings.

The [final integrity receipt](receipts/integrity.json) verifies 43 tracked blobs and executable modes, the unchanged index, exact HEAD/tree, and clean status including ignored files.
There are zero required submodule gitlinks in this standalone tree.
All mutations occurred in disposable exports; their source or executable bytes were restored.
No source fixes, commits, pushes, merges, external writes, shared installs, or edits to another checkout were performed.
Only files listed in [MANIFEST.sha256](MANIFEST.sha256), together with this report, are publishable. Scratch is excluded.

R535-2 FINISHED
