[R277] POSITIVE - exact head 021b2e07b009158bcb0ce19529126eb1d330bba5

Round R277-2: external independent review of issue #387 / PR #540 (Relates to #387, a partial change), correction round 1 by author A224.

- Exact head: `021b2e07b009158bcb0ce19529126eb1d330bba5`.
- Tree: `a7ffb35beea95d5bba593029f382e8c0ab0b1c27`.
- Source base: `759da623072358afdb0e9d570a7b4b6a788492c9`. The head descends linearly from it through six one-line commits with no trailers. Two of them, `fdd613a1` and `021b2e07`, are this correction round, on top of `44bf0891`.
- Independence: the round ran from a cleared context. It used only public state and read the prior review findings only after its own pass over the diff. It did not read any author lane record outside the published evidence tree.

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open at this head. The round applied all five lenses (Conformance, RTL, Robustness, Tests and Docs) and found each one clean at this exact head. The eight MINOR findings of R276-1 (F1-F5) and R277-1 (findings 1-3) are resolved, and so are the six suggestions of those rounds. The resolution table and its evidence are below.

This round leaves two SUGGESTIONs. They are optional and do not affect coverage.

**The verdict covers this partial PR and nothing more.**

- #387 acceptance 3 is still **not met**, and the PR says so. It waits for the `milan_datapath.sv` edit, which is held behind #529.
- Acceptance 4 is the #117 bench.
- The owner ruling on the grid aligner is still to come.

## How the round was reconstructed

These were read in this order:

1. AGENTS.md, CONTRIBUTING.md and docs/README.md.
2. REQUIREMENTS.md REQ-PTP-05, REQ-PTP-07, REQ-PTP-08 and REQ-PTP-09.
3. The #387 body and its frozen acceptance.
4. The #387 decisions: 5606198212 part (b), and 5794731090, which supersedes part (a).
5. The manager's rulings and assignments on #387: 5802264260, 5800693336 and 5804878668.
6. The A214 and A224 REVIEW READY comments.
7. Donor FPGA-gPTP#68 as recorded in the pinned `INTEGRATION.md`.
8. `git diff 759da623..021b2e07`, plus the correction delta `44bf0891..021b2e07`.
9. The public evidence tree `review-evidence/387-r1` at `37d91083`: the author and correction packets only, before the verdict.
10. The hosted checks at the exact head.

## Focus items verified at this head

