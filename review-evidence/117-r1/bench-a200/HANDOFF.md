# HANDOFF: issue 117, A200 bench operator, 2026-09-23

## Outcome

REVIEW READY for steps 2, 4 and the controller part of step 5. Step 3 is
BLOCKED on the owner (no permitted GM-loss path). Nothing was pushed and no PR
was opened: the manager publishes.

- Lane: $LANES/117-silicon-evidence, branch `117-silicon-evidence`,
  head `c3eb95fa9ac86a3f20b45f94057d6c011127db08` = one commit on live dev
  `ede8d48ecd7c7f589a14b957951f040d92c99c70`. Worktree clean.
- Commit subject: "Record the issue 117 gPTP silicon evidence on the dev
  ede8d48e image" (one line, no trailers).
- Files: `docs/findings/117_GPTP_SILICON_EVIDENCE.md` (new, SHA-256
  `caa761cf911bdde486e64e5cd5d475115402b04e28755e3ab3512a372e1153cb`) and one
  row in `docs/findings/README.md`.
- Docs gates at the head, all green (transcript in the packet,
  gates-c3eb95fa.txt): docs_check.py 0 findings (165 md), check_doc_style.py
  OK, gen_toc.py --check OK (also --verify-anchors OK), check_em_dash.py
  --base ede8d48e 0 findings over 314 added lines.
- Public comment: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5795658105
  (posted 2026-09-23T13:24:32Z; public-comment-117.md is the posted text;
  posted-comment-117.readback.md is the API readback, identical except one
  trailing newline the API adds).
- Label note: the assignment text said to post "[A196] REVIEW READY". A196 is
  the previous operator's session label; this session is A200 (per the
  assignment comment 5794954599), so the comment is prefixed [A200].

## Per-step result

| Step | Result |
|---|---|
| Identity gate (CRC readback, dev unchanged) | PASS: ROM f6afa4ec, QSPI payload 02036e95 (asl seed), AEM 93742dd2, VERSION 00020060, grader 10/10; origin/dev == ede8d48e |
| 2 asCapable, cadence, turnaround, no daemon, peer firmware | PASS for retention/limits; initial reach NOT RUN (happened at the 12:35 flash, before these windows) |
| 3 GM loss and return | NOT RUN: owner blockers B1 (no permitted path) and B2 (no documented bound) |
| 4 publication CSRs and tu vs wire | PASS steady state (incl. 34,061 CRF PDUs tu=0 during a 60 s bind); transition NOT RUN |
| 5 controller | counters probe PASS (parity with the peer); la_avdecc full enumeration FAIL (Milan downgraded: CRF STREAM_INPUT counters_valid 0); Hive NOT RUN; behave NOT RUN (no hardware tier) |

Key topology fact: the grandmaster is the bench AVB switch (clock
3cc0c6fffefe0210, priority1 246); the DUT's asCapable partner is its port 1;
the reference peer is a slave on another switch port (AS path [GM, peer]).

## Owner blockers (also on the issue)

- B1: the peer exposes only IDENTIFY; the switch has no AVDECC entity, no IP
  on the AVB segment (it DHCP-requests every 15 s, unanswered), no provisioned
  management path. The repository checklist entry
  phys.switch-cycle.gm-partition is a power-strip cycle of the switch (outlet
  4 per the checklist), excluded by this assignment. Decision: authorize it
  under the lock, or provision switch management.
- B2: no numeric GM-recovery bound in the docs (GM_LOSS_RECOVERY.md gives
  none).
- B3: switch firmware identity unreadable without management access.
- B4: Hive needs an interactive desktop.

## Follow-up issues suggested (not filed)

1. DUT CRF talker ends its own bursts while bound (15.00 s after the latest
   successful probe response in 3 of 4 cases; TalkerAdvertise Leave follows
   the stop); first burst began 0.18 ms after a TALKER_DEST_MAC_FAIL probe
   response and 4.7 s before any Listener Ready.
2. STREAM_OUTPUT 1 FRAMES_TX = 16 after 34,061 PDUs (CRFT_COUNT and the
   wire agree on 34,061).
3. la_avdecc Milan downgrade over the CRF STREAM_INPUT counters (the gap
   REGISTER_MAP already documents with closure criteria).
4. Non-DUT: the bench switch answered 2 of 570 of the DUT's Pdelay requests
   after 18.3 ms (over its 15 ms limit).
5. Tooling: the build box clock is not NTP-synchronized (about 1.2 s behind
   the NTP-synchronized bench hosts).

## Bench access and state

Lock windows (flock /tmp/milan-bench.lock; build-box UTC, about 1.2 s slow):
identity 12:41:19.353 to 12:41:43.323; mem_read check 12:51:58.098 to
12:51:58.272; Run A 12:56:16.635 to 13:01:16.659; Run B 13:04:37.993 to
13:06:23.017; final 13:13:48.522 to 13:13:49.031. Console commands were
read-only (milan_status, mem_list, crc, mem_read, the UART grader); termios
restored on close.

State changes made and undone:
- Run B bound the reference peer's STREAM_INPUT 8 (primary CRF input; its
  clock source stayed INTERNAL) to the DUT's STREAM_OUTPUT 1, 13:04:49.249 to
  13:05:49.249 NTP time; unbind succeeded on the first attempt.
- la_avdecc registered for unsolicited notifications on both entities
  (13:10:47) and deregistered (13:11:26); DUT CTLR_DIAG 0 afterwards.

Final census (bench/final/census-final.jsonl) equals the start census
(bench/census-start.jsonl) for all 18 ACMP states; peer config 0, 96 kHz,
clock source 0, CRF format, firmware hash unchanged (READ_DESCRIPTOR payloads
identical apart from the peer's varying reserved half-word). DUT grader 10/10
at 13:13; CRFT_CTRL back to 0x3; no stream on the wire. Temporary files on the
controller host and capture server were copied, hash-verified and removed; no
leftover process; lock free. Not touched: flash, JTAG, power strip, wiring,
instruments.

## Packet

$REVIEWS/117-a200-packet, which is also this directory: the
management path 2026-09-23/117-a200 is a symlink to it. README.md gives the
layout. MANIFEST.sha256 holds the SHA-256 of every file here except itself,
this HANDOFF.md and the posted-comment files included, verified with
`sha256sum -c`.

## Reproduce

- Identity: `tools/console_read.py <console by-id> <out> milan_status mem_list
  'crc 0x00000000 52200' 'crc 0x01000000 3825788' 'crc 0x01400000 7352'` under
  the lock; compare with `tools/expected_crc.py` over the build directories.
- Runs: `tools/run_a.sh`, `tools/run_b.sh`, `tools/run_c.sh` (they expect
  avdecc_ro.py, crf_bind_window.py and the a200_enum binary in /tmp/a200 on
  the controller host); analysis: `tools/analyze_run.py <run dir> <pcap>
  [--host-offset-s 1.24]`, `tools/stream_timeline.py <pcap>`,
  `tools/pdelay_turnaround.py <pcap>`.
