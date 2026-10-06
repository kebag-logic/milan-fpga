[R509] POSITIVE - exact head 4dab80ae4564ef8d6e1030564dcea4ba19235ee6

Round R509-3 is an external independent review of the ingress-filter requirement delta for issue #664 / PR #674. Tree: `bcca74ee4dd8c8a4a45b26e0b7accda5131f9ce1`. All five lenses are CLEAN. No BLOCKER, MAJOR or MINOR remains. Two wording-only residues are retained below; neither changes coverage or the verdict.

All five lenses were applied independently, and the verdict and ledger were written in independent-verdict.md before reading prior public findings. The reconciliation below followed that independent pass. No private author material, management checkout or other reviewer's report was read before that verdict and ledger.

The governing public decisions are [the filter rule](https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6014311316), [approval of the preceding text](https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6014321497), and [the round-3 assignment](https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6014341135). The issue's earlier VERSION and placement language is superseded by public decision 6009576644. This round approves requirement text, not implementation of the future filter.

[R509] PASS Conformance - REQUIREMENTS.md:42,58,68; docs/reference/FR_NFR.md:322,328,406,599 - All five owner rules appear, with all six table rows, exact destination/EtherType/subtype combinations, per-interface own MACs, separate identity terms and retained token buckets. Both AECP directions include the liveness response. Primary clauses confirm MVRP addressing, multicast ACMP transmission and the two identity fields; own-unicast ACMP reception is explicitly a project tolerance. See clause-checks.md and standards-identity.json.

[R509] PASS RTL - ingress.diff; docs/design/MAILBOX_SPLIT.md:149; sw/mailbox/mailbox.yaml:372; hdl/milan/mailbox/KL_mbx_rx.sv:113,146,208 - The delta changes no RTL, bus interface, clock/reset, CDC, firmware or generated contract. The existing classifier and acceptance path were examined to verify the implementation boundary. The design note explicitly assigns the new MAC checks, response identity and counter to the contract lane after FT, before F2 to F5. Existing F0 behavior is not claimed to implement the new rules.

[R509] PASS Robustness - REQUIREMENTS.md:76; docs/reference/FR_NFR.md:403,405,406,409,410,412 - Rejected tagged, foreign-address, wrong-EtherType/subtype and identity-mismatch input is observed before publication; no record and no core delivery are required. The counter increments once for each untagged control tuple failure and excludes valid/tagged input. Crossed AECP IDs, unrelated opposite IDs for positive cases, each interface MAC, untagged AAF/CRF and MRP without an invented subtype prevent vacuous coverage. Token-bucket refusals remain a separate observation.

[R509] PASS Tests - docs/reference/FR_NFR.md:328,394,403,412; tb/verilator/mbx/suite.hpp:259,314,346; checks/results.json - The future hooks require valid controls, independent changes of each tuple/identity input and planted defects through both adapters and the host model. Existing F0 checks were inspected and are not counted as proof of the future filter. All ten focused checks passed, including generator drift/cross-output checks and planted generator controls. These establish documentation and current-contract consistency, not target runtime behavior.

[R509] PASS Docs - docs/design/MAILBOX_SPLIT.md:149; docs/reference/FR_NFR.md:599; public-pr-body.md; scope.log - NFR-SCOUT-08 traces the filter to sw/mailbox/mailbox.yaml and named hooks. All 19 old/new approval entries match source text. The preceding approved text is preserved outside the ingress delta and the permitted dev merge. Documentation, paths, style, navigation, feature status, wire accountability and traceability checks passed.

The independent merge reconstruction produced tree `3243e5dd67cc64bd122d4bb96d230dc4ed999644`, identical to merge `f48d47cd93cc4b46fad3e537dee661fc2cd3ee6d`, with ordered parents `8fb296e3e02985aee27ef04cb08278836b734a14` and `30e3c018b9add0cb182d8f1229eeec062218130d`. After that merge, only REQUIREMENTS.md, docs/reference/FR_NFR.md and docs/design/MAILBOX_SPLIT.md change. All three pre-delta blobs equal their approved-head blobs. Compared with live dev, the branch changes 21 Markdown files and no executable artifact or gitlink. Thus the imported #658 changes are not represented as new ingress work.

