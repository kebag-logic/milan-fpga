[A624] REVIEW READY

Round 2 of bench lane B19 (Refs #117, Refs #387, Refs #621), under the [round 2 assignment](https://github.com/kebag-logic/milan-fpga/pull/751#issuecomment-6208623939). No bench, hardware, console, power-strip, tap, JTAG or controller-host access, and no bench lock; no graded result was re-run on hardware.

Commit: `c2243f791ced37dd2288dbf870758d93c5aa5325`, local on `117-b19-bench`, not pushed (the manager publishes). Six one-line commits on `d812a604`, which equalled origin at the start.
Changed: the two findings pages only (`734eb780..c2243f79`: +312 and +197 lines). The packet gained four analysis tools that read the hashed raws from the durable archive copy, by path. All 151 raws there were re-hashed at the start: 151 equal, 0 differ.
Validation: all 11 gates rc 0 at `c2243f79`, unpiped, physical path, pinned Markdown environment. They are `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base 734eb780` (0 findings over 509 added lines), `check_doc_paths.py`, `ci_scope.py --selftest`, `check_baremetal_only.py --check`, `check_feature_status.py --self-test`, `git diff --check`, `git diff --check 734eb780 HEAD` and `gen_toc.py --verify-anchors`. Tool controls: the box 3 grader 13 of 13, the GM-step tool 9 of 9.
Acceptance criteria: met for this round. Every round-1 finding is answered below. No PASS/FAIL changed, and no STOP condition was met: no box 3 edge fails under the stated model.
Open risks/questions: the closest box 3 edge (cycle 1 grandmaster loss) holds by 0.66 ms, and only because the read-to-PHC offset is at least 10.9 ms. That bound rests on the console's 144-byte transmit store, so a store 8 or more bytes larger would breach it. The offset's upper bound includes a 1 ms formatting allowance, an engineering bound rather than a measurement. #387 item 4's `A_MCSRV_STAT` observable was not exercised on `9ef71772`, since the DUT ran on INTERNAL.

| Finding | Fixed at (head `c2243f79`) | Discharging output |
|---|---|---|
| R635-1-F1 / R634-1-F5 | `387_SOFTWARE_GM_STEP.md:474` (role label, the `d812a604` amend) | `git grep` under `docs/` for five forms of the value: 0 hits each |
| R635-1-F2 / R634-1-F2 | `117_GPTP_SILICON_EVIDENCE.md:821`, `:866-873`, `:936-939`, `:950`, `:976-982`, `:984-1016` | offset model: d from 10.94 ms to 16.53-19.75 ms per action, from 271-272 line bytes, the 144-byte store, 86.8 us per byte and per-record idle; 0 of 2,880 records refute it. Grader: 27 of 27 PASS, 11 within 25 ms; the three counterexamples were -10.2, -9.1 and -3.7 ms without the offset |
| R635-1-F3 | `387_SOFTWARE_GM_STEP.md:425-441`, `:447-456`, `:458-460`, `:484` | four `tu` set rows one sample earlier, every steady clear 31-32 ms earlier, steady after set 0.25 to 0.75 s, wire episodes 0.376 to 0.684 s. The step-bracket control keeps the first `tu=1` sample, and the round-1 search drops it |
| R634-1-F3 | `387_SOFTWARE_GM_STEP.md:386`, `:415`, `:461`, `:482`; `117_GPTP_SILICON_EVIDENCE.md:1024`, `:1029` | 2,399 samples and 600 answered DUT polls, 0 asCapable 0, peer delay 373 to 392 ns in both; a planted poll with asCapable 0 fails its edge. 149,513 over 300 polls. Lag 167 to 7,925 over 26 reads (first and last of 13 actions), 0 to 7,925 over all 1,495 polls |
| R634-1-F1 | `117_GPTP_SILICON_EVIDENCE.md:835-838`, `387_SOFTWARE_GM_STEP.md:374-381` | PR #747 provenance at `bbc53aab`: bitstream `4b5a391a...4ffcca`, AEM `4fc8d615...db396d`; continuity from item 8 |
| R634-1-F4 | `117_GPTP_SILICON_EVIDENCE.md:1071-1077`, `387_SOFTWARE_GM_STEP.md:503-507` | manager receipt 6208612856 |
| R635-1-R1 / R634-1-R1 | proposed PR body, Status and roles | for the manager to apply |
| R635-1-R2, R634-1-R2, R634-1-S1 | `117_GPTP_SILICON_EVIDENCE.md:822`, `:1023`; `387_SOFTWARE_GM_STEP.md:391-392`, `:400` | applied |

Per cycle (seconds after the OUT4 off command; console times are PHC-read placements, and the words were read 10.9 to 19.7 ms earlier):

| Cycle | CRF binding | Switch first Announce | DUT all-good | Recovery (s) | 5 s bound | Box 3 edges (with the first `tu=1` PDU in cycles 1 to 3) |
|---|---|---:|---:|---:|---|---|
| 1 | yes | 40.26 | 41.75 | 1.49 | PASS | 5 of 5 PASS |
| 2 | yes | 40.37 | 41.00 | 0.63 | PASS | 5 of 5 PASS |
| 3 | yes | 40.23 | 42.00 | 1.77 | PASS | 5 of 5 PASS |
| 4 | no | 40.27 | 41.01 | 0.75 | PASS | 4 of 4 PASS |
| 5 | no | 40.25 | 40.75 | 0.50 | PASS | 4 of 4 PASS |
| 6 | no | 40.26 | 40.74 | 0.47 | PASS | 4 of 4 PASS |

Per step (seconds after the software-grandmaster start; console times at command send, each within an interval at most 0.282 s wide):

| Run | Edge | DUT PHC step | `tu` rises console / CRF | `tu` set / steady clear | asCapable 0, samples / polls | GM_CHANGED | `mr` changes | Grade |
|---|---|---|---|---|---|---:|---:|---|
| 1 | takeover | +9.987 ms | 1 / 1 | 3.756 / 4.256 | 0 / 0 | +1 | 0 | PASS |
| 1 | release | -10.003 ms | 1 / 1 | 50.527 / 51.027 | 0 / 0 | +1 | 0 | PASS |
| 2 | takeover | +9.987 ms | 1 / 1 | 3.755 / 4.005 | 0 / 0 | +1 | 0 | PASS |
| 2 | release | -10.004 ms | 1 / 1 | 50.523 / 51.023 | 0 / 0 | +1 | 0 | PASS |
| 3 | takeover | +9.987 ms | 1 / 1 | 3.505 / 4.006 | 0 / 0 | +1 | 0 | PASS |
| 3 | release | -10.004 ms | 1 / 1 | 50.524 / 51.024 | 0 / 0 | +1 | 0 | PASS |
| 4 | takeover | +9.987 ms | 1 / 1 | 4.005 / 4.255 | 0 / 0 | +1 | 0 | PASS |
| 4 | release | -10.005 ms | 1 / 1 | 50.522 / 51.022 | 0 / 0 | +1 | 0 | PASS |
| 5 | takeover | +9.987 ms | 1 / 1 | 3.550 / 4.300 | 0 / 0 | +1 | 0 | PASS |
| 5 | release | -10.004 ms | 1 / 1 | 50.449 / 50.949 | 0 / 0 | +1 | 0 | PASS |

Delta reviews follow: R634-2 and R635-2.

