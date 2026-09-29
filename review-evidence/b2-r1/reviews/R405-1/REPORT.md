[R405] NEGATIVE - exact head c37f1d04e39be0344dfde77e793cdfa441bd4869

# R405-1: external independent review of PR #622 (issue #606, with #608 and #75)

- Round: R405-1, external independent reviewer, cleared context, own detached clone.
- Exact head: `c37f1d04e39be0344dfde77e793cdfa441bd4869`, tree `44ffbf6fff19ac25b8916051bf9f14bf011b35a5`; `refs/pull/622/head` resolves to the same commit (`receipts/00-head-identity.txt`).
- Base: dev `13eda870d1a6cf3f946fc228a98862366b08d102`, the single parent of the head.
- Diff: two added Markdown pages (mode 100644) and nothing else. All gitlinks equal the base; the processor pin is `c951a9ff` (`receipts/11-clone-integrity.txt`).
  - `docs/findings/606_FIRST_BIND_MEASUREMENT.md`, blob `c09fb9ba`.
  - `docs/findings/608_75_WITHDRAWAL_AND_RESTART.md`, blob `57921a24`.
- Commit message: one line, no trailers. PR body: "Relates to" #606, #608 and #75; `closingIssuesReferences` is empty, so it closes none of them.

## Authorities, in the order read

1. `AGENTS.md`, `CONTRIBUTING.md` (section 6, documentation wording and privacy; the em-dash and Contents rules), `docs/README.md`.
2. Issue #606: body; the [A10] analysis (5860869610); the lane B2 assignment (5885087413).
3. Issue #608: body; the [A10] decision (5860869482); the two #75 facts (5866775445); the manager ruling (5885808887, 07:36:52Z, published after the REVIEW READY at 07:34:43Z).
4. Issue #75: body, "How we prove it" and the three acceptance criteria.
5. PR #622: body and files.
6. Processor documents at pin `c951a9ff`: `05_acmp_engine.md` section 6bis (the `T-SRP-DAFRESH` gate, `T-ACMP-DA-RETRY`), `08_timing.md` (`T-SRP-DAFRESH` 15 s, `T-ACMP-DA-RETRY` 100 ms, `T-MRP-LEAVE` 4500-7500 ms), `10_srp_engine.md` section 6.5 (Δ13, aging at transmit acceptance) and the leavealltimer deviation text at lines 559-570.
7. IEEE 802.1Q-2014 Table 10-4 (registrar), Table 10-5 and section 10.6 (LeaveAll), as quoted by the processor documents.
8. The merged #75 page `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md` (the 9e9954e9 comparison) and lane B1's pages at PR #620 head `931c3edf` (the same image's identity and saved-state record).

## Evidence judged

- The archived packet `review-evidence/b2-r1` at evidence commit `2c9f3df287b1ab433f18265b4bc91d77bc987b3f` (the live `b2-review-evidence` branch tip).
- My extraction is byte-identical to that commit: 1,858 of 1,858 blobs match. The archive `MANIFEST.json` verifies all 1,857 published hashes with no unlisted file. The author's own `MANIFEST.sha256` fails on exactly the four files the archive records as path-redacted (`receipts/01-packet-integrity.txt`).
- The 18 tool hashes on the #606 page equal the packet's tool bytes.
- Raw captures are not in the packet (by design). See Limits for what that leaves unchecked.

## Assigned checks

### 1. Identity gate: PASS

- The console CRCs equal the `eto` seed row of the packet's expected-CRC table for the `13eda870` build: ROM `acad92b9` (53,344 bytes), QSPI payload `d84bce7b` (3,825,788 bytes), AEM `93742dd2` (7,352 bytes). The `eppo` and `asl` seeds read differently, as the page says.
- VERSION `0x00020060`. ENTITY (312 bytes at `0x110`) and CONFIGURATION (106 bytes at `0x248`) match the AEM image byte for byte.
- The same image hashes and CRCs appear independently on lane B1's page `599_394_E1_LINK_CYCLES.md` at `931c3edf`.
- The UART grader passed 10/10 at identity and at the end. The reset epoch read 1 before and after every action, and all console samples read `SYNC=1 ASCAPABLE=1 TU=0` (`receipts/03-restore-state.txt`).
- The page correctly limits the claim: readback proves CRC consistency, not a configuration SHA-256.