| Assignment item (5804878668) | Result | Evidence |
|---|---|---|
| The grid-aligner row quotes decision part (b) verbatim in the Decided column | Yes | `docs/design/GM_LOSS_RECOVERY.md:119` Decided = "the render elastic stage (#386) and the media grid aligner's phase reference re-centre in one bounded, counted event", a byte-for-byte substring of 5606198212(b) |
| The row's tree column records the observed gap and leaves the question with the owner | Yes | `:119` says "no PHC or step input". `KL_media_grid_align.sv:97-106` has only `sel_i`, `frame_ev_i` and `tick_i`, wired at `milan_datapath.sv:5566-5573` to the CRF selection, the TDM capture frame marker and the NCO tick. The NCO has no PHC input either (`KL_media_nco.sv:89-112`). Under CRF selection the frame marker follows the MMCM clock that `KL_mmcm_drp_servo` steers, so the "only through the CRF-steered grid (#539)" claim holds. The owner question is published in the A224 REVIEW READY comment (5805175917, open risk 1) and in the PR's definition of done. The page does not settle it |
| Ruling 5802264260 item 2 is recorded | Yes | `GM_LOSS_RECOVERY.md:124`: the step merges with a pending restart into exactly one restart, never a cancellation, and its MEDIA_RESET is still counted. The tree state "Not yet" is correct: `KL_media_clock_restart.sv:167` does `if (restart_p_i \| src_change_w) tgt_r <= ~tgt_r;`, so a second request before adoption cancels the first |
| The gmstep claims are narrowed to what the leg grades | Yes | `GM_LOSS_RECOVERY.md:135-151,179`, `tb/verilator/milan_dp/README.md:349-397` and the `sim_gmstep.cpp:4-19` banner. Each graded row maps to named checks: `tu` to `:887-910`; the render re-base to `:976-978`; the render law to `:809,:989`; `mr` and MEDIA_RESET to `:1012-1023`; the streams to `:918-959`. Each ungraded row names where it is covered or left open |
| The counted event is tied to the step | Yes | `sim_gmstep.cpp:970` (re-base within 500 cycles after the step pulse), `:1009` (first new-`mr` PDU within two talker intervals) and `:1020-1021` (MEDIA_RESET unmoved at a read between the commit and the step, with `:872-873` proving where that read lands). My own controls P1, P2, P3, P4, P10 and P11 were each caught by the named checks at four phases, and the boundary control P5 passes (receipt 50) |
| The licence check sees a talker that stops for good | Yes | `sim_gmstep.cpp:925` counts the trailing silence to the window end, `:931-942` measures the rate to the window end, and `:909` requires more than 100 PDUs after `tu` clears. In P7 the talker is cut 640000 cycles after the step, with `tu` long clear and more than 100 PDUs already graded after it. It fails the pause and rate checks at all four phases. P6, cut at the step, fails those two checks and the `tu`-after check |
| The render-law arms are independent of the start phase: 42 delays pass on the edited copy, and 10 controls are caught at delays 0 and 12 | Yes, and more strongly | The edited copy equals the tree datapath plus the published patch byte for byte (sha256 `45ac96c0...5930`, receipt 11). On it the clean leg passes **125/125** feed delays, 0 to 124, which is every phase of the 2 MHz / 48 kHz tick pattern. The fill after the push is 14 at every delay, and the fill at accept is 9 or 10 (receipts 50 and 41). My own stage controls P8 (snap low) and P9 (snap high) are caught at delays 0, 29, 83 and 124 by "render: every PDU push leaves the target fill across the event" alone |
| The head fails only the pending datapath behaviours | Yes | At the exact head the leg reports 48 checks and 4 failures, the same four at delays 0, 12, 29, 83 and 124: two counted re-bases (one outside the step window), no `mr` toggle, no MEDIA_RESET (receipts 10 and 50). Build and run took 38 s, over 8,042,838 cycles |

## What else holds at this head

- **The pin.**
  - The `gptp-processor` gitlink `e5dcea6e` is the donor main tip. It is the merge of FPGA-gPTP PR #74 (merged, head `ba926810`), and its tree `5a02fa35` equals `ba926810`'s tree.
  - The donor delta `c1b61743..e5dcea6e` changes the generator, the tracked images, the donor tests and the donor docs. It changes no SystemVerilog.
  - The pinned generator's thresholds are `STEP_LINKUP_NS_C = 20000` and `STEP_LOCKED_NS_C = 100000` (`gen_gptp_ucode.py:405-406`). Its clamp is `ppm_addend(200, clk_hz)`, which `KL_gptp_txret.sv:303-305,434-436` mirrors as `PHC_ADJ_MAX_C` and uses to refuse egress timestamps. That matches `TIME_SYNC.md:93-97`.
- **The ROM ledger.** Regenerating the default image at the pin, the same way `ooc.sh` does, gives `4afe436d...43bb` over 1024 lines. That equals `syn/yosys/rom_digests.tsv:33` (receipt 21).
- **The step policy text.** `TIME_SYNC.md:75-107` agrees with 5794731090, with ruling FPGA-gPTP#68 5798089412 and with the donor `INTEGRATION.md` section "Step versus slew policy" at the pin. The leg's acquisition shows the plane stepping once above 20 us at link-up. Its event shows the plane stepping exactly once, by 1.5 s within 1 us, once locked.
- **The other decision rows.**
  - `tu` takes the plane's step pulse: `milan_datapath.sv:1935-1936`.
  - `mcr_restart_p_w` has no step term: `:3091-3092`.
  - The render trigger includes both the identity change and the step: `:5965-5967`.
  - `tu` gates no emission: the gates `:1906-1909`, `:2014-2018` and `:5260-5262` do not read `tu`.
  - The CRF guard threshold is `2^19` ns per 512 ms window, which is 1024 ppm or 524 us: `KL_mmcm_drp_servo.sv:37-52,266-270`. That matches the band #539 records.
