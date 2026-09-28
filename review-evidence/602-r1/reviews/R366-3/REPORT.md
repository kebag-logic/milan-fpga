[R366] POSITIVE - exact head 6b2ebd1c435136966f84ffc16d28a80c7d6b9387

# R366-3: internal independent re-review of PR #603 (issue #602, deliverable 2)

- Exact head `6b2ebd1c435136966f84ffc16d28a80c7d6b9387`, tree `832c46b5efcf8e937e899c625f6df0ae59adef7b`. Source base `6d5ebd7357c1e468e446f18a61527c5be6118a04`. Delta under review: `471892a9..6b2ebd1c`, one commit by [A397] (`receipts/delta_scope.txt`, raw diff `receipts/delta_471892a9_6b2ebd1c.diff`).
- Reconstructed from the public record:
  - AGENTS.md, CONTRIBUTING.md and docs/README.md.
  - Issue #602: the ruling 5859297355, the assignment 5859299480, the scope correction 5859621253, the round-2 assignment 5860151273, the round-3 assignment 5861304608, [A397] TAKEN 5861314929 and REVIEW READY 5861984828.
  - The diff and its history.
  - The [A397] packet at `602-review-evidence` `438763a3:review-evidence/602-r1/author-r3` (`receipts/public_evidence_read.txt`), and hosted checks at the head.
- My own round-2 packet (R366-2) was re-read for its findings and probe definitions, and those probes were re-run at this head. The verdict, findings and ledger below were written before I read any other reviewer's round-2 or round-3 report.
- `$CLONE` is the detached review clone. `$PACKET` is this packet. All probes and builds ran in a scratch git clone of the exact head with the pinned submodules, never in `$CLONE`.

## Verdict

**POSITIVE.** Every round-3 item is met at this head, and every lens is covered clean. Two SUGGESTIONS are recorded; neither affects coverage.

- **(1) Firmware gate description: MET.**
  - `BAREMETAL_FIRMWARE.md:1469` and `:1471` state what the gate enforces, and both cite #602. This matches the RTL census and the builder's pinned census.
  - My widened stale scan finds no stale hit outside `docs/history/**`.
- **(2) R366-2 F1: RESOLVED.** The option-off adjtime check now catches adjtime-caused `mr` changes delayed by 2, 4, 8, 12, 16, 256 and 65,536 cycles. Each delayed cause fails only that check.
  - The three earlier controls keep their exact broken-check sets.
  - The clean leg is still 234/0.
- **(3) Coincident check: MET.** It is renamed for what it can fail on, and the pending-merge limit is noted beside it.
- **(4) README and Makefile wording: MET.**
- **No other behaviour change.** No file under `hdl/`, `sw/`, `configs/`, `scripts/`, `syn/` or `.github/` changed, and no gitlink moved.

## Round-3 focus items

### (1) The firmware gate description matches what the gate enforces: MET

- **The rows** (`docs/integration/BAREMETAL_FIRMWARE.md`):
  - `:1469` says "`media_rebase_p_w` has exactly two references", namely "its initializer and sole reader, `render_recentre_p_w`", and cites the ruling 5859297355.
  - `:1471` pins `mcr_restart_p_w` as exactly `crf_clk_selected_r & ((tkd_crflk_q_r & ~crf_locked_w) | crf_mr_toggle_p_w)`. It says the ruling "excludes the PHC-step term".
- **Checked against the RTL and the builder.** `fw_doc_census.py` strips comments from `milan_datapath.sv` and counts code references (`receipts/fw_doc_census.txt`, rc 0, 0 disagreements):

