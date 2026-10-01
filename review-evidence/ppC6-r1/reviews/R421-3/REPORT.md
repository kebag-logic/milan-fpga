[R421] POSITIVE - exact head 9624ef4c452d708de68a901d5e645bdfa1f5d6f5

# R421-3: external review of processor PR #139 (lane C6, notifications and Identify), round 3

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, issue #80, PR #139 (closes #54, #58, #80, #86).
- Exact head `9624ef4c452d708de68a901d5e645bdfa1f5d6f5`, tree `7c4193b5cf5af25aba735ee68e64b412b9663f1a`.
- Range: source base `3f3ea56ba61829718a6a288600ab4fdac73aa5ba`..head. Round 3 is two commits on my round-2 head `88e0bf82`, with no merge:
  - `ed000fe`: the press latch, section ID8 and three controls;
  - `9624ef4`: the suggestions (ID9, the `sim_main.cpp` build count, `tb/aecp_notify` section FT and two controls).
- Assignment: #80 comment 5932649053 ("latch, do not document the window"). Public review start: PR #139 comment 5938908794.
- I judged the branch on its base `3f3ea56b`. Processor main has since moved (`16ea10ac`, and later C5a). The merge-only delta round belongs to the manager.

## Verdict

**POSITIVE.** No MINOR, MAJOR or BLOCKER finding is open at this head, and every lens is CLEAN.

- **My round-2 finding F1 is RESOLVED.** That was the press inside the post-burst gap that sent nothing; R420-2 F1 is the same defect.
  - The one-bit latch `prs_r` remembers a press made in the T-IDENT-BURST gap, and its burst starts when the gap ends.
  - No inter-frame gap goes under T-IDENT-BURST.
- **The in-burst latch is acceptable.** That is the latch for a release and a new press made inside a running burst.
- **The three suggestions are taken and verified:** ID9, the build count, and FT.

One new SUGGESTION (S1) does not gate.

I fixed my verdict and ledger (`receipts/verdict_before_prior_findings.txt`, 20:16:05Z) before reading any prior-round finding text. I did not read the other reviewer's round-3 material.

## How the task was reconstructed

- **Repository rules.** This repository has no `AGENTS.md` or `CONTRIBUTING.md` at the head. I used `README.md` and `docs/README.md` (conventions, ID registries, editing workflow), plus the persona guides.
- **Scope.** The #80 body and its frozen acceptance. The design STOP and its ruling (5915752457, 5915765717): `identify_button_i` and `EN_IDENTIFY_NOTIF_P` are authorized with four conditions. The round-2 assignment (5924910356) and its `uns_tx_busy_i` ruling (5929618372). The round-3 assignment (5932649053).
- **Closing issues.** The acceptance lists of #54, #58 and #86.
- **Authorities.** IEEE 1722.1-2021 §7.4.39, §7.5.1, §7.5.1.2.1 and Figure 7-142; Milan v1.2 §5.4.5.4. The repository's 06 §7 / F06.16, F08.1, integrator guide §6 and operator guide.
- **History.** `git diff 3f3ea56b..9624ef4c` and `88e0bf8..9624ef4c`, and the commit history.
- **Public evidence.** The assignment pins milan-fpga `2c532827`, but that commit holds only round 1's author packet. The round-3 packet `review-evidence/ppC6-r1/author-r3` is on branch `ppC6-review-evidence`, at commit `8fb13c82ee`. I read it there. That commit predates the archive of the other reviewer's round-3 report.

## Round-3 RTL: the press latch (`hdl/aecp/KL_aecp_notify.sv`)

Round 3 changes only `KL_aecp_notify.sv` in `hdl/`. It changes no top port, no top parameter and no module port (`receipts/diff_scope.txt`), and the top file is byte-identical to round 2's.

The new flop `prs_r` (`:728`) sits inside `gen_ident`, so it does not exist at `EN_IDENTIFY_NOTIF_P` = 0. It works as follows:

