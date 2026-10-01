[R420] NEGATIVE - exact head 88e0bf82888d6ad83b500425a786814da467610b

# R420-2: internal independent review of processor PR #139 (lane C6, issue #80), round 2

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #139. Closes #54, #58, #80 and #86.
- Exact head `88e0bf82888d6ad83b500425a786814da467610b`, tree `5cc519fb073c2ab124e6f77b55aafbba9cdc24f1`.
- Source base: processor main `3f3ea56ba61829718a6a288600ab4fdac73aa5ba`.
- Round-1 head: `5e806296`. Round 2 adds five commits on it:
  - `a011b14`: the merge of main `3f3ea56b` (#136, #135, #137);
  - `6094928`: the burst schedule;
  - `48718d6`: the CDC rule;
  - `2e99ab0`: the suggestions;
  - `88e0bf8`: the parent idiom gates.
- Reviewer: [R420], internal role, cleared context, own detached clone `$REVIEWS/r420-2-ppC6`. Round R420-2.

## Verdict

**NEGATIVE: one MINOR finding is open (R420-2-F1).** It is new in round 2. The fix for R420-1 F1 added a second guard, the `!gap_r` on the WAITING start. That guard silently drops an identify press made shortly after a burst. No check covers the guard: a control that removes it alone survives all 106 section-ID checks. And the integrator contract says the opposite of what the guard does.

Everything else this round was asked to deliver checks out:

- Both round-1 findings are resolved at this head, and so is R421-1 F1 (section 3):
  - every IDENTIFY_NOTIFICATION frame is now due T-IDENT-BURST after the previous frame left;
  - my own sweeps of the R420-1 and R421-1 shapes find no gap under 15,000 clocks (T-IDENT-BURST);
  - the HDL contract names the synchroniser.
- The merge keeps both sides.
- `88e0bf8` changes no planted string and no check message.
- No top port or parameter changed in round 2.
- Every suite and campaign I re-ran returned rc 0 and matched the author's figures.

## 1. How the task was reconstructed

Public sources, in this order:

1. **Process.** The processor repository has no `AGENTS.md` or `CONTRIBUTING.md`. I read the parent milan-fpga `AGENTS.md` and `CONTRIBUTING.md` at dev `ea3fb388`, then the processor `README.md` and `docs/README.md` (conventions, single-source rules, ID registries).
2. **Frozen acceptance and scope decisions:**
   - the bodies of #80 (acceptance 1-4), #54 (1-4), #58 (1-3) and #86 (1-4);
   - on #80: the assignment 5915639621, the STOP 5915752457 and its ruling 5915765717 (four conditions);
   - the round-2 assignment 5924910356, which names merge items 1-4 and a STOP before any further port, parameter or parent-visible change;
   - the manager ruling 5929618372: the internal `uns_tx_busy_i` is inside the STOP boundary.
3. **Authorities, as cited by the diff and the issues:**
   - IEEE 1722.1-2021 §7.4.39, §7.5.1, §7.5.1.2.1, §7.5.1.3 / Figure 7-142;
   - Milan §5.4.5.1-§5.4.5.4;
   - 01 F01.5, 02 §2, 03 §4/§5, 06 §7 / F06.16, 08 F08.1, 09 §8.3, and the three guides.
4. **Diff and history.**
   - `git diff 3f3ea56b..88e0bf82` (27 files, +2,862/-102).
   - The round-2 delta `5e806296..88e0bf82` and each commit.
   - The merge was checked against both parents (section 4.1).
5. **Public evidence** at kebag-logic/milan-fpga branch `ppC6-review-evidence`:
   - `2c532827` (round 1) and `6f472b26` (round-2 author packet `review-evidence/ppC6-r1/author-r2`). All 46 author-r2 files match their `MANIFEST.json` `published_sha256` (`receipts/evidence-manifest-check.txt`).
   - In that packet I read `HANDOFF.md` §5 and its parent-visible list, `PR-BODY.md`, both parent patches and the receipts.
   - The manager's evidence comment on #139 (5921694276, round 1), and the round-2 review-start notice.

Prior public review findings (R420-1 5921785256, R421-1 5921513647) were read only after my own pass over the diff, my probes and my draft finding were complete. They are resolved or retained in section 3.

## 2. Findings

### R420-2-F1 MINOR: a press made shortly after a burst is silently dropped; the guard that drops it is untested, and the integrator contract says the opposite

- **Lenses:** Conformance, RTL, Robustness, Tests, Docs.

- **Where:**
  - `hdl/aecp/KL_aecp_notify.sv:794`: `I_WAIT: if (btn_q2_r && !gap_r) begin`. WAITING ignores the button while the T-IDENT-BURST gap after a burst's third frame runs. The gap is set at `:807` and cleared at `:791`. Nothing latches the press, unlike `rel_r` inside a burst (`:801`, `:831`).
  - `hdl/aecp/KL_aecp_notify.sv:162-170` (banner).
  - `docs/guides/integrator.md:298-304` (§6): "`identify_button_i` is IEEE 1722.1-2021 Figure 7-142's `identifyButtonPressed` ... a new press after a release starts another burst `T-IDENT-BURST` after the running one ends".
  - `docs/architecture/06_aecp_engine.md:786-793` (§7) and `docs/architecture/08_timing.md:30` (F08.1 T-IDENT-BURST row). Both say the next burst comes "no sooner" than T-IDENT-BURST after the third frame. Neither says that a press can be lost.
  - `tb/pp_top/README.md` section ID and its mutation record (`:1455-1509`). No check presses on the WAITING path inside the gap, and no control covers the WAIT guard alone.

- **Authority:**
  - IEEE 1722.1-2021 Figure 7-142: WAITING moves to IDENTIFY on `identifyButtonPressed`, and IDENTIFY runs txIdentify. The 150 ms spacing of §7.5.1 lies between the transmissions inside one txIdentify. After the third frame the machine answers a new press in WAITING at once.
  - The lane's documented contract, cited above.
  - #54 acceptance 2: "A trigger emits three byte-exact IDENTIFY_NOTIFICATION unsolicited frames".

- **Evidence:** `scripts/r420_probes.py`, which builds an isolated copy of the third build. In the default probe run (`receipts/probes/`), the head is used with no RTL change, plus one reviewer bench function appended to section ID.
  - **RP2:** a short press, then an 80 ms press that starts 20 ms after the burst's third frame left. Result: **0 frames** (`head_with_probe.log`: "an 80 ms press 20 ms after the third frame left: 0 frames after it"). In round 1 this press started a burst. The `!gap_r` guard on the WAITING start is new in `6094928`.
  - **RP1:** the same, but the second press is held 300 ms. The second burst starts 15,301 clocks after the third frame. This is the documented behaviour, and RP1a/RP1b pass at the head.
  - **Control `wait_ignores_gap`:** only `:794`'s `&& !gap_r` is dropped; the HOLD guard stays.
    - It **survives all 106 section-ID checks** (`wait_ignores_gap.log`: 106 checks, 0 failures).
    - Under that control, RP1 puts the second burst 5,167 clocks (about 52 ms) after the third frame, and RP1b fails (`wait_ignores_gap_with_probe.log`). RP2 then answers with 3 frames.
  - **Why the lane's own control does not cover it:** `ident_next_burst_at_once` drops both guards at once. Its named checks, ID3f and ID7r, reach only the HOLD path: a press inside a burst, or a button held through the timeout.
  - **Control `hold_ignores_gap`:** the HOLD guard dropped alone. It is KILLED by ID3f and ID7r, at 166 clocks.

- **Impact:**
  - Up to about 151 ms after every burst (T-IDENT-BURST plus one tick and the timer sweep), a press that also ends inside that window never produces an IDENTIFY_NOTIFICATION. Nothing reports the loss. This contradicts the integrator guide's statement that a new press after a release starts another burst, and the guide's equation of the pin with Figure 7-142's `identifyButtonPressed`.
  - The guard that causes this is unverified in either direction: a regression that removes it passes the whole suite.
  - Severity: the feature is a Milan "should", the parameter defaults to 0, and the window is short. That makes this MINOR, not higher.

- **Required outcome:** choose one of the following, applied consistently in RTL, docs and tests:
  - (a) WAITING latches a press seen while the gap runs, as `rel_r` does inside a burst, and starts the burst when the gap ends. No press is then lost, and the gap still holds.
  - (b) The behaviour stays, stated as a deliberate reading in integrator guide §6, 06 §7 / F06.16 and F08.1. The statement must say that a press which starts and ends within T-IDENT-BURST after a burst's third frame is not seen, and that a press must outlast that window.

  In either case:
  - a section-ID check presses on the WAITING path inside the gap;
  - a control that drops only `:794`'s `&& !gap_r` (as `wait_ignores_gap` does) is KILLED by a named check and recorded in the mutation record.

- **Verification:**
  - Re-run `python3 scripts/r420_probes.py --head <export> --work <dir> --out <dir>`, unchanged.
    - Under (a), RP2 reports 3 frames, and RP1b stays ≥ 15,000 clocks.
    - Under (b), the documents state the window.
  - In both cases, the new check fails under `wait_ignores_gap`, and section ID and `notify_mutants.py` stay rc 0.

### Suggestions (do not affect coverage)

- **R420-2-S1 SUGGESTION (Tests).** The one-tick margin in the BURST deadline cannot be observed on the bench.
  - The margin is `now_ms_i + 32'(IDENT_BURST_MS_C + 1)` (`KL_aecp_notify.sv:746`), which makes a gap at least T-IDENT-BURST rather than up to one tick short.
  - The control `burst_deadline_one_tick_short` (`+ 1` dropped) survives all 106 checks (`receipts/probes/burst_deadline_one_tick_short.log`).
  - Why: at 100 clocks per ms, the timer sweep and the frame build already add about one tick, and the gaps are measured end-of-frame to end-of-frame. On silicon (about 125,000 clocks per ms) the margin is what keeps the gap at or above 150 ms.
  - Proposal: record it among the retained controls with that reason, as R420-1 S1's three were.
- **R420-2-S2 SUGGESTION (Docs, Tests).** A stale tally comment.
  - `tb/pp_top/sim_main.cpp:10930-10933` still says the binary is "ONE of the suite's two builds" and that "The Makefile sums both builds".
  - Since round 1 there are three builds (`tb/pp_top/Makefile:4-11`), and the Makefile checks for three tallies.
  - Proposal: say "three".

## 3. Prior public review findings at this head

| Finding | Status at 88e0bf82 | Evidence |
|---|---|---|
| R420-1-F1 MINOR (a TX stall mid-burst bunches frames) | **Resolved** | RTL fix described below the table. Re-run of my round-1 probe shape (`receipts/probes-sweeps/`, RS1, stalls right after frame 1): the 2->3 gaps are 15,300, 15,306 and 15,305 clocks at 100, 250 and 400 ms (round 1: 15,000, 5,204 and 63). Stalls after frame 2 hold frame 3 and never shorten a gap. Minimum over ten stalls: 15,233. ID7-ID7t pass, and `ident_burst_from_t0` is KILLED by ID3f, ID5k, ID7i, ID7q and ID7r. Corrected text: banner `:151-170`, F08.1 `:30`, 09 §8.3 TIM row, `tb/pp_top/README.md` ID text, and the test renamed `a_press_before_the_restore_goes_out_at_the_release`. |
| R420-1-F2 MINOR (the HDL contract says no CDC lives inside) | **Resolved** | `docs/guides/hdl-engineer.md:64` and `hdl/README.md:25-29` now name `btn_q1_r`/`btn_q2_r` in `KL_aecp_notify`, built only with `EN_IDENTIFY_NOTIF_P` = 1, and link integrator guide §1/§6 and 02 §2 rule 3. The hierarchy path `u_notify.gen_ident.btn_q1_r` in integrator guide §1 matches the instance name (`protocol_processor_top.sv:3759`). `make links` passes: 999 links. |
| R420-1-S1 (arm collision and generation flip unexercised) | Retained, recorded | `tb/pp_top/README.md:1501-1509`: three controls with reasons. Acceptable. |
| R420-1-S2 (no synchroniser marking) | Taken | `(* ASYNC_REG = "TRUE" *)` at `KL_aecp_notify.sv:712-713`; the integrator's false-path / max-delay duty at `integrator.md:38-43`. Lint at EN = 1 is clean. |
| R420-1-S3 (LUT flow not stated) | Taken | The PR body states the flow and remeasures. My module-level run at this head: main 6,454 LUT, head at 0 6,552 LUT, FF 1,721 / 1,721, CARRY4 249 / 249 (`receipts/notify-module-synth.txt`). |
| R420-1-S4 (ST2b one-tick tolerance) | Retained, recorded | `tb/pp_top/README.md` ST2: a decision on the 1 ms timebase for a limiter that predates the lane. Acceptable. |
| R421-1-F1 MINOR (frame 3 scheduled from t0) | **Resolved** | The same RTL fix. My 31-offset SET_NAME fan-out sweep across frame 2's deadline (RS2, R421-1's P1 shape): smallest gap 15,232 clocks (R421-1 measured 13,996 at round 1), largest 1->2 gap 16,250, so the sweep does delay frame 2. ID5i-ID5l pass. |
| R421-1-S1 (release and press inside a burst) | Taken, as a stated reading | 06 §7 `:790-793` and the F06.16 note; graded by ID3f. R420-2-F1 is the same question on the WAITING path, which that reading does not cover. |
| R421-1-S2 (synchroniser marking / constraint) | Taken | As R420-1-S2. |
| R421-1-S3 (`gstri_r` set for SINFO) | Taken, comment only | `KL_aecp_engine.sv:2760-2761`. |
| R421-1-S4 (LUT figures are mapper variance) | Taken | The PR body Validation, round 2, names FF, CARRY4, RAM and DSP as the cost figures. |

