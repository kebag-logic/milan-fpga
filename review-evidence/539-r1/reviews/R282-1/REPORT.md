[R282] NEGATIVE - exact head f49b57a60ae4ce72e7a1a9ea8e5db13f1ca838ed

# R282-1 internal independent review: issue #539 / PR #547

- Head: `f49b57a60ae4ce72e7a1a9ea8e5db13f1ca838ed`, tree `52329eb1f29ffbc774a23da9a3c6e062514ee9e3` (verified in `receipts/clone_integrity.log`).
- Source base: `26d855a9176d63625e6635a029a0c44e3d57ce9a`. Live dev at review time: `f86c34fe2ddbc6cfb7c8c70ddbe0d9726f4d3c2f`.
- Round: R282-1. All five lenses were applied: Conformance, RTL, Robustness, Tests and Docs.
- Reconstructed from: AGENTS.md, CONTRIBUTING.md (sections 1, 3 and 5), docs/README.md, the #539 body and its three comments, the #387 authorities (5794731090, 5606198212, 5802264260), `timestamp_counter.sv`, `ptp_csr_sync.sv`, `KL_crf_rx.sv`, the servo instance in `milan_datapath.sv`, the pinned plane's step microcode, the diff `26d855a9..f49b57a6` (4 commits), and the public evidence tree `review-evidence/539-r1` at `1363d132`.
- That evidence tree holds only the author packet. I did not find a manager bank log at that commit, so every result below comes from my own runs, with receipts in this packet.

## Verdict

The fix is correct. I reproduced the defect myself. The RTL is sound at every step position I examined, and on the real datapath wiring it neither misses a step nor reports a false one. Conformance, RTL and Robustness are clean.

The verdict is NEGATIVE because of two MINOR findings:

- **F1 (Tests, Docs):** two claims this PR adds to the unit harness cannot fail for what they name.
- **F2 (Docs):** the design doc that #540 has since merged to dev states the #539 defect as current. This PR has to correct it when it lands second, and the head does not.

Neither finding touches the product RTL.

## What was checked, and the result

### Acceptance 1: the reproduction (independent)

`scripts/run_base_repro.sh` ran the head's silicon-scale harness against the **base** servo RTL. The probe copy reads `ptp_jump_r` as 0 because the base has no detector. Receipt: `receipts/base_repro.log`.

| Step at mid-window (base RTL) | First close: window error | Integrator | Discards |
|---|---|---|---|
| +21 us | +21040 (+41.09 ppm) | +15680 -> +26200 | 0 |
| +100 us | +100040 (+195.39 ppm) | -> +65700 (+128.32 ppm) | 0 |
| +108 us | +108040 (+211.02 ppm) | -> +69700 | 0 |
| **+150 us** | **+150040 (+293.05 ppm)** | **+15680 -> +90700 (+177.15 ppm)** | 0 |
| -150 us | -149960 | -> -59300 (-115.82 ppm) | 0 |
| +300 us, +524 us | +586, +1023.5 ppm | -> +102400 (the +200 ppm clamp) | 0 |
| +525 us | +1025.47 ppm | held (+15680) | 1 |

- Every step from 21 us to 524 us is integrated. From 525 us up, the old 1024 ppm guard discards the window.
- The head's P-suite run against the base RTL fails 66 of 113 checks, so the suite discriminates.
- My numbers match the author's published pre-fix record, `repro/prefix_step_150000.log`, exactly.
- **Acceptance 1 is met.**

### Acceptance 2: the fix, and the interpretation question put to the reviewer

**The detector** is `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:449-460`.

- `ptp_jump_r` is set on the edge that stages a jumped sample into `ptp_q_r`, so it lines up with the sample `ptp_q_r` holds.
- The 32-bit unsigned difference exceeding 4096 catches forward steps from about 4.1 us.
- It catches backward steps from about one PHC increment up, because a backward step wraps to a large value.
- Only steps within 4 us of k*2^32 ns (4.29 s or more) alias. Those produce |e| of at least 2^20 after ECLAMP, so the kept 1024 ppm guard discards them.

**Sequencing** is `:656-668`. I traced four positions:

- **Mid-window:** `win_valid_r` falls, and the next tick re-bases on post-step time.
- **Boundary tick sampling the stepped value:** T0 fires, and the step clears `pp_run_r` because `pp_seq_r == 0`, so the sequence runs without writeback.
- **One edge after T0:** `pp_seq_r == 1`, so the pre-step window commits and the new window is abandoned.
- **Re-base tick itself** (`win_valid_r == 0`): `step_hit_w` is 0, and the new base is post-step, which is correct.

