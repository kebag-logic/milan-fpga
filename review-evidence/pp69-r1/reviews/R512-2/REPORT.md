[R512] NEGATIVE - exact head 75c4eee4589e9317aca3d07b91f94a38b4cc86af

Independent internal review of issue #69 / PR #165, round R512-2. Tree `43f1dbf62f8151c5ad158546494174fd434032c3`; source base `e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8`.

The three R512-1 findings are resolved. One remaining **MINOR, R512-2-F4**, concerns the numeric storage shape documented for counter stamps. Conformance, RTL, Robustness and Tests are CLEAN; Docs is UNCLEAN. No new functional defect was established. There is no wording-only RESIDUE.

## Reconstruction and independence

I read the supplied workspace instruction, checked applicable ancestor/repository guidance (no AGENTS.md or CONTRIBUTING.md file was present), then read docs/README and the repository entry points. Next came the [issue body](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/69), the [frozen assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/69#issuecomment-6010216843), the [round-two decision](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/69#issuecomment-6016201199), and linked architecture/interface authorities. I then examined the base-to-head diff and history before the public executable-evidence material and prior public findings.

The independent source-pass checkpoint is `receipts/independent-pass.md`. My own verdict and five-lens ledger were written in `receipts/reviewer-verdict-ledger-before-peer.md` before reading the other reviewer's public report. No private author material, management checkout, private reviewer packet, author contact, external write or delegated review was used.

The history distinguishes the original seam work, merge `cb730a2f` bringing #134/#22, and the three round-two commits `3323904`, `fc9bc43`, `75c4eee`. The inherited registrar expiry/receive priorities and packet declaration moves were inspected separately; they are unchanged by round two. The [next merge assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/69#issuecomment-6024309003), bringing processor main `2ad2f845` (#42), is a future delta and is not covered by this exact-head verdict.

## Open finding

### R512-2-F4 — MINOR — counter-stamp storage shape omits the second interface

- **All attributable lenses:** Docs.
- **Location:** `docs/architecture/06_aecp_engine.md:931`, the `GET_COUNTERS stamps ctr_last_r` row in the storage table. The table now describes the interface-count-dependent row table, port storage, cancellation bits and identity index at `:925–928`, but the stamp row still gives `(streams in + out + 2) × 32 bits` without restricting it to count one.
- **Authority/evidence:** `hdl/aecp/KL_aecp_notify.sv:435` defines `N_CTR_DESC_C = N_STREAM_IN_P + N_STREAM_OUT_P + 1 + N_IF_P`; `:446` allocates one 32-bit stamp per descriptor. REQ-SCP-003 and section 6.6 correctly describe one counter-notification slot per AVB interface. The independently built two-interface, one-input/one-output model contains five 32-bit stamps; the table's expression gives four. At the ordinary eight-input/eight-output shape, count two has 19 stamps, while the table gives 18. See `receipts/storage-shape.txt` and `scripts/storage-shape.py`.
- **Impact:** the current architecture table understates this storage by 32 bits at two interfaces and disagrees with the interface-keyed RTL. This is a numerical shape claim, so it does not qualify as wording-only RESIDUE. It does not invalidate the measured count-one identity or any behavioral result.
- **Required outcome:** replace the shape with `(streams in + out + 1 + P-N-AVB-INTERFACES) × 32 bits`, or explicitly scope the old expression to count one and give the count-two expression beside it. No RTL change is required.
- **Verification:** the corrected expression yields 18/19 stamps at eight-in/eight-out for counts one/two, and four/five at one-in/one-out. Review against `N_CTR_DESC_C` and rerun the documentation gates. Existing gates pass without detecting this semantic mismatch.

This stale row originated in the earlier seam change and remains in the storage table updated in round two. It was not raised in the previous review; the three previous findings are nevertheless closed independently below.

## Prior public findings, explicitly disposed at this head

The [R512-1 findings](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/165#issuecomment-6016189510) were read after my independent diff pass. Formal review submissions and inline review comments were both empty in the fetched inventory. The prior external public review contained no findings to retain; it was read only after my own verdict/ledger checkpoint.

| Prior ID and lenses | Disposition at this head | Artifact-specific evidence |
|---|---|---|
| R512-1 F1 — RTL, Robustness, Tests | RESOLVED | `KL_aecp_notify.sv:714–788`: pending bits accumulate every hit and drain one cancellation per cycle; owner turns and the post-cancel wait prevent premature reuse; reports require a live probe and reject a same-cycle command hit. CA1 cancels both live owners of the same controller. CA1b sends both the drain and command cancellation. CA2 rejects late failure/response effects; CA3/CA4 cover shared owners and the wait. All five associated cancellation/report/owner controls fail their named checks. |
| R512-1 F2 — Tests, Docs | RESOLVED | `tb/pp_top/interface_phases.hpp:129–254`: the held REGISTER and DEREGISTER on interface 1 execute after a frame on interface 0. Unequal unsolicited sequence IDs distinguish which registration survives. P1 (`rgy_port_from_latest_frame`) fails IF3 and IF3b; P2 (`dereg_matches_other_port`) fails IF3b. Both finish their simulation tallies with a successful build. The README and 09 §8.9 accurately describe these checks. |
| R512-1 F3 — Conformance, Docs | RESOLVED | `KL_aecp_notify.sv:358–376,544–568,891–917,1520–1595`: capacity is `N_CTRL_P * N_IF_P`, allocation is restricted to the command's port, and timer owner/index decoding preserves the port through the slot. PD1–PD3 and their five controls pass/are killed as required. An independent default-depth probe accepts 16 registrations per interface, refuses each seventeenth, emits 32 initial-sequence notifications, and proves a freed port-1 row cannot refill port 0. F01.5, REQ-SCP-003 and REQ-AEM-016 now agree. |
| R512-1 S1 — Tests suggestion | RESOLVED | The current PR body distinguishes 94 exact-text arms from two BFM observation anchors and enumerates their owners. `tb/acmp_talker/retry_mutants.py:342–347` contains the two observation insertions. The historical 96 count is no longer presented as 96 distinct mutations. |

The originator timing was checked beyond the unit oracle: top `:1198–1203` supplies responses directly from the validator's header pulse, not a queued response stream; `KL_pp_originator.sv:300–309` prioritizes response over parked cancellation, and its action registers report on the following cycle. The count-two wait and live-probe qualification cover the late-report interval for this landed connection. CA4's injected response two cycles after cancellation exercises that boundary. This is a bounded interface review, not exhaustive formal proof.

## Acceptance and scope

The issue's frozen acceptance items 1–7 are met: the top exposes and threads the count, the registry stores the port, count two is built and checked, and REQ-SCP-003 names the actual seam. The manager's additional functional requirements are met; F4 leaves the documentation completion bar open.

The top parameter defaults to one and admits only one/two; the final-byte interface sample follows the matching header acceptance condition, then the transaction carries the index. `aecp_cmd_if_r` uses the command acceptance handshake, which matches the AECP engine's `cmd_r` load. ADP gets one advertise machine per interface. The internal `rgy_port_i` is necessary to deliver the command's interface to the separate registry, while the external boundary gains only `rx_if_index_i`. AVB_INTERFACE notifications have independent slots/windows and retain the existing index-zero/CLOCK_DOMAIN positions.

The explicitly unkeyed trunks, class-D levels, SRP participant, availability identity matching, AVB-info/path pushes and interface-zero snapshot exports remain acceptable seam limits. Neither the documents nor this review certify a complete redundant product.

**Count one and the retained cancellation gap.** The independent registry comparison finds **25,731 cells at both base and head, every cell-type count identical**. Full statistics files are not byte-identical: the new port and intermediate wires change port/wire counters, as the PR body discloses. See `receipts/count1-stat-comparison.json` and raw `stat-base`/`stat-head` receipts. The existing ADP and registry build tallies remain 1,348 and 41+4 respectively.

The same-cycle count-one drain/command cancellation gap is honestly scoped to [processor issue #167](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/167). My identical diagnostic on source base and this head produces two live probes, only owner-zero's cancellation, then deletion of the surviving row by owner one's orphan failure. The source change preserves that path; CA1b covers its correction at count two. Deferring the count-one repair is consistent with this assignment's unchanged-count-one requirement and the separate issue's explicit resource budget. This is acknowledged existing debt, not a claim that count one is defect-free.

## Executed checks and receipts

All independent campaigns, suites and builds used foreground coordinators that joined their children, explicit campaign concurrency and bounded compilation. Disposable copies and temporary files remained under `scratch/`. The assigned simulator identity was checked before use (`receipts/simulator-identity.json`). No full parent/processor/static/builder bank or physical build was run.

| Execution | Result | Receipt |
|---|---|---|
| ADP suite, both builds | 1,359 checks; 1,348 shipping + 11 interface; zero failures | `receipts/adp-suite.log`, `.rc` |
| Registry suite, all three builds | 64 checks; 41 + 4 + 19; zero failures | `receipts/registry-suite.log`, `.rc` |
| Top interface golden | IF 6 checks, zero failures | `receipts/top-controls/golden-pp_top-obj_if2_Vpp_top_if2.log` |
| Top legal-range guards | counts 1/2 clean; 0/3 refused by the named parameter guard | `receipts/interface-guards.log`, `.rc` |
| Ten new PD/CA controls | 10/10 killed by every required named check; golden passes | `receipts/registry-controls/results.json`, individual raw logs |
| P1/P2 top controls | 2/2 killed; golden passes | `receipts/top-controls/results.json`, individual raw logs |
| Independent 16-per-interface capacity/fanout/refill | 3/3 checks pass | `receipts/depth16.log`, `.rc` |
| Count-one baseline-gap diagnostic at base/head | matching traces; four diagnostic expectations pass at each | `receipts/count1-base.log`, `count1-head.log`, `.rc` |
| Focused count-one registry statistics | every cell count identical | `receipts/count1-stat-comparison.json`, `stat-base/`, `stat-head/` |
| Patch/exact-anchor audit | 298/298 patch files apply; 77/77 notification arms plant | `receipts/plant-check.json`, `.log`, `.rc` |
| Documentation gates | all pass, including 41 diagram blocks, 18 waveform blocks, IDs, figures, parameters and matrices | `receipts/docs-check.log`, `.rc` |
| Diagram 21 | rendered and visually inspected; no observed clipping/overlap | `receipts/diagram-inspection.txt` |

An initial count-one diagnostic omitted servicing the initial random draws, so no probes had issued. Both base/head setup checks failed. That reviewer-harness error was corrected, and the initial receipts are preserved as `*-setup-initial`; `receipts/probe-setup-note.txt` explains it. No source defect is inferred from those setup failures.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen issue/assignments; Milan clauses as quoted by repository authorities; Δ12, F01.5, REQ-SCP-003, REQ-AEM-016, F08.4; ADP/per-interface counter scope; capacity and timer probes | R512-2, R512-1 F3 resolved | 75c4eee4589e9317aca3d07b91f94a38b4cc86af |
| RTL | CLEAN | Full base-to-head diff/history; top sample and command handshakes; registry allocation, cancellation, owner turns, timer/report routing; originator/builder; count-one statistics; inherited #134/#22 changes | R512-2, R512-1 F1 resolved | 75c4eee4589e9317aca3d07b91f94a38b4cc86af |
| Robustness | CLEAN | Multi-hit and drain collisions; late response/failure; shared-owner reuse; post-cancel wait; overflow/port-local refill; range guards; independently reproduced pre-existing count-one debt | R512-2, R512-1 F1 resolved | 75c4eee4589e9317aca3d07b91f94a38b4cc86af |
| Tests | CLEAN | ADP IF; PT/CK/PD/CA; top held-command IF; all twelve new negative controls; Makefiles and guard driver; independent 32-row probe; patch/anchor audit | R512-2, R512-1 F1/F2 resolved | 75c4eee4589e9317aca3d07b91f94a38b4cc86af |
| Docs | UNCLEAN — F4 | docs/README; banners; 00/01/02/06/09; inherited SRP text; integrator guide/diagram; three suite READMEs; PR body; storage-shape comparison and document gates | R512-2, R512-1 F2/F3 resolved; F4 open | 75c4eee4589e9317aca3d07b91f94a38b4cc86af |

## Evidence limits and pending manager duties

The fixed [public evidence directory](https://github.com/kebag-logic/milan-fpga/tree/83221a43e3d1f5922143becbaba0661fef2c201b/review-evidence/pp69-r1) contains the earlier public author handoff, PR body and parent patch. All three published hashes match. It does not contain raw round-two manager banks. The current PR body reports count-one cell identity across 42 tops and OOC 1x1 **23,179 LUT / 19,779 FF at both main `86a7b0c5` and this head, delta 0/0**. The earlier base comparison reported 23,211/19,777 at both endpoints. Those are different source comparisons; the inherited #134 change must not be misattributed to this seam. I did not independently rerun the OOC measurement or all-top census.

The assignment states that the manager's full source static/builder and native banks passed at this exact head. I accept that as supplied manager evidence, distinct from my executions. The fetched issue/PR comments contain the assignments, readiness/start notices and prior reviews, but no additional raw bank-results comment. Publishing/linking those exact-head receipts remains a manager duty, not an inferred source failure.

For the [exact-head hosted run](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/37522488885), docs-gates and portability completed successfully and their substantive steps executed. At the recorded snapshot, suites were still running; subsequent campaigns were pending. The cached simulator build step was skipped. No pending/skipped context is counted as a passing test or complete workflow. Hosted/container acceptance belongs to the manager; no container execution was attempted here.

Standards PDFs were not available in this checkout; clause interpretation uses the repository's published quotations and frozen scope. Focused simulation is not exhaustive proof. **Physical calibration was NOT RUN. Field skips are not hardware proof.**

The manager must obtain F4's documentation correction and exact-head review closure, review the #42/main merge as a delta while preserving both sets of tests/controls, complete hosted acceptance and the other independent review, and build the final current-dev candidate at the merge turn. Source validation at base `e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8` is distinct from the candidate against live dev `6a05347d4e2ec1dcb37d4e5806c7767537de3ce0`. This review does not certify that future candidate.

All **581 tracked blobs and modes and 581 index entries** match the published head. Status is clean; the required submodule-gitlink inventory is empty. See `receipts/checkout-integrity.json`. No source fixes, commits, pushes or merges occurred. Portable scripts and raw receipts are listed with relative paths in `MANIFEST.sha256`; `scratch/` is excluded from publication.

R512-2 FINISHED
