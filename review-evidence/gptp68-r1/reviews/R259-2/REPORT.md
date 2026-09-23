[R259] NEGATIVE - exact head cbccf226068c107fb30764891c98b8d70c54d775

Round R259-2 is the external independent review of Mister-M-alt/FPGA-gPTP issue #68 / PR #74. It is the correction round for R258-1 and R259-1.

| Item | Value |
|---|---|
| Head reviewed | `cbccf226068c107fb30764891c98b8d70c54d775`, tree `e8b9fa23fe5e1d5e3bd3ab1dd3c09196760a5063`. Both are verified, the review clone is clean, and both commits since base have one-line messages with no trailers (`receipts/identity.log`) |
| Parent of head | `77c34e904eba2446755d13e1bf4763d1652c3ca7`, the head R258-1 and R259-1 reviewed |
| Source base | `c1b617435824929a790739ea8585c3fe1a328cc0`, which is the parent's current `gptp-processor` gitlink |
| Parent consumer used | kebag-logic/milan-fpga `ede8d48ecd7c7f589a14b957951f040d92c99c70`, the manager's r2 validation base. Live dev is now `07d85dac` (see pending duties) |
| Simulator | Verilator 5.050 through the pinned wrapper (sha256 `905795b9...e92f`, `verilator_bin` `44898b22...bfdd`), with build jobs capped at 8 by `scripts/bin/verilator`. The system 5.052 was not used for any published receipt |
| Review clone after all probes | Exact head bytes, modes and index. It has no untracked, ignored or hidden-flag entries, and 0 gitlinks, the same as base (`receipts/clone-integrity.log`) |

## Reconstruction

I read the authorities in this order, from public state only:

1. Parent `AGENTS.md` and `CONTRIBUTING.md` at `ede8d48`. The donor repository has neither file.
2. The donor `README.md`, `docs/README.md` and `docs/MANAGER.md`.
3. The #68 issue body (frozen scope) and the public scope decisions:
   - the manager's assignment 5789747601;
   - the owner decision 5794731372, which supersedes the 2026-09-09 step rule;
   - the correction assignment 5794740482;
   - the author's TAKEN, DECISION (superseded) and REVIEW READY comments.
4. On the parent side:
   - the #387 decision 5606198212 (parts a and b);
   - `REQUIREMENTS.md` REQ-PTP-01/05/08/09;
   - `KL_gptp_txret.sv`, whose `PHC_ADJ_MAX_C` is at `:120`, `:296-305` and `:429-436`;
   - `docs/design/GPTP_PLANE.md:127-143`.
5. On the donor side, the interface authorities: `docs/INTEGRATION.md`, `hdl/top/KL_gptp_engine.sv` and `hdl/ucpu/KL_gptp_ucpu.sv`.
6. `git diff c1b61743..cbccf226`, 10 files, and its two commits.
7. The PR #74 body and the manager's PR comments.
8. The public evidence at kebag-logic/milan-fpga `9c9922c4` under `review-evidence/gptp68-r1`: `correction-a199/`, `author-a188/` and `manager-r1/`. I also read `manager-r2/` at `a45e04a1`, which is linked from the manager's r2 comment.

I read the R258-1 and R259-1 reports only after my verdict, F1 and ledger were written. I did not read the concurrent R258-2 round.

## Verdict

**NEGATIVE, because one MAJOR finding (F1) is open.** Its lenses are Conformance, Tests and Docs.

Everything this correction round was assigned is done, and I verified it independently:

- The whole written trim (P plus I) is clamped to exactly the parent's `PHC_ADJ_MAX_C` at every clock tried.
- The two thresholds are exact: a link-up pair steps above 20 us and a locked pair steps above 100 us.
- A grandmaster change without a Sync gap stays locked.
- Each step is one `phc_step_we_o` pulse.
- The ROM changes are the ones claimed.
- The engine tests and the author's 26 mutants hold, and all 9 of my own mutants are caught.
- The parent consumer suites are green at this head.
- The earlier BLOCKER, the out-of-envelope wedge, is gone in the real consumer.

What is open is the link-up definition, the reading the PR body flags for review. The plane re-arms the 20 us link-up after any Sync receipt timeout and after a return from mastership. So after a Sync gap, including the usual grandmaster failover, it steps offsets of 20 to 100 us that the owner decision slews.

## Findings

