[R485] NEGATIVE - exact head d0e29f6dda6f04f3ace1dbb395f57379e58cacaf

# R485-1: external review of #656 / PR #662

- **Role:** external, cleared-context independent reviewer.
- **Head:** exact head `d0e29f6dda6f04f3ace1dbb395f57379e58cacaf`, tree `289f09d8c7151617ffb019f49b5c972924e4fedd`.
- **Lane diff:** `c0280fc0..d0e29f6d`. It touches 2 files, `tb/verilator/milan_dp/sim_ax1x1gptp.cpp` and `tb/verilator/milan_dp/README.md`, with +26/-7 lines (`receipts/lane.diff`).

## Verdict in one paragraph

The TEST-DEFECT ruling holds. I recomputed the mechanism from the RTL and harness constants, and it is exact. In all three of my concurrent physical-leg runs, every window figure reproduces the published evidence:

- the head gives 139 / 0 + 6 / 0 + 20 / 0 + 14 / 0;
- C1 (A2-a removed, new pacing) gives 139 / 5, with 8 cumulative errors;
- C2 (parent pacing, head RTL) gives 139 / 3, with 5 cumulative errors.

Pacing the peer on the modeled audio clock is a faithful model of a peer that follows the DUT's INTERNAL media clock. The corrected checks still catch a DUT-side grid-rate mismatch (C1). The check code, windows, timers and the 139 + 40 count are unchanged.

Every tree artifact is clean. The verdict is NEGATIVE for one reason only: one open MINOR (F2). The PR body's #396 limitation states the slip rate as "about 0.51/s per 10 ppm". The correct rate is 0.48/s per 10 ppm, or 0.51/s at the plan's 10.64 ppm. That is a numeric claim, so under the residue rule it is not purely wording. **The fix is a PR-body edit and needs no new commit.**

## Findings

### F2 - MINOR - Docs - PR #662 body, "Known limitations / out of scope", bullet "INTERNAL against an asynchronous talker" (body lines 195-199 as fetched)

- **Authority/evidence:**
  - The body says the leg "still slips about 0.51/s per 10 ppm on the loopback path".
  - The slip rate is 48,000 x offset, per fed pair. That gives 0.480 events/s per 10 ppm, and 0.5107/s at the plan's 10.64 ppm (`receipts/receipts_rate.txt`; `scripts/rate_recompute.py`).
  - 0.51/s is the figure `docs/reference/REGISTER_MAP.md:2002` gives for the 10.64 ppm plan **per fed pair**, not per 10 ppm.
  - The same bullet also says "before A2-a the slip sat at the TDM junction". That holds for a talker at the nominal packet-grid rate, which is this bench's old axis-paced talker; the PR's own Mechanism section states it correctly in that context. Before A2-a, an arbitrary asynchronous talker also slipped on the loopback path, at its own offset from the nominal NCO.
  - (6) asks whether the #396 consequence is stated correctly. Its substance is correct:
    - At INTERNAL, the loopback path slips against any talker that is off the plan clock.
    - The slip is counted on `SLIP_LB`.
    - A zero-glitch #396 run through the lane needs the clocks followed.
  - The coefficient and the generalisation are not correct.
- **Impact:** a reader sizing #396 from the PR's limitation scales the slip rate 6 % high. The bullet also implies that pre-A2-a INTERNAL never slipped on loopback, which is untrue for an off-nominal talker. No test, code, measurement or in-tree text is affected: README and the code comment state 10.64 ppm / 1.958 s correctly.
- **Required outcome:** the PR body states the loopback slip as about 0.48/s per 10 ppm per fed pair, or 0.51/s at plan A's 10.64 ppm. It qualifies the pre-A2-a clause to "for a talker at the nominal packet-grid rate (this bench's old pacing)", or drops it.
- **Verification:** a re-read of the edited PR body at the same head. No tree change is needed, so the other four lenses' coverage at this head is unaffected.

### F1 - SUGGESTION - Tests, Robustness - `tb/verilator/milan_dp_gptp/verify_abort.py:76`