- **Static gates at the head** (receipt 20). All twelve exit 0:
  - `docs_check`, `check_doc_style` and `check_em_dash --base 759da623`;
  - `check_gptp_docs`, with and without the submodule;
  - `gen_toc --check`, `check_feature_status`, `check_submodule_docs` and `measure_test_evidence --check`;
  - `check_cpp_idiom` and `check_py_idiom`;
  - `git diff --check 759da623 HEAD`.
- **Commit hygiene.** `fdd613a1` and `021b2e07` each have one line, no trailers and one parent.
- **Hot files.** `milan_datapath.sv`, `sim_nxn.cpp` and `CHANGELOG.md` are not in the diff.
- **Hosted checks at the exact head** (receipts 30 and 31). 21 jobs executed and succeeded: all five Verilator shards, all four Yosys shards and both aggregates, each with real steps run. `Physical gPTP (nightly and manual)` is a skipped context. It is not hardware evidence.

## Findings

No BLOCKER, MAJOR or MINOR finding is open.

```text
[R277] SUGGESTION Docs - docs/design/GM_LOSS_RECOVERY.md:118 - the render row's tree column opens "Yes" while the tree double-counts a GM change that steps
ID: R277-2 S1
Authority/evidence: the Decided column says the stage re-centres in "one bounded, counted event" (5606198212(b)). The tree column reads "Yes, at the next PDU end ...; a grandmaster identity change also re-centres it", and :131-133 state that today a grandmaster change that steps counts two re-bases against a decided one. The leg measures exactly that at head (receipt 10: counted re-bases at step pulse -160118 and +132). The other rows with a gap from the decision say "Not yet".
Impact: low. The deviation is disclosed in the same cell and two lines below, but a reader skimming the tree column sees the render row as done.
Required outcome (optional): until the datapath edit lands, the tree cell reads "Partly" or "Not yet", with the double count stated in the cell.
Verification: the tree cell no longer reads as meeting "one" for a grandmaster change that steps; the docs gates stay green.
```

```text
[R277] SUGGESTION Tests, Docs - tb/verilator/milan_dp/README.md:371-374 (also Makefile:281-282) - the start-phase claim is approximate, and the feed delay never moves the step against the listener's PDU grid
ID: R277-2 S2
Authority/evidence:
  - 48 kHz at 2 MHz is exactly 125 cycles per three ticks, and the AAF period is 250 = 2 x 125. So 125 feed phases are distinct, not 42.
  - Measured (receipt 41): the printed fill at accept is periodic in 125. At period 42 it has 2 mismatches, and at period 41 it has 4. The windows where the fill at accept is 10 are 6, 5 and 5 delays wide.
  - Separately, the feed delay shifts the whole event timeline, so the counted re-base lands at +132 cycles after the step pulse at all 125 delays (receipt 50). The new 500-cycle window check is therefore exercised at a single step phase.
  - Reviewer probes: all 125 feed delays pass with the edit (receipt 50). A disposable GM B Sync shift (scripts/step_shift_probe.sh) passes at 8 step phases, with the re-base at +52 to +146 and the mr toggle at +36 to +522 (receipt 40).
Impact: none on this verdict, because the claims hold at every phase tried. A future runner that sweeps only 0..41, as the README implies is complete, would leave 83 feed phases unexercised, and the step phase stays fixed.
Required outcome (optional): when the runner joins with the datapath edit, it sweeps 0..124, or the README states the 125-cycle period. Optionally, the leg also gets a step-phase knob.
Verification: the runner's sweep list or the README wording, and the step offset printed at more than one phase.
```

## Per-lens results

