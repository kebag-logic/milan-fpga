[A231] RESULT: #529 silicon confirmation on the dev `50e78097` image. **PASS: the controller no longer downgrades the DUT from Milan.**

**Identity: PASS.** The console read `ID=MILN` and `VERSION=0x00020060`, and the UART grader passed 10 of 10 before and after the run. The bench lock was held for every console, bind and enumeration window.
- The CRC readback names the image: the QSPI bitstream payload reads `e5fb8b18`, the `eppo` seed of dev `50e78097`. That excludes the `asl` seed `b46a9492`, the `eto` seed `a1be376b` and the #117 image `02036e95`.
- ROM `f6afa4ec` and AEM `93742dd2` are the same as all three `50e78097` seeds.

**gPTP: locked.** The console read `SYNC=1 ASCAPABLE=1 TU=0` in 79 of 79 samples, with the bench AVB switch as grandmaster and a peer delay of 381 to 394 ns. The controller's GET_AVB_INFO reported asCapable in 12 of 12 polls, on both the DUT and the reference peer.

| Acceptance | Result | Evidence |
|---|---|---|
| Full controller enumeration as #117 step 5; no Milan downgrade over the Stream Input counters (CRF input included) | **PASS** | See the step 5 notes below the table. |
| GET_COUNTERS on every Stream Input and Output | PASS | 57 rounds at 5 s: DUT STREAM_INPUT 0 and 1, STREAM_OUTPUT 0 and 1, AVB_INTERFACE 0, CLOCK_DOMAIN 0, and the peer's CRF input. 399 of 399 reads answered SUCCESS. Masks: STREAM_INPUT 0 `0xFFF`, STREAM_INPUT 1 `0xF3F`, both outputs `0x1F`, AVB_INTERFACE `0x23`, CLOCK_DOMAIN `0x3`. |
| Counters before, during and after a bound period, and the unsolicited notifications | PASS (recorded) | See the bind notes below the table. |

**Step 5, re-run as #117 did it.** It used the same enumerator binary, the same la_avdecc 4.3.1-beta1 libraries, the same counters probe, and the same arguments and order.
- The counters probe was CLEAN (rc 0, 0 complaints), with a transcript identical to the reference peer's.
- The full enumeration classified the DUT `IEEE17221|Milan`, with no compatibility event, no complaint about the DUT, 0 query errors and 0 AECP retries or timeouts.
- The CRF Stream Input (STREAM_INPUT 1) answered SUCCESS with `counters_valid` `0x00000F3F`, and la_avdecc decoded all ten counters. At #117 it answered `counters_valid` 0, which triggered "[Milan 1.3 - 5.3.8.10] Milan mandatory counters missing".
- The classification was the same in the 300 s registered session and in the final re-run.

**The bind.** The reference peer's CRF input was bound to the DUT's CRF output for 180 s, with the #117 bounded bind tool unchanged. It unbound on the first attempt.
- **Before:** every DUT counter was 0 except AVB_INTERFACE LINK_UP 1 and CLOCK_DOMAIN LOCKED 1.
- **During and after:** only STREAM_OUTPUT 1 moved. STREAM_START and STREAM_STOP went from 0 to 12, MEDIA_RESET and TIMESTAMP_UNCERTAIN stayed 0, and FRAMES_TX restarted at each STREAM_START (#530). The peer counted 79,103 frames.
- **CRF input:** its counters stayed 0, because the assigned bind makes the DUT the talker and nothing streams into its CRF input.
- **Notifications:** the DUT sent 187 unsolicited GET_COUNTERS for STREAM_OUTPUT 1 to the registered controller, 0 of them lost. All were SUCCESS with cdl 148 and mask `0x1F`, and each carried a change. They came at a 1 s period (mean 0.999996 s, σ 0.075 ms). 185 of 186 gaps were within 0.9 ms of 1 s at the controller host; the other, 9.4 s, spans a stream stop. They stopped when the counters stopped.
- No other descriptor's counters changed, and no other descriptor got a GET_COUNTERS push.

**Not proven on silicon.** This run does not show the CRF input counting, or pushing, non-zero values. That needs a bind of the DUT's CRF input to a CRF talker, which this assignment did not include. The root-wire tests `[CTRS-CRF]` and `[NOTIFY-CRF]` remain the evidence for it.

**Method difference from #117.** The inline tap is an instrument and was not used. The controller host captured its own port instead.

**Outside #529 (for the coordinator; no issue filed):**
- `CTLR_DIAG` (0x6F4) is tied to zero at `hdl/milan/milan_datapath.sv:3201`, but REGISTER_MAP describes it as a live tally. The DUT's 6 CONTROLLER_AVAILABLE probes during the run were all answered on the wire.
- The #530 talker behaviour is reproduced: 12 stream restarts, and the first STREAM_START pushed 0.1 ms after a TALKER_DEST_MAC_FAIL probe response.

**Bench state.** Restored.
- The census after matches the one before for all 18 ACMP states: all unbound, with connection count 0.
- The reference peer is unchanged: configuration 0, 96 kHz, clock source 0, the same CRF format.
- All three controller registrations were deregistered with SUCCESS.
- The DUT's CRF talker is idle, and its grader passed 10 of 10.
- The temporary files on the controller host were hash-copied and removed.
- The lock is free. Flash, JTAG, power, wiring and instruments were not touched.

The private packet, with the HANDOFF, raw logs, captures, tool hashes and manifest, is with the coordinator. I am stopping here.

