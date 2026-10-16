[A624] REVIEW READY

Bench lane B19 on the installed dev `9ef71772` image, under the [B19 assignment](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-6207451080). Refs #117, Refs #387, Refs #621.

Commit: `18b98bbcecf478b903610a07667f232d944d6feb` (branch `117-b19-bench`, one commit on dev `734eb780`; local, not pushed, no PR)
Changed: dated sections "2026-10-16: bench lane B19 on dev 9ef71772" in `docs/findings/117_GPTP_SILICON_EVIDENCE.md` (+261) and `docs/findings/387_SOFTWARE_GM_STEP.md` (+164), with their Contents entries. No other file.

**Identity gate: PASS, 11 of 11** (lane B18's method, 03:37:20 to 03:37:26 UTC, before any power action): `ID=4d494c4e VERSION=00020060`, AEM CRC `5ba355eb` over 7,512 B, live ENTITY/CONFIGURATION equal to QSPI, the three clock sources, grader 10/10, ADP model `001bc5c1935893e1`, ATDECC identity as B18. The cold boot printed the boot line, `AEM 7512 B ... CRC 5ba355eb` and `fabric entity enabled`. Passed again at 04:30:48 UTC.

| Item | Verdict | Key evidence |
|---|---|---|
| Box 1, first reach (one OUT0 cold cycle) | PASS | first frame 8.06 s after power-on; switch Announce/Sync 1.74 s later; DUT second completed Pdelay exchange at +1.00 s; first AECP answer (9.96 s) already asCapable |
| Box 1, retention, cadence, turnaround, no daemon | PASS | 1,200/1,200 console samples, 300/300 polls; all intervals within 30 %; DUT turnaround <= 13.432 us; peer delay 372-391 ns |
| Box 2, six OUT4 cycles (OUT4 re-proven by cycle 1) | PASS 6/6 | 0.47-1.77 s against 5 s; one stream restart per return in cycles 1-3 |
| Box 3, words and `tu` against the wire | PASS | each CSR edge within one 0.25 s console sample of its wire cause; first `tu=1` CRF PDU inside the `CLKV_STAT[0]` interval in cycles 1-3 |
| Box 4, counters probe parity | PASS | identical transcripts, both CLEAN, 0 complaints |
| Box 4, per-AVTPDU counters (#729) | PASS | CRF FRAMES_TX = wire PDUs; all talker/listener pairs at packet rate |
| Box 4, three headless enumerations | PASS | `IEEE17221`+`MILAN`, 0 DUT complaints, 0 query errors, 42 descriptors |
| #621 item 3 | PASS 10/10 | no asCapable loss: 0 of 2,399 samples, 0 of 600 polls |
| #387 item 4 (wire and counters) | PASS 10/10 | below; render re-base count carried by simulation per the decision |

Per cycle (s after the OUT4 off command; console times placed through the DUT PHC):

| Cycle | CRF binding | DUT sync 0 | GM = itself | asCapable 0 | Switch first Announce | asCapable 1 | GM = switch | All-good | Recovery | 5 s |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | yes | 1.73 | 3.73 | 5.73 | 40.26 | 40.75 | 41.50 | 41.75 | 1.49 | PASS |
| 2 | yes | 1.73 | 3.49 | 5.49 | 40.37 | 40.50 | 40.50 | 41.00 | 0.63 | PASS |
| 3 | yes | 1.49 | 3.99 | 5.74 | 40.23 | 40.75 | 41.50 | 42.00 | 1.77 | PASS |
| 4 | no | 1.75 | 3.75 | 6.00 | 40.27 | 40.01 | 40.51 | 41.01 | 0.75 | PASS |
| 5 | no | 1.74 | 3.49 | 6.24 | 40.25 | 40.25 | 40.50 | 40.75 | 0.50 | PASS |
| 6 | no | 1.47 | 3.47 | 6.22 | 40.26 | 40.24 | 40.49 | 40.74 | 0.47 | PASS |

Per step (software grandmaster on the controller host, +10 ms, priority1 240 for 50 s; the as-found CRF stream DUT output 1 to the peer's input 8 locked throughout):

| Run | Edge | DUT PHC step | `tu` rises console / CRF | asCapable 0 | GM_CHANGED | `mr` changes | MEDIA_RESET DUT AAF/CRF talker, peer CRF listener | MEDIA_UNLOCKED DUT / peer CRF / peer AAF | Grade |
|---|---|---|---|---:|---:|---:|---|---|---|
| 1 | takeover | +9.987 ms | 1 / 1 | 0 | +1 | 0 | +0/+0, +0 | +0/+0/+0 | PASS |
| 1 | release | -10.003 ms | 1 / 1 | 0 | +1 | 0 | +0/+0, +0 | +0/+0/+0 | PASS |
| 2 | takeover | +9.987 ms | 1 / 1 | 0 | +1 | 0 | +0/+0, +0 | +0/+0/+0 | PASS |
| 2 | release | -10.004 ms | 1 / 1 | 0 | +1 | 0 | +0/+0, +0 | +0/+0/+0 | PASS |
| 3 | takeover | +9.987 ms | 1 / 1 | 0 | +1 | 0 | +0/+0, +0 | +0/+0/+0 | PASS |
| 3 | release | -10.004 ms | 1 / 1 | 0 | +1 | 0 | +0/+0, +0 | +0/+0/+0 | PASS |
| 4 | takeover | +9.987 ms | 1 / 1 | 0 | +1 | 0 | +0/+0, +0 | +0/+0/+0 | PASS |
| 4 | release | -10.005 ms | 1 / 1 | 0 | +1 | 0 | +0/+0, +0 | +0/+0/+0 | PASS |
| 5 | takeover | +9.987 ms | 1 / 1 | 0 | +1 | 0 | +0/+0, +0 | +0/+0/+0 | PASS |
| 5 | release | -10.004 ms | 1 / 1 | 0 | +1 | 0 | +0/+0, +0 | +0/+0/+0 | PASS |

**Restore: read back.** Outlets OUT0-OUT6 on as found (OUT0 switched once, OUT4 six times). Census 41 of 46 byte-equal: the music bindings, the CRF binding (unbound for cycles 4-6 and rebound, flags `0x0082`), both clock sources (DUT 0, peer 1), formats and maps as found; the 5 others are the DUT's live peer delay and its MAAP destination addresses, re-claimed at the cold boot. Controller host: no gPTP daemon, timestamping tx 0/rx 0, clock 0 ppb and back on its found trajectory within 4.5 us; temporary build removed. DUT grader 10/10. Bench lock free.

Validation, all rc 0 at `18b98bbc`, physical lane path, not piped, Markdown gates in the pinned environment: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base 734eb780` (0 findings, 425 added lines), `check_doc_paths.py`, `scripts/ci_scope.py --selftest`, `scripts/check_baremetal_only.py --check`, `scripts/check_feature_status.py --self-test`, `git diff --check`, `git diff --check 734eb780 HEAD`; also `gen_toc.py --verify-anchors`.

Acceptance criteria: the assignment's items 1 to 8 are met, with the limits below. Closing #117 waits for the manager's review of the remaining rows.

Open risks/questions:
- First reach: the console reader stopped polling after the boot prompt (a loop defect, fixed after). OUT0 is switched once per lane, so the DUT end's asCapable time rests on the wire and its first AECP answer.
- The GM-step leg used the as-found streams. The peer follows the DUT's CRF, so lane B1's reverse CRF binding with CRF selection on the DUT would have closed a media-clock loop and was not made; the DUT's CRF servo stayed idle.
- The capture server now has a second tap interface, on the reference peer's link. It was used only for a 4 s capture to tell the links apart. The peer's own recovery time stays NOT RUN.
- Residuals no permitted command clears: the new MAAP addresses and `SLIP_LB` dups saturated at `0xFFFF` (not polled during the runs; the music stream into the DUT stopped about 40 s in each switch cycle).
- Observations without a verdict: LINK_UP/DOWN now +1/+1 per switch cycle; the DUT's CRF licence held 6.6-17.9 s into an outage and its first PDU came 3.3-4.3 s after all-good; each enumeration logs two complaints naming the reference peer (StreamInfoFlag bit 24); the peer's AAF talker toggles `mr` at each grandmaster step.

The bench packet `117-b19-a624` holds HANDOFF.md, PR-BODY.md, the tools, per-action logs, analyses, `MANIFEST.sha256` and `RAW-ARTIFACTS.json`.

