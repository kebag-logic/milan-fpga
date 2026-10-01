[A477] REVIEW READY

Commit: `f8b842f0a31a73b9328ad6455123df9b68475fec` on `b6-bench-1001`. It is one commit on dev `ea3fb38877842f223afea97e3bd72a10500455c9`, with a one-line subject; it is local and not pushed.

Changed: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (new) and its row in `docs/findings/README.md`. There is no other edit.

Session 2 resumed after the owner's fix to the STOP condition (comment 5929969516). Identity gate PASS: VERSION `00020060`, AEM `93742dd2`, ROM `acad92b9`, QSPI payload `d178f19a`, ENTITY and CONFIGURATION byte-equal to the QSPI AEM bytes, grader 10/10. Every bench action held the lock. No flash, reset, power, wiring, instrument or USB function action occurred, and no DUT CSR was written.

**Tool controls (synthetic, before any live case): PASS.**
- A clean tone sits at the 24-bit floor: THD+N -146.06 / -145.99 dB at 997 / 9,973 Hz.
- One dropped and one repeated frame are each found at the planted frame.
- 16 ppm and 1 ppm, resampled, are fitted as +16.000000 and +1.000000 ppm.
- 16 ppm and 1 ppm as slips are found at the planted spacing: 23 and 4 one-frame skips.

**Per-run tables.** Each window is 630 s, untouched. "At floor" counts blocks with no discontinuity, which sit at the loop's floor within 0.0006 dB with fitted offset below 4e-7 ppm. The counted ratio is McASP0 (the DUT's TDM clock) against the reference peer's output, from the tone's net non-capture-path steps; one frame is 0.033 ppm. The timed ratio puts McASP0 hw_ptr samples and the external capture's reads on the bench host's clock.

| Case | Captured audio, s | Blocks at floor | Listener discontinuities | DUT beat repeats | Counted ratio, ppm | Timed ratio, ppm | Result |
|---|---|---|---|---|---|---|---|
| A0, peer as found (control) | 629.56 | 54 of 629 | 519 drops, 1 silent insert | 321 | +6.519 | +6.44 +-0.72 | PASS as a control |
| A1, peer follows the DUT's AAF | 617.32 | 291 of 617 | 0 | 315 | -10.631 | -12.19 +-2.44 | PASS |
| A2, peer follows the DUT's CRF | 616.14 | 1 of 616 | 494 drops, 180 silent inserts | 316 | -0.068 | -0.59 +-1.24 | FAIL |
| B INTERNAL, DUT on INTERNAL, peer CRF bound (control) | 629.98 | 57 of 629 | 506 drops, 1 silent insert | 322 | +6.052 | +6.85 +-1.46 | PASS as a control |
| B CRF, DUT follows the peer's CRF | 629.95 | 611 of 629 | 0 | 0 | 0.000 (0 net steps in 30,237,600 frames) | -0.01 +-0.65 | PASS |

**THD+N and SNR.** Every case's blocks at the floor read THD+N -146.06 dB and SNR 146.07 dB at 997 Hz, and -145.99 dB and 145.99 dB at 9,973 Hz. A block with one slip falls to about -29 dB at 997 Hz and -8 dB at 9,973 Hz. The other B CRF blocks hold only capture-path losses.

**Binding rule and clock sources.**
- Before every bind, the listener's format was set to the talker's when they differed, and read back. The DUT's AAF to the peer went from 4 to 8 channels, SUCCESS. The probe's peer AAF to the DUT went from 8 to 4 channels, SUCCESS. The CRF binds needed no set.
- No talker format was set.
- Clock sources were set only on the listener and read back: the peer in A1 and A2, the DUT in B CRF.
- Each was restored to its as-found source and read back.

**Findings.**
- **A2 FAIL.** The peer follows the DUT's CRF, which runs on the DUT's physical audio clock (`KL_crf_tx` divides `clk_audio_i` by 512). At INTERNAL, the DUT's AAF stream runs on the free-running 48 kHz packet grid, 10.64 ppm off it. The listener therefore drops one frame per beat, net zero against the DUT's own repeat. Under CRF selection the DUT aligns the two, as B CRF shows. This is an owner decision or a new Issue; it was not filed here.
- **B CRF.** SET_CLOCK_SOURCE 1 read back 1. The servo read LOCKED 6.5 s later, trim -6.0 ppm, and stayed LOCKED. `SLIP_TDM` stayed static: the DUT's beat is gone. The servo status also shows bit 4, DRP config mismatch; it is not analysed.
- **Direction B THD+N: NOT RUN.** A probe under the binding rule bound the peer's AAF talker to the DUT. Its talker channels carry 0 to 2 LSB, not a known signal. Clock following is graded by the frame-rate ratio instead.
- The DUT's AAF following is not in this image.

Validation, at `f8b842f0`, every gate rc 0 and none piped. The Markdown gates ran in the pinned environment: `scripts/docs_check.py`, `scripts/check_doc_style.py`, `scripts/gen_toc.py --check`, `scripts/check_em_dash.py --base ea3fb388`, `scripts/check_doc_paths.py` and `scripts/gen_toc.py --verify-anchors`. The others: `scripts/ci_scope.py --selftest`, `scripts/check_baremetal_only.py --check` (the bare invocation is a usage error, as the script needs a mode), `scripts/check_baremetal_only.py --selftest`, `scripts/check_feature_status.py --self-test`, `git diff --check`, and `git diff --check ea3fb388 HEAD`.

Acceptance (the #629 bench items):
- Identity, tool controls and both INTERNAL controls: met.
- Format rule and clock-source rule with read-back and restore: met.
- A1 and B CRF: met.
- A2: not met.
- Direction B THD+N: NOT RUN, no known signal.
- The DUT following an AAF stream: not in this image.

Open risks and questions:
- **A2.** The decision above.
- **Capture path.** The bench host's external capture lost audio at read stalls up to 13.3 s long: 615,026 frames in A1 and 686,656 in A2. Every loss is attributed separately from clock effects by the read-time record. Events inside lost audio cannot be seen.
- **Console.** Another terminal on the bench host held the SoC board's serial console open. Commands were typed on the console, and their output came back over the board's USB network link. The root shell was confirmed with `id`. The terminal was left alone.
- **Residuals.** DUT NVM commits went from 2 to 8, of the class lane B3 recorded. Two of the peer's talker states keep a stream ID, destination MAC and VLAN with connection count 0. The bridge legs run under new process IDs.
- **Bench as left.** All unbound, both DUT maps empty, every clock source and format as found, census 43 of 46 equal, grader 10/10, controller staging removed, and the lock free.