How the R420-1-F1 RTL fix works:

- `dep_w = (done_w || left_r) && !uns_tx_busy_i` (`KL_aecp_notify.sv:736`).
- Every departure arms BURST at `now_ms_i + 151` (`:746`, `:802-807`).
- `uns_tx_busy_i` comes from `gen_uns_departure` (`protocol_processor_top.sv:4314-4325`). It is set on the LANE_AECP_UNS grant and cleared on the next eof handshake at the arbiter output.
- I checked that this tracks the frame's last byte:
  - the arbiter's grant is registered after `accept_w` in A_START, which is entered only from A_IDLE after the previous eof (`KL_pp_tx_arbiter.sv:193-245`);
  - the non-ACMP path through the shim is combinational to `tx_*` (`protocol_processor_top.sv:4380-4395`);
  - `uns_done_o` is A_FREE, one edge after the grant (`KL_aecp_engine.sv:2510`, `:3649-3653`), so `busy_r` is already high when the job retires.

## 4. The round-2 assignment, the ruling and the closing issues

### 4.1 Item 1: the merge `a011b14` (parents `5e806296`, `3f3ea56b`; merge base `0451d83d`)

`scripts/merge_check.sh` (`receipts/merge-check.txt`):

- Main changed 48 files and the lane 26. All 42 main-only files equal main at the merge, and all 20 lane-only files equal the lane.
- Six files were changed by both sides:
  - `docs/00_MILAN_COMPLIANCE_REVIEW.md`, `docs/architecture/09_verification.md` and `tb/pp_top/pp_top_wrap.sv` equal a clean `git merge-file` reproduction.
  - In `tb/pp_top/README.md`, main's MP/AC block and the lane's C6 block both survive verbatim.
  - In `tb/pp_top/Makefile` (the `.PHONY` line) and `tb/pp_top/sim_main.cpp` (`main()`: all eight flags, `run_maap_internal`, then every section call), every token of both sides is present. I also read both resolutions by hand.
