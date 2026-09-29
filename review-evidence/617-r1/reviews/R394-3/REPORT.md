[R394] NEGATIVE - exact head ddb0774779d10a9b0bd90a4822f4e5df9fdedb1b

# R394-3 internal cleared-context review: issue #617 / PR #618, round 3

- **Head:** `ddb0774779d10a9b0bd90a4822f4e5df9fdedb1b`, tree `8ed377b8eae84e92b00387b7ce377e6aaa763cd1`. Ten commits on dev `ce550952e47fbd92367f0d9b099345100f7f4215`; round 3 is `377d1ac3..ddb07747` (four commits).
- **Reconstructed from:**
  - AGENTS.md, CONTRIBUTING.md and docs/README.md;
  - the #617 body, the round-3 rulings (issue comment 5879911799), the round-3 TAKEN (5879964310) and REVIEW READY (5881204511) comments, and the review-start comment 5881232746;
  - the PR body at this head;
  - `git diff ce550952..ddb07747` and `377d1ac3..ddb07747`, read file by file;
  - the round-3 author evidence on the `617-review-evidence` branch (commit `04d687c52b`: gate summary, suite tally, NCO area, recorded settle/transient summary);
  - hosted check runs at this head and on the PR's two earlier heads;
  - my own round-2 packet (read-only input);
  - executable evidence I re-ran myself.
- **Other reviewers' reports:** none was read before the verdict, findings and ledger below were written. The other reviewer's round-2 probe *scripts* (not its report) were used as tools, as the assignment directs. Prior public findings are resolved in their own section, which was written after the ledger.
- **Lenses:** all five applied.
- **Verdict:** one MAJOR finding is open under `Tests`, so the verdict is NEGATIVE. `Conformance`, `RTL`, `Robustness` and `Docs` are covered clean at this head. Four suggestions do not affect coverage.

## Summary

The round-3 design work is correct, and I confirmed each ruling with my own runs.

- **Ruling 1, the NCO.** The monotone compare is right, and it is minimal.
  - One tick per period, whatever cycle the trim moves.
  - The count never passes `DIV_C`, so it cannot wrap.
  - A late update is a one-cycle phase step inside the legal period set.
  - At a steady trim the grid is bit for bit unchanged.
  - Check 10 is 410 / 0 at the head and 10 failures with the `377d1ac3` NCO.
  - The `==` mutant is killed in both `nco` and `fine`.
  - LUT 101 -> 106 reproduced, with the datapath's `TRIMW_P = 18`.
- **Ruling 2.** The derived keep-off works. RM5 is killed by `band50`.
- **Ruling 3.** The envelope is right in substance.
  - The settled lock holds far past the ruling's bar: in 150,000-column runs it sits 255-256 cycles off the crossing, spread at most 3 cycles, with no tail slip at ±100 **and ±150** ppm.
  - The new tail rule is a correct law. It moves no committed scenario's tail.
- **Rulings 4 and 5.** The banner is fixed. RM7 and RM8 are killed.

What is open is the suite's own hosted run:

- **F1.** The mutation arm cannot build its datapath legs on the hosted runner.
  - `Verilator shard 1/5`, which owns `capture_coherence`, failed for exactly that reason at this head, and the aggregate `verilator-suites` context is red. It also failed on both earlier heads of this PR.
  - I reproduced the mechanism locally.
  - Nothing in round 3 touches it, and the public record never mentions it.
  - Once it is fixed, the suite's hosted time is projected at about 1,900 s, over its 1,800 s guard (Judgment 6).

## Findings

### F1 - MAJOR - lens: Tests

**Location:**

- `tb/verilator/capture_coherence/Makefile:94,98`: `DP_SRCS := $(shell $(MAKE) -s -C $(DP_DIR) print-srcs ...)` and `DP_VFLAGS := $(shell $(MAKE) -s -C $(DP_DIR) print-dp-vflags)`;
- `tb/verilator/capture_coherence/mutants.py:209-219`: `build()`, which runs `make -s -C <suite> dp-build ...` from inside the suite's own `make` and discards the build output;
- `mutants.py:101-102`: the `dp` and `dp-band` legs.

**Title:** the suite's datapath mutation legs never build on the hosted runner, so hosted `capture_coherence` is red.

**Authority / evidence:**

