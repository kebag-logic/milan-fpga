[R420] POSITIVE - exact head 9624ef4c452d708de68a901d5e645bdfa1f5d6f5

# R420-3: internal independent review of processor PR #139 (lane C6, issue #80), round 3

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #139. Closes #54, #58, #80 and #86.
- Exact head `9624ef4c452d708de68a901d5e645bdfa1f5d6f5`, tree `7c4193b5cf5af25aba735ee68e64b412b9663f1a`.
- Source base: processor main `3f3ea56ba61829718a6a288600ab4fdac73aa5ba`. The branch is judged on that base. Processor main has since moved (`16ea10ac`, C5b); the merge-only round and its delta review come later.
- Round-2 head: `88e0bf82`. Round 3 adds two commits on it and no merge:
  - `ed000fe`: the press latch (R420-2 F1, R421-2 F1), `tb/pp_top` ID8 and three controls;
  - `9624ef4`: the suggestions (ID9, the `sim_main.cpp` build count, `tb/aecp_notify` section FT).
- Reviewer: [R420], internal role, cleared context, own detached clone. Round R420-3. Assignment: #80 comment 5932649053 (ruling: latch the press, do not document the window). Review start: PR #139 comment 5938907810.

## Verdict

**POSITIVE. No MINOR, MAJOR or BLOCKER finding is open at this head.** One new SUGGESTION (R420-3-S1, Tests) does not gate.

- **My round-2 finding R420-2-F1 is resolved**, and so is R421-2-F1, the same defect.
  - A press made in the T-IDENT-BURST gap after a burst is now latched by one flop, `prs_r`. Its burst starts when the gap ends. The change adds no port, parameter or register.
  - My round-2 probe, re-run unchanged: RP2 (an 80 ms press 20 ms after the third frame) now sends 3 frames. At round 2 it sent 0.
  - Every inter-frame gap I measured at this head is at least 15,232 clocks (T-IDENT-BURST is 15,000). That covers my round-2 sweeps and 600 new probe checks.
- **The in-burst latch is sound.** It latches a release and a new press made inside a running burst. It loses no press, it adds at most one owed burst, and it never shortens a gap.
- **The new tests discriminate.**
  - The head's section ID fails 29 of 155 checks on round-2 RTL. My failing lines are byte-identical to the author's receipt.
  - All six round-3 controls are KILLED by their named checks, and so is `ident_next_burst_at_once`. The full `notify_mutants.py` campaign gives 40 of 40 KILLED, in five chunks.
- **The docs agree with the RTL**: the operator guide, integrator guide §6, 06 §7 / F06.16, F08.1 and 09 §8.3.
- **No top port or parameter changed in round 3.** The RTL change sits entirely inside the `gen_ident` generate, so the parent's setting (`EN_IDENTIFY_NOTIF_P` = 0) is unchanged.
- **Closing issues:** #54, #58, #80 and #86 are each met in full on their written acceptance (section 4).

## 1. How the task was reconstructed

Public sources, in this order:

1. **Process.** The processor repository has no `AGENTS.md` or `CONTRIBUTING.md`. I read its `README.md` and `docs/README.md`: the reading order, the ID registries, the single-source rules, and the `make check` workflow.
2. **Frozen acceptance and scope decisions:**
   - the body of #80 (acceptance 1-4) and the acceptance lists of #54 (1-4), #58 (1-3) and #86 (1-4);
   - on #80:
     - the assignment 5915639621;
     - the STOP 5915752457 and its ruling 5915765717 (four conditions);
     - round 2 (5924910356) and the ruling on `uns_tx_busy_i` (5929618372);
     - round 3 (5932649053): latch the press; grade a short and a long press in the gap, a press at gap end, and single-guard / latch-removal controls; three suggestions; STOP before any top port, top parameter or parent-visible change;
   - the PR #139 body, including its round-3 section.
3. **Authorities:**
   - IEEE 1722.1-2021 §7.4.39, §7.5.1, §7.5.1.2.1 and Figure 7-142 (WAITING and IDENTIFY, txIdentify, the timeout);
   - Milan §5.4.5.4;
   - 01 F01.5 (P-CLK-HZ), 06 §7 / F06.16, 08 F08.1, 09 §8.3, and the integrator and operator guides.