- `.gitattributes` and `.github/workflows/hdl.yml` are main's, byte-equal.
- No ROM image is tracked. The generated images (`ucode.hex`, `ltn_rom.hex`) are rebuilt by each suite's Makefile, and every build I ran regenerated them.
- Every mutation-driver anchor occurs exactly once at the head (`receipts/mutant-anchor-check-88e0bf8.txt`):
  - `acmp_mutants.py`: 19 mutants;
  - `notify_mutants.py`: 34 mutants, 37 anchors;
  - `d3_mutants.py`: 83 mutants, 92 anchors.
- Nothing of #135, #136 or #137 is lost.
- The suites main touched pass at the head: maap 196, rx_validator 555, acmp_listener 2,988, acmp_nvm 360.

### 4.2 Items 2 to 4

- **Item 2** (burst spacing): met, except R420-2-F1, which is on the WAITING-path guard this item introduced.
- **Item 3** (CDC rule): met.
- **Item 4** (suggestions): each one taken, or retained with its reason.
- **STOP boundary:** round 2 leaves the top's ports and parameters unchanged (`receipts/top-ports-params-r1-vs-head.diff` is empty). Against main the only additions are the authorized `EN_IDENTIFY_NOTIF_P` and `identify_button_i` (`top-ports-params-main-vs-head.diff`). `uns_tx_busy_i` is an internal port, as ruled in 5929618372, and is the constant 0 at the parent's setting.

