[R728] POSITIVE - exact head 2b1565fd9095d6ec8be514849ba9b92b8f4c5b31

# R728-2: external review of PR #805 (issue #803, gPTP pin f97c1803), round 2 delta

- Exact head `2b1565fd9095d6ec8be514849ba9b92b8f4c5b31`, tree `367ade28eae1646e43cac428f797db9136d59450`. Delta reviewed: `fb182b19..2b1565fd` (six commits, 15 files, +117/-60). Source base and live dev: `5fcec84b1aa72c43048eff28bb63a982add830dd`.
- Verdict: POSITIVE. No BLOCKER, MAJOR, MINOR or RESIDUE is open. All six prior findings (R727-1 F1, F2, R1, S1; R728-1 F1, S1) are resolved at this head. Two SUGGESTIONs follow; neither affects coverage.
- All five lenses applied and clean at this head.

## Reconstruction order

1. AGENTS.md, then CONTRIBUTING.md through AGENTS.md's precedence rule.
2. Issue #803 body (acceptance: all consumer gates rc 0; FPGA-gPTP #87-#91 close after an image passes) and the round 2 ruling (issuecomment-6483128755, items 1-6 and its STOP rule).
3. `docs/reference/REGISTER_MAP.md:330-333` (the response snapshot, IEEE 1722.1-2021 7.4.41.2), the RTL it describes (`hdl/milan/milan_datapath.sv:6011-6073, 6300-6310, 6398-6399`), the processor's gather hold (`protocol-processor/hdl/aecp/KL_aecp_engine.sv:2400, 2447-2457`) and the engine queue and bank (`gptp-processor/hdl/top/KL_gptp_engine.sv:200-255`).
4. `git diff fb182b19 2b1565fd`, its six commits, and `git diff --stat 5fcec84b 2b1565fd` for the scope claims.
5. Published evidence at `09a8771f`, `review-evidence/803-r1/author-r2/` (index and 14 receipts hash-checked), the PR body and the exact-head hosted check runs.
6. Only after my own pass: the R727-1 and R728-1 findings on this PR.

## What I ran (exact head bytes; disposable copies only)

Four tracked-file copies of the clone (`clean`, `m9`, `m9b`, `m9c`), two more from `clean` (`h1`, `h2`). Each leg was built fresh with the pinned Verilator 5.050 (`receipts/verilator_identity.txt`) and run in full. The clean copy's `sim_gptp.cpp` and `milan_datapath.sv` blob ids equal the head's (`receipts/clean_copy_identity.txt`).

| Copy | Planted defect (diff) | Leg | Result (`receipts/legs/*.summary.txt`) |
|---|---|---|---|
| clean | none | `gptp` | rc 0, `202 checks: 202 PASS, 0 FAIL`; `[cut] count beat held 474 cycles; commit seen 1; path-entry request before the commit 0`; `[#207] full-queue window: level 1, rp 1->1, wp 2->2` |
| clean | none | `gptp-lat` | rc 0, `202 checks: 202 PASS, 0 FAIL`; same `[cut]` and `[#207]` lines |
| m9 | entry 0 from `asp_live_head_w` (`receipts/probe-r728-m9.diff`) | `gptp` | rc 2, 201/202: `FAIL in-flight response remains wholly old GM got 02a1b2fffec3d4e5 exp 00aaccfffe010204` |
| m9b | entries 1..7 from `asp_live_path_w` (`probe-r728-m9b.diff`) | `gptp` | rc 2, 201/202: `FAIL in-flight response remains wholly old: ends with thisClock got 0000000000000000 exp 02a1b2fffec3d4e5` |
| m9c | count from `asp_live_count_w` (`probe-r728-m9c.diff`) | `gptp` | rc 2, 200/202: `... wholly old count two got 1 exp 2`; `... ends with thisClock got 0 exp 02a1b2fffec3d4e5` |
| h1 | harness: no count-beat hold (`probe-r728-h1.diff`) | `gptp` | rc 2, 201/202: `path-entry request before the commit 1`; `FAIL empty path commits after first-count snapshot, before entry gather` |
| h2 | harness: no second Pdelay_Req at the queue head (`probe-r728-h2.diff`) | `gptp` | rc 2, 194/202: `rp 1->0` (three stale pops); `FAIL the full-queue window pops and pushes no event`, then seven later `#88` checks fail |