4. **Diff and history:** `git diff 3f3ea56b..9624ef4c` (the lane), and in detail the round-3 delta `88e0bf8..9624ef4c` (14 files, +748/-54), commit by commit.
5. **Public evidence:**
   - the evidence branch at kebag-logic/milan-fpga `8fb13c82`, which holds `review-evidence/ppC6-r1/author-r3`; I compared its receipts with my runs (section 6);
   - the round-1 packet at `2c532827`;
   - the manager's evidence comment on #139 (5921694276) and the review-start notices.

Prior public review findings (R420-1, R421-1, R420-2, R421-2) were read only after my own pass, my probes and my draft verdict were complete. Section 3 resolves or retains each of them.

## 2. Findings

No MINOR, MAJOR or BLOCKER finding.

### R420-3-S1 SUGGESTION: the latch's boundary cycle has no discriminating check

- **Lenses:** Tests.
- **Where:**
  - `tb/pp_top/notify_phases.hpp:742-790` (ID8j-ID8n, `press_at_gap_end`);
  - `hdl/aecp/KL_aecp_notify.sv:810` (`if (btn_q2_r && gap_r) prs_r <= 1'b1;`).
- **Evidence:**
  - The "press made exactly at gap end" arm uses a 30 ms press, which is still held when the gap ends. It passes without the latch, as `tb/pp_top/README.md:1414-1415` already says.
  - So the one cycle in which the latch alone saves a press is not graded: the edge that samples the IDENT-BURST expiry, while `gap_r` still reads 1.
  - A reviewer control plants `if (btn_q2_r && gap_r && !exp_b_w) prs_r <= 1'b1;`, which skips the latch in that cycle (`scripts/boundary_control.sh`). It **passes all 178 section-ID checks**.
  - My 1-clock-press sweep RP3j kills it: k = -2 sends 3 frames, want 6 (`receipts/boundary_control.log`).
  - At the head, every RP3j placement sends exactly one burst (`receipts/r420_3_probes_head.log`).
- **Impact:** none on the head's behaviour, which is correct. A debounced button cannot produce a press that is high only on that one edge, so the gap is regression coverage only.
- **Proposal:** add a 1-clock press at k = -2 (sampled only on the expiry edge) to ID8j's arm, or record this control among the retained controls with that reason.

## 3. Prior public review findings at this head

| Finding | Status at 9624ef4c | Evidence |
|---|---|---|
| R420-2-F1 MINOR (a press in the post-burst gap sends nothing; WAIT guard untested; integrator contract says otherwise) | **Resolved**, by option (a) of its required outcome | Detail below the table |
| R421-2-F1 MINOR (the same defect; related note: a second press released before a running burst ends is dropped) | **Resolved** | The same fix. The in-burst latch (`:801-804`) answers the related note: ID8s, and my RP3c and RP3e' |
| R420-2-S1 (one-tick BURST margin invisible on the compressed bench) | **Taken** | `tb/aecp_notify` section FT at 100,000 clocks per ms. FT2 measures 15,000,004 clocks. `ident_burst_deadline_one_tick_short` is the same edit as my round-2 `burst_deadline_one_tick_short`: it is KILLED by FT2 (14,900,004), and it still passes section ID, as expected (`receipts/r420_2_probes_rerun_probes.json`) |
| R420-2-S2 (`sim_main.cpp` says two builds) | **Taken** | `tb/pp_top/sim_main.cpp:20` and `:10931-10934` now say three |
| R421-2-S1 (`ready` term of the departure never graded) | **Taken** | ID9-ID9h (`notify_phases.hpp:848-899`). `ident_departure_ignores_ready` is KILLED by ID9d and ID9h (63 clocks) |
| R421-2-S2 (one-tick floors by inspection only) | **Taken** | FT2-FT4. `ident_t0_same_ms` is KILLED by FT4 (99,900,004) |
| R420-1-F1 / R421-1-F1 MINOR (frames bunch under a stall or contention) | **Still resolved** | My round-2 sweeps, re-run unchanged. RS1, ten stalls of 100-400 ms after frame 1 or 2: min 15,233. RS2, 31-offset fan-out: min 15,232, largest 1->2 gap 16,250 |
| R420-1-F2 MINOR (CDC rule) | **Still resolved** | Untouched in round 3 |
| R420-1-S1, R420-1-S4 | **Retained, recorded** | `tb/pp_top/README.md:1556-1557` and `:1472`. Unchanged and acceptable |
| R420-1-S2/S3, R421-1-S1-S4 | **Taken** at round 2 | Untouched in round 3 |

