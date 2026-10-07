[R474] NEGATIVE - exact head 886e16201654ba0fd0c60c41c228ea4c75b2f6d3

# R474-2: internal cleared-context review of PR #672 (Closes #645, #647), round 2

- **Head and tree.** Head `886e16201654ba0fd0c60c41c228ea4c75b2f6d3`, tree `f2eb9b9b349fd5a1c13df31143c7e20df40e1ba7`. Second parent: live dev `09f1841bd2c6a9dea8eb1994d887f7386ca4f62d`. Source base: `fea346e76c2a57ed5cd131af8fc68dfeff57f877`. Gitlinks: protocol-processor `ead80360`, gptp-processor `5dce647a`, verilog-axis `48ff7a7e`.
- **Reconstruction order.**
  - AGENTS.md, CONTRIBUTING.md and docs/README.md.
  - The #645 and #647 bodies.
  - The round-2 rulings: 6009543884 (symmetric action, sub-arm pulls, traceability, the disengaged text, the dev merge, area), 6009767440 (the two-PDU span), 6010634115 (the quiet band, recovery qualification, the declared residual) and 6009790232 (the timing bar).
  - The earlier scope rulings cited by the design page.
  - `MEDIA_CLOCK_FOLLOWING.md`, `TIME_SYNC.md`, `REGISTER_MAP.md`, `TESTING.md` and the milan_dp README.
  - The PR diff against live dev (38 files), and the round-2 delta `4e1ddee9..886e1620`, split with `--first-parent`: six lane commits and seven `--no-ff` dev merges.
  - The author's public round-2 packet `review-evidence/645-r1/author-r2c` at `b6f28906` (HANDOFF, PR body, quiet-distribution JSON, area comparison, small-pull logs). I did not read the later archive commit `77b6cc89`, which holds the concurrent external round.
  - The [A531] REVIEW READY comment, 6031559796.
- **Prior findings.** I read the prior public findings (R474-1 6009527655 and R475-1 6009109435) only after my own pass over the diff and my probes were complete. Each one is resolved or retained below.
- **Verdict: NEGATIVE.** One MINOR finding is open: a declared settle hold can increment `SLIP_LB`'s dup half. It was reproduced by a probe, and the head's suites do not catch it. Everything else the rulings asked for holds at this head under my own execution, including every ruled behaviour in the focus list. There are also two RESIDUE wording fixes and three suggestions.

## Findings

### F1 MINOR: a declared settle hold on a pair that is still empty is counted as a loopback dup

- **Lenses:** Conformance, RTL, Robustness, Tests, Docs.
- **Where:** `hdl/ieee1722/aaf/KL_chan_map_capture.sv:894-895`. `pop_dup_w` is `pop_visit_w && q_primed_r && q_fed_r && (pop_cnt_w == '0)` and does not exclude `pop_hold_w` (`:885`). It feeds `dup_sum_w` (`:967`).
- **Authority:**
  - Ruling 6009543884 item 1: the action carries "the same lockstep, counter and accounting guarantees as the hold".
  - Ruling 6009767440: "the slip counters stay unchanged".
  - The head's own contract states this in four places. `docs/design/MEDIA_CLOCK_FOLLOWING.md:1096`: "On the loopback ring neither `SLIP_LB` counter moves". `:1234-1236`: "neither `SLIP_LB` counter increments for that step". `docs/reference/REGISTER_MAP.md:1870`: "held pops ... count in neither half". `tb/verilator/milan_dp/README.md:219`: "unchanged loopback slip counters".
  - The physical checker fails on any counter change across a declared action (`tb/verilator/milan_dp/sim_ax1x1gptp.cpp:753`, `:1100`).