Every case matches the header's claims.

**I accept the interpretation.** Acceptance 2's "(the plane's step pulse)" names *which* steps must be discarded, not the mechanism. Detecting the pulse's effect at `ptp_now_i` meets the clause for every plane step, for these reasons:

- The pulse reaches the PHC as exactly one adjtime. It is a toggle-synchronised single pulse in `ptp_csr_sync.sv:138-178`, and it lands in one cycle through `timestamp_counter.sv:156-169`.
- The pinned plane never steps below 20 us (`gen_gptp_ucode.py:378`, `STEP_NS_C = 20000`). The #387 policy steps above 20 us at link-up and above 100 us once locked.
- It also covers CSR adjtime and settime, which matter in plane-off builds.
- It avoids a real hazard of wiring the pulse. The PHC write trails the pulse through `ptp_csr_sync`, so a pulse near a boundary would mark the wrong window.

The rest of the clause, "every step size between 100 us and 1 s leaves the integrator untouched", is met:

- My head run (`receipts/head_suite.log`) covers P1 at +21 us, +/-100 us, +108 us, +/-150 us, +300 us, +524 us, +1 ms and +/-1 s, plus P2a/b/c at the boundary positions. For each:
  - the integrator moves 0 at the step window's close (P2a asserts exactly 0);
  - the next clean window moves it by at most one clean window's worth;
  - LOCKED holds on every edge;
  - one discard is counted.
- The detector is size-monotonic between the sampled sizes, so the sweep stands for the whole range.
- A local step cannot leak through `crf_rate_i`. `KL_crf_rx.sv:476` computes `rate_o` only from PDU timestamps, and its lock logic does not read local time. So discarding the local window is sufficient.

**Acceptance 2 is met.**

### Acceptance 3: failing arms, independently re-derived

`scripts/mutate.py` refuses to run unless each mutant's anchor matches exactly once. Each mutant runs both harnesses at 1 job. Receipts: `receipts/mut/*.log` and `receipts/mutation_summary.txt`.

| Mutant | Unit (59) | Step suite (113) | Verdict |
|---|---|---|---|
| M1 step detector off | 0 fail | 66 fail | killed (step suite only) |
| M2 no abandon | 1 fail | 53 fail | killed |
| M3 no boundary squash | 0 | 19 | killed |
| M4 unconditional squash | 0 | 1 (P2b) | killed |
| M5 1024 ppm guard off | 3 (U11) | 7 | killed |
| M6 single tally | 0 | 1 (P3) | killed |
| M7 guard tightened to 32 ppm | 25 | 3 (P4) | killed |
| M9 detector threshold 25 us | 0 | 23 | killed (the 21 us arm) |
| M10 signed detector compare | 0 | 51 | killed (negative steps) |
| M11 detector one cycle late | 0 | 23 | killed (the P2 alignment arms) |
| M15 step not tallied | 1 | 15 | killed |
| **M8 guard's 4-discard resync removed** | **0** | **0** | **survives (F1)** |
| M12 step does not restart the discard streak | 0 | 0 | survives (S1) |
| M13 step tallied with no open window | 0 | 0 | survives (S1) |
| M14 tally wraps instead of saturating | 0 | 0 | survives (S1) |

- All seven arms the author claims reproduce as failing.
- Acceptance 3's three named arms exist: the step-window discard (P1/P2), the guard (U11 and P3), and the rate path (P4).
- **Acceptance 3 is met**, apart from the coverage claims in F1.

### Real datapath wiring and false-step safety (CRF leg)

`scripts/run_aclk_probe.sh` builds the `milan_dp` aclk leg with the plane off. A probe copy of `sim_aclk.cpp` reads `0x8F8` around `[RENDER-RC-CRF]`; no product source is modified. That phase issues two real CSR PHC adjtimes of 65536 ns while the CRF selection drives the servo. Receipt: `receipts/aclk_probe.log`.

| When | MCSRV_STAT | Discards |
|---|---|---|
| After the CRF lock, before the adjtimes | `0x00000033` (ACQUIRE) | **0**: no false step on the real PHC |
| After the two adjtimes | `0x00000833` | **2**: each real adjtime seen once |
| After `[RING-CRF]` | `0x00000833` | 2: nothing further |