| Net | RTL references | Doc | Builder pin |
|---|---|---|---|
| `media_rebase_p_w` | 2 (`:3132` initializer, `:6054` render reader) | 2 | 2 |
| `mcr_restart_p_w` | 2 (`:3133` initializer, `:3163` `.restart_p_i`) | 2 | 2 |
| `eff_ptp_adjust_w` | 3 | 3 | 3 |
| `cfg_ptp_cmd_load` | 5 | 5 | 5 |

  - The doc's `mcr_restart_p_w` expression equals the RTL initializer character for character, and it matches the builder's `direct_initializer` pin (`sw/builder/test_builder.py:10775-10780`).
  - The neighbouring row `:1468` ("its extra reader is now `media_rebase_p_w` (#387)") is still true.
- **Stale scan.** `stale_scan.sh` repeats my round-2 scans 1-5, and adds four expression-level scans. Round 2 lacked that class, which is how `:1469` and `:1471` escaped it:
  - scan 6: both nets on one line;
  - scan 7: the old census wording ("three references", "two readers", "ungated");
  - scan 8: restart request or `restart_p_i` near a PHC, step or re-base word;
  - scan 9: re-base or PHC-step text within three lines of `mr` or MEDIA_RESET.
- **Scan result** (`receipts/stale_doc_scan.txt`, 154 hit lines, all read in context):
  - Every hit on the #602 contract states the ruling.
  - Scan 5 (the superseded tkdiag claim) returns no hits.
  - The scan-7 "two readers" hits are unrelated prose about parsers. The servo guard-streak hits (`mmcm_servo/sim_main.cpp:26,530`) are unrelated.
  - Zero stale claims outside `docs/history/**`.
- **Builder bank.** The one builder function that loads this document is `test_baremetal_profile_contract`. It does not finish inside this session's 10-minute foreground limit, so I stopped it at 580 s (rc 124, `receipts/builder_baremetal_profile_contract.log`); it is **NOT RUN** here. The full bank is not mine to run. The published [A397] receipts at this head report rc 0 for the full bank in both compiler modes (`receipts/public_evidence_read.txt`):
  - With the RV32 compiler: 756.8 s, "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11, the placed-calibration report).
  - Compiler absent: 550.5 s, "ALL GATES PASS EXCEPT 2 NOT RUN" (gate 1b's compiled census and gate 11).
  - The builder asserts no text from these table rows. The rows restate the census and initializer pins, and the RTL matches those pins.

### (2) The option-off adjtime check sees delayed causes: MET (R366-2 F1 resolved)

- **The change** (`tb/verilator/milan_dp/sim_main.cpp`):
  - `:110`: the before-level is now a harness member.
  - `:576`: it is sampled just before the adjtime write.
  - `:1062-1065`: the check compares it with `settime_mr_before`. That level is read after the 4096-cycle settle (`:1058-1061`), immediately before the settime.
  - So the window runs from the adjtime to the settime baseline, and it covers every section in between.
  - `run()` calls `prove_ptp_clock_control_stays_fabric_owned` (`:2654`) before `prove_the_milan_talker_admission_gate`, which reaches the holdover section (`:647`, `:972`). The order is fixed; see S2.
- **Probes.** Each probe plants its cause into a copy of `milan_datapath.sv` and builds the option-off leg through the suite's own recipe. The definitions are the ones I used in round 2 (`scripts/probes.py`); receipts are `receipts/O*.log` and `receipts/summary.txt`.

| Probe | Result at 6b2ebd1c | At 471892a9 (R366-2) |
|---|---|---|
| O0 clean | rc 0, **234 checks, 0 failures** | 234/0 |
| O1 settime-only | fails `the settime leaves mr unchanged` and `settime adds no MEDIA_RESET`; adjtime check clean | same |
| O2 adjtime-only | fails only `PHC-only steps leave INTERNAL mr unchanged` | same |
| O3 both causes | fails all three (the settime check as got=0 exp=1) | same |
| O6 adjtime delayed 2, 4, 8, 12 cycles | each fails only the adjtime check | same |
| **O4 adjtime delayed 16 cycles** | **fails only the adjtime check** | survived, 234/0 |
| **O5 adjtime delayed 256 cycles** | **fails only the adjtime check** | survived, 234/0 |
| O7 adjtime delayed 65,536 cycles (new) | fails only the adjtime check | not run |
| O8 adjtime cause requested twice, at +0 and +256 (new) | rc 0, 234/0: survives; see S1 | not run |

- **Through the head's own runner** (`run_author_controls.py` imports the head's `gmstep_mutants.py` and calls its `run_control`, including the anchor count and the `stays_clean` rule; `receipts/author_controls_via_head_runner.log`, rc 0):
  - The inventory is 20 controls: 15 gmstep, 5 option-off, 5 acceptance.
  - All five option-off controls and the coincident control are caught, 6/6.
  - The 16- and 256-cycle controls each break exactly one check. Both settime checks are enforced clean through `stays_clean` (`gmstep_mutants.py:199-221`).
  - The author's delayed-cause RTL text is the same as my O4/O5 plants.