How R420-2-F1 is resolved:

- `hdl/aecp/KL_aecp_notify.sv:806-818`: WAITING latches a press seen while `gap_r` runs (`:810`). It starts on `(btn_q2_r || prs_r) && !gap_r` (`:811`) and clears the latch.
- The integrator §6, operator, 06 §7 / F06.16 and F08.1 texts now promise exactly that.
- ID8-ID8e grade the WAITING-path press. `ident_wait_ignores_gap`, the single-guard control that is the successor of my round-2 `wait_ignores_gap`, is KILLED by ID8c and ID8h (367 clocks).
- My round-2 `wait_ignores_gap` probe is now refused, as expected: its anchor is the round-2 line that no longer exists.
- `hold_ignores_gap` (my round-2 probe, unchanged) is KILLED by ID3f, ID7r, ID8q and ID8r.

## 4. The round-3 assignment, the ruling and the closing issues

**Item 1: latch the press.** Met.

- **RTL.** I read the whole sequencer at the head (`KL_aecp_notify.sv:709-870`) for every path WAIT -> SEND -> GAP -> SEND -> HOLD -> WAIT.
  - The new flop `prs_r` (`:728`) is reset (`:777`).
  - It is set in only two places:
    - the in-burst latch (`:804`), which needs `rel_r`, and `rel_r` is set only by a release seen in SEND or GAP of this burst;
    - the WAITING latch (`:810`).
  - It is cleared at both burst starts (`:815`, `:863`). The case assignment comes later than the latch assignment, so a start always wins over a same-edge latch.
  - Every start still requires `!gap_r`, so no inter-frame gap can go under T-IDENT-BURST.
  - In the expiry cycle `gap_r` still reads 1, so a press there is latched and starts one edge later. ID8n measures this: 166 clocks after the expiry, against 167 for k = 2.
  - No stale latch survives a start. Further presses while a burst is owed add none (RP3b, RP3c).
  - At `EN_IDENTIFY_NOTIF_P` = 0 the generate is not built. Every RTL hunk except the banner comment lies at lines 728-863, inside `gen_ident` (`:709`-`:871`).
- **The in-burst latch (manager-accepted).** I judge it conformant.
  - Figure 7-142 answers `identifyButtonPressed` in WAITING with IDENTIFY's entry action txIdentify. A release seen during txIdentify returns the machine to WAITING once txIdentify ends, so a following press is a new IDENTIFY entry.
  - The latch defers that entry only until the T-IDENT-BURST gap after the third frame. So §7.5.1's 150 ms spacing holds across bursts, and no press is lost.
  - Reading the button only as a level after txIdentify would instead leave a held re-press to the 1 s timeout. 06 §7 (`:790-798`) records the latch as a deliberate reading of Figure 7-142.
  - The number of bursts is bounded: at most one burst is owed, so presses cannot queue bursts.
- **Grading asked by the ruling:**
  - a 30 ms press in the gap (ID8-ID8e);
  - a 200 ms press in the gap (ID8f-ID8i);
  - a press at gap end and at k = -1, 0, 1 and 2 edges (ID8j-ID8n; see S1);
  - two in-burst cases (ID8o-ID8v);
  - the single-guard control `ident_wait_ignores_gap` and the two latch removals, all KILLED;
  - `ident_next_burst_at_once`, kept and KILLED (ID3f, ID7r).
- **Docs:** `docs/guides/operator.md:50`, `docs/guides/integrator.md:302-308`, `docs/architecture/06_aecp_engine.md:790-798` with F06.16 `:921`, `08_timing.md:30` and `09_verification.md:220-225` agree with each other and with the RTL. I checked each statement against probes RP3a-RP3j.

**Item 2: the suggestions.** All three were taken (section 3).

