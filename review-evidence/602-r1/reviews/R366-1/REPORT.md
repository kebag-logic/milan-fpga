[R366] NEGATIVE - exact head 49012143b335ea48d6a71c441a05d0c1796887ff

# R366-1: internal independent review of PR #603 (issue #602, deliverable 2)

- Exact head: `49012143b335ea48d6a71c441a05d0c1796887ff`, tree `8b45256c51568c953830ae49e6e24139152ee70d`. Source base: `6d5ebd7357c1e468e446f18a61527c5be6118a04`.
- Reconstructed from the public record, in this order: AGENTS.md, CONTRIBUTING.md, docs/README.md; issue #602 (body, ruling 5859297355, assignment 5859299480, TAKEN 5859307452, STOP 5859611271, scope correction 5859621253, REVIEW READY 5859870644); PR #603's body; the diff and three commits; the public evidence tree `1dab2e7c:review-evidence/602-r1`.
- The verdict and ledger below were written before any other reviewer's report was read. PR #603 carried no review findings when this round started.
- Commands ran in `$CLONE` (the detached review clone). Receipts are in `$PACKET/receipts`, scripts in `$PACKET/scripts`.

## Verdict

**NEGATIVE.** The functional change is exactly what the ruling asks for, and it is proven. The only executable RTL delta is the removal of `| media_rebase_p_w` from `mcr_restart_p_w`. The new gmstep and option-off checks kill every restored PHC cause I planted. The builder edits are forced and weaken nothing. The +182 / +1,606 LUT growth is LUT-mapping sensitivity with no functional meaning: before LUT mapping, the two netlists differ by exactly one `$_OR_` gate.

The verdict is NEGATIVE because Docs and Tests are not clean:

- **F1 (MAJOR).** Four current documents still state the superseded rule, that a PHC step toggles `mr` and counts MEDIA_RESET: the register map, the FPGA design document, the roadmap and the unreleased changelog entry.
- **F2 (MINOR).** The test-campaign documents and the restart-engine harness narrative still describe the #387 inventory and the step-as-restart scenario.
- **F3 (MINOR).** A new option-off check, the settime `mr` check, tests the absolute `mr` level, not whether `mr` changed. Executed controls show it both fails for the wrong cause and passes the defect it names.

## Answers to the six focus items

**(1) Functional RTL delta: confirmed, only the one OR term.**
- A comment-stripped diff of both touched RTL files (`receipts/rtl_code_only_diff.txt`) shows exactly one code change, at `hdl/milan/milan_datapath.sv:3133-3134`: `(crf_clk_selected_r & ((tkd_crflk_q_r & ~crf_locked_w) | crf_mr_toggle_p_w)) | media_rebase_p_w` becomes `crf_clk_selected_r & ((tkd_crflk_q_r & ~crf_locked_w) | crf_mr_toggle_p_w)`.
- `hdl/ieee1722/avtp/KL_media_clock_restart.sv` is comment-only (IDENTICAL CODE). No other file under `hdl/` changed.
- What is untouched:
  - `media_rebase_p_w` (`:3132`) still has exactly one reader, `render_recentre_p_w` (`:6053-6055`).
  - The `tu` paths never read `media_rebase_p_w`. `KL_ptp_clock_validity` takes `cfg_ptp_cmd_load` at `:1951`, and the plane's step reaches it internally. So `tu` is untouched by construction.
  - Source-change detection: `KL_media_clock_restart` `src_change_w`.
  - Selected-CRF disruption and received-`mr` echo: `:3133-3134` and `:3105-3109`.
  - The eight-PDU hold and pending merge.
- tkdiag at the head: 96/96 checks, and all 4 engine mutants caught (`receipts/tkdiag_head.log`).

**(2) gmstep and option-off assertions, controls and mutants: real, with one weakness (F3).**
- Clean runs at the head:
  - gmstep: 64/64 (`receipts/gmstep_head_clean.log`). One step pulse; `tu` rises at the commit, is held 224,891 cycles past the step and then clears; the talker keeps its gate, sequence and rate. The render stage counts one re-base, +132 cycles after the pulse. There are 0 `mr` transitions and a MEDIA_RESET delta of 0. The source control sees 1 toggle; the CRF control sees 1 toggle, with no PHC step supplying it.
  - Option-off: 234/0 (`receipts/optoff_head_clean.log`).
