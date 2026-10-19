[R662] POSITIVE - exact head 2022d363fc622f6bbf4c312239fc3db741b4d29a

All five lenses are CLEAN. No BLOCKER, MAJOR or MINOR remains open. R662-2-F01 is resolved by the corrected coverage description and regenerated index; R662-2-R01 is resolved in the live PR body. One previously recorded wording residue and five optional suggestions remain below. No new defect was found.

Tree: `249bdbe6209bbc7ec17a816c26823ad97bb6d748`. Base: `43acfbcc098f5af1be20a4a5458770ead3717622`, including #82. Earlier functional head: `53ac2e9d75ceb381c2d2b04854e760304d9ae43f`. Source head is unchanged since round 2. [Public review start](https://github.com/Mister-M-alt/FPGA-gPTP/pull/86#issuecomment-6264316975). [Pinned public evidence](https://github.com/kebag-logic/milan-fpga/tree/83fee78c28ee0920be865097424d68b4f45f59c5/review-evidence/gptp84-r1).

**Scope, independence and authority**

The supplied AGENTS instruction and referenced command policy were read first. No repository AGENTS.md, CONTRIBUTING.md, or applicable ancestor AGENTS.md was found. The documentation map, root README and current guides established the source/test/guide truth order. The issue bodies, exact [assignment](https://github.com/Mister-M-alt/FPGA-gPTP/issues/84#issuecomment-6257168490), exact newest [STOP ruling](https://github.com/Mister-M-alt/FPGA-gPTP/issues/84#issuecomment-6259159680), #82 publication acceptance, and [parent-companion ruling](https://github.com/Mister-M-alt/FPGA-gPTP/pull/86#issuecomment-6264025745) constrain this review.

The assignment requires synchronized mastership without removing GM-change holdover; received pathSequence plus thisClock; coherent #82 transitions; simulation and planted defects; parent consumer acceptance; and no parent-visible port or parameter change. The STOP ruling permits the four shadow expectation updates. The later ruling also accepts the #82 adoption debt and the #84 physical-rate harness changes, including the redundant surviving first-GM mutant.

Conformance uses the frozen public requirements: IEEE 1722-2016 4.4.4.7 and 10.4; Milan v1.2 4.3.5.2 and Annex B.1.1; IEEE 802.1AS-2020 10.3.9.23 and 10.3.13.2.4 f) 5); and IEEE 1722.1-2021 7.4.41 / Milan v1.2 5.4.2.24 for GET_AS_PATH. Parent REQ-PTP-07/08, the integration contract, publication wrapper and clock-validity source were inspected at `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`. This is not a separate full-text standards audit or certification.

The independent source/evidence pass and its verdict and ledger were written to `INDEPENDENT-PASS.md` before reading prior reviewer report bodies. Public findings were then reconciled at their causes. No private author material, management source bank, lane scratchpad or other checkout was used. The earlier public findings remain historical records; current acceptance uses the corrected `author-r3` packet.

**Delta and five-lens assessment**

`source.diff` records the full base-to-head change. `later-source.diff` shows that the three commits after `53ac2e9d` change comments/guides only. Executable generator syntax, RTL and all four committed images remain unchanged. The test-harness delta is confined to its header comment. Within the published evidence, every `author-r3` blob was compared with `author-r2`: only `PR-BODY.md`, `receipts/INDEX.md`, and `receipts/round2/search/path-shape-search.md` differ (`evidence-delta.log`). Unchanged functional areas retain their prior clean coverage; this round independently checked the changed claims and their dependencies.

Conformance: `gen_gptp_ucode.py:1734` sets master and sync-ok together after retiring slave correction. The receipt-timeout leg at `:1997` preserves that verdict for a master while clearing it for a slave. Handover to a peer still clears it. Parent `KL_gptp_shadow.sv:676` warns on a committed GM change or sync loss; `KL_ptp_clock_validity.sv:188,211` combines live discontinuity, retained holdover and synchronization. Raising sync-ok therefore does not bypass the Annex B.1.1 hold. A first mastership with thisClock already published arms no new identity-change hold; a prior hold can still be active.

For #85, `KL_gptp_engine.sv:722,977` appends the configured ROM thisClock to nonempty received paths of lengths 1–7. The original received tails remain ordered, count increases by one, and inactive tails clear. Empty remains empty. Eight or more received entries retain the first eight under the existing ABI; thisClock cannot fit there. The frozen Announce context is staged only on BTCA take, and GM/path become consumable together at commit. The #82 reset, peer victory, departure, capability-loss and reacquisition cases retain coherence. Module declaration, ports and parameters match the base after comment removal.

