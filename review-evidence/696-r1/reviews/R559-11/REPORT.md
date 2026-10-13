[R559] POSITIVE - exact head e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd

Round R559-11 covers all five lenses at tree `295aadcc963e941f2fcc97b27d497aa787da0d86`. No BLOCKER, MAJOR or MINOR remains open. The wording residues below change no measurement, executable result, verdict, interface, privacy rule or conformance claim. This is a source-head review, not merge authorization or a claim that the task's completion bar is already met.

The independent verdict and ledger were saved in [independent-verdict.txt](independent-verdict.txt) before previous public review reports were read. Previous findings were then reconciled against this head. No private author material or another reviewer's unpublished material was used.

**Scope and authorities**

Reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README.md, [issue #696](https://github.com/kebag-logic/milan-fpga/issues/696) and its public decisions, linked requirements and interfaces, the requested diff and history, then public executable evidence. The M1–M8 acceptance and public amendments govern this review; they do not constitute unrestricted Annex B certification.

| Public issue decision | Effect on scope |
|---|---|
| [6076750392](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6076750392) | M1–M8 assignment, programmed-MAC integration checks, existing operational link input, resource ceiling, post-merge bench assignment |
| [6076940309](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6076940309) | Withdraw M8 accounting; retain silent discard without state, timer or transmission effects |
| [6079087547](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6079087547) | Apply +60 LUT / +60 FF to the MAAP engine; permit documented bounded shared response storage |
| [6079463350](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6079463350), [6080332335](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6080332335) | Authorize 1,024 programmed identities in the differential and relevant documentation updates |
| [6089712293](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6089712293) | Retain the route timing floor |
| [6102832618](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6102832618) | Narrow first-claim separation to nonzero seeds a power of two apart, including carries, for counts 1–8; distinguish offset words from folded/clipped blocks; require universal checks and discriminating plants |
| [6142198285](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6142198285), [6148294623](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6148294623) | Compose assigned changes; preserve shared-stack pin proof and Annex B differential behavior in the final conflict resolution |

Authorities examined include REQUIREMENTS.md; `docs/reference/FR_NFR.md:223` (FR-MAAP-01); the MAAP register-map section; `docs/design/MAAP_FABRIC.md`; `hdl/ieee1722/maap/doc/KL_maap/KL_maap.md`; `docs/design/AREA_BUDGET.md`; and the resource measurement recipe. Clause attribution follows B.2, Table B.7/note d, B.3.4, B.3.5.9, B.3.6.1, B.3.6.4, B.3.6.6 and B.4/Table B.9 as recorded in those authorities. The complete licensed IEEE text was not independently available in this pass; this limits standards verification beyond the recorded clauses and decisions.

The requested `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc..e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd` diff includes imported lanes. I classified those imports, reviewed the 17 issue-owned paths relative to `d40e4e9827be2516f8f34b9d65f0a483fff2194c`, and checked the merge resolution and relevant interfaces. This does not claim a fresh full implementation review of every imported lane. [source-provenance.json](source-provenance.json) records both diff views and the resolution. Ordered parents are `313616d1a18549d41907db389d378f0beb9bc543` and `d40e4e9827be2516f8f34b9d65f0a483fff2194c`. Only `sw/firmware/ctrl/test/maap_differential.py` has manual conflict resolution; its four hunks retain shared-pin verification, stack-built C code and link ordering, optional RTL input and all 17 differential plants.

**Acceptance and implementation**

In this table, KL_maap.sv means `hdl/ieee1722/maap/KL_maap.sv`; sim_main.cpp and sim_integration.cpp are under `tb/verilator/maap/`; milan_datapath.sv is under `hdl/milan/`.

| Item / authority | Examined artifacts and result |
|---|---|
| M1 — Table B.7 note d; B.3.6.4 | `KL_maap.sv:238,313`; `sim_main.cpp:744`. The missing cells apply reversed-octet comparison. Equality and lower/higher identities are distinguished. Extended half-open range arithmetic avoids wrapping a 16-bit end. |
| M2 — B.3.6.6 | `KL_maap.sv:269,319`; `sim_main.cpp:437`. Response snapshots echo requested start and all 16 count bits separately from overlap fields and own claim count. The below-own-offset test rejects overlap-start substitution. Independent probes also exercise wide counts and overlap boundaries. |
| M3 — B.3.6.1 | `KL_maap.sv:141,193`; `sim_main.cpp:943`. Nonzero 32-bit recurrence has the reviewed taps and maximal-order checks. Zero uses the documented fallback. Fold/clip bias remains disclosed. Public measurements meet the assigned ceiling. |
| M4 — B.3.4 NOTE; amended criterion | `KL_maap.sv:154,331`; `milan_datapath.sv:2933,7181`; `sim_main.cpp:1025,1180`; `sim_integration.cpp`. First enable samples programmed MAC and clock, steps the seed before first folds and does not resample on every restart. Real CSR/MAC wiring participates. Learned maps, all carry runs and offset words grade the narrowed criterion. High-half bijection concerns words, not universal disjoint blocks. |
| M5 — B.3.5.9; Table B.7 | `KL_maap.sv:433,462`; `milan_datapath.sv:3000,7181`; `sim_main.cpp:811,836`. Operational return restarts the claim and four-PROBE sequence from PROBE or ANNOUNCE; a long loss is not treated as return. Existing effective-link and clock contracts remain intact. |
| M6 — Table B.7; B.3.6.6; shared-buffer ruling | `KL_maap.sv:269,319,433`; `sim_main.cpp:774`. One response pending behind PROBE/ANNOUNCE survives stalls without changing the active frame. Disable, restart, link return and reset cancel it. Further PROBEs while the one pending/transmitting response is occupied remain explicitly unsupported. |
| M7 — B.4/Table B.9 | `KL_maap.sv:331`; `sim_main.cpp:874`. Supplied start and extended end must fit the dynamic pool. Invalid seeds fall back. Count 1, 8 and 255 boundaries are tested. Optional count-zero/later-draw coverage suggestions remain listed below. |
| M8 — B.2; accounting withdrawal | `KL_maap.sv:219,399`; `sim_main.cpp:895`; [boundary_probe.cpp](boundary_probe.cpp). Completeness covers every required byte on accepted beats, including sparse keeps and saturated beat index. Truncation does not publish a valid PDU. Independent probes add input gaps/backpressure and confirm subsequent complete-frame acceptance. No discard counter is claimed. |

RTL review also covered reset of state and response fields, timer priority, enable/release/restart ordering, transmit snapshots, widths, byte order and feature-disabled integration. Timestamp and effective-link inputs retain the existing clock contract; no new CDC mechanism is introduced. Reconfiguration during a frame is not newly guaranteed.

**Independent execution**

The pinned simulator identified itself as version 5.050 before use. Foreground orchestration ran concurrent unit, integration and differential campaigns with at most 16 compile workers. All builds and probes lived in the clone or packet scratch. The 12 GiB unit limit remained set; observed peak was 5,040,455,680 bytes, with zero memory-limit/OOM events ([resource-limit-observation.json](resource-limit-observation.json)).

| Execution | Result / receipt |
|---|---|
| Unit control | 186 checks, zero failures; `receipts/unit-control-run.log` |
| Unit plants | 58/58 compile successfully and fail their named checks with exit 1; individual build/run logs and exit files |
| Real datapath | Five clean checks; 5/5 plants compile and fail their named checks with exit 1; `receipts/integration-control-run.log` and plant receipts |
| Firmware/RTL differential | 12 clean cases, 17/17 named defect rejections; `receipts/differential.log`, exit 0 |
| Independent receive/range probe | 1,554 checks, zero failures; `receipts/boundary-run.log`, exit 0 |
| Accepted baseline check | Three endpoints pass; `receipts/resource-baseline.log`, exit 0 |
| Current inventory | All 66 figures across 22 scopes match the accepted record; `receipts/inventory.log`, exit 0 |

The 63 RTL/integration plants plus two controls are 65 campaign rows, not 65 rejected defects. The 17 differential plants are separate. [campaign-summary.json](campaign-summary.json) records all three campaigns passing; [campaign.log](campaign.log) records completion. Plant exit 1 is expected; builds and clean controls exit 0.

Portable reproduction from this packet, with ROOT pointing to the detached exact-head clone and VERILATOR to the verified 5.050 executable:

```sh
python3 run_review.py --root "$ROOT" --verilator "$VERILATOR" --jobs 2
python3 run_boundary.py --root "$ROOT" --verilator "$VERILATOR"
python3 check_inventory.py --root "$ROOT"
python3 verify_integrity.py --root "$ROOT"
```

The campaign wrapper invokes `make -j16` with explicit bounded compile jobs; the source differential uses its own eight-job build. All subprocesses are joined before the foreground runner exits. No full parent, processor, time-protocol, portability or builder bank, implementation route, workflow replication or hardware run was executed by this reviewer.

One private compiler installation prefix was replaced in one published log. [receipt-redactions.json](receipt-redactions.json) records the file, original and public hashes, and exact substitution. Result lines are unchanged; the raw original remains in unpublished scratch. Other execution logs are unmodified.

**Public source evidence**

The author's [Round 14 receipts](https://github.com/kebag-logic/milan-fpga/tree/217cf1306f90460527ab5cf477ad3c16bdaa72d9/review-evidence/696-r1/author-r14/round14-receipts) are source-head evidence, not a manager source bank. [public-receipts.json](public-receipts.json) lists immutable URLs, sizes and hashes. [public-evidence-check.json](public-evidence-check.json) verifies 25 downloaded artifacts against the public manifest and 241 input entries covering 123 unique local source files. Ten external/generated entries were not regenerated here; the author's larger input count is not my independent check.

The examined author evidence distinguishes exact-head executions from historical totals:

- Seven selected suites report 38,218 checks here. The 62-suite, 2,187,183-check bank belongs to `313616d1`, not this head.
- MAAP reports 186 unit checks, 63 rejected defects/two controls, five integration checks, 225/225 eligible lines covered, and the 12-case/17-defect differential. The annotation's 225/250 attached coverage points uses a different denominator.
- Other author receipts report 506/506 firmware plants, 435 store checks, 29 coverage controls, 30 covered files after exclusions, shared-stack boundary/pin/figure controls, static gates, 58/58 portability tops, 44 memory plants, 916 sharded invocations and 406 behavioral scenarios with 1,977 steps. These were inspected, not independently rerun.
- Required builder elaborations executed. Historical calibration gate 11 skipped its absent reference report; it is not a calibration pass. Physical calibration is NOT RUN. Field skips are not hardware evidence.

The MAAP hierarchy is 446 LUT / 340 FF against 439 / 280: +7 LUT / +60 FF, within the +60/+60 allowance and consuming all FF headroom. The source shipping route is 49,277 LUT / 53,419 FF, 15,779 slices and 87.5 BRAM tiles, with WNS +0.242 ns / WHS +0.017 ns. All 100,306 nets are routed with no route errors. The +0.030 ns floor is met. Standalone wrappers remain 23,179 / 19,779 at 1x1 and 30,135 / 27,380 at 8x8; their timing figures belong to standalone endpoint policies, not shipping-route timing.

The accepted source baseline remains the `bee1b0d7` record: 50,013 LUT / 54,306 FF, WNS +0.233 ns / WHS +0.017 ns. D7 does not turn each intermediate measurement into a new accepted baseline. Public checks and three external `record --write` measurement copies preserve that distinction. None of these source measurements validates the final merge result against live dev.

**Prior finding reconciliation**

These dispositions rely on examined artifacts at this head, not inherited approval. Original lens assignments are retained.

| Prior finding / severity / lenses | Disposition and current evidence |
|---|---|
| R558-1-F1 — MINOR — Docs | Resolved. `MAAP_FABRIC.md:155` separately dates historical lane/merge figures. |
| R559-1-F1 — MINOR — Tests | Resolved. `sim_main.cpp:836` holds loss for 24,000 cycles in both states; the link-loss restart plant fails. |
| R559-1-F2 — MINOR — Docs | Resolved. `MARK_II_AREA_PLAN.md:110,121` names the current record; 66/66 figures independently match. |
| R559-1-F3 — MINOR — Docs, Tests | Resolved. `MAAP_FABRIC.md:250` and the fixture name MAC 02:00:00:00:00:00 with clock zero; zero-freeze plants fail. |
| R558-3-F1 = R559-3-F1 — BLOCKER — Conformance, Robustness, Tests | Resolved in source. `integration.mk:12,23` clears inherited flags for both derivations, passes bounded jobs and refuses failed/empty captures. Current controls/plants build and discriminate. Earlier public correction evidence covers the specific 4.3 failure; this pass used installed 4.4.1, not a fresh 4.3 or hosted run. Hosted acceptance remains with the manager. |
| R558-5-F1 — MINOR — Docs | Resolved. `AREA_BUDGET.md:381` and `MARK_II_AREA_PLAN.md:656` distinguish historical M0s base from current #696 record. |
| R558-6-F1 — MINOR — Conformance, RTL, Robustness, Tests | Resolved. `KL_maap.sv:154,331` steps the full sampled seed; datapath and universal checks discriminate the amended criterion. |
| R558-7-F1 — MINOR — Tests | Resolved. `sim_main.cpp:437` grades requested start below own offset; `m2_echo_overlap_start` fails. |
| R559-6-F1 — MINOR — Tests, Conformance | Resolved. Decision 6102832618 narrows the impossible criterion; `sim_main.cpp:1089` and `MAAP_FABRIC.md:106` state the actual pair and word/block claims. |
| R559-6-F2 — MINOR — Tests, Docs | Resolved. `sim_main.cpp:1180` learns actual RTL maps and checks 528 carry masks, 65,536 words, counts 1–8, rank and independence. Fold-row, unstepped-fold and nonlinear/control plants fail. Structural linearity remains an explicit premise. |
| R558-9-F1 — MINOR — Docs | Resolved. `MARK_II_AREA_PLAN.md:696,952` identifies #645/#647's matching base and separately compares against #696. |
| R558-11-F1 — MINOR — Docs | Resolved. `MARK_II_AREA_PLAN.md:1099` makes the same distinction for M5. |

| Earlier wording / optional IDs | Disposition and artifact |
|---|---|
| R559-1-R1/R2/R3 | Resolved: dated area attribution, recorded-deviation wording and findings index now describe #696. |
| R558-2-R1 / R559-2-R1; R558-5-R1 | Retained RESIDUE with exact fixes below. |
| R558-4-R1, R558-6-R1, R558-10-R1, R559-7-R1, R558-13-R1, R559-10-R1 | Earlier head-specific text was replaced; publication wording recurs at Round 14. Consolidated as R559-11-R1 below. |
| R558-7-R1 / R559-6-R1 | Resolved by precise pair list and word/block distinction in `MAAP_FABRIC.md:117,259` and PR limitations. |
| R558-9-R1 / R558-11-R1 | Resolved at `MARK_II_AREA_PLAN.md:707,973,1115`: unchanged-record language is scoped to M2/M6/M5. |
| R558-1-S1 | Applied: plan `:56` states current WNS and binding floor. |
| R559-1-S1, S3, S4 | Retained optional: no exhaustive arbitrary-nonlinear guarantee; no nonshipping high-frequency timing proof; older mutant guard is not a full M1–M8 registration gate. Artifacts: universal harness, integration clock assumptions, mutation table. |
| R559-1-S2 | Applied: PR reproduction runs integration from its output directory. |
| R558-3-S1 / R559-3-S1 / R558-4-S1 / R559-4-S1 | Empty-list arm resolved; directory detection remains optional at `integration.mk:19`. A directory fails at compilation, not silently. |
| R558-3-S2 / R559-4-S2 | Retained optional: no default mutation arm reproduces the historical 4.3 inherited-flag/jobserver shape. |
| R558-4-S2 | Retained optional: precise trigger wording at `integration.mk:8`. |
| R559-5-S1 | Retained optional: no durable repository gate couples all prose record sentences to JSON; current independent inventory check passes. |
| R558-6-S1 / S2 | Retained optional: explicit live-count snapshot plant and fuller placement-specific link-loss documentation. |
| R558-7-S1 / R559-6-S1 | Applied: universal probe-fold check rejects `m4_probe_fold_unstepped`. |
| R558-7-S2 / R559-6-S3 | Retained optional: no separate plant for later Begin! reuse of first fold. |
| R559-6-S2 | Retained optional: larger-count clipping lacks a discriminating fixed-eight-clamp plant. |
| R558-8-S1 | Retained optional: `docs/testing/TESTING.md:612` could mention the real datapath arm. |
| R559-7-S1 | Retained optional: direct checks for M5's precise fresh range, count-zero bounds and announce timer's particular draw. Current code was examined; these were not filed as defects. |

No unresolved defect is moved to another issue to clear a lens. Suggestions retain their original optional status and do not replace acceptance checks.

**Residues for the manager checklist**

R559-11-R1 — RESIDUE — Docs — [PR #706](https://github.com/kebag-logic/milan-fpga/pull/706), Status, checkout introduction and pending-duties bullet.

Authority/evidence: [pr-snapshot.json](pr-snapshot.json) records public head e2cd089c while the body says published head remains 313616d1 until publication. Measurement and prior-verdict attributions are separately explicit. Impact: stale publication wording only. Required exact fix: replace the local/published-head sentences with “Published head: `e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd`.” Replace “After the manager publishes this head:” with “To reproduce this published head:”. Remove “publication,” from pending duties; update review completion only after both finished reports. Verification: compare revised wording against PR head metadata. No measurement, test, verdict or clause claim changes.

R558-2-R1 / R559-2-R1 — retained RESIDUE — Docs — `docs/design/MARK_II_AREA_PLAN.md:66,67,317,1129`.

Authority/evidence: the section explicitly retains dev 5603c353's historical baseline, but its link points to the live record. Impact: ambiguous historical tense; current figures are separately correct. Required exact fixes: at `:66`, use “Source: [pp_resource_baseline.json](../../syn/ooc/pp_resource_baseline.json) as committed on dev `5603c353`, all three `record` objects; #696 has since re-recorded the file (see [Current processor inventory](#current-processor-inventory)).”; at `:67`, replace “Each” with “At that revision, each”; at `:317`, use “The [current ledger](#ledger) starts from the 50,267 route figure of the #645/#647 record.”; at `:1129`, replace “Adopted processor pin and current three-endpoint record” with “Adopted processor pin and the #645/#647 three-endpoint record”. Verification: read historical and current sections together; leave numerical tables unchanged.

R558-5-R1 — retained RESIDUE — Docs — `docs/design/AREA_BUDGET.md:372,389`; `docs/design/MARK_II_AREA_PLAN.md:669`.

Authority/evidence: unchanged-record sentences belong to M0s; surrounding text already distinguishes its base from #696. Impact: grammatical scope only. Required exact fixes, respectively: “M0s does not change acceptance records or policy values.”; “M0s does not change acceptance records, schema or policy.”; “M0s does not change the acceptance schema, thresholds or records.” Verification: confirm scope is M0s, leaving D7/M9 policy and all measurements unchanged.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #696 decisions; MAAP_FABRIC.md:42; KL_maap.sv:141,238,313,331; resource check receipts; acceptance table above | R559-11 | e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd |
| RTL | CLEAN | hdl/ieee1722/maap/KL_maap.sv:141,219,269,313,340,433; hdl/milan/milan_datapath.sv:2933,3000,7181; merge resolution in source-provenance.json | R559-11 | e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd |
| Robustness | CLEAN | KL_maap.sv:319,331,421,433; sim_main.cpp:744,774,811,836,874,895; boundary_probe.cpp; receipts/boundary-run.log; integration.mk:12,23 | R559-11 | e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd |
| Tests | CLEAN | tb/verilator/maap/{sim_main.cpp,sim_integration.cpp,mutants.py,Makefile,integration.mk}; sw/firmware/ctrl/test/{maap_differential.py,test_maap_differential.cpp}; campaign-summary.json and per-case receipts | R559-11 | e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd |
| Docs | CLEAN | docs/design/{MAAP_FABRIC.md,AREA_BUDGET.md,MARK_II_AREA_PLAN.md}; docs/findings/{234_PP_SHADOW_AREA_BASELINE.md,README.md}; KL_maap.md; firmware MAAP README; PR snapshot; public source receipts; 66-value inventory check | R559-11 | e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd |

This ledger covers e2cd089c only. A later change within a lens's scope invalidates its coverage until reviewed again.

**Integrity, limits and manager duties**

[Before](integrity-before.json) and [final integrity](integrity-final.json) checks compare raw tracked blob bytes, modes and every index entry against the exact tree. Final status is clean. They verify 1,311 root blobs, all recorded gitlinks and the initialized required submodules:

| Submodule | Verified head |
|---|---|
| protocol-processor | 2ad2f845dd583f8310075fa2380cb60a04fd091a |
| gptp-processor | 7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9 |
| third_party/verilog-axis | 48ff7a7e2ef782cf778d47910cf85835c64b1bce |
| third_party/tsn-c-stack | 405dc68310a18f669049ffc10cc23eef7300dcff |

No tracked source was changed. Probes and mutations use scratch copies. No commit, push, GitHub write, author contact, merge, hardware access or workflow replication occurred.

The manager retains publication of both finished reviews, residue handling, exact-head hosted/replica acceptance and final current-dev candidate validation. No exact-head hosted jobs were audited here; no skipped or pending context is counted as executed evidence. There is no manager source bank at this head.

The supplied source base is `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`; supplied live dev is `a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0`. At the merge turn, the manager must construct the then-current candidate, run builder and native banks, link receipts on the PR, obtain needed review of resulting changes, and follow merge authorization and post-merge containment rules. Source-head evidence does not establish candidate validity. Acceptance 4 remains assigned to post-merge reference-peer bench work. Physical calibration NOT RUN and field skips remain outside hardware proof.

Only REPORT.md and files enumerated in MANIFEST.sha256 are publishable. Nothing under scratch is included.

R559-11 FINISHED
