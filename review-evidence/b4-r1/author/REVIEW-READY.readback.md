[A468] REVIEW READY

Refs #451, the timing item, after the manager's ruling (5924950994) on the second session's STOP (5924930868). Session 3 had no bench access.

Commit: `35a60c8d6ee742216f98232c85926b435ab01b91` on `b4-bench-1001`, one commit on `4461a1f7` and three on dev `e4b771f9`. Each has a one-line subject with no body and no trailers. Local only: not pushed, no PR.

Changed (in `35a60c8d`, documentation only, as the ruling lists):
- `docs/findings/451_TDM8_TIMING_SOC_BOARD.md`:
  - The capture-length row reads "475.6 s (ruled sufficient by the manager, 5924930868 and 5924950994)".
  - "Why the run stopped" becomes "The USB loss, a bench event", stating why it changes no figure.
  - "Rerun" becomes "Notes for a later capture", since no re-run follows.
  - The intro states the ruling and its reason.
  - The measured figures and stated limits are unchanged.
- `docs/findings/README.md`: the page's index row follows the ruling.

No other doc edit.

| #451 timing item | Verdict | Evidence |
|---|---|---|
| Identity gate, dev `ec0cc0c1` | PASS | VERSION `00020060`; AEM CRC32 `93742dd2`; ROM `acad92b9`; QSPI payload `d178f19a`; ENTITY and CONFIGURATION byte-equal to QSPI; grader 10/10 |
| Framing record | Recorded | `dsp_a`; the codec side (DUT) is bit-clock and frame master; 8 slots x 32 bits on both DAIs; McASP0 AXR1 receives; capture `S32_LE`, 8 channels, 48000 |
| Data one BCLK after the frame-sync edge: bit-exact, all eight slots, in order | PASS, as far as the SoC board shows | 22,831,104 frames: 0 torn, 0 invalid, 0 zero words; channel c = slot c = tag c+1 |
| FSYNC at 48 kHz | fs 47,997.947 Hz on the SoC board's clock | -42.8 ppm against 48 kHz, -32.1 ppm against the plan; +-0.12 ppm timing granularity; crystal tolerance (tens of ppm) not included |
| BCLK 12.288 MHz | 12,287,474 Hz, inferred as 256 x fs | Not measured: the receiver establishes 256 bit clocks per frame only as a minimum |
| Capture length, pattern-checked whole | 475.6 s (ruled sufficient by the manager, 5924930868 and 5924950994) | Every received frame was pattern-checked. The USB loss at 475.7 s ended the capture and changes no figure |
| FSYNC pulse width, edge timing, levels, absolute ppm | Not shown by the SoC board | #626 |

Per-run tables:

| Run | Frames | Seconds | Torn | Invalid words | Zero words | Slot order | Result |
|---|---|---|---|---|---|---|---|
| `timing-long` | 22,831,104 | 475.648 | 0 | 0 | 0 | Identity | PASS |

| Run | Samples | Window | Frames in window | fs, first to last | fs, least-squares | Against 48 kHz | Against the plan | BCLK = 256 x fs |
|---|---|---|---|---|---|---|---|---|
| `timing-long` | 95, 5 s apart | 472.468 s | 22,677,480 | 47,997.947 Hz | 47,997.946 Hz | -42.8 ppm | -32.1 ppm | 12,287,474 Hz |

Why the USB loss changes no figure, from the packet's records:
- The pattern decode covers every received byte. The capture dropped no frame before the event: one trigger in all 95 samples, and the buffer never above 2,048 of 16,384 frames.
- The fs window ends at the last status sample, 475.480 s after the trigger. That is 0.24 s before the SoC board logged the event. That sample's residual, -1.17 frames, is inside the fit's 1.23 frames rms.

Raw capture: 730,595,328 B, SHA-256 `dd201b3a926317a9f488b8290123fa235da7733dae06301f2cd21688da2d36cb`, kept off the packet and re-hashed in this session: equal. The page's 11 evidence-file hashes were re-checked against the packet: all equal.

Validation at `35a60c8d`: all 13 invocations rc 0, unpiped, from the physical `/data` lane path, with the Markdown gates in the pinned Markdown environment.
- `scripts/docs_check.py`: 0 findings.
- `scripts/check_doc_style.py`.
- `scripts/gen_toc.py --check`, and `--verify-anchors`.
- `scripts/check_em_dash.py --base e4b771f9`: 0 findings over 374 added lines.
- `scripts/check_doc_paths.py`: 861 paths.
- `scripts/ci_scope.py --selftest`.
- `scripts/check_baremetal_only.py --check`: 0 findings.
- `scripts/check_feature_status.py --self-test`: 46/46.
- `git diff --check`, also against `e4b771f9`, `35a8b04d` and `4461a1f7`.

Every table on the page (12) and in the index has a constant cell count, rendered and in the source.

Acceptance criteria (the B4 assignment), as far as the SoC board can show them:
1. Identity: PASS.
2. Framing: recorded. Data one BCLK after the frame sync under `dsp_a`: PASS, bit-exact in all eight slots, in order.
3. Frequencies: fs and BCLK = 256 x fs given, with the uncertainty stated. The whole capture was pattern-checked. The capture length was ruled sufficient by the manager.
4. What the board cannot show is named, with #626.
5. Restore: done and proven in the second session. The bench host's USB function is absent until the owner re-attaches it.

Bench state: the bench lock is free. This session touched no console, SoC board, controller host or DUT.

Open risks/questions: the 1,016 unmatched whole-frame discontinuity clusters in the rendered stream are outside this item. Whether they deserve their own issue is the owner's call.

The packet holds the handoff, the PR body, the manifest, the redacted evidence, the tools and the raw-artifact index. No issue state change or review approval is claimed.