RTL: the four-bit count cannot exceed eight. Tail slot `pk` copies when `pk+2 <= n`, receives thisClock when `pk+1 == n`, otherwise clears. No additional state or transaction boundary is introduced. SRTO computes `flags & ((flags << 2) | 7)` over the established low-four-bit flag domain. The bit-layout assertion binds master bit 1 to sync bit 3. BECOME retires the slew before publishing flags, preserving the existing qualification hook. Four independent regenerations match committed bytes and report 1,015/1,024 words, nine free.

Robustness: examined literal direct/multi-hop expectations, absent/seven/eight/deep-path boundaries, stale-tail clearing, losing Announce ownership, warm-reset transitions, the serializer-stalled takeover and queued timeout, and whole-run cycle/commit monitors (`sim_main.cpp:2427,3773,5193,5224`). Named mutation receipts cover omission, wrong identity, wrong slot, stale tails, count boundaries, master verdict, timeout and peer handover. The optional unexercised master-side excessive-delay path is retained as S4 below.

Tests: the accepted physical-rate companion now requires the peer GM before declaring recovery healthy. It checks uncertainty before takeover, separately observes holdover bounds, and checks certainty after takeover and thisClock after loss. The hold interval deliberately omits a stable-tu packet comparison; its elapsed-time bounds remain checked. Published bounds are 0.25 s minus the 4 ms polling allowance through 0.5 s plus that allowance. Extended mode's omitted comparison remains explicit, as S3 below. The accepted redundant `&& gm_r != 0` mutant is recorded as a survivor, not recast as caught.

Docs: the corrected ROM budget, mastership/holdover explanation, SlavePort publication clause note and source anchors agree with source. New source comments contain no prohibited lane labels, review identifiers or comment IDs; bridge constants are not lane labels. The revised coverage note now defers to per-snapshot inventory and expressly excludes skipped field campaigns. The live PR says the parent adoption decisions were accepted. The retained unqualified timeout bullet is wording residue R1 below.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #82/#84/#85 scope and rulings; parent REQ-PTP-07/08, wrapper and validity; mastership/timeout and path staging; four companions | R662-1/2 baseline; independently checked R662-3 | 2022d363fc622f6bbf4c312239fc3db741b4d29a |
| RTL | CLEAN | Full source diff; engine count/append/commit logic; generator flags and slew ordering; module declaration; four image recipes | R662-1/2 baseline; R662-3 equivalence/regeneration | 2022d363fc622f6bbf4c312239fc3db741b4d29a |
| Robustness | CLEAN | Frozen Announce and #82 transitions; boundary paths; queued timeout; named negative controls; accepted parent holdover logic | R662-1/2 baseline; R662-3 artifact checks | 2022d363fc622f6bbf4c312239fc3db741b4d29a |
| Tests | CLEAN | Exact-head source receipts; parent snapshot 564466ea; mutation audit; current coverage note, inventory and indexes; patch applicability | R662-3, retaining unchanged execution coverage from R662-1/2 | 2022d363fc622f6bbf4c312239fc3db741b4d29a |
| Docs | CLEAN | Current guides and source comments; PR; author-r3 method/index; prior mandatory corrections; retained R1 residue | R662-3 | 2022d363fc622f6bbf4c312239fc3db741b4d29a |

**Prior findings resolved or retained**

