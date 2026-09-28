[R366] NEGATIVE - exact head 471892a9bcc2d26fdcfc19db01949ecea83c5e0f

# R366-2: internal independent re-review of PR #603 (issue #602, deliverable 2)

- Exact head `471892a9bcc2d26fdcfc19db01949ecea83c5e0f`, tree `56f7ac7776008b49081a6faa829a22e649a9913c`. Source base `6d5ebd7357c1e468e446f18a61527c5be6118a04`. Delta under review: `49012143..471892a9` (two commits by [A388]).
- Reconstructed from the public record: AGENTS.md, CONTRIBUTING.md and docs/README.md; issue #602 (the ruling 5859297355, assignment 5859299480, scope correction 5859621253, round-2 assignment 5860151273, [A388] TAKEN 5860161666 and REVIEW READY 5861091574); the diff and history; the public evidence at `1dab2e7c:review-evidence/602-r1` and the [A388] round-2 packet at `602-review-evidence` `ee7c3c64:review-evidence/602-r1/author-r2`.
- I read my own round-1 report (R366-1) only after my independent pass over the delta. The verdict, findings and ledger below were written before I read any other reviewer's report.
- `$CLONE` is the detached review clone. `$PACKET` is this packet. Probes built in a shared scratch clone of the exact head, never in `$CLONE`.

## Verdict

**NEGATIVE**, on one MINOR finding (F1) that leaves Tests and Robustness unclean.

- The round-2 work does what the assignment asked:
  - Every item of R366-1 F1 and F2 is resolved.
  - R366-1 F3's three controls behave exactly as specified.
  - The coincident scenario (the R366-1 F4 suggestion, which was taken) is real, and it rejects suppression at run time.
  - The RTL is byte-identical to round 1.
- **F1 (MINOR).** The new event-relative adjtime check samples `mr` about 13 cycles after the adjtime. If the adjtime changes `mr` 16 or more cycles later, no check in the option-off leg sees it: the settime check takes its baseline from the already-changed level. Two executed controls survive the whole leg (16-cycle and 256-cycle delay). The same cause delayed by 2 to 12 cycles is caught.
- **F2 and F3** are SUGGESTIONS. They do not affect the verdict.

## Round-2 focus items

### (1) No current document says that a PHC-only step or re-base toggles `mr` or counts MEDIA_RESET: MET

- **Script.** `stale_scan.sh` runs five scans over the committed tree, outside `docs/history/**` and the submodules. Output: `receipts/stale_doc_scan.txt`, 87 hit lines. Every hit was read in context:
  - Each current-contract hit states the #602 ruling.
  - The rest are unrelated: the servo guard streak in `mmcm_servo/sim_main.cpp:26,530`, CRF silence in `REGISTER_MAP.md:359`, and adjfine resolution in `FR_NFR.md:293`.
  - The superseded tkdiag claim `ORs both onto restart_p_i` returns no hits (scan 5, rc 1).
- **Locations named by R366-1 F1, now corrected:**
  - `docs/fpga/FPGA_DESIGN.md:178-180`.
  - `docs/reference/REGISTER_MAP.md:128-131`.
  - `docs/MILAN_V12_ROADMAP.md:360-362`.
- **CHANGELOG.** `CHANGELOG.md:16` and `:116-141` amend the #387 entry. They cite the ruling link, say the entry "reverses its PHC-only restart obligation", and state "A PHC-only re-base leaves `mr` and MEDIA_RESET unchanged". The heading ("one media event per PHC step") stays true: the event is the single render re-base.
- **GM_LOSS_RECOVERY.md.** `docs/design/GM_LOSS_RECOVERY.md:146-179`, `:201-240` and `:268` agree with the ruling. The claim "132 cycles after the plane's step pulse at each of its 42 feed delays" (`:173`) is reproduced at this head (item 4 below). Only this PR's text was judged; the PR #601 overlap is the manager's composition check.

### (2) Campaign inventory and harness narratives: MET

