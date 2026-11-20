[R866] NEGATIVE - exact head 8dc8588471a096bbe120bbec4c8c0f8ddf44d8cd

External independent composition review, R866-4, PR #945. Tree `22335ec4d79d67a5b9a2e0e7ab480fd868be9bba`. All five lenses were applied. One MINOR evidence finding remains open under Tests and Docs. No functional defect was identified in the composition fixes. Wording residues and inherited optional suggestions are also recorded below.

## Scope and independence

The full `cb96336d..8dc85884` diff and history were acquired. The technical review concentrated on `0839453f..8dc85884`, its dependencies, and the named earlier findings. Unchanged code retains the earlier composition coverage; the constituent PR implementations were not re-reviewed. The independent verdict and five-lens ledger were written before reading prior public reviewer reports. No private author material or another checkout was used.

Context was reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the sixteen assigned issue bodies and public decisions, REQUIREMENTS.md, FR_NFR.md, MAILBOX_SPLIT.md, SAVED_STATE_MATERIALIZATION.md, SPLIT_CONTROL_MEMORY.md, the source interfaces, and then the diff and executable evidence. Clause application follows the repository's authorities for Milan v1.2 5.4.2.7/5.4.2.28, IEEE 1722.1-2021 SET_STREAM_FORMAT, and IEEE 802.1Q clause 35/10.7. The SRP composition fix is assessed as behavioral equivalence against the pinned library; it does not adopt a new protocol interpretation.

