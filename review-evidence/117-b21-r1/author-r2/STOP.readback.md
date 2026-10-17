[A625] STOP

Bench lane B21, #117 acceptance box 4, the audio continuity row, under the [B21 assignment](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-6208207821). Refs #117.

Commit: `d64336badb959349846a226df213621eccb3a334` (branch `117-b21-bench`, one commit on dev `4a9b5a2a`; local, not pushed, no PR). It adds the dated section "2026-10-16: bench lane B21 on dev 9ef71772" to `docs/findings/117_AUDIO_CONTINUITY.md`, with its Contents entry. No other file.

Image: dev `9ef71772`, as installed. Not flashed, reset or power-cycled.

**STOP after step 1, for two reasons.**
1. The capture-path self-test was not clean in either 10-minute window, and the assignment goes on only after a clean one.
2. The SoC board's console stands at a `login:` prompt, not a root shell. Direction A needs it to play the first-light pattern into McASP0, and Direction B to record McASP0. The board's USB audio bridge resamples, so it cannot carry a bit-exact grade. No credential was typed or stored. The console runner's readiness line reached login as a name; login's 60 s timeout returned the console to its prompt, seen by a passive read.

| Item | Verdict | Evidence |
|---|---|---|
| Identity gate | PASS, 11 of 11, at 04:56:04 and 05:29:44 UTC | VERSION `00020060`, AEM CRC `5ba355eb` over 7,512 B, live ENTITY/CONFIGURATION equal to QSPI, clock sources, grader 10/10, ADP model `001bc5c1935893e1` |
| Step 1, capture-path self-test (deficit-only) | NOT CLEAN, both windows | Table below |
| Step 2, Direction A, taps, DUT CSRs, peer counters | NOT RUN (STOP) | Reasons 1 and 2 |
| Step 3, Direction B | NOT RUN (STOP) | Reasons 1 and 2 |
| #117 audio continuity row | Not graded on this image; not passed | Lane B5's losses outside the capture path stay unplaced |

**Step 1.** The external capture exposes no mixer control, so no software loopback could be set and restored; the deficit-only self-test ran instead. It used lane B5's reader and capture parameters, with no DUT, peer, SoC board or controller action. Analysis: `b5_attrib.py`'s definitions, imported unchanged.

| Run | Window, UTC | Seconds | Stalls over 15 ms | Longest read, ms | Stall spacings 2.99 to 3.02 s | Episodes | Losses | Frames lost | 1 ms steps |
|---|---|---|---|---|---|---|---|---|---|
| `st-long` | 05:01:20 to 05:11:51 | 630.0 | 11 | 23.2 | 0 | 2 | 2 | 336 | 11 |
| `st-long2` | 05:15:22 to 05:25:53 | 630.1 | 123 | 88.4 | 0 | 16 | 18 | 10,945 | 13 |

The USB controller interrupt shortfall is counted over 2 s around each event; pressure is in ms per second, from `st-long2`.

| Event class | `st-long`: events, median shortfall | `st-long2`: events, median, largest | `st-long2`: I/O full, memory full, CPU some |
|---|---|---|---|
| Losses | 2, +13.6 | 18, +21.3, +103.0 | 5.39, 0.00, 0.45 |
| 1 ms steps | 11, +0.6 | 13, -0.2, +26.8 | 5.90, 0.00, 0.36 |
| Stalls with no step | 10, +6.6 | 82, -0.8, +102.9 | 5.62, 0.00, 0.42 |
| 300 clear times | +0.6 | -1.2 | 5.51, 0.00, 0.28 |

- Every loss is a whole number of 1 ms USB frames, within 0.02 ms, and falls in a stall episode.
- Each loss comes with frame interrupts missing from the capture's USB host controller. The bench host's CPU, memory and I/O pressure equal the control values, and steal time is 0.003% and 0.008%. The cause therefore lies below the bench host's visible load. Its source was not found, and no host configuration was changed.
- Lane B5's 3.00 s recurrence is absent: no stall spacing falls in 2.99 to 3.02 s.
- The capture path lost no block under 1 ms in 1,260 s, though the floor test resolves about 4 frames.
- The 1 ms steps come about every 60 s, with no interrupt shortfall. They are not attributed.

| Lane B5 loss class | Placement after B21 |
|---|---|
| 236 stall-aligned skips of 60 frames or more | Recording side, as B5 inferred: with no DUT or peer in the path the capture path still loses frames in stall episodes. Today the episodes are irregular and each loss is whole USB frames. |
| Three unaligned skips of 72, 78 and 108 frames | Not placed: 1.5, 1.625 and 2.25 ms, not whole USB frames |
| Skips of 2 to 59 frames | Not placed: no capture-path loss under 1 ms, so they lie at the capture's input or upstream |
| One-frame drops every 1.266 s | Not re-tested (Direction A not run); the peer now follows the DUT's CRF |
| INTERNAL-beat repeats | Not graded; `SLIP_TDM` read 0 at the start and end reads |

**Restore: proven.**
- The end census equals the start in 45 of 46 entries; the other is the DUT's live propagation delay. Bindings, formats, maps and clock sources are as found.
- DUT words are equal but for live counters, with `SLIP_TDM` 0 and `SLIP_LB` at its ceiling, as found. The NVM line is unchanged.
- SYNC=1, ASCAPABLE=1, TU=0; grader 10/10.
- Outlets are all on, none switched. The SoC console is at `login:`, as found.
- The controller staging is removed and no gPTP daemon runs. The taps were not used, and the bench lock is free.
- Nothing was written to the DUT or the peer beyond reads.

**Validation**, all rc 0 at `d64336ba`, unpiped, from the physical lane path, Markdown gates in the pinned environment: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base e4b771f9`, `check_doc_paths.py`, `scripts/ci_scope.py --selftest`, `scripts/check_baremetal_only.py --check`, `scripts/check_feature_status.py --self-test`, `git diff --check` and `git diff --check 4a9b5a2a HEAD`.

**Needed to continue (owner and manager):**
- a root shell on the SoC board's console;
- a capture path that loses no frames, since the stall source sits below the bench host's visible load (the manager's call);
- then step 1 again, and Directions A and B.

The lane packet `117-b21-a625` holds HANDOFF.md, PR-BODY.md, the tools, the self-test records and analyses, RAW-ARTIFACTS.json and MANIFEST.sha256.

