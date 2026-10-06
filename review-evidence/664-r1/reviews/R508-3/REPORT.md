[R508] POSITIVE - exact head 4dab80ae4564ef8d6e1030564dcea4ba19235ee6

R508-3, internal independent review of issue #664 / PR #674. All five lenses are CLEAN for the assigned ingress-filter requirement delta. No open BLOCKER, MAJOR or MINOR was found. Prior technical findings remain resolved. One existing wording RESIDUE remains for the manager.

Tree: `bcca74ee4dd8c8a4a45b26e0b7accda5131f9ce1`.
Source base: `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`.
Approved requirement head: `8fb296e3e02985aee27ef04cb08278836b734a14`.
Merged and observed live dev: `30e3c018b9add0cb182d8f1229eeec062218130d`.

Reconstruction followed repository instructions and the documentation index, then the frozen issue with public scope decisions, requirements and interface authorities, diff/history, and public evidence. The independent verdict and five-lens ledger were written before opening prior public findings; `receipts/independent-verdict.md` preserves that checkpoint. No private author material, other checkout or private review report was read.

Scope follows [assignment 6014341135](https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6014341135), [filter decision 6014311316](https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6014311316), and [approval 6014321497](https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6014321497). Earlier conclusions stand where unaffected. The owner-approved service budget and placement text are not reopened.

**Scope and preservation**

`receipts/scope.log` proves merge `f48d47cd93cc4b46fad3e537dee661fc2cd3ee6d` has the approved head and dev as its ordered parents. Recomputing their merge reproduces its exact tree, `3243e5dd67cc64bd122d4bb96d230dc4ed999644`. The subsequent commit changes only `REQUIREMENTS.md`, `docs/reference/FR_NFR.md`, and `docs/design/MAILBOX_SPLIT.md`. Each file's pre-filter bytes equal its approved-head bytes. Every other change since approval belongs to that exact dev merge, including imported #658 work.

The requested original-base diff, approved-head diff and authored filter diff were measured separately; their identities are in `receipts/scope.log`. The authored delta is `receipts/round3.diff`. Mailbox YAML, RTL, firmware, executable mailbox tests and the split architecture document are unchanged from approval. No source correction or mutation was made.

The public owner-approval section contains exactly 19 filter entries. Every old/new cell matches source after decoding table escaping, replacing links with their visible labels and normalizing whitespace. Everything else is explicitly approved at `8fb296e3`. `receipts/pr-approval.json` retains that section and the complete public body's digest. The public head and complete body were rechecked unchanged at the end.

**Artifact-specific lens results**

[R508] PASS Conformance - `REQUIREMENTS.md:41`, `:57`, `:67`, `:76`, `:84`; `docs/reference/FR_NFR.md:322`, `:328`, `:599`; owner decision 6014311316 - All five owner rules and channel terms are present.

Tagged frames cannot enter a mailbox. The six table rows specify destination, EtherType, subtype where applicable, and identity; untagged AAF/CRF have no channel. ADP, ACMP and MAAP identities match the owner table. ACMP own-unicast admission is explicitly a receive tolerance. AECP requires the receiving interface's own MAC and either an own-target command or an own-controller response. Foreign unicast is rejected. Untagged control tuple failures increment FILTER_MISMATCH, while token buckets remain mandatory. NFR-SCOUT-08 traces these rules to the YAML and named hooks.

Direct standard reading confirms IEEE 802.1Q-2018 Table 10-1 assigns `01-80-C2-00-00-21` to Customer Bridge MVRP. IEEE 1722.1-2021 8.2.1 requires multicast ACMP transmission; Table B.1 assigns `91-E0-F0-01-00-00` to ADP/ACMP. The latter table was visually checked because extraction corrupts its address glyphs. Milan v1.2 5.4.5.3 requires controller liveness probing and processing the reply; IEEE 1722.1-2021 7.4.4 uses the base AEM command/response format. These support the labelled tolerance and own-controller response case. Primary file identities are in `receipts/clause-sources.json`. No clause discrepancy remains.

[R508] PASS RTL - `docs/design/MAILBOX_SPLIT.md:149`; `sw/mailbox/mailbox.yaml:377`; `hdl/milan/mailbox/KL_mbx_rx.sv:115`, `:148`, `:212`; `docs/reference/MAILBOX_CONTRACT.md:299`; `receipts/scope.log` - Required and currently implemented behavior are explicitly separated.

The unchanged F0 classifier uses EtherType/subtype and existing accept terms; the AECP YAML term compares target identity. Its current register/port contract lacks the proposed per-interface own-MAC comparison and FILTER_MISMATCH counter. The new design note acknowledges this gap and assigns YAML, generated output and test changes together to the contract lane after FT, before F2-F5. The record already carries interface identity, and complete-record publication remains the delivery boundary. No new clock, reset, CDC, width, arbitration or resource behavior is implemented by this documentation delta. Current F0 behavior is not approved as satisfying NFR-SCOUT-08.