Key public decisions are [the SRP cut and notice-cost ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-7029526172), [the owner's subsequent item-4 exception](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-7044585511), #894's slice/queued rules, #818's setup/hold floor, and the owner's ROM-as-S14-debt ruling. The later owner exception governs the earlier condition that rows already hold; no owner bound moves.

All `receipts/`, CPU-table and handoff references below are relative to [author-r6 in archive 563c16e5](https://github.com/kebag-logic/milan-fpga/tree/563c16e5f62152a2ff1c9722e23208e1fbad0e88/review-evidence/train1117-r1/author-r6). Every one of its 3,693 files matches the published SHA-256 manifest. The archive commit is unsigned: this verifies contents against the published manifest, not signer authentication. Large original logs are sometimes represented by digest/tail stubs; I have not represented those as complete raw traces.

## Open finding

### R866-4-F1 — MINOR — Tests, Docs — missing public loaded-image comparison

**Artifact:** `HANDOFF-r5.md:96-98`; `receipts/step16/gating/{1x1,8x8}/artifacts.sha256` and `identity.log`; `receipts/step16/images/product-images.txt`; `sw/litex/check_image_identity.py:4-36`.

**Authority/evidence:** the assigned composition acceptance requires the gating bitstreams' loaded firmware to equal the final product images, with public executable evidence under AGENTS.md sections 2, 6 and 7. The product receipt records whole-file hashes `fe12a3f1…` and `c6355962…`; the gating receipt records `c873a0aa…` and `d67fd049…`. Whole-file differences can be harmless symbol/debug differences, but cannot establish loaded-byte equality. The handoff asserts equal loaded-section prefixes `1fd5bc47…` and `ac014c6a…` and points to `../fg4-bench-images.txt`. That file is absent from the entire supplied archive. The new gating manifests are named by hash but are not published in either step16 gating directory. The identity gate checks the firmware against its own manifest and ROM initialization, not against the separate product link. No two-sided loaded-section receipt for these two new gating ELFs was found. `receipt_checks.log` records the inventory and actual identities.

**Impact:** the packet does not let a cold reviewer establish the required connection between the new routed images and the final product firmware. This is an evidence gap, not a demonstrated mismatch or failed timing floor. It changes a required identity/proof claim, so it is not RESIDUE.

**Required outcome:** publish the existing two-sided comparison, binding both full ELF hashes to loaded section addresses, lengths and full digests or byte comparisons at both points. Include the referenced gating manifests, with their hashes matching the artifact lists. A new route or source change is unnecessary if the existing comparison proves equality.

**Verification:** check that receipt's two sides against the product and gating identities, verify the manifests' content hashes and bitstream binding, then explicitly re-review F1. Tests and Docs remain UNCLEAN until then.

## Composition and frozen steps

`audit.py` confirms exact second parents, ancestry, unchanged patches outside shared files, preservation of both sides' additions in shared files, and equality of each entire recorded merge tree to a clean merge:

| Step | Source PR / issue | Frozen head | Train merge | Composition result |
|---|---|---|---|---|
| 13 | #953 / #943 | `a16899b1fb2a0c731ebf18476d1a38627254ea4e` | `c05d5acb` | 20 file patches identical; two shared files preserve both additions; clean merge tree identical |
| 14 | #952 / #951 | `f09d82e05270bdd77e07f7fc2e14d064c1123be8` | `4b9f66c5` | Seven file patches identical; three shared documents preserve both additions; clean merge tree identical |

The shared step-13 files are the AECP README and `test_aecp.cpp`. Step 14 shares MAILBOX_SPLIT.md, SPLIT_CONTROL_MEMORY.md and the budget README. The RESOLUTIONS.md entries agree with the merges; neither merge contains an unrecorded conflict resolution. Public source verdict headers name these frozen heads. Step 13 has R871-2 and R872-2 positives. Step 14 retains R870's timing-evidence condition; its status is not silently converted to approval here.

The composition commits are `01765bb0` (restore-format fix), `c1e95dc1` (boundary classification), `92de01f7` (SRP cut), `fb083864` (two mutant targets), `8c5e2b4f` (owner-authorized costs and derived controls), and `8dc85884` (design-document record). The last commit changes only SPLIT_CONTROL_MEMORY.md. No HDL or dependency pin changes after the prior reviewed head.

## Firmware equivalence and robustness

**Saved format, `aecp_face.c:228`.** Before `aecp_face_open`, the face accepts a supported format without demanding that the reset map already fit it. It still checks the support bit and rejects invalid low-byte verdicts. After open, the live SET_STREAM_FORMAT path again requires the actual map-fit bit. This is consistent with SAVED_STATE_MATERIALIZATION section 8.4: restore supported formats first, then restore/settle the maps. Open sets `ready` before live publication. The change does not bypass live format validation or alter the wire response rules.

`Face.BeforeOpenAFormatVerdictJudgesSupportAlone` at `test_aecp.cpp:5351` covers support/refusal, reserved-low-bit rejection and the live distinction. `test_plat_sinks.cpp:1001` removes mappings that would forbid the narrowing, changes input 0 to one channel, saves it, resets the modeled CPU/fabric while retaining flash, and checks the restored format and maps. I independently ran the sink suites at 1x1/1if and 8x8/1if: 24 tests passed. The published firmware campaign includes the added face and sink plants. This resolves F-G5's software cause; it is not a physical power-cycle recheck.

**SRP, `srp_mbx.c:96,441,515,846-885,996,1022`.** The following comparisons were made against the pinned lwSRP implementation, including `mrp_mad.c` allocation, transition notification and reclaim paths:

- `sources_of()` preserves all matching sources, including duplicate stream identities. The last-byte comparison is only a prefilter before the full eight-byte comparison. The mask's width is protected by the source-count bound; callers preserve source order and their original per-source effects.
- A sink pass is skipped only while its desired state is current. Talker changes, binding/declaration changes and reset paths invalidate it. Listener processing and indications retain their ordering. A changed Talker followed by another attribute in the same received PDU sees the recomputation when it is owed.
- `moved()` owes a reclaim only at Registrar MT with Applicant VO/AO/QO, exactly the library's freeable-state predicate. It still handles listener-presence changes and transmit obligations independently. An already owed reclaim stays owed; a refused reclaim while a build is prepared is not lost.
- Creation at VO/MT is the exception that need not emit a transition. `apply_receive()` compares the pool's attribute-capable room before/after receive and counts moves out of that initial state. This detects an attribute created and left reclaimable even beside another changed attribute. Net temporary map-work allocation cannot hide a retained attribute; conservative extra reclaim requests are harmless. MSRP Listener, Talker Advertise/Failed, Domain and the MVRP observer paths were checked against allocation and callback behavior.
- The walk-free snapshot inlines `capture(s, s->desired)`: its withdrawal transition is impossible when previous and current desired are equal, and its remaining copy condition is unchanged.

`srp_listeners.cpp:421-480` compares the optimized path with the reference walk/reclaim behavior, including wire output, filter/license writes, registrations, timer activity and state. The random sequences cover the six attribute events, all Listener declaration values, Talker Advertise/Failed, Domain, link changes, rebindings, time progression and allocation failure. The four direct tests cover the no-walk steady case, created-MT reclamation alone and beside another change, and reclamation on leaving. The reference shares the underlying protocol library, so the static callback/allocation comparison is part of the evidence rather than treating the differential test as a separate protocol implementation.

I ran both listener suites: 16 tests passed. I also ran all ten new SRP-cut plants plus both retargeted existing plants in three campaigns: all twelve at 1x1/1if, all twelve at 8x8/1if, then the ten new plants at 8x8/2if and the two legacy plants at their default 1x1/2if. All 36/36 were caught on their intended checks. `fb083864` keeps the last-byte plant observable in the stream-matcher near-miss/withdrawal test and the failed-first filter plant observable in the reference-reclaim test. No control was deleted to obtain these passes.

**Boundary classification, `c1e95dc1`.** `sink_mutants.py` and `talker_notice.py` describe mutations/scenarios; they do not launch firmware builds. Their owning builders remain captured. Treating these two files as outside the builder census removes false classification findings without excusing an actual compiler invocation. The published complete boundary run has zero findings with 117 boundary, 185 pin and four figure controls; the scoped run also has zero findings.

## Costs, rules, figures and controls

Only the owner-authorized 1x1/1if notice statements are lowered: ordinary notice 210 to 150 us and long notice 365 to 315 us. Four moved costs rise: paced edit 315 us, held SET_STREAM_INFO 250 us, donor ADP record 105 us and centisecond tick 170 us. The remaining statements retain the no-lowering rule. The owner bounds stay 0.70/0.75 load, 140 ms last notice, 30 ms ACMP and 49 ms txL, with the existing row bounds unchanged.

`audit.py` recalculates all 68 rows at each required point using integer arithmetic equivalent to measured cycles at 100 MHz, plus 5%, rounded up to 5 us. No statement is below that value. The cycle maxima agree with the published survey JSON. For the final 1x1 image, the tick's 15,672 cycles would permit 165 us, but the earlier 170 us statement is retained. The owner's exception does not lower other conservative statements. At 8x8/1if the SRP record is 34,803 cycles, 370 us by the rule, below its retained 375 us statement; reclaim is 995 cycles, 15 us by the rule, below 40 us.

The slice maximizes the prescribed minimum normalized margin over the required grid/rows; an independent call to `rows_tiers.ruled()` selects 950 us. The queued rule gives 130 ms from the 127.31 ms row. This is a tighter derived project figure, not a change to the owner's 140 ms limit.

| Point / evidence head | Cost statements exceeded | Last notice | ACMP | txL | Load |
|---|---:|---:|---:|---:|---:|
| 1x1/1if, `8c5e2b4f` | 0/68 | 127.31 / 130 ms; owner 140 | 29.06 / 30 ms | 47.88 / 49 ms | 0.5114290965 / 0.70 |
| 8x8/1if, `92de01f7`, carried by unchanged images | 0/68 | Every-source rows reported under #872 | Same reporting rule | Same reporting rule | 0.7435707105 / 0.75 |

8x8/1if's separately held transmit row is 76.81 / 77 ms. The declaring-output arm's non-completing paced work remains reported according to its accepted scope; completion-running records remain held. These are not silently treated as ordinary-arm passes.

Both measurements contain 64 rc-zero parts, including the declaring-output arm. The final 1x1 summary records 241 groups, zero refusals and zero of 388,313 passes over the share; its seven held-egress misses remain explicitly attributed to the existing stack issue. The 8x8 run's interrupted parts were resumed on the same recorded images. This review verifies the published part results, summaries and cost records, not every line of the omitted large raw logs.

**Re-anchored controls.** The transmit plants now go one millisecond below the computed row's ceiling rather than below a conservative statement. The shape-fallback fixture deliberately separates equal 130 ms values so incorrect interface fallback remains detectable. The queued constants expect `(130,130,62)`; late notices are planted beyond the new bound. `control_probe.py` verifies intact detectors refuse the plants and blinded/off-by-one detectors make the corresponding controls fail. This checks the five changed controls at their cause. Independent self-tests pass 616/616 flip, 1,033/1,033 tier, 25/25 shape and 28/28 load controls. The full budget self-test result is recorded below.

## Image carry, routing and gate evidence

The image receipts establish the intended measurement carry: the eight budget images at the two 8x8 points are unchanged from `fb083864`, whose receipts bind them to `92de01f7`. All twelve step16 image digests agree with the gate image log. The product comparison preserves the 8x8/1if hash `c635596216d95671d9308f9f31b12db98c9f65747f5834b69f0df683756729b4`; the other unchanged product links are recorded too. The changed 1x1/1if budget/product images have five changed immediates, ten bytes, for the 900-to-950 us slice and derived values, with section/symbol layout unchanged. That point is re-measured in full. `8c5e2b4f..8dc85884` changes only the design record, so executable inputs carry to this head.

This is comparison of published image hashes and disassembly receipts. ELF and bitstream binaries were not independently rebuilt or hashed here. It establishes the source measurement carry; it does not supply the missing product-to-gating comparison in F1.

Both new routed-image receipts meet #818 at all four corners:

| Point | Bitstream SHA-256 | Slow setup / hold | Fast setup / hold |
|---|---|---:|---:|
| 1x1/1if | `c7189218a128b71d632edc82157ea6f31b303383a6fe302d50265ad816332a28` | +0.131 / +0.102 ns | +1.636 / +0.036 ns |
| 8x8/1if | `7d90341299cc65e8c0da249139471a61019255132b66d5207ef9ffb4a5d0b773` | +0.176 / +0.102 ns | +1.523 / +0.036 ns |

Both 0 C and 85 C corners are present. The acceptance floor is setup >= +0.030 ns and hold >= 0, not a new +0.030 hold requirement. The build receipts name the selected placement directive and the established recipe; the final build appends `--eth-port e2` after the generated argv. Build rc is zero and the identity gates report success. F1 prevents certifying the separate loaded-product identity claim.

The release's latest published comparison is `receipts/step15/images/release-export-17.txt` (from `c1e95dc1` to `92de01f7`): generated Verilog differs only in comments; object paths/debug content are distinguished from loaded bytes. Later executable changes are confined to split-control firmware and its tests/budget statements, which the all-fabric release does not link. The release dependency carry is therefore unchanged by this delta. The final export log only says 3,876 files exported; it is not a fresh binary-comparison receipt, and the handoff's final-byte statement has not been independently recomputed here.

The step16 source receipts show four firmware shards passing, 826/826 plants caught, coverage of 40 firmware files, twin plus plants, receive-monitor tests/plants, both split-boot simulations, both boundary runs, nine ledger controls and the cost/grader checks. The docs/generated checks are recorded in `q.log` and `docswf.log`; the former reruns the parser/diagram/register checks successfully in their prepared environment. The remaining environment-dependent failures are the checksum-pinned parser inventory and workflow-only install/event-context operations. They are not counted as passes. No candidate host-orchestrator command was run by this review.

The all-points flip command exits 1 for exactly the same eleven 8x8/2if `OVER` lines as at `0839453f`; `receipt_checks.py` compares the lines byte-for-byte. These accepted reported exceptions are not new misses. Independent required-point checks pass. Final-head `docs_check.py` reports zero findings, and `git diff --check cb96336d HEAD` passes.

ROM remains recorded S14 debt, not a newly waived timing/fit requirement. The step16 ledger records the 8x8/1if product ROM at 139,208 of 139,264 bytes, 56 bytes spare; this is an explicit capacity limit and remains sensitive to later code/layout changes.

## Wording residues and prior findings

The following are wording-only under the owner's rule. They change no measurement, test predicate, generated artifact, clause claim or privacy rule. They do not clean F1 or make its evidence optional.

- **R866-4-R1 — RESIDUE — Docs — new issue-comment IDs in source comments.** Artifacts: `aecp/aecp_mbx.h:77`; `loop/ctrl_loop.h:218,283,344`; budget `edit_rows.py:51`, `load_grade.py:219,273`, `notice_window.py:69`, `poll_grade.py:108`, `shape_costs.py:408,513`; explanatory check label at `selftest_notice.py:115`. Authority: the owner's source-comment rule. Impact: prohibited review-history detail in explanatory source text. Exact fix: remove `issuecomment-7044585511` and redundant punctuation, retaining #665, the owner-decision date, item 4 and the behavior/reason. Verification: comment/docstring/label-only diff with identical executable checks and constants.
- **R866-4-R2 — RESIDUE — Docs — historical PR narrative is not consistently labeled.** Artifact: `pr945-body.md:1,63,440-448`. The current Status correctly names fourteen steps, the full measurement and current figures, but the opening says twelve and the retained old section says “At the final head”; Known limitations still calls the full measurement pending. Exact fix: change opening “twelve” to “fourteen”; label line 63 “At the step-12 head `0839453f`”; remove the superseded CPU-sample/pending bullet or mark it explicitly historical; change the following reference to “the then-final step-12 head `0839453f`.” Preserve historical execution attribution and the actual hardware limitations. Impact: stale duplicate narrative, not a changed figure. Verification: read the resulting body against the current Status and receipt heads.
- **R866-1-R1 — RESIDUE — Docs — RETAINED.** Artifact: `test_plat_boot.cpp:91,95,116,119`, unchanged. Remove the B24 prefix, parenthetical PHY label list and L5/L6 prefixes; preserve the behavioral descriptions and issue/clause references. Verify comment-only equivalence. This retains the originating reviewer's finding rather than silently adopting another review's different label interpretation.
- **R866-1-R2 / R865-1-RES-2 — RESIDUE — Docs — RETAINED.** Artifact: `plat/ctrl_split_hot.txt:14,19`, unchanged. Remove `issuecomment-6959600243` and `issuecomment-6967930396`, retaining #665, dates, item numbers and the procedure. Verify ordered hot-list entries and image-relevant content are unchanged.
- **R865-1-RES-1 — RESIDUE — Docs — RETAINED.** Artifact: `docs/design/AREA_BUDGET.md:139,141`, unchanged. The prose still calls the superseded measurement/current directive the gate's record, while the accepted JSON record is newer. Exact fix: say that it *was* the record until the train's 2026-11-18 re-record and that the selected directive has since been ExtraTimingOpt; preserve historical figures and #640 debt. Verify against `syn/ooc/pp_resource_baseline.json` and the docs check.
- **R866-2-R1 — RESIDUE — Docs — remains RESOLVED.** Current PR Status identifies `8dc85884`; the composition history includes the inventory update. The earlier stale-head cause has not returned in that Status.
- **R866-3-R1 — RESIDUE — Docs — RETAINED.** Artifact: PR Known limitations, `pr945-body.md:470`. Delete the obsolete sentence that the release comparison was last made at step 9; retain the image section's later, explicitly attributed comparison. Verify prose against `release-export-17.txt`; do not imply a new independent binary comparison.
- **R871-2-R1 — RESIDUE — Docs — RETAINED from step 13.** Artifact: `declaring_outputs.py:296,323`, carried unchanged from the frozen head. Replace `R872-1-F2` in the docstring with `#943`; remove `(R872-1-F2's)` from the check label. Verify that only explanatory strings change. This is the previously published source residue, not a fresh review of step 13.

Cause-level dispositions beyond wording:

- Prior PR #945 rounds contain no unresolved BLOCKER/MAJOR/MINOR. Their unaffected coverage remains inherited; this round introduces F1 for the new images' missing receipt.
- F-G1's receive-context format defect remains fixed by step 12; its paths are untouched, and the new published receive-monitor/plants and boot tests pass. F-G2 (one stream bound to two inputs) remains the separately scoped parser-classification limitation; this round does not claim to fix or reclassify it. F-G3's output-status cause is carried exactly from the approved step-13 head. F-G4's PHY-advertisement premise was withdrawn after the tap-versus-DUT distinction; it is not hardware proof. F-G5's saved-format cause is addressed and tested as above; its physical recheck is pending.
- **R870-1-F2's final-image evidence remainder:** the complete source measurements and image carry examined here now supply the source evidence missing from its sample. Its assigned reviewer rechecks that remainder separately; this report does not invent a new R870 verdict or discharge the current-dev merge-candidate condition. R870's already corrected clause/layout findings remain corrected in the frozen delta. The nominal hold-off policy suggestion and conditional reference-device measurement suggestion remain optional, with public manager disposition still owed.
- Step 13's resolved R872-1-F1/F2 and R871-F1 stay resolved at their causes: the preserved declaring fixture keeps `brief`, records completion, and the flag/interface test and plants remain intact. The final re-measure includes its maintained arm. R871-2-S1/S2 remain optional Tests suggestions: anchor the declaring arm's address to the actual allocated base and value-check SET_STREAM_INFO responses as well as GET. Their originating review already identifies the exact product tests that cover those values; no scope expansion is requested here.

Inherited optional suggestions remain public work dispositions, not new requirements for this composition:

- **R869-1-SUG-1 — SUGGESTION — Conformance — `sw/firmware/ctrl/srp/srp_mbx.c:32-46`.** Evidence: the approved hold covers two nominal longest LeaveAll periods, not two Milan tolerance-extreme 15.5 s periods. Impact: the latter is outside the accepted policy. Optional outcome: explicitly retain that policy or authorize separate tolerance-inclusive work. Verification: public policy disposition and, if changed, timing tests and image evidence.
- **R869-1-SUG-2 — SUGGESTION — Docs — #951's conditional reference-device measurement.** Evidence: no conflict-delay hardware result is claimed. Impact: issue closure could obscure the conditional check. Optional outcome: record its transfer or the maintainer's decision to decline it. Verification: public disposition or a dated measurement.
- **R871-2-S1 — SUGGESTION — Tests — `tb/verilator/ctrl_service_budget/declaring_outputs.py:209-213`.** Evidence: the maintained arm checks one MAAP-pool base per interface but not the allocated base itself; the product test pins the exact address. Impact: a uniform offset could evade this arm's value check. Optional outcome: derive the base from the actual allocation. Verification: a shifted-base plant fails the arm.
- **R871-2-S2 — SUGGESTION — Tests — `tb/verilator/ctrl_service_budget/declaring_outputs.py:188-199`.** Evidence: the arm decodes GET_STREAM_INFO values; SET responses are timed and counted. Impact: SET-only wrong values are not checked there, although completion is shared and the source acceptance names GET. Optional outcome: extend its decoder to SET_STREAM_INFO. Verification: a SET-only wrong-address/flags plant fails.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `aecp_face.c:228`; SAVED_STATE_MATERIALIZATION section 8.4; `srp_mbx.c:96,441,515,853`; pinned lwSRP transitions/reclaim; owner rulings and both recomputed CPU tables | R866-4, preserving unaffected earlier coverage | 8dc8588471a096bbe120bbec4c8c0f8ddf44d8cd |
| RTL | CLEAN | Frozen merge trees; firmware readiness/restore sequencing; mask-width and pool/callback invariants; no HDL/pin delta; both step16 signoff receipts against #818 | R866-4, preserving unaffected earlier coverage | 8dc8588471a096bbe120bbec4c8c0f8ddf44d8cd |
| Robustness | CLEAN | `test_plat_sinks.cpp:1001`; `srp_listeners.cpp:421-480`; twelve SRP plants in three campaigns with explicit entity selection; listener/filter ordering, allocation failure, reset, link and withdrawal paths | R866-4 | 8dc8588471a096bbe120bbec4c8c0f8ddf44d8cd |
| Tests | UNCLEAN | Focused tests and control blinding; published source gates/measurements and exception comparison; F1 product-to-gating identity evidence missing | R866-4 applied; no clean covering round for F1 | 8dc8588471a096bbe120bbec4c8c0f8ddf44d8cd |
| Docs | UNCLEAN | Complete composition delta; RESOLUTIONS.md; CPU tables; final PR Status/historical sections; current source/design comments; F1's unsupported public identity connection | R866-4 applied; no clean covering round for F1 | 8dc8588471a096bbe120bbec4c8c0f8ddf44d8cd |

Clean source/architecture results do not certify F1's unverified artifact identity. No number of passing tests substitutes for that missing connection.

## Reproduction, limits and pending duties

Run the packet scripts from this exact checkout. `prepare_evidence.py` extracts only the fixed public author packet and manifest into the packet's `scratch/` directory; it requires archive commit `563c16e5f62152a2ff1c9722e23208e1fbad0e88` to be available locally. `audit.py`, `receipt_checks.py` and `control_probe.py` reproduce the receipt, arithmetic and control checks. `probe.py listeners`, `probe.py sinks`, and `probe.py mutants-11`, `mutants-81`, `mutants-2if` reproduce the native focused tests and three mutation campaigns with four build jobs per campaign. Their published logs and rc files record the results. Independent campaigns ran concurrently within the sixteen-job cap; no shell-background job is left running.

The other executed commands are `flip_grade.py --check --point 1x1/1if`, `--check --point 8x8/1if`, and `--check` (expected inherited rc 1); `flip_grade.py --selftest`, `load_grade.py --selftest`, `rows_tiers.py --selftest`, `shape_costs.py --selftest`, `run.py --self-test`, `scripts/docs_check.py`, and `git diff --check cb96336d HEAD`. The sequential full-budget self-test was stopped after 144 completed mutation checks to reduce wall time; its partial log and rc -15 are retained. `parallel_selftest.py --jobs 12` partitions the unchanged 295-entry mutation list across isolated processes, each running the original baseline checks and its assigned mutations. Parallel completion: rc 0, baseline checks pass in every worker, 295/295 mutations caught and zero failures (`parallel-selftest.log`, `selftest-workers/`). The printed “ESCAPED” lines inside its detector-blinding exercises are intentional negative controls, not by themselves a final failure verdict.

`verify_checkout.py` hashes actual tracked file bytes, checks executable modes and the complete index, and recursively verifies all five required submodules. The checkout's 1,941 entries, head/tree and clean status pass. Pins remain gPTP `1616fc8f062fbf58c35ad31674b5b233207bbdb8`, protocol processor `801ef2283ec793e35a2590fc6593c90313a64041`, lwSRP `08ee86e812a0eb5e1dc6cd61b494d8baf3491348`, TSN stack `715589c1db7cf67e2f3259fd7083ebc7f0923376`, and axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. Optional `external` is uninitialized and unused. Probes worked on disposable copies; no candidate source restoration was needed.

The full parent/processor/synthesis/builder banks were not run by this review. Source gate evidence is the author's published evidence. **No manager source-head bank exists or is inferred.** No hosted acceptance is claimed from this review; the manager owns executed-versus-skipped hosted and local-replica acceptance. Physical calibration is **NOT RUN**; field skips, model boot results and earlier bench observations are not final-head hardware proof. No new physical test was performed.

The manager must publish F1's missing comparison and obtain its re-review, retain all residue/optional dispositions, and await the other required independent reviews. The manager must separately validate the actual current-dev merge candidate with the required builder/native banks and link its receipts. Source base `cb96336d` and supplied live dev `e275d7950ef3385753e6a15d2e191ba855b171ed` are not that eventual candidate. Reuse requires proof that the relevant measured image bytes remain identical. The assigned timing reviewer still owns its explicit final-evidence recheck. Final-head physical checks, required hosted/local gates, explicit merge authorization and post-merge containment remain pending under the public contract.

No source fixes, commits, pushes, GitHub writes, author contact, delegated work, container orchestration or hardware actions were performed. Only this review packet contains new deliverables. This report does not authorize merge.

R866-4 FINISHED