- ID9 holds `tx_ready_i` low on frame 1's eof beat for 400 ms (40,001 clocks), then on frame 2's. The next frame follows by 15,232 and 15,299 clocks.
- FT is a second build of `tb/aecp_notify` at `EN_IDENTIFY_NOTIF_P` = 1 and 100,000 clocks per ms (F01.5 P-CLK-HZ 100 MHz; top `TIM_DIV_US_P` = `CLK_HZ_P`/1e6, `TIM_DIV_MS_P` = 1000).
  - Its timer model fires on the first clock of the deadline's ms.
  - I checked this against `KL_pp_timer_service.sv`. The real service raises `now_ms` on the tick, then sweeps, and fires when `now - deadline` is non-negative. The real service is therefore only later than the model.
  - The sequencer's `now_ms_i` is the same counter the sweep compares (`protocol_processor_top.sv:874, 892, 3879`).
  - FT measures the next frame's presentation, not its departure, so its bound is conservative.

**STOP boundary.**

- `git diff 88e0bf8..9624ef4c -- hdl/top` is empty.
- Against the base, the only top additions are the authorized `EN_IDENTIFY_NOTIF_P` and `identify_button_i` (`receipts/diff_checks.log`).
- The three `dbg_ident_gap_*` outputs live on the test wrap only (`tb/pp_top/pp_top_wrap.sv:434-436, 774-778`). They are combinational reads of top internals with no drive back.

**Ruling conditions (round 1), re-checked:**

- Default 0: lint is clean at 0 and 1 for the notify module, the engine and the top. ID0 passes on the default build (3/3).
- Synchroniser and debounce contract: untouched.
- Parent-visible list: unchanged. Round 3 adds no top or module port. The parent patch application is the manager's.

**Closing issues:**

- **#54: met in full.**
  - 1: input and parameter, default 0, generate-gated.
  - 2: every trigger I probed emits three byte-exact frames to 91-E0-F0-01-00-01 with controller_entity_id 90-E0-F0-FF-FE-01-00-01 and an incrementing sequence_id, through the shared timer service. This includes presses in the gap, at its last clock, 1-clock presses, and presses during stalls; the round-2 counterexample is gone.
  - 3: re-arm, graded with mutants.
  - 4: A6 BAD_ARGUMENTS (ID4) and 06 §7 / GAP-06.
- **#58: met in full.** Unchanged in round 3. The NP golden passes at this head (47/0). The enqueue and class controls are KILLED. MGMT is dispositioned in 06 §7 and REQ-NOT-002.
- **#80: met in full.**
  - 1: as #54.
  - 2: ST golden 18/0.
  - 3: RN golden 4/0 with its mutation record.
  - 4: GAP-06 and 06 §7.
- **#86: met in full.** Unchanged in round 3. The `tb/originator` R golden passes (107/0), and its four inflight controls are KILLED.

## 5. Lens results (artifact-specific)

- **Conformance: CLEAN.**
  - Checked the Figure 7-142 WAITING answer for every press shape: RP3a-RP3j, ID8, ID8f, ID8o and ID8s.
  - The §7.5.1 150 ms spacing holds within and across bursts: minimum 15,232 clocks at 100 clocks/ms, and 15,000,004 at full timebase.
  - The timeout counts from the first frame's next boundary (FT4).
  - identifySequenceID advances once per burst, checked byte-exact in every probe from 0 after reset.
  - The in-burst reading is judged in section 4.
- **RTL: CLEAN.**
  - Covered: the sequencer at `KL_aecp_notify.sv:709-870`, line by line for the new flop; the departure flop at `protocol_processor_top.sv:4314-4324`; the timer service's fire condition.
  - Lint: `lint_hdl.sh` gives 41 LINT OK. The notify module, the engine and the top lint with 0 findings at `EN_IDENTIFY_NOTIF_P` = 0 and = 1.
  - The change is confined to `gen_ident`.
- **Robustness: CLEAN.**
  - Probes: a held-through burst then a re-press in the gap (RP3a); three presses in one gap (RP3b); two re-presses in one burst (RP3c); a release only, which gives no spurious burst (RP3d).
  - Also: 1-clock presses in the gap and in a burst (RP3e); a chain of owed bursts (RP3f); a press while frame 3's last byte is held 300 ms (RP3g); 3-clock and 1-clock presses at clock offsets -12..+6 around the expiry (RP3h, RP3j); a 25-offset press sweep from +2 to +170 ms (RP3i).
  - All 600 probe checks pass, with a minimum gap of 15,233.
  - The same probes on round-2 RTL fail 37 checks: they discriminate.
  - My round-2 stall and fan-out sweeps still hold.
