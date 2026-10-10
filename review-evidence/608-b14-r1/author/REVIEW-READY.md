[A578] REVIEW READY

Commit: `6ec1a3a9a827575a84fb60d42ad3b085ecb70f19` (branch `608-b14-bench`: three one-line commits on dev `5603c353`; local, not pushed).
Changed: `docs/findings/B14_BENCH_5603C353.md` (new, one section per item). No other file changed.
Validation: every command rc 0 at the head, with the pinned Markdown environment:
- `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`;
- `check_em_dash.py --base 5603c353`, `check_doc_paths.py`;
- `check_baremetal_only.py --check` and `--selftest`, `git diff --check 5603c353 HEAD`.

This resumes under the ruling 6094000332, without the SoC board, whose console was not touched. The controller fork was rebuilt: its source export equals B13's hash `23ac438f`, and B13's probe.cpp is unchanged.

| Item | Result |
|---|---|
| 1 Identity | PASS (04:54 UTC; no host or board state change since) |
| 2 #645 / #647 switches | PASS against the declared transient. 10 INTERNAL to AAF: 1 to 3 frames slipped before the settle boundary, 0 after, through 60 s holds. 10 AAF to CRF: 0. `SLIP_TDM` 0; no MEDIA_UNLOCKED while following; no stream gap on the tap. The settle recentre's own count is NOT OBSERVABLE: no silicon register counts it |
| 3 #608 withdrawals | PASS 100/100 (cycles 2 to 101): stop within one PDU of the bridge's `Lv`; STREAM_START/STOP +1/+1 in 100/100; the DUT sent no MRP LeaveAll in 894 s of capture |
| 4 #667 starts | EARLY 0/100, LATE 0/100; first step 124,999 to 125,020 ns (B13: 14/100 EARLY) |
| 5 #682 / #658 | Maps as found: input 4 mappings, output 8. Soak 7,200.5 s, 121 polls, 0 error-class increments, no GM or path change |
| 6 #691 | Link PASS throughout. RX error counters NOT RUN: the RMON window needs a `STATS_CTRL` write, outside this lane's rules |
| 7 #686 | ANNOUNCE interop PASS: one 2-address range, 30.505 to 31.405 s intervals, no overlap or conflict. Acquisition and DEFEND NOT RUN (boot-time; no overlapping probe) |
| 8 Restore | PASS: 44/44 inventory rows equal as found. Residuals: NVM image seq 234 to 272 (0 failed), `SLIP_LB` 0x92, rails 10, advanced counters |

**Deviations** (all in the page):
- As found, the peer followed the DUT's CRF and held two DUT bindings. Items 2 and 3 set its clock source to INTERNAL and restored it.
- Item 2 holds 60 s (AAF) and 45 s (CRF) after LOCKED.
- Item 3's pilot cycle 1 exposed a capture-stop defect on the tap host (rc 137). It was fixed and tested, cycle 1 is listed, and cycles 2 to 101 are graded.
- Capture filters were widened where tagged streams or MSRP were needed.
- The soak ran in 17 locked chunks, so tap coverage is 94.8 %.

**Observations for triage:**
- DUT FRAMES_TX (both talkers) and FRAMES_RX (CRF listener) advance one per second.
- The DUT sends no unsolicited STREAM_INPUT counters.
- One `SLIP_LB` frame at INTERNAL early in the soak.
- 2 of 100 withdrawal holds had a DUT Talker Advertise `Lv`, with the two slowest restarts.

Bench state: restored and read back; the controller and tap staging removed; the bench lock free.
Open risks/questions: none beyond the NOT RUN items and the observations above. This is executor evidence, not a review verdict.

**Item 2, per switch** (frames slipped = SLIP_LB dups / 2; boundary = LOCKED + 4.096 s + 0.5 s)

