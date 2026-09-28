[R367] NEGATIVE - exact head 471892a9bcc2d26fdcfc19db01949ecea83c5e0f

# R367-2: external re-review of PR #603 (issue #602, deliverable 2)

- **Round:** R367-2. This is an external independent reviewer working in a cleared context.
- **Head:** `471892a9bcc2d26fdcfc19db01949ecea83c5e0f`, tree `56f7ac7776008b49081a6faa829a22e649a9913c`. It matches the PR's `headRefOid`.
- **Base:** `6d5ebd7357c1e468e446f18a61527c5be6118a04` is an ancestor of the head.
- **Delta under review:** `49012143..471892a9`, two commits by [A388]:
  - `add85ca6a` isolates the PHC restart exclusions and covers coincident CRF events;
  - `471892a9b` observes the received CRF state independently of propagation.
- **Delta scope:** both commits are one line with no body. The delta touches no path under `hdl/`, `sw/`, `configs/` or any submodule. The RTL and builder are byte-identical to `49012143`.
- **Authorities read:** AGENTS.md, CONTRIBUTING.md and docs/README.md. From issue #602: the body, ruling 5859297355, assignment 5859299480, scope correction 5859621253 and round-2 assignment 5860151273, plus the [A388] TAKEN and REVIEW READY comments. Also the cited clauses as the ruling quotes them (1722-2016 §4.4.4.3, §4.4.4.7 and §10.4.3; Milan v1.2 Annex B.1.2), and the full diff `6d5ebd73..471892a9`.
- **Verdict basis:** one MINOR documentation finding is open (F1). F1 is the residual of this round's required item 1: a current contract document still states the superseded restart initializer. The functional result, the new tests and the controls are correct and reproduce.

## The four assigned checks

### (1) No current document says a PHC-only step or re-base toggles `mr` or counts MEDIA_RESET: NOT MET (F1)

**Fixed at this head:**

- `docs/fpga/FPGA_DESIGN.md:178-180`, `docs/reference/REGISTER_MAP.md:128-130` and `docs/MILAN_V12_ROADMAP.md:360-362` now state the #602 exclusion and cite the ruling.
- `CHANGELOG.md:16` and `:116-142` record the reversal ("The #602 ruling reverses its PHC-only restart obligation ... A PHC-only re-base leaves `mr` and MEDIA_RESET unchanged").
- `docs/testing/CI_WORKFLOWS.md:205` now names five default controls.

**The reviewer's own scan:**

- `stale_scan_r367_2.py` covers every tracked text file outside `docs/history/**` and the submodules. It returned 185 proximity hits in 26 files.
- All are classified in `receipts/stale_scan_classification.md`.
- Two hits are stale. Both are in `docs/integration/BAREMETAL_FIRMWARE.md`, at `:1469` and `:1471`; see F1.

### (2) TESTING.md row, tkdiag narrative and restart-engine text: MET

**The row at `docs/testing/TESTING.md:273` matches the inventory:**

