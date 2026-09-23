# HANDOFF: issue 117, A202 bench operator, 2026-09-23

## Outcome

REVIEW READY for step 3 (GM loss and return) and the GM-change half of step 4,
on the dev `ede8d48e` image, under the owner decisions of 2026-09-23
(https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5795898094).
Nothing was pushed: the manager publishes. PR #531 is to be reviewed at the
new head.

- Lane: $LANES/117-silicon-evidence, branch `117-silicon-evidence`,
  head `0abf147f726721f4a323ee6a32095a02363fe2dc` = one commit on the PR #531
  head `c3eb95fa9ac86a3f20b45f94057d6c011127db08` (itself one commit on live dev
  `ede8d48e`). Worktree clean.
- Commit subject: "Record the issue 117 GM loss and return over six switch
  power cycles and the 5 s recovery bound" (one line, no trailers). An earlier
  local commit `46a1f72d` with one inaccurate sentence was amended before
  anything was published; it was never pushed.
- Files: `docs/findings/117_GPTP_SILICON_EVIDENCE.md` (SHA-256
  `f55810c3c1d91feaf1fef5257735c9fb187485fb6921e575e81d78720c00fd34`),
  `docs/design/GM_LOSS_RECOVERY.md` (`ab43f73e02f20094421e5d13260826955ff9fdb024ccbe01413b6019cc9f5f82`:
  new "Recovery bound" section with the owner's 5 s bound and its derivation;
  Contents separator switched to `--`, the em-dash gate's remedy for adding an
  entry), `docs/findings/README.md` (row status).
- Docs gates at the head, all green (gates-0abf147f.txt): docs_check.py 0
  findings (165 md), check_doc_style.py OK, gen_toc.py --check OK and
  --verify-anchors OK, check_em_dash.py --base ede8d48e 0 findings over 630
  added lines.
- Public comment: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5796668867
  (public-comment-117.md is the posted text; posted-comment-117.readback.md
  is the API readback, identical except one trailing newline).

## Per-step result

| Item | Result |
|---|---|
| Identity gate | PASS: ROM f6afa4ec, QSPI payload 02036e95 (asl), AEM 93742dd2, VERSION 00020060, grader 10/10 (13:45 and 14:13 UTC); origin/dev == ede8d48e |
| OUT4 is the switch | PASS (cycle 1): switch frames stop, controller-host port carrier drops, DUT loses the switch as GM; DUT stays up (RST_EPOCH 1, 1,600 samples, max gap 0.106 s), peer available_index and GM_CHANGED continue, other outlets unchanged |
| Step 3, DUT recovery vs 5 s | PASS 6/6: 0.51, 0.52, 1.51, 0.43, 1.46, 1.60 s from the switch's first post-boot Announce to GM=switch, SYNC=1, ASCAPABLE=1, TU=0 |
| Step 3, automatic | PASS: read-only AECP only; no write, no reset |
| Step 3, stream/media (cycles 4-6, CRF bound) | PASS: one stream restart per return, tu=0 on every PDU after return, listener MEDIA_LOCKED by the next poll; all unbinds first attempt |
| Step 3, reference peer recovery time | NOT RUN: its link is not tapped; controller view recorded (switch GM at first poll in 4 cycles; 46.6 s in cycles 2-3) |
| Step 4, GM-change half | PASS: every publication edge within one 0.1 s console sample of its wire cause; controller agrees at next poll; GM_CHANGED +2/cycle; CRF tu=1 at the loss edge inside the console bracket |

The DUT's behavior while the GM is absent: it selects itself (priority1 248),
publishes GM/parent 020000fffe000001, path [itself], SYNC=0, ASCAPABLE=0
(after ~5 s), TU=1. On link return it acts as master for 0.1 to 0.6 s (Syncs,
and in cycles 3 and 5 one self-naming Announce) until the switch's Announce
(priority1 246) is accepted. When the switch's first Announce arrives before
the DUT is asCapable (cycles 3, 5, 6) the DUT takes the next one, 1.007 s
later; that is the whole spread between ~0.5 s and ~1.5 s recoveries.

## Deviations and incidents (also public)

- Attempt 1 (13:51:23 to 13:52:04 UTC) aborted on my tool error:
  console_poll.py had not been copied into the packet, so the poller exited
  (rc 2) and the guard switched OUT4 back on after 5.95 s off. Not counted.
  Fix: poller copied (hash-identical to the previous packet), pre-flight check
  added so no power action happens unless the console transcript is growing,
  5 s poll check passed. bench/attempt1-aborted/NOTE.md has the details.
- A root-owned __pycache__ left by sudo python on the controller host needed
  `sudo rm`; done and verified (bench/final/hosts-cleanup.txt).
- No other deviation. Only OUT4 was ever switched.

## Bench access and state

Lock windows (build-box UTC; build box 1.080 to 1.085 s behind the NTP hosts):
identity 13:44:58.039-13:45:22.050; outlet status 13:45:31.181-13:45:31.711;
attempt 1 13:51:23.425-13:52:04.479; poll check 13:52:59.855-13:53:04.879;
cycle 1 13:53:17.582-13:55:57.608; cycle 2 13:59:13.322-14:01:13.347;
cycle 3 14:01:56.615-14:03:56.641; cycle 4 14:04:26.298-14:06:31.344;
cycle 5 14:07:26.405-14:09:31.503; cycle 6 14:10:00.470-14:12:05.556;
outlet status 14:12:29.488-14:12:29.968; final 14:13:19.301-14:13:19.766.
Console commands were read-only (milan_status, mem_list, crc, mem_read, the
grader).

State changes made and undone:
- OUT4 switched off/on 7 times (attempt 1 + cycles 1-6). Strip status at
  13:45 and 14:12 identical: OUT0 ON, OUT1 ON, OUT2 ON, OUT3 OFF, OUT4 ON,
  OUT5 ON, OUT6 ON.
- Cycles 4-6 bound peer STREAM_INPUT 8 to DUT STREAM_OUTPUT 1 (peer clock
  source untouched, INTERNAL); each unbound on the first attempt ~110 s after
  the off.

End census equals start census for all 18 ACMP states and 15 settings reads
(only the peer's varying reserved half-word differs). DUT grader 10/10 at
14:13; CRFT_CTRL 0x3; no AVTP on a 22 s capture; drops 0; CTLR_DIAG 0;
RST_EPOCH 1. Temporary files removed from the controller host
(/tmp/a202) and the power-strip host (/tmp/a202-ps.sh); captures removed from
the capture server after hash-checked copies. No leftover process; lock free.
Not touched: flash, JTAG, wiring, instruments, any other outlet.

## Follow-ups suggested (not filed)

1. DUT AVB_INTERFACE LINK_UP/LINK_DOWN do not move across switch outages
   (page observation 8; the peer's don't either).
2. DUT STREAM_OUTPUT TIMESTAMP_UNCERTAIN and FRAMES_TX restart at each
   STREAM_START (observation 9; extends the FRAMES_TX 16 observation 3).
3. DUT never advertises its own GM identity in ADP; re-advertises 0.54 to
   2.56 s after adopting a new GM (observation 10).
4. Tooling: the build box clock is not NTP-synchronized (1.08 s behind).

## Packet

$REVIEWS/117-a202-packet, which is also
$MANAGEMENT/2026-09-23/117-a202 (symlink). README.md
gives the layout. MANIFEST.sha256 holds the SHA-256 of every file here except
itself, this HANDOFF.md and the posted-comment files included; verify with
`sha256sum -c MANIFEST.sha256` from the packet root.