| Switch | Set to LOCKED (s) | Frames before boundary | SLIP_LB after boundary | MEDIA_UNLOCKED following | Tap gaps |
|---|---|---|---|---|---|
| c01-aaf | 6.71-7.21 | 3 | 0/0 | 0/0 | 0 |
| c01-crf | 2.83-3.33 | 0 | 0/0 | 0/0 | 0 |
| c02-aaf | 6.51-7.01 | 2 | 0/0 | 0/0 | 0 |
| c02-crf | 2.71-3.21 | 0 | 0/0 | 0/0 | 0 |
| c03-aaf | 6.62-7.12 | 2 | 0/0 | 0/0 | 0 |
| c03-crf | 2.90-3.40 | 0 | 0/0 | 0/0 | 0 |
| c04-aaf | 6.59-7.10 | 3 | 0/0 | 0/0 | 0 |
| c04-crf | 2.85-3.35 | 0 | 0/0 | 0/0 | 0 |
| c05-aaf | 6.22-6.73 | 2 | 0/0 | 0/0 | 0 |
| c05-crf | 2.84-3.35 | 0 | 0/0 | 0/0 | 0 |
| c06-aaf | 6.57-7.07 | 1 | 0/0 | 0/0 | 0 |
| c06-crf | 2.87-3.39 | 0 | 0/0 | 0/0 | 0 |
| c07-aaf | 6.71-7.21 | 2 | 0/0 | 0/0 | 0 |
| c07-crf | 2.75-3.25 | 0 | 0/0 | 0/0 | 0 |
| c08-aaf | 6.62-7.13 | 2 | 0/0 | 0/0 | 0 |
| c08-crf | 2.87-3.37 | 0 | 0/0 | 0/0 | 0 |
| c09-aaf | 6.21-6.71 | 2 | 0/0 | 0/0 | 0 |
| c09-crf | 2.79-3.29 | 0 | 0/0 | 0/0 | 0 |
| c10-aaf | 6.56-7.06 | 2 | 0/0 | 0/0 | 0 |
| c10-crf | 2.74-3.24 | 0 | 0/0 | 0/0 | 0 |

**Item 3, per cycle** (cycle 001 is the pilot, not graded)

