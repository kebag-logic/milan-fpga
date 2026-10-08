[R554] NEGATIVE - exact head f3fef22448ce4f9bed8fd249a21a5d472148bd3d

# R554-1 independent review: issue #167 / PR #169

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #169 (closes #167), assignment 6050430051.
- Exact head `f3fef22448ce4f9bed8fd249a21a5d472148bd3d`, tree `38da2da1e826d053d384380e202617054a1ef218`. Base: processor main `ed340b9b85258194247334b85e62cf9c23d4d051`.
- Reviewer role: internal independent reviewer, cleared context, own detached clone.
- Sources reconstructed in order: README.md and docs/README.md (the repository has no AGENTS.md or CONTRIBUTING.md); the issue #167 body and its three comments (assignment, TAKEN, REVIEW READY); docs/architecture/06_aecp_engine.md, REQ-NOT-004 and REQ-SCP-003 in docs/00_MILAN_COMPLIANCE_REVIEW.md; the full diff `ed340b9b..f3fef224` and its five commits; the author's published evidence at kebag-logic/milan-fpga@93a14a4c `review-evidence/pp167-r1/` (35 files). The PR has no manager evidence comments. Its only comments are the two review-start notices.
- Prior public review findings on PR #169: **none exist** at this head. The PR has no reviews, no review comments, and no finding comments. Nothing needs to be resolved or retained.

## Verdict

NEGATIVE. One MAJOR finding (F1) remains open.

The change does what acceptance 1 literally asks. At one interface, both cancellations are now sent, exactly once, in either row order. Count two is unchanged. SC1 and its planted control work as described. Every re-run campaign arm still plants.

However, the deferred command cancellation (sent one cycle late) opens a one-cycle window at count one. In that window, the issue's named harm can still happen: a superseded exchange's failure removes a live controller's registry row and sends that controller a DEREGISTER. The count-two path avoids this because a failure report is accepted only for a row whose probe is still live. The count-one path has no such guard. This was shown with two unit probes and reasoning from the code.

## Findings

### F1 - MAJOR - Conformance, RTL, Robustness, Tests

**Location**
- `hdl/aecp/KL_aecp_notify.sv:801-802`: the count-one failure route, `cf_ok_w = ca_fail_valid_i && owner < N_CTRL_P && !rx_cmd_hit_w[cf_ix_w] && valid_r[cf_ix_w]`.
- It works with the new deferral at `hdl/aecp/KL_aecp_notify.sv:785-797` (`cx_wait_r`).
- Compare the count-two route `report_route` at `hdl/aecp/KL_aecp_notify.sv:747-765`, which also requires `ca_probe_r[row]`.

**Authority**
- Issue #167: "the superseded exchange then stays in the originator's in-flight table, and its later failure can remove a live controller's registry row". This is the harm the issue exists to remove.
- REQ-NOT-004 (Milan §5.4.5.3): removal and targeted DEREGISTER happen only on silence.
- docs/architecture/06_aecp_engine.md:893-897: a valid command supersedes and cancels the probe.
- The count-two rule at 06_aecp_engine.md:916: "a superseded probe's late response or failure touches nothing".

**Mechanism.** Let D be the TIME_LIMITED drain row and A the commanding row (owner A).
- **Cycle t.** A's command clears `ca_probe_r[A]` (`:1318-1323`). The drain wins the single cancellation face. A's cancel is held in `cx_wait_r` and is presented at t+1.
- **The originator at t.** `KL_pp_originator` parks a cancel only when it hits a live entry (`hdl/packet_engine/KL_pp_originator.sv:362-364`). Expiry service has lower priority only than a response, a parked cancel, or an acceptance (`:307-309`).
- **When D's cancel misses the originator.** This happens when D's CONTROLLER_AVAILABLE is still in the frame builder. The builder accepts at `req_ready_o = C_IDLE` (`hdl/aecp/KL_aecp_ca_originator.sv:100`), and `ca_probe_r[D]` is set then. It then writes 60 bytes before ISSUE (`:170`). In that case the originator may service A's parked second timeout at t. It then registers `fail_valid_o` for owner A at t+1 (`:476-483`).
- **Cycle t+1.** No command masks the report, and row A is valid. So `cf_ok_w` sets `pend_r[A]` (`:1340-1343`). The live controller's row is drained and a targeted DEREGISTER goes to that controller. The deferred cancel for A then arrives too late to matter.
- **Why base timing was safe.** In the uncontended timing the cancel lands at t. A cancel that hits always takes the originator's event lane ahead of the expiry, so no failure follows.