- **Published run.** The [A397] campaign log at this head reports 22/22: two clean baselines and 20 caught controls.

### (3) The coincident check is named for what it can fail on: MET

- The check is now `coincident: a PHC step does not suppress the CRF restart` (`sim_gmstep.cpp:1143`), with the name aligned in `gmstep_mutants.py:225` and README `:713`.
- The limit is stated beside it: `sim_gmstep.cpp:1098-1099` and README `:661-663` say that pending requests merge, so the trials grade suppression, and that the isolated PHC-step checks grade an added request.
- **Behaviour at this head:**

| Probe | Result |
|---|---|
| G0 clean | 103/0 |
| G3 same-cycle veto | caught only by the renamed check |
| G4 one-cycle-late veto | caught only by the renamed check |
| G2 CRF propagation removed | caught by `CRF control: selected CRF mr propagates exactly once` and by the renamed check (32 trials) |
| G1 re-base term restored | caught by `restart: a PHC-only step leaves outgoing mr unchanged` and `restart: a PHC-only step adds no MEDIA_RESET`, exactly as the new comment says |

- **Feed sweep** (`feed_sweep.sh`; `receipts/feed_sweep_summary.txt`, `feed_sweep_rc.txt`): the clean head binary ran at all 42 `GMSTEP_FEED_DELAY` values. All 42 gave rc 0 and 103/0, and the renamed check passed each time.

### (4) README and Makefile wording: MET

- **README `:683-686`.** The hedge is replaced by a dated measurement at `471892a9` that cites both round-2 reviews. It holds at this head: the feed sweep above gives 42/42 at 103/0.
- **Makefile `:20-21`.** It now reads "five controls of the option-off leg's #602 PHC-only mr exclusions".
- **Counts in the other inventories:**
  - README `:697-713` (the table) has 17 rows, and adding the three #545 controls gives 20.
  - README `:718`, `:985` and `:1001` say twenty controls.
  - `TESTING.md:273`: "fifteen gmstep controls and five option-off controls".
  - `GM_LOSS_RECOVERY.md:236-240`: five option-off controls, two of them delayed.
  - All of these equal the runner's census: 15 + 5 = 20, with 5 acceptance controls.

## Findings

No BLOCKER, MAJOR or MINOR. Two SUGGESTIONS, both optional and outside the verdict.

### S1 - SUGGESTION - Tests, Robustness - the option-off adjtime check compares levels, so an even number of adjtime-caused toggles passes

- **Where:** `tb/verilator/milan_dp/sim_main.cpp:576`, `:1064-1065`.
- **Evidence:**
  - O8 plants an adjtime cause that requests twice, at +0 and +256 cycles. The option-off leg passes 234/0.
  - G8 plants the same cause on the gmstep leg, where the checks count toggles. It is caught there: `restart: a PHC-only step leaves outgoing mr unchanged got=2`, and MEDIA_RESET got=2.
  - The settime event pairs its level check with a MEDIA_RESET delta (`:1089`). The adjtime event has no such delta.