```text
[R277] PASS Conformance - docs/design/GM_LOSS_RECOVERY.md:109-153,179 and docs/design/TIME_SYNC.md:75-107 against #387 5606198212(b), 5794731090, rulings 5802264260 items 1-3, assignment 5804878668, FPGA-gPTP#68 5798089412 and donor INTEGRATION.md at e5dcea6e; REQ-PTP-05/07/08/09; PR #540 body (Relates to #387, acceptance 3 declared not met) - every decided row is traceable to a decision or ruling, the aligner conflict is published for the owner and not settled in the page, the step policy is stated once and correctly, and no acceptance criterion is claimed beyond what is met
[R277] PASS RTL - gptp-processor gitlink e5dcea6e (donor diff c1b61743..e5dcea6e: no .sv); syn/yosys/rom_digests.tsv:33 regenerated (receipt 21); gen_gptp_ucode.py:405-406,428-436 against hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv:303-305,434-436; hdl/milan/milan_datapath.sv:1935-1936,2742-2743,3091-3092,5883-5892,5965-5967 (unchanged step consumers); KL_media_grid_align.sv:97-106; KL_media_nco.sv:89-112; KL_mmcm_drp_servo.sv:266-270; KL_media_clock_restart.sv:167; head elaboration of the gmstep leg - no parent RTL in the diff, the imported ROM and envelope agree with the parent consumers, and every RTL fact the page states is true of the tree
[R277] PASS Robustness - tb/verilator/milan_dp/sim_gmstep.cpp:886-1024 and :1045-1072 under 125 feed phases, 8 step phases and 14 probes P1-P14 (receipts 40, 50) - a talker silenced at the step or long after tu clears, restarts that are late, doubled or keyed to the identity or to tu falling, late re-bases, late tu, and dead Stream Input counters are each caught; the waits are cycle-bounded (AXI 2048, AECP 400000); a malformed feed delay is refused with exit 2; the pending-restart merge is recorded as "Not yet", with its arm ruled into the follow-up edit
[R277] PASS Tests - sim_gmstep.cpp (48 checks) and Makefile:274-294: at head 48/4 at 5 phases with exactly the four declared failures (receipts 10, 50); edited copy 125/125 phases; 12 must-fail controls caught by their named checks at 4 phases (P14 at 2), boundary control P5 passing at 4, informational P12 recorded - each new check fails for the defect it names and passes a correct datapath at every phase tried
[R277] PASS Docs - GM_LOSS_RECOVERY.md:109-153,179; TIME_SYNC.md:63-107; tb/verilator/milan_dp/README.md:340-397; Makefile:96-101,274-294; the pin-following GPTP_PLANE.md, guides/gptp/*, SUBMODULES.md, traceability/ieee8021as.md and both diagrams; 12 static gates (receipt 20) - the text matches the tree, the decisions and the leg's checks; two optional wording suggestions (S1, S2)
```

## Resolution of prior review findings at this head

Read after this round's own pass. "Resolved" means the round checked it independently at this head.