| Cycle | Lv after response (ms) | Last PDU minus Lv (ms) | PDUs after Lv+T | START/STOP | Restart (ms) | Stop |
|---|---|---|---|---|---|---|
| 001 | 8.51 | -0.09 | 0 | +1/+1 | 44.4 | PASS |
| 002 | 8.88 | -1.73 | 0 | +1/+1 | 105.7 | PASS |
| 003 | 8.71 | -1.44 | 0 | +1/+1 | 11.0 | PASS |
| 004 | 9.26 | -1.72 | 0 | +1/+1 | 11.7 | PASS |
| 005 | 8.79 | -1.12 | 0 | +1/+1 | 12.4 | PASS |
| 006 | 9.27 | -1.37 | 0 | +1/+1 | 12.0 | PASS |
| 007 | 8.87 | -0.72 | 0 | +1/+1 | 12.7 | PASS |
| 008 | 9.33 | -1.05 | 0 | +1/+1 | 10.4 | PASS |
| 009 | 8.85 | -0.31 | 0 | +1/+1 | 12.1 | PASS |
| 010 | 8.77 | -1.98 | 0 | +1/+1 | 10.8 | PASS |
| 011 | 8.41 | -0.51 | 0 | +1/+1 | 11.9 | PASS |
| 012 | 10.52 | -0.37 | 0 | +1/+1 | 62.2 | PASS |
| 013 | 8.85 | -1.56 | 0 | +1/+1 | 10.9 | PASS |
| 014 | 8.40 | -0.86 | 0 | +1/+1 | 11.5 | PASS |
| 015 | 9.05 | -1.29 | 0 | +1/+1 | 12.3 | PASS |
| 016 | 8.49 | -1.57 | 0 | +1/+1 | 10.9 | PASS |
| 017 | 8.88 | -1.84 | 0 | +1/+1 | 11.6 | PASS |
| 018 | 9.32 | -0.18 | 0 | +1/+1 | 11.3 | PASS |
| 019 | 8.74 | -1.46 | 0 | +1/+1 | 11.0 | PASS |
| 020 | 9.93 | -0.52 | 0 | +1/+1 | 11.7 | PASS |
| 021 | 8.48 | -1.07 | 0 | +1/+1 | 11.4 | PASS |
| 022 | 9.04 | -1.38 | 0 | +1/+1 | 12.0 | PASS |
| 023 | 8.47 | -0.71 | 0 | +1/+1 | 11.8 | PASS |
| 024 | 8.90 | -0.00 | 0 | +1/+1 | 13.5 | PASS |
| 025 | 11.32 | -1.30 | 0 | +1/+1 | 12.2 | PASS |
| 026 | 84.47 | -0.30 | 0 | +1/+1 | 11.9 | PASS |
| 027 | 9.13 | -1.84 | 0 | +1/+1 | 11.6 | PASS |
| 028 | 8.62 | -1.20 | 0 | +1/+1 | 11.3 | PASS |
| 029 | 8.95 | -1.42 | 0 | +1/+1 | 12.0 | PASS |
| 030 | 8.49 | -0.73 | 0 | +1/+1 | 11.7 | PASS |
| 031 | 9.11 | -0.21 | 0 | +1/+1 | 11.4 | PASS |
| 032 | 9.35 | -1.32 | 0 | +1/+1 | 12.2 | PASS |
| 033 | 8.78 | -0.61 | 0 | +1/+1 | 11.9 | PASS |
| 034 | 8.49 | -0.82 | 0 | +1/+1 | 11.6 | PASS |
| 035 | 8.71 | -0.17 | 0 | +1/+1 | 12.3 | PASS |
| 036 | 9.40 | -0.73 | 0 | +1/+1 | 13.0 | PASS |
| 037 | 8.77 | -1.99 | 0 | +1/+1 | 12.7 | PASS |
| 038 | 8.91 | -1.01 | 0 | +1/+1 | 12.4 | PASS |
| 039 | 8.48 | -1.46 | 0 | +1/+1 | 11.0 | PASS |
| 040 | 8.83 | -0.68 | 0 | +1/+1 | 12.7 | PASS |
| 041 | 9.32 | -0.03 | 0 | +1/+1 | 12.4 | PASS |
| 042 | 9.24 | -1.59 | 0 | +1/+1 | 125.9 | PASS |
| 043 | 9.12 | -1.35 | 0 | +1/+1 | 11.6 | PASS |
| 044 | 9.03 | -1.12 | 0 | +1/+1 | 12.3 | PASS |
| 045 | 11.87 | -0.83 | 0 | +1/+1 | 11.0 | PASS |
| 046 | 9.03 | -1.74 | 0 | +1/+1 | 11.7 | PASS |
| 047 | 8.46 | -1.06 | 0 | +1/+1 | 11.4 | PASS |
| 048 | 8.88 | -0.34 | 0 | +1/+1 | 13.1 | PASS |
| 049 | 8.87 | -0.21 | 0 | +1/+1 | 13.2 | PASS |
| 050 | 8.46 | -0.56 | 0 | +1/+1 | 11.9 | PASS |
| 051 | 10.19 | -1.14 | 0 | +1/+1 | 10.7 | PASS |
| 052 | 9.26 | -1.11 | 0 | +1/+1 | 12.4 | PASS |
| 053 | 8.70 | -0.41 | 0 | +1/+1 | 12.0 | PASS |
| 054 | 9.25 | -1.71 | 0 | +1/+1 | 11.7 | PASS |
| 055 | 8.69 | -1.04 | 0 | +1/+1 | 11.4 | PASS |
| 056 | 95.70 | -0.91 | 0 | +1/+1 | 11.1 | PASS |
| 057 | 8.51 | -0.75 | 0 | +1/+1 | 11.8 | PASS |
| 058 | 9.17 | -1.02 | 0 | +1/+1 | 12.4 | PASS |
| 059 | 8.61 | -0.32 | 0 | +1/+1 | 12.1 | PASS |
| 060 | 8.63 | -0.21 | 0 | +1/+1 | 12.3 | PASS |
| 061 | 10.85 | -1.20 | 0 | +1/+1 | 11.9 | PASS |
| 062 | 8.65 | -1.86 | 0 | +1/+1 | 12.6 | PASS |
| 063 | 9.03 | -0.13 | 0 | +1/+1 | 13.3 | PASS |
| 064 | 9.37 | -0.33 | 0 | +1/+1 | 11.0 | PASS |
| 065 | 9.03 | -0.74 | 0 | +1/+1 | 12.7 | PASS |
| 066 | 8.40 | -0.98 | 0 | +1/+1 | 11.4 | PASS |
| 067 | 8.83 | -0.29 | 0 | +1/+1 | 12.2 | PASS |
| 068 | 9.23 | -0.58 | 0 | +1/+1 | 10.9 | PASS |
| 069 | 8.73 | -1.81 | 0 | +1/+1 | 10.6 | PASS |
| 070 | 10.32 | -0.17 | 0 | +1/+1 | 12.3 | PASS |
| 071 | 8.74 | -0.46 | 0 | +1/+1 | 12.0 | PASS |
| 072 | 8.84 | -0.81 | 0 | +1/+1 | 11.7 | PASS |
| 073 | 8.45 | -0.05 | 0 | +1/+1 | 12.4 | PASS |
| 074 | 9.16 | -1.40 | 0 | +1/+1 | 12.1 | PASS |
| 075 | 8.43 | -1.53 | 0 | +1/+1 | 10.8 | PASS |
| 076 | 8.97 | -0.82 | 0 | +1/+1 | 12.6 | PASS |
| 077 | 8.72 | -1.45 | 0 | +1/+1 | 11.3 | PASS |
| 078 | 8.96 | -1.43 | 0 | +1/+1 | 18.0 | PASS |
| 079 | 8.42 | -1.75 | 0 | +1/+1 | 10.7 | PASS |
| 080 | 8.87 | -1.10 | 0 | +1/+1 | 12.4 | PASS |
| 081 | 8.63 | -1.59 | 0 | +1/+1 | 13.0 | PASS |
| 082 | 8.99 | -1.82 | 0 | +1/+1 | 13.8 | PASS |
| 083 | 9.22 | -1.94 | 0 | +1/+1 | 11.5 | PASS |
| 084 | 8.76 | -0.22 | 0 | +1/+1 | 12.2 | PASS |
| 085 | 9.23 | -1.56 | 0 | +1/+1 | 11.9 | PASS |
| 086 | 8.76 | -0.86 | 0 | +1/+1 | 11.6 | PASS |
| 087 | 9.23 | -1.20 | 0 | +1/+1 | 12.3 | PASS |
| 088 | 8.84 | -0.67 | 0 | +1/+1 | 11.9 | PASS |
| 089 | 9.40 | -0.13 | 0 | +1/+1 | 13.7 | PASS |
| 090 | 9.10 | -1.45 | 0 | +1/+1 | 12.0 | PASS |
| 091 | 8.49 | -0.71 | 0 | +1/+1 | 11.8 | PASS |
| 092 | 9.03 | -1.99 | 0 | +1/+1 | 13.5 | PASS |
| 093 | 8.61 | -0.44 | 0 | +1/+1 | 12.2 | PASS |
| 094 | 8.99 | -1.58 | 0 | +1/+1 | 11.9 | PASS |
| 095 | 8.41 | -1.87 | 0 | +1/+1 | 12.6 | PASS |
| 096 | 8.78 | -0.13 | 0 | +1/+1 | 12.3 | PASS |
| 097 | 57.50 | -0.83 | 0 | +1/+1 | 13.0 | PASS |
| 098 | 8.78 | -1.74 | 0 | +1/+1 | 10.7 | PASS |
| 099 | 8.35 | -0.06 | 0 | +1/+1 | 12.4 | PASS |
| 100 | 8.96 | -1.55 | 0 | +1/+1 | 11.0 | PASS |
| 101 | 9.19 | -0.67 | 0 | +1/+1 | 10.8 | PASS |

