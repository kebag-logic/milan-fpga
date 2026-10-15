[A622] Bench lane B18: #645 acceptance on dev `9ef71772`, all ten binds at INTERNAL hold the loopback ring

Closes #645.

Lane B18 repeats lane B17's ten binds on the image that carries PR #742, under the [B18 assignment](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6199691564). In PR #742, a listener bind's first PDU at INTERNAL arms the settle recentre. The close condition is the [ruling's](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6099627217), as the assignment states it: every bind at INTERNAL holds, apart from the #743 residual. It is met. All ten binds held, and no #743 residual occurred.

## Change

`docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` only. It adds the dated section "Dev 9ef71772, 2026-10-15: lane B18" and its Contents entry. The change is findings only, with no code, test or other document change.

## What was run

- **Image.** The installed dev `9ef71772`, flashed and cold-booted once by the manager before the lane. No flash, JTAG reload or power cycle in the lane, and no SoC board access. No device read distinguishes it from dev `5603c353`, so its identity rests on the manager's [provenance record](https://github.com/kebag-logic/milan-fpga/tree/bbc53aabb02a1654812ba2eaa1642f5e36e69ce0/review-evidence/645-b18-r1/manager-provenance) (evidence commit `bbc53aab`), which the section links: source dev `9ef71772`, bitstream SHA-256 `4b5a391af524cb3b490099381c0fd9e3275383fc51c163a75fb78cdb054ffcca`, verified flash-pair `FLASH_RC=0`, cold power cycle `POWERCYCLE_RC=0`, no fallback, and the boot line, all before the lane's identity reads.
- **Identity gate: PASS**, 11 of 11.
  - Over ATDECC: entity_id `020000fffe000001`, "Milan FPGA 1x1 TDM8", firmware_version `2.96.0`, serial `AX7101-0001`, the values B17 recorded.
  - On the console: `ID=4d494c4e VERSION=00020060`, and AEM CRC `5ba355eb` over 7,512 B.
  - Live ENTITY and CONFIGURATION equal the QSPI AEM bytes, and the clock sources are as for #629.
- **As found.** B17's probe state. The DUT is on CLOCK_SOURCE 0 (INTERNAL), and its STREAM_INPUT 0 is bound to the reference peer's AAF talker (flags `0x0002`), with formats equal. The peer follows the DUT's CRF. `SLIP_LB` reads 0 after the cold boot.
- **B17's method unchanged.** The cycle runner is B17's, with only its paths changed. The poller is B8's, unchanged, SHA-256 `1912837a1e4cfd6a1f8b3615b4d26924efbfd430aff239ebd18cd4dd2a67d4f7`. Each cycle is one locked action:
  1. unbind;
  2. apply the binding rule (formats were equal in all ten cycles, so none was set);
  3. re-bind 6 s later and hold 32 s.

  The poll ran every 0.5 s from 8.00 s before each bind to at least 31.70 s after it: 80 polls per cycle, none unreadable. The tap capture on the DUT's link is B17's.

## Per cycle

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

- **Grade against PR #742.** 10 held. There were 0 #743 residuals (+1 at the first PDU) and 0 of B17's class (c) (+2 at a later burst). `SLIP_LB` read 0 dups and 0 skips in all 800 polls and at both baselines, and `SLIP_TDM` read 0.
- **The stimulus that slipped B17 was present.** In every cycle, no PDU more than 10 us late arrived between the bind and the first burst over 20 us. That burst peaked at 24.9 to 29.0 us, against 24.6 to 29.3 us for the bursts that slipped B17's binds. It came 0.20 to 4.74 s after the bind, against 0.10 to 5.43 s in B17. Later bursts reached 32.0 us, and none moved the counter.
- **CLOCK_SOURCE.** There was no change. The DUT read 0 and the peer 1 at the start and end of every cycle.
- **Counters that moved.**
  - Of the polled words, only `RENDER_STAT` moved: prefill on each unbind, then converged at fill 8 to 14.
  - In GET_COUNTERS, the DUT's STREAM_INPUT 0 TIMESTAMP_VALID and FRAMES_RX restart at each re-bind. The peer's STREAM_OUTPUT 0 STREAM_START and STREAM_STOP each rose by 1 per cycle, and its FRAMES_TX counts on. Nothing else moved: MEDIA_UNLOCKED, STREAM_INTERRUPTED, SEQ_NUM_MISMATCH, MEDIA_RESET, LATE_TIMESTAMP and the other error counters stayed at 0; MEDIA_LOCKED read 1 at both reads.
- **Comparison with B17.** The section has the cycle-by-cycle table. B17 had 10 of 10 binds slip one frame (`SLIP_LB` 208 to 228). B18 had 0 of 10 (`SLIP_LB` 0 to 0).

## Limits

- No CSR on this image exposes the recentre count. The lane shows that the ring held; it does not show the recentre firing.
- In every cycle, the first late burst came at least 32.7 ms after the design's earliest firing time, which is the first PDU plus 42.7 ms. So the arming window itself was not tested; #743 tracks the in-window one-pair dup.
- A change would be timed to its poll interval, about 0.6 s.

## Restore

The DUT's STREAM_INPUT 0 is bound to the peer's talker with flags `0x0002`, as found, on CLOCK_SOURCE 0. Both maps, every format, and the peer's bindings and clock source are as found, all read back. In the census, 45 of 46 entries are equal; the other is the DUT's live propagation delay, 382 to 388 ns. The residuals are the DUT's saved-state commits (0 to 20) and the peer's start and stop counters (+10 each). The bench lock is free. No lane process or file is left on the controller or tap host.

## Validation

All rc 0 at the head, unpiped:
- `scripts/docs_check.py`
- `scripts/check_doc_style.py`
- `scripts/gen_toc.py --check`
- `scripts/check_em_dash.py --base 9ef71772` (315 added lines, 0 findings)
- `scripts/check_doc_paths.py`
- `scripts/check_baremetal_only.py --check`
- `git diff --check`

A mechanical check found that the section's two tables equal the summary tool's output, with 0 mismatches.

The raw counter logs' digest is `2c5e8d6ff8220cb16a9a3d0535279dfd7f04b5642c9aee2d9f97cdefcd939bdb`. The cycle runner's SHA-256 is `d41d0480ba17fdedd8ee73d5ee2ae973180bdda1e55a3d814a408790aa4e76e6`.

## Round 2

Under the [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6200530754), at head `b3f7a696713a96b42265e08a8c3a04a430b7b5ed`, one commit on `480c5e91`, the findings page only (+35, -12 lines in the B18 section). No figure, grade or table cell changed, and no bench access was made.

- **R635-1-F1.** The image paragraph in "B18: identity and setup" now links the manager's provenance record at `bbc53aab` and the chain comment. It states the source dev merge carrying PR #742, the bitstream SHA-256 `4b5a391a…` and AEM descriptor SHA-256, the verified flash-pair with `FLASH_RC=0`, the cold power cycle with `POWERCYCLE_RC=0` and no fallback, the cold-boot line, and that the identity reads ran after that boot with no flash or power cycle before the last cycle's end. It keeps the statement that no device read distinguishes the two images.
- **R634-1-S1.** One clause: in c01 and c10 the last poll fell 0.05 s short of B17's shortest, +31.75 s, from poll timing, and the counter is cumulative over that tail.
- **R634-1-S2.** "the design's earliest firing time" in the method, the bursts paragraph and the limits.
- **R634-1-S3.** The page names the published packet, `review-evidence/645-b18-r1/author` on branch `645-b18-review-evidence`, commit `2e913519`.

The seven gates above are rc 0 at the round-2 head (`check_em_dash.py`: 338 added lines, 0 findings).
