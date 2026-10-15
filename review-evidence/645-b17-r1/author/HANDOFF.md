# [A619] Bench lane B17 handoff

Refs #645: time the loopback ring slips (`SLIP_LB`) through a bind of the reference peer's talker to the DUT's listener with the DUT's media clock on INTERNAL, per the ruling https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6099627217. Installed dev `5603c353` image (B14/B15's), not flashed.

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6186729424
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6186841336 (TAKEN.md; TAKEN.readback.md equal but for one trailing newline; taken-url.txt)
- STOP: https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6186910934 (STOP.md; STOP.readback.md equal but for one trailing newline; stop-url.txt)
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6187529947 (REVIEW-READY.md; REVIEW-READY.readback.md equal but for one trailing newline; review-ready-url.txt)
- Posted on #645: TAKEN, STOP and REVIEW READY only; no existing comment was edited or deleted.
- Branch: `645-b17-bench` from dev `f62602531d415d6c1cae1374a3cc2938faf54049`, lane worktree on the physical /data path. Head `56d008f68f445156a9bdd81eb32f8d5353cc7a7f`, one commit ("Record #645 bench lane B17 on dev 5603c353: ten binds at INTERNAL each slip the loopback ring once, all class (c)"): the dated B17 section and its Contents entry in `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, nothing else. Not pushed; no PR (PR-BODY.md holds the body).
- Packet: this directory. Private endpoints (hosts, interfaces, the peer's and the controller's identifiers, the grandmaster's identity), the redaction map, the unmasked originals, the host view and the SoC console transcripts stay in a private directory outside it.

## State

**RESUMED** (2026-10-15, 09:32 CEST) under the manager's answer https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6186940255: no SoC board (no console access at all); at INTERNAL classify each slip as (a) declared transient between a recentre's arming and firing, (b) rate offset matching 1/(f_s x |delta_ppm|) with delta_ppm measured in the same cycle, or (c) unexplained; poll `SLIP_LB`, the render recentre count and the aligner state every 0.5 s. TAKEN was not posted again.

**DONE: REVIEW READY posted 10:08:49 CEST** (comment 6187529947). 10 cycles ran; one slip per bind, all ten class (c); #645 stays open under the ruling (its close condition is not met, so PR-BODY says Refs #645). Restore read back; the bench lock is free; nothing is left on the controller or tap host. Gates all rc 0 on the head (`gates/gates.txt`).

Observability found at the image's source (dev `5603c353`) before any cycle: the render stage's `recentres_o` reaches no CSR (`hdl/milan/milan_datapath.sv` builds `RENDER_STAT` from rails, converged, prefill and fill only; `docs/reference/REGISTER_MAP.md:2064`, "recentre counters remain separate verification taps"), and the grid aligner's engaged and settled state and the settle-recentre controller's pending state reach no CSR either. The poll therefore reads every word the CSRs do expose for the question (B8's poller: `SLIP_LB`, `SLIP_TDM`, `RENDER_STAT`, `MCSRV_STAT`, `AAFM_STAT`/`AAFM_RATE`, `CRF_CTRL`, `CRF_RATE`), and the gap is published with the result. At INTERNAL no DUT rate CSR measures the peer against the DUT (`AAFM_*` runs only with an AAF source selected, and the DUT's CRF input is unbound), so delta_ppm comes from the AAF presentation timestamps on the DUT's link tap: the peer's received stream against the DUT's own transmitted stream.

### Before the resume

**STOP** (2026-10-15, 09:27:44 CEST), at a bench-rule STOP condition before any probe cycle. The owner's bench recipe requires the SoC board's serial console to be at a root shell, confirmed with one harmless read-only command, and says: on a login prompt, STOP; the manager logs in, and no credential is ever typed or stored. The start baseline's console check sent one empty line and read a login prompt (`soc_check_b17.py` rc 3). Nothing else was sent to the board.

The lane's probe does not use the SoC board (no tone, no TDM capture). Whether it may run without the board, as B14 ran under its ruling, is the manager's decision, not this lane's.

No bind, unbind, stream format, clock source, map or register was written, on the DUT or the peer. The identity gate passed and the as-found state was read (below). The controller staging was removed and the bench lock is free.

## Step ledger (CEST)

| Step | What | Result | Evidence |
|---|---|---|---|
| 0 | Context load (read-only): #645 in full (42 comments), the assignment, the ruling; B15's packet (`SLIP_LB` read as `mem_read 0x900008d4 12` in `restore/dut-*.txt`; no poll); B14's packet and page (the settle boundary, `sw_b14.py`, `sw_summary_b14.py`, the restore rows); B8's packet (`console_poll_b8.py`, the pre-set INTERNAL slips) | Read | this file |
| 1 | Local preconditions | 09:24: the board-link host address present; the board's USB audio card and the external capture card present; three serial adapters; the bench lock free. Controller host reachable (locked read 09:24:37) | private (host view) |
| 2 | HANDOFF skeleton | 09:25 | this file |
| 3 | TAKEN on #645 | POSTED 09:26:06, comment 6186841336 | TAKEN.md, taken-url.txt, TAKEN.readback.md |
| 4 | Identity gate (`identity_b17.sh`, `identity_b15.py`) | 09:26:41 to 09:26:47: **PASS** 11 of 11 | identity/ |
| 5 | Start baseline (`baseline_b17.sh start`) | 09:27:44 to 09:27:47, lock rc 0. SoC console: **login prompt**, rc 3 (STOP). DUT reads, census, counters and controller view rc 0 | restore/*-start*, restore/baseline-start-lock.txt |
| 6 | Controller staging removed | 09:28:45, rc 0; no lane process left on the controller host | restore/controller-cleanup.txt |
| 7 | Redaction pass (`redact_b17.py`, private map) and privacy scan | 9 files masked (identifiers of the peer, the controller and the grandmaster, the controller's interface, an account name); a scan of every packet file for private names, hosts, addresses, adapters and tool names finds none; no file over 200 KB | redaction.json |
| 8 | STOP on #645 | POSTED 09:30:36, comment 6186910934 | STOP.md, stop-url.txt, STOP.readback.md |
| 9 | Manifest | MANIFEST.sha256 over every packet file but itself | MANIFEST.sha256 |
| 10 | Resume: the answer 6186940255 read; observability checked at the image's source (no CSR for `recentres_o`, the aligner state or the settle controller) | 09:32 to 09:38 | State, above |
| 11 | Identity re-check over ATDECC only (`identity_atdecc_b17.sh`) | 09:39:28, lock rc 0: **PASS** (the four ENTITY facts); GET_CLOCK_SOURCE 0 | identity-resume/ |
| 12 | Tap host re-check (read-only, locked) | 09:39:41: reachable, both tap interfaces up, no capture file or tcpdump process left | private (tap pre-check) |
| 13 | Tools: `cyc_b17.py` (cycle runner), `run_locked_b17.sh`, `ana_b17.py` (grading); `ana_b17.py control` | First run 15 of 16: the control's own synthetic `RENDER_STAT` set the prefill bit (`0x10b`); corrected to `0x20b`, no tool code changed; second run **16 of 16** | controls/b17-ana-controls.json |
| 14 | Controller staging (locked) | 09:46:09, rc 0; hashes equal the ORIGIN pins | restore/controller-stage-resume.txt |
| 15 | Cycles c01 to c10 (`run_locked_b17.sh 170 cyc_b17.py N`), one lock hold each | 09:46:15 to 09:56:07 CEST, all rc 0, each ended bound as found | cycles/, cycle ledger below |
| 16 | Grading (`ana_b17.py cycle`), late-PDU list added and controls re-run (17 of 17), lane summary (`summ_b17.py`) | 10 slips, all (c); grades byte-identical across the tool's last change | summary/ |
| 17 | End baseline (`baseline_b17r.sh end`, no SoC access), census compare | 09:57:46 to 09:57:48, lock rc 0; 45 of 46 equal (live propagation delay) | restore/*-end*, restore/census-compare.txt |
| 18 | Redaction pass (map extended with the tap host and its interfaces) and privacy scan | 16 files masked in the pass; one of them was a tool carrying the peer's identifier as a synthetic control value: the value was replaced in the tool instead of masked, and its record entry dropped, leaving 15 masked files; scan finds no private name; no file over 200 KB | redaction.json |
| 19 | Findings section, gates, commit | Head `56d008f68`; all gates rc 0 | gates/gates.txt |
| 20 | REVIEW READY on #645 | POSTED 10:08:49 CEST, comment 6187529947, read back | REVIEW-READY.md, review-ready-url.txt, REVIEW-READY.readback.md |
| 21 | Manifest | MANIFEST.sha256 over every packet file but itself | MANIFEST.sha256 |

## Identity gate (step 4)

`identity/identity-verdict.txt`: entity_id `020000fffe000001`, entity name "Milan FPGA 1x1 TDM8", firmware_version "2.96.0", serial "AX7101-0001"; console `ID=4d494c4e VERSION=00020060`; CRC32 of the 7,512-byte AEM image in QSPI `5ba355eb`; live ENTITY (312 B) and CONFIGURATION (106 B) equal to the QSPI bytes; CLOCK_SOURCE 0 Internal, 1 CRF Clock (STREAM_INPUT 1), 2 Stream Clock (STREAM_INPUT 0), 3 NO_SUCH_DESCRIPTOR; CLOCK_DOMAIN 0 lists 0, 1, 2; GET_CLOCK_SOURCE 0; UART grader PASS 10/10; ADP model `001bc5c1935893e1`. gPTP `SYNC=1 ASCAPABLE=1 TU=0`.

## As found (step 5, 07:27:44 UTC)

From `restore/census-start.jsonl`, `restore/dut-start.txt` and `restore/counters-start.jsonl`:

| Item | As found |
|---|---|
| DUT CLOCK_SOURCE | 0 (INTERNAL) |
| DUT servo (`0x8F8`) | `0x00000020`: state IDLE |
| DUT STREAM_INPUT 0 | **bound** to the reference peer's STREAM_OUTPUT 0, flags `0x0002`, format `0205022001006000` |
| DUT STREAM_INPUT 1 | unbound, format `041060010000bb80` |
| The peer's STREAM_OUTPUT 0 format | `0205022001006000`, equal to the DUT's STREAM_INPUT 0: the binding rule sets nothing |
| The peer's STREAM_INPUT 0 and 8 | bound to the DUT's AAF and CRF talkers, flags `0x0082` |
| The peer's clock source | 1 |
| DUT maps | STREAM_PORT_INPUT 0: 4 mappings; STREAM_PORT_OUTPUT 0: 8 |
| `SLIP_LB` (`0x8D4`) | `0x000000d0`: 208 dups, 0 skips (B15 ended at 152) |
| `SLIP_TDM` (`0x8D8`) | 0 |
| DUT saved state | image seq 295, 54 records, commits ok 61, failed 0, `pend=1` |

So the probe state the ruling names (the DUT on INTERNAL, the peer's talker bound to the DUT's listener) is already the as-found state. A resumed lane's cycle is an unbind of that binding, a pre-bind poll of at least 5 s, the re-bind under the binding rule and a hold of at least 30 s, ending bound as found.

## Cycle ledger (one row per bind cycle)

Times are seconds from the bind's CONNECT_RX command (this host's clock through the agent's sync offset; on the tap the same command is the zero). Settle boundary: B14's definition (first LOCKED poll + 4.096 s + 0.5 s, `docs/findings/B14_BENCH_5603C353.md:80`) is undefined at INTERNAL (servo IDLE in every poll), as the resume ruling states; each slip is classed (a)/(b)/(c) instead. delta_ppm: the peer's AAF presentation-timestamp rate minus the DUT's own AAF stream's, on the DUT's link tap.

| Cycle | Lock window (UTC) | Unbind / bind | Polls (first, last s) | `SLIP_LB` dups start to end | Slips: interval s, dups/skips, largest PDU lateness in it | delta_ppm (rate interval) | First peer PDU after bind | Class | Ended bound as found |
|---|---|---|---|---|---|---|---|---|---|
| c01 | 07:46:14.9-07:47:06.8 | SUCCESS / SUCCESS, format equal, none set | 80 (-8.00, +31.77) | 208 to 210 | 2.56 to 3.14: +2/0; 28.8 us (first burst over 20 us; none over 10 us before it; 20 later bursts to 28.7 us, no slip) | -0.0002 (104,167 s) | 163.5 ms | (c) | yes |
| c02 | 07:47:42.1-07:48:34.0 | SUCCESS / SUCCESS, format equal, none set | 80 (-8.00, +31.83) | 210 to 212 | 1.09 to 1.96: +2/0; 25.0 us (first burst over 20 us; none over 10 us before it; 10 later bursts to 28.4 us, no slip) | +0.0006 (34,722 s) | 93.5 ms | (c) | yes |
| c03 | 07:48:34.1-07:49:25.8 | SUCCESS / SUCCESS, format equal, none set | 80 (-7.99, +31.75) | 212 to 214 | 1.07 to 1.95: +2/0; 26.3 us (first burst over 20 us; none over 10 us before it; 18 later bursts to 28.7 us, no slip) | -0.0005 (41,667 s) | 156.8 ms | (c) | yes |
| c04 | 07:49:25.8-07:50:17.7 | SUCCESS / SUCCESS, format equal, none set | 80 (-8.00, +31.83) | 214 to 216 | 3.10 to 3.68: +2/0; 29.3 us (first burst over 20 us; none over 10 us before it; 14 later bursts to 30.1 us, no slip) | -0.0017 (12,255 s) | 52.8 ms | (c) | yes |
| c05 | 07:50:51.1-07:51:43.2 | SUCCESS / SUCCESS, format equal, none set | 80 (-8.00, +31.84) | 216 to 218 | 0.07 to 0.64: +2/0; 24.6 us (first burst over 20 us; none over 10 us before it; 21 later bursts to 30.3 us, no slip) | +0.0002 (104,167 s) | 7.9 ms | (c) | yes |
| c06 | 07:51:43.3-07:52:35.1 | SUCCESS / SUCCESS, format equal, none set | 80 (-7.99, +31.83) | 218 to 220 | 3.57 to 4.15: +2/0; 25.8 us (first burst over 20 us; none over 10 us before it; 12 later bursts to 28.5 us, no slip) | +0.0016 (13,021 s) | 131.5 ms | (c) | yes |
| c07 | 07:52:35.1-07:53:26.9 | SUCCESS / SUCCESS, format equal, none set | 80 (-8.01, +31.84) | 220 to 222 | 1.06 to 1.94: +2/0; 25.0 us (first burst over 20 us; none over 10 us before it; 21 later bursts to 29.1 us, no slip) | +0.0002 (104,167 s) | 54.9 ms | (c) | yes |
| c08 | 07:53:31.6-07:54:23.7 | SUCCESS / SUCCESS, format equal, none set | 80 (-7.99, +31.93) | 222 to 224 | 1.18 to 1.94: +2/0; 25.6 us (first burst over 20 us; none over 10 us before it; 23 later bursts to 27.6 us, no slip) | +0.0003 (69,444 s) | 28.5 ms | (c) | yes |
| c09 | 07:54:23.7-07:55:15.5 | SUCCESS / SUCCESS, format equal, none set | 80 (-8.00, +31.79) | 224 to 226 | 1.04 to 1.95: +2/0; 25.1 us (first burst over 20 us; none over 10 us before it; 18 later bursts to 29.5 us, no slip) | +0.0001 (208,333 s) | 161.2 ms | (c) | yes |
| c10 | 07:55:15.5-07:56:07.4 | SUCCESS / SUCCESS, format equal, none set | 80 (-8.00, +31.80) | 226 to 228 | 5.09 to 5.67: +2/0; 26.9 us (first burst over 20 us; none over 10 us before it; 12 later bursts to 27.8 us, no slip) | +0.0006 (34,722 s) | 101.1 ms | (c) | yes |

Every cycle: `SLIP_TDM` static at 0; `MCSRV_STAT` state IDLE in every poll (so B14's boundary is undefined); `AAFM_STAT` 0 (no AAF source selected); `RENDER_STAT` out of prefill 0.12 to 0.65 s after the bind, fill 8 to 14 after it, rails 11 throughout; no `SLIP_LB` change in the 2 s bound before the unbind or while unbound. Peer PDU arrival on the DUT's link: 1.41 to 1.45 us (median) after the DUT's own transmit grid, mod 125 us, in every cycle; lateness p99.9 4.4 to 6.1 us, max 27.6 to 30.3 us; 0 sequence gaps in all three streams. The DUT's AAF and CRF streams run +4.99 to +5.02 ppm against gPTP time and the peer's within 0.0017 ppm of them (the peer follows the DUT's CRF, as found).

**Verdict under the resume ruling: 10 slips, all (c); 0 (a), 0 (b). #645 stays open.** Lane totals in `summary/cycles.json`; the raw counter logs' digest is `summary/counter-logs.sha256`, SHA-256 `a1d415300d55cfc2c14178493a244edab56446bbfa3aa860721e8b39819c7848`; poller SHA-256 `1912837a1e4cfd6a1f8b3615b4d26924efbfd430aff239ebd18cd4dd2a67d4f7`.

## Bench actions (one row per locked action, CEST)

| Time | Action | Result |
|---|---|---|
| 09:24:37-09:24:38 | Controller host reachability (read-only) | rc 0 |
| 09:26:41-09:26:47 | Identity gate: DUT console reads, UART grader, AECP descriptor walk, ADP | all rc 0; PASS |
| 09:27:44-09:27:47 | Start baseline: SoC console check (one empty line), DUT reads, census, counters, controller view | SoC: login prompt (STOP); the rest rc 0 |
| 09:28:45 | Controller staging removal | rc 0 |
| 09:39:28-09:39:29 | Resume: identity re-check over ATDECC (ENTITY 0, GET_CLOCK_SOURCE) | rc 0; PASS |
| 09:39:41-09:39:42 | Tap host re-check (read-only) | rc 0 |
| 09:46:09-09:46:10 | Controller staging (`avdecc_ro.py`, `b8_ctl.py`, hashes equal to the ORIGIN pins) | rc 0 |
| 09:46:15 to 09:56:07 | Cycles c01 to c10, one lock hold each (windows in the cycle ledger): unbind and re-bind of the peer's STREAM_OUTPUT 0 to the DUT's STREAM_INPUT 0, formats read (none set), DUT console poll, tap capture on the DUT's link | all rc 0 |
| 09:57:46-09:57:48 | End baseline (`baseline_b17r.sh end`): DUT reads, census, counters, controller view, staging removed | all rc 0 |

No outlet, JTAG, flash, reload, power cycle, wiring or instrument action; no SoC board access after the resume; no USB gadget action. Writes: only the 10 ACMP unbinds and 10 re-binds of the as-found binding (no stream format, clock source, map or register written on either entity). The bench lock was taken for every console, controller and tap action and was free at the end.

## Tool changes

Inherited tools are pinned in `tools/ORIGIN-B15.sha256` and `tools/ORIGIN-B14.sha256` (B14's and B15's shared tools are byte-equal). Used unchanged: `console_read.py`, `avdecc_ro.py`, `b8_ctl.py` (census, counters and agent modes), `identity_b15.py`, `census_cmp.py`, and the poller `console_poll_b8.py`, SHA-256 `1912837a1e4cfd6a1f8b3615b4d26924efbfd430aff239ebd18cd4dd2a67d4f7` (every cycle's `start` event records it). Copied, not run: `b7_decode.py`, `sw_b14.py`, `sw_summary_b14.py`, `baseline_b15.sh`, `identity_b15.sh`.

| Tool | Taken from | Change |
|---|---|---|
| identity_b17.sh | B15's identity_b15.sh | Environment B17_ENV, staging /tmp/a619 |
| baseline_b17.sh | B15's baseline_b15.sh | Environment B17_ENV, staging /tmp/a619; the SoC board checked on its serial console by soc_check_b17.py instead of SSH; descriptor surveys dropped; host view and SoC transcript to the private directory |
| baseline_b17r.sh | baseline_b17.sh | The SoC console check removed (resume ruling) |
| soc_check_b17.py | new | One empty line; only at a root prompt, the board script's read-only `status` verb; on a login prompt nothing more, rc 3 (not run after the resume) |
| identity_atdecc_b17.sh | new | ENTITY 0 and GET_CLOCK_SOURCE over AECP, the four ATDECC facts checked |
| cyc_b17.py | B14's sw_b14.py (Agent, Poll, Capture, binding rule) | One bind cycle per invocation; snap length 96; as-run SHA-256 `12ec02fe06f3ec5970fd46a4b17e81a97bed51334af7b41a8358231fa5555f17` |
| run_locked_b17.sh | B14's run_locked_b14.sh | Environment B17_ENV |
| ana_b17.py | new (tap reading after B14's tapdec_b14.py) | Grades one cycle; `control` 17 of 17. As run for every summary: `299d4f55441e147bf6d27b5b51242d3384157e4905d27f6ed1064398f05f9468`. Earlier versions (private): `72f149a2...` graded c01 to c10 first; `81c2d922...` added the late-PDU list (17 of 17); `299d4f55...` replaced synthetic identifiers in the control that copied a private one, with byte-identical summaries |
| summ_b17.py | new | The lane table, `summary/cycles.json`, the counter-log digest |
| redact_b17.py | B15's redact_b15.py | Its own name and the two ORIGIN files in the skip list |

## Deviations and decisions

- **The STOP.** The owner's bench recipe's login-prompt condition applied at step 5; the lane stopped there, as written, rather than judging privately that a lane not using the board may continue.
- **The settle boundary, stated in TAKEN.** B14 defines it as the first poll that saw LOCKED, plus 4.096 s, plus 0.5 s (`docs/findings/B14_BENCH_5603C353.md:80`; `sw_summary_b14.py`). At INTERNAL the servo reads IDLE (as found here, and in B14's returns to INTERNAL), and the design lists no bind among the settle recentre's arm terms (`docs/design/MEDIA_CLOCK_FOLLOWING.md:1088-1096`; "A bind still primes the ring where its first PDU lands", `:1187-1188`). Under B14's definition the boundary is therefore expected to be undefined in every cycle; TAKEN says the lane would record it so and stop for a ruling if any slip occurs. The manager may rule on this together with the resume.

- **Resume: what the poll can see.** The ruling asks for the render recentre count and the aligner state every 0.5 s. Neither reaches a CSR on this image (State, above); the lane polled every word that does bear on them (B8's poller, unchanged) and published the gap with the result, rather than stopping, because the ruling's "as far as the CSRs expose it" anticipates partial exposure and the cycles only remake the as-found binding.
- **Resume: delta_ppm from the tap.** No DUT rate CSR compares the peer with the DUT at INTERNAL, so delta_ppm comes from the AAF presentation timestamps on the DUT's link tap (the capture point lane B14 used, and B15), the ruling's first named method. Captures kept AVTP and ACMP only, 96 bytes each.
- **Resume: the late-arrival analysis** (first late burst inside each slip's interval) goes beyond the ruling's three classes. It is published as an observation consistent with the design's bind priming, not as a class or a diagnosis.
- **No peer clock change.** Lanes B8 and B9 set the peer to its internal source for their probe; the assignment names only the DUT's clock and the bind, so the peer stayed on its as-found source (following the DUT's CRF). That is why delta_ppm is near zero.

## Restore and residuals

`restore/census-compare.txt`: 45 of 46 census entries equal start to end (the unmasked start against the end); the other is the DUT's live propagation delay in GET_AVB_INFO, 381 to 385 ns. The DUT's STREAM_INPUT 0 is bound to the peer's STREAM_OUTPUT 0 with flags `0x0002`, as found; CLOCK_SOURCE 0; both maps, every format and the peer's bindings and clock source as found. Controller staging removed, no agent left; no capture file left on the tap host (each removed after its hash matched).

Residuals that no permitted command restores:

- `SLIP_LB` 208 to 228 dups, 0 skips (`restore/dut-end.txt`): the 10 slips.
- DUT saved state: image seq 295 to 315, commits ok 61 to 81, failed 0, `pend=1` (each unbind and bind commits).
- The SoC board's console was left at the login prompt it showed before the resume; it was not accessed again.

## Open items for the manager

- #645 stays open under the resume ruling's verdict: every slip is (c). The ruling's (a) needs the recentre count and the aligner state, which no CSR exposes on this image; (b) is excluded by the measured offset in every cycle.
- The observation for the decision: each bind at INTERNAL slipped the loopback ring exactly once, at the first late arrival burst after it, and never again in the hold, through 10 to 23 later bursts as large.

## Packet layout

| Path | What |
|---|---|
| HANDOFF.md | This file |
| TAKEN.*, STOP.*, REVIEW-READY.*, *-url.txt | The posts and their readbacks |
| PR-BODY.md | Proposed PR body (Refs #645) |
| gates/gates.txt | The gate results on the head |
| identity/ | The identity gate: console reads, grader, AECP descriptor walk, ADP, verdict, lock window |
| identity-resume/ | The resume's ATDECC identity re-check and verdict |
| cycles/cNN/ | Per cycle: `events.jsonl` (the runner's events, binds, formats, states, counters, capture record) and `poll.jsonl` (the raw counter log: every 0.5 s poll's words) |
| summary/ | `cNN.json` per cycle (ana_b17.py), `cycles.json`, `table.md`, `counter-logs.sha256` |
| controls/ | `b17-ana-controls.json` |
| restore/ | Start and end baselines: DUT console reads, census, counters, controller view, lock windows; census compare; controller staging and cleanup |
| RAW-ARTIFACTS.json | The 10 tap captures (outside the packet, bench host /tmp/645-b17/pcap/, 872,609,064 bytes in all) and the private controller transcripts, with sizes and SHA-256 |
| tools/ | Every tool used or copied; ORIGIN-B14.sha256 and ORIGIN-B15.sha256 pin the inherited ones |
| redaction.json | Per redacted file: original and retained SHA-256, labels |
| MANIFEST.sha256 | SHA-256 of every packet file except itself |