- **Authority/evidence:**
  - The exact pin `windows[-1] == ("160", "0", "0")` counts RX PDU completions in a 20 ms (1,000,000-cycle) window.
  - At the new period of 6,250 + 26/391 cycles (= 6,250 + 52/782 = 6,250.066496), the window holds 159.998298 periods. So 159 occurs for 10.64 cycles of every period: 0.1702 % of start phases. The PR's 0.17 % is right.
  - The model has no randomness, so the window phase is deterministic.
  - Probe (`receipts/pin-probe.diff`, print-only plus a 20,000-cycle post-window run): it logs every RX AAF completion.
    - For `--no-tx-control` and both `--stop-tx-control` windows, the count is 160.
    - The first completion is 5,926/5,940 cycles after the window start. The last is 313/299 cycles before the window end.
    - The measured 159-band is 11 cycles wide. The windows sit 299-313 cycles from it when shifted earlier, and about 5,927 cycles from it when shifted later (`receipts/pin_margin.*.txt`).
  - With the old 6,250-cycle period the count was 160 at every phase.
- **Impact:** none at this head; the check passes deterministically. A future harness change that moves the window start about 300 cycles earlier relative to the PDU grid would fail the pin loudly, as a false failure; it would never produce a false pass. The PR discloses the exposure. This is not a defect of this PR and not residue: it is a test-robustness option.
- **Suggested outcome:** accept 159-160 for the RX count, or derive the expected count from the pacing constants. The TX = 0 and samples = 0 parts must stay exact.
- **Verification:** the existing `--no-tx-control` / `--stop-tx-control` accounting stays 20 / 0, and a planted window-phase shift does not trip it.

### RES-1 - RESIDUE (pre-existing, not introduced or relied on by this PR) - Docs - `tb/verilator/milan_dp/README.md:297`, `tb/verilator/milan_dp_gptp/README.md:7`, `:9`

- **Evidence:** these lines say 137 physical checks and 177 total. The leg counts 139 physical and 179 total: my head run, the published head driver log, and the nightly 37184411090 log all show `checks: 139`.
- **This PR:** it does not introduce these lines. Its own text uses 139 / 179 and does not rely on them.
- **Exact fix:**
  - `milan_dp/README.md:297`: "The physical harness contributes 139 checks."
  - `milan_dp_gptp/README.md:7`: "The normal total is 179 checks: 139 physical, 40 accounting."
  - `milan_dp_gptp/README.md:9`: "Extended mode runs the physical harness alone, with 139 checks." Confirm the extended count when that mode is next run.

No prior public review finding exists on this PR at this head. The PR carries only the two review-start comments, and the PR review and review-comment lists are empty, so nothing is carried forward.

## Focus items

### (1) Mechanism, recomputed from RTL and harness constants

| Quantity | Source at the head | Value |
|---|---|---|
| Axis clock | `tb/verilator/nvm_capture_cpu/recipe.py` CPU_HZ via `milan_dp/Makefile:425-426` | 50,000,000 Hz |
| Audio rising edges | `sim_ax1x1gptp.cpp:325-329`: +782 every half axis cycle, toggle at 1591, so 782/1591 rising edges per axis cycle | 24,575,738.529 Hz |
| FSYNC | 512 audio edges (`sim_ax1x1gptp.cpp:765` checks it in-harness) | 47,999.489315 Hz, -10.6393 ppm |
| Drain under A2-a | `milan_datapath.sv:5905`: `mga_sel_w = int_clk_selected_r \| follow_sel_r`, so the aligner is engaged at INTERNAL. `:5932`: `mnco_servo_en_w = mga_sel_w`. `:787-788`: NCO trim. `KL_media_grid_align.sv:117-118, 290-298`: the PI integrator gives zero steady-state frequency error. `:1302`: `KL_chan_map_capture.tick_i = media_tick_p` | pop rate = FSYNC |
| Old push | parent `kAafPeriod = kHz * 6 / 48000` = 6,250 cycles | 48,000 samples/s, +10.6394 ppm |
| Queue over-fill | `KL_chan_map_capture.sv:186-219`: depth 8, push-when-full drops the oldest and counts it on `lb_skip_cnt_o` | 0.510685 events/s per pair |
| Slip period | 1 / 0.510685 | 1.958154 s; the trace gives 1.958146 s, quantised |
| Trim | `KL_media_nco.sv:149-163`: 1/16 ppm per u LSB | plan needs -170.23; trace shows -170 |
| New push | `kAafAudioEdges = 6 * 512` = 2,443,776/391 cycles | equals FSYNC exactly; 0 events/s excess |

- Each slip is one event per pair. All four pairs slip together, so `SLIP_LB`'s skip half steps by 4. This matches `REGISTER_MAP.md:1867`'s unit, and the "climbing | static" row (`:2003`) reads "the upstream talker's clock is not this media clock".
- History confirms the first bad commit:
  - `git log -S` finds `d676ecfd4` as the only commit introducing the A2-a select.
  - It is an ancestor of `bbf704ec` and not of `1269cdaf`.
  - The published pair logs give `0b074298` 139 / 0 + 40 / 0 and `d676ecfd` 139 / 3.
  - The nightly 37184411090 is `rtl-full`, scheduled, at `241f9184`. Its Physical gPTP job ended in failure.
