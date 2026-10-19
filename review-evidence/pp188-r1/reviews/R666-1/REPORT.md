[R666] NEGATIVE - exact head cb8bab044d98a89d8c4eb2b56bd81835e6fc5d48

Issue #188 + #189 / PR #195, round R666-1, 2026-10-19. Tree `a19fe4d05c3bfcab317780fe8e57f07f77c23469`. Reviewed the complete 28-file delta `b48312e1..cb8bab044d98a89d8c4eb2b56bd81835e6fc5d48`, its two author commits and the manager merge. The pending-Leave changes pass the focused review. The #189 completion condition remains unmet when type changes coalesce while the listener is busy. One MAJOR finding blocks acceptance; one RESIDUE finding is wording only.

Reconstruction followed the requested order: supplied instructions (no tracked AGENTS.md or CONTRIBUTING.md exists), docs/README and contributor/HDL guidance, frozen issue bodies and the [exact assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/188#issuecomment-6256482476), requirement/interface authorities, diff and history, then [published executable evidence](https://github.com/kebag-logic/milan-fpga/tree/5baa360ef77eeae71b897a7e5ed7aee01673c6f0/review-evidence/pp188-r1). Authorities examined include REQ-ACMP-011/016/018/022, F05.3/F05.14, the SRP service/status contracts in architecture/02, architecture/10 §6.4–6.5, and the independently transcribed applicant/registrar tables in the suites. The normative clause checks use the frozen public extracts and repository authorities; complete specification PDFs were not available in this checkout.

**R666-001 — MAJOR — Conformance, RTL, Robustness, Tests, Docs. REGISTERING_FAILED can permanently describe the first of two completed registration changes.**

Locations: `hdl/acmp/KL_pp_acmp_listener.sv:1169` (new SOK assignment), `:1030` (event payload capture), `hdl/top/protocol_processor_top.sv:3300` (payload-based failed input), `hdl/packet_engine/KL_pp_event_router.sv:165` (first-payload retention), `tb/pp_top/sim_main.cpp:10045` (new tests consume each change before sending the next), `docs/architecture/05_acmp_engine.md:317`, and the residual paragraph in the [PR description](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/195).

Authority: #189 and assignment item 2 require the flag to follow the registered declaration type **on every change**, including both in-place directions, without an added transition. Milan v1.2 §5.5.3.5.44 / Table 5.39 defines the flag by the registered type; Table 5.30 does not authorize a new state-machine arc. IEEE 802.1Q-2018 §35.2.6 permits replacement by the new declaration alone. No public maintainer scope decision waives delayed event consumption.

Reproduction uses only test changes, with every production RTL byte at the reviewed head. Start with a settled sink and a matching Advertise. Hold MAC TX ready low and send six GET_RX_STATE requests, spaced by 2 ms of simulated time. The four ordinary TX slots fill; the reserved slot remains free. Send a valid Failed MRPDU, then a separate valid Advertise MRPDU, separated by another 2 ms. Both reach the registrar. Resume TX, allow 50 ms to drain, then issue a fresh GET_RX_STATE. Repeat in the opposite direction from a matching Failed registration. These are separate received frames, not one MRPDU containing both types.

| Final registered type | Listener declaration | GET_RX_STATE flags after drain | Required flags |
|---|---|---|---|
| Advertise | Ready | `0x0042` | `0x0002` |
| Failed | Asking Failed | `0x0002` | `0x0042` |

The trace records exactly one delivered registration event with its coalesced flag set in each trial. A subsequent unchanged declaration refresh and another 500 ms do not correct the stale bit. With TX available, the identical compiled test delivers both events without coalescing and passes all 58 checks. With TX held, it completes all 58 checks and fails only the four current-type checks. All initial-state, slot-pressure, registration and trace preconditions pass.

Evidence: [test-only reproduction patch](receipts/reviewer-probes.patch), [stalled run](receipts/probe-pp_top.log), [positive control](receipts/probe-pp_top-no-stall.log), and their `.rc` files. The additional nine SRP robustness checks pass in [the stream probe](receipts/probe-srp_stream_fsms.log).

Impact: a controller can continue seeing failure after recovery, or miss a currently failed registration, after ordinary output backpressure has ended. The change repairs individually consumed events but cannot satisfy #189 using a potentially superseded event payload alone. First-payload coalescing predates this PR; this is an unresolved completion condition, not a claim that the PR introduced the router policy. The PR acknowledges a narrower residual involving changes within a few clocks in one MRPDU. The reproduced separate-frame, delayed-consumption case is broader. Architecture prose claiming that the bit follows the registered type is consequently not yet true throughout the required scope; this is substantive, not wording residue.

Required outcome: preserve or reconcile the current registered type when registration events coalesce, while retaining Table 5.30's no-transition behavior and the existing public interface contract. Add a regression and planted control for both delayed-consumption directions. Correct the architecture/PR description to match the completed behavior; merely documenting this exception does not satisfy the frozen acceptance condition.

Verification: both rows above must return the required flags after the queue drains and after an unchanged refresh. Run the same no-stall positive control, preserve the existing no-action/no-transition checks and all existing mutation kills, then provide the appropriate processor and parent acceptance receipts at the repaired head.

**R666-002 — RESIDUE — Docs, Tests. New explanatory source comments contain bench labels.**

Authority: owner comment rule dated 2026-10-15. This is confined to comment wording: no assertion name, expected value, generated artifact, measurement, clause claim or privacy rule needs to change. It does not independently make a lens unclean.

Exact fix, limited to comments introduced or rewritten in this delta:

| Location | Required wording edit |
|---|---|
| `tb/acmp_listener/sim_main.cpp:1178` | Remove the `B4: REF-BUG guard` prefix; describe the no-arc behavior directly. |
| `tb/pp_top/sim_main.cpp:10038` and `:10145` | Remove `AS5b, AS5c:` and `AS7:` from the explanatory headings. |
| `tb/srp_stream_fsms/sim_main.cpp:1072`, `:1092`, `:1117`, `:1133` | Remove section label `M.` and the `RB1`, `RB2`, `RB3` prefixes; retain the rebind/re-probe descriptions and issue/clause references. |
| `tb/srp_stream_fsms/walk_main.cpp:36` | Replace the `WK11` prefix with the behavior description, retaining issue #188. |
| `tb/srp_stream_fsms/walk_main.cpp:462` | Replace the comment with `Every sink but k was still declaring; sink k was already torn down.` |
| `tb/srp_stream_fsms/walk_main.cpp:530` | Delete `(WK11)`. |
| `tb/srp_top/mutants.py:162` | Delete `(walk_main.cpp WK11)` from the explanatory comment. |

Verification: inspect added comment lines against the owner rule. Keep executable check labels, mutation selectors and receipt strings unchanged. Existing unrelated labels remain outside this finding and under #746.

The following evidence supports the portions that passed:

| Examination | Artifact-specific result |
|---|---|
| #188 RTL and conformance | Old-value identity and FourPacked parameter survive the settle; new declaration requests wait; return to the same attribute reuses its applicant. The changed banner removes the abandonment policy. Registrar Δ13 logic and external interfaces are unchanged. Same-value New-before-tx correctly follows LA→VN; that is not cancellation by a different attribute value. |
| #188 robustness | Independent probes pass for a three-stream settle chain, return to the parked old stream, old AskingFailed/new Ready parameter separation, own LeaveAll followed by LO retirement, and reset while parked. Together with the ordinary suite: 1,361/1,361 checks pass. |
| Stream golden and mutation tests | Ordinary suite 1,352/1,352; walk shapes 1/1, 2/2, 3/5, 9/9 pass 38, 50, 74, 134 checks. All nine selected #188 mutations are killed by named RB/WK checks; campaign 11/11 including its two goldens. |
| ACMP golden and mutation tests | Listener suite 3,170/3,170; integrated ACMP-only phase 48/48. All six selected #188/#189 mutation entries are killed by their required named checks. These validate the added ordinary paths, but do not cover R666-001. |
| Merge preservation | Only the two specified mutant-list files conflict in the remerge display. SRP inventory is exactly the union of 129 and 141 parent entries, yielding 150; ACMP is the union of 57 and 54, yielding 60. Every patch applies or replacement anchor occurs exactly once. Both parents' mutation edits are preserved. The sole common-control expectation update changes teardown-as-declare from Listener Lv to VLAN release, as the changed behavior requires. See [inventory audit](receipts/merge-inventory.json) and [resolution diff](receipts/merge-resolution.diff). |
| Documentation gates | `make -j16 check` passes. The initial disposable archive lacked Git metadata and caused three inventory checks to refuse; the retry supplied exact-head metadata and passed. Both receipts are retained; the initial refusal is not counted as a product failure. |
| Source integrity | All 657 tracked blobs, executable modes and index entries match the exact head. The processor repository contains zero gitlinks. The six gitlinks at the supplied parent dev revision were read from public objects and recorded; no parent checkout was changed. See [integrity receipt](receipts/final-integrity.json). |

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN — R666-001 | Frozen issues/assignment; REQ-ACMP-011/016/018/022; F05.3/F05.14; SRP applicant/registrar tables and event/status contracts | R666-1 | cb8bab044d98a89d8c4eb2b56bd81835e6fc5d48 |
| RTL | UNCLEAN — R666-001 | Complete diff; both changed listener modules; top registration payload wiring; router capture/ack; unchanged transition ROM/interface | R666-1 | cb8bab044d98a89d8c4eb2b56bd81835e6fc5d48 |
| Robustness | UNCLEAN — R666-001 | Stalled event consumption in both directions, refresh persistence and positive control; repeated settles, identity return, parameter retention, own LeaveAll and reset | R666-1 | cb8bab044d98a89d8c4eb2b56bd81835e6fc5d48 |
| Tests | UNCLEAN — R666-001 | Focused goldens, 15 killed mutation entries, exact parent-union/anchor audit, independent passing and failing probes, published gate receipts | R666-1 | cb8bab044d98a89d8c4eb2b56bd81835e6fc5d48 |
| Docs | UNCLEAN — R666-001 | docs/README conventions; two architecture deltas; four suite READMEs; design banner; PR residual statement; generated receipt index and publication manifest | R666-1 | cb8bab044d98a89d8c4eb2b56bd81835e6fc5d48 |

The independent verdict and ledger were saved in [the independent-pass checkpoint](receipts/independent-verdict.md) before checking prior reviewer findings. The subsequent public queries found zero submitted reviews, zero inline review comments and only two review-start conversation notices on PR #195. There are no prior public FINDINGS to resolve or retain in that snapshot. No other reviewer's report was read.

**Evidence provenance, limits and pending manager duties**

All 500 files in the published evidence manifest match their published SHA-256 digests. The index covers exactly the other 499 files. For 497 unredacted entries, byte counts and hash prefixes match directly; the two redacted entries reconcile through the publication manifest's original/published hashes. Their original bytes were not accessed. [Publication verification](receipts/public-evidence-verified.json), [index audit](receipts/index-audit.json), and [author return codes](receipts/author-return-codes.json) preserve the checks. Large external/per-arm logs represented only by hash inventories were not independently opened or regraded.

The author's full processor records identify base `5addf297` and head `dc01aec4`, with 1,030,013 and 1,030,026 suite checks respectively and successful final gate statuses. The SRP campaigns were retained from `bacfb90` with the published byte-equivalence explanation; they are not newly executed at `cb8bab04`. Parent consumer records use dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`, the staged processor pin and the two assignment patches. Their documented pin check fails identically before adoption. Initial setup/refusal attempts and the interrupted compile-lock wait are retained separately; the dedicated OOC reruns pass. Builder physical calibration is **NOT RUN**. Field skips and software receipt success are not hardware proof.

At the hosted snapshot, exact-head runs 39223615550 and 39223608580 each have successful docs-gates and portability jobs, while suites remain in progress. These are the actual executed-job statuses; they do not establish overall hosted acceptance. See [hosted summary](receipts/hosted-summary.json). No manager source bank was run or inferred. The public issue/PR comments examined supplied assignment and review-start notices, not a manager exact-head bank receipt.

This review ran focused simulations, selected mutation campaigns and documentation checks only. No full processor/parent/timing/synthesis/builder bank, hardware operation, shared installation, repository fix, commit, push, merge or GitHub write was performed. Independent campaigns ran concurrently in a foreground-owned runner, each with a log and status file, two campaign workers and two compiler workers per build. Disposable copies and raw build receipts are confined to `scratch/` and are not published. Published log copies redact host path prefixes only; [the publication map](receipts/publication-map.json) binds each to its preserved raw digest.

The manager must obtain the R666-001 repair and renewed independent acceptance, carry R666-002 to the residue checklist, complete hosted/host-run acceptance, and build/test the final current-dev merge candidate with linked receipts at the merge turn. Source validation and that candidate validation remain distinct: source base `b48312e1`, supplied live dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`. The source verdict here is not merge authorization.

Portable reproduction: run `scripts/setup.py SOURCE PACKET SIMULATOR` with the scoped 5.050 compiler; then `scripts/run_focused.py PACKET/scratch/source PACKET PACKET/scratch/bin/verilator`. Run `scripts/prepare_probes.py SOURCE PACKET`, `scripts/run_probes.py PACKET`, and `scripts/run_probe_control.py PACKET`. The stalled run is expected to return 1 at this head; the no-stall control returns 0. `scripts/check_merge.py`, `scripts/audit_evidence.py` (after `fetch_evidence.py`) and `scripts/verify_integrity.py` reproduce the corresponding audits. Only files listed in MANIFEST.sha256 and REPORT.md are publishable.

R666-1 FINISHED