- **The `TESTING.md` `gmstep-mutants` row** (`docs/testing/TESTING.md:273`):
  - It says "fifteen gmstep controls and three option-off controls". That matches the `CONTROLS` census at `tb/verilator/milan_dp/gmstep_mutants.py:110-201`: 15 on `gmstep` and 3 on `option-off`, 18 in total.
  - It lists five default controls, and they are exactly the five with `acceptance=True` (`:128-147`).
  - Its trigger list adds `hdl/ieee1722/avtp/KL_media_clock_restart.sv`. The old "PHC-step `mr` checks" routing is replaced by "event-relative PHC-only restart exclusions".
- **Other inventory text:**
  - `docs/testing/CI_WORKFLOWS.md:205` says "five default gmstep controls".
  - The README count rows are marked historical and not re-measured (`tb/verilator/milan_dp/README.md:972-990`).
  - The README row for `obj_gmstep` (103 / 0) is reproduced by my clean run: `receipts/G0_clean.log`, `== gmstep: checks: 103 failures: 0 ==`.
- **tkdiag narrative.** `tb/verilator/tkdiag/sim_main.cpp:650-652` now names two genuine causes and says "A PHC-only step supplies no request (#602)". The comments at `:696` and `:754` now name a received CRF toggle, and the T17/T18 check names say "request". `mcr_mutants.py:69-78` expects the renamed strings.
- **tkdiag run at this head** (`receipts/tkdiag_head.log`): `checks: 96 failures: 0`, and all four engine mutants are caught by the renamed checks (5/5).

### (3) The option-off `mr` checks are event-relative, and R366-1's three controls behave as specified: MET, with F1

- **What the checks compare:**
  - The adjtime check (`tb/verilator/milan_dp/sim_main.cpp:574-580`) compares `mcr_mr_v_w[0]` just before the adjtime write with its value after the following `snap()`.
  - The settime check (`:1061`, `:1081-1083`) compares the level just before the settime with the `mr` bit of the first post-holdover frame.
- **R366-1's three controls**, run through my own driver (`probes.py`, receipts `O1`-`O3`):

| Control | Checks broken |
|---|---|
| O2 adjtime-only | only `CLKV: PHC-only steps leave INTERNAL mr unchanged (#602)` |
| O1 settime-only | `CLKV: the settime leaves mr unchanged (#602)` and `settime adds no MEDIA_RESET`; the adjtime check stays clean |
| O3 both causes | all three; the settime check now fails as got=0 exp=1, because the settime toggles back from the adjtime's level |

- **Clean baseline.** The option-off clean run passes 234/0 (`receipts/O0_clean.log`).
- **Sibling rule.** The runner's `stays_clean` rule (`gmstep_mutants.py:93`, `:290`) enforces the sibling exclusions. The author's published `gmstep-mutants.log` (author-r2) reports the same broken-check sets.
- **Remaining gap.** The adjtime window is short. That is F1.

### (4) The coincident scenario is real, and suppression kills it: MET, with the F2 suggestion

- **The scenario is real.** `check_coincident_restart` (`sim_gmstep.cpp:1098-1142`) drives only real inputs: a received CRF PDU with a toggled `mr`, then a CSR settime at 32 delays. It grades six things:
  - one received toggle per trial;
  - one settime per trial;
  - the PHC actually stepped each time;
  - at least one observed same-cycle overlap;
  - more than eight PDUs per trial, with the sink still locked;
  - exactly one outgoing toggle per trial.
- **Why the overlap is the real one.**
  - The observed signals are `crf_rx.prev_mr_r` and `csr.ptp_load_p`.
  - `ptp_load_p` is `cfg_ptp_cmd_load` itself (`hdl/common/csr/milan_csr.sv:2632`), which feeds `media_rebase_p_w` (`milan_datapath.sv:3132`).
  - `mr_toggle_p_o` is registered off the same accept edge as `prev_mr_r` (`KL_crf_rx.sv:380`, `:468`, `:586`).
