[R474] NEGATIVE - exact head 4e1ddee9d7b9ebf58ebebcacd90c5d72dce0c96f

# R474-1: internal cleared-context review of PR #672 (Closes #645, #647)

- Head `4e1ddee9d7b9ebf58ebebcacd90c5d72dce0c96f`, tree `1cb3772cf102a9296b4fea2db7096315c3c76360`. Source base `fea346e7`; the PR's own diff was read against live dev `28f9666f` (28 files, +3045/-93). Submodule gitlinks: protocol-processor `ead80360`, gptp-processor `5dce647a`, verilog-axis `48ff7a7e`.
- Reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, #645 (body and the rulings 5982568394, 5985974804, 5987852678, 5990646410 and 5994641859), #647, the PR body, the diff and its history, and the public evidence packet `review-evidence/645-r1` at `6efdd244`.
- Prior public review findings on PR #672: none. At the start of this round (03:38Z) the PR carried only the review-start notice, so nothing earlier needs to be resolved or kept. A concurrent external report was posted at 04:05Z, during this round. I read it only after this verdict, these findings and the ledger were written; see the last section.
- Verdict: **NEGATIVE**. Two MAJOR functional gaps came from my own probes. One required merge context (`docs-check`) fails at the exact head, and live dev passes it. There is also one MINOR documentation error.

## Findings

### F1 MAJOR: the loopback settle recentre centres only from the empty side

- **Lenses:** Conformance, RTL, Robustness, Tests, Docs.
- **Where:** `hdl/ieee1722/aaf/KL_chan_map_capture.sv:945` and `:1052`. An "over" decision becomes one drop (`pop_drop_w`, `:886`), described at `:242-244` as "one event toward the target". The campaigns cover one offset sign only: `tb/verilator/follow_ring/sweep.py:70-80` passes no peer offset, so every b8 run uses `sim_main.cpp:131`'s -11.02 ppm against the DUT's -5.10 ppm.
- **Authority:** the depth ruling 5987852678 says "Sixteen entries with the fill centred give about five ticks on each side". `docs/design/MEDIA_CLOCK_FOLLOWING.md:1155-1157` says that after the settle recentre the loopback ring is centred and that anything else "must not happen". The harness's own check is "[B8] the loopback ring is centred after the settle recentre".
- **Evidence:** I ran the shipped follow_ring model, unmodified, with the offset sign reversed: the peer at +0.82 ppm and the DUT's INTERNAL clock at -5.10 ppm, so the DUT reads 5.92 ppm slow. The ring parks at its full edge during the INTERNAL dwell, with left = 10 at the PDU start.
  - At the settle recentre the decision is "over", so one event is dropped. The ring stays at margin 9.19 to 9.95 ticks against the (5, 6] target.
  - The full-side margin is **1.121 to 1.866 ticks** across five set instants, against 4.9 to 5.1 in the bench-sign campaigns.
  - "Centred" fails at 5 of 5 instants, and also with 0 to 60 us lateness (`receipts/probes/fullside_*.log`).
  - A hold of up to five pops centres the ring from the empty side. From the full side it moves one event, out of up to five.
  - At depth 8 (stage 2) a single drop was a full recentre, because the most left at a PDU start was 2. The depth-16 ruling made it partial, and no campaign drives the sign where it matters.
- **Impact:** on any board pair where the followed talker runs faster than the DUT's INTERNAL clock (about half of all pairings), the INTERNAL-to-AAF settle recentre leaves the ring about one tick from overflow instead of centred. The worst instant measured is 1.12 ticks, so the ruled one-tick floor is nearly reached from this side alone. Any arrival earlier than those seen during the INTERNAL parking then skips after the settle, which is an undeclared post-settle discontinuity under #629's fabric item. The depth-16 headroom rationale is delivered for one sign only.
- **Required outcome:** one of the following:
  - the recentre reaches the LB_TARGET_C target from either side, for example by dropping up to (left - 5) events with the same lockstep, counter and one-PDU guarantees as the hold; or
  - a ruling that declares the asymmetric action and its full-side bound.

  In either case, the physical checker's step derivation (`tb/verilator/milan_dp/sim_ax1x1gptp.cpp`, `fill > 5 ? 1`) and the [LRC] cases must follow. The arrival campaigns must also include the reversed sign, with the ring at its full edge at the switch, graded on the same bar.
