[A453] REVIEW READY
Commit: `6dfa64a7506a8660a70d77eaa7c96c5de2886f5d` on `b3-bench-0930`, one commit on dev `ec0cc0c1df7d7ab3e25d973958f53f0074393d2c`. Local only, not pushed; no PR created.
Changed (documentation only, two new pages, one per issue):
- `docs/findings/617_DIN_FRAME_COHERENCE_BENCH.md`: #617 acceptance 4.
- `docs/findings/451_USB_AUDIO_CAPTURE.md`: #451 capture through the USB Audio device, and the continuity check.

Bench actions 2026-09-30, 05:26 to 05:50 CEST, each under the bench lock. No flash, power, wiring, instrument or USB gadget action.

**Identity gate: PASS.** VERSION `00020060`; AEM CRC `93742dd2`; entity `020000fffe000001`. ENTITY (312 B) and CONFIGURATION (106 B) from AECP are byte-equal to the AEM bytes the console dumps from QSPI. NVM slot B seq 230 authoritative, `backed=1`; grader 10/10. ROM CRC `acad92b9` (as on `13eda870`); QSPI payload CRC `d178f19a` (`13eda870`: `d84bce7b`).

**#617 acceptance 4: PASS, 0 torn frames.** The first-light DIN method: SoC-built pattern period (same SHA-256), 70 s playback into McASP0, eight identity mappings on STREAM_PORT_OUTPUT 0, software SRP listener. Torn = a frame whose valid words carry more than one ordinal (samples from two TDM frames).

| Run | Frames | Torn | Invalid words | Order | Discontinuities | Result |
|---|---|---|---|---|---|---|
| `din-long` (DIN, talker stream) | 3,360,036 in the playback region, 4,551,624 recorded; 758,604 PDUs, 0 sequence gaps | 0 in the region, 0 in the recording | 0 | Identity | 36 whole-frame repeats at the same frames in all 8 channels, 93,990-93,993 apart (the 1.958 s INTERNAL beat); `SLIP_TDM` dups +36 over the playback, skips 0 | PASS |
| `dout-long` (DOUT, McASP0 direct, 70 s) | 3,360,000 | 0 | 0 | Identity | 36 beat clusters (696 repeated, 732 dropped, net one drop each); 23 underrun clusters (12 after logged talker lateness, 11 without); listener errors 0, depacketizer drops 0, ts_delta 1.98 ms | PASS |

First light on `9e9954e9` counted 2,267,868 of 3,360,035 DIN frames torn (67.5%), with pair offsets 0/0/-1, 0/-1/-1 and -1/-1/-1. Here every frame is 0/0/0, and the first stop-tail frame is all zero instead of torn.

**#451 capture through the USB Audio device: FAIL, no STOP condition.** The same DOUT method, with the SoC board's bridge left running as found, and 75 s recorded on this host's USB Audio card. Both captures ran full length; the card stayed present; the bridge was not changed.

| Run | Frames | Pass the pattern rule | Silent frames (stretches) | Slot order kept | Rotated by 1-7 words | Rotation changes | Longest run in one rotation | Result |
|---|---|---|---|---|---|---|---|---|
| `usb-long` | 3,600,000 | 0 | 327,339 (2,420) | 344,438 (9.6%) | 2,919,511 | 2,833 | 2,922 frames | FAIL |
| `usb-long2` | 3,600,000 | 0 | 3,244 (4) | 428,820 (11.9%) | 3,166,358 | 238 | 95,998 frames | FAIL |

About 97.5% of words carry a non-zero low byte: the values are interpolated, as by the bridge's sample-rate-converting copy. The channel order moves by whole 32-bit words. The direct McASP0 path is bit-exact on the same image, so the loss is between McASP0 receive and this host's capture buffer; it is not located further.

**#451 continuity check: NOT RUN.** It needs a meter on the unpowered boards; this lane may not power down, or change wiring or instruments. The DIN and DOUT data show that the four signal conductors reach the right pins; the grounds and wire resistances are not measured.

**Restore: done and proven.** Bridge legs running with the recorded command lines (PIDs 1498/1499 replace 1224/1225); SoC on the same boot, USB function configured, fault scan 0, no task file left. All 18 stream states unbound; both DUT maps empty; census 33/33 equal to the start; DUT control words equal. The controller clock frequency reads back as found, and is back on its recorded trajectory (4.4 us); timestamping as found; no gPTP daemon. The bench lock is free. Residual: the method's map and bind edits made the DUT persist its state. NVM commits went 0 to 6 (slots 229/230 to 235/236), with `pend=1` and `PP_STAT` bit 11 set.

Validation at `6dfa64a7`, all rc 0, unpiped, from `$LANES/b3-bench-0930`, Markdown gates in the pinned environment:
- `docs_check.py`;
- `check_doc_style.py`;
- `gen_toc.py --check`;
- `check_em_dash.py --base ec0cc0c1` (0 findings over 474 added lines);
- `check_doc_paths.py`;
- `ci_scope.py --selftest`;
- `check_baremetal_only.py --check`;
- `check_feature_status.py --self-test`;
- `git diff --check`, and `git diff --check ec0cc0c1 HEAD`.

Both pages' tables pass the rendered and source cell-count check.

Acceptance criteria:
- #617 acceptance 4: MET, 0 torn frames.
- #451 capture through the USB Audio device: NOT MET, both runs FAIL.
- #451 continuity check: NOT RUN, with the reason recorded.

Open risks/questions:
1. The findings index has no row for the two pages: the assignment allowed no other doc edit.
2. Locating the USB-path loss needs a change on the SoC board or this host, for example with the bridge's rate conversion off. That is outside this lane.
3. #451's playback direction through the USB Audio device was not assigned; it stays NOT RUN.

Packet `b3-a453`: handoff, PR body, manifest, tools, redacted per-action evidence, gate outputs and the raw-artifact index. No issue closure or review verdict is claimed.
