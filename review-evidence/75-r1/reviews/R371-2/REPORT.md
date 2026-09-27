[R371] NEGATIVE - exact head 5c7577e51702b00683a121f97a9806c167eb072b

External independent review, round R371-2, of issue #75 phase 2 / PR #604.
Head `5c7577e51702b00683a121f97a9806c167eb072b`, tree `e817bda49b6ed644a94c39f07b72762411c0b8dc`, parent `0e8ec0d2bd78b1d87f84d96e095966ae7c07c525`, source base `8bc97021f28fb7f729418d3a00851c84ea0b50fd`. The round-2 delta (`0e8ec0d2..5c7577e5`) changes two files: `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md` (+444/-36) and `docs/findings/README.md` (+1). No RTL, firmware, tooling or gitlink path changes.

Round 2 fixes all four of my round-1 findings and all three round-1 findings from the other review. My own stop-check probe runs on the recorded data. It reproduces the reclassification exactly: 100 listener and 97 talker demonstrated restarts, non-restarts talker 13, 24 and 75. It also reproduces the recomputed quantiles, slope intervals and blocks, and the +97/+97 and +100/+100 counter reconciliation. Planted faults make it fail. The docs gate passes with submodules, without submodules and without Git metadata, and restoring the old relative link makes it fail again.

The verdict is NEGATIVE for one new MINOR finding (F5). The three talker non-restarts are a new observation of this round: the DUT kept transmitting through a successful disconnect. The page gives them neither the tapped attribution the recorded data supports nor a recorded owner. Conformance, Robustness and Docs stay unclean. RTL and Tests are clean.

## Reconstruction (public state only)

- Read: AGENTS.md; CONTRIBUTING.md; docs/README.md; issue #75 body and comments, including the phase-2 assignment 5859652809, the round-2 assignment 5860261220, the [A389] TAKEN and REVIEW READY comments, and the review-start comment 5860438976; issue #606; PR #604 body and metadata (not draft, base `dev`, head `5c7577e5`, "Refs #75"); `git diff 8bc97021..5c7577e5` and `git diff 0e8ec0d2..5c7577e5`; commit messages (one line each, no trailers, no closing keyword); the whole page at head (1181 lines) and `docs/findings/README.md`.
- Evidence: branch `75-review-evidence` at `8791bfa486e4504e7464ca6db3f98f77b57f7c03`, which descends from the round-1 packet commit `a19f2c92`. I used `review-evidence/75-r1/author/` (round-1 operator packet) and `review-evidence/75-r1/author-r2/` (round-2 addendum; `MANIFEST.sha256` verifies). I read the other reviewer's round-1 report only after my own pass and draft findings were complete.
- My own round-1 report (R371-1, PR comment 5860251418) is the baseline for the focus items.

## Focus-item verification

1. **No page link points into a submodule; docs-check passes with and without submodules: RESOLVED.**
   - The page has 12 external or relative links, and none resolves into `external/`, `gptp-processor/`, `protocol-processor/` or `third_party/verilog-axis/` (`receipts/link_audit.txt`).
   - Line 64 now cites the protocol-processor remote pinned at `870ff88a`. That is the gitlink at head. The cited blob `23c5bd4b` is identical to `protocol-processor:870ff88a:docs/architecture/10_srp_engine.md`, and it still carries the open received-LeaveAll deviation (lines 423 and 520-523).
   - `scripts/docs_check.py` returns 0 in three contexts: in the review clone with its populated submodules, in a fresh no-submodule clone at the exact head, and in a no-Git export (`receipts/gates_with_submodules.txt`, `receipts/gates_without_submodules.txt`, `receipts/gates_without_git.txt`).
   - Negative control: putting the old relative link back in the disposable no-submodule clone gives `broken link`, rc 1 (`receipts/link_audit.txt`).
