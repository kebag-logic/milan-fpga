[R513] NEGATIVE - exact head 75c4eee4589e9317aca3d07b91f94a38b4cc86af

Issue [#69](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/69), PR [#165](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/165), round R513-2. Tree `43f1dbf62f8151c5ad158546494174fd434032c3`.

One MINOR remains: the counter-stamp storage formula in the architecture table omits the second interface. Docs is UNCLEAN; the other four lenses are CLEAN for this scoped source review. The three prior internal-review findings are resolved at this head. No new implementation defect was established by this review.

**Reconstruction and independence.** The supplied workspace instruction was read first; no applicable repository/ancestor AGENTS.md or CONTRIBUTING.md was present. Next came docs/README, the issue body and public maintainer/manager scope decisions, the linked requirements and interface/timer authorities, the complete `e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8..75c4eee4589e9317aca3d07b91f94a38b4cc86af` diff and history, then public evidence. The three round-2 commits are `3323904`, `fc9bc43`, and `75c4eee`, above `cb730a2f9dd7e4f60a03a38d4b47b569e68da8df`. The inherited #134 SRP expiry changes and #22 declaration moves were examined separately from the interface seam.

The [independent verdict and five-lens ledger](receipts/independent-verdict.md) were written before reading prior public reviewer reports/findings. No private author material, management checkout, lane scratchpad, other checkout, or subordinate reviewer was used. Public scope snapshots are in [receipts/public](receipts/public/); the [diff](receipts/base-to-head.diff) and [history](receipts/history.txt) are retained.

The controlling assignments are [6010216843](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/69#issuecomment-6010216843) and [6016201199](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/69#issuecomment-6016201199). They require a usable two-interface extension seam and preservation of the shipping count-one implementation. The non-redundant product scope remains: this review does not certify redundant wire egress or hardware conformance. Clause assessment uses the public assignments and the repository's cited requirements; no independently obtained standards PDF was used.

**Open finding R513-2-F1 — MINOR — Docs.**

- **Artifact:** `docs/architecture/06_aecp_engine.md:931`, the `ctr_last_r` row in the storage table revised in this round. Supporting implementation: `hdl/aecp/KL_aecp_notify.sv:435` and `:446`.
- **Authority/evidence:** The table says `(streams in + out + 2) × 32 bits`. The implemented extent is `N_STREAM_IN_P + N_STREAM_OUT_P + 1 + N_IF_P`, and the array contains that many 32-bit stamps. The table now explicitly parameterizes the registry and identity arrays by interface count, but retains the old counter formula without a count-one restriction. Section 6.6 of the same document correctly includes AVB_INTERFACE 1. See the exact excerpts and arithmetic in [storage-shape.txt](receipts/storage-shape.txt); CK1–CK5 also exercise the distinct counter slots.
- **Impact:** At count two, the architecture understates storage by one 32-bit stamp. For an 8/8 shape the declaration has 19 stamps/608 bits while the table describes 18/576. These are array dimensions, not a physical utilization measurement. Count one is correctly described.
- **Required outcome:** Replace the Shape cell with `(streams in + out + 1 + P-N-AVB-INTERFACES) × 32 bits`, or explicitly limit the old formula to count one and provide the count-two formula. No RTL change is requested.
- **Verification:** Compare the documented extent to `N_CTR_DESC_C` and `ctr_last_r` at both legal interface counts; rerun the documentation gate. The current gate passes because it does not validate this numerical formula.

This is MINOR rather than RESIDUE: the correction changes a numerical storage claim. It is not solely a wording improvement. No BLOCKER, MAJOR, additional MINOR, RESIDUE, or SUGGESTION is raised.

**Prior public findings — all resolved at this head.** The prior report is [comment 6016189510](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/165#issuecomment-6016189510); the earlier external report is [6016101360](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/165#issuecomment-6016101360). Review submissions and inline-comment inventories were empty. Their disposition is recorded separately in [prior-findings.json](receipts/public/prior-findings.json).

| Prior item | Exact-head disposition and evidence |
|---|---|
| R512-1 F1 — RTL, Robustness, Tests | **RESOLVED.** Notify `g_ca_turns` (`:717–791`) combines all hit live probes and the TIME_LIMITED drain into pending cancellations, removes only the emitted bit, and drains one owner per clock. Report routing requires a live, non-superseded probe. Shared owners wait for their current probe/cancel and the settling interval. CA1 covers both probes of E; CA1b covers simultaneous drain/command cancellation; CA2–CA4 cover orphan reports, owner turns and settling. The corresponding five controls all fail their specified checks. |
| R512-1 F2 — Tests, Docs | **RESOLVED.** `tb/pp_top/interface_phases.hpp:127` holds the MAC TX, receives REGISTER/DEREGISTER on interface 1 followed by a frame on interface 0, then releases execution. The checks at `:224` give the rows unequal unsolicited sequence IDs and identify the surviving row by sequence 5 rather than 3. P1 (`rgy_port_from_latest_frame`) fails IF3 and IF3b; P2 (`dereg_matches_other_port`) fails IF3b in the top-level build. The README and 09 §8.9 describe this stimulus and result accurately. |
| R512-1 F3 — Conformance, Docs | **RESOLVED.** Notify `:364` derives `N_ROW_C = N_CTRL_P * N_IF_P`; row allocation is restricted to the incoming port, while timer owners use the controller index and expiry decoding recovers the port from the slot. F01.5, REQ-SCP-003 and REQ-AEM-016 now consistently state per-interface depth. PD1–PD3 and their five controls pass/kill as required. The independent production-depth probe additionally fills all 32 rows and checks both interfaces' seventeenth-entry refusal. |
| R512-1 S1 — Tests suggestion | **RESOLVED.** The current PR body enumerates 70 retry arms, 20 GSI arms, three admission arms and one name-write arm, plus two BFM anchors: 94 arms and two anchors. It no longer presents these as 96 distinct mutations. |
| R513-1 | No open finding to retain. Its count-one and unchanged-seam evidence remains relevant; this round independently examines the expanded depth/cancellation implementation and strengthened IF checks. The new storage-table finding above applies to this exact-head report. |

**Acceptance and implementation assessment.**

| Area | Evidence and judgment |
|---|---|
| Top parameter and ingress interface | `hdl/top/protocol_processor_top.sv:106,236,874,1553,1721,1974` exposes the count, sizes the timer map, enforces 1/2, captures the final-byte interface with the matching header, passes it through the normalizer, and binds ADP. The interface guards accept 1/2 cleanly and reject 0/3 by name. |
| Registry command provenance | Top `:4011` captures the interface on the engine's command handshake and supplies `rgy_port_i`; notify `:548` latches and compares it with the registry tuple. The internal port is necessary to communicate the requested tuple; the integration boundary still gains only the requested input with default zero. |
| Per-interface registry depth and timers | The 32-row production-depth probe verifies each port's capacity, all 16 owner indices, all 32 registration/monitor slots, responses, failures, replacement and TIME_LIMITED expiry. The timer map already reserves `2 * n_ctrl * n_if`. The owner/tag widths remain unchanged. |
| Availability cancellation and late reports | The two-interface cancellation state is generated only above one. The originator gives responses priority over parked cancels, with registered reports; the top supplies at most one response per received frame. The three-cycle settling interval prevents immediate owner reuse while the cancelled exchange's last report can arrive. CA4 deliberately injects the raced response two cycles after cancellation. This was assessed against the actual originator/builder wiring, not inferred solely from the module test. |
| Counter keying and explicit limits | AVB_INTERFACE 1 receives its own pending/throttle slot after CLOCK_DOMAIN 0. CK1–CK5 cover independent windows and invalid indices. Actual counter banks remain the integrator's behind descriptor-indexed reads. Shared MAC trunks without an egress index, shared link/GM/domain levels, one SRP participant set, cross-interface EID/MAC monitoring, interface-zero AVB-info/path pushes and interface-zero snapshots are explicitly named in REQ-SCP-003. |
| Count-one identity | Static inspection shows the new port storage, cancellation queue, owner turns and settling are excluded at one interface; the one-interface expressions retain the previous behavior. The public PR reports identical cell counts at main `86a7b0c5`, round-one `cb730a2f` and this head. It explicitly distinguishes cell identity from statistics-file identity: 40/42 files byte-identical, with remaining wire-counter changes. Its paired OOC result is 23,179 LUT / 19,779 FF at both main `86a7b0c5` and this head, delta **0 LUT / 0 FF**. These synthesis/physical figures are attributed evidence, not new reviewer measurements. Comparing directly to `e6a759de` also includes unrelated merged #134 changes; those must not be misattributed to the seam. |

**The pre-existing count-one gap is honestly and correctly scoped.** Public [processor issue #167](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/167) records the same-cycle drain/command cancel loss, its late-failure consequence, and a separate acceptance plan with an area allowance. The count-one branch still selects the drain over a simultaneous command cancellation, as before this PR. Preserving it here follows the explicit count-one identity requirement; fixing it would be separate work. At count two, CA1b and its failing control establish that both cancellations are sent. This distinction does not turn the known count-one defect into a claim of defect-free operation. The [issue snapshot](receipts/issue167.json) is retained.

**Independent executable evidence.** Foreground coordinators waited for all children. Independent suites and the campaign ran concurrently, each with its own log/status file; campaign jobs were explicit, make used `-j16`, and native builds were bounded to three workers each, at most fifteen combined. Disposable files stayed under this packet's `scratch/`. The required pinned simulator reported 5.050 before use; its [identity receipt](receipts/simulator-identity.json) records launcher/executable hashes. No physical build ran.

| Check | Result | Receipt |
|---|---|---|
| ADP, both builds | 1,359 checks, zero failures: 1,348 shipping + 11 IF | [adp-suite.log](receipts/adp-suite.log) |
| Notification, three builds | 64 checks, zero failures: 41 shipping + 4 identify + 19 PT/CK/PD/CA | [notify-suite.log](receipts/notify-suite.log) |
| Top IF golden | Six checks, zero failures, including IF3/IF3b | [golden log](receipts/round2-controls/golden-pp_top-obj_if2_Vpp_top_if2.log) |
| Round-two controls | 12/12 killed; both goldens pass; every build succeeds and every named failure is present | [results.json](receipts/round2-controls/results.json) |
| Interface elaboration guards | Four cases pass: 1/2 clean, 0/3 refused by name | [interface-guards.log](receipts/interface-guards.log) |
| Independent full-depth probe | 448 checks, zero failures across all 32 rows at 16 controllers per interface | [capacity-probe.log](receipts/capacity-probe.log) |
| Notification anchor/context audit | 77 control arms and three refreshed patches, zero refusals | [plant-audit.json](receipts/plant-audit.json) |
| Documentation gate | PASS, including parameters, IDs, figures, links and matrices; diagram 21 rendered and visually inspected | [docs-check-metadata.log](receipts/docs-check-metadata.log) |

The individual round-two kills are:

| Control | Required failed checks observed |
|---|---|
| `cancel_one_per_command` | CA1, CA1b |
| `report_fail_ignores_probe` | CA2, CA3 |
| `report_rsp_ignores_probe` | CA2 |
| `owner_turns_dropped` | CA3, CA4 |
| `settle_dropped` | CA4 |
| `depth_shared` | PD1 |
| `depth_not_keyed` | PD1 |
| `registry_tag_port_bits` | PD2 |
| `monitor_tag_port_bits` | PD2 |
| `expiry_port_dropped` | PD3 |
| `rgy_port_from_latest_frame` | IF3, IF3b |
| `dereg_matches_other_port` | IF3b |

The initial documentation invocation failed because a source archive had no Git metadata. After adding metadata in the disposable tree, the gate passed. Both [initial log](receipts/docs-check.log) and successful rerun are retained; that setup error is not a source finding. The ordinary probe copies' implementation bytes were also [compared with the clone](receipts/probe-source-integrity.json). The capacity probe models the registry's peer services; it does not substitute for integrated physical execution.

**Reviewer-owned ledger.** Each status covers this scoped source review and the exact head below.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen issue and both assignments; F01.5, Δ12, REQ-SCP-003, REQ-AEM-016; 02 RX contract, 06 registry/counters, 07 records, F08.4 timer map; PD/IF and production-depth results | R513-2 | 75c4eee4589e9317aca3d07b91f94a38b4cc86af |
| RTL | CLEAN | Complete diff/history; top ingress/command latches and ADP binding; notify depth, port RAM, owner/tag routing, cancel queue and reports; actual originator/builder connections; inherited SRP and declaration changes | R513-2 | 75c4eee4589e9317aca3d07b91f94a38b4cc86af |
| Robustness | CLEAN | CA1/CA1b/CA2/CA3/CA4 and their controls; shared-owner turns, settling, simultaneous cancellation; per-interface exhaustion/reuse; all 32 timer/response/failure routes; scoped public issue #167 | R513-2 | 75c4eee4589e9317aca3d07b91f94a38b4cc86af |
| Tests | CLEAN | Three IF-related benches/wrappers/Makefiles and guards; 12 executed controls; 77-arm planting audit; independent 448-check probe; public evidence attribution and prior-finding reconciliation | R513-2 | 75c4eee4589e9317aca3d07b91f94a38b4cc86af |
| Docs | UNCLEAN (R513-2-F1) | docs/README conventions; banners; 00/01/02/06/09, inherited SRP text; integrator guide and rendered diagram 21; suite READMEs; passing docs gate; incorrect counter-stamp geometry at 06:931 | R513-2 | 75c4eee4589e9317aca3d07b91f94a38b4cc86af |

**Public evidence, limits and pending manager duties.** The fixed [public packet](https://github.com/kebag-logic/milan-fpga/tree/83221a43e3d1f5922143becbaba0661fef2c201b/review-evidence/pp69-r1) was read after the independent diff pass; all three published file hashes match its manifest. It contains first-round author summaries and a consumer patch, covering processor `d723574`, not executable raw round-two bank receipts. The files are preserved under [public-evidence](receipts/public-evidence/). The current PR body supplies round-two validation/identity summaries. The task states that the manager's complete source static/builder and native banks passed at this head; this is manager-supplied evidence, distinct from my executions. No additional bank-results comment was present in the retrieved issue/PR snapshots.

At the hosted snapshot, [run 37522488885](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/37522488885) is associated with the exact head. Docs-gates and portability completed successfully, including their substantive steps. The suites job was still running; its later campaigns were pending. The cached simulator-build step was skipped. This is not an all-workflow PASS. Raw [job/step evidence](receipts/public/workflow-jobs.json) is retained; hosted acceptance belongs to the manager.

No full parent/processor/time-sync/synthesis/builder banks, container acceptance, physical calibration, field run or hardware test was performed here. Physical calibration remains **NOT RUN**; field skips are not hardware proof. OOC identity and broad bank results were not independently rerun. The implementation checks are focused and do not establish exhaustive behavior.

The manager must carry R513-2-F1 for correction and exact-head re-review, publish/link the source-bank receipts, obtain the other independent verdict, and complete hosted/container acceptance under the manager's rules. Processor main #42 is a future merge delta: retain its DN section/nine controls and this PR's IF/PD/CA work, then review the actual changed artifacts at the resulting head. Earlier judgments remain evidence for untouched artifacts, not acceptance of an unexamined merge.

At the merge turn, build and validate the final current-dev candidate. The source base is `e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8`; the supplied live dev is `6a05347d4e2ec1dcb37d4e5806c7767537de3ce0`. Source validation does not certify that future candidate or authorize its merge.

**Integrity and publication.** All 581 tracked blob bytes and executable/symlink modes, all index entries, detached HEAD and tree match the exact published head; worktree status is clean. This processor tree has no submodule gitlinks, so the required-gitlink inventory is empty. See [checkout-integrity.json](receipts/checkout-integrity.json). No source fixes, commits, pushes, merges, external writes or author contact occurred. [Portable reproduction scripts](scripts/README.md), raw receipts and this report are in the designated packet. Only REPORT.md and relative paths listed in MANIFEST.sha256 are designated for publication; scratch is excluded.

R513-2 FINISHED