### 2. #606 first bind: PASS as measured, with the post-reset path still open

Re-derived from each bind's `msrp.tsv`, `acmp.tsv` and snapshots (`receipts/02-rederive.txt`):

- Five first binds; first valid CRF PDU 0.059352-0.229360 s after the tapped `CONNECT_RX` response. Replay and live values are identical for every bind (`receipts/07-pauses.txt`).
- The reference peer's `PROBE_TX` crossed the tap 26.6-83.2 us after the response; the DUT answered SUCCESS about 7 us later every time.
- The DUT's first Talker Advertise was `JoinMt`, 0.000337-0.172822 s after the response.
- The bridge's first MRPDU after the response carried exactly one event, Listener `New` for the stream (Ready), at 0.057989-0.227724 s. No bridge LeaveAll preceded it. Ready to first PDU was 0.6-1.8 ms.
- **Pre-bind windows** (17.315-17.373 s of tap before each `CONNECT_RX`): 1-2 DUT LeaveAll PDUs each (the last 2.2-9.3 s before the command); DUT Talker Advertise events for the target stream were `Mt` only; zero Talker Advertise declarations for any stream; zero bridge Listener declarations; zero stream PDUs. After its own LeaveAll a declaring applicant would have re-declared, so no DUT Talker Advertise was declared before any bind.
- **No reset.** The fresh state came from unbind plus the 15 s `T-SRP-DAFRESH` gate: each unbind stopped the stream within one PDU; the DUT withdrew its Talker Advertise at +0.021 s (unbind 1) and +7.122 to +7.168 s (unbinds 2-4), and never re-declared. The next `CONNECT_RX` came at least 27.5 s after that withdrawal (quiet tail plus pre-bind window), beyond both the 802.1Q LeaveTime and `T-MRP-LEAVE`.
- **Long hold:** binds 2-5 followed 39.3 / 36.9 / 37.0 / 36.9 s unbound on the controller clock; all four connected within 1 s. Bind 1 ran at 06:56:18Z, 34 minutes after lane B1's 06:22Z restore.
- The 9e9954e9 comparison column matches the merged #75 page (6.889398, 6.888605, 0.079 and 6.080 s) and the [A10] analysis (status 3).
- **What the post-reset allocation path still needs.** The #606 cause was a startup destination-address allocation refused while no MAAP block was valid, which only a DUT reset or power-up reaches. Here both outputs already held MAAP-range destinations, so no allocation ran. A bench close-out needs a maintainer-authorised reset, then, on the tap: the refused or late startup allocation; recovery on the 100 ms `T-ACMP-DA-RETRY` round; a first `PROBE_TX` answered SUCCESS; and a first valid PDU within 1 s of the first `CONNECT_RX` after boot. The saved-state layer should be read before and after, because a reset reloads it. Until then PR #613's first-probe regression is the only evidence for that path. The page's Limits section says so.

### 3. #608 withdrawal: PASS 99 of 99 under the ruling's bar

Re-derived from the replayed per-cycle records (`receipts/02-rederive.txt`):

- The bridge's Listener `Lv` crossed the tap 0.008466-0.098486 s after the disconnect response. No `DISCONNECT_TX` crossed the tap in any cycle.
- Registrar class at the `Lv`, by my own classifier over capture order: 42 IN observed, 57 IN inferred, 1 LV. Every class equals the author's replay.
  - Every IN-inferred cycle has no LeaveAll of any type before its `Lv` in the capture.
  - The inference bound holds: 110 Listener-type LeaveAlls seen while registered (53 DUT, 57 bridge) were each followed by a bridge re-declaration within 0.087969 s. The only unanswered one is cycle 22's own, answered by the `Lv`.
  - The shortest pre-`Lv` capture is 2.742934 s (cycle 4); the page prints 2.743 (see S1).
