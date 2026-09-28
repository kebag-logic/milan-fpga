[R367] POSITIVE - exact head 6b2ebd1c435136966f84ffc16d28a80c7d6b9387

# R367-3: external independent re-review of PR #603 (issue #602, deliverable 2), round 3

- **Head:** `6b2ebd1c435136966f84ffc16d28a80c7d6b9387`, tree `832c46b5efcf8e937e899c625f6df0ae59adef7b`. Source base `6d5ebd7357c1e468e446f18a61527c5be6118a04`. Round-3 delta `471892a9..6b2ebd1c`: one commit. Its subject is one line, with no body and no trailers.
- **Scope:** round-3 assignment 5861304608 against ruling 5859297355, assignments 5859299480 and 5860151273, and scope correction 5859621253. The delta touches 8 files: `GM_LOSS_RECOVERY.md`, `BAREMETAL_FIRMWARE.md`, `TESTING.md`, and in `tb/verilator/milan_dp` the `Makefile`, `README.md`, `gmstep_mutants.py`, `sim_gmstep.cpp` and `sim_main.cpp`. `git diff --quiet 471892a9 6b2ebd1c -- hdl sw scripts syn` returns 0, so no RTL, builder, script or synthesis file changed.
- **Method:** reconstructed from AGENTS.md, CONTRIBUTING.md, the issue body and public comments, and the diff. My independent pass over the diff, together with the probes, came before I read any other reviewer's round-2 findings. All probes ran on disposable copies. The review clone was verified byte-identical afterwards.
- **Verdict basis:** all four round-3 items are met, and every probe from my round 2 reproduces at this head. No BLOCKER, MAJOR or MINOR finding is open. One SUGGESTION (S1) does not affect the verdict.

## Round-3 items

### (1) `BAREMETAL_FIRMWARE.md:1469,1471` state what the gate enforces and cite #602: MET

- **`:1469`** reads "`media_rebase_p_w` has exactly two references | Its initializer and sole reader, `render_recentre_p_w`, under the #602 ruling". This matches:
  - the census at `sw/builder/test_builder.py:10719` (`"media_rebase_p_w": 2`);
  - the RTL, whose only references are `hdl/milan/milan_datapath.sv:3132` (the initializer) and `:6054` (the `render_recentre_p_w` reader).
- **`:1471`** reads "`mcr_restart_p_w` is exactly `crf_clk_selected_r & ((tkd_crflk_q_r & ~crf_locked_w) | crf_mr_toggle_p_w)` | The #602 ruling excludes the PHC-step term. Exactly two references admit its initializer and direct `media_clock_restart.restart_p_i` connection". This matches:
  - the initializer pin at `test_builder.py:10774-10780`;
  - the census at `:10720` (2);
  - the direct-port pin at `:10786`;
  - the RTL at `milan_datapath.sv:3133-3134,3163`.
- **Both rows** link the ruling 5859297355.
- **Unchanged neighbours are still true:**
  - `:1468`: censuses 5 and 3;
  - `:1470`: the render initializer, `test_builder.py:10789-10791`;
  - `:1520-1524`: the control summary.
- **Stale scan.** I re-ran my round-2 scanner, unchanged: 197 hits in 26 files (`receipts/stale_scan_hits.txt`).
  - Hit counts changed only in the five files that gained or lost hits in this commit.
  - Every new or changed hit was read in context: none is stale, and no STALE hit remains outside `docs/history/**` (`receipts/stale_scan_classification.md`).
  - A targeted phrase grep for the superseded wordings finds only `GM_LOSS_RECOVERY.md:156`, which restates the ruling's design rule, and the legitimate source-change check name.
