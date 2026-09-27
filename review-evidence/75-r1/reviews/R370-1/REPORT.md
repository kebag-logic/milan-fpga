[R370] NEGATIVE - exact head 0e8ec0d2bd78b1d87f84d96e095966ae7c07c525

Round R370-1, internal cleared-context review of PR #604 for issue #75, phase 2.
Tree `0e8e3319b58605fb011425dfa1aa90b64935b9c2`, one commit on dev `8bc97021f28fb7f729418d3a00851c84ea0b50fd`.
The diff adds only `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md` (772 lines).
Lenses applied: Conformance, RTL, Robustness, Tests, Docs. RTL is clean. The other four are unclean.
Open findings: 1 BLOCKER, 1 MAJOR, 1 MINOR, plus 4 SUGGESTIONs.

## Reconstruction

The scope comes from these sources, in this order:

1. AGENTS.md and CONTRIBUTING.md, including the seven required contexts at CONTRIBUTING.md:56-57.
2. docs/README.md and docs/findings/README.md.
3. The issue #75 body and its acceptance criteria.
4. The phase-1 disposition (issue comments 5504577387 and 5504891499).
5. The milestone decision (5561827327) and the bench update (5580343075).
6. The phase-2 assignment (5859652809), the operator's TAKEN (5859662625) and REVIEW READY (5860095671).
7. The PR body and the review-start comment (5860116436).
8. The #394 assignment (5858215210) for the assigned image hashes.
9. The diff `8bc97021..0e8ec0d2` and the history.
10. The public operator packet at `a19f2c92e064a1d3998c142eef5bf7d6330add21:review-evidence/75-r1`: tools, the setup, restore and first five cycles per direction, HANDOFF.md, the census files, identity and restore files, and the integrity summary.
11. The exact-head hosted check runs.

## Answers to the review focus

1. **Identity gate, before and after: PASS.** The chain holds up:
   - The assignment's bitstream sha256 `1696d1ea…` and AEM sha256 `9b077636…` match `image-artifacts.json`.
   - `expected-crc.txt` derives ROM `9b6576a9`, flash payload `3c18c276` and AEM `93742dd2` from those files.
   - The DUT UART readback gives those three CRCs before measurement (`identity-uart.txt`) and after it (`final-uart.txt`). VERSION is `0x00020060` both times.
   - The grader passes 10/10 before and after.
   - The image-to-base diff `9e9954e9..8bc97021` reproduces exactly (`receipts/image-to-base-diff.txt`). It touches no product path, and the `protocol-processor` gitlink is `870ff88a` at both ends.
   - The page itself says that the CRC is a consistency check, not a SHA-256 readback of the configured fabric (page:41-42).
2. **Timing method.** The code does what the page claims, with two gaps:
   - Both anchors use the same tap hardware nanosecond word. That is `pkt[16:20]` in `tools/action.py` and `tools/wire_summary.py`. Host time is used only to unwrap the 2^32 ns word. The largest host-to-tap anchor range is 0.107 s, far inside the half-wrap of 2.1 s (`integrity-summary.json`).
   - The live and offline results must agree exactly: `analyze.py` asserts `latency == result['latency_s']`.
   - The response is matched on the tap by message type 7, status 0, sequence and controller ID.
   - A resumed PDU must match the stream ID, tap direction, source, the settled binding's destination, VLAN 2 at PCP 3, the frequency, the length and the interval. The next PDU must advance both sequence and timestamp.
   - **Gap one: "first valid PDU" means the first valid PDU at or after the response, not the first PDU of the resumed stream.** The search starts at the response (`r['ns']>=ack['ns']`). The silence check covers only the 0.5 s before the CONNECT_RX command. It is recorded but never asserted, and it is published for only the ten public cycles. See R370-F2.
   - **Gap two: resolution is not stated.** The resumption instant can only be observed at the CRF PDU period, 2 ms at 500 PDU/s. The validity test also requires `mr = 0` and does not check `tu`. See R370-S2.
