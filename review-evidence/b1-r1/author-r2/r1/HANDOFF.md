[A438] Bench lane B1 handoff

Refs #599 (acceptance 4). Refs #394 (acceptance 2, e1 only). Refs #387 (acceptance 4).

Assignment: https://github.com/kebag-logic/milan-fpga/issues/599#issuecomment-5884216527
TAKEN: https://github.com/kebag-logic/milan-fpga/issues/599#issuecomment-5884282801
REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/599#issuecomment-5885028407 (REVIEW-READY.md is the posted text; REVIEW-READY.readback.md the API readback)
Branch: b1-bench-0929 from dev 13eda870d1a6cf3f946fc228a98862366b08d102 (worktree $LANES/b1-bench-0929).
Packet: this directory. Large raw captures stay under /tmp/b1-a438/raw; RAW-ARTIFACTS.json lists all 213 by relative path, size and SHA-256 (176,644,961 bytes).

## State

REVIEW READY. Commit `f9eab5bf55ca4471e6e48ae3d38018d7e804505b` (one commit on 13eda870, one-line subject, no body, no trailers), local only, not pushed. Worktree clean.
Bench work complete 06:24Z; every outlet, binding, clock source and host restored and proven; bench lock free (verified with a non-blocking flock).
No DUT flash, reset, reboot or power cycle. Only OUT4 was switched: 11 times off and on (the link-drop proof plus ten cycles).

