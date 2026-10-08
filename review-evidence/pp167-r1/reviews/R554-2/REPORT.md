[R554] NEGATIVE - exact head 1411117e646023cb236de02e3acaf9bdfcef49e3

# R554-2 independent review: issue #167 / PR #169, round 2

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #169 (closes #167). Round-2 assignment: issue #167 comment 6052908672. Review start: PR #169 comment 6059442110.
- Exact head `1411117e646023cb236de02e3acaf9bdfcef49e3`, tree `4b2b3045188f7c1403a5bafb56f7e9edc059a6dd`. Base (processor main) `ed340b9b85258194247334b85e62cf9c23d4d051`. Round-1 head `f3fef22448ce4f9bed8fd249a21a5d472148bd3d`. Delta under review: `f3fef224..1411117e` (one commit), read against the whole `ed340b9b..1411117e` diff.
- Role: internal independent reviewer, cleared context, own detached clone.
- Reconstruction order: the repository has no AGENTS.md or CONTRIBUTING.md; README.md and docs/README.md; issue #167 body (acceptance 1 to 3) and its five comments (assignment, TAKEN, REVIEW READY at f3fef224, the round-2 assignment, REVIEW READY at 1411117e); REQ-NOT-004 and REQ-SCP-003 in docs/00_MILAN_COMPLIANCE_REVIEW.md; docs/architecture/06_aecp_engine.md:880-940 and 09_verification.md §8.4; the RTL of `KL_aecp_notify`, `KL_pp_originator`, `KL_aecp_ca_originator` and the top wiring; the six-commit diff and history; then the public evidence at kebag-logic/milan-fpga@5a59492617aa18d116fe881ceffe24b17aa4f9ba `review-evidence/pp167-r1/` (MANIFEST.json and `author-r2/`, 70 files). Neither the issue nor the PR carries a manager evidence comment at this head; the PR's manager comments are the four review-start notices.
- Prior public review reports (R554-1, R555-1) were read only after this review's independent pass, probes and verdict were complete. They are reconciled below.

## Verdict

NEGATIVE, on one MINOR documentation finding (F1). The engineering outcome of round 2 is correct and is verified here.

R554-1-F1 is **resolved**. The guard `&& !cx_wait_w[cf_ix_w]` on `cf_ok_w` (`hdl/aecp/KL_aecp_notify.sv:801-803`) ignores a failure report for a row while its command cancellation is pending, including the cycle that emits the deferred cancel. That closes the offset-1 window. Both cancellations are still sent exactly once. Uncontended base timing and the count-two path are unchanged, shown formally for count two. A failure can only be accepted after the cancel's own cycle, which is the same relation the unchanged uncontended path has. The real originator cannot produce such a failure: this follows from the code, and a 10-million-cycle stress run plus a planted control confirm it.

F1: the new standing checks SC1 and SC2 (section SC) have no row in the normative verification register, docs/architecture/09_verification.md §8.4. Every other named `tb/aecp_notify` section has one, and earlier issues added theirs.

## Findings

### F1 - MINOR - Docs