3. **Distribution and growth.**
   - My recomputation from HANDOFF.md reproduces every row of the page's distribution, per-cycle, first/last-ten and block tables (`receipts/distribution.txt`, 0 mismatches). The 200 page rows equal the ledger. p95 is the nearest-rank 95th value.
   - The no-growth conclusion holds. Both 95% slope intervals include zero. The upper bounds are +30 ms (listener) and +11 ms (talker) per 100 cycles. Block medians are flat.
   - The talker's negative slope depends on cycle 1 alone: without it the slope is +5.1e-5 s/cycle (`receipts/slope-sensitivity.txt`). See R370-S1.
4. **#75 acceptance verdicts.**
   - The CRF scoping is accurate. It is stated at page:5-6, 185, 496-497 and 501, and the page does not claim AAF.
   - The initial-bind exclusion is disclosed (page:128-146), and its facts check out against `talker-setup/msrp.tsv`:
     - the DUT Talker Advertise first appears at +0.079 s and then every 1 s;
     - a bridge LeaveAll arrives at +6.080 s;
     - the bridge Listener Ready (New) arrives at +6.8886 s;
     - valid CRF follows 0.000793 s later.
   - Two gaps remain. The acceptance rows do not carry the 2 s-hold scope or the excluded measured failure. No public issue owns the 6.889 s cold talker start (R370-F3).
   - For the talker direction, "100 of 100 restarts" is not supported. See R370-F2.
5. **MSRP attribution and bounded traffic: supported.**
   - Per-cycle PDU and LeaveAll sums equal the sender table. The per-type LeaveAll columns equal the vector totals. Per-cycle declaration sums equal the attribute table.
   - For all ten public cycles, recomputing from `msrp.tsv` and `analysis.json` reproduces the page rows. Each shows exactly two MSRP sources and zero parse errors (`receipts/msrp-tables.txt`).
   - Combined rates of 1.75 to 2.51 PDU/s and 1 s bursts of at most 11 and 10 match `integrity-summary.json`. There is no sustained 11 PDU/s storm.
6. **Restore proof: supported.** My independent comparison of `census-start.jsonl` and `census-end.jsonl` (`receipts/census-compare.txt`) shows:
   - all 18 stream states have `conn_count` 0 at both start and end;
   - clock, configuration, sample rate and every descriptor match;
   - the only differences are counters, sequence and RTT values, pdelay noise (383 to 385 ns), and one DUT stream-output destination address (R370-S4).
   - Final CRCs and the 10/10 grader match. The cleanup files record driver, script and interface restoration.
7. **Public hygiene of the page: clean.** It has no absolute paths, IP addresses, MAC or EUI identifiers, serials, host, peer, switch or instrument names, or private-suite names. The only long hex string is the stream format `041060010000bb80`. The operator label is neutral. Observations about the evidence packet, which is outside the PR head, are listed for the manager below.

## Findings

[R370] BLOCKER Docs, Tests - docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:61 - Relative link into the protocol-processor submodule fails both required hosted docs contexts
ID: R370-F1
Requirement/evidence:
- CONTRIBUTING.md:56-57 lists `docs-check` and `docs-check-no-git` among the seven required contexts.
- At the exact head both contexts completed `failure`. In each, `scripts/docs_check.py` reports `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:61: broken link -> ../../protocol-processor/docs/architecture/10_srp_engine.md` (`receipts/hosted-check-runs.txt`).
- I reproduced the failure from a `git archive` of the head, where submodule contents are absent: rc 1 (`receipts/docs-check-without-submodule.txt`).
- The same run on the base `8bc97021` returns rc 0 (`receipts/docs-check-without-submodule-base.txt`). This PR introduces the defect.
- The page's Validation section (page:742-757) and the REVIEW READY both report `docs_check.py` rc 0. That holds only in a worktree whose submodule is populated. My clone also passes there (`receipts/gates-renderer.txt`).
- No other document in the tree links into the submodule this way.