- **Evidence:** probe P1 (`probes/probe_lrc_empty_hold.py`, `receipts/probe_p1/`). It adds one case to a copy of the [LRC] block; the RTL is unchanged.
  - The queue is drained to zero left, then the recentre is pulsed. Only the new PDU's first beat is driven (pair 0's event), and a walk runs before pair 1's first commit.
  - **With the declared hold, the dup counter moves by 1.** The control without the pulse moves it by 2. The suite's own "LRC: no recentre moved the dup counter" then fails with 0x3.
  - The existing [LRC] "none left holds five" case lands the whole PDU before ticking, so it cannot reach this state. The unchanged head suite passes 777/0 (`receipts/head/chmap_capture_head.log`).
  - On the 1x1x8 lane, pairs 1 to 3 commit their first event of a PDU one to three wire beats after the decision beat. Any walk whose LOOP pre-walk falls in that gap, with nothing left of the previous PDU, counts one dup per still-empty pair.
  - "Nothing left" is the empty-edge state the recentre exists to correct (#645), and the INTERNAL beat sweeps the ring's margin through zero (`receipts/quiet/b8_6p25MHz_head.log`: margin +0.008..+1.006 ticks at INTERNAL).
- **Impact:**
  - The repeats on the wire are exactly the declared five, but `SLIP_LB` reports a slip for one of them.
  - A bench or physical run that hits this phase reads a non-static `SLIP_LB` across a declared recentre. That is the acceptance signal #645's bench item and REGISTER_MAP use ("a word static from it on is the acceptance state"), and the physical checker would fail on it.
- **Disposition of the prior suggestion.** R474-1 S1 raised this case as a SUGGESTION. I retain it and raise it to MINOR, because the round-2 rulings made unchanged counters an explicit part of the action's contract and the head's documents now assert it without exception.
- **Required outcome:** one of the following:
  - The settle action's held pops never move either counter. For example, a held walk is not counted as a dup, whatever the pair's fill.
  - Or a ruling declares the case, and `MEDIA_CLOCK_FOLLOWING.md`, REGISTER_MAP 0x8D4, the milan_dp README and the physical checker's counter rule all state and account for it.
- **Verification:**
  - Probe P1's pulsed variant shows dup delta 0 (or the declared value).
  - A standing [LRC] case drives a walk between the decision beat and a pair's first commit at zero left.
  - A planted control that counts held pops as dups fails that case. My HOLDDUP plant (below) already fails the existing [LRC] and SPAN counter checks; the new case must fail too.

### R1 RESIDUE: the TIME_SYNC prose omits the declared recovery-window exception

- **Lenses:** Docs (wording only).
- **Where:** `docs/design/TIME_SYNC.md:489-492`. It reads: "A settle recentre follows each change and each pull-in. ... Nothing moves the stage after it."
- **Why it is wording only:** the authoritative row at `TIME_SYNC.md:386` and `MEDIA_CLOCK_FOLLOWING.md:1135-1149` state the residual correctly. The fix changes no measurement, figure, test, code or clause claim.
- **Exact fix:** replace line 489 with "A settle recentre follows each change, and each pull-in that starts outside a previous action's recovery window." Replace line 492 with "Outside that declared residual, nothing moves the stage after it."

### R2 RESIDUE: the 0x8D4 row says "dropped event" for a drop of up to eleven

- **Lenses:** Docs (wording only).
- **Where:** `docs/reference/REGISTER_MAP.md:1870`. It reads: "The #645 settle recentre's own held pops or dropped event count in neither half".
- **Exact fix:** "The #645 settle recentre's own held pops or dropped events count in neither half". This is separate from F1, which concerns whether the claim is true.

### Suggestions (non-blocking)

- **S1 (Tests): the floor of the quiet band is not pinned against the shipped constant.**
  - My plant BAND1 (`SETTLE_EXC_ERR_C = 1`, below "twice the largest quiet excursion") survives:
    - `settle_control.py` at all four rates;
    - the 25 MHz no-hold quiet leg;
    - b8 at 6.25 MHz, 48/0, including every [STEADY] check;
    - the 25 MHz cross-2044 pull.
  - The two-times rule is enforced only by `quiet_distributions.py --band 2`, whose band is typed by hand rather than read from the RTL.
  - Fix: make `settle_control.py` assert that |err| = 2 never arms, or have the reader take the band from `milan_datapath.sv`.
- **S2 (Tests, Docs): the shipping clock has no standing quiet or latency evidence.**
  - The measured 128-phase distribution is at 6.25 MHz only, as the page says (`MEDIA_CLOCK_FOLLOWING.md:1109`).
  - My probes find ±1 axis cycle everywhere I looked:
    - 25 MHz at per-tick resolution: both signs, no lateness, 0 to 60 us, and the 24 us tail (seven windows);
    - 50 MHz at INTERNAL at per-tick resolution (3 s);
    - 50 MHz under AAF following, after LOCKED, at 1 ms resolution (1.6 s; the run was cut by the wall limit before its settle);
    - 100 MHz at INTERNAL at 1 ms resolution.
  - Under the shipped arm there was no false pulse, arm or pending flag in any of these windows (`receipts/quiet/`).
  - At 50 and 100 MHz the INTERNAL pull-in's settle fires **1.20 to 1.33 s** after the hold, against 0.19 to 0.85 s at 6.25 MHz (`receipts/recovery/`).
  - Fix: a standing 50 MHz quiet window, and the shipping-clock pull-in latency stated beside the 6.25 MHz figures.
- **S3 (Tests): the physical leg can pass without a recentre decision.** This retains R474-1 S2. `tb/verilator/milan_dp/sim_ax1x1gptp.cpp:1101` still prints `NOT RUN: declared recentre checks (no decisions; uncounted)` and passes. Startup always yields a decision, so the leg could require at least one.

## Focus items, judged at this head

| Item | Result | Evidence |
|---|---|---|
| **Symmetric action** | Holds. Fewer than five left: holds `5 - left` pops (at most five). More than five: drops exactly `left - 5` before the pop, clamped so a pair can never underflow. All pairs take one stream decision in the same walks. Both widths cover their maxima: 3 bits for 5, 4 bits for 11. A same-cycle push composes with `pop_n_w`. A flush clears the arm, decision and actions. | RTL `KL_chan_map_capture.sv:808-815, 877-913, 939-959, 1051-1081`. Head [LRC] and SPAN 777/0. My plants NODROP and NOHOLD each fail 4 to 5 [LRC] cases plus the SPAN check. Full side at 25 MHz, fast sign: margin +5.007..+5.009 after the settle (`receipts/quiet/b8_25MHz_fast.log`). |
| **Slip counters during the action** | Hold: **not met in one phase** (F1). Drop: met. | P1. Plants HOLDDUP and DROPSKIP are both caught by "LRC: no recentre moved the dup/skip counter" and "SPAN: no action counted as a duplicate/skip". |
| **Consecutive, two-PDU span** | Matches ruling 6009767440. The physical checker allows at most `output_pdu + 1` and consecutive wire slots. Six phases and a two-talker fanout run with offsets 0 to 5, with three controls. | `sim_ax1x1gptp.cpp:739-760`. Head log: SPAN CONTROL nonconsecutive, third-PDU leak and extra repeat are each rejected. NODROP and NOHOLD fail the SPAN check. |
| **Excursion arm, 2-cycle quiet band** | Holds. `settle_exc_w = engaged && |err| > 2`. The 320/80/40/20 ns table is the same 2 cycles at each clock. The 320,462,699 samples in the author's JSON add up across the eight groups, all within ±1. I found ±1 at 25/50/100 MHz (S2). | `milan_datapath.sv:6599-6600`. Plant BAND8 is caught by `settle_control` ("excursion did not arm"); BAND1 is not (S1). |
| **Recovery qualification, 2,048 quiet ticks** | Holds. While recovering, any out-of-band cycle or disengagement restarts the shared counter, and the arm is blocked until 2,048 counted ticks. A source change or re-engagement still arms at once. | `milan_datapath.sv:6602-6604, 6641-6651`. Plants REARM64 and REARM512 are caught by `settle_control` ("re-armed before quiet dwell"). REARM64 also fails the physical legs: two actions from one hold, [STEADY] false pulse, the [TWO-PULL] side check and the [RESIDUAL] checks (`receipts/plants/`). |
| **Declared residual** | Honest, and it matches the ruling's scope. The page declares it only for a second INTERNAL pull that starts after an action and before re-arm (`MEDIA_CLOCK_FOLLOWING.md:1135-1157`). It gives the worst *observed* isolated window (0.551148640 s) over a named stimulus set, and says plainly that continuing disturbance has no finite bound. The ruling's "worst-case length" exists only as that observed figure plus the unbounded statement, and the page says so rather than presenting the observed figure as a bound. The two-pull case grades both sides, against the actual recovery state. | I reproduced **0.551148640 s** exactly (6.25 MHz, 56 us hold). At 50 and 100 MHz the isolated window is the 42.667 ms minimum, inside the declared figure. Head small pulls 10/10, including second-inside (no second action, final OFF THE LAW, declared) and second-outside (one action, on the law). |
| **AAF presentation law unchanged; 56 us slip count** | Holds. `KL_render_setpoint.sv` and the render law (fill 14, delay (8, 9]) are untouched. At 56 us, exactly **4 of 16** phases (p00 to p03) slip once before the settle. At 52 us, none. 32/32 runs pass with zero post-settle slips. This matches `MEDIA_CLOCK_FOLLOWING.md:1209-1214`. | `receipts/sweeps/h52`, `receipts/sweeps/h56`. |
| **Traceability credits compiled sources only** | Holds. `compiled_basenames` drops lines marked `# traceability-text-input:`, and `follow_ring/Makefile` marks `milan_datapath.sv`. `--check` returns rc 0 with 7/7 generator controls. `milan_datapath`'s row does not name `follow_ring`. | `receipts/gates/module_matrix.log`. Hosted `docs-check` at this head: success. |
| **Area: 82 FF and 119 LUT against 120/120** | Measured by the author; not re-run by me. My hand count agrees with the FF rows: the settle block has pend, recover, an 18-bit run, a 21-bit ceiling and a pulse, 42 FF (= 93 - 51); the capture rows give 40. The LUT margin is one. | `round2c/area-ooc/comparison.json` at `b6f28906`. |

## Prior public findings at this head

| Prior finding | Status | Evidence |
|---|---|---|
| R474-1 F1 MAJOR: one-sided recentre | **Resolved** | Full-side drop of `left - 5`. [LRC] "ten left drops five", with the author's SINGLE-DROP control. Fast-sign campaigns. My NODROP plant is caught. Fast-sign runs centre the ring. |
| R474-1 F2 MAJOR: sub-arm INTERNAL pulls | **Resolved** | 2-cycle arm. 1/64-sample harness quantum (`FRAME_DIV 64`). cross-2042/44/46 standing cases with the NO-ARM control; I ran them 10/10. |
| R474-1 F3 BLOCKER / R475-1 F3 MINOR: stale traceability | **Resolved** | `gen_module_matrix.py --check` rc 0 locally and in hosted `docs-check`. The text input is not credited. |
| R474-1 F4 MINOR / R475-1 F2 MINOR: disengaged INTERNAL "at once" | **Resolved** | `MEDIA_CLOCK_FOLLOWING.md:1092` now reads "or has remained disengaged for the same 2,048 ticks", which matches `settle_need_w`. |
| R475-1 F1 MAJOR: hold spans two output PDUs | **Resolved by ruling** 6009767440 | The declaration is now two consecutive PDUs. The checker uses `output_pdu + 1`. Six-phase and fanout span checks run with three controls. |
| R474-1 S1: held empty walk counts a dup | **Retained, raised to MINOR** | Now F1, above. |
| R474-1 S2: physical leg passes with no decision | **Retained as a SUGGESTION** | Now S3. |

## Independent execution at this head

All runs used Verilator 5.050 (`receipts/env/identity.txt`) on a `git archive` export of the head. The commands are in `probes/r474_commands.sh`; every run is in `receipts/`.

| Run | Result |
|---|---|
| `chmap_capture` | 777 checks, 0 failures, including [LRC], SPAN at six phases and the fanout, and the SPAN controls |
| follow_ring b8 at 6.25 MHz (INTERNAL to AAF, then AAF to CRF and CRF to AAF) | 48/0. One settle per transient, 4.096 s after LOCKED. Quiet windows ±1 cycle. No slip after the settle. Ring +5.55 ticks. Render on the law. |
| follow_ring b8 at 25 MHz: slow and fast sign; 60 us slow and fast; 2 us plus the 24 us tail | All PASS (the three lateness runs 17/0 each). Quiet ±1. Settle on time. Fast sign centred from the full side. |
| `small_pulls.py` at 25 MHz | 10/10 |
| INTERNAL pull-in sweeps at 52 and 56 us, 16 phases each | 32/32. At 56 us four phases slip once before the settle; at 52 us none. Zero after. |
| Pull-ins at 6.25, 50 and 100 MHz, 52 and 56 us | 6/6 PASS. Recovery windows 0.042667 to 0.551149 s. Shipping-clock settle 1.20 to 1.33 s after the hold. |
| 50 MHz INTERNAL with no hold | 10/0. ±1 over 143,999 ticks. No pending flag. |
| Probe P1 (F1) | dup +1 under a declared hold (control +2) |
| Reviewer plants, capture | NODROP, NOHOLD, HOLDDUP and DROPSKIP: **4/4 caught** by named [LRC] or SPAN checks |
| Reviewer plants, datapath | BAND8, REARM64 and REARM512: **3/3 caught** by `settle_control`. REARM64 is also caught by three physical legs. BAND1 **survived** (S1). |
| Read-only gates in the review checkout | `lint_rtl --check` PASS (90 <= 90); doc style; doc paths; RTL source lists; module matrix; SV idiom; Python idiom, all rc 0. `check_em_dash` could not judge (its pinned renderer is absent here), but a scan of the added lines finds no U+2014. |
| Merge audit | Six of the seven dev merges equal an automatic `merge-tree` of their parents. `132d79e7` carries a manual resolution of `tb/verilator/milan_dp/Makefile` (union of .PHONY, the lane's `ax1x1gptp-build` beside #658's dynmap targets) and `scripts/measure_test_evidence.py`. The readers entry moved into dev's `measure_test_evidence_readers.py`, as ruled in 6009543884 item 5 (`receipts/merges.txt`). |
| Hosted, exact head (read only) | Success: rtl-fast, docs-check, docs-check-no-git, elaborate, lint, firmware-unit, full-ci-gate, Yosys 4/4, and Verilator shards 0, 2, 3 and 4. **In progress** at the snapshot: Verilator shard 1/5. **Skipped, not executed:** Physical gPTP (`receipts/hosted_checks_886e1620.txt`). |

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #645/#647 acceptance; rulings 6009543884, 6009767440, 6010634115, 6009790232; `MEDIA_CLOCK_FOLLOWING.md:1036-1262`; the symmetric action, span, band, recovery and residual against RTL and runs; 56 us count; unchanged render law | R474-2 | 886e16201654ba0fd0c60c41c228ea4c75b2f6d3 |
| RTL | UNCLEAN (F1) | `KL_chan_map_capture.sv:225-255, 458-520, 808-1100`; `milan_datapath.sv:1215-1315, 6015-6030, 6495-6668`; widths, reset, flush, same-cycle composition; four capture and four datapath plants | R474-2 | 886e16201654ba0fd0c60c41c228ea4c75b2f6d3 |
| Robustness | UNCLEAN (F1) | mid-PDU walk at zero left (P1); both offset signs; 0 to 60 us and tail lateness; 6.25/25/50/100 MHz quiet and recovery; second pull inside and outside recovery; flush and first-beat [LRC] | R474-2 | 886e16201654ba0fd0c60c41c228ea4c75b2f6d3 |
| Tests | UNCLEAN (F1) | `follow_ring` (sim_main, sweep, small_pulls, settle_control, quiet_distributions, recovery_watch, mutants, dp_glue); `chmap_capture` [LRC]/SPAN; `sim_ax1x1gptp.cpp` plan/span/counter oracle; `verify_recentres.py`; builder mutant; generator selftest; 8 reviewer plants (7 caught, BAND1 survives: S1) | R474-2 | 886e16201654ba0fd0c60c41c228ea4c75b2f6d3 |
| Docs | UNCLEAN (F1; R1 and R2 are RESIDUE) | `MEDIA_CLOCK_FOLLOWING.md` settle section and declared transient; `TIME_SYNC.md:386, 489-492`; `REGISTER_MAP.md:1870`; `TESTING.md`; milan_dp README:205-240; MODULE_MATRIX and README-tests rows; PR body and REVIEW READY | R474-2 | 886e16201654ba0fd0c60c41c228ea4c75b2f6d3 |

All five lenses were applied this round. Each is UNCLEAN only because F1 is attributed to every lens: the documents state a counter guarantee that the head's RTL does not keep in one phase. No lens is left unclean by anything else.

## Real limits

- **No hardware or bench claim.** There is no physical calibration (NOT RUN), and no field, bench or vendor-implementation run. The Arty builder arm is a known, unchanged gap. Skipped hosted contexts are not evidence.
- **Not re-run by me:**
  - the full parent, PP, gPTP, Yosys and builder banks;
  - the 128-run arrival campaign (I used 7 targeted 25 MHz windows and the author's JSON);
  - the author's `mutants.py` (I ran my own plants instead);
  - the physical gPTP leg and `verify_recentres.py`;
  - the render pull-in and LAW-boundary legs;
  - timing and area.
- **Partial runs.** The 50 and 100 MHz b8 runs were cut by the 10-minute wall limit. Their following-mode evidence is post-LOCKED, pre-settle and sampled at 1 ms. Long-term quiet at the shipping clock under following is therefore not shown by me (S2).
- **Out of scope as ruled:** #657's render-mutation failures, and the declared second-pull residual itself (only its declaration was judged).

## Pending manager duties

- A fix or ruling for F1, then re-review of the corrected head under every lens.
- R1 and R2 carried to the residue checklist.
- The exact-head hosted Verilator shard 1/5 to completion, and Physical gPTP, which was skipped (hosted and act acceptance).
- The final current-dev candidate build and validation at the merge turn.
- The BUILDING.md section 5 timing gate and the own-area figures, which I judged only as published.
- Two independent POSITIVE reviews and an all-lens ledger at the merge candidate.
- Explicit merge authorization and post-merge containment.
- The issues' physical bench items. "Closes #645/#647" must not discharge those bench items.

## Restoration

- No source edit, commit, push or GitHub write was made. All probes and plants ran in disposable copies under this packet's `scratch/`.
- A `scripts/__pycache__` directory created by the read-only gates was removed.
- `probes/verify_checkout.py` then passed (`receipts/env/checkout_verify.json`):
  - 1,162 tracked blobs, with bytes and modes equal to the index;
  - the index tree equals HEAD's tree, `f2eb9b9b`;
  - gitlinks protocol-processor `ead80360`, gptp-processor `5dce647a` and verilog-axis `48ff7a7e`, with all three submodule worktrees clean;
  - `git status --ignored` is empty.

R474-2 FINISHED