- **Verification:**
  - `scripts/run_probes.sh` probe A (five instants, plus 0 to 60 us) passes "centred" with both margins of at least 1 tick.
  - A reversed-sign 16-phase sweep joins the standing campaigns.
  - A new [LRC] case with more than six events left shows the full action, and a planted single-drop control fails that case.

### F2 MAJOR: an INTERNAL pull under the 1/16-sample excursion arm leaves a running stream off its law, with no recentre

- **Lenses:** Conformance, RTL, Robustness, Tests, Docs.
- **Where:**
  - `hdl/milan/milan_datapath.sv:6343` (`SETTLE_EXC_ERR_C = 4 * SRC_SETTLE_ERR_C`) and `:6353-6358`.
  - The test gap: `tb/verilator/follow_ring/follow_ring_wrap.sv:58` together with `sim_main.cpp:76`. The audio clock is 16 cycles per frame, so the harness can only produce holds in steps of 1/16 sample, which is exactly the arm. The standing holds are 52 and 56 us (`Makefile:91`) and T14's 5,200 cycles (`tb/verilator/milan_dp_render/sim_tdm8_render.cpp:243`).
  - The design text: `docs/design/MEDIA_CLOCK_FOLLOWING.md:1090`.
- **Authority:**
  - #647's acceptance: "After any INTERNAL aligner pull-in ... a running stream returns to the declared render law", and "No change to the declared law without a ruling".
  - The stage-2 ruling (5982568394) keys the INTERNAL trigger on the aligner's band. The ruling does not mention the 4x-band arm, which appears only in the stage-1 option B prototype. No ruling or document declares that a smaller pull may leave a stream off its law.
- **Evidence:** I copied follow_ring with a 1/64-sample serial-clock quantum (audio at 3.072 MHz, FRAME_DIV_P 64) at a 25 MHz axis clock. The wrapper scales the aligner gains, and the arm is 32 cycles. The RTL is unchanged; the diff is in `receipts/probes/probe_b_sim_main.diff`.
  - A +3/64-sample hold (42.64 us) peaks at |err| 24 cycles. That is under the 32-cycle arm, so the settle never pends (`receipts/probes/grid_trace_summary.txt`).
  - Three gradable on-law streams (fill 14, delay 8.963 to 8.984, clearance 0.016 to 0.036 tick) move to **fill 15, delay 9.009 to 9.030** and stay there for the 1.5 s graded after. The result is "LEFT THE LAW" (`receipts/probes/cross_*.log`).
  - Control: a +5/64 hold at the same phase arms the recentre. It fires 0.144 s later and the stream returns to the law, with 8 of 8 checks passing (`ctl_h43.29_l204.4.log`).
  - On silicon the held TDM bit clock quantises far finer than 1/16 sample. At 50 MHz the ambiguity window is about 0.003 sample against a 0.0624-sample arm, so a band of gradable phases is exposed.
- **Impact:** #647's failure mode remains for pulls between the ambiguity width and 1/16 sample. A running stream within the pull's distance of its law boundary ends one event off the declared render latency, permanently. It is rarer, but it is the same undeclared outcome, and it is not declared or graded.
- **Required outcome:** one of the following:
  - an arm that catches any pull able to move a gradable stream across its boundary, for example leaving the 1/64-sample settle band, with the noise case argued and tested; or
  - a ruling that declares the sub-threshold residual (the pull bound and the exposed phase fraction) in the design and grades it.

  In either case, the harness must be able to generate sub-threshold holds, and it needs a planted control.
- **Verification:** probe B (`cross_*`) passes the law after the pull, or the declared residual is graded. A sub-threshold-hold control fails with the arm removed.

### F3 BLOCKER: the required `docs-check` context fails at the exact head (stale traceability matrix)

