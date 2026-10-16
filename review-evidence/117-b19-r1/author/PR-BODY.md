[A624] Bench lane B19 on the installed dev `9ef71772` image: #117 boxes 1 to 3 and box 4's protocol rows, and the software-grandmaster steps for #621 item 3 and #387 item 4.

Refs #117
Refs #387
Refs #621

## Status

Operator evidence, local commit `18b98bbcecf478b903610a07667f232d944d6feb` on branch `117-b19-bench` from dev `734eb780`. Not pushed. Independent review is pending. Closing #117 waits for the manager's review of its remaining rows.

## Linked issue and roles

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-6207451080
- Executor: [A624]. Reviewers: assigned by the manager.

## Description

Two dated sections, findings docs only:

- `docs/findings/117_GPTP_SILICON_EVIDENCE.md`, "2026-10-16: bench lane B19 on dev 9ef71772" (+261 lines with its Contents entry).
- `docs/findings/387_SOFTWARE_GM_STEP.md`, the section of the same name (+164 lines with its Contents entry).

No other file changed.

| Item | Verdict | Evidence |
|---|---|---|
| Identity gate (lane B18's method) | PASS, 11 of 11 | console `ID=4d494c4e VERSION=00020060`, AEM CRC `5ba355eb` over 7,512 B, live ENTITY and CONFIGURATION equal to QSPI, clock sources, grader 10/10, ADP model `001bc5c1935893e1`; the cold boot printed the boot line, the AEM CRC and "fabric entity enabled" |
| Box 1, first reach (one OUT0 cold cycle) | PASS | first frame 8.06 s after power-on; the switch's first Announce and Sync 1.74 s later; the DUT's second completed Pdelay exchange 1.00 s after the first frame; its first AECP answer (9.96 s) already asCapable |
| Box 1, retention, cadence, turnaround, no daemon | PASS | 1,200/1,200 console samples and 300/300 polls asCapable; every interval within 30 %; DUT turnaround at most 13.432 us; peer delay 372 to 391 ns |
| Box 2, six switch cycles | PASS | recovery 0.47 to 1.77 s against 5 s; one stream restart per return in the three bound cycles |
| Box 3, publication words and `tu` | PASS | steady state over 300 s; in every cycle each CSR edge follows its wire cause within one 0.25 s console sample, and the first `tu=1` CRF PDU lies in the interval where `CLKV_STAT[0]` rose |
| Box 4, counters probe parity | PASS | DUT and peer transcripts identical, CLEAN, 0 complaints |
| Box 4, per-AVTPDU counters (#726, PR #729) | PASS | CRF FRAMES_TX equals the wire; every talker and listener pair counts at the packet rate |
| Box 4, three headless enumerations | PASS | `IEEE17221` and `MILAN` every run, 0 DUT complaints, 0 query errors, 42 descriptors |
| #621 item 3, five GM steps | PASS | 10 of 10 edges, no asCapable loss in 2,399 console samples and 600 polls |
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

| Run | Edge | DUT PHC step | `tu` rises console / CRF | asCapable 0 samples | GM_CHANGED | `mr` changes | Grade |
|---|---|---|---|---:|---:|---:|---|
| 1 | takeover / release | +9.987 / -10.003 ms | 1/1, 1/1 | 0, 0 | +1, +1 | 0, 0 | PASS, PASS |
| 2 | takeover / release | +9.987 / -10.004 ms | 1/1, 1/1 | 0, 0 | +1, +1 | 0, 0 | PASS, PASS |
| 3 | takeover / release | +9.987 / -10.004 ms | 1/1, 1/1 | 0, 0 | +1, +1 | 0, 0 | PASS, PASS |
| 4 | takeover / release | +9.987 / -10.005 ms | 1/1, 1/1 | 0, 0 | +1, +1 | 0, 0 | PASS, PASS |
| 5 | takeover / release | +9.987 / -10.004 ms | 1/1, 1/1 | 0, 0 | +1, +1 | 0, 0 | PASS, PASS |

## Authoritative references

- #117 owner decisions: the OUT4 cycle and the 5 s bound (comment 5795898094), the headless enumeration (5858063707).
- #387: the step policy (5794731090), the stimulus (5862116683, 5862731997), the #602 ruling; #621 and PR #707.
- `docs/design/GM_LOSS_RECOVERY.md`, `docs/design/TIME_SYNC.md`, `docs/testing/TESTING.md` sections 6, 6b and 6c, `docs/testing/726_STREAM_COUNTERS.md`.

## How to get into the same state

The bench state is restored and read back: the music and CRF bindings, both clock sources, the controller host's timestamping and clock, and every outlet on, as found. The raw captures and the tools are in the private bench packet `117-b19-a624`, with `MANIFEST.sha256` and `RAW-ARTIFACTS.json`.

## How to validate

All rc 0 at `18b98bbc`, from the physical lane path, none piped, the Markdown gates in the pinned environment: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base 734eb780` (0 findings over 425 added lines), `check_doc_paths.py`, `scripts/ci_scope.py --selftest`, `scripts/check_baremetal_only.py --check`, `scripts/check_feature_status.py --self-test`, `git diff --check`, and `git diff --check 734eb780 HEAD`; also `gen_toc.py --verify-anchors`.

## Known limitations and out of scope

- The first-reach console stopped polling after the boot prompt (a reader defect). OUT0 is switched once per lane, so the DUT end's asCapable time comes from the wire and its first AECP answer.
- The reference peer's own recovery time is not measured: its link was not captured.
- The GM-step leg ran on the as-found streams: the peer follows the DUT's CRF, so lane B1's reverse CRF binding with CRF selection on the DUT was not made, and the DUT's CRF servo stayed idle.
- Residuals no permitted command clears: the DUT's MAAP destination addresses (re-claimed at the cold boot) and `SLIP_LB` dups saturated at `0xFFFF`.
- Out of scope, owner items: audio continuity, latency (#64, #213) and box 4's behave-on-hardware row.

## Definition of done

- [x] Identity gate passed before any power action.
- [x] Boxes 1 to 3, box 4's protocol rows, #621 item 3 and #387 item 4 measured, with per-cycle and per-step tables, PASS/FAIL per item and artifact hashes.
- [x] Bench restored and read back; bench lock free.
- [x] All assigned gates rc 0 at the head.
- [ ] Independent review.
