[R868] POSITIVE - exact head 9f4f3de03f99dc8c7a72f5f8884f00df82c965d2

R868-2, external independent delta review of PR #947 for #946 / #665. Tree `9bdd0b0644d75354b43767e8453db2dc3649ea8b`. All five lenses applied. No open BLOCKER, MAJOR or MINOR found in the reviewed scope. Two wording residues and one suggestion follow. This source verdict does not complete hardware acceptance or authorize merge.

The five commits after `66c6edf3` resolve the deferred-bind defect at its cause. A waiting change cannot be redone onto an AAF input with a monitor context while that input is bound, including before its probe settles. Kept changes write their contexts in the change callback. The per-pass writer is removed. The ROM ledger names the measured source points.

## Reconstruction and scope

Read the operating contract, CONTRIBUTING, documentation map, #946/#665 public scope, #665's ROM decision of 2026-11-15 (`issuecomment-6892332745`), requirements and interface authorities, then the source-base diff/history and five-commit delta. Source base: `cb96336d7aaacbaec76990ab07ef64148808d4ac`. Unchanged code was revisited where the delta depends on it, under the later-round rule.

The public prior-findings comments (`6990342205`, `6990669953`) were examined after the independent diff pass, for cause-level resolution. No current-round peer report or private author material was used. The published author packet is archive `c6fc4753b5b5892046ad9e3f92a4680cbf00f33c`, `review-evidence/946-r1/author-r2`. Public snapshots are retained in `public-state.json`.

Scope remains the split platform's interface-0 AAF inputs above zero. #948 tracks duplicate-SID fan-out, #949 the all-fabric zero-format defect, and #943 the output destination-MAC observation. These are not claimed fixed. Frozen hardware acceptance remains outstanding, not rewritten into simulation-only acceptance.

## Prior finding disposition

| Finding | Disposition at this head | Evidence |
|---|---|---|
| R868-1-F1, MAJOR, all five lenses | RESOLVED | `ctrl_plat.c:163` selects affected contexts; `:189` checks the waiting command against `acmp_view().bound`; `:203` writes kept changes. `aecp.c:906` consumes that result before another protocol event. S6-S10 cover settlement, unanswered probe, timeout, unbind/rebind and configuration. Independent clean, old-platform and refusal-plant receipts confirm the fix. |
| R867-1 F-1, MINOR, Docs/Tests | RESOLVED for source; specified composition action remains mandatory | `ctrl_memory.py:258`, `ctrl_memory_ledger.py` OWN/HELD/REFUSED, memory-test boundaries, `plat_ledger.py` POINTS/controls, boot SoC selection and SPLIT_CONTROL_MEMORY sections 3/5 agree. Source entries: 56.5 and 61.0. Public composition patch raises its own 8x8/2if to 63.0. |
| R867-1 F-2, MINOR, Tests/Robustness | RESOLVED by removal and direct idempotence checks | No `plat_poll` or owed flag remains. S5 checks unrelated changes and 100 idle passes; S2/S4 constrain writes to the affected context. Independent `sink-every-pass-rewrites.log` fails S5 on the prescribed words. |
| R867-1 F-3, MINOR, Docs/Conformance | RESOLVED | Public #948 and #949 exist, remain open, describe the separate causes and link #946/#665. Current PR limitations link both. |
| R868-1-R1 and R867-1 R-1, RESIDUE, Docs | RESOLVED | `sim_ctxfmt.cpp:5` now names the receive stack; `test_plat_sinks.cpp:6` names the saved-state flash model. New residue R1 below is separate. |

F1 is resolved in code, not deferred to another issue. The broader unchanged core behavior below is not substituted for its resolution.

## Findings and residue

### R868-2-R1 - RESIDUE - Docs

**Artifact:** `sw/litex/ctrl_memory.py:254`, newly added comment.

**Authority/evidence:** Owner source-comment rule of 2026-10-15 excludes work-lane names. The comment says `named debt owed to S14 (#665)`.

**Impact:** Wording only; ledger values, figures, debt record and requirement interpretation remain unchanged.

