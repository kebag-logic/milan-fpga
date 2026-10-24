[R690] NEGATIVE - exact head 1b47a3dcff0cb65cb5cebe1f86327429a76f775d

External independent review, R690-2, issue #773 / PR #779.
Reviewed tree: f608aefd73bbc007624782653182d0a6f85c8825.
Source base: a032c6d6e3775f145349d5a495c1e1ad12294936.
Previous reviewed head: 13d8f1e84920aac1dc3e76fb6406c44a744d8145.

The prior bound and full-sweep findings are resolved. One MINOR documentation finding remains at the assigned head: the stated measurement distribution disagrees with the published log. The corrected upper bounds themselves are valid. Conformance, RTL, Robustness and Tests are CLEAN; Docs is UNCLEAN. No functional RTL defect was established by this delta review.

Scope was reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue body and public scope decisions, the cited requirements and interface documents, the base-to-head diff and history, then executable evidence. Authorities include IEEE 1722-2016 4.3.3 Equation (1), 4.3.5 and 10.7 Equation (14); Milan v1.2 4.4.2.1 and 5.3.7.6; REQUIREMENTS.md; docs/overview/ARCHITECTURE.md; docs/integration/INTEGRATION_GUIDE.md; and [ruling (b)](https://github.com/kebag-logic/milan-fpga/issues/773#issuecomment-6380110812). The standards were read directly; their identities are recorded in authority-check.json. The [round-2 assignment](https://github.com/kebag-logic/milan-fpga/pull/779#issuecomment-6383506324) governs this delta.

Only two documentation pages and the domain-event header changed after 13d8f1e8. The independent verdict and ledger were written before reading other reviewer report bodies. Prior findings were reconciled afterward. A manager correction comment was visible during public-state reconstruction; its assertions were independently checked against the assigned source and receipts, not adopted as proof. No private author material was used.

**R690-2-F1 | MINOR | Docs | incorrect claim that every run attains the bound**

- Artifact: docs/design/MEDIA_CLOCK_FOLLOWING.md:1885-1886; published author-r2/PR-BODY.md, Round 2; issue #773 REVIEW READY, comment 6384707314. Evidence: public/author-r2/receipts/round2/sweep/excerpts/capture_coherence.txt and bounds.log.
- Authority/evidence: AGENTS.md section 6 requires accurate documentary evidence. Of the 23 runs at 2 ms, 9 report a maximum of 2,059,807 ns and 14 report 2,059,787 ns. The page says the leg measures the former maximum in every 2 ms run. The latter maximum corresponds to one additional 20 ns clock cycle. Independent check_bounds.py reproduces the distribution and returns 1 specifically for this false sentence, after passing the numerical bounds.
- Impact: a cold reviewer cannot reconcile the reported measurement with its source log. The conservative maximum and buffer margin remain valid; this is not an overflow or timing-conformance defect. It changes a measurement claim and therefore is MINOR, not RESIDUE.
- Required outcome: replace the universal measurement statement with: "The largest 2 ms [HOLD] maximum is 2,059,807 ns, reached in 9 of 23 runs; the other 14 reach 2,059,787 ns." Correct the corresponding PR and REVIEW READY restatements.
- Verification: parse all 23 observations, retain an upper bound at least as large as every observation, and recheck the changed documentation gates. This is the same defect as R689-2-F1, retained at the assigned head.
- Public-state qualification: the current PR body and [manager correction](https://github.com/kebag-logic/milan-fpga/pull/779#issuecomment-6384888081) now state the distribution correctly and announce a source correction at e658682ed451ba46885225e5b3fc16841f61a5ca. That later source head is outside this assignment. It does not change the bytes or verdict at 1b47a3dc.

**R690-2-R1 | RESIDUE | Docs | stale reviewer placeholders**

- Artifact: published author-r2/PR-BODY.md and current PR body, Linked Issue / roles.
- Authority/evidence: public review-start comments identify both reviewers, but the body still says each is "to be assigned" using [R<n>].
- Impact: stale role wording; public assignment is already established and no measurement or verdict changes.
- Exact required fix: "Internal cleared-context reviewer: [R689]" and "External reviewer: [R690]".
- Verification: compare the two role lines with the public starts. This retains R689-2-RES1 and does not affect coverage. No new prohibited provenance labels were found in the added source comment.

**Optional findings retained together**

| ID / severity / all lenses | Artifact and authority/evidence | Impact | Required outcome if taken | Verification |
|---|---|---|---|---|
| R689-2-S1 / SUGGESTION / Conformance, Docs | MEDIA_CLOCK_FOLLOWING.md:1858; IEEE 1722-2016 4.3.3 defines TT at ownership transfer | "2,714 ns late" leaves its reference implicit | Say "2,714 ns after timestamp minus applied offset" and distinguish subsequent egress from TT | Compare the text with the derived MAC arithmetic and reference plane; manager reports this correction at the later, unreviewed head |
| R689-2-S2 / SUGGESTION / Tests | author-r2/receipts/round2/sweep/shard-0/clone_identity.txt:3 reports two tracked changes; run_all_suites.sh:86-90 documents generated result rewrites | A count alone cannot identify the changed files or independently prove pre-run cleanliness | Record pre-run status and post-run changed paths/diff | Confirm only the two expected timestamped TEST_RESULTS outputs changed; this remains a provenance limit, not an established source defect |
| R689-1-S1 / SUGGESTION / RTL, Robustness | KL_aaf_packetizer.sv:243-265; KL_crf_tx.sv:302-317; milan_datapath.sv:1482-1506; ruled spare covers arbitration at the evaluated product clock | Unusual configurations lack an executable check of the documented spare assumption | Optionally guard sufficient spare at the product clock or state the configuration condition | Exercise accepted product shapes and a shape whose spare is too small; not required for this delta |
| R689-1-S3, also R689-2-S3 / SUGGESTION / Tests | capture_coherence/sim_dp.cpp:548-643 and published [WIRE] minima; contention cover remains derived | No measured worst-age contended case anchors that derivation | Optionally add a targeted maximum-frame/other-output contention scenario | Require its measured hand-over to stay inside the window and a targeted defect to fail it |

**Independent arithmetic and reference-plane assessment**

check_bounds.py extends the earlier rational-arithmetic method. It derives the marker, age, walk, pipeline, whole-period lead, both arrival bounds, queue margins, supported ranges and MAC figures, then compares the documentation and every published [HOLD] maximum.

| Quantity | 1x1 TDM8 | 8x8 TDM32 |
|---|---:|---:|
| Grid-live earliest hand-over, rounded ns | 127,991 | 112,275 |
| Grid-live maximum lead at 2 ms | 2,038,676 ns | 2,054,392 ns |
| Startup earliest hand-over | 106,860 ns | 106,860 ns |
| Startup maximum lead at 2 ms | 2,059,807 ns | 2,059,807 ns |
| Startup last-event lead | 2,163,974 ns | 2,163,974 ns |
| Queue ceiling | 2,656,119 ns | 2,650,942 ns |
| Startup margin | 492,145 ns = 492.1 us | 486,968 ns = 487.0 us |
| Grid-live margin | 513,276 ns | 492,383 ns |
| Default-offset transit ceiling | 2,135,548 ns | 2,140,725 ns |
| First-event offset ceiling, plus transit | 2,489,452 ns | 2,484,275 ns |
| Whole-PDU offset ceiling, plus transit | 2,385,285 ns | 2,380,108 ns |

The startup minimum is (5,208 + 78 + 57) cycles at 20 ns. Its 125 us-offset maximum is 184,807 ns. All 31 observations at both offsets remain below their corresponding bound. Milan's 2.126 ms limit and the 2 ms default fit. The strictly derived Equation (1) lead ceiling is 231,860 ns; the documented 231.8 us is conservative. The actual lead is 166,667 ns. The supported-range paragraph now includes that lead and the additional five sample periods for a whole PDU.

At 1 Gb/s, one maximum tagged frame occupies (1,522 + 8 + 12) octets times 8 ns = 12,336 ns. Subtracting it leaves 5,480 / 6,576 ns for AAF and 8,167 / 2,990 ns for CRF. For the stated store-and-forward sequence, the additional egress times are 16,208 ns for AAF and 18,040 ns for CRF. Remaining margins are 1,608 / 2,704 ns AAF, 2,463 ns 1x1 CRF and -2,714 ns 8x8 CRF. These figures recompute correctly.

The 8x8 CRF corner is **not an established Equation (1) Conformance finding**. TT is transfer of ownership to the network interface, not completion of physical egress. The assessed ordering places the added serialization after ownership transfer. The MAC boundary and store-and-forward integration were checked at sw/litex/milan_soc.py:1748-1807 and docs/integration/INTEGRATION_GUIDE.md:74. Post-transfer delay consumes the network transit budget; it does not retroactively make TT late. Conversely, arbitrary backpressure that prevents ownership transfer is not exempt from Equation (1). This review proves neither unrestricted backlog nor physical launch timing. The 8x8 shape is not the shipping shape, and its true-clock evidence remains derived-only as expressly allowed by the ruling. More than one maximum frame, the MAC crossing/pipeline and 100 Mb/s remain outside the stated derivation.

**Evidence and execution**

The [published packet](https://github.com/kebag-logic/milan-fpga/tree/1faf10a1331f93451a6aa4e43956a51de6ab4da3/review-evidence/773-r1) supplied the source-head execution evidence. verify_evidence.py verifies 46 copied publication hashes and reconciles commands, head, tree, return codes, suite membership and counts. The commit is unsigned (Git signature status N); no signature artifact was supplied. Hash verification is claimed, not cryptographic signer authentication. Declared path-redacted bytes are checked against published hashes.

| Check | Result and scope | Receipt |
|---|---|---|
| Complete four-shard sweep | Author execution at 1b47a3dc / f608aefd: shard counts 15,16,17,16; all rc 0; union equals current --list, 64/64 unique; 2,190,887 checks, zero reported failures | evidence-audit.log; public/author-r2/receipts/round2/sweep/ |
| Focused suite evidence | capture_coherence 20,832/0; datapath 847/0; mutation arm 42/42; AAF 34,020/0 and startup controls 8/8; milan_dp legs report zero failures | published sweep excerpts |
| Behavior and lint | Author exact-head receipts: 406 scenarios, 1,977 steps pass; lint 89 <= 89, rc 0 | published gates/behave.log, behave.rc, lint.log, lint.rc |
| Documentation | Author records three named gates rc 0 under GNU Make 4.3; aggregate 41 successes, two declared skips, initial base-lookup rc 128 superseded by direct-base em-dash pass | published gates/docs_named.log and docs/ receipts |
| Numeric check | Independent derivations and all bounds pass; measurement sentence fails as F1 | check_bounds.py; bounds.log; bounds.rc = 1 |
| Documentation style spot-check | Independent 23-document check passes | doc-style.log; doc-style.rc = 0 |
| Comment and delta identity | Exact equality after stripping comments; non-comment SHA-256 ed9cf292a2d8796e83ba635c56b0b5fe90de484afa926f5fede1cbab9b148dba | evidence-audit.log; delta-audit.log |
| Raw source/index/gitlinks | 1,442 parent blobs, modes and index verified; all five required initialized submodules likewise verified | tree-before.log; tree-final.log |

The two aggregate docs skips are the prohibited host-side candidate orchestrator and the destructive no-git wrapper; separate no-git receipts exist. Skips are not executed passes. Source-head synthesis, route, front-end and phase campaigns retain their explicitly named earlier heads; no new execution of those banks is claimed. The prior independent RTL/Robustness examination and mutation results carry by unchanged source/test identity. The new full sweep resolves the prior exact-head completion gap. The PR Status table at the assigned head now distinguishes those heads correctly.

**Prior-finding reconciliation**

The public discussion findings were read after the initial verdict and ledger. Submitted PR reviews and inline comments were both empty at the later snapshot.

| Prior finding | Disposition at assigned head | Evidence |
|---|---|---|
| R689-1-F1, MINOR Docs | Resolved at its cause: startup and grid-live bounds separated, margins corrected, eight-period range included | design:1872-1896,2038-2048; matrix:191; bounds.log |
| R690-1-F1, MINOR Conformance/Docs | Resolved under both original lenses; maximum now bounds every observation | same artifacts; startup last-event margin remains positive |
| R690-1-F2, MINOR Conformance/Tests/Docs | Resolved under all original lenses; complete exact-head sweep now executed and status appropriately scoped | all four shard receipts; evidence-audit.log; published PR Status |
| R689-1-R1, RESIDUE | Resolved with exact requested wording and no behavior change | KL_media_domain_event.sv:28-33; comment-strip equality |
| R689-1-S2, SUGGESTION Docs | Taken; MAC arithmetic is correct, including the newly distinguished store-and-forward case | design:1846-1862; bounds.log |
| R689-1-S1 and S3 | Remain optional, not taken | retained optional table above |
| R689-2-F1, MINOR Docs | Retained as R690-2-F1 at 1b47a3dc; later public correction is acknowledged, not substituted for this head | design:1886; raw maximum distribution |
| R689-2-S1/S2/S3 and RES1 | Retained as optional/residue above; no blocking coverage effect | named artifacts above |

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts and result | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling (b); IEEE 1722-2016 4.3.3/10.7; design:1846-1896,2038-2048; matrix:191; bounds.log and exact-head sweep resolve both original findings | R690-2, delta plus re-review of R690-1-F1/F2 | 1b47a3dcff0cb65cb5cebe1f86327429a76f775d |
| RTL | CLEAN | KL_media_domain_event.sv:28-33 stripped equality; packetizer:238-266,779-785; CRF:299-318,540-546; datapath:1459-1531,7438-7446; no executable delta | R690-2 identity check, carrying R690-1 source coverage | 1b47a3dcff0cb65cb5cebe1f86327429a76f775d |
| Robustness | CLEAN | datapath:7212,7230 fallback; domain-event:47-52 liveness; sim_dp.cpp:548-643; startup, drift, both offsets and MAC boundary derivations; unchanged mutation controls | R690-2 delta, carrying R690-1 unchanged behavior coverage | 1b47a3dcff0cb65cb5cebe1f86327429a76f775d |
| Tests | CLEAN | four shard commands/results/identities, 64-suite union; capture_coherence and AAF excerpts; behave/lint/docs receipts; unchanged test blobs | R690-2, re-review of R690-1-F2 | 1b47a3dcff0cb65cb5cebe1f86327429a76f775d |
| Docs | UNCLEAN: R690-2-F1 | design:1885-1886 false measurement sentence; design/matrix bounds otherwise agree; published PR body and current correction distinguished | R690-2, applied but not clean | 1b47a3dcff0cb65cb5cebe1f86327429a76f775d |

**Limits and pending manager duties**

This is a delta review at the assigned immutable head, not approval of the later live PR head. No full parent, processor, synthesis or builder bank was run here. No manager source-head bank exists or is inferred. No source fixes, commits, pushes, GitHub writes, hosting replicas, shared installs or hardware actions were performed. Physical calibration is NOT RUN; field skips and simulation passes are not hardware proof. Hosted execution was not audited in this round; emitted or skipped contexts are not claimed as executed evidence.

The manager owns review of the later correction, both independent positive reviews, hosted/local-replica acceptance, and the final current-dev merge candidate with its builder/native receipts. Source evidence is distinct from that candidate. The assigned source base and stated live dev are a032c6d6e3775f145349d5a495c1e1ad12294936; revalidate against live dev at the merge turn. Complete authorized merge and post-merge containment only after the full bar. The PR uses "Relates to #773"; issue closure and project completion remain explicit manager duties. This report gives no merge authorization.

Portable reproduction: run verify_evidence.py with an initialized clone containing the evidence commit and an output directory; run check_bounds.py with that clone and the copied capture_coherence excerpt. Its rc 1 is expected at this head for F1. Run audit_tree.py on the unchanged assigned clone. Disposable extractions stay under scratch/. Only REPORT.md and the files listed in MANIFEST.sha256 are publishable. The final raw-byte/mode/index/gitlink audit passed.

R690-2 FINISHED
