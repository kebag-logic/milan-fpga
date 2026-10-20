[R677] NEGATIVE - exact head f1fda3f1f87c64801e436e129326b5bd5952bf20

# R677-1: internal cleared-context review of PR #770 (Relates to #632, #764)

- Head under review: `f1fda3f1f87c64801e436e129326b5bd5952bf20`, tree `b5bb11d04270aeb2721f1961c4d85a11fc7debde`. The review clone was verified at both before and after the probes (`receipts/clone_verification.txt`).
- Source base: dev `e26f1816`; sixteen commits `cd39fea0..f1fda3f1`. Live dev is `78ca9bdf`; composition is the manager's candidate-merge duty and is not claimed here.
- Covering round: R677-1. Lenses applied: Conformance, RTL, Robustness, Tests, Docs.
- Verdict: NEGATIVE. Four MINOR findings are open (F1 to F4). They leave Conformance, Tests and Docs unclean. RTL and Robustness are clean at this head. No BLOCKER or MAJOR was found.

## Reconstruction

Read in order:
1. AGENTS.md and CONTRIBUTING.md (style, comment and privacy rules, verification bar).
2. docs/README.md.
3. #632's body and frozen acceptance.
4. The assignment (issuecomment-6284510903) and its two addenda (issuecomment-6284578201, and issuecomment-6284659263, which replaces item 1 of the first).
5. #764's investigation report (issuecomment-6283948176).
6. The REVIEW READY comment and the PR body.
7. `git diff e26f1816..f1fda3f1` and the commit history.
8. The executable evidence: my own runs first, then the author's published receipts at `review-evidence/632-r1` (tree `8331d72e`): the receipts index, the sweep summaries, the media_phase campaign, the route check and the capture_coherence re-run.

Prior public review findings on this PR: none. The PR has no reviews and no inline comments. Its two conversation comments are the round-start notices, and neither issue thread carries a review finding. So nothing had to be resolved or retained.

## Findings

### F1 - MINOR - Conformance, Tests, Docs - the in-tree two-interface shape (Arty blend) is not given its per-interface constant and is not graded

- **Where:**
  - `tb/verilator/media_phase/pin_wrap.sv:5-6` says "no in-tree shape frames several capture buses on one domain".
  - `docs/design/MEDIA_CLOCK_FOLLOWING.md:1679` lists the blend shape by its TDM closing pair only.
  - `hdl/milan/milan_datapath.sv:6066-6083` binds the domain event to the TDM closing pair.
  - `hdl/ieee1722/aaf/KL_pair_blend.sv:27-29`: the blend shape's two front ends.
- **Authority:**
  - Second addendum (issuecomment-6284659263), item 2: each interface has its own capture age, pair or slot offset and pin delay, applied to the timestamps of the streams it carries.
  - Item 3 of the same addendum: prove it with two interfaces; "a synthetic shape is fine if no in-tree shape has two".
  - First addendum, item 2: the talker timestamps account for the capture age.
- **Evidence:**
  - `configs/endstation_arty_4x4.yaml` and `configs/endstation_arty_8ch.yaml` build `AUDIO_IF_I2S_PAIR_P = 1`. Those shapes put two capture interfaces on one clock domain: the stereo I2S front end at merged pair 0 and the TDM8 master at pairs 1 to 4 (`KL_pair_blend`).
  - The review probe `scripts/blend_probe` binds the two real front ends, `KL_pair_blend` and `KL_media_domain_event` exactly as `milan_datapath` does for this shape. It ran at six reset phases (`receipts/blend_probe.txt`):
    - The TDM frame is stamped within -9.7 to -29.4 ns of its sync.
    - The I2S pair that the stamped frame carries at slot 0 started 20,883.7 to 20,903.4 ns before the stamp: -1.0024 to -1.0034 Ps.
    - So the I2S interface's channels sit on the grid modulo Ps (folded -50 to -70 ns, inside +/-5 %). But their timestamp names an instant one whole sample period after the one at which they crossed the pins.
  - That interface's constant (one frame of capture age) is neither derived, applied nor documented.
  - No case grades the in-tree shape. The synthetic `pin_wrap.sv` was used on the stated premise that no in-tree two-interface shape exists, and that premise is false.