- **Why only a SUGGESTION.**
  - Round-2 assignment 5860151273 accepted "the `mr` level just before the event compared with just after it". Round-3 assignment 5861304608 offers "compare against a level read after the settle interval" as a compliant form, and that form is what was built.
  - The plane adjtime path is counted on the gmstep leg. Only a cause specific to the CSR path that toggles an even number of times would pass.
- **Possible improvement:** add a MEDIA_RESET delta across the same adjtime window, taken at `:576` and compared at `:1061`, or count transmitted toggles there. O8 should then fail the adjtime check only.

### S2 - SUGGESTION - Tests - the adjtime baseline depends on section order, with a silent default

- **Where:** `tb/verilator/milan_dp/sim_main.cpp:110`, which declares `adjtime_mr_before = false`.
- **The risk:**
  - If the holdover section ever ran before `prove_ptp_clock_control_stays_fabric_owned`, the check would compare the level against the default `false`.
  - In the clean run that level is 0, so the check would pass without grading any adjtime.
  - Today `run()` fixes the order (`:2654` before `:647`/`:972`), so nothing is wrong at this head.
- **Possible improvement:** record that the adjtime sample was taken, for example with a flag or a `ck` on it, so a reorder fails instead of passing vacuously.

## My round-2 findings, resolved or retained at this head

| R366-2 finding | Status at 6b2ebd1c | Evidence |
|---|---|---|
| F1 MINOR, Tests and Robustness: an adjtime cause delayed 16 or more cycles survived the option-off leg | **RESOLVED** | Item (2): O4 (16), O5 (256) and O7 (65,536) each fail only the adjtime check. O1-O3 keep their sets. O0 is 234/0. The head runner catches 6/6. |
| F2 SUGGESTION, Tests: the coincident check's name claimed "neither adds" | **TAKEN and verified** | Item (3): renamed, with the merge limit stated at `sim_gmstep.cpp:1098-1099` and README `:661-663` |
| F3 SUGGESTION, Docs: the README `:680` hedge and the Makefile `:20-21` wording | **TAKEN and verified** | Item (4) |

My round-1 findings (R366-1 F1-F4) were resolved at `471892a9` (R366-2). The documents, harness text and tkdiag narrative they concern were not changed back by this delta; the stale scan and tkdiag 96/0 re-confirm this.

## Reviewer-owned lens ledger (R366-3)

| Lens | Status | Examined artifacts (at the head) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round-3 assignment 5861304608, items 1-2 and the taken suggestions, against the delta (`receipts/delta_471892a9_6b2ebd1c.diff`). Ruling 5859297355 against `milan_datapath.sv:3124-3134`, unchanged since `49012143` (`receipts/delta_scope.txt`). The `BAREMETAL_FIRMWARE.md:1468-1471` census against the RTL and builder pins (`receipts/fw_doc_census.txt`). gmstep 103/0 at all 42 feed delays. Option-off 234/0. | R366-3 | `6b2ebd1c435136966f84ffc16d28a80c7d6b9387` |
| RTL | CLEAN | No `hdl/` change in `471892a9..6b2ebd1c` or `49012143..6b2ebd1c`, and gitlinks unchanged (`receipts/delta_scope.txt`). `mcr_restart_p_w`/`media_rebase_p_w` reference census (`milan_datapath.sv:3132,3133,3163,6054`). Restart-engine merge/hold behaviour checked through the G1-G4 and G8 outcomes. `lint_rtl.py --check --jobs 8` PASS, 90 <= 90 (`receipts/rtl_lint.log`). tkdiag 96/0 with 4/4 engine mutants (`receipts/tkdiag_head.log`). | R366-3 | `6b2ebd1c435136966f84ffc16d28a80c7d6b9387` |
| Robustness | CLEAN (S1 is a SUGGESTION) | Delayed-cause boundary O6 (2/4/8/12), O4 (16), O5 (256), O7 (65,536). Repeated request O8/G8. Feature-off INTERNAL leg with combined causes O1-O3. Coincident offsets G3/G4 (same cycle, one cycle late). 42 feed phases. | R366-3 | `6b2ebd1c435136966f84ffc16d28a80c7d6b9387` |
| Tests | CLEAN (S1 and S2 are SUGGESTIONS) | `sim_main.cpp:110,576,1058-1065,1085-1090`; `sim_gmstep.cpp:1098-1143`; `gmstep_mutants.py:23,59-61,93,185-226,274-326`; 18 probe runs (`receipts/summary.txt`); the head runner on 6 controls (`receipts/author_controls_via_head_runner.log`); the published [A397] 22/22 campaign at this head, cross-checked | R366-3 | `6b2ebd1c435136966f84ffc16d28a80c7d6b9387` |
| Docs | CLEAN | `BAREMETAL_FIRMWARE.md:1468-1471`; `GM_LOSS_RECOVERY.md:236-240`; `TESTING.md:273`; `milan_dp/README.md:661-663,683-686,697-735,985,1001`; `milan_dp/Makefile:20-21`; stale scans 1-9 (`receipts/stale_doc_scan.txt`: 154 hits read, 0 stale). Docs gates (`receipts/docs_gates.txt`) all rc 0: docs_check, doc_style, doc_paths, gen_toc `--check`, em_dash `--base 6d5ebd73`, module matrix, hygiene, py/cpp idiom and `git diff --check`. | R366-3 | `6b2ebd1c435136966f84ffc16d28a80c7d6b9387` |