- The leg's result was `media_aclk: 139 checks, 0 failures`.
- The PHC and the servo share one clock in the SoC (`milan_soc.py:781-783`) and in the harness, so `ptp_now_i` is read synchronously.
- A legitimate per-cycle advance is `incr + adj`. That is at most about 384 ns (Q8.24 unsigned `incr` plus signed `adj`), more than 10x below 4096 ns.
- With the plane enabled, a plane step reaches the PHC through the same `cmd_adjust_i` path this probe drove: the `milan_datapath.sv:2739-2743` mux, then `ptp_csr_sync`.

### RTL, cost and gates

- **Area** (`scripts/ooc_servo_area.sh`, the ooc.sh `synth_xilinx -family xc7 -flatten` recipe): base 831 LUT / 789 FF / 140 CARRY4, head 862 / 790 / 150. That confirms +31 LUT, +1 FF and +10 CARRY4: one 32-bit subtract and compare, plus the 7-bit tally. The area figures in `AREA_BUDGET.md` and the builder are dated estimates, not ratchets, so there is nothing to update.
- **Timing structure:** the new cone is `acc` (a register in `timestamp_counter`), then a 32-bit subtract and compare, then `ptp_jump_r`. The servo's own existing cones feed `step_hit_w`. No new CDC. Vivado timing was not run.
- **Reset:** `ptp_jump_r` has a synchronous reset. `disc_cnt_r` clears in IDLE, as `REGISTER_MAP` now states. `ptp_q_r` stays unreset; it already was, and it is a pure pipeline stage.
- **Gates at head**, run in the clone read-only (`receipts/static_gates_clone.log`): `lint_rtl --check` PASS (90 <= 90, no servo line), `check_sv_idiom` OK, `check_cpp_idiom` exit 0, `check_rtl_source_lists` OK, `check_em_dash --base 26d855a9` 0 findings. `docs_check` reported 0 findings on the export (`receipts/static_gates.log`), and `git diff --check` was clean.
- **Suites at head** (`receipts/head_suite.log`, pinned simulator `Verilator 5.050 rev v5.050`, `-j 8`): `mmcm_servo` 59/59 + 8/8 + 113/113, `mmcm_servo_autorepair` 47/47. The repository's `suite_tally.py` reads 227 checks, 0 failures.

### The U10 envelope change

The base harness's single-sample U10 check, run against the head RTL, fails at pre 1519 / post 1579 (|d| = 60 > 48). Receipt: `receipts/old_u10_on_head.log`.

The head run shows this is locked jitter, not a kick:

- the locked envelope before the step is [1459, 1559];
- U11 reaches 1577 with no step at all;
- the rail signature the check hunts is |d| of about 1700.

The envelope check samples every millisecond for 3 windows and adds a one-count discard assertion. So this is a fix of a check that depended on sample phase, **not** a weakening made to obtain a pass. F1 concerns what U10 now *claims*, not this tolerance.

## Findings

### F1: MINOR (Tests, Docs): two new unit-harness claims cannot fail for what they name

- **Where:**
  - `tb/verilator/mmcm_servo/sim_main.cpp:20-22` and `:318-321`. U10 says that since #539 the leg "proves the step guard rides out a sustained storm" and is "the PHC step guard's".
  - `sim_main.cpp:23`, `:395`, `:399` and `:413`. U11 says it covers the 1024 ppm guard's resync: "the 4th consecutive one resyncs the baseline" and "(the resync path included)".
  - PR #547 body: "gives 6 discards and the resync".
- **Evidence:**
  - With the step detector removed (M1), the unit harness passes 59/59, every U10 check included (`receipts/mut/M1_detector_off.log:60-73`). The kept 1024 ppm guard catches the 50 ms step and the 8 ms storm at this compressed scale, and "the step counted once" still reads 1.
  - With the guard's 4-discard resync removed (M8), both harnesses pass (59/59, 113/113).
  - The resync gap predates this PR: the base harness also passes with it removed (`receipts/base_resync_probe.log`). But U11 is new, and it names the resync as covered.
  - The step guard itself is properly armed in `sim_phc_step.cpp`.
