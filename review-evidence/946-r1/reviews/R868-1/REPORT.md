[R868] NEGATIVE - exact head 66c6edf3f0d05915ee8ddb7346302013833cf66a

R868-1: external independent review of PR #947 for #946 / #665. Tree `a37bcaecd8c7761f5da29b47b805dbe84bc39ae9`. All five lenses applied. One MAJOR remains open; one wording residue is non-blocking. This is a source review, not merge authorization or hardware qualification.

The ordinary boot and acknowledged-change paths fix the reported zero-format failure. The delayed-acknowledgement path, however, permits a new binding to settle before the format update finishes. The context writer relies on an unbound-input invariant the composed firmware does not enforce.

## Findings

### R868-1-F1 - MAJOR - Conformance, RTL, Robustness, Tests, Docs

**Artifact:** `sw/firmware/ctrl/plat/ctrl_plat.c:178` and `:193`; related `sw/firmware/ctrl/aecp/aecp.c:906`, `sw/firmware/ctrl/app/ctrl_app_aecp.c:10`, `third_party/tsn-c-stack/src/acmp.c:883`; missing interleaving in `sw/firmware/ctrl/test/test_plat_sinks.cpp:443`; incorrect invariant at `sw/firmware/ctrl/plat/README.md:86` and `ctrl_plat.c:140`.

**Title:** A bind can settle during IN_PROGRESS, leaving its published stream active while current format and LCTX disagree.

**Authority/evidence:** #946's race-free scope; Milan v1.2 Table 5.6 / 4.4.2.2; the SET/GET_STREAM_FORMAT and binding contracts, IEEE 1722.1-2021 7.4.9 / 7.4.10 and 8.2; AGENTS.md section 6. The bound-input refusal checks binding at the original dispatch. A deferred command later swaps its saved change back in without repeating that check. ACMP reads the entity lock; a pending format change does not prevent BIND_RX or its probe response. The new writer supplies no serialization with that binding.

The reviewer probe uses unchanged production firmware with one additional host-composition test. It sends SET_STREAM_FORMAT for input 7, holds acknowledgement until IN_PROGRESS, sends BIND_RX, answers the actual emitted PROBE_TX with its sequence number, waits for settlement, then acknowledges the face:

```text
STALE: bound=1 published_sid=5544332211002233 current=0205022000806000 LCTX=0205022002006000
PROBE: input=7 bound=1 settled=1 final_status=0 old=0205022002006000 current=0205022000806000 window=0205022000806000
```

Three mailbox reads observe the new current format while the settled binding remains published and LCTX holds the old format. Eventually LCTX catches up and SET_STREAM_FORMAT returns SUCCESS. The original five tests pass in the same run; the added named coherence assertion fails, exit 1. Receipts: `deferred-bind.log`, `deferred_bind.cpp`, `probe_deferred_bind.py`. The observer only reads state and does not alter firmware behavior.

**Impact:** The documented statement that formats move only while unbound is false. During the observed interval a PDU for the published binding may encounter the previous channel count. The unchanged monitor compares against those words (`KL_avtp_rx_monitor_ctx.sv:1001` / `:1011`); consequently a PDU matching the new current format can be discarded as UNSUPPORTED_FORMAT. That packet consequence follows from the independently exercised RTL comparator. The probe does not claim to have measured the transient on hardware or in combined CPU/datapath simulation. Write arbitration prevents a lost write, but does not provide binding/format atomicity.

**Required outcome:** Serialize pending format transitions with bind/settle publication, or demonstrate another ordering that keeps active binding, current format and monitor context coherent. Preserve bounded responses, timeout rollback and the mailbox contract. Correct the documented race argument. Retaining only the initial bound-input refusal, or moving this finding to another issue, does not resolve it.

**Verification:** Add delayed acknowledgement plus bind plus successful probe, including timeout and rebind variants. Check coherence while a nonzero SID is published and exercise the first matching PDU at that boundary. Existing S2 binds before a later command; S4 has no competing bind and waits 20 extra passes before checking. Neither covers this order. Re-run the firmware and engine plants after the fix.

All five lenses apply: protocol/current-format correctness; firmware/datapath ordering; delayed acknowledgement with concurrent traffic; missing cross-protocol test; and a new false documentation claim. The documentation defect is substantive, not RESIDUE.

### R868-1-R1 - RESIDUE - Docs

**Artifacts:** `tb/verilator/avtp_rxmon/sim_ctxfmt.cpp:5`, `sw/firmware/ctrl/test/test_plat_sinks.cpp:6`.

**Authority/evidence:** Supplied owner source-comment rule, 2026-10-15: behavior/reason and issue/requirement identifiers, without lane names. New comments say `lane-A stack` and `F1's flash model`.

