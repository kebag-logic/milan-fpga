[R894] NEGATIVE - exact head 64d539f12532b2591f734b8e756f8a9358bb742c

External independent review, R894-2, issue #584 / PR #975. Tree: 761862ef4b05e0284a6150036ea85709466bbeb5.

All five lenses were applied to the five-commit delta from 2b295a44d136275ccbf060fe4f36c42e573b6460. Two MINOR findings remain: an unobserved recovery interval in the new freshness test and two round-two publication-index mismatches. No new RTL implementation defect was found.

The mapping-to-pin integration gap is substantially repaired. The clean ship8 case passes 124 checks independently. Its generated parameters, one-slot adapter composition, mapping/remapping, zero tail, unrouted ports and REMOVE checks are supported. Its claim about the first post-rebind/reset event remains insufficiently tested.

F1 is CLOSED FOR ITS STATEMENT ONLY under this round's instruction. The owner’s scope disposition remains OPEN, separately from this round’s defects. This review does not approve the backing deviation or authorize merge.

**Scope, authorities and method**

Read AGENTS.md / CONTRIBUTING.md, docs/README.md, the issue body and public scope decisions, REQUIREMENTS.md and the linked descriptor/render contracts; then examined the dd163e41-to-head change structure and the round-two diff/history. Untouched implementation retains its previous lens result. The builder's executable syntax tree and YAML data are unchanged from round one; there is no round-two RTL or firmware diff.

