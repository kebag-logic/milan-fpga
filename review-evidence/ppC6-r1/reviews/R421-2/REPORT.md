[R421] NEGATIVE - exact head 88e0bf82888d6ad83b500425a786814da467610b

# R421-2: external review of processor PR #139 (lane C6, notifications and Identify), round 2

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, issue #80, PR #139.
- Exact head `88e0bf82888d6ad83b500425a786814da467610b`, tree `5cc519fb073c2ab124e6f77b55aafbba9cdc24f1`.
- Range: main `3f3ea56b`..head. Round-2 delta: `5e806296`..head, which is the merge `a011b14` plus `6094928`, `48718d6`, `2e99ab0` and `88e0bf8`.
- The review ran in a detached, isolated clone. Every build and probe ran on `git archive` exports under the packet's `scratch/` directory, never in the clone.
- After the run the clone matches the head exactly: HEAD and tree as above, index modes and blobs equal to the HEAD tree, no untracked or ignored file, no gitlinks (the repository has no submodules). See `receipts/17-clone-verification.txt`.

## Verdict

**NEGATIVE.** One open MINOR (F1), introduced by this round.

Round 2 fixes the round-1 defect, and fixes it well:
- Every IDENTIFY_NOTIFICATION frame is now scheduled T-IDENT-BURST after the previous frame's departure, meaning its last byte to the MAC.
- My round-1 probe, re-run unchanged at this head, no longer finds a short gap (P1 minimum 15,231 / 15,232 clocks over 31 offsets; P2 frame 2 to 3 at least 15,244 clocks).
- The lane's 34 controls are all KILLED.
- R420-1 F2 is fixed.
- The merge keeps both sides.

To hold the gap between bursts, round 2 also added `!gap_r` to the WAITING start (`KL_aecp_notify.sv:794`). The WAITING start is level-sensitive. So a debounced press that begins and ends inside the roughly 150 ms after a burst's third frame left is dropped: no burst is ever sent for it. On the round-1 RTL the same press produced a burst. No lane check covers this window.

Two SUGGESTIONs (S1, S2) do not gate.

## Findings

### F1 [MINOR] A short identify press made in WAITING within T-IDENT-BURST of the previous burst's third frame is lost

- **Lenses:** Conformance, RTL, Robustness, Tests, Docs.
- **Where:**
  - `hdl/aecp/KL_aecp_notify.sv:794`: `I_WAIT: if (btn_q2_r && !gap_r)`, a level sampled each cycle, with no latch.
  - `:806-807`: `gap_r` is set at every departure, including the third frame's.
  - `:791`: `gap_r` clears only when IDENT-BURST expires, at least 150 ms later.
  - `:838-839`: I_HOLD goes to WAITING as soon as the button is low.
  - Banner `:160-170`.
- **Docs that promise otherwise, or say nothing:**
  - `docs/guides/operator.md:50`: "The user presses the identify button: three unsolicited IDENTIFY_NOTIFICATION frames".
  - `docs/guides/integrator.md:103` ("a press sends IDENTIFY_NOTIFICATION three times").
  - `docs/guides/integrator.md:298-305`: "Debounce it yourself". No minimum press length is stated.
  - `docs/architecture/06_aecp_engine.md:781-793` and F06.16 (`:912-913`).
  - `docs/architecture/08_timing.md:30`.
- **Authority:**
  - IEEE 1722.1-2021 Figure 7-142: WAITING goes to IDENTIFY when `identifyButtonPressed`, and IDENTIFY's entry action is txIdentify. See also §7.5.1 and §7.5.1.2.1.
  - Milan §5.4.5.4.
  - #54 acceptance 2: "A trigger emits three byte-exact IDENTIFY_NOTIFICATION unsolicited frames".
  - #80 acceptance 1; #86 acceptance 2.
  - The #80 ruling, condition 4 (the burst graded on the wire with mutants).
