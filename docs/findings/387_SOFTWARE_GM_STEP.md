<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# Software grandmaster steps on a running CRF stream

Refs #387. Operator [A438], measured 2026-09-29, under the
[bench assignment](https://github.com/kebag-logic/milan-fpga/issues/599#issuecomment-5884216527)
and the [owner decision of 2026-09-28](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5862731997).

| Acceptance | Verdict | Evidence |
|---|---|---|
| #387 acceptance 4 | PASS, with one recorded deviation | Five takeovers and five releases gave ten PHC steps of +9.99 ms and -10.00 ms on a running, locked CRF stream. No outgoing `mr` changed. MEDIA_RESET stayed flat, and neither listener unlocked. `A_MCSRV_STAT` read LOCKED throughout, and `tu` signalled every step. The DUT was steady again 3.00-4.53 s after each step, inside the 5 s bound. Deviation: every step was followed by a 2.0 s asCapable loss. See [Deviation](#deviation-ascapable-loss-after-every-step). |

These are operator measurements, not review verdicts.

The [switch-cycle page](599_394_E1_LINK_CYCLES.md) records the same session's link cycles and identity.

## Contents

- **[Stimulus](#stimulus)** -- The software grandmaster, its offset, and one run's sequence.
- **[Method and limits](#method-and-limits)** -- How steps, `tu`, `mr` and counters were observed.
- **[Per-step results](#per-step-results)** -- The ten steps, their sign, and the media reaction.
- **[Contract check](#contract-check)** -- Each decided reaction against what the bench showed.
- **[Deviation: asCapable loss after every step](#deviation-ascapable-loss-after-every-step)** -- The one behaviour outside the contract.
- **[Other observations](#other-observations)** -- Counters and peer behaviour recorded without a verdict.
- **[Restore](#restore)** -- The original grandmaster, streams and controller host restored.
- **[Artifact hashes](#artifact-hashes)** -- Tool, configuration and raw-capture identities.

## Stimulus

The image, identity gate and CRF bindings are those of the [switch-cycle page](599_394_E1_LINK_CYCLES.md#identity-and-setup).

CRF was bound both ways, and the DUT selected the CRF input as its clock source.

Both streams were locked and running at 500 PDU/s before every run.

The controller host sits on another port of the bench AVB switch.

Its AVB NIC has a hardware clock and hardware timestamps.

The software grandmaster is the open-source reference gPTP implementation, release 4.4.

It was built in a temporary directory from a hash-checked source tarball.

No package was installed.

The host's crypto library no longer matches that release's optional authentication backend.

A make-variable override built it without authentication, which the gPTP profile does not use.

Each run had four phases:

1. **Align.** A gPTP port that is never grandmaster aligned the host's hardware clock with the switch.
2. **Offset.** That clock was then advanced by 10 ms, 100 times the 100 us locked step threshold.
3. **Takeover.** A second instance announced priority1 240 against the switch's 246, for 50 s.
4. **Release.** It stopped; the switch timed it out and became grandmaster again.

The aligning port uses `gmCapable 0`, which forces clockClass 255.

In the aligning phase, the port converged to at most 10 ns in every run.

For about 2 s before the switch's Announce, that port held a clockClass-255 master role.

A standalone test confirmed that this role changed no grandmaster.

The DUT's and peer's GPTP_GM_CHANGED stayed at 22 and 60.

The grandmaster configuration used a free-running clock with the gPTP profile's intervals.

The switch forwarded the new grandmaster to the DUT with stepsRemoved 1.

The takeover therefore steps the DUT forward; the release steps it back.

Five runs gave ten steps, five of each sign.

## Method and limits

All times are seconds after that run's software-grandmaster start.

**Console.** Every 250 ms the console read these values:

- `milan_status`: GM, sync, asCapable, `tu`, `CLKV_STAT` and the PHC.
- MAC_STATUS, `LINKG_STAT`, `RST_EPOCH`, `CLKV_TUCNT` and `A_MCSRV_STAT`.
- `CRFT_CTRL` and `CRFT_COUNT`.

**Step detection, console.** A step is a change in PHC minus host time between samples.

The measured noise was plus or minus 0.11 ms, so the threshold is 0.5 ms.

**Step detection, wire.** The DUT's Pdelay responses carry its PHC time of the switch's request.

Set against the request's tap time, they give the DUT PHC once a second.

**Grandmaster time.** Sync and Follow_Up forwarded to the DUT gave the time step on the wire.

**Media.** The tap decoded `tu` and `mr` on every CRF PDU in both directions.

**Counters.** The controller read GET_COUNTERS and both ACMP states every second.

**Steady.** "Step to steady" runs from the console step bracket to the steady `tu` clear.

That clear is the first sample from which sync 1, asCapable 1 and `tu=0` hold for two seconds.

**Limits.** No AAF stream was bound.

The render stage's re-base tally has no CSR, so the counted render re-base was not observable.

One console sample in run 4 came back 2.7 ms late, at 97.8 s.

The detector flagged a cancelling pair there; no wire jump, `tu` or holdover accompanied it.

It is a console timing artifact, not a step.

## Per-step results

Takeover steps land 3.4-4.1 s after the start, release steps 50.3-50.9 s.

The DUT PHC step comes from the wire; the console agrees within 0.07 ms.

"`tu` episodes" counts rises of `tu` on the DUT's outgoing CRF within the edge.

| Run | Edge | DUT PHC step | Grandmaster time step | `tu` set / steady clear | Step to steady | `tu` episodes | asCapable lost | DUT / peer `mr` changes | MEDIA_RESET talker / listener | DUT / peer MEDIA_UNLOCKED | Servo state; discards |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | takeover | +9.988 ms | +9.994 ms | 4.05 / 7.34 | 3.25-3.54 | 3 | 4.55-6.55 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 10 to 13 |
| 1 | release | -10.004 ms | -9.997 ms | 50.82 / 54.10 | 3.25-3.53 | 3 | 51.57-53.57 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 13 to 14 |
| 2 | takeover | +9.988 ms | +9.995 ms | 3.78 / 7.06 | 3.25-3.53 | 2 | 4.28-6.28 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 14 to 17 |
| 2 | release | -10.005 ms | -9.998 ms | 50.55 / 54.08 | 3.50-3.78 | 3 | 51.30-53.30 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 17 to 19 |
| 3 | takeover | +9.988 ms | +9.995 ms | 3.78 / 8.06 | 4.25-4.53 | 3 | 4.78-6.78 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 19 to 20 |
| 3 | release | -10.004 ms | -9.996 ms | 50.59 / 54.12 | 3.50-3.78 | 3 | 50.84-52.84 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 20 to 21 |
| 4 | takeover | +9.987 ms | +9.995 ms | 3.78 / 6.81 | 3.00-3.28 | 2 | 4.53-6.53 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 21 to 24 |
| 4 | release | -10.004 ms | -9.997 ms | 50.80 / 53.83 | 3.00-3.28 | 3 | 51.55-53.55 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 24 to 25 |
| 5 | takeover | +9.987 ms | +9.995 ms | 3.78 / 7.07 | 3.25-3.54 | 3 | 4.03-6.03 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 25 to 26 |
| 5 | release | -10.003 ms | -9.996 ms | 50.60 / 54.14 | 3.50-3.78 | 3 | 51.11-53.11 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 26 to 27 |

- Every takeover stepped the DUT PHC forward by 9.987-9.988 ms.
- Every release stepped it back by 10.003-10.005 ms.
- The forwarded grandmaster time moved by +9.994 to +9.995 ms and -9.996 to -9.998 ms.
- `tu` rose in the console sample that first showed the step.
- On the wire, the DUT's first `tu=1` PDU followed the new grandmaster's first Announce within 2 ms.
- In eight edges `tu` first cleared 0.5-0.75 s after rising, then rose again with the asCapable loss.
- In the other two, run 3's release and run 5's takeover, asCapable was lost before `tu` cleared.
- The DUT was steady again 3.00-4.53 s after each step.
- That is inside the 5 s [recovery bound](../design/GM_LOSS_RECOVERY.md#recovery-bound), which is context, not #387's bound.
- The DUT's media servo read LOCKED in every sample.
- Both CRF streams ran throughout: the largest gap in either direction was 2 ms.
- The CRF talker's licence, `CRFT_CTRL` `0x3002e3`, never dropped.

Per run, over both edges:

| Run | Takeover Announce | Release Announce | `CLKV_TUCNT` | DUT GPTP_GM_CHANGED | CLOCK_DOMAIN LOCKED / UNLOCKED | DUT listener TIMESTAMP_UNCERTAIN / LATE / EARLY | `tu=1` PDUs, DUT / peer | Largest CRF gap |
|---|---|---|---|---|---|---|---|---|
| 1 | 3.89 | 50.55 | 461 to 469 | +6 | +6 / +6 | +2 / +1 / +1 | 2685 / 94 | 2 ms |
| 2 | 3.41 | 50.44 | 469 to 477 | +6 | +5 / +5 | +1 / +1 / +0 | 2569 / 39 | 2 ms |
| 3 | 3.49 | 50.52 | 477 to 486 | +6 | +6 / +6 | +2 / +0 / +0 | 2617 / 88 | 2 ms |
| 4 | 3.50 | 50.52 | 486 to 494 | +4 | +5 / +5 | +2 / +0 / +0 | 2425 / 74 | 2 ms |
| 5 | 3.61 | 50.53 | 494 to 504 | +6 | +6 / +6 | +3 / +0 / +0 | 2630 / 91 | 2 ms |

## Contract check

The contract is [media re-base on a PHC step](../design/GM_LOSS_RECOVERY.md#media-re-base-on-a-phc-step).

The [#602 ruling](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859297355) amends it.

The [step policy](../design/TIME_SYNC.md#step-policy) sets the thresholds.

| Element | Decided reaction to one step | Observed over ten steps |
|---|---|---|
| Step policy | Locked servo steps above 100 us; a GM change keeps it locked | Each 10 ms offset stepped once; no second step followed the asCapable return |
| `tu` | Rises on the step; clears after at least 0.25 s of holdover | Rose with the step; in eight edges first cleared 0.5-0.75 s later; rose again with the asCapable loss (deviation) |
| Outgoing `mr` | Unchanged for a PHC-only step | Unchanged: 0 changes on the DUT output and 0 on the peer output |
| Talker MEDIA_RESET | No step-only increment | +0 at every step |
| Listener MEDIA_LOCKED / MEDIA_UNLOCKED | Licensed stream keeps streaming (REQ-PTP-08) | +0 / +0 on the DUT and on the peer: neither listener unlocked |
| CRF servo | Keeps its window guard; discards the step window (#539) | LOCKED in every sample; 1 to 3 discarded windows per step |
| Render re-base | One counted re-base per step | Not observable on this bench: no AAF stream and no tally CSR |
| Step to relocked media | No time bound in item 2 ([#387](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5859048589)) | Media never unlocked; the DUT was steady 3.00-4.53 s after the step |

## Deviation: asCapable loss after every step

After every step the DUT cleared asCapable 0.22-0.97 s later, for 2.0 s each time.

Sync dropped with it and `tu` rose again.

When asCapable returned, the DUT re-adopted the grandmaster with a further holdover.

That gives two or three `tu` episodes per step instead of one.

In the sample where asCapable cleared, the DUT's published peer delay read this:

- 0 ns at all five takeovers;
- 4,039-4,701 ns at all five releases;
- 373-389 ns everywhere else.

That fits a peer-delay exchange computed across the step.

This page does not establish that mechanism.

Media stayed locked, and no `mr` or MEDIA_RESET followed.

The loss still extends each step's `tu` from about 0.5 s to 3.0-4.5 s.

It also adds GPTP_GM_CHANGED and CLOCK_DOMAIN counts.

Item 2 does not grade it.

It is proposed as a follow-up issue for the manager: a PHC step should not cost asCapable.

## Other observations

These are recorded without a verdict.

- DUT GPTP_GM_CHANGED rose by 3 at nine edges and by 1 at one.
- The GM changed once per edge; the extra counts coincide with the asCapable loss and return.
- DUT CLOCK_DOMAIN LOCKED and UNLOCKED rose by 2 or 3 each per edge, following the `tu` episodes.
- The DUT listener counted TIMESTAMP_UNCERTAIN +1 to +3 per run, LATE twice and EARLY once over ten steps.
- The peer's CRF talker set `tu=1` on 0 to 63 PDUs per edge, at most 0.13 s at 500 PDU/s.
- The peer's listener counted TIMESTAMP_UNCERTAIN exactly equal to the DUT's `tu=1` PDUs on the wire.
- `CLKV_TUCNT` rose by 8 to 10 per run.

## Restore

Each run ended with the switch as grandmaster again.

The last run's release restored the original grandmaster, `3cc0c6fffefe0210`.

The console, the wire Announce and the controller's GET_AVB_INFO all name it.

Streams and bench were restored as the [switch-cycle page](599_394_E1_LINK_CYCLES.md#restore-and-validation) records.

The controller host was returned to its found state:

- No gPTP daemon runs, before or after.
- NIC timestamping reads tx 1, rx 1, as found.
- The hardware clock's frequency offset is back to 28,062.35 ppb, read 28,062.33 ppb.
- Its time is back on its original trajectory against the host clock, within 4.4 us.
- The temporary build, configurations and scripts were removed.

One difference remains.

Two stale control-socket files from an earlier run of the same implementation predated this lane.

The implementation removed them at its first start; no daemon was listening on them.

They were not recreated.

## Artifact hashes

The bench packet and index files are as on the [switch-cycle page](599_394_E1_LINK_CYCLES.md#artifact-hashes).

| Item | SHA-256 |
|---|---|
| Reference gPTP implementation 4.4, source tarball, 277,069 bytes | `61757bc0a58d789b8fcbdddf56c88a0230597184a70dcb2ac05b4c6b619f7d5c` |
| Its gPTP port program as built | `25247f3a744532f02e84638915c14922a19c8da8add52c81f5e88e3418dae7bd` |
| Its clock-control program (`phc_ctl`) as built | `ea44d7799a0f7b4dc6a9d3c50f1edf146f98a2efe6053255290f0bfcdc4a002d` |
| Grandmaster configuration | `f798c63330ef976c16dbf4b8a26242d684eb897ff2c98f61b56d8faa42b50413` |
| Alignment configuration | `f1e59efb5843a288a102b6a9bc6f492a2b33e32ca6deea555a817e7cd049948c` |
| `b1_action.py`, acquisition | `dd6d6ec73c2160064d37ace96b789aa2108eb81f4ee75705119594ce9def360c` |
| `b1_analyze.py`, analysis | `e4f7681891e1ed76fc3916a4395f82a6abf5c55a66c40fd4c065cfb019e429e0` |
| `b1_summary.py`, tables | `7c388bb385c9fb417d89c85c14387231c14ba38bf54a1dc4d38b99c84f5089e6` |
| `phc_restore.py`, controller clock restore | `442c0185630b2fa0606d9eb5f805d5171a9b427429f5adbbf510f031a451d231` |

The two port logs are named by role; the packet's per-run index matches them by hash.

| Action | Raw artifact | Bytes | SHA-256 |
|---|---|---:|---|
| gm01 | `console.jsonl` | 1124688 | `f72e7065b6f5a363d2a20d6258679463341ebd7343b6d9177c3188f9d6551ed2` |
| gm01 | `controller.jsonl` | 639590 | `f252de61752452c992829302d352cc8592d6650545113b9a5fc2e41740e69f9f` |
| gm01 | `controller-wire.pcap` | 459526 | `77de6b4ed15dcb48be985dea76476c8c6696ddb8dd215b3e81b6e3912d17c1ca` |
| gm01 | `tap.pcap` | 13625805 | `9a85c4b61f6a21f8f7239f4960088e3273d70f3a1ff08f47d8ef24c286218a64` |
| gm01 | `events.jsonl` | 4122 | `537d187739b2fce75f7478c6194fb37be79ee548abdae4e18a203ae1f8f87bb9` |
| gm01 | alignment port log | 3448 | `880fdb8d204b61b899294363b8cc6e09379c9bd5d62a4bb8e3bfcd90a1eb456e` |
| gm01 | grandmaster port log | 479 | `1aef82ba0ca494f70c96a6710271f21ad2967a47362fa2409915ce9fa96d837e` |
| gm02 | `console.jsonl` | 1124293 | `9ee376fafce7b093324dfe3d1632d4c9fd62291410940028947785692b019065` |
| gm02 | `controller.jsonl` | 639591 | `b7134efdda62576ba5294ccb291bd01b1246166bd0a3326fc89630dc2db6b7ec` |
| gm02 | `controller-wire.pcap` | 461331 | `9abe94d91ad0113807da88849a990fc3298807a627cf3cc0ae556aa8c8970cfe` |
| gm02 | `tap.pcap` | 13619719 | `fbb55efea84122a31325698595045b58cf2309d1b8b2c49661e1ced3a3210642` |
| gm02 | `events.jsonl` | 4120 | `e8ebad60b8eb0c86c14c6c4938e5a9ad00fc9a23a26942cc9e03e2ac59909126` |
| gm02 | alignment port log | 3456 | `a4872aa922897a7113bad409757257de0db0ef3abf6243ea46b1be104333c873` |
| gm02 | grandmaster port log | 479 | `db7adce82609d24de2612c11f79168bf683d42c6af8a77d4eb350f115af3c61c` |
| gm03 | `console.jsonl` | 1124314 | `bbcc51d0f77f4a79946c858ffe1c64c05b6e470da42336bcff9ea7334edd093f` |
| gm03 | `controller.jsonl` | 639595 | `8a602368bc8d5fe367d365c066b76bfe7647f1ff36a8a469af64045b24fad416` |
| gm03 | `controller-wire.pcap` | 461864 | `5e1d6020f10f05450a1672a008213322b88fa40f1abf1fbc61b780af6f96fcf2` |
| gm03 | `tap.pcap` | 13625642 | `c27b4e7eb119e3bc1eedc17d5c7708b986db9778b01fa0ded209089e01882c59` |
| gm03 | `events.jsonl` | 4117 | `9c05be2ba65a213c8dae22c2ae4e40a1a6db9528f987242d877fb2be4689b6e5` |
| gm03 | alignment port log | 3455 | `8771d269dbaf77d532007c9fb8ca23d5debdb1a0a3d9cc21fec5b19075f1120e` |
| gm03 | grandmaster port log | 479 | `be71fc54bafcd6acc2f172c2ba799d348e93920e427845639eadbc101c4fc32f` |
| gm04 | `console.jsonl` | 1124629 | `e2e1914554e0dbd8bb9dac97d3257709ea62d5d546870ba53de315bea8d803a6` |
| gm04 | `controller.jsonl` | 640655 | `281e445fbdee2f89bd3924c3947d3ab1712179704f2786c5a12b69413cac097d` |
| gm04 | `controller-wire.pcap` | 469859 | `33751c9cdc0c6161dafa7d1a060fc81a108659dfaa2f5d0dd939ee2453a637d5` |
| gm04 | `tap.pcap` | 13630825 | `747248b7c98ec0ea49b0e408ceb37bb4d10c6ce8c28e0e31d61b31c7b88d9a22` |
| gm04 | `events.jsonl` | 4115 | `7bff01660d336620fc162bcf02f2cd98cf18eac94e9fd2909efb55b71ae44ec5` |
| gm04 | alignment port log | 3455 | `23ff472a8a031be3484731b848d6dfeab6239c444e39ba8109f490eac7cc7873` |
| gm04 | grandmaster port log | 479 | `69cf477bca78bf606adf5a4239658fabce48e6266a6ed3c22c1d68a9db102970` |
| gm05 | `console.jsonl` | 1124327 | `04efafe2c570666386ecfe2f8afd34e4c855dd0e00c62878d6b231651b15bf7b` |
| gm05 | `controller.jsonl` | 641526 | `988fb3a7a589f0153c857e8958febb2e5125b53f3b029c35b4d0b0d10c571670` |
| gm05 | `controller-wire.pcap` | 463422 | `f7bc4660584866629e59987febf6606129b8b520e0ecbb5a06c7f952cc3f1bf0` |
| gm05 | `tap.pcap` | 13620466 | `444488b1b1f0b9293bbd544860cc66feef0d5e53172b1b861428d7f48f99c060` |
| gm05 | `events.jsonl` | 4121 | `bdfbfbfef6b47670c31e6102efbf78b944dc23c30f150357ead05c2cfcc03a60` |
| gm05 | alignment port log | 3455 | `e8eddea557e3fb3572922a324286ca17db160b146f074a414e4e2341e1e4bd46` |
| gm05 | grandmaster port log | 553 | `2de4be8f78691f3727c1ee89ac37979a338e03f713d575ae910e1c7e0fd4a870` |