- AGENTS.md section 7 requires "exact-head `verilator-suites` ... evidence", and section 6 `Tests` requires "Existing regressions remain green". The `dp` and `dp-band` legs are how the arm shows the rulings' datapath mutants killed: the one-pair frame length in `milan_datapath` and `milan_datapath`'s round-1 aligner binding.
- **Hosted, both earlier heads** (`receipts/hosted-prior-shard1.txt`, from the jobs' own logs and `suite-logs-1` artifacts):
  - `5546b976`, job 109040459305: `failing suites: capture_coherence`, "`the unmutated RTL does NOT pass the dp harness (did not compile)`", and the dp mutant "did not compile". Arm 6 / 8.
  - `377d1ac3`, job 109149243991: the same for `dp` and `dp-band`, controls and mutants. Arm 15 / 19, `in-suite failures: 4`.
  - Everything else in both runs passes, including the in-tree junction and datapath legs, so the RTL and the harness are not the cause.
- **Mechanism, reproduced** (`scripts/r394_mf_repro.py`, `receipts/makeflags-dp-build-repro.txt`):
  - `scripts/run_all_suites.sh:390` runs `make -C <suite>`, and the `mutants` recipe starts `python3 mutants.py`, which runs `make -s -C <suite> dp-build`.
  - With `w` in the inherited `MAKEFLAGS`, the nested `$(shell $(MAKE) -s -C ../milan_dp ...)` prints `make[1]: Entering directory ...` into its output. `DP_SRCS` and `DP_VFLAGS` then begin with that text, the Verilator command is malformed, and `build()` returns `None`, which the arm reports as "did not compile".
  - Driving the committed `mutants.build('dp', ...)` with `MAKEFLAGS=w` reproduces "did not compile". Without it, the same build succeeds.
  - The hosted image is `ubuntu-24.04` (job log), which ships GNU make 4.3. The inferred difference is that it passes `w` to a recipe run under `make -C`. The local GNU make 4.4.1 does not (`receipts/makeflags-recipe-local.txt`: recipe `MAKEFLAGS=[]`), which would explain why every local run, the author's and the manager's included, is green.
  - I could not run make 4.3 here, so the version attribution is inference. What is measured:
    - the failure pattern: exactly the legs that use the nested `$(shell $(MAKE))`, on all three heads;
    - the reproduction.

    The required outcome does not depend on the attribution.
- **At this exact head it fails the same way** (`receipts/hosted-checks.txt`):
  - `Verilator shard 1/5`, job 109196809736: `failing suites: capture_coherence`, `in-suite failures: 4`. Its artifact shows the junction leg at 20,832 / 0 and the datapath leg at 332 / 0, but the arm at `27 checks: 23 PASS, 4 FAIL`: the `dp` and `dp-band` controls and their two mutants "did not compile".
  - The aggregate `verilator-suites` context is `failure`. Every other hosted context passed; `Physical gPTP` was skipped.
  - Round 3 kept both legs and left the Makefile lines untouched.
  - The REVIEW READY comment says "Hosted checks have not run on this head" and does not mention the two red hosted runs of the earlier heads. Neither ruling mentions them.
- **Diagnosability.** `build()` captures the make output and prints none of it, so the hosted log says only "did not compile". That is why two rounds of red hosted runs carry no cause.

**Impact:**

- The mandatory hosted `verilator-suites` context cannot go green at any head of this PR. The merge bar is unreachable as the suite stands.
- In the hosted gate, the datapath-level mutants are never shown killed.
- A future recipe or environment failure in any leg would also be undiagnosable from the hosted log.

**Required outcome:**

- The `dp` and `dp-band` legs build and run in the hosted environment. The mechanism is the executor's choice; two examples:
  - the nested `$(shell $(MAKE) ...)` calls cannot inherit a print-directory flag (for example `--no-print-directory`);
  - or `mutants.py` builds with a controlled `MAKEFLAGS`.
- `Verilator shard 1/5` passes at the exact head, with the arm reporting all its legs, dp included.
- The suite's hosted wall time is inside its 1,800 s per-suite guard (`scripts/run_all_suites.sh:243-247`). It is already 1,442 s with the dp items skipped, and projected at about 1,900 s once they run, so a split or sharing (S4) is needed as well (Judgment 6).
- Recommended, not required: `build()` prints the tail of a failed build's output.

**Verification:**

- `receipts/makeflags-dp-build-repro.txt` must build under `MAKEFLAGS=w`.
- The hosted shard 1/5 log at the new head must show `capture_coherence` PASS, its arm tally including the `dp` and `dp-band` controls, and its elapsed time.

## Suggestions (optional; they do not affect coverage)

### S1 - Tests: a binding-level keep-off mutant survives every leg

**Mutant (RM9).** `milan_datapath.sv:5727` binds a literal: `.LOCK_KEEPOFF_CYC_P (128)`. The `MGA_KEEPOFF_CYC_C` declaration stays at 256 (`receipts/rm9.diff`).

**Result.** It survives:

- the datapath leg, 332 / 0;
- its `--band` run, 198 / 0.

It is also invisible to the junction and `band50` legs, which bind the declaration. Its lock phases visibly move: tail tick 40 against 63 cycles at the same placement (`receipts/rm9-dp-*.log`, `receipts/head-dp-band.log`).

**Why it is only a suggestion.** Ruling 2 as worded, "derived ... or a check fails when they differ", is met, and RM5 is killed. What remains is `coherence_wrap.sv:143`'s promise that "the keep-off every sweep grades is the one the datapath ships". That holds only while the instance binds the declaration.

**Suggested fix.** Either of these closes it:

- `mga_keepoff.py` also requires `.LOCK_KEEPOFF_CYC_P (MGA_KEEPOFF_CYC_C)` exactly once;
- or the datapath leg reads the aligner instance's keep-off.

### S2 - Docs/Tests: CRF-settle grades a lock that is still converging

**Where.** `docs/design/TIME_SYNC.md:551`, "Settled lock | ... the lock sits 256 cycles off | MEASURED to +/-100 ppm, CRF-settle", and `sim_main.cpp:692-700`.

**What CRF-settle actually shows.** The aligner's integrator converges with a time constant of about 13,000 frames, so in the committed 30,000-column runs the tail from column 15,000 is still converging:

- at the tail's start the close is 26-104 cycles from the crossing on the negative side and 35-106 cycles on the positive side;
- it then moves 109-159 cycles through the tail (`receipts/sum-head-junction.txt`);
- `[V] the CRF lock held its phase` passes because its bound is a quarter frame, 260 cycles.

The author's recorded 60,000-column runs converge further but not fully: spreads of 41-84 cycles.

**What a settled lock shows.** 150,000-column runs at ±100 and ±150 ppm reach it. The lock sits at 255-256 cycles, spread at most 3, with no tail slip (`receipts/probe-settle-*-150k.log`). So the claim is true, but CRF-settle is not the measurement that shows it.

**Suggested fix.** Either:

- state the convergence (about 0.3 s, and that CRF-settle grades the approach, not the final phase) and cite a long run;
- or tighten the `[V]` bound for these scenarios.

### S3 - Docs: the below-nominal on-crossing limit does not reproduce

**The claim.** "About 63 ppm below nominal ... carried across at -63" (RECORDED). It appears in:

- `TIME_SYNC.md:548`;
- `REGISTER_MAP.md:1956`;
- `KL_chan_map_capture.sv:100`;
- `milan_datapath.sv:5679`;
- `coherence_bench.hpp:82`.

No receipt for it is published.

**What I measured.** With the same sub-cycle probe re-derived from this head, at 3,000 columns:

| Rate | Engagements | Result | Last slip column |
|---|---|---|---|
| -63 ppm | 1,024 (every sub-step phase x 4 holds x -1..+2 cycles) | 0 failures, 0 carried across | 426 |
| -63 ppm, -4..+4 cycles | 288 | 0 carried across | 426 |
| -64 / -65 / -66 ppm | 128 each | net zero | 615 / 945 / 1,323 |
| -67 ppm | 128 | last pair at column 1,719, past a 3,000-column run's half | 1,719 |

The close never passes more than 1-2 cycles beyond the crossing through -66 ppm. Receipts: `receipts/fine-sub16--63-3000.log`, `fine-rest--63-3000.log`, `fine-sub8-*.log`.

**Why it is only a suggestion.** The stated limit is conservative: the envelope it claims is narrower than the true one. The behaviour it describes on both sides (one repeat and one skip, net zero, counted) is what I measured. At +66 and +68 ppm I agree with the stated figures (`receipts/fine-p66-1000.log`, `fine-sub16-68-3000.log`).

**Suggested fix.** Either publish the -63 receipt, or restate the limit as the pull (64 ppm) with the measured tail columns.

### S4 - Tests: the per-suite time guard needs headroom

This is Judgment 6, restated as a suggestion. When F1 is fixed, give the suite headroom against its 1,800 s guard. One option is to share the identical clean `dp` and `dp-band` control builds. Another is a quick/full split: the full arm in the scheduled bank, and `--quick` plus the fast legs on every PR.

## Judgments the round asked for

### 1. Ruling 1: the NCO terminal compare

**The period law** (`KL_media_nco.sv:241`, `cnt_r >= end_w`):

- `end_w` is one of `DIV_C-2`, `DIV_C-1` or `DIV_C`.
- The count increments only while `cnt_r < end_w <= DIV_C`, so it never exceeds `DIV_C`. `CNTW_C = $clog2(DIV_C+2)` holds it, so there is no wrap.
- Every period ends on the first cycle the count reaches or passes the end, with exactly one `tick_o`.
- A double tick would need `cnt_r = 0 >= end_w`, and `DIV_C >= 2` (guarded) keeps `end_w >= 0`. It cannot occur except at the legal borrowed period of `DIV_C = 2`, which is also unchanged.

**The phase step.** An update that lowers the end below the count ends the period at old-end + 1 cycles or earlier, so its length stays inside the legal set:

| Clock | Legal period set, cycles |
|---|---|
| 50 MHz | {1041, 1042} (no borrow is reachable at `REM_C` 32000 with a 16000 clamp) |
| 100 MHz | {2082, 2083, 2084} |

The accumulator books the trim in force on the last cycle, so the grid runs one cycle behind its account. That is exactly the declared "one-cycle phase step".

Check 10's printed trials confirm it (`receipts/head-media_nco.log`): periods 2084 / 2083 at 100 MHz and 1042 at 50 MHz, with the top count equal to the old end. "Two" cycles needs a step of more than `DEN_C` LSB, and the servo cannot produce one:

| Clock | Aligner's maximum one-frame swing | `DEN_C` |
|---|---|---|
| 100 MHz | ±200 ppm = 40,000 LSB | 48,000 |
| 50 MHz | 20,000 LSB | 48,000 |

**Steady trim.** `end_w` moves only when `trim_r` or `frac_r` moves, and `frac_r` moves only at the terminal. So at a steady trim `>=` first holds exactly where `==` did, and INTERNAL (`servo_en_i = 0`, `trim_i` tied to 0) is bit for bit the old grid. The legacy tick-for-tick transcription checks pass in `media_nco` 410 / 0.

**Consumers of `media_tick_p`** (traced in `milan_datapath.sv`):

| Consumer | Location | Effect of a one-cycle step within the legal period set |
|---|---|---|
| Capture crossbar walk | `:1288` | invisible; it drains one walk per tick |
| Tone pilot | `:787` | invisible |
| J11.9 lrclk test point | `:759` | invisible |
| `KL_render_setpoint` (render feed) | `:6282` | invisible |
| #386 settled-grid trigger's tick counter | `:6104` | invisible |
| Grid aligner, via `media_tick_q_r` | `:5719-5734` | absorbed as phase error |

CRF TX timestamps the audio-MMCM event grid, not `media_tick_p` (`KL_crf_tx.sv:17-31`). The MMCM servo consumes the CRF rate error. Neither sees the step.

**Which updates can land late.** `u_o` changes only on the frame marker, or to 0 on disengage (`KL_media_grid_align.sv:268-298`). Only an engagement whose close sits at the crossing lands updates on the terminal cycles, and the settled lock keeps them 256 cycles away.

**Required checks, all reproduced:**

| Check | Result | Receipt |
|---|---|---|
| `media_nco` at the head | 410 / 0 | `head-media_nco.log` |
| `media_nco` with the `377d1ac3` NCO | 10 failures, all check 10 (for example a 6,179-cycle period, top count 4095, at 100 MHz) | `old377-media_nco.log` |
| Other reviewer's `run_fine.sh -50 -1 2` | 20,544 checks, 0 failures; 162 of 1,024 engagements repeat and skip once, last at column 57 | `fine-m50.log` |
| Committed `CRF-fine-50` | 768 engagements, 141 single pairs, last at column 57, 0 failures | `sum-head-junction.txt` |
| The `==` mutant | killed in both legs | `head-mutation-arm.log` |

**Area.** Reproduced exactly with `KL_media_nco` bound as `milan_datapath` binds it (`TRIMW_P = 18`); Yosys 0.66, sv2v v0.0.13 (`receipts/ooc-nco-summary.txt`):

| Clock | LUT | FF | CARRY4 |
|---|---|---|---|
| 50 MHz | 101 -> 106 | 46 -> 46 | 35 -> 37 |
| 100 MHz | 103 -> 104 | 47 -> 47 | 35 -> 37 |

At the module's default `TRIMW_P = 16` the figures differ (50 MHz: 106 -> 106 LUT), which is synthesis noise. The PR should say which binding it measured, but this is immaterial.

### 2. Ruling 2: the keep-off

- `mga_keepoff.py` copies both `localparam int unsigned` declarations exactly once. Its regex spans the two-line `MGA_KEEPOFF_CYC_C` statement and fails the build on zero or two matches.
- `coherence_wrap.sv` elaborates them against `MILAN_CLK_FREQ_HZ = CLK_HZ_P`. The junction log prints "aligner keep-off 256 cycles ... engagement pull 64.0 ppm".
- RM5 (the declaration at 128) is killed by `band50` with `[C] slips while the CRF lock held` (`head-mutation-arm.log`).
- The binding-level gap is S1.

### 3. Ruling 3: the envelope, the settled lock and the grading change

**Envelope figures reproduced:**

| Figure | Measured | Receipt |
|---|---|---|
| Pull (keep-off << `KP_LOG2_P`) | 64 ppm | junction log |
| Margin 256 - 4r | 56 at 50 ppm | pulled close approaches at 53-61 cycles, round 2 |
| Unpulled transient peaks | 149 at 50 ppm, 238 at 80, 299 at 100 | `CRF-50-1`, `CRF-settle` |
| Transient limit, about 86 ppm | consistent with the recorded runs | author's summary |
| Net-zero last-slip columns | 57 at -50 ppm, 8 at +50, 181 at -60, 294 at -62, 8 at +66 | `fine-*.log` |
| ±75 ppm, 30,000 columns | one net-zero pair by column 4,690, 0 failures | `probe-[pm]75-30k.log` |

At ±75 ppm, 30,000 columns, the round-2 placements that failed at 9,000 columns now pass as acquisition under the law. The below-nominal limit is S3.

**The settled lock** is guarded well past ±100 ppm (`receipts/probe-settle-*-150k.log`). At ±100 and ±150 ppm, at 150,000 columns:

- pulled engagements lock at 255 (negative) and 256 (positive) cycles off;
- unpulled ones lock at their engagement phase;
- the tail spread is 1-3 cycles, with no tail slip;
- acquisition's single net-zero pair ends by column 19,564 at 150 ppm.

The committed `CRF-settle` shows no tail slip at ±80 and ±100 ppm, but its tail is the converging approach, not the final lock (S2). The ruling's bar, "no tail slip after acquisition, and `[V]` holds", is met.

**The grading change: a correct law, and it hides nothing.**

- `tail_start = max(frames/2, window)` and `last_slip < min(window, tail_start)` (`coherence_bench.hpp:84-97,366-369`).
- The window is the time the net departure (64 - |r|) ppm needs to carry the close one cycle clear. It is `kEngageColumns` inside the Milan bound, stretched as 14/(64 - |r|) beyond it, and unbounded at or past the pull. That is the physics of a proportional pull against a rate, and the measured last slips sit inside it:

  | Rate | Window, columns | Measured last slip |
  |---|---|---|
  | 55 ppm | 100 | 87 |
  | 60 ppm | 224 | 181 |
  | 62 ppm | 448 | 294 |
  | 63 ppm | 896 | 426 |

- It moves no committed tail. Every committed CRF run has either |r| <= 50 with `frames/2 >= 150 > 64`, or an unbounded window, where the tail stays `frames/2`.
- An empty tail cannot pass: `grade_lock` requires `lock_seen` (`sim_main.cpp:589-590`).
- **The -60 ppm slow-clearing slips are not a hidden defect.** In the other reviewer's -60 ppm probe at this head, all 115 slipping engagements of 1,024 slip exactly one repeat and one skip, net zero, counted, by column 181 (`fine-m60.log`). That is the documented behaviour between 50 ppm and the pull, and the settled lock after it is clean.
- The datapath leg asserts its CRF plan is inside the Milan bound before using `kEngageColumns` (`sim_dp.cpp:303-309`).

**`kEngageColumns` derivation.** (64 - 50) x 1e-6 x 1041.7 = 0.0146 cycles per frame gives 68 frames per cycle, less about 4 frames to the first column: 64 columns. Measured 57. The 64-column claim is now stated for ±50 ppm only in every place I checked: the TIME_SYNC tables, REGISTER_MAP, the crossbar banner and the PR body.

### 4. Ruling 4: the aligner banner

`KL_media_grid_align.sv:79-87` now:

- scopes the settle-band sentence to the module default;
- names `milan_datapath`'s 256-cycle binding and one-cycle-late tick;
- states that the #386 recentre waits up to its 32,768-tick ceiling (`SRC_SETTLE_CEIL_C = 32768`, `milan_datapath.sv:6072`).

It is a comment-only change and it resolves my R394-2 F1.

### 5. Ruling 5: the [Q] arm

`chmap_capture` `[Q]` (`sim_main.cpp:1561-1620`) drives a tick mid-walk with frame 3 closing before the queued tick and frame 4 after it. It grades all six columns pair by pair, and the counters (one skip, no dup). It also asserts the walk was still running when frame 4 closed, a vacuity guard.

- RM7 is killed by `Q: col 2 pair 0 L is frame 4`.
- RM8 is killed by `Q: col 1 pair 2 L is frame 2` and `Q: col 2 pair 0 L is frame 4`.
- Evidence: `head-mutation-arm.log`, `head-chmap_capture.log` (371 / 0, netlist 20 / 0).

### 6. CI time and the hosted risk

**Measured here** (`head-junction-full.log`, `head-dp-leg.log`, `head-mutation-arm.log`):

| Part | Wall time |
|---|---|
| Junction leg | 253 s |
| Datapath leg | 122 s |
| Committed arm, 6 threads | 172 s |

The author's sequential gate run took 1,236 s against the 1,800 s per-suite guard.

**Hosted** (`hosted-checks.txt`, `hosted-prior-shard1.txt`). `capture_coherence` took:

| Head | Hosted time |
|---|---|
| `5546b976` | about 7 min |
| `377d1ac3` | 17.6 min |
| this head | **1,442 s** (24 min 2 s: from `avtp_rxmon`'s PASS at 00:23:11 to the FAIL at 00:47:13) |

All three ran with the four dp mutation builds failing fast (F1). So 1,442 s is a floor, already 80% of the 1,800 s guard.

**Projection once F1 is fixed.** The work the hosted run skipped costs about 306 s locally:

- four dp builds, about 24 s each on 4 CPUs;
- the two controls' runs, `--quick` 48 s and `--band` 57 s on one CPU;
- the two mutants' runs, about the same (`receipts/dp-build-4cpu-timing.txt`).

This head's hosted time is about 1.55 times the matching local work (1,442 s against about 930 s). That puts a fixed suite near 1,900 s: over the guard, so it would time out instead of failing.

**Conclusion.** The suite needs a quick/full split, or build and run sharing (the `dp` and `dp-band` controls build the same unmutated datapath twice), before it can pass in the per-PR hosted shard. This is part of F1's required outcome, with the options in S4.

## Lens results (clean lenses carry their artifact)

```text
[R394] PASS Conformance — hdl/ieee1722/crf/KL_media_nco.sv:209-252; hdl/milan/milan_datapath.sv:5658-5739; tb/verilator/capture_coherence/{coherence_bench.hpp:53-97,366-369, sim_main.cpp:492,589-592,676-700} @ddb07747; receipts/head-media_nco.log, old377-media_nco.log, head-junction-full.log, sum-head-junction.txt, fine-m50.log, fine-m60.log, probe-settle-*-150k.log — round-3 rulings (5879911799) items 1-6 against #617 acceptance 1-3 and IEEE 1722-2016 7.3.5: the NCO never loses or doubles a tick at any update cycle (check 10 red at 377d1ac3, green at head); -50/-60 ppm probes 0 failures; settled lock slip-free to ±100 ppm (committed) and ±150 ppm (150k-column probes); envelope stated as relative rate; 64-column claim scoped to ±50 ppm; no torn column in any scenario.
[R394] PASS RTL — hdl/ieee1722/crf/KL_media_nco.sv:144-252 (CNTW_C/end_w widths, reset, terminal law); milan_datapath.sv:736-787,1288,5716-5739,6104,6282 (every media_tick_p consumer); KL_media_grid_align.sv:268-298 (u_o update timing); KL_chan_map_capture.sv:92-106 and KL_media_grid_align.sv:78-87 (comment-only) @ddb07747; receipts/ooc-nco-summary.txt, ooc-nco/*.stat.txt — count bounded by DIV_C, one tick per period, a late update keeps the period length in the legal set, steady trim bit-exact, INTERNAL unchanged; CRF TX and the MMCM servo do not consume the grid; area LUT 101->106 (50 MHz) / 103->104 (100 MHz), FF unchanged, CARRY4 35->37 reproduced at TRIMW_P=18.
[R394] PASS Robustness — KL_media_nco.sv:241 under trim moves on every cycle offset -3..+1 (media_nco check 10, both shapes); receipts/fine-m50.log, fine-p50.log, fine-m60.log, fine-m62-1000.log, fine-p66-1000.log, fine-sub16--63-3000.log, fine-rest--63-3000.log, fine-sub8-*.log, fine-sub16-68-3000.log, probe-[pm]75-30k.log, probe-m63-30k.log, probe-p68-30k.log, probe-settle-[mp]1[05]0-150k.log @ddb07747 — sub-cycle engagement at -50/+50/-60/-62..-67/+66/+68 ppm (every slip a single net-zero pair, counted); ±75 ppm acquisition net zero; settled lock at ±100/±150 ppm 255-256 cycles off, spread <=3, no tail slip; update-at-terminal, disengage-to-zero and INTERNAL->CRF all fall under the any-cycle guarantee; reset of cnt_r/frac_r/tick_o/trim_r unchanged.
[R394] NEGATIVE Tests — F1 (tb/verilator/capture_coherence/Makefile:94,98 with mutants.py:209-219): hosted shard 1/5 / verilator-suites red at this exact head (job 109196809736, arm 23/27) and on both earlier heads; mechanism reproduced; hosted time 1,442 s with the dp items skipped, projected about 1,900 s. Otherwise examined and sound: media_nco check 10 (sim_main.cpp:516-655) can fail (10 failures at 377d1ac3); CRF-fine-50/CRF-settle and the band50/fine/nco legs; chmap [Q]; committed arm 27/27 locally; reviewer mutants RM5/RM7/RM8/== killed, RM9 survives (S1).
[R394] PASS Docs — docs/design/TIME_SYNC.md:164-170,454-586; docs/reference/REGISTER_MAP.md:1936-1985; docs/testing/TESTING.md:490,514; CHANGELOG.md:40-62; tb/verilator/media_nco/README.md:48,115; KL_media_nco.sv:187-234; KL_media_grid_align.sv:78-87; KL_chan_map_capture.sv:92-106; milan_datapath.sv:5658-5705; PR #618 body @ddb07747 — each checked against my runs: NCO guarantee and phase step, derived keep-off, relative-rate envelope table, window law, latency-table scope and other-shape row (520.8 cycles, 104·t), [Q], nineteen mutants; R394-2 F1/F2 resolved; S2/S3 precision points are optional.
```

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round-3 rulings 1-6, #617 acceptance 1-3; KL_media_nco.sv; the aligner binding; capture_coherence grading; media_nco / junction / fine / settle / 150k-column logs | R394-3 | ddb0774779d10a9b0bd90a4822f4e5df9fdedb1b |
| RTL | CLEAN | KL_media_nco.sv whole module; every `media_tick_p` consumer in milan_datapath.sv; aligner `u_o` timing; comment-only diffs in the aligner and crossbar; NCO OOC 377d1ac3 vs head | R394-3 | ddb0774779d10a9b0bd90a4822f4e5df9fdedb1b |
| Robustness | CLEAN | Check 10 update offsets; sub-cycle probes -50...-67 / +50 / +66 / +68 ppm; ±75 ppm; settled lock ±100 / ±150 ppm at 150,000 columns | R394-3 | ddb0774779d10a9b0bd90a4822f4e5df9fdedb1b |
| Tests | UNCLEAN (F1) | capture_coherence (all files), media_nco, chmap_capture [Q]; committed arm 27/27; RM9; hosted shard 1/5 logs and artifacts; MAKEFLAGS reproduction | R394-3 | ddb0774779d10a9b0bd90a4822f4e5df9fdedb1b |
| Docs | CLEAN | TIME_SYNC.md, REGISTER_MAP.md, TESTING.md, CHANGELOG.md, media_nco README, module banners, datapath comment, PR body, REVIEW READY | R394-3 | ddb0774779d10a9b0bd90a4822f4e5df9fdedb1b |

**Note on banking.** A fix for F1 touches `tb/verilator/capture_coherence/{Makefile,mutants.py}`, which is `Tests` scope, and possibly `docs/testing/TESTING.md` if the suite is split. It does not touch the RTL, and it leaves the `Conformance`, `RTL` and `Robustness` coverage above standing, unless the split changes what the committed sweeps grade. `Docs` would need a re-read only for whatever TESTING.md or the PR body say about the split.

## Prior public review findings at this head

I wrote this section after the verdict and ledger above. It covers the round-2 reports on this PR: my R394-2 (comment 5879806778) and the external R395-2 (comment 5879904352). The round-1 findings were resolved at `377d1ac3` (R394-2's table), and nothing in round 3 reopens them. No round-3 report by another reviewer was read. Nothing here changes the verdict or the ledger.

| Prior finding | Status at ddb07747 | Evidence |
|---|---|---|
| R395-2 F1 (MAJOR, all lenses): an on-crossing engagement at -50 ppm loses two media ticks (the NCO `==` race) and slips net non-zero | **RESOLVED** in `KL_media_nco` (monotone compare), independent of the aligner's timing, as ruling 1 required | Judgment 1: `media_nco` check 10 (10 failures at `377d1ac3`, 0 at head); committed `CRF-fine-50` (768 engagements, 0 failures, killed by `==` in the arm); the other reviewer's `run_fine.sh -50 -1 2` at head 0 failures, every slip a single net-zero pair by column 57 |
| R395-2 F1, its -60 ppm row (98 failures) | **RESOLVED**, by the corrected window rather than by the NCO fix: every -60 ppm slip is a single net-zero pair by column 181, inside the window 224 | `fine-m60.log` (0 failures; 115 slipping engagements, all `1 repeats, 1 skips`); Judgment 3 on the grading law |
| R395-2 F2 (MINOR, Tests) = R394-2 S2: the shipped keep-off unprotected | **RESOLVED** as ruling 2 worded it: the wrapper binds the declaration, and `band50` kills RM5 | `head-mutation-arm.log`. The residual binding-level gap is my new S1 (optional) |
| R395-2 F3 (MINOR, Docs/Robustness/Tests) = R394-2 F2 (MINOR, Docs): envelope misstated (±75 ppm of source error), `kEngageColumns` derivation wrong | **RESOLVED.** The envelope is a relative rate with measured limits and behaviour beyond them; the derivation is (64 - 50) ppm; no "±75" remains in the PR body, TIME_SYNC.md, REGISTER_MAP.md, the crossbar banner or the CHANGELOG | Judgment 3. The precision points are my new S2 and S3 (optional) |
| R394-2 F1 (MINOR, Docs): the aligner banner said a raced engagement starts inside the root's settle band | **RESOLVED** | `KL_media_grid_align.sv:79-87` (Judgment 4) |
| R394-2 S1 (Tests): the queued-tick path had no check | **TAKEN** | `chmap_capture` `[Q]`; RM7 and RM8 killed |
| R394-2 S3 (Docs): the pulled-engagement margin and the latency-table scope | **TAKEN** | TIME_SYNC.md:474-481,494,547; `milan_datapath.sv:5673-5679` |
| R395-2 S1 (Docs): a pointer from the aligner banner to the datapath binding | **TAKEN** | Ruling 4 |
| R395-2 S2 (Tests/CI): confirm the hosted duration against the 1,800 s guard | **STILL OPEN.** It is carried into F1's required outcome. The hosted run at this head took 1,442 s with the dp legs failing fast; with them, projected about 1,900 s (Judgment 6) | `hosted-checks.txt`, `hosted-prior-shard1.txt` |

## Evidence I ran (receipts listed in MANIFEST.sha256)

**Setup.**

- **Simulator:** Verilator 5.050. The assignment's path under `372-manager-candidate1` does not exist. I used `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator`, whose wrapper hash matches the one my round-1 and round-2 packets recorded (`receipts/tool-identity.txt`).
- **Tree:** every run used a `git archive` of the head (`receipts/r394-scratch-tree.txt`).
- **Clone:** never built or edited. `receipts/r394-clone-integrity.txt` shows HEAD, tree and index at the exact head, a clean worktree and submodules with nothing ignored, and all four gitlinks equal to `HEAD`'s.
- **Parallelism:** at most 8 parallel jobs.

| Run | Result | Receipt |
|---|---|---|
| `capture_coherence` junction leg (`make run`) | 20,832 checks, 0 failures, rc 0, 253 s | `head-junction-full.log`, `sum-head-junction.txt` |
| Datapath leg (`make dp`) | 332 / 0, rc 0, 122 s; `--band` 198 / 0 | `head-dp-leg.log`, `head-dp-band.log` |
| Committed mutation arm, via its own `clean_control`/`grade_mutant`, 6 threads (`scripts/r394_run_arm.py`) | 27 / 27 PASS, 172 s | `head-mutation-arm.log` |
| `media_nco` at head / with the `377d1ac3` NCO (`NCO_SRC`) | 410 / 0; 400 / 10, all check 10 | `head-media_nco.log`, `old377-media_nco.log` |
| `chmap_capture` | 371 / 0; netlist 20 / 0 | `head-chmap_capture.log` |
| `media_grid_align` | 45 / 0; 3 negative controls red | `head-media_grid_align.log` |
| Other reviewer's sub-cycle probe, re-derived at this head: -50 / -60 / +50 ppm | 20,544 / 0; 20,544 / 0; 25,664 / 0; last slips 57 / 181 / 8 | `fine-m50.log`, `fine-m60.log`, `fine-p50.log` |
| Sub-cycle probe at -62 / +66 ppm, 1,000 columns | 0 failures; last slips 294 / 8 | `fine-m62-1000.log`, `fine-p66-1000.log` |
| Sub-cycle probe at -63 (all phases) and -63 wide, -64...-67, +68, 3,000 columns | net zero through -66; last pair at column 1,719 at -67 and about 1,700 at +68 (past a 3,000-column run's half) | `fine-sub16--63-3000.log`, `fine-rest--63-3000.log`, `fine-sub8-*.log`, `fine-sub16-68-3000.log` |
| Placed probes, 30,000 columns (`scripts/r394_probe.py`): ±75, -63, +68 ppm | 0 failures; ±75 one net-zero pair by column 4,690 | `probe-[pm]75-30k.log`, `probe-m63-30k.log`, `probe-p68-30k.log` |
| Settled lock, 150,000 columns: ±100, ±150 ppm, on the crossing and 256 cycles off | 0 failures; lock 255-256 cycles off, spread 1-3, no tail slip | `probe-settle-*-150k.log` |
| RM9, a literal 128 keep-off in the `milan_datapath` instance, through the datapath leg | survives: 332 / 0, `--band` 198 / 0, with lock phases moved | `rm9.diff`, `rm9-dp-*.log`, `rm9-dp-build.txt` |
| `MAKEFLAGS` reproduction through the committed `mutants.build('dp')` (`scripts/r394_mf_repro.py`) | builds without it; `None` ("did not compile") with `MAKEFLAGS=w` | `makeflags-dp-build-repro.txt` |
| dp build and `--quick` run pinned to 4 CPUs | 22-24 s build, 49 s run | `dp-build-4cpu-timing.txt` |
| NCO OOC, `377d1ac3` vs head (`scripts/r394_ooc_nco.sh`, Yosys 0.66, sv2v v0.0.13) | at `TRIMW_P=18`: 50 MHz LUT 101 -> 106, 100 MHz 103 -> 104; FF unchanged; CARRY4 35 -> 37 | `ooc-nco-summary.txt`, `ooc-nco/*.stat.txt` |
| Hosted, earlier heads (read-only job logs and artifacts) | shard 1/5 red at `5546b976` and `377d1ac3`, dp mutation legs "did not compile" | `hosted-prior-shard1.txt` |
| Hosted, this head (read-only job log and artifact) | `verilator-suites` **failure**: shard 1/5 red, `capture_coherence` arm 23 / 27, the 4 dp items "did not compile", junction 20,832 / 0, dp 332 / 0, 1,442 s. Shards 0, 2, 3, 4 and Yosys shards 0-3 pass; `yosys-portability`, `rtl-fast`, lint, elaborate and docs checks pass; `Physical gPTP` skipped | `hosted-checks.txt` |

## Limits

- **Not run by me:**
  - `milan_dp`, `milan_dp_render`, `tdm`, `pair_fill`, `pp_shadow` and the `hdl/ieee1722/crf` suites (`crf_rx`, `crf_tx`, `mmcm_servo`, `mmcm_servo_autorepair`), all of which instantiate or neighbour the NCO;
  - the builder bank, lint, xvlog and Yosys `run.sh`;
  - the Markdown and code-quality gates;
  - act and any host runner.

  These are the manager's. The published round-3 evidence reports 52,285 checks with 0 failures (`suite-tally-ddb0774.txt`). My NCO consumer analysis is by RTL reading.
- **F1's version attribution.** I could not run GNU make 4.3, so attributing F1 to it is inference from the hosted image. The failure pattern and the `MAKEFLAGS=w` reproduction are measured.
- **Drift-level coverage.** Simulation covers the 1x1 TDM8 shape at 50 MHz. The 100 MHz grid is covered only by `media_nco`'s shape A and RTL reading.
- **Source model.** The harness's plan ppm stands for the relative rate at the aligner (TDM frame against the axis clock). Envelope figures are harness measurements, not product measurements.
- **No hardware.** Physical calibration was NOT RUN, and #617 acceptance 4 (the #451 bench re-run) is open. Simulation passes and skipped field contexts (`Physical gPTP`) are not hardware proof.
- **Redaction.** The home-directory prefix is redacted to `$HOME` in receipts.

## Pending manager duties

- **Route F1.** The fix makes the `dp` and `dp-band` legs build hosted. Then obtain an exact-head `Verilator shard 1/5` that passes with the full arm, and record `capture_coherence`'s hosted elapsed time against the 1,800 s guard. Decide the quick/full split, or build sharing, if it is over or close (S4). Request a `Tests` re-review at the resulting head.
- **Hosted and act acceptance** at the exact head. `verilator-suites` is red at this head (F1). Every other hosted context passed, except `Physical gPTP`, which was skipped (`hosted-checks.txt`).
- **Final current-dev candidate validation** at the merge turn: source base `ce550952`, live dev `eaa88a32eb77adeba9c1c631198c7fb516a11095`.
- **Acceptance 4** (the #451 bench re-run on the next image) remains open; the PR says "Relates to #617".
- **Optional:** S1-S4.

R394-3 FINISHED