| ID | Severity / all attributable lenses | Required outcome and disposition at this head | Cause-specific verification |
|---|---|---|---|
| R662-2-F01 | MINOR / Tests, Docs | RESOLVED: remove the overstatement that every enabled suite ran unpatched, which inflated execution coverage | Current `author-r3/receipts/round2/search/path-shape-search.md:16` uses the requested replacement. Inventory distinguishes adoption-only GM steps, snapshot 6814d01c plane/tables/timestamps, and skipped field campaigns. Raw logs agree; regenerated index/hash checks pass. |
| R662-2-R01 | RESIDUE / Docs | RESOLVED: remove obsolete pending-approval wording | Live PR body line 119 and author-r3 PR body say “Parent adoption decisions accepted by the manager,” matching the ruling. Historical handoff wording need not be rewritten. |
| R662-1-F01; R661-1-F2 | MINOR / Docs | RESOLVED: correct overstated available ROM capacity | `docs/MANAGER.md:103,107` states 1,015 words, 99.1%, nine free; all four independent regenerations agree. Generator `:1859` no longer states 88 percent. |
| R661-1-F1 | MAJOR / Tests, Docs | RESOLVED: cover the parent path expectations that otherwise break pin adoption | Four patches apply in order. The eight named milan_dp rows, loop-exit count, new tails and physical-rate rows are covered; adoption receipts show 185/185 for both legs, shadow 310/310, physical-rate 155/155 and 11/11 consumer rc 0. |
| R661-1-F3 | MINOR / Docs | RESOLVED: qualify the incorrect universal mastership holdover claim | Generator `:1737`, suite phase-37 header and PR distinguish replacement of a peer from an already-published thisClock. Parent identity/discontinuity logic agrees. |
| R661-1-F4 | MINOR / Docs | RESOLVED: correct the obsolete no-reader clause claim | Generator `:72` identifies the SlavePort copy as published GET_AS_PATH state; only Announce transmission lacks a slave-side reader. |
| R661-1-R1 | RESIDUE / Docs | RESOLVED: put phase descriptions in call order | Suite header lists 37 before 38. |
| R661-2-R1 | RESIDUE / Docs | RETAINED below | No source delta changes the timeout bullet. |
| R661-2-S1/S2/S3/S4/S5; R661-1-S1 | SUGGESTION / lenses below | RETAINED below; R661-1-S1 is the same item as R661-2-S4 | No executable or guide delta addresses these optional items. |

No submitted review or inline-review finding was omitted: those public endpoints returned zero records; the prior FINDINGS are issue-comment reports.

**Retained residue and suggestions**

- **R661-2-R1 — RESIDUE — Docs.** Artifact: `docs/INTEGRATION.md:299`. The list says a 375 ms receipt timeout clears synchronization without the mastership qualification, although `:546` and `prog_leg_srto` state the correct rule. Impact is a local prose ambiguity; the behavioral contract is already explicit in the same guide. Exact fix: `- A 375 ms Sync receipt timeout outside mastership.` Verification: reread both sections and run the documentation check. Retained under the owner's wording-only rule; no lens becomes unclean.
- **R661-2-S1 — SUGGESTION — Conformance, Docs.** Artifact: `docs/INTEGRATION.md:536`, generator BECOME and the priority1-255 test pass. A non-grandmaster-capable master has gmPresent clear while publishing sync-ok. The issue scope and 802.1AS 10.3.13.2.4 g) leave a policy clarification useful, but no supplied authority establishes a defect. Suggested outcome: owner confirms the intended tu policy and documents this case. Verification: align that statement with the priority1-255 flags and parent tu equation.
- **R661-2-S2 — SUGGESTION — Conformance, Docs.** Artifact: `docs/INTEGRATION.md:482`, parent GET_AS_PATH documentation. The existing eight-entry ABI omits thisClock for received paths already filling the window. Impact: parent consumers may mistake the disclosed truncation for a regression. Suggested outcome: carry the bound into the parent-facing GET_AS_PATH limitations. Verification: compare the parent wording with seven/eight/deep-path expectations; widening remains outside this assignment.
- **R661-2-S3 — SUGGESTION — Tests.** Artifact: `parent-adoption-milan_dp_gptp-84.patch`, extended-mode branch. That branch marks the entire 4.6 s loss window as a transition with tu ungraded; default mode grades the split. Suggested outcome: grade at least the pre-GM-change tu-1 portion when next extending the harness. Verification: normal extended execution passes and a pre-change certainty fault fails the added check. No new extended execution is claimed here.
- **R661-2-S4 / R661-1-S1 — SUGGESTION — Tests.** Artifact: generator excessive-Pdelay capability-fall path near `:1976`, engine harness. Earlier public probes recorded a sync-clearing fault surviving on this master-side path, unlike the lost-response and multiple-response cases. The implementation is unchanged and correct; coverage is incomplete across those optional scenarios. Suggested outcome: add a master-side excessive-delay case. Verification: retain master sync-ok in control and fail a targeted sync-clearing mutant. The earlier survivor is retained, not rerun or represented as caught.
- **R661-2-S5 — SUGGESTION — RTL, Docs.** Artifact: dated out-of-context snapshot in `docs/MANAGER.md:33` and new path-tail selection in the engine. The dated measurement predates this mux; it is not advertised as an exact-head measurement. Suggested outcome: record the delta at the next scheduled resource measurement. Verification: compare resources and timing under the same part, constraints and configuration. No new synthesis or timing result is inferred.