**Evidence** (reviewer probes, disposable, in scratch copies of the exact-head sources)

P1 (`scripts/probes/p1_fail_window.cpp`, `p1_build.sh`; receipt `receipts/probe-p1-head.log`): `KL_aecp_notify` at head, SC1 setup, with a failure report for the commanding owner presented relative to the coincidence cycle.

| Report offset | Cancels | Registry entries | DEREGISTER to the commanding controller |
|---|---|---|---|
| 0 | {1,1} | 1 | 0 |
| **1** | {1,1} | **0** | **1** |

Offset 1 is where the originator places it (P2). The deferred cancel for owner 1 is emitted at offset 1, the same cycle.

P2 (`scripts/probes/p2_originator.cpp`, `p2_build.sh`; receipt `receipts/probe-p2-head.log`): `KL_pp_originator` with one live exchange of owner 1 whose second timeout is serviced in cycle E.

| Cancel presented at E | Failure for owner 1 | Offset from E |
|---|---|---|
| Owner 0, not in the table (D in the builder) | yes | +1 |
| Owner 1 (base timing) | none | n/a |
| None | yes | +1 |

P1-guard (`receipts/probe-p1-guard.log`, `.diff`): adding `&& !cx_wait_w[cf_ix_w]` to `cf_ok_w`, in a disposable copy only, keeps the registry at 1 entry with no DEREGISTER at offset 1. Both cancels are still sent once. The reachable window is therefore closable inside the module. Offset 2 is not reachable: the cancel presented at t+1 hits the live entry and takes the originator's lane ahead of the expiry.

**Impact.** At P-N-AVB-INTERFACES = 1 (the shipping 1x1 shape), a rare but reachable alignment of three events in one cycle still removes a live controller. The three events are: a TIME_LIMITED drain whose probe is still being built, another controller's command, and that controller's second probe timeout being serviced. The controller receives a targeted DEREGISTER. Acceptance 1's wording ("both cancels are sent") is met. The issue's stated harm is not fully closed, and the count-one path does not have the stale-report protection that the count-two path it claims to mirror has. SC1 does not grade the report window. The count-two suite grades the equivalent window (CA2).

**Required outcome**
- At count one, a failure (and preferably a response) for a row whose command cancellation is still pending, or whose probe is no longer live, must not drain or re-arm the row. One option is to gate `cf_ok_w`/`cr_ok_w` on `!cx_wait_w[...]` or on `ca_probe_r[...]`, as `report_route` does. Another is a proof that the report cannot land at t+1.
- Add a count-one check in the style of CA2 (a failure for the commanding owner one cycle after the coincidence leaves the row and sends no DEREGISTER), with a planted control that removes the guard.
- Keep SC1 and every existing arm planting. Keep OOC 1x1 within +20 LUT / +20 FF.
- Update the 06 paragraph at `:919-925` to state the count-one report rule.

**Verification.** Re-run P1 at the new head: offset 1 must give 1 entry and no DEREGISTER. Run the new check against the guard-removed control. Run the aecp_notify suite and the notify campaign.

No other findings. No RESIDUE and no SUGGESTION items are recorded.

## Lens evidence

