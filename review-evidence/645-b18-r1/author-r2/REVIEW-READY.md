[A622] REVIEW READY
Commit: `480c5e916f8bf711c47e1985ba3efe2b2471bdda` (branch `645-b18-bench` from dev `9ef717727e6fdac11ee7f01672fefae948452343`; local, not pushed, no PR, as assigned)
Changed: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` only: the dated section "Dev 9ef71772, 2026-10-15: lane B18" and its Contents entry (+315 lines). Findings only.
Validation: all rc 0 at the head, unpiped, on the physical path:
- with the pinned Markdown interpreter: `scripts/docs_check.py`, `scripts/check_doc_style.py`, `scripts/gen_toc.py --check`, `scripts/check_em_dash.py --base 9ef71772` (315 added lines, 0 findings) and `scripts/check_doc_paths.py`;
- `scripts/check_baremetal_only.py --check` and `git diff --check`.

A mechanical check found that the section's two tables equal the summary tool's output, with 0 mismatches.
Acceptance criteria: the assignment's items 1 to 5 are met. The identity gate passed. B17's method ran unchanged for ten cycles, each graded against PR #742. The restore is read back, and the section is added. **The ruling's close condition is met.** Every bind at INTERNAL held, and no #743 residual occurred, so the PR body says "Closes #645".
Open risks/questions: no CSR exposes the recentre count, so "held" rests on `SLIP_LB` alone. In every cycle the first late burst came at least 32.7 ms after the design's firing time (the first PDU plus 42.7 ms), so the arming window itself was not exercised. #743 tracks the in-window one-pair dup.

**Run.**
- **Identity gate: PASS**, 11 of 11, 18:50:11 to 18:50:17 UTC.
  - Over ATDECC: entity_id `020000fffe000001`, "Milan FPGA 1x1 TDM8", firmware_version `2.96.0`, serial `AX7101-0001`, the values B17 recorded.
  - On the console: `ID=4d494c4e VERSION=00020060`, and AEM CRC `5ba355eb` over 7,512 B.
  - Live ENTITY and CONFIGURATION equal the QSPI bytes, and the clock sources are as for #629.
  - The flash record (`FLASH_RC=0`, `POWERCYCLE_RC=0`, the same boot line) is the image's identity proof.
- **As found.** B17's probe state. The DUT is on CLOCK_SOURCE 0, with STREAM_INPUT 0 bound to the peer's AAF talker (flags `0x0002`) and formats equal. The peer follows the DUT's CRF on its CLOCK_SOURCE 1. `SLIP_LB` reads 0 after the cold boot.
- **Method.** B17's cycle runner, changed only in its paths (SHA-256 `d41d0480ba17fdedd8ee73d5ee2ae973180bdda1e55a3d814a408790aa4e76e6`). B8's poller, unchanged (`1912837a1e4cfd6a1f8b3615b4d26924efbfd430aff239ebd18cd4dd2a67d4f7`). B17's grader `ana_b17.py`, unchanged (`299d4f55441e147bf6d27b5b51242d3384157e4905d27f6ed1064398f05f9468`), and a new summary tool that grades against PR #742 and compares with B17.
  - Ten cycles ran, one lock hold each, from 18:50:47 to 18:59:53 UTC: unbind, binding rule (formats equal, none set), re-bind 6 s later, then a 32 s hold.
  - Every unbind and bind answered SUCCESS, and every cycle ended bound as found.
  - Polls ran every 0.5 s from 8.00 s before each bind to +31.70 to +31.88 s after it: 80 per cycle, none unreadable.
  - The raw counter logs' digest is `2c5e8d6ff8220cb16a9a3d0535279dfd7f04b5642c9aee2d9f97cdefcd939bdb`.

| Cycle | Bind, UTC | Polls, s from the bind | `SLIP_LB` dups, skips | Change | Grade | First peer PDU, ms | First burst over 20 us: s, peak | Bursts to the last poll, peak | CLOCK_SOURCE DUT, peer | delta_ppm |
|---|---|---|---|---|---|---|---|---|---|---|
| c01 | 18:50:56.251 | 80, -8.00 to +31.70 | 0, 0 to 0, 0 | None | Held | 135.267 | 4.74, 25.7 us | 17, 29.3 us | 0 to 0, 1 to 1 | +0.0009 |
| c02 | 18:51:59.961 | 80, -8.00 to +31.84 | 0, 0 to 0, 0 | None | Held | 25.015 | 4.03, 25.1 us | 11, 32.0 us | 0 to 0, 1 to 1 | -0.0008 |
| c03 | 18:52:51.821 | 80, -8.00 to +31.83 | 0, 0 to 0, 0 | None | Held | 165.076 | 0.38, 25.8 us | 9, 28.4 us | 0 to 0, 1 to 1 | +0.0012 |
| c04 | 18:53:43.565 | 80, -8.00 to +31.78 | 0, 0 to 0, 0 | None | Held | 20.959 | 0.44, 26.2 us | 11, 28.9 us | 0 to 0, 1 to 1 | 0.0000 |
| c05 | 18:54:46.633 | 80, -8.00 to +31.88 | 0, 0 to 0, 0 | None | Held | 153.259 | 2.38, 25.7 us | 10, 27.3 us | 0 to 0, 1 to 1 | -0.0004 |
| c06 | 18:55:38.529 | 80, -8.00 to +31.85 | 0, 0 to 0, 0 | None | Held | 57.238 | 2.50, 29.0 us | 11, 29.0 us | 0 to 0, 1 to 1 | +0.0005 |
| c07 | 18:56:30.394 | 80, -8.00 to +31.84 | 0, 0 to 0, 0 | None | Held | 192.267 | 2.64, 26.8 us | 9, 31.1 us | 0 to 0, 1 to 1 | -0.0009 |
| c08 | 18:57:27.295 | 80, -8.00 to +31.77 | 0, 0 to 0, 0 | None | Held | 91.662 | 0.20, 27.6 us | 19, 31.5 us | 0 to 0, 1 to 1 | +0.0002 |
| c09 | 18:58:19.017 | 80, -8.00 to +31.77 | 0, 0 to 0, 0 | None | Held | 170.932 | 0.25, 24.9 us | 13, 28.0 us | 0 to 0, 1 to 1 | +0.0004 |
| c10 | 18:59:10.797 | 80, -8.00 to +31.70 | 0, 0 to 0, 0 | None | Held | 189.988 | 3.26, 25.3 us | 11, 31.2 us | 0 to 0, 1 to 1 | +0.0019 |

Against B17's ten, on the same method:

| Cycle | B17 first peer PDU, ms | B17 slip: s from the bind, count | B17 first burst: s, peak | B18 first peer PDU, ms | B18 `SLIP_LB` change | B18 first burst: s, peak |
|---|---|---|---|---|---|---|
| c01 | 163.485 | 2.56 to 3.14, +2 dups | 2.82, 28.8 us | 135.267 | None | 4.74, 25.7 us |
| c02 | 93.536 | 1.09 to 1.96, +2 dups | 1.56, 25.0 us | 25.015 | None | 4.03, 25.1 us |
| c03 | 156.762 | 1.07 to 1.95, +2 dups | 1.83, 26.3 us | 165.076 | None | 0.38, 25.8 us |
| c04 | 52.750 | 3.10 to 3.68, +2 dups | 3.20, 29.3 us | 20.959 | None | 0.44, 26.2 us |
| c05 | 7.854 | 0.07 to 0.64, +2 dups | 0.10, 24.6 us | 153.259 | None | 2.38, 25.7 us |
| c06 | 131.486 | 3.57 to 4.15, +2 dups | 3.63, 25.8 us | 57.238 | None | 2.50, 29.0 us |
| c07 | 54.945 | 1.06 to 1.94, +2 dups | 1.36, 25.0 us | 192.267 | None | 2.64, 26.8 us |
| c08 | 28.539 | 1.17 to 1.94, +2 dups | 1.34, 25.6 us | 91.662 | None | 0.20, 27.6 us |
| c09 | 161.240 | 1.04 to 1.95, +2 dups | 1.28, 25.1 us | 170.932 | None | 0.25, 24.9 us |
| c10 | 101.128 | 5.09 to 5.67, +2 dups | 5.43, 26.9 us | 189.988 | None | 3.26, 25.3 us |

- **Grade.**
  - 10 held. There were 0 #743 residuals (+1 at the first PDU) and 0 of B17's class (c) (+2 at a later burst).
  - `SLIP_LB` read 0/0 in all 800 polls and at both baselines, and `SLIP_TDM` read 0.
  - No PDU more than 10 us late arrived before each cycle's first burst. That burst peaked at 24.9 to 29.0 us, against 24.6 to 29.3 us for the bursts that slipped B17's binds. Later bursts reached 32.0 us and slipped nothing.
- **CLOCK_SOURCE changes: none.**
- **Counters that moved.**
  - Of the polled words, only `RENDER_STAT` moved: prefill on each unbind, then converged at fill 8 to 14.
  - `MCSRV_STAT` read IDLE throughout, and `AAFM_STAT`, `AAFM_RATE`, `CRF_CTRL` and `CRF_RATE` read 0 throughout.
  - In GET_COUNTERS, the DUT's STREAM_INPUT 0 TIMESTAMP_VALID and FRAMES_RX restart at each re-bind. The peer's STREAM_OUTPUT 0 STREAM_START and STREAM_STOP each rose by 1 per cycle, and its FRAMES_TX counts on. Nothing else moved, on the DUT's STREAM_INPUT 0 or AVB_INTERFACE 0.
- **Restore.** The as-found binding (flags `0x0002`), CLOCK_SOURCE 0, both maps, every format, and the peer's bindings and clock source all read back. In the census, 45 of 46 entries are equal; the other is the DUT's live propagation delay, 382 to 388 ns. The residuals are the DUT's saved-state commits (0 to 20) and the peer's start and stop counters (+10 each). The bench lock is free. No lane process or file is left on the controller or tap host.

`HANDOFF.md`, `PR-BODY.md` and `MANIFEST.sha256` are in the lane's packet, `645-b18-a622`. Stopping here.
