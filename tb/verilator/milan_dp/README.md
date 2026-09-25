<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# milan_dp — the `milan_datapath` integration suite

`make` builds **fourteen elaborations** of `hdl/milan/milan_datapath.sv` (the vendor-neutral
Section A.9 wrapper the LiteX SoC instantiates) and runs a self-checking harness
against each. `make` exits non-zero if any leg fails; **gate on the exit code**,
never on grepping the log — a compile error prints no `FAIL` line at all.

The `sim_nxn` legs regenerate their descriptor image in a unique directory
under `TMPDIR` (falling back to `/tmp`) and remove it after a successful load.
Set `TMPDIR` to a filesystem with enough quota when review lanes run in
parallel. A failed generator deliberately leaves that directory and names its
log in the failure so the artifact can be inspected.

The eleven ordinary simulations use `sim_pool.py` after all model builds.
They include the #508 GET_STREAM_INFO checks in `obj_notify`,
the #443 render CSR checks in `obj_aclk`, and `obj_crflic`.
Focused build and mutation targets retain their existing recipes.
`SIM_JOBS=2` is the default; `SIM_JOBS=1` reproduces sequential execution.
Only these two values are accepted, independently of make flags.
Build recipes, gPTP prerequisites and render mutation phases remain unchanged.
The mutation driver starts only after every ordinary simulation succeeds.

Five `sim_nxn` legs share one exclusive group, in legacy order:
`obj_notify`, `obj_nxn`, `obj_nxndv`, `obj_nxn8`, then `obj_nxn4c`.
Their builder also rewrites tracked per-config shape headers.
Independent simulations can overlap that group within the two-child limit.
Presence of `MILAN_COUNTER_FRAME_OUT` serializes the entire ordinary set.
This includes empty values and preserves the final writer's outcome.

Each child's complete stdout/stderr stays together under `obj_legs/`.
Captures, banners and commands replay in legacy order.
Failed, crashed or missing children fail the recipe.
SIGINT, SIGTERM and SIGHUP terminate and reap owned descendants.
Started children retain attributable partial logs; unstarted children are named.
The ordered transcript also stays in `obj_legs/replay.log`.
Blocked stdout never delays cancellation, descendant cleanup, or shutdown.
Cancellation writes only immediately available stdout bytes after cleanup.
Drain or inspect the disk transcript for any remaining output.
Normal runs replay every byte, including through pipes.
Linux subreaper support is required before any child starts.
Run one suite invocation per working directory.

```sh
make -C tb/verilator/milan_dp run SIM_JOBS=1 VERILATOR_JOBS=8
make -C tb/verilator/milan_dp run SIM_JOBS=2 VERILATOR_JOBS=8
python3 tb/verilator/milan_dp/test_sim_pool.py
python3 tb/verilator/milan_dp/test_sim_pool_backpressure.py
```

The runner tests use real processes with controlled shared writes.
They cover exclusion, independent overlap, order, failures and descendant cleanup.
They also check frame serialization, complete output and Makefile inventory.
Backpressure controls execute both direct and actual Makefile paths.
They cover blocked copies, final flushes, signals, and exit races.
Their consumer stays blocked until shutdown and reaping are observed.
Normal draining checks binary output against the complete ordered transcript.
Runner diagnostics contribute no checks to `suite_tally.py`.

