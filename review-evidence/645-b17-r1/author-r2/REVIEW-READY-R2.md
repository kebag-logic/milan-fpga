[A619] REVIEW READY (B17 round 2, PR #741)
Commit: b2891a8f29598fff1865f855991ad4c1505e35a3 (branch `645-b17-bench`, one commit on the round 1 head `56d008f68f445156a9bdd81eb32f8d5353cc7a7f`; not pushed, per the assignment)
Changed: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, inside the B17 section only (+98/-29). Recorded data only: no bench, console, controller, tap or power access in this round.

Answers [the round 2 assignment](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6187961942):

- **R634-1-F1.** Every after-slip figure now names its window: "to the last poll" (+31.75 to +31.93 s after the bind; the 32 s hold gives the same ranges) or "to the capture's end" (about 41.9 s). To the last poll there were 8 to 18 bursts after the slip, peaking at 27.1 to 30.1 us, and a later, larger burst in 9 of 10 cycles. To the capture's end there were 10 to 23, peaking at 27.6 to 30.3 us. Bursts per cycle: 9 to 19 to the last poll and 11 to 24 to the capture's end. The section says that nothing slipping after the last poll rests on the cumulative counter: c01's first `SLIP_LB` read equals the start baseline (208), each later first read equals the previous cycle's last, and c10's last equals the end baseline (228). `RENDER_STAT` is now a bracket: prefill read 0 by 0.12 to 0.65 s after the bind (the end of the first poll that read it), and the exit comes after the first peer PDU. Converged read 1 one poll later in c02, c04, c05 and c07 (by 0.64 to 0.67 s). The summary tool generates the windowed table; the PR body bullet is bounded the same way.
- **R635-1-F1.** The summary tool now computes every poll figure from the raw counter log and rounds it once. A tap figure, which only the grade carries, is printed only where no rounding tie makes it depend on the grade's dropped digits; there were 0 ties. c08's slip now reads 1.17 to 1.94 and c09's last poll +31.78. A new check recomputes every poll cell of the slips table from the raw counter logs and compares the page and the PR body with the summary: 84 checks, 0 mismatches. On the round 1 page the same check finds 15 mismatches, including exactly the c08 and c09 cells.
- **Residue and suggestions, all taken.** The RTL citation now names its revision (`:6810-6812` at dev `f6260253`, `:6797-6799` in `5603c353`). The phase sentence reads "as expected with". The section locates the published round 1 packet (`review-evidence/645-b17-r1/author`, branch `645-b17-review-evidence`, commit `35cc1ae4`). It adds the two longer polls per cycle (S1). The one after the bind lies inside five slip intervals and outside five, so it does not line up with the slips. It explains c08's extra frames (S2): the peer's own AAF stream kept arriving on the DUT's link for 4.87 s after the unbind (0.02 to 0.18 s in the other nine cycles). Meanwhile the DUT read prefill and `SLIP_LB` did not move, and no other stream appears. It states the 0.0001 ppm resolution of delta_ppm (S3), at which the rate interval is still at least 11,574 s.

No class, count, verdict or slip time changed: 10 slips, all (c), and #645 stays open.

Validation (all rc 0 on `b2891a8f2`, pinned Markdown environment): `scripts/docs_check.py`, `scripts/check_doc_style.py`, `scripts/gen_toc.py --check` (and `--verify-anchors`), `scripts/check_em_dash.py --base f6260253` (370 added lines, 0 findings), `scripts/check_doc_paths.py`, `scripts/check_baremetal_only.py --check`, `git diff --check f6260253 HEAD` and `git diff --check`.

Per cycle, slips table as on the page:

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

Per cycle, after-slip windows and `RENDER_STAT` brackets (seconds from the bind; burst = PDUs over 20 us late, under 1 ms apart):

| Cycle | Last poll, s | Slipping burst peak | After the slip, to the last poll: bursts, peak | Later and larger | After the slip, to the capture's end: bursts, peak | `RENDER_STAT` prefill exit bracket, s | Converged by, s |
|---|---|---|---|---|---|---|---|
| c01 | +31.77 | 28.8 us | 13, 28.7 us | no | 20, 28.7 us | 0.163 to 0.625 | 0.63 |
| c02 | +31.83 | 25.0 us | 8, 28.4 us | yes | 10, 28.4 us | 0.094 to 0.165 | 0.67 |
| c03 | +31.75 | 26.3 us | 12, 28.7 us | yes | 18, 28.7 us | 0.157 to 0.649 | 0.65 |
| c04 | +31.83 | 29.3 us | 10, 30.1 us | yes | 14, 30.1 us | 0.053 to 0.140 | 0.65 |
| c05 | +31.84 | 24.6 us | 18, 29.3 us | yes | 21, 30.3 us | 0.008 to 0.138 | 0.64 |
| c06 | +31.83 | 25.8 us | 10, 28.5 us | yes | 12, 28.5 us | 0.131 to 0.643 | 0.64 |
| c07 | +31.84 | 25.0 us | 17, 29.1 us | yes | 21, 29.1 us | 0.055 to 0.123 | 0.64 |
| c08 | +31.93 | 25.6 us | 17, 27.1 us | yes | 23, 27.6 us | 0.029 to 0.249 | 0.25 |
| c09 | +31.78 | 25.1 us | 12, 29.5 us | yes | 18, 29.5 us | 0.161 to 0.622 | 0.62 |
| c10 | +31.80 | 26.9 us | 8, 27.8 us | yes | 12, 27.8 us | 0.101 to 0.653 | 0.65 |

Acceptance criteria: the round 2 items 1 to 3 are met, with the evidence above. The ruling's close condition is still not met, so the PR body says Refs #645.
Open risks/questions: none new. The round 2 tools and summary are in the manager's packet. Round 1 publication of the packet is unaffected.
