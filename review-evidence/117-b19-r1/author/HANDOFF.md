# [A624] Bench lane B19 handoff

Refs #117 (boxes 1 to 3, box 4's protocol rows), Refs #621 (item 3), Refs #387 (item 4).

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-6207451080
- Image: dev `9ef71772` as installed (flash 2026-10-15 18:44 UTC). Not flashed, never JTAG-reloaded.
- Branch: `117-b19-bench` from dev `734eb780dc93896a5961cd95180f79475a401650`, lane worktree on the physical /data path. Findings docs only. Not pushed; no PR.
- Packet: this directory. Large raw captures stay under /tmp/a624/raw (listed in RAW-ARTIFACTS.json); private endpoints under /tmp/a624/priv (not in the packet).

## State

**DONE: REVIEW READY posted** (https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-6208250865; REVIEW-READY.md, review-ready-url.txt, REVIEW-READY.readback.md, equal but for one trailing newline). Bench done 04:31Z, restore read back, bench lock free (non-blocking flock rc 0). Head `18b98bbcecf478b903610a07667f232d944d6feb`, one commit on dev `734eb780`, one-line subject, no body, no trailers; two findings pages only (+425 lines). All gates rc 0 (gates/gates.txt). Not pushed; no PR (PR-BODY.md holds the body). Posted on #117: TAKEN and REVIEW READY only; no existing comment edited or deleted.

| Item | Verdict |
|---|---|
| Identity gate | PASS 11/11 (and again at the end) |
| Box 1 first reach / retention, cadence, turnaround, no daemon | PASS / PASS |
| Box 2, six OUT4 cycles | PASS 6/6, 0.47-1.77 s against 5 s; one stream restart per bound return |
| Box 3, steady state and transitions | PASS |
| Box 4 counters-probe parity / per-AVTPDU / three enumerations | PASS / PASS / PASS (0 DUT complaints; 2 per run name the peer) |
| #621 item 3 | PASS 10/10 edges, no asCapable loss |
| #387 item 4 (wire and counters) | PASS 10/10; render re-base count carried by simulation (decision) |

## Step ledger (bench times UTC)

| Step | What | Result | Evidence |
|---|---|---|---|
| 0 | Context load: #117, #621, #387 (bodies, [A10] comments, owner decisions), the five docs, packets B1, B18, A375, A200, A202, A373 | Read | this file |
| 1 | Tools copied, origin pins | Done | tools/ORIGIN.sha256 |
| 2 | TAKEN on #117 | Posted 03:36Z, comment 6207516834, read back (equal but for one trailing newline) | TAKEN.md, taken-url.txt, TAKEN.readback.md |
| 3 | Identity gate (B18 method) | PASS 11/11, 03:37:20-03:37:26Z | identity/ |
| 4 | As-found baseline | 03:37:41-03:37:44Z: outlets all ON; DUT SI0 bound to peer SO0, peer SI0 and SI8 bound to DUT SO0 and SO1 (flags 0x0082); DUT clock source 0, peer clock source 1 (= its CRF input 8) | restore/*-start* |
| 5 | Tap interface identification (4 s on each tap interface) | DUT link on the first tap interface; the second is on the peer's link and was not used for any measurement | private (host names) |
| 6 | Dry run (30 s observe, no power) | rc 0 | bench/dryrun |
| 7 | First reach: OUT0 off 11.19 s, on, once | rc 0; boot line captured; console polling after the boot failed (runner defect), see Deviations | firstreach/ |
| 8 | Retention, cadence, turnaround (300 s observe) | 1200/1200 console samples healthy; 300/300 AECP asCapable; cadences in 30 %; DUT turnaround <= 13.4 us | bench/retention |
| 9 | OUT4 cycles 1-3 with the CRF binding | all RECOVERED | bench/cycle01-03 |
| 10 | CRF pair unbound (04:00:16Z), cycles 4-6, rebound (04:06:49Z, flags 0x0082, locked) | all RECOVERED | bench/crf-binding, bench/cycle04-06 |
| 11 | Box 3 correlation, six cycles (DUT-PHC time base) | every CSR edge brackets its wire cause; first CRF `tu=1` inside the CSR `tu` bracket in cycles 1-3 | bench/cycleNN/correlation.json |
| 12 | Reference gPTP implementation 4.4 built on the controller host in /tmp/a624 (hash-checked tarball, auth backends off) | ptp4l and phc_ctl byte-identical to lane B1's | gm/ |
| 13 | Controller host found state (04:10:25Z) | no gPTP daemon; timestamping tx 0 / rx 0; PHC freq 0 ppb, realtime minus PHC 20.150 s | gm/host-original-state.txt |
| 14 | Software-GM runs gm01-gm05 (04:11-04:25Z), offset +10 ms, priority1 240 for 50 s | 10 of 10 edges PASS; gm03's closing clock read failed once (SSH), outlets read by hand, retry added | bench/gm01-05, summary/gm-steps.* |
| 15 | Box 4: counters probe on DUT and peer, three headless enumerations (04:27:04-04:27:58Z) | probe transcripts identical, CLEAN, 0 complaints; enumerations IEEE17221+MILAN, 42 descriptors, 0 DUT complaints (2 per run name the peer) | box4/ |
| 16 | Restore: controller host clock and timestamping (04:30:10Z), end baseline (04:30:45Z), identity and grader (04:30:48Z), controller staging removed | freq 0, tx 0/rx 0, PHC 4.5 us from its found trajectory; census 41/46 equal; outlets all ON; identity PASS, grader 10/10 | restore/, identity-end/ |
| 17 | Analyses and page tables (no bench access) | fr_analyze, ret_analyze, a624_analyze, corr_analyze, avtpdu_parity, gm_summary, box4_summarize, summ_b19; DUT listener FRAMES_RX lag checked across 26 reads (167 to 7,925 PDUs, bounded, the coalesced interval publication) | firstreach/, bench/*/, summary/, box4/ |
| 18 | Findings sections, commit `18b98bbc` | 117 page +261, 387 page +164, Contents entries via gen_toc | the diff |
| 19 | Gates at the head (unpiped, physical path, pinned Markdown interpreter) | 11 commands, all rc 0 | gates/ |
| 20 | REVIEW READY on #117 | posted 2026-10-16, comment 6208250865, read back | REVIEW-READY.* |