2. **Every sub-PDU-period interval has a recorded stop check, and the reclassification holds: RESOLVED.** One new issue, F5, is below.
   - `stop_probe.py` is my own code. It does not use the author's `recompute.py`. It runs on the recorded ledger `author-r2/stop-checks.csv`, the public per-cycle records, the setup and restore snapshots, and the page (`receipts/stop_probe.txt`, 0 failing checks):
     - Window arithmetic holds for all 200 rows: settle start = disconnect response + 0.5 s, hold at least 2 s, settled count = settled-to-command + command-to-response, latency = first PDU minus response.
     - My wire rule (zero valid target PDUs from settle start up to the response, and first post-settle PDU at or after the response) gives RESTART for exactly 197 rows. The non-restarts are exactly talker 13, 24 and 75.
     - The counters independently give +1/+1 for every restart and 0/0 for every non-restart.
     - Every accepted restart shows a silent gap spanning settle start to response, with a final-half-second count of 0. The stream's last PDU falls at most 98.8 ms (talker) or 189.5 ms (listener) after the disconnect response, well inside the 0.5 s settle allowance.
     - The three non-restarts carry 754, 754 and 755 settled PDUs against 754.5-754.7 expected at 500 PDU/s, and 1000 hold PDUs each. Their maximum hold gap is 2.000053 ms and their DUT counters stay at 0/0, so the stream never stopped.
   - Quantiles I recompute from demonstrated restarts only:
     - Listener, n=100: 0.006641 / 0.110280 / 0.188503 / 0.204859.
     - Talker, n=97: 0.017427 / 0.019175 / 0.042347 / 0.117736, nearest-rank p95.
     - Both equal page line 175-176.
     - The stated effect is right: the minimum moves from 0.000297 to 0.017427 s and the maximum is unchanged (lines 184-187).
   - The retained counters reconcile:
     - Talker: DUT output 1 goes 18/17 at setup to 115/114 before restore, +97/+97. That equals the ledger sum and the count of demonstrated restarts.
     - Listener: reference output 2 goes 12/11 to 112/111, +100/+100.
     - The inactive DUT output is unchanged in all 100 listener cycles.
     - Page lines 831-846 are correct.
   - Cross-checks:
     - For the public cycles 1-5 in each direction, the ledger matches `result.json`, `analysis.json` and the snapshot counters: anchors, latency, final-half-second count, PDU total, deltas and cycle-to-cycle continuity. All ten are listed in `author-r2/input-hashes.csv` with matching sha256.
     - For all 200 captures, the sha256 and size agree across the ledger, `RAW-ARTIFACTS.json` and the page index.
     - The capture-size identity holds for all 200: bytes = 24 + 108 x CRF PDUs + other. The six-largest table (lines 806-813) matches.
     - `mr`, `fs` and `tu` are zero in every target PDU.
   - Mutation controls (`receipts/mutations.txt`). The probe fails on each planted fault:
     - one PDU planted in a restart's hold fails 9 checks;
     - a start/stop pair planted on a non-restart fails 3 checks;
     - a 1 microsecond shift in one restart latency fails 6 checks.
     - The author's `assert_stop` rejects a non-zero hold count and a pre-response resumption.
3. **Acceptance scope and the initial bind: RESOLVED.**
   - Rows 1-2 of the acceptance table (lines 875-876) are scoped to the two CRF pairs and the `DISCONNECT_RX`, two-second hold, `CONNECT_RX` sequence.
   - Row 3 (line 877) records the 6.889398 s initial DUT-talker bind as an open exception linked to #606. The rationale is stated: no preceding disconnect or hold, so it forms a separate population under the recorded decision.
   - Row 4 (line 878) records talker 97/100 as NOT MET.
   - Lines 211-225 record the DUT-side difference: no DUT Talker Advertise before the bind, the first one +0.079 s after the response, and the bridge silent until its LeaveAll at +6.080 s. Line 223 says the wait cannot all be attributed to the peer.
   - `initial_bind_check.py` confirms every figure against the public `talker-setup` records and `author-r2/disclosures.json` source hashes (`receipts/initial_bind_check.txt`): latency 6.889398468 s; no DUT Talker Advertise before the response; first bridge MSRP a LeaveAll at +6.080007742 s; Ready at +6.888605306 s; CRF 0.000793162 s later; listener initial bind 0.198316 s.
4. **Index, slope intervals, resolution and validity predicate, restore difference; #75 stays open: RESOLVED.**
   - The index row is at `docs/findings/README.md:11`.
   - The slope intervals (lines 234-250) equal my OLS/Student-t recomputation. I compute t numerically at df 98 and 95, and the talker slope without cycle 1 is +0.000040905.
   - Lines 121-136 state the resolution: a 1 ns tap word, the 2 ms PDU cadence, unwrap spread 0.106533 s against the half-wrap, and no calibration claim.
   - Lines 101-116 state the validity predicate. Its rows match `recompute.py` term by term, and it correctly says the `0xf0` mask leaves `mr`, `fs` and `tu` unchecked, while the replay records them zero.
   - Lines 851-855 state the restore residue. My census comparison finds exactly one differing field in 18 state keys: DUT `state-6-1` destination, all-zero to MAAP-range. All 18 states are unbound.
   - The PR says "Refs #75", no commit closes it, and #75 is OPEN.