My m9 and m9b edits are byte-identical to the published `probe-m9.diff` and `probe-m9b.diff` (R727-1 packet), compared after I had planted mine.

Other commands at the head, all in the review clone: `scripts/ci_events.py --check` rc 0 (2199 contract items, 4 workflow files and the policy page); `scripts/ci_events.py --selftest` rc 0 (`selftest: PASS (2199 contract items, 5258 arms)`); `scripts/measure_test_evidence.py --selftest` rc 0 (`105 checks: 105 PASS, 0 FAIL`); `check_doc_style.py` rc 0; `docs_check.py` rc 0. The clone ends byte-exact: HEAD and index tree `367ade28`, porcelain empty, six gitlinks as recorded (`receipts/clone_integrity.txt`).

## The ruling's items, checked

1. **F1, the GET_AS_PATH snapshot check.** Resolved.
   - The arm sets `hold_gsi_beat` once `asp_resp_capture_w` has been seen (`tb/verilator/milan_dp/sim_gptp.cpp:1462-1482`). The tick hook clears `gsi_srv1_r` on every cycle (`:426-428`), so `gsi_srv2_r` never completes the count beat. The processor HOLDs it inside its bounded gather wait (`KL_aecp_engine.sv:2400, 2454`; 4096 cycles by default, `milan_datapath.sv:350`). The beat is held 474 cycles and the poll is bounded at 3000.
   - The new check `empty path commits after first-count snapshot, before entry gather` (`:1497`) requires both the commit and no `asp_resp_entry_w` since capture. So the publication lands between the snapshot and the gather, as the RTL comment at `milan_datapath.sv:6032-6035` requires. h1 proves the check can fail.
   - m9 and m9b each print FAIL on a named check, one at a time. m9c (count served live) fails as well, which backs the comment's "count, entry 0 or entries 1..7" claim. A new entry-1 check (`:1504`) is the one that catches m9b.
   - The clean `gptp` and `gptp-lat` legs pass every check. They now have 202 checks rather than 200: the two checks this round adds, as the PR body says.
   - The arm comments (`:1424-1430, 1474-1480`) now state what the arm proves. The old claim "These checks kill torn-response mutations" is gone.
2. **F2, the adoption record's scope.** Resolved. `docs/reference/SUBMODULES.md:310-314` and `CHANGELOG.md:72-75` say: no top-level port, parameter or register change; `KL_gptp_shadow.pub_path_o` widens with the engine's to eight entries from entry 0; the wrapper `gptp_shadow_wrap` adds `pub_path_head_o`. Checked against `git diff 5fcec84b 2b1565fd`. The shadow's `pub_path_o` goes `[7*64-1:0]` to `[8*64-1:0]` and the wrapper gains one output. `milan_csr.sv` changes port comments only, as `SUBMODULES.md:306-308` already says. `milan_datapath.sv` has no port or parameter line change.
3. **R1.** Resolved. `SUBMODULES.md:334` reads "Its shipping route meets timing at +0.333 ns WNS." `CHANGELOG.md:83` says "WNS is +0.333 ns" and makes no claim that the figure is unchanged.
4. **S1, the #207 full-queue arm.** Resolved.
   - The window is pop-free by construction (`sim_gptp.cpp:1667-1722`). s1's Pdelay_Resp is claimed and held at the MAC, and s1b, a second real Pdelay_Req, waits at the queue head.
   - Both pointers are captured before and after the window, a new check grades them equal (`:1719`), and the level is restored to its captured value. The clean run prints `level 1, rp 1->1, wp 2->2`, so the engine leaves the window as it entered.
   - h2 shows the check is live: without s1b, three stale pops occur and the check fails. Every later graded arm then runs on the unperturbed engine.
   - The refused Sync's message-bank write is not a residue anyone can observe. A refused push does not flip `bank_sel_r`, the next accepted frame overwrites that bank, no queued event names it, and the queued Pdelay_Req carries its own snapshot (`KL_gptp_engine.sv:201-208`).