- **Set in WAITING** while the gap runs: `:810`, `if (btn_q2_r && gap_r) prs_r <= 1`.
- **Set outside WAITING** on a press after a release seen inside the burst: `:804`, `btn_q2_r && rel_r && (i_st_r != I_WAIT)`.
- **Cleared at both starts.** The WAITING start is `:811-817`, `(btn_q2_r || prs_r) && !gap_r`. The HOLD start is `:863`. Within the clock block the case statement's clear comes after the set at `:804`, so a start never leaves the latch set.
- **Every start still waits for `!gap_r`.** `gap_r` is set at every departure and cleared only by the IDENT-BURST expiry, so the inter-frame floor of round 2 is kept.

I traced every path by hand; the probes and mutants below confirm the reading:

- A press seen while a burst is already owed sets an already-set flop. It adds nothing.
- A release that is not followed by a new press leaves `rel_r` set and `prs_r` clear. I_HOLD then goes to WAITING with no burst owed.
- A held button with no release never sets `prs_r`, because the set needs `rel_r`. The 1 s re-arm path is therefore unchanged.
- The WAITING latch's `&& gap_r` term is redundant. When the gap is over, the start in the same cycle clears the latch, and that clear wins. My mutant `p_wait_latch_always` confirms this as an equivalent mutant (below). The redundancy is harmless.

**In-burst latch (judged).** IEEE 1722.1-2021 Figure 7-142 enters IDENTIFY from WAITING on `identifyButtonPressed`, and IDENTIFY's entry action is txIdentify, three frames 150 ms apart. A literal machine that ran txIdentify atomically would not see a release and a new press inside the burst, unless the button was still held at the timeout. The lane reads such a press as a new IDENTIFY entry and answers it at the gap's end. I accept this reading:

- It loses no press, and every new press after a release is answered, as WAITING answers every press.
- It never breaks the 150 ms floor between transmissions or the one identifySequenceID per burst.
- Its rate is bounded: one burst per three frames plus the gap, about 450 ms. That rate is reachable under the standard's own machine anyway, by a release and a press right after each burst.
- 06 §7 states it as a deliberate reading, and the manager accepts it.

## Evidence (all re-run here; receipts under `receipts/`)

Builds used the pinned simulator: Verilator 5.050 rev v5.050, wrapper sha256 `905795b9…` (`receipts/tool_identity.txt`). They ran on `git archive` exports in a disposable scratch area, at most 8 jobs at once. The reviewed clone was only read.

