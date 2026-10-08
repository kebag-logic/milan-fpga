[R533] POSITIVE - exact head b98eb2d5a21522bab3bc6bb943332cf8edf11893

R533-11 external independent source review of issue #665 / PR #690. All five lenses are CLEAN. The five round-10 findings are resolved in the reviewed source and tests. No new BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION is filed. This verdict does not clear the separate hosted, current-dev candidate, integration or merge obligations.

Tree: `45e0efdbceac0cd7cc9b97d76d0245e33643c1ab`. Source base: `d8b355fe0f41d49dca6cae1cd8b3826e2edde364`. Focused delta: `82a79638405c3365e4078da471be56758f8dd679..b98eb2d5a21522bab3bc6bb943332cf8edf11893`, three commits and 18 files. The complete source-base diff and history supplied context; this is a delta review against the round-10 baseline, not a claim to have executed every historical bank.

Reconstruction followed AGENTS/CONTRIBUTING, the documentation index, frozen issue scope and public decisions, requirements/interfaces, and source diff/history. The published HANDOFF's written event model was examined before the implementation. The independent verdict and five-lens ledger were written in `receipts/independent-pass.md` before reading either round-10 review. Their public findings and earlier disposition tables were then reconciled. No private author material or another current-round review supplied this verdict.

