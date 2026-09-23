[A199] Step over 20 us at link-up and over 100 us once locked, and clamp the whole trim to 200 ppm (#68)

Correction round on this PR under the owner's re-decided policy (https://github.com/Mister-M-alt/FPGA-gPTP/issues/68#issuecomment-5794731372). It resolves R258-1 F1 (BLOCKER), R258-1 F2 (MAJOR) and R259-1 F1 (BLOCKER), and takes up both reviews' suggestions.

| Item | Value |
|---|---|
| Branch | `68-step-policy` |
| Head | `cbccf226068c107fb30764891c98b8d70c54d775`, tree `e8b9fa23fe5e1d5e3bd3ab1dd3c09196760a5063` |
| Parent of head | `77c34e904eba2446755d13e1bf4763d1652c3ca7` (the reviewed head) |
| Base (main) | `c1b617435824929a790739ea8585c3fe1a328cc0` |

## What the plane does now

The offset is local time minus grandmaster time.

| Servo state | Slews while \|offset\| is | Steps when \|offset\| exceeds |
|---|---|---|
| Link-up | at most 20 us | 20 us |
| Locked | at most 100 us | 100 us |

- **Link-up** is the first pair consumed after any of these:
  - asCapable rises, which includes after every reset, cold or warm;
  - a 375 ms Sync receipt timeout;
  - this plane was grandmaster.

  Losing asCapable stops Sync consumption, and the receipt timeout always fires before asCapable can return. So the first pair after asCapable is a link-up.
- **Locked**: every consumed pair locks the servo. A grandmaster identity change still clears the published sync verdict (`pub_flags_o` bit 3, unchanged), but it leaves the servo locked. So the next pair uses 100 us.
- **Each step is one `phc_step_we_o` pulse carrying -offset.** It is followed by one addend pulse carrying the retained integrator alone. Stepping was already this shape before; only when it fires has changed.
- **The whole written trim, proportional plus integral, is clamped to +-200 ppm**, and so is the integrator. The step's bare integrator is inside the envelope too. The engine holds each trim between pulses, so a trim held after consumption stops is inside the envelope as well.

**Reading, flagged for the reviewers.** The manager's assignment defines link-up as the pair that raises the sync verdict, and the owner's decision keeps a grandmaster change locked. The implementation matches both: a link-up pair is exactly the pair that raises the verdict, except after a grandmaster identity change clears it. Two consequences follow:

- A receipt timeout while asCapable holds makes the next pair a link-up.
- A return from being grandmaster makes the next pair a link-up.

If only an asCapable rise was meant, delete the one `S_LOCK` write in the SRTO leg. The mutant "a receipt timeout keeps the lock" shows which tests would then change.

### The clamp, derived as the parent derives `PHC_ADJ_MAX_C`

`KL_gptp_txret.sv` refuses every egress timestamp while `|adj| > PHC_ADJ_MAX_C`, where

```text
PHC_ADJ_MAX_C = (RECON_REL_PPM_P * 2^24 * 1000 + PHC_CLK_HZ_P / 2) / PHC_CLK_HZ_P
```

Here `RECON_REL_PPM_P = 200`, and `PHC_CLK_HZ_P` is the clock the generator is given.

- The generator now computes its rate envelope with the same integer expression, rounded half up, in the new `ppm_addend(ppm, clk_hz)` with `RATE_PPM_C = 200`.
- Before, it used `round()` on a float, which differs only at exact ties. So the two agree to the unit at every clock.
- One value, `RUNTIME["ilim"]`, clamps both the integrator and the whole trim. No constant is copied.
- `receipts/rom-differential-head.log` checks the ROM against the parent's expression at 2, 25, 50, 100 and 125 MHz: 1677722, 134218, 67109, 33554 and 26844 units.
- The engine harness derives the consumer envelope from the same expression, written out on its own. It grades every addend pulse of the run against that envelope.

### Why the slew input is no longer saturated

Every slewed offset is now at most 100 us, because anything larger steps. So the 32 x 32 MULS operand is exact without the previous head's +-20 us input saturation, and that saturation is removed.

A per-pair model (`scripts/slew_variants_model.py`, `receipts/slew-variants-model.log`) compares both variants under the new clamp, for jumps up to +-100 us against masters at -140, 0 and +140 ppm:

- **Settling:** both settle within about 1.0 to 2.6 s.
- **Overshoot:** at most 42.5 us, far under the 100 us that would step.

Keeping the saturation did not fit the ROM; see "ROM" below.

## Microcode

`hdl/ucode/gen_gptp_ucode.py`:

- **SERVO (52 -> 51 words).**
  - The step threshold is `STEP_LINKUP_NS_C + S_LOCK`: 20000 at link-up, 100000 once locked.
  - The step test is `(offset + T) / (2T + 1) == 0`, a u64 DIVU with a 32-bit register divisor. That is exactly `|offset| <= T`, so exactly the threshold slews.
  - The step arm writes adjtime `-offset`, then the bare integrator.
  - The slew arm is the v5 PI with its input unsaturated and the integrator clamp unchanged.
  - Both arms end in one `e_sat` clamp of the whole trim to `+-RUNTIME["ilim"]`.
  - The tail writes `S_LOCK = STEP_LOCKED_NS_C - STEP_LINKUP_NS_C`.
- **New scratch cell `S_LOCK = 43`.** Its written-before-read invariant is recorded at the scratch map.
  - It has no init and no reset-backed validity, and scratch survives a warm reset.
  - Its only reader, SERVO, runs only while asCapable stands.
  - Reset clears asCapable, and asCapable's single setter, the PDPAIR verdict, writes `S_LOCK = 0` whenever it finds the flag clear.
  - A pre-reset lock can therefore never reach the first pair after a reset. The warm-reset phase 28b proves it, and the mutant "asCapable's rise keeps the lock" is caught there.
- **PDPAIR (59 -> 61).** The verdict tells a rise from a repeat and writes `S_LOCK = 0` on the rise. The `S_PDGOT` write both verdicts made now leads the verdict. Only compares, which write nothing, moved past it, so the write order is unchanged.
- **SRTO (5 -> 6) and BECOME (21 -> 22)**: each writes `S_LOCK = 0`.
- **`e_sat` docstring** states its exact domain (R258-1 S1).

**Inside +-20 us the loop is bit-identical to the base wherever the base's trim stayed inside +-200 ppm.** The receipt `rom-differential-head.log` executes the real SERVO words of the base and head images at five clocks, with random offsets and integrators including both rails:

| Case | Result |
|---|---|
| In band, base trim inside +-200 ppm | 5762 to 5934 cases per clock write identical sequences |
| In band, base trim outside +-200 ppm | 1405 to 1562 cases per clock differ ONLY in the trim, which is exactly the base trim clamped |
| Head image against the documented rule | matches, 20100 cases per clock |
| Base image against the pre-#68 rule | matches, which validates the emulator |

The same receipt executes PDPAIR from both images. Their writes are identical and in the same order, plus one `S_LOCK = 0` exactly at an asCapable rise. It also emits every other program of the base generator at the new addresses, and each is word-for-word the head image. Only SERVO, PDPAIR, SRTO and BECOME change content.

## ROM

The ROM had 15 free words, and the largest gap was full. To fit, first-fit packing moved these legs:

- BECOME 159 -> 103, TXLOST 103 -> 159, TXT1OK 180 -> 181, SRTO 59 -> 249;
- FUTO 125 -> 59, PDREQ 898 -> 900, SYNCTX 957 -> 959, RESUME 1014 -> 1016.

These moves also change the branch words that name those legs. SERVO stays at 651 (652 in the seeded images) and PDPAIR at 839. Real words go 989 (base) -> 993 (reviewed) -> 996 of 1024, in every configuration tried.

| Tracked image | Generator arguments | SHA-256 at base `c1b6174` | SHA-256 at reviewed `77c34e9` | SHA-256 at head |
|---|---|---|---|---|
| `tb/verilator/engine/gptp_ucode.hex` | `--clk-hz 2000000 --cease-ms 3000` | `dee031848c5410d4f0d819eb3d5b124a8d2d0c95b83ffd465dfbff6b15f5c5d9` | `1e52fb26135da78254b96ab5349e2cf590c334d928a17cdee4cceb159a7ba823` | `e06b74c4cba2768fb3ccf7f737f106114c19fb96736563b48e29713c583d73e2` |
| `tb/tsngen/gptp_ucode.hex` | `--clk-hz 2000000` | `a5d3f91884943afab62c99fe9bbf0111cde8cffe4b318f0cfe9ba1fab9aeba7d` | `7e64371861e6f54ac824c4adb429ff8308919f371b8ad92336cdbad77a902d5d` | `7316979d77ae9f05c1edff424b111291aaff20b6f1c841c53969e0b0370c19f0` |
| `tb/verilator/ucpu/gptp_ucode.hex` | defaults | `83f14a7d020d6b3d95d5e0e8e9cb878ac78d0a6aed7812ffac9b2dc39981a939` | `f3d73858d62b484145653ce55df239620fede86be7d1f22a093d234b054f2762` | `02fbcec209d38eb039371c879982b71eff371052a67ea4bfd8b97a0cb86acf11` |
| `syn/ooc/work/gptp_ucode.hex` | defaults (the generator step of `syn/ooc/run.sh`; synthesis not run) | `83f14a7d020d6b3d95d5e0e8e9cb878ac78d0a6aed7812ffac9b2dc39981a939` | `f3d73858d62b484145653ce55df239620fede86be7d1f22a093d234b054f2762` | `02fbcec209d38eb039371c879982b71eff371052a67ea4bfd8b97a0cb86acf11` |

Each tracked image equals its generator's output at all three revisions. `receipts/rom-digests-head.log` also gives:

- the digests of the two seeded regression images and of the 25, 50 and 125 MHz images;
- the changed word ranges (head vs base: 270 words; head vs reviewed: 251 words).

Every per-configuration image the parent generates changes.

## Documentation

`docs/INTEGRATION.md` "PHC control" now states:

- **the pulse semantics**, including that the addend is signed and a negative trim slows the PHC, and that each step pulse is exactly one phase step;
- **the policy**, as a table with both thresholds;
- **the link-up and locked definitions**;
- **the rate envelope**: the bound, its integer expression, the rule that consumers derive their envelope from the same expression, and that the held trim is inside it;
- **what the verdict and `pub_offset_o` mean while a slew is in progress** (R259-1 suggestion 2): bit 3 rises on every consumed pair, so a slew of at most 100 us may be outstanding, and `pub_offset_o` holds the low 32 bits, wrapping beyond about 2.147 s, where the pair always steps.

It also gains a checklist line. `SOURCE_EVIDENCE.md` gains one row and `TEST_DEVELOPER.md` two bullets. `docs/MANAGER.md`'s "931 words" belongs to the dated 2026-08-27 synthesis record and is left as it is.

## Tests (engine suite, `make -C tb/verilator/engine`)

The suite now has 1207 checks on the shipping image and on both seeded images (1137 at the reviewed head). The per-pair helper grades each #68 pair on:

- the verdict before the pair;
- the published offset;
- the exact step-pulse and addend-pulse counts;
- the addend against an exact-integer mirror of the documented rule, and that it is inside the envelope;
- for a step: its value `-offset`, that it precedes its addend, and that its data holds.

Whether a pair is a link-up is scripted by the phase, never read from the DUT.

| Required case | Phase |
|---|---|
| link-up: 15 us slews, 25 us steps | 13: after a receipt timeout each, +-15 us slew and +-25 us step once; boundary +-20 us slews, +-(20 us + 1 ns) steps. Also 21 (after the re-adoption that follows mastership, +25 us steps), 21 (after asCapable falls and returns, -25 us steps) and 28b (after a warm reset, +25 us steps) |
| locked: 90 us slews, 110 us steps | 13b: +-90 us slew, +-110 us step once; boundary +-100 us slews, +-(100 us + 1 ns) steps |
| GM change: 50 us slews, 5 ms steps | 18c: identity change (verdict cleared, servo locked), then +50 us slews with no step; second change, then -5 ms steps once |
| a long slew never exceeds +-200 ppm | 15b: the +140 ppm closed-loop master of phase 15 jumps +90 us, then -90 us, while locked. For 48 and 40 pairs: every pair locked, asCapable held, more than 4 Pdelay exchanges, no step, every addend on the mirror. The trim rides exactly +1677722 and then -1677722 for several pairs, never beyond, and the loop settles back to lock |
| consumer-envelope assertion | 34: every addend pulse of the whole run, all phases, lies inside the derived envelope, and some sit exactly on it |

Existing checks return to the base's re-base expectations where their offsets are now over the threshold:

- phase 10, the link-up about 1 ms off;
- phases 11 and 11c to 11e, locked pairs about 2 ms off.

Phase 19 adds "becoming grandmaster clears sync-ok" (R259-1 suggestion 1).

**Each test fails when its rule is removed.** The 12 #68 mutants below are in the suite's own mutation arm, which catches all 26 of its mutants. The matrix comes from `scripts/policy_mutation_evidence.py`, which uses the same harness, build flags and image arguments. Each cell is the number of that test's checks that failed:

| run | T1 15/25 us | T1 20 us edge | T1 after asCapable | T1 after become | T1 after warm reset | T2 90/110 us | T2 100 us edge | T3 GM 50 us / 5 ms | T4 long slew | T5 envelope | become clears sync-ok |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clean sources | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| every pair uses the locked threshold | 8 | 8 | 2 | 2 | 3 | 2 | 0 | 0 | 0 | 0 | 0 |
| every pair uses the link-up threshold | 0 | 0 | 1 | 1 | 4 | 7 | 6 | 6 | 7 | 1 | 0 |
| exactly the threshold steps | 1 | 7 | 0 | 0 | 0 | 3 | 4 | 0 | 0 | 0 | 0 |
| the step arm is unreachable | 9 | 8 | 2 | 2 | 4 | 5 | 4 | 4 | 7 | 0 | 0 |
| a grandmaster change unlocks the servo | 0 | 0 | 1 | 1 | 3 | 0 | 0 | 5 | 0 | 0 | 0 |
| a receipt timeout keeps the lock | 8 | 8 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| becoming grandmaster keeps the lock | 0 | 0 | 1 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| asCapable's rise keeps the lock | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| becoming grandmaster keeps sync-ok | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| the whole trim is not clamped | 0 | 0 | 0 | 0 | 2 | 4 | 4 | 2 | 8 | 2 | 0 |
| the trim clamp is one unit wider than the envelope | 0 | 0 | 0 | 0 | 2 | 4 | 4 | 2 | 9 | 2 | 0 |
| the integrator is not clamped | 0 | 0 | 1 | 1 | 2 | 0 | 2 | 2 | 2 | 0 | 0 |
| base generator `c1b6174` (20 us on every pair, no whole-trim clamp) | 0 | 0 | 1 | 1 | 4 | 7 | 6 | 6 | 7 | 1 | 0 |
| reviewed generator `77c34e9` (first sync over 1 s) | 11 | 10 | 3 | 2 | 4 | 9 | 8 | 6 | 7 | 2 | 0 |

Notes on the matrix:

- **"a grandmaster change unlocks the servo" is word-neutral.** BTCA fills its gap, and one more word is a packing refusal, not a mutant. So the unlock takes the slot of the grandmaster change's Sync-cadence disarm. For a plane that is already a slave (phase 18c's), that disarm does nothing.
- **Why the base generator passes T1:** its 20 us rule on every pair coincides with the link-up rule.
- **The asCapable-return case is covered twice.** The rise write and the receipt-timeout write each re-arm the link-up there. Each alone is caught elsewhere: the rise by 28b, the timeout by 13.