### 4.3 The idiom commit `88e0bf8`

`scripts/idiom_commit_check.py` (`receipts/idiom-commit-check.txt`):

- the 34 mutants' names, edits and named checks are identical between `2e99ab0` and `88e0bf8`;
- the 128 string literals in `notify_phases.hpp` form an identical multiset.

The diff is a split of the initializer and the declarations, and four extracted functions called in the same order. Section ID at the head: 106/106, with the author's gaps.

### 4.4 Ruling conditions (round 1, re-checked at this head)

1. **Default 0 and zero area.**
   - Default 0 in the top, notify and engine.
   - Module level (`receipts/notify-module-synth.txt`): FF/CARRY4 at 0 equal main (1,721 / 249); at 1 they are 1,787 / 279.
   - Whole-top author receipts at this head: 30,454 FF / 2,317 CARRY4 at 0 = main; +79 FF / +22 CARRY4 at 1.
2. **Synchroniser and debounce contract:** met, and now marked `ASYNC_REG`.
3. **Parent-visible list:**
   - `parent-adoption-c4c6-ea3fb388.patch` passes `git apply --check` against milan-fpga `ea3fb388`'s `KL_pp_shadow.sv` and `measure_test_evidence.py`, whose blob ids `fc0fad60` and `b9bcd3f0` match the patch's index lines (`receipts/parent-patch-apply-check.txt`).
   - It ties `identify_button_i` to 0 and binds `EN_IDENTIFY_NOTIF_P` to 0, each with a rationale, and carries the `notify_mutants.py` and #137 `acmp_mutants.py` dispositions.