## Commands and receipts (all run in the foreground)

- **Tool identity** (`receipts/tools_identity.txt`):
  - The assigned Verilator path does not exist on this host.
  - I used the #602 round-3 manager wrapper. Its sha256 is identical to the round-2 wrapper. It reports `Verilator 5.050 2026-07-01 rev v5.050`, which is the project pin (`rtl-fast.yml:18`), and the binary hash is recorded.
- **Scratch clone.** A `git clone` of `$CLONE` at the exact head, with the three initialized gitlinks cloned at their pins. The `external` gitlink is uninitialised in `$CLONE` and was not cloned.
- **Probes** (`python3 scripts/probes.py <verilator> <names...>`):
  - Batches of four builds with `VERILATOR_JOBS=2`, never more than 8 jobs.
  - Per-probe logs are in `receipts/<probe>.log`.
- **The head's runner:** `python3 scripts/run_author_controls.py <verilator>`, sequential, `VERILATOR_JOBS=8`.
- **Feed sweep:** `sh scripts/feed_sweep.sh <G0 obj> <suite> <out>`, 8 at a time. 42/42 rc 0.
- **Firmware census:** `python3 -B scripts/fw_doc_census.py $CLONE`, which is read-only.
- **Stale scan:** `sh scripts/stale_scan.sh $CLONE`, which is read-only.
- **Lint, tkdiag and docs gates:**
  - Lint, tkdiag and most docs gates ran in the scratch clone.
  - gen_toc and em_dash use the pinned Markdown-renderer interpreter.
  - hygiene and the py/cpp idiom gates need registered submodules, so they ran in `$CLONE` with `PYTHONDONTWRITEBYTECODE=1`.
- **Hosted checks at the head** (read-only; `receipts/hosted_check_runs_at_head.txt`):
  - Completed successfully: bdd-conformance, changes, docs-check, docs-check-no-git, elaborate, full-ci-gate, rtl-fast, verilator-lint, wire-accountability, yosys-elaboration, Yosys shards 0-3, and Verilator shards 0, 2 and 3.
  - Still in progress when read: Verilator shards 1 and 4.
  - Skipped by design: Physical gPTP.
- **Clone integrity after all work** (`scripts/clone_integrity.sh $CLONE` → `receipts/clone_integrity.txt`):
  - HEAD, tree and index tree equal the reviewed ids.
  - Status is empty, including untracked and ignored files.
  - All 930 tracked blobs and modes match HEAD.
  - The gitlinks `gptp-processor 5dce647a`, `protocol-processor 870ff88a` and `third_party/verilog-axis 48ff7a7e` are at their pins with 0 dirty entries.
  - `external` is uninitialised and empty, as before this round.