```text
[R259] MAJOR Conformance, Tests, Docs - hdl/ucode/gen_gptp_ucode.py:1843 and :1618 (with :19-20); docs/INTEGRATION.md:206-210 (under :191); tb/verilator/engine/sim_main.cpp:2984-3016 and :3389-3405; tb/verilator/engine/mutants.py:211-219 - F1: the link-up is re-armed by a Sync receipt timeout and by a return from mastership, which the owner decision does not name
```

**Requirement and evidence.**

The owner decision (issue 68 comment 5794731372) reads: "steps the PHC at link-up (the first synchronization after asCapable) when the offset exceeds 20 us; once locked, including after a grandmaster change, it slews offsets up to 100 us and steps above 100 us".

- That parenthesis is the only public definition of link-up. The correction assignment (5794740482) restates the thresholds only.
- The implementation writes `S_LOCK = 0` at three points, and the tests and `INTEGRATION.md` state all three as #68 policy:
  - the asCapable rise (`:1815`), which the decision names;
  - the Sync receipt timeout (SRTO, `:1843`);
  - becoming grandmaster (BECOME, `:1618`).
- R258-1 and R259-1 accepted "the pair that raises the sync verdict" as the reading of the same phrase, but under the superseded rule, where a grandmaster change also counted as first. The owner then made a grandmaster change explicitly locked. The decision's two clauses now disagree for any grandmaster change that follows a receipt timeout.
- The PR body flags this reading and offers the narrowing. AGENTS.md section 2 requires such a conflict to be decided in public, not settled in the implementation, and no decision has been recorded.

**Measured** (`receipts/literal-lock-probe.log`, using patch `scripts/probe-literal-lock.patch` in a disposable copy of the harness). This is a phase inserted after 18c, graded against the owner text. With asCapable held throughout, a Sync gap longer than the 375 ms receipt timeout is followed by one of three pairs:

- the same grandmaster at +50 us;
- a new grandmaster, the failover shape, at -50 us;
- the same grandmaster at +90 us.

At head, each produces one step pulse. The owner text says each is locked and slews.

With only the SRTO leg's `S_LOCK` write removed, all three slew, and the probe's own checks pass. The unmodified suite then fails exactly 18 checks, all in phase 13, whose link-up probes are built on the receipt timeout. The author's mutant "a receipt timeout keeps the lock" shows the same result (`receipts/mutants-author-05-25.log`).

**Impact.**

