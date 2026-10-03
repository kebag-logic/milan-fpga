[A521] STOP

Head: `c17997fbc72f9611e9b69264c89245536adf8697` on `629-b8-bench`, one commit on PR #644's head `40714c1b`. Local, not pushed. It adds the dated section "Dev bbf704ec, 2026-10-03: lane B8" to `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, which records this STOP, and updates its row in `docs/findings/README.md`. Every docs gate is rc 0 at the head.

**Condition:** "a tone that does not reach the peer's talker" (the [B8 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5970760794)'s STOP list).

**Evidence:**
- The identity gate passed first, every check equal to the build's, as in lane B7.
- Lane B6's two tones, 997 Hz and 9,973 Hz at -20 dBFS, were played into the reference peer's talker inputs by the owner's method, from 18:04:59 to 18:06:51 CEST. The playback was confirmed running through the proof. No instrument setting was read or changed.
- The proof is lane B7's known-signal probe. Under the binding rule the DUT's STREAM_INPUT 0 took the peer talker's `0205022001006000`, set and read back. Four identity mappings went on STREAM_PORT_INPUT 0, and the bind answered SUCCESS with connection count 1. McASP0 then recorded 10 s (480,000 frames) of the DUT's TDM output, which was graded on the bench host.

| TDM output channel | Level, dBFS RMS | Range, 24-bit LSB | Power within 5 Hz of 997 Hz / 9,973 Hz |
|---|---|---|---|
| 0 | -141.1 | -2 to 0 | 0.04 % / 0.04 % |
| 1 | -141.1 | -2 to +1 | 0.04 % / 0.04 % |
| 2 | -141.5 | -1 to 0 | 0.03 % / 0.04 % |
| 3 | -141.5 | -1 to 0 | 0.04 % / 0.04 % |
| 4 to 7, unmapped | every word zero | 0 | - |

- No channel carries either tone: this is the idle floor lanes B6 and B7 found.
- The stream itself arrived. The DUT's STREAM_INPUT 0 read MEDIA_LOCKED 1 and MEDIA_UNLOCKED 0, with no interruption and no sequence mismatch. Its FRAMES_RX rose by 103,998 across the recording.
- So the peer's talker carries no tone with the owner's method as it stands. Where along that path the tone is lost was not examined, because no setting of it may be read or changed.

**Per-run table:**

| Run | Window | Result |
|---|---|---|
| Identity gate | - | PASS |
| Tone proof | 10 s from 18:05:13 CEST | TONE ABSENT: STOP |
| 1. B0, B-CRF, B-AAF by THD+N and SNR | - | NOT RUN |
| 2. Source switch, AAF to CRF and CRF to AAF | - | NOT RUN |
| 3. CRF lock loss | - | NOT RUN |
| 4. Saved selection across a power cycle | - | NOT RUN; the authorised power cycle was not used |

**State as left:**
- The tone is stopped.
- The DUT is unbound on CLOCK_SOURCE 0, both maps empty, and its STREAM_INPUT 0 format is as found, all read back. The peer is as found.
- The census is 46 of 46 entries equal, and the grader reads 10/10.
- The SoC board's bridge legs are restarted with the recorded command lines.
- The controller's staging is removed, and the bench lock is free.
- Residuals: two NVM commits (the probe's edits and their restores), and `SLIP_LB` +12 dups from the probe's bind on INTERNAL.

**Incident:**
- The playback's first start left the bench lock held for about 1.5 minutes, through a descriptor the detached playback inherited.
- Only this lane's own probe attempt waited on it, and it did nothing.
- The playback was stopped by its process ID and started again with the descriptor closed.

**Needed to resume:** the owner checks the tone's path into the peer's talker inputs. Items 1 to 4 can then run as assigned, the power cycle included.