- **Builder bank.** The builder bank that loads this document (`test_builder.py:3046-3054`) was not run by me: it is a full bank and outside my permissions. The executor's round-3 receipts on the public evidence branch record rc 0 at this exact head:
  - `review-evidence/602-r1/author-r3/builder-rv32.json` (`--require-rv32`, rc 0, "ALL GATES PASS EXCEPT 1 NOT RUN": gate 11, no placed report);
  - `builder-absent.json` (rc 0; gate 1b's compiled instruments and gate 11 NOT RUN).
  - The assignment brief states that the manager's own static/builder bank passed at this head.
  - The edited table rows are not among the phrases the bank asserts (`test_builder.py:11522-11541`).

### (2) The option-off adjtime check catches a delayed adjtime-caused `mr` change: MET

- **The change.** `adjtime_mr_before` is now a member (`sim_main.cpp:109-110`), sampled just before the adjtime command (`:576`). The adjtime check moved to `:1062-1065`. It now compares the adjtime baseline with `settime_mr_before` (`:1061`), which is read after the 4096-cycle settle (`:1058-1059`) and immediately before the settime.
- **My independent plants** (`probe_r367_3.py`) use a reviewer-written down-counter, not the executor's shift register:

| Probe | Harness | Result | Failed checks |
|---|---|---|---|
| O0 clean | head | rc 0, 234/0 | none |
| O5 adjtime cause +16 cycles | head | rc 1, 234/1 | adjtime check only |
| O6 adjtime cause +256 cycles | head | rc 1, 234/1 | adjtime check only |
| O7 adjtime cause +4096 cycles | head | rc 1, 234/1 | adjtime check only |
| O8 adjtime cause +65536 cycles | head | rc 1, 234/1 | adjtime check only |
| OH0 clean | round-2 harness (`471892a9`) | rc 0, 234/0 | none |
| OH5 +16 cycles | round-2 harness | rc 0, 234/0: survives | none |
| OH6 +256 cycles | round-2 harness | rc 0, 234/0: survives | none |

- **The fix has teeth.** The same plants survive the round-2 harness and are caught by this one.
- **The three existing controls keep their broken-check sets.** They are identical to my round-2 `summary.tsv`:
  - O1, adjtime only: the adjtime check;
  - O2, settime only: settime `mr` and settime MEDIA_RESET;
  - O3, both causes: all three.
- **O4 (the event-relative witness, `mr` resetting high) still passes** at 234/0.
- **The clean leg count is unchanged** at 234/0.
- **The executor's own controls, run through its own runner** (`receipts/executor_controls_subset.log`), all pass: 8/8.
  - Both clean legs pass.
  - The five option-off controls are caught with the stated sets. The two delayed controls each broke exactly one check, and the runner enforced their `stays_clean` tuples (both settime checks).
  - The coincident control is caught.
- **Exactness witness (TC).** A counter added to a disposable harness copy tallies every talker-0 `mr` level change between the adjtime and the settime baseline. On the clean leg it reports 0 changes (`receipts/TC_clean.log`, patch in `receipts/togglecount_harness.patch`). So today the level comparison equals a toggle count on this leg.

### (3) The coincident check is named for what it can fail on, and notes the pending-merge limitation: MET

- **Name.** The check is now `coincident: a PHC step does not suppress the CRF restart` (`sim_gmstep.cpp:1143`). It is renamed consistently at `gmstep_mutants.py:225` and in `README.md:713`.
- **Merge limitation.** It is noted at `sim_gmstep.cpp:1098-1099` and `README.md:661-663`: pending requests merge, and the isolated checks grade an added request.
- **Probes:**
  - G2 (suppression) fails only this check.
  - G3 (CRF propagation removed) fails the CRF control and this check.
  - G1 (re-base restored) fails both isolated-step checks and leaves this one green, as the new note says.
  - G4 (settime restored) passes the gmstep leg and is caught by the option-off leg (O2). This is the same division as in round 2.

### (4) README `:680` and Makefile `:20-21` wording: MET

- **README.** `README.md:684-686` now dates the feed-delay claim: "At head `471892a9`, both round-2 reviews measured 103 checks and zero failures at all 42 delays". This is true of my round-2 `feed/feed_sweep.tsv`, and of R366-2's report (its item 4: 42 runs, rc 0, 103/0).
  - I re-ran the sweep at this head: all 42 delays give rc 0 and 103/0, with the overlap observed (`receipts/feed/feed_sweep.tsv`).
- **Makefile.** `Makefile:20-22` now reads "five controls of the option-off leg's #602 PHC-only mr exclusions".

### No other behaviour change

- **The rest of the delta is test and inventory text:**
  - the two new `CONTROLS` entries and the `RESTART_DECL` anchor (`gmstep_mutants.py:62,199-220`), each unique in the datapath;
  - the count updates in `README.md:711-733,985,1001`, `TESTING.md:273` and `GM_LOSS_RECOVERY.md:236-243`.
- **The counts match `CONTROLS` exactly:** 20 total, 5 default, 5 option-off, 15 gmstep, 3 #545.
- **Default sweep** (`receipts/gmstep_mutants_default.log`): 6/6, with the clean gmstep leg passing and all five acceptance controls caught.
- **tkdiag:** 96/0 with 5/5, meaning 4 mutants caught plus the clean control.

## Findings

### S1 - SUGGESTION - Tests, Docs - the adjtime window spans several unrelated sections, and a level comparison cannot see an even number of changes

- **Where:**
  - the adjtime baseline is read in section 7 (`sim_main.cpp:576`, called at `:2654`);
  - the comparison level is read at `:1061`;
  - between the two, the talker-admission, bypass-escape, tone, crossbar and CLKV publication sections run (`:2655`, `:642-647`, `:970-972`), followed by the 4096-cycle settle.
- **The README describes the window as** "the level after the settle interval, immediately before the settime baseline" (`README.md:730-731`). That is accurate, but it does not say the window also covers those sections.
- **Evidence.** O8 is still caught 65536 cycles after the adjtime, so the window is at least that long. On the clean leg, TC measures 0 `mr` changes inside it.
- **Impact** (none today, which is why this is a SUGGESTION):
  - a later change that legitimately moves `mr` inside those sections would fail under the adjtime check's name, which fails closed but misattributes the failure;
  - two changes inside the window would cancel under a level comparison.
- **Authority.** Assignment 5861304608 explicitly allows the level-after-settle form ("compare against a level read after the settle interval, or count the toggles"), so this is not an unmet criterion.
- **Optional outcome:** state the window's real span beside the check, or count transmitted toggles across it.
- **Verification:** read the text, or run TC-style counting in the harness.

## Prior public findings, resolved or retained at this head

| Finding | Status | Evidence |
|---|---|---|
| R367-2 F1 (MINOR; Docs, Conformance): `BAREMETAL_FIRMWARE.md:1469,1471` stated the PHC-inclusive initializer | **RESOLVED** | Item (1) |
| R367-2 F2 (SUGGESTION, Tests) = R366-2 F2: the coincident name claimed "neither adds" | **TAKEN, RESOLVED** | Item (3) |
| R367-2 F3 (SUGGESTION, Docs) = R366-2 F3: dated README `:680` and Makefile `:19-20` wording | **TAKEN, RESOLVED** | Item (4) |
| R366-2 F1 (MINOR; Tests, Robustness): the adjtime check missed a cause landing 16 or more cycles late | **RESOLVED** | Item (2): its verification bullets are met at 16 and 256 cycles, and also at 4096 and 65536; the round-2 harness is shown to miss 16 and 256 |
| R367-1 F1-F4 and R366-1 F1-F4 | **RESOLVED** or **closed** in round 2 (the area question by assignment 5860151273). No artifact in their scope regressed in this delta | Stale scan; this report's items (1)-(4) |

## Reviewer-owned completion ledger (R367-3)

| Lens | Result | Examined artifacts (at the head) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling 5859297355 and round-3 items 1-4 (5861304608) against `milan_datapath.sv:3121-3134` (no PHC term in `mcr_restart_p_w`; `media_rebase_p_w` feeds only the render at `:6054`); `BAREMETAL_FIRMWARE.md:1468-1471` against `test_builder.py:10719-10720,10770-10791`; gmstep G0-G4 and 42 feed delays at 103/0; option-off O0-O8 | R367-3 | `6b2ebd1c435136966f84ffc16d28a80c7d6b9387` |
| RTL | CLEAN | The whole-PR RTL diff `6d5ebd73..6b2ebd1c -- hdl/` (`milan_datapath.sv:3094-3134`, `KL_media_clock_restart.sv:60-62,102-109,168-172`), unchanged since `471892a9`. One OR term was removed; `media_rebase_p_w` and `mcr_restart_p_w` are in the same `axis_clk` domain as the engine (`:3162`); there is no new state, width or CDC. Hosted `rtl-fast`, `verilator-lint`, `elaborate`, `yosys-elaboration` and Yosys shards 0-3 succeed at this head | R367-3 | `6b2ebd1c435136966f84ffc16d28a80c7d6b9387` |
| Robustness | CLEAN | Delayed-cause plants of 16, 256, 4096 and 65536 cycles (O5-O8), and the same plants on the round-2 harness (OH5, OH6); combined causes (O3); the reset-level witness (O4); coincidence at 32 offsets and 42 feed phases; suppression (G2) and propagation removal (G3); the TC window witness | R367-3 | `6b2ebd1c435136966f84ffc16d28a80c7d6b9387` |
| Tests | CLEAN (S1 is a SUGGESTION) | `sim_main.cpp:109-110,571-581,1052-1091`; `sim_gmstep.cpp:1096-1143`; `gmstep_mutants.py:20-23,59-63,83-94,180-226,288-306`. Runs: `receipts/summary.tsv` (17 probes), the executor's controls through its runner 8/8, the default sweep 6/6, tkdiag 96/0 with 5/5, and the feed sweep 42/42 | R367-3 | `6b2ebd1c435136966f84ffc16d28a80c7d6b9387` |
| Docs | CLEAN (S1 is a SUGGESTION) | `BAREMETAL_FIRMWARE.md:1466-1471,1520-1524`; `GM_LOSS_RECOVERY.md:142-160,230-243`; `TESTING.md:273`; `milan_dp/README.md:640-740,982-1001`; `Makefile:17-22`; the stale scan (197 hits classified, 0 stale). Gates rc 0: `docs_check`, `check_doc_paths`, `check_doc_style`, `check_hygiene --check`, `check_em_dash --base 6d5ebd73`, `gen_toc --check`, `measure_test_evidence --check`, `check_cpp_idiom`, `check_py_idiom`, `check_sv_idiom`, `check_rtl_source_lists`, `git diff --check` (`receipts/gates_summary.txt`) | R367-3 | `6b2ebd1c435136966f84ffc16d28a80c7d6b9387` |

Every lens was applied at this exact head. None is carried from an earlier round.

## Real limits

- **Not run by me:**
  - the full builder bank (both compiler modes), the parent, PP, gPTP and Yosys banks;
  - `check_baremetal_only.py`, `ci_scope.py --selftest`, `lint_rtl.py`;
  - the full `milan_dp run`, the full `gmstep-mutants` campaign, the OOC area measurement and the five-configuration identity check.

  For these I rely on the executor's round-3 receipts at this head (`602-review-evidence` commit `438763a3`, `author-r3/*.json`, all rc 0) and on the manager's statement in the assignment brief. I did not reproduce them.
- **Builder coverage.** Both builder modes record gate 11 (placed calibration) as NOT RUN. The compiler-absent mode also records gate 1b's compiled instruments as NOT RUN. These are disclosed coverage limits, not passes.
- **Hosted snapshot** (2026-09-28 02:27 UTC, `receipts/hosted_snapshot.json`):
  - 20 check runs: 16 success, 3 in progress (Verilator shards 1, 2 and 4 of 5), 1 skipped ("Physical gPTP (nightly and manual)").
  - The skipped context is not hardware proof, and the in-progress shards are not evidence.
- **Physical coverage.** Physical calibration was NOT RUN, and no hardware was used. The gmstep leg runs compressed clocks and the streaming escape. It does not prove physical clock continuity or an lwSRP reservation.
- **Tool.** The assigned Verilator path does not exist. I used the same 5.050 wrapper as in round 2, with the same SHA-256 (`receipts/tool_identity.txt`).
- **Renderer.** `check_em_dash` and `gen_toc` need the pinned Markdown renderer. I ran them under an existing Python 3.14.7 environment that has it, without installing anything; the scripts refuse any other renderer release.
- **Integrity.** Importing `gmstep_mutants` for the count check created two `__pycache__` directories, which were ignored and untracked, in the review clone. I removed them. The final check shows:
  - no untracked or ignored files;
  - worktree and index equal to HEAD;
  - all 930 tracked blobs match by SHA-1 and mode;
  - the index hash is unchanged from before the probes;
  - the four gitlinks are unchanged, and the three initialised submodules are clean at their gitlinks (`receipts/clone_integrity_after.txt`).

## Pending manager duties

- Run the final current-dev candidate at the merge turn: source base `6d5ebd73`, live dev `931f396e`. That includes the composition with any PR #601 overlap in the gmstep/restart documents, and the candidate banks.
- Accept the hosted and `act` results on the exact head once Verilator shards 1, 2 and 4 complete.
- S1 is optional and needs no routing. Any further commit un-covers the lenses whose scope it touches.
- Publish this packet: `REPORT.md` and the files listed in `MANIFEST.sha256`.

R367-3 FINISHED