Reviewer-owned ledger, scoped to this assigned delta:

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | REQUIREMENTS.md:42,58,68; docs/reference/FR_NFR.md:322,328,406; clause-checks.md | R509-3 | 4dab80ae4564ef8d6e1030564dcea4ba19235ee6 |
| RTL | CLEAN | ingress.diff; docs/design/MAILBOX_SPLIT.md:149; sw/mailbox/mailbox.yaml:372; hdl/milan/mailbox/KL_mbx_rx.sv:113,146,208; scope.log | R509-3 | 4dab80ae4564ef8d6e1030564dcea4ba19235ee6 |
| Robustness | CLEAN | REQUIREMENTS.md:76; docs/reference/FR_NFR.md:403,405,406,409,410,412 | R509-3 | 4dab80ae4564ef8d6e1030564dcea4ba19235ee6 |
| Tests | CLEAN | docs/reference/FR_NFR.md:328,394,412; tb/verilator/mbx/suite.hpp:259,314,346; checks/results.json | R509-3 | 4dab80ae4564ef8d6e1030564dcea4ba19235ee6 |
| Docs | CLEAN | docs/reference/FR_NFR.md:599; docs/design/MAILBOX_SPLIT.md:149; public-pr-body.md; scope.log; checks/results.json | R509-3 | 4dab80ae4564ef8d6e1030564dcea4ba19235ee6 |