**Harness robustness.** The pre-existing RTL mutant "byte face advances without ready" stops every pair being consumed. The new phases then read an empty addend record, which crashed the harness, and a crash is not a catch. Every such read now goes through `last_adj()` or `steered_as_mirror()`, and that mutant is caught with 262 failed checks.

## Parent consumer (kebag-logic/milan-fpga, not changed)

Setup:

- A private disposable clone of the parent at live dev `574c29fa111c74e5e5ed63e4670aff1f492e28e2`.
- The `gptp-processor` gitlink staged at this head.
- verilog-axis at its pin `48ff7a7e`, and protocol-processor at `424c688f` for the builder.

Every command below is the parent's own; the scratch clone has since been deleted.

| Parent check | base `c1b6174` | reviewed `77c34e9` | this head |
|---|---|---|---|
| `make -C tb/verilator/gptp_shadow` (default target: run, then its mutation arm) | 309/309 | 307/309: "closed loop locked"; "every measured result reconstructs its own launch" (19 wrong) | **309/309; mutation arm PASS (9 controls caught, 0 failures)** |
| `make -C tb/verilator/gptp_plane` | 29/29 | 24/29 (five phase-4 checks) | **29/29** |
| `python3 sw/builder/test_builder.py` | not run here | PASS per the manager's validation | **ALL GATES PASS EXCEPT 1 NOT RUN**. The arm not run, gate 11, needs a hardware build tree not on this host |