- **All 42 feed phases.** The clean head binary was run at every `GMSTEP_FEED_DELAY` from 0 to 41 (`feed_sweep.sh`; `receipts/feed_sweep_summary.txt`, `feed_sweep_rc.txt`). Every run gave rc 0 and 103/0, with the overlap at delay 8, exactly one toggle in all 32 trials, and the render re-base at step pulse +132.
- **Controls:**

| Probe | Result |
|---|---|
| G3: same-cycle veto `& ~media_rebase_p_w` (the author's control) | caught only by `coincident: a PHC step neither adds nor suppresses the CRF restart` (the delay-8 trial sends 0 toggles) |
| G4: one-cycle-late veto (my probe, registered `media_rebase_p_w`) | caught by the same check (the delay-7 trial sends 0 toggles) |
| G2: CRF propagation removed | caught by `CRF control: selected CRF mr propagates exactly once` and by the coincident check (32 wrong trials) |
| G1: re-base restart term restored | caught by `restart: a PHC-only step leaves outgoing mr unchanged` and `restart: a PHC-only step adds no MEDIA_RESET`. The coincident check itself passes 32/32: under the engine's pending-merge rule a coincident extra request merges (see F2). |
| G5: settime-only cause restored, gmstep leg | passes the leg, as expected. Settime is caught by the option-off leg (O1). |
| G7: same, delayed by 16 cycles, gmstep leg | passes the leg, as expected. Settime is caught by the option-off leg (O1). |
| G6: adjtime cause delayed by 16 cycles, gmstep leg | caught by the isolated-step checks. The plane step path is covered there. |

- So restoring the re-base term is killed by the leg, and suppression is killed by the new scenario. By construction, the new scenario alone cannot kill a restored re-base.

## Findings

### F1 - MINOR - Tests, Robustness - the option-off adjtime check misses an adjtime-caused `mr` change that lands 16 or more cycles after the event

- **Where:**
  - `tb/verilator/milan_dp/sim_main.cpp:574-580`: the "after" sample is taken after one `snap()`, about 13 cycles.
  - `:1061`: the settime baseline, read thousands of cycles later.
- **Evidence (executed, `probes.py`).** Each probe restores `eff_ptp_adjust_w` as a restart cause through a delay:

| Delay | Result | Receipts |
|---|---|---|
| 2, 4, 8, 12 cycles | caught by the adjtime check | `receipts/O6_adjtime_delay{2,4,8,12}.log` |
| 16 cycles | rc 0, 234/0: survives every check | `receipts/O4_adjtime_delay16.log` |
| 256 cycles | rc 0, 234/0: survives every check | `receipts/O5_adjtime_delay256.log` |

- **Why it survives.** The late toggle is absorbed into `settime_mr_before`, so the settime check stays clean, and no absolute check remains.
- **Contrast with round 1.** At round 1 the absolute frame check graded the same cause whatever its delay.
- **Authority:**
  - AGENTS.md §6 Tests: "Each new test can fail for the defect it claims to detect."
  - Round-2 assignment 5860151273 item 3: "Each fails if and only if its event changes `mr`."
  - This inventory already treats "N cycles late" as a defect class: "tu reaches the talkers four cycles late" and "the policy level misses an extra addend stage".
- **Impact.** Suppose a later change re-introduces software adjtime as an `mr` cause under INTERNAL through any path slower than about 13 cycles: a pipeline or CDC stage, or an adoption the engine defers behind an incomplete hold. The only check that grades adjtime then passes, and so does the rest of the leg. The gmstep leg does not cover this: its adjtime is the plane step, and G6 shows the plane path is caught.
- **Lens note.** Not filed under Conformance. The assignment names "the `mr` level just before the event compared with just after it" as an acceptable form, and its three named controls behave as specified. Every cause the RTL can present today is same-cycle. This is a test-strength gap, not an unmet acceptance criterion.
- **Required outcome.** The adjtime check sees any `mr` change that the adjtime causes before the settime baseline is taken. For example, it could compare against a level read after the leg's existing settle interval, or count the transmitted toggles between the adjtime and the settime baseline. A delayed adjtime cause must fail the adjtime check and leave the settime check clean.
- **Verification:**
  - A delayed-cause control (for example 16 and 256 cycles) is caught by the adjtime check only.
  - The three existing controls keep their current broken-check sets.
  - The clean leg stays 234/0.

### F2 - SUGGESTION - Tests - the coincident check's name claims "neither adds" but cannot fail on an added request

- **Where:** `tb/verilator/milan_dp/sim_gmstep.cpp:1141`, and README `:705`.
- **Evidence:** G1 (the re-base term restored), G5 and G7 (settime restored, immediate or delayed) all pass all 32 coincident trials with one toggle each. The engine's pending merge makes a coincident extra request invisible on the wire. The "adds" direction is graded by the isolated-step checks (`sim_gmstep.cpp:1065`, `:1075`).
- **Suggestion:** name the check for what it can fail on (for example "a coincident PHC step does not suppress the CRF restart"), or note the merge limitation beside it. Optional.

### F3 - SUGGESTION - Docs - leftover hedges and wording

- **README.** `tb/verilator/milan_dp/README.md:680` says "The #387 run passed at all 42; later counts require re-measurement". At this head all 42 feed delays pass 103/0 (`receipts/feed_sweep_summary.txt`), so the sentence could state the measurement.
- **Makefile.** `tb/verilator/milan_dp/Makefile:20-21` still calls the option-off checks "#387 mr checks".
- Optional.

## Prior public findings on this PR, resolved or retained at this head

This section covers my own round 1. It was written after the independent pass above.

| R366-1 finding | Status at 471892a9 | Evidence |
|---|---|---|
| F1 MAJOR, Docs: stale current documents | **RESOLVED** | Item (1): all four named locations and the CHANGELOG are corrected; the scan finds zero current-contract hits |
| F2 MINOR, Docs and Tests: campaign documents and the tkdiag narrative | **RESOLVED** | Item (2): TESTING/CI_WORKFLOWS/README counts, defaults and triggers match `CONTROLS`; count rows are marked historical; the tkdiag narrative and names are corrected; tkdiag 96/0 and 4/4 |
| F3 MINOR, Tests: the settime check graded the absolute level | **RESOLVED** as specified | Item (3): the three controls behave exactly as required. The adjtime half of the fix has a new, narrower gap, filed as R366-2 F1. |
| F4 SUGGESTION, Tests and Robustness: no coincident scenario | **TAKEN and verified** | Item (4): the overlap is observed at every feed phase, and same-cycle and one-cycle-late vetoes are caught. See F2 for the check's name. |

## Reviewer-owned lens ledger (R366-2)

| Lens | Status | Examined artifacts (at the head) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling 5859297355 and assignments 5859299480/5860151273 against `milan_datapath.sv:3124-3134` (unchanged since round 1, `receipts/delta_scope.txt`); gmstep 103/0 at all 42 feed delays (isolated step: 0 `mr` toggles and +0 MEDIA_RESET; source and CRF controls: 1 toggle each; coincident: 1 toggle in 32/32 trials); option-off 234/0; the ruling as stated in the CHANGELOG, REGISTER_MAP, FPGA_DESIGN, ROADMAP and GM_LOSS_RECOVERY | R366-2 | `471892a9bcc2d26fdcfc19db01949ecea83c5e0f` |
| RTL | CLEAN | `hdl/` byte-identical to `49012143` (`receipts/delta_scope.txt`); the trigger `milan_datapath.sv:3132-3134` and `KL_media_clock_restart.sv` `mcr_track` (merge/hold) checked against the G1/G3/G4 outcomes; `csr.ptp_load_p` = `cfg_ptp_cmd_load`; `KL_crf_rx.sv:380,468,586` pulse timing; `lint_rtl.py --check --jobs 8` PASS 90 <= 90 (`receipts/rtl_lint.log`); tkdiag 96/0 + 4/4 | R366-2 | `471892a9bcc2d26fdcfc19db01949ecea83c5e0f` |
| Robustness | UNCLEAN (F1 open) | Delayed-cause probes O4/O5/O6 (F1); coincident offsets G3/G4 (same cycle and one cycle late); 42 feed phases; INTERNAL feature-off leg with causes combined (O1-O3); CRF-selected leg with delayed plane adjtime (G6) | R366-2 | `471892a9bcc2d26fdcfc19db01949ecea83c5e0f` |
| Tests | UNCLEAN (F1 open; F2 is a SUGGESTION) | `sim_main.cpp:574-580,1061-1086`; `sim_gmstep.cpp:1098-1142`; `gmstep_mutants.py:93,110-201,290`; `tkdiag/sim_main.cpp`, `mcr_mutants.py`; 18 probe runs (`receipts/summary.txt`); author-r2 `gmstep-mutants.log` cross-checked | R366-2 | `471892a9bcc2d26fdcfc19db01949ecea83c5e0f` |
| Docs | CLEAN (F3 is a SUGGESTION) | `stale_scan.sh` → `receipts/stale_doc_scan.txt` (87 hits read, 0 stale); `CHANGELOG.md:16,116-141`; `REGISTER_MAP.md:128-131`; `FPGA_DESIGN.md:178-180`; `MILAN_V12_ROADMAP.md:360-362`; `GM_LOSS_RECOVERY.md:146-240,268`; `TESTING.md:273`; `CI_WORKFLOWS.md:205`; `milan_dp/README.md:656-722,969-990`; docs gates (`receipts/docs_gates.txt`): docs_check, doc_style, doc_paths, gen_toc, em_dash, hygiene, module matrix and `git diff --check`, all rc 0 | R366-2 | `471892a9bcc2d26fdcfc19db01949ecea83c5e0f` |

## Commands and receipts (all run in the foreground)

- **Tool identity** (`receipts/tools_identity.txt`). The assignment-named Verilator path does not exist on this host. I used the #602 manager wrapper, which reports `Verilator 5.050 2026-07-01 rev v5.050`, the project pin (`rtl-fast.yml:18`). Its binary hash is recorded.
- **Probes.** `python3 probes.py <verilator> <names...>` ran in batches of four builds with `VERILATOR_JOBS=2`, never more than 8 jobs:
  - `G0`-`G7` are on the gmstep leg; `O0`-`O6` are on the option-off leg.
  - Each probe plants its edit into a copy of `milan_datapath.sv` in a scratch clone (`DP_SRC` override, private `Mdir`), builds through the suite's own recipe and runs once.
  - Per-probe logs are in `receipts/`, and `receipts/summary.txt` summarizes them.
- **Feed sweep.** `feed_sweep.sh <G0 obj> <suite> <out>`: 42 runs, 8 at a time, all rc 0.
- **tkdiag.** `make` of `tb/verilator/tkdiag` in the scratch clone: rc 0, 96/0, mutants 5/5.
- **Lint and docs gates.** Lint ran in the scratch clone. The docs gates ran in the scratch clone; hygiene and the module matrix ran in `$CLONE`, because they need the registered submodules. All rc 0.
- **Stale scan.** `stale_scan.sh $CLONE`.
- **Hosted checks at the head** (read-only; `receipts/hosted_check_runs_at_head.txt`):
  - Completed successfully: bdd-conformance, changes, docs-check-no-git, elaborate, full-ci-gate, verilator-lint, wire-accountability and Yosys shards 0-3.
  - Still in progress when read: docs-check, Verilator shards 0-4 and yosys-elaboration.
  - SKIPPED by design: Physical gPTP.
- **Clone integrity after all probes** (`clone_integrity.sh $CLONE` → `receipts/clone_integrity.txt`):
  - HEAD, tree and index tree equal the reviewed ids.
  - Status is empty, including untracked and ignored files; the `scripts/__pycache__` created by the in-clone gates was removed.
  - All 930 tracked blobs and modes match HEAD.
  - The gitlinks `gptp-processor 5dce647a`, `protocol-processor 870ff88a` and `third_party/verilog-axis 48ff7a7e` are at their pins with 0 dirty entries.
  - `external` is uninitialised and empty, as before this round.

## Real limits

- **Not run, by assignment:** the full `milan_dp` `run`, the whole `gmstep_mutants.py --all` runner, the builder banks, the full parent/PP/gPTP/Yosys banks, OOC (the area question is closed), act and the hosted jobs.
  - This round planted the six author controls that bear on #602 (the three option-off controls, suppression, the restored re-base term and CRF propagation) plus ten probes of my own (G4-G7, O4, O5 and four O6 delays).
  - The other twelve controls in the inventory were not re-run; they cover slew, render, `tu` and licence. They and their targets are unchanged since R366-1, which re-ran all 16 then, and the author's published round-2 log reports 20/20 at this head.
- **Artifact identity.** The five-configuration identity was not re-run. The delta touches no `sw/`, `configs/` or `hdl/` file (`receipts/delta_scope.txt`), and R366-1 verified 50/50 at `49012143`.
- **Simulation scope.** gmstep is a compressed-time model: the TDM clocks are held, the DRP answers zero, and the talker is opened by the escape bit. This round gives no lwSRP, physical-clock or placed-area proof. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Manager evidence.** The manager's source banks at this head are referenced by the assignment. I did not find a public receipt for them other than the [A388] packet, and I did not re-execute them.

## Pending manager duties

- Route F1 back to the executor. A fix commit un-covers Tests and Robustness, and they must be re-reviewed at the new head.
- Hosted exact-head acceptance: docs-check, Verilator shards 0-4 and yosys-elaboration were in progress when read. Act-first local replication is also still needed.
- The candidate-merge build on live dev `63de19bdb600b6d85cb3ea2f85d705874b24d39d` (source validation here was against base `6d5ebd73`), and the composition check of `GM_LOSS_RECOVERY.md` with PR #601 (#593).
- The external independent verdict and the full completion bar. No merge without explicit maintainer authorization.

## Other public round-1 findings (R367-1), reconciled at this head

This section was written after the verdict, findings and ledger above. None of them changed after reading R367-1.

| R367-1 finding | Status at 471892a9 | Evidence |
|---|---|---|
| F1 MINOR, Docs: FPGA_DESIGN, REGISTER_MAP, ROADMAP and CHANGELOG state the superseded contract | **RESOLVED** | Same locations as R366-1 F1; item (1) and `receipts/stale_doc_scan.txt` |
| F2 MINOR, Docs and Tests: the TESTING.md routing row and the tkdiag header | **RESOLVED** | Item (2). The row now reads 15 + 3 = 18 against `CONTROLS` (the head has 18 after the two round-2 additions), 5 defaults, no stale option-off wording, and `KL_media_clock_restart.sv` among its triggers. The tkdiag header describes genuine requests; tkdiag 96/0 and 4/4. |
| F3 SUGGESTION, Tests and Robustness: the coincident guarantee was only structural | **TAKEN and verified** | Item (4). Suppression, R367's RV5 (identical to G3), is now caught at run time, and so is a one-cycle-late veto (G4). The "adds" half stays with the isolated-step checks and the gate-1b pin (R366-2 F2). |
| F4 SUGGESTION, RTL: the rename control shows determinism, not insensitivity | **No action needed in this PR** | The area question was closed by round-2 assignment 5860151273 (R366-1 check 5). The delta touches no RTL and no area evidence. |

None of R367-1's findings remain open at this head. R366-2 F1 is new in this round; neither round-1 report could have raised it, because the check it concerns was written in round 2.

R366-2 FINISHED
