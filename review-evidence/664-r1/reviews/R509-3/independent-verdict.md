[R509] POSITIVE - exact head 4dab80ae4564ef8d6e1030564dcea4ba19235ee6

Round R509-3 is an external independent review of the ingress-filter requirement delta for issue #664 / PR #674. Tree: `bcca74ee4dd8c8a4a45b26e0b7accda5131f9ce1`. All five lenses were applied independently before reading prior findings. No new finding was identified.

This initial independent verdict and ledger were written before prior public finding reconciliation. The final report will record that reconciliation separately.

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

Limits and manager duties: implement and validate the filter in its assigned later contract lane; record decision parity and the second independent review; close all review rounds; construct and validate the final current-dev candidate; accept hosted and local-replica evidence; obtain explicit merge authorization; update the closure keyword; run post-merge containment and close/move the issue only afterward. Source validation does not clear those duties. The historical evidence packet names an earlier head; the current issue comment and PR body enumerate new-head source results. No full banks, hardware, hosted jobs, local replica or physical calibration were run in this review. Calibration NOT RUN and field skips do not prove hardware behavior. No source edits, commits, pushes or GitHub writes were made.

R509-3 FINISHED