## Cycle ledger (box 2/3, one row per OUT4 cycle)

Seconds after the OUT4 off command. Recovery: the switch's first post-boot Announce to all-good, the first console sample from which GM = switch, sync 1, asCapable 1 and `tu` 0 hold, with console samples placed on the tap clock through the DUT PHC (corr_analyze.py; these are the page's figures). Lane B1's coarser definition (sample end on the build-box clock, analysis.json `gptp_recovery_s`) gives 1.55, 0.69, 1.82, 0.79, 0.56 and 0.54 s; both are far inside 5 s.

| Cycle | CRF bound | Off for | Switch first Announce | DUT all-good | Recovery | 5 s bound | DUT CRF STREAM_START + | DUT GM_CHANGED + | DUT LINK_UP/DOWN + | Check |
|---|---|---:|---:|---:|---:|---|---:|---:|---|---|
| 1 | yes | 21.14 | 40.26 | 41.75 | **1.49** | PASS | 1 | 2 | 1/1 | RECOVERED |
| 2 | yes | 21.18 | 40.37 | 41.00 | **0.63** | PASS | 1 | 2 | 1/1 | RECOVERED |
| 3 | yes | 21.09 | 40.23 | 42.00 | **1.77** | PASS | 1 | 2 | 1/1 | RECOVERED |
| 4 | no | 21.11 | 40.27 | 41.01 | **0.75** | PASS | - | 2 | 1/1 | RECOVERED |
| 5 | no | 21.12 | 40.25 | 40.75 | **0.50** | PASS | - | 2 | 1/1 | RECOVERED |
| 6 | no | 21.18 | 40.26 | 40.74 | **0.47** | PASS | - | 2 | 1/1 | RECOVERED |

## GM-step ledger (#621 item 3, #387 item 4, one row per edge)

| Run | Edge | DUT PHC step (wire) | `tu` rises console / CRF | asCapable 0 samples | GM_CHANGED | `mr` changes | MEDIA_RESET DUT AAF/CRF talker, peer CRF listener | MEDIA_UNLOCKED DUT/peer CRF/peer AAF | Grade |
|---|---|---|---|---:|---:|---:|---|---|---|
| 1 | takeover | +9.987 ms | 1 / 1 | 0 | +1 | 0 | +0/+0/+0 | +0/+0/+0 | PASS |
| 1 | release | -10.003 ms | 1 / 1 | 0 | +1 | 0 | +0/+0/+0 | +0/+0/+0 | PASS |
| 2 | takeover | +9.987 ms | 1 / 1 | 0 | +1 | 0 | +0/+0/+0 | +0/+0/+0 | PASS |
| 2 | release | -10.004 ms | 1 / 1 | 0 | +1 | 0 | +0/+0/+0 | +0/+0/+0 | PASS |
| 3 | takeover | +9.987 ms | 1 / 1 | 0 | +1 | 0 | +0/+0/+0 | +0/+0/+0 | PASS |
| 3 | release | -10.004 ms | 1 / 1 | 0 | +1 | 0 | +0/+0/+0 | +0/+0/+0 | PASS |
| 4 | takeover | +9.987 ms | 1 / 1 | 0 | +1 | 0 | +0/+0/+0 | +0/+0/+0 | PASS |
| 4 | release | -10.005 ms | 1 / 1 | 0 | +1 | 0 | +0/+0/+0 | +0/+0/+0 | PASS |
| 5 | takeover | +9.987 ms | 1 / 1 | 0 | +1 | 0 | +0/+0/+0 | +0/+0/+0 | PASS |
| 5 | release | -10.004 ms | 1 / 1 | 0 | +1 | 0 | +0/+0/+0 | +0/+0/+0 | PASS |

