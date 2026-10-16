[A624] Bench lane B19 on the installed dev `9ef71772` image: #117 boxes 1 to 3 and box 4's protocol rows, and the software-grandmaster steps for #621 item 3 and #387 item 4.

Refs #117
Refs #387
Refs #621

## Status

Commit `c2243f791ced37dd2288dbf870758d93c5aa5325` on branch `117-b19-bench` from dev `734eb780`: round 2, six commits on `d812a604`. Published for independent review; PR open against `dev`; reviewers R634 (internal) and R635 (external). Closing #117 waits for the manager's review of its remaining rows.

## Linked issue and roles

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-6207451080
- Executor: [A624]. Reviewers: R634 (internal) and R635 (external).
- Round 2 assignment: https://github.com/kebag-logic/milan-fpga/pull/751#issuecomment-6208623939

## Description

Two dated sections, findings docs only:

- `docs/findings/117_GPTP_SILICON_EVIDENCE.md`, "2026-10-16: bench lane B19 on dev 9ef71772" (+312 lines with its Contents entry).
- `docs/findings/387_SOFTWARE_GM_STEP.md`, the section of the same name (+197 lines with its Contents entry).

No other file changed.

| Item | Verdict | Evidence |
|---|---|---|
| Identity gate (lane B18's method) | PASS, 11 of 11 | identity rests on PR #747's provenance record (bitstream SHA-256 `4b5a391a...4ffcca`, AEM `4fc8d615...db396d`), since no device read distinguishes the image from `5603c353`; continuity from the manager's receipt (round 2 assignment, item 8). Console `ID=4d494c4e VERSION=00020060`, AEM CRC `5ba355eb` over 7,512 B, live ENTITY and CONFIGURATION equal to QSPI, clock sources, grader 10/10, ADP model `001bc5c1935893e1`; the cold boot printed the boot line, the AEM CRC and "fabric entity enabled" |
| Box 1, first reach (one OUT0 cold cycle) | PASS | first frame 8.06 s after power-on; the switch's first Announce and Sync 1.74 s later; the DUT's second completed Pdelay exchange 1.00 s after the first frame; its first AECP answer (9.96 s) already asCapable |
| Box 1, retention, cadence, turnaround, no daemon | PASS | 1,200/1,200 console samples and 300/300 polls asCapable; every interval within 30 %; DUT turnaround at most 13.432 us; peer delay 372 to 391 ns |
| Box 2, six switch cycles | PASS | recovery 0.47 to 1.77 s against 5 s; one stream restart per return in the three bound cycles |
| Box 3, publication words and `tu` | PASS | steady state over 300 s; under the stated time base (read-to-PHC offset 10.9 to 19.7 ms, placement error at most 1.32 ms) all 27 graded edges hold for every admissible offset: 24 CSR edges have their wire cause or receipt timeout inside the read bracket, and the first `tu=1` CRF PDU lies in the `CLKV_STAT[0]` rise interval in cycles 1 to 3. 11 edges lie within 25 ms of a boundary, the closest by 0.66 ms |
| Box 4, counters probe parity | PASS | identical result lines; the target-identity line differs; both CLEAN, 0 complaints |
| Box 4, per-AVTPDU counters (#726, PR #729) | PASS | CRF FRAMES_TX equals the wire; every talker and listener pair counts at the packet rate |
| Box 4, three headless enumerations | PASS | `IEEE17221` and `MILAN` every run, 0 DUT complaints, 0 query errors, 42 descriptors |
| #621 item 3, five GM steps | PASS | 10 of 10 edges, no asCapable loss in 2,399 console samples and 600 answered DUT polls, both arms of the grade |
| #387 item 4, wire and counter observables | PASS | one `tu` episode, GPTP_GM_CHANGED +1, no `mr` change, MEDIA_RESET flat and no listener unlock at every edge; the render re-base count is carried by simulation per the assignment's decision |

Seconds after the OUT4 off command:

| Cycle | CRF binding | Switch first Announce | DUT all-good | Recovery (s) | 5 s bound |
|---|---|---:|---:|---:|---|
| 1 | yes | 40.26 | 41.75 | 1.49 | PASS |
| 2 | yes | 40.37 | 41.00 | 0.63 | PASS |
| 3 | yes | 40.23 | 42.00 | 1.77 | PASS |
| 4 | no | 40.27 | 41.01 | 0.75 | PASS |
| 5 | no | 40.25 | 40.75 | 0.50 | PASS |
| 6 | no | 40.26 | 40.74 | 0.47 | PASS |

| Run | Edge | DUT PHC step | `tu` rises console / CRF | `tu` set / steady clear (s) | asCapable 0, samples / polls | GM_CHANGED | `mr` changes | Grade |
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

## Authoritative references

- #117 owner decisions: the OUT4 cycle and the 5 s bound (comment 5795898094), the headless enumeration (5858063707).
- #387: the step policy (5794731090), the stimulus (5862116683, 5862731997), the #602 ruling; #621 and PR #707.
- `docs/design/GM_LOSS_RECOVERY.md`, `docs/design/TIME_SYNC.md`, `docs/testing/TESTING.md` sections 6, 6b and 6c, `docs/testing/726_STREAM_COUNTERS.md`.

## How to get into the same state

The bench state is restored and read back: the music and CRF bindings, both clock sources, the controller host's timestamping and clock, and every outlet on, as found. The tools are in the private bench packet `117-b19-a624`, with `MANIFEST.sha256` and `RAW-ARTIFACTS.json`. All 151 raw files are in the project's durable cold archive, SHA-256 re-verified there (manager receipt 6208612856: 151 equal, 0 differ, 0 missing).

## How to validate

All rc 0 at `c2243f79`, from the physical lane path, none piped, the Markdown gates in the pinned environment: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base 734eb780` (0 findings over 509 added lines), `check_doc_paths.py`, `scripts/ci_scope.py --selftest`, `scripts/check_baremetal_only.py --check`, `scripts/check_feature_status.py --self-test`, `git diff --check`, and `git diff --check 734eb780 HEAD`; also `gen_toc.py --verify-anchors`.

## Known limitations and out of scope

- The first-reach console stopped polling after the boot prompt (a reader defect). OUT0 is switched once per lane, so the DUT end's asCapable time comes from the wire and its first AECP answer.
- The reference peer's own recovery time is not measured: its link was not captured.
- The GM-step leg ran on the as-found streams: the peer follows the DUT's CRF, so lane B1's reverse CRF binding with CRF selection on the DUT was not made, and the DUT's CRF servo stayed idle.
- Residuals no permitted command clears: the DUT's MAAP destination addresses (re-claimed at the cold boot) and `SLIP_LB` dups saturated at `0xFFFF`.
- Out of scope, owner items: audio continuity, latency (#64, #213) and box 4's behave-on-hardware row.
- The box 3 offset's upper bound includes a 1 ms formatting allowance, an engineering bound rather than a measurement; the closest upper margin is 6.94 ms. The calibrated-placement error is the measured spread of the coarse offset in the same action.
- #387 item 4's `A_MCSRV_STAT` observable was not exercised on `9ef71772`: the DUT ran on INTERNAL and its CRF servo stayed IDLE.

## Definition of done

- [x] Identity gate passed before any power action.
- [x] Boxes 1 to 3, box 4's protocol rows, #621 item 3 and #387 item 4 measured, with per-cycle and per-step tables, PASS/FAIL per item and artifact hashes.
- [x] Bench restored and read back; bench lock free.
- [x] All assigned gates rc 0 at the head.
- [x] Round 2: every round-1 finding answered (below); all gates rc 0 at `c2243f79`.
- [ ] Independent review (R634-2 and R635-2).

## Round 2

No bench, hardware, console, power-strip, tap, JTAG or controller-host access, and no bench lock. Six one-line commits on `d812a604`, the two findings pages only. Four new packet tools read the hashed raws from the durable archive copy, by path; their outputs are hashed on the pages. Lines are at `c2243f79`.

| Finding | Fixed at | Discharging tool output |
|---|---|---|
| R635-1-F1 / R634-1-F5, host clock identity | `387_SOFTWARE_GM_STEP.md:474` (role label, the manager's amend `d812a604`) | `git grep` under `docs/` for five forms of the value: 0 hits each |
| R635-1-F2 / R634-1-F2, box 3 time base | `117_GPTP_SILICON_EVIDENCE.md:821`, `:866-873`, `:936-939`, `:950`, `:976-982`, `:984-1016` | `r2_box3_model.py`: read-to-PHC offset 10.94 ms to 16.53-19.75 ms per action (271 or 272 line bytes, 144-byte console store, 86.8 us per byte, per-record idle bound, 0 of 2,880 records refuting the baud model); `r2_box3_grade.py`: 27 of 27 PASS, 11 within 25 ms, closest 0.66 ms; the three counterexamples were -10.2, -9.1 and -3.7 ms without the offset; 13 of 13 planted controls give their expected verdicts |
| R635-1-F3, `tu` set and clear times | `387_SOFTWARE_GM_STEP.md:425-441`, `:447-456`, `:458-460`, `:484` | `r2_gm.py`: four `tu` set rows one sample earlier (run 1 takeover, runs 2, 3, 5 release), every steady clear 31 or 32 ms earlier, steady after set 0.25 to 0.75 s, wire episodes 0.376 to 0.684 s; the planted step-bracket control keeps the first `tu=1` sample and shows the round-1 search drops it |
| R634-1-F3, underived figures and the poll arm | `387_SOFTWARE_GM_STEP.md:386`, `:415`, `:461`, `:482`; `117_GPTP_SILICON_EVIDENCE.md:1024`, `:1029` | `r2_gm.py`: 2,399 samples and 600 answered DUT polls, 0 with asCapable 0, peer delay 373 to 392 ns in both; a planted poll with asCapable 0 fails its edge. `r2_box4.py`: the peer's input 8 FRAMES_RX 149,513 over 300 polls; 26 first and last reads 167 to 7,925; all 1,495 polls 0 to 7,925, none negative |
| R634-1-F1, image identity | `117_GPTP_SILICON_EVIDENCE.md:835-838`, `387_SOFTWARE_GM_STEP.md:374-381` | PR #747 `provenance.json` at `bbc53aab`: bitstream and AEM SHA-256 as quoted; continuity: round 2 assignment item 8 |
| R634-1-F4, raw retention | `117_GPTP_SILICON_EVIDENCE.md:1071-1077`, `387_SOFTWARE_GM_STEP.md:503-507` | manager receipt 6208612856 |
| R635-1-R1 / R634-1-R1 | this body, Status and roles | wording applied |
| R635-1-R2 | `117_GPTP_SILICON_EVIDENCE.md:822`, `:1023` | the two probe logs differ only at the target-identity line |
| R634-1-R2 | `387_SOFTWARE_GM_STEP.md:391-392` | the base record: +3 at nine edges, +1 at the tenth |
| R634-1-S1 | `387_SOFTWARE_GM_STEP.md:400` | applied |
