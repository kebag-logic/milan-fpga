<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# Software grandmaster steps on a running CRF stream

Refs #387. Operator [A438], measured 2026-09-29, under the
[bench assignment](https://github.com/kebag-logic/milan-fpga/issues/599#issuecomment-5884216527)
and the [owner decision of 2026-09-28](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5862731997).

| Acceptance | Verdict | Evidence |
|---|---|---|
| #387 acceptance 4 | PARTLY MET | Met: five takeovers and five releases gave ten PHC steps of +9.99 ms and -10.00 ms on a running, locked CRF stream. No outgoing `mr` changed. MEDIA_RESET stayed flat, and neither listener unlocked. `A_MCSRV_STAT` read LOCKED throughout. Not met: the decided one counted event per step. `tu` was signalled 2-3 times per step instead of once. asCapable was lost for 2.0 s after every step ([#621](https://github.com/kebag-logic/milan-fpga/issues/621)). DUT GPTP_GM_CHANGED rose by 3 at nine of ten edges, against one grandmaster change. Not observable on this bench: the counted render re-base, because no AAF stream was bound and its count has no register. Item 2 sets no time bound; the DUT was steady again 3.00-4.53 s after each step. See [Deviation](#deviation-from-the-one-counted-event-contract). |

These are operator measurements, not review verdicts.

The [switch-cycle page](599_394_E1_LINK_CYCLES.md) records the same session's link cycles and identity.

## Contents

- **[Stimulus](#stimulus)** -- The software grandmaster, its offset, and one run's sequence.
- **[Method and limits](#method-and-limits)** -- How steps, `tu`, `mr` and counters were observed.
- **[Per-step results](#per-step-results)** -- The ten steps, their sign, and the media reaction.
- **[Contract check](#contract-check)** -- Each decided reaction against what the bench showed.
- **[Deviation from the one-counted-event contract](#deviation-from-the-one-counted-event-contract)** -- The asCapable loss after every step, which turns one counted `tu` event into two or three.
- **[Other observations](#other-observations)** -- Counters and peer behaviour recorded without a verdict.
- **[Restore](#restore)** -- The original grandmaster, streams and controller host restored, and the DUT's saved-state residue.
- **[Artifact hashes](#artifact-hashes)** -- Tool, configuration and raw-capture identities, and where the raw captures are kept.
- **[2026-10-16: bench lane B19 on dev 9ef71772](#2026-10-16-bench-lane-b19-on-dev-9ef71772)** -- The same recipe on the image with the #621 correction: ten steps on a locked CRF stream, each with one `tu` event and no asCapable loss.

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

The packet's `extract_alignment_counters.py` reproduces both from the hashed controller transcripts before and after the test.

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

Two things would make it observable on a bench.

- An AAF stream bound into the DUT's render stage and running across each step.
- The stage's recentre count published on a register or console command.

Today that count is a [verification tap](../reference/REGISTER_MAP.md#0x8dc-----render-setpoint-state) that only simulation reads.

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

Item 2 decides one counted `tu` event per step; the #602 ruling removes only its `mr` and MEDIA_RESET parts.

Each step here gave two or three `tu` episodes, and the render re-base was not observable.

So #387 acceptance 4 is PARTLY MET: the media-plane reactions are met, and the single counted event is not.

"Media" in the last row means the listeners' MEDIA_LOCKED state and the CRF servo.

The DUT's CLOCK_DOMAIN counters follow `tu`, and they did count UNLOCKED with each `tu` episode (see [Other observations](#other-observations)).

## Deviation from the one-counted-event contract

The decided contract is one counted event per step.

Every one of the ten steps departed from it.

After every step the DUT cleared asCapable 0.22-0.97 s later, for 2.0 s each time.

Sync dropped with it and `tu` rose again.

When asCapable returned, the DUT re-adopted the grandmaster with a further holdover.

That gives two or three `tu` episodes per step instead of one counted event.

DUT GPTP_GM_CHANGED rose by 3 at nine of ten edges and by 1 at the tenth, against one grandmaster change per edge.

In the sample where asCapable cleared, the DUT's published peer delay read this:

- 0 ns at all five takeovers;
- 4,039-4,701 ns at all five releases;
- 373-389 ns in every other sample of the five runs.

The 0 ns and 4,039-4,701 ns readings each held for four or five samples, about 1 s.

The packet's `extract_pdelay.py` reproduces these values from the hashed console captures.

That fits a peer-delay exchange computed across the step.

This page does not establish that mechanism.

Media stayed locked, and no `mr` or MEDIA_RESET followed.

The loss still extends each step's `tu` from about 0.5 s to 3.0-4.5 s.

It also adds GPTP_GM_CHANGED and CLOCK_DOMAIN counts.

The asCapable loss is [#621](https://github.com/kebag-logic/milan-fpga/issues/621): a PHC step should not cost asCapable.

This lane records it and does not fix it.

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

Two differences remain.

**The DUT's saved-state layer** did not end as found:

| Saved-state field | Identity gate, 05:31Z | Final restore, 06:22Z |
|---|---|---|
| NVM slots A / B, image sequence | 227 / 228, image 228 | 229 / 230, image 230 |
| Commits ok / failed | 0 / 0 | 2 / 0 |
| `PP_STAT`, `nvm_pend` (bit 11) | `0x5b000444`, 0 | `0x5b000c44`, 1 |
| `PP_NVM_STAT` | `0xc30000e4`, pend 0 | `0xc34000e4`, pend 1 |

The setup bound the DUT listener and selected the CRF input as clock source.

The restore selected INTERNAL again and unbound it.

Only the binding records have a writer, so each binding change committed one image: the bind 229, the unbind 230.

The clock-source writes have no record writer.

They set a sticky pending source that only a reset clears.

The [switch-cycle page](599_394_E1_LINK_CYCLES.md#saved-state-layer) derives this from the captures.

The persisted records were not read back or compared with the found state.

The pending flag cannot be cleared without a DUT reset, which this lane may not perform.

**Two stale control-socket files** from an earlier run of the same implementation predated this lane.

The implementation removed them at its first start; no daemon was listening on them.

They were not recreated.

## Artifact hashes

The bench packet and index files are as on the [switch-cycle page](599_394_E1_LINK_CYCLES.md#artifact-hashes).

The public packet is on branch `b1-review-evidence` under `review-evidence/b1-r1/author-r2/`; PR #620 records its pinned commit.

Raw captures are retained in private cold storage, keyed by the SHA-256 values in the table below.

The packet's retention manifest matches every retained copy to its row.

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

## 2026-10-16: bench lane B19 on dev `9ef71772`

Refs #387, Refs #621 and Refs #117. Operator [A624], measured 2026-10-16
between 04:10 and 04:31 UTC, under the
[B19 assignment](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-6207451080)
(item 5). These are operator measurements, not review verdicts.

The image is dev `9ef717727e6fdac11ee7f01672fefae948452343`, the one
installed on 2026-10-15. It carries PR #707, the #621 correction: a phase
step invalidates rate history and keeps the last valid link delay. The
identity gate, the switch cycles and the rest of the session are in the
[#117 findings](117_GPTP_SILICON_EVIDENCE.md#2026-10-16-bench-lane-b19-on-dev-9ef71772).
No read on the device distinguishes this image from dev `5603c353`, so its
identity rests on the
[provenance record](https://github.com/kebag-logic/milan-fpga/tree/bbc53aabb02a1654812ba2eaa1642f5e36e69ce0/review-evidence/645-b18-r1/manager-provenance)
(bitstream SHA-256 `4b5a391af524cb3b490099381c0fd9e3275383fc51c163a75fb78cdb054ffcca`,
AEM descriptor SHA-256 `4fc8d61582a965fe648abc0c15d0551153ff2b27f202d1fbc8319fbb4bdb396d`).
Its continuity to this session is the
[manager's receipt](https://github.com/kebag-logic/milan-fpga/pull/751#issuecomment-6208623939)
(item 8), as the [#117 image paragraph](117_GPTP_SILICON_EVIDENCE.md#b19-image-identity-and-setup) states.
Everything above this section is the dated record of dev `13eda870`.

| Acceptance | Verdict | Evidence |
|---|---|---|
| #621 item 3: five grandmaster steps with no asCapable loss | PASS | Five takeovers and five releases stepped the DUT PHC by +9.987 ms and -10.003 to -10.005 ms. asCapable never cleared: 0 of 2,399 console samples and 0 of 600 answered controller polls of the DUT, both arms of the grade. The published peer delay stayed 373 to 392 ns, in `PDELAY_NS` and in GET_AVB_INFO alike. The packet's `r2_gm.py` derives each figure from the hashed raws. |
| #387 item 4, the wire and counter observables | PASS | Each of the ten edges gave one `tu` episode on the console and on the DUT's CRF PDUs. GPTP_GM_CHANGED rose by exactly 1. The outgoing `mr` never changed, the talkers' and the peer's CRF listener's MEDIA_RESET stayed flat, and no listener counted MEDIA_UNLOCKED. |
| #387 item 4, the counted render re-base | Not graded here | By the [assignment's decision](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-6207451080) the re-base count has no register, so the `milan_dp_gm_steps` simulation carries it. |

Against the 2026-09-29 run on dev `13eda870`, the 2.0 s asCapable loss after
every step is gone. So are the second and third `tu` episodes and the
GPTP_GM_CHANGED count of 3 per edge.

### B19: stimulus and setup

- **Recipe.** Lane B1's, as [Stimulus](#stimulus) describes, with the same configurations (hashes below). The open-source reference gPTP implementation, release 4.4, was built in a temporary directory on the controller host from the same hash-checked tarball, without its optional authentication backends. Its port and clock-control programs came out byte-identical to lane B1's.
- **Each run.** A never-grandmaster port (`gmCapable 0`) aligned the host's hardware clock with the switch for 40 s; it converged to at most 7 ns in every run. Then that clock was advanced by 10 ms, 100 times the 100 us locked step threshold. A grandmaster instance with priority1 240 against the switch's 246 announced for 50 s, and then stopped; the switch timed it out and became grandmaster again.
- **Streams.** The as-found bindings ran throughout. The DUT's CRF Stream Output 1 fed the peer's CRF Stream Input 8, locked, and that input is the peer's selected clock source. Both music AAF streams ran too: the DUT's Stream Input 0 from the peer, and the peer's Stream Input 0 from the DUT. The DUT stayed on INTERNAL.
- **Deviation from lane B1.** Lane B1 also bound the peer's CRF output to the DUT and selected it as the DUT's clock source. Here the peer already follows the DUT's CRF, so that binding with that selection would close a media-clock loop, and it was not made. The DUT's CRF servo therefore stayed IDLE (`MCSRV_STAT` state 0, no discards); the assignment's grades do not include it.
- **Controller host.** Found, 04:10:25 UTC: no gPTP daemon, hardware timestamping off (tx 0, rx 0), clock frequency offset 0 ppb, CLOCK_REALTIME 20.150 s ahead of the clock. Restored, 04:30:10 UTC: the same state, the clock back on its found trajectory within 4.5 us; the build and every script removed.

### B19: method and grades

Times are seconds after each run's software-grandmaster start. The console
was polled every 0.25 s, the controller read GET_AVB_INFO, GET_COUNTERS and
the ACMP states each second, and the tap recorded the DUT link, as on the
[#117 page](117_GPTP_SILICON_EVIDENCE.md#b19-method). Each run splits at
27 s: the takeover edge before, the release edge after. An edge passes only
if all six hold:

| Grade | Observable |
|---|---|
| One `tu` event | one rise of `tu` in the console samples, and one `tu=1` episode on the DUT's CRF PDUs |
| No asCapable loss | no console sample and no DUT GET_AVB_INFO poll with asCapable 0; a poll that does not answer is counted apart, and none failed to answer |
| One GM_CHANGED | the DUT's GPTP_GM_CHANGED rises by exactly 1 |
| No `mr` change | the DUT's CRF PDUs keep one `mr` value |
| MEDIA_RESET flat | MEDIA_RESET +0 on the DUT's AAF and CRF talkers and on the peer's CRF listener |
| No listener unlock | MEDIA_UNLOCKED +0 on the DUT's AAF listener and both peer listeners |

The DUT PHC step comes from the wire: the DUT's Pdelay responses carry its
PHC at the switch's request. The grandmaster time step comes from the Sync
and Follow_Up pairs forwarded to the DUT.

**Timestamp convention.** A console sample is timed at its command-send time
on the build-box clock. Its words were read before the command completed,
about 32 ms later. An edge first shown by a sample happened after the
previous sample was sent and before this one completed. That interval is
0.28 s wide at most, and the edge is reported at this sample's send time.
Assertion and clear come from each run's complete transition history, not
from a window around the PHC step. Wire `tu` episodes come from the DUT's
CRF PDUs on the tap clock, one PDU each 2 ms. They are kept apart from the
sampled console edges.

The round-1 analyzer searched for `tu` from the start of the console PHC-step
bracket, which can fall one sample after the rise. It also took the clear
time at command completion. So four `tu` set times were one sample late, and
every steady clear was 31 or 32 ms late. The packet's `r2_gm.py` replaces both
derivations. Its planted controls show a step bracket starting one sample
after the rise no longer drops the first `tu=1` sample. They also show a
planted controller poll with asCapable 0 fails its edge.

### B19: per-step results

| Run | Edge | DUT PHC step | GM time step | `tu` rises (console / CRF) | `tu` set / steady clear | asCapable 0, samples / polls | GM_CHANGED | `mr` changes | MEDIA_RESET DUT AAF / CRF talker, peer CRF listener | MEDIA_UNLOCKED DUT / peer CRF / peer AAF | Grade |
|---|---|---|---|---|---|---|---:|---:|---|---|---|
| 1 | takeover | +9.987 ms | +9.994 ms | 1 / 1 | 3.756 / 4.256 | 0 / 0 | +1 | 0 | +0 / +0, +0 | +0 / +0 / +0 | PASS |
| 1 | release | -10.003 ms | -9.995 ms | 1 / 1 | 50.527 / 51.027 | 0 / 0 | +1 | 0 | +0 / +0, +0 | +0 / +0 / +0 | PASS |
| 2 | takeover | +9.987 ms | +9.995 ms | 1 / 1 | 3.755 / 4.005 | 0 / 0 | +1 | 0 | +0 / +0, +0 | +0 / +0 / +0 | PASS |
| 2 | release | -10.004 ms | -9.996 ms | 1 / 1 | 50.523 / 51.023 | 0 / 0 | +1 | 0 | +0 / +0, +0 | +0 / +0 / +0 | PASS |
| 3 | takeover | +9.987 ms | +9.995 ms | 1 / 1 | 3.505 / 4.006 | 0 / 0 | +1 | 0 | +0 / +0, +0 | +0 / +0 / +0 | PASS |
| 3 | release | -10.004 ms | -9.996 ms | 1 / 1 | 50.524 / 51.024 | 0 / 0 | +1 | 0 | +0 / +0, +0 | +0 / +0 / +0 | PASS |
| 4 | takeover | +9.987 ms | +9.994 ms | 1 / 1 | 4.005 / 4.255 | 0 / 0 | +1 | 0 | +0 / +0, +0 | +0 / +0 / +0 | PASS |
| 4 | release | -10.005 ms | -9.997 ms | 1 / 1 | 50.522 / 51.022 | 0 / 0 | +1 | 0 | +0 / +0, +0 | +0 / +0 / +0 | PASS |
| 5 | takeover | +9.987 ms | +9.995 ms | 1 / 1 | 3.550 / 4.300 | 0 / 0 | +1 | 0 | +0 / +0, +0 | +0 / +0 / +0 | PASS |
| 5 | release | -10.004 ms | -9.996 ms | 1 / 1 | 50.449 / 50.949 | 0 / 0 | +1 | 0 | +0 / +0, +0 | +0 / +0 / +0 | PASS |

- "`tu` set" is the first console sample of the edge with `tu` set after one without it. "Steady clear" is the first sample from which sync 1, asCapable 1 and `tu` 0 hold for 2 s. Both use the convention above, each within an interval at most 0.282 s wide. The DUT was steady again 0.25 to 0.75 s after `tu` rose, by the same convention; on dev `13eda870` it took 3.00 to 4.53 s.
- On the wire the DUT's `tu=1` episode ran 0.376 to 0.684 s per edge, from its first to its last `tu=1` PDU, 189 to 343 PDUs at 500 PDU/s. It began with the new grandmaster's first Announce on the DUT link.
- **Minimum holdover.** Every wire episode exceeds the 0.25 s holdover. The console samples alone cannot show it: at two edges only one sample had `tu` set, which bounds the episode only to 0 to 0.53 s.
- The answered DUT polls numbered 36 in each takeover window and 83 in each release window. The other five of the 600 fell before the takeover window.
- The DUT's CRF never paused: the largest gap in any run was 2 ms, and `CRFT_CTRL` read `0x3002e3`, licensed, in every sample.

Per run, over both edges:

| Run | Takeover Announce | Last software-GM Announce | Release Announce | `CLKV_TUCNT` | DUT GPTP_GM_CHANGED | DUT CRF `tu=1` PDUs | Peer CRF listener TIMESTAMP_UNCERTAIN |
|---|---:|---:|---:|---|---|---:|---:|
| 1 | 3.611 | 49.670 | 50.399 | 253 to 255 | 12 to 14 | 432 | +432 |
| 2 | 3.562 | 49.651 | 50.470 | 255 to 257 | 14 to 16 | 436 | +436 |
| 3 | 3.409 | 49.539 | 50.449 | 257 to 260 | 16 to 18 | 500 | +500 |
| 4 | 3.755 | 49.841 | 50.411 | 260 to 263 | 18 to 20 | 492 | +492 |
| 5 | 3.341 | 49.448 | 50.399 | 263 to 265 | 20 to 22 | 532 | +532 |

The takeover Announce named the controller host's clock identity, priority1 240, stepsRemoved
1. The release Announce named the switch, `3cc0c6fffefe0210`, priority1 246,
stepsRemoved 0.

### B19: contract check

| Element | Decided reaction to one step | Observed over ten steps |
|---|---|---|
| asCapable (#621) | A PHC step keeps asCapable and a valid link delay | Kept in every console sample and every controller poll; peer delay 373 to 392 ns in both |
| Step policy | A locked servo steps above 100 us; a GM change keeps it locked | Each 10 ms offset stepped once; no other step followed |
| `tu` | Rises on the step; clears after at least 0.25 s of holdover | One episode per edge. On the wire `tu=1` ran 0.376 to 0.684 s from its first to its last PDU, so the holdover held at least 0.25 s. The console bounds the episode only to 0 to 1.03 s |
| Outgoing `mr` | Unchanged for a PHC-only step ([#602 ruling](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859297355)) | 0 changes on the DUT's CRF output; DUT AAF talker MEDIA_RESET +0 |
| Talker MEDIA_RESET | No step-only increment | +0 on both DUT talkers at every edge |
| Listeners | A licensed stream keeps streaming (REQ-PTP-08) | MEDIA_UNLOCKED +0 on the DUT's listener and both peer listeners |
| GPTP_GM_CHANGED | One per grandmaster change | +1 at every edge, on the DUT and on the peer |
| Render re-base | One counted re-base per step | Not graded on the bench: the simulation carries it |

### B19: other observations

These are recorded without a verdict.

- **The peer's AAF talker toggled `mr`.** Its MEDIA_RESET rose by 2 at every edge, and the DUT's AAF listener counted MEDIA_RESET +1 per edge from that stream. The DUT's own talkers counted none.
- **Presentation counters.** The DUT's AAF listener counted LATE_TIMESTAMP +1 at each takeover and EARLY_TIMESTAMP +1 at four of the five releases. It counted TIMESTAMP_UNCERTAIN +1 per edge (+2 at two edges whose episode crossed a counter interval).
- **Interval counters.** The DUT talkers' TIMESTAMP_UNCERTAIN, its CLOCK_DOMAIN LOCKED and UNLOCKED and `CLKV_TUCNT` rose by 1 per edge, or by 2 where the episode crossed a 1 s interval.
- **A console artifact.** In run 5, one console sample came back late at 1.5 to 2.1 s. The step detector saw a cancelling +4.98 ms and -5.02 ms pair there, with no wire jump, no `tu` and no holdover: a timing artifact, not a step.
- **One clock read failed.** After run 3's measurement, the runner's closing clock read of the capture server failed once (an SSH error), so its last outlet read and copy were done by hand at 04:19:51 UTC, all outlets on. The runner then gained a retry for that read.

### B19: artifact hashes

The raw files are listed in the private bench packet `117-b19-a624`
(`RAW-ARTIFACTS.json`, sizes and SHA-256). All 151, the files over 200,000
bytes included, are in the project's durable cold archive. The
[manager's receipt](https://github.com/kebag-logic/milan-fpga/pull/751#issuecomment-6208612856)
re-verified every SHA-256 there: 151 equal, 0 differ, 0 missing.

| Item | SHA-256 |
|---|---|
| Reference gPTP implementation 4.4, source tarball, 277,069 bytes | `61757bc0a58d789b8fcbdddf56c88a0230597184a70dcb2ac05b4c6b619f7d5c` |
| Its gPTP port program as built | `25247f3a744532f02e84638915c14922a19c8da8add52c81f5e88e3418dae7bd` |
| Its clock-control program as built | `ea44d7799a0f7b4dc6a9d3c50f1edf146f98a2efe6053255290f0bfcdc4a002d` |
| Its timestamping-control program as built | `c29b72c7116fb3389e2e3aa7d5f0c2fd0ddb0d846f54b98418c930d060ccdb4e` |
| Grandmaster configuration | `f798c63330ef976c16dbf4b8a26242d684eb897ff2c98f61b56d8faa42b50413` |
| Alignment configuration | `f1e59efb5843a288a102b6a9bc6f492a2b33e32ca6deea555a817e7cd049948c` |
| `a624_action.py`, runs 1 to 3 | `9da7bbaf555558439f32fec79b31473d1bd52cb7ce577d2b3d624d1efdd94eee` |
| `a624_action.py`, runs 4 and 5 (the clock-read retry) | `433d6fb7be417308e710f096648df7249c54ddf94628a467f8473e93975c0152` |
| `a624_analyze.py`, analysis | `61823723b1e74d59bdd6a81a061ca9d747cf89544585668a944ebbaea276f4c6` |
| `gm_summary.py`, grades and tables | `3aea02fb088366fa76b98fc3f7108c08b052134acdd0a740415170480c9e92d3` |
| `phc_restore_b19.py`, controller clock restore | `7cb9158eb87170f9597c49af2d1dad7d0e5537d7e353b751d49dc9e26072e7be` |

| Run | Raw artifact | Bytes | SHA-256 |
|---|---|---:|---|
| gm01 | `console.jsonl` | 1124715 | `41e7a7561b9adbdb4bc28fa157f4cbc4cd1a8bf3ea69c1301aa510f4516732bb` |
| gm01 | `controller.jsonl` | 804812 | `b9df838ed047bf8289849f02e7c0bb6fe665a4cb43b3e7c588cae495a2043706` |
| gm01 | `controller-wire.pcap` | 532174 | `ebcd44a63fc413488df32cb7b24e499ce432300f89a200cbf139539794de4d57` |
| gm01 | `tap.pcap` | 7118045 | `2835c80d698a30ebd3fdf4ccc313904dc47755c2169c103210e54ec50708ea6a` |
| gm01 | alignment port log | 3448 | `d48d6f8bb6f5229a3426429aeaf38f946baba20af1974ad3e2e0a9649f2c3d3b` |
| gm01 | grandmaster port log | 485 | `a004b07387650c2d9bd6e97bc3a2462ca7f62ecc86bee2962801eaea485593e1` |
| gm02 | `console.jsonl` | 1124300 | `7a00c5a3e8b9c132d1458d45937f13f0b694098ca9cd157bcf2b40eccc33a4c5` |
| gm02 | `controller.jsonl` | 804963 | `e2359da22c1b916dea9510c1d9aa7e4a0c6748bb2d178971945f13b635b1e842` |
| gm02 | `controller-wire.pcap` | 538132 | `095f20c2bdd90f75fc6b4d64888b44698047c400dc6164e4f11bdb0f74e5b648` |
| gm02 | `tap.pcap` | 7120986 | `8315c5657debe48af7dc3b884db7a87c3271956726789c9764e70ebd7d7c9b23` |
| gm02 | alignment port log | 3501 | `4c5b7b36a9d34157e81d6e692c76ae8eb808989f2d9d9118543e93b1ba187f42` |
| gm02 | grandmaster port log | 560 | `1daa680a589c35b7ba42d271093d94fc69b7b0911f5612538b2ea4ffb7e46916` |
| gm03 | `console.jsonl` | 1124324 | `12ba0197888fcaa0160534b084a42681a9f3960528fd97203569c3bbd8a93eae` |
| gm03 | `controller.jsonl` | 806075 | `1ce9332e74422d72a055898fc0f96ad1af95065fb316a09d1eea009034c4d5ee` |
| gm03 | `controller-wire.pcap` | 532670 | `768a373a58db1265d048117f0570d264b6c33345ceb5115570d60270ce7a3b89` |
| gm03 | `tap.pcap` | 7114571 | `4c84baf24a4582cdb8371d93c7ee627c0e310ee3f4d4b5b39a49240094dbd073` |
| gm03 | alignment port log | 3501 | `05f2c169756ee3e2395fb3786b604ab20c0496f7891fad62398cbc9c2381e60d` |
| gm03 | grandmaster port log | 560 | `108f8c7ad5c2f0b1bce897345a9be6157f5d6e950dd5da1fad8a5d32235e9d1f` |
| gm04 | `console.jsonl` | 1124257 | `b7e311f3a541daaf4acd3753b922e2244c64b4ce665f1115358dcbe64d5a3593` |
| gm04 | `controller.jsonl` | 805436 | `774fb6621fe0419a8c980b98751a664ae9d633ae1b5a234fc5d0ddab9a313e37` |
| gm04 | `controller-wire.pcap` | 538497 | `14e5b4ad9d45af503b3db42fe0525672f1d2e284505338cd50b6460bfe5348f2` |
| gm04 | `tap.pcap` | 7125680 | `996279bdd13a51f859003ecf634d0a981f8e6d6b0cb7a85166343e57f290cb6c` |
| gm04 | alignment port log | 3501 | `e93bffc7fa14079b046d043b5ee5e65d8d15154ffb188c65fad5336761452c6f` |
| gm04 | grandmaster port log | 560 | `076f47e6f7c78851b6c982064d882afb75afe845bebde11d671faf7b90d8f691` |
| gm05 | `console.jsonl` | 1121876 | `d9ea75c22fdd99f4653fb473aaf37e77d4983de9c3906fe44aa007a5a1a05c8c` |
| gm05 | `controller.jsonl` | 805626 | `1d1b7fec79e8872bee783946a81ad7196a9f842d58db65911d867a5d1291883b` |
| gm05 | `controller-wire.pcap` | 536447 | `f9de48c7a5f4281cca1d08da557574e5717dfb4da01569773671b1023f70e151` |
| gm05 | `tap.pcap` | 7116950 | `09d5b6bce3ddaa67e970557f8e46ee0ec85c87df4809fe73e319e77b77203254` |
| gm05 | alignment port log | 3424 | `b0c88e85f4395b72a963ea82cf8c1c7b5ee42ec2ba06b6518d4e444c8299d2a5` |
| gm05 | grandmaster port log | 485 | `6f2610444091b41b69a12ae8b8e1b8073a8e43636bb41d8b802d3675a0bfdd5a` |