5. **The physical leg's deadline.** Resolved.
   - The re-projection follows the README's method (`tb/verilator/milan_dp/README.md:406-436`). The simulation term is scaled by the cycle ratio 899637137/849624822 = 1.058864 and the 830 s remainder is not scaled. Recomputed: 4265.7 x r + 830 = 5346.8 s and (5225 - 830) x r + 830 = 5483.7 s. That is 99.0 and 101.6 % of 5400 s, and 77.5 and 79.5 % of 6900 s. A worst case of at most 80 % needs at least 6855 s. With the 30 setup minutes kept, the job permits 145 min, and margins are 53.6 to 55.9 min. The physical leg's sources (`sim_ax1x1gptp.cpp`, RTL, gitlinks) are untouched by the delta, so the scenario length stands.
   - Only the `physical-gptp` job changed: `timeout-minutes` 120 to 145 in `.github/ci-templates/rtl.yml:321` and generated `.github/workflows/rtl.yml:418`. The suite deadline moved 5400 to 6900 in `scripts/run_all_suites.sh:259`; the job runs it with `env -u SUITE_TIMEOUT`, so the default applies. The pinned contracts moved with it (`scripts/ci_events.py:178, 2008`; `scripts/measure_test_evidence.py:673, 680`; its selftest `:297`). No other `timeout-minutes` and no PR-gating job changed. `ci_events --check` confirms the generated workflow matches its template.
6. **Slice headroom.** `docs/design/AREA_BUDGET.md:140` states 15,843 slices placed and 7 of 15,850 free at FPGA-gPTP `f97c1803`. `:141` keeps the sentence that further growth needs an owner decision. Not ruled here; the acceptance is the owner's.
7. **Scope, comments, PR body.**
   - `git diff fb182b19 2b1565fd --stat` touches no `hdl/`, submodule, `syn/` or register-map file (`receipts/delta_stat.txt`, `delta_files.txt`). The STOP rule is not triggered.
   - The added-line scan (`receipts/delta_comment_scan.txt`) finds no lane label, lane name, review round, reviewer ID, issue-comment ID, private path, or tool or model name. Its four hits are false positives inside "plane" and hierarchy names.
   - The PR body is at this head, says "Relates to #803" and has no closing reference (`closingIssuesReferences` empty). Its figures match my receipts: 202/202 on both legs, the FAIL lines, 6900 s, 145 min, 5347-5484 s and 7 of 15,850.

## Prior findings at this head

| Finding | Origin | Status at `2b1565fd` | Evidence |
|---|---|---|---|
| F1 MINOR (Tests, Robustness): no check fails if the GET_AS_PATH snapshot is bypassed | R727-1 | RESOLVED | m9 and m9b killed on named checks; h1 kills the ordering check; clean 202/202 on both legs |
| F2 MINOR (Docs): "No parent port..." understated the scope | R727-1 | RESOLVED | `SUBMODULES.md:310-314`, `CHANGELOG.md:72-75` |
| R1 RESIDUE (Docs): "keeps +0.333 ns WNS" | R727-1 | RESOLVED | `SUBMODULES.md:334` |
| S1 SUGGESTION (Tests): stale pops in the #207 window | R727-1 | RESOLVED (taken) | pointers 1->1, 2->2; h2 control |
| F1 MINOR (Tests): snapshot bypass survives; the `asp_resp_entry_w` ordering claim is untested | R728-1 | RESOLVED | as R727-1 F1; the harness now reads `asp_resp_entry_w` and asserts the ordering (`sim_gptp.cpp:426-428, 1490-1497`) |
| S1 SUGGESTION (Tests): the #207 residue comment depends on arm order | R728-1 | RESOLVED (taken) | as R727-1 S1; the invariant no longer depends on order |

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE.