5. **Public hygiene of the round-2 addendum, page and PR body: CLEAN** (`receipts/hygiene_scan.txt`).
   - None of the three contains an absolute or temporary path, the site-local command-wrapper name, the lane-root variable, a host, instrument, vendor or tool name, a MAC address, an entity or clock identifier, or a serial.
   - The scanner does flag some hex strings, and none is an identifier: 16-hex-digit runs inside float digits in `recomputed-summary.json`, the all-zero placeholder in `verify_disclosures.py`, and the page's stream format.
   - Positive control: the same scanner still finds the wrapper name, lane variable and temporary paths in the unchanged round-1 `author/tools`, which the round-2 decision leaves as is.

## Findings

### F5 - MINOR - Conformance, Robustness, Docs - `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:574-586, 878`; `docs/findings/README.md:11` - The three talker non-restarts are left unattributed and without a recorded owner, although the recorded data points to DUT-side behaviour

- **Authority/evidence.**
  - AGENTS.md section 4: newly discovered work becomes a public Issue. Section 2: when scope is unclear, publish the conflict and ask for a decision rather than choose one privately.
  - The round-2 decision (issue #75 comment 5860261220) required recording the DUT-side difference for the initial bind, not attributing it only to the peer. It gave the first-bind path to #606. It predates this round's discovery that three talker attempts never stopped, so it decided nothing about them.
  - At head the page says only "No stopped stream, early resumption, or counter mismatch is demonstrated", "#75 retains this behavior" and "The follow-up must establish why transmission continued through disconnect" (lines 581-586). No follow-up is named, and no open issue covers the behaviour (issue search, 2026-09-27).
  - The recorded tapped data localizes the non-stop more than the page says (`receipts/stop_probe.txt`, section 8):
    - In each public talker cycle (1-5), exactly one bridge Listener `Lv` crosses the tap 9.5-11.0 ms after the disconnect response. The DUT's stream stops within one PDU period of it.
    - Across all 97 demonstrated talker restarts, the median stop falls 9.1 ms after the disconnect response. So the DUT's stop is driven by the Listener withdrawal. No ACMP DISCONNECT_TX appears on the tap (`acmp_wire_counts`).
    - The page's own attribution table records 100 bridge Listener `Lv` across the 100 talker captures (line 341).
    - The per-cycle MSRP profiles of cycles 13 and 75 are identical to restart cycles 42, 54, 59 and 90. Cycle 24's profile is identical to restart cycles 36 and 80 (lines 469, 480, 531 against 492, 498, 510, 515, 536, 546).
    - So the tapped record indicates that the bridge's Listener withdrawal reached the DUT's segment in the three non-restart cycles too. The DUT then kept transmitting about 1000 PDUs through the hold without incrementing STREAM_STOP.
  - The public packet does not contain those three cycles' `msrp.tsv`. The page neither states nor publishes what they show.
- **Impact.**
  - A possible DUT talker defect is recorded only as a counting shortfall against #75's 100-cycle requirement. #75 is a restart-latency issue. The defect is a stream that keeps transmitting after its listener registration is withdrawn, in 3 of 100 disconnects, and it holds a reservation and bandwidth.
  - Re-running the bench, which #75 needs anyway, would hit the same behaviour with no owner and no localization.
  - It is the same shape as the round-1 initial-bind gap, now for a second population.
- **Required outcome.**
  - From the retained per-cycle records of talker cycles 13, 24 and 75, the page (or the addendum it links) states whether and when the bridge Listener `Lv` and any Listener re-declaration crossed the tap, relative to the disconnect response and the continuing stream. It then states the attribution the tapped segment supports (DUT-side, upstream, or undetermined, with the reason).
  - The supporting per-cycle records are published so a reviewer can check the statement. They are small and scrubbable, as the cycles 1-5 records already are.
  - A public owner is recorded, either a new Issue linked from the Stop checks section, the acceptance row and the index row, or a maintainer decision on #75 that places this behaviour there.
- **Verification.** At the new head the three cycles' Listener events and the stated attribution are in the page or addendum and match the published records. The linked Issue or decision resolves and names cycles 13, 24 and 75.

### Suggestions (optional; they do not affect coverage)

- **S5 - Tests - `author-r2/recompute.py` (`assert_stop` inside `try/except AssertionError`; `assert rejected == [...]`).** The replay's RESTART/NOT_RESTART verdict is computed by catching `AssertionError`. Under `python3 -O` or `PYTHONOPTIMIZE`, every `assert` is stripped, so all 200 attempts would classify as RESTART with no error, silently reproducing the withdrawn round-1 result. The addendum README warns about this. A plain `if` for the classification and the consistency checks, plus a refusal when `sys.flags.optimize` is set, would make the evidence tool fail closed. The hard-coded expected rejection list is a consistency check, not a classifier. My independent probe does not depend on either construct.
- **S6 - Docs - page line 214.** "It then repeats every second while Ready remains absent" slightly simplifies the record. The DUT's Talker Advertise declarations are spaced 0.2 s, then 1.0 s six times, then 0.2 s after the bridge LeaveAll (`receipts/initial_bind_check.txt`). #606 may want the exact cadence.

## Prior public review findings on PR #604: resolved or retained at this head

| Finding | Status at `5c7577e5` | Evidence |
|---|---|---|
| R371-1 F3 BLOCKER (submodule link breaks docs gates) | RESOLVED | Pinned upstream URL at line 64; docs_check rc 0 with, without submodules and without Git; negative control rc 1 (`receipts/link_audit.txt`, `receipts/gates_*.txt`) |
| R371-1 F1 MAJOR (criterion 1 PASS despite 6.889 s bind; no follow-up) | RESOLVED | Acceptance rows 875-878 scoped; exception row linked to #606 with rationale; DUT-side difference at 211-225; figures verified (`receipts/initial_bind_check.txt`) |
| R371-1 F2 MINOR (sub-period cycles not shown stopped) | RESOLVED; follow-on attribution and owner gap raised as F5 | All 200 stop checks published (588-789); 13/24/75 reclassified; quantiles recomputed; size excess explained (791-813); `receipts/stop_probe.txt` |
| R371-1 F4 MINOR (findings index) | RESOLVED | `docs/findings/README.md:11` |
| R371-1 S1-S3 (timing bound, slope intervals, restore residue) | Taken | Lines 121-136, 234-250, 851-855 |
| R371-1 S4 (restart decomposition) | Not taken; optional | none |
| R370-1 F1 BLOCKER (submodule link) | RESOLVED | as R371-1 F3 |
| R370-1 F2 MAJOR (three talker restarts not shown; counters 97/100) | RESOLVED for the per-cycle counts, deltas, reconciliation, reclassification and method statement (lines 138-153, 558-586, 831-846). Its requirement that an exposed DUT behaviour be owned by a public issue remains open under F5 | `receipts/stop_probe.txt` |
| R370-1 F3 MINOR (acceptance rows omit 6.889 s; no owner) | RESOLVED | #606 exists and is linked; rows scoped |
| R370-1 S1-S4 | Taken | S2's statement that the mask requires `mr = 0` is corrected at lines 115-116; the `0xf0` mask covers only `sv` and version, which I confirmed against the CRF header layout used in `recompute.py` |

## Clean-lens evidence

[R371] PASS RTL - `git diff --stat 8bc97021..5c7577e5` (two Markdown files only); gitlinks at head (`receipts/clone_integrity.txt`); page lines 50-66 against `protocol-processor` blob `23c5bd4b` at gitlink `870ff88a` (lines 423, 520-523) and the retired `hdl/ieee8021q/srp/KL_lwsrp_ctx.sv` at `eb375c13` - No RTL, firmware, constraint or gitlink change. The page's architecture statements (retired context module, replacement SRP engine, open received-LeaveAll timer deviation) still match their pinned sources. F5 concerns a possible behaviour of the shipped DUT that this PR neither changes nor describes as RTL, so the RTL lens has no open item at this head.

[R371] PASS Tests - `receipts/gates_with_submodules.txt`, `receipts/gates_without_submodules.txt`, `receipts/gates_without_git.txt` (the nine assigned gates plus the `check_doc_style.py --selftest` and committed-diff `git diff --check`, all rc 0, pinned renderer from `tools/markdown/requirements.txt` in a disposable environment); negative control in `receipts/link_audit.txt`; `author-r2/recompute.py` logic read against my independent `stop_probe.py` (0 failing checks) and its mutation controls (`receipts/mutations.txt`) - The round-2 stop assertion can fail for the defect it claims to detect (planted PDU, planted counter pair, latency shift), and it agrees with the wire/counter redundancy. The docs gate reproduces in the hosted conditions.

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F5) | #75 criteria and round-2 decision 5860261220 against page lines 171-225 and 873-882; #606 body; `author-r2/stop-checks.csv`; public talker cycle `msrp.tsv`/`analysis.json`; `receipts/stop_probe.txt`, `receipts/initial_bind_check.txt` | R371-2 | `5c7577e51702b00683a121f97a9806c167eb072b` |
| RTL | CLEAN | diff stat (docs only); gitlinks; page lines 50-66 against pinned `10_srp_engine.md` blob `23c5bd4b` and history `eb375c13` | R371-2 | `5c7577e51702b00683a121f97a9806c167eb072b` |
| Robustness | UNCLEAN (F5) | non-restart continuity (hold PDUs, gaps, counters), settle-allowance adequacy (stop at most 189.5 ms after disconnect), pre-response resumption rule (lines 149-153), unwrap bound, initial-bind state path, restore residue (`receipts/stop_probe.txt`, `receipts/initial_bind_check.txt`) | R371-2 | `5c7577e51702b00683a121f97a9806c167eb072b` |
| Tests | CLEAN | gates with, without submodules and without Git; negative link control; `recompute.py` against independent probe; three mutations; author `assert_stop` controls | R371-2 | `5c7577e51702b00683a121f97a9806c167eb072b` |
| Docs | UNCLEAN (F5) | the whole page (1181 lines) and `docs/findings/README.md`; link audit; every page table recomputed or cross-checked (distribution, growth, 20 blocks, 200-row cycle and stop tables, six-largest, capture index); PR body; addendum README/HANDOFF/disclosures; hygiene scan | R371-2 | `5c7577e51702b00683a121f97a9806c167eb072b` |

