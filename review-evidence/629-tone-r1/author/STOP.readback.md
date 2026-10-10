[A588] STOP

Head: `70cd90a42fdc8c9b5059383e657a8b5a26f1da8e` on `629-b15-tone`, one commit on dev `e8454e275`. Local, not pushed. It adds the dated section "Dev 5603c353, 2026-10-10: lane B15" to `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, with its Contents line, the introduction's pointer and the title's image list, and updates its row in `docs/findings/README.md`. No other file changes. Every gate is rc 0 at the head. Refs #629.

**Condition:** step 3 of the [B15 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6097827871), "Tone absent at (a): the loss is upstream of the reference peer's talker, so it is instrument-side ... STOP with the evidence, because the owner decides instrument changes."

**Evidence:**
- The identity gate passed first, at 15:17 CEST: entity_id `020000fffe000001`, entity name "Milan FPGA 1x1 TDM8", firmware_version "2.96.0" and serial "AX7101-0001" over ATDECC; console ID `4d494c4e`, VERSION `00020060`; AEM CRC32 `5ba355eb` over 7,512 bytes; live ENTITY and CONFIGURATION byte-equal to the QSPI AEM; the clock sources of #629; grader 10/10.
- Lane B9's loop (997 Hz and 9,973 Hz at -20 dBFS, `d9684a8f...`) played through the authorised tone source from 15:26:59 to 15:35:31 CEST. Its own meters, read passively, show the tone leaving it at -38.5 dBFS on the outputs that carry it (playback -20.0 dB, an output level setting read as -18.5 dB). No instrument setting was changed.
- The peer's AAF talker was bound to the DUT's STREAM_INPUT 0 under the binding rule (formats already equal). Four points were captured at once, twice: (a) the peer's talker stream on the peer's own link tap; (b) the same stream on the DUT's link tap; (c) McASP0's 10 s recording of the DUT's TDM output; (d) the external capture.

| Run | Point | Channels 0 / 1 / 2 / 3, dBFS RMS | Range, LSB | 997 Hz / 9,973 Hz | PDUs, sequence gaps | Capture SHA-256 |
|---|---|---|---|---|---|---|
| pts1 | (a) | -141.09 / -141.10 / -141.48 / -141.49 | -2 to +1 | Absent / absent (0.04 % of power within 5 Hz) | 191,843, 0 | `6abff905...` |
| pts1 | (b) | the same | -2 to +1 | Absent / absent | 191,842, 0 | `3e1d81ba...` |
| pts1 | (c) | the same; 4 to 7 zero | -2 to 0 | Absent / absent | - | `7e059d75...` |
| pts1 | (d) | Exact zero: the peer's listener was bound to its own talker, which a switch cannot deliver; unusable | - | - | - | `7040fae1...` |
| pts2 | (a) | -141.09 / -141.10 / -141.48 / -141.48 | -2 to +1 | Absent / absent | 191,639, 0 | `9d408d76...` |
| pts2 | (b) | the same | -2 to +1 | Absent / absent | 191,637, 0 | `88c41bc5...` |
| pts2 | (c) | the same; 4 to 7 zero | -2 to 0 | Absent / absent | - | `1a331755...` |
| pts2 | Positive control: lane B6's loop played into the DUT's TDM input, on the DUT's talker at both taps and at (d) | -1.00 dBFS per block on its two channels | - | Present / present: 997.0000 and 9,973.0000 Hz, SNR 146.07 / 145.99 dB, THD+N at the loop's 24-bit floor in every block wholly inside the playback | 0 gaps | `9d408d76...`, `88c41bc5...`, `fa771dcc...` |

- (c) equals (b) sample for sample in both runs: 480,000 of 480,000 frames on the four mapped channels, the first 256-frame window matching the stream at one offset only, 0 slips (`align_b15.py`, 5 of 5 planted controls PASS). The DUT's STREAM_INPUT 0: MEDIA_LOCKED 1, MEDIA_UNLOCKED 0, no interruption, sequence mismatch, late, early or invalid timestamp.
- So the peer's talker carries no tone on its own link, and the DUT renders exactly what it receives. The loss is upstream of the peer's talker.
- Read only, as the branch asks: the peer's GET_AUDIO_MAP takes its talker's channels 0 to 3 from its output port's clusters by identity; those clusters take their signal from its AUDIO_UNIT 0; its model declares no jack, external or internal port and one control, IDENTIFY. Its input path is not observable over ATDECC.

**Per-run table:**

| Run | Window | Result |
|---|---|---|
| Identity gate | - | PASS |
| Tool controls | - | PASS: lanes B6 and B9's byte-equal to lane B10's; tap decode 5 of 5; alignment 5 of 5 |
| pts1, four points | captures from 15:27:28.7 CEST | TONE ABSENT at (a), (b), (c); (d) unusable |
| pts2, four points and the positive control | captures from 15:31:13.1 CEST | TONE ABSENT at (a), (b), (c); the control present at both taps and (d) |
| DUT stage localisation and fix | - | NOT RUN: the DUT does not lose the tone |
| B0, B-CRF, B-AAF by THD+N and SNR | - | NOT RUN: no tone reaches the DUT |
| #629 bench quality metric | - | NOT met for Direction B, unchanged; #645 stays open |

**State as left:**
- The tone is stopped and its playback closed (0 underruns).
- The DUT is unbound on CLOCK_SOURCE 0, STREAM_INPUT 0 format and both maps as found. The peer is as found, its listener bound to the DUT's AAF talker and its clock on the DUT's CRF. All read back; census 45 of 46 equal (the other is the DUT's live propagation delay).
- The SoC board's to-host leg runs under a new process ID with its recorded line; the from-host leg is dead, as found.
- Controller staging removed, no file left on the tap host, the bench lock free, nothing left running.
- Residuals: four NVM commits (the binds and unbinds), `SLIP_LB` +6 dups.

**Incident:** pts1's restart of the to-host leg checked for a running leg with a `ps` pattern that matched its own command line, so the leg stayed down from 15:27:23 to 15:28:23 CEST. It was restarted under the lock and the check now reads the bridge's `status`.

**Needed to resume:** the owner checks the tone's path into the peer's talker channels. With a tone at (a), pts2's method grades the whole chain, and B0, B-CRF and B-AAF can run.