Changed files (docs only):
- `docs/findings/599_394_E1_LINK_CYCLES.md` (#599 acceptance 4, #394 acceptance 2)
- `docs/findings/387_SOFTWARE_GM_STEP.md` (#387 acceptance 4)

## Verdicts (operator measurements, not review verdicts)

| Acceptance | Verdict |
|---|---|
| #599 acc. 4, first half (does a switch cycle drop the DUT PHY link?) | PASS, it drops; no owner decision needed |
| #599 acc. 4 (+1/+1 per cycle) | PASS, 10/10 |
| #394 acc. 2 (e1 only) | PASS, 10/10; restart time recorded (not a #75 verdict) |
| #387 acc. 4 | PASS with one recorded deviation: every PHC step is followed by a 2.0 s asCapable loss (proposed follow-up issue) |

## Step ledger

| Step | What | Result | Evidence |
|---|---|---|---|
| 1 | Identity gate | PASS 05:31Z: VERSION 00020060; ROM acad92b9, QSPI payload d84bce7b (seed eto of dev 13eda870), AEM 93742dd2; ENTITY/CONFIGURATION exact match to aem_desc.bin, entity 020000fffe000001; grader 10/10 | identity/ |
| 2 | #599 acc. 4 first half: BMSR during one OUT4 cycle | PASS (link drops) 05:36-05:38Z: firmware BMSR publication MAC_STATUS 0x0d->0x00 between +2.31 and +2.56 s after OFF, back 0x0d between +37.07 and +37.32 s; link_status CSR identical; LINKG_STAT 0x83->0x03 at +3.84 s; LINK_UP/DOWN 1/0 -> 2/1. OUT4 re-proof: far frames stop at +0.96 s, none from +5 s to ON, controller carrier down +1.39 s, DUT console max gap 0.250 s, RST_EPOCH 1, peer ADP index 87336->87354, other outlets unchanged. gPTP recovery 1.832 s | bench/bmsr-proof/ |
| 3 | Ten OUT4 cycles (#599 acc. 4, #394 acc. 2 e1) | PASS 05:42-06:02Z: every cycle LINK_DOWN/LINK_UP +1/+1 (DUT 2/1 -> 12/11), MAC_STATUS 0x0d->0x00->0x0d; gPTP recovery 0.544-1.786 s; both CRF streams and bindings recovered, no re-bind, no reboot; RST_EPOCH 1 | bench/cycle01..10/, table below |
| 4 | #387 acc. 4: software GM takeover, five runs | Measured 06:05-06:21Z: 5 runs x 2 edges; DUT PHC step +9.987/+9.988 ms at takeover, -10.003..-10.005 ms at release (wire); no mr toggle, MEDIA_RESET +0, both listeners never unlocked, servo LOCKED throughout, CRF gap max 2 ms; steady 3.00-4.53 s after each step; asCapable lost 2.0 s after every step | bench/gm01..05/, table below |
| 5 | Restore everything, prove it | PASS 06:22-06:24Z: switch GM (console, wire, controller); both pairs unbound first attempt, 18/18 states conn 0; DUT clock source 0; census 53/53 equal (peer reserved half-word and DUT pdelay masked); no CRF on 20 s final tap; grader 10/10; outlets as found; controller PHC freq/trajectory and ts config restored, temp files removed; tap module unloaded, temp build removed | restore/, capture/, bench/final/ |
| 6 | Findings pages, gates, commit | PASS: all gate commands rc 0 at f9eab5bf | gates/ |

## Per-cycle table (step 3)

| Cycle | OFF (s) | LINK_DOWN / LINK_UP delta | MAC_STATUS down / up | gPTP recovery (s) | Streams / bindings | Result |
|---|---|---|---|---|---|---|
| 01 | 20.90 | +1 / +1 (2/1 -> 3/2) | 1.812-2.062 / 36.824-37.074 | 0.544 | both recovered / held | RECOVERED |
| 02 | 20.97 | +1 / +1 (3/2 -> 4/3) | 2.061-2.311 / 36.823-37.074 | 1.555 | both recovered / held | RECOVERED |
| 03 | 20.88 | +1 / +1 (4/3 -> 5/4) | 2.312-2.562 / 36.828-37.078 | 1.704 | both recovered / held | RECOVERED |
| 04 | 20.86 | +1 / +1 (5/4 -> 6/5) | 2.061-2.311 / 37.073-37.323 | 1.513 | both recovered / held | RECOVERED |
| 05 | 20.86 | +1 / +1 (6/5 -> 7/6) | 1.811-2.061 / 36.823-37.073 | 0.72 | both recovered / held | RECOVERED |
| 06 | 21.06 | +1 / +1 (7/6 -> 8/7) | 2.312-2.562 / 39.102-39.352 | 1.75 | both recovered / held | RECOVERED |
| 07 | 20.88 | +1 / +1 (8/7 -> 9/8) | 1.813-2.063 / 36.587-36.838 | 1.463 | both recovered / held | RECOVERED |
| 08 | 20.85 | +1 / +1 (9/8 -> 10/9) | 1.811-2.061 / 37.075-37.325 | 1.523 | both recovered / held | RECOVERED |
| 09 | 20.87 | +1 / +1 (10/9 -> 11/10) | 2.311-2.561 / 36.822-37.072 | 1.427 | both recovered / held | RECOVERED |
| 10 | 21.05 | +1 / +1 (11/10 -> 12/11) | 2.061-2.312 / 36.824-37.074 | 1.786 | both recovered / held | RECOVERED |

Counters (DUT, bound baseline -> after cycle 10): LINK_UP/LINK_DOWN 2/1 -> 12/11; GPTP_GM_CHANGED 2 -> 22; CRF input MEDIA_LOCKED/UNLOCKED 1/0 -> 11/10; CRF output STREAM_START/STOP 1/0 -> 11/10; CLOCK_DOMAIN 2/1 -> 12/11. Reference peer LINK_UP/LINK_DOWN 1/0 flat, GPTP_GM_CHANGED 40 -> 60.

## Per-step table (step 4)

Times: seconds after the software-GM start. Step: DUT PHC, from its Pdelay_Resp t2 on the tap.

| Run | Edge | DUT PHC step | GM time step | tu set / steady clear | Step to steady (s) | tu episodes | asCapable lost | DUT / peer mr changes | MEDIA_RESET talker / listener | DUT / peer MEDIA_UNLOCKED | Servo; discards |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | takeover | +9.988 ms | +9.994 ms | 4.05 / 7.34 | 3.25-3.54 | 3 | 4.55-6.55 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 10 to 13 |
| 1 | release | -10.004 ms | -9.997 ms | 50.82 / 54.10 | 3.25-3.53 | 3 | 51.57-53.57 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 13 to 14 |
| 2 | takeover | +9.988 ms | +9.995 ms | 3.78 / 7.06 | 3.25-3.53 | 2 | 4.28-6.28 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 14 to 17 |
| 2 | release | -10.005 ms | -9.998 ms | 50.55 / 54.08 | 3.50-3.78 | 3 | 51.30-53.30 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 17 to 19 |
| 3 | takeover | +9.988 ms | +9.995 ms | 3.78 / 8.06 | 4.25-4.53 | 3 | 4.78-6.78 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 19 to 20 |
| 3 | release | -10.004 ms | -9.996 ms | 50.59 / 54.12 | 3.50-3.78 | 3 | 50.84-52.84 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 20 to 21 |
| 4 | takeover | +9.987 ms | +9.995 ms | 3.78 / 6.81 | 3.00-3.28 | 2 | 4.53-6.53 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 21 to 24 |
| 4 | release | -10.004 ms | -9.997 ms | 50.80 / 53.83 | 3.00-3.28 | 3 | 51.55-53.55 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 24 to 25 |
| 5 | takeover | +9.987 ms | +9.995 ms | 3.78 / 7.07 | 3.25-3.54 | 3 | 4.03-6.03 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 25 to 26 |
| 5 | release | -10.003 ms | -9.996 ms | 50.60 / 54.14 | 3.50-3.78 | 3 | 51.11-53.11 | 0 / 0 | +0 / +0 | +0 / +0 | LOCKED; 26 to 27 |

## Gates at f9eab5bf (all rc 0, foreground, not piped; gates/gates.txt)

1. md-venv python scripts/docs_check.py: 0 findings, 176 md + 938 scrubbed
2. md-venv python scripts/check_doc_style.py: OK (22 current documents)
3. md-venv python scripts/gen_toc.py --check: OK (118 pages)
4. md-venv python scripts/check_em_dash.py --base 13eda870: 0 findings over 671 added lines in 2 pages
5. md-venv python scripts/check_doc_paths.py: OK (854 paths)
6. python3 scripts/ci_scope.py --selftest: PASS
7. python3 scripts/check_baremetal_only.py --check: OK, 0 findings (the script requires a mode; --check is the tree scan)
8. python3 scripts/check_feature_status.py --self-test: 46/46, 0 findings
9. git diff --check: clean; also git diff --check 13eda870..HEAD: clean

The first commit (f98994d2, never pushed) failed gate 7 on retired-stack vocabulary (the implementation's program names and "kernel"); the pages were reworded and the commit amended to f9eab5bf.

## Deviations and incidents

- As found (05:33Z): OUT1 and OUT3 OFF, the others ON (PR #600 found all seven ON). Restored to this state.
- As found: the reference peer is in configuration 1 at 48 kHz (PR #600 found configuration 0 at 96 kHz); its CRF input 8 and output 2 have format 041060010000bb80 in configuration 1. Not changed by this lane.
- The tap had no capture interface on the capture host's current OS release (same state as PR #600's preflight). Temporary rebuild of the same three hash-identical inputs in a temporary directory on the capture host, module loaded 05:34Z, unloaded and removed 06:24Z. capture/.
- The software GM: the reference gPTP implementation 4.4 (buildroot-pinned tarball, sha256 61757bc0...) built in a temporary directory on the controller host with the auth backends disabled by a make-variable override (the host's crypto library API is newer); removed after the runs. The first alignment config was rejected (slaveOnly with gmCapable 0) before any socket or PHC action; gmCapable 0 alone was used.
- The alignment port briefly held a clockClass-255 master role for ~2 s before receiving the switch's Announce; the DUT and peer GPTP_GM_CHANGED did not move (22 and 60 before and after the standalone test).
- The controller host had two stale control-socket files from an earlier, unknown run of the same implementation (it logged removing them at its first start; its rejected first start exits before creating sockets). Not recreated; no daemon ran before or after.
- Console step detector flagged one delayed console sample in gm04 (+2.726/-2.790 ms at +97.6..98.1 s, cancelling, no wire jump, no tu): console timing artifact, not a PHC step.
- b1_action.py changed once between the cycles and the GM runs, only in its GM-prep convergence parse; the recorded hash is the final one. All analyses were re-run with the final analyzer.

## Open questions for the manager

1. Proposed follow-up issue (not filed; this lane may only post on #599): every PHC step of the locked servo is followed 0.22-0.97 s later by a 2.0 s asCapable loss (published peer delay 0 ns at takeovers, 4,039-4,701 ns at releases), adding one or two `tu` episodes, +2 GPTP_GM_CHANGED and +2 CLOCK_DOMAIN LOCKED/UNLOCKED per step. Media was unaffected. Consistent with a peer-delay exchange computed across the step; mechanism not established.
2. The render re-base tally of #387's contract is not observable on this bench (no AAF stream bound; no CSR).
3. The DUT link-up-to-first-PDU times (5.74-14.84 s) exceed #75's 1 s, but they start at link-up, not CONNECT_RX; recorded only.

## Packet layout

| Path | What |
|---|---|
| TAKEN.md | posted TAKEN text |
| identity/ | console CRC readback, grader, AECP descriptor comparison, expected CRCs, csr.csv, lock windows |
| capture/ | temporary capture-driver build and cleanup records (instrument name masked) |
| bench/<action>/ | per action: events, results, small raw files (<= 200 KB), analysis.json, raw-artifacts.json, check.txt |
| gm/ | GM and alignment configs, host original state, standalone alignment test, build log |
| restore/ | census comparison, final grader and console, outlets start/end, controller PHC restore and cleanup |
| summary/ | cycles.json, steps.json, tables and the page tables as generated |
| tools/ | every script used; ORIGIN-A375.sha256 pins the reused PR #600 tools as copied |
| gates/ | gate outputs and gates.txt |
| RAW-ARTIFACTS.json | all raw files kept outside the packet |
| PR-BODY.md | proposed PR body |
| MANIFEST.sha256 | SHA-256 of every packet file except itself |