**No parent check fails at this head.** Each failure the manager and the reviews reported, explained:

- **`gptp_shadow` "closed loop locked"** and all five `gptp_plane` phase-4 failures. Phase 4 jumps the master 1 ms while synchronized (shadow) or starts 1 ms off (plane). Under the reviewed rule that slewed. Now 1 ms is over the locked 100 us (and the link-up 20 us), so it re-bases, as it did under the base's 20 us rule, and the suites pass unchanged.
  - **For #387:** the phase no longer tells the old and new thresholds apart. An adoption lane may want a 20 to 100 us case.
- **`gptp_shadow` "every measured result reconstructs its own launch" (19 wrong): gone.** The reviews measured those 19 results with an in-envelope addend of 1,442,253: the integrator the slewed 1 ms jump had railed.
  - This bench runs an 8 ns counter but declares 2 MHz, so such an addend is about 1% of a tick and misses the bench's +-1 ns law by 4 to 5 ns.
  - At this head the jump steps, the integrator never rails, and the law holds.
  - **For #387, measured:** the probe `probe-locked-slew-plus90us-continue.patch` inserts a locked 90 us slew into phase 4 and lets the suite continue. The trim rides exactly 1677722, the envelope, with zero PHC-history refusals and asCapable held, and the bench's law then flags 1 result (308/309).
  - That is the bench's clock shape, not an out-of-envelope rate. In the product the same term is at most 0.09 ns (`GPTP_PLANE.md:132`).
  - If #387 adds a slew case to this bench, the law's tolerance needs re-deriving for that shape.

