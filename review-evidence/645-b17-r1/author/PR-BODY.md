[A619] Record #645 bench lane B17 on dev 5603c353: the loopback slips timed through ten binds at INTERNAL

Refs #645

Adds the dated section "Dev 5603c353, 2026-10-15: lane B17" and its Contents entry to `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, the page lane B15 used. No other file changes. Findings documents only: no RTL, firmware, test or gate change.

Lane B17 carries out the ruling https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6099627217 under the assignment https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6186729424, resumed under https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6186940255 (no SoC board; each slip classed (a), (b) or (c)).

## Result

On the installed dev `5603c353` image, the DUT was on INTERNAL with the reference peer's AAF talker bound to the DUT's STREAM_INPUT 0, the state as found. Ten unbind and re-bind cycles were polled every 0.5 s, from about 8 s before each bind to at least 31.75 s after it.

| Cycle | Bind, UTC | Settle boundary | `SLIP_LB` dups | Slip: s from the bind, count | Class | delta_ppm, rate interval |
|---|---|---|---|---|---|---|
| c01 | 07:46:23.700 | Undefined (servo IDLE) | 208 to 210 | 2.56 to 3.14, +2 dups | (c) | -0.0002, 104,167 s |
| c02 | 07:47:50.970 | Undefined (servo IDLE) | 210 to 212 | 1.09 to 1.96, +2 dups | (c) | +0.0006, 34,722 s |
| c03 | 07:48:42.707 | Undefined (servo IDLE) | 212 to 214 | 1.07 to 1.95, +2 dups | (c) | -0.0005, 41,667 s |
| c04 | 07:49:34.411 | Undefined (servo IDLE) | 214 to 216 | 3.10 to 3.68, +2 dups | (c) | -0.0017, 12,255 s |
| c05 | 07:51:00.056 | Undefined (servo IDLE) | 216 to 218 | 0.07 to 0.64, +2 dups | (c) | +0.0002, 104,167 s |
| c06 | 07:51:51.933 | Undefined (servo IDLE) | 218 to 220 | 3.57 to 4.15, +2 dups | (c) | +0.0016, 13,021 s |
| c07 | 07:52:43.809 | Undefined (servo IDLE) | 220 to 222 | 1.06 to 1.94, +2 dups | (c) | +0.0002, 104,167 s |
| c08 | 07:53:40.237 | Undefined (servo IDLE) | 222 to 224 | 1.18 to 1.94, +2 dups | (c) | +0.0003, 69,444 s |
| c09 | 07:54:32.303 | Undefined (servo IDLE) | 224 to 226 | 1.04 to 1.95, +2 dups | (c) | +0.0001, 208,333 s |
| c10 | 07:55:24.165 | Undefined (servo IDLE) | 226 to 228 | 5.09 to 5.67, +2 dups | (c) | +0.0006, 34,722 s |

- **Slips.** One per bind, one frame each: +2 dups, with two loopback pairs fed. Each fell 0.07 to 5.67 s after the bind. None came later in any hold, before the unbind or while unbound. `SLIP_TDM` read 0 throughout.
- **Class (a): none shown.** No CLOCK_SOURCE changed. On this image no CSR exposes the render recentre count or the aligner's state.
- **Class (b): excluded.** delta_ppm comes from the AAF presentation timestamps on the DUT's link tap. It stayed within -0.0017 to +0.0016 ppm, a rate interval of at least 12,255 s.
- **Verdict.** All ten slips are (c), so under the ruling #645 stays open.
- **Bind priming.** In every cycle, no PDU more than 10 us late arrived between the bind and the slip. The first peer-PDU burst over 20 us late after the bind (24.6 to 29.3 us) fell inside the slip's interval. The 10 to 23 later bursts, up to 30.3 us, slipped nothing.
- **Restore.** The as-found binding, formats, maps and clock sources read back. 45 of 46 census entries are equal; the other is the live propagation delay. Residuals: `SLIP_LB` 208 to 228, and the DUT's saved-state commits 61 to 81.

## Validation

All rc 0 on the head, with the pinned Markdown environment: `scripts/docs_check.py`, `scripts/check_doc_style.py`, `scripts/gen_toc.py --check`, `scripts/check_em_dash.py --base f6260253` (301 added lines, 0 findings), `scripts/check_doc_paths.py`, `scripts/check_baremetal_only.py --check`, and `git diff --check`.

The manager holds the lane packet `645-b17-a619`, which is not published in the tree. It carries the per-cycle events and raw counter logs, the grades, the controls, the restore reads and the tool hashes.