## Real limits

- **Builder.** The builder function that loads `BAREMETAL_FIRMWARE.md` did not finish within the 10-minute foreground limit (rc 124, stopped by me), so it is NOT RUN in this round. Item (1) rests on:
  - the executed census comparison;
  - the builder's own pins, read at this head;
  - the published [A397] full-bank receipts, which I read but did not re-execute. In compiler-absent mode gate 1b's compiled census is NOT RUN, and gate 11 is NOT RUN in both modes.
- **Not run, by assignment:**
  - the full `milan_dp` `run`, the whole `gmstep_mutants.py` inventory, the builder banks, and the full parent/PP/gPTP/Yosys banks;
  - OOC (the area question is closed);
  - act, and the hosted jobs.
  - I ran 6 of the 20 inventory controls through the head's runner, plus 18 probes of my own. The other 14 controls are unchanged since round 2, and the published [A397] campaign reports 22/22 at this head.
- **Artifact identity was not re-run.** The delta touches no `sw/`, `configs/` or `hdl/` file. R366-1 verified 50/50 at `49012143`, and [A397] reports a match at this head.
- **Simulation scope.** gmstep is a compressed-time model: the TDM clocks are held, the DRP answers zero, and the talker is opened by the escape bit. This round gives no lwSRP, physical-clock or placed-area proof. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Manager evidence.** The assignment says the manager's full source static, builder and native banks passed at this head. The only public receipts I found for this head are the [A397] packet on `602-review-evidence`, and I did not re-execute them.

## Pending manager duties

- **Hosted exact-head acceptance.** Verilator shards 1 and 4 were still in progress when read. Act-first local replication is also needed.
- **The candidate merge build** on live dev `931f396ec9f13271e9e67b755e18833d0024f234`. Source validation here was against base `6d5ebd73`.
- **The composition check** of `GM_LOSS_RECOVERY.md` and the `BAREMETAL_FIRMWARE.md` census rows with dev changes since the base, including PR #601 (#593).
- **The external independent verdict** and the full completion bar.
- **No merge** without explicit maintainer authorization.

## Other public round-2 findings (R367-2), reconciled at this head

I wrote this section after the verdict, findings and ledger above. None of them changed after I read R367-2 (PR comment 5861301512).

| R367-2 finding | Status at 6b2ebd1c | Evidence |
|---|---|---|
| F1 MINOR, Docs and Conformance: `BAREMETAL_FIRMWARE.md:1469,1471` state the PHC-inclusive restart initializer | **RESOLVED** | Item (1) above. Both rows now state two references and the CRF-only initializer, and both cite #602. The census and initializer agree with the RTL and with `test_builder.py:10705-10720,10770-10781` (`receipts/fw_doc_census.txt`). The widened stale scan finds 0 stale hits outside `docs/history/**`. docs_check and doc_paths are rc 0. The builder bank: the published [A397] receipts give rc 0 in both modes; my own focused run did not finish (see Real limits). |
| F2 SUGGESTION, Tests: the coincident check's name | **TAKEN and verified** (the rename option) | Item (3), the same outcome as my R366-2 F2. The alternative, extra offsets past the first adopted PDU, was not taken. It was optional, and the isolated-step checks still grade an added request (G1). |
| F3 SUGGESTION, Docs: the Makefile `:19-20` and README `:680` wording | **TAKEN and verified** | Item (4) |

- R367-2 carried R367-1 F1 as its own F1, now resolved above. It recorded R367-1 F2-F4 as resolved, taken or closed by the manager.
- My R366-2 report reconciled the same R367-1 findings at `471892a9`.
- This delta does not reopen any of them. No finding from R366-1, R366-2, R367-1 or R367-2 remains open at this head.

R366-3 FINISHED
