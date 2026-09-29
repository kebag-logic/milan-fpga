[R404] NEGATIVE - exact head c37f1d04e39be0344dfde77e793cdfa441bd4869

# R404-1: internal independent review of PR #622 (issue #606, with #608 and #75)

- Round: R404-1, internal independent reviewer, cleared context.
- Exact head: `c37f1d04e39be0344dfde77e793cdfa441bd4869`, tree `44ffbf6fff19ac25b8916051bf9f14bf011b35a5`.
- Base: dev `13eda870d1a6cf3f946fc228a98862366b08d102`.
- Diff: two added Markdown pages, and nothing else.
  - `docs/findings/606_FIRST_BIND_MEASUREMENT.md` (blob `c09fb9ba`).
  - `docs/findings/608_75_WITHDRAWAL_AND_RESTART.md` (blob `57921a24`).
  - No gitlink changes; see `receipts/clone_integrity.txt`.
- Evidence judged:
  - The archived packet `review-evidence/b2-r1` at evidence commit `2c9f3df287b1ab433f18265b4bc91d77bc987b3f`.
  - My local extraction is byte-identical to that commit's tree.
  - The archive's `MANIFEST.json` verifies all 1,857 published hashes (`receipts/archive_manifest.txt`).
  - The four files where the author's own `MANIFEST.sha256` no longer matches are exactly the archive's four recorded path redactions.

Authorities, read in this order:
1. AGENTS.md, CONTRIBUTING.md and docs/README.md.
2. Issue #606: body, the [A10] analysis (5860869610) and the lane B2 assignment (5885087413).
3. Issue #608: body, the [A10] decision (5860869482) and the manager ruling (5885808887).
4. Issue #75: body and acceptance criteria.
5. PR #622: body and files.
6. Processor docs at pin `c951a9ff`:
   - `05_acmp_engine.md` §6bis;
   - `08_timing.md`;
   - `10_srp_engine.md` §6.5 and the leavealltimer deviation text.
7. IEEE 802.1Q-2014:
   - Table 10-4 (registrar);
   - Table 10-5 and §10.6 (LeaveAll).

## Verdict summary

The measurements hold up. Everything I can re-derive from the public packet agrees with both pages:
- every per-bind and per-cycle row;
- the stop classes;
- the counters;
- the restart distribution and slope;
- the capture index;
- the tool hashes;
- the identity gate.

Seven planted mutants were all rejected by the re-derivation. Four MINOR findings are open, so the verdict is NEGATIVE:
- **F1:** the #608 page still presents the #608 reading as undecided, although the maintainer has ruled on it.
- **F2:** the restore proof leaves out the saved-state layer.
- **F3:** cycle 22's LV window was opened by a documented DUT-side 802.1Q deviation. Neither page says so.
- **F4:** the archived packet carries unmasked MAC-derived identities.

None of the four questions a measured number.

## Assigned checks

1. **Identity gate: PASS.** The gate binds the run to the installed `13eda870` image.
   - Console CRCs match the `eto` build of `13eda870` (`identity/expected-crc.txt`):
     - ROM `acad92b9`, 53,344 bytes;
     - QSPI payload `d84bce7b`, 3,825,788 bytes;
     - AEM `93742dd2`, 7,352 bytes.
   - The same CRCs appear on lane B1's public page at `931c3edf` (`599_394_E1_LINK_CYCLES.md:38-39`).
   - VERSION reads `0x00020060`.
   - ENTITY (312 bytes at `0x110`) and CONFIGURATION (106 bytes at `0x248`) match the image byte for byte.
   - The UART grader passed 10/10 at identity and at the end.
   - The reset epoch (`0x90000720`) read 1 before and after all 112 actions and at both console reads (`receipts/holds_epoch_nvm.txt`).
   - The page correctly says that readback proves CRC consistency, not a configuration SHA-256.