- The 99 stops within one PDU are exactly the 99 IN cycles. In them the last PDU fell 1.974 ms before to 0.001 ms after the `Lv` (0.006858-0.097036 s after the disconnect response, median 0.008363 s), and no valid PDU followed `Lv` + 2 ms.
- STREAM_START/STREAM_STOP, decoded from the raw GET_COUNTERS payload bytes, moved +1/+1 in each of the 99 cycles and +0/+0 in cycle 22. Each action's after-counters equal the next action's before-counters, and the session reconciles 11/11 to 115/115 (+5/+0 binds, +0/+4 unbinds, +99/+99 cycles, +0/+1 restore).
- **Cycle 22**, seconds after the disconnect response, all reproduced: the bridge LeaveAll at -0.391721 carries its Listener `JoinMt` for the stream in the same MRPDU (registrar back to IN); the DUT's own LeaveAll for all four types at +0.009401; the bridge `Lv` at +0.010791. That is 1.390731 ms after the own LeaveAll, with no re-declaration between, so the registrar was LV. There were 1,005 hold PDUs; the reconnect response came at +2.008674 and the bridge `New` at +2.020318, before any leave-timer expiry.
- The near-LeaveAll table (cycles 20, 21, 22, 35, 45, 60, 73 and 88) reproduces exactly. In cycles 35, 45, 60 and 73 the bridge re-declared between the DUT's own LeaveAll and its `Lv`.
- F3 below concerns why cycle 22's LV window existed, not the classification.

### 4. #75 restart: PASS for the DUT-talker CRF pair on this image, given the ruling

- 99 of 99 demonstrated restarts within 1 s: min 0.011239, median 0.013195, p95 (nearest rank) 0.081912, max 0.139247 s. Subgroups reproduce: 96 with Talker Advertise held (max 0.101353); 3 with it withdrawn in the hold (cycles 1, 4 and 44, max 0.139247). Exactly those three cycles followed host-clock pauses over 15 s (56.5, 88.9 and 43.0 s).
- No growth: OLS slope -0.000082801 s/cycle, standard error 0.000076628, t(0.975, 97) 1.984723, 95% interval [-0.000234887, +0.000069285]; first-ten median 0.013168, last-ten median 0.013255 s. As a distribution-free cross-check, Spearman's rho is -0.096. All ten block rows reproduce, including the combined MSRP rate of 1.764-2.068 PDU/s.
- **Does 99 meet #75's acceptance?** Yes, for this pair. #75's three acceptance criteria carry no count, and all three hold: every one of the 100 successful reconnects had a valid PDU within 1 s (cycle 22's stream never stopped, and its first PDU after the response came at 0.001547 s); the slope interval includes zero; and the result is documented. The count of 100 is in "How we prove it". 100 physical cycles ran, 99 of them demonstrated a restart, and the ruling states that no additional cycle is required. AAF and the DUT-listener direction on this image remain outside this lane, as both pages say.

### 5. Restore and the saved-state layer

The restore proof is sound as far as it goes (`receipts/03-restore-state.txt`): 18 of 18 stream states read connection count 0 at start and end; 53 of 53 non-counter census reads are equal (the only byte difference is GET_AVB_INFO's measured peer delay, 379 vs 383 ns, which the author's compare masks as a measurement); the AVB_INTERFACE counters are unchanged; the restore unbind stopped within one PDU; the final 16.9 s tap carried no target PDU and the DUT's CRF transmit count did not move; the grader passed 10/10; the reset epoch read 1.

The saved-state layer was read, at identity (06:49:58Z) and at the end (07:20:45Z), and the two reads are identical:

| Saved-state field | Start, 06:49:58Z | End, 07:20:45Z |
|---|---|---|
| NVM slots A / B, image sequence | 229 / 230, both `VD_OK`, authoritative B, image 230 | same |
| Records, writer | 53 records, 3,264 B, writer live | same |
| `PP_NVM_STAT` | `0xc34000e4`: pend 1, dirty 0, commit_busy 0 | same |
| `PP_STAT`, `nvm_pend` (bit 11) | `0x5b000c44`, 1 | `0x5b000c44`, 1 (all 226 console samples) |
| Commits | ok 2, failed 0 | ok 2, failed 0 |

So the layer ended as found. `nvm_pend=1` and slots 229/230 are lane B1's recorded end state at `931c3edf`, inherited. As an observation, not a finding: no commit ran during the 31 minutes of binds and unbinds while `nvm_pend` stayed 1. Neither page records any of this (F2).

### 6. Privacy and gates

- **Token scan** (`receipts/04-token-scan.txt`; identifiers printed only as sha256 prefixes; a private deny-list of host, vendor and account tokens was applied from a file held outside this packet):
  - Both pages are clean. Their only identifier-shaped tokens are the DUT's locally administered entity ID and MAAP multicast stream destinations. Their one account-class hit is the public processor repository URL.
  - The archived packet has no private host, instrument, interface, serial or account name, no absolute private path and no IPv4 address (the one dotted hit is an 802.1AS clause number). Interface, module and host-MAC strings are masked.
  - The archived packet does carry vendor-OUI identifiers. The bench switch's gPTP clock identity and the peer's entity ID and MAC are already in tracked files at dev, for example `docs/findings/117_GPTP_SILICON_EVIDENCE.md`. The peer's stream ID is that public MAC plus a unique ID. The controller host's EUI-64 entity ID (`sha256:66a7cdc0edbc`, in 449 files) encodes a host MAC that is in no tracked file at dev or at live dev; it was previously public only in PR #604's evidence archive. See F4.
- **Markdown gates at this head in the pinned environment** (a disposable venv from `tools/markdown/requirements.txt` with `--require-hashes`: cmarkgfm 2025.10.22, html5lib 1.1): all rc 0 (`receipts/05-docs-gates.txt`).
  - `docs_check.py`: 0 findings over 176 pages and 938 scrubbed files.
  - `check_em_dash.py --base 13eda870`: 0 findings over 802 added lines. Its `--selftest` passes.
  - Also rc 0: `gen_toc.py --check`, `check_doc_style.py` and its `--selftest`, `check_doc_paths.py`, `check_gptp_docs.py`, `docs/DOC_MAP.gen.py --check`, `check_feature_status.py --self-test`, `check_baremetal_only.py --check`, `ci_scope.py --selftest`, and `git diff --check 13eda870 HEAD`.
- All 34 relative links and anchors in the two pages resolve (`receipts/06-links.txt`).

## Findings

F1 and F2 were found in my own pass before I read any prior review. F3 and F4 were raised by R404-1; I verified both independently from primary sources and retain them (see "Prior public findings").

### F1 MINOR: the #608 page presents a decided reading as undecided

- **Lenses:** Conformance, Docs.
- **Where:** `docs/findings/608_75_WITHDRAWAL_AND_RESTART.md:17`, `:23` and `:27-35`. The PR body's lines 19, 24 and 26 repeat them.
- **Authority/evidence:** The manager ruling on #608, 5885808887:
  - the bar is a withdrawal that reaches an IN registrar;
  - #608 item 3 is PASS 99 of 99, and STREAM_STOP counted each stop;
  - the LV case is graded separately, in a processor simulation arm;
  - for #75, no additional cycle is required.

  The page still says "The two readings of #608 item 3 need a decision; this page does not choose", and grades "#75: at least 100 physical restarts" NOT MET. It also links the earlier [A10] decision (5860869482), which already stated this reading, as "the #608 decision" while calling the question open.
