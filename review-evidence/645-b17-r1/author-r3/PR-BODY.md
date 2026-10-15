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
| c08 | 07:53:40.237 | Undefined (servo IDLE) | 222 to 224 | 1.17 to 1.94, +2 dups | (c) | +0.0003, 69,444 s |
| c09 | 07:54:32.303 | Undefined (servo IDLE) | 224 to 226 | 1.04 to 1.95, +2 dups | (c) | +0.0001, 208,333 s |
| c10 | 07:55:24.165 | Undefined (servo IDLE) | 226 to 228 | 5.09 to 5.67, +2 dups | (c) | +0.0006, 34,722 s |

- **Slips.** One per bind, one frame each: +2 dups, with two loopback pairs fed. Each fell 0.07 to 5.67 s after the bind. None came later in any hold, before the unbind or while unbound. `SLIP_TDM` read 0 throughout.
- **Class (a): none shown.** No CLOCK_SOURCE changed. On this image no CSR exposes the render recentre count or the aligner's state.
- **Class (b): excluded.** delta_ppm comes from the AAF presentation timestamps on the DUT's link tap. It stayed within -0.0017 to +0.0016 ppm, a rate interval of at least 12,255 s.
- **Verdict.** All ten slips are (c), so under the ruling #645 stays open.
- **Bind priming.** A burst groups PDUs more than 20 us late while less than 1 ms apart, with 3 to 12 such PDUs each. In every cycle, no PDU more than 10 us late arrived between the bind and the slip. The first peer-PDU burst over 20 us late after the bind (24.6 to 29.3 us) fell inside the slip's interval. To the last poll (+31.75 to +31.93 s after the bind; the 32 s hold gives the same ranges), the 8 to 18 later bursts, up to 30.1 us, left `SLIP_LB` unchanged. The 2 to 7 further bursts per cycle to the capture's end (about 41.9 s after the bind) slipped nothing either; that rests on the cumulative counter: each cycle's first `SLIP_LB` read equals the previous cycle's last, c01's first equals the start baseline (208) and c10's last the end baseline (228).
- **Restore.** The as-found binding, formats, maps and clock sources read back. 45 of 46 census entries are equal; the other is the live propagation delay. Residuals: `SLIP_LB` 208 to 228, and the DUT's saved-state commits 61 to 81.

## Validation

All rc 0 on the head, with the pinned Markdown environment: `scripts/docs_check.py`, `scripts/check_doc_style.py`, `scripts/gen_toc.py --check`, `scripts/check_em_dash.py --base f6260253` (370 added lines, 0 findings), `scripts/check_doc_paths.py`, `scripts/check_baremetal_only.py --check`, and `git diff --check`.

The lane packet `645-b17-a619` carries the per-cycle events and raw counter logs, the grades, the controls, the restore reads and the tool hashes. Its first round is published as `review-evidence/645-b17-r1/author` on branch `645-b17-review-evidence` (commit `35cc1ae4`); the manager holds the second round's tools and summary.

## Round 2

Answers the two round-1 reviews, R634-1 and R635-1, from the recorded data only: no bench, console, controller or tap access.

- **R634-1-F1 (after-slip windows).** Bursts use the same grouping stated above. Every after-slip figure now names its window. To the last poll: 8 to 18 bursts after the slip, peaking at 27.1 to 30.1 us, and a later, larger burst in 9 of 10 cycles; the 32 s hold gives the same ranges. To the capture's end, about 41.9 s after the bind: 10 to 23 bursts, peaking at 27.6 to 30.3 us. Bursts per cycle: 9 to 19 to the last poll and 11 to 24 to the capture's end. That nothing slipped after the last poll is stated as resting on the cumulative counter. `RENDER_STAT` is now given as a bracket: prefill read 0 by 0.12 to 0.65 s after each bind (the end of the first poll that read it), after the first peer PDU; in c05 the bracket is 0.008 to 0.138 s. Converged read 1 from that poll in six cycles and from the next one, by 0.64 to 0.67 s, in c02, c04, c05 and c07.
- **R635-1-F1 (rounding).** The summary tool now computes every poll figure from the raw counter log and rounds it once. A tap figure, which only the grade carries, is printed only where no rounding tie makes it depend on the grade's dropped digits; none does. c08's slip reads 1.17 to 1.94 s and c09's last poll +31.78 s. A new check recomputes every poll cell of the slips table from the raw counter logs: 0 mismatches on this page. On the round-1 page it finds exactly those two cells.
- **Residue and suggestions.** The RTL line citation now names its revision. The arrival-phase sentence now reads "as expected with", not "because". The section says where the round-1 packet is published. It records the two polls per cycle that took longer than the rest, about 1.55 s after each unbind and each bind: the one after the bind lies inside five slip intervals and outside the other five, so it does not line up with the slips. It records c08's extra capture frames: the peer's own stream, still arriving on the DUT's link for 4.87 s after the unbind, while the DUT read prefill and `SLIP_LB` did not move. It states the 0.0001 ppm resolution of delta_ppm, at which the rate interval is still at least 11,574 s.

No class, count, verdict or slip time changes. Every slip is still (c), and #645 stays open.

## Round 3

Answers R634-2-F1 under the round 3 assignment (https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6188583660). The page now states the existing burst grouping: PDUs more than 20 us late, grouped while less than 1 ms apart, with 3 to 12 such PDUs each. Every printed range is retained. Recorded data only; R634 re-checks this delta.

Round 3 head: `71d5e08506168e88f52a998a05f1d43b4801d2a5`. The recorded-data summary reproduces every burst range; the page check returns 84 checks, 0 mismatches. All seven required gates return 0. Only the B17 burst wording and its two artifact receipts change in this delta.
