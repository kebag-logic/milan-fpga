[R870] NEGATIVE - exact head f09d82e05270bdd77e07f7fc2e14d064c1123be8

Round R870-2, external independent delta review of PR #952 for #951/#665.
Tree: `13ff87928a0c2b9448475c2725c4f18fbc76f1dc`.
Delta: `0d1eb8e4c5821e9431097950882659f2083d96ba..f09d82e05270bdd77e07f7fc2e14d064c1123be8`.
Original comparison base: `0839453f6d7135063e904bcaf4ac1852ad6b522a`.

All five lenses were applied. The requested documentation/comment corrections pass. There is no new source defect or new wording residue. **R870-1-F2 remains partially open, MINOR under Tests, solely because its required complete final-image timing evidence is still pending.** No source fix or duplicate source-head measurement bank is requested.

The independent delta verdict and ledger were written before reading prior review findings. That pass found the corrections sound. Reconciliation with the published R870-1 finding then retained its explicit condition that the timing-evidence portion of Tests stays unclean until the complete final bank is checked. A pending measurement is not a wording-only residue. The final verdict above supersedes the preliminary delta-only assessment.

Scope was reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, [#951 and its public acceptance/evidence comments](https://github.com/kebag-logic/milan-fpga/issues/951), [#665's ruling, item 2](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-7007273447), #895's acceptance, REQUIREMENTS.md, FR_NFR.md 3.4.1 and the mailbox/SRP contracts. The two one-line commits are `e7b0272b` and `f09d82e0`. Eight files change after round 1. The full original ten-file diff and history were inspected for context; unaffected executable behavior keeps its prior review coverage.

**Prior findings: explicit dispositions**

- **R870-1-F1, MINOR, Conformance/Docs: RESOLVED.** Artifacts: `sw/firmware/ctrl/srp/srp_mbx.c:35-44`, `sw/firmware/ctrl/srp/README.md:223-246`, `docs/design/MAILBOX_SPLIT.md:1290-1293`, `docs/design/SPLIT_CONTROL_MEMORY.md:2855,3003,3171-3175`. The nominal maximum is attributed to IEEE 802.1Q-2018 10.7.4.3; Milan Table 4.3's additional tolerance up to 15.5 s is explicitly excluded. Source and durable explanations state that two upper-edge intervals can reach 31 s. This removes the overstated clause/coverage claim. The approved formula and 3,023/3,027/3,030 cs values remain unchanged. Verification: complete delta inspection and independent comment-only checks; the repository's Table 4.3 reading in `FR_NFR.md:427` agrees. The unchanged normative interpretation from round 1 is carried; external standards were not downloaded again.
- **R870-1-F2, MINOR, Tests/Docs: PARTIALLY RESOLVED; remaining finding below.** Artifacts: PR body's CPU paragraph and limitations; `SPLIT_CONTROL_MEMORY.md:3177-3184`; `tb/verilator/ctrl_service_budget/README.md:261`. The unconditional carry claim is removed. The text names three valid-destinations groups, five arm A groups at 1x1/1if and four at 8x8/1if, and explicitly excludes omitted groups, answering arms and 8x8/2if from the evidence. Complete validation is marked PENDING. The Docs component is resolved; the remaining evidence obligation belongs to Tests.
- **R870-1-F3, MINOR, Docs: RESOLVED.** Artifacts: `SPLIT_CONTROL_MEMORY.md:3176`, PR image paragraph and all twenty original `author-r1/receipts/images/pairs/*.imgdiff.txt` files. Following code moves four bytes; .rodata moves zero or eight by alignment, zero in thirteen pairs including every platform pair; SRAM remains fixed. The independent parser recomputed these counts from the original section-address pairs, rather than trusting the round-2 summary. The inaccurate measurement figure is corrected.
- **R870-1-RS1, RESIDUE, Docs: RESOLVED.** PR Linked Issue / roles now names R869 as internal and R870 as external, matching the public assignments. No placeholder remains. This is the requested administrative fix.
- **R869-1-RES-1, RESIDUE, Docs: RESOLVED.** `SPLIT_CONTROL_MEMORY.md:2857` retains the historical test name with its current #951 name and nominal 30,000 ms horizon beside it. The historical measurements remain historical; the current test is findable at `srp_talker.cpp:340`.
- **R869-1-RES-2, RESIDUE, Docs: RESOLVED.** `tb/verilator/ctrl_service_budget/talker_notice.py:22-23` now says two nominal longest LeaveAll periods, about 30 s. The module AST is identical after removing its docstring, and the harness uses its symbols rather than consuming that docstring.

**Open finding**

**R870-1-F2 (retained remainder) - MINOR - Tests - final-image CPU timing evidence**

Artifact: [R870-1's F2](https://github.com/kebag-logic/milan-fpga/pull/952#issuecomment-7012143102); `docs/design/SPLIT_CONTROL_MEMORY.md:3184`; PR #952 CPU timing limitations; public archive `author-r1/receipts/cpu/legs/` and `cpu/compare/`.

Authority/evidence: NFR-SCOUT-03, FR_NFR.md 3.4.1 and the formal coverage rule in `tb/verilator/ctrl_service_budget/README.md:261`. The prior finding expressly required the complete final-image bank and left timing-evidence coverage unclean until it was checked. Current prose correctly calls the existing 156 paired probes a sample. Their verdicts agree, but placement changes their measured times. No complete final-image bank is published in the inspected issue/PR evidence, and the round-2 acceptance still marks it pending.

Impact: the sample does not establish the timing of omitted paths at the changed layout or at the eventual composed candidate. No regression on an omitted path is alleged. This is an unmet existing verification condition, not a new requirement for another source-head campaign.

Required outcome: at the already-planned merge turn, publish the complete final train/current-dev candidate measurement, with candidate commit/tree, image hashes, required points/arms/groups, statement/load/share checks, and explicit existing-miss dispositions. Where evidence is reused, prove identity of the relevant measured and final image bytes. Retain the current accurate pending wording until then.

Verification: a reviewer checks that published bank's coverage, image identity and regrading and explicitly closes this remainder. Then the Tests ledger can become CLEAN. The manager's future builder/native-bank validation must not be inferred from source receipts.

**Retained optional suggestions**

- **R869-1-SUG-1 - SUGGESTION - Conformance - `srp_mbx.c:35-44`, #665 ruling item 2.** Evidence: the approved nominal hold excludes Milan's additional tolerance. Impact: it does not guarantee aging through two 15.5 s peer intervals, while still satisfying the accepted minimum. Outcome: the maintainer may explicitly retain this policy or authorize separate tolerance-inclusive work. Verification: a public policy disposition; changed timing would require new tests/image evidence. This suggestion remains optional and does not unclean Conformance.
- **R869-1-SUG-2 - SUGGESTION - Docs - #951's conditional reference-device measurement.** Evidence: the issue and PR state that conflict delay was not measured because bench access was unavailable. Impact: closing the issue can obscure this conditional measurement. Outcome: record its transfer to a bench run or the maintainer's decision to decline it before closure. Verification: public disposition or a dated measurement. No hardware result is claimed.

The internal review's additional note about “matches the release” remains a historical wording question for the manager's train record. This delta does not change that ruling. The PR correctly distinguishes the all-fabric path, which changes Stream ID and does not use this hold-off.

**Per-lens evidence**

[R870] PASS Conformance - `srp_mbx.c:32-46,526-527`; SRP README:223-246; MAILBOX_SPLIT.md:1290-1293; SPLIT_CONTROL_MEMORY.md:3171-3175 - checked the nominal/tolerance distinction against the accepted ruling and repository clause authority. Arithmetic, the single LeaveAllTime source, JoinTime/transmit terms and the accepted minimum are unchanged.

[R870] PASS RTL - `delta.diff`, `source.diff`, `audit-delta.log`, `checkout-integrity.log` - no RTL, clock/reset, CDC, mailbox interface, build-driver or submodule change. All changed C/C++ lines are complete comment lines with unchanged line counts and no line-continuation hazard. Prior reviewed counter/loading/countdown behavior and width checks therefore carry. Original image-pair receipts support the four-byte instruction expansion and unchanged SRAM.

[R870] PASS Robustness - `sw/firmware/ctrl/test/srp_talker.cpp:294,340,465`; `srp_gate.hpp:318-345`; round-2 focused receipts; `audit-delta.log` - reset, changed/unchanged destination, latest Leave, refused withdrawal and conflict test behavior remains byte-identical outside comments. Mutation tables are unchanged. Published round-2 tests pass 16/16 at 1x1/1if, 16/16 at 8x8/2if and 9/9 composed tests. Round-1 robustness evidence carries for the approved nominal hold; no new malformed-input or configuration path was introduced.

Tests - `audit_delta.py`, `audit-delta.log`, test/mutation files and published CPU receipts - comment-only equivalence and existing functional tests are adequate for this delta. The separate final-image timing condition in F2 remains unclean; the receipt audit is not a replacement for it.

[R870] PASS Docs - complete eight-file delta; `SPLIT_CONTROL_MEMORY.md:2857,3176,3184`; `talker_notice.py:22-23`; PR roles/limitations; `docs-check.log` - all named corrections are accurate and consistent with published receipts. Added source comments state behavior/reason and issue/clause references, with no new bench lane, review round, reviewer or comment identifiers. No new residue found.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | srp_mbx.c:32-46; SRP README:223-246; MAILBOX_SPLIT.md:1290-1293; SPLIT_CONTROL_MEMORY.md:3171-3175; ruling/FR_NFR.md | R870-2 | f09d82e05270bdd77e07f7fc2e14d064c1123be8 |
| RTL | CLEAN | delta.diff; original source.diff; image pairs; checkout-integrity.log; unchanged counter and interface dependencies | R870-2, preserving unaffected R870-1 coverage | f09d82e05270bdd77e07f7fc2e14d064c1123be8 |
| Robustness | CLEAN | srp_talker.cpp; srp_gate.hpp; unchanged mutations; round-2 focused receipts and comment equivalence | R870-2, preserving unaffected R870-1 coverage | f09d82e05270bdd77e07f7fc2e14d064c1123be8 |
| Tests | UNCLEAN (remaining F2) | audit-delta.log; functional receipts; CPU subset receipts; formal coverage rule and pending final bank | R870-2 applied; no clean covering round for F2 | f09d82e05270bdd77e07f7fc2e14d064c1123be8 |
| Docs | CLEAN | complete delta; corrected clause/measurement/scope statements; PR roles; docs-check.log | R870-2 | f09d82e05270bdd77e07f7fc2e14d064c1123be8 |

**Executed checks and evidence limits**

Reproduce the read-only checks from this exact checkout after fetching archive `af70bbe3ceb299a0c65826df70c8bea492f28e0d`:

```sh
python3 -B "$PACKET/audit_delta.py"
python3 -B scripts/docs_check.py
git diff --check 0d1eb8e4 HEAD
python3 -B "$PACKET/verify_checkout.py" "$CHECKOUT"
```

All exited zero. `audit-delta.log` verifies all 176 published author-file hashes against the archive manifest; checks C/C++ line equivalence and Python AST equivalence; matches all 20 round-2 image hashes to round 1; recomputes all twenty placement pairs; checks the 16/16/9 focused receipts; and counts 104/104 rc-zero selected docs steps at both round-2 heads. The last commit affects only a design page and the harness docstring, so the images measured at `e7b0272b` carry to `f09d82e0`. The image binaries themselves were not republished or rebuilt in this review; this is a verified published-hash/receipt comparison.

The archive commit has **no cryptographic signature**, and no signature file is present in the supplied packet. Manifest/hash integrity was verified; signer authentication was not. The archive's content address is fixed and public. No assertion of a verified signed packet is made.

The independent docs check reports zero findings across 223 Markdown and 1,907 scrubbed text files, with 23/23 scrub controls and 4/4 routing arms. The author's 104 selected docs steps are not every hosted workflow operation: installation/recording steps and the candidate CI-orchestrator self-test are excluded, and builder legs are separate. The carried builder receipts each have one NOT RUN arm, including physical calibration. These exclusions remain visible.

Checkout verification hashes actual tracked file bytes rather than trusting status: 1,938 candidate entries plus the five required submodules match their pinned blobs, modes and complete indexes. Pins: gPTP `1616fc8f062fbf58c35ad31674b5b233207bbdb8`; protocol processor `801ef2283ec793e35a2590fc6593c90313a64041`; lwSRP `08ee86e812a0eb5e1dc6cd61b494d8baf3491348`; TSN stack `715589c1db7cf67e2f3259fd7083ebc7f0923376`; axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. Optional external is uninitialized and unused. No source probe edits required restoration.

The one-time hosted snapshot records successful executed wire-accountability, docs-check-no-git and specification-facing jobs, alongside successful selectors/setup jobs. Other work was running/queued; physical gPTP was skipped. It establishes neither complete hosted acceptance nor exhaustive aggregate success. Setup and skipped work are not test passes. The manager owns hosted and local-replica acceptance.

No new full firmware, parent/processor, synthesis, builder or CPU bank was run; no simulator or compiler was invoked. Existing functional evidence carries because its executable inputs are unchanged. Physical calibration and reference-device conflict delay are NOT RUN; field skips are not hardware proof. No manager source-head bank exists or is inferred.

**Pending manager duties**

Publish and obtain review of F2's complete final-image measurement, preserving its remaining Tests finding until then. Validate the eventual current-dev merge candidate with the required builder/native banks and link receipts; source base `0839453f` and supplied live dev `e275d7950ef3385753e6a15d2e191ba855b171ed` are distinct from that eventual candidate. Obtain complete hosted/local evidence, the independent review completion bar, explicit merge authorization, and post-merge containment before closing/moving the issue to Done. Carry the two optional suggestions to their public dispositions.

No source fix, commit, push, GitHub write, author contact, delegated review, container execution or hardware action occurred. Only the designated review packet contains new files. This report does not authorize merge.

R870-2 FINISHED