**Conformance.** Acceptance 1: at count one, both cancels are sent exactly once in either order.
- Reviewer re-run of SC1 at head: `{1,1}` both orders (`receipts/head-suite-aecp_notify.log`).
- SC1 against base RTL: `{1,0}` and `{0,1}`, rc 2 (`receipts/sc1-on-base-rtl.log`).
- Drain priority is kept. The uncontended cancel is still same-cycle (CX1 passes). A command and a drain for the same row coalesce: the clear of the emitted index wins the non-blocking order at `:790-791`.
- At t+1 the FSM is always in N_IDLE (N_DRAIN lasts one cycle), so a pending cancel is never starved by back-to-back drains.
- No duplication: pending bits clear only on emission.
- Count two is functionally unchanged. The `g_ca_turns` block differs from base only by `assign cx_wait_w = '0;` (`receipts/count-two-block.diff`). At count two, `ca_cancel_ok_w`/`ca_cancel_ix_w` have no reader. `port_tuple.hpp` is byte-identical. CA1b's control `cancel_one_per_command` still fails exactly CA1 and CA1b.
- Acceptance 4 (no port, parameter or register-map change): the module header and the top are unchanged in the diff. No file in docs/architecture/07_memory_maps.md or hdl/top is touched. The author's scope proof agrees.
- Unclean because of F1 (REQ-NOT-004).

**RTL.** The 17-line change was read in full.
- Pending bits are reset and unioned before the selective clear. Lowest-index pick is reused. Lint is clean (`receipts/head-lint_hdl.log`, rc 0).
- OOC 1x1 is not re-measured: the vendor tool is not available here. The author's receipt (`area-comparison.json`) gives LUT 23,160 → 23,101 (−59) and FF 19,787 → 19,802 (+15), measured at `521373f6`. `git diff 521373f6..f3fef224 -- hdl syn` is empty, so the measured production inputs equal the head. +15 FF is consistent with one pending bit per row at P-N-CONTROLLERS = 16.
- Unclean because of F1.

**Robustness.**
- Reset clears `cx_wait_r`.
- Delay is bounded: at most the number of rows, and in the coincidence case exactly one cycle.
- A deferred cancel cannot overlap a new probe of the same row. `ca_pend_r[A]` is cleared by the command, and a new probe needs a fresh PRNG draw and a monitor expiry (milliseconds).
- A cancel at t+1 to an entry still in the builder is caught by the builder's own `cancel_hit_w`. One still in the originator takes the event lane ahead of the expiry.
- The single uncovered interaction is F1. Unclean.

**Tests.**
- SC1 is real and discriminating: it fails on base and fails under `cancel_collision_drops_command`.
- `make` runs four tallies (66 checks). The `run` target keeps the three-run record, and `collision` runs SC1 alone.
- Notify campaign subset at head: every arm graded by `tb/aecp_notify` plus the four `--withdraw-only` arms, 39 arms and 5 goldens. Result: 39 of 39 KILLED, goldens PASS (`receipts/campaign-head/results.json`).
- Exact failing-check records: `cancel_one_clock_late` gives IX3 and CX1, `cancel_one_per_command` gives CA1 and CA1b, `report_fail_ignores_probe` gives CA2 and CA3, and `cancel_collision_drops_command` gives SC1. These equal the records in `tb/aecp_notify/README.md:270` and `tb/pp_top/README.md:2728-2745`.
- Focused suites at head: aecp_notify 66/66, originator 107/107, ca_originator 16/16, pp_top 10469/10469. The aecp_notify and pp_top counts match the author's suite table.
- Unclean because of F1: no count-one check grades the post-coincidence report window, while count two has CA2.

