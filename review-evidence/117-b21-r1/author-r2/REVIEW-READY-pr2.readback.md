[A625] REVIEW READY

Commit: `75853d80c22893448936bd1890e782bd0a0ce642` on branch `117-b21-bench` (one commit on `867fb945`; dev not merged; not pushed). PR #758 round 2, under the [PR round 2 assignment](https://github.com/kebag-logic/milan-fpga/pull/758#issuecomment-6231784136), answering R635-1 and R634-1.

Changed: `docs/findings/117_AUDIO_CONTINUITY.md` only (+232, -57), in the round 3 section and one round 1 sentence:
- restarts bounded from the rebind command to the first valid output sample, with a per-cycle table and planted-latency controls;
- the McASP grader compares slot words, and the Direction B recording is re-graded;
- step 1's nine floor groups stated as printed, with the sampler explanation corrected;
- published computations for every figure the reviews named;
- R1 to R5, S1 and S2.

Offline, from the round 3 records and the archived raws read by path. No bench action ran, and no lock was taken, so nothing needed restoring.

| Finding | Result |
|---|---|
| R635-1-F1, restart endpoint | PASS, 20 of 20. Upper bound on one clock, the bench host's: from the cycle driver's last event before the command to the external capture's read that delivered the first valid frame, so every output latency is inside it. Lower bound on the peer-link tap: from the received CONNECT_RX command to the packet carrying the first output frame's counter. Planted output latency: 0.5 s passes, 0.903 s fails cycle 19 only, 1.0 s fails all 20, each as predicted |
| R635-1-F2, grader proof | Alignments and runs are accepted only on equal words. The collision control now reads 1 foreign frame (the as-run grader: fully matched). Real recording: clean, 30,480,000 matched at offset 148,874, 0 unequal; the exact comparator agrees. The as-run grader is kept unchanged |
| R635-1-F3, leading insertion | Completes: 3 foreign zero frames, then an insertion of 3 (the as-run grader: exits 1) |
| R635-1-F4, R634-1-F1 | Eight positive groups (+6.3 to +8.4) and one negative (-2.5, reads 57,646 to 57,845). The sampler woke every 1.02 to 1.04 s, so no group is a missing cycle. In all nine, the sign follows the two windows' deepest sampler dips: a computed association |
| R634-1-F2 | Published: the transit fit (-13.070107 ppm, residual -27.681 to +23.894 µs), CRF per tap (324,903 and 324,906, 0 breaks, 500 pps), repeated frames (6,437,039 of 30,480,000, 21.1%) and the grader controls |
| R634-1-F3 | 17 of the 20 round 1 losses exceed the control maximum. The other three read +7.8, +6.8 and -5.2 |
| R1 to R5, S1, S2 | Applied. Direction B's values run -2 to +1 LSB. Step 1's mechanical verdict is CLEAN, and 9 of 9 planted losses are caught |

Restarts, rebind to the first valid output sample, in ms:

| Cycle | Lower bound, tap | Upper bound, bench host | Below 1 s |
|---|---|---|---|
| 1 | 41.5 | 51.0 | yes |
| 2 | 23.5 | 28.6 | yes |
| 3 | 23.4 | 33.7 | yes |
| 4 | 24.2 | 28.0 | yes |
| 5 | 23.2 | 32.3 | yes |
| 6 | 23.5 | 36.4 | yes |
| 7 | 23.5 | 32.6 | yes |
| 8 | 26.7 | 39.0 | yes |
| 9 | 23.7 | 33.3 | yes |
| 10 | 23.7 | 27.5 | yes |
| 11 | 23.7 | 31.8 | yes |
| 12 | 23.7 | 36.1 | yes |
| 13 | 23.7 | 32.2 | yes |
| 14 | 23.6 | 36.5 | yes |
| 15 | 23.9 | 30.8 | yes |
| 16 | 23.6 | 35.8 | yes |
| 17 | 23.8 | 30.3 | yes |
| 18 | 23.7 | 34.6 | yes |
| 19 | 96.7 | 100.7 | yes |
| 20 | 23.6 | 34.9 | yes |

Per-run results, round 3 as corrected:

| Run | Result |
|---|---|
| `mst-long`, step 1 | CLEAN: 63,000 reads of one period, 0 overruns, 0 stamper drops, block-floor change 2.81 frames, at most 4 allowed |
| `dA` | PASS: both taps 0 sequence breaks; 30,951,504 pattern frames valid and in order; 5,198,372 common packets equal in sequence number, timestamp and payload; peer output 638.0 s with 0 repeats, skips, zero or torn frames |
| `dB` | PASS: 30,480,000 McASP frames equal word for word to the received frames at one offset; corrected grader and exact comparator agree |
| `rA` | PASS: 20 of 20, upper bound 27.5 / 33.5 / 100.7 ms (min / median / max), lower bound 23.2 / 23.7 / 96.7 ms |

One correction to round 3 itself: its output figure assumed that the peer's last output frame before each silence was the wire's last frame. The frame counters show 486 to 540 more frames on the wire. The figure is kept as published and replaced by the two bounds.

Validation: working tree 9 gates and head 11 gates, all rc 0, unpiped, physical path, pinned Markdown interpreter: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base e4b771f9`, `check_doc_paths.py`, `ci_scope.py --selftest`, `check_baremetal_only.py --check`, `check_feature_status.py --self-test`, `git diff --check`, plus `git diff --check 867fb945 HEAD` and `git diff --check 4a9b5a2a HEAD`. Every analysis command, with its input hashes, is in the lane packet's `pr2/REPRODUCE.txt`; each exits 0.

Acceptance criteria: box 4, the audio continuity row, is PASS as measured on dev `9ef71772`, with the restart endpoint now the criterion's. This is an operator measurement, not a review verdict. Box 4's other rows and #117's other boxes are not this lane's.

Open risks/questions:
- The upper bound needs the bench host's realtime clock to run without a step through the capture. It moved 0.03 ms against the monotonic clock, and the tool refuses more than 1 ms.
- Step 1's verdict catches a 6-frame loss with 0.58 to 1.82 frames of margin.
- Re-review by R634-2 and R635-2.

Refs #117