- **Impact:**
  - On the Arty 4x4 and 8ch images, talker 0's channels 1 and 2 are presented one sample late against their AAF timestamp, relative to the TDM channels of the same frame.
  - The PR and the design page say capture age leaves the timestamp, and that is not true for this interface.
  - The owner's condition for using a synthetic shape is not met.
- **Required outcome:** one of these.
  - The blend's I2S interface gets its derived constant (or a frame assembly without the one-sample age), and the in-tree blend shape is graded at its I2S and TDM pins against one stamp, with a planted control that fails.
  - Or the gap is published on the Issue and PR as a decision needed, the per-interface table carries the blend's I2S interface with its one-frame age, and `pin_wrap.sv`'s premise is corrected.
- **Verification:** a pin-level grade of the blend shape (what `scripts/blend_probe` measures) inside +/-5 % of Ps with no whole-period error, or the published decision and corrected text.

### F2 - MINOR - Tests, Docs - the local PHC step hold (#539) is claimed but no case or planted defect grades it

- **Where:**
  - `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:703-704`: `ptp_jump_r` in `ph_hold_w`.
  - `tb/verilator/media_phase/sim_main.cpp`: no local PHC step case.
  - `tb/verilator/media_phase/phase_mutants.py`: no defect for this hold term.
  - `docs/testing/TESTING.md:279` claims "one planted defect per ... hold condition".
  - `docs/design/MEDIA_CLOCK_FOLLOWING.md:1599` lists the PHC step among the holds.
- **Authority:**
  - Assignment item 4: bounded re-acquisition after each event.
  - AGENTS.md section 6, Tests: each new test can fail for the defect it claims to detect.
- **Evidence:**
  - Planted defect P1 (`scripts/probes/servo_p1_no_step_hold.patch`) removes `ptp_jump_r` from the hold. All ten PR cases still pass with it (`receipts/probes/obj_p1.<case>.rc` = 0).
  - Two review cases from `scripts/probes/sim_main_phcstep.patch`: `phcstep` (+20,000 ns, the link-up step) and `phcstep7` (+7,000 ns, 0.34 Ps).
    - On the clean RTL both pass. The term lets go within 5 ms. After the 7 us step the phase is re-acquired at 22.27 s and held (max 562.7 ns). See `receipts/probes/obj_clean2.*`.
    - With P1, both fail exactly "[phcstep] the phase term let go at the PHC step (within 5 ms)". See `receipts/probes/obj_p1b.*`.
  - The RTL behaviour is correct. The proof is missing.
- **Impact:** a regression that drops the PHC step hold passes the suite and its campaign. TESTING.md's "a defect per hold condition" is not true.
- **Required outcome:** a case that steps the local PHC with no slew level, graded by re-acquisition and let-go, and a planted defect removing `ptp_jump_r` from the hold that fails at it. The TESTING.md row then matches.
- **Verification:** `make -C tb/verilator/media_phase` passes the new case, and `make -C tb/verilator/media_phase mutants` kills the new defect at its named check.

### F3 - MINOR - Tests - two claimed behaviours of the phase detector survive planted defects

- **Where:**
  - `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:1308-1309`: the settled flag, which is also `MCSRV_STAT[9]`.
  - `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:730-731` and `:782`: the +/-2^25 ns fold-range guard.
- **Authority:**
  - `docs/reference/REGISTER_MAP.md` 0x8F8 `[9]`: settled means inside +/-5 % of Ps for four windows running, and reads 0 while re-acquiring.
  - The servo banner and `:777-779`: a timestamp outside the fold range is not sampled.
  - AGENTS.md section 6, Tests: negative and boundary behaviour covered, and each test able to fail for its defect.
