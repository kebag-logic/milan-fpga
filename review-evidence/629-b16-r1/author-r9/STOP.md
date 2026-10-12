[A603] STOP

Head: `694d7da601a29c099d1d01fd29b61fc23f2160c0` on `629-b16-tone`, one commit on dev `c20c85bd`. Local, not pushed. It adds the dated section "Dev 5603c353, 2026-10-12: lane B16" to `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, with its Contents line and the introduction's pointer, and updates its row in `docs/findings/README.md`. No other file changes. Every gate is rc 0 at the head. Refs #629.

**Condition:** step 2 of the [B16 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117305187): "If the tone is absent here, record the per-channel levels for each source output channel that the documented wiring allows, read the source's routing read-only, and STOP".

**Evidence:**
- The identity gate passed first, at 05:45 CEST: entity_id `020000fffe000001`, entity name "Milan FPGA 1x1 TDM8", firmware_version "2.96.0" and serial "AX7101-0001" over ATDECC; console ID `4d494c4e`, VERSION `00020060`; AEM CRC32 `5ba355eb` over 7,512 bytes; live ENTITY and CONFIGURATION byte-equal to the QSPI AEM; the clock sources of #629; grader 10/10. The bench was in lane B15's end state, and the SoC board's McASP playback was closed.
- Lane B15's tone (997 Hz and 9,973 Hz at -20 dBFS, `d9684a8f...`) played into the peer's talker inputs through the same authorised source from 05:55:38 to 06:02:00 CEST.
- The loopback, twice: the peer's STREAM_INPUT 0 was unbound from the DUT's AAF talker and bound to the peer's own STREAM_OUTPUT 0 under the binding rule (the listener took the talker's `0205022001006000`, read back). The bind answered SUCCESS with connection count 1, but no stream formed:

| Run | Window, CEST | Listener, polled every 2 s (14 reads) | Talker connection count | The peer's talker on its link and the DUT's link | The peer's digital output at the external capture |
|---|---|---|---|---|---|
| `loop1` | 05:56:31 to 05:57:31 | Stream ID and destination 0, flags `0x0002`, MEDIA_LOCKED 0, FRAMES_RX 0 at every read | 0 at every read | 0 PDUs (taps 30.6 s) | Its two channels: every word zero, 22 s |
| `loop2` | 05:59:18 to 06:00:29 | The same | 0 at every read | 0 PDUs (taps 52.5 s, started before the bind) | Its two channels: every word zero, 16 s |

- Why, from `loop2`'s peer-link tap: 99.6 ms after the BIND_RX command, the peer answered BIND_RX (SUCCESS, stream ID 0) and sent PROBE_TX (IEEE 1722.1's CONNECT_TX) for its own talker onto the network; it repeated it 200 ms later. No PROBE_TX response and no further probe appear in the remaining 49 s. A switch does not send a frame back out of the port it came in on, and the peer evidently does not answer its own probe internally, so its listener never learns the stream and its talker never starts. Lane B15's `pts1` read the same (flags `0x0002`, stream ID 0, counters 0, output zero); its tap did not cover the bind.
- So the working loopback the maintainer reports is not this bind on this network path; the step where the setups differ is the bind itself.
- The tone source, read only (state read at 05:48 and 06:01, identical; meters passively): the playback reaches the outputs the documented wiring uses at 0 dB (-20.0 dBFS before their -18.5 dB output setting, -38.5 dBFS leaving), as lane B15 read. It now also reaches a second pair of outputs, -20.0 dBFS before a +6.0 dB setting, -14.0 dBFS leaving, which lane B15 read silent with the same setting: that route changed between the two lanes, outside this lane. Nothing was written.
- Tool controls before any grade: lanes B6 and B9's byte-equal to lane B15's; the tap decode 8 of 8 (lane B15's 5 plus 3 for its lower presence floor, -100 dBFS); a full-value alignment for step 4, 6 of 6 (one new control that lane B15's low-byte key misses).

**Per-run table:**

| Run | Window | Result |
|---|---|---|
| Identity gate | - | PASS |
| Tool controls | - | PASS |
| Step 2, `loop1` | 05:56:31 to 05:57:31 CEST | No stream formed; TONE ABSENT at the peer's output: STOP |
| Step 2, `loop2` (taps over the bind) | 05:59:18 to 06:00:29 CEST | The same; the unanswered PROBE_TX recorded |
| Step 3, the talker stream with the loopback carrying the tone | - | NOT RUN: no loopback; the talker sent no PDU |
| Step 4, Direction B end to end; B0, B-CRF, B-AAF | - | NOT RUN: STOP at step 2 |
| #629 bench quality metric | - | NOT met for Direction B, unchanged; #645 stays open |

**State as left:**
- The tone is stopped and its playback closed.
- The peer's STREAM_INPUT 0 is bound back to the DUT's AAF talker at `0205022002006000` and its STREAM_INPUT 8 to the DUT's CRF talker, its clock source as found (never set). The DUT is unbound on INTERNAL with its formats and maps as found (never bound). All read back; census 45 of 46 equal (the other is the DUT's live propagation delay).
- The SoC board's McASP playback is free and its bridge legs as found (never stopped); the controller staging removed; no file on the tap host; the bench lock free; nothing left running.
- Residuals: the DUT's AAF talker counted two more stream stops and starts (the peer's unbinds and rebinds); the peer's STREAM_INPUT 0 counters restarted at the rebinds; DUT NVM and `SLIP_LB` unchanged.

**Needed to resume:** the owner's description of the working loopback (its network path and how it is bound), or a ruling to run lane B15's four-point capture with the DUT's listener bound to the peer's talker, which shows directly whether the talker now carries the tone given the source's new route. Step 4 and B0, B-CRF and B-AAF can then run with the lane's tools.
