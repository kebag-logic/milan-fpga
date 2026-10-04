# [A535] Bench lane B11 handoff

Refs #653: the disconnect order a real controller sees (#653's bench item), on the dev `bbf704ec` image as booted (no flash).

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5983239639
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5983278802 (posted 20:54:30 CEST; TAKEN.readback.md equal but for one trailing newline)
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5983553123 (posted 21:25:33 CEST with the head and the per-run table; REVIEW-READY.readback.md equal but for one trailing newline)
- REVIEW READY, round 2: https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5983801043 (posted 21:55:23 CEST with the head `6b83de00` and the per-run tables; REVIEW-READY-R2.readback.md equal but for one trailing newline)
- Posted on #653: TAKEN, REVIEW READY and the round-2 REVIEW READY only. Nothing posted on #629, PR #659 or elsewhere; no existing comment edited or deleted.
- Branch: `653-b11-bench` from dev `6c22d3cad7c8c24ed3f0c5eab535922a3428c8d5`, lane worktree on the physical /data path.
- Packet: this directory. Raw files (the 23 cycle pcaps, each session's enumeration and quit pcaps, probe and driver logs) stay outside it under /tmp/b11-a535/raw (RAW-ARTIFACTS.json); private endpoints, the redaction map and the unmasked originals under /tmp/b11-a535/private (not in the packet).

## Round 2 (2026-10-04, from 21:45 CEST; docs only, no bench access)

**State: REVIEW READY at `6b83de0009673ce2c438985a0f9720f079a3715d`** on `653-b11-bench`, one commit on round 1's `6f76d612` (pushed by the manager as PR #659). One-line subject, no body, no trailers, no rebase or amend. Local, not pushed.

- Round-2 assignment: https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5983716764. Reviews answered: R482-1 (https://github.com/kebag-logic/milan-fpga/pull/659#issuecomment-5983714179) and R483-1 (https://github.com/kebag-logic/milan-fpga/pull/659#issuecomment-5983705791), both NEGATIVE at `6f76d612` on the same two MINORs.
- **No bench access in this round:** no console, tap, controller host, SoC board, instrument or bench lock. The only network reads were the repository's own (git fetch, ls-remote, the issue and PR comments) and the controller library's public source at its tag.
- **Dev:** `git ls-remote` read dev `6c22d3cad7c8c24ed3f0c5eab535922a3428c8d5`, the branch base, at about 21:50 and again at 21:54:23 CEST, so no merge commit (item 4: "if it moved").

| Step | What | Result | Evidence |
|---|---|---|---|
| R2-0 | Read the round-2 assignment, R482-1 and R483-1 | Two MINORs (the library check; the control interval), R483-1 R1 and R2, suggestions | - |
| R2-1 | The library check at the tag: the public source archive of tag `v4.3.1.1` (tag object `080ab851`, commit `6d61a92e`), kept outside the packet under /tmp/b11-a535/r2 (archive 832,506 bytes, sha256 `76aec04c0d135dcb6cbaaba695c3e0e3b981bd53502cb307f76cd67ddf1ca8c7`; `avdeccControllerImpl.cpp` 404,524 bytes, `5f70fbfac4c6db2e4a99c728f519fe82849bf80912e215cba1ee954d78ee941d`) | Check at `src/controller/avdeccControllerImpl.cpp:1611-1613` in `updateStreamInputCounters` (`:1590`); the only other MEDIA_UNLOCKED use in `src/` is the mandatory-counter list at `avdeccControllerImplHandlers.cpp:35`. The bench tree's describe line reads `v4.3.1.1` and its copied header equals the tag's (`3d09fa69...`) | round2/library-check.txt |
| R2-2 | The control's intervals, from the provided decoder's C0 text | Answer to command 1,629.836 µs (the grade's `own_rsp_to_cmd_us` 1629.8); answer to response 1,637.340 µs; command to response 7.504 µs | round2/control-interval.txt |
| R2-3 | The library's counters updates, from the s0b and s1 probe logs | 69 DUT STREAM_INPUT updates: 0/0 Connected x23, 1/0 Connected x23, 1/1 NotConnected x23, all accepted by the check. R01 and R02: no update between NotConnected and the 1/1 one (the held 1/0 came 1,003 ms after the bind, while Connected) | round2/library-updates.txt, round2/r2_receipts.py |
| R2-4 | Page and README row edits; gates on the worktree | All rc 0 | round2/gates-worktree/ |
| R2-5 | Commit `6b83de00`; gates at the head | All rc 0; em-dash 0 findings over 394 added lines; private-name scan of `git diff 6c22d3ca HEAD` clean | round2/gates/ |
| R2-6 | PR-BODY.md restructured into the template's sections | Done | PR-BODY.md |
| R2-7 | REVIEW READY on #653 | POSTED 21:55:23 CEST, https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5983801043; readback equal but for one trailing newline | REVIEW-READY-R2.md, REVIEW-READY-R2.readback.md, review-ready-r2-url.txt |
| R2-8 | HANDOFF.md, MANIFEST.sha256 | Updated; the manifest covers every packet file except itself | MANIFEST.sha256 |

**Changes at `6b83de00`** (`docs/findings/653_DISCONNECT_ORDER_BENCH.md`, `docs/findings/README.md`; no other file):

| Finding | Change |
|---|---|
| R483-1 F2 = R482-1 F1 (MINOR, Conformance, Tests, Docs) | The library section cites the check at the tag (file, lines, commit, link), its function, its condition (MEDIA_LOCKED = MEDIA_UNLOCKED or + 1, connection state not an input), the one other MEDIA_UNLOCKED use, and the bench tree's tie to the tag. It states that the check can flag neither order nor the CRF 1/0 window, that every update carried an accepted pair, and the conclusion: the owner's flag cannot come from this check and must come from the Hive application's own rules, not run here. Acceptance row 4: "No miscount flagged by the library; not a test of the order". The headline, the Contents line, the README row, the CRF section (no update inside either window; the held 1/0 came while Connected) and Limits (Hive as the only remaining source; the check read from source, not the installed binary) carry it |
| R483-1 F1 = R482-1 F2 (MINOR, Tests, Docs) | "The UNBIND_RX command left 1,629.8 µs after the probe's own GET_COUNTERS answer, and its response 1,637.3 µs after it." |
| R483-1 R1; R482-1 S1 | Identity row as written by R483-1 R1; it is also R482-1 S1's sentence |
| R483-1 R2 | PR-BODY.md in the template's sections (Status, Linked Issue / roles, Description, Authoritative references, How to get into the same state, How to validate, Known limitations, Definition of Done), plus a Round 2 section |
| R482-1 S2 = R483-1 S1 | Taken as one sentence in the control section and one Limits line |
| R483-1 S2 | Not taken: the grader stays as run; every capture holds one UNBIND_RX command and response |

No verdict, capture, measured order or per-cycle figure changed. The packet tools are unchanged; round2/r2_receipts.py is new and reads only packet files and the public library source.

## State at round 1

**REVIEW READY** (2026-10-04, 20:50 to 21:27 CEST). Bench work ran 20:55:56 to 21:15:44 CEST. Every change was restored and read back; the bench lock is free; nothing is left running on this host, the controller host, the tap host or the SoC board. The probe and its staging are removed from the controller host; the lane's captures are removed from the tap host.

- **Result:** the owner's report is not reproduced. In 23 of 23 disconnects (20 AAF on STREAM_INPUT 0, 2 CRF on STREAM_INPUT 1, 1 control) the UNBIND_RX response left the DUT's port first: 7.5 µs after the command; the unlock's unsolicited GET_COUNTERS 114.2 to 116.8 µs after the response (AAF), 99.3 and 99.7 ms (CRF). The la_avdecc controller library raised no compatibility change, diagnostic, query error or lost notification, and held 1/1/0 after every unbind. The control reads COUNTERS_FIRST against the probe's own GET_COUNTERS.
- **Commit:** `6f76d612a3191b77ac8a1fe2b9c66da42aeb405a` on `653-b11-bench`, one commit on dev `6c22d3ca`, one-line subject, no body, no trailers. Local, not pushed, no PR. It adds `docs/findings/653_DISCONNECT_ORDER_BENCH.md` (the dated section "#653 bench: disconnect order, 2026-10-04" and its supporting sections) and its row in `docs/findings/README.md`; no other doc edit.
- **Gates:** every gate rc 0 at `6f76d612` (gates/gates.txt, 12 commands, unpiped, physical /data path, Markdown gates in the pinned Markdown environment): `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base 6c22d3ca` (0 findings over 357 added lines), `check_doc_paths.py`, `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test`, `git diff --check`, `git diff --check 6c22d3ca HEAD`. The bare `check_baremetal_only.py` is a usage error, rc 2 (gates/check_baremetal_only.py_bare.out), as lanes B6 to B10 recorded. The same set passed on the uncommitted (staged) worktree first (gates-worktree/).
- **PR body:** PR-BODY.md, "Refs #653".

## Step ledger (CEST)

| Step | What | Result | Evidence |
|---|---|---|---|
| 0 | Context load (read-only): #653, its lane comments, STOP and ruling, the assignment, lane B10's packet and STOP, lane B9's tools, the earlier packets' methods | Read | this file |
| 1 | Local preconditions | PASS 20:54: board-link host address present; the UAC2 card and the external capture card present; three serial adapters; the lock free | - |
| 2 | TAKEN on #653 | POSTED 20:54:30 | TAKEN.md, taken-url.txt, TAKEN.readback.md |
| 3 | Identity gate (identity_b11.sh; identity_entity_b10.py; identity_cmp.py) | 20:55:56 to 20:56:25. **PASS: the four ATDECC facts** (entity_id `020000fffe000001`, "Milan FPGA 1x1 TDM8", "2.96.0", "AX7101-0001"); VERSION `0x00020060`; AEM, BIOS and payload CRCs equal the build's; static descriptors byte-equal; grader 10/10; ADP model `001bc5c1935893e1`. Lane B7's verdict file reads FAIL on the same three live-state checks as lane B10 (STREAM_INPUT 0's current format, CLOCK_DOMAIN 0's current source, GET_CLOCK_SOURCE 1) | identity/ |
| 4 | SoC console | 20:56:47 one carriage return: root prompt; 20:56:52 `id` over the board link: uid 0; bridge legs to-host 22063, from-host 22064 (as lane B10 left them) | soc/peek.log, soc/shell-check-net.log |
| 5 | Start baseline (baseline_b11.sh start) | 20:56:59 to 20:57:07, all rc 0. **As found:** CLOCK_SOURCE 1, servo IDLE (`MCSRV_STAT` 0x00000020); STREAM_INPUT 0 `0205022001006000`, STREAM_INPUT 1 `041060010000bb80` (the peer's AAF and CRF talker formats); one mapping on STREAM_PORT_INPUT 0, output map empty; every stream of both entities unbound; DUT inputs 0 and 1 at LOCKED/UNLOCKED 1/1; NVM image seq 51, 20 commits. Equal to lane B10's end state | restore/*-start*, soc/start-health.log |
| 6 | Controller library inspection (read-only; no lock: no bench resource) | la_avdecc 4.3.1.1 installed (headers, shared libraries); the installed include tree lacks `avdeccVirtualControlledEntityInterface.hpp`; the host's same-tag source tree has it and its other headers equal the installed ones | runs/build/ |
| 7 | Tap check (locked) | 21:00:34 to 21:00:40: sudo rights, tcpdump 4.99.6, a 4 s capture; 21:06:57 to 21:07:01 the pty start and Ctrl-C stop test; both test files removed from the tap host | runs/tap-check/ |
| 8 | Probe build 1, 2, 3 (build_o653.sh; no lock) | All GXX_RC 0. Build 2 fixed the status-text comparison ("Success." with a full stop); build 3 fixed the lock-wait predicate (the DUT resets an input's counters at a bind) | runs/build/build-1.txt to build-3.txt |
| 9 | Session s0 (run_o653.py, locked) | 21:07:50 to 21:07:55: both entities online, subscribed; cycle C0 ended FORMAT_READ_FAILED before the bind (build 1 defect); nothing bound; deregistration SUCCESS on both | runs/s0/ |
| 10 | Session s0b, the control (locked) | 21:08:19 to 21:08:31: C0 OK; the probe's own GET_COUNTERS (1/0) answered before the UNBIND_RX command | runs/s0b/ |
| 11 | Session s1, 20 AAF and 2 CRF cycles (locked) | 21:09:42 to 21:12:14: A01 to A20, R01, R02 all OK; 25 pcaps copied, hashes equal on both hosts, removed from the tap host; no probe left | runs/s1/ |
| 12 | Grade (o653_grade.py, o653_tables.py; offline) | 23 of 23 RESPONSE_FIRST (grader and provided decoder agree); tap time monotonic in file order in all 23; the control reads COUNTERS_FIRST against its own GET_COUNTERS | summary/ |
| 13 | Post-run snapshot (baseline_b11.sh post) | 21:14:50 to 21:14:57: servo HOLDOVER `0xffa40035` (the CRF cycles; CLOCK_SOURCE 1 selects the CRF input); census 45 of 46 equal; NVM image seq 97, 66 commits | restore/*-post* |
| 14 | Servo release (clock_release_b11.sh, locked) | 21:15:22 to 21:15:25: GET_CLOCK_SOURCE 1; SET_CLOCK_SOURCE 0 SUCCESS, read back 0; SET_CLOCK_SOURCE 1 SUCCESS, read back 1; servo IDLE `0x00000020` | restore/clock-release* , restore/servo-*-release.txt |
| 15 | End baseline (baseline_b11.sh end), controller staging removed; UART grader | 21:15:36 to 21:15:44, all rc 0; census 45 of 46 equal (the live propagation delay, 381 to 387 ns); servo IDLE; NVM image seq 98, 67 commits; `/tmp/a535` gone, no agent or probe process; grader 10/10 | restore/*-end*, restore/census-compare.txt, restore/controller-cleanup.txt, restore/grader-end.txt |
| 16 | Redaction | redact_b11.py, first pass 39 files changed, then a final pass over the late files; token scan clean | redaction.json |
| 17 | Findings page, index row, gates, commit | `6f76d612`, every gate rc 0 | gates/, gates-worktree/ |
| 18 | REVIEW READY on #653 | POSTED 21:25:33; readback equal but for one trailing newline | REVIEW-READY.md, REVIEW-READY.readback.md, review-ready-url.txt |

## Bench actions (one row per locked action, CEST)

| Time | Action | Result |
|---|---|---|
| 20:55:56-20:56:25 | Identity gate (identity_b11.sh): DUT console CRCs and QSPI reads, UART grader, AECP descriptor walk, ADP | all rc 0 |
| 20:56:43-20:56:47 | SoC console peek (one carriage return) | root prompt |
| 20:56:52-20:56:53 | SoC `id` and the bridge status over the board link | uid 0 |
| 20:56:59-20:57:07 | Start baseline (baseline_b11.sh start): SoC health, DUT reads, census, counters, peer and DUT descriptor surveys, controller, host view | all rc 0 |
| 21:00:34-21:00:40 | Tap host check and a 4 s test capture | rc 0 |
| 21:06:57-21:07:01 | Tap capture start and Ctrl-C stop test | stopped in 0.02 s; test files removed |
| 21:07:50-21:07:55 | Session s0 (probe build 1) with tap captures | FORMAT_READ_FAILED, nothing bound |
| 21:08:19-21:08:31 | Session s0b (probe build 2): control C0 | OK |
| 21:09:42-21:12:14 | Session s1 (probe build 3): A01 to A20, R01, R02 | 22 of 22 OK |
| 21:14:50-21:14:57 | Post-run snapshot (baseline_b11.sh post) | all rc 0; servo HOLDOVER |
| 21:15:22-21:15:25 | Servo release: DUT CLOCK_SOURCE 0, then 1, each read back | IDLE |
| 21:15:36-21:15:44 | End baseline (baseline_b11.sh end) and controller staging removal | all rc 0 |
| 21:15:44 | UART grader | 10/10 |

No outlet, JTAG, flash, SoC board reboot, USB gadget action, wiring or instrument setting was touched. Nothing was played on any instrument. No DUT register was written; the DUT changes were the probe's binds and unbinds and the clock-source release, each restored and read back.

## Run ledger (one row per cycle)

| Cycle | Kind | Window start (CEST) | Result |
|---|---|---|---|
| s0 C0 | AAF, control | 21:07:53 | FORMAT_READ_FAILED (probe defect); nothing bound; not graded |
| s0b C0 | AAF, control | 21:08:23 | RESPONSE_FIRST; COUNTERS_FIRST against its own GET_COUNTERS |
| s1 A01 to A20 | AAF, STREAM_INPUT 0 | 21:09:47 to 21:11:50, about 6.4 s apart | 20 of 20 RESPONSE_FIRST; library flags none; pair after 1/1/0 |
| s1 R01, R02 | CRF, STREAM_INPUT 1 | 21:11:57, 21:12:04 | RESPONSE_FIRST; unlock push 99.3 and 99.7 ms after the response; library held 1/0 for 95.0 and 100.0 ms while NotConnected, no flag |

The per-cycle table with every interval and capture hash is in summary/o653-page-tables.md and on the findings page.

## Tool changes

Lane B9's tools were copied as taken (tools/ORIGIN-B9.sha256 pins every file of lane B9's tools directory); lane B10's identity_entity_b10.py and lane_state_b10.sh were copied as taken (tools/ORIGIN-B10.sha256). The provided tap_order_decode.py is unchanged (sha256 `144fce57...`, equal to lane B10's copy). Unchanged and used: identity_entity_b10.py, identity_cmp.py, avdecc_ro.py, b8_ctl.py, console_read.py, soc_peek.py, census_cmp.py. The other copies of lane B9's tools (tone, THD+N, run and grade tools) were not run.

| Tool | Taken from | Change |
|---|---|---|
| identity_b11.sh, baseline_b11.sh | lane B9's `*_b9.sh` | The environment name (B11_ENV) and the controller staging (/tmp/a535) only; a sed rewrite also changed those names inside older comment lines |
| lane_state_b11.sh | lane B10's lane_state_b10.sh | The environment name and the staging only; prepared, not run |
| soccon_net.py | lane B9's | The tag prefix only (A535) |
| redact_b11.py | lane B9's redact_b9.py | Its own name in the skip list, and the ORIGIN hash lists skipped |
| o653_probe.cpp | new | The controller probe (session through the library's high-level controller; a low-level auxiliary entity for live format reads and the control's GET_COUNTERS; deregistration at the end). Three builds, see step 8 |
| build_o653.sh | new | Stages and builds the probe on the controller host; overlays the one missing header from the same-tag source tree |
| run_o653.py | new | One locked session: per-cycle tap capture on a pty (stopped with Ctrl-C), the probe's cycle, then the pcaps copied, hashed on both hosts and removed from the tap host |
| o653_grade.py | new | Per-cycle wire order from the tap captures (file order, tap timestamp checked) and the library's view from the probe log; runs the provided decoder unchanged on each capture. Its first two runs used wrong tap-record offsets (bytes 12..15 taken as a record counter) and found no UNBIND_RX; fixed to the 64-bit timestamp (high word first) and file order, then re-run |
| o653_tables.py | new | Renders the page's tables and ranges from the grade |
| clock_release_b11.sh | new | One locked action through lane B8's agent: DUT CLOCK_SOURCE 0 then 1, each read back, with the servo word read before and after |

## Deviations and decisions

- **Posts on #653, not #629.** The lane prompt's template asked for TAKEN on #629, but this lane runs only #653's item, the public assignment is on #653 and directs REVIEW READY there, and posting on #653 is the only issue posting the prompt allows. TAKEN and REVIEW READY went to #653; nothing to #629.
- **Clock source during the cycles.** The cycles ran at the as-found CLOCK_SOURCE 1 (no clock change before them). The CRF binds therefore engaged the DUT's servo, which was left in HOLDOVER; the release (INTERNAL and back, on the listener's CLOCK_DOMAIN, read back) restored IDLE, as lane B10 found it releases the held trim.
- **Binding rule.** Read live before every bind; formats equal in all 23 cycles; no SET_STREAM_FORMAT sent.
- **The control** ran in its own short session (s0b) on probe build 2, which differs from build 3 only in the lock-wait predicate (correct for a session's first cycle, as C0 was).
- **The missing header** was taken from the controller host's la_avdecc source tree at the same tag; its hash is in the build logs and on the page.
- **The capture filter** (the assignment's) also keeps stream frames, so the AAF pcaps are 4 to 6 MB each; all 31 pcaps (about 104 MB) stay under /tmp/b11-a535/raw.
- **The provided decoder** was kept unchanged. Its time column reads the tap timestamp's 32-bit words swapped and its ACMP listener, unique ID and count columns read wrong offsets; its line order is correct and agrees with the grader in all 23 captures.
- **SoC board:** read-only health only (as lane B10 did), no bridge action.

## Residuals

- **DUT NVM:** image seq 51 to 98, commits 20 to 67 (`pend=1` at both ends): the 23 binds, the 23 unbinds and the clock-source restore.
- **DUT CLOCK_DOMAIN 0 counters:** LOCKED/UNLOCKED 3/3 to 6/6 (three servo lock and unlock pairs).
- **DUT STREAM_INPUT counters:** 1/1 at both ends on inputs 0 and 1; their FRAMES_RX and TIMESTAMP_VALID now count the last cycles.
- **Raw files:** /tmp/b11-a535/raw (RAW-ARTIFACTS.json), kept outside the packet.

## Open items for the owner and the manager

- The report came from a Hive session; this lane records what the la_avdecc library itself reports. Round 2: the library's one counter check (v4.3.1.1) cannot flag the order, so the owner's flag must come from Hive's own rules. The owner's Hive and library versions, or a capture from that session, would locate it.
- PR #655 (the CRF unlock at the bind fall) is not on this image; the CRF 1/0 window is its pre-fix behaviour.
- #653 stays open: "Refs #653".

## Packet layout

| Path | What |
|---|---|
| HANDOFF.md | This file |
| TAKEN.*, REVIEW-READY.*, *-url.txt | The posts and their readbacks |
| PR-BODY.md | Proposed PR body |
| identity/ | The identity gate: console CRCs and QSPI AEM reads, AECP descriptor walk, ADP, grader, expected.json (the build's values), identity-verdict.txt (lane B7's form), identity-entity-verdict.txt (the four facts), lock window |
| soc/ | SoC console peek and root-shell check; health at start, post and end |
| runs/build/ | The three probe builds (redacted) |
| runs/tap-check/ | The tap host check and the capture stop test |
| runs/s0/, runs/s0b/, runs/s1/ | Each session's probe log (JSON lines), driver log and lock window |
| summary/ | o653-grade.json (per cycle: wire and library), o653-table.md, o653-page-tables.md (the page's tables and ranges), decode/ (the provided decoder's output per capture) |
| restore/ | Census, counters, DUT reads, controller and host views at start, post and end; the census comparison; the clock release; the servo reads; the controller cleanup; the end grader |
| tools/ | Every tool used or prepared; ORIGIN-B9.sha256 and ORIGIN-B10.sha256 pin the copies as taken |
| gates/, gates-worktree/ | Gate commands and outputs at `6f76d612` and on the staged worktree |
| redaction.json | Per redacted file: original and retained SHA-256, labels |
| RAW-ARTIFACTS.json | Every raw file under /tmp/b11-a535/raw by path, size and SHA-256 |
| tap_order_decode.py | The provided #653 tap decoder, unchanged |
| round2/ | Round 2: r2_receipts.py and its three receipts (library-check.txt, control-interval.txt, library-updates.txt); gates/ at `6b83de00` and gates-worktree/ before the commit |
| REVIEW-READY-R2.*, review-ready-r2-url.txt | The round-2 REVIEW READY post and its readback |
| MANIFEST.sha256 | SHA-256 of every packet file except itself |