- **Evidence:**
  - P2 (`scripts/probes/servo_p2_settled_always.patch`) makes `ph_settled_o` equal to "engaged", ignoring the band and the four-window count. All ten cases pass (`receipts/probes/obj_p2.*.rc` = 0). The suite only checks that settled reads 1 at the end. Nothing checks that it reads 0 while the phase is outside the band, or before four in-band windows.
  - P3 (`scripts/probes/servo_p3_no_range.patch`) removes the fold-range guard. All ten cases pass (`receipts/probes/obj_p3.*.rc` = 0).
- **Impact:** the one new register field's defining property, and the detector's out-of-range rejection, can regress unseen.
- **Required outcome:**
  - A check that `phase_o[21]` and `MCSRV_STAT[9]` read 0 while the phase is outside the band after an event, and become 1 only after four in-band windows.
  - A case that feeds timestamps outside the fold range and requires them not to be sampled.
  - Each with a planted defect that fails it.
- **Verification:** P2 and P3 (or equivalents) killed at named checks.

### F4 - MINOR - Docs - the recorded basis of `media_phase`'s 900 s suite budget describes nine cases

- **Where:**
  - `docs/testing/CI_WORKFLOWS.md:432`: "nine cases ran in 7.5 minutes locally at three jobs".
  - `scripts/run_all_suites.sh:250`: the same figure.
  - `tb/verilator/media_phase/Makefile`: "about 6 minutes for every case".
- **Authority:** CONTRIBUTING.md section 3, "Measure, don't assume": a gate's figure states what was measured.
- **Evidence:**
  - The suite at this head runs ten cases plus `pins` (`receipts/media_phase.log`).
  - The two recorded wall-clock figures disagree with each other, and neither describes the present suite.
  - The author's shard-1 sweep at `e85df091` passed `media_phase` inside the 900 s window, so the budget held there. The figure that justifies it is still stale.
- **Impact:** the provisional budget's provenance cannot be reproduced from the text. This is a measurement figure, so it is not RESIDUE.
- **Required outcome:** re-measure the present suite (ten cases and pins at the default `CASE_JOBS`) and record that figure in both places, consistent with the Makefile note.
- **Verification:** the three texts agree with a fresh timing.

### F5 - RESIDUE - Docs - stale comments still say `KL_crf_tx` divides the audio clock

- **Where:**
  - `hdl/milan/milan_datapath.sv:6265`, a pre-existing comment in a file this PR edits: "the CRF output (KL_crf_tx, which divides the physical audio clock)".
  - `sw/builder/endstation_builder.py:4748` ("KL_crf_tx /512, ").
  - `sw/builder/test_builder.py:21628` ("KL_crf_tx /512, ").
  - The PR body discloses the builder ones as a proposed follow-up.
- These are wording only: no code, measurement or claim changes.
- **Exact fix:**
  - At `milan_datapath.sv:6265`, write "the CRF output (KL_crf_tx, which stamps the domain's frame grid)".
  - In the two builder lines, delete "KL_crf_tx /512, " from the contract list.

### F6 - SUGGESTION - RTL - the marker latency's data-delay term is a literal beside three literal instantiations