[R508] PASS Robustness - `docs/reference/FR_NFR.md:403`, `:406`, `:410`, `:412`, `:447`; `REQUIREMENTS.md:76`; `tb/verilator/mbx/suite.hpp:313`, `:353`, `:405` - Rejection, identity and overload cases have distinguishable outcomes.

Hooks independently vary tag, destination, EtherType, subtype and identity, with a valid positive control per table row. Rejection must create neither a published RX record nor core delivery. An unassigned AVTP subtype avoids accidentally constructing a valid different channel. MSRP/MVRP tests substitute AVTP without inventing an MRP subtype. Untagged AAF/CRF are explicit negatives. Each untagged control tuple mismatch increments once; valid and tagged input do not increment that counter. Token-bucket refusal is observed separately.

AECP checks defeat an overbroad identity OR: a foreign-controller response is rejected even with own target, and a foreign-target command is rejected even with own controller. Positive cases use unrelated opposite IDs, exposing command-only and both-IDs-required filters. CONTROLLER_AVAILABLE is explicit. Per-interface own-MAC checks reject another interface's MAC and foreign destinations. Shared hook obligations retain saturation, reset, wrap, CPU stalls, both adapters and supported placements. These are falsifiable future integration requirements, not executed ingress results here.

[R508] PASS Tests - `docs/reference/FR_NFR.md:328`, `:395`, `:412`; `tb/verilator/mbx/frames.hpp:59`, `:73`, `:98`; `tb/verilator/mbx/suite.hpp:313`; `receipts/focused-results.json` - The specified checks can expose the new filter defects without claiming present runtime coverage.

The hooks observe ingress before publication, preventing rejected input from disappearing from an RX-only measurement. They require planted acceptance-rule defects to fail their named hooks through both adapters and the host model. The unchanged suite and clause-derived frame builders provide current target-ID, tagged-frame and rate-limit checks; they do not establish the new destination/direction/counter behavior. No runtime simulation was performed for this requirements-only delta.

Nine focused checks ran concurrently under one foreground process, at most four workers, each with a raw log and exit receipt. All exits were zero: document health/privacy, style, paths, contents, anchors, generated traceability, added-line punctuation, mailbox generation/cross-check, and mailbox generator controls. Traceability passed 5/5 controls without drift. Mailbox controls passed their positive case, eight output defects and seven invalid-contract arms. Those controls establish generation consistency, not execution of the future filter.

[R508] PASS Docs - `receipts/scope.log`; `receipts/pr-approval.json`; `docs/design/MAILBOX_SPLIT.md:149`; `receipts/docs.log`, `receipts/paths.log`, `receipts/toc.log`, `receipts/traceability.log` - Scope, approval text and current-versus-required behavior agree.

The new requirement row and trace-summary entry point to the single-source contract. F0 is explicitly identified as the current implementation awaiting the new rules. Prior timing, placement and VERSION text is preserved. The approval section contains only round-3 filter changes and all 19 source comparisons pass. No additional documentation conflict was found in the assigned delta.

**Prior public findings**

The prior discussion reports were opened only after the independent verdict. No submitted reviews or inline review comments were present. See `receipts/prior-findings-inventory.json` and `receipts/prior-preservation.log`.

| ID | Severity and all attributable lenses | Artifact and disposition at this head |
|---|---|---|
| R508-1-F1 = R509-1-F1 | MINOR; Conformance, Docs | RESOLVED, retained from R508-2/R509-2. `docs/reference/FR_NFR.md:368` and `:369` retain B.3.2/Table B.7 for conflict/loss/retry and B.3.3/Table B.8 for constants. Both corrected rows are byte-identical to approval. |
| R509-1-F2 | MINOR; Conformance, Robustness, Tests, Docs | RESOLVED, retained from R508-2/R509-2. `docs/reference/FR_NFR.md:361`, `:404`, `:430`; `docs/design/MAILBOX_SPLIT.md:356` retain received AVAILABLE/DEPARTING and original aging-deadline starts, every matching sink, state/connection and subsequent TX completion, one allowance, and the full listener checks. Corrected text is unchanged. |
| R508-1-R1 = R509-1-R1 | RESIDUE; Docs | RESOLVED. PR reproduction names the exact current candidate and checkout command. The no-push statement is attributed to the executor; its local phase is described historically. No claim that the branch is unpublished remains. |
| R509-2-R1 | RESIDUE; Docs | RETAINED. `sw/firmware/ctrl_nvm/README.md:464` still calls F0's switch unmerged. This file is unchanged from approval and outside ingress-only edits. Exact fix below. |

The technical findings' required outcomes remain met: correct MAAP transition authority, and explicit listener-discovery timing independent of advertiser checks. Their prior impacts were misleading normative authority and missing per-path timing checks. Verification here proves the corrected rows, listener check block and matching mailbox design survived this delta; unaffected clause conclusions remain covered by the clearing reviews. Public originals and dispositions: [R508-1](https://github.com/kebag-logic/milan-fpga/pull/674#issuecomment-6010426351), [R509-1](https://github.com/kebag-logic/milan-fpga/pull/674#issuecomment-6010388957), [R508-2](https://github.com/kebag-logic/milan-fpga/pull/674#issuecomment-6010971658), [R509-2](https://github.com/kebag-logic/milan-fpga/pull/674#issuecomment-6011008257).