2. **#606: PASS as measured.** All values below re-derive from the packet (`receipts/replay_b2.txt`).
   - Five first binds: first valid PDU 0.059352-0.229360 s after the tapped `CONNECT_RX` response.
   - The first `PROBE_TX` answer was SUCCESS every time, 7.1 µs after the command.
   - The DUT's first Talker Advertise was a `JoinMt` at 0.000337-0.172822 s.
   - The bridge's first MRPDU was its Listener `New`, with no LeaveAll before it. Ready to first PDU: 0.580-1.783 ms.
   - Pre-bind tap windows were 17.315-17.373 s long. Each contained:
     - 1-2 DUT LeaveAll PDUs;
     - DUT Talker Advertise events for the target stream of `Mt` only, 0 declarations (`New`/`JoinIn`/`JoinMt`);
     - 0 bridge Listener declarations;
     - 0 stream PDUs.
     So no DUT Talker Advertise was declared before any bind.
   - The fresh state was reached by unbind and the leave path, with no reset. Each unbind stopped the stream within one PDU. The DUT withdrew its Talker Advertise at +0.021 s (unbind 1) and +7.12-7.17 s (unbinds 2-4), and did not re-declare afterwards.
   - Long hold: binds 2-5 followed 39.3 / 36.9 / 37.0 / 36.9 s unbound on the controller clock (`receipts/holds_epoch_nvm.txt`). All four connected within 1 s.
   - **What the post-reset allocation path still needs.** The #606 cause was a refused startup destination allocation, which is reachable only after a DUT reset or power-up. Here both outputs already held MAAP-range destinations, so no allocation ran. A bench close-out of that path needs an assignment that authorises a reset. It would show, on the tap:
     - the refused or late startup allocation;
     - the 100 ms `T-ACMP-DA-RETRY` recovery;
     - a first `PROBE_TX` answered SUCCESS;
     - a first valid PDU within 1 s of the first `CONNECT_RX` after boot.
     Because a reset reloads bindings, the saved-state layer would have to be read before and after. Until then, PR #613's first-probe regression is the only evidence. The page's Limits section says so.
3. **#608: PASS 99 of 99 under the ruling's bar**, re-derived from the replayed per-cycle records.
   - Bridge `Lv` at 0.008466-0.098486 s after the disconnect response.
   - Registrar class at the `Lv`: 42 IN observed, 57 IN inferred, 1 LV.
     - The inferred class rests on a measured bound: 110 Listener-type LeaveAlls seen while registered, all re-declared within 0.087969 s (53 DUT, 57 bridge).
     - Every capture holds at least 2.742934 s before its `Lv` (`receipts/drill_b2.txt`).
   - Every IN cycle stopped. The last PDU fell 1.974 ms before to 0.001 ms after the `Lv`, and no PDU followed `Lv` + 2 ms.
   - STREAM_START and STREAM_STOP moved +1/+1 in each of the 99 cycles and +0/+0 in cycle 22. The session reconciles 11/11 → 115/115 (`receipts/census_check.txt`).
   - Cycle 22 (`receipts/cycle22_and_binds.txt`):
     - At -0.391721 s the bridge's MSRP LeaveAll for all four types carried a Listener `JoinMt` for the stream, so the registrar was IN.
     - At +0.009401 s the DUT's own LeaveAll followed, for all four types.
     - At +0.010791 s the bridge's `Lv` arrived. Own LeaveAll minus `Lv` is -1.390731 ms, so the registrar was LV.
     - The hold carried 1,005 PDUs.
     - Reconnect `New` came at +2.020318 s, before any leave-timer expiry.
   - The page's stop and class tables are correct. F3 concerns why the LV window existed.
