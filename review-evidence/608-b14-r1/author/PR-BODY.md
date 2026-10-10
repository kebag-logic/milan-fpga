[A578] B14 bench on dev 5603c353: source switches, withdrawals, talker starts, default map, two-hour soak, MAAP

Refs #608 #645 #647 #667 #682 #686 #691

Head `6ec1a3a9a827575a84fb60d42ad3b085ecb70f19` on dev `5603c353`: three one-line commits that add `docs/findings/B14_BENCH_5603C353.md` and change no other file. The image is dev `5603c353`, seed eppo, as flashed. The SoC board was not used, per the ruling of 2026-10-10.

| Item | Issue | Result |
|---|---|---|
| 1 Identity | - | PASS: entity_id `020000fffe000001`, "Milan FPGA 1x1 TDM8", 2.96.0, AX7101-0001; VERSION `00020060`; AEM CRC `5ba355eb` |
| 2 Source switches | #645 acceptance 3, #647 bench item | PASS against the declared behaviour. 10 INTERNAL to AAF switches slipped 1 to 3 frames before the settle boundary and none after it; 10 AAF to CRF switches slipped none. `SLIP_TDM` 0, no MEDIA_UNLOCKED while following, no stream gap on the tap. The settle recentre's count is NOT OBSERVABLE on silicon (no register counts it) |
| 3 Withdrawals | #608 item 3 | PASS 100 of 100: the stream stopped within one PDU of the bridge's Listener `Lv`; STREAM_START and STREAM_STOP +1 each per cycle; the DUT sent no MRP LeaveAll in 894 s of capture (the 3/100 failure needed one) |
| 4 Talker starts | #667 | 0 of 100 EARLY, 0 of 100 LATE; first presentation-time step 124,999 to 125,020 ns in all 100 (B13: 14 of 100 EARLY on `28f9666f`) |
| 5 Default map and soak | #682 acceptance 5, #658 | Maps: STREAM_PORT_INPUT 0 holds 4 mappings, STREAM_PORT_OUTPUT 0 holds 8. Soak: 7,200.5 s, 121 counter polls, 0 error-class increments, no grandmaster or path change |
| 6 Ethernet receive | #691 | Link PASS (up at 1000 Mb/s, full duplex, throughout). RX error counters NOT RUN: the RMON window needs a `STATS_CTRL` write this lane may not make |
| 7 MAAP | #686 acceptance 4 | ANNOUNCE interoperation PASS: one range of 2 addresses, ANNOUNCE every 30.505 to 31.405 s, no overlap with the reference peer's ranges, no conflict. Acquisition and DEFEND NOT RUN (boot-time only; no overlapping probe occurred) |
| 8 Restore | - | PASS: 44 of 44 inventory rows equal the as-found record; residuals listed |

Observations for triage, recorded in the page:
- The DUT's FRAMES_TX on both talkers and FRAMES_RX on its CRF listener advance by one per second, not one per PDU.
- The DUT sends no unsolicited GET_COUNTERS for its STREAM_INPUTs.
- One loopback-ring slip occurred at INTERNAL during the soak, with the peer following the DUT's CRF.
- In 2 of 100 withdrawal holds the DUT withdrew its Talker Advertise; those two cycles have the slowest restarts.

Deviations, recorded in the page:
- As found, the reference peer followed the DUT's CRF. Items 2 and 3 set its clock source to INTERNAL for their duration and restored it.
- Item 2 holds 60 s and 45 s after LOCKED.
- A capture-stop fix after item 3's pilot cycle.
- Capture filters widened beyond the brief's where the streams or MSRP needed it.
- The soak ran in 17 locked chunks, so tap coverage is 94.8 %.

Validation, every command rc 0 at the head, with the pinned Markdown environment: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base 5603c353`, `check_doc_paths.py`, `check_baremetal_only.py --check` and `--selftest`, `git diff --check 5603c353 HEAD`.

The per-cycle records, the tools with their origins, the raw-capture index and the restore read-backs are in the lane's handoff packet.
