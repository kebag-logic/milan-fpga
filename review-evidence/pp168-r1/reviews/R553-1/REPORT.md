[R553] NEGATIVE - exact head 96d3b78384f34a630d6056ebd8fa5e30f6836650

Round R553-1, issue #168 / PR #171. Tree `37ee429d6fb58f8c3f93d735131e4821f5240004`. Two open MINOR findings leave Conformance and Docs unclean. The six RTL corrections, their new mutation checks, the measured area reduction, and the unchanged public port/parameter boundary passed this review. The findings concern normative behavior and data ownership; they are not wording-only RESIDUE.

**Independent reconstruction and scope**

The supplied instructions were followed with no sub-agents, source fixes, commits, pushes, GitHub writes, parent/source banks, container execution, shared installations, or hardware access. No repository or ancestor AGENTS.md or CONTRIBUTING.md was present. The supplied instruction file, `docs/README.md`, root/HDL reading guides, the [frozen issue](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/168), [original assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/168#issuecomment-6050429859), [round-1b ruling](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/168#issuecomment-6050554601), and [round-2 assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/168#issuecomment-6076502893) establish the review boundary.

The governing standards were read directly: Milan Specification Consolidated v1.2 Final Approved 2023-11-30 and IEEE 1722.1-2021. Their hashes are in [authority-sha256.txt](receipts/authority-sha256.txt), and match the published evidence's standard identities. The linked requirement matrix and architecture/interface authorities were examined, including ACMP requirements 007 and 012–023, F05.3/F05.11/F05.14, F07.6, and the GSI ownership contract in architecture 02/06.

The complete `ed340b9b85258194247334b85e62cf9c23d4d051..96d3b78384f34a630d6056ebd8fa5e30f6836650` [diff](receipts/base-head.diff) and [history](receipts/history.txt) were examined independently. The [independent verdict and five-lens ledger](receipts/independent-pass.md) were written before consulting public executable evidence or checking prior public review findings. No private author material, lane scratchpads, management checkout, or other reviewer's report was read. Subsequent public evidence came from the [frozen evidence publication](https://github.com/kebag-logic/milan-fpga/tree/1570e00395c98ed4ea1c21e6abde28948346c82b/review-evidence/pp168-r1) and the issue/PR comments. The PR's available comment/review history contained the two review-start notices and no prior FINDINGS or submitted/inline reviews; there were no previous findings to retain or resolve. The parent review named in the issue was not used as an oracle.

**Findings**

**R553-F1 — MINOR — Conformance, Docs. Normative ACMP behavior still specifies two corrected defects.**

Artifacts: [architecture 05:283](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/96d3b78384f34a630d6056ebd8fa5e30f6836650/docs/architecture/05_acmp_engine.md#L283) and line 290 (A5/A12), [architecture 05:13](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/96d3b78384f34a630d6056ebd8fa5e30f6836650/docs/architecture/05_acmp_engine.md#L13) and [F05.11 at line 387](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/96d3b78384f34a630d6056ebd8fa5e30f6836650/docs/architecture/05_acmp_engine.md#L387), and [REQ-ACMP-007 at compliance review:391](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/96d3b78384f34a630d6056ebd8fa5e30f6836650/docs/00_MILAN_COMPLIANCE_REVIEW.md#L391).

Authority/evidence: Milan 5.5.3.5.30 step 2 and 5.5.3.5.10 preserve the previous ACMP status on the discovered retry/delay path. A12 and A5 still prescribe unconditional `acmpsta←0`. Milan 5.5.4.2 step 1/Table 5.44 requires TALKER_UNKNOWN_ID for an invalid disconnect source, but the role table, normative decision tree and requirement row still specify unconditional SUCCESS. The corrected implementation is at listener:1273/1345 and talker:1304; local LD2 and TD1 checks pass and their reverting mutants fail. The suite READMEs describe the correction, while architecture 05 still calls F05.3 its single authoritative artifact. The public author handoff acknowledges the old prose as an out-of-scope follow-up; no public manager ruling superseding those normative claims was found.

Impact: a maintainer or verifier following the normative action legend or talker decision tree would restore the exact defects this PR corrects. This changes clause claims and a figure, so the wording-only exception does not apply.

Required outcome: align the authoritative documents with the clauses and landed behavior. Qualify A12 to retain status on TMR_RETRY and A5 to retain status on TMR_DELAY; retain the reset behavior on the other applicable transitions. Make DISCONNECT_TX validate the source first, return TALKER_UNKNOWN_ID for an invalid source and SUCCESS without a state change for a valid source, including F05.11 and REQ-ACMP-007. Resolve the documentation scope with the manager rather than leaving competing normative descriptions.

Verification: re-read the revised action/decision tables against those clauses and the unchanged clause tests; run `make -j16 check`. Mechanical freshness checks alone cannot establish the corrected semantics.

**R553-F2 — MINOR — Conformance, Docs. The authoritative VLAN layout and GSI ownership contract omit the widened path.**

Artifacts: [architecture 05:131](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/96d3b78384f34a630d6056ebd8fa5e30f6836650/docs/architecture/05_acmp_engine.md#L131); [architecture 07:495](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/96d3b78384f34a630d6056ebd8fa5e30f6836650/docs/architecture/07_memory_maps.md#L495) and its committed `docs/diagrams/wavedrom/fig-07-sinkrec.svg`; [architecture 06:331](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/96d3b78384f34a630d6056ebd8fa5e30f6836650/docs/architecture/06_aecp_engine.md#L331); [architecture 02:412](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/96d3b78384f34a630d6056ebd8fa5e30f6836650/docs/architecture/02_interfaces.md#L412); [integrator guide:570](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/96d3b78384f34a630d6056ebd8fa5e30f6836650/docs/guides/integrator.md#L570).

Authority/evidence: Milan 5.3.8.9, Table 5.38, 5.4.2.10, and the round-1b ruling require preservation of the complete received value internally. `pp_acmp_pkg.sv:152` now uses bits 319:304 for the 16-bit settled VLAN, while F07.6 still gives it 12 bits plus four reserved bits and architecture 05 lists 12. `protocol_processor_top.sv:3536` now replaces input GSI selector 6's upper 16 bits with the settled VLAN (zero while unsettled); architecture 06 still assigns all other input words to the integrator. Architecture 02 and the integrator guide omit this new exception. The selector still requests external data and honors its wait because the lower 48 bits remain externally supplied. The local integrated golden observes `0xF123`, with parent VID `0x123`; truncation and external-owner mutants fail.

Impact: the record's normative figure labels live bits as reserved, and the integration contract names the wrong owner for a wire-visible field. This affects a figure, data layout and conformance claim, not just phrasing.

Required outcome: document a 16-bit internal settled VLAN and regenerate F07.6 from its source; distinguish the unchanged 12-bit top-level/SRP VID projection. Update GSI ownership consistently: selector 6 upper 16 bits come from the addressed input's settled state, lower 48 bits and handshake remain external, output behavior is unchanged, and unsettled input VLAN is zero. Document the private pending-probe controller overlay versus the published zero unsettled stream-ID view where the record layout is explained.

Verification: inspect the regenerated figure and the revised ownership statements against package:152 and top:1042/2714/3536; run `make -j16 check` and retain the existing VLAN/parent-VID mutation witnesses. No RTL change is requested by this finding.

**Clause checks and implementation evidence**

The standards, rather than either implementation or its reference model, supplied the expected behavior. Every row below was traced through the final RTL, its checks and its planted defects. [Local mutation results](receipts/fields/results.json) record successful completion and all required failing witnesses; compilation failure is not credited as a killed defect.

| Item | Authority and final behavior | Specific evidence |
|---|---|---|
| LD1 | Milan Table 5.36: successful UNBIND has zero talker EID and unique ID; command controller/listener/sequence remain | listener:679; field_cases.hpp:109; `unbind_talker_echo` killed; updated AL1/AS6 expectations are byte-exact |
| LD2 | Milan 5.5.3.5.30 step 2 and .10: discovered retry and subsequent probe retain status; not-discovered path still clears it | listener:1269/1338 and A17; field_cases.hpp:124; `retry_status_cleared` and both `retry_probe_status_cleared` arms killed; integrated RETRY-RETAIN queries status 7 |
| LD3 | IEEE 1722.1-2021 8.2.1.5/Table 8-3 and Milan Tables 5.31/5.35: both lock refusals use 16 and preserve binding | package:123; listener A1; field_cases.hpp:142; `lock_status_13` and `lock_gate_bypassed` killed; integrated L4b updated |
| TD1 | Milan 5.5.4.2/Tables 5.44–5.45: invalid source returns TALKER_UNKNOWN_ID, valid source retains SUCCESS, neither changes talker state | talker:1301; suite:1187 tests 8 and 65535, defined identity fields, acceptance and no source actions; all three disconnect controls killed |
| VLAN | Milan 5.3.8.9/Table 5.38/5.4.2.10 and scope ruling: retain all 16 bits in settlement, storage and both readbacks; parent sees low 12 | package:152; listener:187/698/808/1300; top:1021/1042/1901/2714/3536; storage, settlement, external-GSI and parent-projection controls all killed |
| Probe guard/retry | Milan 5.5.3.5.16/.17/.18 and .25: match and retry the probe actually sent across same-talker controller replacement | listener:531/729/789/1340; field_cases.hpp:66/81/93; current-controller guard and retry controls killed; independent PW2/lifetime probe passes |

The response reduction selects equality results rather than multiplexing full controller values before comparison, and selects the controller octet before its source. Byte positions 12–19 select shifts 56 down to 0. The walker keeps those source registers stable during its 56-byte response build. A5 captures the sent controller into the private stream-ID word; A13 reuses it; A15 replaces it with the real stream ID. Published unsettled records mask that private value. Removing the unbind clear therefore does not disclose it or change the next probe. Timer, discovery, lock refusal, invalid-ID and nonmatching-response behavior were examined separately from the happy path.

The reviewer-owned [probe patch](scripts/reviewer-lifetimes.patch) adds 177 checks across all eight sinks, including rebind in PW2, rejection of the replacement controller, acceptance of the sent controller, distinct upper VLAN bits, zero/full VLAN values, unbind/rebind reuse, stale-response rejection and the published zero stream-ID view. It passes 3,344 checks in total ([receipt](receipts/reviewer-lifetimes.log)). The unmodified golden passes 3,167. These are focused simulation observations, not hardware proof.

**Area, interface stability and merge**

The [independent evidence audit](receipts/evidence-audit.json) reconstructs all six item patches against `09e357fb4bf3d35c8a9deba9a787e13f74d08c83`, compares every recorded HDL input hash, parses the raw utilization reports, and verifies the unchanged recipe. Baseline, merged and final source archives also match the published hashes byte-for-byte ([archive audit](receipts/source-archive-audit.json)). No local area synthesis or full portability bank was run.

| Variant | LUT | FF | Delta versus 09e357fb |
|---|---:|---:|---|
| Baseline | 21,614 | 18,908 | 0 / 0 |
| LD1 alone | 21,500 | 18,901 | −114 / −7 |
| LD2 alone | 21,613 | 18,908 | −1 / 0 |
| LD3 alone | 21,628 | 18,905 | +14 / −3 |
| TD1 alone | 21,614 | 18,908 | 0 / 0 |
| VLAN alone | 21,606 | 18,925 | −8 / +17 |
| Guard alone | 21,750 | 18,905 | +136 / −3 |
| Unreduced combined | 21,741 | 18,922 | +127 / +14 |
| Selected final implementation | 21,643 | 18,922 | **+29 / +14** |

The individual deltas sum to +27 LUT/+4 FF. The unreduced combined implementation exceeds that sum by +100/+10; synthesis results are not additive. The selected reduction saves 98 LUT and meets both +40 limits. The earlier +178/+18 figure belongs to the parked round-1b baseline, not the fresh round-2 comparison. Recipe: unchanged `syn/ooc/protocol_processor_ooc.tcl`, one input/one output, `xc7a100tfgg484-2`, eight synthesis threads, 10 ns post-synthesis clock, generated ROM inputs. These are OOC area measurements, not routed timing or physical qualification. Raw area reports and input identities are in the [published round-2 evidence](https://github.com/kebag-logic/milan-fpga/tree/1570e00395c98ed4ea1c21e6abde28948346c82b/review-evidence/pp168-r1/author/round2-recovery/area).

The first 1,000 top-level source lines, including public parameters and ports, are identical to 09e357fb. No host register-map implementation changed. The 384-bit internal record consumes four previously reserved bits for VLAN; this is the authorized internal change, not a public register-map expansion. The external VLAN output remains 12 bits per sink and the SRP service request uses bits 11:0. Only 13 source/test files differ from 09e357fb.

`fee74ef977b0a56a98c2b8a8677e25cfdf994c08` has parents `ba3f3f31e8fda01c3ef5271ff8005f3cf92ab4de` and `09e357fb4bf3d35c8a9deba9a787e13f74d08c83`; its recomputed merge diff is empty. The merged notification changes, cancellation controls, and shared suite changes were reviewed as part of the full requested diff. Public merge receipts show `aecp_notify` 67/67 and `pp_top` 10,470/10,470 passing at the merge revision; both also appear in the final full sweep. The local final-head notification suite independently passes 67/67.

**Executable coverage and limits**

| Evidence owner / scope | Result and receipt |
|---|---|
| Reviewer: three unmodified focused goldens | Listener 3,167; talker 1,376; integrated GSI 6,183 checks, all pass; [local summary](receipts/local-summary.json) |
| Reviewer: every added issue-168 control | 18/18 killed by all named assertions; three goldens pass; [campaign log](receipts/focused-fields.log), [per-arm results](receipts/fields/results.json) |
| Reviewer: merge-affected notification suite | 67/67, rc 0; [raw log](receipts/merged-notify-suite.log) |
| Reviewer: independent robustness probe | 3,344/3,344, including 177 added checks; [raw log](receipts/reviewer-lifetimes.log) |
| Reviewer: lint, documentation gates, explicit matrix check | All rc 0; [lint](receipts/local-lint.log), [make check](receipts/local-docs-check.log), [matrix](receipts/local-matrix.log) |
| Author: complete processor sweep | All 33 suites at both revisions; 1,028,293 baseline and 1,028,384 final checks, zero failures. Every suite tally and gate receipt is enumerated in [evidence-audit.json](receipts/evidence-audit.json) |
| Author: other processor gates | Lint, `make -j16 check`, `gen_matrix.py --check`, and `syn/yosys/run.sh` return zero at baseline and final. Portability receipt covers 42 tops and the AECP technology-mapping arm, with warnings disclosed |
| Author: all 13 affected campaigns | Both-revision receipts return zero; full ACMP campaign records 51 killed controls and six passing goldens; detailed comparisons preserve the documented clause-required changes |
| Author: parent consumers | 17 commands return zero at parent dev `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`, comparing the baseline and final processor pins. This is the author's scratch-parent evidence |

The affected campaign inventory covers talker retry; ACMP, GSI, D3, AECP dispatch, AECP, counters, notifications and name-write integration; ADP; MAAP; SRP top and admission. The interface-guard and NVM figure checks are included in the suite sweep; the descriptor-memory-guard-only campaign builds no changed module. The reviewer independently compared all 291 canonical records across the five published structured campaign pairs; they are identical after keying by arm ([comparison receipt](receipts/canonical-campaign-comparison.json)). The required notification failure witnesses remain present in the GSI campaign's changed traces. The GSI retained-status rewrite removes an obsolete notification wait; the public comparison explains its removed secondary timeout cascade and preserves the required notification failures. This was checked against the actual changed expectations, not accepted from aggregate return codes alone.

Hosted observations are recorded separately in [hosted-observation.json](receipts/hosted-observation.json). Both runs identify this exact head. The pull-request documentation and portability jobs completed successfully. The push portability job also succeeded, but its documentation job failed during dependency installation and its `make check` step was **SKIPPED**. Both suite jobs were still **IN_PROGRESS** at the recorded observation. No pending/skipped context is counted as executed success. Hosted/act acceptance belongs to the manager; no local container/act run was attempted.

There is **no manager source-bank run at this exact head**, and none is inferred from author receipts. The manager's donor bank (9), parent consumer bank (17), and builder/native checks belong to the final current-dev merge candidate, using source base `ed340b9b85258194247334b85e62cf9c23d4d051` and live dev `5603c353137e90c1fa95429f6d00ef7a2298d9ee`. The manager must publish that candidate's identity and receipts on the PR at the merge turn. The author parent at 6aa25dec is not that candidate.

Physical report calibration is **NOT RUN**: the author builder receipt explicitly ends with one unrun gate arm because the historical placement report is absent. The equal-clock inapplicability is separate. Field skips, a zero enclosing command status, simulation and OOC synthesis provide no hardware proof. Hardware was not accessed.

**Reviewer-owned final ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | Direct standards clauses; issue rulings; six RTL field paths and clause tests; normative F05.3/F05.11/F07.6 and GSI ownership; R553-F1/F2 remain | R553-1 | 96d3b78384f34a630d6056ebd8fa5e30f6836650 |
| RTL | CLEAN | Listener/talker/package and top VLAN path; private record publication; controller-byte selection; merged notification logic; exact source/area hashes and public boundary audit | R553-1 | 96d3b78384f34a630d6056ebd8fa5e30f6836650 |
| Robustness | CLEAN | Lock and invalid-ID refusal; same-talker rebind, retry, PW2, all eight sinks, stale responses, VLAN upper bits, reset/setup refusal and record reuse; local planted controls and additional probe | R553-1 | 96d3b78384f34a630d6056ebd8fa5e30f6836650 |
| Tests | CLEAN | Changed standalone/integrated expectations; 18 local controls and goldens; merged notification suite; 33-suite receipts, five processor gates, 13 campaigns and record comparisons; source archives verified | R553-1 | 96d3b78384f34a630d6056ebd8fa5e30f6836650 |
| Docs | UNCLEAN | Reading/authority guides, compliance matrix, architecture 02/05/06/07, integrator guide, suite READMEs, public handoff/PR and area claims; R553-F1/F2 remain | R553-1 | 96d3b78384f34a630d6056ebd8fa5e30f6836650 |

All five lenses were applied. CLEAN is limited to the examined source and evidence; it does not waive the documented pending manager duties or claim complete system/hardware validation. No SUGGESTION or RESIDUE finding is used to dilute the two substantive documentation findings.

**Packet and restoration**

The original detached clone was never modified. [Final tree verification](receipts/exact-tree.json) verifies all 582 tracked blob bytes and executable modes against the requested head, the exact index, and a clean working tree. This processor repository has zero submodule gitlinks. The author parent gitlink receipts name the baseline/final processor hashes explicitly; no other checkout was edited. All builds, temporary extracts and fault copies are under this packet's `scratch/`, which is excluded from publication. Local processes completed; measured peak memory was 5.38 GiB under the 12 GiB unit cap, with no memory-limit or out-of-memory events. No area run overlapped a build.

[reproduce.py](scripts/reproduce.py) repeats the focused foreground commands with bounded concurrency, [audit_evidence.py](scripts/audit_evidence.py) repeats the source/area/gate audit, and [verify_tree.py](scripts/verify_tree.py) verifies restoration. [fetch_public.py](scripts/fetch_public.py) refetches the immutable public artifacts and verifies the included public manifest before the evidence audit. The simulator identity was verified as the required 5.050 before use. `MANIFEST.sha256` lists every publishable receipt and script using packet-relative paths; unlisted downloads and all scratch trees are excluded. The manager publishes the report and listed files after terminal execution.

R553-1 FINISHED
