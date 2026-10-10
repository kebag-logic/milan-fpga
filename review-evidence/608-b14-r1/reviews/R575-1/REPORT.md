[R575] NEGATIVE - exact head 6ec1a3a9a827575a84fb60d42ad3b085ecb70f19

# R575-1: external independent review of PR #709 (issue #608, B14 bench on dev 5603c353)

- Head `6ec1a3a9a827575a84fb60d42ad3b085ecb70f19`, tree `efa7f95f688d7e3380e0c3b18fa514f6360e803e`, source base dev `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.
- Diff: one new file, `docs/findings/B14_BENCH_5603C353.md` (619 lines, three one-line commits). Gitlinks unchanged from the base.
- Verdict: **NEGATIVE**. There are four MINOR findings: three recorded facts disagree with the archived records, and one register-contract statement is wrong. Six RESIDUE wording fixes and one SUGGESTION follow. No BLOCKER or MAJOR.
- Every result the page grades (items 2, 3, 4, 5, 6-link, 7-announce, 8) is reproduced from the archived packet. None of the findings changes a PASS, a NOT RUN or a count of cycles, switches or starts.

## Reconstruction (public state only)

1. AGENTS.md and CONTRIBUTING.md (sections 2, 3, 6: the bench suite token, naming bench equipment by role, the privacy scrub, the em-dash rule), then docs/README.md and docs/findings/README.md.
2. Issue #608: the body, the item-3 ruling 5885808887 and its correction 5886425487, the Mark II note 6009639876, the B14 assignment 6085135051, the two STOPs (6088157558 and 6093984746), the ruling 6094000332 to continue without the SoC board, and REVIEW READY 6095837334.
3. The referenced issues' acceptance: #645 (acceptance 3), #647 (bench item), #667, #682 (acceptance 5), #658, #686 (acceptance 4), #691.
4. Interface authorities at the head: `docs/design/MEDIA_CLOCK_FOLLOWING.md` (Settle recentre, The declared transient), `docs/reference/REGISTER_MAP.md` (0x200 RMON, 0x8D4 `SLIP_LB`, 0x8DC `RENDER_STAT`), `docs/design/MAAP_FABRIC.md` (Annex B contract), `hdl/milan/milan_datapath.sv:6603-6650` (settle arm and fire), `hdl/common/eth_event_counter/ethernet_events.svh` (the RMON lane order), and the prior findings 608_75_WITHDRAWAL_AND_RESTART.md and 667_TALKER_START_BENCH.md.
5. `git diff 5603c353..6ec1a3a9` and the three commits.
6. The archived packet `review-evidence/608-b14-r1` at commit `c848925d2e88a98e7f31b663e5dd4f342b765487`, fetched by SHA into a disposable tree.
   - Its `MANIFEST.json` verifies: 2,356 of 2,356 files match `published_sha256`, 422 of them redacted.
   - The author's `MANIFEST.sha256` fails 16 files. All 16 are redacted files whose archive `original_sha256` equals the author hash (`receipts/packet_manifest_check.txt`, `receipts/packet_manifest_json_check.txt`).
7. PR #709 comments and reviews, read only after this pass. There are two review-start notices and no prior findings, so there is nothing to resolve or retain.

## Findings

### R575-1-F1 MINOR: the DUT Talker Advertise withdrawal times are measured from the wrong event

- Lenses: Conformance, Tests, Docs.
- Where: `docs/findings/B14_BENCH_5603C353.md:190`.
- The page says cycles 2 and 42 show the DUT withdrawing its Talker Advertise "0.104 and 0.328 s after the bridge's `Lv`".
- Evidence: `author/item3/cycles/cycle-002` and `cycle-042`, `msrp.tsv` and `acmp.tsv`, which share one capture time base (`receipts/findings_check.txt`):

  | Cycle | After the bridge's Listener `Lv` | After the DISCONNECT_RX response |
  |---|---|---|
  | 2 | 0.0951 s | 0.1040 s |
  | 42 | 0.3184 s | 0.3277 s |

  The published figures are the response-relative times, attributed to the bridge's `Lv`.
- Impact: the record of the DUT's MSRP behaviour in the two slowest-restart cycles is wrong by 9 ms against its stated reference. The issue asks for the MSRP profile to be recorded per cycle, and this is the observation flagged for triage.
- Required outcome: either state the figures as "after the DISCONNECT_RX response", or give 0.095 and 0.318 s after the bridge's `Lv`.
- Verification: `scripts/check_findings.py`, section F1.

### R575-1-F2 MINOR: the soak capture-loss bursts did not hit all four streams

- Lenses: Tests, Docs.
- Where: `docs/findings/B14_BENCH_5603C353.md:460`, "on all four streams at once: 9 to 12 AAF PDUs and 1 CRF PDU".
- Evidence: `author/soak/soak-overlap-recovery.txt` and `soak-wire-aggregate.txt`.
  - Capture 035 lost PDUs on three streams only. The DUT's CRF stream (port 3, `0001`) has no loss there.
  - The aggregate counts 2 gaps for that stream and 3 for each of the others.
- Impact: a recorded observation about the capture path does not match the packet. The attribution to the capture path still holds, because every missing PDU was recovered from the previous capture.
- Required outcome: say three or four streams, for example "on three or all four streams at once (capture 035 lost no CRF PDU of the DUT's)".
- Verification: `scripts/check_findings.py`, section F2.

### R575-1-F3 MINOR: a second `SLIP_LB` step after the soak binds is not recorded

- Lenses: Robustness, Tests, Docs.
- Where: `docs/findings/B14_BENCH_5603C353.md:477-483`, and the summary row at line 38.
- The page records "one loopback slip at INTERNAL", between 06:28:23 and 06:33:23. It explains that a freshly primed ring "can slip once".
- Evidence: the console reads of `0x8D4` (`receipts/findings_check.txt`):

  | Read | Time | `SLIP_LB` |
  |---|---|---|
  | `console-prebind.txt` | 06:22:39.06 | `0x8e` |
  | `console-soak-000.txt` | 06:23:23.21 | `0x90` |
  | `console-soak-005.txt` | 06:28:23.21 | `0x90` |
  | `console-soak-010.txt` | 06:33:23.21 | `0x92` |

  - The peer's AAF stream was bound to the DUT's STREAM_INPUT 0 at 06:22:39.51 (`bind-a-aaf.jsonl`), and soak t0 is 06:23:22.71.
  - So the freshly bound ring at INTERNAL slipped one frame within 44 s of the bind, almost certainly before t0, and again 6 to 11 minutes later. That is two slips, not one, and the first is unrecorded.
  - The design arms no settle recentre on a bind (`milan_datapath.sv:6603-6605`), which matches the page's mechanism. The count does not.
- Impact: the behaviour of a bind at INTERNAL, outside the declared transient, is under-reported. The page's "slip once" explanation is not what the counter shows, and #645/#647 triage depends on this observation.
- Required outcome:
  - record the `0x8e` to `0x90` step and its bracket;
  - state whether it falls before t0, so that it is outside the graded soak;
  - restate the observation as two one-frame slips after the bind.
- Verification: `scripts/check_findings.py`, section F3.

### R575-1-F4 MINOR: the receive-drop lane has no source on this build

- Lenses: Conformance, RTL, Docs.
- Where: `docs/findings/B14_BENCH_5603C353.md:494-497`, and line 500.
- The page says "The RMON lanes hold the FCS, preamble or alignment and receive-drop counts", and grades the drop count NOT RUN only for want of a `STATS_CTRL[0]` snapshot.
- Evidence:
  - The page's own `STATS_CAP` read is `0x1B8`, which sets bit 6 to 0.
  - Lane 6 at `0x228` is `RX_FIFO_OVERFLOW` (`ethernet_events.svh:21`).
  - `REGISTER_MAP.md:507` and `:533` define that lane as "none - MAC-internal, not exposed" and "no source, see `STATS_CAP`". The map also says a structurally silent lane must be rendered "not supported", never "0 errors".
  - FCS (`0x224`), alignment (`0x220`) and delivered-bad (`0x22C`) are real lanes. A receive-drop lane is not.
- Impact: the record implies that a later lane allowed one snapshot write could grade item 6's drops. On this build it cannot.
- Required outcome: item 6 states that the FCS and alignment lanes need a snapshot to read, and that receive drops (`RX_FIFO_OVERFLOW`) are not supported on this build (`STATS_CAP` bit 6 = 0).
- Verification: `scripts/check_findings.py`, section F4.

### RESIDUE (wording only; the exact fix for each)

- **R575-1-R1**, line 172. Replace "It came 57 to 96 ms late in cycles 26, 56 and 97" with "It came late, 57 to 96 ms after the response, in cycles 26, 56 and 97". The figures are after-response times, about 49 to 87 ms later than the median.
- **R575-1-R2**, line 188. Replace "86 cycles show only the bridge's Listener `Lv` and the DUT's Domain JoinIn and Talker Advertise JoinMt" with "86 cycles show only the bridge's Listener `Lv` and the DUT's Domain JoinIn and Talker Advertise JoinMt, besides the DUT's own Listener declaration for the peer's CRF stream". `msrp.tsv` carries DUT Listener JoinMt in every hold.
- **R575-1-R3**, line 41 (summary). Replace "44 of 44 inventory rows equal the as-found record" with "44 of 44 inventory rows equal the 06:22 pre-soak inventory, and its formats, clock sources, listener states and DUT maps also equal the 05:17-05:20 as-found reads". The body (lines 541-543) is already exact. The talker states and peer maps are not among the 05:17-05:20 as-found reads examined.
- **R575-1-R4**, line 90. Replace "No other counter moved." with "No other counter moved except the traffic counters (FRAMES_TX, FRAMES_RX and TIMESTAMP_VALID)".
- **R575-1-R5**, line 458. After the four tap PDU totals, add "summed over the 121 captures of each filter, whose spans total 6,858.7 s including overlaps and the 16 s before t0". The figures are per-file sums (`soak-wire-aggregate.txt`, "span sum 6858.7"), not unique PDUs inside the 6,823.7 s coverage.
- **R575-1-R6**, lines 35 and 149. Write "NOT RUN (not observable: no silicon register counts it)" in place of "NOT OBSERVABLE", so the recentre count uses the lane's NOT RUN vocabulary. The page already does not imply a pass.

### SUGGESTION

- **R575-1-S1**, `docs/findings/README.md`. This is outside the assigned single-file scope. The index row for `608_75_WITHDRAWAL_AND_RESTART.md` still reads "pending a re-run after processor PR #133", and this page is that re-run. A row for B14 (and B13), or a forward pointer, would keep the index current.

## Item-by-item judgement against the archived evidence

| Item | Recorded | Recomputed from the packet | Receipt |
|---|---|---|---|
| 1 Identity | entity_id, name, firmware 2.96.0, serial; CSR ID, VERSION, AEM CRC; SYNC/ASCAPABLE/TU | `identity/identity.json`: all four ATDECC fields and the three console checks match. The serial is the committed config value (`configs/endstation_ax7101_1x1_tdm8.yaml:28`) | inspection |
| 2 Switches (#645, #647) | 10+10; 1 to 3 frames before the boundary, none after; `SLIP_TDM` 0; MEDIA_UNLOCKED 0; no tap gap | **Match.** `switches.json`: 3,2,2,3,2,1,2,2,2,2 frames, 0/0 after, LOCKED 6.21-7.21 s and 2.71-3.40 s, trim -6.06 to -5.94 ppm, 5 converged-low polls. From an independent decode of every GET_COUNTERS payload in `cycNN/events.jsonl`: CLOCK_DOMAIN +1/+1 and MEDIA_RESET +1 per switch, no MEDIA_UNLOCKED anywhere. No step fell between first-LOCKED + 4.096 s and the +0.5 s margin, so the margin decided nothing | `item2_check.txt`, `item2_counters.txt` |
| 3 Withdrawals (#608) | 100/100; last PDU 0.004 to 1.99 ms before `Lv`; `Lv` 8.35-95.7 ms, median 8.88; START/STOP +1/+1; restart 10.4-125.9 ms, median 12.0; bridge 97 LeaveAll MRPDUs, DUT 0, in 894 s; profiles 86/12/2 | **Match.** All 101 table rows equal `analysis.json`/`result.json`. `Lv` was recomputed from `msrp.tsv`/`acmp.tsv` and START/STOP from snapshot payloads. LeaveAll: bridge 97, DUT 0, none before any `Lv`; 894.005 s; profiles 86/11+1/2. Exception: F1 | `item3_check.txt` |
| 4 Starts (#667) | EARLY 0, LATE 0; steps 66/26/6/2; 1,000 headers tv=1 tu=0; no gaps | **Match.** Every doc row equals `startup-cycles.csv`. The 1,000 raw AVTP headers were decoded independently (subtype AAF; tv, tu, mr, sequence and timestamp all equal the CSV). The step histogram equals the raw headers. 800 post-bind polls have no EARLY or LATE | `item4_check.txt`, `item4_headers.txt` |
| 5 Map and soak (#682, #658) | maps 4 and 8; 7,200.5 s, 121 polls, 25 timing reads; 0 error-class increments; tap totals; 363 captures, 0 drops; 6,823.7 s coverage; observations | **Match**, except F2, F3 and R5. The map payloads decode to 4 and 8 mappings. 121/121 CLEAN, poll interval 59.1-61.2 s. Every error-class delta is 0. 363/363 report 0 kernel drops. FRAMES_TX/RX +7,200. Unsolicited: the DUT sent 60 each for STREAM_OUTPUT 0/1 and none for its inputs; the application rule saw 6,909 per peer listener | `soak_check.txt` |
| 6 Ethernet receive (#691) | Link PASS; RX error counters NOT RUN | Link: `MAC_STATUS` `0x0d` at 27/27 reads, LINK_DOWN 0. NOT RUN is stated with its reason. Exception: F4 | `soak_check.txt` |
| 7 MAAP (#686) | ANNOUNCE PASS; acquisition and DEFEND NOT RUN | **Match.** 879 PDUs: DUT 220, peer 440, third station 219, all ANNOUNCE. The DUT's 127 intervals run 30.505-31.405 s, mean 31.004, inside the declared 30.488-31.511 s draw (`MAAP_FABRIC.md`). No overlap, no PROBE or DEFEND. The console words are the same at 05:17, 05:20, 05:45, through the soak and at 08:23 | packet `maap/summary.json`, inspection |
| 8 Restore | 44/44; peer clock restored at 05:45:36 and 06:08:53; residuals | **Match**, except R3. `restore-compare.txt` has 44/44 rows. Peer SET_CLOCK_SOURCE 0 at 05:20:08 and 05:48:59, back to 1 at 05:45:36 and 06:08:53, each read back. NVM seq 234 to 272, 38 commits, 0 failed, `dirty=0`. `SLIP_LB` 0 to `0x92` and rails 0 to 10 (as found at 05:17: both 0) | inspection |
| Evidence totals | 20 / 1.51 GB, 101 / 89.8 MB, 300 / 452 MB, 363 / 25.9 GB | **Match** (`raw-index/*.jsonl`); every pcap carries a SHA-256 | `raw_index_check.txt` |

**NOT RUN items.** All of them are stated as such, with reasons, and none is implied to pass:

- the #691 receive error counters (with F4's correction);
- MAAP acquisition, PROBE timing and DEFEND (boot-time; no overlapping PROBE; no reset allowed);
- the settle recentre's per-switch count ("NOT OBSERVABLE", with its reason; R6);
- absolute gPTP correlation in item 4.

The SoC board was untouched after the ruling: `identity/soc-check.txt` holds the single 04:54 carriage return from before it, and `precheck/host-checks-s3.json` says "not touched".

**Bench state deviation.** It is recorded accurately (lines 530-533 and 561-565):

- As found, the peer followed the DUT's CRF and held two DUT bindings.
- Items 2 and 3 set the peer to INTERNAL and restored it.
- Item 4 released and re-bound the peer's STREAM_INPUT 0 (`asfound-release.jsonl`, `asfound-rebind.jsonl`, flags `0x0082`).
- Every read-back is in the packet.

**Privacy.**

- The page names no bench instrument, peer product, host, interface, path, subnet or private suite.
- The only MAC-shaped strings are MAAP-pool multicast addresses in `91:E0:F0:00:xx:xx`. They are dynamic allocations, not station identifiers, and the packet itself leaves stream destination addresses in this pool unmasked. A findings page already merged at the base publishes one too (`606_FIRST_BIND_MEASUREMENT.md:80`).
- The entity_id and serial are the DUT's committed configuration.
- `docs_check.py` (scrub self-test 23/23) passes.

## Per referenced issue (the PR says Refs, not Closes)

| Issue | Met by this evidence | Remains open or unexercised |
|---|---|---|
| #608 (open) | Item 3 on this image: 100/100 withdrawals stop within one PDU of the bridge's `Lv`, and STREAM_STOP counts each. The DUT sent no LeaveAll, which is consistent with the received-LeaveAll restart. This is the re-run that correction 5886425487 required | The registrar at `Lv` was UNDETERMINED in 100/100, so the LV-registrar case (processor #134, #665 F4) was not bench-exercised. Closure is the manager's |
| #645 (open) | Acceptance 3: 20/20 switches show no undeclared discontinuity on the followed receive path | F3's slip at a bind at INTERNAL is outside the declared transient and the followed path. It needs triage, not grading here |
| #647 (open) | Bench item: B8's INTERNAL to AAF repeat behaves as declared (no slip after settle) | The once-per-switch recentre count was NOT RUN (no register). #647's own mechanism, the INTERNAL aligner pull-in under a held serial clock, was not exercised on the bench |
| #667 (closed) | 0/100 EARLY and 0/100 LATE, every first step within 21 ns of 125 us | The conditions differ from B13 (DUT at INTERNAL, peer following). This is recorded at lines 573-575 |
| #682 (closed) | Acceptance 5: the #608 re-run, the #658 map read and the soak are all done | none |
| #658 (closed) | Effective maps of 4 and 8 mappings | The page states that a saved mapping cannot be excluded (54 NVM records) |
| #686 (closed) | Acceptance 4, ANNOUNCE coexistence with the reference peer: no overlap or conflict, intervals inside B.3.4.1 | PROBE and DEFEND are not exercised, and no comparison with a pre-#686 exchange exists ("unchanged" is not shown) |
| #691 (closed) | Its acceptance is build-side (IOB pack). The bench shows a stable 1000/full link | RX error counters NOT RUN; receive drops are unsupported on this build (F4) |

## Lens results

| Lens | Result | Artifact examined at the head | What was checked, against what |
|---|---|---|---|
| Conformance | UNCLEAN (F1, F4) | `B14_BENCH_5603C353.md:28-41, 156-302, 485-526, 584-599`; issue #608 item 3 and rulings 5885808887/5886425487; the assignment 6085135051; the #645/#647/#682/#686 acceptance | Every graded item against its issue bar; the NOT RUN statements; the citation table against the clause use in merged findings (`667_TALKER_START_BENCH.md`, `608_75_WITHDRAWAL_AND_RESTART.md`, `MAAP_FABRIC.md`) |
| RTL | UNCLEAN (F4) | `hdl/milan/milan_datapath.sv:6589-6650`; `ethernet_events.svh:15-23`; `REGISTER_MAP.md:455-536, 1870, 2009-2069`; `MEDIA_CLOCK_FOLLOWING.md:1060-1249` | The page's hardware claims: no settle arm on a bind, 8 windows = 4.096 s, `SLIP_LB` 2 dups per frame with 2 fed pairs, the recentre count as a verification tap only, and the RMON lane semantics. No RTL is in the diff |
| Robustness | UNCLEAN (F3) | The packet's soak console reads, binds and chunk log; item 3 pilot `cycle-001` (rc 137); `soak-coverage.txt` gaps | Edge states and failure paths: the bind at INTERNAL, the capture-stop defect and its fix, chunk gaps, the boundary margin, STOP and NOT RUN handling, and the restore under the clock-loop deviation |
| Tests | UNCLEAN (F1, F2, F3) | Packet `c848925d` item2/3/4/soak/maap/restore records; the scripts in `scripts/` | Each figure recomputed independently: raw GET_COUNTERS decode, raw AVTP header decode, MSRP/ACMP re-timing, per-poll ledger, capture receipts. Grading can fail (it counts PDUs after `Lv` + T, and slips after the boundary) |
| Docs | UNCLEAN (F1-F4) | `B14_BENCH_5603C353.md` (all 619 lines); docs gates at the head | Text against evidence; privacy; links and anchors. Gates rc 0: `docs_check`, `check_doc_style`, `gen_toc --check`, `--verify-anchors`, `check_em_dash --base 5603c353`, `check_doc_paths`, `check_baremetal_only --check`, `git diff --check` (`receipts/gates/`) |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F4) | the page; #608/#645/#647/#667/#682/#658/#686/#691 acceptance and rulings; the citation cross-check | R575-1 | 6ec1a3a9a827575a84fb60d42ad3b085ecb70f19 |
| RTL | UNCLEAN (F4) | `milan_datapath.sv` settle block; `ethernet_events.svh`; `REGISTER_MAP.md`; `MEDIA_CLOCK_FOLLOWING.md` | R575-1 | 6ec1a3a9a827575a84fb60d42ad3b085ecb70f19 |
| Robustness | UNCLEAN (F3) | soak binds and console reads; item 3 pilot; coverage gaps; restore | R575-1 | 6ec1a3a9a827575a84fb60d42ad3b085ecb70f19 |
| Tests | UNCLEAN (F1, F2, F3) | packet records items 1-8; independent recomputes | R575-1 | 6ec1a3a9a827575a84fb60d42ad3b085ecb70f19 |
| Docs | UNCLEAN (F1, F2, F3, F4) | the page; the eight docs gates; privacy scan | R575-1 | 6ec1a3a9a827575a84fb60d42ad3b085ecb70f19 |

RESIDUE R1-R6 and S1 leave no lens unclean.

## Real limits

- The raw captures (about 27.9 GB) and the raw console and poll logs are outside the packet, listed by SHA-256 only.
  - Tap-derived figures (last PDU before `Lv`, PDUs after `Lv` + T, tap gaps, `mr`, tv and tu over the switch captures, the 0.5 s `SLIP_LB` poll series) were checked against the archived derived records, not re-decoded from pcaps.
  - Counter, MSRP/ACMP, first-ten-header and console figures were re-derived from archived raw payloads.
- Clause numbers were cross-checked against merged repository usage only; no standards text was available.
- The protocol-processor submodule was not initialised. Whether pin `2ad2f845` carries processor #133 is inferred from the wire behaviour (the DUT sent no LeaveAll against 97 received), not checked in source.
- Physical calibration is NOT RUN, and no hardware was touched. These are bench records, not reviewer hardware proof.

## Hosted evidence at the exact head (observed, not accepted)

- `rtl-fast` success, `full-ci-gate` success, `docs-check-no-git` success, `elaborate` success, `bdd-conformance` success, `wire-accountability` success.
- `docs-check` was still in progress at 09:09 UTC.
- `verilator-suites`, `yosys-portability`, their shards, `verilator-lint`, `firmware-unit`, `yosys-elaboration` and physical gPTP were skipped (the PR is not a draft; these were skipped for a doc-only diff and not executed).
- Snapshot: `receipts/checkruns_head.json`.

## Pending manager duties

- Hosted and act acceptance at the exact head, including the in-progress `docs-check`.
- The current-dev merge-candidate validation (builder and native banks) against live dev `e8454e2751d05b02ee8e5a571857589ab358ab86`. No manager source bank ran at this head, and none is claimed or inferred here.
- Carry R1-R6 to the residue checklist.
- Rule on S1 (findings index).
- Re-review after F1-F4 are answered.
- Decide #608 closure (the PR says Refs).

## Clone state after the review

- HEAD and tree are exact; worktree, index and modes match the tree; there are no untracked files.
- Gitlinks are unchanged: `external` efeb541a, `gptp-processor` 5dce647a, `protocol-processor` 2ad2f845 (`receipts/clone_integrity.txt`).
- No probe edited the clone. There were no source edits, commits, pushes or GitHub writes.

## Publishable files

`REPORT.md`, plus everything listed in `MANIFEST.sha256`: the scripts (`scripts/run_all.sh <packet-root> <checkout> <out>` reproduces every recompute receipt byte-for-byte) and the receipts.

R575-1 FINISHED
