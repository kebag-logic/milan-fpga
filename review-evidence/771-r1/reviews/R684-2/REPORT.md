[R684] POSITIVE - exact head 1098978f4a931a667e147b68a791520eb141c917

Round R684-2, external independent source review of issue #771 / PR #772. All five lenses are CLEAN. R684-1-F1 and R683-1-F1/F2/F3 are resolved at this head. No open BLOCKER, MAJOR or MINOR remains in the assigned delta. The retained RESIDUE and optional SUGGESTION below do not clear or waive any pending merge gate.

Reviewed tree: `cad31d5084366583e8cd18c46e71ca6277c5d825`. Source base: `d77a8afdbc960d70d1ceeee9af1163624f102b16`. Previous reviewed head: `a97aea01449492b1f640924f5a34726f602cabed`. The three delta commits are `b6fc1590ca63bb5f851a17b9bda7d15a9d790c4d`, `bbdd24d00661007da6ae7c902402bd927e9fe814`, and the reviewed head. This is not validation of a future current-dev merge candidate.

## Scope and evidence

Reconstructed the operating contract, documentation map, [frozen acceptance](https://github.com/kebag-logic/milan-fpga/issues/771), public assignment/STOP/area decision, requirements and affected interface authorities before assessing the source delta. Read the [round-2 assignment](https://github.com/kebag-logic/milan-fpga/pull/772#issuecomment-6342664760) in full. The base-to-head diff and history establish the adoption context; this later round judges the three new commits and every named prior finding at its cause. Unchanged artifacts retain their prior reviewed results. No private author material or other current-round report was used. The independent verdict and ledger were written before reconciling the prior public reviews.

The public evidence source is [archive b6d9eaa](https://github.com/kebag-logic/milan-fpga/tree/b6d9eaa187cb2c43548e22e7adae21b35b539107/review-evidence/771-r1). All 44 original author and 196 round-2 author files in its publication manifest match their published SHA-256 values. Redacted publication hashes were checked, not substituted with original private-file hashes. The full firmware log is the published text version, `author-r2/round2/firmware-gates/text/ctrl_firmware.log`: 316,446 bytes, SHA-256 `0316e30263902dbfa140a4e1e9a209f9fdc79f509800581b6b0b9c15e08b8b86`, matching the summary's original text digest. The archive commit has no signature header; these checks establish immutable-object and receipt integrity, not a verified cryptographic signer. No separate signature was supplied in the inspected author packet.

## Prior findings resolved

**R684-1-F1 (MAJOR; Conformance, Robustness, Tests, Docs) and R683-1-F1 (BLOCKER; Conformance, Tests, Docs): RESOLVED at this head for the source review.**

- The public assignment explicitly authorizes case (a) if production already implements the behavior. `sw/firmware/ctrl/app/ctrl_app_srp.c:90-100` sends a first registration to `acmp_tk_registered` and a settled kind change to `acmp_tk_kind_changed`. The latter, `third_party/tsn-c-stack/src/acmp.c:1176-1187`, requires SETTLED_RSV_OK, updates `tk_failed`, and calls `finish()` without a state transition. The view includes REGISTERING_FAILED (`:431-448`); `finish()` compares it and issues the change callback (`:495-515`); GET_RX_STATE reports the kind (`:891-892`). This establishes the cause as the test adapter, not a production-core discrepancy.
- `sw/firmware/ctrl/test/acmp_walk.cpp:258-261` now maps the already-settled stimulus to that same API. The imported processor model, its pinned extraction, and the walk's Table 5.22 comparison at `:180-201,496-497` are unchanged. It neither skips the cell nor normalizes away the result. The prior model/stack gitlinks are unchanged throughout round 2.
- Independent focused rerun: **127 checks, 0 failures**, matching the published log byte for byte. The published previous-head run is **127/1**, with the expected registered-state and notification failures.
- Independently planted both defects using the campaign's `plant()` and named `caught()` checks. `acmp-kind-lost` is killed by `AcmpCore.KindChangesOnlyTheSettledView` and walk `TK_REG_SOK`'s registered-state check. `acmp-kind-not-notified` is killed by the core's notification check and the walk's Table 5.22 notification check. The latter is the walk's only failed assertion for the notification-only defect. The first control existed previously; this delta adds its walk kill. The notification-only control is new.
- Production-path evidence was inspected separately, not inferred from the walk. The archived `probe_production.py` composes the real application/SRP/ACMP implementations with mailbox MSRP vectors and GET_RX_STATE wire responses. Its small test-only diff arms and checks a consumed CHANGED callback on both swap directions. At one and two interfaces, each clean run passes **19/0**; dropping the production glue call fails state, wire and notification checks; pre-marking the stack view as reported fails only the notification checks. The callback is checked before the subsequent GET_RX_STATE traffic, so later traffic cannot manufacture this pass. This is host-model integration evidence, not hardware evidence.
- The assigned complete local firmware block ran and passes in the public receipts, as detailed below. The PR now acknowledges the previous omission and lists what actually ran. Hosted acceptance remains a manager duty, distinct from resolving the adapter cause and local evidence gap.

**R683-1-F2 (MINOR; Docs, Conformance): RESOLVED.** `docs/reference/REGISTER_MAP.md:1480-1486`, `docs/reference/SUBMODULES.md:244`, and `CHANGELOG.md:73-77` state the first-eight/count-eight/no-thisClock behavior for eight or more received entries. This agrees with `gptp-processor/hdl/top/KL_gptp_engine.sv:714-730,981-991` and the unchanged maximum-path checks in `tb/verilator/gptp_shadow/sim_main.cpp:950-955` and `tb/verilator/milan_dp/sim_gptp.cpp:1497-1527`. The bound is disclosed where the contract is stated.

**R683-1-F3 (MINOR; Docs, RTL): RESOLVED.** The five requested locations now distinguish absent count zero, self `{thisClock}` count one before a peer, and an explicit received `[GM]` path publishing count two: `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:635-644`, `hdl/milan/milan_datapath.sv:2153-2162`, `hdl/milan/KL_pp_shadow.sv:456-466`, `README.md:170-177`, and `docs/reference/REGISTER_MAP.md:334-339`. The comments cite donor #82/#85. Removing whole-line comments makes each of the three RTL files byte-identical to its prior reviewed version. There is no new logic, timing, clock/reset, CDC, port-width or state change in this round.

## Gate claims checked

The source-head evidence is the author's published receipts. No manager source bank exists at this head and none is inferred.

| Evidence at 1098978f | Checked result and limitation |
|---|---|
| Verified RV32 SDK | Install/verify receipts identify the pinned Bootlin archive `d42680e9...`, GCC 14.3.0, compiler `.br_real` digest `f2f6ec09...`; the gate environment selects that compiler and records clean exact head before/after. The receipt is evidence of the author's installation, not a reviewer reinstallation. |
| `test_ctrl_firmware.py --require-rv32 --self-test --lwsrp ... --jobs 4` | Full text log independently recounted: 66 arm tallies, 1,593 checks, zero failures; 521/521 control mutants, including both named ACMP controls; 358 subsequent AECP/SRP campaign catches; PASS. |
| Remaining assigned firmware block | Tally listener 18/18 defect catches; saved-state 435 tests and 109/109 catches; coverage self-test 29/29 and coverage check PASS for 30 files; boundary self-test PASS with 0 findings and 0 misbehaved controls. RV32 self-test and shard census also return 0. |
| Boundary rerun | Initial host-interpreter run returns 2 because required builder dependencies are missing. The separately identified interpreter run returns 0 at the same clean head. The successful log records all required builders and host/RV32 compilation. It does not claim every image link succeeded: the boundary gate explicitly records expected stopped-at-link image arms. |
| Firmware workflow census | Returns 1, explicitly disclosed. Archived head and dev-input output are byte-identical, and its workflow/census inputs are outside this delta. It is not counted as passing or as one of the assigned block's six commands. Carry the existing discrepancy to a public follow-up; do not erase it from the evidence. |
| Parent source suites | 63/63, 2,189,520 checks, zero failures/timeouts; named gPTP legs remain included. Separate physical-rate simulation: 209/0. These are inspected author results, not full-bank reviewer reruns. |
| Other source gates | Yosys 58/58, no unjustified tied inputs and tap-purity PASS; behave 406 scenarios; xvlog zero findings; required quick-gate receipts return 0. |
| Local docs workflow replica | 44 step records: 42 executed with rc 0, two explicit skips. Builder leg 1 has a separate successful interpreter rerun. Neither a skipped no-git deletion step nor the skipped candidate host-runner step is represented as an executed pass. |
| Saved-state capture | Independent `check_nvm_capture.py` passes, including its adverse controls. Shipping source `sw/firmware/milan_baremetal/milan_baremetal.c` remains SHA-256 `497845e6243b919638285ce4de18e6687beff6a509d72c8e2e2f2d45ba7b1bed`, byte-identical to source base. No remeasurement is required; retained maximum 13.86328 ms is below 24.5 ms. |

Acceptance 1 remains satisfied by the exact donor gitlinks, unchanged in round 2: processor `93fb0b2d736b36588ea7321e25fba2f8819ea41f`, gPTP `55680bff3b287b9a7b0c759f51471fa617c17335`. Acceptance 2's resource re-baseline and image evidence retain the prior reviewed disposition under the [owner area exception](https://github.com/kebag-logic/milan-fpga/issues/771#issuecomment-6333175429): route/ooc growth was accepted, not made compliant with the old tolerance. This test/comment delta changes no implemented behavior or bitstream. Source validation for acceptance 4 is now evidenced by the listed receipts; final hosted and candidate acceptance is pending. Acceptance 5 is explicitly post-merge work.

## Retained and wording findings

**R683-1-R1 — RESIDUE — RTL, Docs — `hdl/milan/KL_pp_shadow.sv:1281-1282` — retained unchanged.**

Authority/evidence: the prior public comment-rule finding identifies “scratch only:” as consumer-bank provenance in the shipping connection's comment. The round-2 delta does not edit those lines. Impact: misleading wording only; no declaration or measurement changes. Required exact wording:

```text
//! processor issue #190: one MaxFrameSize per talker source; every slot is
//! driven with this wrapper's one value, so each declaration is unchanged
```

Verification: comment-only diff and unchanged connection expression. The manager carries this to the residue checklist. No new source-comment lane, review-round, reviewer-ID or issue-comment-ID residue was found in the round-2 additions.

**R683-1-S1 — SUGGESTION — Tests, Robustness — retained, optional.**

Artifacts: `tb/verilator/milan_dp/Makefile:386`, `tb/verilator/pp_shadow/Makefile:137`, `tb/verilator/capture_coherence/Makefile:122`, `tb/verilator/milan_dp_mclk/Makefile:107`, `tb/verilator/milan_dp_render/Makefile:152`. Authority/evidence: these unchanged `ucode.hex` rules depend on the generator, while the adopted generator also reads `aecp_commands.json` and `aecp_fields.json`. Impact: a later JSON-only change can leave an incremental ROM stale; fresh source builds are unaffected. Suggested outcome: add both JSON prerequisites. Verification: changing either prerequisite causes ROM regeneration. The author did not take this optional suggestion; it does not invalidate current clean-build evidence.

**R684-2-R1 — RESIDUE — Docs — PR #772, “Linked Issue / roles”.**

Authority/evidence: that section still shows `[R<n>]` placeholders despite the public review-start notices naming the assigned reviewers. Impact: redundant role information is stale; public assignments and review identity remain unambiguous. Exact fix: replace the internal placeholder with `[R683]` and the external placeholder with `[R684]`. Verification: compare that section with the two round-2 start notices. This affects no result, clause claim or privacy rule.

## Reviewer-owned ledger

All five lenses were applied to the delta, its dependencies and the prior causes. The untouched adoption scope retains its prior verdict; this table banks the corrected and inspected scope at the current head.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #771 and round-2 assignment; `sw/firmware/ctrl/app/ctrl_app_srp.c:90-100`; `third_party/tsn-c-stack/src/acmp.c:1176-1187`; `docs/reference/REGISTER_MAP.md:1469-1486`; public production probe | R684-2 | 1098978f4a931a667e147b68a791520eb141c917 |
| RTL | CLEAN | Three whole-line-comment-only RTL diffs; `gptp-processor/hdl/top/KL_gptp_engine.sv:714-730,981-991`; `receipts/delta.txt`; exact gitlinks and integrity receipts | R684-2 | 1098978f4a931a667e147b68a791520eb141c917 |
| Robustness | CLEAN | `third_party/tsn-c-stack/tests/test_acmp.cpp:786-813` (both swap directions, idempotence, invalid state/sink); `sw/firmware/ctrl/test/srp_feedback.hpp:53-110`; both independent fault controls; maximum-path contract | R684-2 | 1098978f4a931a667e147b68a791520eb141c917 |
| Tests | CLEAN | `sw/firmware/ctrl/test/acmp_walk.cpp:180-201,258-261,475-497`; `acmp_mutants.py:372-382`; clean 127/0 and named core/walk kills; full published firmware text log and required block receipts | R684-2 | 1098978f4a931a667e147b68a791520eb141c917 |
| Docs | CLEAN | Five count contracts and three bound descriptions listed above; `receipts/pr-body.json`; public manifests, SDK and gate logs; explicit skipped/refused-run accounting | R684-2 | 1098978f4a931a667e147b68a791520eb141c917 |

## Limits and pending manager duties

- No full parent, donor, Yosys or builder bank was rerun by this reviewer. The independent executions were the bounded ACMP walk/core controls, capture checker and integrity/delta/receipt audits. The production-path probe and complete gate totals are inspected published evidence. No current-head hosted job execution or acceptance is claimed by this report.
- The manager owns hosted/act acceptance, the second independent positive review and completion ledger, and the final current-dev merge candidate's builder/native banks. Source base/live dev was `d77a8afdbc960d70d1ceeee9af1163624f102b16` at assignment; verify the actual live tip at the merge turn. Publish candidate receipts, obtain maintainer merge authorization and finish containment before Done.
- Preserve the disclosed 8x8 exception share (+2,185 LUT/+769 FF over dev) and reduced image-build thread counts in the manager's acceptance record. The owner accepted the adoption's area; neither figure is a pass against the former baseline. Mark II #640 owns recovery.
- Carry the known firmware-census discrepancy to a public follow-up. Preserve the CRF-specific MaxFrameSize parent work when closing donor #190; closure of the adoption must not lose that unfinished item. Retain the optional Makefile suggestion and comment residue with their existing classifications.
- Physical calibration **NOT RUN**. Physical-rate simulation, software field campaigns and field/calibration skips are not hardware proof. Post-merge DUT identity, #637 cold power-cycle/audio-map checks, all-stream/counter soak and the named donor-issue closures remain pending. Release qualification #76 follows #770.

Final integrity verification hashes every tracked blob directly, checks executable/symlink modes and the full index against the tree, and verifies all five required initialized submodule heads/bytes/modes/indexes. It passes for 1,423 parent blobs and 703/107/98/214/65 submodule blobs. The unused external submodule remains uninitialized. No tracked source change, commit, push, GitHub write, merge or hardware operation was made. All probe trees are under this packet's excluded `scratch/` directory.

`REPRODUCE.md` maps the portable scripts and receipts. `MANIFEST.sha256` lists every publishable file; `receipts/public-sources.json` anchors copied public evidence to its immutable source.

R684-2 FINISHED