- **Counts:** it names fifteen gmstep controls and three option-off controls. `gmstep_mutants.py` `CONTROLS` holds 18 entries: 15 with `leg="gmstep"` (the three #545 slew controls among them) and 3 with `leg="option-off"`.
- **Default sweep:** it names the five controls with `acceptance=True` correctly (restored PHC cause, missing source change, missing CRF propagation, extra identity re-base, missing step re-base).
- **Routing:** the PHC-step `mr` routing is gone; the row now says "event-relative PHC-only restart exclusions".
- **Triggers:** `hdl/ieee1722/avtp/KL_media_clock_restart.sv` is among them.
- **Cross-check:** `tb/verilator/milan_dp/README.md:689-712` agrees. Its control table has 15 rows, and it says "eighteen" controls in all and five in the sweep.

**tkdiag and restart-engine text:**

- `tb/verilator/tkdiag/sim_main.cpp:650-652` now reads "Two genuine causes, a CRF disruption and a received CRF mr toggle, reach restart_p_i. A PHC-only step supplies no request (#602)."
- The stimulus comments at `:696` and `:754` and every T17/T18 check name now say "request".
- `mcr_mutants.py:69,74,78` carry the renamed check strings.
- `KL_media_clock_restart.sv:60-62,105-109,168-172` names no PHC step as a restart cause.
- No other harness that instantiates `KL_media_clock_restart` (outside `milan_dp`) mentions a PHC step.
- **Run:** `make -C tb/verilator/tkdiag` gives rc 0, 96 checks and 0 failures, with the unmutated engine passing and 4 of 4 mutants caught by their renamed checks (`receipts/tkdiag_make.log`).

### (3) The option-off settime and adjtime `mr` checks are event-relative, and the three controls behave as specified: MET

**The two checks:**

- **adjtime:** `sim_main.cpp:574` samples `mcr_mr_v_w[0]` before the CLKV adjtime. `:579-580` compares it with the level after the adjtime.
- **settime:** `:1061` samples the level before the settime. `:1081-1083` compares the first post-holdover frame's wire `mr` with it.
- **MEDIA_RESET:** it stays a delta across the settime (`:1085-1086`).
- **Removed check:** the old absolute check on the ownerless frame (`mr` equal to 0) is gone.

**The reviewer's own plants** (`receipts/summary.tsv`) ran through the suite's `option-off-build` recipe. Every run elaborated 234 checks.

| Probe | Result | Failed checks |
|---|---|---|
| O0 clean | rc 0, 0 failures | none |
| O1 adjtime only (`\| eff_ptp_adjust_w`) | rc 1 | the adjtime check only |
| O2 settime only (`\| cfg_ptp_cmd_load`) | rc 1 | the settime `mr` check and `settime adds no MEDIA_RESET`; the adjtime check is clean |
| O3 both (`\| media_rebase_p_w`) | rc 1 | the adjtime and settime `mr` checks and `settime adds no MEDIA_RESET` |
| O4 event-relative witness: the engine resets `tgt_r` and `mr_o` to 1 | rc 0, 0 failures | none |

**Reading the table:**

- Adjtime-only breaks only the adjtime check. Settime-only and both-causes each break the settime check. That is exactly the behaviour the assignment specifies.
- O4 shows the checks grade a change caused by the event, not an absolute level. With a pre-event level of 1 and no causing event, both checks pass. The removed absolute form would have failed.
- The runner enforces the sibling exclusions: `gmstep_mutants.py:288-292` fails a control that also breaks one of its `stays_clean` checks.

### (4) The coincident scenario is real; suppression and removed propagation kill it: MET, with one bound (F2)

**The scenario is real.** `sim_gmstep.cpp:1094-1142` drives only real inputs:

- a CRF PDU carrying toggled `mr` on the wire;
- a software settime through CSR `0x510`/`0x514`/`0x520`, at 32 offsets.

It grades the following:

- received toggles (from `crf_rx.prev_mr_r`, independent of propagation);
- settime pulses;
- actual PHC steps;
- at least one observed same-cycle overlap of the received toggle with `ptp_load_p`;
- at least eight outgoing PDUs per trial;
- the CRF sink staying locked;
- exactly one outgoing toggle per trial.

The phase runs last (`:1187`).

**Measured:**

- **Clean:** 103 checks and 0 failures at feed delay 0 (`receipts_gmstep_clean_d0.log`). The overlap lands at trial delay 8.
- **All 42 feed delays** (`GMSTEP_FEED_DELAY` 0..41, `receipts/feed/feed_sweep.tsv`): rc 0 and 103/0 each, with exactly one overlapping trial in every run. The overlap guard therefore does not depend on the start phase.
- **G2** (a one-cycle veto, `& ~media_rebase_p_w`) fails only `coincident: a PHC step neither adds nor suppresses the CRF restart`. The overlap trial transmits 0 toggles; the other 31 transmit 1.
- **G3** (CRF propagation removed) fails `CRF control: selected CRF mr propagates exactly once` and the coincident check. `every trial consumes one received CRF toggle` stays green, so the received-side observation does not depend on the propagation wire, as `471892a9` intends.
- **G1** (re-base term restored) is killed by the leg, at `restart: a PHC-only step leaves outgoing mr unchanged` and `restart: a PHC-only step adds no MEDIA_RESET`. The coincident check itself stays green: all 32 trials transmit one toggle. G4 (settime-only restored) passes the whole gmstep leg, 103/0; option-off control O2 kills it instead.

The coincident check therefore grades the "does not suppress" half at run time. The "does not add" half is graded by the isolated-step checks and the option-off controls, not by this check. This is expected: `KL_media_clock_restart.sv:236-246` merges a request that lands on a pending restart. See F2.

**Default sweep:** `python3 gmstep_mutants.py` gives rc 0 (`receipts/gmstep_mutants_default.log`). The clean leg passes, and all five default controls are caught by their named checks.

## Findings

### F1 - MINOR - Docs, Conformance - the bare-metal gate contract still states the PHC-inclusive restart initializer

**Location:** `docs/integration/BAREMETAL_FIRMWARE.md:1469` and `:1471`, at the exact head.

- `:1469`: "`media_rebase_p_w` has exactly three references | Its initializer and two readers: `render_recentre_p_w` and `mcr_restart_p_w`."
- `:1471`: "`mcr_restart_p_w` is exactly `(crf_clk_selected_r & ((tkd_crflk_q_r & ~crf_locked_w) | crf_mr_toggle_p_w)) | media_rebase_p_w` | The step is ungated by clock selection."

**Authority/evidence:**

- **Round-2 required item 1 (5860151273):** "no current document says that a PHC-only step or re-base toggles `mr` ... and every other hit of the reviewers' stale-document scan outside `docs/history/**`."
- **AGENTS.md section 6, `Docs`:** "Changed contracts are reflected in authoritative docs."
- **The document is current:** it is the gate contract that `sw/builder/test_builder.py:3046-3054` loads as `docs_source`.
- **The gate it describes changed in this PR** (`49012143`):
  - `test_builder.py:10719` now censuses `"media_rebase_p_w": 2`;
  - `:10774-10780` pins the initializer without the re-base term;
  - `hdl/milan/milan_datapath.sv:3132-3134` has no restart reader of `media_rebase_p_w`.
- **The rows name the removed coupling:** "The step is ungated by clock selection" plus an initializer that ORs the PHC re-base into `restart_p_i` is the #387 PHC-step `mr` cause that #602 removed.
- **Neighbouring rows are still true:** `:1468` (censuses 5 and 3 at `test_builder.py:10705,10716`) and `:1470` (the render initializer).
- **Round of origin:** this is the unresolved residual of R367-1 F1 (MINOR in R367-1; the merged round-2 item is carried as MAJOR in 5860151273). No earlier scan reported this file.

**Impact:**

- A firmware or builder maintainer who reads the gate contract is told that the PHC step feeds the media-clock restart, ungated. That is the pre-#602 behaviour.
- They are also told that the census is three references, while the gate enforces two.
- So the contract document and the enforced gate disagree at the merge head, on exactly the coupling this issue reverses.

**Required outcome:** at the merge head, the two rows state what the gate enforces:

- `media_rebase_p_w` has two references (the initializer and `render_recentre_p_w`);
- `mcr_restart_p_w` is `crf_clk_selected_r & ((tkd_crflk_q_r & ~crf_locked_w) | crf_mr_toggle_p_w)`, with no PHC-step term;
- the rows cite #602.

Moving this to another Issue does not clear the lenses (AGENTS.md section 7).

**Verification:**

- Re-run `stale_scan_r367_2.py` (or an equivalent scan) at the new head, and confirm there is no STALE hit outside `docs/history/**`.
- Read both rows against `test_builder.py:10705-10720` and `:10770-10781`.
- Re-run `scripts/docs_check.py` and `scripts/check_doc_paths.py`, expecting rc 0.
- The builder test loads this document, so the manager should also re-run the builder bank after the fix.

### F2 - SUGGESTION - Tests - the coincident check's name claims "neither adds" but can fail only for suppression

**Location:** `tb/verilator/milan_dp/sim_gmstep.cpp:1141`, the check `coincident: a PHC step neither adds nor suppresses the CRF restart`. The same name is in `README.md:705` and `gmstep_mutants.py:199`.

**Evidence:**

- G1 (the re-base term restored) and G4 (settime restored) both leave this check green. Every trial transmits one toggle (`receipts/G1_rebase_restored.log`, `receipts/G4_settime_restored.log`).
- The reason is structural. All 32 offsets put the settime inside the CRF restart's pending window, so a restored PHC request merges (`KL_media_clock_restart.sv:236-246`).
- Nothing escapes the inventory:
  - G1 is killed by the isolated-step checks, in the default sweep;
  - G4 is killed by the option-off leg (O2 here, and the lane's `software settime is restored as an mr cause` control);
  - the clean option-off harness in `run` fails for the same RTL.
- The docs describe the phase accurately ("exactly one outgoing toggle"; "must reject that suppression").

**Optional outcome:** do one of these:

- rename the check to its measured scope, for example "a coincident PHC step does not suppress the CRF restart";
- or add offsets past the first PDU at the adopted level, still inside the step's `tu` window, where a restored PHC cause would transmit a second toggle.

### F3 - SUGGESTION - Docs - two dated phrasings in the milan_dp suite

**Locations:**

- `tb/verilator/milan_dp/Makefile:19-20` still says "three controls of the option-off leg's #387 mr checks". Those are #602 exclusion checks.
- `tb/verilator/milan_dp/README.md:680` says "later counts require re-measurement". This round measured 42/42 feed delays at 103/0 (`receipts/feed/feed_sweep.tsv`).

Neither text claims that a PHC step toggles `mr`.

**Optional outcome:** update the wording.

## Reviewer-owned completion ledger (R367-2)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Ruling 5859297355 and round-2 items 1-4 against: `milan_datapath.sv:3121-3134` (no PHC term in `mcr_restart_p_w`); `sim_gmstep.cpp` `restart:`, `source control:`, `CRF control:` and `coincident:` checks; `sim_main.cpp:574-580,1061-1086`; probes O0-O4 and G0-G4; the 42-delay feed sweep. Item 1 is not met at `BAREMETAL_FIRMWARE.md:1469,1471` | R367-2 | 471892a9bcc2d26fdcfc19db01949ecea83c5e0f |
| RTL | CLEAN | The delta has no `hdl/` change (`git diff 49012143..471892a9 -- hdl` is empty). `milan_datapath.sv:3132-3134,3163` and `:6053-6055`. `KL_media_clock_restart.sv:219-257` (request, merge and hold logic, as the new tests rely on it). The `crf_rx.prev_mr_r` and `csr.ptp_load_p` observation points used by `sim_gmstep.cpp:459-468`. R367-1's lint and cone results at `49012143` hold, since nothing in RTL scope has changed since | R367-2 | 471892a9bcc2d26fdcfc19db01949ecea83c5e0f |
| Robustness | CLEAN | 42 accept phases × 32 coincidence offsets, 103/0 each, one overlap each (`receipts/feed/`). Repeated settime (32 steps in one run). INTERNAL option-off adjtime then settime, and a non-zero pre-event `mr` level (O4). A one-cycle veto (G2). Propagation removal with receive-side independence (G3) | R367-2 | 471892a9bcc2d26fdcfc19db01949ecea83c5e0f |
| Tests | CLEAN (F2 is a SUGGESTION) | `sim_gmstep.cpp:1094-1142,1187`; `sim_main.cpp:571-580,991-996,1058-1086`; `gmstep_mutants.py:83-94,180-201,288-292`; `tkdiag/sim_main.cpp:647-760`; `mcr_mutants.py:66-78`; `Makefile:17-20,397-399`. Runs: gmstep clean 103/0; default sweep 5/5 caught; probes O1-O3 match the spec and O4 passes; G1, G2 and G3 killed, G4 killed only on the option-off leg; tkdiag 96/0 with 4/4 caught | R367-2 | 471892a9bcc2d26fdcfc19db01949ecea83c5e0f |
| Docs | UNCLEAN (F1) | Correct: CHANGELOG.md:16,116-142; MILAN_V12_ROADMAP.md:360-362; FPGA_DESIGN.md:178-180; REGISTER_MAP.md:128-130; GM_LOSS_RECOVERY.md:142-157,170-243; TIME_SYNC.md:113,255-261,354; CI_WORKFLOWS.md:205; TESTING.md:273; milan_dp README.md:640-744,969-997; tkdiag narrative. Stale: BAREMETAL_FIRMWARE.md:1469,1471. The 185-hit scan is classified in `receipts/stale_scan_classification.md`. Gates `docs_check`, `check_doc_paths`, `check_doc_style` and `check_hygiene`: rc 0 | R367-2 | 471892a9bcc2d26fdcfc19db01949ecea83c5e0f |

## Evidence

The probes ran on a disposable copy of the exact head under `scratch/` (not published), with its submodules at their gitlinks: `gptp-processor` `5dce647a`, `protocol-processor` `870ff88a`, `third_party/verilog-axis` `48ff7a7e`.

**Simulator:**

- Verilator 5.050 (rev v5.050).
- The assigned wrapper path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist.
- The reviewer used the manager tool wrapper at `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator`. Its version is confirmed, and it is recorded in `receipts/tool_identity.txt`.

**Commands:** listed in `PROBES.md`.

| Probe | Result |
|---|---|
| gmstep clean, delay 0 | rc 0, 103/0 |
| gmstep clean, feed delays 0..41 | 42/42 rc 0, 103/0, 1 overlapping trial each |
| `gmstep_mutants.py` (default) | rc 0; clean pass; 5/5 caught |
| option-off O0-O4 | as tabulated in check (3) |
| gmstep G1-G4 | as in check (4) |
| tkdiag | rc 0, 96/0, 4/4 mutants caught |
| docs, doc-path, doc-style, hygiene, C++ and Python idiom gates | all rc 0 (`receipts/gate_*.log`) |
| `git diff --check 6d5ebd73 471892a9` | clean |
| commit format | 5 commits, one line each, no body or trailers |
| hosted snapshot (read-only, 2026-09-28 00:29 UTC) | see below (`receipts/hosted_snapshot.json`) |
| review-clone integrity after all probes | see below (`receipts/clone_integrity.txt`) |

**Hosted snapshot:**

- Completed with success: `verilator-lint`, `elaborate`, `full-ci-gate`, `changes`, `bdd-conformance`, `docs-check-no-git`, `wire-accountability`, Yosys shards 0-3, and Verilator shards 0, 2 and 3.
- Still in progress: `yosys-elaboration`, `docs-check`, and Verilator shards 1 and 4.
- Skipped, not executed: `Physical gPTP`.

**Review-clone integrity:**

- HEAD and tree match the exact head.
- The 934-entry index is identical to the pre-probe snapshot.
- The worktree and index show no difference from HEAD (bytes and modes), with no untracked or ignored files.
- The gitlinks `external` `efeb541a` (not checked out), `gptp-processor` `5dce647a`, `protocol-processor` `870ff88a` and `third_party/verilog-axis` `48ff7a7e` match HEAD, and each checked-out submodule is clean.
- The review clone was never modified.

## Prior public review findings on PR #603, resolved or retained at this head

This section was written after the verdict, findings and ledger above. The only reports read were R367-1 (5860047260) and R366-1 (5860148636). No round-2 report of the other reviewer was read.

| Prior finding | Status at `471892a9` | Evidence |
|---|---|---|
| R367-1 F1 (MINOR, Docs) = R366-1 F1 (MAJOR, Docs): current documents state the PHC-step `mr`/MEDIA_RESET rule | **Retained, narrowed to F1 above.** All the named locations are resolved (FPGA_DESIGN, REGISTER_MAP, ROADMAP, CHANGELOG). The residual is `BAREMETAL_FIRMWARE.md:1469,1471` | check (1); `receipts/stale_scan_classification.md`. R366-1's own grep (`PHC step toggles\|toggles mr once\|counts that toggle in MEDIA_RESET`, outside history) now matches only the legitimate source-change check names |
| R367-1 F2 (MINOR, Docs/Tests) = R366-1 F2 (MINOR, Docs/Tests): TESTING row, CI budget text, README counts rows, tkdiag narrative | **Resolved.** TESTING.md:273 counts, defaults, routing and triggers are correct. CI_WORKFLOWS.md:205 says five and states that the historical samples do not measure this candidate. README:975-997 marks the #387 counts as not re-measured and gives gmstep 103/0, which this round reproduced. tkdiag `:647-760`, its check names and `mcr_mutants.py` say "request"; `git grep "ORs both onto restart_p_i"` finds nothing | check (2); `receipts/tkdiag_make.log` |
| R366-1 F3 (MINOR, Tests): the option-off settime `mr` check graded an absolute level | **Resolved.** Both checks are now event-relative. Adjtime-only breaks only adjtime; both-causes and settime-only each break the settime check; the O4 witness passes | check (3); `receipts/summary.tsv` |
| R367-1 F3 (SUGGESTION) = R366-1 F4 (SUGGESTION): no dynamic coincident scenario | **Taken and resolved for suppression.** Suppression is graded at run time, robustly across 42 feed phases. Addition is not graded by the coincident check; that is now SUGGESTION F2 | check (4) |
| R367-1 F4 (SUGGESTION, RTL): the neutral-rename area control | **Closed by the manager.** Round-2 assignment 5860151273 closes the area question through R366-1 check 5; not re-opened | 5860151273 |

## Real limits

- **Not run** (this round was not permitted to run them): the full `milan_dp run` sweep, `make gmstep-mutants --all` (18 controls), the full parent, PP, gPTP, Yosys and builder banks, RTL lint, OOC synthesis, five-configuration artifact identity, and act or the hosted replica.
  - RTL, builder and configurations are unchanged since `49012143`, where R367-1 measured lint, artifact identity and the lane's 16 controls.
  - This round planted its own equivalent of each of the four newest controls: O2, O1 and O3 match the lane's settime, adjtime and both-causes controls, and G2 matches the suppression control.
- **Coincidence probe:** the overlap is observed at `crf_rx.prev_mr_r` and `csr.ptp_load_p`. That they coincide at the gated restart term is shown by G2's kill, not by a waveform.
- **gmstep model:** the leg runs in compressed time, the CRF servo DRP answers zero, and the escape bit licenses the talker. No physical clock continuity, no lwSRP reservation and no placed area are claimed.
- **Hardware:** no physical calibration and no hardware. The skipped physical-gPTP context is not hardware proof.
- **Overlap with PR #601:** that PR also edits `GM_LOSS_RECOVERY.md`. Only this PR's text was judged.

## Pending manager duties

- Resolve F1, then have the Docs and Conformance lenses re-covered at the new head. A docs-only fix leaves the RTL, Robustness and Tests coverage above banked at `471892a9`, unless the fix touches their scope.
- Hosted exact-head acceptance: `yosys-elaboration`, `docs-check`, and Verilator shards 1 and 4 were still in progress at the snapshot. The act/local replica for this head.
- The current-dev candidate at the merge turn: source base `6d5ebd73`, live dev `63de19bd`. That includes the composition with PR #601 in `GM_LOSS_RECOVERY.md` and `TESTING.md`.
- F2 and F3 are optional.

R367-2 FINISHED