- I re-ran the executor's full inventory (`gmstep_mutants.py --all`): both clean controls pass, and all 16 controls are caught (`receipts/executor_inventory_rerun_gmstep_mutants_all.log`).
- My own ten probes (`scripts/r366_mutants.py`, `receipts/r366_mutants_summary.txt`, `receipts/r366_mutants_results.json`):

| Probe | Leg | Result |
|---|---|---|
| P1 base restart expression restored verbatim | gmstep; option-off | CAUGHT (named check); CAUGHT |
| P2 re-base term restored, but inside the CRF-selection gate | gmstep; option-off | CAUGHT; passes (expected: INTERNAL) |
| P3 GM identity pulse (`gm_recentre_p_r`) ORed into the restart | gmstep | CAUGHT: `mr` changes and MEDIA_RESET moves between commit and step |
| P4 PHC step suppresses genuine restarts (`& ~media_rebase_p_w`) | gmstep | passes: no coincident scenario (F4); statically rejected, see below |
| P5 settime-only cause restored | gmstep; option-off | passes (the plane step is not settime); CAUGHT |
| P6 source-change detector disabled | gmstep | CAUGHT: source control 0 != 1 |
| P7 CRF disruption term removed | gmstep | passes: disruption is outside this leg's scope, so this probe only maps what the leg reaches |
| P8 received-CRF `mr` echo removed | gmstep | CAUGHT: CRF control 0 != 1 |
| P9 whole base datapath under the head's tests | gmstep; option-off | CAUGHT; CAUGHT, but see F3 |
| P10 render re-base dropped, restart intact | gmstep | CAUGHT: one counted re-base 0 != 1 |

- **Static pins.** `scripts/static_pin_probe.py` re-applies the two gate-1b pins this PR edits: the `media_rebase_p_w`/`mcr_restart_p_w` reference census and the exact `mcr_restart_p_w` initializer. It accepts the head and rejects every probe copy, including P4 (`receipts/static_pin_probe.txt`).
- **The "neither adds nor suppresses" clause.** It is guaranteed structurally: no PHC net reaches the restart request. It is pinned statically, not exercised dynamically (F4).
- **The retained negative control is real.** "The step does not re-centre the render stage" and my P10 both fail `render: the GM change is one counted re-base event`.

**(3) `test_builder.py` gate-1b edits: exactly what the ruling forces.**
- The change is 17 lines out and 17 lines in, across 9 hunks.
- Mutant and assertion counts are identical at base and head: 97 `MutantFiles(`, 264 `replace_once(`, 1238 `assert`.
- Each edit follows from the RTL change:
  - census `media_rebase_p_w` 3 -> 2 (`:10719`);
  - the pinned initializer RHS (`:10777-10780`);
  - two mutation anchors re-anchored to the new last line (`:12481-12482`, `:12503-12504`), which still inject `cfg_adp_enable` and an extra reader;
  - the matching diagnostics (`:15103`, `:15115`) and the prose (`:10767`, `:16654-16657`).
- The pin stays exact (whitespace-insensitive equality), so nothing is loosened.
- I did not run the bank (not permitted). The executor's published receipts show rc 0 in both modes (`builder-rv32.json`, `builder-absent.json`).

**(4) Named documents: done and correct, but the change did not reach the rest of the tree (F1, F2).**
- These state the ruling, cite #602 by link, and keep "render re-base" distinct from "media-clock restart":
  - `GM_LOSS_RECOVERY.md:146-168`, `:177-179`, `:205-237`, `:263`;
  - `TIME_SYNC.md:108-113`, `:255-261`, `:354`;
  - `MILAN_COMPLIANCE_MATRIX.md:120`, `:169`, `:206`;
  - `KL_media_clock_restart.sv:63-64`, `:105-109`, `:171-172`;
  - `milan_datapath.sv:3097-3098`, `:3124-3131`.
- `TIME_SYNC.md:108` now says "Each step is one counted render re-base", which is correct.