- **Lenses:** Tests, Docs.
- **Where:** `docs/traceability/MODULE_MATRIX.md` and 12 `hdl/**/README-tests.md` files, which are generated by `docs/traceability/gen_module_matrix.py`.
- **Authority:** CONTRIBUTING.md:55-58 lists `docs-check` among the seven required contexts. The workflow step is `.github/workflows/docs.yml:137-138`.
- **Evidence:**
  - At this head, `python3 -B docs/traceability/gen_module_matrix.py --check` returns rc 1 and reports 13 stale files (`receipts/traceability/head_check.log`).
  - Live dev `28f9666f` returns rc 0 (`receipts/traceability/dev_28f9666f_check.log`).
  - The hosted `docs-check` at `4e1ddee9` failed at that step, and its later steps did not execute (`receipts/hosted/`).
  - The new `follow_ring` suite causes the drift. Regenerating would also credit `follow_ring` as a direct test of `milan_datapath`, and transitively of its descendants (`adp_tx_arbiter`, `KL_aaf_packetizer`, `KL_chan_map_render` and others), because its Makefile names `DP_SRC`. `follow_ring` only copies glue text from that file through `dp_glue.py` and never compiles it (`receipts/traceability/MODULE_MATRIX_regen_at_head.diff`).
  - The PR body's "26/26 source/documentation gates" did not include this gate.
- **Impact:** the merge ruleset cannot be met at this head. A blind regeneration would publish a false coverage claim.
- **Required outcome:** `gen_module_matrix.py --check` passes at the head. The matrix must not attribute `milan_datapath`'s descendants to `follow_ring`: either the generator distinguishes the `dp_glue.py` text copy, or the attribution is justified.
- **Verification:** the gate returns rc 0 locally and in hosted `docs-check`, and the regenerated rows are inspected for `follow_ring`.

### F4 MINOR: the "Fires at INTERNAL" row misstates the timing when the aligner is not engaged

- **Lenses:** Docs.
- **Where:** `docs/design/MEDIA_CLOCK_FOLLOWING.md:1092`: "or at once if it is not engaged".
- **Evidence:** at `hdl/milan/milan_datapath.sv:6359-6365`, a disengaged aligner only makes `settle_steady_w` true. `settle_need_w` is still `SRC_SETTLE_TICKS_C`, so the pulse comes 2,048 ticks (43 ms) after the arming, not at once.
- **Impact:** the authoritative design page misstates a timing contract.
- **Required outcome:** the row states the 2,048-tick run in both cases.
- **Verification:** a reading of the row against `:6359-6365`.

### Suggestions (non-blocking)

- **S1 (Robustness, Docs).** A held walk that finds the queue empty still counts a dup (`pop_dup_w`, `KL_chan_map_capture.sv:888-889`, does not exclude `pop_hold_w`). This happens when the decision read "none left" and a tick lands before the PDU's first event commits, about 1 to 2 % of such decisions. The count is honest, because the queue really was empty. However, REGISTER_MAP `0x8D4` says held pops count in neither half, and the physical checker's "declared recentres leave both loopback slip counters unchanged" would flag it. State the case in the register row, or let the checker account for it.
- **S2 (Tests).** The physical leg prints `NOT RUN: declared recentre checks (no decisions; uncounted)` and passes when no settle decision occurs (`sim_ax1x1gptp.cpp`, `report()`). Startup always yields one decision, so the leg could require at least one.

## What was checked and held (evidence for the clean parts of each lens)

### Function, at the head with pinned Verilator 5.050 (identity in `receipts/env/identity.txt`)

All four arrival campaigns and the INTERNAL holds were re-run independently (`receipts/campaigns/SUMMARY.txt`; `scripts/summarize_campaigns.sh`):

| Campaign | Runs | Decisions | Post-settle slips | Min empty / full (ticks) | Max pre-settle |
|---|---|---|---|---|---|
| None | 16/16 | 48 | 0 | 4.984320 / 5.076480 | 2 |
| Uniform 0..5 us | 16/16 | 48 | 0 | 4.899840 / 4.907520 | 2 |
| 0..2 us + 1e-4 tail to 24 us | 16/16 | 48 | 0 | 3.893760 / 5.091840 | 3 |
| Uniform 0..60 us | 16/16 | 48 | 0 | 2.565120 / 2.234880 | 2 |
| INTERNAL 52/56 us holds | 32/32 | 32 | 0 | 4.984320 / 5.091840 | 1 |