4. **#75: PASS for the DUT-talker CRF pair on this image, given the ruling.**
   - 99 of 99 demonstrated restarts came within 1 s: min 0.011239, median 0.013195, p95 0.081912, max 0.139247 s.
   - No growth:
     - OLS slope -0.000082801 s/cycle, 95% interval [-0.000234887, +0.000069285], df 97;
     - first-ten median 0.013168 s, last-ten median 0.013255 s.
   - Cycle 22's stream never stopped. Its first valid PDU after the reconnect response came at 0.001547 s, so criterion 1 also holds for that reconnect.
   - Criteria 1-3 are met for this pair. The ruling states that no additional cycle is required, so "100 physical cycles" is met with 99 demonstrated restarts.
   - AAF, and the DUT-listener direction on this image, remain outside this lane. Both pages say so.
5. **Restore and saved-state layer.** The restore proof itself is sound:
   - 18/18 stream states read connection count 0;
   - 53/53 non-counter census reads are equal;
   - AVB_INTERFACE counters are unchanged;
   - the final 16.9 s tap carried no CRF;
   - the grader passed 10/10 and the reset epoch read 1.

   The packet also holds the saved-state reads, and they are equal at start (06:49:58Z) and end (07:20:45Z):
   - slot A seq 229 and slot B seq 230, authoritative B, image seq 230, 53 records;
   - `nvm_pend=1` and commits ok=2 / failed=0;
   - `PP_STAT=5b000c44` (bit 11 set) in all 226 console samples.

   So the layer ended as found. `nvm_pend=1` was inherited from lane B1's recorded residue: B1's final restore at `931c3edf` shows the same slots and `PP_STAT`. Neither page records any of this (F2). Observation, not a finding: no commit ran during the 31 minutes of binds and unbinds while `nvm_pend` stayed 1. The reads cannot say why.
