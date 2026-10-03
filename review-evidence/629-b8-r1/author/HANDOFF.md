# [A521] Bench lane B8 handoff

Refs #629: the remaining bench items after lane B7 (PR #644), on the dev `bbf704ec` image as flashed for B7.

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5970760794
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5970786724 (posted 17:53 CEST; readback equal but for one trailing newline)
- STOP: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5970982211 (posted 18:16 CEST; STOP.md, STOP.readback.md, stop-url.txt)
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5971525043 (posted 19:12 CEST with the head and the per-run tables; REVIEW-READY.md, its readback REVIEW-READY.readback.md equal but for one trailing newline, review-ready-url.txt)
- Manager's ruling on the STOP: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5970994127 (item 1 waits for the owner; items 2 to 4 run now, the one power cycle included; no tone this session; REVIEW READY with the head; "Refs #629" while item 1 is open)
- Branch: `629-b8-bench` on PR #644's head `40714c1bd166c2a05f9607a861e8550c705d183a`; session 1's commit `c17997fb`; this session's commit on top of it.
- Packet: this directory. Raw files stay outside it under /tmp/b8-a521/raw (RAW-ARTIFACTS.json); private endpoints, the power strip's own output and the tone tools' unmasked originals under /tmp/b8-a521/private (not in the packet).

## State

**Session 2 (resume, 18:17 CEST): items 2, 3 and 4 RUN; item 1 NOT RUN (tone absent, the owner's check pending).** All bench work ended at 18:52:42 CEST with the bench lock free, every change restored and read back, and nothing left running on any host.

- **Item 2, the source switch:** AAF to CRF and CRF to AAF, each as the design declares: one MEDIA_RESET on the DUT's AAF talker per switch (and one as received by the peer's listener), CLOCK_DOMAIN LOCKED and UNLOCKED +1 each, LOCKED again 2.6 to 3.1 s (CRF) and 6.0 to 6.5 s (AAF) after the set, GET_CLOCK_SOURCE the set index at every read, `SLIP_LB` and `SLIP_TDM` static, `RENDER_STAT` rails static, the DUT's two listeners counting no interruption, and the tone path through the DUT's talker 0 listener discontinuities with 0 net steps over the whole 417 s span. The INTERNAL-to-AAF set that started the case repeated #645: `SLIP_LB` +2 (one frame) 2.0 to 3.0 s after the servo first read LOCKED, +2 during ACQUIRE, and +4 on INTERNAL between the binds and the set.
- **Item 3, the CRF lock loss:** as declared. HOLDOVER within 0.06 to 0.56 s of the unbind with the trim frozen at -6.0 ppm for 11 s, GET_CLOCK_SOURCE 1 throughout, one `mr` toggle at the loss and none at the return, CLOCK_DOMAIN UNLOCKED +1 at the loss and LOCKED +1 at the return, STREAM_INPUT 1 MEDIA_UNLOCKED +1, LOCKED 2.66 to 3.16 s after the rebind; the tone path clean through it.
- **Item 4, the saved selection across the power cycle:** held. CLOCK_SOURCE 2 set and read back; NVM commit 30 to 31 (image seq 31) before the cycle; the one authorised cold power cycle (outlet 0, the documented command, under the lock) at 18:49:51 to 18:49:59 CEST; boot PASS (the UART grader 10/10 at its first run, 18:51:19); after boot GET_CLOCK_SOURCE read 2 at the first command, the DUT had restored its listener binding and format itself, and the servo read LOCKED at the first poll with no command sent; the post-boot identity gate PASS (verdict byte-equal); restored to CLOCK_SOURCE 0 and read back; NVM image seq 31 held across the cycle, 33 at the end.

**Commit:** `4fb5125a2e43997384839deeb1fe4742a5b2dca8` on `629-b8-bench`, on session 1's `c17997fb`, one-line subject, no body, no trailers. Local, not pushed, no PR. It completes the section "Dev bbf704ec, 2026-10-03: lane B8" in `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (and the introduction's pointer and Contents line) and updates its row in `docs/findings/README.md`; no other doc edit. PR-BODY.md says "Refs #629".

**Gates:** every gate rc 0 at `4fb5125a` (gates-r2/gates.txt): `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base 40714c1b`, `check_doc_paths.py` (pinned Markdown environment), `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test`, `git diff --check 40714c1b HEAD`. The same set ran on the uncommitted worktree (gates-r2-worktree/): `check_doc_paths.py` first failed on raw-file cells written `sw/...` (the repository has an `sw/` directory); the raw table gained a Run column and every gate then passed (the second run's outputs replaced the first's in that directory).