- **Tests: CLEAN** (S1 is a suggestion).
  - Section ID at the head: 178/0. ID0: 3/0. `tb/aecp_notify`: 14/0 (10 + FT 4).
  - The head's tests on round-2 RTL: 155 checks, 29 failures, identical to the author's receipt.
  - `notify_mutants.py`: 40 of 40 KILLED, every golden PASS. The kill counts match the README mutation record mutant by mutant.
  - A `d3_mutants.py` sample of three is KILLED, goldens PASS. The round-3 files are not among its planting targets.
- **Docs: CLEAN.**
  - Covered: the round-3 text in the operator guide, integrator §6, 06 §7 / F06.16, F08.1, 09 §8.3, `tb/pp_top/README.md` (ID8, ID9, mutation record), `tb/aecp_notify/README.md` (FT) and the PR body round 3. I checked each against the RTL and my measurements (15,301 / 166 / 167 / 63 / 15,232 / 15,299 / 40,001; FT 15,000,004 / 15,100,002 / 100,000,004).
  - `make check`: rc 0. `gen_matrix.py --check`: 94 rows, 0 untested. `git diff --check` is clean on both ranges.

## 6. What I executed

Builds and runs used an exact-head `git archive` export under `scratch/`, never the clone. Every command ran in the foreground. Build parallelism was capped at 8 by `scripts/vl8.sh`, which rewrites `-j 0` to `-j 8` around the pinned wrapper. Mutation drivers ran with `--jobs 1`.

| Command | rc | Result |
|---|---:|---|
| `make -C tb/pp_top identify-build` + `./obj_idn/Vpp_top_idn` | 0 | ID 178 checks, 0 failures (`receipts/head_pp_top_ID.log`) |
| `make -C tb/pp_top gsi-build` + `./obj_dir/Vpp_top_sim --identify-only` | 0 | ID0 3/0 |
| `make -C tb/aecp_notify run` | 0 | 10 + 4 = 14 PASS; FT2 15,000,004, FT3 15,100,002, FT4 100,000,004 |
| the head's `tb/` on round-2 `hdl/` (`88e0bf8`), section ID | 1 (expected) | 155 checks, 29 failures, FAIL lines identical to `author-r3/receipts/id-head-tests-on-round2-rtl.log` |
| `notify_mutants.py --jobs 1 --only` (five chunks: 7 + 13 + 5 + 5 + 10) | 0 | 40 of 40 KILLED, goldens PASS (`receipts/notify_mutants_*.log`, `receipts/mutants/`) |
| `d3_mutants.py --jobs 1 --only` (3) | 0 | 3 of 3 KILLED, goldens PASS |
| `scripts/run_probes.sh` (reviewer probes RP3a-RP3j) at the head | 0 | 600 checks, 0 failures; min gap 15,233 |
| the same on round-2 RTL | 1 (expected) | 378 checks, 37 failures (lost presses) |
| `scripts/boundary_control.sh` (S1) | 0 | section ID 178/0 under the control; RP3j k = -2 fails |
| `scripts/r420_2_probes_unchanged.py` (my round-2 driver, blob `c33b9444`, unchanged) | 0 | RP1 15,301; RP2 3 frames (round 2: 0); RS1 min 15,233; RS2 min 15,232; `hold_ignores_gap` KILLED; `burst_deadline_one_tick_short` passes ID (killed by FT2); `wait_ignores_gap` refused (anchor gone) |
| `./scripts/lint_hdl.sh` | 0 | 41 LINT OK |
| lint of notify, engine and top at `-GEN_IDENTIFY_NOTIF_P=0/1` | 0 | 0 findings each |
| `make check`; `python3 scripts/gen_matrix.py --check` | 0 | lint, wavedrom 18, links 999, matrices, parameters 27 = 27 = 27; 94 rows, 0 untested |
| `git diff --check` base..head and r2..head | 0 | clean |

Not run, by this round's rules: `run_suites.sh` (the full processor bank), the whole-top `syn/yosys/run.sh`, the parent, gPTP and builder banks, the adp, maap, srp_top, gsi and acmp_talker campaigns, 80 of the d3 mutants, Docker/act and hardware. The author's round-3 receipts and the manager's banks cover them.