- Acceptance 1 is met.

### (2) Faithfulness of the new peer model

- A Milan peer that follows the DUT's INTERNAL media clock produces samples at the DUT's media rate: here plan A, 47,999.489 Hz in the peer's gPTP time. The peer's gPTP time is axis-locked in this model (`Peer clock ... no drift`).
- Pacing on 3,072 audio rising edges per PDU is exactly that rate, with no long-term drift. Deferral by PTP reservations or `rx_busy` delays one PDU without moving the grid, because `next_audio_edge += kAafAudioEdges` (`sim_ax1x1gptp.cpp:500-505`).
- After reset, `configure()` re-arms the pacing from the live edge count (`:743`), so no catch-up burst follows.
- This is the same cadence `obj_aclk`'s ring phases use (`sim_aclk.cpp:816-852`: 12,500 + 52/391 at 100 MHz, the same 3,072-edge PDU).
- It is the case in which the queue's documented contract is "With locked clocks both stay at ZERO" (`KL_chan_map_capture.sv:219-220`), so zero dup/gap is the correct expectation only there.
- **It does not hide a defect the leg is meant to catch.** The leg grades order through gPTP acquisition, loss, recovery, backpressure and reset. None of these moves the media clock at INTERNAL. A DUT whose grid leaves the audio clock is still caught (C1).
- **Diff check:**
  - Only the header comment changes, plus the pacing constant (`:79-89`), the member rename (`:187`), the `schedule()` condition and step (`:500-504`), and the `configure()` initialiser (`:743`).
  - `grade_audio`, `audio_window`, `loss_recovery`, `report`, every window deadline, timer, `audio_warm_until`, and every check label and count are untouched.
  - `verify_abort.py` is untouched.

### (3) Controls

| Run (this round, pinned 5.050, concurrent) | Binary sha256 | Physical | Ordering errors | Accounting | Wall |
|---|---|---|---|---|---|
| head | `e9052849...` | 139 / 0, rc 0 | 0 | 6 / 0, 20 / 0, 14 / 0 | 3,438 s |
| C1: A2-a removed (`mga_sel_w = follow_sel_r`), new pacing | `3b035d43...` | 139 / 5, rc 2 | 1 + 3 + 1 + 1 windows, 8 cumulative | not reached | 3,415 s |
| C2: parent harness, head RTL | `4cd8a8c9...` | 139 / 3, rc 2 | 2 + 2 windows, 5 cumulative | not reached | 3,406 s |

- Every `AUDIO result` line of each run matches the published `head-driver-milan_dp_gptp.log`, `ctl-fix-noA2a.log` and `dev-c0280fc0.log` respectively.
- **The corrected checks detect a DUT-side rate mismatch.** C1 removes the INTERNAL alignment, so the NCO pops at nominal 48 kHz against a 47,999.489 Hz push. The queue then under-runs and dups. That fails 4 windows and the cumulative check.
- They also detect a talker off the DUT's media clock (C2).
- **Sensitivity limit (estimate, not measured):** the queue keeps about 2 events of margin and the epochs last about 10.7 s and 6.2 s. So a steady DUT-side grid error below a few ppm may not surface as an order error in this leg. Rate accuracy is graded elsewhere (the `[CRF] |ppm| < 0.5` check that the `sim_aclk.cpp:816-852` banner names), and the old pacing graded no finer.

### (4) The 160-PDU pin

See F1. The 0.17 % figure is right, the window phase is deterministic, and the measured margin is 299-313 cycles. The pin is not a defect of this PR and not residue: it is a SUGGESTION.

### (5) Docs

- **`milan_dp/README.md:173`** (model row) and **`:200-207`** (paragraph) are accurate against the RTL and harness, checked sentence by sentence:
  - 3,072 rising edges per PDU;
  - A2-a holds the packet grid on FSYNC at INTERNAL;
  - the queue drains on the packet grid;
  - an axis-paced talker runs 10.64 ppm fast;
  - one sample (one event per pair) is dropped every 1.958 s, counted on `SLIP_LB`.
- **Code comments** at `sim_ax1x1gptp.cpp:22-25` and `:82-88` are also accurate.
- **The stale 137/177 counts** are graded RES-1.