**Impact:** Wording only; no code, measurement, verdict, clause interpretation or privacy change.

**Exact fix:** Replace `the lane-A stack of avtp_rxmon_nx_wrap` with `the receive stack of avtp_rxmon_nx_wrap`; replace `F1's flash` with `the saved-state flash`. Keep module names and #946/clause references.

**Verification:** Inspect the added lines and confirm a comment-only diff. This residue does not itself leave a lens unclean.

## Reviewer-owned ledger

Reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README.md, frozen issue/public decisions, requirements and interface authorities, then the entire 15-file diff and six one-line commits from `cb96336d`, then public executable evidence at `7bb94e82746cfb8f2a29c5b2b880a528dcbb3764`. No private author material or other review report informed this verdict. Relevant public scope is retained in `public-scope.json`.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN, F1 | #946 body/scope; REQUIREMENTS.md sections 1/3/8; REGISTER_MAP.md 0x800; MAILBOX_SPLIT.md publication/face contracts; ctrl_plat.c:158; aecp_commands.c:125/:180; deferred-bind.log | R868-1 applied; no clean covering round | 66c6edf3f0d05915ee8ddb7346302013833cf66a |
| RTL | UNCLEAN, F1 | milan_csr.sv:1117/:1665/:1888; KL_avtp_rx_monitor_ctx.sv:617/:719/:1001/:1177; milan_datapath.sv:7855/:9995; milan_soc.py:802; N=8 RTL logs | R868-1 applied; no clean covering round | 66c6edf3f0d05915ee8ddb7346302013833cf66a |
| Robustness | UNCLEAN, F1 | ctrl_plat_csr.c:70/:92; C5/C6 and S1-S5; aecp.c:906; ctrl_loop.c; CF1-CF5; deferred-bind.log | R868-1 applied; no clean covering round | 66c6edf3f0d05915ee8ddb7346302013833cf66a |
| Tests | UNCLEAN, F1 | plat_arms.py:116; sink_mutants.py; ctrl_mutants.py; test_ctrl_firmware.py; ctxfmt_mutants.py; sim_ctxfmt.cpp; measure_test_evidence_readers.py:91; baseline/plant/old-platform/ordering receipts | R868-1 applied; no clean covering round | 66c6edf3f0d05915ee8ddb7346302013833cf66a |
| Docs | UNCLEAN, F1; R1 non-blocking | platform README ports/tests; issue acceptance; PR body; public handoff and 40-file archive manifest; boot/budget/ROM/twin/sweep receipts; new source comments | R868-1 applied; no clean covering round | 66c6edf3f0d05915ee8ddb7346302013833cf66a |

## Independent checks

- Platform CSR/console: 12 tests plus two MMIO tests pass. Sink composition: five tests at 8x8/1if and five at 1x1/1if pass. All 19 firmware plants are caught by their prescribed assertions, including every additional kill listed in the table. See `firmware-summary.log`, `firmware-*.log`, `plant-*.log`.
- Base `cb96336d` platform orchestration was compiled with new tests and the new, uncalled helper API. S1, S2, S4 and S5 fail by name; S1 names all seven unwritten inputs. S3 passes. This is executable old behavior, not a compile-failure claim (`old-platform.log`).
- Pinned RTL compiler identity: version 5.050, revision v5.050. N=8 CF1-CF5: 96 checks, zero failures. All four exact engine plants fail the prescribed named checks; clean control passes (`rtl-summary.log`, `rtl-clean.log`, `rtl-plant*.log`). No existing assertion was removed or weakened. Wrapper match index becomes three bits at N=8 and stays two at N=4.
- Firmware and RTL campaigns ran concurrently with eight compiler jobs each, within 16 total. Every process completed before finalization. Generated trees and objects are under `scratch/`; scripts accept repository and packet paths.

Architecture checks: words 2/3 decode to the selected listener. Stream 0 stays excluded and uses `fmt0_i`; CRF stays excluded with its separate receiver. The descriptor filter rejects short descriptors and other types/interfaces/configurations. Selection is saved/restored. Engine writes have priority; CSR holds external requests and blocks the following selection write until FMT_HI is accepted. CSR and monitor share the datapath domain; CPU accesses use the existing ordered AXI-Lite crossing. No mailbox ABI, product RTL, AECP-face source or submodule pin changes. Unbind/silence-unlock preserve nonzero contexts' formats. These correct mechanisms do not resolve F1.

## Train and evidence assessment