**(5) OOC area: explained. It is LUT-mapping sensitivity with no functional meaning.**
- Method: `scripts/ooc_probe.py` runs the executor's published recipe (shaped datapath defaults plus `syn/yosys/ooc.sh`) with one change: `synth_xilinx -flatten` is split at `map_luts`, and a `stat` is taken before LUT mapping.
- Results (`receipts/ooc_comparison.txt`, `receipts/ooc/`):
  - **Reproduction.** Base and head post-map cell counts are IDENTICAL to the published `ooc-before`/`ooc-after` stats at both shapes: LUT 97,630 -> 97,812 (+182) and 141,366 -> 142,972 (+1,606). FF, LUTRAM, RAMB, DSP and CARRY4 are unchanged.
  - **Before LUT mapping,** head minus base is exactly `$_OR_ -1` (and one wire) at both shapes. Every other gate class and flop count is equal: `$_AND_`, `$_MUX_`, `$_NOT_`, `$_XOR_`, `$_ORNOT_` and all DFF types. So removing the term defeats no optimisation; nothing had been simplified through the strobe. The whole LUT difference arises inside ABC's LUT mapping.
  - **Control c1:** a comparable one-term edit elsewhere in the same OR (base minus `crf_mr_toggle_p_w`; before mapping: -1 OR, -1 NOT, -1 flop, and -5 AND at 8x8). It gives LUT **-262** (1x1) and **+673** (8x8). One-term edits swing the mapped count by hundreds, and the sign is unrelated to the logic removed.
  - **Control c2:** the head expression with operands reordered gives an identical pre-map netlist and identical LUT counts to the head.
- The executor's rename control (0 delta) cannot probe mapping sensitivity: a rename leaves the netlist unchanged, and so does c2. That is why it "does not reproduce or explain" the delta.
- **Bound.** The only logic removed is one 2-input OR, worth at most one LUT input. The functional scope is proven by the RTL diff and by the pre-map census. The mapped LUT figure varies by about 0.2-1.1% under edits of this size. This says nothing functional. Release area remains a placed-build measurement.

**(6) Five configurations' generated artifacts: byte-identical.**
- `scripts/artifact_identity.py` generated all five `configs/endstation_*.yaml` from the head clone and from a `git archive` of the base, with the unchanged submodule gitlinks. Result: 50/50 artifacts identical (`receipts/artifact_identity.txt`).
- All 50 head hashes also equal the executor's published `generated-after.json` (`receipts/artifact_identity_vs_published.txt`).

## Findings

### F1 - MAJOR - Docs - current documents still state the superseded PHC-step `mr` / MEDIA_RESET rule

- **Where:**
  - `docs/reference/REGISTER_MAP.md:128-130`: "A PHC step toggles `mr` on every running Stream Output whatever the selection, and that output's Table 5.4 MEDIA_RESET counts the toggle it transmits (#387)."
  - `docs/fpga/FPGA_DESIGN.md:178-179`: "A PHC step toggles `mr` whatever the clock-source selection. Every running Stream Output counts that toggle in MEDIA_RESET."
  - `docs/MILAN_V12_ROADMAP.md:360-361`: the same two sentences.
  - `CHANGELOG.md:16` and `:116-128`: the section "Unreleased - one media event per PHC step" says "Every step now toggles `mr` once, on every running stream … whatever the media clock source. Each talker's MEDIA_RESET counts the toggle it sends", and no entry records the reversal.
- **Authority and evidence:**
  - Ruling 5859297355: a PHC-only re-base is not an `mr` cause and adds no MEDIA_RESET.
  - AGENTS.md §6 Docs ("Changed contracts are reflected in authoritative docs") and §7 ("authoritative documentation is current").
  - `docs/README.md:64,68,103,116` lists these pages as the current documents for RTL modules, software registers, measured changes and the roadmap.
  - At the head the RTL does the opposite of what they say: gmstep reports 0 transitions and a MEDIA_RESET delta of 0; option-off reports settime MEDIA_RESET +0.
- **Impact:**
  - The register map is the software-facing contract for the Table 5.4 counters. Firmware, controller or test authors reading it will expect a MEDIA_RESET increment per PHC step. That is exactly the cause the #593 release gate now rejects.
  - The changelog advertises an unreleased behaviour that no longer ships.
  - The PR leaves the tree contradicting itself on the ruling it implements.
- **Required outcome:** every current (non-history) statement that a PHC step toggles `mr` or counts MEDIA_RESET either states the #602 ruling, or is removed and the ruling cited. The unreleased changelog records the partial reversal.
- **Verification:** `git grep -n -i -E "PHC step toggles|toggles \`?mr\`? once|counts that toggle in MEDIA_RESET" -- ':!docs/history'` returns no current-contract hits. A reviewer re-reads the four locations against ruling 5859297355.
- **Lens note:** this is not also filed under Conformance. Assignment 5859299480 item 3 names a document list, and every named document and module comment is correctly updated. This is completion-bar documentation debt, not an unmet acceptance criterion.