R509-2-R1 authority/evidence: the same page describes the merged HAL at line 124; `docs/design/MAILBOX_SPLIT.md:3` identifies the implemented, default-off foundation. Impact is obsolete publication wording only; the absent integrated store image remains a real limitation. Required outcome/exact fix: replace the two-line bullet at line 464 with `- The #665 switch and its link: no image links this store yet.` Verification: compare the corrected bullet with the merged-HAL statement while preserving that limitation. This changes no measurement, figure, verdict, test, code, generated artifact, conformance/clause claim or privacy rule. It leaves Docs CLEAN under the owner's RESIDUE rule and remains on the manager's checklist.

**Reviewer-owned completion ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | REQUIREMENTS.md:41,67,84; FR_NFR.md:322,328,599; owner decision 6014311316; primary clause checks | R508-3 | 4dab80ae4564ef8d6e1030564dcea4ba19235ee6 |
| RTL | CLEAN | MAILBOX_SPLIT.md:149; mailbox.yaml:377; KL_mbx_rx.sv:115,148,212; MAILBOX_CONTRACT.md:299; scope.log | R508-3 | 4dab80ae4564ef8d6e1030564dcea4ba19235ee6 |
| Robustness | CLEAN | FR_NFR.md:403,406,410,412,447; REQUIREMENTS.md:76; suite.hpp:313,353,405; preserved H-DISC checks | R508-3 | 4dab80ae4564ef8d6e1030564dcea4ba19235ee6 |
| Tests | CLEAN | FR_NFR.md:328,395,412; tb/verilator/mbx/frames.hpp and suite.hpp; focused-results.json; mailbox-controls.log | R508-3 | 4dab80ae4564ef8d6e1030564dcea4ba19235ee6 |
| Docs | CLEAN; retained RESIDUE nonblocking | Three-file authored diff; 19 approval rows; scope.log; prior-preservation.log; documentation/traceability receipts | R508-3 | 4dab80ae4564ef8d6e1030564dcea4ba19235ee6 |

The ledger covers the assigned #664 delta and preservation of earlier approved conclusions. It does not re-review the separately merged #658 implementation or discharge future integration, hardware timing or merge acceptance.

**Limits and pending manager duties**

The fixed [first-round evidence packet](https://github.com/kebag-logic/milan-fpga/tree/b8faae80174f23ea928a49d0611a21884711c475/review-evidence/664-r1) describes `a2780837`. Its handoff digest matches its manifest; it contains summaries/digests rather than complete raw bank logs. Current-head [review-ready evidence](https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6014810929) and the PR body report 93 zero command exits. The assignment reports successful manager source/static, builder and native banks. These are source-validation evidence, not reviewer execution or final current-dev candidate acceptance. Vendor analysis is SKIPPED and historical placement calibration is NOT RUN. Field skips and compiler-absence controls supply no hardware proof.

`receipts/hosted-observation.json` records one exact-head observation: several digital jobs had succeeded, others remained in progress, and the physical job was skipped. No eventual success is inferred. Hosted/local-replica acceptance remains the manager's duty. Live dev was observed at `30e3c018` and must be rechecked at the merge turn.

`receipts/integrity-final.log` hashes raw tracked blobs and checks executable/symlink modes, complete stage-zero index entries, submodule registration and pins. The candidate and required submodules match: protocol processor `ead8036035affd53ef4b29979190f2f4f67084c0`, timing processor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, stream library `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. The final worktree status is clean. No tracked bytes required restoration.

The manager must:

- Verify added rows against the owner decision and switch linkage to `Closes #664` when authorized. Prior text and the 10 ms budget already have owner approval.
- Obtain the other independent exact-head verdict, accept the reviewer-owned ledger, and ensure no review remains in flight. Carry R509-2-R1 on the residue checklist.
- Accept source evidence with its limits, finish hosted/local-replica acceptance, and validate the final candidate against live dev at merge time, recording its identities.
- Obtain explicit maintainer merge authorization, then perform containment and review-integrity checks with their stated proof limits. Close/move the issue only when the full bar is met.
- Retain filter implementation and planted runtime tests, F2-F5 target measurements, stream/counter bench acceptance, audio soak and the VERSION-3 flip as later obligations.

No prohibited banks, runtime builds, host CI orchestration, containers, privilege, hardware, source edits, commits, pushes, public writes, author contact or delegated work occurred. Portable reproduction is in `REPRODUCE.md`. `MANIFEST.sha256` is the publication allowlist. Disposable environments, licensed extracts and unlisted source snapshots remain under unpublished `scratch/`.

R508-3 FINISHED
