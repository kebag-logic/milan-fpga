[R237] NEGATIVE - exact head 65df1df50a80cd5f540a93d8f0cfabc97da3da75

Independent internal review R237-r1 of issue #437 / PR #515. Tree: `da06c8609b7a574e3df121fbcb8a1fc8f207dcb7`. Parent and comparison base: `88e9276b2a220c716f64a843f7e1eb8f9265e896`. All five lenses were applied. Three MAJOR findings remain open. This is not merge approval.

The public contract was reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, issue #437 and its public decision, REQUIREMENTS.md section 8, CODE_QUALITY rule 12, docs/DOC_GENERATION.md, architecture/submodule authorities, issues #413/#440, the one-commit PR history and exact diff, then executable evidence. No other reviewer report, private author reasoning or local author-lane material was read.

The [settled decision](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5775771538) fixes family one's escaping list-paragraph classification. Family two takes the explicit limitation path: the three setext forms, quoted ATX heading and indented list-item ATX heading remain omitted. It explicitly preserves acceptance 1, requires unchanged classifications on the tracked corpus, and preserves the exemption, provenance, prior controls and ratchets. It does not authorize new omissions of ordinary top-level ATX headings.

[R237] MAJOR Conformance, Robustness, Tests - scripts/gen_toc.py:458 and scripts/gen_toc.py:549 - F1: A type-7 tag inside the resumed item paragraph hides a visible top-level heading.

