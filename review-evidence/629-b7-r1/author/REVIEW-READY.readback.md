[A519] REVIEW READY
Commit: `4eee41a558a56024e57b27a956fdaf7910ca69dc` on `629-b7-bench`, one commit on dev `bbf704ecc3ef2e9cdd4cfdb72ec085e7428d1352`. Local, not pushed, no PR.
Changed: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` gains the dated section "Dev bbf704ec, 2026-10-03: lane B7", with its Contents line, a pointer in the intro and a two-image title. Its row in `docs/findings/README.md` is updated. No other file changes.
Validation: at `4eee41a5`, every gate is rc 0, run unpiped from the physical /data path:
- `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base bbf704ec` and `check_doc_paths.py`, in the pinned Markdown environment;
- `ci_scope.py --selftest`;
- `check_baremetal_only.py --check` and `--selftest` (the bare invocation is a usage error, rc 2, as in lane B6);
- `check_feature_status.py --self-test`;
- `git diff --check`, and `git diff --check bbf704ec HEAD`;
- `gen_toc.py --verify-anchors`.

Bench: 14:28 to 15:50 CEST. Lane B6's method, with the changes stated on the page and fixed at 14:50, before any graded case. Every case restored and read back, the bench lock free, no task process left.

**Identity: PASS.**
- VERSION `00020060`.
- Console CRCs equal the build's: AEM image `5ba355eb` (7,512 B), BIOS ROM `2144df1c`, QSPI bitstream payload `e6b8febc`.
- 12 live descriptors byte-equal to the build's AEM image.
- Clock sources: 0 INTERNAL, 1 INPUT_STREAM on the CRF input, 2 INPUT_STREAM on the AAF input. CLOCK_SOURCE 3 absent. Grader 10/10.

**Tool controls: PASS**, byte-equal to lane B6's `controls.json`.

Direction A, the DUT's talker to the reference peer's listener (two-tone loop, external audio capture):

| Case | The peer follows | Window, s | Blocks at the floor | Listener discontinuities | DUT beat repeats, `SLIP_TDM` | Counted ratio, ppm | Timed ratio, ppm | Result |
|---|---|---|---|---|---|---|---|---|
| A0 | Its INTERNAL | 630.31 | 444 of 630 | 470 drops, 291 silent inserts | 0, static | +5.916 | +5.71 +-0.55 | PASS as a control |
| A1 | The DUT's AAF stream | 629.88 | 597 of 629 | 0 | 0, static | 0 | -0.28 +-1.40 | PASS |
| A2 | The DUT's CRF stream | 628.04 | 578 of 628 | 0 | 0, static | 0 | +2.15 +-4.42 | PASS |

Direction B, the reference peer's talker to the DUT's listener, graded by the frame-rate ratio and the tone path:

| Case | The DUT follows | Window, s | Servo | Set to LOCKED, s | Counted ratio, ppm | Timed ratio, ppm | Listener discontinuities | Result |
|---|---|---|---|---|---|---|---|---|
| B0 | INTERNAL | 629.55 | IDLE | - | +5.924 | +5.62 +-0.44 | 457 drops, 278 silent inserts | PASS as a control |
| B-CRF | CLOCK_SOURCE 1, the peer's CRF | 628.53 | LOCKED at all 21 reads, trim -6.0 ppm | 3.1 to 3.6 | 0 (0 net steps in 30,169,440 frames) | +1.98 +-6.52 | 0 | PASS |
| B-AAF | CLOCK_SOURCE 2, the peer's AAF | 627.74 | LOCKED at all 21 reads, trim -6.0 ppm | 6.6 to 7.1 | 0 (0 net steps in 30,131,520 frames) | -1.49 +-11.64 | 0 | PASS |

B-AAF also met the design's bench row:
- the CLOCK_DOMAIN counters stayed at 5/4 through the window;
- `SLIP_TDM` stayed static;
- the AAF meter stayed locked with a valid rate (+11.02 to +11.04 ppm), its history never restarted, and its largest deviation was 29 ns.

**Lock loss, B-AAF, observation:** the followed talker was unbound for 11.1 s. Everything happened as declared:
- HOLDOVER within 0.56 s, with the trim held and GET_CLOCK_SOURCE 2 throughout;
- the DUT's AAF output MEDIA_RESET went from 1 to 2 at the loss and stayed 2 after the return; the peer's received count matched;
- CLOCK_DOMAIN went from 5/4 to 5/5 to 6/5;
- LOCKED again 5.6 to 6.1 s after the rebind;
- 0 tone-path discontinuities through it.

**INTERNAL clock, observation:** +5.92 ppm from the reference peer, about -5.1 ppm against gPTP time. Inside +-50 ppm; the oscillator grade stays the owner's known risk.

**Direction B THD+N: NOT RUN.** The known-signal probe was repeated: the peer's talker channels carry -2 to 0 LSB.

Acceptance criteria: judged item by item on the page.
- **Met:** requirements; model and builder (on this image); the fabric's recovery and gating; the AAF lock loss; the bench in both directions for each followed source; the Direction A metric; A2-a.
- **Met in part at the bench:** the processor's saved selection. Persistence across a power cycle is not testable in this lane.
- **Met by PR #634's evidence, not re-run here:** simulation.
- **Not met:** the Direction B quality metric (no known signal). The PR body therefore says "Refs #629".
- **No bench evidence:** a switch between the AAF and CRF streams, and a followed CRF stream's lock loss.

Open risks/questions:
- A2 and B-AAF rest on lane B6's capture-path attribution. Five capture-path clusters (A2: 2, B-AAF: 3) are one or two frames short of the 48 n + 12 size signature, and the page states the conservative reading.
- In B-AAF the DUT listener's loopback ring slipped one frame 14 to 45 s after lock, then held for 570 s. It is recorded beside #632, not analysed.
- The DRP config mismatch bit is set under following, as lane B6 recorded.
- The DUT's NVM went from 0 to 17 commits on the new image's first saved state.