Public authorities: [frozen F4 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6030279477), [round-11 assignment and kind-change decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6049530812), [serialization rule #678](https://github.com/kebag-logic/milan-fpga/issues/678), [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6050418707), [review start](https://github.com/kebag-logic/milan-fpga/pull/690#issuecomment-6050445074), and [public evidence at 2f7ab26d](https://github.com/kebag-logic/milan-fpga/tree/2f7ab26dadbd359c55eb248ef56fcbcbe4e6bd40/review-evidence/665f4-r1/author-r11). Repository authorities include `REQUIREMENTS.md:24`, `docs/reference/FR_NFR.md:333`, `docs/design/MAILBOX_SPLIT.md:715`, and the ACMP/SRP public headers and READMEs.

The implementation matches the written feedback model. Each accepted sink/interface binding retains its latest continuous kind and first withdrawal. Read-only observations occur between complete wire events, on receive return, after ticks, at reset and at poll. They preserve an atomic JoinIn/JoinMt replacement while distinguishing Lv then New, including within one PDU. Registration or kind delivery precedes a retained withdrawal. That withdrawal terminates the binding through deferred stop/reprobe, so later observations of the retiring epoch need no unbounded queue. Pending intent immediately gates old feedback; accepted intent resets the prefix even when the wire identity is unchanged. Delivery remains outside protocol and port callbacks.

`acmp_tk_kind_changed` admits only SETTLED_RSV_OK and updates the reported failure view through the existing finish/notification path. It does not replay EVT_TK_REGISTERED or change the state machine. This follows the manager's explicit option (a), the in-repository Table 5.23/5.30 contract, and the GET_RX_STATE wire checks. Unchanged repeats do not generate another notification. The new entry also participates in the reentry tests.

**Round-10 finding disposition at this head.** Original severities and attributable lenses are retained; none was relabeled to obtain coverage.

| Finding | Original severity / lenses | Resolution and verification |
|---|---|---|
| R533-10-F1 | MAJOR / Conformance, RTL, Robustness, Tests | RESOLVED. `acmp.h:420`, `acmp.c:1132`, `ctrl_app_srp.c:84`, and `srp_feedback.hpp:36` implement the authorized view update. Both original R533 kind probes pass at IF=1/2. Both direction plants fail the named current-kind assertion at both counts. |
| R532-10-F1 | MINOR / Conformance, RTL, Robustness, Tests, Docs | RESOLVED. Both original `R10KindChangeWhileSettledReachesAcmp` and `R10FailedToAdvertiseWhileSettledReachesAcmp` pass at IF=1/2. Wire flags follow the current registration; state remains settled. The header and both READMEs state the authorized Table 5.30 interpretation. |
| R533-10-F2 | MAJOR / Conformance, RTL, Robustness, Tests | RESOLVED. `srp_mbx.h:34`, `srp_mbx.c:127,383,515,643`, and `ctrl_app_srp.c:61` retain and retire the event prefix. `R533WithdrawalBeforeReregistrationStillReprobes` passes at IF=1/2, with `R533SeparatePassWithdrawalDoesReprobe` green. Standing cases also pass for single-PDU Lv/New, expiry then fresh receive, first registration then withdrawal, kind-before-withdrawal, isolation and identical-identity supersession. Their named plants are caught at both counts. |
| R532-10-F2 | MINOR / Tests | RESOLVED. `srp_feedback.hpp:147,159` tests refused replacement and earlier-sink retry accumulation. Both original guard probes pass. `r10-feedback-ignores-pending` and `r10-transient-refusal-forgotten` fail their named assertions at IF=1/2. The complete driver includes both in the IF=1 repeat selection. |
| R532-10-F3 | MINOR / Tests, Conformance, Docs | RESOLVED. `srp_feedback.hpp:167` reaches ENTITY_AVAILABLE followed by withdrawal and measures the delivery poll itself. It also measures first registration followed by withdrawal. Both allowance plants fail the measured per-sink assertion at IF=1/2. `ctrl_app.h:69`, both READMEs and `MAILBOX_SPLIT.md:715` agree on six accesses per sink and totals 3224/4073. |
| R532-10-S1 | SUGGESTION / Docs | ADDRESSED. `ctrl_app.h:140` wraps the attach comment. |

The original round-10 reports are [R533-10](https://github.com/kebag-logic/milan-fpga/pull/690#issuecomment-6049503727) and [R532-10](https://github.com/kebag-logic/milan-fpga/pull/690#issuecomment-6049526439). The broader part of R532-9-F1 that R533-10 retained through its two findings is now resolved as well; it has not been moved to target integration or another issue.

**Independent execution.** Scripts run from the candidate root, keep products under packet `scratch/`, wait for their children, and retain logs and return codes. Three campaigns ran concurrently, with four compilation jobs each; maximum requested concurrency was 12. No shell job was detached.

| Execution | Result / receipts |
|---|---|
| Five focused suites at IF=1/2 | 124 tests pass per count: four-module composition 44, SRP application/bounds 5, adapter 53, receive recovery 17, selected processor-wire differential 5. `focused-if1.log`, `focused-if2.log`, `validation.json`. |
| Focused feedback campaign | All 19 plants caught at each count, 38 catches. Includes both kind directions, unchanged-repeat protection, first and intrapdu withdrawal, expiry, ordering, supersession, sink/interface isolation, and all four `r10-*` plants. Individual `if1-*.log` / `if2-*.log` retain named failures, not compilation failures. |
| Original round-10 probes | Nine applicable tests pass per count, 18 passes. `replay-1.log`, `replay-2.log`, `probe-inputs.json`. The three imported headers are byte-identical to their public packet versions and included in `scripts/prior-probes/`. |
| AddressSanitizer | 22 binding/feedback tests pass per interface count; the separate core/adapter control passes 85 tests. `acmp-kind-lost`, `acmp-kind-any-state`, `acmp-open-unguarded`, and `acmp-init-too-many-sources` each fail the named assertion under instrumentation, without an address-error report. `replay-0.log`, four `*-asan.log` files, and `sanitizer-instrumentation.json`. The open-entry plant is caught at entry 10. |
| Coverage | `fw_coverage.py --check --jobs 4`: PASS, all 22 files at 100% lines/branches after unchanged exclusions. ACMP is 742/742 lines and 348/348 branches; composition delivery 82/82 and 62/62; adapter 489/489 and 454/454. `coverage.log`. No ratchet or source was written. |
| Documentation/contract checks | Eight commands pass: generated mailbox, documentation, style, C/C++ and Python idioms, submodule documentation, added em-dash check, and diff whitespace. `docs.json` and `docs-*.log/.rc`. |
| Public evidence binding | All 113 final gate records have rc 0; all 111 retained logs match their published sizes and SHA256 hashes. The remaining two invocations have receipt metadata only. `public-evidence-audit.json`. This audit is not a fresh execution of those banks. |
| Source integrity | Parent and four required dependencies match their tracked blob bytes, modes, stage-zero index and exact pins, with no hidden index flags. Parent status is clean. `integrity.json`. |

The nine original acceptance probes include the four R533 cases, the two R532 kind cases, the two R532 pending/refusal cases, and discovered withdrawal. The diagnostic `R10WithdrawalFeedbackCostFitsAllowance` is excluded: it demands nonzero accesses from an undiscovered withdrawal that correctly goes passive without mailbox work. Its discovered-talker counterpart is run unchanged, and the standing test measures both funded paths.

Measured feedback accesses for two sinks:

| Path | IF=1 | IF=2 | Two-sink allowance |
|---|---:|---:|---:|
| Settled discovered withdrawal | 5 | 7 | 12 |
| First registration followed by discovered withdrawal | 5 | 11 | 12 |

Both allowance understatements are caught. The complete envelope reserves 96 accesses for 16 possible sinks, yielding 3224/4073 per four-module pass. Independently funded SRP terms remain 770/1540 for poll and 1596/2366 for pass. These are mailbox-access envelopes over alternative paths, not a simultaneous worst-case trace or measured target execution time. The changed observer also performs registrar scans whose CPU cost remains outside that access count.

**Published images and builder receipt.** The source audit confirms that `803e8c3c9e7506c4f004d562437ae4f374fbad8e..b98eb2d5a21522bab3bc6bb943332cf8edf11893` changes only the expected failure text in `acmp_review_mutants.py`, entry 9 to entry 10. No production, positive-test, coverage, image or builder input changes follow the builder receipt. The local sanitizer run independently catches that corrected oracle. The public complete firmware campaign is at the final head.

| Published linked fixture | IF | Text | Read-only | BSS | Reserved stack | RAM span |
|---|---:|---:|---:|---:|---:|---:|
| 1x1 TDM8 | 1 | 45392 | 2878 | 23440 | 8192 | 79904 |
| 1x1 TDM8 | 2 | 46676 | 2878 | 34808 | 8192 | 92576 |
| 8x8 | 1 | 45444 | 2878 | 38200 | 8192 | 94736 |
| 8x8 | 2 | 46820 | 2878 | 64328 | 8192 | 122240 |

Initialized data is zero. The public section totals, spans, runtime and ELF hashes were inspected and preserved in the evidence audit; these images were not freshly linked in this review. Recorded spans include section placement and alignment. A reviewer audit assumption about total alignment padding was corrected as recorded in `reviewer-control-correction.txt`; no product measurement or acceptance test changed. The 8192-byte stack is a reservation, not a measured call-chain bound. The source-base diff changes no RTL, mailbox YAML/generated contract, shipping configuration or SoC input.

**Earlier findings retained at this head.** These dispositions use the round-10 public baseline and the current artifacts named below. “Retained resolved” does not claim a rerun of every old mutation campaign.

| Earlier finding(s) | Current disposition and evidence |
|---|---|
| R532-9-F1 | RESOLVED in full source scope: both feedback directions, healthy registration beyond TMR_NO_TK, kind changes and withdrawal now pass; `ctrl_app_srp.c`, `srp_binding.hpp`, `srp_feedback.hpp`. |
| R532-9-F2/F3; R532-9-S1/S2 | Retained resolved/addressed: parking, retirement and transient retry remain in the composition; current native parking and independently funded poll/pass tests pass. The prior original term-plant results remain baseline evidence; those older campaigns were not rerun here. |
| R533-8-F1 | Retained resolved: deferred ACMP-to-SRP ownership, retry, cancellation, interface and sink identity; current 44-case composition suite and original replacement/refusal probes pass. |
| R532-8-F1 | Source/test defect resolved: the owned extra-byte fixture remains and the source-count plant is caught under AddressSanitizer without overflow. Separately requested hosted acceptance is still unverified and remains with the manager. |
| R532-8-F2/F3/F4 | Retained resolved: real SRP access measurements pass; `maap/README.md:134` attributes 1580/1659 to the three-module bound; `ctrl/README.md` limits named plant claims to their supported checks. Current four-module totals are 3224/4073. |
| R533-1-F1; R532-1-F1 | Retained resolved: immediate MSRP IN leave and the original LV/#608 deadline remain in the pinned library and adapter; current adapter and wire-differential suites pass. |
| R533-1-F2; R532-2-F1 | Retained resolved: link-level reconciliation, restart fencing and recovery remain in `srp_mbx.c`; current lifecycle tests pass. |
| R533-1-F3; R533-2-F1; R532-2-F3/F4; R532-3-F1/F2 | Retained resolved: shared StreamID reconciliation, replacement Applicant inheritance, final-user VID and Domain ownership remain; current shared-binding tests pass. |
| R532-1-F2 parts 1/2 | Retained resolved: admission ceiling and Ready/ReadyFailed cases remain in the current passing adapter suite. |
| R532-1-F2 part 3; R533-2-F2 | Retained resolved from the round-10 baseline: the public lwSRP pin is unchanged at `9197193e47a6bb1c45a56d90a18c1784123aba44`, including its accepted note-4/5 work. Upstream full profiles were not rerun. |
| R532-2-F2 | Retained resolved: public dependency pin, `THIRD_PARTY.md`, `SUBMODULES.md`, current passing submodule/doc checks. |
| R533-5-F1; R532-5-F1; R532-6-F1 | Retained resolved: whole-record retention, allocation recovery, cancellation and original-arrival 1000 ms expiration remain; all 17 receive-recovery cases pass at both counts. |
| R533-1-F4; R532-6-F2 | Retained resolved: historical baseline/delta measurements remain public, and the round-11 image receipt records the four current figures above. No fresh linked-size reproduction is claimed here. |
| R533-6-F1 | Retained resolved: the public mailbox export recipe names existing tracked paths and the NVM header directory. No mailbox/RTL delta is introduced in this round. |
| R532-1-R1/R2; R532-2-R1/R2; R532-3-R1; R532-5-R1/R2; R532-6-R1; R532-7-R1; R532-8-R1/R2; R533-6-R1; R533-7-R1; R533-8-R1 | Retained resolved under baseline dispositions: current prose preserves tick units, measurement scope, public dependency status, merged-note wording, “completes or expires,” composition attachment and corrected checkout wording. Current documentation checks pass. |
| Earlier optional suggestions through round 8 | Prior addressed/optional dispositions retained. None is promoted to a source defect or used as proof of new behavior. |

**Reviewer-owned ledger.** Every lens was applied at this exact head. These are source-review results, not the manager's complete merge ledger.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #665 frozen scope and kind decision; `REQUIREMENTS.md:24`; `FR_NFR.md:333`; `acmp.h:420`; `acmp.c:1116,1132,1145`; real GET_RX_STATE and withdrawal probe receipts | R533-11 | b98eb2d5a21522bab3bc6bb943332cf8edf11893 |
| RTL | CLEAN | Empty protected RTL/contract/configuration diff; `ctrl_app_srp.c:55`; `srp_mbx.c:127,383,515,643`; pinned `mrp_mad.c:990,1170`; deferred request lifecycle, bounded storage and reentry checks | R533-11 | b98eb2d5a21522bab3bc6bb943332cf8edf11893 |
| Robustness | CLEAN | `srp_feedback.hpp:63,85,125,147,159`; current lifecycle/shared-binding/receive-recovery suites; supersession, expiry, refused replacement and two-interface receipts | R533-11 | b98eb2d5a21522bab3bc6bb943332cf8edf11893 |
| Tests | CLEAN | `srp_feedback.hpp:36,167`; `test_acmp.cpp:751`; `srp_mutants.py:786`; `test_ctrl_firmware.py:202`; 38 feedback catches, four sanitized core plants, original probes and 22-file coverage check | R533-11 | b98eb2d5a21522bab3bc6bb943332cf8edf11893 |
| Docs | CLEAN | Published author-r11 HANDOFF feedback event design; `ctrl/README.md:134`; `srp/README.md:53`; `MAILBOX_SPLIT.md:715`; public gate/image audit, corrected oracle diff and live PR body | R533-11 | b98eb2d5a21522bab3bc6bb943332cf8edf11893 |

**Real limits and pending manager duties.**

- This review checks the public manager interpretation and repository clause/interface contracts. It does not claim a fresh independent reading of the complete licensed Milan and IEEE editions. Unchanged wire probes, current state guards and the public option-(a) decision are direct evidence for the reviewed change.
- Local sanitizer execution covers first-party core/composition/adapter code, with instrumentation verified in the recorded objects. The inherited library build is not claimed as instrumented. The public two-compiler sanitizer bank is separate evidence.
- Full parent/processor/timing/synthesis/builder banks, fresh linked images and physical work were not run. The provided source-bank status and published author receipts are source evidence; they do not validate a current-dev merge candidate. The HDL compiler's specified release identity was checked, but no HDL build was needed or run here.
- Physical calibration remains NOT RUN. Field skips, host-model results and linked size fixtures are not hardware, boot, audio-soak or target timing proof. Live stream/MAAP updates, the fabric licence output and target scheduling remain integration work. PR #690 remains partial for #665.
- The exact-head API returned no check runs and no workflow runs. No executed or skipped hosted context is counted as evidence. Hosted firmware-unit/rtl-fast acceptance, ready-state gates and trusted local replication remain manager duties, including the separately requested hosted portion of R532-8-F1.
- Assigned live dev was `291710b180ca9196780a6d17f2517957c9bcb89c`; the read-only query during this review returned `99e4eb6c14462aafa84bb1ac597fd241abc1a240`. The manager must construct and validate the candidate from the then-current remote dev, obtain the complete independent review bar and explicit merge authorization, and perform post-merge containment. This source verdict is not that candidate validation.
- Publication belongs to the manager. This session made no source fixes, commits, pushes, GitHub writes, other-checkout edits or merge. Only REPORT.md and files listed by MANIFEST.sha256 are intended for publication; scratch is excluded.

R533-11 FINISHED
