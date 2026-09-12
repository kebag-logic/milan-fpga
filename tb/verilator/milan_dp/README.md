<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# milan_dp — the `milan_datapath` integration suite

`make` builds **eleven elaborations** of `hdl/milan/milan_datapath.sv` (the vendor-neutral
Section A.9 wrapper the LiteX SoC instantiates) and runs a self-checking harness
against each. `make` exits non-zero if any leg fails; **gate on the exit code**,
never on grepping the log — a compile error prints no `FAIL` line at all.

The `sim_nxn` legs regenerate their descriptor image in a unique directory
under `TMPDIR` (falling back to `/tmp`) and remove it after a successful load.
Set `TMPDIR` to a filesystem with enough quota when review lanes run in
parallel. A failed generator deliberately leaves that directory and names its
log in the failure so the artifact can be inspected.

| objdir | harness | shape | what it is for |
|---|---|---|---|
| `obj_dir` | `sim_main.cpp` | `endstation_arty_current`, N=1 | CSR, fabric protocol/media RX/TX, PHC, CLKV, CRF, RMON, and link guard |
| `obj_nxn` | `sim_nxn.cpp` | `endstation_arty_4x4`, N=4 | the 0x800 window → real engines, per-stream routing, TRAP-1 |
| `obj_nxndv` | `sim_nxn.cpp` | arty_4x4 with a GENERATED divergent header (input row 1 declares the 96 kHz base) | the per-row format facts: every tracked config is row-uniform, so only this leg can prove the verdict base and reset GET answer are the ADDRESSED row's and not row 0's -- same channel count on both rows, so the base is the one discriminator. `gen_divergent_shape.py` emits the header and the bench expectations at build time, like `ltn_rom.hex` |
| `obj_nxn8` | `sim_nxn.cpp` | `endstation_ax7101_8x8`, N=8 | the AX 8×8 target, retired input-pool posture, dynamic output maps, and loopback lane |
| `obj_nxn4c` | `sim_nxn.cpp` | `endstation_arty_4x4`, N=4, 4 wire channels | the shipping Arty shape (framer width ≠ shadow reset) |
| `obj_nolpf` | `sim_main.cpp` | `endstation_arty_current`, `LPF_P=0` | the spent area lever: no digital acceptance surface may move |
| `obj_prune` | `sim_prune.cpp` | all six tier-1 blocks pruned | the inert values are STRUCTURAL zeros, not not-armed-yet zeros; `SLIP_LB` (#390) is read behind listener 0 bound, fed well-formed AAF PDUs and then starved, so a built ring would count. The same section then establishes the lane the way the [register map](../../../docs/reference/REGISTER_MAP.md) instructs, `CHMAP_LOOP` `{mask_valid, valid, fed}` = 1, 1, 0, so the zero is a measured absent lane and not an unarmed word |
| `obj_ax1x1` | `sim_main.cpp` | `endstation_ax7101_1x1_tdm8`, direct option OFF | AX7101 geometry and media datapath coverage plus exact ownerless gPTP state; this verification elaboration is not a flashable product image |
| `obj_aclk` | `sim_aclk.cpp` | same ownerless option-OFF geometry, true 391/1591 `clk_audio` ratio | two phases (#74): the INTERNAL free-run drift (-10.64 ppm, the standing free-run rule), then CRF selected - the grids aligned (|ppm| < 0.5, zero junction slips), the servo in ACQUIRE through the live select, both 4.4.4.3 `mr` triggers and the 10.4.3 negative; the #390 ring phases ride the same instrument: the loopback ring is fed at the physical rate (6 x 512 x 1591/391 = 12500 + 52/391 axis cycles per PDU, the cadence a peer disciplined to the same CRF produces) and dups once per beat period at INTERNAL on the predicted beat, one event per fed pair. The closed form: the burst-vs-tick phase walks 52/391 cycle per PDU, so the first dup comes (P - phi) / (52/391) PDUs after a restart (P = 2083.33 cycles, phi = the offset of the burst's first beat after the preceding tick); the harness aims the restart burst's `tlast` 0.93 of a tick after a media tick (band 0.90 to 0.96), predicts the first dup from the first beat and grades it within 25 percent over a window of 1.5 times the prediction. The same aim and window under CRF show zero, a ONE-SIDED sensitivity: a pop grid faster than the push by more than 7 ppm dups inside the window, a slower one would need about 300 ppm to skip (the grids' own two-sided check is [CRF] abs(ppm) < 0.5). `SLIP_LB`/`SLIP_TDM` (`0x8D4`/`0x8D8`) read their taps after induced ring and TDM-junction slips, and `CHMAP_LOOP` reads `{mask_valid, valid, fed}` = 1, 1, 1 here - the fed half of the two-leg lane-establishment pair whose other half is `obj_prune` |
| `obj_notify` | `sim_nxn.cpp` (`NOTIFY_TIMED_TB`) | `endstation_ax7101_1x1_tdm8`, direct option OFF, `PP_TIM_DIV_US_P=1` + `PP_TIM_DIV_MS_P=100` | Milan 5.4.5 scheduler timing: the GET_COUNTERS one-second limit and 30–60 s departing-controller monitor; retained gPTP writes are graded inert and emit no notification |
| `obj_gptp` | `sim_gptp.cpp` | product-default `endstation_ax7101_1x1_tdm8`, fabric gPTP at 2 MHz | selected-peer Pdelay/Announce/Sync publication through CSR and AECP; GM-switch AVB_INTERFACE/CLOCK_DOMAIN counters and dirty notifications; per-descriptor one-second suppression and pending release; AAF+CRF `tu` wire propagation; bounded PathTrace, coherent cutover, and inert legacy writes |

The separate `milan_dp_gptp` suite reuses this Makefile's physical recipe:

| objdir | harness | shape | what it is for |
|---|---|---|---|
| `obj_ax1x1gptp` | `sim_ax1x1gptp.cpp` | AX7101 1x1 TDM8, gPTP ON, 50 MHz | Physical timer cadence, independent scheduled peer, eight-channel diagnostic loopback, loss/recovery/reset and stalls |

## Contents

- **[First AX7101 1x1 eight-channel run](#first-ax7101-1x1-eight-channel-run)** -- Run the focused datapath baseline and identify its coverage limits.
- **[AX7101 1x1 eight-channel gPTP physical-rate run](#ax7101-1x1-eight-channel-gptp-physical-rate-run)** -- Run combined clocks, peer exchange, and diagnostic audio checks.
- **[2026-08-13 — the control plane was SUBSTITUTED, and this suite was rewritten around it](#2026-08-13--the-control-plane-was-substituted-and-this-suite-was-rewritten-around-it)** -- What the legacy-plane deletion did to this suite: which checks were repointed to the protocol processor's class-D face and the 0x920 window, and which were deleted because their subject no longer exists
- **[The device answers AECP now — and what this suite can and cannot see of it](#the-device-answers-aecp-now--and-what-this-suite-can-and-cannot-see-of-it)** -- What the AECP µCPU answers, why every leg here drives the descriptor-memory ports into the documented degrade path deliberately, and the dynamic-output-map capability that the substitution cost
- **[Check counts, before and after](#check-counts-before-and-after)** -- Per-leg check totals, with every row that was not re-measured after the last edit marked as such rather than projected
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
Every default suite retains its 1800-second deadline.
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
The `milan_dp` default retains its eleven existing legs.
`suite_tally.py` reads its separate physical-rate summary.
It also counts 40 setup, audio and missing-response accounting checks.
`suite_shards.py` selects `milan_dp_gptp` only through `--physical-gptp`.
The nightly/manual job runs that selection without sharding.
The historical `milan_dp` directory remains on shard 0/4.
The existing `gptp` compressed smoke remains separately counted.
The option-OFF and fractional-audio legs retain their original models.

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

| leg | before (measured) | after (measured; date noted below) | note |
|---|---|---|---|
| `obj_gptp` (`sim_gptp`) | not available | **164 / 0** | product-default fabric-owner run; inert-write negatives, both counter dirty paths, limiter pending-release, AAF+CRF `tu`, the three drop-counter routes at 0x7E8/0x7EC |
| `obj_dir` (`sim_main`) | 273 checks / 75 fail | **230 / 0** | the focused ownerless option-OFF target; exact CRF `tu=1` on every captured PDU |
| `obj_notify` (`sim_nxn`, timed) | not in the old table | **117 / 0** | the compressed-timebase 5.4.5 notify leg |
| `obj_nxn` (`sim_nxn`) | 378 / — (did not compile) | **1679 / 0** | the old 145 was already stale at #294's merge (issue #314 measured 1673 there); the suite has kept growing since |
| `obj_nxndv` (`sim_nxn`) | not in the old table | **1682 / 0** | the divergent-shape leg |
| `obj_nxn8` (`sim_nxn`) | 512 / not available | **3179 / 0** | `[T66]` grades atomic audio-map mutation (the old row's "current run summary below" pointer named a section that never existed — this cell is the measurement) |
| `obj_nxn4c` (`sim_nxn`) | 378 / — | **1679 / 0** | |
| `obj_nolpf` (`sim_main`) | 273 / 75 | **230 / 0** | re-run current (the old "not rerun after the `tu` assertion" caveat is retired) |
| `obj_prune` (`sim_prune`) | 31 / 0 | **31 / 0** | the old 31 was already stale at #294's merge (issue #314 measured 28 there) and this 31 is a different 31; #390 adds the `SLIP_LB` structural zero, read behind listener 0 bound, fed and then starved, plus the `CHMAP_LOOP` lane-establishment read that makes the zero a measurement (3 checks) |
| `obj_ax1x1` (`sim_main`) | 273 / 73 | **227 / 0** | 5 sections guarded out on this shape |
| `obj_aclk` (`sim_aclk`) | 5 / 0 | **44 / 0** | the #74 two-phase rework: INTERNAL drift kept, CRF alignment + servo + mr added; #390 adds the loopback-ring beat at INTERNAL, the zero-slip window under CRF, the SLIP CSR pair and the `CHMAP_LOOP` lane-establishment read (22 checks) |
| `obj_ax1x1gptp` (`sim_ax1x1gptp`) | **126 / 0** before round two | **127 / 0** (2026-09-07 UTC) | Separate `milan_dp_gptp` suite; trimmed waits; additional four-interval assertion; original spans remain opt-in |

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