### F2 - MINOR - Docs, Tests - test-campaign documents and the restart-engine harness narrative describe the #387 inventory and scenario

- **Where:**
  - `docs/testing/TESTING.md:273`, the explicit-campaign row:
    - it says "twelve gmstep controls and two option-off controls"; the head has 14 + 2;
    - it says "The default sweep runs the three controls #387's acceptance names"; the head runs five, including #602's three;
    - its reviewer-trigger list omits `KL_media_clock_restart.sv`, although the new "source-change term is removed" control plants into that file through `MCR_SRC`.
  - `docs/testing/CI_WORKFLOWS.md:205`: "The three default gmstep controls remain in `run`." The head's `run` elaborates five. That sentence sits inside the hosted-shard budget argument, and the README's measured sweep cost (the removed "three controls took 133 s") was dropped without a new figure.
  - `tb/verilator/milan_dp/README.md:969,976,978`: the counts table still says "#387 adds the PHC-step `mr` checks, including settime toggle and MEDIA_RESET". Those checks now assert the opposite.
  - `tb/verilator/milan_dp/README.md:980`: the `obj_gmstep` row still says "48 / 0 … three controls in the sweep … all eleven". The head leg runs 64 checks with 5/16 controls. The section's own rule is that no row may project unexecuted checks and that rows not re-measured must be marked as such.
  - `tb/verilator/tkdiag/sim_main.cpp:648-664` and check names at `:711`, `:755`, `:759`, `:768`: they model the second request as "a PHC step" and state "milan_datapath ORs both onto restart_p_i". After this PR that is false. The engine test itself stays valid for two genuine `restart_p_i` requests.
- **Authority and evidence:**
  - AGENTS.md §6 Docs.
  - TESTING.md's explicit-campaign rule: that page keeps the list of campaigns and who must run them.
  - `receipts/executor_inventory_rerun_gmstep_mutants_all.log` (16 controls); the `CONTROLS` census (14 gmstep + 2 option-off, 5 default).
- **Impact:**
  - A later change to `KL_media_clock_restart.sv` is not routed by the documented rule to the campaign that now guards its source-change trigger.
  - The CI budget text understates the default sweep.
  - The harness narrative tells a future reviewer that a PHC step is a restart request.
- **Required outcome:**
  - The counts, the default-sweep size and the trigger list match the head inventory.
  - The counts rows are either re-measured or explicitly marked not re-measured.
  - The tkdiag narrative and check names describe genuine requests (for example, a CRF disruption plus a received toggle, or a source change) and do not claim the datapath ORs a PHC step.
- **Verification:** a reviewer compares `gmstep_mutants.CONTROLS` against TESTING.md and CI_WORKFLOWS.md, and `git grep -n "ORs both onto restart_p_i"` returns nothing.

### F3 - MINOR - Tests - the option-off settime `mr` check measures the absolute level, not a change caused by settime

- **Where:** `tb/verilator/milan_dp/sim_main.cpp:1080-1082`. The check `CLKV: the settime leaves mr unchanged (#602)` expects `mr == 0` on the post-holdover frame. `:991` does the same for the earlier adjtime.
- **Evidence (executed):**
  - The executor's own control "PHC adjtime is restored as an mr cause" breaks this settime check as well as its own. The settime did not toggle `mr`; the level was already 1 from the adjtime (`receipts/executor_inventory_rerun_gmstep_mutants_all.log`).
  - My P1 and P9 restore both causes. The settime toggles `mr` back to 0 and the check passes while the defect it names is present. Only the sibling delta check `settime adds no MEDIA_RESET` catches it (`receipts/probe_logs/P1_*_run_optoff.summary.txt`, `P9_*_run_optoff.summary.txt`).
- **Authority:** AGENTS.md §6 Tests: "Each new test can fail for the defect it claims to detect"; "Tests do not merely reproduce implementation assumptions." This check is new in this PR, and README `:701` names it as the settime control's detector.
- **Impact:** the check's name and the README table misattribute failures, and the check misses its own defect when causes combine. Coverage survives only through the MEDIA_RESET sibling.
- **Required outcome:** grade settime by the `mr` level just before the settime compared with just after it, or by the transmitted-toggle count across the settime, so it fails if and only if the settime changes `mr`.
- **Verification:**
  - The adjtime-only control breaks only the adjtime check.
  - A both-causes control breaks the settime `mr` check.
  - The settime-only control still breaks it.