- **Evidence** (reviewer arms in `scripts/r421_arms.py`, inserted into a scratch copy of the head's section ID; no RTL change):
  - **R421c** (30 ms press, 2 ms after frame 3), at the head: a short press, then a second 30 ms press made 2 ms after the burst's third frame left. Only the first burst's 3 frames appear; the second press sends nothing (`receipts/05-probe-arms-golden-head.log`).
  - **R421d** (200 ms press), at the head: the same with a 200 ms second press. The next burst goes out 15,301 clocks after frame 3, as documented (same log).
  - **On the round-1 RTL** (the merge `a011b14`'s `hdl/` with the head's tests): R421c produces the second burst, so 6 frames, 367 clocks after frame 3. The loss is new in round 2 (`receipts/13-probe-arms-on-round1-rtl.log`).
  - **Not covered by any lane check:** the reviewer control `p_wait_gap_dropped` removes `!gap_r` from the WAITING start only, and it SURVIVES all 106 section-ID checks (`receipts/03-probes-head-results.json`). The lane control `ident_next_burst_at_once` removes it from both starts and is killed only through the HOLD path (ID3f, ID7r). ID3 grades a second press that is still held when the burst ends; no arm presses in WAITING while `gap_r` runs. With R421d added, the reviewer control is KILLED (next burst 367 clocks after frame 3; `receipts/06-probe-arms-mutants-results.json`).
- **Impact:**
  - When the window is hit, a user's identify request is silently dropped. Example: a second debounced press of about 100 ms, made about 300-450 ms after the first, which a double press can produce.
  - No IDENTIFY_NOTIFICATION leaves, and nothing tells the integrator that a press must outlast the gap.
  - The feature is a SHOULD and defaults to 0, so this is MINOR and not higher. But this round introduced the defect, and the documents describe the opposite behaviour.
  - Related wording: the "latched while txIdentify runs" reading in 06 §7 / F06.16 latches the release, not the press. A second press released before the burst ends is also dropped. That is consistent with an atomic txIdentify, but the text should say so.
- **Required outcome**, either of:
  - **(a), recommended:** latch a press seen in WAITING while `gap_r` runs, and start the burst when the gap ends. This keeps the documented at-least-T-IDENT-BURST gap after a third frame.
  - **(b):** drop the WAITING-start gap (Figure 7-142's immediate txIdentify), and correct the banner, 06 §7, F06.16, F08.1 and integrator §6 statements that the gap also holds between bursts.
  - **Either way:**
    - add section-ID arms for a short press and a long press made in WAITING inside the gap, grading the frame count and the gap;
    - add a recorded control that removes the new latch (for (a)) or restores the gap (for (b)), KILLED by a named check;
    - state the behaviour in 06 §7 / F06.16 and integrator §6, including what happens to a press released before a running burst ends.
- **Verification:**
  - `scripts/run_r421_2.sh <clone> <work> arms r1rtl`: at the new head, R421c and R421d both send a second burst, with the gap the docs state.
  - `python3 tb/pp_top/notify_mutants.py`: the new control is KILLED and the other 34 are unchanged.

### Suggestions (non-blocking)

- **S1 [SUGGESTION] (Tests, Robustness): the departure handshake's `ready` term is never graded.**
  - Where: `hdl/top/protocol_processor_top.sv:4318-4319` clears `busy_r` on `arb_tx_valid_w && arb_tx_eof_w && arb_tx_ready_w`.
  - What survives: the reviewer control `p_busy_clear_without_ready`, which drops `&& arb_tx_ready_w`, SURVIVES all 106 checks. ID7's stalls start mid-frame (byte 6 or later) or between frames, never on the eof beat.
  - What the probe shows: with the bench's existing `stall_tx_at_eof` hook (`tb/pp_top/sim_main.cpp:1303-1306`), arms R421a and R421b stall frame 1's, then frame 2's, last byte for 400 ms.
    - At the head the next gap holds: 15,232 and 15,299 clocks.
    - Under the control the frames bunch to 63 clocks, the round-1 defect class (`receipts/06-probe-arms-mutants-results.json`, `receipts/06-probe-arm-mutant-logs/`).
  - The RTL is correct. Suggested: add an eof-beat stall to ID7 and record this control.
- **S2 [SUGGESTION] (Tests, Docs): the one-tick floors are by inspection only.**
  - The floors are `now_ms_i + 151` (`KL_aecp_notify.sv:746`) and `t0 = now_ms_i + 1` (`:814`). They are what makes each gap at least 150 ms, and the timeout at least 1 s, when one ms tick is far longer than the frame build, as in silicon.
  - On the bench's 100-clock ms the build and serialization (over 100 clocks) hide one tick. So the reviewer controls `p_burst_deadline_150` and `p_t0_same_ms` SURVIVE (`receipts/03-probes-head-results.json`).
  - Suggested: record this as a limit next to section ID's `SLACK` text (`tb/pp_top/README.md:1328-1333`), or grade the deadline arithmetic where the tick is slow (for example `tb/aecp_notify`).

## Lens results (artifact-specific)

### Conformance: UNCLEAN (F1)

- §7.5.1 spacing now holds under contention and MAC stalls. Checked by:
  - ID1-ID7 at head, gaps 15,240-16,147 clocks;
  - my round-1 P1/P2 re-run;
  - R421a/R421b eof-beat stalls.
- Figure 7-142 re-arm (ID2d: 100,265 and 100,300 clocks) and the identifySequenceID per burst are unchanged.
- The command form still answers BAD_ARGUMENTS (ID4).
- At `EN_IDENTIFY_NOTIF_P` = 0 nothing is sent (ID0).
- The WAITING start drops a short press (F1).

### RTL: UNCLEAN (F1)

- `gen_uns_departure` is sound, checked against `KL_pp_tx_arbiter.sv:193-287`:
  - the grant is registered and frame-atomic, and is selected only in A_IDLE, so one frame is in flight;
  - `busy_r` is set on the UNS grant edge, which is the same edge on which the engine enters A_FREE (`KL_aecp_engine.sv:2510, :3649-3653`). So `dep_w` cannot fire at retirement;
  - the ACMP shim is a combinational passthrough, so `arb_tx_*` with ready is the MAC handshake.
- `left_r`, `gap_r`, the BURST and REARM arm order, and `fired_r` latching through I_SEND / I_GAP all behave as documented.
- At 0, `uns_tx_busy_i` is a constant-0 net that nothing reads.
- `ASYNC_REG` is on `btn_q1_r` / `btn_q2_r`.
- Lint is clean: 41 modules, plus `KL_aecp_notify` and the top at parameter 1.
- Defect: F1 (`:794`).

### Robustness: UNCLEAN (F1)

- MAC stalls at a mid-frame byte, between frames and at the eof beat never shorten a gap at head.
- A stall past the timeout does not put two bursts back to back (ID7n-ID7t).
- A fan-out at frame 2's deadline: ID5i-ID5l.
- A lost user action under a short press: F1.

### Tests: UNCLEAN (F1)

- Section ID: 106/106 and ID0: 3/3 at head (`receipts/01`).
- `notify_mutants.py`: 34/34 KILLED, all four goldens PASS (`receipts/02`). This includes:
  - `ident_burst_from_t0`: ID3f, ID5k, ID7i, ID7q, ID7r;
  - `ident_departure_is_retirement` and `ident_departure_unwired`: ID7d, ID7q;
  - `ident_next_burst_at_once`: ID3f, ID7r.
- The head's section ID on the round-1 RTL fails exactly the seven stated checks with the stated values (`receipts/12`).
- d3: the receipts name all 83 driver mutants KILLED, none missing (cross-checked against `d3_mutants.MUTANTS`).
- `tb/aecp_notify` 10/10; UPC map gate PASS.
- Gaps: F1 (the WAITING window is not graded); S1 and S2.

### Docs: UNCLEAN (F1)

- The round-1 claims are corrected: banner, F08.1, 09 §8.3, 06 §7, integrator §6, README section ID, and the ID6 rename.
- R420-1 F2 is fixed in `docs/guides/hdl-engineer.md:64` and `hdl/README.md:24-28`. They are consistent with integrator §1 (`u_notify.gen_ident.btn_q1_r`; `u_notify` is a top-level instance) and 02 §2 rule 3.
- The README's equivalence statement (`tb/pp_top/README.md:1386-1389`) holds at this head: I re-proved it with round 2's third unread input deleted, 6,365 of 6,365 cells (`receipts/11`).
- `make check` rc 0; `gen_matrix.py --check` rc 0; `git diff --check` clean on both ranges.
- Defect: the operator and integrator guides and 06 §7 promise a burst per press (F1).

## The merge `a011b14`

- **Both sides kept:**
  - `git diff <merge-base> 3f3ea56b` and `git diff 5e806296 a011b14` have identical per-file stats, except one resolved line in `tb/pp_top/sim_main.cpp`: the `one_section` union now carries all eight flags.
  - `git diff 0451d83d 5e806296` and `git diff 3f3ea56b a011b14` are identical per file.
- `.gitattributes`, `.github/`, `scripts/` and `syn/` are byte-identical to main.
- `tb/pp_top/Makefile` keeps `maap-internal` and adds `identify-build identify`. The README keeps MP and AC, then Lane C6.
- Main did not touch `gen_ucode.py`, `KL_aecp_engine.sv` or `pp_pkg.sv`. The ROM images are build products, regenerated by the Makefile; the UPC map gate passes.

## Ruling conditions and issue acceptance at this head

- **No top port or parameter change in round 2.** The only port and parameter lines in main..head are round 1's authorized `EN_IDENTIFY_NOTIF_P` and `identify_button_i`.
- **`uns_tx_busy_i`** is an internal `KL_aecp_notify` port, within the STOP boundary per the newest ruling on #80.
- **Condition 1** (default 0, zero area): met.
  - At 0 the top's FF, CARRY4, RAM and DSP equal main's (author yosys receipts: 30,454 FF, 2,317 CARRY4).
  - Notify's equivalence is re-proven at this head.
  - The cost at 1 is +79 FF and +22 CARRY4. LUT is mapper variance, as now stated.
- **Condition 2** (synchronized, debounce duty stated): met. 2FF with `ASYNC_REG`, and the integrator's false-path / max-delay duty is stated.
- **Condition 3** (parent-visible list): met, pending the manager's parent bank.
  - `parent-adoption-c4c6-ea3fb388.patch` ties `identify_button_i` to 0 and binds `EN_IDENTIFY_NOTIF_P` to 0.
  - It carries both mutation-driver dispositions.
- **Condition 4** (both settings graded): met at 0. At 1, met except F1.
- **#54:** 1, 3 and 4 met. 2 is not met in full (F1: a trigger in the WAITING gap emits nothing).
- **#58:** 1, 2 and 3 met (arm 2). Round 2 changes nothing here; the NP controls are KILLED at head. `Closes #58` is supported.
- **#80:** 2, 3 and 4 met. 1 is met except F1.
- **#86:** 1, 3 and 4 met. 2 is met except F1.
- **Closing:** `Closes #54`, `#80` and `#86` should wait for F1.

## Prior public findings on this PR (resolved or retained at this head; read after my verdict and ledger were written)

| Finding | State at 88e0bf82 | Evidence |
|---|---|---|
| R421-1 F1 / R420-1 F1 (MINOR, the same defect: frames scheduled from t0 bunch under contention or a stall) | **RESOLVED.** Option (a), with departure taken as the last byte to the MAC, which is stricter than retirement | My round-1 probe re-run unchanged (`receipts/16`): P1 minimum gaps 15,231 / 15,232, P2 2->3 at least 15,244. ID5i-l and ID7. `ident_burst_from_t0` KILLED. Banner, F08.1, 09, 06, integrator §6 and README corrected; ID6 renamed |
| R420-1 F2 (MINOR, HDL engineer contract says no CDC inside) | **RESOLVED** | `hdl-engineer.md:64`, `hdl/README.md:24-28` |
| R421-1 S1 (release and press inside a burst) | **Resolved as a stated reading** (06 §7, F06.16; ID3). Its "latched" wording is folded into F1's docs outcome | above |
| R421-1 S2 / R420-1 S2 (synchroniser marking and constraint) | **RESOLVED** | `KL_aecp_notify.sv:712-713`, integrator §1 |
| R421-1 S3 (`gstri_r` for SINFO) | **RESOLVED** (the reason is now an RTL comment) | `KL_aecp_engine.sv:2760-2761` |
| R421-1 S4 / R420-1 S3 (LUT figures) | **RESOLVED** (flow stated, FF/CARRY as the cost) | PR body, round-2 validation |
| R420-1 S1 (`!core_arm_w`, `gen_r`, second flop not exercised) | **Retained, recorded** with reasons in `tb/pp_top/README.md:1501-1509`. Acceptable for a SUGGESTION | |
| R420-1 S4 (GET_COUNTERS limiter one tick) | **Retained, recorded** (pre-existing shared limiter) | `tb/pp_top/README.md` ST2 |

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | IEEE 1722.1-2021 §7.4.39, §7.5.1, Figure 7-142; Milan §5.4.5.4; #54/#58/#80/#86 acceptance; #80 rulings; `KL_aecp_notify.sv` identify block; receipts 01, 05, 13, 16 | R421-2 | 88e0bf82888d6ad83b500425a786814da467610b |
| RTL | UNCLEAN (F1) | `KL_aecp_notify.sv:687-868`, `protocol_processor_top.sv:3223, 3870, 4305-4325`, `KL_pp_tx_arbiter.sv:193-287`, `KL_aecp_engine.sv:2503-2510, 2757-2762, 3644-3653`; lint receipts 07/08; equivalence receipt 11 | R421-2 | 88e0bf82888d6ad83b500425a786814da467610b |
| Robustness | UNCLEAN (F1) | MAC stalls mid-frame, between frames and at eof (ID7, R421a/b); fan-out at frame 2 (ID5i, P1); stall past timeout (ID7n); short press in the gap (R421c); receipts 03, 05, 06, 16 | R421-2 | 88e0bf82888d6ad83b500425a786814da467610b |
| Tests | UNCLEAN (F1) | `tb/pp_top/notify_phases.hpp` (ID, ID0), `notify_mutants.py` (34 KILLED), six reviewer probe controls, two arm controls, the head's tests on round-1 RTL, the d3 receipts against the driver list, `tb/aecp_notify`; receipts 01-06, 12, 13, 15 | R421-2 | 88e0bf82888d6ad83b500425a786814da467610b |
| Docs | UNCLEAN (F1) | 06 §7 / F06.16, 08 F08.1, 09 §8.3, 02 §2, integrator §1/§2/§6, operator row, hdl-engineer CDC row, `hdl/README.md`, `tb/pp_top/README.md` sections ID / ID0 / mutation record, PR body round 2; `make check` (receipt 10) | R421-2 | 88e0bf82888d6ad83b500425a786814da467610b |

## What I executed

All runs used Verilator 5.050 (`receipts/00-tool-identity.txt`), with builds capped at eight parallel jobs, in the foreground, on `git archive` exports. `scripts/run_r421_2.sh` reproduces every step; I validated its `equiv` and `arms` steps after the fact.

- **Section ID** (third build) at head: 106/106; ID0 3/3.
- **`notify_mutants.py`**, full: 34/34 KILLED, 4 goldens PASS.
- **Six reviewer probe controls** (`scripts/r421_probes.py`):
  - KILLED: `p_hold_gap_dropped` (ID3f, ID7r) and `p_busy_clear_at_sof` (ID7d).
  - SURVIVED: `p_wait_gap_dropped`, `p_busy_clear_without_ready`, `p_burst_deadline_150` and `p_t0_same_ms`.
- **Reviewer arms R421a-d** at head: R421c fails, as F1 states; the others pass. The two targeted controls run against the arms without R421c: both KILLED.
- **The head's section ID on the round-1 RTL:** 7 of 106 fail, as the author states. The arms on the round-1 RTL: R421c sends a second burst.
- **R421-1's probe (P1, P2)** re-run unchanged at head.
- **`KL_aecp_notify` equivalence** at 0 against main: 6,365/6,365 proven.
- **Gates:** `lint_hdl.sh` rc 0, plus lint at parameter 1; `make check` rc 0; `gen_matrix.py --check` rc 0; `check_upc_map.py` PASS; `tb/aecp_notify` 10/10; `git diff --check` on both ranges.
- **Hosted checks** at the exact head, read only (`receipts/09`):
  - `docs-gates` and `portability`: success in both workflow runs.
  - `suites`: still in progress in both runs at 11:02Z, so it is neither a pass nor a failure here.

## Real limits

- **Simulator path.** The Verilator path named in the assignment does not exist on this host. I used `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator`, version 5.050. All 226 `pinned-tool-bin/verilator` wrappers on the host are byte-identical (sha256 `905795b9…`), and the binary's hash is recorded. The system Verilator (5.052) was not used.
- **Not run by me:**
  - the full `run_suites.sh`;
  - the whole-top yosys synthesis;
  - the parent consumer and donor banks;
  - act or hosted reruns.

  For these I rely on the author's round-2 receipts (33 suites, 1,018,084 checks, 0 failing; yosys stats at 0 and 1, which agree with the stated FF and CARRY4 deltas) and on the manager's banks.
- **Manager evidence.** I found no public manager bank comment for this head on PR #139 or issue #80 when I queried. The pinned evidence commit `2c532827` carries only round 1. The round-2 author packet is on the public `ppC6-review-evidence` branch (head `6f472b26`), which I read only under `author-r2/`.
- **Probe arms are reviewer-owned and disposable.** The first draft of R421a released the button before the synchroniser could see it (a premise failure). It was corrected before any result above was used.
- **No hardware**, no physical calibration, and no silicon timing. The S2 floors are by inspection.
- **I did not read R420-2.**

## Pending manager duties

- The parent consumer bank (16 commands) and the donor bank at milan-fpga dev `ea3fb388`, with the combined C4 + C6 patch (`parent-adoption-c4c6-ea3fb388.patch`).
- The hosted `suites` jobs at this head (in progress when I queried).
- The final current-dev candidate at the merge turn (source base `3f3ea56b`, live dev `ea3fb388`).
- The round-3 assignment for F1. Closing #54, #80 and #86 only once F1 is resolved.

## Receipts

The files are listed in `MANIFEST.sha256`:
- `receipts/00`-`17`;
- the per-control logs in `receipts/03-probe-logs/` and `receipts/06-probe-arm-mutant-logs/`;
- the scripts: `run_r421_2.sh`, `r421_probes.py`, `r421_arms.py`, `r421_ident_probe.hpp`, `equiv_notify_r2.ys` and `verilator-j8.sh`.

R421-2 FINISHED