6. **Privacy and gates.**
   - Both pages are clean in every scanned class (`receipts/token_scan.txt`), including a private-name pattern set that is held outside the published packet. The archived packet has no private host, instrument, interface or account names, but it does carry MAC-derived identities (F4).
   - Markdown gates return rc 0 at this head in the pinned environment (`receipts/gates/md_env_pins.txt` matches `tools/markdown/requirements.txt`): `docs_check.py` with and without git, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base 13eda870` (802 lines, 0 findings) and `check_doc_paths.py`.
   - `ci_scope.py --selftest`, `check_baremetal_only.py --check`, `check_feature_status.py --self-test` and `git diff --check` also return rc 0.
   - The PR body says "Refs #606 / #608 / #75" and contains no closing keyword.

## Findings

### F1 MINOR: the #608 page keeps the #608 reading undecided after the ruling

- **Lenses:** Conformance, Docs.
- **Where:** `docs/findings/608_75_WITHDRAWAL_AND_RESTART.md:17`, `:23` and `:27-35`. The PR body's verdict table repeats the same rows.
- **Authority and evidence:** Maintainer ruling on #608, [5885808887](https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-5885808887).
  - The bar is a withdrawal that reaches an IN registrar (802.1Q-2014 Table 10-4).
  - #608 item 3 is PASS 99 of 99.
  - The LV case is graded separately, in a processor simulation arm.
  - For #75, 99 of 99 demonstrated restarts, with no additional cycle required.

  The page, at this head, still says: "The two readings of #608 item 3 need a decision; this page does not choose". It also grades #75 "at least 100 physical restarts" as NOT MET.
- **Impact:** A durable findings page contradicts the recorded decision. A cold reader sees an open decision and a failed #75 row that the maintainer has already resolved.
- **Required outcome:** The page cites the ruling and grades #608 item 3 and the #75 cycle-count row under it. It names the LV simulation arm as the owner of the LV case. The literal-text reading may remain as history.
- **Verification:** Re-read both verdict tables and the "two readings" paragraph against 5885808887. The Markdown gates stay at rc 0.

### F2 MINOR: the restore proof omits the saved-state layer

- **Lenses:** Conformance, Docs.
- **Where:**
  - `docs/findings/606_FIRST_BIND_MEASUREMENT.md:226-239`;
  - `docs/findings/608_75_WITHDRAWAL_AND_RESTART.md:352-381`.
- **Authority and evidence:**
  - Assignment 5885087413, step 4: "Restore everything as found and prove it."
  - This lane bound and unbound streams. Binding records (ids `0x20`-`0x2F`) are the saved-state writer's records.
  - Lane B1 round 2 recorded the NVM slots and `nvm_pend` at start and end, and found that this layer had not been restored (`599_394_E1_LINK_CYCLES.md` at `931c3edf`, section "Saved-state layer").
  - The packet holds the reads: `identity/console-identity.txt:34-35`, `restore/console-final.txt:39-40`, and `PP_STAT` in every console sample.
  - Neither page mentions them.
- **Impact:** The "all proven" restore claim is silent on the one layer the previous lane showed can stay changed. A reader cannot tell that it ended as found, or that `nvm_pend=1` was already set by lane B1.
- **Required outcome:** Both pages, or the #606 page with a link from the other, record the following at start and end: slot A/B sequence numbers, image sequence, `nvm_pend` (`PP_STAT` bit 11) and commit counts. They should note that `nvm_pend=1` was inherited from lane B1.
- **Verification:** The recorded values match `receipts/holds_epoch_nvm.txt`.

### F3 MINOR: cycle 22's LV window came from the DUT's own LeaveAll-timer deviation, and neither page says so

- **Lenses:** Conformance, Docs.
- **Where:** `docs/findings/608_75_WITHDRAWAL_AND_RESTART.md:33-35` ("a genuine LeaveAll cycle. Cycle 22 is such a cycle") and `:177-197`.
- **Authority and evidence:**
  - IEEE 802.1Q-2014 §10.6 and Table 10-5 (§10.7.9): a received LeaveAll (rLA!) restarts the participant's leavealltimer and suppresses its own LeaveAll.
  - The processor documents that it does not do this, as an open deviation tracked in processor issue #108 (`protocol-processor/docs/architecture/10_srp_engine.md:559-570` at `c951a9ff`).
  - In cycle 22 the bridge's MSRP LeaveAll for all four types crossed the tap at -0.391721 s. The DUT's own LeaveAll followed 0.401121 s later. A conformant participant would not have sent it. The registrar would then have been IN at the `Lv`, and Δ13 would have stopped the stream.
  - Across the session, 67 of 112 captures show a DUT LeaveAll less than 10 s after a received bridge LeaveAll (minimum 0.1996 s; `receipts/leaveall_damping.txt`). The DUT therefore opens roughly twice the LV windows a conformant participant would.
- **Impact:** The page presents the residual non-stop as the standard's behaviour. The ruling's premise ("the standard's behaviour, not a talker defect") holds for the registrar's rLv-in-LV step, but the LV state itself was created by a DUT-side MRP deviation. #608's owner cannot see that closing processor #108 would remove this class of non-stop.
- **Required outcome:**
  - The page records the 0.401 s gap and the #108 deviation in the cycle-22 attribution.
  - The page qualifies "genuine LeaveAll cycle".
  - The conflict with the ruling's premise is published for a maintainer decision.

  This review does not re-grade #608 item 3; the bar is the maintainer's.
- **Verification:** Page text against `receipts/cycle22_and_binds.txt` and `receipts/leaveall_damping.txt`, and a public maintainer disposition.

### F4 MINOR: the archived packet publishes MAC-derived identities

- **Lenses:** Conformance, Docs.
- **Where:** `review-evidence/b2-r1/author` at `2c9f3df2`. Counts are in `receipts/token_scan.txt`, printed masked.
- **Authority and evidence:**
  - The assignment's privacy rule, and this review's brief: no private host, peer, switch, instrument, interface, account or MAC-derived identity in the pages or the archived packet.
  - The packet masks interface, module and home-path strings (four archive redactions plus the author's masking). It does not mask identifiers:
    - two EUI-64 identifiers in the `fffe`-insertion form, in 676 files: the controller host's entity ID in every ACMP state snapshot, and the switch's gPTP clock identity in console and AVB_INFO records;
    - three vendor-prefix 16-hex identifiers, in 665 files: the reference peer's entity and listener stream IDs, and the DUT model ID.
  - Mitigation: the switch clock identity and the peer entity ID already appear in tracked files at dev (for example `docs/findings/117_GPTP_SILICON_EVIDENCE.md` and `tb/tools/hive_compliance.py`). The controller identity already appears in earlier public archives (PR #604's round-3 packet and lane B1's review packet). The pages are clean.
- **Impact:** A MAC-derived identity of the controller host is republished in about 450 files. Tracked documentation has no precedent that makes it public.
- **Required outcome:** One of the following:
  - the archive masks these identifiers, at minimum the controller host's; or
  - a maintainer disposition records that bench AVDECC entity and gPTP clock identities are public.
- **Verification:** Re-run `scripts/token_scan.py` over the re-archived packet. The `eui64-from-mac` and `hex16-vendor` classes are empty or dispositioned.

### Suggestions (non-blocking)

- **S1 (Docs).** `docs/findings/README.md:11`: the #75 row still reads "three non-restarts tracked by #608; initial-bind exception tracked by #606", and neither new page is indexed. The assignment froze "no other doc edits", so scheduling the index update is the maintainer's call.
- **S2 (Docs).** `docs/findings/606_FIRST_BIND_MEASUREMENT.md:19` and `:198` say DUT MSRP "kept a 1.000 s spacing". The baseline and final captures show DUT MSRP PDU spacing of 0.2 s minimum and 1.0 s maximum, the 0.2 s being the join period after a LeaveAll. Suggested wording: "1.000 s periodic spacing, 0.2 s after a LeaveAll."

## Prior public findings on this PR

This is round 1. The PR #622 thread holds only the review-start notice, [5885922821](https://github.com/kebag-logic/milan-fpga/pull/622#issuecomment-5885922821), and no review findings. I read it after my own pass. There is nothing to resolve or retain.

## Per-lens results

- **Conformance: UNCLEAN** (F1, F2, F3, F4).
  - Checked, and correct: the identity gate; the #606 fresh-bind, long-hold and probe results; the #608 IN-bar stops and STREAM_STOP counts; #75 criteria 1-3.
  - Checked against the pinned processor docs, and correct: the page's registrar and gate claims (`T-SRP-DAFRESH` 15 s, `T-ACMP-DA-RETRY` 100 ms, `T-MRP-LEAVE` 4.5-7.5 s from Milan Table 4.3, Δ13, and the aging at transmit acceptance).
- **RTL: CLEAN.**
  - Artifacts: `git diff --raw 13eda870..c37f1d04` (two `.md` files, modes 100644) and the four gitlinks, which equal base (`receipts/clone_integrity.txt`).
  - The processor behaviour the pages cite matches `05_acmp_engine.md:389-399`, `08_timing.md:34,40` and `10_srp_engine.md:423-501` at `c951a9ff`.
  - No RTL or tooling changed, so there is no clock, CDC, width or FSM surface in scope.
  - The pre-existing #108 timer deviation is processor-owned, predates this diff, and is carried as F3's evidence rather than as an RTL change of this PR.
- **Robustness: CLEAN.**
  - Capture integrity: 0 kernel drops in all 112 `capture.txt` records, 0 timestamp reversals, 0 malformed MSRPDUs (per the author's replay, consistent in `analysis.json`).
  - Stop-predicate boundaries: cycle 62's last PDU at +0.001 ms; the 1 ms own-LeaveAll rule; no misclassification at the 0.25 s LeaveAll neighbours (cycles 20, 21, 35, 45, 60, 73 and 88).
  - The inferred-IN bound was measured on every capture, not assumed.
  - Reset epoch 1 across all 112 actions. Non-counter state was equal at start and end.
- **Tests: CLEAN.**
  - This PR adds no executable test.
  - The evidence chain was replayed independently: `scripts/replay_b2.py` FAILS 0 over 100 cycles, 5 binds and 5 unbinds. Raw index, tool hashes, census and long-hold checks all PASS.
  - 7 of 7 planted mutants are rejected and the control passes (`receipts/mutate_replay.txt`). The mutants cover a restart value, two stop classes, a pre-bind declaration count, a first-PDU time, a counter delta, and a packet-side shift of cycle 22's own LeaveAll.
- **Docs: UNCLEAN** (F1, F2, F3, F4). Both pages were read in full against the packet and the issue records. All Markdown gates return rc 0 in the pinned environment (`receipts/gates/`).

## Ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3, F4) | Both pages; issues #606, #608 and #75 with decisions 5860869482 and 5885808887; packet `identity/`, `bind/`, `cycles/`, `restore/`; processor docs at `c951a9ff`; 802.1Q-2014 Tables 10-4 and 10-5 | R404-1 | `c37f1d04e39be0344dfde77e793cdfa441bd4869` |
| RTL | CLEAN | `git diff --raw` base..head; gitlinks; processor `05_acmp_engine.md` §6bis, `08_timing.md`, `10_srp_engine.md` §6.5 at `c951a9ff` | R404-1 | `c37f1d04e39be0344dfde77e793cdfa441bd4869` |
| Robustness | CLEAN | 112 `capture.txt` and `analysis.json`; `receipts/drill_b2.txt`, `holds_epoch_nvm.txt`, `census_check.txt` | R404-1 | `c37f1d04e39be0344dfde77e793cdfa441bd4869` |
| Tests | CLEAN | `receipts/replay_b2.txt`, `mutate_replay.txt`, `capture_hashes.txt`, `tool_hashes.txt` | R404-1 | `c37f1d04e39be0344dfde77e793cdfa441bd4869` |
| Docs | UNCLEAN (F1, F2, F3, F4) | Both pages in full; `docs/findings/README.md`; `receipts/gates/*`; `receipts/token_scan.txt` | R404-1 | `c37f1d04e39be0344dfde77e793cdfa441bd4869` |

## Limits

- **Raw captures not re-parsed.** The raw captures stay outside the public packet, on the build host's scratch area.
  - I did not re-parse them. MSRP and ACMP timing, registrar classes, counters and statistics were recomputed from the packet's per-action `msrp.tsv`, `acmp.tsv` and controller transcripts.
  - AVTP PDU timing (last PDU, hold PDUs, first valid PDU) exists in the packet only as `analysis.json` fields. It was consumed as given and cross-checked for internal consistency.
  - The capture identity chain (index → per-action records → page rows) was checked. The capture bytes were not re-hashed.
- **Not evidence of timestamp accuracy.** Physical calibration was NOT RUN. Printed precision is not calibrated accuracy.
- **No hardware.** No hardware, bench, Docker, act or GitHub write was used.
- **Hosted checks at this head** (`receipts/hosted_checks.txt`).
  - Executed and successful: rtl-fast, docs-check, docs-check-no-git, elaborate, bdd-conformance, wire-accountability, changes, full-ci-gate.
  - Skipped (docs-only scope): verilator-suites, yosys-portability and their shards, verilator-lint, yosys-elaboration, and physical gPTP. Skipped contexts are not proof.
- **Tree-wide banks not re-run.** The manager's source static, builder and native banks were not re-run here, as instructed.
- **Clone untouched.** This clone was never modified: worktree, index, both page blobs, modes and the four gitlinks equal the exact head (`receipts/clone_integrity.txt`).

## Pending manager duties

- Publish this report.
- Route F1-F3 to an author round.
- Decide the conflict in F3 between the ruling's premise and the #108 deviation.
- Dispose of F4 by re-archiving or by a recorded decision.
- Schedule S1 if wanted.
- Obtain the external review.
- Own hosted and act acceptance.
- Build and validate the final current-dev candidate at the merge turn (source base `13eda870`, live dev `57b8c867`).
- Re-cover every lens this report leaves UNCLEAN at the new head, and re-cover any CLEAN lens whose scope a later commit touches.

R404-1 FINISHED
