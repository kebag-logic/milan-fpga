[R259] NEGATIVE - exact head 77c34e904eba2446755d13e1bf4763d1652c3ca7

Round R259-1, external independent review of Mister-M-alt/FPGA-gPTP issue #68 / PR #74.

| Item | Value |
|---|---|
| Head reviewed | `77c34e904eba2446755d13e1bf4763d1652c3ca7`, tree `10154fc3f95ccc542a6f5dcd8a58105d302fd1af` (one commit) |
| Source base | `c1b617435824929a790739ea8585c3fe1a328cc0` (the parent's current gitlink) |
| Parent consumer checked | kebag-logic/milan-fpga live dev `574c29fa111c74e5e5ed63e4670aff1f492e28e2` |
| Tool | Verilator 5.050 through the pinned wrapper, sha256 `905795b9...e92f` (`receipts/identity.log`) |
| Review clone after all probes | exact head bytes, modes and index; 0 gitlinks (the donor pins none) (`receipts/verify-clone.log`) |

Authorities, read in this order: parent `AGENTS.md` and `CONTRIBUTING.md` (the donor has neither); donor `docs/README.md`; issue #68 body, the manager's assignment comment, the author's DECISION comment (issuecomment-5790066720); the parent decision kebag-logic/milan-fpga#387 (issuecomment-5606198212) and #387's acceptance; parent `REQUIREMENTS.md` REQ-PTP-01/05/08/09. Then the diff `c1b61743..77c34e90`, the public author packet (`review-evidence/gptp68-r1/author-a188` at `5dafe5ab`) and the manager's receipts (`manager-r1` at `374e2008`, where the author packet is byte-identical).

## Summary

The step decision is correct. A pair steps only when it finds the published sync verdict clear and |offset| > 1 s. It is encoded exactly: the boundary is inclusive, the unsigned 64-bit tests are sound, and the ROM changes only the SERVO leg in every configuration. The new engine tests fail for each rule removed. The author's first-synchronization reading is consistent with the recorded rule, #387 decision (a) and #387 acceptance 3. The signed-addend correction is right.

The slew path is not. Under #68 the servo holds a trim of about 1.6 times its own integrator clamp for as long as |offset| > 20 us. The parent consumer refuses every egress timestamp while the trim exceeds exactly that clamp. The combination latches:

1. The plane's own Pdelay exchanges lose their t1.
2. asCapable falls and Sync consumption stops.
3. The out-of-envelope trim is held, so no egress timestamp is ever accepted again.

This was measured in the parent consumer path for the issue's own 900 ms case. The same scenario at the base steps once and stays locked. This is F1, a BLOCKER. It also means the parent path cannot be made clean by updating the parent test alone.

## Findings

### F1

```text
[R259] BLOCKER Conformance, RTL, Robustness, Tests, Docs - hdl/ucode/gen_gptp_ucode.py:783-797 (slew arm; only the integrator is bounded) with docs/INTEGRATION.md:235-243 and tb/verilator/engine/sim_main.cpp:2967 - a sub-second slew holds a trim the parent consumer refuses, which latches asCapable low with no recovery
```

**Requirement and evidence:**

- **Producer.** The #68 slew saturates only the PI input at ±20 us (`:783`) and clamps only the integrator to ±ILIM (`:790`). The written trim is kp + I (`:793-797`), which reaches 120 + 200 ≈ 320 ppm, or 1.6 × ILIM. It stays there as long as |offset| > 20 us. The suite asserts exactly this as the expected widest trim (`sim_main.cpp:2965-2968`). The author's own slew model gives a peak of 320 ppm held for 33 to 83 minutes on a 900 ms offset (`author-a188/receipts/servo-slew-model.log`).
- **Consumer.** At parent `574c29fa`, `KL_gptp_txret.sv` derives its addend envelope `PHC_ADJ_MAX_C` from the producer's own integrator-clamp expression (`:115-127`, `:298-305`). It marks every capture ineligible while `adj_abs_w > PHC_ADJ_MAX_C` (`:434-436`), and such a capture is returned as an explicit loss. The design text says "a transient proportional excursion past that clamp is a counted loss". The product instantiation keeps `RECON_REL_PPM_P = 200` (`KL_gptp_shadow.sv:978-987`, `milan_datapath.sv:6766-6772`), and the published error budget depends on it (`docs/design/GPTP_PLANE.md:132`). Under #68 the excursion is no longer transient.
- **Latch.**
  - A lost Pdelay_Req t1 leaves S_PDGOT clear (`gen_gptp_ucode.py:1163-1186`, `:1618-1640`). The lost-response ladder then drops asCapable at the fourth loss (`:1400-1418`).
  - Consumption stops. Only a consumed pair rewrites the addend, because `:797` and `:818` are the only PHC-region writers. The engine holds the data output between pulses (`KL_gptp_engine.sv:796-797`, `:899-903`), so the out-of-envelope trim stays applied.
  - The fabric owns the addend (parent REQ-PTP-09), so only a plane reset clears it.
- **Measured (probe D, `receipts/parent/D-*.probe.log`, `D-*.stdout.log`).** Parent gptp_shadow bench, donor hdl at this head. The #68 required case is a first synchronization 900 ms off, with a live master and a live Pdelay peer for 20 s.
  - The trim reaches 2,684,363 (1.6 × the envelope 1,677,722) at pair 4.
  - From about 6.2 s, every Pdelay_Req result is refused as a PHC-history loss.
  - asCapable falls at pair 39, about 10.3 s, and never returns.
  - Sync-ok clears, the offset freezes at -898,503,363 ns, and the trim holds at 2,684,363.
  - 20 of 20 Pdelay_Req are refused by the end.
  - The identical scenario with the donor at base steps once (+900,001,193 ns), locks within ±1 ns, and loses nothing.
- **Why it is not a bench artifact.** The servo gains and the consumer envelope derive from the same `CLK_HZ_P`, so the 1.6 ratio and the four-lost fall do not depend on the clock. The latch is inherent to the pinned combination.

**Impact:** The parent's own decision (#387 (a)) makes this path normal: "below that it slews through the rate path". Consider a first synchronization whose offset is a few milliseconds up to 1 s, for example:

- a grandmaster change to a clock that far off;
- the first pair after asCapable returns from a long outage;
- a synchronized servo facing a comparable jump.

In each case the plane loses its link verdict and its Sync consumption. It then stays desynchronized, with its PHC running at the held trim, until a reset. The offset range is by analysis; only the 900 ms case is measured. Downstream, #387 acceptance 4 (the relock measurement) cannot be met through this path.

**Required change:** Make the producer's sustained trim and the consumer's reconstruction envelope consistent, and record which side changes as a public decision on #68 and #387. The two sides are parent and donor. The outcome must be:

- a first-synchronization slew of any |offset| up to 1 s never drives the trim outside the consumer's envelope long enough to latch asCapable low;
- a synchronized servo facing a large offset does not either;
- a trim held when consumption stops cannot leave egress timestamps refused indefinitely.

The design is not prescribed. Possible routes include bounding the whole written trim rather than only its integrator, re-deriving the consumer envelope and error budget, or a defined fallback for the held trim. `docs/INTEGRATION.md` must state the resulting trim bound and what happens to the held trim when consumption stops. The DECISION's "never exceeds what the old loop could already program" must be corrected for duration.

**Verification:**

- Re-run probe D (`scripts/parent_probes.sh`) with the fixed head content. asCapable must stay up, or recover, through the 900 ms first synchronization, with PHC-history refusals bounded.
- An executable test in the owning repository must fail on the current head for this mechanism.
- If the parent envelope changes, the parent's gptp_shadow reconstruction law must be re-derived against it.
- The engine suite and its mutation arm must stay green.

### Suggestions (no effect on the verdict)

```text
[R259] SUGGESTION Tests - hdl/ucode/gen_gptp_ucode.py:1588 with docs/INTEGRATION.md:215 - the documented "becoming grandmaster clears the verdict" has no guarding check
```

Reviewer mutant R2 keeps sync-ok on become, and it survives the whole engine suite (`receipts/engine/mutants-reviewer.log`). It is equivalent for the step decision, because any later slave pair must follow a grandmaster-identity change, which clears the verdict (`:1538`). It does change the published verdict while this plane is grandmaster. Add a check, or record it as an equivalent mutant.

```text
[R259] SUGGESTION Docs - docs/INTEGRATION.md:200-208 and :255 - say what bit 3 and pub_offset_o mean while a slew is in progress
```

A first-synchronization slew raises the sync verdict with up to 1 s of offset outstanding, and #68 can keep it there for tens of minutes. `pub_offset_o` carries the low 32 bits (`KL_gptp_engine.sv:862`), which wrap beyond ±2.147 s. Under #68 such offsets can persist on a synchronized servo instead of being stepped at once. A reviewer probe with a wrapped master time published +899,998,807 ns for a 64-bit offset near -1.27e18 ns. Consumers such as #387's tu logic need both facts stated.

## Parent consumer failures raised by the manager, resolved

The failures were reproduced independently. At head, gptp_shadow gives 307/309; at base, 309/309 (`receipts/parent/A-*.stdout.log`).

1. **`closed loop locked` - CONFIRMED as the retired step policy's expectation.** The phase shows a synchronized servo a 1 ms master jump. #68 slews it with a saturated input: over 12 pairs the offset goes from -1,002,420 to -609,014 ns while the trim rails at 2,684,363 (`B-head.probe.log`, PROBE LOOP). At base the jump steps at pair 0 and locks to -5 ns. Counterfactual C rescripts only that phase as a first synchronization 1.5 s off, after the 375 ms receipt timeout. It passes 310/310 at both head and base (`C-*.stdout.log`).
2. **`every measured result reconstructs its own launch` (19 wrong) - EXPLAINED.** It is a consequence of the same slewed jump, not an independent donor defect.
   - The slewed jump leaves the integrator on its -ILIM rail. All 19 wrong results launched with an in-envelope trim of 1,442,253 units and land +4 to +5 ns late (`B-head.probe.log`, PROBE RECON).
   - At base the same launches carry -222,075 and land -1 to 0 ns (`B-base.probe.log`).
   - In this bench, 2 MHz servo gains drive an 8 ns counter. That trim is about 0.086 ns per tick over the roughly 52 nominal periods the reconstruction subtracts, which exceeds the bench law's ±1 ns (`kPhcTruncNs`). In the product configuration the same in-envelope term is at most 0.09 ns (`GPTP_PLANE.md:132`).
   - With counterfactual C there are 0 wrong results.

   The parent adoption lane must update this bench (the phase, or the law's tolerance).

A parent test update is necessary, but because of F1 it is not sufficient to make the parent path clean.

## Acceptance (issue #68, as frozen and as assigned)

| Criterion | Status | Evidence |
|---|---|---|
| State the policy (threshold, first-sync rule, GM-change rule, `phc_step_we_o` pulse semantics) in `docs/INTEGRATION.md` | Met in content, incomplete on the slew contract (F1) | `INTEGRATION.md:148-243` checked against RTL `:775-784`, `:796-797`, `:899-903` and generator `:797`, `:818`, `:1538`, `:1588`, `:1804` |
| Microcode implements exactly the rule | Step decision met; slew path not met in the consumer path (F1) | Code at `:767-822`; mutants 14 to 22 and R1, R3, R4, R6, R7, R10, R12 caught; probe D |
| Engine tests: 900 ms slews with no step, 1.1 s steps once, GM change with small offset no step | Met, each fails when its rule is removed | Phases 13, 13b, 18c, 10, 21; `receipts/engine/*` |
| Parent regenerated ROM digests and suites green at the resulting pin | NOT met at this head (retained R258-1 F2) | gptp_shadow 307/309 (A-head); gptp_plane 24/29 (E-head, run after the verdict was written); the parent change needed goes beyond the tests (F1) |
| DECISION 1, first-synchronization reading | Accepted | Clear paths `:775`, `:1538`, `:1588`, `:1804`; asCapable fall paths keep the verdict and the 375 ms timeout clears it before asCapable can return (ASCAP_UP_C = 2 at the 1 s cadence) |
| DECISION 2, PI input saturated at ±20 us | Bit-identical inside the band; incompatible outside it with the consumer (F1) | Code; R3 and R4 caught; author differential receipt |
| DECISION 3, signed addend | Accepted | `bench/arty/bench_phc.sv:50`; parent `timestamp_counter.sv:110`, `:144-145` |
| ROM: only the SERVO leg changes | Met | `receipts/rom-check.log`: four tracked images regenerate byte-identically. In 10 configurations (both seeded images; 1, 2, 25, 50, 100 and 125 MHz; other MAC and p1), 52 words change inside SERVO (651..702, or 652..703 seeded) and no leg moves |

## Clean-result evidence per lens (examined, apart from F1)

- **Conformance.** The step rule, the exact 1 s boundary (`:809-816`, a u64 DIVU with a 32-bit divisor 2e9+1, and a 64-bit zero compare in `KL_gptp_ucpu.sv:193-203`, `:619-624`), the first-synchronization reading, the GM-change and same-GM-refresh behaviour (R12 caught), and the #387 acceptance 3 shape (phase 18c contrast arm) are all correct.
- **RTL.** There is no RTL diff. The `e_sat` arithmetic is exact within the operand widths (a 24-bit immediate divisor is asserted, `:685`). MULS never sees more than ±20000 × gain. The step still writes -offset before the bare-integrator addend. SERVO grows 48 to 52 words in place.
- **Robustness.** Reset zeroes the verdict and both PHC data outputs. The seeded images pass. The only hazard found is F1.
- **Tests.**
  - Engine: 1137/1137 on all three images (`receipts/engine/engine-run-head.log`), and the suite's own arm catches 23 of 23 with the control passing.
  - Reviewer mutants: 7 of 8 caught; the survivor, R2, is equivalent for the step decision (see the suggestion).
  - tsngen 288/288 and ucpu 768/768 on the regenerated images.
  - contract, lint and docs (with diagrams and selftests) pass (`receipts/donor-gates/`).
- **Docs.** The pulse-semantics lines, the verdict-clear list and the grandmaster-change text are accurate against the code. `SOURCE_EVIDENCE.md` and `TEST_DEVELOPER.md` rows are accurate. No added line carries U+2014.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1; retained R258-1 F2) | #68 body and assignment, DECISION comment, #387 decision (a) and acceptance 3 and 4, REQ-PTP-01/05/09; `gen_gptp_ucode.py:767-822`, `:1400-1418`, `:1538`, `:1588`, `:1804`; parent gptp_shadow at `574c29fa` (probes A to D) | R259-1 | `77c34e904eba2446755d13e1bf4763d1652c3ca7` |
| RTL | UNCLEAN (F1) | `gen_gptp_ucode.py:680-694`, `:767-822`, generated ROMs (`rom-check.log`); `KL_gptp_ucpu.sv:185-230`, `:595-640`; `KL_gptp_engine.sv:767-926`; parent `KL_gptp_txret.sv:115-127`, `:298-305`, `:425-470`, `KL_gptp_shadow.sv:978-987` | R259-1 | `77c34e904eba2446755d13e1bf4763d1652c3ca7` |
| Robustness | UNCLEAN (F1) | Lost-t1 and ladder paths `:1163-1186`, `:1400-1418`, `:1604-1640`; held-trim behaviour; seeded images; probe D at head and base | R259-1 | `77c34e904eba2446755d13e1bf4763d1652c3ca7` |
| Tests | UNCLEAN (F1; retained R258-1 F2) | `tb/verilator/engine/sim_main.cpp` diff (phases 10 to 21, `expect_policy_pair`, mirror), `mutants.py:180-228`; engine run ×3; 23-mutant arm; 8 reviewer mutants; tsngen and ucpu runs | R259-1 | `77c34e904eba2446755d13e1bf4763d1652c3ca7` |
| Docs | UNCLEAN (F1) | `docs/INTEGRATION.md:148-295`, `docs/SOURCE_EVIDENCE.md:29`, `docs/TEST_DEVELOPER.md:99`, generator docstring `:15-25`, `:162`; PR body; the issue's DECISION and REVIEW READY comments | R259-1 | `77c34e904eba2446755d13e1bf4763d1652c3ca7` |

## Limits

- No hardware, no physical calibration (NOT RUN), no synthesis. Field skips are not hardware proof.
- The latch was measured in the parent gptp_shadow bench configuration: 2 MHz servo gains on an 8 ns counter, slewing about 62 times faster in relative terms than the product. The product claim is by construction (the same `CLK_HZ_P` derivation on both sides, `RECON_REL_PPM_P = 200`), not simulated. The offset range quoted in F1 is analysis.
- Parent probes ran in disposable replicas: parent `hdl/`, `tb/common` and `tb/verilator/gptp_shadow` at `574c29fa`, plus the donor `hdl/` at head or base and verilog-axis at its gitlink `48ff7a7e`. Only the gptp_shadow `run` target was used, and B to D add report-only instrumentation. The gptp_plane `run` target (E) was added after the verdict was written. No parent bank was run. The parent idiom, xvlog, source-list and builder gates are the manager's receipts, not re-run here.
- Donor suites not re-run here: parser, gaskets, bench tag test, and the tsngen and gaskets mutation arms. They are covered by the manager's full donor `make -j8` at this head (exit 0).
- The author's ROM differential, slew model and base-harness-on-new-ROM scripts were read as receipts, not re-executed.
- The donor repository has no hosted workflows, and there are 0 check runs at this head.
- One parent-suite build used that Makefile's default Verilator `-j 0` (all host cores) for about 5 s before later builds were capped at `-j 8`. This is disclosed as a deviation from the 8-job limit.
- The internal reviewer's local packet was not read.

## Pending manager duties

- Do not merge. F1 and the retained F2 are open, and the parent consumer gate is not clean at this head: gptp_shadow and also gptp_plane, which is outside the manager's current receipts. Under the parent-consumer rule, an owned parent change must also address F1, not only these tests.
- Obtain and record the F1 decision on #68 and #387: which side changes the trim bound or the envelope, and the held-trim behaviour.
- After a new head: re-review all five lenses, re-run probe D and the parent consumer gates with the gitlink staged, and regenerate the parent ROM digests.
- At the merge turn: validate the current-dev candidate (source base `c1b61743`, live dev `574c29fa` or later), and handle hosted and act acceptance.
- Physical calibration remains NOT RUN.

## Public review findings on this PR, resolved or retained

None existed on PR #74 or issue #68 at the start of this round: only manager and author comments, no reviews.

After the verdict line, F1 and the ledger above were written, the concurrent internal round's comment was read: `[R258] NEGATIVE`, issuecomment-5791184500, posted 07:55Z at this head. My position on each of its findings at this head:

```text
[R259] RETAINED BLOCKER Conformance, RTL, Robustness, Tests, Docs - R258-1 F1 (slew trim beyond the consumer envelope wedges the plane)
```

This is the same defect as F1 above, found and measured independently (probe D). It stays open.

```text
[R259] RETAINED MAJOR Conformance, Tests - #68 acceptance "keep the parent's regenerated ROM digests and suites green at the resulting pin" (R258-1 F2)
```

It is open at this head. The evidence is independent:

- parent `gptp_shadow` gives 307/309 at head against 309/309 at base (`receipts/parent/A-*`);
- parent `gptp_plane` gives 24/29 at head against 29/29 at base (`receipts/parent/E-*`, `scripts/parent_gptp_plane.sh`).

All seven failing checks encode the retired step expectation: a 1 ms offset that is re-based (gptp_plane phase 4 `:420-465`; gptp_shadow phase 4 `:958-992`). The 19 reconstruction misses follow from it, as explained above. Required outcome: an owned parent change updates those expectations and the gptp_shadow reconstruction law, judged against the fixed donor head, because F1's fix changes these trajectories. Verification: both suites and the manager's parent consumer gates pass with the gitlink staged at the fixed head. The ledger rows for Conformance and Tests were already UNCLEAN and carry this finding too.

```text
[R259] RETAINED SUGGESTION RTL, Docs - hdl/ucode/gen_gptp_ucode.py:680-694 - the e_sat docstring claims any signed value (R258-1 S1)
```

This is agreed by inspection. The bound's sign is taken from the sum reg + lim, which wraps for reg within lim of 2^63-1. The integrator operand is bounded, and the offset operand cannot reach that range from a real PHC. There is no effect on the verdict.

## Reproduction

The environment needs `REVIEW_CLONE` (the exact-head clone) and `PINNED_BIN` (the Verilator 5.050 wrapper directory).

- `scripts/identity.sh` and `scripts/verify_clone.sh`: identity and clone-integrity receipts.
- `scripts/engine_suite_run.sh <donor> <log>` and `scripts/suite_run.sh <donor> <suite> <log>`: donor suites.
- `scripts/engine_mutants_run.py <donor> author <i> <j>` or `... reviewer`: the suite's own arm in slices, and the reviewer mutants.
- `scripts/rom_check.py <head> <base>`: ROM regeneration and word diff.
- `scripts/parent_probes.sh <work> <out>`: parent probes A to D. It uses `instrument_gptp_shadow.py`, `counterfactual_first_sync_loop.py` and `probe_long_slew.py`.
- `scripts/parent_gptp_plane.sh <work> <out>`: E, the parent gptp_plane suite at head and base.
- `scripts/sanitize_receipts.sh`: path placeholders.

Every publishable file is in `MANIFEST.sha256`.

R259-1 FINISHED