Prior public findings were read from [R509-1](https://github.com/kebag-logic/milan-fpga/pull/674#issuecomment-6010388957), [R508-1](https://github.com/kebag-logic/milan-fpga/pull/674#issuecomment-6010426351), [R508-2](https://github.com/kebag-logic/milan-fpga/pull/674#issuecomment-6010971658) and [R509-2](https://github.com/kebag-logic/milan-fpga/pull/674#issuecomment-6011008257). Submitted-review and inline-comment channels contained no additional findings. Earlier unaffected verdicts stand.

| Prior finding | Original severity and all attributable lenses | Disposition at this head |
|---|---|---|
| R508-1-F1 = R509-1-F1 | MINOR; Conformance, Docs | RESOLVED and preserved. docs/reference/FR_NFR.md:368,369 still assigns conflict/loss/retry to B.3.2/Table B.7 and constants to B.3.3/Table B.8. Both rows are byte-identical to the approved head. They remain approved text, correctly absent from round 3's approval table. |
| R509-1-F2 | MINOR; Conformance, Robustness, Tests, Docs | RESOLVED and preserved. docs/reference/FR_NFR.md:361,404,428 and docs/design/MAILBOX_SPLIT.md:352 retain listener receive/expiry starts, every matching sink, discovery/connection and resulting TX completion, one allowance, separate normative waits and adverse-transition checks. The relevant rows and complete blocks are byte-identical to the approved head; prior-resolution.log records the comparisons. |
| R508-1-R1 = R509-1-R1 | RESIDUE; Docs | Publication-wording residue recurs in the revised public body; retained as R509-3-R1 below. Its historical executor-action statement is correctly scoped. |
| R509-2-R1 | RESIDUE; Docs | RETAINED. sw/firmware/ctrl_nvm/README.md:464 is unchanged from the approved head. Exact fix below. |

Finding R509-3-R1: RESIDUE; Docs.

- Artifact: PR #674 body, reproduction paragraph; public-pr-body.md:99.
- Authority/evidence: The public PR exposes the reviewed head, but this paragraph calls it a local candidate and asks readers to obtain it. The qualifier that the executor did not push is accurate; the preparation framing is stale for the published review object. This carries forward R508-1-R1/R509-1-R1's publication-wording concern.
- Impact: Wording only. The exact checkout command remains correct; no measurement, figure, verdict, test, code, generated artifact, conformance/clause claim or privacy rule changes.
- Required outcome / exact fix: Replace that paragraph with: `The published review candidate is 4dab80ae4564ef8d6e1030564dcea4ba19235ee6. Check out that exact commit before reproducing the validation.`
- Verification: Compare the replacement and checkout command with the public head. Carry the fix to the manager's residue checklist.

Finding R509-2-R1: RESIDUE; Docs; retained without reclassification.

- Artifact: sw/firmware/ctrl_nvm/README.md:464.
- Authority/evidence: The limitation still calls F0's switch unmerged; this unchanged page's line 124 calls its HAL merged and docs/design/MAILBOX_SPLIT.md:3 identifies the implemented default-off foundation. The prior public round classified this as publication wording, and the ingress delta does not touch it.
- Impact: Obsolete publication status only. The missing image integration remains a real, unchanged limitation. No measurement, figure, verdict, test, code, generated artifact, conformance/clause claim or privacy rule changes.
- Required outcome / exact fix: Replace the two-line bullet with: `- The #665 switch and its link: no image links this store yet.`
- Verification: Read the corrected bullet against the merged-HAL statement while preserving the unintegrated-store limitation. Carry it to the manager's residue checklist, outside this ingress-only source assignment.

Direct validation: all ten checks in checks/results.json returned zero. Traceability reports 77 modules, zero untested and 5/5 controls. Wire accountability reports 77 checks and zero findings. Document health reports zero findings across 195 Markdown and 1,085 scrubbed text files. The generated mailbox cross-check and all its planted controls passed. scope.log proves merge provenance and all 19 approval entries. No runtime simulation was needed or claimed for this documentation delta. Independent checks ran concurrently under one foreground driver, at most four workers; each has a raw log and exit receipt. No background work remains.

The [fixed historical evidence packet](https://github.com/kebag-logic/milan-fpga/tree/b8faae80174f23ea928a49d0611a21884711c475/review-evidence/664-r1) matches its published manifest but identifies the earlier head a27808375427859dc357f6bfd0a88842062b20ed. It contains handoff/body results and artifact digests, not the full raw bank logs. The current [review-ready comment](https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6014810929) and PR body enumerate 93 zero-exit source commands at this head with explicit skips. The assignment also reports successful manager source/static, builder and native banks. These are source-validation evidence, not executions by this reviewer and not final candidate acceptance. evidence-assessment.md records this distinction.

integrity-before.log and integrity-final.log verify the detached head/tree, all 1,113 root tracked entries, all 876 required-submodule entries, raw blob bytes, file kinds and executable modes, complete stage-zero indexes and unchanged index-flag fingerprints. Required gitlinks are protocol-processor `ead8036035affd53ef4b29979190f2f4f67084c0`, gptp-processor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, and verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. The optional external gitlink is unchanged and uninitialized. No source bytes required restoration. Public-state-final.json confirms the head and PR body stayed unchanged.

Limits and pending manager duties:

- Record the filter-text decision-parity check, the second independent verdict and acceptance of the reviewer-owned ledger. Close all review rounds and carry both residues to the checklist. The earlier 10 ms and non-ingress text approval is preserved, not reopened.
- Construct and validate the final candidate against live dev at the merge turn. The source base is 423ac5d910d09ab189b3acc39ae3ae1d10d50b19; this head includes dev 30e3c018b9add0cb182d8f1229eeec062218130d. That provenance is not a substitute for final candidate validation.
- Complete hosted and local-replica acceptance with executed jobs distinguished from skipped contexts. This reviewer neither queried nor accepted those runs. No full banks, container execution, privilege, hardware or physical calibration were used. Calibration NOT RUN, field skips and desk checks provide no hardware proof.
- Obtain explicit merge authorization, update the closure keyword as assigned, and perform post-merge containment/review-integrity checks before closing and moving the issue to Done. This verdict authorizes no merge or public write.
- The later contract lane still owes the YAML, generated interfaces, filter implementation and planted runtime tests after FT and before F2 to F5. Target timing, all-stream/counter acceptance, audio soak and the VERSION-3 default flip remain later obligations.

Portable reproduction is in REPRODUCE.md. Only REPORT.md and the files listed in MANIFEST.sha256 are publication artifacts. Disposable extracts and other scratch inputs are excluded. No source edits, commits, pushes, GitHub writes, author contact or delegated review occurred.

R509-3 FINISHED