**Item 4, per start**

| Start | EARLY | LATE | First step (ns) |
|---|---|---|---|
| 001 | 0 | 0 | 124999 |
| 002 | 0 | 0 | 125000 |
| 003 | 0 | 0 | 124999 |
| 004 | 0 | 0 | 124999 |
| 005 | 0 | 0 | 124999 |
| 006 | 0 | 0 | 124999 |
| 007 | 0 | 0 | 124999 |
| 008 | 0 | 0 | 124999 |
| 009 | 0 | 0 | 125000 |
| 010 | 0 | 0 | 124999 |
| 011 | 0 | 0 | 124999 |
| 012 | 0 | 0 | 124999 |
| 013 | 0 | 0 | 125019 |
| 014 | 0 | 0 | 124999 |
| 015 | 0 | 0 | 125000 |
| 016 | 0 | 0 | 124999 |
| 017 | 0 | 0 | 125020 |
| 018 | 0 | 0 | 124999 |
| 019 | 0 | 0 | 124999 |
| 020 | 0 | 0 | 125000 |
| 021 | 0 | 0 | 124999 |
| 022 | 0 | 0 | 124999 |
| 023 | 0 | 0 | 125000 |
| 024 | 0 | 0 | 124999 |
| 025 | 0 | 0 | 124999 |
| 026 | 0 | 0 | 124999 |
| 027 | 0 | 0 | 124999 |
| 028 | 0 | 0 | 124999 |
| 029 | 0 | 0 | 124999 |
| 030 | 0 | 0 | 125000 |
| 031 | 0 | 0 | 125019 |
| 032 | 0 | 0 | 125000 |
| 033 | 0 | 0 | 124999 |
| 034 | 0 | 0 | 124999 |
| 035 | 0 | 0 | 124999 |
| 036 | 0 | 0 | 124999 |
| 037 | 0 | 0 | 125000 |
| 038 | 0 | 0 | 125019 |
| 039 | 0 | 0 | 124999 |
| 040 | 0 | 0 | 124999 |
| 041 | 0 | 0 | 124999 |
| 042 | 0 | 0 | 124999 |
| 043 | 0 | 0 | 125000 |
| 044 | 0 | 0 | 124999 |
| 045 | 0 | 0 | 124999 |
| 046 | 0 | 0 | 124999 |
| 047 | 0 | 0 | 124999 |
| 048 | 0 | 0 | 124999 |
| 049 | 0 | 0 | 124999 |
| 050 | 0 | 0 | 125000 |
| 051 | 0 | 0 | 125000 |
| 052 | 0 | 0 | 125000 |
| 053 | 0 | 0 | 125000 |
| 054 | 0 | 0 | 124999 |
| 055 | 0 | 0 | 125000 |
| 056 | 0 | 0 | 124999 |
| 057 | 0 | 0 | 124999 |
| 058 | 0 | 0 | 124999 |
| 059 | 0 | 0 | 124999 |
| 060 | 0 | 0 | 125000 |
| 061 | 0 | 0 | 124999 |
| 062 | 0 | 0 | 124999 |
| 063 | 0 | 0 | 125000 |
| 064 | 0 | 0 | 125000 |
| 065 | 0 | 0 | 125019 |
| 066 | 0 | 0 | 125000 |
| 067 | 0 | 0 | 124999 |
| 068 | 0 | 0 | 124999 |
| 069 | 0 | 0 | 125000 |
| 070 | 0 | 0 | 124999 |
| 071 | 0 | 0 | 124999 |
| 072 | 0 | 0 | 124999 |
| 073 | 0 | 0 | 124999 |
| 074 | 0 | 0 | 124999 |
| 075 | 0 | 0 | 124999 |
| 076 | 0 | 0 | 124999 |
| 077 | 0 | 0 | 125000 |
| 078 | 0 | 0 | 124999 |
| 079 | 0 | 0 | 124999 |
| 080 | 0 | 0 | 125000 |
| 081 | 0 | 0 | 125019 |
| 082 | 0 | 0 | 125000 |
| 083 | 0 | 0 | 124999 |
| 084 | 0 | 0 | 124999 |
| 085 | 0 | 0 | 125000 |
| 086 | 0 | 0 | 124999 |
| 087 | 0 | 0 | 124999 |
| 088 | 0 | 0 | 124999 |
| 089 | 0 | 0 | 124999 |
| 090 | 0 | 0 | 124999 |
| 091 | 0 | 0 | 125000 |
| 092 | 0 | 0 | 124999 |
| 093 | 0 | 0 | 124999 |
| 094 | 0 | 0 | 125020 |
| 095 | 0 | 0 | 124999 |
| 096 | 0 | 0 | 125019 |
| 097 | 0 | 0 | 125000 |
| 098 | 0 | 0 | 125000 |
| 099 | 0 | 0 | 124999 |
| 100 | 0 | 0 | 124999 |

