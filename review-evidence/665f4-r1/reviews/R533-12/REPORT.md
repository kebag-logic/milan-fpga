[R533] POSITIVE - exact head efea74858dffc482820d4f19c26c38796a57ff75

R533-12 is the external independent source review of issue #665, lane F4, and PR #690. Tree: `4e28d2409425b352c51d79526e4b48d6c93a38b7`. All five lenses are CLEAN. No BLOCKER, MAJOR or MINOR remains in the reviewed source scope. One prose-only RESIDUE is recorded below. This verdict does not authorize merge or certify target execution.

**Reconstruction and independence.** Read AGENTS.md and CONTRIBUTING.md, docs/README.md, the issue body and public scope decisions, linked requirement/interface authorities, the source-base diff `99e4eb6c14462aafa84bb1ac597fd241abc1a240..efea74858dffc482820d4f19c26c38796a57ff75`, history and both merge parents, then public executable evidence. The focused delta is `b98eb2d5a21522bab3bc6bb943332cf8edf11893..efea74858dffc482820d4f19c26c38796a57ff75`.

Controlling public inputs: [F4 scope](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6030279477), [full testing](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6008744385), [interface/#608 additions](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6009661573), [linked-size acceptance](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6030870481), [kind-change decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6049530812), [round-12 decision (a)](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6050694779), and [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6051676441).

The independent pass and provisional verdict/ledger were written to `receipts/independent-assessment.md` before reading any prior reviewer report. Prior public findings were then reconciled against current artifacts. No private author material, management scratchpad or other checkout was used.

**Round-12 resolution.**

| Finding / obligation | Result and artifact-specific evidence |
|---|---|
| R532-11-F1, MINOR, RTL and Docs | RESOLVED under decision (a). `srp_mbx.c:79-115` copies indication data. `interested_msrp` at :159-190 reads adapter state and callback values; `capture` at :562-570 calls no library entry. Registrar visits at :581 occur at receive boundaries (:424-432), after library timer service (:49-52), and in the poll (:766), outside library callbacks. Neither pin nor library contract changed. |
| Atomic replacement and intra-PDU ordering | Preserved. Pinned `mrp_mad.c:989-1067` calls the filter before the next AttributeEvent and completes both replacement indications inside one event. The next filter observes the completed prior event; receive return observes the last event. Single-PDU kind-replacement, Lv/New and identity-mismatch/recovery cases pass at IF=1/2. `feedback-intrapdu-lost` and the three indication-copy plants fail their named assertions at both counts. |
| Contract citations | Correct. `srp/README.md:70-82` cites the exact `9197193e` [integrator contract, lines 321-323](https://github.com/kebag-logic/lwSRP/blob/9197193e47a6bb1c45a56d90a18c1784123aba44/doc/integrator.md#L321-L323) and [filter contract, lines 288-290](https://github.com/kebag-logic/lwSRP/blob/9197193e47a6bb1c45a56d90a18c1784123aba44/src/include/shish_lan/mrp.h#L288-L290). Both were read at the pin; both prohibit the former reentry. The code comment cites the same authorities. |
| R532-11-F2, MINOR, Tests and Docs | RESOLVED. `srp_feedback.hpp:184-240` exercises identical-identity rebind after undelivered withdrawal; settled link down and down/up with re-registration before delivery; and retained pre-withdrawal kind. Real mailbox input and the composition poll are used. The exact `p11-supersession-kind-stale`, `p11-reset-withdrawal-lost` and `p11-postwithdrawal-kind-overwrite` plants are caught by name at IF=1/2. `test_ctrl_firmware.py:202-204` includes `p11-` in the standing IF=1 selection. README and PR-body claims match those tests. |
| Original acceptance probes | PASS at IF=1/2. Byte-identical public probes run from disposable copies. `R533WithdrawalBeforeReregistrationStillReprobes` and `R533SeparatePassWithdrawalDoesReprobe` pass. Kind probes report wire flags 0x42 for Failed and 0x02 for Advertise. Original R532-11 supersession/reset/kind and unchanged-repeat probes also pass. See `replay-if1.log`, `replay-if2.log`, `prior-probe-inputs.json`. |
| R532-11-S1, optional Docs suggestion | ADDRESSED. `MAILBOX_SPLIT.md:737-739` names per-event sink scans and receive/tick/poll registrar visits separately from mailbox-access bounds. Target calibration still owes both costs. |

**Merge and composition.** Merge `d1fe17d13c9ab976dd11667f36231718314ef7c6` has exactly the previous reviewed head and assigned dev `99e4eb6c14462aafa84bb1ac597fd241abc1a240` as parents. Its entire firmware tree equals its first parent's tree: the merge preserves F3's composition, ACMP implementation, saved-state/image fixture and F4's SRP code. Against the dev parent, `hdl`, `sw/mailbox`, `sw/litex`, processor and gPTP gitlinks remain unchanged at the reviewed head. GMII capture patch 0007, its constraints and test are retained. Processor pin: `2ad2f845dd583f8310075fa2380cb60a04fd091a`; lwSRP pin: `9197193e47a6bb1c45a56d90a18c1784123aba44`.

The four-module attachment and deferred fifth poll remain at `ctrl_app_srp.c:51-133`; ACMP's kind-only entry remains at `acmp.c:1132-1143`. IRQ/filter composition, sink/interface routing, pending intent, parking, retirement and feedback ordering pass the current composition suites. Dependency-document conflict resolution retains the processor pin and lwSRP node. The PNG was visually inspected and agrees with the merged inventory. `receipts/merge-audit.json` records both-parent comparisons.

**Independent execution.** Foreground executions waited for their children. Independent campaigns ran concurrently, with at most twelve requested compilation workers, below the sixteen-job limit. Disposable products stayed under packet `scratch/`; no source fixes were made.

| Check | Result / receipt |
|---|---|
| Six focused suites, IF=1/2 | 134 tests per count: composition 49, adapter 53, receive recovery 17, application/bounds 5, latency 5, selected processor-wire differential 5. All pass. `baseline-if1.log`, `baseline-if2.log`, individual suite logs. |
| Focused mutation campaign | Seven plants per count, fourteen named catches. Four intra-PDU/copy plants plus all three exact `p11-*` plants. Compiled behavioral failures, never build failures. `mutants-if1.log`, `mutants-if2.log`, individual diagnostics. |
| AddressSanitizer | The same 134 tests per count pass. Sixteen first-party firmware objects contain 169 sanitizer references in each composition build. The inherited library and host-helper builds are uninstrumented; no library instrumentation is claimed. `asan-if1.log`, `asan-if2.log`, `sanitizer-instrumentation.json`. |
| Original public feedback probes | Eight tests per count, sixteen passes. Probe source hashes retained; firmware unchanged. `replay-if1.log`, `replay-if2.log`. |
| Coverage ratchet | PASS: 22 files at 100% lines/branches after unchanged exclusions. Adapter 515/515 lines, 478/478 branches; delivery 82/82 and 62/62; ACMP 742/742 and 348/348. `coverage.log`, `coverage.rc`. No ratchet written. |
| Docs/contract checks | Generated mailbox, submodule documentation, documentation/privacy, style, C/C++ idioms, Python idioms, added-em-dash and diff-whitespace checks pass. Earlier reviewer command-name/flag errors and missing-renderer refusal remain recorded; correct invocations pass with the locked renderer provisioned only under scratch. `docs.json`, `docs-corrected.json`, `docs-final.json`. |
| Public gate audit | All 114 final records have rc 0; all 112 retained logs match published sizes and hashes. Two records have metadata only. Evidence audit, not fresh execution of those banks. `public-gates-audit.json`. |
| Integrity | 1,215 parent blobs and all four required dependency populations match commit bytes, file modes and complete stage-zero indexes. No hidden flags or tracked changes. Gitlinks and tree match the assignment. `integrity.json`. |

**Builder, images and bounds.** The [immutable public packet](https://github.com/kebag-logic/milan-fpga/tree/30357b9239a8a5e88298e662b65a20fda1a8b9a2/review-evidence/665f4-r1/author-r12) contains the source-gate evidence. Builder log lines 254-257 record gate 23h passing with all five patches and five missing-patch controls, including both GMII patches composing on the same file. Its final verdict explicitly retains one physical-calibration NOT RUN. The compiler-absent instrument is also intentionally NOT RUN.

Builder/compiler snapshot `7b47f333ecde4af16e32ca95730f56c3c454d0eb` differs from the final head solely by the `p11-` IF=1 mutation-selection prefix (`builder-input-audit.json`). Builder, image and sanitizer source inputs are unchanged. Published complete firmware/coverage runs were repeated at the final head.

| Published linked fixture | IF | Text | Read-only | BSS | Stack reservation | RAM span | Round-11 span delta |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1x1 TDM8 | 1 | 45828 | 2898 | 23440 | 8192 | 80368 | +464 |
| 1x1 TDM8 | 2 | 47112 | 2898 | 34808 | 8192 | 93024 | +448 |
| 8x8 | 1 | 45864 | 2898 | 38200 | 8192 | 95168 | +432 |
| 8x8 | 2 | 47240 | 2898 | 64328 | 8192 | 122672 | +432 |

Initialized data is zero. The copied-kind byte occupies existing structure padding; BSS is unchanged. Public image logs and the size table agree. Images were not freshly linked here. Spans include alignment and reserved stack; that reservation is not a call-chain or routed-resource bound.

Current application/feedback tests and published compiled macros agree on 1596/2366 SRP accesses and 3224/4073 four-module accesses at IF=1/2. Two-sink discovered withdrawal uses 5/7 accesses; first registration followed by withdrawal uses 5/11, within twelve. These are conservative mailbox-access envelopes across alternative paths, excluding CPU and external-port execution. They are not target service-latency measurements.

**Earlier findings.** [R533-11](https://github.com/kebag-logic/milan-fpga/pull/690#issuecomment-6050670567) and [R532-11](https://github.com/kebag-logic/milan-fpga/pull/690#issuecomment-6050691676) are the baseline. Current artifacts support the following dispositions. Retained resolution does not claim rerunning every historical mutation.

| Finding(s) | Current disposition and evidence |
|---|---|
| R533-10-F1; R532-10-F1 | Retained RESOLVED: authorized kind-only entry and current wire-view/original R533 probes pass; `acmp.h:420`, `acmp.c:1132`, `ctrl_app_srp.c:84`. |
| R533-10-F2 | Retained RESOLVED: same-pass, single-PDU, expiry and reset withdrawals remain latched; temporal cases and original withdrawal/control probes pass. |
| R532-10-F2/F3 | Retained RESOLVED: pending-replacement and accumulated-refusal tests remain; funded feedback paths still measure 5/7 and 5/11 accesses. `srp_feedback.hpp:243-288`, `ctrl_app.h:69`. Historical plant dispositions remain baseline evidence. |
| R532-9-F1/F2/F3 | Retained RESOLVED: registration feedback, healthy lifetime, parking, retirement, retry and measured bound terms remain in `ctrl_app_srp.c`, `srp_binding.hpp`, `srp_feedback.hpp`, `srp_app.cpp`; current suites pass. |
| R533-8-F1 | Retained RESOLVED: asynchronous binding delivery, retry, supersession and sink/interface identity; current 49-case composition suites pass. |
| R532-8-F1 | Source/test defect remains RESOLVED: owned extra-byte source-count fixture in `test_acmp.cpp` is unchanged; published sanitizer/core evidence remains valid. Separately required hosted acceptance remains pending with the manager at the recorded query. |
| R532-8-F2/F3/F4 | Retained RESOLVED: real access-path tests pass; MAAP README names the three-module bound; parent README's plant claim is scoped to supported checks. |
| R533-1-F1; R532-1-F1 | Retained RESOLVED: MSRP-only immediate IN leave and original LV/#608 deadline remain in the unchanged library pin; current adapter/differential suites pass. Generic MVRP behavior is retained. |
| R533-1-F2; R532-2-F1 | Retained RESOLVED: link reconciliation, restart fencing and recreation at `srp_mbx.c:674-770`; lifecycle and settled-reset cases pass. |
| R533-1-F3; R533-2-F1; R532-2-F3/F4; R532-3-F1/F2 | Retained RESOLVED: shared identity reconciliation, replacement inheritance, final-user VLAN withdrawal and Domain ownership at `srp_mbx.c:324-393,587-667`; shared-binding cases pass. |
| R532-1-F2 parts 1/2 | Retained RESOLVED: boundary admission and Ready/ReadyFailed tests remain in the passing adapter suite. |
| R532-1-F2 part 3; R533-2-F2 | Retained RESOLVED from baseline: unchanged public lwSRP pin contains note-4/5 tests and reversals. Full upstream profiles not rerun. |
| R532-2-F2 | Retained RESOLVED: dependency pin, licence/inventory and regenerated diagram present; local docs/submodule checks pass. |
| R533-5-F1; R532-5-F1; R532-6-F1 | Retained RESOLVED: whole-record retry, cancellation and original-arrival 1000 ms expiration; all seventeen receive-recovery cases pass at both counts, normal and sanitized. |
| R533-1-F4; R532-6-F2 | Retained RESOLVED: historical base/delta evidence remains public; four current images and round-11 deltas recorded above. No fresh linked build claimed. |
| R533-6-F1 | Retained RESOLVED: current export recipe names tracked mailbox paths and NVM headers. Mailbox sources equal dev; full mailbox bank not rerun. |
| R532-1-R1/R2; R532-2-R1/R2; R532-3-R1; R532-5-R1/R2; R532-6-R1; R532-7-R1; R532-8-R1/R2; R533-6-R1; R533-7-R1; R533-8-R1 | Prior wording dispositions retained: tick units, publication status, measurement scope, retry completion/expiry, attachment and checkout wording remain corrected. R533-12-R1 below is separate. |
| Optional suggestions through round 10 | Prior addressed/optional dispositions retained; none establishes new behavior or leaves an open source defect. R532-11-S1 is addressed above. |

**R533-12-R1 | RESIDUE | Docs | `docs/design/MAILBOX_SPLIT.md:294-297` | Historical lwSRP pin in the port paragraph.**

- Authority/evidence: the paragraph names `19f5796b63652eb1151906de73cb827d4980a53f`; the gitlink, `ctrl_arms.LWSRP_REV`, adapter README and verified dependency name `9197193e47a6bb1c45a56d90a18c1784123aba44`.
- Impact: inconsistent historical wording in the descriptive port paragraph. The executable pin check and acceptance result are already correct.
- Exact required outcome: replace `19f5796b63652eb1151906de73cb827d4980a53f` in that paragraph with `9197193e47a6bb1c45a56d90a18c1784123aba44`.
- Verification: compare with the gitlink and harness constant; rerun documentation checks. No measurement, figure, verdict, test, code, generated artifact, protocol/conformance or clause claim changes; no privacy rule is touched. Under the supplied owner rule this remains on the residue checklist without dirtying Docs.

**Reviewer-owned ledger.** Source-head coverage, not the manager's final merge-candidate ledger.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #665 scope/decisions; REQUIREMENTS.md:24-52; FR_NFR.md:333; pinned callback contracts; srp_mbx.c:79,159,424,562; real wire/withdrawal receipts | R533-12 | efea74858dffc482820d4f19c26c38796a57ff75 |
| RTL | CLEAN | Both merge parents; merge-audit.json; unchanged dev hdl/mailbox/GMII artifacts; ctrl_app_srp.c:51; srp_mbx.c:159,572,674; pinned mrp_mad.c:989 | R533-12 | efea74858dffc482820d4f19c26c38796a57ff75 |
| Robustness | CLEAN | srp_feedback.hpp:72,184,207,226; srp_mbx.c:337,446,674; IF=1/2 lifecycle, shared-binding, malformed-input, retry and sanitizer receipts | R533-12 | efea74858dffc482820d4f19c26c38796a57ff75 |
| Tests | CLEAN | srp_mutants.py:798,818-839; test_ctrl_firmware.py:202; fourteen named catches, original probes, 22-file coverage and public receipt audit | R533-12 | efea74858dffc482820d4f19c26c38796a57ff75 |
| Docs | CLEAN | srp/README.md:70,258; MAILBOX_SPLIT.md:715-757; current PR body; merged SUBMODULES.md and inspected PNG; builder/image receipts; R1 residue | R533-12 | efea74858dffc482820d4f19c26c38796a57ff75 |

**Real limits and pending manager duties.**

- This review applies public decisions and repository/pinned interface authorities. It does not claim a fresh complete reading of licensed IEEE/Milan editions. Recorded clause contracts and executable wire cases support the changed behavior.
- Full parent, processor, gPTP, synthesis and builder banks, complete historical mutations, fresh linked images and physical work were not run here. Manager-reported source-bank success and audited public receipts remain separate evidence. The assigned HDL compiler's release identity was checked; no HDL build was needed for this focused review.
- Physical calibration is NOT RUN. Field skips, host timing envelopes and linked fixtures are not hardware, boot, audio-soak or target-service proof. Live stream/MAAP configuration, fabric licence wiring, scheduling and call-chain stack bounds remain integration duties. PR #690 remains partial for #665.
- At the exact-head query, four hosted workflows existed and remained in progress. Executed successes included `docs-check-no-git`, `wire-accountability`, conformance, lint and three synthesis shards. `firmware-unit`, `docs-check`, elaboration and remaining long jobs were running. Physical gPTP was **skipped**, not executed. No completed `rtl-fast`/long-gate aggregate is claimed. `hosted-status.json` records that snapshot. Hosted acceptance and trusted local replication remain manager duties, including R532-8-F1's hosted requirement.
- Queried live dev remains `99e4eb6c14462aafa84bb1ac597fd241abc1a240`; reviewed source descends from it. The manager must bind validation to the then-current dev candidate, finish required hosted contexts, obtain both independent reviews with no round outstanding and explicit merge authorization, and perform post-merge containment. This source verdict does not complete those duties.
- The manager publishes the packet and carries R533-12-R1 to the residue checklist. This session made no source fix, commit, push, GitHub write or merge. Only REPORT.md and MANIFEST.sha256-listed files are publishable; scratch is excluded.

R533-12 FINISHED
