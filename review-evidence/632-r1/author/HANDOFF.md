# A659: milan-fpga #632 + #764 (phase-align the recovered media clock to the followed CRF)

**Status: REVIEW READY at `f1fda3f1` (2026-10-20, session 5).** Every gate passes at the head (gate table below):
the sweep (64 of 64 suites), the 17 phase mutants, route-1x1 within the resource gate and timing floor (at
`a6ae20f9`, RTL identical), lint, Yosys and the docs gates. route-1x1 had failed at `e96f3928` (R1); the servo
shrink passed it at `5537cc41` (R2) and again with the window cap at `a6ae20f9` (R3). The sweep found two fixture
timings that assumed the retired CRF divider (D5), fixed in `33a460db` and `f1fda3f1`. REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6299127112 (head `f1fda3f1`).

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6284510903
- Addendum 1 (in/out latencies at the pins): https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6284578201
- Addendum 2 (one reference per media clock domain; replaces addendum 1 item 1): https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6284659263
- #764 report: https://github.com/kebag-logic/milan-fpga/issues/764#issuecomment-6283948176
- Lane: branch `632-764-media-phase` from dev `e26f1816` (checked: `git merge-base HEAD origin/dev` = e26f1816;
  origin = https://github.com/kebag-logic/milan-fpga.git). Not pushed (pushing is outside this lane).
- TAKEN (session 1): https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6284564768. Not re-posted.
- REVIEW READY (session 5, head `f1fda3f1`): https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6299127112

## Session history

| Session | What happened |
|---|---|
| 1 | TAKEN posted; stopped by the manager for addendum 1. No commit. |
| 2 | Stopped by the manager for addendum 2. No commit. |
| 3 | Four commits: `cd39fea0` servo phase loop; `b7d3ad20` domain event, phased CRF output, AAF time base; `5081c7b2` media_phase bench and two-interface pins; `dac4ce37` capture_coherence `[PIN]` leg. Cut by a host reset (memory error) at 10:00 with an uncommitted media_phase Makefile/suite-budget change. |
| 4 | Resumed 12:07. Found and fixed two defects in session 3's design (D1, D2 below) and one robustness gap (D3); committed the session-3 leftovers; wrote the docs; ran the gates. route-1x1 at `e96f3928` failed the resource gate (R1 below); began shrinking the servo, uncommitted, when the host reset at 14:01. |
| 5 | Resumed 14:10. Validated the shrink (all media_phase cases pass, OOC 1168 LUT / 982 FF), fixed six stale comments and the clamp mutant's removed anchor, added the HOLDOVER and INTERNAL let-go mutants, committed `6f4a2b46` + `5537cc41`; route-1x1 at `5537cc41` PASSED (R2). Found a window-phase wrap under a talker sending faster than it declares (D4) and capped the window (`e887d937`, `a6ae20f9`); route-1x1 passed at `a6ae20f9` (R3). One mutant survived the 16-bit phase (fixed, `e85df091`). The sweep found D5 (two `milan_dp` fixture timings, `33a460db`, `f1fda3f1`); every gate then passed at `f1fda3f1`; REVIEW READY posted. |

## Commits (base `e26f1816`)

| Commit | Subject |
|---|---|
| `cd39fea0` | Phase the media servo to the followed CRF stream: an exact fold, a type-2 term under a slew limit, and an integrator that carries its odd errors |
| `b7d3ad20` | Stamp the CRF output and the AAF talkers from the clock domain's media event, back-dated by each interface's derived latency |
| `5081c7b2` | Grade the phase loop at the silicon window and two interfaces at their pins, with a planted defect per loop term |
| `dac4ce37` | Grade the shipping talker's timestamps against its TDM pins in the coherence datapath leg |
| `9ca025c9` | Carry each frame's instant through the capture crossbar, count the marker latency to the frame's closing pair, re-fold the phase on a PHC slew, and grade three interfaces at their pins |
| `e96f3928` | Document the phase contract per source, the domain event and per-interface constants, the listener decision and the -0.46 Ps accounting (#632, #764) |
| `0ee46622` | Name the new event ports by their unit, split the phase harness's multi-declarators, and register the media_phase budget and mutation reader with the test-evidence gate |
| `f49851da` | Regenerate the module matrix and the CDC census for the domain event and the retired CRF divider crossing, and record the media_phase budget |
| `974f17df` | Follow the domain event's renamed PHC port in the phase campaign's back-dating anchor |
| `6f4a2b46` | Fold each phase sample to its own nearest period, take the window phase as its sum over the nominal PDU count on the low 32 bits of each instant, and grade the phase term's let-go at every hold |
| `5537cc41` | Document the per-sample fold, the window sum and the hold conditions with their let-go mutants (#632) |
| `e887d937` | Cap the phase window at the nominal count plus 1/32 so a talker sending faster than it declares cannot wrap the window phase, and grade the cap with a burst case |
| `a6ae20f9` | Document the phase window's sample cap and its burst case (#632) |
| `e85df091` | Give the uncentred-fold mutant the one phase bit its range needs, so it plants a fold into [0, Ps) rather than one that wraps back to the centred reading |
| `33a460db` | Size the #726 TX wrap run in TDM frames: the CRF talker now stamps every 96th domain event, and the counters fixture clocks the TDM bus with axis_clk |
| `f1fda3f1` | Wait out the CRF talker's slower cadence in the nxn legs: with no audio frame running it stamps every 96th media tick, 200,000 clocks at 100 MHz |

## R1: the resource gate at `e96f3928`, and the shrink

route-1x1 at `e96f3928` (`receipts/route_e96f3928/`): LUT 50,329 (+716 against the 49,613 record; tolerance +500),
FF 53,072 (+719; +600), SLICE 15,802 (+77; +80), DSP 14 (+0), WNS 0.048 ns (floor 0.030), WHS 0.033. Gate exit 1.
Per block against a route of the recorded baseline's RTL (another lane's route of dev `e9cbb676`, which equals the
record in every figure; `e26f1816` differs from it only in firmware tests and docs): servo +581 LUT / +381 FF, domain
event +6 / +79, CRF rx -11 / +65, CRF tx -22 / +51, capture crossbar -19 / +64; outside this lane's logic the
processor wrapper moved +384 LUT and the gPTP shadow -233 (no RTL change there: optimisation movement). The worst
setup path is in the soft CPU's DMA bridge (20 levels, 100 MHz), not in this lane's logic.

The shrink (`6f4a2b46`), each step measured with `syn/yosys/ooc.sh KL_mmcm_drp_servo` (`receipts/ooc/`):
base 865 LUT / 792 FF; `974f17df` 1,457 / 1,183; now 1,168 / 982.
- the PDU-to-PDU unwrap and its runaway re-fold removed: each sample folds to its own nearest whole period, so every
  pull is the short way by construction (the slew case's 27 us re-acquired as its 6.2 us fold, as before);
- the window mean's division removed: Theta is the window sum over the nominal 256 PDUs, a shift (a short window
  only pulls less; it reads settled only when full); the divider is now by the constant Ps alone;
- the detector takes the low 32 bits of the domain event and of the CRF timestamp (their difference is exact within
  2^31 ns; the fold range is 2^25 ns, 33.5 ms, against a 2 ms default Max Transit Time);
- the PI operand 48 -> 40 bits; `KL_crf_tx`'s registered event instant dropped (the engine takes `ev_ns_i` on the
  event's cycle);
- the hold replaces the re-fold: every hold condition lets the term go and spoils the open window. Each case now
  grades the let-go (`phase_o[20]` low within 5 to 200 ms of its event), with a mutant per hold condition.

## R2: route-1x1 at `5537cc41` passes

`receipts/route_5537cc41/`: LUT 49,643 (+30), FF 52,662 (+309), SLICE 15,782 (+57 of +80), RAMB36 74, RAMB18 25,
DSP 14, WNS +0.418 ns, WHS +0.013 ns, route complete; gate exit 0. Per block against the reference route
(`hier_delta_vs_ref.txt`): servo +274 LUT / +180 FF, domain event +6 / +79, CRF rx +8 / +33, CRF tx -17 / -14,
capture crossbar -60 / +63; outside the lane the processor wrapper -106 LUT and the gPTP shadow -238. Comparing the
two routes, the processor wrapper's movement alone swung by 490 LUTs (+384 at `e96f3928`, -106 here) with no
processor RTL change: the route's LUT figure carries a few hundred LUTs of placement-dependent movement that this
lane does not control. The worst setup path is the SoC's AXI-Lite-to-Wishbone bridge, outside the lane.

## R3: route-1x1 at `a6ae20f9` (the head) passes

`receipts/route_a6ae20f9/`: LUT 49,644 (+31 of +500), FF 52,641 (+288 of +600), SLICE 15,785 (+60 of +80), RAMB36 74
(+0), RAMB18 25 (+0), DSP 14 (+0), WNS +0.276 ns (floor +0.030; fall -0.061 is a rise), WHS +0.032 ns (floor 0),
route complete; gate exit 0. Per block against the reference route: servo +264 LUT / +180 FF, domain event +6 / +79,
CRF rx -1 / +33, CRF tx -15 / -14, capture crossbar -5 / +64; processor wrapper -44 LUT, gPTP shadow -232. The
worst setup path is the existing reset synchroniser into the servo's 200 MHz phase-shift domain (`psrst_sync_r`, one
LUT, 3.8 ns of routing, unchanged RTL): placement-dependent, above the floor. Not re-recorded (see the decision).

## D4: the window phase could wrap (found in session 5, fixed)

The window phase is the window sum over 256 in 16 bits; 268 samples near Ps/2 overflow it. `KL_crf_rx` checks
the declared interval (96) and the 2 ms timestamp spacing, but not the arrival rate, and it consumes EARLY PDUs, so
a talker sending faster than it declares puts more than 256 samples in a window while its timestamps stay within the
33.5 ms fold range (about 15 extra). With samples within 0.0015 Ps of Ps/2 that window's phase wrapped sign: one
window's pull, at the slew limit, the wrong way. Fix (`e887d937`): a window keeps at most `PH_CAP_C` = 264 samples
(256 + 1/32); an elaboration guard proves 264 x Ps/2 / 256 inside 16 bits. New `burst` case: the talker sends every
1.92 ms for 0.6 s from a servo window boundary (267 PDUs in 512 ms); the window keeps exactly 264, the phase holds.
Mutant `window_cap_removed` fails `[burst] the window the burst filled kept exactly 264 samples, the cap` (max 267).
OOC unchanged (1,168 / 982).

## Defects found in session 4 (and fixed)

- **D1, the AAF time base latched at the tick (found by the new `[PIN]` check).** `capture_coherence` dp leg,
  engagement DP-band-true+0 (one cycle before the walk's crossing): stamps exactly 20,833 ns off their frame. When a
  frame closes ON the tick's cycle with none pending, the crossbar's walk takes the closing frame (#74 item 2
  coincidence law) but `aaf_tbase_r` latched the domain event of the frame before. Fix: the frame's instant is banked
  in `KL_chan_map_capture` beside the frame and loaded into the walk with it (`tdm_close_ns_i` -> `tdm_frame_ns_r` ->
  `tdm_walk_ns_o`), fed by `KL_media_domain_event.mark_ns_o`. After the fix: max 15 ns at that engagement.
- **D2, the marker latency counted to the frame's end (found by reviewing every shipping shape).** The crossbar closes a
  frame on the last pair it KEEPS (at most four), so on the 8x8 TDM32 shape the marker is pair 3 of 16 (a quarter
  of the frame in) and on the Arty I2S blend it is TDM pair 2; session 3 derived the latency as one whole frame.
  Those shapes' events would have been 0.75 Ps and 0.25 Ps off. Fix: `close_pair()` and `pair_end_bits()` in
  `KL_media_if_latency_pkg`; the datapath derives from `CMAP_TDM_FRAME_PAIRS_C`. The 1x1 value is unchanged
  (20,964 ns). New interface C in the synthetic shape: the 8x8's own TDM32 front end on 98.304 MHz, graded at
  every slot's pin, max 30.6 ns; its planted control (C counted to the frame's end) fails.
- **D3, a PHC policy slew did not re-fold (found by review against #545).** A slew below the unwrap's runaway bound
  (87 us) accumulated in the unwrapped phase and the loop pulled it back the long way. Fix: `phc_slew_q_r` in
  `ph_hold_w`. New `slew` case (27 us at 200 ppm): re-acquired in 20.0 s from +0.30 Ps, the short way; its
  planted control fails (phase out of band, 10,325 ns). Superseded in session 5: no unwrap remains, so the slew
  now holds the term (graded by the let-go check and `slew_hold_removed`) and the short way is the fold's.

## Changes (file:line at `f1fda3f1`, clause)

| File:line | Change | Clause |
|---|---|---|
| `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:46-92` | banner: the phase term, its per-sample fold, window sum, cap, gains, poles, slew limit, hold conditions | Milan v1.2 7.6.1; IEEE 1722-2016 10.7 Eq. 14, 10.8 Eq. 15, 4.3.5 |
| `KL_mmcm_drp_servo.sv:323-333` | parameters `FS_HZ_P`, `PH_GAIN_LSH_P`, `PH_SLEW_NS_P`, `PH_MIN_PDU_P`, `PH_SETTLE_WIN_P` | 10.8 |
| `KL_mmcm_drp_servo.sv:438` | `IF_C = 8` integrator fractional bits (#764 floor) | 7.6.1 |
| `KL_mmcm_drp_servo.sv:444-507` | Ps as 62,500/3 exactly; fold range 2^25 ns; nominal 256 PDUs per window; `PH_CAP_C` 264 with its guard; slew clamp | 10.8, Milan 7.3.2 |
| `KL_mmcm_drp_servo.sv:703` | `ph_hold_w`: outside LOCKED, term off, mr toggle, broken history, PHC step or slew | 10.8 |
| `KL_mmcm_drp_servo.sv:763-831` | `phase_det`: per-PDU exact fold in 1/3 ns (restoring divider by Ps), window sum capped at 264, Theta = sum >> 8, verdicts | 10.7, 10.8 |
| `KL_mmcm_drp_servo.sv:836` | `pi_isum_x_w`: integ + e/2 + phase term in fixed point | 7.6.1 |
| `KL_mmcm_drp_servo.sv:948` | the phase term clamped to the slew limit, one window late | 10.8 |
| `KL_mmcm_drp_servo.sv:1308-1318` | `ph_settled_o`, `phase_o`; `MCSRV_STAT[9]` | 10.8 |
| `hdl/ieee1722/crf/KL_media_domain_event.sv` (new) | the domain media event: marker back-dated, `mark_ns_o`, liveness, alt tick | 4.3.5, 10.8 |
| `hdl/ieee1722/crf/KL_media_if_latency_pkg.sv:78-118` (new) | `cyc_ns`, `half_cyc_ns`, `close_pair`, `pair_end_bits`, `mark_lat_ns`, `slot_msb_ns` | 4.3.5, 10.8 |
| `hdl/ieee1722/crf/KL_crf_tx.sv:388-394`, `:480-483` | event grid = every 96th domain event; ts = its instant + Eq. 14 offset; /512 divider and its cdc_pulse retired | 10.7 Eq. 14, 4.3.5 |
| `hdl/ieee1722/crf/KL_crf_rx.sv:488` | `ts_p_o`/`ts_o`: the consumed timing point | 10.8 |
| `hdl/ieee1722/aaf/KL_chan_map_capture.sv:451`, `:654`, `:1284` | the frame instant banked with the frame and loaded into the walk (D1) | 4.3.5, 10.8 |
| `hdl/milan/milan_datapath.sv:6078-6108` | domain event, closing-pair latency (D2), AAF time base from the walk (the packetizer reads its low 32 bits) | 4.3.5, 10.8 |
| `milan_datapath.sv:6150-6155`, `:6320`, `:5948` | servo phase operands (low 32 bits); CRF output events; CRF rx timing point | 10.8 |
| `sw/litex/milan_soc.py`, `syn/yosys/run.sh`, `syn/yosys/ooc.sh`, `tb/verilator/milan_dp/Makefile` | source lists for the two new files | -- |
| `scripts/lint.budget` | crf 4 -> 3 (one SYNCASYNCNET fewer with `KL_crf_tx`'s cdc_pulse gone) | -- |
| `scripts/run_all_suites.sh`, `scripts/suite_shards.py`, `scripts/measure_test_evidence.py`, `scripts/measure_test_evidence_readers.py` | media_phase budget 900 s (provisional), its reader disposition | -- |
| `tb/verilator/milan_dp/stream_counters.py:180-189`, `stream_counters.hpp:300-304`, `sim_nxn.cpp:5046-5052`, `:7757-7760` | fixture waits sized for the CRF talker's domain-event cadence (D5) | -- |
| docs: `docs/design/MEDIA_CLOCK_FOLLOWING.md` (Phase alignment), `docs/design/TIME_SYNC.md`, `docs/testing/TESTING.md`, `CHANGELOG.md`, generated module matrix and CDC census, `hdl/*/README-tests.md` | contract, constants, decision, accounting, proof table | -- |

No top-level port, no register-map layout change: one reserved read-only bit, `MCSRV_STAT[9]`, now reads the phase
settled (STOP condition 1 allows new read-only status fields). Module ports changed: `KL_mmcm_drp_servo` (phase
inputs, `phase_o`, `ph_settled_o`), `KL_crf_tx` (`clk_audio_i`/`ptp_ns_i` -> `ev_p_i`/`ev_ns_i`), `KL_crf_rx`
(`ts_p_o`/`ts_o`), `KL_chan_map_capture` (`tdm_close_ns_i` defaulted, `tdm_walk_ns_o`).

## New checks (planted mutant, failing words)

media_phase campaign (`make -C tb/verilator/media_phase mutants`), 17 mutants (`tb/verilator/media_phase/phase_mutants.py`):

| Mutant | Case | Required failing check |
|---|---|---|
| phase_term_removed | engage | `[engage] phase inside +/-5 % of Ps within 45 s of the event` |
| phase_sign_flipped | engage | `[engage] phase held inside +/-5 % of Ps to the end` |
| rate_damping_removed | engage | `[engage] phase inside +/-5 % of Ps within 45 s of the event` |
| integrator_floored | carry | `[carry] the integrator moved by exactly sum(e) / 2 (no LSB floored)` |
| slew_clamp_removed (clamp at Ps/2) | engage | `[engage] the pull is slew-limited` |
| fold_not_centred | engage2 | `[engage2] the pull went the short way` |
| history_hold_removed | step | `[step] the phase term let go at the reference's history restart` |
| mr_hold_removed | mr | `[mr] the phase term let go at the mr toggle` |
| holdover_hold_removed (state and history terms; either alone suffices, so one alone survives, measured) | holdover | `[holdover] the phase term let go at HOLDOVER` |
| idle_hold_removed (state term and the IDLE reset) | internal | `[internal] the phase term let go at INTERNAL` |
| window_cap_removed (D4) | burst | `[burst] the window the burst filled kept exactly 264 samples, the cap` |
| slew_hold_removed | slew | `[slew] the phase term let go at the slew level` |
| domain_event_not_backdated | engage | `[engage] every DUT CRF timestamp is a frame instant of its own grid` |
| crf_output_off_grid | engage | `[engage] every DUT CRF timestamp is a frame instant of its own grid` |
| pins_b_constant_dropped | pins | `[pins B] every stamped frame instant is each slot's MSB pin instant less its offset, inside +/-5 % of Ps` |
| pins_constants_swapped | pins | `[pins A] ...and inside the derivation` |
| pins_c_closed_at_frame_end (D2) | pins | `[pins C] every stamped frame instant is each slot's MSB pin instant less its offset, inside +/-5 % of Ps` |

The let-go checks are new in session 5 (`sim_main.cpp` `watch_letgo`/`check_letgo`): the engaged bit `phase_o[20]`
must read low on some datapath cycle within 10 ms (step), 5 ms (mr, INTERNAL, slew) or 200 ms (HOLDOVER) of the
event. The session-4 mutants `refold_removed` and `slew_refold_removed` targeted the unwrap, which no longer exists.

capture_coherence (`mutants.py`, default target), the five #632 mutants of 25:

| Mutant | Leg | Required failing check |
|---|---|---|
| the live PHC at the walk | dp | `[PIN] every slot's MSB pin instant, less its slot offset, is its AAF timestamp less the presentation offset, inside +/-5 % of Ps` |
| the time base latched at the tick (D1) | dp-band | same |
| the marker latency's frame term dropped | dp | same |
| the marker latency's write term dropped | dp | `[PIN] ...and inside the marker latency's derivation` |
| the walk's instant latched at the snapshot (D1) | chmap | `F: tick-cycle: col 1 walk instant is frame 2's` |

Positive controls: `[PIN] control: the same stamps graded without the per-slot constant are refused`; the
clean builds of every leg pass first.

## Loop design (gains, bandwidths, why)

- Units: 1 trim unit = 1 ns per 512 ms window of rate = 1/512 ppm; the plant moves the rate one unit per unit.
- PI per window: `integ += e/2 + 3/128 x Theta_ns` (Theta: last window's phase, its sample sum over the nominal 256,
  clamped), `u = integ + e/4`.
- Linear model (desk, `receipts/loop/poles.py`, output `poles.log`, the g = 3/128 row): poles 0.944 (phase; time constant 17
  windows = 8.9 s), 0.70 (rate; 2.8 windows = 1.4 s), -0.40, 0. Phase bandwidth about 0.018 Hz, rate about 0.11 Hz:
  six times apart, so the rate loop has settled before the phase moves, and the phase term never fights it.
- Slew limit: Theta clamped at +/-5,461 ns, which makes the integrator settle at e = -256 ns per window: the phase
  moves at most 256 ns a window = 0.5 ppm. Inside the 2 ppm lock test (no LOCKED drop, no CLOCK_DOMAIN count) and
  glitch-free through the MMCM fine phase shift (no slip; TDM frames continuous).
- Pull-in from Ps/2: ~41 windows at the clamp, then the pole: 23-28 s measured.
- Fold exact: Ps = 62,500/3 ns, worked in 1/3 ns (3d mod 62,500 by a restoring divider by the constant Ps, 29
  cycles; PDUs are 2 ms apart). Each sample folds to its own nearest period; Theta = window sum >> 8 (nominal 256).

## Latency constants (per interface, derivation)

Marker latency = closing pair's last bit (2(k+1) word_bits + d - 1 bit periods) + FIFO write + 4.5 datapath cycles
(`receipts/latency/` evaluates the package): 1x1 TDM8 master 20,964 ns; 8x8 TDM32 master 5,308 ns; Arty TDM8+I2S
blend 15,756 ns; Arty I2S 21,126 ns; TDM8 slave 21,004 ns; synthetic TDM4 d=0 20,802 ns. Slot k pin offset:
(k x word_bits + d) bit periods. Listener post-grid: crossbar (streams x 4 + 2 cycles) + bank walk 9 cycles + adopt
wait phi (0.229..21.059 us, per lock) + slot offset: NOT compensated (see the open decision).

## -0.46 Ps accounting (addendum item 4)

`receipts/acct/`: base KL_crf_tx beside the TDM8 master, one audio clock and reset, three reset phases: the old CRF
divider event sits +40.4..+59.9 ns (+0.002..+0.003 Ps) after the frame sync at the pins. So the constant is the old
AAF stamp's distance from its own frame: marker latency (+0.006 Ps folded) + capture age. -0.46 Ps folds to +0.54;
less 0.006, plus 0.0025: 0.536 Ps = 11.2 us = ~559 axis cycles, unique in the recorded 256..785 band.

## Open decision (published with REVIEW READY)

The listener's post-grid pin delay cannot be "counted against the presentation time offset": the render path
(`KL_render_setpoint`) presents by fill, 8 events after accept, not at the avtp_timestamp. A timestamp-driven render
is a listener-datapath change outside the media-clock chain (STOP condition 3). Constants derived and documented.

## Stale text left outside the scope (follow-up)

`configs/endstation_ax7101_8x8.yaml:159` comment, `sw/builder/endstation_builder.py:4009-4011` comment and `:4748`
build-plan text, `sw/builder/test_builder.py:21628` comment, all "KL_crf_tx /512". The builder and configs are
outside the media-clock chain; build plans are untracked.

## Resource before/after, route timing

| Measure | Base (record, `e26f1816` inputs) | `e96f3928` | Head (`a6ae20f9` = `e85df091` RTL) |
|---|---:|---:|---:|
| route-1x1 LUT | 49,613 | 50,329 (+716, fail) | 49,644 (+31) |
| route-1x1 FF | 52,353 | 53,072 (+719, fail) | 52,641 (+288) |
| route-1x1 SLICE | 15,725 | 15,802 (+77) | 15,785 (+60) |
| RAMB36 / RAMB18 / DSP | 74 / 25 / 14 | 74 / 25 / 14 | 74 / 25 / 14 |
| WNS / WHS | +0.215 / +0.036 ns | +0.048 / +0.033 ns | +0.276 / +0.032 ns |
| servo, routed hierarchy | 897 LUT / 814 FF | 1,478 / 1,195 | 1,161 / 994 |
| servo, Yosys OOC | 865 / 792 | 1,457 / 1,183 | 1,168 / 982 |

Details and per-block movements: R1, R2, R3 above.

## Gate table (head `f1fda3f1`; the RTL is identical since `a6ae20f9`, where the route ran)

| Gate | Command | Result | Receipt |
|---|---|---|---|
| route-1x1 resource gate | `syn/ooc/pp_resource_gate.py check <gateware> --endpoint route-1x1` after the recipe route | exit 0: LUT +31, FF +288, SLICE +60, DSP/BRAM +0, WNS +0.276, WHS +0.032, route complete | `receipts/route_a6ae20f9/` |
| media_phase mutants | `make -C tb/verilator/media_phase mutants MUTANT_JOBS=4` at `e85df091` (no media_phase or RTL file changed since) | rc 0: 10 clean cases, 17 of 17 mutants fail their named checks (27 checks, 0 failures) | `receipts/media_phase_e85df091/mutants.log` |
| full sweep, shards 0-3 | `scripts/run_all_suites.sh <out> --shard i/4` (pinned Verilator 5.050, CPython 3.12.3, tsn-gen `deca300`) | shard 0 at `f1fda3f1`: 15/15, 52,903 checks, 0 failures (`milan_dp` included); its `tsn_fuzz` campaigns re-run with tsn-gen at `f1fda3f1`: 164 + 677 pass, all campaigns passed. Shard 1 at `e85df091`: 16/16, 331,441 checks, 0 failures (`media_phase` included; the diff to `f1fda3f1` is three `milan_dp` fixture files, which no shard-1 suite compiles). Shard 2 at `f1fda3f1`: 16/17 under the runner, 262,022 checks, 0 failures, and `capture_coherence` killed by the 2,400 s wall clock on two CPUs (result unknown), re-run alone at `f1fda3f1` inside the same budget: PASS in 21 min (run 20,832 checks, dp 447, campaign 35 of 35 with all 25 mutants caught; the runner's `suite_tally.py --verdict` rc 0). Shard 3 at `f1fda3f1`: 16/16, 1,540,268 checks, 0 failures | `receipts/sweep_f1fda3f1/` (with `shard2_capture_coherence_uncontended/`), `receipts/sweep_e85df091/shard1/` |
| lint | `python3 scripts/lint_rtl.py --check` | rc 0: 89 <= ratchet 89 | `receipts/lint_f1fda3f1.log` |
| Yosys synthesis gate | `syn/yosys/run.sh` (serial, every top) at `e85df091` (RTL identical) | rc 0: 59 of 59 tops PASS; tap-purity PASS | `receipts/yosys_e85df091/` |
| docs gates (49, the docs workflow's) | `scripts/docs_gates.sh` in the output dir | all 49 rc 0 at `f1fda3f1` | `receipts/docs-gates/` |
| servo OOC (Yosys) | `syn/yosys/ooc.sh KL_mmcm_drp_servo` | 1,168 LUT / 982 FF / 3 DSP (Vivado maps none) | `receipts/ooc/` |

Earlier, superseded: route-1x1 at `e96f3928` exit 1 (R1); at `5537cc41` exit 0 (R2); the mutant campaign at
`a6ae20f9` had one survivor, `fold_not_centred`, fixed in `e85df091` (`receipts/media_phase_a6ae20f9/`).

## Sweep launch note (session 5)

The first launch at 16:36 named shards `1 2 3 4` (they are 0-indexed, 0..3) and pinned them to CPUs 0-5 (session
4's script; this session is booked on 112-127). It was cancelled with TERM after 5 minutes (`CANCELLED: TERM`),
`sweep.sh` now derives its CPUs from the session's affinity, and the sweep was re-run as shards 0..3.

## D5: milan_dp counters-8 failed in the sweep (session 5, fixed in the fixture)

Sweep shard 0 at `e85df091`: `milan_dp` FAIL, `[726 TX] restart/wrap emitted enough got=0x0 exp=0x1` (both
phases) in `stream_counters.py --shape 8`; reproduced (`TX_RUN,0,8,0,2,2`: the CRF talker emitted 2 PDUs; base
`e26f1816` emits 8, AAF 64 in both). Cause: a fixture artifact the lane exposes. The nxn fixture toggles
`clk_audio_i` and `clk_tdm_i` 1:1 with `axis_clk`; the base CRF talker divided `clk_audio_i` (/512 /96: a PDU every
49,152 cycles on both shapes), the lane's counts 96 domain events, one per TDM frame: 2 x 8 x 32 = 512 cycles on
TDM8 (49,152 per PDU, as before) but 2 x 32 x 32 = 2,048 on the 8x8's TDM32 (196,608 per PDU). In hardware
`clk_tdm_i` is 98.304 MHz on that shape, so both are 48 kHz. make stopped there, so the cases after `counters-8`
(counters-*-frames, base, notify, crflic, dynmap, nxn*, nolpf, prune, ax1x1, aclk, render-mutants) never ran:
Fix (`33a460db`, test only): `stream_counters.py` passes the bus's slot count (`-DTDM_SLOTS_TB`, the same value as
`AUDIO_IF_SLOTS_P`) and `stream_counters.hpp` runs the TX wrap leg `400000 x TDM_SLOTS_TB / 8` cycles, so every
talker still crosses the six-PDU wrap seed: shape 8 now emits 9 and 8 CRF PDUs (base 8 and 8), shape 1 is
unchanged (same cycle count). The checks are untouched (`>6` emitted, counter follows the wire exactly). Then the
cases after `counters-8` were run at `33a460db` with `make -k` (`receipts/milan_dp_d5/`): all pass except `nxn4c`,
the Arty shape (TDM8 master with the I2S pair blended), three checks: `[CTRS-OUT] real q3/q4 stimuli reach every
AAF and CRF index`, `[CTRS-OUT] every real FRAMES_TX source raises dirty` (0xf of 0x1f), `class A off: a CRF PDU
still reaches the MAC`. Same cause: the nxn fixture leaves `clk_tdm_i` at 0 outside the counters build (the
fixture's own note: only `ax1x1` clocks the TDM master), so on nxn4c no audio frame runs, the domain event falls back
to the 48 kHz media tick (the designed liveness fallback) and a CRF PDU comes every 96 x 2083.3 = 200,000 clocks at
100 MHz, while the waits were sized for the old 49,152 (`RealPduWait` 52,000, `CRF_BUDGET` 160,000). The I2S-only legs
(nxn, nxndv, nxn8) keep 49,152 (I2S frame = clk_audio/512). Fix (`f1fda3f1`, test only): `CRF_PDU_MAX_CLK` = 200,000,
`RealPduWait` = it + 5,000, `CRF_BUDGET` = 2 x it + 10,000; nxn4c then passes with 0 failures. No other suite
compiles `sim_nxn.cpp` or the counters files (checked), so shard 1's pass at `e85df091` stands for the head.

## tsn-gen note (session 5)

The final shard 0 (`f1fda3f1`) passed 15 of 15 but `tsn_fuzz` declared its two field campaigns SKIPPED: the
tsn-gen checkout the sweep pointed at (another lane's temporary directory) was deleted between 16:38 and 18:07.
tsn-gen was rebuilt in this lane's scratch at CI's `TSN_GEN_REV` `deca300` (`packet_gen`, Release, as the rtl
workflow builds it) and `tsn_fuzz` re-run alone at `f1fda3f1` with it. At `e85df091` the campaigns had run (shard 0
of the superseded sweep).

## capture_coherence wall clock (session 5)

Shard 2 at `f1fda3f1` ran on two CPUs (its campaign sizes itself by affinity, and two keeps it at two builds):
`capture_coherence` hit the runner's 2,400 s wall clock with 24 of 25 mutants caught and the last in flight
(`TIMEOUT ... result UNKNOWN, not a failure`). Per the runner's contract it was re-run uncontended, alone, with the
campaign pinned to two units (`python3 mutants.py --jobs 2`, the same two builds at once) on more CPUs.

## Decision for the merge: the resource re-baseline

`docs/design/AREA_BUDGET.md` asks a merge that moves the shipping image to re-record its endpoints on the merge
result (`record --write`) with the budget and #234 findings text. That is outside the media-clock chain (STOP
condition 3), so it is not in this lane; the head's route passes the gate against the existing record. The
standalone endpoints' source list includes this lane's files (the OOC script keeps the integrated read set), so
their digests would change too; their figures should not, since the processor RTL is unchanged.

## Receipts

`receipts/INDEX.md` (generated from the files present).