**Soak, per locked chunk** (one poll per 60 s; t0 06:23:22 UTC)

| Chunk | Lock (UTC) | Polls | Elapsed at last poll (s) | Error-class increments |
|---|---|---|---|---|
| 00 | 06:23:03-06:30:27 | 000-007 | 420.2 | 0 |
| 01 | 06:31:04-06:38:27 | 008-015 | 900.5 | 0 |
| 02 | 06:38:34-06:45:29 | 016-022 | 1320.2 | 0 |
| 03 | 06:45:59-06:53:27 | 023-030 | 1800.5 | 0 |
| 04 | 06:53:35-07:00:26 | 031-037 | 2220.2 | 0 |
| 05 | 07:00:41-07:07:26 | 038-044 | 2640.2 | 0 |
| 06 | 07:07:45-07:14:25 | 045-051 | 3060.2 | 0 |
| 07 | 07:14:49-07:22:25 | 052-059 | 3540.2 | 0 |
| 08 | 07:22:32-07:29:26 | 060-066 | 3960.2 | 0 |
| 09 | 07:29:48-07:37:30 | 067-074 | 4440.3 | 0 |
| 10 | 07:37:46-07:44:26 | 075-081 | 4860.2 | 0 |
| 11 | 07:44:33-07:51:28 | 082-088 | 5280.2 | 0 |
| 12 | 07:51:44-07:58:28 | 089-095 | 5700.6 | 0 |
| 13 | 07:58:34-08:05:26 | 096-102 | 6120.2 | 0 |
| 14 | 08:05:51-08:13:28 | 103-110 | 6600.6 | 0 |
| 15 | 08:13:42-08:20:27 | 111-117 | 7020.2 | 0 |
| 16 | 08:20:33-08:23:26 | 118-120 | 7200.5 | 0 |
