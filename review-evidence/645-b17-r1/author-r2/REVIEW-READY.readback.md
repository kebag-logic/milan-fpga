[A619] REVIEW READY
Commit: 56d008f68f445156a9bdd81eb32f8d5353cc7a7f (branch `645-b17-bench` from dev `f6260253`; local, not pushed, as assigned)
Changed: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` only: the dated section "Dev 5603c353, 2026-10-15: lane B17" and its Contents entry. Findings only.
Validation: all rc 0 on the head: `scripts/docs_check.py`, `scripts/check_doc_style.py`, `scripts/gen_toc.py --check`, `scripts/check_em_dash.py --base f6260253` (301 added lines, 0 findings), `scripts/check_doc_paths.py`, `scripts/check_baremetal_only.py --check`, `git diff --check`.
Acceptance criteria: 10 bind cycles run and polled as ruled; every slip timed and classed under [6186940255](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6186940255); restore done. Close condition NOT met: all 10 slips are (c), so #645 stays open.
Open risks/questions: on this image no CSR exposes the render recentre count (`recentres_o`) or the aligner's engaged and settled state, so (a) can be tested only through a CLOCK_SOURCE change, and none was made. The section states this.

**Run.** Resumed under the answer above, without the SoC board. Identity re-checked over ATDECC: PASS, the four ENTITY facts and CLOCK_SOURCE 0. The probe state was the state as found: the DUT on INTERNAL, its STREAM_INPUT 0 bound to the reference peer's AAF talker, and the peer's clock domain on the source of its CRF input, bound to the DUT's CRF talker.

Ten cycles were run, each one locked action: unbind, binding rule, re-bind 6 s later, then a 32 s hold. Formats were equal in all ten, so none was set. Every unbind and bind answered SUCCESS, and each cycle ended bound as found.

B8's poller ran unchanged, SHA-256 `1912837a1e4cfd6a1f8b3615b4d26924efbfd430aff239ebd18cd4dd2a67d4f7`. It read every 0.5 s from about 8 s before each bind to at least 31.75 s after it: 80 polls per cycle, none unreadable. The raw counter logs' digest is `a1d415300d55cfc2c14178493a244edab56446bbfa3aa860721e8b39819c7848`.

delta_ppm comes from the AAF presentation timestamps on the DUT's link tap: the peer's received stream less the DUT's own transmitted stream. At INTERNAL no DUT rate CSR compares them.

| Cycle | Bind, UTC | Settle boundary (B14's) | `SLIP_LB` dups | Slip: s from the bind, count | Before or after | Class | delta_ppm, rate interval | Largest PDU lateness in the slip's interval |
|---|---|---|---|---|---|---|---|---|
| c01 | 07:46:23.700 | Undefined (servo IDLE) | 208 to 210 | 2.56 to 3.14, +2 dups, 0 skips | No boundary | (c) | -0.0002, 104,167 s | 28.8 us |
| c02 | 07:47:50.970 | Undefined (servo IDLE) | 210 to 212 | 1.09 to 1.96, +2 dups, 0 skips | No boundary | (c) | +0.0006, 34,722 s | 25.0 us |
| c03 | 07:48:42.707 | Undefined (servo IDLE) | 212 to 214 | 1.07 to 1.95, +2 dups, 0 skips | No boundary | (c) | -0.0005, 41,667 s | 26.3 us |
| c04 | 07:49:34.411 | Undefined (servo IDLE) | 214 to 216 | 3.10 to 3.68, +2 dups, 0 skips | No boundary | (c) | -0.0017, 12,255 s | 29.3 us |
| c05 | 07:51:00.056 | Undefined (servo IDLE) | 216 to 218 | 0.07 to 0.64, +2 dups, 0 skips | No boundary | (c) | +0.0002, 104,167 s | 24.6 us |
| c06 | 07:51:51.933 | Undefined (servo IDLE) | 218 to 220 | 3.57 to 4.15, +2 dups, 0 skips | No boundary | (c) | +0.0016, 13,021 s | 25.8 us |
| c07 | 07:52:43.809 | Undefined (servo IDLE) | 220 to 222 | 1.06 to 1.94, +2 dups, 0 skips | No boundary | (c) | +0.0002, 104,167 s | 25.0 us |
| c08 | 07:53:40.237 | Undefined (servo IDLE) | 222 to 224 | 1.18 to 1.94, +2 dups, 0 skips | No boundary | (c) | +0.0003, 69,444 s | 25.6 us |
| c09 | 07:54:32.303 | Undefined (servo IDLE) | 224 to 226 | 1.04 to 1.95, +2 dups, 0 skips | No boundary | (c) | +0.0001, 208,333 s | 25.1 us |
| c10 | 07:55:24.165 | Undefined (servo IDLE) | 226 to 228 | 5.09 to 5.67, +2 dups, 0 skips | No boundary | (c) | +0.0006, 34,722 s | 26.9 us |

- **Slips.** One per bind, one frame each (2 dups per frame, as B14 counted), 0.07 to 5.67 s after the bind. There was no other `SLIP_LB` change: none in the 2 s bound before each unbind, none while unbound, none in the 26.1 to 31.2 s of each hold after the slip. `SLIP_TDM` read 0 throughout.
- **Aligner and servo state.** `MCSRV_STAT` read IDLE and `AAFM_STAT` 0 in every poll. `RENDER_STAT` left prefill 0.12 to 0.65 s after each bind, then read fill 8 to 14 and converged; rails stayed 11.
- **Class (a): 0.** No CLOCK_SOURCE change in any cycle. The aligner's re-engagement and excursions are not observable on this image.
- **Class (b): 0.** delta_ppm stayed within -0.0017 to +0.0016 ppm with the peer following the DUT's CRF. The rate interval was at least 12,255 s against about 34 s of bound polling, and a rate offset would not slip once per bind.
- **Bind priming.** The first peer PDU arrived 7.9 to 163.5 ms after the bind's command, at an arrival phase that was the same in every cycle. In every cycle, no PDU more than 10 us late arrived between the bind and the slip, and the first burst over 20 us late fell inside the slip's interval. The 10 to 23 later bursts per cycle, up to 30.3 us, slipped nothing.
- **Restore.** The as-found binding (flags `0x0002`), formats, maps and both clock sources read back. 45 of 46 census entries are equal; the other is the DUT's live propagation delay, 381 to 385 ns. Residuals: `SLIP_LB` 208 to 228 dups, and the DUT's saved-state commits 61 to 81. The bench lock is free and no lane process or file is left on the controller or tap host.