**Exact required outcome:** Replace this comment fragment with `named debt owed to the cold-code and descriptor flash migration (#665 decision D3)`. Keep the formal S14 debt identification in the ledger record and public documentation.

**Verification:** Comment-only diff; the three LEDGERED entries and their values remain identical. Docs stays clean.

### R868-2-R2 - RESIDUE - Docs

**Artifact:** PR #947 Description / Why it is race-free: `with no mailbox access between the change and the write`, also repeated in the author resolution narrative.

**Authority/evidence:** `ctrl_plat.c:207` forwards to the face change callback before writing contexts. `aecp_face.c:77` publishes through the mailbox; `ctrl_plat.c:208` may query applied state. Event-loop ordering should not be phrased as absence of mailbox accesses.

**Impact:** Imprecise interval wording. The checked invariant and conformance result do not change: during those accesses the affected input is unbound, the non-reentrant owner cannot deliver a competing bind, and the context is written before the final response. No test, figure, verdict or implementation needs changing.

**Exact required outcome:** Replace the phrase with `before returning to the event loop or sending the final response; face-publication mailbox accesses precede the context writes while the affected input is unbound`.

**Verification:** Compare to `sink_changed`, `publish` and the non-reentry contract in `aecp.h:156`. Preserve the published-SID/current-format/LCTX coherence claim. This clarifies wording, not the synchronization requirement.

### R868-2-S1 - SUGGESTION - Conformance, RTL, Robustness, Docs

**Artifacts:** `aecp.c:906`, `aecp_face.c:77`, `hdl/milan/milan_datapath.sv:4699`, PR Known limitations.

**Authority/evidence:** The original core retry does not revalidate every input/output's running state. The face can temporarily contain a value the core has undone. This wrapper covers the inputs whose monitor words this issue owns.

**Impact:** Broader deferred-command and audio-map consistency remain unqualified outside this fix. Those paths exist at the source base; no general retry-correctness or glitch-free audio claim is earned here.

**Suggested outcome:** Give the proposed broader core/face follow-up a public issue, with delayed-acknowledgement tests for input 0, CRF, outputs and channel-map behavior, and an explicit response-status/rollback contract.

**Verification:** Exercise its real consumers and affected service-budget images in that separate task. This suggestion neither postpones F1 nor changes this verdict.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #946 scope; REQUIREMENTS sections 1/3/8; REGISTER_MAP 0x800; Milan Table 5.6 / 4.4.2.2 and IEEE 1722.1 7.4.9/7.4.10/7.4.16/8.2 as cited; `ctrl_plat.c:163`; `aecp_commands.c:125`; `aecp.c:906`; clean/old-platform logs | R868-2 | 9f4f3de03f99dc8c7a72f5f8884f00df82c965d2 |
| RTL | CLEAN | `hdl/common/csr/milan_csr.sv:1117`, `:1665`, `:1888`; `KL_avtp_rx_monitor_ctx.sv:719`, `:1177`; `milan_datapath.sv:3768`, `:10025`; `aecp_face.c:77`; `tsn-c-stack/src/acmp.c:222`; published N=8 CF1-CF5/plant receipt | R868-2 | 9f4f3de03f99dc8c7a72f5f8884f00df82c965d2 |
| Robustness | CLEAN | `test_plat_sinks.cpp:203` observer and S3-S10; `sink_mutants.py:78`; `ctrl_plat.c:189`; clean, refusal and idle-rewrite logs; CF4/CF5 | R868-2 | 9f4f3de03f99dc8c7a72f5f8884f00df82c965d2 |
| Tests | CLEAN | `plat_arms.py:116`; `ctrl_mutants.py:948`; test_ctrl_firmware suite/coverage registration; ctrl_memory_ledger refusal/plant tables; `test_ctrl_memory.py:233`; plat_ledger controls; independent probes and hashed gate receipts | R868-2 | 9f4f3de03f99dc8c7a72f5f8884f00df82c965d2 |
| Docs | CLEAN, R1/R2 residue only | `plat/README.md:79`, `:83`, ROM/tests sections; SPLIT_CONTROL_MEMORY sections 3/5; public scope/ROM decisions; #948/#949; PR limitations; author-r2 RESOLUTIONS and 38-file audit | R868-2 | 9f4f3de03f99dc8c7a72f5f8884f00df82c965d2 |