- **Location.** `docs/architecture/09_verification.md:297-320` (§8.4). The intro at `:300-301` says "plus one section of the originator's unit suite and six of the notification block's". The table lists `tb/aecp_notify` FT, IX, TS, TW, DR and CX, with PT/CK/PD/CA in the two-interface table at `:431-434`. It has no row for section SC (SC1, added in round 1; SC2, added in this round).
- **Authority and evidence.**
  - docs/README.md §1: 09 is the document that answers how compliance is demonstrated.
  - Project practice: each new notification-suite section was registered in 09 in the change that added it. Examples are TW (#148), DR (#158), CX and WD (#163, commit 740b15b), IX and TS (#232), and PT/CK/PD/CA (#69).
  - SC is now the only named section in `tb/aecp_notify/README.md` (headings at `:21-324`) without a 09 row. A search of docs/ for "SC1", "SC2", "section SC" or "#167" finds only 06_aecp_engine.md:925-928.
  - SC2 is new in this round's delta. SC1's omission was in the round-1 baseline.
- **Impact.** The verification register understates what is graded for REQ-NOT-004 at one interface: the drain/command cancellation coincidence and the pending-cancel report window. A reader of 09 cannot find the evidence for the count-one rule that 06:919-929 states. The analogous count-two property is registered (CA row, `:434`). Nothing is measured wrongly, and no code or test is affected. A missing register entry is not wording of existing prose, so this is recorded as MINOR, not RESIDUE.
- **Required outcome.**
  - Add a §8.4 row (category DIR or TIM) for `tb/aecp_notify` SC, in the style of the CX row. It should say that a TIME_LIMITED drain and another controller's command in one cycle at one interface send both cancellations exactly once, in either row order. It should also say that a failure for the commanding owner presented in the deferred cancel's cycle leaves that controller registered with no DEREGISTER.
  - Update "six of the notification block's" to seven.
  - The existing sentence already points the mutation records to the suites' READMEs.
- **Verification.** Read the row at the new head. `make check` rc 0. No RTL, test or record change is expected.

### Suggestion (does not affect the verdict)

- **S1 - SUGGESTION - RTL (comment only).** The `g_ca_own` comment at `hdl/aecp/KL_aecp_notify.sv:779-784` describes `cx_wait_r` but not its second role at `:803`, where a failure is ignored while its row's cancellation is pending. One sentence would keep the RTL self-describing; it would mirror 06:923-925 and the `report_route` comment of `g_ca_turns`.

## Reconciliation of prior public findings at this head

| Prior finding | Status at 1411117e | Evidence |
|---|---|---|
| R554-1-F1 (MAJOR): the count-one deferred cancel lets a failure at offset 1 remove the live controller's row and send it a targeted DEREGISTER | **RESOLVED** | Guard at `KL_aecp_notify.sv:801-803`. R554-1's own P1, rerun here: head offset 1 gives 1 entry and 0 DEREGISTER; the round-1 head gives 0 entries and 1 DEREGISTER (`receipts/r554-1-P1-rerun-{head,r1}.log`). R554-1's P2 is identical at base and head (`receipts/r554-1-P2-rerun-{base,head}.log`). This review's sweep and stress runs, below, add to that. The required 06 update is present at 06:923-925. SC2 and its control `cancel_pending_accepts_failure` exist and behave as claimed. |
| R555-1: no findings, residue or suggestions | nothing to resolve or retain | — |

## Assignment checks (round 2), with this review's evidence

1. **Offset-1 window closed, both cancels once.** The sweep probe `scripts/probe_fail_offset.cpp` sets up both row orders at one interface and presents a failure for the commanding owner at offsets k = -1 (none), 0, 1, 2 and 3 from the coincidence. Receipts: `receipts/probe-offset-{base,r1,head}.txt`.
   - Head, coincident case: cancels `{expired@0, live@1}` in both orders. At k = 0 and 1 the live row is KEPT with 0 DEREGISTER. At k = 2 and 3 it is removed.
   - Round-1 head: removed already at k = 1 (the R554-1 defect).
   - Base: the live cancel is never sent (the #167 defect).
   - So the guard covers exactly the command's cycle through the deferred cancel's emission cycle. A failure is accepted only from the cycle after the cancel.
2. **That remaining acceptance is unreachable, and it is the same as base.**
   - Uncontended case: identical at base, round-1 head and head. The cancel is in its own cycle (k = 0 ignored) and a failure one cycle after the cancel is accepted. So the head keeps the existing "cancel cycle, then accept" relation; it only moves it by the deferral.
   - By code: `KL_pp_originator` registers `fail_valid_o` one cycle after its expiry event (`KL_pp_originator.sv:471-486`). The expiry event is blocked whenever a cancel is live or parked (`cancel_work_w`, `:195-207`; priority at `:306-311`). A failure for owner o can therefore appear no later than the cycle that presents o's cancel.
   - The top wires that face directly (`protocol_processor_top.sv:1196-1209`, `:4139-4144`) to an originator dedicated to CONTROLLER_AVAILABLE (`:1177-1233`). An exchange still in the frame builder is aborted there on the same cancel (`KL_aecp_ca_originator.sv:98-99`).
   - Stress run: `scripts/probe_orig_cancel_fail.cpp` drives the originator at the CA shape for 5 seeds × 2,000,000 random cycles, under the top's contract. Result: 0 violations of "no failure for o after a cycle presenting o's cancel". About 2,650 failures per seed fall in the cancel cycle itself, the case the guard masks (`receipts/probe-orig-stress-head.txt`).
   - Planted control for the stress run: letting expiry outrank a parked cancel gives 3,395 violations, rc 1 (`receipts/probe-orig-stress-plant*.{txt,diff}`).
3. **Base timing and count two unchanged.**
   - Yosys sequential equivalence of `KL_aecp_notify` between base and head at N_IF_P = 2: 12,788 of 12,788 equivalence points proven (`receipts/equiv-count-two-if2.txt`, `scripts/equiv_count_two.sh`).
   - Sensitivity control at N_IF_P = 1: only `ca_cancel_ok_w`, `ca_cancel_ix_w` and `cf_ok_w` are unproven. These are exactly the intended changes (`receipts/equiv-count-one-control-if1.txt`).
   - The count-two control `cancel_one_per_command` still fails exactly CA1 and CA1b, with a record identical to base.
4. **SC2 and its control.** The head suite passes 67 of 67 checks: SC1 `{1,1}` and SC2 `{1,1}`, with 1 entry and 0 live DEREGISTER in both orders (`receipts/gates/notify-suite-head.log`). The base suite passes 65 of 65.
   - `cancel_pending_accepts_failure` is KILLED by SC2 alone, and `cancel_collision_drops_command` by SC1 alone (`receipts/campaign-head/`).
   - An extra plant from this review leaves the guard open only in the emission cycle: `!(cx_wait && !cx_ok)`. SC2 still fails, with 0 entries and 1 live DEREGISTER in both orders (`receipts/plant-sc2-emission-cycle-open.log`). SC2 therefore grades the "including the emitting cycle" clause that 06 states.
5. **Every existing arm still plants.** This review re-ran every notify-campaign arm graded by `tb/aecp_notify`: 34 existing arms plus the 2 new ones, with goldens, at head; the 34 existing arms were also run at base.
   - Head: 36 of 36 KILLED, 5 goldens PASS. Base: 34 of 34 KILLED, 3 goldens PASS.
   - Each of the 34 shared arms has a failing-check record identical between base and head (`receipts/campaign-compare.txt`, `receipts/campaign-{base,head}/results.json`).
6. **OOC 1x1 within +20 LUT / +20 FF.**
   - Author receipt `author-r2/round2/area-comparison.json`: LUT 23,160 → 23,171 (+11), FF 19,787 → 19,807 (+20, at the limit), BRAM and DSP unchanged, parameters and six image hashes identical.
   - The receipt's bytes differ from the round-2 evidence index. The manager's MANIFEST.json records it as path-redacted on publication, with the original hash equal to the index hash. Every other indexed file matches (`receipts/evidence-index-verify-round2.txt`).
   - The author's 581-file source inventories match the exact base and head trees byte for byte (`receipts/source-inventory-{base,head}.txt`).
   - Not reproduced here: the vendor synthesis tool is not installed. Round 1 measured +15 FF on RTL that differs from this head only by the combinational guard, so the +5 FF between rounds is synthesis variation. Either value meets the limit.
7. **Processor and parent gates.**
   - Reviewer runs at head, all rc 0: `scripts/lint_hdl.sh`, `make check` (in a git-backed clone), `gen_matrix.py --check` (94 rows, 0 untested) and the `tb/aecp_notify` suite.
   - Full suites, Yosys `syn/yosys/run.sh`, the ten campaigns and the 17 parent consumer gates are author receipts (`final-receipts.json`, `suite-comparison.json`: 1,028,291 → 1,028,293 checks; `parent-comparison.json`). They were inspected, not reproduced: the full banks are outside this review's allowance.

## Lens evidence

- **Conformance - CLEAN.**
  - Acceptance 1: both cancels at count one, exactly once, either order (SC1, sweep).
  - Acceptance 2: SC1 with its planted control, plus SC2 with its planted control.
  - Acceptance 3: OOC 1x1 author receipt within limits; every arm plants.
  - The issue's stated harm, removal of a live controller's row and a targeted DEREGISTER (REQ-NOT-004, Milan §5.4.5.3; 06:893-897, :916), is closed at count one (items 1 and 2). Count-two REQ-SCP-003 behaviour is formally unchanged.
  - No port, parameter or register-map change: the module declaration and the top are untouched, so no STOP condition applies.
- **RTL - CLEAN.**
  - The round-2 change is the single term at `:803`. Read with the `cx_wait_r` register (`:785-793`), the common pick (`:619`) and the count-two tie-off (`:718`).
  - `cx_wait_r` resets synchronously. The clear of the emitted index wins the non-blocking order, so an uncontended cancel never sets a pending bit.
  - At count two, `ca_cancel_ok_w` has no reader.
  - Lint is clean. The structural difference is confined to the intended nets (Yosys).
- **Robustness - CLEAN.**
  - A pending bit lasts until its cancel is emitted. That is one cycle in the coincidence (N_DRAIN always returns to N_IDLE), and at most the number of rows in general.
  - It cannot mask a new probe's failure: a fresh probe of the row needs a PRNG draw and a monitor expiry after the command, and the command set `mon_draw_pend_r` (`:1319-1324`, `:1327-1331`).
  - The guard's premise about the originator holds under the cycle-random stress run, which has a planted control. Reset clears all pending state.
  - A stale response at offset 1 sets only bits the command already set: `cr_ok_w` is unguarded, which is harmless.
- **Tests - CLEAN.**
  - SC2 observes before each edge, presents the failure in the deferred cancel's cycle, and requires both cancels once, the surviving entry, no live DEREGISTER and the expired controller's DEREGISTER, in both row orders.
  - SC2 fails without the guard and with an emission-cycle-open guard.
  - Isolated runs keep every earlier arm's record. `make` sums five runs to 67, matching the README.
- **Docs - UNCLEAN (F1).**
  - 06:919-929 accurately states the count-one rule and SC1/SC2, and the storage row at :940 is accurate.
  - `tb/aecp_notify/README.md` (five-run accounting 42 + 4 + 19 + 2, the SC section and mutant table) and `tb/pp_top/README.md` (93 controls and the new arm row) agree with the code and the campaign.
  - The PR body's figures agree with the receipts.
  - 09 §8.4 lacks the SC row (F1).

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #167 acceptance 1-3, assignment comments 6050430051 and 6052908672; REQ-NOT-004, REQ-SCP-003; 06:880-940; offset sweep at base, round-1 head and head; R554-1 P1/P2 reruns; module declaration and top unchanged | R554-2 | 1411117e646023cb236de02e3acaf9bdfcef49e3 |
| RTL | CLEAN | `KL_aecp_notify.sv:452-806,1316-1345,1550-1637`; `KL_pp_originator.sv:188-489`; `KL_aecp_ca_originator.sv`; `protocol_processor_top.sv:1150-1260,4139-4144`; lint rc 0; Yosys equivalence at N_IF_P 2 (proven) and 1 (control); author OOC receipt | R554-2 | 1411117e646023cb236de02e3acaf9bdfcef49e3 |
| Robustness | CLEAN | pending-bit lifetime, reset, same-row coalescing, overlap with a new probe, stale response; originator stress 10M cycles with 0 violations and a planted control with 3,395 violations | R554-2 | 1411117e646023cb236de02e3acaf9bdfcef49e3 |
| Tests | CLEAN | `tb/aecp_notify/sim_main.cpp` SC1/SC2, Makefile `check`/`collision`/`failure-window`; `notify_mutants.py`; 36 arms + 5 goldens at head, 34 arms + 3 goldens at base, records identical; extra SC2 plant; suite 67/67 head, 65/65 base | R554-2 | 1411117e646023cb236de02e3acaf9bdfcef49e3 |
| Docs | UNCLEAN (F1) | 06_aecp_engine.md:917-940; 09_verification.md §8.4 and two-interface table; tb/aecp_notify and tb/pp_top READMEs; PR body; `make check` rc 0; matrix rc 0 | R554-2 | 1411117e646023cb236de02e3acaf9bdfcef49e3 |

## Real limits

- **Not run by this reviewer**, by the assignment's rules or for lack of tools: the full processor suite bank, `syn/yosys/run.sh`, the OOC 1x1 synthesis (vendor tool not installed), the nine other affected campaigns, the 57 pp_top-built and originator-built arms of the notify campaign, and the 17 parent consumer gates. For these, the author's published receipts are the only source-head execution evidence. They were inspected and their hashes checked, not reproduced.
- **Unit-level probes.** The probes are unit-level: notify alone, and the originator alone at the CA shape. The originator premise rests on code reading plus a randomized stress run; it is not a formal proof. No end-to-end `tb/pp_top` alignment of the three events was simulated.
- **Hosted CI at the exact head**, snapshot 2026-10-08 12:24Z (`receipts/hosted-check-runs-head.tsv`): docs-gates and portability completed with success in both runs (37773990341, 37773985394), and both `suites` jobs were still in progress. No hosted suite conclusion is claimed.
- **No manager source bank** exists at this exact head, and none is inferred. No manager donor or consumer bank receipt was present on the issue or PR at the snapshot.
- **Physical calibration** NOT RUN. Field skips are not hardware proof. The external calibration-report arm is recorded by the author as not run.
- **Toolchain.** Pinned Verilator 5.050 wrapper, identity in `receipts/environment.txt`. Yosys 0.66 with sv2v 0.0.13 for the equivalence. At most 16 concurrent jobs.
- **Clone integrity** after all work (`receipts/clone-integrity.txt`): HEAD and tree are exact, and the index tree equals the HEAD tree. All 581 tracked blobs match byte for byte, with modes 564 × 100644 and 17 × 100755. There are no untracked or ignored files and no gitlinks; the processor has no submodules. All builds, probes and plants ran in disposable trees under the unpublished `scratch/`.
- **Redaction.** Build-command lines in six receipt logs had the host tool-root prefix replaced with `<TOOLROOT>` (`scripts/redact_receipts.py`). No result line was changed.

## Pending manager duties

- Carry F1 to the author: add the 09 §8.4 SC row and the count. Then run a new review round at the new head; a docs-only change needs no re-measurement of RTL gates.
- Hosted/act acceptance at the exact head, including the two in-progress `suites` jobs.
- The current-dev merge candidate (source base ed340b9b85258194247334b85e62cf9c23d4d051 onto live dev 17f62ef64a66562384e8a93b1d6be6f86e51f95c): builder and native banks at the merge turn, with receipts linked on the PR.
- The second (external) independent review of this round. Merge requires two positive reviews and the full completion bar.

## Packet

Scripts: `scripts/probe_fail_offset.cpp`, `run_probe.sh`, `probe_orig_cancel_fail.cpp`, `run_orig_stress.sh`, `equiv_count_two.sh`, `launch_gates.sh`, `compare_campaign.py`, `verify_index.py`, `verify_source_inventory.py`, `fetch_evidence.py`, `redact_receipts.py`. Receipts under `receipts/`. Every published file is listed in `MANIFEST.sha256`.

R554-2 FINISHED
