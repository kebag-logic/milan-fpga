[A403] REVIEW READY

Refs #451. Local head: `6339479d69830614d4267bd3170113737afbf8f4` on `451-tdm8-first-light` (parent `4f06bfc762724a71999371840a36fadfc1cf08d9`, then the STOP head `361d1f47`), base `6d5ebd7357c1e468e446f18a61527c5be6118a04`. Nothing amended; no push or PR creation performed.

**DIN first light is now established in all eight slots, and DOUT has not regressed.** My STOP above was wrong about the cause of the all-zero DIN: it was not the wiring. In this image STREAM_PORT_OUTPUT 0 has a dynamic audio map. `ADP_DMAP_OUT_MASK_C` bit 0 is set in the `endstation_ax7101_1x1_tdm8` shape, and GET_AUDIO_MAP on that port answers `number_of_maps` 1. That makes the capture crossbar feed the talker (`hdl/milan/milan_datapath.sv` line 1344), and with an empty map every channel is digital silence. The first session left that map empty. The owner's wire check was prompted by my incorrect inference.

Changed: `docs/findings/451_TDM8_FIRST_LIGHT.md` only, in two commits. `4f06bfc7` records the result. `6339479d` rewords one line, because gate 7 rejected a retired-stack word.

Second session (2026-09-28, bench actions 16:00 to 16:22 CEST):

- **SoC read-only first.** Same boot, image build #6, both bridge legs running. McASP0 receive DMA ran at 249.8 periods/s, so BCLK and FSYNC still arrive. The DUT was on the same boot: its slip counter was continuous, and VERSION, `PP_STAT` and every control word were unchanged. The bridge legs were stopped by PID.
- **Pattern source.** The SoC board's USB function was not visible on the bench host. The SoC board built the 65,536-frame pattern period itself (SHA-256 equal to the host pattern) and played it in a loop, so the bytes played equal the first session's.
- **DIN run 1, exactly as before:** all 4,554,432 frames zero; 0 AVTP sequence gaps.
- **DIN run 2:** the same, plus eight identity mappings on STREAM_PORT_OUTPUT 0. Stream channel `c` comes from cluster `c`, which the generated source table puts on TDM input slot `c`. The mappings were removed afterwards and the map read back empty.
- **DOUT sanity, 3 s, method unchanged.** The capture came off over the serial console as gzip plus base64, with SHA-256 checked on both ends.

DIN: SoC transmit toward the DUT talker stream, routed, 70 s.

| SoC playback channel | Pattern tag | TDM slot | Output cluster | Recovered tag | Recovered stream channel | Valid words | Result |
|---|---|---|---|---|---|---|---|
| 0 | 1 | 0 | 0 | 1 | 0 | 3,360,035 | In order |
| 1 | 2 | 1 | 1 | 2 | 1 | 3,360,035 | In order |
| 2 | 3 | 2 | 2 | 3 | 2 | 3,360,035 | In order |
| 3 | 4 | 3 | 3 | 4 | 3 | 3,360,035 | In order |
| 4 | 5 | 4 | 4 | 5 | 4 | 3,360,035 | In order |
| 5 | 6 | 5 | 5 | 6 | 5 | 3,360,035 | In order |
| 6 | 7 | 6 | 6 | 7 | 6 | 3,360,035 | In order |
| 7 | 8 | 7 | 7 | 8 | 7 | 3,360,035 | In order |

DOUT: DUT listener stream toward the SoC capture, first session, 70 s. The second session's 3 s capture repeated it: all 144,000 frames held their own tag in every channel, with 0 torn and 0 invalid words.

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

Continuity:

- **DIN, 70.001 s of playback.** All 3,360,035 frames carried a valid word of its own channel's tag in every channel. Every channel steps by one ordinal per frame, except at 35 or 36 INTERNAL-beat clusters. The clusters are spaced 93,990 to 93,993 frames, and each nets one repeated frame: 0.51 per second, the slip the DUT counts. There were 0 AVTP sequence gaps in 758,870 PDUs. Outside playback the DIN line reads all ones, so a zero word cannot come from the pin.
- **DOUT, 3 s.** 0 torn, 0 invalid. The only discontinuities are two beat clusters 93,989 frames apart, each netting one drop.
- **Frame-rate offset.** `SLIP_TDM` counted 0.5108 dups/s over 8,244.7 s across both sessions, which is 10.64 ppm and matches the -10.64 ppm plan.

**Open risk: DIN frame coherence, for triage as a separate issue (not filed).** The two channels of each TDM pair always agree. Pairs 1 to 3, however, carry the previous TDM frame in 67.5% of frames:

- `[0,0,-1]`: 22.7%;
- `[0,-1,-1]`: 22.7%;
- `[-1,-1,-1]`: 22.2%.

The state cycles once per 1.958 s beat. Each pair's hold in `KL_chan_map_capture.sv` is written by its own pulse (lines 486 to 487). The media tick reads the latest hold of each pair with no frame-wide buffer (lines 958 to 960). This is a DUT capture-path property, not the link.

Restoration: both legs restarted with the bridge script's command lines, and status reports both running. The DUT maps are empty and all streams unbound. The census matches in 32 of 33 entries, all but the live propagation delay. `PP_STAT` and every control word are unchanged. The controller is clean and the lock is released. The residuals are as in the STOP. The SoC board's USB function is still not visible on the bench host, as at the start of the session; that needs the owner.

Validation at `6339479d`, all rc 0, unpiped, from the physical path: `scripts/docs_check.py`, `scripts/check_doc_style.py`, `scripts/gen_toc.py --check`, `scripts/check_em_dash.py --base 6d5ebd73`, `scripts/check_doc_paths.py`, `scripts/ci_scope.py --selftest`, `scripts/check_baremetal_only.py --check`, `git diff --check` (also `6d5ebd73 HEAD`). All eleven page tables pass rendered and source cell-count checks.

NOT RUN, owner items: the recorded continuity check, scope measurements, #386 acceptance 4 and the calibrated #117 listener-audio sequence.

Packet `451-a403` adds the second session's redacted evidence, tools and raw-artifact index. No issue closure or review approval is claimed.