### (6) The #396 consequence

Its substance is stated correctly, and changing it is not this PR's scope. The coefficient and one clause are wrong: see F2.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #656 acceptance 1-3 against the bisect pair logs and `git log -S` / ancestry. Acceptance 2's planted controls: my C1 and C2 reruns. Acceptance 3 local: my head run, 139 / 0 + 40 / 0. The hosted half is pending, and "Relates to" is correct. `KL_chan_map_capture.sv:173-220`, the honest-slip contract | R485-1 | `d0e29f6d` |
| RTL | CLEAN | No RTL in the diff. The mechanism was checked against `milan_datapath.sv:750-790`, `:1234-1306`, `:5886-5932`, `KL_media_grid_align.sv:10-45, 117-118, 282-298`, `KL_media_nco.sv:85-163` and `KL_chan_map_capture.sv:173-220` | R485-1 | `d0e29f6d` |
| Robustness | CLEAN (F1 SUGGESTION only) | `sim_ax1x1gptp.cpp:483-505` (deferral keeps the grid), `:743` (reset re-arm), `:839-896` (windows unchanged). The `verify_abort.py:76` pin phase was measured by probe (`receipts/pin_margin.*`) | R485-1 | `d0e29f6d` |
| Tests | CLEAN | `receipts/run.head.log`, `run.c1.log`, `run.c2.log` (three distinct binaries); the check code unchanged by diff (`receipts/lane.diff`); `test_clock_contract.py` rc 0; `check_cpp_idiom`, `measure_naming --check`, `check_hygiene --check` rc 0 (`receipts/receipts_static.txt`) | R485-1 | `d0e29f6d` |
| Docs | UNCLEAN (F2 MINOR open; RES-1 residue) | `milan_dp/README.md:158-207`, `:290-300`; `milan_dp_gptp/README.md:1-15`; `REGISTER_MAP.md:1867-2004`; `MEDIA_CLOCK_FOLLOWING.md:1133-1148, 1504-1515`; the PR #662 body; `docs_check`, `check_doc_style`, `check_doc_paths` rc 0 | R485-1 | `d0e29f6d` (the PR body as fetched during the round) |

## Real limits

- **Simulation only.** Physical calibration was NOT RUN. No hardware or bench. Field skips are not hardware proof.
- **Not run:**
  - the full parent, PP, gPTP, Yosys and builder banks (not allowed);
  - `check_em_dash.py`: its pinned markdown renderer is not installed here, and installing it is not allowed. A literal search finds 0 em-dash characters in the lane diff;
  - the extended mode;
  - Docker/act.
- **Probe copies.** The three control runs and the pin probe ran in disposable copies under the packet's scratch directory. The review clone was never built in. Afterwards its HEAD, tree, index tree and work tree equal the exact head, there are 0 untracked files, and the submodule gitlinks match (`receipts/clone-integrity.txt`). `external` is uninitialised, as it was at the start; this suite does not use it.
- **Hosted evidence at the exact head, observed but not owned:**
  - The Physical gPTP context **was skipped** on the PR event (nightly and manual only).
  - Yosys shards 0-3, `verilator-lint`, `full-ci-gate`, `bdd-conformance`, `wire-accountability`, `changes` and `docs-check-no-git` succeeded.
  - Verilator shards 0-4, `yosys-elaboration`, `elaborate` and `docs-check` were in progress when observed.
- **The detection-sensitivity figure in (3) is an estimate.** No sweep of DUT-side ppm offsets was run.

## Pending manager duties

- Carry F2 to the executor: a PR-body edit only. Then a re-read of the edited body at this head can bank Docs.
- Carry RES-1 to the residue checklist.
- Record F1 as optional.
- The hosted Physical gPTP half of acceptance 3 needs a dispatch at a pushed head or the first post-merge nightly. Keep "Relates to #656" until then.
- Exact-head `verilator-suites` and `yosys-portability` must complete.
- Build and validate the current-dev candidate: source base `c0280fc0`, live dev `506d91db`.
- The internal positive (R484) and post-merge containment are still owed.

## Receipts

All receipts are listed in `MANIFEST.sha256`:

- `receipts/`: the lane diff; the three run logs and rc files; the C1 plant diff and C2 stat; the pin probe diff, its logs and the margin outputs; the rate recomputation; static gate outputs; clone integrity.
- `scripts/`: `rate_recompute.py`, `pin_margin.py`, `run_controls.sh`.

R485-1 FINISHED