| Prior item | Lenses as assigned | Disposition at 021b2e07 | Evidence |
|---|---|---|---|
| R276-1 F1 (MINOR): the aligner "decided" row contradicts part (b) | Conformance, Docs | **RESOLVED** | The Decided column quotes (b) verbatim, and the tree column states the gap. The owner question is published (5805175917). R276-1's interim requirement ("until that ruling exists, the Decided column carries part (b)'s wording and the tree column carries the observation") is met. The ruling itself is a #387 item for the manager |
| R276-1 F2 (MINOR): the page omits ruling 5802264260 item 2 | Conformance, Docs | **RESOLVED** | `GM_LOSS_RECOVERY.md:124`, with the tree state verified at `KL_media_clock_restart.sv:167` |
| R276-1 F3 (MINOR): "measures all of this" | Docs | **RESOLVED** | `:135-151,179`. Each graded row maps to named checks, and each ungraded row names its owner |
| R276-1 F4 (MINOR): the counted event is not tied to the step | Tests | **RESOLVED** | New checks at `sim_gmstep.cpp:970,1009,1020`. The identity-keyed variants P1, P2 and P10 are caught at 4 phases, and so are the late or wrong-trigger variants P3, P4 and P11 |
| R276-1 F5 (MINOR): the licence checks cannot see a talker that stops for good | Tests, Robustness | **RESOLVED** | `:909,925,931-942`. P6 and P7 are caught at 4 phases. P7 isolates the trailing-silence arm |
| R276-1 S1: the Makefile names an untracked runner | Docs | Resolved | `Makefile:99-101,278-280` now say the runner joins with the datapath edit |
| R276-1 S2: no counters_valid guard | Tests | Resolved | `:953-957` (Stream Input valid bits and the FRAMES_RX advance) and `:1014-1019` (all three Stream Output reads). P14 is caught |
| R276-1 S3: cite #539 on the CRF servo row | Docs | Resolved | `GM_LOSS_RECOVERY.md:121` |
| R277-1 finding 1 (MINOR) = R276-1 F1 | Conformance, Docs | **RESOLVED** | As R276-1 F1 |
| R277-1 finding 2 (MINOR) = R276-1 F3 | Docs, Tests | **RESOLVED** | As R276-1 F3. R277-1's verification ("every row the page says the leg measures maps to a named check") holds |
| R277-1 finding 3 (MINOR): the render-law arms depend on the start phase | Tests, Robustness, Docs | **RESOLVED** | The law is graded at the stage's own reference, the fill after the push (`:437-447,809,989`). 125/125 phases pass with the edit. P8 and P9 are caught at 4 phases. The banner (`:46-53`) and README (`:363-369`) are corrected |
| R277-1 suggestion: the Makefile names a runner | Docs, Tests | Resolved | As R276-1 S1 |
| R277-1 suggestion: Stream Input validity | Tests, Robustness | Resolved | As R276-1 S2 (P14) |
| R277-1 suggestion: TIME_SYNC.md:95 "enforces" | Docs | Resolved | `TIME_SYNC.md:95-97`, checked against `KL_gptp_txret.sv:434-436` and the donor clamp |
| R277-1 observation: the commit discontinuity path for `tu` | not a finding | Unchanged | P12 (`tu` one cycle late) passes, and P13 (two cycles late) is caught. See Limits |

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | GM_LOSS_RECOVERY.md re-base table and grading list; TIME_SYNC.md step policy; #387 decisions 5606198212(b), 5794731090; rulings 5802264260, assignment 5804878668; FPGA-gPTP#68 5798089412 and donor INTEGRATION.md at e5dcea6e; REQ-PTP-05/07/08/09; PR body | R277-2 | 021b2e07b009158bcb0ce19529126eb1d330bba5 |
| RTL | CLEAN | gitlink e5dcea6e and donor delta; ROM regeneration against rom_digests.tsv:33; generator thresholds and clamp against KL_gptp_txret; datapath step, restart and render wiring; grid aligner, NCO, CRF servo guard and restart module facts; head elaboration | R277-2 | 021b2e07b009158bcb0ce19529126eb1d330bba5 |
| Robustness | CLEAN | sim_gmstep.cpp failure paths, transport bounds, input validation; 125 feed phases; 8 step phases; 14 probes (P1-P14), including a talker that stops for good, late, doubled and wrong-trigger restarts and re-bases, late tu, and dead counters | R277-2 | 021b2e07b009158bcb0ce19529126eb1d330bba5 |
| Tests | CLEAN | gmstep leg at head (48/4 at 5 phases); edited copy (125/125); 12 must-fail controls, 1 boundary control and 1 informational probe; Makefile recipe and overrides | R277-2 | 021b2e07b009158bcb0ce19529126eb1d330bba5 |
| Docs | CLEAN (2 SUGGESTIONs) | GM_LOSS_RECOVERY.md, TIME_SYNC.md, milan_dp README and Makefile comments, sim_gmstep.cpp banner, pin-following pages and diagrams; 12 static gates | R277-2 | 021b2e07b009158bcb0ce19529126eb1d330bba5 |

## Limits

