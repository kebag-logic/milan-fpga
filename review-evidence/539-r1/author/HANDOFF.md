# HANDOFF: #539 CRF servo PHC step guard (author A227)

Lane: `539-crf-servo-step-guard`, local only (not pushed), worktree
`$LANES/539-crf-servo-step-guard`, base dev
`26d855a9176d63625e6635a029a0c44e3d57ce9a`.

Head: `f49b57a60ae4ce72e7a1a9ea8e5db13f1ca838ed`

| Commit | Subject |
|---|---|
| `c16cd61e7bddb33a835c49d98290b1a08640b204` | Reproduce #539 at the silicon window scale (the trace harness alone) |
| `8dd0dd8ab82a64ef9f135f19e1c038a9aea0253a` | Abandon the CRF servo window that contains a PHC step (RTL + both benches) |
| `1c043ffacae6d7ade8c50c45f1b8d9611e079e64` | Read the step suite's LOCKED verdict past the close |
| `f49b57a60ae4ce72e7a1a9ea8e5db13f1ca838ed` | Docs: TIME_SYNC loop table, REGISTER_MAP `0x8F8`, TESTING `mmcm_servo` row |

## Outcome

- Reproduced (acceptance 1). A locked servo under CRF selection takes a 150 us PHC step, simulated with the servo's DEFAULT (silicon) parameters: a 1 ms tick, a 512 ms window and `NORM_SHIFT_P = 0`. The step is committed to the integrator: +30.62 ppm to +177.15 ppm, and the written rate jumps +100 ppm (slew-limited). The claim is wider than filed. Every step below 524.288 us is integrated, including 100 us to 108 us and the 21 us link-up step (mutant M1). Only steps above 2^19 ns meet the old guard.
- Fixed (acceptance 2) inside `KL_mmcm_drp_servo` only. The servo detects the step by its effect: `ptp_now_i` advancing more than 4096 ns in one `clk_i` cycle. The window that contains the step is abandoned and re-based at the next tick. Every size from 21 us to 1 s, both signs, leaves the integrator, the written rate and LOCKED untouched, and each step is counted once in `MCSRV_STAT[15:10]`.
- **No `milan_datapath.sv` edit is needed.** The servo port list is unchanged. The plane's `phc_step_we_o` becomes one adjtime in `timestamp_counter`, which lands in `ptp_now_w` in one cycle, and the servo sees exactly that. CSR adjtime and settime are caught by the same rule. So there is no wiring edit to hand over, and no dependency on #529.
- Failing arms (acceptance 3): seven one-line RTL mutants, each failing its named check (below).

## Reproduction (pre-fix RTL, base 26d855a9)

`make -C tb/verilator/mmcm_servo trace STEP_NS=<n>` at `c16cd61e`. Talker +20 ppm, PSCLK 200 MHz, the step lands at tick 256 of a locked window. Units are ns per 512 ms window (512 = 1 ppm). Raw logs: `repro/prefix_step_<n>.log`.

| Step | Window error | Integrator | Written rate | Next state | Discards |
|---|---|---|---|---|---|
| +100 us | +100040 (+195.39 ppm) | +15680 -> +65700 (+128.32 ppm) | +30.65 -> +130.65 ppm | ACQUIRE | 0 |
| +150 us | +150040 (+293.05 ppm) | +15680 -> +90700 (+177.15 ppm) | +30.65 -> +130.65 ppm | ACQUIRE | 0 |
| -150 us | -149960 (-292.89 ppm) | +15680 -> -59300 (-115.82 ppm) | +30.65 -> -69.35 ppm | ACQUIRE | 0 |
| +300 us | +300040 (+586.02 ppm) | +15680 -> +102400 (clamp, +200 ppm) | +30.65 -> +130.65 ppm | ACQUIRE | 0 |
| +524 us | +524040 (+1023.52 ppm) | +15680 -> +102400 (clamp) | +30.65 -> +130.65 ppm | ACQUIRE | 0 |
| +525 us | +525040 (+1025.47 ppm) | held (discarded) | held | LOCKED | 1 |
| +1 ms | +1000040 | held (discarded) | held | LOCKED | 1 |
| +1 s | +1058816 (ECLAMP) | held (discarded) | held | LOCKED | 1 |