**Tool controls:** `b6_thdn.py controls` at 19:00 CEST, after the cases and their grades: byte-equal to lanes B6 and B7 (`7bbefc71...`).

## Step ledger, session 2 (CEST)

| Step | What | Result | Evidence |
|---|---|---|---|
| 18 | Resume context: the manager's ruling, the design's switching, lock-loss, `mr`, CLOCK_DOMAIN, bench and TIME_SYNC settle rows, the render setpoint's recentre rule, the register map's `SLIP_LB`, `SLIP_TDM` and `RENDER_STAT` | Read | this file |
| 19 | Tools written (below) | - | tools/ |
| 20 | Local preconditions | PASS 18:30:37: board link address, both USB audio cards, three serial adapters, the lock free | - |
| 21 | Controller survey and the power strip's status (locked, read-only) | 18:30:44: no gPTP daemon, no staging, sudo ok; the strip reachable, outlet 0 on | (private) |
| 22 | Identity gate again | **PASS** 18:30:55 to 18:31:24; verdict byte-equal to session 1's | identity-resume/ |
| 23 | SoC console peek | 18:31:29: root prompt | soc/peek-resume.log |
| 24 | Start baseline (start2) | 18:31:37 to 18:31:44, all rc 0; bridge legs 15675/15676; NVM seq 19/18, 19 commits | restore/*-start2*, soc/start2-health.log |
| 25 | Bridge legs stopped by PID | 18:31:51 to 18:31:56: KILLED; UDC configured; BAD=1 as found | soc/s03-stop-legs.log |
| 26 | Item 2: case SW | 18:32:19 to 18:39:59, ACTION_RC 0 | runs/sw/, runs/sw-lock.txt |
| 27 | Item 3: case CRFLL | 18:40:09 to 18:48:17, ACTION_RC 0 | runs/crfll/, runs/crfll-lock.txt |
| 28 | Item 4, pre | 18:48:36 to 18:48:45, PRE_OK | runs/pc/, runs/pc-pre-lock.txt |
| 29 | Item 4, the power cycle and the boot | 18:49:48 to 18:51:19, CYCLE_RC 0, BOOT_PASS | runs/pc-cycle-lock.txt, runs/pc/grader-boot-0.txt, runs/pc/boot-console.txt |
| 30 | Item 4, post | 18:51:28 to 18:51:37, POST_DONE | runs/pc/, runs/pc-post-lock.txt |
| 31 | Identity gate after the boot | **PASS** 18:51:52 to 18:52:21; verdict byte-equal | identity-postboot/ |
| 32 | Bridge legs restarted | 18:52:26 to 18:52:30: to-host 21431, from-host 21432 with the recorded lines; UDC configured; BAD=1 as found | soc/s04-start-legs.log |
| 33 | End baseline (end2), controller staging removed | 18:52:34 to 18:52:42, all rc 0; census 43 of 46 equal (the other three are power-cycle residuals); the lock free | restore/*-end2*, restore/census-compare-r2.txt, restore/controller-cleanup.txt |
| 34 | Grades and summaries | grade_b8.py on SW's span, CRFLL's window and its lock-loss segment; b8_events.py | summary/ |
| 35 | Tool controls | 19:00:09 to 19:00:30, byte-equal to lanes B6 and B7 | controls/ |
| 36 | Redaction | Passes with the private map, extended for the grader's upper-case grandmaster ID, the tone tool's file names, one `run_b8.py` line and the snippet's size in the run records; 78 files recorded; token scan clean | redaction.json |
| 37 | Findings section, index row, gates, commit | `4fb5125a`, every gate rc 0 | gates-r2/, gates-r2-worktree/ |
| 38 | REVIEW READY on #629 | POSTED 19:12:43 | REVIEW-READY.md, REVIEW-READY.readback.md, review-ready-url.txt |

Session 1's steps 0 to 17 are unchanged: the identity gate PASS at 17:57, the tone proof at 18:05 (tone absent), the STOP and the restore. They are in the findings section and in git history at `c17997fb` (this file's previous version).

## Bench actions, session 2 (one row per locked action, CEST)

| Time | Action | Result |
|---|---|---|
| 18:30:44-18:30:45 | Controller survey; power strip status (read-only) | rc 0; outlet 0 on |
| 18:30:55-18:31:24 | Identity gate (identity_b8.sh, identity-resume) | all rc 0; PASS |
| 18:31:29-18:31:33 | SoC console peek (one carriage return) | root prompt |
| 18:31:37-18:31:44 | Start baseline (baseline_b8.sh start2) | all rc 0 |
| 18:31:51-18:31:56 | SoC bridge legs 15675/15676 stopped by PID | KILLED |
| 18:32:19-18:39:59 | run_b8.py SW (item 2) | ACTION_RC 0 |
| 18:40:09-18:48:17 | run_b8.py CRFLL (item 3) | ACTION_RC 0 |
| 18:48:36-18:48:45 | pc_b8.py pre (item 4) | PRE_OK |
| 18:49:48-18:51:19 | pc_cycle_b8.sh: strip status, **the one power cycle of outlet 0**, strip status, boot record, UART grader | CYCLE_RC 0; BOOT_PASS |
| 18:51:28-18:51:37 | pc_b8.py post (item 4) | POST_DONE |
| 18:51:52-18:52:21 | Identity gate (identity-postboot) | all rc 0; PASS |
| 18:52:26-18:52:30 | SoC bridge legs restarted | STARTED: to-host 21431, from-host 21432 |
| 18:52:34-18:52:42 | End baseline (baseline_b8.sh end2) and controller staging removal | all rc 0 |

No other outlet, no JTAG, no flash, no SoC board reboot, no wiring or instrument change, no tone playback, no DUT register write. The only power-strip commands were two `status` reads at the pre-check and the documented `off 0; sleep 8; on 0` with a `status` before and after it.

## Run ledger (one row per case or cycle)

| Case | Window start | Window | Result |
|---|---|---|---|
| Tone proof (session 1) | 18:05:13 | 10 s | TONE ABSENT: STOP |
| B0, B-CRF, B-AAF by THD+N (item 1) | - | - | NOT RUN: the tone does not reach the peer's talker; the owner checks the path |
| SW: INTERNAL to AAF (the case's first set) | 18:32:31 set | LOCKED 6.64 to 7.14 s; 120 s hold | #645 repeated: `SLIP_LB` +2 at 2.0 to 3.0 s after LOCKED; otherwise as declared |
| SW: AAF to CRF (item 2) | 18:34:38 set | LOCKED 2.62 to 3.12 s; 150 s hold | PASS against the declared switch behaviour |
| SW: CRF to AAF (item 2) | 18:37:11 set | LOCKED 5.96 to 6.48 s; 150 s hold | PASS against the declared switch behaviour |
| SW tone path, 20 s after the first set to the hold's end | 18:32:51 | 417.3 s | 0 listener events; 0 net steps in 20,030,400 frames; 416 of 417 blocks at the floor |
| CRFLL window (B-CRF repeated) | 18:40:41 | 420 s (401.3 s captured) | PASS on B7's B-CRF criteria; 19.0 s hidden by three host capture stalls |
| CRFLL lock loss (item 3) | 18:47:42 unbind | held 11.04 s | Observed as declared |
| PC: the saved selection across the power cycle (item 4) | 18:49:51 off, 18:49:59 on | boot to prompt 8.4 s | Held: GET_CLOCK_SOURCE 2 after boot; servo LOCKED with no command |

## Tool changes, session 2

Every tool is in tools/. New or changed in session 2:

| Tool | Taken from | Change |
|---|---|---|
| console_poll_b8.py | lane B7's console_poll.py | Each poll also reads `SLIP_LB`, `SLIP_TDM`, `RENDER_STAT` (`0x8D4`, 12 bytes), `CRF_CTRL` (`0x738`) and `CRF_RATE` (`0x748`); a `file:` stop so one poll runs through a whole case |
| run_b8.py | lane B7's run_b7.py | Cases SW and CRFLL (item 2, item 3); one console poll every 0.5 s from before the case's binds to after the restore, in place of the 30 s DUT reads; GET_COUNTERS and GET_CLOCK_SOURCE marks per phase; the clock-source restore and unbinds run before the board's playback is stopped, so the poll records them; the capture's layout from the private environment, so the file names none of it and is not masked |
| grade_b8.py | lane B7's grade_b7.py | Segment by two event kinds; capture layout from the environment; the `SLIP_TDM` gate and `servo_window` from the poll; B7's B-AAF lock-loss section dropped (b8_events.py reports the lock loss) |
| b8_events.py | new | The per-switch, lock-loss and power-cycle summaries and the reduced grades |
| pc_b8.py | new | Item 4's pre and post stages |
| pc_cycle_b8.sh | new | The one power cycle under the lock, with the strip's status before and after, a passive console record and the UART grader as the boot verdict; the strip host from the private environment |
| pc_locked_b8.sh | new | pc_b8.py under the lock with a deadline |
| console_listen.py | new | A read-only console record (never writes) |
| identity_b8.sh | session 1's | An optional third argument names the output directory (identity-resume, identity-postboot) |
| baseline_b8.sh | session 1's | The controller staging is removed at any `end*` tag (end2) |

Session 1's tool table is unchanged (git history at `c17997fb`). The four unmasked B7 originals and the tone tools' originals stay private.

## Deviations and decisions

- **Window lengths.** Every foreground command must end inside 10 minutes, so each case is one locked action under 575 s: SW holds 120, 150 and 150 s after each LOCKED; the CRF window is 420 s, not lane B7's 630 s. Item 1, which named B7's windows, did not run.
- **The tone.** No tone was played into the peer's talker this session (the ruling). The SW and CRFLL tone path is lane B6's and B7's: the B6 loop played into McASP0 on the SoC board, through the DUT's AAF talker to the peer's listener, captured externally.
- **The receive path.** The peer's talker carries no known signal, so the audio the DUT receives cannot be graded for discontinuities. The receive path is observed through `SLIP_LB`, `SLIP_TDM`, `RENDER_STAT` and the DUT's listener counters. The #386 recentre count is a simulation tap, not a register: on silicon the recentre is seen only as `RENDER_STAT`'s converged bit dropping for under 0.5 s with no rail counted, as the stage's short-queue recentre branch does.
- **#645.** The INTERNAL-to-AAF slip is recorded with its data in the findings section ("B8: the INTERNAL-to-AAF set and #645") and named in REVIEW READY. Nothing was posted on #645: this lane's posting rule lists only TAKEN, REVIEW READY and STOP on #629.
- **One poll missing a word** (CRFLL poll 618, in the window): skipped by every summary.

## Residuals

- SoC board bridge legs under new PIDs (21431 to-host, 21432 from-host).
- DUT: power-cycled once (authorised). Its counters restarted at the boot, so `SLIP_LB` and the other never-cleared words now read from zero; the talkers' MAAP destination addresses were re-allocated at boot (census rows 3 and 4); the live propagation delay reads 378 ns (385 before).
- DUT NVM: image seq 33 (slots 33/32, `VD_OK`), 2 commits since the boot; session 2's method edits and restores before the cycle took it from 19 to 31.

## Open items for the owner and the manager

- **Item 1:** the tone does not reach the peer's talker; the owner checks the path. Direction B by THD+N stays NOT RUN.
- **#645:** the INTERNAL-to-AAF ring slip after LOCKED repeated; the data is in the findings section for #645.
- #629 stays open: "Refs #629".

## Packet layout

| Path | What |
|---|---|
| HANDOFF.md | This file |
| TAKEN.*, STOP.*, REVIEW-READY.*, *-url.txt | The posts and their readbacks |
| PR-BODY.md | Proposed PR body |
| identity/, identity-resume/, identity-postboot/ | The identity gate at 17:57, 18:31 and after the boot |
| soc/ | SoC console peeks, health at each baseline, bridge stop and restart transcripts |
| runs/proof/ | Session 1's tone proof |
| runs/sw/, runs/crfll/ | Items 2 and 3: events, controller transactions, DUT reads before and after, board transcripts |
| runs/pc/ | Item 4: events, controller transactions, NVM reads, servo polls, the boot grader and the boot record |
| summary/proof/ | Session 1's proof grade |
| summary/sw/, summary/crfll/, summary/pc/ | The grades (reduced) and b8_events.py's summaries |
| restore/ | Census and counters at each baseline and their comparisons, descriptor surveys, DUT reads, controller state and cleanup, host view |
| tools/ | Every tool used |
| gates*/ | Gate commands and outputs |
| redaction.json | Per redacted file: original and retained SHA-256, labels |
| RAW-ARTIFACTS.json | Every raw file under /tmp/b8-a521/raw by path, size and SHA-256 |
| MANIFEST.sha256 | SHA-256 of every packet file except itself |