## 7. Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | IEEE 1722.1-2021 §7.5.1 / Figure 7-142 WAITING and IDENTIFY against `KL_aecp_notify.sv:709-870`; 06 §7 in-burst reading; ID8/ID9/FT measurements; probes RP3a-RP3j; #54/#58/#80/#86 acceptance | R420-3 | 9624ef4c452d708de68a901d5e645bdfa1f5d6f5 |
| RTL | CLEAN | `KL_aecp_notify.sv:170-176, 709-870` (`prs_r` at `:728, :777, :801-804, :806-818, :863`); `protocol_processor_top.sv:874-903, 3223, 3870, 4314-4324`; `KL_pp_timer_service.sv:85-200`; lint at 0 and 1; top port/param diff | R420-3 | 9624ef4c452d708de68a901d5e645bdfa1f5d6f5 |
| Robustness | CLEAN | 600 probe checks (RP3a-RP3j: re-press shapes, 1-clock presses, owed-burst chain, eof stall plus press, clock-level boundary sweeps, 25-offset press sweep); round-2 RS1/RS2 re-run; the same probes on round-2 RTL (37 failures) | R420-3 | 9624ef4c452d708de68a901d5e645bdfa1f5d6f5 |
| Tests | CLEAN (S1 suggestion) | `tb/pp_top/notify_phases.hpp:622-905`, `pp_top_wrap.sv:425-437, 771-778`, `sim_main.cpp:20, 10931-10934`, `tb/aecp_notify/sim_main.cpp:207-391` and Makefile; `notify_mutants.py` 40/40; head tests on round-2 RTL 29/155; d3 sample 3/3; boundary control | R420-3 | 9624ef4c452d708de68a901d5e645bdfa1f5d6f5 |
| Docs | CLEAN | `operator.md:50`, `integrator.md:302-308`, `06_aecp_engine.md:790-798, 904-921`, `08_timing.md:30`, `09_verification.md:217-226`, `tb/pp_top/README.md:1381-1420, 1510-1560`, `tb/aecp_notify/README.md`, PR body round 3; `make check`, matrix | R420-3 | 9624ef4c452d708de68a901d5e645bdfa1f5d6f5 |

## 8. Real limits and pending manager duties

- **Verilator:** the pinned wrapper reports `Verilator 5.050 2026-07-01 rev v5.050`, behind a shim capping build jobs at 8 (`receipts/verilator_identity.txt`).
- **Standards:** the IEEE 1722.1-2021 and Milan v1.2 texts were not available here. Conformance is judged from the clauses as quoted in the issues, the repository and the bench, including the Figure 7-142 transitions.
- **Probes:** they run on the compressed timebase of `tb/pp_top` (100 clocks per ms). The full-timebase margins rest on the lane's FT bench, whose timer is a model; I checked that model against the RTL timer service by reading it, not by co-simulation.
- **Synthesis:** I ran none. The yosys module figures (one flip-flop at 1, none at 0) are the author's receipts. Vivado out-of-context at the parent is authoritative.
- **Hosted checks at the exact head** (`receipts/hosted_check_runs_9624ef4.txt`, queried 2026-10-01T19:54Z): docs-gates success, portability success, suites **in_progress**; the combined status is pending. Hosted/act acceptance is the manager's.
- **Hardware:** physical calibration NOT RUN. No hardware was used, and simulation is not hardware proof.
- **Manager duties:**
  - the donor bank and the parent consumer set at milan-fpga dev `7f0927bb` with the combined C4 + C6 parent patch;
  - the hosted suites conclusion;
  - the final current-dev candidate at the merge turn (source base `3f3ea56b`, live dev `7f0927bb`);
  - the merge-only round onto processor main (`16ea10ac` and after) and its delta review;
  - the S1 disposition (optional).
- **Clone integrity** (`receipts/clone_integrity.txt`):
  - HEAD is `9624ef4c`, tree `7c4193b5`, and `git write-tree` equals the tree;
  - the index digest equals the tree digest (modes, blobs and paths);
  - the worktree and index are clean, with no untracked or ignored files;
  - there are no gitlinks: the repository has no submodules, so none are required.
- **Publication:** receipts replace the home-directory prefix with `~`, and the pinned image path with `<pinned-image>`. `scratch/` is not published.

R420-3 FINISHED
