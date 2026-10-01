[A468] STOP

Refs #451, the timing item, second session. Local head `4461a1f7db55f4c37bc6dd8363c114deeb85eee2` on `b4-bench-1001`: one commit on `35a8b04d` (the first session's attempt record), with a one-line subject. It replaces the attempt record in `docs/findings/451_TDM8_TIMING_SOC_BOARD.md` with the measured result and updates that page's row in `docs/findings/README.md`. Nothing was pushed, and no PR was opened.

**STOP: the bench host lost the SoC board's USB function 475.7 s into the 630 s capture, and its USB Audio card is gone.** The owner must re-attach it. At 04:25:01Z the bench host's USB host controller logged "Set TR Deq Ptr cmd failed due to incorrect slot or ep state", and the device disconnected 1.1 ms later. The SoC board logged "remote wakeup not configured" about 0.15 s before that. The capture was streaming over the USB network link at 1.536 MB/s, and the cause is not established. The device did not come back, and no USB function, gadget or UDC action was taken. At 04:31:24Z another USB audio device, not part of this lane, enumerated on the bench host.

The owner's root shell was confirmed with `id` (uid 0). No credential was typed or stored.

| #451 timing item | Verdict | Evidence |
|---|---|---|
| Identity gate, dev `ec0cc0c1` | PASS (first session; the second ran on the same DUT boot, with control words unchanged) | VERSION `00020060`; AEM CRC32 `93742dd2`; ROM `acad92b9`; QSPI payload `d178f19a`; ENTITY and CONFIGURATION byte-equal to QSPI; grader 10/10 |
| Framing record | Recorded | `dsp_a`; the codec side (DUT) is bit-clock and frame master; 8 slots x 32 bits on both DAIs; McASP0 AXR1 receives, `rx-num-evt` 32; capture `S32_LE`, 8 channels, 48000 (48000/1), period 2,048, buffer 16,384, timestamps MONOTONIC |
| Data one BCLK after the frame-sync edge: bit-exact, all eight slots, in order | PASS, as far as the SoC board shows | 22,831,104 frames: 0 torn, 0 invalid, 0 zero words; channel c = slot c = tag c+1 |
| FSYNC at 48 kHz | fs 47,997.947 Hz on the SoC board's clock | -42.8 ppm against 48 kHz, -32.1 ppm against the plan's 47,999.489 Hz; +-0.12 ppm timing granularity (+-0.35 ppm worst case); crystal tolerance (tens of ppm, #626) not included |
| BCLK 12.288 MHz | 12,287,474 Hz, inferred as 256 x fs | The receiver establishes 256 bit clocks per frame only as a minimum |
| One capture of at least 10 minutes, pattern-checked whole | NOT MET | 475.648 s received, all of it pattern-checked, then the STOP |
| FSYNC pulse width, edge timing, levels, absolute ppm | Not shown by the SoC board | #626 |

Per-run tables:

| Run | Frames | Seconds | Torn | Invalid words | Zero words | Slot order | Result |
|---|---|---|---|---|---|---|---|
| `timing-long` | 22,831,104 | 475.648 | 0 | 0 | 0 | Identity | PASS |

| Run | Samples | Window | Frames in window | fs, first to last | fs, least-squares | Against 48 kHz | Against the plan | BCLK = 256 x fs |
|---|---|---|---|---|---|---|---|---|
| `timing-long` | 95, 5 s apart | 472.468 s | 22,677,480 | 47,997.947 Hz | 47,997.946 Hz | -42.8 ppm | -32.1 ppm | 12,287,474 Hz |

The capture lost nothing before the stall. All 95 running samples share one trigger, and the buffer never held more than 2,048 of its 16,384 frames. The raw capture is 730,595,328 B, SHA-256 `dd201b3a926317a9f488b8290123fa235da7733dae06301f2cd21688da2d36cb`, kept off the packet on the bench host.

Discontinuities are whole frames only: 1,221 clusters in 475.6 s, against 59 in the #617 page's 70 s run.
- 189 are the INTERNAL-source beat.
- 16 follow a logged talker lateness.
- 1,016 match neither. They repeat a median of 18 frames, most then jump by 5, 5 and 8 to 12, and 838 are about 0.5 s apart.

The talker's late-PDU list caps at 5,000 entries, which it reached at 292 s, so attribution after that is blind. The page draws no conclusion on these clusters, since they do not bear on the link's framing. They may merit their own issue; that is the owner's call. `SLIP_TDM` rose 0.510/s, 10.63 ppm, in line with the plan.

Bench as left:
- **SoC board.** The lane's own recorder blocked on the dead link. It was ended by PID after its command line was checked: the first terminate signal was caught, the second ended it. The bridge legs were stopped by PID before the run and restarted with the recorded lines (new PIDs). PCM states match the start, the USB function reads configured on the SoC board side, the fault scan is empty, and `/tmp` is as found.
- **Controller.** No gPTP daemon. The NIC clock reads 0 ppb, back on its recorded trajectory (4.5 us). Timestamping is off, as found, and the staging was removed.
- **DUT.** The maps were removed and read back empty, and the stream is unbound. The census equals the start in 31/33 entries. One is the live propagation delay. The other is the reference peer's GET_SAMPLING_RATE: SUCCESS at the start, ENTITY_LOCKED at the end. This lane sent the peer read commands only.
- **Residuals.** NVM persistence advanced by the method's map and bind edits (commits 0 to 2, slots 237/238, `pend=1`, `PP_STAT` bit 11), as lane B3 recorded. `SLIP_LB` is saturated, after about 340/s from the bind on, against about 70/s in lane B3's run. RENDER_STAT rails rose 0 to 6,264. The talker also ended about 55 s before the unbind, because the stalled capture held the SoC console to its deadline. Both counters clear only on reset.
- **Bench lock.** Free. No flash, reset, power, wiring or instrument action occurred.

Owner items:
1. Re-attach the SoC board's USB function (USB Audio card and USB network link) to the bench host.
2. Decide the rerun's shape. It can repeat this method. Or, if the stream's load is suspected, fs can come from a capture discarded on the SoC board (no USB traffic). The pattern check of that same capture still needs its data off the board.

Validation at `4461a1f7`, all rc 0, unpiped, from the physical `/data` lane path, with the Markdown gates in the pinned Markdown environment:
- `scripts/docs_check.py`: 0 findings.
- `scripts/check_doc_style.py`.
- `scripts/gen_toc.py --check`, and `--verify-anchors`.
- `scripts/check_em_dash.py --base e4b771f9`: 0 findings over 356 added lines.
- `scripts/check_doc_paths.py`: 861 paths.
- `scripts/ci_scope.py --selftest`.
- `scripts/check_baremetal_only.py --check`: 0 findings.
- `scripts/check_feature_status.py --self-test`: 46/46.
- `git diff --check`, also against `e4b771f9` and `35a8b04d`.

Every table on the page (12) and in the index has a constant cell count, rendered and in the source. Packet `b4-a468` holds the handoff, the PR body, the manifest, the redacted evidence, the tools and the raw-artifact index. No issue closure or review approval is claimed.
