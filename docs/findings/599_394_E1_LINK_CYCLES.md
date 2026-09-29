<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# Published link state over ten e1 switch power cycles

Refs #599 and #394. Operator [A438], measured 2026-09-29, under the
[bench assignment](https://github.com/kebag-logic/milan-fpga/issues/599#issuecomment-5884216527).

| Acceptance | Verdict | Evidence |
|---|---|---|
| #599 acceptance 4, first half: does a switch cycle drop the DUT PHY link? | PASS: it drops | The firmware's BMSR publication fell 2.31-2.56 s after OFF and returned 37.07-37.32 s after OFF. The inline capture point does not hold the link up. See [Link-drop proof](#link-drop-proof). |
| #599 acceptance 4: +1/+1 on LINK_DOWN/LINK_UP in every cycle | PASS | Ten of ten cycles: LINK_DOWN +1 and LINK_UP +1, DUT 2/1 before cycle 1 and 12/11 after cycle 10. MAC_STATUS went `0x0d`, `0x00`, `0x0d` in every cycle. |
| #394 acceptance 2, e1 only | PASS | Ten of ten cycles recovered the reservation, both bindings, asCapable and MEDIA_LOCKED with no reboot and no re-bind. GET_COUNTERS showed LINK_DOWN, LINK_UP and MEDIA_UNLOCKED +1 each per cycle. gPTP recovered in 0.544-1.786 s against the 5 s bound. The restart time is recorded, not graded against #75. |

These are operator measurements, not review verdicts.

The [#387 page](387_SOFTWARE_GM_STEP.md) records the same session's grandmaster steps.

## Contents

- **[Identity and setup](#identity-and-setup)** -- The image, its identity readback, and the starting bench state.
- **[Method and limits](#method-and-limits)** -- How the link state was read, what was sampled, and the timing limits.
- **[Link-drop proof](#link-drop-proof)** -- The read-only switch cycle that answered #599's first question.
- **[Per-cycle results](#per-cycle-results)** -- Link edges, counters, recovery and restart in each of ten cycles.
- **[Counters and media](#counters-and-media)** -- Counter blocks before and after, and the media observations.
- **[Restore and validation](#restore-and-validation)** -- The restored bench and the local gates.
- **[Artifact hashes](#artifact-hashes)** -- Image, tool and raw-capture identities.

## Identity and setup

The image is dev `13eda870d1a6cf3f946fc228a98862366b08d102`, seed `eto`.

The lane base is the same commit, so no source differs.

| Identity check | Result |
|---|---|
| VERSION | `0x00020060` |
| ROM CRC32, 53,344 bytes | `acad92b9` |
| QSPI payload CRC32, 3,825,788 bytes | `d84bce7b`, the `eto` seed; `eppo` reads `bf44ccc9` and `asl` reads `809fcffa` |
| AEM CRC32, 7,352 bytes | `93742dd2` |
| Bitstream SHA-256, 3,825,992 bytes | `690d87e407bbb7f7bba52bbe7a7e0dc85cd264df2db5eec87bfaf85f99bda24b` |
| Bitstream payload SHA-256 | `6597f7a601ddb3dbba1bf058c38716277e8feb1147fb89edcf1d39e755dc369f` |
| AEM SHA-256 | `9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404` |
| CSR map SHA-256, 9,033 bytes | `7723d0b8129df7b77b3b49980366f18c91adb15f8c38526f48a5ebd32d1207a2` |
| Live ENTITY and CONFIGURATION | Byte-exact matches to the AEM image; entity `020000fffe000001` |
| NVM walk | Both slots `VD_OK`, `backed=1`, writer live |
| UART grader | 10 of 10, exit 0 |

Readback proves CRC consistency, not a configuration SHA-256.

The [identity method](117_GPTP_SILICON_EVIDENCE.md#candidate-image-and-identity-proof) was repeated.

As found, OUT1 and OUT3 read OFF and the other five outlets ON.

PR #600 had found all seven ON; this run restored the state it found.

All eighteen queried stream states were unbound.

The DUT selected INTERNAL, source 0.

The reference peer was in configuration 1 at 48 kHz, on INTERNAL.

PR #600 had found configuration 0 at 96 kHz; this run changed neither.

In configuration 1 the peer's CRF input 8 and output 2 keep format `041060010000bb80`.

| Direction | Binding | Format |
|---|---|---|
| DUT to reference peer | Output 1 to input 8 | CRF, `041060010000bb80` |
| Reference peer to DUT | Output 2 to input 1 | Same CRF format |

DUT source 1 selected the bound CRF input.

A 30-second bound baseline carried 15,000 PDUs each way, all with `tu=0`.

The DUT listener was MEDIA_LOCKED and its media servo LOCKED at about -5.9 ppm.

## Method and limits

**Reading the link state.** This image has no console MDIO command.

A manual Clause-22 read needs writes to the bit-bang MDIO CSR.

The bench rules forbid those writes.

They would also clear the BMSR latch the firmware's poll relies on.

So the BMSR was read through the firmware's own poll, which is read-only to the bench.

The [firmware contract](../integration/BAREMETAL_FIRMWARE.md) polls every 125 ms and publishes within 250 ms.

Console `mem_read` sampled `MAC_STATUS` (`0x110`) and the `link_status` CSR every 250 ms.

Both agreed in all 7,520 console rounds of the session.

`LINKG_STAT` (`0x774`) was sampled with them.

A link edge therefore lies inside a 0.25 s console bracket.

The poll adds up to one further period before the bracket.

**Other observations.** Each 250 ms console round also read these words:

- `milan_status`: GM, sync, asCapable, `tu`, `CLKV_STAT` and the PHC.
- `RST_EPOCH`, `CLKV_TUCNT`, `A_MCSRV_STAT`, `CRFT_CTRL` and `CRFT_COUNT`.

The controller read GET_COUNTERS and both ACMP states every second.

A separate 100 ms sampler logged the controller port's carrier.

The inline tap recorded the DUT link, including both CRF directions.

The controller port was captured too.

**Timing.** Every time is seconds after that cycle's OFF command.

Cross-host offsets use three clock probes before and after each action.

The quickest round trip supplies each offset.

**Scope.** Only OUT4, the bench AVB switch, was cycled, each time for about 20 s.

The DUT was never rebooted, flashed or power-cycled.

`RST_EPOCH` read 1 in every sample.

The largest console sampling gap in any cycle was 0.255 s.

Each action held the bench lock only for its own duration.

**Capture prerequisite.** The tap again had no capture interface on the capture host's current operating-system release.

As in PR #600, the same three driver inputs were rebuilt in a temporary directory.

They matched PR #600's recorded SHA-256 values.

No source change, permanent installation, firmware write or wiring change occurred.

The module was unloaded and its build removed at restore.

**Definitions.** gPTP recovery runs from the first returning Announce or Sync on the DUT link.

It ends at the first console sample with the switch as GM, sync 1, asCapable 1 and `tu=0`.

That state then held to the end of every cycle.

Valid CRF PDUs match PR #600's shape checks.

These cover subtype, version, 48 kHz, interval 96, VLAN 2, PCP 3 and the bound stream ID.

"Link-up to first PDU" starts at the MAC_STATUS up sample.

Issue [#75](https://github.com/kebag-logic/milan-fpga/issues/75) times from CONNECT_RX success instead.

These automatic returns issued no CONNECT_RX, so the column is recorded, not graded.

## Link-drop proof

One OUT4 cycle ran with nothing bound, before any other cycle.

It also repeated the earlier [OUT4 proof](117_GPTP_SILICON_EVIDENCE.md#out4-is-the-switch).

| Observation | Seconds after OFF |
|---|---|
| Switch's last frame on the DUT link | 0.96; none from 5 s until ON |
| Controller port carrier lost | 1.39 |
| DUT sync lost, `tu` set | 1.53 |
| MAC_STATUS and `link_status` `0x0d` to `0x00` | 2.31-2.56 |
| DUT names itself grandmaster | 3.53 |
| `LINKG_STAT` `0x83` to `0x03` | 3.84 |
| OUT4 ON | 20.86 |
| Controller port carrier back | 34.68 |
| MAC_STATUS and `link_status` `0x00` to `0x0d` | 37.07-37.32 |
| First frame on the DUT link | 38.71 |
| `LINKG_STAT` back to `0x83` | 38.85 |
| Switch's first Sync | 39.74 |
| gPTP recovered | 41.57, 1.832 s after that Sync |

The DUT's LINK_UP/LINK_DOWN went from 1/0 to 2/1.

The DUT console answered throughout; its reset epoch stayed 1.

The reference peer's advertisement index went on counting, 87336 to 87354.

With OUT4 off, every other outlet read as found.

The inline capture point does not hold the DUT PHY link up.

No owner decision on the method is needed.

## Per-cycle results

All table times are seconds after OFF.

Link brackets are the last console sample before and the first after the edge.

"GM return" is the switch's first Announce or Sync after ON: a Sync in six cycles, an Announce in four.

"CRF licence" is `CRFT_CTRL` leaving and regaining `0x3002e3`.

| Cycle | OFF | MAC_STATUS down | MAC_STATUS up | LINK_DOWN / LINK_UP | GM return | gPTP recovery | First DUT / peer PDU | Link-up to first DUT / peer PDU | CRF licence off / on | Bindings |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 20.90 | 1.81-2.06 | 36.82-37.07 | +1 / +1 | 39.78 | 0.544 | 45.05 / 46.12 | 7.97 / 9.05 | 13.41 / 45.17 | held |
| 2 | 20.97 | 2.06-2.31 | 36.82-37.07 | +1 / +1 | 40.02 | 1.555 | 45.22 / 47.96 | 8.15 / 10.88 | 15.15 / 45.42 | held |
| 3 | 20.88 | 2.31-2.56 | 36.83-37.08 | +1 / +1 | 39.88 | 1.704 | 51.91 / 49.17 | 14.84 / 12.09 | 14.90 / 51.92 | held |
| 4 | 20.86 | 2.06-2.31 | 37.07-37.32 | +1 / +1 | 39.81 | 1.513 | 43.06 / 45.60 | 5.74 / 8.28 | 16.40 / 43.17 | held |
| 5 | 20.86 | 1.81-2.06 | 36.82-37.07 | +1 / +1 | 39.85 | 0.720 | 45.27 / 46.71 | 8.19 / 9.64 | 19.65 / 45.42 | held |
| 6 | 21.06 | 2.31-2.56 | 39.10-39.35 | +1 / +1 | 42.10 | 1.750 | 46.30 / 46.65 | 6.95 / 7.29 | 6.67 / 46.44 | held |
| 7 | 20.88 | 1.81-2.06 | 36.59-36.84 | +1 / +1 | 39.88 | 1.463 | 45.25 / 45.58 | 8.41 / 8.75 | 11.65 / 45.43 | held |
| 8 | 20.85 | 1.81-2.06 | 37.08-37.33 | +1 / +1 | 39.81 | 1.523 | 45.10 / 46.20 | 7.78 / 8.88 | 16.41 / 45.17 | held |
| 9 | 20.87 | 2.31-2.56 | 36.82-37.07 | +1 / +1 | 39.90 | 1.427 | 49.06 / 49.41 | 11.99 / 12.33 | 10.90 / 49.17 | held |
| 10 | 21.05 | 2.06-2.31 | 36.82-37.07 | +1 / +1 | 40.04 | 1.786 | 45.36 / 45.67 | 8.29 / 8.60 | 18.16 / 45.42 | held |

- All ten cycles counted LINK_DOWN +1 and LINK_UP +1.
- The PHY link dropped 1.81-2.56 s after OFF, about 1 s after the switch's last frame.
- It returned 36.59-39.35 s after OFF, 1.43-1.96 s before the first frame on the link.
- gPTP recovered in 0.544-1.786 s, inside the [5 s bound](../design/GM_LOSS_RECOVERY.md#recovery-bound).
- Both listeners were MEDIA_LOCKED again 43.95-52.55 s after OFF.
- The media servo was LOCKED again 48.40-52.40 s after OFF.
- Both CRF streams and both bindings recovered with no controller action.
- First valid PDUs followed the first returning frame by 4.26-13.04 s (DUT) and 5.56-10.60 s (peer).
- Link-up to first PDU was 5.74-14.84 s (DUT) and 7.29-12.33 s (peer).
- All of these exceed #75's one second; the trigger differs, so this is no #75 verdict.
- Each grandmaster return stepped the DUT PHC by -115.9 to -340.7 s.
- The switch's time restarts at each power-on, as #117 recorded.
- No cycle approached the 180-second stop deadline.

## Counters and media

GET_COUNTERS on the DUT, from the bound baseline to the end of cycle 10:

| Counter block | Before cycle 1 | After cycle 10 | Per cycle |
|---|---|---|---|
| AVB_INTERFACE LINK_UP / LINK_DOWN | 2 / 1 | 12 / 11 | +1 / +1 |
| AVB_INTERFACE GPTP_GM_CHANGED | 2 | 22 | +2: itself, then the switch |
| CRF STREAM_INPUT MEDIA_LOCKED / MEDIA_UNLOCKED | 1 / 0 | 11 / 10 | +1 / +1 |
| CRF STREAM_OUTPUT STREAM_START / STREAM_STOP | 1 / 0 | 11 / 10 | +1 / +1 |
| CLOCK_DOMAIN LOCKED / UNLOCKED | 2 / 1 | 12 / 11 | +1 / +1 |

The link-drop proof cycle moved LINK_UP/LINK_DOWN from 1/0 to 2/1 before this table.

The reference peer's LINK_UP/LINK_DOWN stayed 1/0 throughout, as in #117.

Its GPTP_GM_CHANGED went from 40 to 60.

The DUT's outgoing `mr` changed once per cycle, at the loss.

That is the selected-CRF disruption cause the [#602 ruling](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859297355) keeps.

It did not change again on resumed transmission.

The reference peer's `mr` never changed.

DUT talker MEDIA_RESET read 1 after the loss and 0 after the next STREAM_START.

STREAM_START resets its interval count, as PR #600 recorded.

These restart observations are recorded without applying #593.

## Restore and validation

- Both bindings unbound on their first attempt; all eighteen stream states read connection count 0.
- DUT clock source 0, INTERNAL, was restored.
- The start and end censuses agree on all 53 non-counter reads.
- The peer's varying reserved half-word and the measured peer delay are excluded.
- The peer's Stream Output 2 still names its last stream and destination, with connection count 0.
- Outlets read as found: OUT1 and OUT3 OFF, the other five ON.
- The grandmaster is the switch on the console, on the wire and at the controller.
- Final console: sync 1, asCapable 1, `tu=0`, reset epoch 1, servo IDLE, CRF talker control `0x3`.
- The UART grader passed 10 of 10.
- A final 20-second tap capture carried no CRF PDUs.
- The temporary capture module was unloaded and its build removed.
- The tap was left as found, visible without a capture interface.
- The bench lock was released and verified free.

The controller host's restore is recorded on the [#387 page](387_SOFTWARE_GM_STEP.md#restore).

No RTL, firmware or other documentation changed in this lane.

## Artifact hashes

The author's bench packet holds scripts, transcripts, analyses and `MANIFEST.sha256`.

Each action's `raw-artifacts.json` indexes its raw files by size and SHA-256.

Raw captures are kept outside the packet on the bench host; the table identifies them.

Raw retention follows [TESTING section 6b](../testing/TESTING.md#6b-bench-evidence-retention).

| Tool | SHA-256 |
|---|---|
| `b1_action.py`, acquisition | `dd6d6ec73c2160064d37ace96b789aa2108eb81f4ee75705119594ce9def360c` |
| `b1_analyze.py`, analysis | `e4f7681891e1ed76fc3916a4395f82a6abf5c55a66c40fd4c065cfb019e429e0` |
| `b1_summary.py`, tables | `7c388bb385c9fb417d89c85c14387231c14ba38bf54a1dc4d38b99c84f5089e6` |
| `census_compare.py` | `f014c6f2bd80e4622960c76dba3c908299357f8c9fcc03097441750d40d8db79` |
| `wire_summary.py`, tap decoder, unchanged from PR #600 | `7a8af475fa5f8bfbb90636b92bf9d07a86140c54a9be10c12f9b76235bccd922` |
| `console_poll.py`, unchanged from PR #600 | `3a0de7d8e1f9f4e0f87d03364c3cf35e9965210dd7095b21ef9d1b7bdb1bd326` |
| Controller reader, unchanged from PR #600 | `172836966609645d6e12adf19a8341a145a4dadc51edb81c6d29a23aae1fd75a` |
| Controller actions | `94c3473d26b1451dc0d63e4c3390942abf2ecf6e03111ac9dc250a208a849330` |
| [UART grader](../../scripts/baremetal_uart_smoke.py) at `13eda870` | `bc41ab03e64198b10a517124f960b9b59b77d7143661f728fe5666314e433886` |

The acquisition script changed once before the grandmaster runs.

The change touched only its grandmaster preparation; the cycle path is unchanged.

| Action | Raw artifact | Bytes | SHA-256 |
|---|---|---:|---|
| baseline-bound | `console.jsonl` | 281035 | `1a18cf76b5dd2cc6c7a29daf6ce0976e9ba3ef152ae77cb904b828394cc72829` |
| baseline-bound | `controller.jsonl` | 158776 | `5f349b929152cc145ae47f2d9993f132c76a5e832b0f863bd6132f5fe4ce12b3` |
| baseline-bound | `controller-wire.pcap` | 83285 | `e1759b461f8fc1bb12423200998c552074277e8be9befa5b515a3a77b1bbebf8` |
| baseline-bound | `tap.pcap` | 3405061 | `8dbb5991e4005f2f19401270e3b756d866c773e2804b9c1254b8fb5f0d56a3af` |
| baseline-bound | `events.jsonl` | 3523 | `19b117327439c17e549ea2d6ffce513d1d5c32df8287891e72914c91a1180a22` |
| bmsr-proof | `console.jsonl` | 1030629 | `4764df46a24c298998419f68415bbf17d2ed4b3cee77a771e341aa117ca01686` |
| bmsr-proof | `controller.jsonl` | 391063 | `16d12ad49a454ee78317ec9e7a06bd721d289753eb8b0337e2925f2209aff7ee` |
| bmsr-proof | `controller-wire.pcap` | 221631 | `1047525ce7111d045cd4a0418268b4685f89eafdf12ebc00b2e30d84bc2597f7` |
| bmsr-proof | `tap.pcap` | 392694 | `8626e39d5be93c84cef647a6eeb858a09b7c590d2fa4017a04281a41fff3dd4d` |
| bmsr-proof | `events.jsonl` | 4432 | `1a64223ddc6fcd7fffdab74c920544f20ba1c18983158d29ee0fe54ff05737c4` |
| cycle01 | `console.jsonl` | 1030610 | `4a9064e38aa89e07d055ad06c11be6321693ae8cf6dc25e6a559c6d4381607c4` |
| cycle01 | `controller.jsonl` | 387042 | `b920fef033174caed079734b8cab04477f0c5aa9cb0cd2415d494dd8dcdd215e` |
| cycle01 | `controller-wire.pcap` | 221088 | `d47c3064750add2ad9121fbe582f3ea734305b364e39f1a66a409916f2ba5636` |
| cycle01 | `tap.pcap` | 7389317 | `1d4590facaf2dd1067b2d238e60121f6e164b1bf0f98fe8d86c4122388c77c29` |
| cycle01 | `events.jsonl` | 4427 | `9fa46da855f28c3f6d2b0d9b143b1aed9fdf833c6235a993c177abbc491453d7` |
| cycle02 | `console.jsonl` | 1030651 | `c54a59cfb1b48c35a134d50a81995a83b9af841a3485bcf96c90f227399d0461` |
| cycle02 | `controller.jsonl` | 393492 | `82e82dfa50a5b6a0cd297d5de307be73477b4aa2007ab6f425256f14ea33dbab` |
| cycle02 | `controller-wire.pcap` | 223641 | `e062b34a22bd919ef1b62787f2ad220d9742f14742ea832cf33415e8094d465d` |
| cycle02 | `tap.pcap` | 7308248 | `f321bec940aba6c1ab0d1bb37b9ea401ed61c20ab2b23915ecb1d0d6418b45ba` |
| cycle02 | `events.jsonl` | 4426 | `37120ebbcc5ba17b068a7b5ab07c80007678989465ab0e0075f2b2f4854cb4cf` |
| cycle03 | `console.jsonl` | 1030581 | `8e395b8e1b7401f60194e7318a30a5c0f101015dbcb4de0e8d0f26d9a8a3a712` |
| cycle03 | `controller.jsonl` | 386971 | `ff4296d591d8c887c5ff581ddd03aa4e33efc84b6a76cee76a73941123779357` |
| cycle03 | `controller-wire.pcap` | 218508 | `028bce855ebb0f5ca525d648d581dcd2c44299fbea57b80a6b60af9cd4ce07ca` |
| cycle03 | `tap.pcap` | 6990195 | `1064e8021bedd01eb31d29e32d311f6c2870d725c97ccbb7cc6f6244f4d244be` |
| cycle03 | `events.jsonl` | 4423 | `ad25b1385eb6124597406e4637060e5cab087ff4f8d93a9fc01f02ac0faa0553` |
| cycle04 | `console.jsonl` | 1030948 | `d8b2168bf3757aa561554f71200a237cdd58f950f91b206b493741b45c4fbfcf` |
| cycle04 | `controller.jsonl` | 392490 | `b75848b86669821d816f224528403212ce6e551ee08cf70f4a8e3f0603ac4e6a` |
| cycle04 | `controller-wire.pcap` | 225327 | `6d94816f6795e1b6fcde6a85878b509b71cc07fc59ee9a8dd1fea1eba765bed8` |
| cycle04 | `tap.pcap` | 7653986 | `50766adf9764cb6b918bd43f101a970fd84dcc27063b40e8bda1374526b8ed4a` |
| cycle04 | `events.jsonl` | 4416 | `4ee4418dcda6f632c3f2d0be8f05eb90ab7592f6bb1ac343c80e1348db12bd89` |
| cycle05 | `console.jsonl` | 1031063 | `13e290bdc7be01d09e4f81268e87b802f858e1c642784cdff2507167a0d41c61` |
| cycle05 | `controller.jsonl` | 392836 | `3fc16cd6946b59fc08e75f99dd28b33dedb856b0020c48ca51b319df0caad077` |
| cycle05 | `controller-wire.pcap` | 223217 | `679072d7a99a0a90ea51c1630fd773a1a562ae4a8adfe0d7c1f1cc756ee1f2f8` |
| cycle05 | `tap.pcap` | 7471838 | `1c650feec66029c52844f385087ac44f99488cc170aeba24f244cbcb95cc20bb` |
| cycle05 | `events.jsonl` | 4424 | `db41a82c607677eb7d8dfb344b706506968c711f4effa1b0ad2de949100baa1d` |
| cycle06 | `console.jsonl` | 1030958 | `db21fc3b4633fac8ae9f96a91e401ddce2d36e6a540242eb8a25f61317410117` |
| cycle06 | `controller.jsonl` | 376378 | `2331685243cad23f55a533dcf582546358fb3e9e5600448050e7bd8c15f9c22e` |
| cycle06 | `controller-wire.pcap` | 216528 | `ea1366598313b314fba8e294ab8d9aa122f6c5db379466fa703218eed28ce140` |
| cycle06 | `tap.pcap` | 7419798 | `1bd3902547dfbe627d598c5c7444e0aacf4dba23ba157b3a0ca0093b7cad4aae` |
| cycle06 | `events.jsonl` | 4423 | `f2fdc17ddd29104c89e4a5c528a72fcd703ecee1cbcd2969ba3a76dbff5a5e73` |
| cycle07 | `console.jsonl` | 1030626 | `ee0ef7e43a5b782fa36b43b86fa77297bb0c19e681312fdc8fec4a3a18817656` |
| cycle07 | `controller.jsonl` | 392833 | `b0735c1dd0bcc4708689f86767c5f8ccbf2899bad59cfcb883c14dba92c2dd70` |
| cycle07 | `controller-wire.pcap` | 223209 | `75b9db5c039952e1ebfb27eb044558ad15ee7c1acfb9910a27f764c529ae9c48` |
| cycle07 | `tap.pcap` | 7517794 | `7e1970fd874ddc66af58dece8d06bd6d18c570d0b2bf3ccc39b6f9781fbd6677` |
| cycle07 | `events.jsonl` | 4430 | `ac2f72ca6ea59cd87e25c74f3408d54122f974cf9f2d49fe6d56390e838db0c4` |
| cycle08 | `console.jsonl` | 1030503 | `e08f65975c6683a36fe775f7057e6e2ad23409daae9e48e46892d260e79f5e8b` |
| cycle08 | `controller.jsonl` | 392607 | `6e26bcf5d77ebe3754e19f38c3948737ec957776bd2b11f691072805069bd1a1` |
| cycle08 | `controller-wire.pcap` | 223027 | `9472394b0c949a7bfccf27fce7dcf7e8e5e576e3b011491ab12da09f93036ab8` |
| cycle08 | `tap.pcap` | 7499543 | `4e51f77ff27b158c1baa32fad0aa666ae6f30900e2b98ccbd30fa70d4883d709` |
| cycle08 | `events.jsonl` | 4429 | `e05c8054b43f53d89fd46dd7e983f3f1a234c0e7e470a3bcba5830902b0d2451` |
| cycle09 | `console.jsonl` | 1030587 | `c4966de2234ed48bff7b39d4aa14d2fd5587c38a84c7f304c514bc8d52c64199` |
| cycle09 | `controller.jsonl` | 387426 | `13518a9b122d9684cb467fe386d99cf930299141eb7b625016954a4c5f0a33dc` |
| cycle09 | `controller-wire.pcap` | 222394 | `e7f43fc866cc6926177c6285752126a991a75a6b051a2258dade061bb158a08a` |
| cycle09 | `tap.pcap` | 7026007 | `cfe8b42e0be6917aa09b25859788e989f082e075b482b28cae95ab9276e59e4a` |
| cycle09 | `events.jsonl` | 4427 | `49e70cddae0f081dd04b9fe2424d3bb7cb178d60c366747e88aa2075d9b79649` |
| cycle10 | `console.jsonl` | 1030456 | `855eaa4aaa2091c8f176e683237cde2986de1c1da99954eb6b0dfba25dbf1b66` |
| cycle10 | `controller.jsonl` | 387630 | `268c21ddd42314c14c48407554caab9f734afa97367a06a0b8fc679108f04c38` |
| cycle10 | `controller-wire.pcap` | 217955 | `09723298565221fa07bf305a8a442a45469e62fa5d6131fdda0057e6b8e8a965` |
| cycle10 | `tap.pcap` | 7535225 | `959b33d3e92e700d54ba77ebfa9d095a2f1d64c34974bae4b0dbb34ce9a76518` |
| cycle10 | `events.jsonl` | 4423 | `cefe475b77241b654714a49bd8f9d42d22f91f8732838e479cd1ad6f2780e875` |
| final | `console.jsonl` | 187365 | `a31acfa62ec6dafb4cc435d4bc2d659cce5ad57e4aa4884e3701810163f83abc` |
| final | `controller.jsonl` | 106986 | `c3d713b1e6a7b3e1c19a91dde235257bf24f4d7a92f4a3a53b8365b470d0f8f0` |
| final | `controller-wire.pcap` | 55794 | `d7f133423855bdf01caf76f0bc83d8fa951489144295184fbd4ee64b26571ed9` |
| final | `tap.pcap` | 107324 | `d4a257684d4a5d3cf007b45d0801e51b9a89b94bc6bb8e527bd6355f1d99b591` |
| final | `events.jsonl` | 3524 | `7273adbd2c3885e6a610f43a786f3969a79b94f434636133031df18917244f5c` |