4. **Both settings graded:** ID 106/106 at 1, and the default build (8,044) with ID0 at 0.

### 4.5 Closing issues

- **#58: met in full.**
  - NP, re-run at this head in the default build.
  - The enqueue and class controls are KILLED.
  - The MGMT disposition is in 06 §7 class (2) and the REQ-NOT-002 row.
- **#80: met in full on its written acceptance.**
  - 1: origination and spacing, graded.
  - 2: ST churns `ctr_change_i` (`notify_phases.hpp:860-864`).
  - 3: RN seed 0xC6A46301 against an independent model, with a mutation record.
  - 4: GAP-06 and 06 §7.
- **#86: met in full on its written acceptance.**
  - 03 §4/§5 and GAP-17.
  - Identify originated and graded.
  - `tb/originator` R (seed 0x86A46301, 16 owners).
  - The PROBE_TX owner in 03 §5 (`:182`).
- **#54: not met in full while R420-2-F1 is open.** Acceptance 2 ("A trigger emits three byte-exact ... frames") holds for every graded trigger. RP2 is a trigger that emits nothing. Acceptance 1, 3 and 4 are met.

## 5. Lens results (artifact-specific)

- **Conformance: UNCLEAN (F1).**
  - Re-checked: the IDENTIFY_NOTIFICATION schedule against §7.5.1's "150 ms delay between transmissions", now from departure; the re-arm from the first frame's departure (Figure 7-142 timeout); identifySequenceID per burst.
  - The SET_STREAM_INFO and push conformance did not change in round 2. NP/ST/RN were re-run green.
  - F1 is the Figure 7-142 WAITING press.
- **RTL: UNCLEAN (F1).** I read the whole sequencer at the head (`KL_aecp_notify.sv:687-868`):
  - `dep_w`/`left_r`/`gap_r` for every path SEND->GAP->SEND->HOLD->WAIT;
  - the `exp_r_w` latch into `fired_r` while `gap_r` holds;
  - the BURST arm deadline taken at grant time, which is only ever later;
  - no stale BURST expiry is possible;
  - `gen_uns_departure` against the arbiter FSM and the shim;
  - `uns_done_o` timing;
  - a no-send retirement, where `busy` is low and departure is at once;
  - the engine edit (comment only).

  Lint: 41/41 modules, plus the three changed modules at EN = 1 with 0 findings. F1 is at `:794`.