### N1 - SUGGESTION - Docs - `tb/verilator/milan_dp/README.md:422-423`

- Authority: AGENTS.md section 6 Docs, that obsolete statements are not left reading as current.
- These lines come before the delta and describe the previous 849,624,822-cycle scenario: "The 5400-second deadline therefore still holds on projection" and "The 120-minute job keeps more than 30 minutes of margin". The new paragraph at `:426-436` supersedes them, so a careful reader is not misled, but read alone they sound current.
- Optional outcome: past-tense wording, for example "For that scenario, the 5400-second deadline held on projection ...".
- Verification: read `:420-436`.

### N2 - SUGGESTION - Tests - `tb/verilator/milan_dp/sim_gptp.cpp:1490-1496`

- The `[cut]` diagnostic prints "count beat held N cycles" from `sim_cyc - capture_cyc` even when no hold is active. h1 prints "held 474 cycles" with the hold removed.
- The graded check is correct, so this is diagnostic wording only.
- Optional outcome: "capture to commit N cycles", or print `hold_gsi_beat` as well.

## Lens results (clean lenses in the finding format)

```text
[R728] PASS Conformance - hdl/milan/milan_datapath.sv:6011-6073,6300-6310 at 2b1565fd; tb/verilator/milan_dp/sim_gptp.cpp:1462-1507 - the in-flight response's count, entry 0 and entry 1 stay on the first-count snapshot while live state and the next read are new, as IEEE 1722.1-2021 7.4.41.2 and REGISTER_MAP.md:333 require; the delta changes no RTL; ruling items 1-6 checked above
[R728] PASS RTL - git diff fb182b19 2b1565fd --stat (no hdl/, submodule, syn/ or register-map file); KL_aecp_engine.sv:2400,2454 (bounded gather HOLD that the harness uses); KL_gptp_engine.sv:200-255 (queue and bank ping-pong behind the #207 window) - the delta changes no RTL; the harness pokes (gsi_srv1_r, evq_lvl_r) stay inside existing bounded-wait and queue-full contracts, and the pointers are proven unmoved
[R728] PASS Robustness - receipts/legs/{m9,m9b,m9c,h1,h2}.gptp.summary.txt; sim_gptp.cpp:1667-1722 - a publication mid-gather (one torn field at a time) and a forced-full queue with a live head entry each fail on named checks; at the head the window pops nothing and the engine is restored, so later arms grade an unperturbed engine
[R728] PASS Tests - receipts/legs/*.summary.txt (clean gptp and gptp-lat 202/202; 5 planted defects, each KILLED on a named check); receipts/ci_events_selftest.log; receipts/measure_test_evidence_selftest.log - every new check fails for the defect it names, h1 and h2 show the two new guards are live, and the two contract selftests pass with the 6900/145 pins
[R728] PASS Docs - SUBMODULES.md:306-334; CHANGELOG.md:69-84; AREA_BUDGET.md:140-141; CI_WORKFLOWS.md:537,656-661; TESTING.md:172-173; RUNNING_TESTS.md:88; milan_dp/README.md:354-355,426-436; milan_dp_gptp/README.md:26-27; run_all_suites.sh:41,252-259; PR #805 body - the scope, WNS wording, slice figures, deadline and projection match the head and my recomputation; check_doc_style and docs_check rc 0; the em-dash gate cannot run here (see limits), and a manual scan of added Markdown lines found 0 em dashes
```