### F4 - SUGGESTION - Tests, Robustness - no dynamic scenario for a PHC step coincident with a genuine restart

- **Where:** `tb/verilator/milan_dp/sim_gmstep.cpp` (`check_crf_restart` runs after the step window).
- **Evidence:** P4 (a step suppresses genuine requests) passes gmstep. The static gate-1b pins reject it (`receipts/static_pin_probe.txt`), and the RTL has no PHC input on the restart path, so the ruling's "neither adds nor suppresses" clause holds today by construction.
- **Suggestion:** toggle the received CRF `mr` inside the step's window and require exactly one outgoing toggle. That would make the clause dynamically graded as well as structurally pinned. The assignment did not require it, so this is optional.

## Reviewer-owned lens ledger (R366-1)

| Lens | Status | Examined artifacts (at the head) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling 5859297355 and assignment 5859299480 against `milan_datapath.sv:3124-3134`, `:6053-6055`, `:1951`; `KL_media_clock_restart.sv` (code identical); gmstep 64/0 and option-off 234/0 logs; named docs (answer 4); artifact identity 50/50; OOC reproduction | R366-1 | `49012143b335ea48d6a71c441a05d0c1796887ff` |
| RTL | CLEAN | `receipts/rtl_code_only_diff.txt` (one OR term; same `axis_clk` domain, no width or CDC change, no new state); pre-map gate census (`$_OR_ -1` only) and post-map counts at both AX shapes; `scripts/lint_rtl.py --check` PASS 90 <= 90 (`receipts/rtl_lint.log`); tkdiag 96/0 + 4/4 engine mutants | R366-1 | `49012143b335ea48d6a71c441a05d0c1796887ff` |
| Robustness | CLEAN (F4 is a SUGGESTION) | Coincident-cause probes P2/P4/P5 and static pins; INTERNAL (feature-off) leg with adjtime then settime; repeated-request merge (tkdiag T17/T18); CRF-selected versus INTERNAL gating (P2) | R366-1 | `49012143b335ea48d6a71c441a05d0c1796887ff` |
| Tests | UNCLEAN (F2, F3 open) | `sim_gmstep.cpp`, `sim_main.cpp`, `gmstep_mutants.py`, `Makefile`, `test_builder.py` diff; executor inventory re-run 16/16; reviewer probes P1-P10; static pin probe | R366-1 | `49012143b335ea48d6a71c441a05d0c1796887ff` |
| Docs | UNCLEAN (F1, F2 open) | `GM_LOSS_RECOVERY.md`, `TIME_SYNC.md`, `MILAN_COMPLIANCE_MATRIX.md`, `milan_dp/README.md`, module comments; tree-wide search for the superseded rule; `REGISTER_MAP.md:128-130`, `FPGA_DESIGN.md:178-179`, `MILAN_V12_ROADMAP.md:360-361`, `CHANGELOG.md:116-128`, `TESTING.md:273`, `CI_WORKFLOWS.md:205`; docs gates rc 0 (`receipts/docs_gates.txt`) | R366-1 | `49012143b335ea48d6a71c441a05d0c1796887ff` |

## Commands and receipts (all run in the foreground unless noted)

- Clean legs:
  - `make -s gmstep-build GMSTEP_MDIR=$PACKET/scratch/obj_gmstep_head`, then run the binary: rc 0, 64/0.
  - `make -s option-off-build OPTOFF_MDIR=…`, then run: rc 0, 234/0.
  - `make run TKDIAG_MDIR=<relative scratch>` (tkdiag): rc 0.
