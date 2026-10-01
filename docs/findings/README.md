# Findings retained in the bare-metal product tree

This directory contains current hardware findings that still inform the
shipping Milan v1.2 design. Superseded target-runtime campaigns and operational
logs are preserved in Git history, not in the checked-out product tree (#259).

## Current entries

| Document | Scope | State |
|---|---|---|
| [451_TDM8_FIRST_LIGHT.md](451_TDM8_FIRST_LIGHT.md) | TDM8 first light between the AX7101 J11 header and the SoC board of the #451 amendment, image source `9e9954e9`: slot and channel order in both directions over 70 s each, continuity and the frame-rate offset (#451) | Both directions decoded in all eight slots, in order; DIN frame coherence NOT MET, tracked by [#617](https://github.com/kebag-logic/milan-fpga/issues/617); continuity check, scope and calibrated items NOT RUN. On `ec0cc0c1` the DIN re-run counts 0 torn frames in [617_DIN_FRAME_COHERENCE_BENCH.md](617_DIN_FRAME_COHERENCE_BENCH.md), and [451_USB_AUDIO_CAPTURE.md](451_USB_AUDIO_CAPTURE.md) records the capture through the USB Audio device as FAIL |
| [451_TDM8_TIMING_SOC_BOARD.md](451_TDM8_TIMING_SOC_BOARD.md) | The #451 timing item (BCLK, FSYNC and DOUT at the AM62x end) measured on the SoC board's McASP0, on dev `ec0cc0c1`; the oscilloscope version is [#626](https://github.com/kebag-logic/milan-fpga/issues/626) | STOP at 475.6 s of one McASP0 capture, when the bench host lost the SoC board's USB function: the capture of at least 10 minutes is NOT MET. Up to then, data one BCLK after the frame-sync edge PASS (22,831,104 frames bit-exact in all eight slots, 0 torn), fs 47,997.947 Hz on the SoC board's clock (-42.8 ppm, +-0.12 ppm granularity, crystal tolerance excluded) and BCLK 12,287,474 Hz inferred as 256 x fs. FSYNC pulse width, edge timing, levels and absolute ppm stay with #626 |
| [451_USB_AUDIO_CAPTURE.md](451_USB_AUDIO_CAPTURE.md) | Capture of the DUT's rendered pattern on the bench host's USB Audio card through the SoC board's audio bridge, on dev `ec0cc0c1`: slot and channel order and continuity over two 75 s runs; the continuity check (#451) | FAIL: 0 of 3,600,000 frames pass the pattern rule in either run, with a rotating channel order and silent stretches; the direct McASP0 path is bit-exact on the same image. Continuity check, playback direction, scope and calibrated items NOT RUN |
| [617_DIN_FRAME_COHERENCE_BENCH.md](617_DIN_FRAME_COHERENCE_BENCH.md) | Bench re-run of the #451 first-light DIN capture on dev `ec0cc0c1`, with the frame-atomic capture handoff of PR #618, and a DOUT re-run (#617 acceptance 4) | 0 torn of 3,360,036 playback frames (first light 67.5%); slot and channel order identity in both directions; render path unchanged |
| [75_RECONNECT_RESTART_MEASUREMENT.md](75_RECONNECT_RESTART_MEASUREMENT.md) | Two CRF pairs on `9e9954e9`; disconnect, two-second hold, reconnect (#75) | 100 listener and 97 talker restarts measured; AAF unmeasured. On `13eda870` the talker non-restarts are re-measured in [608_75_WITHDRAWAL_AND_RESTART.md](608_75_WITHDRAWAL_AND_RESTART.md) and the initial bind in [606_FIRST_BIND_MEASUREMENT.md](606_FIRST_BIND_MEASUREMENT.md) |
| [606_FIRST_BIND_MEASUREMENT.md](606_FIRST_BIND_MEASUREMENT.md) | First talker bind and long-hold connect of the DUT-talker CRF pair on dev `13eda870` (#606 item 3) | 5 of 5 first binds and 4 of 4 long-hold connects within 1 s; the post-reset allocation path is not exercised |
| [608_75_WITHDRAWAL_AND_RESTART.md](608_75_WITHDRAWAL_AND_RESTART.md) | 100 listener withdrawals and reconnects of the DUT-talker CRF pair on dev `13eda870` (#608 item 3, #75) | 99 of 99 withdrawals that reached an IN registrar stopped; the one LV case is attributed to processor #108, pending a re-run after processor PR #133; 99 of 99 demonstrated restarts within 1 s |
| [COMMERCIAL_TIMING_395.md](COMMERCIAL_TIMING_395.md) | AX7101 commercial-grade timing at both fixed speed models for the `9e9954e9` shipping checkpoint (#395 items 1, 2 and 5) | Applied constraints meet the recorded margin; rejected constraints belong to #607; physical temperature and oscillator measurements remain open |
| [397_SERVICE_BUDGET.md](397_SERVICE_BUDGET.md) | Product-CPU firmware service intervals at 50 MHz after the #590, #592 and #599 repairs, with external markers (#397) | Simulation measurement under the one-hart decision; future duties, physical torture and bench proof remain open |
| [117_GPTP_SILICON_EVIDENCE.md](117_GPTP_SILICON_EVIDENCE.md) | One AX7101 against the reference peer on dev `ede8d48e`: asCapable, cadence, turnaround, GM loss and return over six switch power cycles, publication and `tu` against the wire, controller enumeration (#117) | Current; GM loss and return inside the 5 s bound (worst 1.60 s) |
| [ADP shape (historical)](../history/v1/findings/ADP_SHAPE_STATIC_0727.md) | Generated ADP/AEM shape must match the instantiated stream geometry | Fixed; guarded by `scripts/check_entity_shape.py` |
| [CBS_DATAPATH_BUG.md](CBS_DATAPATH_BUG.md) | Per-frame classifier sideband timing at the CBS boundary | Fixed; covered by the controller-rate bench |
| [Media-clock lock (historical)](../history/v1/findings/MEDIA_CLOCK_LOCK_0810.md) | Media-clock lock observations and the then-open CRF consumption boundary (closed by #74) | Current design input; physical revalidation belongs to #117 |
| [Protocol area (historical)](../history/v1/findings/PP_SHADOW_AREA_0812.md) | Protocol-processor integration area accounting | Current synthesis evidence |
| [Throughput campaign (historical)](../history/v1/findings/PERFORMANCE_GOAL.md) | Closed >500 Mbit/s campaign measured on the retired 2-hart platform | Closed 2026-07-11; archived record only — the shipping fabric datapath supersedes it |

New findings must describe the exact candidate, measurement boundary, raw
artifact identity, conclusion, and owning issue. Findings that cease to
describe the current bare-metal product leave the checkout and remain
recoverable from Git history.