- **Authority:** AGENTS.md section 6, Tests lens: "Each new test can fail for the defect it claims to detect". Docs lens: the PR must give a cold reviewer accurate evidence.
- **Impact:** a later reader, or a later change, relies on U10 as the step guard's storm proof and on U11 as the resync's proof. Neither holds. Removing the resync, or regressing the step guard at unit scale, would pass the unit harness while its text says it is covered.
- **Required outcome:** either make the checks discriminating, or correct the text to what the checks prove, in the harness comments, the check labels and the PR body.
  - For U10: a check that fails with the step detector off, or text that credits the storm to whichever guard catches it.
  - For U11: a check that fails without the resync, or no resync claim.
- **Verification:**
  - Re-run `scripts/run_mutant.sh M1_detector_off` and `M8_no_guard_resync`.
  - Either the named checks now fail, or the claims are gone from `sim_main.cpp` and the PR body.
  - Every other arm in the table above stays killed.

### F2: MINOR (Docs): at the merge target, an authoritative design doc states the #539 defect as current

- **Where:** live dev `f86c34fe`, `docs/design/GM_LOSS_RECOVERY.md` (`receipts/dev_gm_loss_539_rows.txt`):
  - `:154`, CRF servo row: "discards a window above 1024 ppm; a locked step of about 108 to 524 us passes that guard (#539)";
  - `:152`, grid aligner row: "a step reaches it only through the CRF-steered grid (#539)".
- **Evidence:**
  - #540 merged at 2026-09-24T05:45Z, after this head was committed at 02:12Z.
  - The PR body commits that "whichever PR lands second updates it". #547 now lands second.
  - The head's tree predates the row, so the head has no update.
  - Once this change is in, a local PHC step no longer reaches the servo. The remaining paths into the CRF-steered grid are the ones filed as #545 (slew) and #546 (talker step).