**The reviews' wedge, re-run.** These are the first review's own probe patches, plus two new ones, in the parent bench with the real `KL_gptp_txret`. "phcl" is the PHC-history loss count and "lost" the lost-result count, both over the whole run:

| Probe | Pairs | Max \|addend\| (envelope 1677722) | Flags other than 13 | phcl | lost |
|---|---|---|---|---|---|
| synchronized +10 ms jump (steps) | 120 | 13512 | 0 | 0 | 0 |
| first sync 900 ms off after a lapse (link-up, steps) | 120 | 13552 | 0 | 0 | 0 |
| locked +90 us jump (slews on the clamp) | 120 | 1677722 | 0 | 0 | 0 |
| locked -90 us jump (slews on the clamp) | 120 | 1677722 | 0 | 0 | 0 |
| same +90 us probe at the reviewed head | 120 | 2684363 | 0 | 3 | 3 |

## Verification

**Root gate.** `make` (contract, tb, lint, docs) with Verilator 5.050 exits 0 at the head. Wrapper sha256 `905795b9...e92f`, `verilator_bin` `44898b22...bfdd`; the system default is 5.052 and was not used.

- A single invocation in this lane is time-limited, so the gate ran as its recipes in the Makefile's order, one invocation each.
- The ignored build products were removed first, so every suite built from scratch.
- The engine mutation arm ran as four disjoint slices of its own list, each with the unmutated control.
- Results:
  - contract PASS; ucpu 768/768; parser 268/268;
  - engine 1207/1207 x3, with 26/26 mutants caught and the control passing in all four slices;
  - gaskets 81/81 with 4/4 mutants; tsngen 288/288 with 3/3 mutants;
  - bench tag test PASS; lint PASS; docs, diagrams and selftests PASS.

**Tree.** The working tree was clean before and after: all four regenerated tracked images equal the committed ones.

## Not in this change

- **No push, no parent change, no parent pin.** The parent adoption (kebag-logic/milan-fpga#387) and its regenerated per-configuration ROM digests are a separate lane.
- **No hardware and no synthesis.** The product clock is analysed, not simulated: the envelope and the gains both derive from `--clk-hz`, and the parent bench runs at 2 MHz.
- **The neighbour-rate-ratio observation after a forward step** (in the previous body) is pre-existing and unchanged. Steps now happen above 20 us at link-up and 100 us locked.
- **The superseded DECISION comment on #68** described the saturated input and the 320 ppm trim. Both are gone.

Closes #68