## Bench actions (one row per locked action)

Build-box UTC (1.50 s behind the NTP hosts). Every console, power-strip, tap and controller-AVB action took `flock /tmp/milan-bench.lock` for its own window only.

| Window (UTC) | Action | Result |
|---|---|---|
| 03:33:30-03:33:32 | host reachability and daemon check (bench hosts) | no gPTP daemon |
| 03:37:20-03:37:26 | identity gate | PASS 11/11 |
| 03:37:41-03:37:44 | start baseline (console, census, counters, outlets) | all rc 0 |
| 03:37:58-03:37:58 | the peer's clock-source descriptors, read-only | source 1 = its input 8 |
| 03:38:45-03:38:55 | 4 s capture on each tap interface (identification) | DUT link found |
| 03:41:14-03:41:49 | dry run, 30 s observe | rc 0 |
| 03:42:05-03:44:10 | first reach: OUT0 off 03:42:18.25, on 03:42:29.45 | rc 0 |
| 03:44:42 | post-boot console read | healthy, CLKV_TUCNT 10 |
| 03:46:42-03:51:48 | retention, 300 s | rc 0 |
| 03:52:56-04:00:09 | cycles 1-3 (one window each) | all rc 0, RECOVERED |
| 04:00:16-04:00:17 | CRF pair unbind | rc 0 |
| 04:00:28-04:06:44 | cycles 4-6 | all rc 0, RECOVERED |
| 04:06:49-04:06:55 | CRF pair rebind and snapshot | rc 0, locked |
| 04:10:25-04:10:45 | controller host found state, read-only | recorded |
| 04:11:00-04:25:32 | software-GM runs 1-5 (one window each) | runs 1, 2, 4, 5 rc 0; run 3 rc 1 on its closing clock read only |
| 04:19:51 | outlet read after run 3 | all ON |
| 04:27:04-04:27:58 | counters probe x2, enumerations x3 | all rc 0 |
| 04:30:10-04:30:31 | controller host clock and timestamping restore | rc 0 |
| 04:30:45-04:30:47 | end baseline, controller staging removed | all rc 0 |
| 04:30:48-04:30:53 | identity gate and grader | PASS |

## Deviations and decisions

