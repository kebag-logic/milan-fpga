[A603] STOP (B16b)

Head: `0d4ff91952bf46f786e08c7da24ffe777ba166da` on `629-b16-tone`, one new commit on `694d7da6` (no rebase, no amend). Local, not pushed. It adds a B16b part to lane B16's dated section in `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (ten `B16b:` subsections, its Contents line and the introduction's pointer) and updates its row in `docs/findings/README.md`. No other file changes. Every gate is rc 0 at the head. Refs #629.

**Condition:** step 4 of the [ruling](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117672835): B-CRF and B-AAF need a decision. As found, and as the B16 restore keeps it, the peer's CLOCK_DOMAIN follows its CRF input, which is bound to the DUT's CRF talker. Both of the peer's talkers therefore run on a clock that follows the DUT's. B-CRF and B-AAF set the DUT to follow one of those talkers, so the DUT would follow its own clock through the peer: a closed loop with no independent reference, which does not test following. The clock-source rule allows a set on the listener only, and in both cases the peer is the talker, so this lane cannot put the peer on its internal source. Lanes B7 and B8 found the peer there, and lanes B9 and B10's run tools refuse to start otherwise. The lane ran B0 and stopped before B-CRF and B-AAF.

**Evidence:**
- The identity gate passed again at 06:22 CEST, every fact as in B16. The bench was as B16 left it: census 45 of 46 equal, the other the DUT's live propagation delay. The SoC board's McASP playback was closed at every check: no music was playing.
- Lane B15's four-point capture ran with the DUT's STREAM_INPUT 0 bound to the peer's AAF talker under the binding rule (the formats were already equal; nothing was set). THD+N is the median over one-second blocks, at 997 Hz on channel 0 / 9,973 Hz on channel 1; SNR equals minus THD+N within 0.01 dB.

| Run | Window, CEST | (a) The peer's talker, its link | (b) The DUT's link | (c) The DUT's TDM output, McASP0, 10 s | (d) The external capture | (c) against (a) and (b) |
|---|---|---|---|---|---|---|
| `pts1` | 06:23:39 to 06:24:28 | PRESENT at -14.1353 dBFS, +6.94 ppm; -108.74 / -88.87 dB | PRESENT; -107.17 / -87.26 dB | PRESENT; -105.27 / -85.33 dB | No control in this mode | SAMPLE-EXACT, 480,000 of 480,000 frames |
| `pts2`, with the positive control | 06:28:06 to 06:28:56 | PRESENT at -14.1353 dBFS, +6.96 ppm; -107.72 / -87.82 dB | PRESENT; -108.33 / -88.44 dB | PRESENT; -109.70 / -89.87 dB | Lane B6's loop at -1.00 dBFS, at the loop's floor in 13 of 16 blocks; two 2-frame repeats that neither tap carries | SAMPLE-EXACT, 480,000 of 480,000 |
| `pts3` | 06:48:55 to 06:49:45 | PRESENT at -14.1035 dBFS, 0.000 ppm; -123.93 / -122.47 dB | PRESENT; -123.93 / -122.47 dB | PRESENT; -123.97 / -123.97 dB | No control in this mode | SAMPLE-EXACT, 480,000 of 480,000 |

- Step 4, B0: `b0-2`, 06:37:31 to 06:43:17 CEST. The DUT stayed on INTERNAL, with the peer's CRF talker bound to its STREAM_INPUT 1 and its AAF talker to STREAM_INPUT 0. Over 300 s at McASP0:
  - THD+N -123.95 / -122.80 dB median, worst -100.47 / -80.48 dB;
  - at the path's floor (169 of 300 blocks), -123.98 / -123.95 dB;
  - level -14.10 dBFS, offset 0.0000 ppm, phase drift 0.0005 frames;
  - 0 discontinuities;
  - (c) equal to (a) and (b) sample for sample over the 34.1 s the taps cover;
  - (d) lane B6's loop with 0 discontinuities in 14,583,286 decoded frames;
  - the DUT's servo IDLE and `SLIP_TDM` static.
- Attribution: every impairment is already in the peer's talker stream at (a). That covers the path's floor, 131 degraded blocks that hold no discontinuity, and, before 06:29, the +6.95 ppm offset with a floor 13 to 34 dB higher. The network and the DUT add none: every one of the 3,077,452 frames compared against (a) is equal. No DUT fix is needed.
- The tone source, read only: its clock setting changed between 06:23 and 06:50 CEST, outside the lane. Four of the 1,255 state entries both reads hold differ, and the lane wrote none of them. With the change, the tone at (a) stepped from +6.95 ppm and -14.1353 dBFS to 0.000 ppm and -14.1035 dBFS, between 06:28:50 and 06:31:52 CEST. `pts3`, without the CRF bind, reads as B0, so the bind did not cause it. `pts2`'s two repeats at (d) also stopped. The tone's level at (a) is the level at which the source's meters show it leaving the second output pair, -14.0 dBFS; lane B15 read that pair silent.
- Two incidents, neither in a graded window:
  - Run `b0` (06:31 to 06:37): McASP0's recording found the device busy, because the wrapper did not yet stop the to-host leg for the new mode. Nothing else was affected. The wrapper was fixed and `b0-2` re-ran the case.
  - The tone's playback underran five times, 06:45 to 06:46 CEST, during offline grading on the bench host.

**Per-run table:**

| Run | Result |
|---|---|
| Identity gate | PASS |
| Tool controls | PASS: B16's, and the loop decode's planted control |
| `pts1`, `pts2`, `pts3`: the four points | TONE PRESENT at (a), (b) and (c); (c) sample-exact to (a) and (b); (d) positive control PRESENT in `pts2` |
| `b0` | Incident: no McASP0 recording; B0 not graded on it |
| B0 (`b0-2`) | Graded: THD+N -123.95 / -122.80 dB, 0 discontinuities; no loss in the network or the DUT |
| B-CRF, B-AAF | NOT RUN: decision needed. STOP |
| #629 bench quality metric | Direction B graded at INTERNAL only; the following cases wait. #629 stays open |

**State as left (verified by census and counters at 06:52 CEST):**
- the DUT unbound on INTERNAL, its formats and maps as found;
- the peer's STREAM_INPUT 0 bound to the DUT's STREAM_OUTPUT 0, its STREAM_INPUT 8 to the DUT's STREAM_OUTPUT 1, its clock source as found (never set);
- the tone stopped;
- the SoC board's McASP playback free, the to-host leg running with its recorded line, the from-host leg dead as found;
- the controller staging removed, no file or capture on the tap host, the bench lock free, nothing left running.

Residuals: the peer's AAF talker counted five more stream starts and stops (one per DUT bind), its CRF talker two. `SLIP_LB` went 152 to 162 dups (five slipped frames over five binds; #645). DUT NVM went seq 276 to 286.

**Needed to resume:** a decision between:
1. a set of the peer's CLOCK_DOMAIN to its internal source for B-CRF and B-AAF, read back, and restored to the as-found source with a read-back (an exception to the clock-source rule);
2. B-CRF and B-AAF run in the loop as found, reported as loop cases, not as following;
3. step 4 closed on B0.