- **Authority:** AGENTS.md section 7, "authoritative documentation is current" and "the candidate merge result is validated". Docs lens: a changed contract is reflected in the authoritative docs.
- **Impact:** merged as-is, dev's recovery design doc says the servo integrates a 108 to 524 us step, which contradicts the RTL, `TIME_SYNC.md` and `REGISTER_MAP.md` in the same tree.
- **Required outcome:** the head that merges corrects `GM_LOSS_RECOVERY.md:154`, and `:152` where its `#539` pointer no longer names the live path. It also checks that the `TIME_SYNC.md` loop-table rows combine cleanly with dev's new "Step policy" section. This can be the lane merging dev, or a fix-up commit.
- **Verification:**
  - `git grep -n "108 to 524" <candidate>` returns nothing under `docs/design/`.
  - The CRF servo row states that the step window is discarded (#539), and points at #545 and #546 for what remains.
  - A Docs re-review at that head.

### Suggestions (optional; they do not affect coverage)

- **S1 (Tests).** Three survivors pin behaviour that no check reaches:
  - M12: a step restarts the 1024 ppm discard streak (the RTL comment at `:655`).
  - M13: `step_hit_w` requires an open window, so a second step before the re-base tick is not counted again.
  - M14: `[15:10]` saturates at 63, which `REGISTER_MAP.md` 0x8F8 now documents. The rewritten clamp at `:664-668` is correct by inspection: 63 + 2 = 65 fits the 7-bit sum.

  A short arm per item would pin them.
- **S2 (Docs/RTL).** The `STEP_DET_NS_C` note at `KL_mmcm_drp_servo.sv:296-301` bounds a legitimate advance by the Q8.24 increment alone, "below 256 ns". The per-cycle advance is `incr + adj`, up to about 384 ns. The 4096 ns margin still holds by more than 10x, but the note could say so.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #539 acceptance 1-3; #387 authorities 5794731090, 5606198212, 5802264260; `KL_mmcm_drp_servo.sv:54-77, 296-302, 444-460, 596-668`; `receipts/base_repro.log` (the defect reproduced on base); `receipts/head_suite.log` P0-P4; `KL_crf_rx.sv:476` (rate independent of local time); `gen_gptp_ucode.py:378`; the acceptance 2 interpretation is judged met | R282-1 | f49b57a60ae4ce72e7a1a9ea8e5db13f1ca838ed |
| RTL | CLEAN | `KL_mmcm_drp_servo.sv:439-460` (alignment and width), `:549-668` (T0, micro-sequence, step and guard precedence, tally), `:902` (status map); `timestamp_counter.sv:145-169`; `ptp_csr_sync.sv:138-178`; `milan_datapath.sv:2739-2743, 2808-2833, 5484-5490`; `receipts/ooc_servo_area.log` (831->862 LUT); `receipts/static_gates_clone.log` (lint, sv idiom) | R282-1 | f49b57a60ae4ce72e7a1a9ea8e5db13f1ca838ed |
| Robustness | CLEAN | Step at mid-window, on the boundary sample, one edge after, and in the last tick; both signs; 21 us to 1 s; aliasing near 2^32 falls to the guard; a coincident guard discard; a step storm (U10); false-step safety on the real PHC and a true positive on a real CSR adjtime (`receipts/aclk_probe.log`); the legitimate-advance bound; IDLE clears; mutants M9-M11 and M15 killed | R282-1 | f49b57a60ae4ce72e7a1a9ea8e5db13f1ca838ed |
| Tests | UNCLEAN (F1 open) | `tb/verilator/mmcm_servo/sim_phc_step.cpp` (all 494 lines), `sim_main.cpp` U10/U11, `Makefile` (the run gate includes Vphc_step); `receipts/mutation_summary.txt` (15 mutants); `receipts/old_u10_on_head.log`; `receipts/base_resync_probe.log` | R282-1 | f49b57a60ae4ce72e7a1a9ea8e5db13f1ca838ed |
| Docs | UNCLEAN (F1, F2 open) | `docs/design/TIME_SYNC.md:109-110`, `docs/reference/REGISTER_MAP.md` 0x8F8 row (it corrects the old "[15:9] reserved" error), `docs/testing/TESTING.md:481`, the servo header `:54-77`, PR #547 body; dev `f86c34fe` `GM_LOSS_RECOVERY.md:152,154,181`; `check_em_dash` and `docs_check` clean | R282-1 | f49b57a60ae4ce72e7a1a9ea8e5db13f1ca838ed |

## Real limits of this round

- **Physical calibration was NOT RUN**, and no hardware was used. Every result is a Verilator 5.050 simulation.
- I did not run the full `milan_dp` default suite, `milan_dp_render tdm8render`, the Yosys portability bank, the builder bank, hosted CI, act, or Vivado timing.
- The `xvlog_gate` could not be run here because no Vivado was available.
- The plane-enabled step path was checked by reading the RTL. Only the plane-off CSR adjtime path was exercised on the datapath.
- The manager's bank evidence named in the review start was not present in the evidence tree at `1363d132`. My conclusions rest on my own runs.
- The base reproduction reads `ptp_jump_r` as constant 0 in a probe copy of the harness. The base RTL has no such signal. Only P2's arm assertions read it.

## Prior public review findings on this PR (read after the verdict and ledger above were written)

The only prior review is the external round, [R283] NEGATIVE at this same head (PR #547 comment 5808190731). Its items at this head:

- **R283 F1, MINOR, Tests (U11 claims the resync path; the `no_resync` mutant survives): RETAINED.**
  - It is the same defect as the U11 half of my F1. My M8 reproduces it independently: 59/59 and 113/113, and the base harness also survives the mutant.
  - My F1 goes further in two ways. It adds the U10 half: with the step detector off, U10 passes 59/59. It also attributes the finding to Docs, because the PR body repeats the claim.
  - Open at this head.
- **R283 S1 (streak reset unarmed), R283 S2 (saturation and the open-window tally rule unarmed), R283 S3 (the 256 ns bound omits `adj`): RETAINED as SUGGESTIONS.** They match my S1 (M12, M13, M14) and my S2.
- **R283's Docs PASS rested on "the GM_LOSS_RECOVERY row lives on #540's lane".** R283 was posted at 05:20Z. #540 merged to dev at 05:45Z (`f86c34fe`), so that row is now on the merge target. That change after R283 is what my F2 records, and it does not contradict R283 at the time it was written.

## Pending manager duties

- Build and validate the current-dev candidate against `f86c34fe`, including the F2 doc correction and the `TIME_SYNC.md` merge with dev's step-policy section.
- Record hosted exact-head `rtl-fast`, `verilator-suites` and `yosys-portability` evidence, distinguishing executed jobs from skipped ones.
- Decide whether the newly documented `MCSRV_STAT[15:10]` semantics need a `CHANGELOG.md` line. The assignment named that file as held by #529.
- Re-review at the head that answers F1 and F2. Tests and Docs must be covered again at that head.

R282-1 FINISHED