Impact: the PR cannot satisfy the protected merge bar. On github.com the link does not resolve to the cited document. The recorded gate evidence does not reproduce the required context.
Required change: the citation must resolve without the submodule populated, and both hosted docs contexts must pass at the new head. The Validation section must describe gate results that reproduce under the hosted conditions.
Verification: `python3 scripts/docs_check.py` returns 0 on an archive of the new head without submodule contents. `docs-check` and `docs-check-no-git` succeed at the new head.

[R370] MAJOR Conformance, Robustness, Tests, Docs - docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:87-97, 126, 370, 381, 432, 470, 496 - Three DUT-talker "restarts" are not shown to be restarts, and the retained counters contradict 100/100
ID: R370-F2
Requirement/evidence:
- Issue #75 requires at least 100 physical disconnect/reconnect cycles that *resume* the stream. The assignment requires 100 cycles per direction and the DUT counters.
- The public setup and restore snapshots bracket numbered talker cycles 1-100 exactly. Across them, DUT Stream Output 1 STREAM_START goes 18 to 115 and STREAM_STOP goes 17 to 114: +97 each where 100 are expected (`receipts/stream-start-stop.txt`).
- Each of the five public talker cycles advances both counters by exactly 1.
- The reference talker's counters over the listener series advance by exactly +100 and +100.
- The project records these DUT counters as matching wire bursts (docs/findings/117_GPTP_SILICON_EVIDENCE.md:419, 487).
- Exactly three talker cycles report restart values below one CRF PDU period (2 ms): cycle 13 at 0.000364 s (page:370), cycle 24 at 0.000297 s (page:381) and cycle 75 at 0.001864 s (page:432). A stream that is already flowing when the response crosses the tap produces exactly this signature.
- Those three captures rank 6th, 2nd and 3rd by size among the 100 talker captures (chance about 1.2e-4). Cycles 24 and 75 are about 109 KB above the median, roughly one 2 s hold of 500 PDU/s CRF (`receipts/capture-sizes.txt`). Capture duration also varies, so this is corroboration, not proof.
- The acquisition records `frames_last_half_second_disconnected` but does not assert it. Its window ends at the CONNECT_RX command, not at the response, which leaves about 9 ms unchecked in the talker direction.
- The offline search for the first valid PDU starts at the response. A resumed stream that precedes the response, or one that never stopped, therefore yields a sub-period PASS rather than a flag.
- The page's method (page:81-98) does not state the silence precondition. The GET_COUNTERS row (page:470) says "Retained before/after snapshots" and does not report the 97/100 discrepancy.
- The ten public cycles are sound: the inferred stream absence is 1.999 to 2.114 s, and the recorded silence count is 0 (`receipts/public-gap.txt`).

Impact:
- The page and PR claim 100 of 100 DUT-talker reconnect restarts below 1 s. The retained evidence supports 97 counted stop/start pairs.
- If the stream did not stop in those cycles, the talker series measured three non-restarts, and either the DUT kept transmitting about 2 s after Ready withdrawal or Ready was not withdrawn. Both need an owner.
- If the stream did stop, the DUT counters missed three start/stop pairs. That is a counter defect against the documented invariant, and it also needs an owner.
- The talker minimum (0.000297 s) is then a PDU-grid phase, not a restart time.

Required change:
- From the retained per-cycle records, publish for every numbered cycle the valid-PDU count of the bound stream from the disconnect settling up to the CONNECT_RX response. Also publish the per-cycle DUT STREAM_START and STREAM_STOP deltas.
- Explain the 97/100 discrepancy on the page.
- Mark any cycle whose stream did not stop as not a restart. Then either report the direction's count of demonstrated restarts against the 100-cycle requirement, or record a public maintainer decision.
- A DUT behaviour or counter defect exposed by this must be owned by a public issue.
- The method must state the silence precondition, that the response's tap crossing is the anchor, and how a PDU that precedes the response is treated.

Verification:
- The per-cycle values reproduce from the retained `result.json` and `analysis.json`.
- The counter deltas sum to the published figure.
- The talker distribution and acceptance rows count only demonstrated restarts, or they state the decision.

