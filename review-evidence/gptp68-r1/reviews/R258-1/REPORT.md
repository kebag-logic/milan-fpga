[R258] NEGATIVE - exact head 77c34e904eba2446755d13e1bf4763d1652c3ca7

# R258-1: independent review of FPGA-gPTP #68 / PR #74

| Item | Value |
|---|---|
| Reviewer | R258, internal cleared-context review, round R258-1 |
| Head | `77c34e904eba2446755d13e1bf4763d1652c3ca7`, tree `10154fc3f95ccc542a6f5dcd8a58105d302fd1af` (verified, `receipts/identity.log`) |
| Base | `c1b617435824929a790739ea8585c3fe1a328cc0` (the parent's current `gptp-processor` pin) |
| Parent used for consumer probes | kebag-logic/milan-fpga live dev `574c29fa111c74e5e5ed63e4670aff1f492e28e2` |
| Simulator | Verilator 5.050, pinned wrapper sha256 `905795b9...e92f`, `verilator_bin` sha256 `44898b22...bfdd` |
| Verdict | NEGATIVE: one BLOCKER, one MAJOR, one SUGGESTION |

## Reconstruction

Read in this order, from public state only:

1. Parent `AGENTS.md` and `CONTRIBUTING.md` at `574c29fa` (the donor has no contributor file of its own), the donor `README.md` and `docs/README.md`.
2. Issue #68 body (frozen acceptance) and all four issue comments: the assignment, the author's TAKEN, the author's material DECISION (5790066720) and REVIEW READY.
3. The parent decision kebag-logic/milan-fpga#387 comment 5606198212 and the #387 body. Parent `REQUIREMENTS.md` REQ-PTP-01, 05, 07, 08 and 09.
4. The interface authorities: donor `docs/INTEGRATION.md`, `hdl/top/KL_gptp_engine.sv`, `hdl/ucpu/KL_gptp_ucpu.sv`. On the parent consumer side: `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv`, `KL_gptp_txret.sv` and `docs/design/GPTP_PLANE.md`.
5. `git diff c1b61743..77c34e90` (10 files) and the single commit, whose message is one line with no trailers.
6. Public evidence at kebag-logic/milan-fpga `5dafe5ab` and its child `374e2008` under `review-evidence/gptp68-r1`: `author-a188/` (identical in both) and `manager-r1/`. The PR #74 body and both PR comments: the manager validation and the review start.

Prior public review findings on PR #74 at this head: none. The PR has no review objects and no review comments. Checked again after this verdict and ledger were written, its comments are the manager's validation and two manager review-start notices, R258-1 and R259-1. None carries a finding. Nothing is carried forward to resolve or retain.

## Findings

### F1 BLOCKER: slewing holds the addend at ~320 ppm, beyond the parent consumer's 200 ppm envelope, so the plane loses synchronization permanently

- **Severity:** BLOCKER.
- **Lenses:** Conformance, RTL, Robustness, Tests, Docs.
- **Donor locations at head:**
  - `hdl/ucode/gen_gptp_ucode.py:779-797`, the slew arm. The input is saturated at `SLEW_NS_C` (line 783), the integrator clamped at `ILIM` (line 790), and the addend written is `-(kp + I)` (lines 792-797).
  - `docs/INTEGRATION.md:235-243`.
  - `tb/verilator/engine/sim_main.cpp:490` and `:2967-2968`.
  - `tb/verilator/engine/mutants.py:220-223`.
- **Parent consumer locations:**
  - `hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv:115-127, 298-305, 433-440, 575-587`.
  - `KL_gptp_shadow.sv:985`.
  - `docs/design/GPTP_PLANE.md:131-132`.

**Authority and evidence.**

The parent's egress reconstruction accepts a timestamp only while the applied addend satisfies `|adj| <= PHC_ADJ_MAX_C`. That constant is derived, "the same quantity the producer's own servo integrator is clamped to", from the clock the generator is given. The parent states that it "refuses exactly the steady rates its producer refuses to ask for, and a transient proportional excursion past that clamp is a counted loss" (txret :115-127). `GPTP_PLANE.md:131-132` states it for the product: "a record whose `adj_abs_w` exceeds `PHC_ADJ_MAX_C` is returned as a loss".

At this head the slew arm keeps a saturated input for as long as |offset| > 20 us. The integrator reaches its rail after about five pairs (40 ppm per pair), and the written addend then sits at `kp_sat + ILIM`. The new text in `INTEGRATION.md` records that value as "about 320 ppm" and says it lasts "tens of minutes". The author's own public model gives a 320.0 to 320.1 ppm peak for 33 to 83 minutes.

`receipts/envelope-table.log` computes this with the generator's own `set_servo_gains` and the parent's envelope formula. The sustained trim is 320 ppm against a 200 ppm envelope at 2, 25, 50, 100 and 125 MHz: REFUSED at every clock. Before #68 the same magnitude occurred only transiently, because every offset over 20 us stepped.

The donor already recorded the downstream chain:

1. A refused Pdelay_Req result goes to TXLOST, which clears `S_T1V`/`S_PDWAIT`, so that exchange never completes (`gen_gptp_ucode.py:1163-1186`).
2. The fourth consecutive incomplete exchange clears asCapable (`:1395-1418`).
3. Sync and Follow_Up are consumed only while asCapable (`:707-708`, `:729-730`).
4. The SERVO leg is the only writer of the PHC region (`:797`, `:818`), so the out-of-envelope addend is never rewritten.
5. Mastership needs asCapable (`:1562-1571`).

**Demonstrated in the parent's own `tb/verilator/gptp_shadow` bench** (real `KL_gptp_txret`, gitlink content at this head; probes add prints only):

- **Synchronized +10 ms master jump** (`receipts/parent-shadow-wedge-head.log`, patch `scripts/probe-wedge-10ms.patch`):
  - The addend pins at 2,684,363, against an envelope of 1,677,722.
  - The lost-result counter reaches 4, and flags fall from 13 to 1 by pair 30 (asCapable and sync-ok gone).
  - The offset freezes at -9,513,606 ns.
  - Refusals keep climbing to 16 through pair 118, and nothing recovers.
- **The issue's own required case**, a first synchronization 900 ms off after a receipt timeout (`receipts/parent-shadow-wedge900-head.log`, `scripts/probe-wedge-900ms-first.patch`): the same wedge from about pair 25, with flags at 1 to the end.
- **Base contrast** (`*-base.log`): the old rule steps, and the same harness locks with zero refusals. That shows the scenario is otherwise healthy. It is not the target behaviour, since the recorded rule requires these offsets to slew.

**Tests.**

The donor harness models the PHC with no consumer envelope (`sim_main.cpp:490`). Its phase 13 asserts as correct the very value the consumer refuses: "widest slew is the pre-#68 envelope" equals `slew_envelope()`, which is `kp_sat + ILIM` (`:2967-2968`). No test in either repository drives a slew longer than four Pdelay intervals against an enforcing consumer.

**Docs.**

`INTEGRATION.md:235-243` gives the 320 ppm figure but does not say that it exceeds the +-200 ppm integrator clamp that consumers derive their envelope from. DECISION item 2 and the PR body say the trim "never exceeds what the old loop could already program". That is true in magnitude, but the old loop held it only transiently, and the consumer contract distinguishes transient from sustained. The PR's read-only parent check covered the addend's signedness but not its range.

**Impact.** In the parent product, a slew that keeps the trim out of envelope for four consecutive Pdelay intervals wedges the plane. That covers the 900 ms first synchronization that #68 requires to slew. It also covers any synchronized offset jump beyond roughly 1.3 to 1.6 ms at the 320 ppm slew rate; that threshold is analysis, while the 10 ms and 900 ms cases are measured. The wedge persists until a reset or an external override:

- every egress timestamp is refused;
- asCapable falls and cannot be re-earned;
- Sync is never consumed again;
- the plane can neither synchronize nor take mastership;
- its PHC runs about 320 ppm off.

This defeats the recorded rule's "below that it slews through the rate path" end to end. It violates REQ-PTP-05 (the fabric PHC servo) and #68's acceptance to keep the parent suites green at the pin.

**Required outcome.** For as long as a slew lasts, the trim the plane holds must be one its consumer accepts. Egress timestamps and asCapable must then survive every slew the recorded rule allows: up to one second at a first synchronization, and unbounded when synchronized. The alternative is a recorded cross-repository decision that changes the consumer's envelope contract, with an owned parent change landing with the pin. Whichever holds, three things must also be true:

- the donor's integration guide states the sustained-trim bound consumers may rely on;
- a test drives a slew longer than allowedLostResponses + 1 Pdelay intervals against an enforcing consumer (the parent bench, or a donor harness that models the envelope) and shows asCapable held and results measured;
- a mutant that restores an out-of-envelope sustained trim is caught.

**Verification.**

- `scripts/parent_shadow.sh <label> <fixed-head> scripts/probe-wedge-10ms.patch`, and the same with `probe-wedge-900ms-first.patch`. Through the slew, flags keep bit 2, bit 3 returns after convergence, and `phcl` does not grow each Pdelay interval.
- The donor engine suite and mutation arm are green with the new test and mutant.

### F2 MAJOR: #68 acceptance "keep the parent's regenerated ROM digests and suites green at the resulting pin" is not met

- **Severity:** MAJOR.
- **Lenses:** Conformance, Tests.
- **Where:**
  - The #68 issue body, Scope paragraph.
  - Parent `tb/verilator/gptp_shadow/sim_main.cpp:959-991` (phase 4) and `:672-685` (the reconstruction law).
  - Parent `tb/verilator/gptp_plane/sim_main.cpp:420-485` (phase 4).

**Authority and evidence.**

With the donor tree at this head in place of the pin, `gptp_shadow` gives 307/309 (`receipts/parent-shadow-head.log`, reproduced in `parent-shadow-recheck-head.log`) against 309/309 at base. `gptp_plane` gives 24/29 (`receipts/parent-gptp-plane-plane-head.log`) against 29/29 at base. The manager's receipts cover `gptp_shadow` only.

On the manager's two questions:

- **`gptp_shadow` "closed loop locked": the manager's reading is confirmed.** Phase 4 jumps the master 1 ms while the plane is synchronized and expects lock within 12 pairs. Under the recorded rule that pair slews, the addend rails (`receipts/parent-shadow-adj-head.log`: 1,325,294 rising to 2,684,363 by pair 5), and a 1 ms slew needs about 25 pairs.
  - **`gptp_plane`'s five failures have the same cause:** "one adjtime re-base", "re-base near +1 ms", "measured offset locked", "addend at the +100 ppm ideal" and "counter tracks the master". Phase 4 expects a first synchronization 1 ms off to re-base, and the recorded rule makes it slew.
- **`gptp_shadow` "every measured result reconstructs its own launch", 19 wrong: explained. It is a consequence of the policy in this bench's shape, not a reconstruction defect** (`receipts/parent-shadow-probe-head.log`, `parent-shadow-adj-head.log`).
  - All 19 are measured results (`ok=1`), each with the addend at 1,442,253 at both launch and delivery, and a deviation of 4 to 5 ns.
  - That addend is the integrator the phase-4 slew railed. The plane carried it through the grandmaster change and into mastership.
  - This bench runs an 8 ns counter (`PHC_TICK_NS_P = 8`) but declares 2 MHz to both the generator and the envelope (`PHC_CLK_HZ_P = CLK_HZ_P`). An in-envelope addend is therefore about 1.07% of the tick here, and the fixed-duration reconstruction over about 50 ticks is off by about 4.3 ns.
  - In a product whose declared clock is its PHC tick, the same in-envelope addend is at most 200 ppm, and the error is at most 0.09 ns (`GPTP_PLANE.md:131-132`).
  - The same run also shows F1's refusal: a LOST Pdelay_Req result at k=24, with the addend at 2,684,363.

**Impact.** The frozen acceptance fails at the pin. Adopting this head leaves two parent suites red. Their expectations encode the retired rule, and the reconstruction law assumes an addend that is small relative to that bench's tick.

**Required outcome.** An owned parent change (in the #387 adoption lane or a parent issue) updates both phase-4 expectations to the recorded rule. It must also make the `gptp_shadow` reconstruction law hold, or re-scope it honestly, without weakening its product meaning. That change must be ready with the pin. F1's resolution may change these trajectories, so the parent change is judged against the fixed donor head.

**Verification.** Parent `gptp_shadow` and `gptp_plane` pass, together with the manager's parent consumer gates and the other gPTP ROM consumers, with the `gptp-processor` gitlink staged at the fixed donor head.

### S1 SUGGESTION: the `e_sat` docstring overstates its domain

- **Severity:** SUGGESTION.
- **Lenses:** RTL, Docs.
- **Where:** `hdl/ucode/gen_gptp_ucode.py:680-694`.
- **Evidence:** the docstring says the helper saturates any signed value. For inputs within `lim` of 2^63-1 the sum wraps negative, and the helper returns `-lim` (`receipts/esat-edges.log`, an exact 64-bit model of the emitted words). The integrator operand is bounded. For the offset operand, the PHC would have to read near 2^63 ns (about 292 years), so this is unreachable in practice.
- **Suggested change:** state the domain in the docstring, or take the sign from the input. This does not affect coverage.

## What was verified clean inside each lens

These results stand but do not clear any lens while F1 or F2 is open under it.

- **Conformance.**
  - The implemented rule matches the recorded rule under the author's DECISION reading, and that reading is faithful:
    - A step needs a first pair, meaning the sync verdict is clear (`gen:775-778`), and |offset| above 1 s exactly (`gen:806-816`; exactly 1 s slews).
    - A grandmaster identity change clears the verdict (`gen:1535-1538`); a same-grandmaster parent refresh keeps it.
    - The receipt timeout clears it (`gen:1801-1807`).
    - Every asCapable fall zeroes the ladder (`gen:1369`, `1416`, `1781`), and a rise needs two exchanges at the 1 s cadence (`gen:1771-1776`). Consumption stops at the fall (`gen:707`, `729`), and the only arming of the 375 ms watch is a consumed pair (`gen:800`). So the timeout always clears sync-ok before asCapable can return, and "first after asCapable" holds.
    - Treating a grandmaster change as first is what makes clause 3 ("does not step when the new offset is below the threshold") and #387 acceptance 3 (a grandmaster change stepping more than 1 s) coherent.
  - The signed Q8.24 addend documentation matches REQ-PTP-01 and the engine.
- **RTL.**
  - The new divisor 2e9+1 fits the 32-bit DIVU divisor (`KL_gptp_ucpu.sv:20-22`, `619-624`), and the `e_sat` immediates are under 2^24.
  - Saturation keeps the 32x32 MULS operand exact.
  - The step path writes adjtime before adjfine (`gen:817-822`).
  - The engine pulses last one cycle, the data holds between pulses, and reset zeroes it (`KL_gptp_engine.sv:781-784`, `796-797`, `899-903`).
  - `receipts/rom-check.log`: all four tracked images regenerate byte-identical from the head generator. Only words 651..702 change (652..703 in the seeded images), and no other leg moves at 2, 25, 50 or 125 MHz or in the seeded images.
- **Robustness.** The ±1 s and ±(1 s + 1 ns) boundaries are exercised by the engine harness. Otherwise see F1 and S1.
- **Tests.**
  - `receipts/donor-engine-run-head.log`: 1137/1137 on each of the three images.
  - `receipts/donor-engine-mutants-head.log`: 23/23 mutants caught, with the unmutated control passing. The nine #68 mutants each hit their own rule.
  - The harness mirror is written from the documented rule, and the `first` flag is scripted by each phase, not read from the DUT.
  - The required cases are present: phase 13 (900 ms slews with no step), 13b (1.1 s steps once, and the ±1 s boundary), 18c (grandmaster change at 300 us, no step, with a 1.5 s contrast), and 10 and 21 (first synchronization after asCapable).
- **Docs.**
  - The `INTEGRATION.md` policy and pulse-semantics text matches the microcode and RTL (lines 161-243).
  - `SOURCE_EVIDENCE.md` and `TEST_DEVELOPER.md` each gain one accurate line.
  - No current guide restates the retired 20 us rule.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | #68 acceptance and DECISION, #387 decision, REQ-PTP-01/05/08/09, `gen_gptp_ucode.py` SERVO leg and flag writers, parent `gptp_shadow`/`gptp_plane` runs | R258-1 | `77c34e904eba2446755d13e1bf4763d1652c3ca7` |
| RTL | UNCLEAN (F1) | `gen_gptp_ucode.py:680-823`, `KL_gptp_ucpu.sv` MD/ALU operands, `KL_gptp_engine.sv` PHC face, parent `KL_gptp_txret.sv` envelope, ROM word diff | R258-1 | `77c34e904eba2446755d13e1bf4763d1652c3ca7` |
| Robustness | UNCLEAN (F1) | parent-bench long-slew probes (10 ms synchronized, 900 ms first), TXLOST and asCapable ladder paths, `e_sat` 64-bit edges | R258-1 | `77c34e904eba2446755d13e1bf4763d1652c3ca7` |
| Tests | UNCLEAN (F1, F2) | `tb/verilator/engine/sim_main.cpp` and `mutants.py` diff, engine run x3 and mutation arm, parent `gptp_shadow` and `gptp_plane` at head and base | R258-1 | `77c34e904eba2446755d13e1bf4763d1652c3ca7` |
| Docs | UNCLEAN (F1) | `docs/INTEGRATION.md`, `docs/SOURCE_EVIDENCE.md`, `docs/TEST_DEVELOPER.md`, generator docstrings, PR body, DECISION comment | R258-1 | `77c34e904eba2446755d13e1bf4763d1652c3ca7` |

## Limits

- No hardware, no synthesis, no physical calibration. Field skips are not hardware proof.
- The donor repository has no hosted workflows at this head: zero check runs and zero statuses. No hosted job was executed or skipped.
- The parent probes ran on a disposable export of parent `574c29fa`. The donor tree was copied into the `gptp-processor` path at the head or base; it was not a registered gitlink, and `verilog-axis` was fetched at its pin.
  - Only the `gptp_shadow` and `gptp_plane` `run` targets were executed.
  - Not run by this review: the parent mutation arms, `milan_dp` (the gPTP-ON leg), `clkvalid`, `media_grid_align`, the idiom, xvlog and source-list gates, and the builder.
- The wedge was simulated in the parent bench shape: an 8 ns counter declared at 2 MHz. The product-clock claim rests on the shared derivation (`receipts/envelope-table.log`) and on `GPTP_PLANE.md`; it was not simulated at 50 or 125 MHz.
- The PR's follow-up observation about the neighbour rate ratio after a forward step was not examined.
- The author's per-test mutation matrix and ROM differential were read, not re-run. The engine mutation arm was run at the head only.
- The home and storage path prefixes in the receipts are replaced by `$HOME` and `$DATA`. They are otherwise raw.
- After the runs, `scripts/env.sh` was made location-relative with identical effective values. `receipts/parent-shadow-recheck-head.log` reproduces the head result under the rewritten file.

## Pending manager duties

- Route F1 as a cross-repository decision, since the fix may land in the donor, the parent, or both. Record the owner's acceptance of the DECISION reading.
- Own the parent change F2 names, and rerun the parent consumer gates. That includes `gptp_plane`, which is outside the manager's current receipts, and the `milan_dp` gPTP-ON leg, with the gitlink staged at the fixed head.
- Build and gate the final current-dev candidate at the merge turn: source base `c1b61743`, live dev `574c29fa`.
- Own hosted and act acceptance.
- A second independent positive review is still required.

## Receipts and reproduction

Every file in `receipts/` and `scripts/` is listed in `MANIFEST.sha256`. `scripts/env.sh` pins the head, base, parent and simulator. Run the following from the packet:

- **Donor:**
  - `scripts/donor_copy.sh engine-head <rev> -C tb/verilator/engine run`
  - `scripts/donor_mutants.sh mut-head <rev>`
  - `python3 scripts/rom_check.py <head-tree> <base-tree>`
  - `python3 scripts/envelope_table.py <head-tree>`
  - `python3 scripts/esat_edges.py`
- **Parent** (after a shallow parent export at `574c29fa` in `scratch/parent`, with `verilog-axis` at `48ff7a7e`):
  - `scripts/parent_shadow.sh <label> <rev> [patch]`
  - `scripts/parent_suite.sh <label> <rev> gptp_plane`
- **Probe patches:** built by `scripts/make_*_patch.py` from the pinned harness. They add prints only; the wedge probes exit after their loop.
- **Integrity:** `scripts/clone_integrity.sh` (`receipts/clone-integrity.log`: PASS). The review clone is at the exact head, clean including ignored and untracked files, with no hidden index flags. The index equals the head tree, and all 103 tracked blobs match in bytes and mode. This repository has no gitlinks.

R258-1 FINISHED