**Docs.**
- 06_aecp_engine.md:919-925 and the storage-table row correctly describe the count-one pending bits and SC1.
- The aecp_notify README covers Section SC, the four-run accounting (66 = 42 + 4 + 19 + 1) and the mutant row. The pp_top README covers the 92-control count, the revised late-cancel control and the new arm row. The notify_mutants docstring is updated.
- `make -j16 check` at head is rc 0 in a git-backed scratch clone (`receipts/head-make_check-git.log`). The first attempt in a plain export without git metadata failed in `check-ids`/`check-figures` (`receipts/head-make_check.log`, rc 2). That is a reviewer environment artifact, not a defect: the gates read `git ls-files`.
- `gen_matrix.py --check` is rc 0.
- The required F1 doc update is part of F1's outcome. The present text accurately describes the present RTL. Clean.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | issue #167 acceptance 1-3 and assignment items 1-5; REQ-NOT-004, REQ-SCP-003; SC1 at head and against base RTL; count-two block diff; port/parameter scope | R554-1 | f3fef22448ce4f9bed8fd249a21a5d472148bd3d |
| RTL | UNCLEAN (F1) | `KL_aecp_notify.sv` diff and the cancel, report, drain and monitor paths; `KL_pp_originator.sv` event priority; `KL_aecp_ca_originator.sv` issue timing; lint; author OOC receipt | R554-1 | f3fef22448ce4f9bed8fd249a21a5d472148bd3d |
| Robustness | UNCLEAN (F1) | reset, starvation, duplicate and same-row coalescing, reuse, builder/originator cancel races; probes P1, P2, P1-guard | R554-1 | f3fef22448ce4f9bed8fd249a21a5d472148bd3d |
| Tests | UNCLEAN (F1) | `tb/aecp_notify/sim_main.cpp` SC1 and Makefile; `notify_mutants.py`; 39 arms and 5 goldens re-run; 4 focused suites | R554-1 | f3fef22448ce4f9bed8fd249a21a5d472148bd3d |
| Docs | CLEAN | `06_aecp_engine.md`, `tb/aecp_notify/README.md`, `tb/pp_top/README.md`, mutant docstring, PR body; `make check`; matrix check | R554-1 | f3fef22448ce4f9bed8fd249a21a5d472148bd3d |

## Real limits

- **Not run by this reviewer, by the assignment's rules or for lack of tools:** the full processor suite bank (`run_suites.sh`), `syn/yosys/run.sh`, the OOC 1x1 synthesis, the nine other affected campaigns, the remaining 53 arms of the notify campaign (pp_top builds other than the withdraw arms), and the 17 parent consumer gates on the scratch parent. For these, the author's published receipts (`final-receipts.json`, `suite-comparison.json`, `processor-static-comparison.json`, `parent-comparison.json`, `area-comparison.json`, `plant-head.json`) are the only source-head execution evidence. They were inspected, not reproduced.
- **F1's probes are unit-level** (notify alone, originator alone). The three-event alignment was not simulated end to end at `tb/pp_top`. The builder precondition (a probe live in notify but not yet in the originator table) is derived from the code at the cited lines.
- **Toolchain:** the pinned 5.050 wrapper was used, identity checked (`receipts/environment.txt`), with compile parallelism capped at 4 per build and at most two builds at once.
- **Hosted CI at the exact head**, snapshot at 05:17Z (`receipts/hosted-checks-f3fef224.tsv`): docs-gates and portability completed with success on both runs; both `suites` jobs were still in progress. No hosted conclusion is claimed for suites.
- No manager source bank exists at this head, and none is inferred.
- Physical calibration was NOT RUN. Field skips are not hardware proof. The builder ledger's unavailable external calibration-report arm is reported by the author as not run.
- **Clone integrity:** after the probes, the review clone was verified at the exact head. All 581 tracked files' bytes equal their index blobs. Modes are 564 × 100644 and 17 × 100755, matching. The index equals the HEAD tree. No untracked or ignored files remain: one bytecode cache from importing the mutant driver was removed. The processor repository has no submodule gitlinks (zero 160000 entries).

## Pending manager duties

- Hosted/act acceptance at the exact head, including the two in-progress `suites` jobs.
- The current-dev merge candidate (source base ed340b9b85258194247334b85e62cf9c23d4d051 onto live dev 99e4eb6c14462aafa84bb1ac597fd241abc1a240): builder and native banks at the merge turn, with receipts linked on the PR.
- After F1 is addressed: a new review round at the new head, a re-measured OOC 1x1 delta, and the parent consumer gates on the scratch parent (dev 28f9666f plus the two adoption patches).
- The second (external) independent review; merge requires two positive reviews and the full completion bar.

R554-1 FINISHED