| What | Result | Receipt |
|---|---|---|
| `tb/pp_top` section ID (third build) at head | **178 checks, 0 failures** | `head_pp_top_identify.log` |
| ID8: a 30 ms press 2 ms after the third frame | one burst, 15,301 clocks after the third frame, first frame 166 clocks after the IDENT-BURST expiry (63 clocks into its ms) | same |
| ID8j-n: a press at the gap's end, k = -1, 0, 1, 2 | starts 166, 166, 166, 167 clocks after the expiry: the measure resolves one clock | same |
| ID9 / ID9e: the last byte held 400 ms | gaps 15,232 / 15,300, and 55,267 / 15,299 | same |
| The head's tests on round 2's `hdl/` (the failing arm) | **155 checks, 29 failures**, exactly as claimed. The lost presses are ID8, ID8o and ID8s (3 frames, want 6). The rest are the sequence_id knock-ons ID8g, ID8l, ID9b and ID9f, and the never-measured starts ID8i and ID8n | `failarm_head_tests_r2_rtl.log` |
| **My round-2 arms, re-run unchanged at head** (`scripts/r421_arms.py`) | 188 / 0. R421c, the 30 ms press that sent nothing in round 2, now sends its burst: 6 frames, 15,301 clocks after frame 3. R421d gives 15,301. The eof-beat stalls R421a and R421b give 15,232 / 15,300 and 55,267 / 15,299 | `r421_2_arms_at_head.log` |
| The same arms on round 2's RTL (control) | R421c sends 3 frames, so it FAILS; 164 checks, 30 failures | `r421_2_arms_on_r2_rtl.log` |
| **New: seeded random-press probe**, 16 campaigns of 200 steps; 8 add random MAC `tx_ready` stalls (974 stalls in total) | **all rc 0.** 3,200 press edges, 3,217 bursts (719 re-arms). Not one press lost, not one unexplained burst, and every burst byte-exact with one sequence_id each. Smallest inter-frame gap **15,230** clocks (>= 15,000). Stall-free press-to-first-frame is 167 to 46,004 clocks, inside the bound 3 × T-IDENT-BURST + 4 × SLACK = 46,600 | `random/` |
| The same probe on round 2's RTL | **all 16 FAIL** R421R3 (lost presses), 16 to 27 per campaign | `random_on_r2_rtl/` |
| Reviewer latch mutants (`scripts/r421_3_probes.py`, through the lane's own driver; golden PASS) | KILLED by section ID: `p_hold_keeps_prs` (ID3, ID5d…), `p_wait_keeps_prs` (ID8, ID8f…), `p_burst_latch_no_rel` (ID1, ID2…), `p_wait_keeps_rel` (ID2, ID2d…). The lane controls re-planted from my anchors are also KILLED: `c_press_not_latched` (ID8…), `c_burst_press_not_latched` (ID8o, ID8s), `c_wait_ignores_gap` (ID8c…ID8u). `p_wait_latch_always` SURVIVES section ID and the probe: it is equivalent by construction (above). At its default seed (no stalls) the probe kills 6 of the 7 non-equivalent mutants; it misses `c_press_not_latched`, which the 16-campaign run on round 2's RTL does catch | `latch_probes.stdout`, `latch_probes/` |
| The lane's full control campaign, `tb/pp_top/notify_mutants.py` | **40 of 40 KILLED** by their named checks, all five goldens PASS. Round 3's controls: `ident_wait_ignores_gap` (ID8c, ID8h, and 7 more), `ident_press_not_latched` (ID8…), `ident_burst_press_not_latched` (ID8o, ID8s), `ident_next_burst_at_once` (ID3f, ID7r, and now also ID8c…), `ident_departure_ignores_ready` (ID9d / ID9h: 63 clocks), `ident_burst_deadline_one_tick_short` (FT2: 14,900,004), `ident_t0_same_ms` (FT4: 99,900,004). Round 2's `ident_burst_from_t0` is KILLED (ID7i, ID5k) | `notify_mutants.stdout`, `notify_mutants/results.json` |
| `tb/aecp_notify`, both builds | **14 checks, 0 failures**. FT2 15,000,004, FT3 15,100,002, FT4 100,000,004 clocks | `head_aecp_notify_run.log` |
| New: FT departure-phase sweep (`scripts/r421_3_ft_sweep.sh`), phases 0, 1, 2, 3, 50000 and 99996-99999 | both lower bounds hold at every phase. Departure to next job is at least 15,000,004 clocks (phase 99998); first frame to re-arm is at least 100,000,003 clocks (phase 99999) | `ft_phase_sweep_head.txt` |
| `tb/pp_top`, all three builds | **8,242 checks, 0 failures** (default 8,044, fixture 20, identify 178) | `head_pp_top_full.log` |
| `scripts/lint_hdl.sh` | rc 0, every module LINT OK | `lint_hdl_head.log` |
| `KL_aecp_notify`, `KL_aecp_engine` and `protocol_processor_top` at `EN_IDENTIFY_NOTIF_P` = 1 (the script's flags) | LINT OK ×3 | `lint_en1.log` |
| `make check`; `python3 scripts/gen_matrix.py --check` | rc 0 (lint 41 + 18 blocks, links 999, matrices, parameters 27 = 27 = 27); rc 0 (94 rows, 0 untested) | `make_check_head.log`, `gen_matrix_check_head.log` |
| `git diff --check` over base..head and r2..head | rc 0 and rc 0 | `diff_scope.txt` |
| Hosted checks at head (read-only query, 20:16Z) | `docs-gates` success, `portability` success. `suites` was still **in_progress**: not executed to a conclusion when queried | `hosted_checks_9624ef4.txt` |

The author's round-3 receipts agree with these figures: run_suites 1,018,160 / 0, notify 40/40, FT 4/4, lint at 1 clean, module synthesis +1 FF at 1.

## Findings

No MINOR, MAJOR or BLOCKER finding is open.

### S1 [SUGGESTION] (Tests): FT4 could also grade a departure on a ms's last clock

- **Where:** `tb/aecp_notify/sim_main.cpp`, `IdentHarness::run`. FT4 measures the re-arm from frame 1 leaving at phase `END` = 99,998.
- **Evidence:** `receipts/ft_phase_sweep_head.txt`. The re-arm margin is 4 clocks at phase 99,998 and **3 clocks at phase 99,999**. t0 is taken from `now_ms_i + 1` at the departure edge, not through an arm on the next clock. The bound holds at every phase swept, and `ident_t0_same_ms` is KILLED anyway.
- **Impact:** none on correctness. FT4 does not sample the tightest phase of its own margin.
- **Suggested outcome:** add phase 99,999 to FT4, or note in the README that FT2's phase is the tightest for the burst gap and phase 99,999 for the re-arm.
- **Verification:** `scripts/r421_3_ft_sweep.sh`.

## Prior public review findings at this head

All read after my verdict and ledger were fixed.

| Finding | State at 9624ef4c | Evidence |
|---|---|---|
| **R421-2 F1 / R420-2 F1** (MINOR, the same defect: a press in WAITING inside the post-burst gap sends nothing) | **RESOLVED**, outcome (a): the latch | `prs_r` at `:728`, `:804`, `:810-817`, `:863`. Section ID8 has the short and long press in the gap, the press at the gap's end and either side of it, and both in-burst cases. My R421c now sends its burst (15,301). The random probe loses no press in 3,200 presses, and loses 16-27 per campaign on round 2's RTL. The single-guard control `ident_wait_ignores_gap` is KILLED by ID8c and ID8h. `ident_next_burst_at_once` is kept and KILLED. The docs now state the behaviour, including a press released before a running burst ends: operator guide row, integrator guide §6, 06 §7 and F06.16, F08.1 T-IDENT-BURST, 09 §8.3, `tb/pp_top/README.md` ID8 |
| R421-2 S1 (the departure's `ready` term never graded) | **RESOLVED**, taken | ID9-ID9h; `ident_departure_ignores_ready` KILLED (ID9d / ID9h, 63 clocks); my R421a / R421b give 15,232 / 15,300 and 55,267 / 15,299 |
| R421-2 S2 / R420-2 S1 (the one-tick floors by inspection only) | **RESOLVED**, taken | `tb/aecp_notify` section FT at 100,000 clocks per ms. `ident_burst_deadline_one_tick_short` (FT2) and `ident_t0_same_ms` (FT4) KILLED. My phase sweep holds both floors at nine phases; S1 above is a refinement only |
| R420-2 S2 (stale "two builds" comment) | **RESOLVED** | `tb/pp_top/sim_main.cpp` header and tally comment say three. The `tb/aecp_notify` comment correctly says two |
| R421-1 F1 / R420-1 F1 (MINOR, frames scheduled from t0 bunch) | **RESOLVED** (unchanged since round 2) | ID5i-l and ID7 pass with values unchanged; `ident_burst_from_t0` KILLED in my campaign; random-stall campaigns: minimum gap 15,230 |
| R420-1 F2 (MINOR, the CDC rule) | **RESOLVED** (unchanged) | `docs/guides/hdl-engineer.md:64`, `hdl/README.md:25`, `ASYNC_REG` at `KL_aecp_notify.sv:718-719` |
| R421-1 S1 (release and press inside a burst) | **RESOLVED** | Now latched for a press released before the burst ends too (ID8s), and stated in 06 §7 |
| R421-1 S2 / R420-1 S2, R421-1 S3, R421-1 S4 / R420-1 S3 | **RESOLVED** (unchanged since round 2) | As recorded at round 2; round 3 does not touch them |
| R420-1 S1 (three controls survive by design), R420-1 S4 (the limiter's one-tick reading) | **Retained, recorded** | `tb/pp_top/README.md:1556` and `:1472`, with reasons. Acceptable for SUGGESTIONs |

## Lens results (artifact-specific)

- **Conformance: CLEAN.**
  - Figure 7-142 WAITING answers every press after a release. That covers the gap press, the gap-end press, a press inside a burst, and one released before the burst ends (ID8, ID8j-n, ID8o, ID8s; random R421R3).
  - §7.5.1's 150 ms between transmissions holds on the wire: minimum 15,230 clocks over 3,217 random bursts with stalls. FT2 and FT3 show it at the full timebase.
  - §7.5.1.2.1's one identifySequenceID per burst, +1 per burst, holds (R421R1; ID8b/g/l/p/t).
  - The re-arm is no sooner than T-IDENT-REARM (FT4; the phase sweep; R421R5).
  - The in-burst latch reading is judged acceptable (above).
- **RTL: CLEAN.**
  - `prs_r` set and clear paths are traced above; each clear is exercised by a KILLED mutant.
  - The `!gap_r` gate is on both starts.
  - Nothing is built at 0. Lint is clean at 0 and 1.
  - No port, parameter or register change.
- **Robustness: CLEAN.**
  - Random press patterns from 1 ms to 2.5 s, with and without random MAC stalls, show no lost press, no spurious burst and no short gap.
  - The last-byte stall (ID9, R421a/b) shows no bunching.
  - Deadline arithmetic is graded at the silicon timebase.
- **Tests: CLEAN.**
  - Section ID 178/178. The failing arm on round 2's RTL is reproduced (29/155).
  - 40/40 lane controls KILLED. The assigned controls are present: the single-guard control, both latch removals, `ident_next_burst_at_once` kept.
  - The three observe-only wrapper taps are test RTL only (`tb/pp_top/pp_top_wrap.sv`), and the default build compiles and passes with them.
  - S1 is a suggestion only.
- **Docs: CLEAN.**
  - The operator guide row, integrator guide §6, 06 §7 and the F06.16 note, F08.1, 09 §8.3, the RTL banner and both suite READMEs agree with the RTL and with one another.
  - The README figures (15,301; 166/167; 15,232/15,299; FT 15,000,004 / 15,100,002 / 100,000,004) match my runs.
  - `make check` passes.

## Ruling conditions and issue closure at this head

- **STOP boundary.** No top port or parameter change in round 3. `prs_r` is internal, inside the identify generate. The test wrap's three `dbg_ident_gap_*` outputs are processor test code.
- **#80 ruling, conditions 1-4.** Condition 1 (default 0, zero area): met; the new flop is in the generate not built at 0. Condition 2 (synchronised, debounce duty stated): met. Condition 3 (parent-visible list): unchanged; the combined patch carries it. Condition 4 (both settings graded): met at 0 (ID0 in the default build) and at 1 (section ID, FT, 40 controls).
- **#54:** acceptance 1-4 met. The gap that blocked item 2 at round 2 is closed.
- **#58:** 1-3 met; unchanged this round. NP passes in the default build, and the class controls are KILLED.
- **#80:** 1-4 met. ST and RN pass in the default build, and their controls are KILLED.
- **#86:** 1-4 met. `tb/originator`'s golden passes in the campaign, and the inflight controls are KILLED.
- **Closing.** `Closes #54 #58 #80 #86` is supported at this head, subject to the manager's duties below.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_aecp_notify.sv` identify sequencer (`:700-875`) against IEEE 1722.1-2021 §7.5.1, §7.5.1.2.1, Figure 7-142 and Milan §5.4.5.4. Section ID8/ID9 and FT output; random probe R421R1-R5 | R421-3 | 9624ef4c452d708de68a901d5e645bdfa1f5d6f5 |
| RTL | CLEAN | `git diff 88e0bf8..9624ef4c -- hdl` (one file); `prs_r`/`rel_r`/`gap_r` paths; lint at 0 and 1; diff scope (no port or parameter lines) | R421-3 | 9624ef4c452d708de68a901d5e645bdfa1f5d6f5 |
| Robustness | CLEAN | 16 seeded random-press campaigns (8 with 974 MAC stalls in total); the eof-beat stall arms; the FT phase sweep | R421-3 | 9624ef4c452d708de68a901d5e645bdfa1f5d6f5 |
| Tests | CLEAN | `tb/pp_top/notify_phases.hpp` ID8/ID9, `pp_top_wrap.sv` taps, `sim_main.cpp`, `tb/aecp_notify/sim_main.cpp` FT and Makefile, `notify_mutants.py` (40/40), the failing arm, 8 reviewer mutants, the full `tb/pp_top` 8,242 | R421-3 | 9624ef4c452d708de68a901d5e645bdfa1f5d6f5 |
| Docs | CLEAN | `docs/guides/operator.md:50`, `docs/guides/integrator.md:298-311`, `docs/architecture/06_aecp_engine.md:781-800` and the F06.16 note, `08_timing.md:30`, `09_verification.md` §8.3, `tb/pp_top/README.md` ID, `tb/aecp_notify/README.md`, the RTL banner; `make check` | R421-3 | 9624ef4c452d708de68a901d5e645bdfa1f5d6f5 |

## Real limits

- Simulation only. Physical calibration was NOT RUN, and no hardware was used; field skips are not hardware proof.
- The identify sequencer exists only at `EN_IDENTIFY_NOTIF_P` = 1, which the parent does not use.
- I did not run these: the full processor `run_suites.sh` bank, the other campaigns (d3, acmp, adp, maap, srp, gsi, retry, nvm figures), yosys, the parent consumer set, the donor bank, the builder, Docker/act or the hosted jobs. Those are banks outside a focused review. I read the author's receipts for them.
- I ran the focused suites the round touches: `tb/pp_top` (all builds), `tb/aecp_notify` (both builds), lint, docs gates and the matrix. `tb/originator` ran only as the campaign's golden.
- The random probe judges the wire against invariants, not a cycle-exact model. In stall mode its attribution of a press to a burst is relaxed in two stated ways (see the script header and code comments): a press inside a burst whose first frame a stall delayed, and a re-arm decided before a stall. Stall-free mode is strict. At its default seed the probe alone misses `c_press_not_latched`. The 16-campaign run catches the round-2 defect in every campaign.
- The pinned evidence commit in the assignment (`2c532827`) does not contain `author-r3`; I read it at `8fb13c82ee` on `ppC6-review-evidence`.
- In my receipts, the simulator's host install path is replaced by `<PINNED_VERILATOR_PREFIX>`.
- The reviewed clone was verified after the probes (`receipts/clone_verification.txt`):
  - HEAD and tree are exact, and the status is empty;
  - the index equals HEAD in modes and blobs, and the work-tree blob hashes equal the index;
  - this repository has no submodule gitlinks and no `.gitmodules`.

## Pending manager duties

- Hosted acceptance at this head: the `suites` job was in progress when I queried it. The manager owns hosted and act acceptance.
- The donor bank and the parent consumer set at milan-fpga dev `7f0927bb`, with the combined C4 + C6 parent patch.
- The merge-turn final current-dev candidate (source base `3f3ea56b`, live dev `7f0927bb`). The merge-only round onto processor main (`16ea10ac` and C5a) needs its own delta review.
- A second independent positive review, before merge.

## Receipts

`MANIFEST.sha256` lists every published file. Scripts are under `scripts/`:

- `run_r421_3.sh`: the reproduction;
- `r421_3_random.py`, `run_random.sh`: the random probe;
- `r421_3_probes.py`: the latch mutants;
- `r421_3_ft_sweep.sh`: the FT phase sweep;
- `r421_arms.py`: round 2's arms, unchanged;
- `verilator-j8.sh`: the job-capped simulator wrapper.

R421-3 FINISHED
