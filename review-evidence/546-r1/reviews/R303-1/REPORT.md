[R303] NEGATIVE - exact head 39a0171c8c39e68065b14b9178b30d708a9f7645

Round R303-1, cleared-context external review of PR #554 (issue #546). Head `39a0171c8c39e68065b14b9178b30d708a9f7645`, tree `5399d73e1e581116e8cc8dd9f82ead83bbf3c666`, source base `57456af96b3127b9d309a995bbbd35a6113ce52d`. All five lenses were applied at this head.

## Summary

The RTL does what the issue asks. `KL_crf_rx` restarts its 256-interval rate ring on a `tu` edge, an adjacent-timestamp jump beyond 2048 ns, or a sequence gap. It holds `rate_o` at the last clean value, and `rate_valid_o` stays low until 256 clean intervals follow the event. The servo samples only valid history. I found no RTL defect. Every detector term I mutated in isolation is killed by `sim_discontinuity.cpp` (10 of 10 reviewer mutants, plus the author's 4 of 4).

Acceptance 2 holds in the RTL, but the in-tree connected GM-change test cannot show it. `sim_talker_step.cpp` passes 19 of 19, bit-identically, with the jump backstop removed, with both detectors removed, and with the servo ignoring validity. The local PHC step 100 ms after the talker step is what protects the integrator: the #539 guard abandons the open window, and the re-based window closes after the ring has aged the talker step out. The scenario's "withholds crossing samples" check is satisfied by a one-clock artefact of how the harness drives the receiver. A reviewer variant that steps the listener first and the talker 100 ms later discriminates. The head passes it with the integrator unchanged. With both detectors removed it reproduces the issue's -115.7 ppm excursion, and the servo drops to ACQUIRE. That test gap is F1 (MAJOR). F2 and F3 are MINOR; S1 and S2 are optional.

## Findings

### F1 - MAJOR - Tests - the connected GM-change scenario cannot fail for the defect it claims to detect

- Artifact: `tb/verilator/crf_rx/sim_talker_step.cpp:124-129` (event order in `gm_change`) and `:66` (`saw_invalid` reads the combinational `rate_valid_o`). The same scenario is described in `docs/design/GM_LOSS_RECOVERY.md` (test table row "`crf_rx` talker_step") and is the PR's evidence for acceptance 2.
- Authority/evidence: AGENTS.md section 6, Tests lens: "Each new test can fail for the defect it claims to detect". Receipts `receipts/mutant_probe_part2b.txt`, `receipts/mutant_probe_part2c.txt`:
  - `C2_jump_removed` (unmarked -150 us case has only the backstop): rc 0, 19/19 PASS, integrator 30.703..30.723 ppm, same as the clean head.
  - `C3_tu_and_jump_removed` (no receiver talker-step isolation at all): rc 0, 19/19 PASS, bit-identical trajectory.
  - `C4_servo_ignores_valid`: rc 0, 19/19 PASS.
  - `C5_rx_valid_forced` (port tied high): killed only by "receiver withholds crossing rate samples", with the integrator unaffected.
- Mechanism, from the harness and the RTL:
  1. The talker steps first and the listener 100 ms later.
  2. The listener step trips the #539 detector (`KL_mmcm_drp_servo.sv:662-666`), which abandons the open window.
  3. The re-based window closes about 613 ms after the talker step. The ring stops spanning the step 512 ms after it.
  4. So no servo boundary reads contaminated history unless one happens to fall in the 100 ms gap. None does at this phase.
  5. Separately, the harness raises `frame_p_i` with the rising edge and holds it until the next one. Read after the accepting edge, the combinational `rate_valid_o` is then low on every PDU, because `w_acc` is still true against the just-updated `prev_ts_ns_r`/`exp_seq_r`. `receipts/probe_artifact.log`: 300 of 300 clean PDUs read low on the port and 0 of 300 on `rate_valid_r`. So `saw_invalid` is satisfied with or without any detector.
- Discriminating counter-evidence (`probes/probe_gm_order.cpp`, the same harness with only the order swapped and `saw_invalid` reading `rate_valid_r`; `receipts/mutant_probe_part3.txt`, `receipts/mutant_probe_part4.txt`, `receipts/mutant_probe_part2d.txt`):

  | Case | Checks | Integrator range | Servo state |
  |---|---|---|---|
  | Head | 19/19 | 30.703..30.723 ppm | 4 (LOCKED) throughout |
  | Jump removed | 3 failures | up to 177.188 ppm | 3 (ACQUIRE) |
  | Both detectors removed | 6 failures | -115.742 ppm, the issue's -115.82 | 3 (ACQUIRE) |
  | Servo ignores validity | 1 failure ("invalid sample cannot update the integrator") | - | - |
  | `tu` ignored | passes: the 150 us marked step is also caught by the backstop, as designed | - | - |
- Impact: the published acceptance-2 evidence, "The servo remains LOCKED ... The integrator is unchanged", would be equally green if the fix regressed or were absent. The sweep therefore has no connected regression for the behaviour #546 adds. The unit-level arms (`sim_discontinuity.cpp`, U13) cover the pieces but not the receiver-to-servo claim.
- Required outcome: the connected GM-change evidence must fail when the receiver's talker-step isolation is removed. At minimum that means both detectors removed; for the unmarked case it also means the jump backstop removed. That needs at least one arm in which a servo boundary falls while the ring spans the talker step. The listener-first order does this deterministically at this head; a phase sweep would also work. The "withholds" check must observe edge-sampled or registered validity, not the combinational port after the accepting edge. The existing talker-first arm can stay as a second ordering.
- Verification: rerun the connected target clean and with the three mutants above. Clean must pass. Jump-removed and both-removed must fail on an integrator or lock check, not only on the validity observation.

### F2 - MINOR - Conformance, Docs - the jump threshold's derivation cites an authority for a term that authority does not state

- Artifact: `hdl/ieee1722/crf/KL_crf_rx.sv:274-281` ("Bound legitimate spacing using Milan Annex B.1.1's 100 ppm media clock ...") and `docs/design/TIME_SYNC.md:190-192` ("+/-100 ppm media ...", no authority).
- Authority/evidence: the repository's own authority records use Milan v1.2 Annex B.1.1 for the rule that `tu` is 1 for 0.25 s on a grandmaster change. See `docs/reference/REGISTER_MAP.md:750`, `hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv:36`, and the issue's own citation. The only +/-100 ppm Annex B.1.1 row is `docs/reference/MILAN_COMPLIANCE_MATRIX.md:228`, under section "IEEE 802.1AS". That is the LocalClock (PHC oscillator) frequency accuracy, not a media-clock bound. The quantization term (2 x 384 ns, `incr + adj`) is this design's `timestamp_counter` bound. The derivation applies it to a remote talker's CRF timestamps without saying that is an assumption.
- Impact: the #546 assignment asked for a threshold "derived from, not mirrored from" the #539 rationale. A cold reader following the cited clause cannot reproduce the first input, and nothing records that the second input assumes a talker built like this one.
  - This is not a functional defect. The value has margin: the harness's +/-601 ns sustained drift and the 2048/2049 boundary pass at the head. In the reviewer probe, +/-500 ns random timestamp jitter over 4 s never invalidates the registered validity (`receipts/mutant_probe_part2d.txt`, phase C). The 2048/4096/1024 mutants are killed.
- Required outcome: cite the actual source of the media-clock accuracy term, or state it as a design assumption with its rationale. Record that the quantization term is the local PHC's bound, assumed for the remote talker. Keep the RTL comment and TIME_SYNC consistent.
- Verification: text inspection of the two locations against the cited clauses.

### F3 - MINOR - Tests, Docs - the receiver mutation arm runs in no gate and is missing from the explicit-campaign list

- Artifact: `tb/verilator/crf_rx/Makefile:52-79` (`all: run`, `run: unit discontinuity talker_step`, `mutants` separate). `docs/testing/TESTING.md:257-266` (explicit-campaign rule and table) and `:462` (suite row). `scripts/run_all_suites.sh:390` runs `make -C <suite>`, the default target only.
- Authority/evidence: TESTING.md says "A long mutation campaign is an explicit target, never a raised deadline. #367 settled that rule and this page keeps the list of such targets." This campaign is not long: `receipts/crf_rx_author_mutants.log` shows 26.62 s wall on this host for five small builds. Suites of the same size run their arm by default (`tcam`, "~25 s, four extra Verilator builds"; `render_setpoint`; `gptp_shadow`). The explicit-campaign table does not list it.
- Impact: acceptance 1's "failing arm" was demonstrated once. A later change that makes `sim_discontinuity.cpp` blind to a detector passes every sweep.
- Required outcome: either the default target runs `mutants`, or TESTING.md's explicit-campaign table lists it with who runs it, per its own rule.
- Verification: `make -C tb/verilator/crf_rx` output includes the mutant verdicts, or the table row exists.

### S1 - SUGGESTION - Robustness - sustained invalidity is an unbounded, invisible hold under a LOCKED label

- Evidence: `receipts/mutant_probe_part2d.txt`, phase D. Starting from LOCKED, +/-1200 ns source timestamp jitter keeps `rate_valid_r` low for 99.7 % of 6 s. Through it the servo reports state 4, the integrator is frozen at 30.703 ppm, the `MCSRV_STAT[15:10]` discard tally does not move, and `CRF_RATE` shows a plausible held value. This is the documented "no CSR bit or counter" choice.
- Optional: bound the hold (for example, fall to HOLDOVER after N skipped windows) or expose sustained invalidity. It is not blocking. `tu` flapping and sequence gaps already show in Table 5.6 counters, and more than 1.4 us of timestamp noise is outside the derived envelope.

### S2 - SUGGESTION - Docs - wording

- `docs/reference/REGISTER_MAP.md:838` (`CRF_RATE`) dropped what the value measures ("the talker's media clock measured against gPTP - the servo frequency input").
- `docs/design/GM_LOSS_RECOVERY.md:152` reads "(#539); The receiver ...", with a capital after the semicolon.

## Lens results

- `[R303] PASS RTL - hdl/ieee1722/crf/KL_crf_rx.sv:274-395,514-519,540-547,583-599,611-616; hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:249,561-571; hdl/milan/milan_datapath.sv:1725,5488,5547` - checked against issue #546 acceptance 1 and the servo contract:
  - Refill boundary: the break PDU seeds, and the first read after the break reads the break timestamp (`D9` and the author's `refill_short` are killed).
  - Widths: the 64-bit wrapping spacing catches both signs and the 2^32 aliases (`D5` killed); the natural 64-bit rollover stays clean.
  - Pending-rate collision (`D6` killed).
  - Reset, bind-rise and silence invalidation (`D3`, `D4` killed). STOP gating (`D2` killed). Sequence gaps (`D1` killed). Falling `tu` edge (`D10` killed).
  - Same `axis_clk` domain for receiver and servo, so no CDC.
  - Servo change is confined to the `pp_run_r` qualification; guard logic is untouched.
  - Area: head `KL_crf_rx` 433 LUT / 544 FF / 147 CARRY4 / 1 RAMB18, identical to the published figure. The base measured 368 LUT here against the published 355, so the published LUT delta is not an understatement. +35 FF is 32 upper timestamp bits plus 3 flags; the lower 32 bits merge with `ts_new_r`. Receipt `receipts/area_probe.log`.
- `[R303] PASS Robustness - tb/verilator/crf_rx/sim_discontinuity.cpp:105-178 at head plus probes/probe_talker.cpp` - checked against the #546 false-positive and lifecycle claims:
  - Malformed and foreign markers.
  - Duplicate and lost PDUs.
  - STOP, silence, rebind, reset.
  - 64-bit rollover.
  - Both 2^32 aliases.
  - Back-to-back pending collision.
  - A legitimate 300 ms `tu` pulse with no step: one registered invalidation episode of the `tu` hold plus one 256-interval refill, LOCKED throughout, integrator within 0.02 ppm.
  - +/-500 ns random timestamp jitter: 0 invalid clocks over 4 s.
  - Receipts `receipts/mutant_probe_part1_disc.txt`, `receipts/mutant_probe_part2d.txt`.
  - S1 is a suggestion only.
- Conformance: UNCLEAN, F2. What was checked:
  - Acceptance 1 is met: the discontinuity harness has a failing arm (author 4/4 and reviewer 10/10 kills).
  - Acceptance 2 is met by the RTL: in the listener-first variant the head stays LOCKED with the integrator unchanged for both +/-150 us cases, and the no-isolation mutant reproduces the issue's -115.7 ppm.
  - Acceptance 3: the manager's gates and the exact-head hosted checks are green.
  - `tu` handling is consistent with IEEE 1722-2016 4.4.4.7 and 10.4.5 as the repository cites them. Either edge restarts; a held level does not block recovery.
- Tests: UNCLEAN, F1 and F3.
- Docs: UNCLEAN, F2 and F3.

## Reviewer ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2) | issue #546 body and assignment comment; `KL_crf_rx.sv:274-395`; TIME_SYNC.md:147,167-213; REGISTER_MAP.md:750,838; MILAN_COMPLIANCE_MATRIX.md:228; `KL_ptp_clock_validity.sv:30-40`; probes/probe_gm_order.cpp results | R303-1 | 39a0171c8c39e68065b14b9178b30d708a9f7645 |
| RTL | CLEAN | `KL_crf_rx.sv` full; `KL_mmcm_drp_servo.sv:240-700`; `milan_datapath.sv:1725,5444-5560`; D1-D10 and author mutants; area_probe.log | R303-1 | 39a0171c8c39e68065b14b9178b30d708a9f7645 |
| Robustness | CLEAN (S1 suggestion only) | `sim_discontinuity.cpp`; probes/probe_talker.cpp phases B, C, D, E; D1-D10 | R303-1 | 39a0171c8c39e68065b14b9178b30d708a9f7645 |
| Tests | UNCLEAN (F1, F3) | `sim_talker_step.cpp`, `crf_talker_wrap.sv`, `sim_discontinuity.cpp`, `mutants.py`, `Makefile`, `sim_main.cpp` diff, `mmcm_servo/sim_main.cpp` U13; C1-C5, O0-O4, probe_artifact | R303-1 | 39a0171c8c39e68065b14b9178b30d708a9f7645 |
| Docs | UNCLEAN (F2, F3) | TIME_SYNC.md, GM_LOSS_RECOVERY.md, REGISTER_MAP.md, TESTING.md, MODULE_MATRIX.md, README-tests.md diffs; PR body; issue REVIEW READY comment | R303-1 | 39a0171c8c39e68065b14b9178b30d708a9f7645 |

## Executed evidence at this head

The runs used an exported copy of the exact head under the private scratch area. The clone itself was not modified; see Limits for the one exception, which I removed. Simulator: Verilator 5.050 rev v5.050 through the pinned wrapper, whose sha256 is `905795b9...979e92f`.

- `make` in `tb/verilator/crf_rx`: rc 0 (local tool and packet paths in its compile log are replaced by placeholders). Unit 13,836 checks, discontinuity 1,658, talker_step 19, all passing. Integrator 30.723 ppm steady; +150 us 30.723..30.723; -150 us 30.703..30.723. Receipt `receipts/crf_rx_default.log`.
- `python3 mutants.py`: rc 0, 4 of 4 killed, 26.62 s wall. Receipt `receipts/crf_rx_author_mutants.log`.
- Reviewer runner `probes/mutant_probe.py` with `probes/probe_talker.cpp` and `probes/probe_gm_order.cpp`:

  | Receipt | Contents | Outcome |
  |---|---|---|
  | `mutant_probe_part1_disc.txt` | clean plus D1-D10 | all 10 killed |
  | `mutant_probe_part2a.txt` | clean talker; C1 | clean passes; C1 passes, which is expected |
  | `mutant_probe_part2b.txt` | C2, C3 | both survive, F1 |
  | `mutant_probe_part2c.txt` | C4, C5 | C4 survives; C5 killed only by the artefact-dependent check |
  | `mutant_probe_part2d.txt` | false-positive probe; O1 | probe passes |
  | `mutant_probe_part3.txt` | O0, O2 | O0 clean; O2 killed |
  | `mutant_probe_part4.txt` | O3, O4 | both killed |

  An earlier full run graded `make`'s rc 2 as "survived". I fixed the grading and re-ran every case; only the re-run receipts are published.
- `probes/probe_artifact.cpp`: 300/300 PDUs read low on the port and 0/300 on the register. Receipt `receipts/probe_artifact.log`.
- `area_probe.sh` (synthesis tool 0.66, native front-end; the servo needs an SV front-end this host lacks): `receipts/area_probe.log`.
- Hosted exact-head check runs, read-only: 21 executed contexts succeeded, including rtl-fast, verilator-suites and its five shards, yosys-portability and its four shards, docs-check, elaborate and lint. "Physical gPTP (nightly and manual)" was skipped, not executed.
- Clone integrity after all probes: HEAD, tree, index and tree agree. 885 tracked blobs match by content and mode, and the 4 gitlinks are unchanged. Receipt `receipts/clone_integrity.txt`.

## Prior public findings on this PR

I read these only after my own pass, verdict and ledger above were written. At round start the PR carried only the two review-start comments. During this round the internal round R302-1 published `[R302] NEGATIVE` on the same head (PR comment 5817998312). Disposition of its items at this head:

| Prior item | Status at `39a0171c8` | Relation to this round |
|---|---|---|
| R302-1-F1 MAJOR (Tests, Docs): the connected GM-change harness cannot fail for the #546 defect | **Retained, open.** No commit since. My C2, C3 and C4 survivors and the 300/300 artefact probe reproduce it independently. | Same defect as F1 here. I record it under Tests; R302 also records Docs for the published acceptance-2 evidence text. Per AGENTS.md section 3, both lens attributions stand, and neither lens is clean. |
| R302-1 S1 (Docs): the 100 ppm term credited to Annex B.1.1 as a "media clock" | **Retained, open.** | F2 here, which I rate MINOR (Conformance, Docs). The cited clause is the one the repository uses for the `tu` hold rule. |
| R302-1 S2 (Tests): `mutants` outside `all` | **Retained, open.** | F3 here, which I rate MINOR (Tests, Docs) under TESTING.md's own explicit-campaign rule. |
| R302-1 S3 (Docs): the servo banner omits the new validity skip | **Concur, retained as a suggestion.** I did not file it separately. | - |
| R302-1 S4 (Robustness): unmarked-jump discards are uncounted, and the servo is frozen while LOCKED | **Retained, suggestion.** | S1 here. My probe phase D reproduces it. |
| R302-1 S5 (Docs): capital after the semicolon | **Retained, suggestion.** | S2 here. |

R302-1 also recorded an informative limit: an unmarked 2,000 ns talker step, below the backstop by construction, moves the servo from LOCKED to ACQUIRE. I did not re-run that case. It is consistent with the threshold's stated band, which sits below the plane's smallest 20 us step.

## Limits

- Physical calibration and hardware: not run. Nothing here is hardware evidence, and the skipped physical gPTP context is not a pass.
- Timing closure: not evaluated. The new 64-bit subtract and compare sit on the accept cone and feed the servo's `pp_run_r` combinationally. There is no place-and-route evidence for this head.
- Area: the servo's +2 LUT was not independently measured, because this host's synthesis front-end cannot parse `KL_mmcm_drp_servo.sv`.
- Remote talkers: I checked the threshold only against synthetic uniform jitter. I have no data on real third-party CRF talker timestamp noise.
- The mmcm_servo, mmcm_servo_autorepair and milan_dp suites were not re-run by me. I read U13 but did not execute it.
- The default suite and the author's campaign use the Makefile's `--build -j 0`. That target's C++ compile briefly used every host core, more than the 8-job budget. My own runner forced `-j 4` with two cases at a time.
- My area probe ran the synthesis tool with the clone as its working directory, and its ABC step created an empty ignored `abc.history` there at 17:39. I removed it before the integrity check. No tracked byte was affected.

## Pending manager duties

- Final current-dev candidate build and validation at the merge turn.
- Hosted and `act` acceptance.
- Publication of this report and the manifest-listed receipts.
- Re-review after F1-F3 are addressed. A commit that touches the harness or docs un-covers Tests and Docs, and any RTL touch un-covers RTL and Robustness.

R303-1 FINISHED