RTL and Tests are clean at this head. Conformance, Robustness and Docs have to be covered clean again once F5 is fixed.

## Real limits

- All raw captures are private, and so are the per-cycle records outside cycles 1-5 in each direction. I did not replay any capture. My probe checks the ledger's per-PDU window counts through internal arithmetic, the 500 PDU/s expectation, the independent counter redundancy, and the public cycles 1-5. It cannot re-derive those counts for cycles 6-100.
- F5's inference that a bridge Listener `Lv` was present in cycles 13, 24 and 75 rests on the page's aggregate count and identical per-cycle profiles. I did not observe it directly, and F5 asks the author to state the direct record.
- There was no bench access. Physical calibration of the tap clock was NOT RUN. Hosted skipped contexts and field skips are not hardware proof.
- The pinned Verilator was not used, because the round-2 delta has no RTL. No parent, protocol-processor, gPTP, Yosys or builder bank was run.
- Hosted check runs at this head (read-only snapshot, `receipts/hosted_check_runs.txt`, 2026-09-27T22:42Z) are 14 success, 1 skipped (physical gPTP) and 5 in progress: `docs-check`, `elaborate` and three Verilator shards. `docs-check-no-git`, `rtl-fast`, `verilator-lint`, `yosys-elaboration`, the four Yosys shards and two Verilator shards had succeeded. I do not treat this as acceptance.

## Pending manager duties

- Hosted and act acceptance at the exact head, including completion of `docs-check`, `elaborate` and the remaining Verilator shards.
- Candidate-merge validation against live dev (`20aa4eab`) at the merge turn. Source base `8bc97021` is distinct from it.
- The ownership decision F5 asks for, if the owner is to be #75 rather than a new issue.
- The unchanged round-1 packet `author/` still carries the wrapper name, the lane-root variable and temporary paths in its tools. The round-2 decision leaves that packet as is. This is recorded for the publisher and is not a finding against the PR head.

## Clone state

No tracked file was modified. The gate runs created an ignored `scripts/__pycache__`, which I removed after checking that every entry was newer than this review's start. HEAD is `5c7577e5`, `git write-tree` equals tree `e817bda4`, `ls-files -s` equals `ls-tree` for all 945 entries (modes and blob ids), and there are zero porcelain entries including ignored and untracked. The gitlinks are unchanged (`external efeb541a` uninitialized, `gptp-processor 5dce647a`, `protocol-processor 870ff88a`, `third_party/verilog-axis 48ff7a7e`), and the submodule worktrees are clean (`receipts/clone_integrity.txt`). Probe copies ran only under the packet's scratch directory, which is not published.

R371-2 FINISHED