- **Robustness: UNCLEAN (F1).**
  - Stall sweeps (RS1): ten stalls of 100-400 ms after frame 1 or 2.
  - Contention sweep (RS2): 31 offsets of a 15-row fan-out.
  - The lane's ID5i-ID5l and ID7.
  - A release and a press inside a burst (ID3).
  - The timeout passing mid-stall (ID7n-ID7t).
  - F1 is a lost input in the post-burst window.
- **Tests: UNCLEAN (F1).**
  - `make -C tb/pp_top run`: 8,170 = 8,044 + 20 + 106.
  - `notify_mutants.py`: 34/34 KILLED, goldens PASS (four chunks).
  - A sample of `d3_mutants.py` in the files round 2 edited: 4/4 KILLED.
  - Probe controls: `hold_ignores_gap` KILLED; `wait_ignores_gap` SURVIVED (F1); `burst_deadline_one_tick_short` SURVIVED (S1).
  - `88e0bf8` left the tests intact (4.3).
- **Docs: UNCLEAN (F1).**
  - Round-2 text in 06 §7 and F06.16, F08.1, 09 §8.3, integrator §1/§6, hdl-engineer CDC row, `hdl/README.md`, `tb/pp_top/README.md` and the PR body, checked against the RTL.
  - `make` lint, links, matrix, modmatrix, params and stale all rc 0.
  - F1 is the integrator §6 contract. S2 is the stale comment.

## 6. Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R420-2-F1 open) | `KL_aecp_notify.sv:687-868`; F06.16 / 06 §7 reading; section ID frames and gaps; NP/ST/RN re-run; RP1/RP2 probes | R420-2 | 88e0bf82888d6ad83b500425a786814da467610b |
| RTL | UNCLEAN (R420-2-F1 open) | `KL_aecp_notify.sv` sequencer, `protocol_processor_top.sv:3220, 3867, 4308-4325, 4345-4395`, `KL_pp_tx_arbiter.sv:193-287`, `KL_aecp_engine.sv:2503-2510, 2757-2761, 3603-3653`; lint at 0 and 1; module synth at 0 and 1; top port/param diff | R420-2 | 88e0bf82888d6ad83b500425a786814da467610b |
| Robustness | UNCLEAN (R420-2-F1 open) | RS1 stall sweep (10), RS2 fan-out sweep (31), ID3/ID5i-l/ID7, RP2 lost press | R420-2 | 88e0bf82888d6ad83b500425a786814da467610b |
| Tests | UNCLEAN (R420-2-F1 open) | `tb/pp_top/notify_phases.hpp` (round-2 diff and ID section), `notify_mutants.py` 34/34, d3 sample 4/4 plus the author's 83/83 receipts cross-checked by name, 9 suites, 5 reviewer probes, `88e0bf8` string/edit identity | R420-2 | 88e0bf82888d6ad83b500425a786814da467610b |
| Docs | UNCLEAN (R420-2-F1 open) | 06 §7/F06.16, 08 F08.1, 09 §8.3, `integrator.md` §1/§6, `hdl-engineer.md:64`, `hdl/README.md`, `tb/pp_top/README.md`, PR body round 2, merge of 00/09; docs make targets | R420-2 | 88e0bf82888d6ad83b500425a786814da467610b |

## 7. What I executed

Builds and runs used an exact-head `git archive` export under `scratch/`, never the clone. Every command ran in the foreground, with build parallelism capped at 8 (`receipts/verilator-wrapper.sh`, `taskset -c 0-7`).