- **Composition:** independent `git merge-tree --write-tree b1f1161b HEAD` succeeds, tree `74c60aaa301c2db41f3b5e1af7396fbb87bc2178`. This proves textual composition onto #945's identified head, not validation against current dev or runtime correctness.
- **Release:** specified all-fabric input scopes hash identically across source-base/head and train/composition. SHA-256 respectively: `4e3c6c4358bf3b4025136dff2f010c3344f0f628ec76266715452ae6864906a8` and `9bcdc5e581fba88e28ea7775dcf5a3b21fd36945b57a2a3f8539f379129a4f9d`. The packet provides no paired release ELF/bitstream bytes or artifact hashes. Actual release-image byte identity was **not independently verified by artifact hash**; input identity is not that measurement. The unchanged all-fabric zero-format defect also remains outside this split-only fix.
- **CPU rows:** public `budget/image-hashes-arm-a.txt` records 1x1 `55484254e638ed7f05ada7c8d6e36fd18791d42d0a45d2c5f7f2bf0d30516e58`, 8x8/1if `175418f4b5b1a9d463607792be769c1c8f7cc9c612cc1b0f970c6179a8e14093`, equal to the recorded train images. Independent budget-input hashes match (`identity.log`). This carries existing fixture rows only: those images do not link the changed platform wrapper. No new production runtime-service measurement is claimed.
- **Boot:** author receipt gives 6,724,060 cycles / 67.241 ms against 6,713,381 / 67.134 ms: +10,679 cycles / 0.10679 ms, within the 20,000 ms boot bound. Seven contexts add 28 stores; logged write span is 2,858 cycles / 28.58 us at 100 MHz. At 1x1: +4,160 cycles / 0.0416 ms, no context writes. UART spans/first-byte delays stay inside the receipt's 500 ms / 20 ms limits. Boot measurements do not establish every steady-state service bound.
- **ROM:** public receipts show source 8x8/1if 56 -> 56.5 RAMB36 (ROM 131,464 bytes), train 8x8/2if 62.5 -> 63.0 (140,008 bytes). The public owner decision of 2026-11-15 permits these entry overruns as S14 debt, while retaining device fit/timing gates. The train's 63.0 ledger entry remains to be recorded. Ledger failures are not treated as passes. No route or physical timing run was performed here.
- **F-G2/F-G3:** parser `avtp_stream_parser.sv:193` chooses the highest matching enabled entry, so two equal SIDs do not fan out: a separate structural cause. F-G3 matches open #943's public GSI/MAAP defect and unchanged wiring. Neither is claimed fixed.
- **Published banks:** author reports source 75 passing firmware verdicts / 1,546 caught plants; composition 74 / 1,778. Coverage reports 100% for changed files after declared exclusions. Composition sweep: 65 suites, 2,713,122 checks. Four external-generator/freshness skips are not field validation. Source twin's `split-talker-failed` also occurs at base with matching capture hashes; train twin reports zero. These are author receipts, not reviewer full-bank reruns.
- **Provenance:** all 40 published file hashes match the archive manifest. Source executable receipts at `0749e0d8` carry because only two README lines change afterward. Composition executable receipts are attributed by the author to `8dbd0a48`, boot/size to `b180fda5`, final scratch composition to `d6d71354`. None is substituted for a manager-validated current-dev candidate.

## Prior public findings

After writing this independent verdict and ledger, the PR discussion, submitted reviews and inline review threads were read. They contain only two review-start comments, zero submitted reviews and zero inline threads. No prior public finding was present to resolve or retain (`prior-findings.json`). This says nothing about the other review still in flight.

## Limits and pending duties

No manager source bank exists at this head and none is inferred. Full parent/processor/gPTP/builder/portability banks were not run here. Hosted/local-workflow acceptance, hardware, physical calibration, field campaigns, power cycles and soak were not performed. Full standards documents were unavailable in this clone; clause checks used the frozen public task's cited statements and repository requirements/interfaces. No substitute standards edition was treated as authority.

The manager must obtain a fix and fresh independent review for F1, carry R1 to the residue checklist, record train ROM debt, and validate the actual current-dev merge candidate with builder/native receipts and protected hosted/local-workflow acceptance. Obtain paired release-artifact hashes before asserting image byte identity. Reassess CPU-row carry if the fix changes budget inputs. Frozen 8x8/1if hardware stream, power-cycle and soak criteria remain outstanding. Final candidate validation, two positive independent reviews, explicit merge authorization, containment, issue closure and project completion remain pending.

Integrity audit: every tracked blob's raw bytes and executable/symlink mode matches the exact tree; index matches; all five required initialized submodules match their gitlinks and tracked bytes/modes/index. Probes never edited checkout source. See `identity.log`. Only manifest-listed receipts and REPORT.md are publishable; disposable trees and unredacted build logs remain under `scratch/`.

R868-1 FINISHED