[R370] MINOR Conformance, Docs - docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:128-146, 494-498 - Acceptance rows omit the excluded 6.889 s measured CRF start, and no issue owns it
ID: R370-F3
Requirement/evidence:
- Issue #75 criterion 1 concerns the first valid AVTP PDU within 1 s after a successful (re)connect.
- The initial DUT-talker bind is a measured CRF CONNECT_RX-to-first-valid-PDU interval of 6.889398468 s (`talker-setup/analysis.json`). The page discloses it and excludes it from quantiles (page:128-146).
- The page states no basis for the exclusion. The basis is the assignment's cycle definition, a disconnect then a 2 s hold, whereas the initial bind registers a Talker Advertise cold: the DUT's first declaration comes 0.079 s after the response.
- The acceptance rows (page:496-497) read "PASS for measured CRF". They do not mention the 2 s-hold condition or the measured failure.
- AGENTS.md section 4 says newly discovered work becomes a public issue. A search of open and closed issues finds none for this observation. The page (page:146) names only the need for a peer-side capture.
- The capture also shows that the DUT never used `New` for this Talker Advertise, including its first declaration. Only `JoinMt` and `Mt` appear, while the bridge uses `New` for its own new declarations. This is recorded here as a lead for the owner, not as a defect.

Impact: a reader or a closing decision on #75 can take "PASS for measured CRF" to cover every measured CRF start, while a 6.9x overrun of the bound has no owner and can be lost.
Required change: scope the acceptance rows to numbered reconnect cycles after a 2 s unbound hold, and cross-reference the initial-bind failure. State the basis for the exclusion. Link a public issue that owns the cold DUT-talker start, or a recorded maintainer decision that places it.
Verification: the page re-read shows the scoped rows and the stated basis, and the linked issue resolves.

### Suggestions (do not affect lens coverage)

[R370] SUGGESTION Tests, Docs - docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:153-156, 181-184 - Report slope intervals, not only the slope sign
ID: R370-S1
- The talker slope is negative only because of cycle 1. Without cycle 1 it is +5.1e-5 s/cycle.
- Both 95% intervals include zero (`receipts/slope-sensitivity.txt`).
- The no-growth conclusion stands on the block table and the intervals. The page could present those as the evidence.

[R370] SUGGESTION Conformance, Docs - docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:93-103 - State resolution and the full validity predicate
ID: R370-S2
- The resumption instant is observable only at the 2 ms CRF PDU period.
- The anchor is the response's crossing of the tap, not its receipt at the controller.
- Validity also requires `mr = 0` and does not examine `tu`.
- None of these changes a verdict, given the 0.205 s maximum against a 1 s bound.

[R370] SUGGESTION Docs - docs/findings/README.md:9-17 - Add the new page to "Current entries"
ID: R370-S3
- The immediately preceding finding (397) added its own row. This page is reachable only by a direct path.

[R370] SUGGESTION Docs - docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:475-479 - Disclose the one non-setting state difference after restore
ID: R370-S4
- DUT Stream Output 1 GET_TX_STATE reports an all-zero destination address at the start census and a MAAP-range address at the end (`receipts/census-compare.txt`).
- It is dynamic state, not a setting, but the restore statement could name it.

## Clean-lens evidence

[R370] PASS RTL - `git diff --stat 8bc97021..0e8ec0d2`; `receipts/image-to-base-diff.txt`; protocol-processor gitlink `870ff88a` at 9e9954e9, 8bc97021 and head; protocol-processor/docs/architecture/10_srp_engine.md:423,520-523; docs/reference/REGISTER_MAP.md:1069,1180,1236,2242; `git cat-file -e eb375c13:hdl/ieee8021q/srp/KL_lwsrp_ctx.sv` - The checks and their results:
- The diff contains no RTL, and the image-to-base diff contains no product path.
- The page's architecture claims hold:
  - The retired lwSRP context exists only in history at `eb375c13` and is absent at head.
  - The current SRP design documents the open received-LeaveAll timer deviation.
  - Counter words 0x650, 0x69C and 0x6B0 are structural zeros, and 0x930 is the aggregate PP_DIAG word, as the page states.
