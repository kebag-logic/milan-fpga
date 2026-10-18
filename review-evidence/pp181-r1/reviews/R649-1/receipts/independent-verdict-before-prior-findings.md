[R649] NEGATIVE - exact head 42eb9aef3642f6d98058fe634a70f6a9c749cd25

Independent review of issue #181 / PR #187, round R649-1. Tree: `f7319d373b083043cf896a68712302f640212838`. The blocking finding is missing public executable evidence, not an observed functional regression. Focused execution passes, including queue-boundary probes and six fault controls.

## Authority and scope

The checkout has neither AGENTS.md nor CONTRIBUTING.md. The supplied workspace instructions and `docs/README.md` govern this review. The frozen assignment is [issue #181](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/181), including its assignment comment. The [replacement ruling](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/181#issuecomment-6249065327) replaces depth-halving with the requirement that this cone no longer limit the shipping timing gate. Failure to halve the depth is therefore **not** a finding.

Behavior authorities examined: Milan v1.2 §5.4.5 and IEEE 1722.1-2021 §7.5.2 as identified in the assignment and repository's requirement interpretation; `docs/00_MILAN_COMPLIANCE_REVIEW.md:466` (REQ-NOT-001 through REQ-NOT-005); `docs/architecture/02_interfaces.md:474` (F02.6 event holding/coalescing/acknowledgment); `06_aecp_engine.md` §7 (registry, exclusion, sequence numbers and queues); `08_timing.md:178` (service measurements and limits); `09_verification.md` §§7–8 (gates and notification evidence). The copyrighted specification texts were not independently obtained or authenticated.

The five-file delta is against `77cf6fb4`. History establishes author head `16c89c53` on `22c139a4` plus main `77cf6fb4`. Reconstructing the merge produces the exact reviewed tree. Every inherited main file except the intentionally combined architecture document is byte-identical to main; both changed RTL files are byte-identical to the author head. Their module declarations, all register-map files and the top-level interface remain unchanged. The inherited SET_CONFIGURATION and GET_AVB_INFO behavior is retained and covered by the focused response checks.

## Findings

### R649-F1 — MAJOR — Conformance, RTL, Tests, Docs

**Artifact:** [published evidence at 5131f4ad](https://github.com/kebag-logic/milan-fpga/tree/5131f4ad9f4e4a9e8bd195c78a693e59aa4d9859/review-evidence/pp181-r1), its `MANIFEST.json`, `author/HANDOFF.md` sections “Behaviour”, “Base and head records”, “Scratch-parent consumer gate table” and “Scratch”; `syn/ooc/README.md:241`; PR #187 body.

**Authority/evidence:** The assignment requires reproducible OOC/routed measurements and executable source validation, including planted faults for new checks. The complete, non-truncated repository-tree response shows only the manifest and two narrative Markdown documents in the published directory. The manifest lists only those documents. The handoff explicitly places the raw gate logs, proof inputs/results, mutant outputs, OOC reports, route reports and route chain in unpublished scratch. Neither the manager ruling nor the PR review-start comments supplies them. The committed OOC recipe exists, but the added timing-query procedure and measured outputs are not published as executable receipts.

The handoff reports removal of every count-to-select path, 22-level residual OOC paths, routed WNS +0.016 ns at base with #760, +0.181 ns at head without #760 and +0.144 ns at head with #760, plus passing source gates/proof controls. Those are **reported results**, not independently inspected raw measurements. The parent timing comment corroborates the old +0.016 ns problem; it does not supply the missing head receipts. The parent resource policy retains the +0.030 ns floor. This review ran neither a reroute nor a full bank.

**Impact:** The central shipping-timing acceptance claim, exact measurement inputs/recipes, complete source-gate results and formal mutant failures cannot be reproduced or audited from the supplied public packet. Source inspection and focused simulation cannot establish routed timing. The public source evidence describes the author head and RTL-equivalent predecessors; it must not be relabeled as an executed manager bank at this merged head.

**Required outcome:** Publish the already-reported source-validation and measurement receipts with checksums and portable reproduction instructions: exact source/parent/#760 identities, source inputs or patches, unchanged recipe/constraint identity, OOC queries/reports, routed timing/utilization and resource-gate outputs, commands/return codes, and proof/control/mutant scripts/logs. Identify what ran at the author head versus the composed source head. This requires no invented manager source bank and does not preempt the manager's later candidate bank.

**Verification:** From a fresh public checkout, verify the inventory, reconstruct each input, reproduce focused proof controls and trace every timing/gate figure to its raw result. Verify full relevant endpoint coverage of count-to-select queries, inclusion of #760 in the +0.144 ns run, unchanged shipping recipe, and passing resource-gate output. Reassess when those receipts are public.

### R649-F2 — RESIDUE — Docs

**Paths:** `hdl/aecp/KL_aecp_notify.sv:426`; `hdl/packet_engine/KL_pp_event_router.sv:110`.

**Authority/evidence:** The owner's 2026-10-15 source-comment rule requires issue and requirement IDs. These new explanatory comments state behavior/reason and cite issue #181, but omit requirement IDs. No prohibited lane label, reviewer identifier or issue-comment ID was introduced in the source delta.

**Impact:** Comment traceability only; no behavior, measurement, figure, test, verdict, normative interpretation or privacy boundary changes. This residue does not leave a lens unclean.

**Exact fix:** In the occupancy comment, replace `(issue #181)` with `(issue #181; REQ-NOT-001, REQ-NOT-002)`. In the scan comment, replace `(issue #181)` with `(issue #181; REQ-REU-001, F02.6)`. These identify existing notification/interface-contract authorities without adding an obligation.

**Required outcome/verification:** Carry the wording edits on the residue checklist; inspect the comment-only diff and rerun the identifier check. No source edits were made by this reviewer.

## Independent lens evidence

**Conformance.** Queue class, descriptor identity, arguments, excluded requester and controller sequence semantics are unchanged. Integrated notification checks pass, including registered-controller fan-out, requester exclusion and byte-exact command notifications. The replacement timing ruling is honored. R649-F1 prevents closure of its physical acceptance claim.

**RTL.** The new flag resets with the count, sets on accepted push, and takes `count != 1` on pop without push. Simultaneous accepted push/pop holds count and keeps the flag set. Full-queue rejection retains the old drop behavior; a coincident pop still decrements and retains nonempty. These cases preserve `nonempty == (count != 0)` after reset without an added cycle. Remaining count comparisons control queue intake/state updates. Router scan inputs are registered pending/valid/pointer state; acknowledgment controls loading. On delivery, valid and deliver agree; while idle both are zero; while held the speculative grant is unused. Grant hold, round-robin order, payload and coalescing behavior are preserved. Implementation folding and residual depth are explicitly acknowledged in the synthesis documentation; physical evidence remains subject to F1.

**Robustness.** The unchanged router suite passes 81 checks, including held events, acknowledgment plus re-fire, saturation, fairness and randomized per-source conservation. The unchanged notify suite passes 67 checks across default, identify, two-interface and cancellation-window runs. The disposable queue probe holds transmission, offers 20 commands, retains 16 waiting plus one active command, counts exactly three excess offers, and verifies ordered content, controller identity, exclusion and sequence. It drains, refills back-to-back and resets while nonempty. Base and head produce identical 1,147-cycle traces and 31 delivered jobs. This forced overdrive verifies preservation of the block's existing full-queue behavior; it does not authorize production loss of mandatory notifications. Integrated admission/fan-out is checked separately.

**Tests.** Reviewer results at this head: router 81/81; notify 67/67; top notification 76/76; dispatch/response 955/955; notification spacing 9/9; hazards 189/189; service budget 56/56. Documentation gates and their standing self-tests pass. Service measurements reproduce 12,709 / 24,550 / 24,681 clocks behind a 15-frame fan-out. The queue probe passes at base/head and rejects push-unseen, pop-stays-occupied and off-by-one-empty faults. The router suite rejects fixed-idle-pointer, presented-event-retained and ignore-ack faults. Their builds succeed and executions fail named checks: these are not build-failure kills. No source suite/check changed in this PR's five-file delta. The author's new formal checks and complete campaigns lack raw public receipts under F1.

**Docs.** Architecture prose matches the state updates. The OOC table retains the 22/24-level residual paths and disclaims routed/hardware proof. The older PR/handoff statement about unmet depth-halving is read chronologically under the later replacement ruling, not as current acceptance. The published parent consumer table has two failing gate families at both base and author head: pin-document synchronization and the test-evidence ratchet, including its self-test. It is not an all-pass parent result and is not evidence of a new source regression. F1 covers missing receipts; F2 covers comment traceability.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN — F1 | Frozen issue/ruling; REQ-NOT-001–005; F02.6; notification/budget executions; public timing inventory | R649-1 | 42eb9aef3642f6d98058fe634a70f6a9c749cd25 |
| RTL | UNCLEAN — F1 | Both complete changed RTL modules; count writers/readers; router grant/load; merge/interface audit; OOC recipe/table | R649-1 | 42eb9aef3642f6d98058fe634a70f6a9c749cd25 |
| Robustness | CLEAN | Router/notify suites; full/empty/reset queue traces; six failing fault controls; integrated fan-out/hazards | R649-1 | 42eb9aef3642f6d98058fe634a70f6a9c749cd25 |
| Tests | UNCLEAN — F1 | Focused logs/return codes; mutation logs; published source proof/bank claims; exact-head hosted snapshot | R649-1 | 42eb9aef3642f6d98058fe634a70f6a9c749cd25 |
| Docs | UNCLEAN — F1; F2 nonblocking | docs/README; architecture 02/03/06/08/09; compliance matrix; OOC table/recipe; public manifest/handoff; parent timing policy | R649-1 | 42eb9aef3642f6d98058fe634a70f6a9c749cd25 |

## Independence, limits and pending duties

This verdict and ledger were written before inspecting any prior reviewer findings. Final public-findings reconciliation is recorded in the completed report.

Only focused suites and disposable fault probes ran. No full processor/parent/build banks, physical implementation runs, hardware operations, shared installs, source fixes, commits, pushes, merges, author contact or GitHub writes occurred. All build/probe trees are under this packet's excluded `scratch/`. Independent work ran concurrently with bounded compile parallelism; each process was waited for in the foreground. All 632 tracked blobs/modes, index, exact head/tree and clean status were verified. This processor tree has no submodule gitlinks to restore. Merge-tree calculation reconstructed the published tree without performing a merge.

There is no manager source bank at this head, and none is inferred. The manager owns hosted/act acceptance, the final current-dev candidate built from source base `77cf6fb4` against live dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`, builder/native receipts and parent consumer-gate closure. The next adopted shipping image must remeasure timing under the replacement ruling. Physical calibration is NOT RUN; field skips and simulation are not hardware proof. Two independent positive reviews and required passing banks remain conditions for merge/closure.

Portable scripts and raw reviewer receipts are listed in `MANIFEST.sha256`; disposable trees are excluded.

R649-1 FINISHED