## Reviewer-owned completion ledger (this round)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `milan_datapath.sv:6011-6073, 6300-6310`; `REGISTER_MAP.md:330-333`; `sim_gptp.cpp:1424-1507`; ruling items 1-6 | R728-2 | `2b1565fd9095d6ec8be514849ba9b92b8f4c5b31` |
| RTL | CLEAN | `git diff fb182b19 2b1565fd --stat` (no RTL); `KL_aecp_engine.sv:2400-2457`; `KL_gptp_engine.sv:200-255`; R728-1's RTL coverage at `fb182b19` carries forward because the delta does not touch its scope | R728-2 (delta), R728-1 (unchanged RTL) | `2b1565fd...` (ancestor `fb182b19`; no RTL file has changed since) |
| Robustness | CLEAN | m9, m9b, m9c, h1, h2 probe legs; `sim_gptp.cpp:1462-1507, 1667-1722` | R728-2 | `2b1565fd...` |
| Tests | CLEAN | clean `gptp` and `gptp-lat` 202/202; 5 planted defects killed; `ci_events --check` and `--selftest`; `measure_test_evidence --selftest`; author mutant table (19 rows, hash-checked) | R728-2 | `2b1565fd...` |
| Docs | CLEAN | `SUBMODULES.md`, `CHANGELOG.md`, `AREA_BUDGET.md`, `CI_WORKFLOWS.md`, `TESTING.md`, `RUNNING_TESTS.md`, both milan_dp READMEs, `run_all_suites.sh` comment, PR body; doc gates | R728-2 | `2b1565fd...` |

## Real limits

- **Read from the author's published receipts only (hash-checked against the published manifest, `receipts/evidence_spotcheck.txt`):**
  - the full parent sweep (64 suites, 2,191,421 checks, 0 failures);
  - the physical leg at the head (205 checks, 0 failures, 5391 s against 6900 s);
  - the docs workflow (md312 5 steps rc 0, including the em-dash gate);
  - the 19-row mutant table;
  - the projection script output.
  I did not run the sweep, the physical leg, Yosys, Vivado, rtl-fast or the builder; they are bank-scale or not allowed in this round.
- **Area and timing:** the delta changes no synthesis input, so the slice, LUT and WNS figures rest on round 1's route receipts as R728-1 verified them. Not re-run.
- **Em-dash gate:** `scripts/check_em_dash.py --base ...` returns rc 2 here because the pinned Markdown renderer is not installed, and installs are not allowed (`receipts/check_em_dash.log`). A manual scan of added Markdown lines found none; the author's md312 receipt shows the gate rc 0.
- **The ruling's "200/200":** the clean legs now run 202 checks, and all 202 pass. I read this as the ruling's intent (no failures, every check passes), not as a literal count.
- **Hosted contexts:** at snapshot time (`receipts/hosted_checks_snapshot.tsv`), 17 jobs had completed successfully, 26 were in progress or queued, and `Physical gPTP (nightly and manual)` was skipped on this PR event. That is not proof. No manager source bank was run or inferred.
- **Standard text:** no IEEE or Milan text was opened. The 7.4.41.2 pairing of count with path_sequence rests on `REGISTER_MAP.md:333` and the issue's citation.
- **No hardware.** Physical calibration NOT RUN; field skips are not hardware proof.

## Pending manager duties

- Current-dev merge-candidate validation (builder and native banks) at the merge turn, against live dev `5fcec84b`.
- Exact-head hosted `verilator-suites` and `yosys-portability`, and act acceptance.
- The first completed hosted run of the physical leg against the 6900 s deadline (it is skipped on PR events).
- The owner's decision on slice headroom (7 of 15,850 free, +20 over dev), recorded on #803 before merge.
- R727-2, the internal review of this head.
- Optional: carry N1 and N2.
- FPGA-gPTP #87-#91 close only after an image passes the in-house scenarios.

R728-2 FINISHED
