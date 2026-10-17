[A625] REVIEW READY

Bench lane B21, round 3, on the installed dev `9ef71772` image: not flashed, reset or power-cycled. It resumes after the [round 2 STOP](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-6217670001). The #117 audio continuity row passes as measured. These are operator measurements, not review verdicts.

Commit: `867fb9459486fa1bfaaba7a69e6a6f4ec0563d0b` (branch `117-b21-bench`, three one-line commits on dev `4a9b5a2a`; local, not pushed)
Changed: `docs/findings/117_AUDIO_CONTINUITY.md` only, +334 lines: the dated section "2026-10-17: bench lane B21 round 3 on dev 9ef71772" and its Contents entry.
Validation: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base e4b771f9` and `check_doc_paths.py` in the pinned Markdown environment; `ci_scope.py --selftest`, `check_baremetal_only.py --check`, `check_feature_status.py --self-test`; `git diff --check` on the tree, `acba86cf..HEAD` and `4a9b5a2a..HEAD`. All 11 rc 0 at the head, unpiped, on the physical path.
Acceptance criteria: the audio continuity row, met as measured. Every frame was bit-exact and in order in both directions over 10 minutes or more, with no missing, repeated or silent frame, and every restart was under 1 s. Evidence below.
Open risks/questions: see the limits at the end.

| Item | Verdict | Evidence |
|---|---|---|
| Identity gate | PASS, 11 of 11, three times | 2026-10-16 17:22 UTC; 2026-10-17 06:51 UTC after the controller host's restart; 07:51 UTC at the end |
| Step 1, McASP capture-path self-test | CLEAN | 630 s, 63,000 reads of one period each, 0 overruns, 0 stalls, no permanent floor step |
| Step 2, Direction A, both taps, DUT CSRs, peer counters | PASS | 644.8 s of pattern frames on both taps, all valid and in order; the peer's output 638.0 s clean |
| Step 3, Direction B, both taps, DUT CSRs, SoC board McASP | PASS | 30,480,000 frames (635.0 s) equal to the frames the DUT received, bit for bit and in order |
| Restarts, 20 cycles | PASS, 20 of 20 under 1 s | Wire median 13.8 ms, maximum 86.8 ms |
| #117 audio continuity row | PASS as measured | |

| Run | Window (UTC, 2026-10-17) | Result |
|---|---|---|
| `mst-long`, McASP self-test | 07:05:09 to 07:15:39 | 30,240,000 frames; 0 overruns, 0 stall reads, longest read interval 11.1 ms; 10 s floors within -3.50 to +1.94 frames of a +43.06 ppm line |
| `dA`, Direction A | 07:17:32 to 07:28:22 | DUT-link tap 5,198,452 AAF packets, peer-link tap 5,198,499, 0 sequence breaks, `avtp_timestamp` steps 124,999 to 125,020 ns; 30,951,504 pattern frames, 0 repeats, 0 skips, 0 torn, 0 invalid; 5,198,372 common packets equal in header and payload |
| `dA` DUT CSRs, 128 samples | 07:17:32 to 07:28:07 | `SLIP_TDM` 0 throughout; `RENDER_STAT` converged, fill 8 to 14, rails 0; `AVTPRX_STAT`/`AVTPRX_ERR` static; `AAF_FRAMES` 7,999.9/s |
| `dA` counters | pre, mid, post | DUT STREAM_OUTPUT 0 FRAMES_TX = peer STREAM_INPUT 0 FRAMES_RX = 5,245,516; only frame counters moved |
| `dA` external capture, cross-check | 07:17:35 + 640 s | 30,624,574 valid frames (638.0 s), 0 repeats, 0 skips, 0 zero, 0 torn; 0 stalls in 64,005 reads |
| `dB`, Direction B | 07:31:30 to 07:42:20 | Peer-link tap 5,198,371 packets, all present and equal on the DUT-link tap, 0 sequence breaks; McASP 30,480,000 frames at one constant offset to the received frames: 0 skips, 0 repeats, 0 foreign; 0 overruns (25 board read stalls up to 87.1 ms absorbed by the buffer) |
| `dB` DUT CSRs and counters | 07:31:30 to 07:42:05 | `SLIP_TDM` 0; `RENDER_STAT` converged, fill 8 to 14, rails 0; listener words static; peer FRAMES_TX 5,207,829, DUT FRAMES_RX 5,207,944 (read instants differ); only frame counters moved |
| `rA`, restarts | 07:44:28 to 07:46:28 | 20 binds SUCCESS, formats equal before each (no set), ended bound as found; wire restart 13.4 / 13.8 / 86.8 ms (min / median / max); at the peer's output less the steady latency 23.5 / 24.8 / 97.8 ms; no packet in any hold; first 480 frames valid each time |

- **Placement.** No loss occurred, so none needed placing, and step 5's debug trace is not needed. Lane B5's one-frame drops every 1.266 s are absent, with the peer following the DUT's CRF, as found. The INTERNAL beat did not occur: `SLIP_TDM` stayed 0.
- **Restore.** The end census equals the start in 45 of 46 entries; the other is the DUT's live propagation delay. DUT words are equal but for live counters, and the NVM line is unchanged. Outlets are on, and no file or process is left on the taps or the controller host. On the SoC board, the bridge leg runs again with its recorded command line. The board's audio player was restarted through its own scripts. Its stop script removes a runtime CA mount the player needs, which its start script does not make, so the lane recreated it from the player's own directory and the player logged in again. Bench lock free.
- **Limits.** One window per direction. Direction B's signal is the noise already at the peer's talker inputs, made known by the wire record. The output restart excludes the unmeasured steady latency. The restart driver's format comparison read a field the agent does not emit; the reads ran before every bind and were all equal, so no set was due.

Packet `117-b21-a625` (publication is the manager's): `r3/` records, `RAW-ARTIFACTS-r3.json`, `HANDOFF.md`, `MANIFEST.sha256`, `PR-BODY.md`. No push, no PR; no existing comment edited.