- **Impact:** Once merged, a durable findings page on dev contradicts the recorded decision. A cold reader sees an open decision and a failed #75 line that the maintainer has already resolved, and could reopen #608 item 3 or schedule a needless extra cycle campaign.
- **Required outcome:**
  - The page cites the ruling and grades #608 item 3 and the #75 cycle-count line under it.
  - It names the LV simulation arm as the owner of the LV case.
  - The literal-text count may stay as context.
- **Verification:** Re-read the two verdict rows and the "two readings" paragraph at the new head against 5885808887. The Markdown gates stay rc 0.

### F2 MINOR: the restore proof omits the saved-state layer

- **Lenses:** Conformance, Docs.
- **Where:** `docs/findings/606_FIRST_BIND_MEASUREMENT.md:226-239` and `docs/findings/608_75_WITHDRAWAL_AND_RESTART.md:352-381` ("Restore, all proven").
- **Authority/evidence:**
  - Assignment 5885087413, step 4: "Restore everything as found and prove it."
  - The census compares AEM state only. Lane B1 round 2 showed, on this image the same morning, that the saved-state layer is where a lane's residue stays. It recorded slots, image sequence, `nvm_pend` and `PP_NVM_STAT` at start and end (`599_394_E1_LINK_CYCLES.md` "Saved-state layer" at `931c3edf`).
  - This lane made 105 binds and 105 unbinds, and its packet holds both reads (`identity/console-identity.txt`, `restore/console-final.txt`) plus `PP_STAT` in every console sample. Neither page mentions them.
- **Impact:** The restore claim is silent on the one layer the previous lane found changed. A reader cannot tell that it ended as found, or that `nvm_pend=1` was inherited from lane B1 rather than caused here. The next lane loses its baseline.
- **Required outcome:** A page records, at start and end: slot A/B sequences, image sequence, record count, `nvm_pend` (`PP_STAT` bit 11 and `PP_NVM_STAT`) and commit counts. It notes that the state was inherited from lane B1 and unchanged. One page may carry the table and the other link to it.
- **Verification:** The values equal the table in check 5 above and `receipts/03-restore-state.txt`.

### F3 MINOR (retained from R404-1): cycle 22's LV window came from a documented DUT-side LeaveAll deviation, and the page calls it a genuine LeaveAll cycle

- **Lenses:** Conformance, Docs.
- **Where:** `docs/findings/608_75_WITHDRAWAL_AND_RESTART.md:33-35` ("It keeps the documented LV + rLv behavior for a genuine LeaveAll cycle. Cycle 22 is such a cycle") and the cycle-22 section `:177-197`.
- **Authority/evidence:**
  - IEEE 802.1Q-2014 Table 10-5 (section 10.7.9) maps rLA! to "Start leavealltimer". Section 10.6 says a received LeaveAll restarts the timer "thus suppressing multiple LeaveAll messages".
  - The pinned processor documents that it does not restart its own timer on receipt: an open deviation tracked in processor issue #108 (`protocol-processor/docs/architecture/10_srp_engine.md:559-570` at `c951a9ff`). The same text notes that without the restart "both ends send a LeaveAll each cycle instead of one between them".
  - In cycle 22 the bridge's MSRP LeaveAll, for all four types, crossed the tap at -0.391721 s. The DUT's own LeaveAll followed 0.401121 s later. A conformant participant would not have sent that LeaveAll; the registrar would then have been IN at the `Lv`, and Δ13 would have stopped the stream.
  - Over the session, 64 of 112 captures show a DUT LeaveAll less than 9.5 s after a received bridge LeaveAll (minimum 0.199564 s; `receipts/10-leaveall-damping.txt`). R404-1 counted 67 under its own rule; the minimum gap agrees and the conclusion does not depend on the count.