- Every step is a counted media event in the parent: tu, one mr toggle and one MEDIA_RESET (#387 decision part b).
- After any Sync gap of 375 ms or more with asCapable held, the plane re-bases offsets of 20 to 100 us that the decided policy slews in at most 0.5 s.
- A failover in which the old grandmaster falls silent passes through such a gap. Upstream selection of a new grandmaster waits on receipt timeouts at least as long as this plane's own 375 ms. So "including after a grandmaster change" holds only for a change without a gap, such as preemption by a better grandmaster that is already running.
- The return-from-mastership re-arm has the same effect when the plane had been locked before it became grandmaster. Whether such a plane is still "locked" is a question the decision does not answer.

**Required change.** The link-up set the plane implements must equal one that a public owner decision on #68 names. There are two routes:

- **(a)** The owner records that a Sync receipt timeout and a return from mastership each re-arm the link-up. `docs/INTEGRATION.md:191-216` then cites that record, and the code and tests stand.
- **(b)** The SRTO write is removed, and the BECOME write too unless the ruling keeps it. Then:
  - phases 13 and 21 create link-ups only through an asCapable rise or a reset;
  - a test shows that a pair after a Sync gap slews up to 100 us, both with and without a grandmaster change;
  - the generator docstring (`:15-27`, `:1839-1840`), `INTEGRATION.md:206-216` and `mutants.py:211-219` are made to agree.

**Verification.**

- For (a): the public ruling, and the `INTEGRATION.md` link to it.
- For (b):
  - the engine suite passes on all three images;
  - its mutation arm is fully caught;
  - `scripts/literal_lock_probe.sh` reports 0 step pulses in all three cases on the fixed head's own generator.

**Lens attribution.** This finding is not filed under RTL or Robustness:

- The re-arm paths are well-formed microcode. The emulator executes the shipped SRTO and BECOME words and each writes only the lock and flag cells (`receipts/servo-rom-emulator-head.log`).
- Either policy is safe: bounded, inside the envelope, with no wedge (see the parent probes below).
- The defect is which policy these paths implement.

```text
[R259] SUGGESTION Docs - hdl/ucode/gen_gptp_ucode.py:713-715 - S1: the e_sat docstring still slightly misstates its callers
```

The text reads "the trim is the PI output for a slewed offset, which never exceeds STEP_LOCKED_NS_C". Two details are off:

- The step arm also enters the same clamp, carrying the bare integrator.
- It is the offset that is bounded by 100 us, not the trim.

The code is correct, as the emulator shows, so this does not affect coverage. It follows up R258-1 S1, which the author did address by stating the domain.

## Focus items verified (evidence per lens)

```text
[R259] PASS RTL - hdl/ucode/gen_gptp_ucode.py:707-725,798-852 executed as ROM words; hdl/ucpu/KL_gptp_ucpu.sv:185-236,597-675; hdl/top/KL_gptp_engine.sv:724-731,767-905 - operand widths, DIVU/MULS exactness, clamp, pulse shape, scratch cell, ROM parity and packing
```

- **Threshold test.** The threshold T is `S_LOCK + 20000`. The test `(offset + T) / (2T + 1) == 0` runs as a 64/32 unsigned DIVU with a register divisor, followed by a 64-bit zero compare (`KL_gptp_ucpu.sv:193,202,619-636`). That is exactly `|offset| <= T`, including 64-bit extremes and wrap.
- **MULS.** A slewed offset is at most 100 us, so the signed 32x32 MULS (`:226`) is exact at every clock the generator accepts. Its own assertion `2*ilim+1 < 2^24` bounds the clock above about 400 kHz. At that bound the product reaches at most 100000 x 21474, which is below 2^31.
- **`e_sat`.** Its two DIVU immediates are `2*ilim+1`, which the ROM carries at every clock tried.
- **Emulator.** `receipts/servo-rom-emulator-head.log` executes the shipped SERVO words at 1, 2, 25, 50, 62.5, 100, 125 and 156.25 MHz on a µCPU model written from the RTL. It covers 38,214 cases per clock across both lock states, with offsets from 0 to the 64-bit extremes and integrators at and inside both rails. The results match an independent reference of the decided policy:
  - a step happens exactly when `|offset| > T`, and it writes `-offset`;
  - the step's addend is the clamped bare integrator;
  - a slew writes the v5 PI with its integrator clamped and the whole trim clamped;
  - every written addend lies inside the parent's `PHC_ADJ_MAX_C`, and the largest equals it exactly;
  - the clamp is load-bearing: about 8,500 slews per clock had P plus I beyond the envelope before it.
- **Envelope arithmetic.** `ppm_addend(200, clk)` equals the parent's SystemVerilog expression at 411 clocks, including the three exact half-unit ties.
- **PHC writes.** SERVO is the only PHC-region writer. The engine's step and addend enables are one-cycle pulses, their data holds between pulses, and reset clears both (`KL_gptp_engine.sv:781-784,796-797,897-905`).
- **Scratch cell.** Cell 43 (`S_LOCK`) is plain scratch. It does not collide with the engine's reset-backed or mirrored cells 18, 25, 37, 38 and 41 (`:724-731,834-855`).
- **ROM images** (`receipts/rom-parity.log`, `receipts/leg-sizes.log`):
  - all four tracked images regenerate byte-identically at base, reviewed and head, with the digests the PR body gives;
  - real words go 989, then 993, then 996 of 1024;
  - SERVO goes from 52 to 51 words, PDPAIR from 59 to 61, SRTO from 5 to 6 and BECOME from 21 to 22;
  - the eight relocations are exactly the PR's list.
- **Lint.** Engine and bench lint pass (`receipts/focused-gates-head.log`).

```text
[R259] PASS Robustness - gen_gptp_ucode.py:336-342,752-761,1785-1820,1838-1846; KL_gptp_engine.sv:775; engine phases 21, 28b, 15b; reviewer mutant R1; emulator extremes; parent probes - reset, ordering, repeats, timeouts, extremes, held trim
```

- **The S_LOCK written-before-read invariant holds.**
  - The only reader is SERVO, which is reached only through FOLLOWUP's asCapable gate (`:760-761`).
  - Every reset clears `pub_flags_r` (`KL_gptp_engine.sv:775`).
  - asCapable has one setter, and it writes `S_LOCK = 0` exactly on a rise (`:1809-1815`).
  - A repeated verdict leaves the lock alone. Reviewer mutant R1, "a repeat verdict also unlocks", is caught by 11 checks.
  - A warm reset with a retained lock gives a link-up (phase 28b).
- **Extremes.** 64-bit offsets, both rails and every accepted clock are clean in the emulator.
- **Held trim.** A trim held after consumption stops is inside the envelope, because every written trim is.
- **Real consumer, 120 pairs each** (`receipts/parent-probe-*`):
  - R258-1's own wedge probes (a synchronized 10 ms jump, and a first synchronization 900 ms off) now step once and lock, with flags 13 on every pair and zero PHC-history refusals or lost results.
  - A locked ±90 us jump slews on exactly ±1,677,722, the envelope, with zero refusals and zero lost results, and then settles.
  - The same +90 us probe at the reviewed head reaches 2,684,363, with 3 refusals and 3 lost results. That control shows the probe discriminates.

**Clean inside the lenses F1 leaves UNCLEAN.** These results stand, but they do not clear the lens while F1 is open.

- **Conformance.**
  - Both thresholds are strictly "exceeds", with exact boundaries, and each step is one pulse.
  - The grandmaster change without a gap stays locked (phase 18c; mutant "a grandmaster change unlocks" caught).
  - The whole-trim clamp is the parent's expression, not a copied constant.
- **Tests.**
  - The engine suite passes 1207/1207 on the shipping image and both seeded images (`receipts/engine-suite-head.full.log`).
  - The suite's own arm catches 26/26 with the control passing (`receipts/mutants-author-*.log`).
  - My mutants R1 to R9 are 9/9 caught (`receipts/mutants-reviewer.log`). They cover: a repeat verdict unlocking, a logical-shift bound selection, the trim clamp one unit narrow, the integrator clamp one unit wide, the locked threshold and the positive boundary each 1 ns wide, a zero addend on step, the threshold reading the wrong cell, and a step of +offset.
  - The mirror takes its link-up flag from the phase's script, never from the DUT.
  - Phase 34 grades every addend pulse of the run against a separately written envelope.
  - uCPU passes 768/768 and tsngen 288/288, with 3/3 mutants, on the regenerated images (`receipts/focused-gates-head.log`).
- **Docs.**
  - The pulse semantics, the thresholds, the locked and grandmaster-change text, the rate envelope and its integer expression, the held trim, and "Publication during a slew" all match the RTL and the microcode (`docs/INTEGRATION.md:148-275`).
  - The checklist lines (`:325-326`) and the `SOURCE_EVIDENCE.md` and `TEST_DEVELOPER.md` rows are accurate.
  - The docs and diagram checks pass, and no added line carries U+2014.

**Parent impact** (`receipts/parent-*`). Every fetched parent file is verified against its blob id at `ede8d48`, and `gptp-processor` holds the exact donor tree.

- `gptp_shadow` `run` passes 309/309 at head, from a fresh build.
- `gptp_plane` passes 29/29 at head (exit 0), against 24/29 at the reviewed head (exit 2).
- The manager's r2 receipts add the parent `gptp_shadow` default target (309/309 plus its mutation arm) and the idiom, xvlog, source-list and builder gates. All pass, except builder gate 11, which is NOT RUN because it needs a hardware build tree.

No parent failure remains at this head.

**Hosted evidence.** The donor repository defines no workflows. At the exact head there are 0 check runs, 0 statuses and 0 workflow runs (`receipts/hosted-evidence.log`). Nothing hosted executed or was skipped.

## Prior public review findings at this head

| Finding | Status at this head | Evidence |
|---|---|---|
| R258-1 F1 BLOCKER (Conformance, RTL, Robustness, Tests, Docs): the slew held about 320 ppm beyond the 200 ppm envelope and wedged the plane | **RESOLVED** | The whole trim is clamped to the envelope at every clock (emulator). Slews are at most 100 us. `INTEGRATION.md:230-256` states the bound and the held trim. Engine phase 15b drives a slew longer than allowedLostResponses + 1 Pdelay intervals on the rail, with asCapable held and more than 4 exchanges completing. The trim-clamp mutants are caught. The prior 10 ms and 900 ms wedge probes and the ±90 us rail probes are clean in the parent's real consumer, with the reviewed-head control failing |
| R259-1 F1 BLOCKER (same five lenses): the same defect, measured as probe D | **RESOLVED** | As above. The 900 ms first synchronization, the probe D shape, now steps and locks with 0 refusals. The mechanism's test fails on the reviewed head (the author's matrix row, and my parent control). The superseded DECISION's "never exceeds" claim is withdrawn in the PR body |
| R258-1 F2 MAJOR (Conformance, Tests), retained by R259-1: the parent suites were not green at the pin | **RESOLVED** | `gptp_shadow` passes 309/309 (my fresh build, and the manager's r2 with its arm). `gptp_plane` passes 29/29. Under the decided policy a 1 ms offset steps, so the parent's phase-4 expectations hold unchanged and no parent change is needed. The reconstruction-law misses are gone because that jump steps. The law's behaviour for in-envelope rail slews in that bench's 8 ns / 2 MHz shape is a parent-bench scoping item for #387 (see pending duties), not a product term (`GPTP_PLANE.md:131-132`: at most 0.09 ns) |
| R258-1 S1 SUGGESTION (RTL, Docs), retained by R259-1: the `e_sat` docstring claimed any signed value | **ADDRESSED** | The docstring now states the exact domain. A residual wording point is S1 above, a SUGGESTION |
| R259-1 suggestion (Tests): "becoming grandmaster clears the verdict" had no check | **RESOLVED** | Phase 19 checks it (`sim_main.cpp:3366-3376`). The author's mutant "becoming grandmaster keeps sync-ok" is caught |
| R259-1 suggestion (Docs): say what bit 3 and `pub_offset_o` mean during a slew | **RESOLVED** | `INTEGRATION.md:258-274` is accurate against `KL_gptp_engine.sv:862` and the step rule |
| Manager r1 parent failures: "closed loop locked" and "every measured result reconstructs its own launch" | **GONE** | Parent `gptp_shadow` passes 309/309 at head |

No prior finding is retained open. F1 above is new at this head, because the owner's re-decision introduced the locked grandmaster-change clause it conflicts with.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Owner decision 5794731372, assignments 5789747601 and 5794740482, #68 body, #387 decision 5606198212, REQ-PTP-01/05/08/09. Parent `KL_gptp_txret.sv:120,296-305,429-436` and `GPTP_PLANE.md:127-143`. `gen_gptp_ucode.py:15-27,334-342,402-445,707-852,1500-1631,1785-1846`. `receipts/servo-rom-emulator-head.log`, `receipts/literal-lock-probe.log`, `receipts/parent-*` | R259-2 | `cbccf226068c107fb30764891c98b8d70c54d775` |
| RTL | CLEAN | `KL_gptp_ucpu.sv:185-236,597-675`; `KL_gptp_engine.sv:724-731,767-905`; SERVO, SRTO and BECOME words executed (`receipts/servo-rom-emulator-head.log`); `receipts/rom-parity.log`; `receipts/leg-sizes.log`; lint in `receipts/focused-gates-head.log` | R259-2 | `cbccf226068c107fb30764891c98b8d70c54d775` |
| Robustness | CLEAN | S_LOCK invariant (`gen_gptp_ucode.py:336-342,752-761,1785-1820`; `KL_gptp_engine.sv:775`); engine phases 21, 28b and 15b; reviewer mutant R1; emulator 64-bit and rail extremes; parent wedge and rail probes with the reviewed-head control (`receipts/parent-probe-*`) | R259-2 | `cbccf226068c107fb30764891c98b8d70c54d775` |
| Tests | UNCLEAN (F1) | `sim_main.cpp:458-516,622-700,845-883,2984-3050,3119-3223,3340-3376,3389-3418,3790-3809,4527-4534`; `mutants.py:180-246`; `receipts/engine-suite-head.full.log`; `receipts/mutants-author-00-04.log`; `receipts/mutants-author-05-25.log`; `receipts/mutants-reviewer.log`; `receipts/focused-gates-head.log`; `receipts/parent-gptp_plane-ede8d48-*.log`; `receipts/parent-gptp_shadow-run-ede8d48-cbccf22.log` | R259-2 | `cbccf226068c107fb30764891c98b8d70c54d775` |
| Docs | UNCLEAN (F1) | `docs/INTEGRATION.md:148-275,314-329`; `docs/SOURCE_EVIDENCE.md:29-30`; `docs/TEST_DEVELOPER.md:99-100`; generator docstrings `:15-27,707-716,1786-1790,1839-1840`; PR #74 body; docs and diagram checks in `receipts/focused-gates-head.log` | R259-2 | `cbccf226068c107fb30764891c98b8d70c54d775` |

## Limits

- No hardware, no synthesis, and no physical calibration (NOT RUN). Field skips are not hardware proof.
- **Parent suites.** They ran from minimal trees assembled from blob-verified parent files at `ede8d48`, with the donor tree at the `gptp-processor` path. That is not a registered gitlink, so the parent's own pin-proof machinery was not exercised.
  - verilog-axis `axis_fifo.v` came from the parent's pin `48ff7a7e`.
  - Only the `run` targets were executed.
  - Not run by this review: the parent mutation arms, `milan_dp` (gPTP ON), the builder, and the idiom, xvlog and source-list gates. Those are the manager's receipts where they exist.
  - Live dev `07d85dac` was not used.
- **Bench shape.** The parent benches run 2 MHz servo gains on an 8 ns counter. The product-clock claims rest on the shared integer derivation (emulator, eight clocks) and on `GPTP_PLANE.md`, not on a product-clock simulation.
- **Probe phase.** The owner-text probe ends the run after its own phase. Its script exits 0 by design; the verdict is the probe lines in the receipt.
- **Author scripts.** The author's `rom_differential.py`, slew model and policy matrix were read, not re-executed. The independent emulator and mutation runs stand in for them.
- **Donor suites not re-run:** parser, gaskets and the bench tag test. The manager's full donor `make -j8` at this head (exit 0) covers them.
- **Superseded run.** An early run of the mutation driver was launched outside `env.sh` and used the host's default Verilator 5.052. It was discarded. All three slices were re-run under 5.050, and they are the published receipts. Every published receipt was produced by the published scripts, in their final form.
- **Path placeholders.** Host paths in the receipts are replaced by `$PACKET`, `$CLONE`, `$PIN_BIN`, `$PINNED_ROOT`, `$HOME` and `$DATA` (`scripts/sanitize_receipts.sh`). The receipts are otherwise raw.

## Pending manager duties

- **F1.** Obtain and record the owner's ruling on the link-up set, or route the narrowing to the author. Merge still needs two positive reviews and every lens covered clean at the merge head.
- **Live dev has moved** to `07d85dac`: 13 commits past `ede8d48`, with PR #526 changing `tb/verilator/gptp_shadow/Makefile` and `mutants.py` and adding pinned-input proofs. The merge-turn candidate (source base `c1b61743`, live dev at merge time) must re-run the parent `gptp_shadow` default target and its mutation arm with the gitlink staged at the candidate head.
- **Two parent gates are missing from the manager's r2 receipts:**
  - `gptp_plane` (this review: 29/29 at `ede8d48`);
  - the `milan_dp` gPTP-ON datapath leg, which neither the author nor this review ran.
- **The manager's r2 `gptp_shadow` run reused an existing build**, as its log shows ("Nothing to be done"). The ROM, which carries the whole #68 change, was regenerated at run time. This review's fresh build confirms 309/309.
- **For #387:**
  - re-record the per-configuration ROM digests at the pin bump;
  - the parent phase-4 cases no longer distinguish 20 us from 100 us;
  - the `gptp_shadow` reconstruction law needs re-deriving before that bench adds a locked slew on the rail. The author measured 1 flagged result with 0 refusals; the product term is at most 0.09 ns.
- **Hosted and act acceptance.** The donor has no hosted workflows.
- **Builder gate 11** and physical calibration remain NOT RUN.

## Reproduction

Every file in `receipts/` and `scripts/` is listed in `MANIFEST.sha256`.

- **Settings.** `scripts/env.sh` locates the packet relative to itself. `CLONE`, the exact-head clone, and `PIN_BIN`, the directory holding the pinned Verilator wrapper, may be set in the environment. `scripts/bin/verilator` caps `-j 0` at 8.
- **Donor:**
  - `sh scripts/identity.sh`
  - `sh scripts/rom_parity.sh`
  - `sh scripts/leg_sizes.sh`
  - `sh scripts/servo_rom_emulator.sh`
  - `sh scripts/engine_suite.sh`
  - `sh scripts/focused_gates.sh`
  - `sh scripts/mutation_arm.sh author:0-4 a1`
  - `sh scripts/mutation_arm.sh author:5-25 a2`
  - `sh scripts/mutation_arm.sh reviewer r`
  - `sh scripts/literal_lock_probe.sh`
- **Parent:**
  - `sh scripts/parent_gptp_plane.sh <parent-rev> <donor-rev>`
  - `sh scripts/parent_shadow_probe.sh <parent-rev> <donor-rev> [patch]`. The patches are the public R258-1 and author probes, copied into `scripts/`.
- **Integrity:** `sh scripts/clone_integrity.sh`

R259-2 FINISHED