The RTL lens covers the firmware's interaction with unchanged hardware. No product RTL, mailbox contract, AECP core/face source or gitlink changes in this delta. The test wrapper's N-dependent match index remains correct at N=4/N=8. The CSR holds pending writes until engine acceptance; selection restore cannot overtake FMT_HI. Nonzero contexts retain format across bind/unlock walks. Clock and crossing contracts are unchanged.

## Ordering, bounds and open points

Original dispatch refuses an already-bound input with STREAM_IS_RUNNING. During a deferred command the wrapper checks `bound`, not `settled`; neither a completed nor an unanswered probe enables redo while the input stays bound. If unbound again, redo and context writing finish in the same non-reentrant protocol turn before a later bind can publish a nonzero SID. At timeout the original format remains in force and the face receives it again. Identical-value writes during rollback do not change the format.

ENTITY_MISBEHAVING is the existing applied-failure timeout path (`aecp.h:180`, `aecp.c:906`, MAILBOX_SPLIT's firmware-writer contract). The change neither accepts a new format while bound nor reports false SUCCESS. S6-S8/S10 exercise the 100 ms failure path; S9 exercises redo after unbinding. This is acceptable for a command originally accepted while unbound, not a claim that the two statuses are interchangeable for ordinary dispatch.

The face's temporary F_FMT_IN copy is separate from the above-zero monitor comparator. It feeds the map channel limit (`milan_datapath.sv:4699`, `:4983`) and can differ until rollback publication. That existing exposure does not recreate the reviewed LCTX/current-format mismatch. Input 0 uses the face alias; CRF and outputs remain outside this writer. Their unchecked redo is unchanged core behavior, suitable for S1's separate task. No all-path audio guarantee or new acknowledgement semantics is inferred.

## Independent execution

`probe.py <checkout> <packet>` ran four focused jobs, at most three concurrent builds with four compilation workers each (12 total). Copies/builds stayed under `scratch/`; logs and exit statuses are separate.

| Run | Result | Receipts |
|---|---|---|
| Exact-head composition, 8x8/1if and 1x1/1if | 10/10 tests each; rc 0/0. S6-S10's 1x1 early-return cases do not prove races on a nonexistent context. | `clean.log`, `clean.rc` |
| Round-one ctrl_plat.c, current tests | rc 1; S4/S5/S6/S7/S10 fail by name. S6 reproduces `input 7: current 0205022000806000, context 0205022002006000`. | `old-platform.log`, `.rc` |
| Remove waiting-bound refusal | rc 1; prescribed S6 assertion catches it. | `sink-redo-refusal-skipped.log`, `.rc` |
| Rewrite contexts every pass | rc 1; prescribed S5 idle-pass assertion catches it. | `sink-every-pass-rewrites.log`, `.rc` |

The observer reads production published-binding state before every mailbox access. The stack updates that state before its publication callback (`acmp.c:233`), so the publication boundary is included. Successful format responses are checked against written words. No assertion was weakened. Old-code failures are completed test runs, not compilation failures.

## Published evidence

All 38 author-r2 files match the published SHA-256 manifest (`integrity-and-provenance.log`). This proves archive-byte identity. The archive commit has no signature (`N`); no detached signature was supplied, so signer authentication is not claimed.

Source firmware/coverage/ledger receipts at `548324b5` carry: the sole later change rewraps a Python docstring. Memory, docs and source boot receipts name the exact head. N=8 receipts at `0f6c12ba` carry because their inputs do not change afterward. Relevant result, failure, skip and control sections were checked; summary receipts are not represented as complete raw execution traces.

| Evidence | Result and interpretation |
|---|---|
| Firmware/plants | Source: 75 passing verdicts, 743 control and 729 AECP/SRP plants caught. Composition: 74, 823 and 875. All 26 sink plants caught by named assertions. Arm counts are separate from plant counts; round one's inflated totals are corrected publicly. |
| Coverage | Both PASS; changed platform C files report 100% lines/branches after declared exclusions. Not a state-space proof. |
| N=8 monitor | 96 checks, zero failures; four plants plus clean control 5/5. CF4 checks the first PDU after binding with the format written the preceding cycle. Carried evidence, not rerun here. |
| Sweep | Composition 65/65 suites, 2,713,122 checks, zero in-suite failures. Four external-generator/freshness skips remain skips. |
| Twin | Source and base share `split-talker-failed`, equal published capture hashes and the `srp-plus-k` escape. Composition: zero findings, all plants refused. The source escape is not called PASS. |
| ROM | Source points 43.5/44.0/56.5/61.0 RAMB36; 8/8 controls. Composition 45.0/46.0/58.0/63.0; 9/9 controls. Source 8x8 ROM 131,656/133,224 B; composition 138,624/140,200 B. Both memory-test receipts: zero failures. |
| Boot | Source 8x8 PASS, 65.775 ms. Composition 8x8 67.328 vs train 67.134 ms: +19,467 cycles, 28 stores, seven context pairs. Composition 1x1 27.936 vs 27.981 ms, no context stores. Well within 20,000 ms; not steady-state CPU measurements. |
| CPU images | Composition equals recorded train hashes: 1x1 `55484254e638ed7f05ada7c8d6e36fd18791d42d0a45d2c5f7f2bf0d30516e58`; 8x8/1if `175418f4b5b1a9d463607792be769c1c8f7cc9c612cc1b0f970c6179a8e14093`. Those fixtures do not link this product wrapper. Existing rows carry; no new product runtime measurement is inferred. |
| Docs | Source applicable steps pass; five train-only steps are distinguished. Composition 97/97. |

Composition receipts name `d98dd322`, tree `21a39a5cd3bf862599ba16828e2db9a0d7bfdaf8`, and a repeat at the exact source head yielding that tree. Seven ROM-related files conflict with the earlier train. The documented recipe takes the train's ledger files, preserves non-ROM README changes, then applies the 63.0 patch. This is an author-tested earlier-train composition, not the current-dev candidate.

All-fabric firmware/RTL are outside the functional diff; the memory changes affect split planning (`milan_soc.py:3715`). This supports unchanged release behavior. Author-r2 supplies neither paired release bytes nor paired ELF/bitstream hashes; no release build was authorized here. Actual release-image byte identity is unverified by artifact comparison and must not be promoted from input-scope reasoning to a measured result.

## Limits and pending manager duties

No manager source bank exists at this head and none is inferred. Full parent, processor, gPTP, portability and builder banks were not run. Hosted contexts and local workflow replication were not inspected/run; acceptance belongs to the manager. No hardware, calibration, field campaigns, power cycles or soak ran. Physical calibration is NOT RUN. Firmware and monitor tests demonstrate two halves of a contract, not end-to-end hardware behavior.

Full standards texts were unavailable in the clone. As in round one, clause checks use frozen cited requirements and repository authorities, without substituting another edition. This delta verdict does not certify general Milan compliance, multi-configuration operation or interface-1 media placement.

The source product SoC still defaults to an unoverridden 56-tile limit, explicitly documented; its 8x8 product build needs the train's own-point selection. Approval is for this source as the documented train component, not a standalone dev-soft-core shipping image.

The manager must preserve the composed ROM entries, validate the actual candidate against current dev `e275d7950ef3385753e6a15d2e191ba855b171ed`, publish builder/native receipts, and complete protected hosted/local-workflow acceptance. Obtain paired release artifact hashes before asserting measured byte identity. Carry R1/R2 to the residue checklist and consider S1. Complete frozen 8x8/1if stream, power-cycle and soak acceptance before declaring #946 done. Two positive independent reviews, no review in flight, explicit merge authorization, containment and project closure remain separate requirements.

Final integrity: 1,632 source blobs and all five required initialized submodules match exact committed raw bytes, executable/symlink modes and index records. Submodule HEADs match gitlinks. Optional `external` stays uninitialized with its gitlink unchanged. Source status is clean. Every probe completed; no source fix, commit, push, GitHub write, contact or merge occurred. Publish only REPORT.md and manifest-listed files; scratch is excluded.

R868-2 FINISHED