| objdir | harness | shape | what it is for |
|---|---|---|---|
| `obj_dir` | `sim_main.cpp` | `endstation_arty_current`, N=1 | CSR, fabric protocol/media RX/TX, PHC, CLKV, CRF, RMON, and link guard |
| `obj_nxn` | `sim_nxn.cpp` | `endstation_arty_4x4`, N=4 | the 0x800 window → real engines, per-stream routing, TRAP-1 |
| `obj_nxndv` | `sim_nxn.cpp` | arty_4x4 with a GENERATED divergent header (input row 1 declares the 96 kHz base) | the per-row format facts: every tracked config is row-uniform, so only this leg can prove the verdict base and reset GET answer are the ADDRESSED row's and not row 0's -- same channel count on both rows, so the base is the one discriminator. `gen_divergent_shape.py` emits the header and the bench expectations at build time, like `ltn_rom.hex` |
| `obj_nxn8` | `sim_nxn.cpp` | `endstation_ax7101_8x8`, N=8 | the AX 8×8 target, retired input-pool posture, dynamic output maps, and loopback lane |
| `obj_nxn4c` | `sim_nxn.cpp` | `endstation_arty_4x4`, N=4, 4 wire channels | the shipping Arty shape (framer width ≠ shadow reset) |
| `obj_nolpf` | `sim_main.cpp` | `endstation_arty_current`, `LPF_P=0` | the spent area lever: no digital acceptance surface may move |
| `obj_prune` | `sim_prune.cpp` | all six tier-1 blocks pruned | the inert values are STRUCTURAL zeros, not not-armed-yet zeros; `SLIP_LB` (#390) is read behind listener 0 bound, fed well-formed AAF PDUs and then starved, so a built ring would count. The same section then establishes the lane the way the [register map](../../../docs/reference/REGISTER_MAP.md) instructs, and in that order: the whole `0x914` word is graded against the `0xDEADDEAD` not-a-measurement poison, and `CHMAP_SNAP[1]` valid with it, before any projection of it, because that poison projects to the same `{mask_valid, valid, fed}` = 1, 1, 0 this leg expects; behind those two grades the readback answers 1, 1, 0, so the zero is a measured absent lane, and a readback left un-armed fails this leg instead of passing it |
| `obj_ax1x1` | `sim_main.cpp` | `endstation_ax7101_1x1_tdm8`, direct option OFF | AX7101 geometry and media datapath coverage plus exact ownerless gPTP state; this verification elaboration is not a flashable product image |
| `obj_aclk` | `sim_aclk.cpp` | same ownerless option-OFF geometry, true 391/1591 `clk_audio` ratio | two phases (#74): the INTERNAL free-run drift (-10.64 ppm, the standing free-run rule), then CRF selected - the grids aligned (|ppm| < 0.5, zero junction slips), the servo in ACQUIRE through the live select, both 4.4.4.3 `mr` triggers and the 10.4.3 negative; the #390 ring phases ride the same instrument: the loopback ring is fed at the physical rate (6 x 512 x 1591/391 = 12500 + 52/391 axis cycles per PDU, the cadence a peer disciplined to the same CRF produces) and dups once per beat period at INTERNAL on the predicted beat, one event per fed pair. The closed form: the burst-vs-tick phase walks 52/391 cycle per PDU, so the first dup comes (P - phi) / (52/391) PDUs after a restart (P = 2083.33 cycles, phi = the offset of the burst's first beat after the preceding tick); the harness aims the restart burst's `tlast` 0.93 of a tick after a media tick (band 0.90 to 0.96), predicts the first dup from the first beat and grades it within 25 percent over a window of 1.5 times the prediction. The same aim and window under CRF show zero, a ONE-SIDED sensitivity: a pop grid faster than the push by more than 7 ppm dups inside the window, a slower one would need about 300 ppm to skip (the grids' own two-sided check is [CRF] abs(ppm) < 0.5). `SLIP_LB`/`SLIP_TDM` (`0x8D4`/`0x8D8`) read their taps after induced ring and TDM-junction slips, and `CHMAP_LOOP` reads `{mask_valid, valid, fed}` = 1, 1, 1 here, behind the same whole-word `0xDEADDEAD` and `CHMAP_SNAP[1]` valid grades - the fed half of the two-leg lane-establishment pair whose other half is `obj_prune` |
| `obj_notify` | `sim_nxn.cpp` (`NOTIFY_TIMED_TB`) | `endstation_ax7101_1x1_tdm8`, direct option OFF, `PP_TIM_DIV_US_P=1` + `PP_TIM_DIV_MS_P=100` | Milan 5.4.5 scheduler timing: the GET_COUNTERS one-second limit and 30–60 s departing-controller monitor; retained gPTP writes are graded inert and emit no notification. Then `[GSI]` (#508): every GET_STREAM_INFO field the processor owns, through real ACMP, MSRP and AECP transitions on both sinks; its mutation campaign is `make gsi-mutants` |
| `obj_crflic` | `sim_crf_licence.cpp` | `endstation_ax7101_1x1_tdm8`, direct option OFF, the processor and `KL_maap` millisecond on one 100-cycle grid, a 2000 ms Table 5.4 interval | #530: nothing is emitted before a Listener Ready, the CRF and AAF gates follow the processor's ACTIVE on every cycle, and a bound CRF talker keeps its Talker Advertise through the Run B per-type LeaveAll exchange; its mutation campaign is `make crflic-mutants` |
| `obj_gptp` | `sim_gptp.cpp` | product-default `endstation_ax7101_1x1_tdm8`, fabric gPTP at 2 MHz | selected-peer Pdelay/Announce/Sync publication through CSR and AECP; GM-switch AVB_INTERFACE/CLOCK_DOMAIN counters and dirty notifications; per-descriptor one-second suppression and pending release; AAF+CRF `tu` wire propagation; bounded PathTrace, coherent cutover, and inert legacy writes |
| `obj_gptplat` | `sim_gptp.cpp` | the `obj_gptp` elaboration with unequal ingress/egress latency corrections | #358: each reconstructed timestamp moves by its own correction |
| `obj_gmstep` | `sim_gmstep.cpp` | the `obj_gptp` elaboration, product-default `endstation_ax7101_1x1_tdm8` with fabric gPTP at 2 MHz | #387: a grandmaster change that steps the PHC by 1.5 s under CRF selection is one counted media event (`tu`, one render re-base, one `mr` toggle, one MEDIA_RESET) and stops no stream; `gmstep_mutants.py` plants the acceptance's three controls in the sweep and `make gmstep-mutants` the whole inventory |

The separate `milan_dp_gptp` suite reuses this Makefile's physical recipe:

| objdir | harness | shape | what it is for |
|---|---|---|---|
| `obj_ax1x1gptp` | `sim_ax1x1gptp.cpp` | AX7101 1x1 TDM8, gPTP ON, 50 MHz | Physical timer cadence, independent scheduled peer, eight-channel diagnostic loopback, loss/recovery/reset and stalls |

## Contents

- **[First AX7101 1x1 eight-channel run](#first-ax7101-1x1-eight-channel-run)** -- Run the focused datapath baseline and identify its coverage limits.
- **[AX7101 1x1 eight-channel gPTP physical-rate run](#ax7101-1x1-eight-channel-gptp-physical-rate-run)** -- Run combined clocks, peer exchange, and diagnostic audio checks.
- **[The #530 CRF talker licence leg (obj_crflic)](#the-530-crf-talker-licence-leg-obj_crflic)** -- The compressed-time leg that reproduces the Run B CRF bursts and early emission, what each phase proves, the failing arms, and why FRAMES_TX is an interval count
- **[The #508 GET_STREAM_INFO seam (the GSI section of obj_notify)](#the-508-get_stream_info-seam-the-gsi-section-of-obj_notify)** -- The four Stream Input fields the processor now owns, the transitions the timed leg drives through real wiring, its mutants, and the boot walk every binding harness starts
- **[GM step re-base leg (#387)](#gm-step-re-base-leg-387)** -- A grandmaster change that steps the PHC under CRF selection, graded against the #387 decision, and its negative controls
- **[2026-08-13 — the control plane was SUBSTITUTED, and this suite was rewritten around it](#2026-08-13--the-control-plane-was-substituted-and-this-suite-was-rewritten-around-it)** -- What the legacy-plane deletion did to this suite: which checks were repointed to the protocol processor's class-D face and the 0x920 window, and which were deleted because their subject no longer exists
- **[The device answers AECP now — and what this suite can and cannot see of it](#the-device-answers-aecp-now--and-what-this-suite-can-and-cannot-see-of-it)** -- What the AECP µCPU answers, why every leg here drives the descriptor-memory ports into the documented degrade path deliberately, and the dynamic-output-map capability that the substitution cost
- **[Check counts, before and after](#check-counts-before-and-after)** -- Per-leg check totals, with every row that was not re-measured after the last edit marked as such rather than projected
- **[Render phase records from the mutation controls](#render-phase-records-from-the-mutation-controls)** -- The record the render mutation arm prints around each build and run it already makes: the fields, the fixed case labels, and the limits that keep it an observation rather than a result
- **[Rules this suite is held to](#rules-this-suite-is-held-to)** -- The standing contract: gate on exit codes, never repoint a check to a structural zero without naming it as one, and never leave a check that passes vacuously

## First AX7101 1x1 eight-channel run

Run from the repository root:

```sh
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
make -C tb/verilator/milan_dp ax1x1 VERILATOR_JOBS=2
```

This selects the existing `obj_ax1x1` elaboration only.
The complete `make` sweep still includes the identical leg.

| Parameter | Selected baseline |
|---|---|
| Entity configuration | `endstation_ax7101_1x1_tdm8` |
| AAF streams | One talker and one listener |
| Wire channels | Eight |
| Audio interface | TDM8 master |
| Loopback lane | Enabled |
| I2S playback / render LPF | Disabled |
| Fabric gPTP | Disabled; ownerless verification boundary |
| Datapath frequency parameter | Default 100 MHz, not deployment's 50 MHz |
| Audio clocks | Toggled with the datapath, not the physical audio ratio |
| Harness | Unchanged `sim_main.cpp` assertions |

`VERILATOR_JOBS=2` limits compilation to two jobs.
It does not change simulation parameters or assertions.

Check the command's exit status and assertion summary.
Preserve every printed `SKIP`, `GAP`, and guarded-check count.
Excluded checks are not passes.

This is a first datapath baseline, not product qualification.
It excludes physical LiteEth/GMII behavior and CPU/DDR execution.
The [suite boundaries](../../../docs/testing/SIMULATION.md) explain those distinctions.

The separate `make gptp` target exercises fabric gPTP ownership.
It does not select this complete eight-channel/TDM8 parameter set.
The combined physical-rate leg below supplies separate evidence.

## AX7101 1x1 eight-channel gPTP physical-rate run

Run the focused leg with bounded compilation:

```sh
make -C tb/verilator/milan_dp ax1x1gptp VERILATOR_JOBS=4
```

The maintained DUT boundary is milan_datapath's AXI-Lite and MAC packet interfaces.
LiteEth/PHY, CPU/DDR, physical clock primitives and hardware compliance are not covered by this task.

The target elaborates one AAF stream in each direction.
Both streams carry eight channels.
TDM8 master and the backed loopback remain enabled.
I2S playback and render LPF remain pruned.
CSR shape words must both equal `0x48010002`.
Packet lengths and channel fields are checked separately.

| Model | Behavior |
|---|---|
| Milan and PHC | 50 MHz aliases; nominal PHC increment 20 ns |
| Audio and TDM | Plan A, 782/1591 of Milan; 24,575,738.529 Hz |
| Auxiliary phase clock | Explicit 200 MHz; four rising edges per Milan cycle |
| Phase quantization | Audio edges rounded upward onto 10 ns half-cycles; auxiliary edges every 2.5 ns |
| Reset | Both resets asserted together for 64 Milan cycles; release before the next falling edge; clocks continue |
| TDM master | FSYNC cadence and captured-pair counters measured; serial input silent |
| Peer clock | Independent 125 MHz timestamp edges; 10 us epoch offset; no drift |
| Peer link | 320 ns each direction; 20 us residence; independent event timestamps |
| Packet interface | Exact keep/last; RX beats every 80 ns; PTP ingress reservations; TX handshake collection |
| Response memory | Ordered 592-byte store for AECP gPTP getters |
| Descriptor memory | Builder-generated AEM image; 12-cycle initial read latency |
| Auxiliary feedback | MMCM locked; DRP/phase acknowledgments idle; INTERNAL media selection |
| Ethernet liveness | Synthetic receive/transmit clock toggles |

The ROM is separately generated as `gptp_ax1x1_ucode.hex`.
Generation uses `--clk-hz 50000000`, station MAC, and priority1.
The generator uses that frequency for its servo gains.
The engine timer independently receives the same frequency.
No gPTP or protocol-processor timers are compressed.
Boot Pdelay waits 1.2 seconds; requests repeat each second.
Sync/Follow_Up repeats every 125 milliseconds.
Announce repeats each second, initially phased at 250 milliseconds.
Sync loss waits beyond the real 375 ms timeout.
Peer loss includes the fourth unanswered request interval.
Recovery and reset reacquisition retain the original timers.

The peer timestamps scheduled arrival and departure events.
It never reads PHC to construct its timestamps.
Its delay oracle uses actual accepted packet event times.
The comparison allows 28 ns for timestamp quantization only.
This allowance contains no physical calibration correction.

Audio uses diagnostic provisioning through documented CSR windows.
`AAF_CTRL[1]` bypasses talker admission.
The listener stream override and capture-map window select loopback.
This run is **not licensed end-to-end streaming evidence**.
The closed admission gate is checked before enabling bypass.

Incoming PCM32 encodes channel identity and a monotonic sample index.
All eight returned channels must match that supplied ramp.
Sample order and packet sequence must remain continuous.
Acquisition, healthy streaming, stalls, loss, recovery, and reset are graded.
Stable phases also compare outgoing uncertainty with public state.
CSR and AECP getters must expose consistent GM/parent/delay/PathTrace.
Identity reads consume both halves of each CSR snapshot, including reset checks.
AECP status must report successful descriptor validation.
Short responses retain Ethernet minimum-frame padding.
Final cumulative assertions include traffic between named audio windows.
Warm-up payload and transition-state comparisons are explicitly excluded.
Every exclusion prints `NOT RUN` and contributes no pass.
Cumulative assertions require their own executed comparisons.
Per-window order, sequence, and uncertainty assertions require new comparisons.
Earlier traffic cannot supply evidence for a later silent window.
Without comparisons, each prints an explicit uncounted omission.
Payload, sample-order, and packet-sequence counters are independent.
Reset restarts ordering history, preserving cumulative comparison counts.
A missing AEM image aborts before the first cycle.
Only its setup failure counts; no audio assertion passes.
The separate suite also grades this setup failure automatically.
Two admission controls exercise initial silence and silence after traffic.
Each silent window retains activity/payload failures and uncounted comparison omissions.
Peer-delay and arrival comparisons require an accepted response in the current reset epoch.
Cadence checks require two requests; stall comparisons require observed stalled beats.
Their missing prerequisites produce explicit, uncounted omissions.

Physical omissions include MAC buffers, preamble, FCS, and PHY timing.
Issue #360 remains outside this packet-interface simulation.
Other omissions: CPU/DDR execution, NVM, and ACMP/SRP admission.
Analog audio, pad delays, PLL lock transients, and metastability are absent.
Oscillator drift, jitter, and MMCM actuation are absent.
Physical rendering, CRF recovery, and multiple-responder cease are untested.
No hardware compliance claim follows from this run.

The negative control corrupts peer residence and one audio channel:

```sh
cd tb/verilator/milan_dp
sha256sum obj_ax1x1gptp/Vmilan_dp_ax1x1gptp gptp_ax1x1_ucode.hex obj_ax1x1gptp/aemi.bin
/usr/bin/time -f 'wall_clock_seconds=%e process_exit_status=%x' \
  ./obj_ax1x1gptp/Vmilan_dp_ax1x1gptp --negative-control
```

Expected: nonzero exit, peer-delay failure, and audio-payload failure.
The switch defaults off and changes no RTL or ROM.
It stops after the first real Pdelay exchange.
Later acquisition, loss/reset/stall arms are explicitly unexecuted.
Negative-control results never enter the broad sweep's passing count.
The 2026-09-07 control measured 27 checks and 3 expected failures, exit 1.
It took 192.37 wall seconds; all five later phases stayed uncounted.
The peer-delay assertion and both payload assertions detected corruption.

The focused compilation limit is at most four jobs.
Smaller positive `VERILATOR_JOBS` values remain available.

The original fixed-window scenario spans 18.443565400 simulated seconds over 922178270 cycles.
The opt-in extended target retains those windows.
The default now ends transition windows upon observed public state.
Polling uses AXI-Lite every simulated millisecond.
Each reached transition gets another millisecond for packet/publication settling.
Audio monitoring continues throughout polling and between named windows.
No physical clock, protocol timer, or comparison threshold changes.

| Phase | Required span and stopping condition |
|---|---|
| Geometry and initial audio | Clock measurement takes about 3.4 ms. Payload warm-up excludes 10 ms. The 20 ms audio window covers 160 PDUs and 960 samples. |
| First Pdelay | Boot request occurs at 1.2 s. Inspection follows its response and Follow_Up, before the second request. |
| Acquisition and public getters | Second exchange occurs at 2.2 s. Announce and Sync/Follow_Up select the GM at 2.25 s. The unchanged discontinuity holdover clears `tu` near 2.75 s. Stop on healthy CLKV, then compare GM/parent/delay/path through CSR and AECP. Original 1.8 s window remains the failure bound. |
| Healthy audio | Twenty milliseconds compares all eight channels, ordering, and certain `tu`. |
| Backpressure | Wait for the next DUT Pdelay at 3.2 s. Every transmitted frame stalls for 64 cycles. Stop after a stalled PTP frame, then settle its response. The earlier acquisition requires approximately 0.43 s before that same request. The polling bound permits one unchanged Pdelay interval; the cadence tolerance remains unchanged. |
| Sync loss | Last selected Sync expires after 375 ms. Loss starts after the last Sync, leaving about 300 ms. Stop on public uncertain state; the original 450 ms failure bound remains. |
| Peer loss | Four unanswered request intervals must finish. After the successful 3.2 s request, these finish around 8.2 s. Stop only after public loss and the fifth unanswered request. The combined loss deadline remains 5.05 s. Audio and uncertain `tu` remain graded. |
| Recovery | Two fresh exchanges and selected Announce/Sync are required. Then Announce/Sync and the discontinuity holdover must complete. Stop on healthy public state within the original 3 s bound, then grade 20 ms of certain audio. |
| Reset | Assert both resets during active traffic. Warm-reset public health can return after one exchange. Continue through two completed exchanges, at 1.2/2.2 s, to grade the reset epoch's one-second cadence. Require healthy public state within 3 s, then grade 20 ms of certain audio. |

The four missed intervals prevent a 600-second default run.
Acquisition, recovery, and reset also require real Pdelay exchanges.
The trimmed scenario requires 16.992496440 simulated seconds over 849624822 cycles.
The closing transmit-flag phase adds four simulated seconds.
Consequently, the physical leg runs separately from the default sweep:

```sh
VERILATOR_JOBS=4 scripts/run_all_suites.sh /tmp/physical-logs --physical-gptp
make -C tb/verilator/milan_dp_gptp VERILATOR_JOBS=4
```

The wrapper calls the focused recipe and accounting regressions.
The physical harness contributes 137 checks.
Ten of them grade the transmitted flag words against Table 11-4.
Setup-abort contributes six; two no-TX controls contribute twenty.
The missing-response control contributes fourteen additional accounting checks.
It preserves real unanswered requests and their failed response/publication assertions.
The unchanged acquisition deadline expires before the acquired-publication check.
First-exchange, arrival and delay comparisons remain uncounted without an accepted response.
Its separate deadline is 5400 seconds, including compilation.
The four-core `ubuntu-latest` job permits 120 minutes, including toolchain setup.
Every other default suite retains its 1800-second deadline; `milan_dp` has 3600 seconds ([#387 decision](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5820240308)).
The [workflow policy](../../../docs/testing/CI_WORKFLOWS.md) assigns nightly and manual execution.
Physical regressions are therefore caught nightly, outside the PR aggregate.
Expiry still reports TIMEOUT/UNKNOWN and exits nonzero.

The former 2400-second hosted budget expired on 2026-09-07.
Its twelve shard companions passed; the physical result remained unknown.
The reference machine needed approximately 2080 simulation seconds.
It uses an AMD EPYC 9554P with 128 logical CPUs.
That established a hosted/local ratio above approximately 1.15.
The killed run supplied no finite upper bound.
The scheduling decision used that conservative, unbounded end.
It did not treat the lower bound as a prediction.

Round-three measurements used Verilator 5.050 on 2026-09-07.
Each experiment was confined to four distinct logical CPUs.
Each allocation also ran one CPU-bound SHA-256 background worker.
Experiments used separate build directories and disjoint CPU allocations.
Every build used four compilation jobs.
All three tabulated models ran completely.

| Build configuration | Fresh build and run | Simulation only | Checks / failures |
|---|---:|---:|---:|
| Baseline, single thread, `-O2` | 2079.57 s | 2058.94 s | 127 / 0 |
| Verilator `-O3`, model/runtime C++ `-O3`, `--threads 1` | 2024.43 s | 2002.53 s | 127 / 0 |
| Same optimization, `--threads 3 --threads-max-mtasks 3` | 2050.32 s | 2027.80 s | 127 / 0 |

The three-thread build's coarse partition schedules all work serially.
The user harness retains Verilator's `OPT_FAST` default, `-Os`.
These measured flags do not set every translation unit to `-O3`.
It proves equivalent output, without demonstrating parallel acceleration.
Unrestricted parallel and intermediate partition trials were stopped as impractical.
Those incomplete trials provide no passing coverage or equivalence verdict.
The shipped recipe therefore selects the faster single-threaded optimization.
It improves complete local runtime by 2.65 percent.

All three completed simulation transcripts are byte-identical.
Their SHA-256 is `15e5f27266e8c56a28122492282012dbc4d6361a2b360780742321485886bdad`.
They retained 649624822 cycles and 12.992496440 simulated seconds.
Their payload/order/sequence comparison counts were 4981392/622672/103937.
Every publication value, phase, and assertion result was identical across them.

The killed hosted workload divided by the measured baseline exceeds 1.15408.
The optimistic optimized projection therefore exceeds 2336.36 seconds.
The interval has no finite upper bound.
A 30-percent margin would require at most 1680 seconds.
Even its optimistic end misses that target substantially.
The conservative, unbounded end therefore requires decision branch 2.
The new nightly deadline remains an operational limit awaiting hosted evidence.

The 2026-09-11 remeasurement covers the current scenario.
It used Verilator 5.052, four compilation jobs, and four confined logical CPUs under background load.
The fresh build, physical run, and accounting controls took 3303.16 wall seconds.
The physical simulation alone took 2774.55 seconds for 16.992496440 simulated seconds.
The whole suite therefore used 61 percent of its 5400-second deadline locally.
Three hosted nightly runs of the previous scenario completed on 2026-09-08, 2026-09-10 and 2026-09-11.
Their whole suites took 2730.79, 4021.27 and 4091.59 seconds.
The two slower runs' physical simulations took 3208.32 and 3261.56 seconds.
Hosted simulation therefore took up to 1.58 times the 2058.94-second local baseline.
The projection scales the slowest hosted run.
Scaling its simulation by the cycle ratio 849624822/649624822 projects 4265.7 seconds.
The 830-second hosted remainder covers the build, image generation, and three accounting controls.
That remainder does not scale with the span.
The projected hosted suite time is therefore about 5096 seconds, 94 percent of the deadline.
Scaling by the measured local slowdown of 1.3476 instead projects about 5225 seconds, 97 percent.
The 5400-second deadline therefore still holds on projection, with a margin between 3 and 6 percent.
The 120-minute job keeps more than 30 minutes of margin on the same projection.
That margin is smaller than the 50 percent spread between the fastest and slowest hosted runs.
A completed hosted run of the current scenario remains required to confirm the deadline.

The original spans remain explicitly available:

```sh
make -C tb/verilator/milan_dp ax1x1gptp-extended VERILATOR_JOBS=4
# Equivalent entry from the separate suite:
make -C tb/verilator/milan_dp_gptp extended
```

Extended mode retains every original fixed-duration audio window.
The 2026-09-11 extended run passed 137 checks in 3052.05 simulation seconds.
Both modes execute the same assertions and comparison thresholds.
The new elapsed-interval assertion also checks four unanswered Pdelay intervals.
Extended mode is excluded from the default sweep.

The normal log includes simulated duration and counted verdicts.
The recipe records wall duration, process status, and SHA-256 hashes.
Each phase has a bounded simulated deadline.
Transport timeout aborts print the remaining unexecuted scope.

The explicit physical driver runs this leg once through `milan_dp_gptp`.
The `milan_dp` default retains its twelve existing legs.
`suite_tally.py` reads its separate physical-rate summary.
It also counts 40 setup, audio and missing-response accounting checks.
`suite_shards.py` selects `milan_dp_gptp` only through `--physical-gptp`.
The nightly/manual job runs that selection without sharding.
The historical `milan_dp` directory runs alone on hosted shard 4/5 (#444).
The existing `gptp` compressed smoke remains separately counted.
The option-OFF and fractional-audio legs retain their original models.

## The #530 CRF talker licence leg (`obj_crflic`)

Issue #530 records what the #117 silicon Run B measured on the AX7101 1x1
TDM8 image's CRF Media Clock Output. Two items were defects and the third
was a counter question:

1. **A bound CRF talker ended its own bursts.** The bench AVB switch applies
   a received LeaveAll per attribute type (802.1Q-2014 10.7.5.20 NOTE). The
   DUT's LeaveAll MRPDU flagged only its Domain message, so the switch never
   re-declared its Listener after it. The processor also re-aged the Listener
   registration at every flagged VectorHeader of the switch's own LeaveAll
   MRPDU. Once the 15 s PROBE_TX window had closed (Milan v1.2 4.3.3.1) the DA
   gate closed and the DUT withdrew its Talker Advertise. The protocol
   processor fixed both halves at pin `09f9bf38` (its issue 106).
2. **Emission began before a reservation existed.** Every talker gate read
   the processor's raw admission verdict, which the declaration alone raises,
   instead of its ACTIVE: Talker Advertise declared, a Listener Ready or Ready
   Failed registered, admitted (Milan v1.2 5.3.7.3). `milan_datapath` now
   drives `lwsrp_stream_gate` from `pp_cd_srp_active_w`.
3. **FRAMES_TX read 16 against 34,061 PDUs.** That is the documented
   semantics, not a defect; see [FRAMES_TX is an interval count](#frames_tx-is-an-interval-count).

`sim_crf_licence.cpp` elaborates `endstation_ax7101_1x1_tdm8`, where the CRF
output is source uid 1. The processor's millisecond and `KL_maap`'s
millisecond sit on one 100-cycle grid (the `pp_shadow` recipe), and the Table
5.4 observation interval is 2000 of those milliseconds. The CRF grid is not
compressed: it runs off `clk_audio`, one PDU every 49,152 cycles (491.52
compressed ms). The leg writes the firmware boot values the #117 image
wrote (`AAF_CTRL` `0x00020001`, `LWSRP_CTRL` `0x13`, `MAAP_CTRL` `0x201`,
`CRFT_CTRL` `0x3`) and plays the two Run B peers:

- **The listener** probes a source, retries 4 s after a
  TALKER_DEST_MAC_FAIL answer and re-probes 0.5 s after a Talker Advertise
  Leave.
- **The switch port** declares Listener Ready 40 ms after the listener's
  successful probe. It re-declares, 2 ms after a DUT LeaveAll, only the
  attribute types that LeaveAll flags. It sends its own LeaveAll 9.99 s after
  each DUT LeaveAll, in the capture's layout: Listener JoinMt first, then the
  Domain, then LeaveAll-only Talker Advertise and Talker Failed vectors. It
  withdraws its Listener 2 ms after a Talker Advertise Leave.

The licence, both sources' ACTIVE, raw verdict, DA gate and Talker
Advertise state are sampled on every cycle.

| phase | what it proves |
|---|---|
| `[A]` | Run B's opening: both first probes are refused, MAAP grants, the DUT declares Talker Advertise and is admitted, and no Listener Ready exists. No CRF or AAF PDU leaves, `CRFT_COUNT` stays 0 and `CRFT_CTRL[6]`/`[7]` read 0 (item 2). |
| `[B]` | The first Listener Ready opens each gate on the cycle ACTIVE rises. Every CRF PDU is C-tagged {PCP 3, VID 2} with the stream {MAC, uid 1} and the MAAP DA. |
| `[B2]` | The AAF closing edge: a withdrawn Listener closes the AAF gate on the cycle ACTIVE falls, while the talker still declares and is admitted. |
| `[C]` | Item 1: 76 s bound across five DUT and five switch LeaveAll MRPDUs, the last 45 s or more held by the registration alone. No self-Leave, no licence drop, and no gap over 1.5 CRF periods. Every DUT LeaveAll flags all four MSRP attribute types. |
| `[D]` | A registered Asking Failed closes the licence; Ready Failed reopens it. |
| `[E]` | The unbind: the licence closes when the Listener registration ends, inside a fresh probe window, not when the window closes (Run B's last burst ran 9.95 s past its unbind). |
| `[F]` | Item 3: FRAMES_TX counts observation intervals since STREAM_START, far fewer than the PDUs, and restarts at the next STREAM_START. |
| `[INV]` | Every cycle: the CRF licence equals ACTIVE[CRF], and the AAF gate is never open without ACTIVE[AAF]. |

**Failing arms.** Each was run on this head (2026-09-24 UTC):

| arm | how | result |
|---|---|---|
| the licence mutants | `make crflic-mutants`: `crflic_mutants.py` plants each consumer back on the raw verdict (the whole gate, the CRF slot alone, AAF source 0 alone) | all three caught, each on its named check; the clean leg passes |
| the gate reverted | the first mutant, run as the reproduction before the fix | 23 of 85 fail, the Run B item 2 signature: the licence opens at 1770.38 ms, 1.34 ms after the first probe and before its TALKER_DEST_MAC_FAIL answer at 1772.00 ms; the first CRF PDU leaves at 1966.30 ms, 3.85 s before the first Listener Ready; and the licence never closes again, through Asking Failed and the unbind |
| the previous processor pin `424c688f` | by hand, the only arm that needs a second processor checkout: `git -C protocol-processor checkout 424c688f`, `make crflic CRFLIC_MDIR=obj_crflic_oldpin`, then restore the pin | 17 of 85 fail, the Run B item 1 signature: every DUT LeaveAll flags only the Domain. ACTIVE and the licence fall six times by the end of `[C]`, each 5.0 s after a LeaveAll that aged the Listener registration with no re-declaration. The DUT withdraws its Talker Advertise four times: once at a registration loss 5.0 s after a switch LeaveAll, three times 15.1 s after the listener's latest probe, as Run B's bursts ended |

The mutants are an explicit campaign, not a sweep step: three elaborations
and four runs, 139 s on an eight-core host, which the stated `milan_dp`
deadline margin was not sized for. The leg itself builds in about 14 s
there and runs in about 20 s.

**What it cannot show.** The switch's timing is modelled from the Run B
capture: its LeaveAll 9.99 s after each DUT LeaveAll. A switch with a fixed
LeaveAll period is not modelled. This station's leavealltimer does not
restart on a received LeaveAll (processor issue 108), and nothing here
measures that. The silicon rerun of #530 is the acceptance.

### FRAMES_TX is an interval count

Milan v1.2 5.3.7.7 Table 5.4 defines the Stream Output FRAMES_TX as
"Incremented at the end of every observation interval during which at least
one Stream Data AVTPDU has been transmitted on this Stream Output", with an
interval of at most 1 second, "Reset to 0 each time the Talker starts
streaming". `KL_talker_diag_ctx` implements exactly that with a 1 s interval
(`DIAG_TICK_CYC_P` = `MILAN_CLK_FREQ_HZ`), and `tb/verilator/tkdiag` grades
the counter itself. Run B's last burst lasted 15.00 s. It started inside
one interval and ended inside the sixteenth, and each of those sixteen
intervals carried PDUs at 500 per second, so FRAMES_TX read 16. The
#117 findings' item 9 saw it rise by one per 1 s poll and return to 0 at
each of the four STREAM_STARTs. The PDU total is `CRFT_COUNT` (`0x764`):
34,061. Table 5.6 in 5.3.8.10 is the Stream Input set, where FRAMES_RX
lives; it does not define FRAMES_TX. After #530 a continuously bound output
should read STREAM_START 1 and FRAMES_TX equal to the seconds it has streamed.

## The #508 GET_STREAM_INFO seam (the GSI section of `obj_notify`)

Since processor pin `a8f8ce81` the processor owns four Stream Input fields.
Its top answers them from its own state:

| Field | Milan clause | State owner | Selector | Response bytes |
|---|---|---|---|---|
| `probing_status`, `acmp_status` | 5.3.8.6 | listener record, committed | 7, internal | `@76` (frame 90) |
| `msrp_failure_code` | 5.3.8.8 | SRP registrar | 4, byte `[15:8]` replaced | `@58` (frame 72) |
| `msrp_failure_bridge_id` | 5.3.8.8 | SRP registrar, gated on FAILED | 5, internal | `@60..@67` (frame 74..81) |

The processor never asks `milan_datapath` for selectors 5 and 7 of a Stream Input.
So the datapath answers neither, and leaves the selector 4 byte zero.
Its old bound/settled approximation and its zero bridge id are deleted.
The validity flags stay the datapath's: `MSRP_FAILURE_VALID`, `REGISTERING_FAILED`, `BOUND`.

`[GSI]` runs at the end of the timed leg, on the AX 1x1 shape.
Its two sinks are the AAF input (0) and the CRF input (1).
The section owns both MAC ports, so no frame is lost between waits.
Controllers A and B register for notifications first.

The adopted pin `990f9652` also includes processor issue 113 (PR 115).
It adds a notification for a latency-only Talker refresh.
No existing notify or `[GSI]` check drives that isolated transition.
`gsi_talker_failed()` always sends accumulated latency 500000 ns.
G5 changes latency alongside initial registration and FailureInformation.
Those events coalesce into the single notification G5 already checks.
G6 repeats that latency unchanged; G7 changes FailureInformation alone.
The earlier notify phases inject no registering Talker attribute.
Their notification expectations therefore need no adaptation.
The processor's response tests own isolated latency-change coverage.

| Phase | What happens on the wire | Graded |
|---|---|---|
| G0 | nothing bound | both sinks DISABLED; STREAM_INPUT 2 answers NO_SUCH_DESCRIPTOR with the zero cdl-68 body |
| G1 | BIND_RX sink 0; the talker never answers | ACTIVE with `acmp_status` 0 at once; the duplicate probe pushes nothing |
| G2 | the second probe times out; sink 1's probe is refused | sink 0 ACTIVE/7 (LISTENER_TALKER_TIMEOUT), sink 1 ACTIVE/3 (TALKER_DEST_MAC_FAIL) |
| G3 | each retry expires; no talker was discovered | both PASSIVE, `acmp_status` 0, no new probe |
| G4 | UNBIND_RX sink 0, then fresh binds with answered probes | DISABLED, ACTIVE, then COMPLETED with the talker's stream_id |
| G5 | the bridge declares Talker Failed on each stream | code and 64-bit bridge id per sink, distinct values, flags set |
| G6 | the same Talker Failed, refreshed | no push |
| G7 | sink 1's FailureInformation changes | one push for sink 1, new values; sink 0 untouched |
| G8 | sink 0's Talker Failed is withdrawn | exactly two pushes per controller: registrar withdrawal, then settlement teardown; both PASSIVE with cleared failure fields; sink 1 quiet |
| G9 | STOP_STREAMING(sink 1) from A | B gets STOP_STREAMING, A gets nothing, nobody gets GET_STREAM_INFO |
| G10 | a reset | both sinks DISABLED with nothing carried |

Each named change pushes one GET_STREAM_INFO to each controller.
G8 has two changes, producing exactly two pushes per controller.
The first follows `srp_evt_tk_unreg_w`: the registrar withdraws its attribute.
The second follows `lstn_gsi_changed_r`: settlement tears down to PASSIVE.
Both trigger `protocol_processor_top.stri_events` at the adopted pin.
Both responses carry PASSIVE, zero ACMP status, and cleared failures.
The first already sees teardown because response gathers read live.
See [F06.13, field lineage](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/990f96526bb89356c963a260ebbdcf2a77e6623a/docs/architecture/06_aecp_engine.md#fig-06-lineage) and [F05.5, settlement detail](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/990f96526bb89356c963a260ebbdcf2a77e6623a/docs/architecture/05_acmp_engine.md#fig-05-settled).
G8 grades both ordered responses to each controller against that state.
Both bodies equal the subsequent solicited answer; sink 1 stays quiet.
Acceptance 2 names PASSIVE after a bind.
The processor reads Milan 5.5.3.5.3 and 5.5.3.5.29 as ACTIVE first.
A bind probes at once, and PASSIVE follows an unanswered probe's retry.
G1 and G3 grade that order (processor issue 43, PR 111).

**Failing arms.** `make gsi-mutants` runs `gsi_mutants.py`.
It plants each defect in a copy of the processor tree or the datapath.
The submodule checkout is never edited.
Measured on 2026-09-25 UTC: the clean leg passes 380/380 checks.

| Mutant | Named check that fails | Failures |
|---|---|---|
| the processor ties the bridge id to zero | G5 sink 0 `msrp_failure_bridge_id` | 7 of 380 |
| selector 5 goes back to the datapath, which answers zero | G5 sink 0 `msrp_failure_bridge_id` | 7 of 380 |
| the processor ties the failure code to zero | G5 sink 0 `msrp_failure_code` | 7 of 380 |
| the failure-code byte is left to the datapath | G5 sink 1 `msrp_failure_code` | 7 of 380 |
| the processor ties probing/ACMP status to zero | G2 sink 0 `acmp_status` | 21 of 380 |
| the processor reads the other sink's owners | G5 sink 0 beside the other sink, bridge id | 42 of 380 |
| the datapath's bound/settled approximation returns | G1 sink 0 `probing_status` | 14 of 380 |
| the processor duplicates withdrawal after 4096 cycles | G8 sink 0 unsolicited GET_STREAM_INFO count to A | 2 of 396 |

The duplicate also fails the exact count to B.
It replays `srp_evt_tk_unreg_w` after the legitimate pushes drain.
A simultaneous duplicate would coalesce, providing no extra push.
The mutant's two extra responses receive the same content checks.
That adds sixteen checks to its run.
The campaign runs explicitly: eight mutant elaborations and nine runs.

**Every harness that binds a sink starts the restore walk.**
Since the same pin, the processor holds its ACMP listener from reset.
It releases it when the NVM binding walk ends.
`PP_CTRL[1]` starts that walk, as the firmware's `nvm_boot()` does.
`sim_main`, `sim_nxn`, `sim_aclk` and `milan_dp_render` now set it at boot.
Without it the 1x1 leg fails 24 checks: no sink ever probes.

## GM step re-base leg (#387)

The true-ratio leg also commands an absolute software settime.
`RENDER-SETTIME` requires one pulse and one counted render re-base.
A further 100 PDUs must produce no second event.

`make gmstep` builds `obj_gmstep` from `sim_gmstep.cpp` on the `gptp` leg's
elaboration: the AX7101 1x1 TDM8 entity, fabric gPTP on, a 2 MHz fabric clock
and an 8 ns PHC. It drives issue #387's acceptance 3: a grandmaster change
that steps the PHC by 1.5 s while the AAF listener is bound and locked under
CRF selection.

| Phase | What it grades |
|---|---|
| Acquisition | Pdelay to asCapable, then GM A's Sync; the link-up pair steps once, above 20 us |
| Media | SET_CLOCK_SOURCE to the CRF answers SUCCESS and the root resolves it; the CRF sink locks; the talker gate opens |
| Baseline | every PDU push leaves the #386 target fill (setpoint 8 + one PDU = 14 events); the talker streams with `tu` clear |
| GM change | one plane step of 1.5 s, after the commit; `tu` set in the first cycle the bank names GM B, held at least a quarter tick after the step, then clear, with talker PDUs graded both inside the hold and after it; every talker PDU carries the verdict of its instant; the talker keeps its gate, sequence and rate, and no pause beyond four of its intervals up to the end of the window; the listener stays locked and its FRAMES_RX moves by the PDUs it accepted; one counted render re-base, no rail, every push on the target fill; one outgoing `mr` toggle; the talker's MEDIA_RESET counts one |

**The counted event is the step's, not the commit's.** The render re-base
must be counted at a PDU end within two AAF periods (500 cycles) after the
plane's step pulse, and the first PDU carrying the new `mr` level must leave
within two talker intervals of it. The talker's counters are read once more
between the commit and the step, and MEDIA_RESET must not have moved there.
A re-base keyed to the grandmaster identity change therefore fails; in this
scenario the identity change lands about 160000 cycles before the step.

**The render law is graded where the stage states it.** `KL_render_setpoint`
judges its bands on the fill right after each PDU's push, TARGET_C =
setpoint + one PDU. The leg reads that fill as the peak of the registered fill
between two accepts: pops only lower it after the push, and the next PDU
pushes only after its own accept. The fill at the accept is printed, not
graded: it depends on how many media ticks fall between the last push and the
accept, so it moves with the feed's start phase (9 or 10 events here).

**Start phase.** The binary's optional second argument, `GMSTEP_FEED_DELAY`
through `make`, idles that many fabric cycles before the peer's media feed
starts. One media tick is 41.67 cycles at 2 MHz, so delays 0 to 41 cover every
accept phase. With the #387 datapath edit the leg passes at all 42.

**It runs in the default sweep, with its negative controls.** Before the
#387 datapath edit the leg passed 44 of its 48 checks: the render stage
counted two re-bases, one on the grandmaster identity (outside the step's
window) and one on the step, and the step neither toggled `mr` nor counted
MEDIA_RESET. With the edit it passes 48 of 48. `run` then runs
`gmstep_mutants.py`, which rebuilds the leg against a mutated copy through the
`gmstep-build` recipe (`GMSTEP_MDIR` and `DP_SRC`, `CLKV_SRC` or `RSP_SRC`
overridden), and each control must fail its named check by the leg's own
verdict:

| Control | Planted in | Named check it fails | Runs in |
|---|---|---|---|
| the step does not toggle `mr` | datapath | restart: the outgoing mr toggles exactly once | the sweep |
| the grandmaster identity re-bases the render stage as well as the step | datapath | render: the GM change is one counted re-base event | the sweep |
| the step does not re-centre the render stage (ruling 5802264260 item 1) | datapath | render: the GM change is one counted re-base event | the sweep |
| the render re-base is keyed to the identity, not the step | datapath | render: every counted re-base lands at a PDU end right after the step | `gmstep-mutants` |
| `tu` reaches the talkers four cycles late | clock validity | tu: set in the first cycle the bank names GM B | `gmstep-mutants` |
| the plane's step does not re-arm the holdover | datapath | tu: held at least the 0.25 s holdover after the step | `gmstep-mutants` |
| `tu` stops the talker | datapath | licence: the talker never pauses beyond four of its intervals | `gmstep-mutants` |
| the grandmaster change stops the talker for good | datapath | licence: the talker never pauses beyond four of its intervals | `gmstep-mutants` |
| the step's re-centre snaps one event off the setpoint | render stage | render: every PDU push leaves the target fill across the event | `gmstep-mutants` |
| a software settime does not toggle `mr` | datapath | CLKV: the settime toggled mr once more (#387) | `gmstep-mutants`, option-off leg |
| the step's `mr` toggle is gated by the CRF clock-source selection | datapath | CLKV: its mr toggled once per PHC step issued so far (#387) | `gmstep-mutants`, option-off leg |

Each control costs one elaboration of the datapath, so the sweep carries the
three the acceptance names and the explicit `make gmstep-mutants` target runs
all eleven (the explicit-campaign rule of
[TESTING.md](../../../docs/testing/TESTING.md#1-verilator-rtl-harnesses---tbverilator-the-live-regression)).
The last two grade the option-off leg (`sim_main.cpp`, rebuilt through
`option-off-build` with `OPTOFF_MDIR` and `DP_SRC` overridden) on an INTERNAL
media clock, where the harness issues a CLKV adjtime and then a software
settime: each is one `mr` toggle, and the settime one MEDIA_RESET. The runner
prints every check each control broke, not only the named one. A clean binary
older than its recipe's inputs is rebuilt, not graded.

What the leg does not grade:

- The grid aligner. The TDM clocks are held, so it stays disengaged. By [owner decision on #387](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5810378282) it gets no re-centre of its own: #539 keeps the step out of its reference at the CRF servo, and #545 and #546 close the remaining paths. Option B, an explicit counted re-lock, is revisited only if #545 or #546 cannot close its path.
- The CRF servo. The MMCM DRP answers zero. `Vphc_step` grades its step discard (#539).
- An lwSRP licence. The talker is opened by `AAF_CTRL[1]`; no SRP peer exists here.
- A step that lands while an `mr` restart is pending. Ruling 5802264260 item 2 merges the two, and pending lasts until a PDU at the new level has gone out (ruling 5818091077). `tb/verilator/tkdiag` T17 and T18 grade the restart engine PDU by PDU, and its `mcr_mutants.py` plants the engine that cancels, a shared target, and a pending window that ends at the adoption or runs to the end of the hold.
- The step policy's thresholds. The donor's engine suite proves them; this leg only relies on them.
- The physical re-base. The #117 bench measures it.

The talker's cadence in this compressed model is not the product's, so its
stream is graded against its own baseline rate.

`CLKV_SRC`, like `RSP_SRC` and `DP_SRC`, rebuilds this leg against a mutated copy.
Measured on 2026-09-24 with Verilator 5.050: 8.04 M cycles, about 40 s including the build.
On the same eight-job host the sweep's three controls took 133 s, and `make gmstep-mutants` (the leg and all eleven controls) 405 s.

## 2026-08-13 — the control plane was SUBSTITUTED, and this suite was rewritten around it

The entire legacy IEEE 1722.1 / SRP control plane is **deleted**:
`hdl/ieee17221/aecp/**`, `hdl/ieee17221/acmp/**`,
`hdl/ieee17221/adp/{adp_advertiser, KL_adp_parser, adp_pkg}.sv` and
`hdl/ieee8021q/srp/**`. `milan_datapath` instantiates `hdl/milan/KL_pp_shadow.sv`
**unconditionally** as THE control plane, `tx_drain_i` is 0, and the processor's
packed TX rides the control lane through `ctl_tx_mux`.

That is not a refactor from a test's point of view. Whole classes of witness
stopped existing, and a harness that kept reading them would have been asserting
against structural zeros — the exact failure mode the zeros are documented to
prevent. **Every deleted check below names its subject and why it is gone; every
repointed check names its old witness and its new one.** Nothing was neutered to
make a run pass.

### What the plane deletion cost this suite, honestly

Three things are structurally unreachable **on these legs**, and the reason is
arithmetic rather than a defect:

1. **The ADP advertisement.** Milan 5.6.3.5.2 makes the first advertisement wait
   `T-ADP-DELAY-START`, a PRNG draw of 0…2000 ms. `milan_dp` passes no
   `-GPP_TIM_DIV_*`, so the processor's millisecond is the silicon one —
   100,000 axis cycles — and the draw is up to 2·10⁸ of them. *Measured: no
   ADPDU in 40,000,000 cycles.*
2. **The talker's destination address, and therefore ACMP `SUCCESS`, the SRP
   Talker Advertise, MSRP/MVRP on the wire and every class-A tag.**
   `acmp_declaring_o` is reachable only through a MAAP `ALLOC_DA` success, and
   `KL_maap` is elaborated here at the silicon rate (`MAAP_CLK_HZ_P` defaults to
   `MILAN_CLK_FREQ_HZ`), so its Annex B claim walk — 3 probes × ~500 ms plus
   announce — is ~1.5·10⁸ cycles away. *Measured: still PROBING after
   40,000,000 cycles.* Waiting would add ~25 minutes **per elaboration** to a
   ten-leg suite.
3. **A MAAP-granted destination address for talkers `t > 0`**, which is the same
   arithmetic as (2) seen from the framer: a source that never reaches
   `acmp_declaring_o` never gets a DMAC. `cfg_aaf_bypass` (AAF_CTRL[1]) is the
   escape hatch these legs use to keep the framers awake without one.

**Where that coverage went:** `tb/verilator/pp_shadow` elaborates the *same*
gateware with both millisecond scales compressed onto one grid
(`-GPP_TIM_DIV_MS_P=100`, `-GMAAP_CLK_HZ_P=100000`) and grades the DA gate, the
`SUCCESS` `PROBE_TX` answer with its `stream_id` and `stream_dest_mac`, the
whole 82-octet ADPDU byte-exact against the `0x600` CSR group, and the
MSRP/MVRP frames sharing `ctl_tx_mux` with MAAP. It is not lost coverage; it
moved to the only suite that can run it.

**What stayed here** is everything the data path owns and everything the control
plane can still do at real-time rates: the listener BIND_RX ladder (the
processor answers, launches its own PROBE_TX, and settles — this harness now
plays the talker), the ACMP responder, the stream-table alias (TRAP-1), the SRP
**Domain adoption** surface (`0x788` and the AAF C-TAG really do move together),
AAF/CRF wire truth, the channel-map crossbars, PCMRX and fabric-render policy,
I2S, CBS/queues/classifier, PTP, the TCAM/RX filter, latency taps, the loopback
lane, and the LiteX CSR boundary itself.

### Two RTL findings this suite used to report — both now CLOSED in `hdl/`

**`aecp_in0_fmt` was tied to `64'd0`.** That net is `fmt0_i` for
`KL_avtp_rx_monitor_ctx` — **the expected format for `STREAM_INPUT[0]`** — and
the monitor's first acceptance term is `subtype == fmt[63:56]`, so against a
zero format a *perfectly conformant* AAF PDU on the bound `stream_id` was
counted `UNSUPPORTED_FORMAT` and never reached the depacketizer or fabric render.
Stream 0 accepted nothing. `milan_datapath.sv` now folds the setting over the
declaration: `aecp_in0_fmt` reads the processor's published SET_STREAM_FORMAT
row 0 when a controller has set one and the generated `ADP_STRIN0_FMT_C`
otherwise, exactly as `aecp_pres_offset` folds set offsets over `PRES_DFLT_C`
rather than a zero. The declaration is the default; the setter owns the rest
(issue #67).

`sim_main.cpp` grades the acceptance path again end to end and byte-exact:
untagged and C-tagged conformant PDUs advance PCMRX and produce all six
48-byte-payload render beats, `MEDIA_LOCKED` asserts, an unbound `stream_id` does not move
`FRAMES_RX`, and the TCAM prefilter section proves both halves of its property
again (the filtered observer leg goes silent **while** PCMRX and fabric render keep consuming).
The gate is shown to be *discriminating* and not merely open by the wrong-rate
PDU two sections later: `nsr 0x07` still counts `UNSUPPORTED_FORMAT` and
delivers no PCMRX or render traffic.

**The CRF clock-source compare had no driver.** `aem_crf_clksrc_w` lost its
only writer with the old AECP response builder, while `KL_mmcm_drp_servo` and
`mcr_restart_p_w` still compared it against `aecp_clk_src`; `0 == 0` read TRUE,
so the fabric behaved as if the CRF media clock were selected. Both nets are
**deleted** — first for an interim trio of constants, and since #74 for the
LIVE resolve: `media_clk_resolve` compares the stored selection against the
shape's generated `AEM_CRF_CLKSRC_C` once, registered, with the `16'hFFFF`
no-descriptor fold keeping a CRF-less shape structurally false. The
consumers read the resolved nets. `sim_main.cpp` and `sim_nxn.cpp` assert
the consequence on this suite's never-selects-CRF legs — `mnco_servo_en_w`
0 and `MCSRV_STAT[2:0]` IDLE at the live default — while `obj_aclk`'s [CRF]
phase and `[CRF-SEL]` grade the selected half. On the broken build
`MCSRV_STAT` read `0x21`.

## The device answers AECP now — and what this suite can and cannot see of it

"No AECP" is dead as a premise. The protocol processor carries an AECP µCPU
(`KL_aecp_ucpu` + `KL_aecp_desc_store` + `KL_aecp_engine`, driven from
`ucode.hex`) and handles 30 AEM opcodes plus Milan `GET_MILAN_INFO`. The served
set includes descriptor reads, lock and configuration operations, read-side
stream and clock commands, sampling-rate and clock-source setters, the stream
setters (`SET_STREAM_FORMAT` both directions and `SET_STREAM_INFO`'s
MSRP_ACC_LAT_VALID sub-command, with this fabric answering the format verdict
and consuming the published settings - the `#67` block in `sim_nxn.cpp` grades
the whole loop), Identify,
registration, counters, AVB information, AS path, and both audio-map
directions. `IDENTIFY_NOTIFICATION` sent as a command returns `BAD_ARGUMENTS`
(IEEE Section 7.4.39.2 beats Section 9.3.5.3.3). Commands outside the implemented inventory
receive a conformant `NOT_IMPLEMENTED` echo with the command payload and length
preserved and the frame padded to the 60-octet minimum. The exact inventory is
gated by [`aecp_engine_steps.py`](../../../tests/steps/aecp_engine_steps.py) and
the pinned processor's
[`06_aecp_engine.md`](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/44489453cf362c7a41c9e020f4896f967dc2a4d1/docs/architecture/06_aecp_engine.md).

**This suite backs no descriptor memory, on purpose and on record.**
`milan_datapath` exposes nine ports for the AEM image the store fetches
(`o_desc_mem_req_valid` … `i_desc_mem_rsp_err`). Every leg here drives
`i_desc_mem_req_ready` **low explicitly**, in the reset section, next to a
comment that says what that means: it is `KL_aecp_desc_store`'s documented
degrade path — the watchdog abandons the burst, the image never validates, and
`READ_DESCRIPTOR` comes back well formed but empty-handed. A zero left at a port
by accident and a zero driven by a decision look identical on a waveform, so it
is stated. The `[AECP]` checks in `sim_nxn.cpp` grade that path: an answer
arrives, it is an `AEM_RESPONSE`, its status is `BAD_ARGUMENTS` (an unvalidated
image reports `configurations_count = 0`, and the µprogram range-checks the
configuration index *before* it locates, so this is not
`NO_SUCH_DESCRIPTOR`), it carries the Section 7.4.5 stub at `cdl = 20`, and it is
padded to 60.

**The SERVED path lives in `tb/verilator/pp_shadow`**, which backs those ports
with a real `AEMI` image and grades `SUCCESS` with the descriptor bytes compared
octet for octet, the locate miss, the bad configuration index, the
`NOT_IMPLEMENTED` echo, the two silent-refusal cases, and the no-memory degrade
with recovery.

**`[NOTIFY]` is Milan 5.4.5 on the wire (issue #69).** The broad `sim_nxn`
legs elaborate the direct option-OFF verification boundary. Two controllers
register, and the section grades requester exclusion, no-op suppression,
per-controller sequence IDs, byte-identical notification content, and the
departing-controller monitor over the real RX and TX trunks. Its gPTP block
pins the ownerless option-OFF boundary: maximal writes to GM, parent, domain,
pdelay, CLKV, and AS_PATH remain inert; public state stays
zero with `tu=1`; solicited `GET_AVB_INFO`/`GET_AS_PATH` serve that ownerless
state; and no gPTP, counter, or path notification is manufactured.

The product-on assertions live in `obj_gptp`, where the fabric engine supplies
the evidence. A selected peer drives Pdelay, Announce, and a legal
Sync/Follow_Up through the real MAC tap. Sync lock and a later GM switch must
move the CLOCK_DOMAIN LOCKED/UNLOCKED counters; the GM switch must also move
AVB_INTERFACE GPTP_GM_CHANGED. Both dirty paths must appear at `pp_ctr_evt_*`,
emit descriptor-specific unsolicited `GET_COUNTERS`, and match the following
solicited counter bodies. The same CLKV verdict is checked in MAC-bound AAF and
CRF headers as `tu=0` while locked and `tu=1` before Sync and during GM-change
holdover. A LINK_DOWN/LINK_UP pair inside one compressed processor second also
proves that the second AVB_INTERFACE event is suppressed, retained dirty, and
released exactly once when that descriptor's limiter opens. These checks fail
if either `ctr_avb_dirty_w`, `ctr_ckd_dirty_w`, or either media `tu` connection
is removed.

The timed option-OFF leg keeps the scheduler timebase compressed for the
30–60 s controller monitor. `[CTRS]`/`[CTRS-OUT]`/`[CTRS2]` still grade the
served counter geometry and lossless descriptor arbiter; their gPTP writes
specifically prove that ownerless state cannot create a hidden counter edge.

**`[CTRS-CRF]` is the CRF Media Clock Input's row (#529).** The shape appends
that Stream Input at index `N_STREAMS`, and its ten Milan Table 5.16 counters
are `KL_crf_rx`'s. On every broad `sim_nxn` leg, before the 5.3.8.7 section
binds the sink, the section reads `GET_COUNTERS(STREAM_INPUT, N_STREAMS)`
through the processor. It checks the full SUCCESS response from reset (cdl 148,
mask `0xF3F`, ten zeros, every unclaimed quadlet zero). It writes a distinct
full-width signature into each root tally wire by name and reads each quadlet
back, with `CRF_STATUS` as the second reader of three of them. That arm grades
the gather mux only: it cannot see which `KL_crf_rx` output drives a wire. It
proves that no AAF input carries a CRF quadlet or loses `0xFFF`, and that index
`N_STREAMS + 1` is still NO_SUCH_DESCRIPTOR with the empty body. Raising the
bench lever at `0x738` is the not-bound to bound edge. It must wipe the row and
reach the descriptor arbiter as {STREAM_INPUT, `N_STREAMS`} alone. The harness
records every tuple the arbiter hands over in that window, of any type and at
any index, so another STREAM_INPUT row, a STREAM_OUTPUT row (the CRF output's
at the same index included), AVB_INTERFACE 0, CLOCK_DOMAIN 0 or any other tuple
there fails. Real PDUs of the followed stream then carry FRAMES_RX (interval
law) and STREAM_INTERRUPTED (per-event law) from `0xFFFFFFFF` through zero.
Last, in a fresh era and with no tally seeded, each of the ten is moved by its
own engine event to a count no other tally shares. The events are rejected
PDUs, sequence gaps of one and of two or more, two runs of eight clean PDUs
that each lock, `mr` toggles, `tu` bits, timestamps in the past and beyond the
early limit, and the engine's 100 ms silence timeout for the unlock. The
harness advances that timeout counter to its last millisecond, which runs for
real. This arm grades each `KL_crf_rx` output binding, not only the mux. The
timed leg's `[NOTIFY-CRF]` raises the same edge with two controllers
registered. The push must reach both controllers, each copy byte-identical from
the body on to the solicited answer. A second edge inside the same processor
second is withheld until the one-second limit releases it, and the next two
seconds without a change bring no further push. Each of these wiring mutations
turns at least one of those checks red: the row removed, two quadlets permuted,
a 16-bit slice, a claimed tv pair, the dirty source removed, the CRF row
answering for the AAF inputs, the AAF guard answering for the CRF input, one
tally unwired, the row's pending bit never cleared, and the CRF pulse also
raising the AAF inputs, STREAM_OUTPUT `N_STREAMS`, AVB_INTERFACE 0,
CLOCK_DOMAIN 0 or a tuple at an undeclared index. Each of the 45 pairwise
exchanges of the ten `KL_crf_rx` output bindings turns both of its quadlets red
on `obj_nxn` and `obj_nxn8`.

`sim_nxn.cpp`'s `[T66]` covers the other side of the same coin.
`GET_AUDIO_MAP` succeeds on both Stream Port directions, and
`ADD_AUDIO_MAPPINGS` plus `REMOVE_AUDIO_MAPPINGS` use the processor's two-pass
transaction face to update the live root stores. The harness proves full-page
ADD and readback, idempotent ADD, all-or-nothing refusal after a late invalid
row, duplicate-safe REMOVE, cross-port output ownership, running-output
refusal, and generated input-port geometry through the live crossbar RAM. It
derives the AX7101 output cluster count from the generated descriptor, accepts
and round-trips every published offset, preserves a clear fabric-source marker
for unbacked clusters, rejects same-key and cross-port replacement, and refuses
the first offset beyond the model.

## Check counts, before and after

"Before" is the state after the compile fix that made the suite build at all
(`sim_nxn.cpp` reached deleted RTL through Verilator XMRs and did not compile,
so *no* leg ran). Every after value below was measured in one broad run
on 2026-09-06 UTC for Issue #367, except the separate physical suite.
The eleven existing legs retain their 2026-09-02 counts.
Round two separates the physical leg's driver deadline.
No row projects unexecuted checks.
These are pre-merge measurements from the two implementation branches.
No count is inferred for their merged tree.

Rows dated 2026-09-24 UTC were re-measured for #508, in one sweep at its head.

| leg | before (measured) | #508 round 1 (measured; date noted below) | note | dev c266432d record |
|---|---|---|---|---|
| `obj_gptp` (`sim_gptp`) | not available | **181 / 0** (2026-09-24 UTC) | product-default fabric-owner run; inert-write negatives, both counter dirty paths, limiter pending-release, AAF+CRF `tu`, the three drop-counter routes at 0x7E8/0x7EC | **164 / 0** |
| `obj_dir` (`sim_main`) | 273 checks / 75 fail | **231 / 0** (2026-09-24 UTC) | the focused ownerless option-OFF target; exact CRF `tu=1` on every captured PDU | **233 / 0** (2026-09-24 UTC); #387 adds the PHC-step `mr` checks, including settime toggle and MEDIA_RESET |
| `obj_notify` (`sim_nxn`, timed) | not in the old table | **345 / 0** (2026-09-24 UTC) | the compressed-timebase 5.4.5 notify leg | **117 / 0** |
| `obj_crflic` (`sim_crf_licence`) | not in the old table | **85 / 0** (2026-09-24 UTC) | #530; its three mutants are caught by `make crflic-mutants` | same |
| `obj_nxn` (`sim_nxn`) | 378 / - (did not compile) | **1709 / 0** (2026-09-24 UTC) | the old 145 was already stale at #294's merge (issue #314 measured 1673 there); the suite has kept growing since | **1679 / 0** |
| `obj_nxndv` (`sim_nxn`) | not in the old table | **1711 / 0** (2026-09-24 UTC) | the divergent-shape leg | **1682 / 0** |
| `obj_nxn8` (`sim_nxn`) | 512 / not available | **3137 / 0** (2026-09-24 UTC) | `[T66]` grades atomic audio-map mutation (the old row's "current run summary below" pointer named a section that never existed - this cell is the measurement) | **3179 / 0** |
| `obj_nxn4c` (`sim_nxn`) | 378 / - | **1709 / 0** (2026-09-24 UTC) | | **1679 / 0** |
| `obj_nolpf` (`sim_main`) | 273 / 75 | **231 / 0** (2026-09-24 UTC) | re-run current (the old "not rerun after the `tu` assertion" caveat is retired) | **233 / 0** (2026-09-24 UTC); #387 adds the PHC-step `mr` checks, including settime toggle and MEDIA_RESET |
| `obj_prune` (`sim_prune`) | 31 / 0 | **33 / 0** (2026-09-24 UTC) | the old 31 was already stale at #294's merge (issue #314 measured 28 there); #390 adds the `SLIP_LB` structural zero, read behind listener 0 bound, fed and then starved, plus the `CHMAP_LOOP` lane-establishment read that makes the zero a measurement, whole word against the `0xDEADDEAD` poison and `CHMAP_SNAP[1]` valid before the projection (5 checks) | **33 / 0** |
| `obj_ax1x1` (`sim_main`) | 273 / 73 | **228 / 0** (2026-09-24 UTC) | 5 sections guarded out on this shape | **230 / 0** (2026-09-24 UTC); #387 adds the PHC-step `mr` checks, including settime toggle and MEDIA_RESET |
| `obj_aclk` (`sim_aclk`) | 5 / 0 | **140 / 0** (2026-09-24 UTC) | the #74 two-phase rework: INTERNAL drift kept, CRF alignment + servo + mr added; #390 adds the loopback-ring beat at INTERNAL, the zero-slip window under CRF, the SLIP CSR pair and the `CHMAP_LOOP` lane-establishment read behind its whole-word poison and `CHMAP_SNAP[1]` grades, and the priming PDU's loop-tap transit, which is what grades the drain that separates this phase's own priming PDU from one the render-law phases left in flight (25 checks); the balance is the #386 render law, which landed in this same leg with PR #435 | **139 / 0** |
| `obj_gmstep` (`sim_gmstep`) | not in the old table | not in #508 round 1 | #387; `gmstep_mutants.py` catches the acceptance's three controls in the sweep, and `make gmstep-mutants` all eleven (two on the option-off leg) | **48 / 0** (2026-09-24 UTC) |
| `obj_ax1x1gptp` (`sim_ax1x1gptp`) | **126 / 0** before round two | **127 / 0** (2026-09-07 UTC) | Separate `milan_dp_gptp` suite; trimmed waits; additional four-interval assertion; original spans remain opt-in | same |

Earlier re-measurement had stopped because the `protocol-processor` submodule
working tree went out from under the build — `protocol_processor_top.sv` had an
uncommitted `KL_aecp_engine` instantiation and a nine-pin `desc_mem_*` port that
the source list did not name, so elaboration failed with `MODMISSING`. That is
resolved: the submodule is at its recorded pin, the Makefile names
`ucpu_pkg.sv`, `KL_aecp_ucpu.sv`, `KL_aecp_desc_store.sv` and
`KL_aecp_engine.sv`, and it generates `ucode.hex` next to `ltn_rom.hex`.

The `sim_nxn` drop is the deleted lwSRP attribute-row and ACMP context-table
windows: eight whole sections whose subject is a table `milan_datapath` now ties
to zero. Each one is replaced in place by a block comment naming the subject,
the tie-off, the measurement behind "unreachable", and where the coverage went.

### Two checks that were failing for reasons worth writing down

* **`[T67]` cadence read 3072 cycles/PDU instead of 12500.** With
  `aecp_odmap_dyn_w` tied off, `CHMAP_CTRL[0]` is the *whole* selector between
  the `media_tick`-paced crossbar and the `clk_audio/512` zero-fill path, and
  `[T66]` had deliberately left it at 0. Every leg but `obj_aclk` clocks
  `clk_audio` 1:1 with `axis_clk`, so the static path measured 195.3 kHz and
  looked like a 6× cadence defect. `[T66]` now leaves the crossbar armed and
  `[T67]`'s banner states which grid it is on.
* **The `0x002C` boot seed.** There is no seeder any more, so key 0 reads empty.
  The check grades the two halves of the new structural truth — the read mux is
  still live, the RAM is empty, `CHMAP_CTRL[0]` is 0 — and will fail the day a
  seeder returns in any form.

Issue #443 adds `RENDER-CSR` checks to `obj_aclk`.
They read `RENDER_STAT` (`0x8DC`) through AXI-Lite.
The expected word samples independent taps at the capture edge.
Checks cover prefill, nonzero fill, convergence, rails and backpressure.
Talker and invalid-listener selections return zero; writes are ignored.

The additional control campaign is explicit:

```sh
make -C tb/verilator/milan_dp render-csr-controls
```

| Control | Required result |
|---|---|
| Clean `--render-csr-only` | All checks pass, including reset after a rail |
| Fill field tied zero | Fails `RENDER-CSR: filling mirrors taps` |
| Bit 9 forces listener 0 | Fails `RENDER-CSR: bit 9 preserves talker rejection` |
| Stage instance removed, outputs tied zero | `--render-csr-absent` passes despite accepted ingress |

Temporary control sources leave tracked RTL unchanged.
Three extra elaborations stay outside the default sweep's deadline.
The default sweep still runs the positive CSR checks.
The two-stream `milan_dp_render` leg separately checks listener selection.

## Render phase records from the mutation controls

`render_mutants.py` prints one flushed `RENDER-PHASE` line around each build
and each short-mode run it already makes (Issue #445). They are an observation
of WHEN each phase ran and nothing else: they add no check, no tally and no
verdict, they change no command, argument, status or exit, and the `[PASS]` /
`[FAIL]` lines and the closing check tally are the ones this driver printed
before. The measurement they exist for is which case and phase the sweep's
per-suite guard lands in when the suite is killed with results missing.

Each line is `RENDER-PHASE ` followed by a JSON object. Every record carries
`seq`, a sequence number that advances even when a write fails, so a lost
record leaves a visible gap; and `t_s`, seconds since the `origin` record,
from a monotonic clock read for observation only. Durations compare inside
one run and mean nothing across runs.

| `event` | when | fields beyond `seq`, `event`, `t_s` |
|---|---|---|
| `origin` | once, before any phase | `clock`, `unit`: the origin every later `t_s` counts from |
| `baseline` | before the positive controls | `case`, `selected`: `prebuilt` when the executable the sweep already built was reused, `fallback-build` when this driver built the unmutated leg itself |
| `start` | before an existing build or run call | `case`, `phase`, `mode`, `idle_s`: the gap since the previous phase ended, or since the origin |
| `end` | after that call returned | `case`, `phase`, `mode`, `elapsed_s`, `status`, and `returncode` on a build |
| `interrupted` | inside the existing SIGTERM handler | `state`: `active` with the running `case`, `phase`, `mode`, `elapsed_s` and `incomplete`, or `idle` with `idle_s` |
| `end-of-run` | after the last phase, before the tally | `state`, `idle_s` |

`case` is a fixed logical label: `control` for the unmutated leg, and the
mutation's own name with spaces and hyphens turned into underscores for each
of the four defects. `phase` is `build` or `simulation`. `mode` is the short
mode the leg runs, and is `null` on a build, which serves both control legs.
The six outcomes this arm grades are the two `control` modes and the four
mutations, and `case` with `mode` names each one.

`status` is what the existing call returned, so it reads differently per
phase: a `simulation` end carries the child's integer return status (negative
is the signal that killed it), and a `build` end carries `built` or
`no-executable`, which is what the build helper returns to its caller.

A `build` end carries `returncode` as well: the exit status the `make` recipe
itself returned, which the helper does see. The two answer different questions,
and a diagnostic needs both: a recipe that returned 0 and left no executable
behind is a different failure from one that returned 2, and `status` alone
reports them identically. A build that completed always observed the status,
so a `null` `returncode` would mean it never reached the record.

The limits, so a reader does not over-read a record:

* **A phase with a `start` and no `end` is incomplete.** It earns no pass and
  no caught mutation, and the driver's own verdict lines stay the only result.
* **Missing records make the diagnostic incomplete, never a different
  outcome.** A write that fails, a kill before the handler runs, or a log the
  sweep truncated loses records; nothing recomputes them, and no case's result
  is inferred from another's.
* **A missing timing is `null`, not a number.** Reading the clock is part of
  the telemetry, so a reading the clock will not give costs that record its
  `t_s`, `elapsed_s` or `idle_s` and nothing else: no offset is estimated from
  a neighbour, and the run's results, verdicts, tally, exit 143 and cleanup are
  the ones it would have had with no instrument at all. A `null` origin makes
  every later `t_s` `null`, which is a run with the phase order recorded and
  no durations.
* **`interrupted` reports which call was running, not which record was last.**
  A phase stops being the running one before the record that closes it is
  written, so a kill can never report a phase both ended and incomplete. In
  the moment between a call returning and its `end` record reaching the log,
  the driver is genuinely idle and a kill there says `idle`; the `end` record
  it displaced is then one of the missing records above.
* **Nothing about the child is recorded**: no path, no environment, no
  captured output. The captured output still reaches the log through the
  existing failure paths only.
* **A case whose pattern check fails builds and runs nothing**, so it
  contributes no phase record at all; its existing `[FAIL]` line is the report.
* **The clock is the host's.** A duration includes whatever else that machine
  was doing, and the per-suite guard (3600 s for this suite under #387) is
  still owned by `scripts/run_all_suites.sh`.

`test_render_phase_observation.py` holds this contract with pure fixtures: a
fake clock (including one that refuses readings), a recording stream that can
hand the kill to the installed handler at a chosen record, stubbed build and
wait results, and a guard in place of the subprocess handle, so an arm that
reaches a real process launch fails instead of running one.

```sh
python3 tb/verilator/milan_dp/test_render_phase_observation.py
```

## Rules this suite is held to

* **Gate on exit codes.** A compile error prints no `FAILED` line, so grepping
  the output for "fail" reads as green.
* **A check that asserts a structural zero must say so, and say why.**
  Otherwise it is deleted — a zero that nobody can distinguish from "idle" is
  not evidence.
* **No vacuous passes.** Where a property becomes unprovable (the class-A
  tag withdrawal) the check is removed and the gap is printed as a `[GAP]`
  line on every run, rather than left passing for the wrong reason. (The
  10.4.3 `mr` gate carried such a line until #74 made the trigger reachable;
  `obj_aclk`'s [MR] arm grades it now, both directions.)
* **Name the shape.** Every leg puts its config's generated directory *first* on
  the include path. Without it the build falls through to
  `hdl/common/gen/`, which is whichever config last ran `--write-rtl`.