- No module or interface contract is changed or contradicted.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2 MAJOR, F3 MINOR) | #75 body and acceptance; assignment 5859652809; page:5-6, 81-146, 492-501; HANDOFF.md 200-row ledger; `talker-setup/{analysis.json,msrp.tsv}`; setup/restore/cycle 1-5 snapshots | R370-1 | 0e8ec0d2bd78b1d87f84d96e095966ae7c07c525 |
| RTL | CLEAN | diff stat; image-to-base diff; gitlinks; 10_srp_engine.md:423-523; REGISTER_MAP.md:1069,1180,1236,2242; history `eb375c13` | R370-1 | 0e8ec0d2bd78b1d87f84d96e095966ae7c07c525 |
| Robustness | UNCLEAN (F2 MAJOR) | `tools/action.py` (silence window, 30 s cap, early stop, missing-response assert); `tools/analyze.py` (search start, validity, progression assert); `tools/wire_summary.py` (unwrap); `integrity-summary.json`; public cycle `result.json` | R370-1 | 0e8ec0d2bd78b1d87f84d96e095966ae7c07c525 |
| Tests | UNCLEAN (F1 BLOCKER, F2 MAJOR) | nine assigned gates at head (`receipts/gates.txt`, `receipts/gates-renderer.txt`); hosted check runs; no-submodule reproduction on head and base; my recomputations `scripts/*.py` with `receipts/*.txt` | R370-1 | 0e8ec0d2bd78b1d87f84d96e095966ae7c07c525 |
| Docs | UNCLEAN (F1 BLOCKER, F2 MAJOR, F3 MINOR) | whole page (1-773) including links and hygiene scan; docs/findings/README.md; TESTING.md 6b; PR body; REVIEW READY | R370-1 | 0e8ec0d2bd78b1d87f84d96e095966ae7c07c525 |

Prior public review findings on PR #604: none. I checked only after this verdict and ledger were written. The PR has two review-start notices (R370-1 and the parallel external R371-1), no review bodies and no review comments. There is nothing to resolve or retain.

## Real limits

- The 190 per-cycle records outside cycles 1-5 and every raw capture are private. I checked them only through the page, HANDOFF.md, the aggregate manifests and the bracketing setup and restore snapshots. I replayed no capture.
- Settling F2 needs the private `result.json`, `analysis.json` and snapshot files for talker cycles 13, 24 and 75 at least.
- The hypothesis tying the counter deficit to those three cycles is inferred. It is not observed.
- The identity chain relies on the operator's local file hashes and CRC32 readback. No configured-fabric SHA-256 readback exists.
- Physical calibration of the tap timestamp was not run. Printed nanosecond precision is not a calibration claim.
- Hosted contexts `verilator-suites`, `yosys-portability`, `verilator-lint`, `yosys-elaboration`, their shards and the physical gPTP job were skipped at this head. Those skips are not hardware or RTL proof.
- No RTL changed, so no simulator run was needed and none was made. No bench action, Docker, local CI replica, source edit, commit, push or GitHub write was made.
- The clone was verified at exact head afterwards (`receipts/clone-integrity.txt`):
  - HEAD, tree, index modes and blobs are identical to the HEAD tree;
  - the worktree is clean;
  - gitlinks are unchanged;
  - a gate-created ignored bytecode cache was removed.

## Pending manager duties

- Hosted acceptance at the next head, including `docs-check` and `docs-check-no-git` (F1). Local replica acceptance and candidate-merge validation against live dev.
- A decision on whether #75 may close on CRF-only evidence. AAF is unmeasured, and the page states this.
- **Observation outside the PR head, for the manager's decision.** The published operator packet (`review-evidence/75-r1`) contains:
  - identifiers that the assignment's hygiene rule for public evidence arguably covers: MAC and EUI-64 values carrying a vendor-assigned OUI for the bridge, the reference peer and the gPTP grandmaster, and a controller entity ID derived from a host NIC address;
  - absolute private paths under a temporary directory, in README, METHOD-NOTES, tools and `raw-artifacts.json`;
  - a lane-root variable and a site-local command-wrapper name in the tools.

  This report does not reproduce those values.

R370-1 FINISHED