- **First-reach console.** The runner's boot logger went back to passive reading right after the boot prompt (a loop re-entered its passive branch), so no CSR poll ran after the boot. OUT0 may be switched once, so the cycle was not repeated. The DUT end's asCapable comes from the wire (its completed Pdelay exchanges, its PHC step) and the controller's first AECP answer (9.955 s after on, already asCapable). The defect is fixed in `tools/a624_action.py`; the as-run copy is `tools/a624_action_firstreach_asrun.py`.
- **Second tap interface.** The capture host now has two tap interfaces; a 4 s capture on each identified the DUT link. The second is on the reference peer's link, which no earlier operator used, so it was not used for any measurement.
- **CRF binding for the no-CRF cycles.** As found, the peer's CRF input 8 is bound to the DUT's CRF output and is the peer's selected clock source. Cycles 1-3 ran with it; it was unbound for cycles 4-6 and rebound after cycle 6 (same flags; a new MAAP destination address).
- **GM-step streams.** The as-found streams were used: the peer follows the DUT's CRF, so lane B1's reverse CRF binding with CRF selection on the DUT would close a media-clock loop and was not made; the DUT's CRF servo stayed idle. Grades are the assignment's six; no servo grade.
- **Run 3 closing clock read.** The runner's after-action clock read of the capture server failed once (SSH). The measurement had completed; the outlet read and the packet copy were done by hand; `a624_action.py` gained a retry (`9da7bbaf...` to `433d6fb7...`) before runs 4 and 5.
- **Runner versions.** `a624_action_firstreach_asrun.py` (`5b690477...`): dry run and first reach. `a624_action_cycles_gm01-03_asrun.py` (`9da7bbaf...`): retention, cycles 1-6, GM runs 1-3. `a624_action.py` (`433d6fb7...`): GM runs 4-5.
- **Enumeration complaints.** Each run logged two complaints, both naming the reference peer's entity (StreamInfoFlag bit 24 reserved). None names the DUT; graded on the DUT.
- **Time base for box 3.** Console samples are placed on the tap clock through the DUT PHC (TAI_NS against the t3 of the DUT's Pdelay responses on the wire), not through the cross-host offsets (whose error measured 24 to 52 ms per cycle).

## Restore

| Item | Start (03:37Z) | End (04:30Z) |
|---|---|---|
| Outlets | OUT0-OUT6 ON | OUT0-OUT6 ON (OUT0 switched once, OUT4 six times) |
| DUT STREAM_INPUT 0 | bound to the peer's STREAM_OUTPUT 0, flags 0x0002 | same |
| Peer STREAM_INPUT 0 and 8 | bound to the DUT's STREAM_OUTPUT 0 and 1, flags 0x0082 | same; destination MACs 91e0f000915b/915c instead of fd56/fd57 |
| DUT / peer clock source | 0 / 1 | 0 / 1 |
| Formats, maps, configuration, sampling rate | as read | equal |
| Controller host | no daemon, timestamping tx 0 / rx 0, PHC freq 0 ppb | same; PHC within 4.5 us of its found trajectory at restore |
| DUT NVM | image seq 335, VD_OK, pend 0 | same (commits counter restarted at the cold boot) |

Residuals no permitted command clears: the DUT's MAAP-claimed destination addresses (new claim at the cold boot; `MAAP_CTRL` seed offset 0xfd56 to 0x915b); `SLIP_LB` dups read 0xFFFF (saturated; restarted at the cold boot, not polled during the runs); counters that moved (GPTP_GM_CHANGED 0 to 22, LINK_UP/DOWN 1/0 to 7/6, stream starts and stops, AS_PATH_GEN 1 to 7).

## Tools (SHA-256 as run)

Origins of copied tools: tools/ORIGIN.sha256. New or adapted:

| Tool | From | Change |
|---|---|---|
| a624_action.py (+ two as-run copies) | lane B1's b1_action.py | paths; tap 160 octets with the AAF-only drop filter; PAIRS; dutcycle kind with the boot logger and the once-only OUT0 guard; outlet checks per switched outlet; clock-read retry |
| a624_controller.py | lane B1's a438_controller.py | the lane's stream set, crf bind/unbind, watch pairs |
| a624_analyze.py | lane B1's b1_analyze.py | the lane's counters, A202-style cycle edges |
| corr_analyze.py, fr_analyze.py, ret_analyze.py, avtpdu_parity.py, gm_summary.py, summ_b19.py, cyc_check.py, box4_summarize.py | new (box4_summarize from A373's summarize.py) | analyses, no bench access |
| identity_b19.sh, baseline_b19.sh, run_locked_b19.sh, cycles_b19.sh, gmruns_b19.sh | lanes B18 and B1 | environment and staging; outlet read in the baseline |
| a624_build_probe.py, a624_enumerate_once.py | A373 | staging path only |
| phc_restore_b19.py | lane B1's phc_restore.py | this lane's found readings, frequency 0 |

All other hashes: MANIFEST.sha256.

## Packet layout

| Path | What |
|---|---|
| HANDOFF.md, PR-BODY.md | this file; the proposed PR body |
| TAKEN.*, REVIEW-READY.*, *-url.txt | the two posts and their readbacks |
| identity/, identity-end/ | identity gate at the start and the end; image-to-base diff |
| firstreach/ | first-reach analysis and the post-boot console read |
| bench/<action>/ | per action: events, results, small raw files (<= 200 KB), analysis.json, check.txt, correlation.json (cycles), retention.json and pdelay outputs (retention) |
| bench/crf-binding/ | the CRF unbind and rebind |
| gm/ | grandmaster and alignment configurations, the controller host's found state |
| box4/ | probe transcripts, enumeration logs, DUT entity dumps, build provenance, summary |
| restore/ | start and end baselines, census comparison, controller host restore and cleanup, capture server check |
| summary/ | cycle, correlation and GM-step tables |
| gates/ | gate outputs and gates.txt |
| tools/ | every script used, with ORIGIN.sha256 |
| RAW-ARTIFACTS.json | all 151 raw files (108,011,178 bytes) by path, size and SHA-256; the 54 over 200 KB stay under /tmp/a624/raw |
| MANIFEST.sha256 | SHA-256 of every packet file except itself |