- **Impact:** The page presents the residual non-stop as purely the standard's behaviour. The registrar's rLv-in-LV step is standard, but the LV state itself was opened by a DUT-side MRP deviation that roughly doubles the LV windows. #608's owner cannot see that closing processor #108 would remove this class of non-stop. The ruling's premise ("the standard's behaviour, not a talker defect") rests on the same incomplete attribution.
- **Required outcome:**
  - The cycle-22 attribution records the 0.401 s gap and the #108 deviation, and "genuine LeaveAll cycle" is qualified.
  - The tension with the ruling's premise is published for a maintainer disposition.

  This review does not re-grade #608 item 3; that bar is the maintainer's.
- **Verification:** The page text agrees with `receipts/02-rederive.txt` (cycle-22 table) and `receipts/10-leaveall-damping.txt`, and a public maintainer disposition exists.

### F4 MINOR (retained from R404-1, narrowed): the archived packet publishes the controller host's MAC-derived identity

- **Lenses:** Conformance, Docs.
- **Where:** `review-evidence/b2-r1/author` at `2c9f3df2`. Every ACMP state snapshot and census record carries the controller entity ID (`sha256:66a7cdc0edbc`, EUI-64 of a universally administered host MAC, 449 files; `receipts/04-token-scan.txt`).
- **Authority/evidence:**
  - The assignment's privacy rule, CONTRIBUTING section 6 (no bench-identifying information), and this round's brief: no private MAC-derived identity in the pages or the archived packet.
  - The packet masks `<host-mac>`, `<tap-mac>` and the interfaces, but leaves this EUI-64, which encodes a bench host MAC.
  - That MAC is in no tracked file at dev or live dev; its only earlier public appearance is PR #604's evidence archive, which is not a disposition.
  - Narrowed from R404-1: the switch clock identity, the peer entity ID and MAC, and the DUT identities are already in tracked dev documentation or code, so I do not count them.
- **Impact:** A bench host's MAC is republished in about 450 public files, contrary to the masking the same packet applies to host MACs elsewhere.
- **Required outcome:** Either the archive masks the controller entity ID (and any other non-public host identity), or a maintainer disposition records that bench AVDECC controller entity IDs are public.
- **Verification:** Re-run `scripts/scan_tokens.py` over the re-archived packet. The `sha256:66a7cdc0edbc` class is empty or dispositioned.

### Suggestions (non-blocking)

- **S1 (Docs).** `docs/findings/608_75_WITHDRAWAL_AND_RESTART.md:130` says "at least 2.743 s", but the exact minimum is 2.742934 s (cycle 4). Suggest "at least 2.742 s". This does not change the inference.
- **S2 (Docs; agrees with R404-1 S2).** `docs/findings/606_FIRST_BIND_MEASUREMENT.md:19` and `:198` say DUT MSRP "kept a 1.000 s spacing". The periodic refresh sits on a 1.000 s grid (16 of 19 and 17 of 19 DUT MRPDUs in baseline and final). Every off-grid PDU is a LeaveAll or falls within one join period after one (`receipts/03-restore-state.txt`). Suggested wording: "periodic refresh stayed on a 1.000 s grid apart from LeaveAll rounds".
- **S3 (Docs; agrees with R404-1 S1).** `docs/findings/README.md:11` still describes #75 with "three non-restarts tracked by #608; initial-bind exception tracked by #606", and neither new page is indexed. The assignment froze "no other doc edits", so scheduling this is the maintainer's call.

## Prior public findings on this PR

I read the PR #622 thread only after my own pass was complete and F1 and F2 were written down. It holds the two review-start notices (5885922821, 5886031991) and R404-1's NEGATIVE report (5886414299). Nothing has changed at this head since R404-1, so none of its findings is resolved by a fix.

| R404-1 item | Disposition at this head |
|---|---|
| F1 MINOR (Conformance, Docs) | **Retained.** Identical to my F1, found independently. |
| F2 MINOR (Conformance, Docs) | **Retained.** Identical to my F2, found independently. |
| F3 MINOR (Conformance, Docs) | **Retained** after independent verification of the processor deviation text at `c951a9ff` and the cycle-22 gap (0.401121 s). My session count is 64 of 112 captures; R404-1 reported 67 with its own rule. The minimum gap agrees. |
| F4 MINOR (Conformance, Docs) | **Retained, narrowed** to the controller host's entity ID. The switch, peer and DUT identities are already in tracked dev files. |
| S1 findings index | Agreed; carried as my S3. |
| S2 MSRP spacing wording | Agreed; carried as my S2. |