After an integrated step, the servo was still 29 ppm off its operating point four windows later (+150 us row: written rate +59.45 ppm against +30.65 ppm).

Post-fix, the same traces at `1c043ffa` (`postfix/step_<n>.log`) show +100 us, +/-150 us, +524 us and +1 s each give: one discard, the next window's error +40 (+0.08 ppm), the integrator +15680 -> +15700, trim 490, LOCKED throughout.

## Design, and what a reviewer should challenge

- A threshold cannot do this. Once locked the plane steps above 100 us, which is 195 ppm of one window, while a legitimate window error reaches about 211 ppm (base plus authority). So the fix does not tune `GUARD_THR_C`.
- The pulse is not wired. Detecting the effect at `ptp_now_i` covers every PHC step source (the plane, CSR adjtime, settime). It needs no port. And it cannot be misordered against the PHC write: `phc_step_we_o` reaches the counter through `ptp_csr_sync`, so a wired pulse would arrive cycles before the time moves. This is the one material interpretation of acceptance 2 ("any PHC step (the plane's step pulse) discards the servo window that contains it"). It is stated in the PR body and the REVIEW READY comment.
- The detector is registered aligned with `ptp_q_r` (`ptp_jump_r` compares `ptp_now_i[31:0]` with `ptp_q_r[31:0]`), so the boundary logic reads the verdict about the very sample it snapshots:
  - A boundary closing on the stepped sample is squashed (P2a).
  - A micro-sequence already in flight closed on a pre-step sample and commits (P2b).
  - A step inside the last tick turns the boundary tick into a re-base (P2c).
- The discard tally moved to one place (`disc_tally`) so that a 1024 ppm discard and a step on the same cycle count two (P3).
- Threshold 4096 ns: a legitimate per-cycle advance is below 256 ns on any clock (the counter increment is Q8.24), and the plane's smallest step is 20 us. Steps within about 4 us of a whole multiple of 2^32 ns alias in the 32-bit difference; the 1024 ppm guard catches those, because their window error clamps at 2^20.
- Contract: `ptp_now_i` must be synchronous to `clk_i`. The window measurement already requires this, and `milan_datapath.sv` states that `gtx_clk == axis_clk` in every real instantiation. A torn multi-bit read would cost a discarded window, never a wrong commit.

## Failing arms (one-line mutants of the RTL at HEAD, unchanged since `8dd0dd8a`; run against the HEAD harness; `mut/<name>/suite_final.log`)

| Mutant | Edit | Fails |
|---|---|---|
| M1 detector off | `ptp_jump_r <= 1'b0` | P1 every size from 21 us, P2 (66 checks) |
| M2 no boundary squash | drop `if (pp_seq_r == '0) pp_run_r <= 1'b0;` | P2a: the squashed close commits integ +75000, rate +51200 (19 checks, P2b/P2c cascade) |
| M3 unconditional squash | drop the `pp_seq_r == '0` condition | P2b: "the closed (pre-step) window commits" (1 check) |
| M4 no abandon | drop `win_valid_r <= 1'b0` | P1 every size, P2a (53 checks) |
| M5 1024 ppm guard off | `guard_hit_w = 1'b0 && ...` | silicon P3 (implausible window committed, integ -94840) and unit U11 (0 discards, ACQUIRE) |
| M6 single tally | `+ 7'(guard_hit_w \| step_hit_w)` | P3 "discards counted = 1 in [2, 2]" |
| M7 guard tightened to 32 ppm | `GUARD_THR_C = 1 << 14` | P4 rate path: a real 40 ppm talker change discarded 3 times, integrator never follows |

M1 passes the compressed unit bench (59/59), because at 128x the 1024 ppm guard still catches every jump there. That is why the step guard's arm lives in the silicon-scale `sim_phc_step.cpp`, and why U11 was added as the 1024 ppm guard's own arm: every jump in U10 is now the step guard's. U10's single-sample "trim held across the step" check became an envelope check. Locked at +80 ppm, that bench's trim already cycles 1499..1579 window to window, and the re-base moves the sampling phase, so one sample landed at +60 against the fixed 48. The envelope check is stricter (every window, inside the pre-step range +-48), and it still rejects the pre-guard kick of 540.