| Command | rc | Result |
|---|---:|---|
| `make -C tb/pp_top run` | 0 | default 8,044, fixture 20, identify 106: 8,170 PASS, 0 FAIL |
| `./obj_idn/Vpp_top_idn` (section ID alone) | 0 | 106/0; gaps as the author's receipt |
| `make` in aecp_notify, originator, ucpu, ca_originator | 0 | 10, 107, 396, 16 |
| `make` in maap, rx_validator, acmp_listener, acmp_nvm | 0 | 196, 555, 2,988, 360 |
| `python3 scripts/check_upc_map.py` | 0 | PASS |
| `./scripts/lint_hdl.sh` | 0 | 41 LINT OK |
| lint of `KL_aecp_notify`, `KL_aecp_engine`, top with `-GEN_IDENTIFY_NOTIF_P=1` | 0 | 0 findings each |
| `make lint links matrix modmatrix params` (export), `make stale` (clone, read-only) | 0 | 41 mermaid + 18 wavedrom; 999 links; 115 REQ / 17 GAP; 94 rows, 0 untested; 27 = 27 = 27 |
| `python3 tb/pp_top/notify_mutants.py --jobs 1 --only ...` (four chunks) | 0 | 4 + 11 + 7 + 12 = 34 KILLED, every golden PASS |
| `python3 tb/pp_top/d3_mutants.py --jobs 1 --only` 4 mutants in the top or engine | 0 | 4/4 KILLED, goldens PASS |
| `scripts/r420_probes.py` (5 probes), plus the `head_with_sweeps` probe | 0 | section 2 and 3 tables |
| `scripts/merge_check.sh`, `scripts/idiom_commit_check.py` | 0 | section 4 |
| yosys `synth_xilinx -family xc7 -flatten`, module `KL_aecp_notify` (main, head@0, head@1) | 0 | FF 1,721 / 1,721 / 1,787; CARRY4 249 / 249 / 279 |
| `git apply --check` of the C4+C6 parent patch at milan-fpga `ea3fb388` (two files fetched read-only) | 0 | applies; blob ids match |

Not run, by this round's rules: `run_suites.sh` (the full processor bank), the whole-top `syn/yosys/run.sh`, parent, gPTP and builder banks, Docker/act, hardware. Also not re-run: the adp, srp_top, maap, gsi and acmp_talker campaigns, and 79 of the 83 d3 mutants. The author's round-2 receipts cover them, and I cross-checked the d3 kill list by name against the driver's 83.

## 8. Real limits and pending manager duties

- **Verilator.** The wrapper named in the assignment (`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`) does not exist on this host. I used a copy of `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator`, which reports `Verilator 5.050 2026-07-01 rev v5.050`, behind a shim that rewrites `-j 0` to `-j 8`. The identity and hashes are in `receipts/verilator-identity.txt`.
- **Standards.** The IEEE 1722.1-2021 and Milan v1.2 texts were not available. I judged conformance from the clauses as quoted in the issues, the repository and the bench, including the Figure 7-142 transitions. F1's conformance reading rests on that quotation.
- **Synthesis.** My figures are module-level yosys only. The whole-top figures are the author's receipts. Vivado out-of-context at the parent is authoritative.
- **Hosted checks at the exact head** (`receipts/hosted-check-runs-88e0bf8.txt`, queried 2026-10-01T11:21Z): docs-gates success ×2, portability success ×2, suites **in_progress** ×2, combined pending. Hosted/act acceptance is the manager's.
- **Hardware.** Physical calibration NOT RUN. No hardware was used. Simulation is not hardware proof.
- **Manager duties:**
  - the donor bank and the parent consumer set at milan-fpga dev `ea3fb388` with `parent-adoption-c4c6-ea3fb388.patch`;
  - the final current-dev candidate at the merge turn (source base `3f3ea56b`, live dev `ea3fb388`);
  - the hosted suites conclusion;
  - resolution of R420-2-F1, then a re-review of the new head.
- **Clone integrity** (`receipts/clone-integrity.txt`):
  - HEAD `88e0bf82`, tree `5cc519fb`, and `git write-tree` of the index equals the tree;
  - the index mode/blob/path digest equals the tree's;
  - worktree and index clean, with no untracked or ignored files;
  - no gitlinks. The repository has no submodules, so none are required.
  - One incident: the module-level synthesis ran with the clone as its working directory, and its ABC step left an empty untracked `abc.history` there. I removed it before the integrity record. No tracked byte was touched.
- **Publication.** Receipts replace the home-directory prefix with `~`. `scratch/` is not published.

R420-2 FINISHED