Requirement/evidence: The item's paragraph context must be distinguished by its content column. A type-7 tag cannot interrupt the paragraph containing it; the tag's membership in that item matters. See [CommonMark 4.6](https://spec.commonmark.org/0.31.2/#html-blocks) and [5.2](https://spec.commonmark.org/0.31.2/#list-items), CONTRIBUTING.md 6.1 and the selected #437 scope. This exact input demonstrates the regression:

```text
- item

  text
  <span>
## Old
</span>

## Real
```

Fresh GitHub GFM rendering yields `Old, Real`; the parent parser also yields `Old, Real`. The reviewed parser yields only `Real`. The new helper converts the resumed paragraph to `HELD`, but `_opens()` receives no item-column context and treats this still-contained tag as free to open HTML. The same regression occurs at three spaces and with a closing tag or an attributed opening tag: six measured failing combinations. Tags at zero/one spaces correctly open HTML outside this item, and four-space tag controls remain correct. Exact requests, response HTML, timestamps and base/head results are in `renderer-responses.json`, `renderer-summary.json` and `renderer-{base,head}.json`.

Impact: Generated navigation drops a visible top-level section. In 15 real-Git controls, the six regressed combinations also reject a legitimate copied em-dash label: parent `(findings, exemptions) = (0, 1)`, reviewed parser `(1, 0)`, with the specific `mirrors no heading` finding. Head navigation has valid generator provenance; the defect is its base-heading authority. `consumer-summary.json` preserves the full synthetic base/head bytes, commit identities, navigation and verdicts. This is a new regression, not one of the five selected omissions. The shipped fixtures always place the probe tag at column zero (`scripts/gen_toc_container_cases.py:76`), so all shipped gates remain green.

Required outcome: Preserve the resumed item's paragraph for tags still inside it, while retaining the intended HTML opening for tags outside it. Add boundary controls for both consumers without changing the exemption policy or enlarging the documented limitation.

Verification: Reproduce the zero-through-four-space matrix with opening, closing and attributed tags; require renderer agreement for heading presence, correct generated navigation and the intended real-Git exemption/refusal. A mutation removing the relevant distinction must fail the new controls for that distinction. Preserve the prior corpus and #507 controls.

[R237] MAJOR Conformance, Tests, Docs - issue #437 acceptance 1; public renderer receipt 5775985191; scripts/gen_toc_container_cases.py:5 - F2: The eleven historical cases have not been accounted for under the frozen acceptance contract.

Requirement/evidence: Acceptance 1 requires the eleven measured family-one shapes to agree with GitHub, and the selected decision explicitly does not relax it. The [author's exact public receipt](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5775985191) names the historical IDs `H01/H02/H05/H06/H10/H13/H25/H28/H29/H31/G02` but disclaims an exact mapping to them. Its eleven F1 reconstructions include explicit plus-item and custom-tag variants. The public takeover and manager completion continue to disclose the limit without changing acceptance.

I independently replayed all 47 published new fixtures and reproduced their published heading results, including the eleven F1 fixtures, six boundary fixtures, five omissions and 25 additional controls (`published-replay-responses.json`, `published-replay-summary.json`). That validates those new bytes. It does not establish coverage of every historical shape. Equal counts do not establish a one-to-one semantic correspondence.

Impact: A cold reviewer cannot establish acceptance 1's completeness. This is an open evidence/acceptance gap, not an allegation that the new renderer receipts are false. Unavailable archival byte identity alone would not require rejection if every historical case were publicly and adequately reconstructed; the missing case correspondence is the unresolved part here.

Required outcome: Publish retrievable originals or a justified per-historical-ID semantic reconstruction, with exact requests/responses and an explanation sufficient to check that each original distinction is preserved. If that cannot be established, obtain an explicit public maintainer decision changing the acceptance contract before claiming completion. Continue distinguishing newly reconstructed bytes from archival identity.

Verification: Account for all eleven historical IDs without substitutions justified only by total count; run the identified cases through GitHub, navigation and real-Git provenance. Reassess against the still-frozen contract or an explicitly revised public decision. The existing family-two limitation does not resolve this finding.

[R237] MAJOR Conformance, Tests - scripts/gen_toc_container_cases.py:57; public author/mutations.py and mutations-head/markers-in-blocks logs - F3: Block-marker inertness is not protected by the claimed mutation evidence.

Requirement/evidence: Acceptance 3 requires an arm that fails when each new property is removed. The new fixture table explicitly names fenced, commented and HTML-contained markers as inert. I replayed all 17 published mutations in scratch. All fail both shipped self-tests, but `markers-in-blocks` fails only `thematic break is no item` and `noninterrupting ordinal is no item`; none of the block-marker arms fails. The other 16 mutations reach a specifically selected arm for their intended defect (`mutation-results.json`).

A narrower mutation at `scripts/gen_toc.py:460` changes `label == TEXT and after == HELD` to `label != TEXT or after == HELD`. It preserves the existing condition for TEXT lines while allowing non-TEXT block content to seed item context. Both shipped suites still report PASS: 754/754 and 99/99. This mutation is confined to a scratch copy; it is not a defect claimed to exist in the unmodified production source.

Independent controls put `- fake item` inside a fence, comment or raw HTML block, close the block with a two-space-indented closer, then resume two-space text before a column-zero type-7 tag. GitHub and the unmodified head render `Old, Real`; the mutant loses `Old`. With the existing column-zero closer, context is discarded before observation, masking the erroneous marker recognition. See `block-marker-summary.json` and `published-replay-responses.json`. Real-Git controls likewise change from zero findings/one exemption to one `mirrors no heading` finding/zero exemptions (`marker-consumer-summary.json`), without an unrelated added-heading finding.

Impact: The advertised block-precedence property can be removed while both shipped self-tests remain green. Nonzero exits of the broader mutation overstate sensitivity to this particular defect.

Required outcome: Add observable block-marker controls to both consumers and attribute mutation kills to the property actually removed. Preserve the marker context long enough in the negative control to expose erroneous recognition, while retaining correct production behavior.

Verification: The narrower mutation must fail specifically for block-marker classification and real-Git provenance; the unmodified head must pass those controls. Existing thematic-break and ordinal controls must continue to run independently. Do not satisfy this by an unrelated guard failure or a count-only change.

[R237] PASS RTL - exact base/head raw diff in preservation-summary.json; docs/overview/ARCHITECTURE.md:39; docs/reference/SUBMODULES.md:20; final-integrity.json - Product and ownership boundaries are preserved.

Only CONTRIBUTING.md and four Markdown-tooling Python files differ. No HDL, firmware, workflow, configuration, budget, interface or gitlink changes exist. `gen_toc.py` remains the classification owner; every non-selftest function/class in `check_em_dash.py` is AST-identical to the parent. The architecture's fabric, clock/reset/CDC and processor interfaces therefore have no changed product behavior in this PR. This is scoped structural coverage, not fresh physical or exhaustive RTL execution.

Other verified results, with limits:

- `focused-gates.json`: independently ran TOC selftest 754/754, TOC check (105 navigation pages, 17 below threshold), anchor verification (144 existing fragment links), em-dash selftest 99/99 and base gate (zero findings, nine added lines, zero exemptions), docs check and Python idiom gate. All exited zero. These passes do not clear F1-F3.
- `preservation-summary.json`: both parsers produce identical blocks, line kinds, headings/anchors, generated provenance and refusal results on all 163 original pages and all 163 updated pages. All 707 prior arm inputs also classify identically. The 428-arm I440/#507 family remains present, and its source is byte-identical. Guard changes only expand the family/site enumerations; no budget file changes.
- `CONTRIBUTING.md:518` and `scripts/gen_toc.py:375` explicitly name all five retained omissions and their withholding/exemption direction. Independent GitHub controls confirm each omission. No family-two heading or anchor was added. F1 is additional behavior beyond these selected omissions.
- `renderer-summary.json`: 42 independently constructed controls examine content-column type-7 boundaries, quoted/list/table/setext/fence/HTML interactions, empty/ordered/sibling items and retained closer behavior. Six type-7 combinations regress as F1 describes. Intentional setext/container omissions are recorded separately. GitHub's Markdown API supplies heading elements without anchor attributes; these receipts prove heading presence, not newly measured GitHub anchor IDs.
- The immutable [manager packet](https://github.com/kebag-logic/milan-fpga/tree/e6013980ef12e558b633c0d18faecc59f1939e8a/review-evidence/437-r1/manager) attributes 43 static/builder commands and five native groups to `65df1df50a80cd5f540a93d8f0cfabc97da3da75`, base `88e9276b2a220c716f64a843f7e1eb8f9265e896`. Their recorded exits are zero. Selected factual artifacts were fetched by immutable Git blob and verified against published manifest SHA-256 values. No full native/RTL/Yosys/processor/builder rerun was performed here.
- Native logs record 55 parent suites, 2,118,264 checks, zero failures, and four field-campaign skips contributing zero checks; PP records 14,903 checks, zero failures; behave records 14 features, 316 scenarios and 1,515 steps passing. Native Verilator is 5.052. It is not workflow-pinned 5.050 evidence. The builder log explicitly says calibration gate 11 NOT RUN; it supplies no physical measurement.
- The two public manager final-integrity receipts identify this same head/tree and required pins. The manager's candidate-tree equivalence belongs to its recorded base and time. It is not proof about a later live dev tip.

Reviewer-owned lens ledger:

| Lens | Covering round | Exact head | Result/open findings |
|---|---|---|---|
| Conformance | None; applied R237-r1 | 65df1df50a80cd5f540a93d8f0cfabc97da3da75 | UNCLEAN: F1, F2, F3 |
| RTL | R237-r1 | 65df1df50a80cd5f540a93d8f0cfabc97da3da75 | CLEAN within the artifact scope above |
| Robustness | None; applied R237-r1 | 65df1df50a80cd5f540a93d8f0cfabc97da3da75 | UNCLEAN: F1 |
| Tests | None; applied R237-r1 | 65df1df50a80cd5f540a93d8f0cfabc97da3da75 | UNCLEAN: F1, F2, F3 |
| Docs | None; applied R237-r1 | 65df1df50a80cd5f540a93d8f0cfabc97da3da75 | UNCLEAN: F2 |

Open findings: F1 MAJOR, F2 MAJOR, F3 MAJOR. No MINOR or SUGGESTION findings. Acceptance 2's selected limitation and acceptance 4's unchanged-corpus requirement are demonstrated; acceptance 1 remains unproven and acceptance 3 is not met for F3. The focused gates and unchanged ratchets satisfy the measured parts of acceptance 5, without establishing overall completion.

Manager-owned outstanding duties: resolve findings and obtain independent corrected-head reviews; complete reviewer-owned five-lens coverage and the required internal/external positives; finish trusted-dev act replication and required hosted contexts on the relevant exact head; recheck live dev and validate any changed candidate merge result; obtain explicit maintainer merge authorization; complete merge, containment/review-integrity checks, required post-merge hosted completion, and issue/project Closed/Done. A queued wrapper or observed start is not a pass. Following the [round-start boundary](https://github.com/kebag-logic/milan-fpga/pull/515#issuecomment-5777588851), I did not inspect hosted runs, checks, statuses, Actions APIs or hosted dashboards/logs. No CI completion is inferred.

Final preservation: `final-integrity.json` verifies all 852 parent blobs, executable modes/file kinds and index entries against the exact tree, plus 214 verilog-axis, 222 protocol-processor and 103 gPTP files against their committed pins, modes/kinds and indexes. Required submodules remain registered at the correct parent; all recorded statuses are clean. The optional unused external gitlink is unchanged and was not initialized or claimed as tested. The review checkout received no source fixes, commits, pushes or metadata changes. No other agents, author contact, installs, privilege changes, hardware, Docker/act or candidate act runner execution occurred. Focused controls used at most eight concurrent jobs; all mutations and synthetic commits stayed in isolated scratch.

Reproduction commands and artifact descriptions are in `COMMANDS.md`. This report is for faithful manager publication with path neutralization; the reviewer did not self-publish.

R237-r1 FINISHED
