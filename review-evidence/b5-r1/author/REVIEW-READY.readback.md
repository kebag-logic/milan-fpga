[A472] REVIEW READY

Bench lane B5, #117 acceptance box 4, the audio continuity row, under the [A10] assignment (https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5925737609). Refs #117.

Commit: `bf9e5d82a401d167a8ffc786677a19dc7aac0cf2`
Branch: `b5-bench-1001`, base dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`. One commit, local only: not pushed, no PR.
Changed: `docs/findings/117_AUDIO_CONTINUITY.md` (new) and its row in `docs/findings/README.md`. No other doc edit.

**Identity: PASS.** VERSION `0x00020060`, AEM CRC32 `93742dd2`, ROM `acad92b9`, QSPI payload `d178f19a`, all equal to lanes B3 and B4. Live ENTITY and CONFIGURATION are byte-equal to the QSPI AEM bytes. The UART grader passed 10 of 10 at the start and at the end.

**Binding rule.** Each bind was preceded by reads of the talker's (DUT STREAM_OUTPUT 0) and the listener's (reference peer STREAM_INPUT 0) formats. On each run's first bind the listener read `0205022001006000` (4 channels) against the talker's `0205022002006000` (8 channels). It was set to the talker's format (SUCCESS) and read back equal. The 30 rebinds found the formats equal. The talker was never set. After every run the listener was set back to `0205022001006000` and read back.

| Run | Purpose | Result |
|---|---|---|
| `a-try1` | First bind | Bind and format set SUCCESS, talker streamed; the tool watched the wrong capture channels, timed out, restored |
| `diag1` | Every capture channel, 15 s bound | Identified the two channels; peer listener media locked, no late, early or sequence-mismatch count |
| `a-long` | Initial bind, 660 s untouched, 30 cycles | Graded below |
| `cap-test1` | 40 s, 125 ms capture period | Capture path loses frames at the same rate |

| Direction A item (`a-long`) | Verdict | Evidence |
|---|---|---|
| Integrity, stream channels 0 and 1, 24 bits, in order | PASS | 31,569,594 of 31,569,600 window frames bit-exact; 0 torn, 0 invalid; 6 single zero frames |
| Continuity, 660 s | FAIL | Table below |
| Restarts, 30 cycles | PASS, 30 of 30 under 1 s | Table below |
| #117 audio continuity row | FAIL as measured | Peer output drops one frame every 1.266 s; the capture path also loses frames |

| Continuity class | Events | Frames | Per second | Cause |
|---|---|---|---|---|
| Whole-frame repeat | 334 | 334 | 0.508 | DUT INTERNAL beat, 93,989 to 93,992 frames apart (TIME_SYNC.md) |
| One-frame skip | 526 (520 slip events) | 526 | 0.800 | Peer output 16.4 ppm slower than the stream, one event every 1.266 s; the peer's media clock is INTERNAL |
| Skip of 2 to 59 frames | 521 | 7,176 | 0.792 | Bench host USB path, by the frame-count drift |
| Skip of 60 frames or more | 239 | 109,928 | 0.363 | Bench host USB path: capture stalls of the same length, about every 2.99 s |
| Single zero frame | 6 | 6 | - | Part of six slip events (skip, zero, skip) |

| Restarts | Count | Below 1 s | Min, s | Median, s | p95, s | Max, s |
|---|---|---|---|---|---|---|
| Rebind response to first valid sample | 30 | 30 | 0.0262 | 0.0279 | 0.0389 | 0.1358 |

| Cycles | Restart, s |
|---|---|
| 1-10 | 0.1358, 0.0282, 0.0269, 0.0273, 0.0276, 0.0287, 0.0262, 0.0271, 0.0268, 0.0279 |
| 11-20 | 0.0288, 0.0270, 0.0281, 0.0285, 0.0274, 0.0283, 0.0282, 0.0270, 0.0273, 0.0389 |
| 21-30 | 0.0279, 0.0275, 0.0280, 0.0284, 0.0285, 0.0283, 0.0271, 0.0282, 0.0269, 0.0275 |

- Every cycle stopped in its 2 s hold: the last valid frame came 14.4 to 24.6 ms after the unbind response.
- The growth slope is -0.00066 s per cycle, 95% interval [-0.00150, +0.00017].
- The initial bind took 0.2676 s.
- Cycle 20 had a 19.8 ms capture stall inside its restart.

**Direction B: NOT RUN.** The peer's talker channels carry its own physical inputs. No known signal drives them without an instrument output or a wiring change.

**Restore: proven.**
- All 18 stream states are unbound. The end census equals the start in 45 of 46 entries; the other is the live propagation delay.
- The peer's format is as found and both DUT maps are empty.
- DUT console words are equal but for live counters. The NVM line is unchanged, with no commit in this lane. SYNC=1 ASCAPABLE=1 TU=0.
- The SoC board is on the same boot. Its bridge legs run with the script's command lines under new PIDs, its USB function is configured, and the fault scan is as at the start.
- The controller staging is removed and no task process is left.
- Both USB audio devices are present on the bench host, and the bench lock is free.
- No flash, reset, power, wiring or instrument change; no DUT PHY or CSR write; no gadget down or up.

**Validation**, all rc 0 at the commit, from the physical lane path: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base e4b771f9`, `check_doc_paths.py` (pinned Markdown environment); `scripts/ci_scope.py --selftest`; `scripts/check_baremetal_only.py --check`; `scripts/check_feature_status.py --self-test`; `git diff --check` and `git diff --check e4b771f9 HEAD`; `gen_toc.py --verify-anchors`.

**Open risks and questions.**
- The capture path loses 0.37% of the frames, so a clean window was not recorded. Owner item: a capture path that loses no frames.
- The attribution of the one-frame skips to the peer's output rate rests on their period and on the bench host's uncalibrated clock. Testing it needs the peer's media clock to follow the stream, a peer clock-source change that this lane did not make. Decision item.
- Packet `b5-a472` holds the tools, per-action evidence, summaries, `RAW-ARTIFACTS.json`, `redaction.json`, `MANIFEST.sha256` and `HANDOFF.md`.

