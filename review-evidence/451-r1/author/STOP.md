[A403] STOP

Refs #451. Local head: `361d1f47fe29ada509f99813001369188217eaaa` on `451-tdm8-first-light`, base `6d5ebd7357c1e468e446f18a61527c5be6118a04`.
Findings: `docs/findings/451_TDM8_FIRST_LIGHT.md`; the attempt page is removed in the same commit. No push or PR creation performed.

**DOUT first light is established. DIN is not.** While the SoC transmitted the pattern for 70 s, the DUT talker stream carried only zero words. BCLK, FSYNC and DOUT are shown working by the DOUT decode, so this is a wiring or physical question for the owner: J11.7 to P1.02, the SoC's AXR0 pad on P1.02, or its transmit setup. The image does connect the `tdm` resource's `din` pad (F20) to the capture master.

Identity gate PASS: VERSION 00020060; ROM CRC 9b6576a9; QSPI payload CRC 3c18c276; AEM CRC 93742dd2; ENTITY and CONFIGURATION replies byte-identical to verified payloads. SoC read-only health came first. The bridge was running on the repaired board, and McASP0 is a slave (`dsp_a`, codec side is bit-clock and frame master, 8 x 32-bit slots) receiving clocks: 249.7 receive periods of 192 frames per second with the bridge up, and a direct 3 s capture of 144,000 frames in 3.05 s.

Pattern: 24-bit sample `(tag << 16) | (ordinal & 0xffff)` in bits 31:8, tag = channel + 1.

- DOUT used a software AAF talker on the controller host: an untagged unicast diagnostic transport, paced on gPTP time, timestamps +2 ms. DUT STREAM_INPUT 0 was bound, with identity mappings on STREAM_PORT_INPUT 0, and McASP0 was captured directly.
- DIN used direct McASP0 playback. The controller joined gPTP as a slave and declared an MSRP Listener Ready. The DUT admitted a real reservation and streamed.

DOUT: DUT listener stream toward the SoC capture.

| SoC capture channel | Mapped stream channel | TDM slot | Recovered tag | Recovered stream channel | Valid words | Result |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 1 | 0 | 3,357,952 | In order |
| 1 | 1 | 1 | 2 | 1 | 3,357,952 | In order |
| 2 | 2 | 2 | 3 | 2 | 3,357,952 | In order |
| 3 | 3 | 3 | 4 | 3 | 3,357,952 | In order |
| 4 | 4 | 4 | 5 | 4 | 3,357,952 | In order |
| 5 | 5 | 5 | 6 | 5 | 3,357,952 | In order |
| 6 | 6 | 6 | 7 | 6 | 3,357,952 | In order |
| 7 | 7 | 7 | 8 | 7 | 3,357,952 | In order |

DIN: SoC transmit toward the DUT talker stream.

| SoC playback channel | Pattern tag | Expected TDM slot | Expected stream channel | Recovered words | Result |
|---|---|---|---|---|---|
| 0 | 1 | 0 | 0 | 4,550,280 zero | Not decoded |
| 1 | 2 | 1 | 1 | 4,550,280 zero | Not decoded |
| 2 | 3 | 2 | 2 | 4,550,280 zero | Not decoded |
| 3 | 4 | 3 | 3 | 4,550,280 zero | Not decoded |
| 4 | 5 | 4 | 4 | 4,550,280 zero | Not decoded |
| 5 | 6 | 5 | 5 | 4,550,280 zero | Not decoded |
| 6 | 7 | 6 | 6 | 4,550,280 zero | Not decoded |
| 7 | 8 | 7 | 7 | 4,550,280 zero | Not decoded |

Continuity:

- **DOUT, 70 s.** 3,357,952 frames, 0 torn frames, 0 invalid words; slot order is the identity with no rotation. There were 2,173 repeated and 2,191 dropped whole frames, net 18 dropped. 34 clusters are the documented INTERNAL beat, one per 93,990 frames (1.958 s), netting one drop each. 17 are render-queue underruns from software-talker jitter; 9 follow a logged lateness of 150 us or more. The DUT listener reported 0 sequence mismatches and 0 depacketizer drops, media stayed locked, and ts_delta read 1.98 ms.
- **DIN, 70 s of playback inside a 94.8 s stream.** 758,380 PDUs with 0 sequence gaps, and all content zero. The SoC transmit DMA consumed the pattern: 1,648 periods of 2,048 frames.
- **Frame-rate offset.** SLIP_TDM counted 0.5109 dups/s over 2,303.7 s, which is 10.64 ppm and matches the -10.64 ppm divider plan. The pin-level beat agrees.

What changed since the attempt:

- The SoC board was repaired: its image now carries a BCDMA cyclic-receive fix.
- A slave-only gPTP daemon on the controller port, run per action, puts that port inside the SRP domain. The attempt's controller port was outside it, which explains its empty DIN recordings.
- The talker now answers PROBE_TX.
- File transfers are now binary-safe.

Restoration: all 18 stream states are unbound, and both DUT audio maps are empty. Clock sources and rates and every DUT control word are as before, with SYNC=1, ASCAPABLE=1 and TU=0. The SoC bridge legs were restarted with the script's own command lines, and status shows both running. The controller is clean and the lock is released. The census matches in 28 of 30 entries; the other two are the live propagation delay and DUT output 0 now reporting its MAAP destination.

Residuals:

- DUT output 0 now reports its MAAP destination address.
- `PP_STAT` nvm_pend is set, as the attempt also left it.
- The controller NIC clock is left at the daemon's frequency, with hardware timestamping on.

Operator error, disclosed: the first census sent AEM `0x002A` (REBOOT) twice, intending GET_AUDIO_MAP. Both were refused with NOT_IMPLEMENTED, and no reset occurred: the counters stayed continuous and the MAAP state was unchanged.

NOT RUN, owner items: electrical continuity, scope measurements, #386 acceptance 4, and the calibrated #117 listener-audio sequence. The DIN path above is also for the owner.

Validation at the local head, all rc 0, unpiped, from the physical path: `scripts/docs_check.py`, `scripts/check_doc_style.py`, `scripts/gen_toc.py --check`, `scripts/check_em_dash.py --base 6d5ebd73`, `scripts/check_doc_paths.py`, `scripts/ci_scope.py --selftest`, `scripts/check_baremetal_only.py --check`, `git diff --check` (also `6d5ebd73 HEAD`). All nine page tables pass rendered and source cell-count checks.

Packet `451-a403` holds the handoff, PR body, manifest, redacted evidence, tools and a raw-artifact index. No issue closure or review approval is claimed.