- **Where:** `hdl/milan/milan_datapath.sv:6070-6071` passes `1` to `pair_end_bits`, while `.DATA_DELAY_P (1'b1)` is written separately at `:1028`, `:1073` and `:1108`. The comment at `:6060` records the coupling.
- **Suggestion:** one localparam feeding all four, so the constant is derived rather than mirrored (the owner's "never mirror a number").
- This is optional: no root parameter varies the data delay, and `capture_coherence`'s `[PIN]` derivation band catches a mismatch on the shipping 1x1 shape.

## Per-lens results

### Conformance - UNCLEAN (F1)

- [R677] PASS Conformance - `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:693-839,941-951,986-1035` @f1fda3f1 - The phase term lives inside the one servo; there is no second loop. Per accepted, consumed PDU, d = domain event - CRF timestamp is folded exactly:
  - In 1/3 ns units, Ps = 62,500.
  - The numerator is 3d + 62,500 x 2^11, positive and below 2^28 for |d| < 2^25.
  - A 28-step restoring divide by the constant gives the remainder, centred into [-31,250, 31,249].
  - The window phase is the sum over the nominal 256, capped at 264 samples. It enters the integrator one window late, clamped to 16,384 units, which is 256 ns a window (0.5 ppm).
  - Read against assignment items 1 and 2, Milan v1.2 7.6.1, and IEEE 1722-2016 10.7 Eq. 14 and 10.8 Eq. 15.
- [R677] PASS Conformance - `receipts/loop_model.txt` (`scripts/loop_model.py`) - An independent per-window linear model of the PI plus phase term gives closed-loop poles 0.9437, 0.7016, -0.3953 and 0:
  - This matches the banner's 0.944 (phase) and 0.70 (rate): type 2 against phase, the rate loop as damping, no complex pole.
  - From 0.49 Ps it pulls in by 25.6 s at 256 ns/window on the clamp, against the 23 to 28 s measured.
- [R677] PASS Conformance - `receipts/media_phase.log` @f1fda3f1:
  - Every case is inside +/-5 % of Ps within its bound and held: engage 27.46 s, engage2 23.36 s, step 21.70 s, holdover 27.33 s, plus ramp, internal, mr, slew, burst and carry.
  - Every DUT CRF timestamp is a frame instant of its own grid and lies on the reference's grid.
  - `pins`: three interfaces of one domain, each slot's MSB within 30.6 ns of its stamp, and every CRF timing point a frame instant of all three.
  - 129 checks, 0 failures.
- [R677] PASS Conformance - `receipts/cc_run_dp.log` @f1fda3f1 - The shipping 1x1 TDM8 talker's stamps are graded at the TDM pins through the whole `milan_datapath` (`[PIN]`), at INTERNAL and under CRF. 20,832 junction and 447 datapath checks, 0 failures. Assignment item 3 and first addendum item 3 are met for the shipping shape.
- [R677] PASS Conformance - `git diff e26f1816..f1fda3f1 -- hdl/milan/milan_datapath.sv docs/reference/REGISTER_MAP.md sw/litex/milan_soc.py` - No top-level port changes. The only register change is `MCSRV_STAT[9]`, a previously reserved RO bit, now RO "phase settled". This is inside the assignment's STOP conditions.
- Frozen acceptance:
  - The simulation item is met (`step` plus the campaign).
  - The bench item was not run: it is the manager's after merge and is not counted here.
- Open under this lens: F1.

### RTL - CLEAN

- [R677] PASS RTL - `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:436-507,693-839,986-1035` @f1fda3f1 - Checked:
  - Widths: phase 16 bits signed, window sum 26, count 10, divider remainder 18, integrator sum 40 bits for any 32-bit e.
  - Elaboration guards on the fold offset, the nominal power-of-two count, the cap and the clamp.
  - The integrator fraction is carried, and zeroed when clamped.
  - Every phase register is reset in `!rst_n` or IDLE.
  - A hold spoils the open window, as the last writer.
  - The divider is busy 29 cycles, against PDUs 2 ms apart.
  - The 32-bit modular difference.
  - No new clock domain: the detector, domain event, CRF output and crossbar bank all run in `axis_clk`.
- [R677] PASS RTL - `hdl/ieee1722/crf/KL_media_domain_event.sv`, `hdl/ieee1722/crf/KL_media_if_latency_pkg.sv`, `hdl/ieee1722/crf/KL_crf_tx.sv:378-397,477-484`, `hdl/ieee1722/crf/KL_crf_rx.sv:461-489`, `hdl/ieee1722/aaf/KL_chan_map_capture.sv:623-655,1273-1285`, `hdl/milan/milan_datapath.sv:6038-6108,6148-6156` @f1fda3f1 - Checked:
  - `ev_p_o` and `ev_ns_o` are registered together.
  - The liveness timeout falls back to the packet-grid tick.
  - `KL_crf_tx`'s event counter follows the module's own reset style, and its `cdc_pulse` and audio-domain reset sync are retired. `scripts/lint.budget` drops one SYNCASYNCNET in `crf`.
  - The frame instant is banked on the same cycle and `tdm_close` condition as the frame, and loaded into the walk with it.
  - `aaf_tbase_w` keeps the live PHC's high half, and the packetizer reads only `[31:0]` (`hdl/ieee1722/aaf/KL_aaf_packetizer.sv:733`).
- [R677] PASS RTL - `receipts/lint_rtl.log` - `scripts/lint_rtl.py --check` with Verilator 5.050: "LINT GATE: PASS (89 violation(s) <= ratchet 89)".
- [R677] PASS RTL - `receipts/blend_probe.txt` - The I2S-only shape's derived marker latency (64 bit periods + 5 audio cycles + 4.5 axis cycles) lands within -11.3 to -29.1 ns of the true frame instant at six reset phases.
- Open under this lens: none. F6 is a SUGGESTION and F5 is RESIDUE.

### Robustness - CLEAN

- [R677] PASS Robustness - `receipts/probes/obj_clean2.phcstep.log` and `obj_clean2.phcstep7.log`, at the head's RTL - An instantaneous local PHC step of +20,000 ns and of +7,000 ns, with no slew level:
  - The term lets go within 5 ms and re-acquires (22.27 s for the 0.34 Ps step).
  - It is held (max 562.7 ns), stays LOCKED and reads settled.
- [R677] PASS Robustness - `receipts/media_phase.log`:
  - Re-acquisition within its bound after a 0.37 Ps reference step, an `mr` toggle with a 1.8 us jump, 15 s of holdover with the oscillator moved 0.5 ppm, 15 s at INTERNAL, and a 27 us policy slew taken the short way.
  - A 4 ppm ramp is held throughout.
  - A talker 4 % faster than it declares is capped at exactly 264 samples.
  - Each event's let-go is observed.
- [R677] PASS Robustness - `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:703-704,780-788,825-829` and `hdl/milan/milan_datapath.sv:6151` - The term is held:
  - outside LOCKED;
  - with `ph_en_i` low (AAF following, or a dead grid through `dom_live_w`);
  - at `mr`;
  - on a broken history;
  - on a PHC step or a slew level.

  A PDU with no domain event since the last one, or a timestamp outside +/-2^25 ns, is not sampled. Reset and IDLE clear every phase register.
- Open under this lens: none. The untested guards are filed as F2 and F3 under Tests.

### Tests - UNCLEAN (F1, F2, F3)

- [R677] PASS Tests - `receipts/media_phase_mutants.log` @f1fda3f1 - `make -C tb/verilator/media_phase mutants MUTANT_JOBS=4`: 10 clean cases pass, then 17 of 17 planted defects fail their named checks. 27 checks, 0 failures. Reproduced at this head; the author ran it at `e85df091`.
- [R677] PASS Tests - `receipts/cc_mutants.log` @f1fda3f1 - `capture_coherence`'s `mutants.py --jobs 3`: "35 checks: 35 PASS, 0 FAIL". That is 25 mutants caught, including the five #632 ones (live PHC at the walk, tick-latched time base, frame term dropped, write term dropped, walk instant latched at the snapshot), plus the build-break and MAKEFLAGS arms and eight clean controls.
- [R677] PASS Tests - `receipts/chmap_capture.log`, `receipts/crf_tx.log`:
  - `chmap_capture` ([F] and [Q] walk instants through the coincidence law and a queued tick): rc 0.
  - `crf_tx`: 129 checks, 0 failures.
- [R677] PASS Tests - `git diff e26f1816..f1fda3f1 -- tb/verilator/milan_dp/` - The two re-timed fixtures change only loop lengths:
  - `RealPduWait` becomes `CRF_PDU_MAX_CLK + 5000`.
  - `CRF_BUDGET` becomes `2 x 200,000 + 10,000`.
  - The #726 TX wrap run becomes `400000 x TDM_SLOTS_TB / 8`.
  - No check, threshold or expected value changes. The author's shard-0 receipt at `f1fda3f1` shows `milan_dp` passing, counters 1/8 and frames-only included. Not re-run here.
- Open under this lens: F1, F2, F3.

### Docs - UNCLEAN (F1, F2, F4)

- [R677] PASS Docs - `docs/design/MEDIA_CLOCK_FOLLOWING.md:1528-1756`, `docs/design/TIME_SYNC.md`, `docs/reference/REGISTER_MAP.md` 0x8F8, `docs/reference/MILAN_COMPLIANCE_MATRIX.md` 4.3.5/10.8 row, `CHANGELOG.md` - Checked against the RTL and my runs:
  - The per-source contract, the detector, the loop terms, the gains and poles, and the hold list.
  - The re-acquisition table: engage 27.5 s, engage2 23.4 s and step 21.7 s reproduce at 27.46, 23.36 and 21.70 s.
  - The listener decision, the -0.46 Ps accounting and the proof table.
  - The compliance row reads "partial" with the bench open.
- [R677] PASS Docs - `receipts/docs_check.log`, `receipts/module_matrix.log`, `receipts/gptp_docs.log`:
  - `scripts/docs_check.py`: 0 findings across 210 md and 1406 scrubbed files.
  - `docs/traceability/gen_module_matrix.py --check`: up to date, 78 modules.
  - `scripts/check_gptp_docs.py`: OK.
  - No U+2014 in any added line (a grep of the diff).
  - No bench lane label, reviewer ID, review round or issue-comment ID in any added source line. The "lane A/B" hits are `chmap_capture`'s pre-existing names for its two DUT instances.
- Open under this lens: F1, F2, F4. F5 is RESIDUE.

## Completion ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | servo phase path; domain event; latency package; datapath binding; register map; `media_phase` cases and pins; `capture_coherence` `[PIN]`; loop model; blend probe | R677-1 | f1fda3f1f87c64801e436e129326b5bd5952bf20 |
| RTL | CLEAN | `KL_mmcm_drp_servo.sv`, `KL_media_domain_event.sv`, `KL_media_if_latency_pkg.sv`, `KL_crf_tx.sv`, `KL_crf_rx.sv`, `KL_chan_map_capture.sv` and `milan_datapath.sv` deltas; lint gate; I2S latency probe | R677-1 | f1fda3f1f87c64801e436e129326b5bd5952bf20 |
| Robustness | CLEAN | hold and spoil logic; range and freshness gating; the ten event cases; review PHC step cases (20 us and 7 us) | R677-1 | f1fda3f1f87c64801e436e129326b5bd5952bf20 |
| Tests | UNCLEAN (F1, F2, F3) | `media_phase` suite and campaign; probes P1 to P3; `capture_coherence` legs and campaign; `chmap_capture`; `crf_tx`; `milan_dp` fixture diffs | R677-1 | f1fda3f1f87c64801e436e129326b5bd5952bf20 |
| Docs | UNCLEAN (F1, F2, F4) | MEDIA_CLOCK_FOLLOWING Phase alignment; TIME_SYNC; REGISTER_MAP; compliance matrix; TESTING; CI_WORKFLOWS; CHANGELOG; source comments; docs_check, module matrix and gPTP docs gates | R677-1 | f1fda3f1f87c64801e436e129326b5bd5952bf20 |

## Real limits of this round

- `milan_dp` was not re-run. The re-timed fixtures were judged by diff (checks unchanged) and by the author's shard-0 receipt at `f1fda3f1`.
- No Yosys, no route-1x1 and no resource gate. The author's receipt `route_a6ae20f9` (RTL identical to the head) reports LUT +31, FF +288, slice +60, WNS +0.276 ns, gate exit 0. It was not reproduced here.
- Docs gates run here: `docs_check`, `gen_module_matrix --check` and `check_gptp_docs`, plus an em-dash grep of the added lines. `gen_toc --check` and `check_em_dash.py` were not run, because the pinned Markdown renderer lock is not installed on this host. The new CHANGELOG contents anchor was checked by hand.
- Hosted checks at the exact head were mostly queued or in progress at my snapshot (`receipts/hosted_checks_snapshot.txt`).
  - Executed and successful: `full-ci-gate`, `bdd-conformance` and `Prepare pinned Yosys`.
  - Skipped: `Physical gPTP`.
  - Executed: no hosted Verilator or Yosys shard.
- The `media_phase` loop cases scale the clocks (3.125 MHz datapath, 768 kHz audio) but keep the 512 ms window and the plant gain. The pin and `capture_coherence` legs run at 50 MHz and 24.576 MHz.
- Physical calibration was NOT RUN. Simulation is not hardware proof. The bench proof (the #764 method) is the manager's after merge and is not counted as a finding.
- The host was shared with other heavy jobs (load 40 to 75), so no wall-clock figure here is a budget measurement.

## Pending manager and owner duties

- The current-dev candidate merge (live dev `78ca9bdf`): builder and native banks at the merge turn.
- Hosted exact-head acceptance: `verilator-suites`, `yosys-portability`, docs, elaborate.
- Watch `capture_coherence`'s 2,400 s window. The author's shard-2 sweep timed out at it on two CPUs, and the suite passed alone on eight in 1,274 s.
- `media_phase`'s 900 s window is provisional (F4).
- The post-merge bench proof with the #764 method: 10 minutes plus the INTERNAL and unbind re-engagements, every engagement inside +/-5 % of Ps.
- Owner decisions the executor published, still open:
  - Listener compensation: the render path presents by fill, not at the timestamp.
  - Re-recording the area endpoints on the merge result.
  - The AAF phase follow-on.
  - F1's blend I2S interface, if it is not fixed in-lane.

## Receipts (each listed in MANIFEST.sha256)

- `receipts/media_phase.log` and `.rc`: the clean suite, pins plus ten cases, 129 checks, 0 failures.
- `receipts/media_phase_mutants.log` and `.rc`: 27 checks, 0 failures.
- `receipts/cc_run_dp.log` and `.rc`: `capture_coherence` junction and dp legs.
- `receipts/cc_mutants.log` and `.rc`: the `capture_coherence` campaign, 35/35.
- `receipts/chmap_capture.log` and `.rc`, `receipts/crf_tx.log` and `.rc`.
- `receipts/lint_rtl.log`, `receipts/docs_check.log`, `receipts/module_matrix.log`, `receipts/gptp_docs.log`.
- `receipts/probes/*`:
  - P1, P2 and P3 over the ten cases (`obj_p<n>.<case>`);
  - the PHC step cases on the clean RTL (`obj_clean2`) and on P1 (`obj_p1b`).
- `receipts/blend_probe.txt`, `receipts/blend_probe_build.log`, `receipts/loop_model.txt`, `receipts/hosted_checks_snapshot.txt`, `receipts/verilator_version.txt`, `receipts/clone_verification.txt`.
- Scripts:
  - `scripts/run_probes.sh`, `scripts/probes/*.patch`, `scripts/probes/jobs.txt` (the first batch's job list);
  - `scripts/blend_probe/blend_wrap.sv`, `scripts/blend_probe/sim_blend.cpp`, `scripts/blend_probe/run.sh`;
  - `scripts/loop_model.py`.

Host paths in the receipts are replaced by `<verilator-root>`, `<verilator-5.050>`, `<packet>`, `<clone>` and `<tmp>`.

All probes ran in disposable copies under the packet's `scratch/`. The review clone is at the exact head: index equal to the tree, clean status, gitlinks unchanged.

R677-1 FINISHED
