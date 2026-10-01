[A468] Bench lane B4 on the dev `ec0cc0c1` image: the #451 timing item, measured on the SoC board. One McASP0 capture of 475.6 s, which the manager ruled sufficient, with no re-run.

Refs #451, the timing item ("Scope BCLK, FSYNC and DOUT at the AM62x end: 12.288 MHz, a one-BCLK FSYNC pulse at 48 kHz, data starting one BCLK after it"). The oscilloscope version is #626, which this PR leaves unchanged. Whether the #451 item is done is for review and the owner; this PR claims no issue state change.

Head `35a60c8d6ee742216f98232c85926b435ab01b91` on `b4-bench-1001` is three commits on dev `e4b771f9`, documentation only:

- `35a8b04d`: the first session's attempt record, which stopped at the SoC board's console login.
- `4461a1f7`: the second session, after the owner logged the console in. It replaces the attempt record in `docs/findings/451_TDM8_TIMING_SOC_BOARD.md` with the measured result, and updates that page's row in `docs/findings/README.md`.
- `35a60c8d`: the manager's ruling ([5924950994](https://github.com/kebag-logic/milan-fpga/issues/451#issuecomment-5924950994)) on the second session's STOP ([5924930868](https://github.com/kebag-logic/milan-fpga/issues/451#issuecomment-5924930868)). The capture-length row reads "475.6 s (ruled sufficient by the manager, 5924930868 and 5924950994)". The USB loss at 475.7 s is recorded as a bench event with no effect on the figures. The "Rerun" section becomes "Notes for a later capture", and the index row follows. The measured figures and stated limits are unchanged. No bench access in this commit's session.

## Verdicts (operator observations, not review verdicts)

| Item | Verdict | Evidence |
|---|---|---|
| Identity gate | PASS | VERSION `00020060`, AEM CRC `93742dd2`, entity `020000fffe000001`; ENTITY and CONFIGURATION byte-equal to the QSPI AEM bytes; grader 10/10; ROM `acad92b9`; QSPI payload `d178f19a`, as lane B3 read it. The second session ran on the same DUT boot |
| Framing record | Recorded | `dsp_a`, the DUT side as bit-clock and frame master, eight 32-bit slots; capture `S32_LE`, 8 channels, 48 kHz, MONOTONIC timestamps |
| Data one BCLK after the frame-sync edge: bit-exact, all eight slots, in order | PASS, as far as the SoC board shows | 22,831,104 frames: 0 torn, 0 invalid, 0 zero words |
| FSYNC at 48 kHz | fs 47,997.947 Hz on the SoC board's clock | -42.8 ppm against 48 kHz, -32.1 ppm against the plan; +-0.12 ppm granularity; crystal tolerance (tens of ppm) not included |
| BCLK 12.288 MHz | 12,287,474 Hz, inferred as 256 x fs | Not measured: the receiver establishes 256 bit clocks per frame only as a minimum |
| Capture length, pattern-checked whole | 475.6 s (ruled sufficient by the manager, 5924930868 and 5924950994) | Every received frame pattern-checked; the USB loss at 475.7 s changes no figure |
| FSYNC pulse width, edge timing, levels, absolute ppm | Not shown by the SoC board | #626 |

## Per-run results

| Run | Frames | Seconds | Torn | Invalid words | Zero words | Slot order | Result |
|---|---|---|---|---|---|---|---|
| `timing-long` | 22,831,104 | 475.648 | 0 | 0 | 0 | Identity | PASS |

| Run | Samples | Window | Frames in window | fs, first to last | fs, least-squares | Against 48 kHz | Against the plan's 47,999.489 Hz | BCLK = 256 x fs |
|---|---|---|---|---|---|---|---|---|
| `timing-long` | 95, 5 s apart | 472.468 s | 22,677,480 | 47,997.947 Hz | 47,997.946 Hz | -42.8 ppm | -32.1 ppm | 12,287,474 Hz |

Raw capture: 730,595,328 B, SHA-256 `dd201b3a926317a9f488b8290123fa235da7733dae06301f2cd21688da2d36cb`, kept on the bench host (re-hashed in the third session: equal).

## The USB loss, a bench event

At 04:25:01Z the bench host's USB host controller logged a failed endpoint command, and the SoC board's USB device disconnected. That ended the capture at 475.7 s of a planned 630 s. It changes no figure:

- The pattern decode covers every received byte, and the capture dropped no frame before the event (one trigger in all 95 status samples; the buffer never above 2,048 of 16,384 frames).
- The fs window ends at the last status sample, 475.480 s after the trigger and 0.24 s before the SoC board logged the event. That sample's residual, -1.17 frames, is inside the fit's 1.23 frames rms.

The cause is not established. The owner re-attaches the SoC board's USB function, and no lane touches it until then.

## Bench as left (end of the second session; the third had no bench access)

| State | As left |
|---|---|
| DUT | Mappings removed and read back empty; stream unbound. The census equals the start in 31 of 33 entries: the live propagation delay, and the reference peer's GET_SAMPLING_RATE, which answered ENTITY_LOCKED at the end. This lane sent the peer read commands only |
| DUT residuals | NVM persistence advanced by the method's map and bind edits (`pend=1`, `PP_STAT` bit 11), as in lane B3. `SLIP_LB` saturated and the render rail count at 6,264. Both clear only on reset |
| Controller host | No gPTP daemon; NIC clock 0 ppb and on its recorded trajectory (4.5 us); timestamping off, as found; staging removed |
| SoC board | Bridge legs restarted with the recorded command lines, under new PIDs; PCM states as at the start; fault scan empty; `/tmp` as found |
| Bench host | USB Audio card and USB network link absent (owner re-attaches) |
| Bench lock | Free |

## Validation at `35a60c8d`

All 13 invocations rc 0, unpiped, from the physical `/data` lane path; the Markdown gates ran with the pinned Markdown environment.

- `scripts/docs_check.py`: 0 findings.
- `scripts/check_doc_style.py`.
- `scripts/gen_toc.py --check`, and `--verify-anchors`.
- `scripts/check_em_dash.py --base e4b771f9`: 0 findings over 374 added lines in 2 pages.
- `scripts/check_doc_paths.py`: 861 paths.
- `scripts/ci_scope.py --selftest`.
- `scripts/check_baremetal_only.py --check`: 0 findings.
- `scripts/check_feature_status.py --self-test`: 46/46.
- `git diff --check`, also against `e4b771f9`, `35a8b04d` and `4461a1f7`.

Every table in both pages has a constant cell count, rendered and in the source. The page's 11 evidence-file hashes were re-checked against the packet: all equal.

## Open questions

1. 1,016 discontinuity clusters, about every 0.5 s, match no logged talker lateness, against 59 clusters of any kind in lane B3's 70 s run. The talker's late-PDU list was full at 292 s. These are whole frames of the rendered stream, outside this item. Whether they deserve their own issue is the owner's call.