**Verification and execution evidence**

This round ran only lightweight checks, regenerations, receipt audits and disposable patch application. Independent lightweight checks and downloads ran concurrently under foreground drivers. No simulation or full bank was rerun: no new functional delta or unresolved falsification target justified it. Thus the scoped simulator was not invoked. Builds and extracted adoption files stayed under `scratch/`.

| Evidence | Result and provenance |
|---|---|
| `audit.log`; `contract.log`, `docs.log`, `diagrams.log` and rc files | Independent checks rc 0; all four images byte-identical, 1,015/1,024 words; executable generator/RTL/ROM equivalence to 53ac2e9d. |
| Published-file integrity | 251 selected files match pinned Git blobs and applicable full published SHA-256 entries. Both indexes exactly cover 414 receipt files; original hash prefixes match publication mapping, and unredacted sizes match. Redacted published bytes are checked against published hashes. |
| `receipt-check.log` | 72 source mutation patterns occur once; all 72 caught receipts and 24 positive slice controls verified; 148 required named failures in the #82/#84/#85/priority1-255 groups matched. Other unchanged mutation details retain earlier coverage. |
| Author exact-head source receipts | `author-r2/receipts/round2/lane-head-2022d363`: required gate rc 0; engine 1,703/1,703 in three passes and 53/53 with priority1 255. Public author-r3 copies are byte-identical. |
| Author exact-head parent adoption | Snapshot `564466ea0a06720b8209c45e13303907beaf0569`: 11/11 consumer rc 0; shadow 310/310; gptp/gptp-lat 185/185 each; physical-rate harness 155/155 with verifier counts 6/6, 20/20, 14/14, 14/14; GM steps 190/190 and 6/6 controls. |
| Parent mutation and additional suite evidence | Negative controls at recorded earlier snapshot 3f053cc1; plane/tables/timestamps at 6814d01c. These are not relabeled exact-head executions. The executable delta is unchanged; final adoption executions are recorded separately. |
| Parent companions and dependencies | Four patches apply cleanly to the three public parent test files in specified order. Six recorded adoption gitlinks match public dev dependency pins with donor advanced to this head. No parent checkout was edited. |
| Exact-head hosted queries | Zero workflow runs, zero check runs, zero status contexts. No hosted success or skipped context is inferred from an empty response. |

The source and evidence publication commits report **unsigned**. No verifiable cryptographic signature was supplied. This review verifies pinned content and checksums; it does not claim signature verification.

Builder union reports 103 gates once with digest `8800c441e33bfdedbc0a2b41321ebc75251b43c1a36b0e11362b5df8d0367e84`, but gate 11 calibration is NOT RUN. The HDL-analysis receipt reports zero modules analyzed, so its rc 0 is not credited as executed HDL analysis. Both field campaigns were SUITE-SKIP; their selftests and traceability checks do not exercise the engine. The physical-rate suite is simulation, not physical calibration or hardware proof.

**Integrity, limits and manager duties**

All 107 tracked source blob bytes, executable modes, and index entries match the exact head and tree. There are no nested donor submodule gitlinks. Parent dependency verification is a comparison of published pins/receipts, not execution of a parent bank. No source fixes, commits, pushes, GitHub writes, merges, author contact, hardware work or prohibited full campaigns occurred.

There is **no manager source bank at this head**. Source validation above is the author's published evidence, plus this review's limited checks. Final current-dev validation remains distinct: the manager builds the merge candidate at the merge turn using source base `43acfbcc` and stated live parent dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`, executes builder and native banks, owns hosted/local acceptance, and links its receipts on the PR. Required independent positive reviews and the full completion bar still govern merging.

The manager must carry all four companions with the fourth pin adoption in order: shadow-85, milan_dp-85, milan_dp-82, then milan_dp_gptp-84. Preserve the suite-inventory distinctions when widening consumer coverage. Carry R661-2-R1 on the residue checklist and retain the five suggestions as optional follow-up. Physical calibration and field acceptance remain pending.

Portable checks: `fetch_public.py` refetches selected immutable evidence; `audit.py SOURCE_ROOT` checks source/evidence and runs lightweight verification; `check_receipts.py SOURCE_ROOT` checks mutation receipts, reconstructs companion application and checks parent pins. `MANIFEST.sha256` names every publishable receipt relative to this packet; `scratch/` is excluded. `INDEPENDENT-PASS.md` records the independence checkpoint; this report is the final verdict.

R662-3 FINISHED