- **The probes judge the harness, not the follow-up RTL.** Every "edited" run uses the tree datapath with the published proposed patch applied, on a disposable copy. That patch is not in this PR, and its design was not reviewed here. Examples: the restart is no longer gated by the clock source, and the I2S element still follows the identity trigger.
- **The pending-restart merge is not simulated.** Ruling 5802264260 item 2 has no arm yet, by ruling.
- **The model is compressed.** It runs at 2 MHz, with the TDM clocks held (the aligner stays disengaged), the DRP stubbed and the talker opened by the escape bit. The talker cadence (642 cycles) is the model's own. The step's phase against the listener's PDU grid is limited by the harness's AAF slot guard: 8 shifts produced re-base offsets of +52 to +146 only.
- **The `tu` boundary.** A one-cycle-late `tu` (P12) passes "tu: set in the first cycle the bank names GM B", because the discontinuity pulse precedes the bank copy by one cycle. A two-cycle delay (P13) is caught. The leg grades that no talker PDU shows new identity with old health. The exact-edge property belongs to `gptp_shadow` and `clkvalid`, which were not re-run here.
- **Not run by this reviewer:**
  - the full parent, protocol-processor, gPTP, Yosys and builder banks;
  - the `milan_dp` `run` recipe and the `gptp` and `gptp-lat` legs;
  - `gptp_shadow`, `clkvalid`, `media_grid_align` and `tsn_fuzz`;
  - `ooc.sh`, act and hardware.

  The manager's published source banks at this head are the evidence for those. No RTL or suite source changed in the correction round.
- **No physical evidence.** Physical calibration was NOT RUN. The skipped hosted physical context and the model's stubs are not hardware proof.

## Pending manager duties

- Obtain the owner ruling on whether the media grid aligner's phase reference needs its own re-centre (A224 open risk 1). Then turn the `GM_LOSS_RECOVERY.md:119` row.
- Obtain a ruling on acceptance 3's "the stream stays licensed", given that the leg opens the talker with the `AAF_CTRL[1]` escape rather than an lwSRP licence (A214 open question 5, still unruled). This must happen before acceptance 3 is claimed met.
- Build and gate the final current-dev candidate at the merge turn: source base `759da623`, live dev `50e78097564244c124e1ec30dd8821f83951ab06` as briefed. Own hosted and act acceptance.
- Obtain the internal review verdict (R276-2) at this head, and confirm that no review round is in flight before any merge.
- Track the follow-up after #529:
  - the `milan_datapath.sv` edit, with the ruling-item-2 merge arm;
  - wiring gmstep and its negative-control runner into the sweep (see S2 for the phase list);
  - turning the "Not yet" rows;
  - the CHANGELOG entry;
  - #539;
  - the #117 bench (acceptance 4).

## Clone state

Receipts 00 and 90 cover the clone state.

- The review clone was never written to. Every build and probe ran in a disposable local clone under `scratch/`.
- At the end, HEAD, the tree and the index digest all equal the exact head.
- All 877 index entries match HEAD. Every tracked blob and mode was re-hashed, with 0 mismatches.
- No index entry carries an assume-unchanged or skip-worktree flag.
- No untracked or ignored files exist.
- `gptp-processor`, `protocol-processor` and `third_party/verilog-axis` are clean at their gitlinks. `external` is uninitialised, as it was at the start.

## Receipts

Every file below is listed in `MANIFEST.sha256`. Paths are relative to this packet.

- `scripts/verify_clone.sh`: clone identity (head, tree, index, blobs, modes, submodules).
- `scripts/static_gates.sh`: the twelve static gates.
- `scripts/r277_2_probes.py`: the clean sweep, the head runs and probes P1-P14, built through the Makefile's own `gmstep-build` recipe with source overrides.
- `scripts/step_shift_probe.sh`: the step-phase probe on a disposable harness copy.
- `receipts/00-clone-baseline.txt` and `receipts/90-clone-final-verify.txt`.
- `receipts/01-tool-identity.txt`: Verilator 5.050 through the pinned wrapper (sha256 `905795b9...e92f`).
- `receipts/10-gmstep-head-build-run.log`: `make gmstep` at head, with the build log. Private host paths are replaced by placeholders.
- `receipts/11-edited-copy-identity.txt`: the tree datapath plus the published patch equals the published edited copy.
- `receipts/20-static-gates.txt` and `receipts/21-rom-digest-regeneration.txt`.
- `receipts/30-hosted-check-runs.tsv` and `receipts/31-hosted-job-steps.tsv`.
- `receipts/40-step-phase-shift.txt` and `receipts/41-phase-periodicity.txt`.
- `receipts/50-probe-summary.txt`.
- `receipts/probes/{sweep,head,probes}.jsonl` and `receipts/probes/raw/*.log`: the full output of every run.

R277-2 FINISHED