- These are identical to the author's table.
- No lateness: 45 on the law and 3 not gradable.
- INTERNAL holds: 27 on the law, 2 BEFORE and 3 AFTER not gradable.
- Every settle came 4.096 s after LOCKED.
- The pre-settle count stayed within the declared bound of 3 in all four models, including the 0 to 60 us model, which the design page's bound paragraph (`:1132-1141`) does not list.

Other suites and controls:
- follow_ring mutation arm: 5 of 5 caught (NO-SETTLE, RENDER-ONLY, EARLY, W1, OVERSHOOT17; `receipts/suites/fr_mutants.log`).
- `chmap_capture`: 408 checks, 0 failures, including every [LRC] case, plus the netlist pin at 20/0 (`receipts/suites/chmap.log`).

### RTL, read against the contract

- `g_settle_recentre`:
  - The arm, run and ceiling are on one clock (axis), and its reset is complete.
  - `SETTLE_RUN_W_C` = 18 bits covers 196,608.
  - The ceiling bit fires at 2^20 ticks.
  - The excursion while pending restarts the run only.
  - `follow_sel_r` is a pure function of the selected index (`milan_datapath.sv:1604-1622`), so the need cannot switch under a pending run.
- The capture recentre:
  - The drop reads `rd+1`, consumes 2, and composes correctly with a same-cycle push (`push_pop_n_w`).
  - Holds are excluded from `pop_act_w`.
  - A flush clears the arm, the decision and the actions.
  - A pulse on a first beat arms the next PDU.
  - The hold width of 3 bits covers 5.
  - All pairs act in the same walks.
- The `lb_recentre_i` binding in the datapath is pinned by the builder gate (`sw/builder/test_builder.py`, the "settle recentre withheld from the LOOP queues" mutant).
- The startup and reset recentre is declared and bounded (`MEDIA_CLOCK_FOLLOWING.md:1159-1174`). The physical evidence shows step -5 at output PDUs 6047 and 92220, with counters 0 -> 0.

### Physical checker (code review; the leg was not re-run, see Limits)

- The expected step comes from the declared target and the decision-instant fill.
- The plan is carried per walk to the emitted PDU and graded per sample slot.
- The span is confined to one output PDU.
- Both counters are compared at the decision and at completion.
- The extra-repeat control (outside the PDU) and the understated-declaration (larger step) control each assert location, measured step and no unrelated failure.
- The published evidence is 143/0 physical, 40/0 accounting and 14/0 controls.

### Docs and history

- The stale-depth fix `e80dd7ad` is correct.
- The remaining "depth 8" texts at `tb/verilator/milan_dp/sim_nxn.cpp:8296` and `hdl/milan/milan_datapath.sv:1180` are histories of VERSION 0x0036, not current claims.
- TIME_SYNC's rows and REGISTER_MAP `0x8D4` match the RTL, apart from S1.
- The #396 steady-state scope is stated.
- The four #657 render-mutation failures are cited and not claimed.

### Area and timing, judged as measured (no vendor run)

- Area:
  - OOC: recentre +26/+41 and capture +54/+32, for **+80 LUT / +73 FF**.
  - Routed own logic: 112/73, with the 80 - 1 - 6 - 10 + 49 arithmetic checked.
  - The ten shared band LUTs are proved equal over 65,536 inputs, with a planted inverted-INIT control caught (`area-route/shared_logic_equivalence.json`).
  - Both figures are within 120/120.
- Timing at this head:
  - ExtraTimingOpt has slow WNS **-0.209 ns** (TNS -0.294 ns, two endpoints) on processor path `u_notify/wr_ix_r_reg[0]_replica_4` to `u_tx_arbiter/slot_r_reg[0]` (42 levels). This is a real setup failure.
  - The fa450d30 base predates processor pin `ead80360`, so the two tables are not like for like.
  - I raise no finding against this lane's logic for it. The merge waits on the manager's dev `28f9666f` table, as the PR body states.

### Hosted evidence at `4e1ddee9` (read-only, `receipts/hosted/`)

- **Executed with success:** rtl-fast, verilator-lint, yosys-elaboration, Yosys shards 0-3, Verilator shards 0 and 3, elaborate, docs-check-no-git, wire-accountability, bdd-conformance, full-ci-gate, changes.
- **Executed and failed:** docs-check (F3).
- **In progress at read time:** Verilator shards 1, 2 and 4.
- **Skipped (not executed):** Physical gPTP.