## Validation (all local, Verilator 5.050 pinned, 8 jobs or fewer)

| Gate | Result | Log |
|---|---|---|
| `make -C tb/verilator/mmcm_servo run` | unit 59/59, rails 8/8, phc_step 113/113, exit 0; `suite_tally` 180 checks, `--verdict` 0 | `gate_mmcm_servo.log` |
| `make -C tb/verilator/mmcm_servo_autorepair` | 47/47, exit 0 | `gate_mmcm_servo_autorepair.log` |
| `make -C tb/verilator/milan_dp aclk` (the CRF leg engaging the servo) | media_aclk 139/139; `A_MCSRV_STAT = 0x33` (no false step) | `run_milan_dp_aclk.log` |
| `make -C tb/verilator/milan_dp_render tdm8render` | 150/150 | `run_milan_dp_tdm8render.log` |
| `check_rtl_source_lists.py` | exit 0 | `gates/` |
| `xvlog_gate.py --check` | PASS, `hdl/` 0 findings (ran, not skipped) | `gates/xvlog_gate.log` |
| `check_sv_idiom.py`, `check_cpp_idiom.py`, `lint_rtl.py --check` | exit 0 (lint 90 <= 90) | `gates/` |
| `check_em_dash.py --base 26d855a9`, `docs_check.py` | 0 findings (4 added lines, 3 pages) | `gates/` |
| `gen_module_matrix.py --check`, `git diff --check` | clean | |
| Yosys OOC `KL_mmcm_drp_servo` (same recipe as `ooc.sh`) | base 831 LUT / 789 FF / 140 CARRY4; head 862 / 790 / 150 | `gates/area/` |

Not run here: the full `milan_dp` default suite (the two legs that engage the servo were run), hosted CI, `act`, Vivado implementation timing. The detector's 32-bit subtract on `ptp_now_i` is lighter than `KL_crf_rx`'s existing combinational `w_crf_ts - ptp_now_i` on the same net, but it is not timed. `sim_phc_step` adds about 5.3 min (local) to the `mmcm_servo` suite; the default suite timeout is 1800 s.

## Left for the manager

1. Push, open the PR from `PR-BODY.md` (draft first), run the act replica and the hosted gates, assign the reviewers.
2. PR #540 (`387-gm-step-rebase`, not merged) adds a `GM_LOSS_RECOVERY.md` row: "CRF servo | Keeps its window guard | ... a locked step of about 108 to 524 us passes that guard (#539)". Whichever of the two lands second updates it to say the servo discards the window any PHC step lands in (#539). The talker's own step, below, still reaches it.
3. Two new-issue candidates, measured with this lane's trace modes (`postfix/`). Both are outside #539's acceptance, and neither is fixed here:
   - **The plane's slew is integrated as a rate error.** `+trace_slew_ns=100000` (the owner policy's largest locked slew, at 200 ppm): window error +100.08 ppm, integrator +30.62 -> +80.66 ppm, written rate +30.65 -> +105.68 ppm, LOCKED -> ACQUIRE, 0 discards, written rate still +38.43 ppm (against +30.65) at the fifth close. A slew is not a step, so neither guard can see it. A fix needs either the plane's rate trim or a slew-active signal, which is a design decision.
   - **The talker's step reaches the servo through `KL_crf_rx` `rate_o`.** In a grandmaster change the talker steps too. Its CRF timestamps jump, and the 256-PDU ring carries the jump for 512 ms. `+trace_talker_step_ns=150000`: window error -292.89 ppm, integrator -> -115.82 ppm, ACQUIRE; 100 us gives -66.99 ppm. That is the pre-fix local signature through the other operand. The natural owner is `KL_crf_rx` (restart the rate ring on a timestamp discontinuity).
4. Once #540's gmstep leg is in, it can assert `MCSRV_STAT[15:10]` under a real GM step: a real-wiring check of this guard.
