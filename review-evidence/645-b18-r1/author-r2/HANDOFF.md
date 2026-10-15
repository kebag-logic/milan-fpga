# [A622] Bench lane B18 handoff

Refs #645: the acceptance repeat of lane B17's ten binds at INTERNAL on the installed dev `9ef71772` image, which carries PR #742 (a bind's first PDU at INTERNAL arms the settle recentre). Not flashed, not power-cycled.

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6199691564
- Ruling it carries out: https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6099627217 (close condition, as the assignment states it: every bind at INTERNAL holds, apart from the #743 residual)
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6199781988 (TAKEN.md, taken-url.txt, TAKEN.readback.md)
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6200209744 (REVIEW-READY.md, review-ready-url.txt, REVIEW-READY.readback.md)
- Posted on #645: TAKEN and REVIEW READY only; no existing comment was edited or deleted.
- Branch: `645-b18-bench` from dev `9ef717727e6fdac11ee7f01672fefae948452343`, lane worktree on the physical /data path. Findings docs only. Not pushed; no PR (PR-BODY.md holds the body).
- Packet: this directory. Private endpoints, the redaction map, the unmasked originals, the host views and the per-cycle runner logs stay in a private directory outside it.

## State

**DONE: REVIEW READY posted (comment 6200209744).** Bench done 2026-10-15, 20:59:59 CEST. Ten cycles ran, all ten **held**: `SLIP_LB` read 0 dups, 0 skips in every one of 800 polls and at both baselines. No #743 residual, no class (c) slip, no CLOCK_SOURCE change. The ruling's close condition is met, so PR-BODY.md says "Closes #645". Restore read back; the bench lock is free; nothing is left on the controller or tap host. Head `480c5e916f8bf711c47e1985ba3efe2b2471bdda` (one commit on dev `9ef71772`, the section and its Contents entry, +315 lines); all gates rc 0 (`gates/gates.txt`). REVIEW READY: see the step ledger.

**Round 2 (docs only, no bench access): see the Round 2 section at the end.** Head `b3f7a696713a96b42265e08a8c3a04a430b7b5ed`.

## Step ledger (2026-10-15; bench times UTC, CEST = UTC + 2)

| Step | What | Result | Evidence |
|---|---|---|---|
| 0 | Context load (read-only): the assignment, #645 in full (56 comments), #743, the B17 packet and section, the PR #742 design text ("A bind at INTERNAL", the settle-recentre table) | Read | this file |
| 1 | Local preconditions (18:49 UTC) | Board-link host address present; the board's USB audio card and the external capture card present; three serial adapters; bench lock free | private (host view) |
| 2 | Tools copied from B17, B18 variants made (paths and environment only) | Done | Tool changes, below |
| 3 | HANDOFF skeleton | Done | this file |
| 4 | TAKEN on #645 | Posted 18:50:08 UTC, comment 6199781988, read back (equal but for one trailing newline) | TAKEN.md, taken-url.txt, TAKEN.readback.md |
| 5 | Identity gate (`identity_b18.sh`, `identity_b15.py`) | 18:50:11 to 18:50:17 UTC: **PASS** 11 of 11 | identity/ |
| 6 | Flash record cross-check (read-only, outside the packet) | `build-9ef71772/flash.log` SHA-256 `a1539c67fc8c6490034332976024248decf3046fdc8da72a9c867762e09d9d46`: `FLASH_RC=0`, `POWERCYCLE_RC=0`, boot line `CSR ID=4d494c4e VERSION=00020060`, AEM 7512 B, CRC `5ba355eb` | this file |
| 7 | Start baseline (`baseline_b18.sh start`, no SoC access) | 18:50:28 to 18:50:29 UTC, all rc 0 | restore/*-start*, restore/baseline-start-lock.txt |
| 8 | Cycles c01 to c10 (`run_locked_b18.sh 170 cyc_b18.py N`), one lock hold each | 18:50:47 to 18:59:53 UTC, all rc 0, each ended bound as found | cycles/, cycle ledger below |
| 9 | End baseline (`baseline_b18.sh end`), controller staging removed, census compare | 18:59:58 to 18:59:59 UTC, all rc 0; 45 of 46 equal | restore/*-end*, restore/census-compare.txt, restore/controller-cleanup.txt |
| 10 | Grading: `ana_b17.py cycle` (unchanged) on each capture; `summ_b18.py` | 10 of 10 rc 0; summary rc 0, 0 failed checks | summary/, gates/summ-b18-run.txt |
| 11 | `peer_gap_b17.py` (unchanged) over the ten captures | c01's peer stream ran 4.951 s after the unbind (others 0.002 to 0.181 s) | summary/peer-gap.json |
| 12 | Redaction pass (`redact_b18.py`, B17's private map) and privacy scan | 14 files masked; scan finds no private name, host, interface, identifier, account or tool name; no file over 200 KB. Summary re-run after it: byte-identical | redaction.json |
| 13 | Findings section, commit | Head `480c5e916f8bf711c47e1985ba3efe2b2471bdda`, "Record #645 bench lane B18 on dev 9ef71772: all ten binds at INTERNAL hold the loopback ring", +315 lines in `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` only | the diff |
| 14 | Gates on the head (unpiped, physical path, pinned Markdown interpreter for the five Markdown gates) | all rc 0: docs_check, check_doc_style, gen_toc --check, check_em_dash --base 9ef71772 (315 added lines, 0 findings), check_doc_paths, check_baremetal_only --check, git diff --check | gates/gates.txt |
| 15 | Page tables against the summary tool's tables, and PR-BODY.md's table against the page | 0 mismatches | gates/page-vs-summary.txt |
| 16 | REVIEW READY on #645 | Posted 2026-10-15T19:11:32Z, comment 6200209744, read back (equal but for one trailing newline) | REVIEW-READY.md, review-ready-url.txt, REVIEW-READY.readback.md |
| 17 | Manifest | MANIFEST.sha256 over every packet file but itself | MANIFEST.sha256 |

## Identity gate (step 5)

`identity/identity-verdict.txt`: entity_id `020000fffe000001`, entity name "Milan FPGA 1x1 TDM8", firmware_version "2.96.0", serial "AX7101-0001" (equal to B17's `identity/` records); console `ID=4d494c4e VERSION=00020060`; CRC32 of the 7,512-byte AEM image in QSPI `5ba355eb`; live ENTITY (312 B) and CONFIGURATION (106 B) equal to the QSPI bytes; CLOCK_SOURCE 0 Internal, 1 CRF Clock (STREAM_INPUT 1), 2 Stream Clock (STREAM_INPUT 0), 3 NO_SUCH_DESCRIPTOR; CLOCK_DOMAIN 0 lists 0, 1, 2; GET_CLOCK_SOURCE 0; UART grader PASS 10/10; ADP model `001bc5c1935893e1`. VERSION and AEM CRC are unchanged from dev `5603c353` by design; the flash record (step 6) is the image's identity proof.

## As found (step 7, 18:50:28 UTC)

| Item | As found |
|---|---|
| DUT CLOCK_SOURCE | 0 (INTERNAL) |
| DUT servo (`0x8F8`) | `0x00000020`: state IDLE |
| DUT STREAM_INPUT 0 | **bound** to the reference peer's STREAM_OUTPUT 0, flags `0x0002`, format `0205022001006000` |
| DUT STREAM_INPUT 1 | unbound, format `041060010000bb80` |
| The peer's STREAM_OUTPUT 0 format | `0205022001006000`, equal: the binding rule sets nothing |
| The peer's STREAM_INPUT 0 and 8 | bound to the DUT's AAF and CRF talkers, flags `0x0082` |
| The peer's clock source | 1 |
| DUT maps | STREAM_PORT_INPUT 0: 4 mappings; STREAM_PORT_OUTPUT 0: 8 |
| `SLIP_LB` (`0x8D4`) | `0x00000000`: 0 dups, 0 skips (counters restart at the 18:43 cold boot) |
| `SLIP_TDM` (`0x8D8`) | 0 |
| `RENDER_STAT` (`0x8DC`) | `0x0000020a`: fill 10, converged, rails 0 |
| DUT saved state | image seq 315, 54 records, commits ok 0, failed 0, `pend=0` |

This is B17's probe state: the cycle runner's own start check passed in every cycle.

## Cycle ledger (one row per bind cycle)

Times are seconds from the bind's CONNECT_RX command (B17's time base). "Burst": B17's rule, PDUs more than 20 us late against the post-bind fit, grouped while less than 1 ms apart. "First PDU + 42.7 ms" is the design's firing time of the bind's settle recentre (2,048 ticks); no CSR exposes the recentre on this image, so it is the design's, not observed. Lock windows UTC.

| Cycle | Lock window | Unbind / bind | Polls (first, last s) | `SLIP_LB` dups | Change, grade | First peer PDU | First burst over 20 us (after first PDU + 42.7 ms by) | Bursts to the last poll, peak | delta_ppm | `SLIP_TDM`, CLOCK_SOURCE DUT/peer | Note | Ended bound as found |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| c01 | 18:50:47.3-18:51:39.4 | SUCCESS / SUCCESS, format equal, none set | 80 (-8.00, +31.70) | 0 to 0, 0 skips | none: **held** | 135.267 ms | 4.74 s, 25.7 us (4557.2 ms) | 17, 29.3 us | +0.0009 | 0, 0 to 0 / 1 to 1 | peer stream ran 4.951 s after the unbind | yes |
| c02 | 18:51:51.1-18:52:43.1 | SUCCESS / SUCCESS, format equal, none set | 80 (-8.00, +31.84) | 0 to 0, 0 skips | none: **held** | 25.015 ms | 4.03 s, 25.1 us (3965.7 ms) | 11, 32.0 us | -0.0008 | 0, 0 to 0 / 1 to 1 | 0.037 s | yes |
| c03 | 18:52:43.2-18:53:34.9 | SUCCESS / SUCCESS, format equal, none set | 80 (-8.00, +31.83) | 0 to 0, 0 skips | none: **held** | 165.076 ms | 0.38 s, 25.8 us (172.2 ms) | 9, 28.4 us | +0.0012 | 0, 0 to 0 / 1 to 1 | 0.177 s | yes |
| c04 | 18:53:35.0-18:54:26.7 | SUCCESS / SUCCESS, format equal, none set | 80 (-8.00, +31.78) | 0 to 0, 0 skips | none: **held** | 20.959 ms | 0.44 s, 26.2 us (379.2 ms) | 11, 28.9 us | 0.0000 | 0, 0 to 0 / 1 to 1 | 0.033 s | yes |
| c05 | 18:54:37.8-18:55:29.8 | SUCCESS / SUCCESS, format equal, none set | 80 (-8.00, +31.88) | 0 to 0, 0 skips | none: **held** | 153.259 ms | 2.38 s, 25.7 us (2188.0 ms) | 10, 27.3 us | -0.0004 | 0, 0 to 0 / 1 to 1 | 0.167 s | yes |
| c06 | 18:55:29.9-18:56:21.7 | SUCCESS / SUCCESS, format equal, none set | 80 (-8.00, +31.85) | 0 to 0, 0 skips | none: **held** | 57.238 ms | 2.50 s, 29.0 us (2395.1 ms) | 11, 29.0 us | +0.0005 | 0, 0 to 0 / 1 to 1 | 0.069 s | yes |
| c07 | 18:56:21.8-18:57:13.4 | SUCCESS / SUCCESS, format equal, none set | 80 (-8.00, +31.84) | 0 to 0, 0 skips | none: **held** | 192.267 ms | 2.64 s, 26.8 us (2402.1 ms) | 9, 31.1 us | -0.0009 | 0, 0 to 0 / 1 to 1 | 0.005 s | yes |
| c08 | 18:57:18.7-18:58:10.3 | SUCCESS / SUCCESS, format equal, none set | 80 (-8.00, +31.77) | 0 to 0, 0 skips | none: **held** | 91.662 ms | 0.20 s, 27.6 us (68.6 ms) | 19, 31.5 us | +0.0002 | 0, 0 to 0 / 1 to 1 | 0.102 s | yes |
| c09 | 18:58:10.5-18:59:02.1 | SUCCESS / SUCCESS, format equal, none set | 80 (-8.00, +31.77) | 0 to 0, 0 skips | none: **held** | 170.932 ms | 0.25 s, 24.9 us (32.7 ms) | 13, 28.0 us | +0.0004 | 0, 0 to 0 / 1 to 1 | 0.181 s | yes |
| c10 | 18:59:02.2-18:59:53.9 | SUCCESS / SUCCESS, format equal, none set | 80 (-8.00, +31.70) | 0 to 0, 0 skips | none: **held** | 189.988 ms | 3.26 s, 25.3 us (3023.9 ms) | 11, 31.2 us | +0.0019 | 0, 0 to 0 / 1 to 1 | 0.002 s | yes |

Every cycle: no `SLIP_LB` or `SLIP_TDM` change in any poll (800 polls, 0 unreadable); `MCSRV_STAT` `0x00000020` (IDLE), `AAFM_STAT`, `AAFM_RATE`, `CRF_CTRL` and `CRF_RATE` 0 in every poll; `RENDER_STAT` the only polled word that moved (504 changes: fill 8 to 14, prefill on the unbind, prefill 0 by 0.11 to 0.67 s after the bind, converged by 0.59 to 0.67 s and held, rails 0). No PDU more than 10 us late arrived between the bind and the first burst in any cycle. GET_COUNTERS moved, per cycle: the DUT's STREAM_INPUT 0 TIMESTAMP_VALID and FRAMES_RX restart at the re-bind (end below start); the peer's STREAM_OUTPUT 0 STREAM_START and STREAM_STOP +1 each and FRAMES_TX on; nothing else (`summary/counters.md`). The cumulative counter joins 11 of 11 (start baseline 0 = c01 first; each next first = previous last; c10 last = end baseline 0).

**Verdict against #742's stated behaviour: 10 of 10 held; 0 #743 residual; 0 B17 class (c); 0 other. The ruling's close condition is met.**

## Bench actions (one row per locked action, UTC)

| Time | Action | Result |
|---|---|---|
| 18:50:11-18:50:17 | Identity gate: DUT console reads, UART grader, AECP descriptor walk, ADP | all rc 0; PASS |
| 18:50:28-18:50:29 | Start baseline: DUT console reads, census, counters, controller view (controller staging /tmp/a622 made) | all rc 0 |
| 18:50:47 to 18:59:53 | Cycles c01 to c10, one lock hold each (windows above): unbind and re-bind of the peer's STREAM_OUTPUT 0 to the DUT's STREAM_INPUT 0, formats read (none set), DUT console poll, tap capture on the DUT's link | all rc 0 |
| 18:59:58-18:59:59 | End baseline: DUT reads, census, counters, controller view, staging removed | all rc 0 |

No outlet, JTAG, flash, reload, power cycle, wiring or instrument action; no SoC board access; no USB gadget action; nothing played on the external audio interface. Writes: only the 10 ACMP unbinds and 10 re-binds of the as-found binding (no stream format, clock source, map or register written on either entity). The bench lock was taken for every console, controller and tap action and was free at the end.

## Tool changes

Hashes (SHA-256) as run. Inherited tools are pinned in `tools/ORIGIN-B14.sha256` and `tools/ORIGIN-B15.sha256` (copied from B17).

| Tool | Taken from | Change | SHA-256 |
|---|---|---|---|
| cyc_b18.py (cycle runner) | B17's cyc_b17.py (`12ec02fe...`) | Raw directory /tmp/645-b18/raw, controller staging /tmp/a622, capture name 645-b18-cNN.pcap, a two-line header comment; nothing else | `d41d0480ba17fdedd8ee73d5ee2ae973180bdda1e55a3d814a408790aa4e76e6` (every cycle's `start` event records it) |
| console_poll_b8.py (poller) | B8, via B17 | Unchanged | `1912837a1e4cfd6a1f8b3615b4d26924efbfd430aff239ebd18cd4dd2a67d4f7` (every cycle's `start` event records it) |
| ana_b17.py (grading) | B17 | Unchanged | `299d4f55441e147bf6d27b5b51242d3384157e4905d27f6ed1064398f05f9468` |
| peer_gap_b17.py | B17 | Unchanged | see MANIFEST.sha256 |
| run_locked_b18.sh | B17's run_locked_b17.sh | Environment B18_ENV | see MANIFEST.sha256 |
| identity_b18.sh | B17's identity_b17.sh | Environment B18_ENV, staging /tmp/a622 | see MANIFEST.sha256 |
| baseline_b18.sh | B17's baseline_b17r.sh | Environment B18_ENV, staging /tmp/a622 | see MANIFEST.sha256 |
| redact_b18.py | B17's redact_b17.py | Its own name in the skip list and the record | see MANIFEST.sha256 |
| summ_b18.py | new (B17's summ_b17.py rules: burst rule, round-once, tie check, counter continuity) | Grades each cycle against #742 (held / #743 residual / class (c) / other), the comparison with B17's ten from B17's packet (slip intervals from B17's raw counter logs), counters moved, the counter-log digest | see MANIFEST.sha256 |
| Unchanged copies | B17's packet | b8_ctl.py, avdecc_ro.py, console_read.py, identity_b15.py, census_cmp.py, summ_b17.py (copied, not run) | ORIGIN pins |

## Deviations and decisions

- **The SoC board is not used**, as in B17 under https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6186940255 (the method is unchanged; no tone, no TDM capture). Its console was not touched.
- **The +1 timing.** The poll times a change only to its interval (about 0.6 s), so "within about 3 ms of the first PDU" is not resolvable; TAKEN stated the substitute rule. It was not exercised: no `SLIP_LB` change occurred.
- **The recentre is not observed.** No CSR on this image exposes `recentres_o` (`docs/reference/REGISTER_MAP.md:2064`). The first-PDU + 42.7 ms figure is the design's; "held" rests on `SLIP_LB` alone, as the assignment grades it.
- **c01's capture** holds 814,740 frames, 38,434 to 40,085 more than each of the others: the peer's own AAF stream kept arriving on the DUT's link for 4.951 s after the unbind (B17's c08 showed the same, 4.87 s). The DUT read prefill with fill 0 from the first poll after the unbind and `SLIP_LB` did not move.

## Restore and residuals

`restore/census-compare.txt`: 45 of 46 census entries equal start to end; the other is the DUT's live propagation delay in GET_AVB_INFO, 382 to 388 ns. The DUT's STREAM_INPUT 0 is bound to the peer's STREAM_OUTPUT 0 with flags `0x0002`, as found; CLOCK_SOURCE 0; both maps, every format, the peer's bindings and its clock source 1 as found. `restore/dut-end.txt`: `SLIP_LB` 0, `SLIP_TDM` 0, servo IDLE. Controller staging removed (`restore/controller-cleanup.txt`), no agent left; no capture file left on the tap host (each removed after its copy's hash matched).

Residuals that no permitted command restores: the DUT's saved state advanced through the ten unbinds and binds, image seq 315 to 335, commits ok 0 to 20, failed 0, `pend=0`, `VD_OK`; the peer's STREAM_OUTPUT 0 STREAM_START and STREAM_STOP counters +10 each.

## Raw artifacts (outside the packet)

`RAW-ARTIFACTS.json`: the ten tap captures on the bench host under /tmp/645-b18/pcap/ (871,965,004 bytes in all), each with its SHA-256 equal to the tap host's copy before that copy was removed, and the 30 controller transcripts under /tmp/645-b18/raw/.

## Packet layout

| Path | What |
|---|---|
| HANDOFF.md | This file |
| TAKEN.*, REVIEW-READY.*, *-url.txt | The posts and their readbacks |
| PR-BODY.md | Proposed PR body |
| identity/ | The identity gate: console reads, grader, AECP descriptor walk, ADP, verdict, lock window |
| cycles/cNN/ | Per cycle: `events.jsonl` (the runner's events) and `poll.jsonl` (the raw counter log) |
| summary/ | `cNN.json` per cycle (ana_b17.py), `cycles.json`, `table.md`, `compare.md`, `counters.md`, `peer-gap.json`, `counter-logs.sha256` |
| restore/ | Start and end baselines, census compare, controller cleanup |
| gates/ | The summary run's output and the gate results |
| RAW-ARTIFACTS.json | The raw captures and transcripts outside the packet |
| tools/ | Every tool used or copied |
| redaction.json | Per redacted file: original and retained SHA-256, labels |
| MANIFEST.sha256 | SHA-256 of every packet file except itself |

## Round 2 (2026-10-15, from 21:28 CEST; docs only, no bench access)

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6200530754 ("Round 2 for PR #747"). Reviews: R635-1 NEGATIVE for one MAJOR (https://github.com/kebag-logic/milan-fpga/pull/747#issuecomment-6200475354), R634-1 POSITIVE (https://github.com/kebag-logic/milan-fpga/pull/747#issuecomment-6200518911). Provenance chain: https://github.com/kebag-logic/milan-fpga/pull/747#issuecomment-6200503436, record at evidence commit `bbc53aabb02a1654812ba2eaa1642f5e36e69ce0`, `review-evidence/645-b18-r1/manager-provenance`.
- Start head confirmed `480c5e916f8bf711c47e1985ba3efe2b2471bdda`, equal to origin's `645-b18-bench`. TAKEN not posted again. No bench lock taken; no console, JTAG, power strip, tap or controller access.
- Provenance read-only cross-check (public record at `bbc53aab`): `provenance.json` and `flash.log` give the source head `9ef717727e6fdac11ee7f01672fefae948452343` (tree `8979dd5a`), bitstream SHA-256 `4b5a391af524cb3b490099381c0fd9e3275383fc51c163a75fb78cdb054ffcca` (3,825,992 B), AEM descriptor SHA-256 `4fc8d61582a965fe648abc0c15d0551153ff2b27f202d1fbc8319fbb4bdb396d` (7,512 B), AEM and bitstream write+verify, `FLASH_RC=0`, `POWERCYCLE_RC=0`, BOOTSTS FALLBACK 0 and 1 "Normal configuration", 18:42:24 to 18:44:49 UTC; the cold-boot console lines match the page's boot line. The packet layout at `2e913519` is `review-evidence/645-b18-r1/{MANIFEST.json,author/}`, branch `645-b18-review-evidence`.
- Commit `b3f7a696713a96b42265e08a8c3a04a430b7b5ed` "Link B18's image provenance from the #645 findings page and apply R634-1's suggestions (#645)", findings page only, +35 / -12 in the B18 section:

| Item | Change on the page |
|---|---|
| R635-1-F1 (MAJOR) | "B18: identity and setup" image paragraph: keeps "no read on the device distinguishes the two images"; links the provenance record and the chain comment; lists source, bitstream and AEM hashes, the verified flash-pair with `FLASH_RC=0`, the cold power cycle with `POWERCYCLE_RC=0` and no fallback, the boot line, and that the identity reads (from 18:50:11 UTC) came after that boot with no flash or power cycle before the last cycle's end at 18:59:53 UTC |
| R634-1-S1 | "B18: the binds": one clause, c01 and c10's last poll 0.05 s short of B17's shortest (+31.75 s) from poll timing, the counter cumulative over that tail |
| R634-1-S2 | "the design's earliest firing time" in the method, the bursts paragraph and the limits |
| R634-1-S3 | The intro names `review-evidence/645-b18-r1/author` on branch `645-b18-review-evidence`, commit `2e913519`, as B17's section does |

- No figure, grade, table cell or other document changed. A private-name scan of the added lines found nothing.
- Gates at `b3f7a696`, all rc 0, unpiped, physical /data path, Markdown gates with the pinned environment (`gates/gates-r2.txt`): docs_check.py, check_doc_style.py, gen_toc.py --check, check_em_dash.py --base 9ef71772 (338 added lines, 0 findings), check_doc_paths.py, check_baremetal_only.py --check, git diff --check 9ef71772 HEAD.
- PR-BODY.md: the Image bullet now cites the provenance record; the Limits line says "earliest firing time"; a "Round 2" section is appended. The manager's RS1 counter sentence is kept as is.
- Not pushed. REVIEW READY (round 2) posted on #645 at 2026-10-15 ~21:40 CEST: https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6200622931 (REVIEW-READY-r2.md, review-ready-r2-url.txt, REVIEW-READY-r2.readback.md; equal but for one trailing newline). Lane stopped after it.