## Per-lens results

- **Conformance: UNCLEAN** (F1, F2, F3, F4).
  - Applied and correct: the identity gate; the #606 fresh-bind, probe, long-hold and no-reset results; the #608 IN-bar stops and STREAM_STOP counts; #75 criteria 1-3 and the cycle-count reading under the ruling.
  - Also correct: the pages' processor claims, checked against the pinned documents (`T-SRP-DAFRESH` 15 s under section 6bis, `T-ACMP-DA-RETRY` 100 ms, `T-MRP-LEAVE` 4.5-7.5 s, Δ13, aging at transmit acceptance) and against the pin's history (processor PRs #129 and #130 are ancestors of `c951a9ff`).
- [R405] PASS RTL - `git diff --raw 13eda870..c37f1d04` (two `.md` files, 100644) and the four gitlinks equal to base; `protocol-processor` at `c951a9ff` (`05_acmp_engine.md:359-418`, `08_timing.md:34-40`, `10_srp_engine.md:423-505,559-570`; `hdl/srp/KL_srp_top.sv` own-LeaveAll acceptance comments) - No RTL, constraint or tooling changed, so there is no clock, CDC, width, FSM or timing surface in this diff. The processor behaviour the pages describe matches the pinned design. The pre-existing #108 timer deviation is processor-owned, predates this diff and is already documented at the pin; it is carried as F3's evidence against the page's attribution, not as an RTL change of this PR.
- [R405] PASS Robustness - packet `cycles/*/analysis.json`, `bind/*/analysis.json`, `*/capture.txt`, `*/msrp.tsv`; `receipts/02-rederive.txt`, `03-restore-state.txt`, `07-pauses.txt` - Checked:
  - malformed input: 0 malformed MSRPDUs, 0 invalid or misdirected target PDUs and 0 tap-clock reversals in all 112 captures;
  - boundaries: cycle 62's last PDU at +0.001 ms against the 2 ms limit; the 1 ms own-LeaveAll rule and the 7.5 s LeaveTime cutoff change no result in this data; the 0.25 s LeaveAll neighbours classify correctly;
  - the inferred-IN bound: measured on every capture, and no IN-class non-stop appears whichever way the 57 inferred cycles are read;
  - reset: epoch 1 across every action;
  - repeated commands: 100 cycles with an exact counter chain;
  - the 30 s cap and the ten-consecutive-slow stop: neither was reached;
  - long-hold and withdrawn-advertise paths: binds 2-5 and cycles 1, 4 and 44.
- [R405] PASS Tests - `scripts/rederive.py` (1,111 checks, 0 failures), `scripts/restore_state.py`, `scripts/mutate.py` with `receipts/09-mutation-probe.txt` - This PR adds no executable test.
  - The evidence chain was replayed independently: registrar classes, the LeaveAll bound, the stops, counters from raw payload bytes, distributions and the OLS interval.
  - Every row of the per-cycle, bind, unbind, near-LeaveAll, block, distribution, growth and cycle-22 tables was rebuilt from derived values and compared.
  - 10 of 10 planted defects are detected: a re-declaration before cycle 22's `Lv`, an IN cycle that keeps streaming, a removed own LeaveAll, an uncounted STREAM_STOP, a pre-bind declaration, and five page-cell edits.
  - A gap in my own checker, found by that probe (the #606 tables were transcribed rather than parsed), was fixed before the final run.
- **Docs: UNCLEAN** (F1, F2, F3, F4). Both pages were read in full against the packet, the issues and the ruling. All Markdown gates return rc 0 in the pinned environment, and every link and anchor resolves.

## Ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3, F4) | Both pages; issues #606, #608 and #75 with 5860869610, 5885087413, 5860869482 and 5885808887; PR body; packet `identity/`, `bind/`, `cycles/`, `restore/`; processor docs at `c951a9ff`; B1 pages at `931c3edf`; merged #75 page | R405-1 | `c37f1d04e39be0344dfde77e793cdfa441bd4869` |
| RTL | CLEAN | `git diff --raw` base..head; gitlinks; processor `05_acmp_engine.md` section 6bis, `08_timing.md`, `10_srp_engine.md` section 6.5 and lines 559-570, `KL_srp_top.sv` at `c951a9ff` | R405-1 | `c37f1d04e39be0344dfde77e793cdfa441bd4869` |
| Robustness | CLEAN | 112 `analysis.json`, `capture.txt` and `msrp.tsv`; `receipts/02-rederive.txt`, `03-restore-state.txt`, `07-pauses.txt` | R405-1 | `c37f1d04e39be0344dfde77e793cdfa441bd4869` |
| Tests | CLEAN | `scripts/rederive.py`, `restore_state.py`, `mutate.py`; `receipts/02-rederive.txt`, `09-mutation-probe.txt` | R405-1 | `c37f1d04e39be0344dfde77e793cdfa441bd4869` |
| Docs | UNCLEAN (F1, F2, F3, F4) | Both pages in full; `docs/findings/README.md`; `receipts/04-token-scan.txt`, `05-docs-gates.txt`, `06-links.txt` | R405-1 | `c37f1d04e39be0344dfde77e793cdfa441bd4869` |

## Limits

- **Raw captures not re-parsed.** They are outside the public packet.
  - MSRP and ACMP timing, registrar classes, the LeaveAll bound, counters and statistics were recomputed from the packet's `msrp.tsv`, `acmp.tsv` and controller transcripts.
  - AVTP PDU timing (last PDU, hold PDUs, first valid PDU, validity) exists in the packet only as `analysis.json` fields. It was consumed as given and cross-checked for internal consistency and against the live results.
  - The capture bytes were not re-hashed against `RAW-ARTIFACTS.json`.
- **Physical calibration NOT RUN.** Printed precision is not calibrated timestamp accuracy. No hardware, bench, Docker, act or GitHub write was used.
- **Hosted checks at this head** (`receipts/08-hosted-checks.txt`; PR ready, not draft):
  - Executed and successful: rtl-fast, docs-check, docs-check-no-git, elaborate, bdd-conformance, wire-accountability, changes, full-ci-gate.
  - Skipped by scope for this docs-only change: verilator-suites, yosys-portability and their shards, verilator-lint, yosys-elaboration, physical gPTP. Skipped contexts are not proof.
- **Banks not re-run.** The manager's source static, builder and native banks were not re-run, as instructed. The scoped Verilator was not used: no RTL was in scope, and no simulation probe was needed.
- **Clone untouched.** Worktree, index, both page blobs and modes, and the gitlinks equal the exact head at the end (`receipts/11-clone-integrity.txt`). Only read-only object fetches of public refs were made.
- **Interruption.** This round was interrupted once by a session limit. Every receipt listed in `MANIFEST.sha256` was regenerated in the resumed session.

## Pending manager duties

- Publish this report.
- Route F1-F4 to an author round (F4 is archive-side), and schedule S1-S3 if wanted.
- Decide the tension in F3 between the ruling's premise and processor deviation #108.
- File or confirm the LV-case simulation arm named in the ruling.
- Own hosted and act acceptance.
- Build and validate the final current-dev candidate at the merge turn (source base `13eda870d1a6cf3f946fc228a98862366b08d102`, live dev `57b8c8676864e2564a1c867a2ee6623018a33002`).
- At the new head, re-cover Conformance and Docs, and re-cover any CLEAN lens whose scope a later commit touches.

R405-1 FINISHED
