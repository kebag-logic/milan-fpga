<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# Ten e1 switch power cycles

Measured on 2026-09-27, under the [bench assignment](https://github.com/kebag-logic/milan-fpga/issues/394#issuecomment-5858215210).

| Acceptance | Verdict | Evidence |
|---|---|---|
| #394 acceptance 2, e1 only | FAIL | Recovery succeeded, but expected LINK_UP/LINK_DOWN increments were absent. DUT PHY link loss and link-edge times were not observed. |
| #387 acceptance 4 | NOT MET (not exercised) | Every step occurred during HOLDOVER with both streams absent. Needed: a grandmaster change while a locked CRF stream keeps running. |

The [round-2 decision](https://github.com/kebag-logic/milan-fpga/issues/394#issuecomment-5859045504) leaves #394 and #387 open.

It does not close #75 or grade #593.

## Contents

- **[Identity and setup](#identity-and-setup)** -- Identify the image, port, streams and starting state.
- **[Method and limits](#method-and-limits)** -- Define capture boundaries, timing uncertainty and observable quantities.
- **[Per-cycle results](#per-cycle-results)** -- Record each outage, recovery and media transition.
- **[Counter and restart findings](#counter-and-restart-findings)** -- Separate the failed link counters from measured media behavior.
- **[Restore and validation](#restore-and-validation)** -- Record the restored bench and local gates.
- **[Artifact hashes](#artifact-hashes)** -- Locate retained raw evidence through its hashes and sizes.

## Identity and setup

The assigned image derives from `9e9954e96bf55181edb9949ae94c9abd4ab6aaf5`.

The lane base is `2a2a7bb655e528edc3087c88033cd3a47546feb4`.

Only documentation and evidence differ between those commits.

| Identity check | Result |
|---|---|
| VERSION | `0x00020060` |
| ROM CRC32, 52,216 bytes | `9b6576a9` |
| QSPI payload CRC32, 3,825,788 bytes | `3c18c276` |
| AEM CRC32, 7,352 bytes | `93742dd2` |
| Bitstream SHA-256, 3,825,992 bytes | `1696d1ea7568b2cf3cd536b1d34488e1ce7702e4a79e7cf3aca2c6ed6a54d2c7` |
| AEM SHA-256 | `9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404` |
| CSR map SHA-256, 9033 bytes | `92981a367616f79dc5d5382257afdb0aeff211845f86ea3b322102292c562e35` |
| Live ENTITY and CONFIGURATION | Exact matches to the assigned AEM descriptors |
| e1 constraints | RX clock K18, MDIO L16; match the [platform](../../sw/litex/platforms/alinx_ax7101.py) |

Readback proves CRC consistency, not configuration SHA-256.

The existing [identity method](117_GPTP_SILICON_EVIDENCE.md#candidate-image-and-identity-proof) was repeated.

All seven outlets initially read ON.

All eighteen queried stream states were unbound.

The DUT initially selected INTERNAL, source 0.

The reference peer retained INTERNAL and its original sampling rate.

| Direction | Binding | Format |
|---|---|---|
| DUT to reference peer | Output 1 to input 8 | CRF, `041060010000bb80` |
| Reference peer to DUT | Output 2 to input 1 | Same CRF format |

DUT source 1 selected the bound CRF input.

Both listeners reported MEDIA_LOCKED before the first outage.

The DUT reported `SYNC=1`, `ASCAPABLE=1`, `TU=0`.

Its media servo reported LOCKED.

The 12-second baseline captured 6,000 PDUs in each direction.

All carried `tu=0`.

AAF render timing was not measured by this CRF run.

## Method and limits

Only OUT4, the bench AVB switch, was cycled.

Cycle 1 repeated the earlier [OUT4 proof](117_GPTP_SILICON_EVIDENCE.md#out4-is-the-switch).

Switch messages stopped, and the controller port lost carrier.

DUT console replies continued; its reset epoch remained 1.

The reference peer's advertisement index continued increasing.

Its grandmaster-change counter also continued, without resetting.

Every other outlet remained ON.

No later cycle started before this proof passed.

Every action held the bench lock for its own duration.

All commands and captures ran in bounded foreground processes.

The DUT was never rebooted, flashed or power-cycled.

No controller re-bind occurred during any cycle.

The console sampled every 250 ms.

Each cycle retained these independent observations:

- DUT console health, PHC time, reset epoch and MAC status.
- `CLKV_STAT`, `CLKV_TUCNT`, `A_MCSRV_STAT` and CRF emission words.
- Controller GET_COUNTERS and retained ACMP bindings, approximately every second.
- Inline capture on the DUT link, including both CRF directions.
- Controller-port capture, carrier edges, and timed outlet commands.

Counter snapshots cover AVB_INTERFACE, STREAM_INPUT, STREAM_OUTPUT and CLOCK_DOMAIN.

The [register map](../reference/REGISTER_MAP.md) defines the sampled fields.

Captures use the earlier tap envelope and timestamp decoder.

Within-capture intervals use unwrapped hardware timestamps.

Cross-host comparisons use three clock probes before and after.

The quickest round trip supplies each clock-offset estimate.

Those estimates and their half-round-trip bounds remain in every analysis.

Console resolution is 250 ms; controller observations are coarser.

Table decimals identify estimates, not matching absolute accuracy.

The console and controller record request-observation times.

Clock-probe half-round-trip bounds were approximately 0.15 s and 0.07 s.

The tap anchor spread was approximately plus or minus 0.05 s.

USB acquisition latency was not independently calibrated.

PHC steps are inferred from discontinuous UART PHC readings.

Each recorded bracket spans the final pre-step and first post-step reads.

No hardware step strobe or exact step counter was available.

The large observed steps cannot be explained by UART sampling jitter.

Valid CRF PDUs match the bound stream and advertised format.

The checks include subtype, version, length, frequency and timestamp interval.

They also require the expected VLAN and priority.

Every resumed PDU carried `tu=0`.

The recovery clock starts at the first returning Announce or Sync.

It ends when asCapable, sync and `tu=0` coexist.

The [documented bound](../design/GM_LOSS_RECOVERY.md#recovery-bound) is five seconds.

The media row permits recovery within one further stream restart.

That row is #117 outage-recovery context, not #387's bound.

#387 item 2 records the [media re-base contract](../design/GM_LOSS_RECOVERY.md#media-re-base-on-a-phc-step).

The [step policy](../design/TIME_SYNC.md#step-policy) identifies the triggering PHC steps.

The contract requires one counted event per step.

Licensed streams keep running.

One `mr` toggle and one MEDIA_RESET record that event.

It specifies no step-to-relocked-media time bound.

Every observed step occurred while the servo was in HOLDOVER.

Both CRF streams were absent from the wire.

These intervals measure outage recovery, including stream return and acquisition.

They do not measure a locked stream's step reaction.

DUT MAC_STATUS stayed at its software-published reset value, `0x0d`.

Nothing in this build writes it ([#599](https://github.com/kebag-logic/milan-fpga/issues/599)).

Whether the DUT PHY link dropped was not observed.

The inline capture point may hold that link up.

DUT link-down and link-up timestamps therefore remain unavailable.

Controller carrier edges describe another switch port, not DUT edges.

Cycle 1 carrier loss was delayed by blocking controller queries.

Later cycles used a separate 100 ms carrier sampler.

Both carrier methods and their raw records are retained.

The first returning tapped frame supplies a separate wire landmark.

The requested one-second restart comparison uses that observable landmark.

It cannot replace an exact physical link-up measurement.

Issue [#75](https://github.com/kebag-logic/milan-fpga/issues/75) separately starts timing at CONNECT_RX success.

These automatic returns issued no CONNECT_RX from the controller.

They do not satisfy that issue's hundred-reconnect experiment.

## Per-cycle results

All table times are seconds.

Carrier edges, GM return, PHC step brackets and first PDUs are relative to OFF.

Recovery is measured from the first returning GM message.

Outage media recovery is timed from the measured step bracket.

Its endpoint requires DUT MEDIA_LOCKED, `tu=0` and servo LOCKED.

The raw analysis separately records each contributing observation.

It also retains every GM, health and servo-state transition.

The range brackets step timing; polling adds observation latency.

The final two columns report observations without applying #593.

| Cycle | OFF duration | Controller down / up | GM return / PHC step | gPTP recovery | First DUT / peer PDU | Outage media recovery after step | DUT / peer mr changes | DUT MEDIA_RESET sequence |
|---|---|---|---|---|---|---|---|---|
| 1 | 21.09 | 10.74 / 34.94 | 39.99 / 41.02-41.30 | 1.56 | 43.99 / 46.52 | 8.00-8.28 | 2 / 0 | 1 > 2 > 0 > 1 |
| 2 | 20.89 | 1.38 / 34.88 | 39.87 / 39.77-40.05 | 0.68 | 46.77 / 47.55 | 10.25-10.54 | 2 / 0 | 1 > 2 > 0 > 1 |
| 3 | 20.96 | 1.45 / 34.83 | 39.93 / 41.02-41.30 | 1.62 | 45.24 / 45.74 | 7.50-7.78 | 2 / 0 | 1 > 2 > 1 |
| 4 | 20.92 | 1.37 / 34.86 | 41.74 / 42.77-43.05 | 1.81 | 51.18 / 47.83 | 7.50-7.79 | 2 / 0 | 1 > 2 > 1 |
| 5 | 20.90 | 1.38 / 34.87 | 39.92 / 39.77-40.05 | 0.63 | 48.52 / 48.44 | 11.25-11.54 | 2 / 0 | 1 > 2 > 1 |
| 6 | 20.94 | 1.45 / 34.94 | 39.92 / 39.77-40.05 | 0.64 | 52.60 / 48.05 | 10.75-11.04 | 2 / 0 | 1 > 2 > 0 > 1 |
| 7 | 21.05 | 1.48 / 35.06 | 40.11 / 40.02-40.30 | 0.44 | 44.69 / 45.85 | 8.25-8.53 | 2 / 0 | 1 > 2 > 0 > 1 |
| 8 | 21.05 | 1.46 / 35.05 | 40.08 / 40.02-40.30 | 0.47 | 49.00 / 49.88 | 12.25-12.54 | 2 / 0 | 1 > 2 > 1 |
| 9 | 21.02 | 1.37 / 34.89 | 39.99 / 41.02-41.30 | 1.82 | 44.20 / 46.75 | 8.50-8.78 | 2 / 0 | 1 > 2 > 1 |
| 10 | 20.92 | 1.38 / 34.87 | 39.87 / 39.77-40.05 | 0.68 | 45.87 / 46.00 | 8.75-9.04 | 2 / 0 | 1 > 2 > 0 > 1 |

All ten gPTP recoveries passed: 0.44 to 1.82 seconds.

The longest outage media recovery interval was 12.54 seconds.

This elapsed time starts at the measured step bracket.

Every cycle regained both streams and retained both bindings.

Each talker counted one further STREAM_START and one STREAM_STOP.

No cycle approached the 180-second stop deadline.

The largest console sampling gap was 0.251 seconds.

DUT reset epoch remained 1 in every sample.

First valid PDUs followed wire return by 5.07-14.00 seconds.

Those observed restart intervals all exceed one second.

Exact DUT link-up-to-PDU delays remain unmeasured.

## Counter and restart findings

The expected link-counter increments were absent in all ten cycles.

LINK_UP remained 1; LINK_DOWN remained 0.

Their valid-mask bits were present in every successful response.

This confirms the earlier [flat-counter observation](117_GPTP_SILICON_EVIDENCE.md#return-and-recovery).

The [integration source](../../sw/litex/milan_soc.py) explains the status dependency.

MAC_STATUS remains at its unwritten reset value, `0x0d` ([#599](https://github.com/kebag-logic/milan-fpga/issues/599)).

Whatever the PHY did, this status cannot advance LINK_UP/LINK_DOWN.

The counters also depend on the link guard's RX-clock-alive veto.

Neither LINKG_STAT nor LINK_CTRL was sampled.

No PHY-status read established whether the DUT link dropped.

The reference peer's LINK_UP/LINK_DOWN also stayed flat at 1/0.

The build defect is missing publication, not an observed missed edge.

| DUT observation | Per-cycle result |
|---|---|
| AVB_INTERFACE LINK_UP / LINK_DOWN | `+0 / +0`; expected increments absent; publication defect #599 |
| AVB_INTERFACE GPTP_GM_CHANGED | `+2`, selected itself and then the switch |
| CRF STREAM_INPUT MEDIA_LOCKED / MEDIA_UNLOCKED | `+1 / +1` |
| CLOCK_DOMAIN LOCKED / UNLOCKED | `+1 / +1` |
| CRF STREAM_OUTPUT STREAM_START / STREAM_STOP | `+1 / +1` |
| Stream reservation and ACMP binding | Recovered automatically; both bindings retained |

The media servo moved LOCKED, HOLDOVER, ACQUIRE, then LOCKED.

One large PHC discontinuity accompanied each grandmaster return.

The first step was approximately minus 358,781 seconds.

Cycle 2 stepped approximately minus 162.46 seconds.

Cycles 3 to 10 stepped between minus 95.74 and minus 96.47 seconds.

The raw analysis records each measured amount and time bracket.

DUT outgoing `mr` changed at loss and on resumed transmission.

The reference peer's captured `mr` stayed unchanged.

No claim counts unseen toggles during the wire gap.

DUT MEDIA_RESET was observed at 2 after loss.

It returned to 1 after the new STREAM_START.

STREAM_START resets its observation-interval count to zero.

That reset follows the [counter contract](../../hdl/ieee1722/avtp/KL_talker_diag_ctx.sv).

Endpoint subtraction would incorrectly hide those increments.

The table therefore preserves each observed counter sequence.

Polling caught the intermediate zero in five of ten cycles.

The other five do not prove the timing of that reset.

The reference listener also reset counters on reacquisition.

Its raw trajectory records unlock before the reset.

This run reports these restart observations without grading #593.

#387 acceptance 4 remains NOT MET: its condition was not exercised.

A grandmaster change must occur while locked CRF keeps running.

That measurement must observe the step's counted media event.

This run also leaves AAF render timing and waveform continuity unmeasured.

## Restore and validation

All seven outlets were restored ON, matching the starting census.

All eighteen stream states were unbound after both disconnections.

DUT clock source 0, INTERNAL, was restored.

Original configurations, clock sources, rates and descriptors compared equal.

Final UART health was sync 1, asCapable 1 and `tu=0`.

Reset epoch remained 1, and the media servo returned IDLE.

The final 12-second tap capture contained no CRF PDUs.

The bare-metal UART grader passed 10 of 10 checks.

The temporary capture driver was unloaded and its build removed.

Temporary controller files were removed, with no acquisition process remaining.

The bench lock was released and its availability verified.

The required documentation, scope, bare-metal and feature-status gates are recorded in the packet.

No RTL or firmware changed in this lane.

## Artifact hashes

The [public packet archive](https://github.com/kebag-logic/milan-fpga/tree/8f983d245a12e18a47ced37904d405b624c7e024/review-evidence/394-387-r1) contains scripts, transcripts and analyses.

Its branch is `394-387-review-evidence`; its path is `review-evidence/394-387-r1`.

The archive commit is `8f983d245a12e18a47ced37904d405b624c7e024`.

The publisher's [MANIFEST.json](https://github.com/kebag-logic/milan-fpga/blob/8f983d245a12e18a47ced37904d405b624c7e024/review-evidence/394-387-r1/MANIFEST.json) records the published files' SHA-256 values.

Raw captures are retained in private cold storage.

[RAW-ARTIFACTS.json](https://github.com/kebag-logic/milan-fpga/blob/8f983d245a12e18a47ced37904d405b624c7e024/review-evidence/394-387-r1/author/RAW-ARTIFACTS.json) indexes them by size and SHA-256.

The per-cycle `author/cycleNN/raw-artifacts.json` indexes retain the same identifiers.

Their temporary-directory paths are historical names, not current storage locators.

Raw retention follows [TESTING section 6b](../testing/TESTING.md#6b-bench-evidence-retention).

The assigned build and CSR map are identified by hashes.

The initial capture preflight failed before any outlet operation.

The tap was attached but lacked a matching capture driver.

A temporary rebuild restored the same capture interface.

No driver source change, permanent installation or wiring change occurred.

The successful baseline then proved both tapped directions.

| Cycle | Raw artifact | Bytes | SHA-256 |
|---|---|---:|---|
| 1 | `console.jsonl` | 670801 | `9aa7aa7d45d5ee5c56a412b5a94f4abebb12cde5fd8b12ac20eac5479ea315b5` |
| 1 | `controller-wire.pcap` | 156161 | `0daed9832f9db5424b31b20e2f9a2c20a36b0f9c10b7a85146b1fc0bea61c61d` |
| 1 | `tap.pcap` | 5275332 | `a83a8e769dcf0278f80f3738503f9c13a11253b109b80d31952d16d37e39bb31` |
| 1 | `controller.jsonl` | 287595 | `71fc0b42ac7d3212f68fc87201ff2bb1780dd40d61893fa8ee077dab837aa3e1` |
| 1 | `events.jsonl` | 3887 | `e116c2c5caa2fdaf0d9c2fd1602f6281b3d7402f9a42853e1f1dbc37443b7d9f` |
| 2 | `console.jsonl` | 670812 | `ae882b1e0a7b0449f9cca6f1944148b122eb1338a4367a58c5b81e8f2f96eba3` |
| 2 | `controller-wire.pcap` | 159731 | `946cda842af10b1354e795f21d120a6ad00d749afd8ec262510cf26e992f64a0` |
| 2 | `tap.pcap` | 5074088 | `7c92949fef1f06b8b83c46d99c58706a9b44ec2d48575dfa54c7aca100589b84` |
| 2 | `controller.jsonl` | 286355 | `54c0db499f631f4bd1eaebb25fd05fb1a87c1da768525e7b8d222f5819269868` |
| 2 | `events.jsonl` | 3881 | `5302c99e4407c057dd787543a78ceb9efcbff85309864c71ea64f72e5d511cd1` |
| 3 | `console.jsonl` | 670807 | `82b714f1645906184dd05ae4f546b785ffd65c5f59d0448001f257314ae7b8d9` |
| 3 | `controller-wire.pcap` | 159583 | `7201ea8ff2c3c80c4e301aea2c9d3140d47b1fa710340358b9a4c1012e2abe9f` |
| 3 | `tap.pcap` | 5277766 | `9ae8fa4f84afe9da7afbca6466d66b106263669b8b96eae1f7d684ba4c6487fa` |
| 3 | `controller.jsonl` | 286921 | `ddcdd37e88ba61629366b771a336294bb14d4a6ed7940ca1c837c9d9d44a23bb` |
| 3 | `events.jsonl` | 3881 | `6e3f1ae124361405ad2c8afa68117f32aa54a1e14ebc4bbbc15cc26dbe254b68` |
| 4 | `console.jsonl` | 670686 | `2b71e7f8e5212d1c7cb3b9854cd74c09c0fdaae2929ed61058adaa4ad7eee205` |
| 4 | `controller-wire.pcap` | 153956 | `8c098f56730eb85f72d672035f8c3e0c60bb12626ad4afcfa8ab78c55e065aad` |
| 4 | `tap.pcap` | 4795536 | `8dda4b70e7959c3f410ca5696be2117aa4dc1c1868f26a4bc241d1e714d866a4` |
| 4 | `controller.jsonl` | 275660 | `006b3aa5135b79b993f55153cc029b0c0abc1e7fbed5237939edd3204b3d0677` |
| 4 | `events.jsonl` | 3883 | `9a9dda69954ba3095168452b48ea48243abbd761195e98c236b5eed43ab82978` |
| 5 | `console.jsonl` | 671084 | `aef70b9c668bcf39728058f24c0f62093898c27bd58c42ed18990b1a3d4cda91` |
| 5 | `controller-wire.pcap` | 159450 | `f84c7074fcc2f28167888740f5b3facdbbbbdd4ba1f2ed1997be95ccf097fbef` |
| 5 | `tap.pcap` | 4946420 | `63439e6cca40d5a2772f54410d8016eb0747138b08bd3cbc8c9ea5bf3bdbd9b6` |
| 5 | `controller.jsonl` | 287006 | `d71a5aaa5f40aec3993449b5176c60fc73b1a2798c8dac8d51c8d69f193cec74` |
| 5 | `events.jsonl` | 3888 | `cf21b4ba4e374f80ef6258137130ef82870472bc790d5176226059e2b27b23b0` |
| 6 | `console.jsonl` | 671152 | `5dc23a4e560ec9ff48feeb5018c656a87409a997c56fb7a3aa8efcccb98cbaf0` |
| 6 | `controller-wire.pcap` | 159604 | `82b0b03712ab2406c0258b8bc1bbd997bde08bee9d5613566aa49fa3182a4ce7` |
| 6 | `tap.pcap` | 4733247 | `f65263b93898c4d983058f7cf3d5aa90960bc99df9884559a51abdb95c1f21b3` |
| 6 | `controller.jsonl` | 287306 | `625efc8f8731d1178a30ff45ad41aecdb945e1f7a45df2d8caa32f59a87d2912` |
| 6 | `events.jsonl` | 3891 | `e4fa91e2906d185bdbe221a70a326e1e76c31d3760b28612709f981d0a869905` |
| 7 | `console.jsonl` | 671178 | `389ed2744e8e25e60d2e962e8ac9aca54524dc0e2be041470cb9a207749b183f` |
| 7 | `controller-wire.pcap` | 156739 | `6b227866f66673adf2f1eba40c72f56f96cad35e40f1e17ddadd8d76299a4a67` |
| 7 | `tap.pcap` | 5287813 | `1af2faf1a481c11f8f24419eec8696741a5f07b942048211b3089054b462e307` |
| 7 | `controller.jsonl` | 281106 | `66eb71c6eff6b2f49f3e9475c74015a91411de21322de1a388344c86421b8b5e` |
| 7 | `events.jsonl` | 3892 | `ad4580f7be418269465dcb858f54c4812467feb830567f591673b55fc8613487` |
| 8 | `console.jsonl` | 670881 | `48966b8361b954bd2f8caadbbf4c21c2c140e4982aa14fe1272b689fce33be54` |
| 8 | `controller-wire.pcap` | 157000 | `64763dddacf5a5db665793d053dd3f34dae94caf920c9aa0e575364888c3214d` |
| 8 | `tap.pcap` | 4830829 | `86ab2e1eb67bd9a0c337996ba72aae6932c8d1b051a93515b467ef662d32fe25` |
| 8 | `controller.jsonl` | 281128 | `797fb5e349cde1aa9e92c382b68ef201b7de771e83b80d370da4f7bd4d22cb81` |
| 8 | `events.jsonl` | 3882 | `a107ec7d3e47398a3d9c8022a69c23e7794e8ffe93f50a173e34d4ce8ea895d6` |
| 9 | `console.jsonl` | 670764 | `9949305e413a6a6dd081ea5d312f6e180c31df3214b34fb2c97d82e23ebbced6` |
| 9 | `controller-wire.pcap` | 159414 | `97a1b752df834c3d6619dce072fae54cc9696fcd36c38d059c409fb519b2ebba` |
| 9 | `tap.pcap` | 5278580 | `812fe41ae2315b48ff3d5dc9954e33053c9dfb9c12534caf94a01e5ba3fed4fb` |
| 9 | `controller.jsonl` | 287169 | `10998e5de9e183270526b974bc172602bbea37f75d9248e859235c1c73f3f7bb` |
| 9 | `events.jsonl` | 3886 | `85e83423b1e1dbdfd90693a1d8b995fb12dda7dad7d1474ddc94eb09977ac42f` |
| 10 | `console.jsonl` | 670780 | `7b810d605e9ac2359a0176a640429f537f817d6679ffbcae34d919fb1d45549b` |
| 10 | `controller-wire.pcap` | 159431 | `f57b8046d6ddc81e098fbae90d2244b150624825c5a0e568d87da3609fed8b61` |
| 10 | `tap.pcap` | 5196824 | `9a7eabdf2cad2feac2ec4ef714a64fad0104fc81304e3ae8e67a3ef4ce4c85e4` |
| 10 | `controller.jsonl` | 287092 | `c060963359fe7b291b053b8ba3f73b1c3787b479deb221880cbd43a7ba9cc0a9` |
| 10 | `events.jsonl` | 3887 | `f92f5e90aa425e015f90c83dc9a4bb47fb535299075a16f29bf845bf7fd90116` |