Authorities: Milan v1.2 5.3.3.7–5.3.3.9 and 5.4.2.26–5.4.2.28; IEEE 1722.1-2021 6.2.2.8, 7.2.13, 7.2.16 and 7.2.19; ENDSTATION_BUILDER D1/D2/D7/D8/D10; PP_DESCRIPTOR_OWNERSHIP; CHANNEL_MAP_64 sections 3 and 3.1; the saved-state and control-memory contracts. The public [processor #122 disposition](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/122#issuecomment-5853884588) retains the input/output cluster minimum: zero dynamic maps does not authorize zero clusters.

Public scope and evidence:
- [Issue #584](https://github.com/kebag-logic/milan-fpga/issues/584), including the approval, fallback, parking and November decision.
- [Round-two REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/584#issuecomment-7085448602).
- [Immutable author packet](https://github.com/kebag-logic/milan-fpga/tree/e3127c9139ae456ef671b098eab55bed6d41d0f4/review-evidence/584-r1).
- Prior public findings [R894-1](https://github.com/kebag-logic/milan-fpga/pull/975#issuecomment-7083745128) and [R893-1](https://github.com/kebag-logic/milan-fpga/pull/975#issuecomment-7083855570), reconciled after the independent diff pass.

No private author material or management checkout was consulted. No current-round peer report was consulted. No source fixes, commits, pushes, GitHub writes, author contact, hardware operations, container operations or sub-agents were used.

**Findings**

[R894] MINOR Conformance, Robustness, Tests, Docs - F2-R2 - tb/verilator/milan_dp_render/sim_ship8_render.cpp:1095 and :1128 - Freshness collection starts after the recovery interval it claims to check

Authority/evidence: prior F2 explicitly requires reset/bind freshness at the generated shipping shape. CHANNEL_MAP_64.md:157–168 requires silence through the closed epoch and post-flush freshness before commits resume. The new test calls bind, then run_pdus(kLeadPdus), and only then decode_a_window. kLeadPdus is 19, about 2.375 ms. decode_a_window resets the decoder and discards earlier observations. Consequently B3 FRESHNESS and Z3 FRESHNESS check the first event in a later window, not the first event after rebind/reset as their verdict strings say.

Independent falsification: probe_freshness.py changes only the simulated pin receiver's data input in a disposable checkout. It replays the known pre-loss event-zero sample into slot zero during these uncollected intervals, leaving expected values, assertions and DUT state unchanged. It records 116 affected slot-zero frame starts before B3 collection and 245 cumulatively after Z3 recovery, an additional 129. The existing test still returns 0 with 124 checks, zero failures, and both FRESHNESS assertions passing. See freshness.log, freshness-summary.txt and freshness.rc. This is a receiver fault-injection test of checker sensitivity, not evidence that the actual RTL emits stale samples.

Impact: transient stale output during recovery can pass the new shipping-shape regression. The steady-state sample, silence and epoch checks remain useful, but cannot discharge the whole prior freshness requirement. The corresponding description in docs/testing/TESTING.md's ship8 row and the PR validation text overstates what this test observes.

Required outcome: collect and grade the recovery transition from before rebind and across reset recovery, accounting explicitly for the permitted interrupted/in-flight frame. Require every subsequent nonzero frame to belong to the fresh injection epoch and grade the actual first nonzero frame. Keep the later steady-state windows. Add a negative control that emits a stale event only before the current window starts.

Verification: the clean case must pass; the transient stale-event control must fail by a named freshness check. Preserve all existing projection/adapter/bus plants and the loopback-on control. The original absence of the mapping-to-pin test is repaired; this bounded remaining test weakness is MINOR rather than the original MAJOR. It retains the combined prior F2 lenses, with Docs added for the new test-coverage claim.

[R894] MINOR Tests, Docs - F5-R2 - author-r2/receipts/INDEX.md:19 and :20 at e3127c9139ae456ef671b098eab55bed6d41d0f4 - The replacement index is itself indexed with pre-publication hashes

Authority/evidence: audit_public.py reads immutable Git blobs directly. The replacement round-one index contains 80 rows and all 80 match the published round-one receipts. However, the round-two INDEX has 16 rows and two fail size/hash verification:

| Indexed file, relative to author-r2/receipts | Indexed bytes | Published bytes | Published SHA-256 |
|---|---:|---:|---|
| f5/index-check.md | 944 | 930 | 2028461caefbe9d38a8ac90a1e67ff33e2108066bf34059a76f80e615030479f |
| f5/round1-INDEX-corrected.md | 10852 | 10838 | d132b10e40e22722e59df58ab56547d2f4896a339f67225a8698ba51ea2c758c |

The indexed hashes are respectively 1eb005c34989f02c0de7543c8760102ac1598916588351b2b1baa24572ca96e6 and 8fe24e6611e9f5ac4d7cb6582b86e5c0fc8c6b29f08f2892b4cc059f04a36591. The top-level MANIFEST.json correctly hashes all 98 author receipt/index files checked. The unchanged original round-one INDEX still has its original three mismatches; its separately published replacement repairs those three as promised.

Impact: a consumer following the new round-two receipt index cannot authenticate the correction artifacts with the supplied sizes/hashes. This is an integrity-metadata defect, not an allegation that test results were fabricated or that the corrected inner 80-row index is wrong.

Required outcome: regenerate the round-two INDEX from the final public bytes after normalization, then generate its enclosing manifest. Preserve the corrected inner index and identify it as superseding the original round-one index.

Verification: audit every nested receipt index against the same immutable publication, including indexes listed inside other indexes. Expected: 80/80 for the replacement round-one index and 16/16 for the round-two index, with the top-level manifest still matching. public-audit.txt contains the raw arithmetic and hashes.

**Non-blocking residue**

[R894] RESIDUE Docs - R4 (carried from R893-1) - sw/builder/endstation_builder.py, generated build_plan.md cluster-name template

Authority/evidence: the template's nonphysical-name examples omit Unrouted S<p>. The prior review explicitly allowed this to remain because changing it changes every configuration's build_plan.md. Impact: an incomplete example list only. Exact optional fix: add Unrouted S<p> to that example list when the generated-document byte-identity constraint permits. Verification: generated prose lists the existing role; no model or behavior change. Retained, not treated as a blocking finding.

[R894] RESIDUE Docs - R5 - CHANGELOG.md:81 - Make the pending TDM interpretation explicit in the short summary

Authority/evidence: the changelog's “Both points” follows the two loopback statements; D8, D10, the ownership page and PR also explicitly put the TDM32-slot-zero interpretation under pending disposition. Impact: the short summary leaves that reference implicit; the detailed pending decision is already explicit. Exact fix: append “The TDM32 slot-0 interpretation also awaits that disposition.” Verification: the summary unambiguously points to the same pending decision. No scope approval or conformance claim changes.

[R894] RESIDUE Docs - R6 - author-r2/receipts/f5/index-check.md, Cause paragraph; f5/round1-INDEX-corrected.md, introductory paragraph

Authority/evidence: normalization turned the examples of before/after path strings into identical placeholders. Impact: the explanation reads as replacing a string with itself. Exact fix: replace the literal examples with “Publication redacted private home-path prefixes in three receipts before hashing.” Verification: the explanation remains understandable after publication normalization; recompute its index entry as F5-R2 requires. The wording correction itself changes no result.

No new prohibited bench-lane, reviewer or review-round identifiers were found in the added source comments.

**Disposition of every named prior finding**

| Prior item | Disposition at this head |
|---|---|
| R894 F1 / R893 F1 | Statement closed under this round's instruction. PR, D8, D10, ownership page and changelog disclose pending backing disposition. No input cluster is named loopback. The owner's disposition is still open and is not graded as a new defect here. R5 is summary wording only. |
| R894 F2 / R893 F2 | Generated-shape mapping-to-wire leg, real sample path, zero tail, REMOVE, unrouted isolation, control-face equivalence, four plants/refusal and CI registration are supplied. Retain the narrower freshness deficiency as F2-R2. |
| R894 F3 / R893 F3 | Closed. Per-image ROM/SRAM deltas recompute correctly; unsupported symbol-by-symbol attribution is no longer claimed. |
| R894 F4 | Closed. L1 names STREAM_PORT_CLUSTER_MINIMUM and the absent waiver; builder row 45 says no tracked waiver; 32x32 census prose agrees with one cluster per listener and 11 + 13N. |
| R894 F5 | Original three rows corrected in the separately published 80-row replacement. Retain publication integrity under F5-R2 because the new outer index mismatches that replacement and its audit note. |
| R893 R1 | Closed: “an 8x8 talker”. |
| R893 R2 | Closed across D8, row 16f, builder comments and YAML: first binds every physical render channel to input port 0. Executable code is unchanged. |
| R893 R3 | Closed: obj_nxn8 now describes one mono cluster per input port and its loopback-on control role. |
| R893 R4 | Retained as optional RESIDUE above. |

**Independent lens evidence**

Conformance: compared the issue's frozen acceptance and pending backing statement with D8/D10, ownership L1/F5, YAML and generated shape. The generated shape comparison passes. The unchanged builder executable AST and YAML data support carrying the previous five-configuration descriptor/refusal/identity/byte-equality results. The new test supplies the previously missing shipping-geometry integration path; F2-R2 leaves its freshness portion unclean. No newly observed protocol implementation violation is asserted.

[R894] PASS RTL - hdl/milan/milan_datapath.sv:8681, :8732, :10193; hdl/ieee1722/aaf/KL_tdm_render_master.sv:137; delta-history.txt - No round-two RTL/firmware change; the prior bus/lane-width, indexing, CDC and reset result carries. Traced the adapter and bus binding used by ship8 and the split i_ctl_edit_* to ppo_amap_edit_* assignments. The all-fabric test exercises the shared transaction-server/media path; it is not a split CPU end-to-end execution. No new RTL defect found.

Robustness: independently ran ship8's port-7 invalid offset, unmapped ports with live feeds, REMOVE silence, stream-qualified bind loss and reset checks. The published four projection/adapter/bus mutations plus the direct binding refusal have distinct named failure requirements; crashes and unrelated compile errors do not count as catches. The generated-parameter reader responds to perturbed inputs and refuses duplicate/unmapped/missing-master cases. F2-R2 identifies the recovery interval those checks miss.

Tests: read the entire new harness, its pin decoder, injection identity/timestamp record, independent route record, parameter reader, mutation runner and Makefile. The new flags come from regenerated soc_params.json and aem_overlay.json; tracked/generated headers are compared, and geometry assertions constrain the bench. Independent parameter perturbations prove the values are consumed rather than merely mirrored. The suite lists ship, multi, leg-defects, ship8; build/exec/receipt targets and the fourth 240-second shard entry exist. The loopback-on nxn8 recipe is retained. F2-R2 and F5-R2 leave this lens unclean.

Docs: checked the full documentation delta against generated shape, cluster_layout semantics, published memory image sizes and the census checker. The four ROM/SRAM increases are respectively 1336/1744, 1336/1808, 1336/1744 and 1344/1744 bytes. The representative fixture's 61.0 tiles remains distinct from its maximum variants' 61.5 entry. F1's scope status is pending, not approved. F2-R2's coverage description and F5-R2's integrity claims leave this lens unclean; R4–R6 are non-blocking residue.

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F2-R2 | issue acceptance/decisions; D8/D10; PP_DESCRIPTOR_OWNERSHIP; generated shape; ship8 recovery claims | R894-2 applied; no clean covering round | 64d539f12532b2591f734b8e756f8a9358bb742c |
| RTL | CLEAN | milan_datapath guards/adapter/shared edit server; KL_tdm_render_master; no RTL delta; prior source/unit result | R894-1 carried; R894-2 dependency check | 2b295a44d136275ccbf060fe4f36c42e573b6460, unchanged through 64d539f12532b2591f734b8e756f8a9358bb742c |
| Robustness | UNCLEAN: F2-R2 | sim_ship8_render.cpp; ship8_mutants.py; parameter refusals; clean and transient-fault receipts | R894-2 applied; no clean covering round | 64d539f12532b2591f734b8e756f8a9358bb742c |
| Tests | UNCLEAN: F2-R2, F5-R2 | harness/decoder/oracles; generated flags; Makefile and suite_shards.py; published indexes | R894-2 applied; no clean covering round | 64d539f12532b2591f734b8e756f8a9358bb742c |
| Docs | UNCLEAN: F2-R2, F5-R2 | builder/ownership/memory/census/changelog/testing pages; PR body; public receipt indexes | R894-2 applied; no clean covering round | 64d539f12532b2591f734b8e756f8a9358bb742c |

The ledger does not convert the pending owner decision into approval.

**Execution receipts and reproduction**

All disposable checkouts, builds and fault copies are under scratch/. Commands ran in foreground sessions and all sessions completed. Compilation used at most 16 jobs. The required simulator identity was verified before execution.

| Check | Receipt | Result |
|---|---|---|
| Clean ship8 at exact source head | ship8-clean.log, ship8-clean.rc | 124 checks, zero failures, rc 0 |
| Transient stale receiver-input fault | freshness.log, freshness-summary.txt, freshness.rc | Fault survives: 124 checks, zero failures, rc 0; F2-R2 |
| Builder/YAML semantic equality, generated flags and perturbations, header equality, memory arithmetic | delta-audit.txt, delta-audit.rc | PASS |
| Saved-state 32x32 documentation/census | census-check.log, census-check.rc | 0 findings, rc 0 |
| Shard planner self-test | shards-selftest.log, shards-selftest.rc | PASS |
| Immutable publication hashes and nested index checks | public-audit.txt | Top-level 98/98; replacement 80/80; new index 14/16 |
| Exact tracked blobs, modes, stage-0 indexes and required submodule gitlinks | tree-integrity.txt, tree-integrity.rc | PASS |

Portable scripts:
- audit_public.py CHECKOUT PACKET reads the immutable evidence commit.
- audit_delta.py CHECKOUT GENERATED_8X8_DIR verifies the focused semantic/parameter claims.
- probe_freshness.py DISPOSABLE_CHECKOUT PACKET requires a previously built ship8 case; it restores its edited C++ file in a finally block. REVIEW_VERILATOR may override the simulator path.
- verify_tree.py CHECKOUT verifies source identity independently of Git's working-tree status cache.
- package_receipts.py CHECKOUT PACKET extracts runtime stdout and hashes publishable files.

To build the clean case, use make -j16 -C tb/verilator/milan_dp_render ship8 VERILATOR=<required simulator> VERILATOR_JOBS=16 in the disposable checkout. The runtime logs in this packet are byte-preserved stdout extracted from the foreground build/run transcripts; build trees and transcripts stay unpublished under scratch/. The fault probe changes only the disposable copy; the reviewed checkout was never edited.

**Published evidence and limits**

The author’s exact-head ship8 receipt agrees with the independent clean result. The author’s ship8-mutants receipt reports the clean control, four named plants and one named elaboration refusal, six passes. That campaign was inspected, not rerun here. The full default render-suite receipt at 25ad9c9a reports the existing cases plus ship8 and leg-side controls. The cold fourth-piece CI receipt is 147.88 seconds at e2a0858c; 240 seconds is a scaled planning estimate, not a measured hosted result.

The round-two builder union reports 113 gates with the existing not-run arms; the docs receipt reports 99/103 passing, with four hosted-environment rows failing as recorded. These are author executions, not independent full-bank reruns. Physical calibration NOT RUN and field skips are not hardware proof.

The model, firmware, route inputs and saved-state implementation are unchanged in round two, so their prior evidence remains carried evidence. The source review does not claim new routing, image links, capture measurements, CPU-budget banks or full parent/processor/gPTP/Yosys/builder-bank execution. No manager source bank ran at this exact head and none is claimed or inferred.

Publication verification is against immutable Git blobs and SHA-256 indexes. The supplied publication commit has no signature header, and the supplied MANIFEST is a hash list, not a detached cryptographic signature. No cryptographic signer authentication is claimed.

The final source audit verifies the exact head/tree, all tracked superproject bytes/modes/index entries, and materialized required submodules against their gitlinks. The initialized lwSRP submodule was also verified. The uninitialized legacy external entry was checked as a gitlink only.

**Pending manager duties**

- Obtain the owner's public disposition of no loopback-backed input cluster, loopback off at 8x8, and TDM32 slot 0 standing for the first TDM8 channel. This remains an open scope decision, not an additional defect of this round.
- Route F2-R2 and F5-R2 for correction and re-review; carry R4–R6 to the residue checklist.
- Obtain hosted/local-replica acceptance and the ship8 hosted runtime evidence. This review did not execute or certify those gates.
- Build and validate the final current-dev merge candidate with the builder and native banks, and publish its receipts. Source base dd163e41438acb86e0c4d4e76df90f3f91ace1c0 and live dev e275d7950ef3385753e6a15d2e191ba855b171ed are distinct from the reviewed source head.
- Complete independent review coverage, merge authorization and post-merge containment under CONTRIBUTING. The pre-existing all-fabric milan_nvm listing overrun remains separately owned.

R894-2 FINISHED
