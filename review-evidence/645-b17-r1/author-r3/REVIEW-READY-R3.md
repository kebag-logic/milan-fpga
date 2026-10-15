[A619] REVIEW READY (B17 round 3, PR #741)

Commit: `71d5e08506168e88f52a998a05f1d43b4801d2a5` on `645-b17-bench`, one commit after `b2891a8f29598fff1865f855991ad4c1505e35a3`. Not pushed.

Answers [the round 3 assignment](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6188583660) and R634-2-F1. The B17 section now states the grouping actually used: PDUs more than 20 us late, grouped while less than 1 ms apart, with 3 to 12 such PDUs each. The PR body bullet follows the page. Every printed range is retained. Only that definition and two artifact hash rows change in the repository (+3/-3).

Verification: the lane summary rerun returns 0 and reproduces every burst range. Numeric summaries and raw counter-log digest remain byte-identical to round 2. The page/PR-body check returns 84 checks, 0 mismatches. Source: `tools/summ_b17.py`, 20,127 bytes, SHA-256 `6e3335558430775f481e0fce56dcbfaffee494134eeec03a0d14e7e9717b5652`.

All required gates return 0 with the pinned Markdown environment: `scripts/docs_check.py`, `scripts/check_doc_style.py`, `scripts/gen_toc.py --check`, `scripts/check_em_dash.py --base f6260253`, `scripts/check_doc_paths.py`, `scripts/check_baremetal_only.py --check`, and `git diff --check`.

Per-cycle slips, unchanged:

| Cycle | Bind, UTC | Settle boundary | Polls, s from the bind | `SLIP_LB` dups | Slip: s from the bind, count | Before or after | Class | delta_ppm, rate interval | Largest lateness in the slip's interval |
|---|---|---|---|---|---|---|---|---|---|
| c01 | 07:46:23.700 | Undefined (servo IDLE) | 80, -8.00 to +31.77 | 208 to 210 | 2.56 to 3.14, +2 dups, 0 skips | No boundary | (c) | -0.0002, 104,167 s | 28.8 us |
| c02 | 07:47:50.970 | Undefined (servo IDLE) | 80, -8.00 to +31.83 | 210 to 212 | 1.09 to 1.96, +2 dups, 0 skips | No boundary | (c) | +0.0006, 34,722 s | 25.0 us |
| c03 | 07:48:42.707 | Undefined (servo IDLE) | 80, -7.99 to +31.75 | 212 to 214 | 1.07 to 1.95, +2 dups, 0 skips | No boundary | (c) | -0.0005, 41,667 s | 26.3 us |
| c04 | 07:49:34.411 | Undefined (servo IDLE) | 80, -8.00 to +31.83 | 214 to 216 | 3.10 to 3.68, +2 dups, 0 skips | No boundary | (c) | -0.0017, 12,255 s | 29.3 us |
| c05 | 07:51:00.056 | Undefined (servo IDLE) | 80, -8.00 to +31.84 | 216 to 218 | 0.07 to 0.64, +2 dups, 0 skips | No boundary | (c) | +0.0002, 104,167 s | 24.6 us |
| c06 | 07:51:51.933 | Undefined (servo IDLE) | 80, -7.99 to +31.83 | 218 to 220 | 3.57 to 4.15, +2 dups, 0 skips | No boundary | (c) | +0.0016, 13,021 s | 25.8 us |
| c07 | 07:52:43.809 | Undefined (servo IDLE) | 80, -8.01 to +31.84 | 220 to 222 | 1.06 to 1.94, +2 dups, 0 skips | No boundary | (c) | +0.0002, 104,167 s | 25.0 us |
| c08 | 07:53:40.237 | Undefined (servo IDLE) | 80, -7.99 to +31.93 | 222 to 224 | 1.17 to 1.94, +2 dups, 0 skips | No boundary | (c) | +0.0003, 69,444 s | 25.6 us |
| c09 | 07:54:32.303 | Undefined (servo IDLE) | 80, -8.00 to +31.78 | 224 to 226 | 1.04 to 1.95, +2 dups, 0 skips | No boundary | (c) | +0.0001, 208,333 s | 25.1 us |
| c10 | 07:55:24.165 | Undefined (servo IDLE) | 80, -8.00 to +31.80 | 226 to 228 | 5.09 to 5.67, +2 dups, 0 skips | No boundary | (c) | +0.0006, 34,722 s | 26.9 us |

Per-cycle burst counts under the stated rule:

| Cycle | Bursts to last poll | Bursts to capture end | After slip to last poll | After slip to capture end | Further bursts |
|---|---|---|---|---|---|
| c01 | 14 | 21 | 13 | 20 | 7 |
| c02 | 9 | 11 | 8 | 10 | 2 |
| c03 | 13 | 19 | 12 | 18 | 6 |
| c04 | 11 | 15 | 10 | 14 | 4 |
| c05 | 19 | 22 | 18 | 21 | 3 |
| c06 | 11 | 13 | 10 | 12 | 2 |
| c07 | 18 | 22 | 17 | 21 | 4 |
| c08 | 18 | 24 | 17 | 23 | 6 |
| c09 | 13 | 19 | 12 | 18 | 6 |
| c10 | 9 | 13 | 8 | 12 | 4 |

The last poll is +31.75 to +31.93 s after the bind; capture end is about +41.9 s. The further-burst column is capture count minus last-poll count.

HANDOFF.md, PR-BODY.md and MANIFEST.sha256 are current in packet `645-b17-a619`. Recorded data only; no bench, console, controller, tap or power access, and no lock acquired. The recorded restore is unchanged. No new TAKEN post. R634 alone re-checks this delta under the assignment.

Refs #645. All ten slips remain class (c); the issue stays open.