## Reviewer ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | #645/#647 acceptance and the five rulings; `KL_chan_map_capture.sv:225-255,505-517,875-960,1038-1072`; `milan_datapath.sv:6322-6395`; four arrival campaigns plus holds re-run; probes A and B | R474-1 | 4e1ddee9d7b9ebf58ebebcacd90c5d72dce0c96f |
| RTL | UNCLEAN (F1, F2) | the same RTL ranges; `follow_sel_r` decode `:1604-1622`; builder pin; `chmap_capture` 408/0 | R474-1 | 4e1ddee9d7b9ebf58ebebcacd90c5d72dce0c96f |
| Robustness | UNCLEAN (F1, F2) | reversed offset sign at five instants and 0 to 60 us; sub-threshold, above-threshold and whole-frame holds; flush, first-beat and unprimed [LRC] cases | R474-1 | 4e1ddee9d7b9ebf58ebebcacd90c5d72dce0c96f |
| Tests | UNCLEAN (F1, F2, F3) | `follow_ring` sim_main/sweep/mutants (5/5); [LRC]; [PULLIN] code; `sim_ax1x1gptp.cpp` and `verify_recentres.py`; builder mutant; traceability gate rc 1 (dev rc 0) | R474-1 | 4e1ddee9d7b9ebf58ebebcacd90c5d72dce0c96f |
| Docs | UNCLEAN (F1, F2, F3, F4) | `MEDIA_CLOCK_FOLLOWING.md:1036-1188`; TIME_SYNC rows; REGISTER_MAP 0x8D4; TESTING rows; `MODULE_MATRIX.md`; PR body; `e80dd7ad` and the depth-text search | R474-1 | 4e1ddee9d7b9ebf58ebebcacd90c5d72dce0c96f |

## Limits

- I did not re-run the physical gPTP leg, its accounting leg or its controls (about 63 minutes per leg unloaded, on a host at load 70 to 160), nor the full datapath, render, media-clock, processor, Yosys or builder banks. Those rest on the published evidence and the manager's source banks.
- No vendor run (prohibited).
- No bench work. Physical calibration is NOT RUN, and field skips are not hardware proof.
- Probe B changes the test harness only (audio quantum and axis clock), never the RTL. Its above-threshold control passes on the same build.
- For one transient period of about a minute, 17 probe processes ran against the 16-job budget. Every other interval stayed at or under 16.
- The `chmap_capture` run target wrote an ignored `obj_net/` into the clone. I moved it to scratch before the restoration check.

## Pending manager duties

- The dev `28f9666f` three-directive timing table, and the STOP-or-ticket decision for the -0.209 ns ExtraTimingOpt path.
- Rulings or fixes for F1 and F2, and the F3 gate.
- Exact-head `verilator-suites` completion.
- The final candidate merge build.
- The bench repeats for #645 and #647.
- The external review.

## Restoration

The clone is at the exact head. The index tree equals the head tree (`1cb3772c`), with no tracked, untracked or ignored changes. The four gitlinks match, and the initialised submodules are clean (`receipts/env/restoration.txt`).

## Concurrent external report (read after the above was written)

This section is filled in after the verdict, findings and ledger above were fixed. It changes none of them. The concurrent external NEGATIVE (posted 04:05Z) was read only for cross-reference.

- **Its MINOR on `MEDIA_CLOCK_FOLLOWING.md:1092`** is the same defect as my F4, at the same severity.
- **Its MINOR on the stale traceability artifacts** is the same defect as my F3. I grade it BLOCKER, because it fails the required `docs-check` context at this head. I add that a blind regeneration credits `follow_ring` with `milan_datapath`'s descendants.
- **Its MAJOR "the declared five-pop hold can occupy two output PDUs"** (`KL_chan_map_capture.sv:1062`) is a finding I did not examine in this round. I neither confirm nor dispute it, and it stays for the next round to resolve.
- **My F1 (full-side asymmetry) and F2 (sub-threshold INTERNAL pull)** do not appear in that report.

R474-1 FINISHED