- Probes: `python3 scripts/r366_mutants.py $CLONE $PACKET/scratch/mut`. Driver rc 1 only because P9's option-off expectation named the settime check, which that combined mutant does not break (F3). Every other expectation was met.
- `python3 gmstep_mutants.py --all`: 18/18 PASS. Launched detached and polled in the foreground until it exited, because it runs longer than one foreground call allows.
- `python3 scripts/ooc_probe.py $CLONE scratch/ooc base head c1 c2`: all 8 rc 0. Detached and polled the same way; runs of about 14 minutes each.
- `python3 scripts/ooc_compare.py`, `scripts/static_pin_probe.py`, `scripts/artifact_identity.py`.
- `lint_rtl.py --check --jobs 2`, with the pinned 5.050 first on PATH.
- `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, `check_hygiene.py --check`, `gen_module_matrix.py --check`, `git diff --check`: all rc 0. `gen_toc.py --check` and `check_em_dash.py --base 6d5ebd73` returned rc 2 under the system interpreter (renderer missing) and rc 0 under an existing pinned Markdown environment.
- Clone integrity after all probes (`receipts/clone_integrity.txt`):
  - HEAD, tree and index equal the reviewed ids;
  - status is clean including untracked files;
  - 930/930 tracked blobs and modes match HEAD;
  - gitlinks `gptp-processor 5dce647a`, `protocol-processor 870ff88a` and `third_party/verilog-axis 48ff7a7e` are checked out at their pins with no dirty entries;
  - `external` was uninitialised before and after this round.
  - Ignored build products created by this round (the three ROM hex files and `__pycache__`) were removed.

## Real limits

- **Verilator path.** The assignment-named path `$VALIDATION_TMP/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host. I used another host wrapper that reports `Verilator 5.050 2026-07-01 rev v5.050` and matches the project pin (`rtl-fast.yml:18`); its binary hash is in `receipts/tools_identity.txt`.
- **Not run (not permitted):** the builder banks, full parent/PP/gPTP/Yosys banks, `make run` of the whole `milan_dp` suite, act, and the hosted jobs. Builder rc 0 and the full `milan_dp` run are the executor's published receipts, not re-executed here.
- **OOC scope.** OOC is out-of-context `synth_xilinx` area only. It measures neither placed area nor timing. The pre-map comparison is a per-class cell census, not a structural equivalence proof; the RTL diff is the functional proof.
- **Simulation scope.** gmstep is a compressed-time model: TDM clocks held, DRP answering zero, the talker opened by the escape bit. There is no lwSRP or physical-clock proof. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Hosted evidence at the head (read-only):** rtl-fast, elaborate, verilator-lint, docs-check, the Yosys shards and Verilator shards 0, 2 and 3 were successful. Verilator shards 1 and 4 were still in progress when read. "Physical gPTP (nightly and manual)" was SKIPPED by design (`receipts/hosted_check_runs_at_head.txt`).

## Pending manager duties

- Route F1-F3 back to the executor. A fix commit un-covers Docs and Tests, and they must be re-reviewed at the new head.
- Hosted exact-head acceptance, including the in-progress Verilator shards 1/5 and 4/5, and act-first local replication.
- The candidate-merge build on live dev `8bc97021f28fb7f729418d3a00851c84ea0b50fd` (source validation here was on base `6d5ebd73`), and the composition review of the overlap with PR #601 / #593 in `GM_LOSS_RECOVERY.md`. This round judged only PR #603's text.
- The second independent positive review, and the full completion bar. No merge without explicit maintainer authorization.

## Public review findings on PR #603, reconciled at this head

This section was written after the verdict, findings and ledger above. None of those were changed after reading any other report.

- **Before this round:** PR #603 had no review findings. It had no PR reviews, no inline comments, and only the two review-start notices (5859885900, 5859888993).
- **Origin of #602:** R362-1 F4 on PR #601, known here only from the #602 issue body. That report was not read. At this head its RTL half is resolved: a PHC-only step produces 0 `mr` transitions and 0 MEDIA_RESET. Its documentation half is **retained** as F1.
- **Concurrent external round R367-1** ([R367] NEGATIVE at this head, posted after this round began, read only after the above was written):
  - **R367 F1 (stale current docs):** the same locations as my F1, so the finding is **retained**. R367 rates it MINOR; this round keeps it **MAJOR**. The register map is the software-facing counter contract, and it now contradicts both the shipped behaviour and the #593 release gate. The manager may reconcile the severity. Both rounds leave Docs unclean.
  - **R367 F2 (TESTING.md row, tkdiag narrative):** the same as the TESTING.md and tkdiag parts of my F2, so it is **retained**. My F2 also covers `CI_WORKFLOWS.md:205` and the `milan_dp/README.md` count rows.
  - **R367 F3 (coincident step not simulated):** the same as my F4, at the same severity (SUGGESTION).
  - **R367 F4 (the rename control shows determinism, not insensitivity):** agreed and answered above. The one-term control c1 moves mapped LUTs by -262 / +673, and the pre-map census isolates the head delta to one `$_OR_`. R367's cone bound (-4 / -1 LUT locally) is consistent with this.
  - **Not raised by R367:** my F3 (the settime `mr` check measures the absolute level). It is supported by executed controls in both inventories, so it is **retained** as MINOR.

R366-1 FINISHED
