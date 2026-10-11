[R558] POSITIVE - exact head aa980479aafd1d72c72015707fa6618b5aa47cb1

# R558-10 - issue #696 / PR #706 - delta review at `aa980479`

- **Head:** `aa980479aafd1d72c72015707fa6618b5aa47cb1`, tree `a7adf20bdededdf76fd4b9fdc9f6b8c820be6082`.
- **Role:** cleared-context internal reviewer. This is a delta review. The source head `32582421` has two POSITIVE reviews (R558-8, R559-7). Composition review R558-9 found R558-9-F1 (MINOR, Docs) and R558-9-R1 (RESIDUE).
- **Delta since `32582421`:** two commits.
  - `a7291311` merges dev `09c7231e`.
  - `aa980479` changes five lines of `docs/design/MARK_II_AREA_PLAN.md`.
- **Verdict:** POSITIVE.
  - The merge is the automatic merge and carries every PR patch byte-for-byte.
  - R558-9-F1 and R558-9-R1 are resolved.
  - Every lens is clean at this head.
  - One new RESIDUE is in the PR body (R558-10-R1). Earlier residues are retained.

## 1. Scope reconstructed from public state

- **Read in order:**
  - AGENTS.md and CONTRIBUTING.md;
  - docs/README.md;
  - the #696 issue body and every manager assignment and ruling: 6076750392, 6076940309, 6079087547, 6079463350, 6080332335, 6089712293, 6093171536, 6097504752, 6102832618;
  - the round's start comment 6113976787 and the PR body;
  - `syn/ooc/pp_resource_baseline.json` at `e8454e27`, `09c7231e`, `32582421` and the head, with `syn/ooc/pp_resource_gate.py`;
  - `docs/design/AREA_BUDGET.md` and `docs/design/MARK_II_AREA_PLAN.md`;
  - then `git diff 09c7231e..aa980479` and the history.
- **Prior review reports:** I read them only after my own pass and draft verdict (section 5).
- **Frozen acceptance:**
  1. Each item is conformed with a suite check and a planted defect, or justified by clause.
  2. M4 is fixed in RTL first, with a datapath two-MAC check.
  3. OOC area and one shipping route stay within budget, re-recorded through the recipe.
  4. Bench interop, which ruling 6076750392 item 6 assigns to a post-merge bench lane.
- **Delta questions from the assignment:**
  - Is the merge only the automatic merge?
  - Does the plan name the record each lane was compared against, and say that #696's 50,013-LUT record replaced it?
  - Does any other sentence imply that the current `route-1x1` record is 50,267?
  - Does the merged `milan_datapath.sv` keep this PR's MAAP hunks and M6's hunks?
  - Do the docs gates and `pp_resource_gate.py check-baseline` pass?

## 2. Delta facts (`receipts/composition.txt`)

- **The merge `a7291311` is the automatic merge, with nothing added.**
  - Its parents are the source head `32582421` and dev `09c7231e`.
  - A fresh `git merge-tree --write-tree 32582421 09c7231e` exits 0 with tree `0705eb4a`, which is the merge commit's tree.
  - The merge base is `e8454e27`.
- **Every PR patch is carried byte-for-byte.**
  - The head differs from dev in exactly the PR's 17 files.
  - Each file's `git patch-id --stable` over `e8454e27..32582421` equals its patch-id over `09c7231e..a7291311`: 17 of 17 are the same.
- **Files changed on both sides since `e8454e27`** were `AREA_BUDGET.md`, `MARK_II_AREA_PLAN.md`, `docs/findings/README.md`, `milan_datapath.sv` and `sw/firmware/ctrl/maap/README.md`.
  - Dev's README change is F-INT's `DA_GATE` text at `:108-150`. The PR's is the differential text at `:198-204`. They are disjoint and consistent: F-INT changes `maap_mbx.c` and `.h`, not `maap.c` or `KL_maap.sv`.
  - The findings index merges dev's #629 row with the PR's #234 row.
- **`milan_datapath.sv` keeps both sides.**
  - From dev to head, the file differs only in the PR's two hunks: the `:267` comment and `:7184-7185`, `.port_operational_i (eff_link_w)` and `.realtime_ns_i (ptp_now_w[31:0])`.
  - So every dev hunk survives intact, including M6's (#719).
  - `eff_link_w` (`:2165`, assigned `:3000`) and `ptp_now_w` (`:2124`) are declared once and are unchanged by dev.
- **`aa980479` changes only `MARK_II_AREA_PLAN.md` lines 695, 696, 706, 947 and 968**, to the exact R558-9-F1 and R558-9-R1 wording.

## 3. Executed evidence at this head (this round)

- **Toolchain:**
  - Verilator 5.050 through the scoped wrapper. The wrapper's sha256 is `905795b9…`. The `verilator_bin` it runs has sha256 `44898b22…` (`receipts/verilator_identity.txt`).
  - Markdown gates ran under the existing pinned renderer environment (cmarkgfm 2025.10.22, html5lib 1.1), used read-only.
  - Host python3 3.14.
  - Builds ran in a disposable git clone of the head with the three needed submodules at their gitlinks (`protocol-processor 2ad2f845`, `gptp-processor 5dce647a`, `verilog-axis 48ff7a7e`).
- **Record against the lane routes** (`record_vs_lane_routes.py`; `receipts/record_vs_lane_routes.log`, rc 0):
  - It applies the gate's own `verdict_for()` and the BRAM-tile ceiling to every figure the plan quotes for M2 (`:691`) and M6 (`:943`), against both records.
  - Against #645/#647's record, the one at `e8454e27`: both base-route rows (`:690`, `:942`) equal it in every quoted gated figure, and M2 and M6 PASS.
  - Against #696's record at the head: M2 and M6 PASS. M2 is +126 LUT, +48 FF and +18 slices, with WNS up. M6 is +38 slices, with WNS down by 0.092 ns to +0.141. Both are within every tolerance, floor and ceiling.
  - DSP is not quoted in the tables. Both records hold DSP 14 and DSP tolerance is 0, so "passes against #645/#647's record" already implies DSP 14 against #696's.
  - So the new `:696` and `:947` claims ("it also passes against #696's record") hold.
- **The 50,267 sweep.** `git grep 50,267|50267` over the tree finds no non-Markdown hit. Every Markdown hit is scoped to a baseline, a predecessor or a historical section:
  - `AREA_BUDGET.md:136`, `:170` (Round 1d ledger at `5603c353`) and `:379`;
  - `MARK_II_AREA_PLAN.md:27` ("Recorded start"), `:76` (dated baseline section), `:317`, `:655`, `:690`, `:695`, `:942`, `:977`, `:1035` and `:1086`;
  - `234_PP_SHADOW_AREA_BASELINE.md:198` (the #645/#647 section).
  - One phrase, `MARK_II_AREA_PLAN.md:1086` "current three-endpoint record … Already in 50,267", pairs the word "current" with the old record. That is the already-retained RESIDUE R558-2-R1 (section 5), wording only. The ledger keeps the baseline figures by `:110`.
  - Search for sibling anchor sentences ("comparison record", "comparison anchor", "Against that record", "unchanged under D7"):
    - `AREA_BUDGET.md:379` and `MARK_II_AREA_PLAN.md:656` name #696's record;
    - `MARK_II_AREA_PLAN.md:696`, `:706` and `:968` are the corrected lines;
    - no other occurrence.
- **MAAP target** (`make -j8 run` then `mutants.py`, pinned Verilator; `receipts/maap_target.log`, rc 0):
  - unit `KL_maap: 186 checks, 0 failures`;
  - campaign `checks: 65 failures: 0`: both clean controls pass, unit and the real `milan_datapath` (`m4_datapath_clean`), and 63 of 63 planted defects fail their named checks.
  - The real-datapath arm elaborates the merged `milan_datapath.sv`. Its source list comes from `tb/verilator/milan_dp print-srcs`.
- **Merged-datapath wiring probes** (`datapath_wiring_probes.py`; `receipts/datapath_wiring_probes.log`, rc 0):
  - **Why:** the datapath flags waive `PINMISSING`, so a merge that dropped or mis-tied a MAAP connection could compile silently.
  - **Method:** each probe edits one exactly-once anchor in a disposable clone of the merged datapath, builds `integration-build` and runs `maap_integration`.
  - clean control: 5 checks, 0 failures;
  - `.port_operational_i` tied to `1'b1`: CAUGHT at "M5 datapath: link return starts four fresh PROBEs";
  - `.realtime_ns_i` tied to `32'd0`: CAUGHT at both M3 datapath checks;
  - the MAAP instance's `station_mac_i[31:0]` tied to zero: CAUGHT at both M4 datapath checks.
  - The datapath file was restored after each probe and verified clean.
- **`milan_dp` legs that read MAAP and counters** (`receipts/milan_dp_dp.log`, `receipts/milan_dp_dp2.log`, each rc 0):
  - `option-off`, the `sim_main` 1x1 legacy leg: 236 checks, 0 failures. It covers the admission gate's MAAP term and the STREAM_INPUT counters at 0x6B8.
  - `ax1x1`, the shipping AX7101 shape: 233 checks, 0 failures. Its build recipe uses `sim_main.cpp`. The receipt's leg label "sim_nxn shipping" is my own echo text and is wrong about the harness.
  - The `obj_nxn` 4x4 leg (`sim_nxn.cpp`): 1,967 checks, 0 failures. It includes "MAAP unclaimed: t1/t0 held" and "MAAP off: both restored", and the GET_COUNTERS reads of M6's counter table.
  - The `obj_prune` leg (MAAP_P = 0): 33 checks, 0 failures. MAAP_STAT0/1 read 0 with the engine pruned.
  - These two legs were built with the `run` target's own recipe lines through a scratch-only wrapper makefile.
- **Firmware MAAP differential** (`maap_differential.py`; `receipts/maap_differential.log`, rc 0): 12 of 12 tests pass. Its inputs (`maap.c`, `KL_maap.sv`, the test) are unchanged since `32582421`, and the merge touches none of them.
- **Lint** (`lint_rtl.py --check`, pinned Verilator; `receipts/lint_rtl_check.log`): rc 0, `90 violation(s) <= ratchet 90`.
- **Docs and static gates**, all rc 0 at the head:
  - In the disposable clone (`receipts/docs_gates.log`, `receipts/docs_markdown_gates.log`, `receipts/check_doc_paths.log`):
    - `docs_check.py`: 0 findings over 203 md files;
    - `check_em_dash.py --base 09c7231e`: 0 findings over 344 added lines in 7 pages;
    - `gen_toc.py --check` and `--verify-anchors`;
    - `check_doc_style.py`, `check_gptp_docs.py`, `DOC_MAP.gen.py --check`, `timesync_chain.gen.py --check`, `check_solution_docs.py`, `submodule_boundaries.gen.py --check`, `check_submodule_docs.py`, `check_diagram_pngs.py`, `check_feature_status.py`, `check_archive.py`, `check_doc_paths.py` (963 cited paths);
    - **`pp_resource_gate.py check-baseline`: `baseline PASS: 3 endpoints`**.
  - In the review clone, read-only (`receipts/code_quality_gates.log`): `check_hygiene.py --check`, `check_py_idiom.py`, `check_cpp_idiom.py`, `measure_test_evidence.py --check`, `check_todo_ownership.py`, `check_sv_idiom.py`, `measure_fail_fast.py --check`, `measure_naming.py --check` and `check_port_contracts.py`.
  - The rc 2 lines in `receipts/docs_gates.log` are refusals from the environment, not gate failures:
    - the three Markdown gates under the bare interpreter, which lacks the renderer;
    - five code-quality gates in the disposable clone, which has unregistered submodules.
    - Each of those gates was rerun as listed above and exits 0.
- **Hosted evidence** (`receipts/hosted_check_runs.txt`, snapshot 2026-10-11T21:44Z at this head):
  - success: `changes`, `full-ci-gate`, `bdd-conformance`, `wire-accountability`, `docs-check-no-git`, `verilator-lint`, Yosys shards 0-3 and Verilator shard 3/5;
  - in progress: `docs-check`, `elaborate`, `firmware-unit`, `publication-census`, `yosys-elaboration` and Verilator shards 0, 1, 2 and 4;
  - skipped: the nightly/manual physical gPTP context, which is not hardware proof.
  - The manager owns hosted and act acceptance. I claim no hosted verdict.
- **Clone after all runs** (`receipts/tree_state_final.txt`, rc 0):
  - HEAD `aa980479` and tree `a7adf20b`;
  - index equals HEAD, and the worktree equals the index in bytes and modes;
  - no untracked or ignored path;
  - gitlinks: protocol-processor `2ad2f845`, gptp-processor `5dce647a` and verilog-axis `48ff7a7e` match; lwSRP `08ee86e8` and `external` `efeb541a` are recorded but not checked out, as at the start.
  - One `syn/ooc/__pycache__` my comparison script wrote during the round was removed before this check.

## 4. Findings of this round

### R558-10-R1 - RESIDUE - Docs - PR #706 body, "Status" and "How to get into the same state" - the body still names `32582421` as the review-ready head

- **Evidence:** "Status" reads "GREEN locally, review ready at `32582421…`". The checkout block expects `git rev-parse HEAD   # 32582421…`. The PR head is `aa980479`, and the body's own "Composition repair" section describes `a7291311` and `aa980479`.
- **Why RESIDUE:** this is PR-body wording only. Every figure, check, gate and verdict stated there is unchanged, and the Composition repair section gives the head's gate results.
- **Exact fix:**
  - "Status": "GREEN locally, review ready at `aa980479aafd1d72c72015707fa6618b5aa47cb1` (source `32582421` merged with dev `09c7231e` in `a7291311`) - `696-maap-annexb` -> `dev`."
  - Checkout block: `git rev-parse HEAD   # aa980479aafd1d72c72015707fa6618b5aa47cb1`.
  - Carry R559-7-R1's exact fix with the head updated to `aa980479`.
- **Verification:** reread the body.

No BLOCKER, MAJOR or MINOR.

## 5. Prior public findings on this PR, at this head (read after my own pass and draft verdict)

| Finding | State at `aa980479` | Evidence |
|---|---|---|
| R558-9-F1 (MINOR, Docs; `MARK_II_AREA_PLAN.md:695-696`, `:947`) | **Resolved** | `aa980479` applies the exact required text. `receipts/record_vs_lane_routes.log`: the base rows equal #645/#647's record, the record at `e8454e27`; M2 and M6 pass against both records. No other sentence names 50,267 as the current record (section 3, the 50,267 sweep) |
| R558-9-R1 (RESIDUE, Docs; `:706`, `:968`) | **Resolved** | Both lines now read "M2/M6 does not re-record the gate under D7." |
| R558-7-F1, R559-6-F1, R559-6-F2 (MINOR) | **Still resolved** | `sim_main.cpp`, `mutants.py` and `MAAP_FABRIC.md` carry the same patch-ids. The campaign rejects q3, q9, q1 and `m2_echo_overlap_start` by name (`receipts/maap_target.log`) |
| R558-6-F1 (MINOR; first draw) | **Still resolved** | `KL_maap.sv` carries the same patch-id. Both p7 plants, unit and datapath, are rejected |
| R558-5-F1 (MINOR, Docs) | **Still resolved** | `AREA_BUDGET.md:379` and `MARK_II_AREA_PLAN.md:655-656` name #696's 50,013 record |
| R558-3-F1 = R559-3-F1 (BLOCKER, `integration.mk`) | **Still resolved** | `integration.mk` carries the same patch-id. The integration build derives the merged source list and passes 5/0 |
| R558-1-F1, R559-1-F1/F2/F3 (MINOR) | **Still resolved** | The plan inventory and MAAP area text are unchanged by the delta. The M5 loss check passes in the campaign |
| R558-2-R1 / R559-2-R1 (RESIDUE) | **Retained** | Still applies at `MARK_II_AREA_PLAN.md:66-67`, `:317` and `:1086`. I found `:1086` independently before reading these. Wording only |
| R558-5-R1 (RESIDUE) | **Retained** | `AREA_BUDGET.md:370`, `:387` and `MARK_II_AREA_PLAN.md:668` are unchanged |
| R559-7-R1 (RESIDUE, PR body) | **Retained**, with its head updated | The body still says "Hosted checks and the local workflow replica need the pushed head." See R558-10-R1 |
| R558-8-S1, R559-7-S1, R558-7-S2, R559-6-S2, R559-6-S3, R558-6-S1/S2, R559-5-S1, R558-3-S1/S2, R559-3-S1, R558-4-S1/S2, R559-4-S1/S2, R559-1-S1..S4 (SUGGESTION) | **Retained, optional, no lens effect** | The delta changes none of their sources |

R558-9's composition candidate used dev `cfadd767`. The actual merge uses dev `09c7231e`, which adds #704 (F-INT): mailbox RTL, firmware split and CI files, and no `milan_datapath.sv`, `KL_maap.sv` or MAAP-suite change. This round's runs are on the actual merge.

## 6. Lens results

```text
[R558] PASS Conformance - hdl/milan/milan_datapath.sv:7181-7190 (KL_maap instance at the head), tb/verilator/maap, receipts/maap_target.log, receipts/maap_differential.log - against #696 acceptance 1-3 and rulings 6076940309/6079087547/6102832618: KL_maap.sv and the MAAP suite carry the source head's patch-ids; unit 186/0, real merged datapath 5/0, campaign 65/0, differential 12/12; M3/M4/M5 behaviour reaches the engine through the merged datapath (wiring probes); acceptance 3's re-record stands, check-baseline PASS; acceptance 4 is the bench lane's
[R558] PASS RTL - hdl/milan/milan_datapath.sv:267,2124,2165,3000,7184-7185; receipts/composition.txt; receipts/lint_rtl_check.log - fresh merge-tree equals a7291311's tree; dev-to-head diff of the datapath is only the PR's two hunks, so M6/F-INT/M2 hunks survive; both new connections reach once-declared nets unchanged by dev; lint 90 <= 90; legs option-off 236/0, ax1x1 233/0, nxn 4x4 1,967/0, prune (MAAP_P=0) 33/0 elaborate and pass
[R558] PASS Robustness - receipts/datapath_wiring_probes.log, receipts/milan_dp_dp2.log, receipts/maap_target.log - with PINMISSING waived, link tied high, clock tied zero and MAC low word tied zero are each caught by name on the merged datapath; pruned engine reads structural zeros; MAAP-unclaimed/off talker holds and GET_COUNTERS reads pass beside the live engine; campaign rows for truncation (M8), link loss/return (M5), pending response (M6) and supplied-seed bounds (M7) all reject their plants
[R558] PASS Tests - tb/verilator/maap/{Makefile,integration.mk,mutants.py,sim_integration.cpp,sim_main.cpp} at the head, receipts/maap_target.log, receipts/datapath_wiring_probes.log - no test changed by the delta (patch-ids identical); the integration arm derives the merged source list; 65-row campaign with both clean controls; my three wiring plants show the datapath checks can fail for merge-shaped defects; SUGGESTIONs retained as optional
[R558] PASS Docs - docs/design/MARK_II_AREA_PLAN.md:655-656,690-706,942-968 (and the 50,267 sweep in section 3), docs/design/AREA_BUDGET.md:104-152,370-387, docs/findings/README.md, syn/ooc/pp_resource_baseline.json; receipts/record_vs_lane_routes.log, receipts/docs_gates.log, receipts/docs_markdown_gates.log, receipts/check_doc_paths.log - the five changed lines name the record each lane was compared against and that #696's 50,013 record replaced it, verified against both records with the gate's own verdict; no other sentence names 50,267 as the current record; every docs gate and check-baseline exits 0; RESIDUE R558-10-R1 new, R558-2-R1/R559-2-R1, R558-5-R1, R559-7-R1 retained (wording only, no lens effect)
```

## 7. Reviewer-owned completion ledger

The delta touches every lens's scope. The merge brings dev's RTL into the datapath that the MAAP integration arm and the `milan_dp` legs elaborate, and `aa980479` changes Docs. So each lens was applied again at this head.

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | merged KL_maap instance; MAAP unit 186/0, datapath 5/0, campaign 65/0; differential 12/12; record check-baseline | R558-10 | `aa980479aafd1d72c72015707fa6618b5aa47cb1` |
| RTL | CLEAN | merge-tree reproduction; datapath dev-to-head diff; net declarations; lint 90 <= 90; four `milan_dp` elaborations | R558-10 | `aa980479aafd1d72c72015707fa6618b5aa47cb1` |
| Robustness | CLEAN | three wiring probes plus control; prune leg; MAAP-off/unclaimed holds; GET_COUNTERS; campaign robustness rows | R558-10 | `aa980479aafd1d72c72015707fa6618b5aa47cb1` |
| Tests | CLEAN (SUGGESTIONs retained) | MAAP harnesses and campaign (patch-ids identical); integration arm on the merged sources; probe sensitivity | R558-10 | `aa980479aafd1d72c72015707fa6618b5aa47cb1` |
| Docs | CLEAN (RESIDUE R558-10-R1; R558-2-R1 / R559-2-R1, R558-5-R1, R559-7-R1 retained) | `MARK_II_AREA_PLAN.md` changed lines and the 50,267 sweep; `AREA_BUDGET.md`; findings index; record file; 16 documentation and record gates plus 9 code-quality gates | R558-10 | `aa980479aafd1d72c72015707fa6618b5aa47cb1` |

## 8. Real limits

- **Not run here:**
  - no Vivado, Yosys or xvlog run;
  - no full parent sweep, processor/gPTP/Yosys/builder banks, firmware bank, field campaigns or behave;
  - no `act`/`act_ci`;
  - not the remaining `milan_dp` legs (gptp, gmstep, notify, crflic, dynmap, nxn8, nxn4c, nolpf, divergent, aclk) or the M6 lockstep suites. The delta changes none of their inputs beyond what dev's own reviewed PRs carried.
- **Resource record:** checked by `check-baseline` and by comparing quoted figures. The merged image (#696 plus M2, M6 and F-INT) has never been measured. The record describes `bee1b0d7`.
- **No manager source bank was run or inferred at this head.** Source-head execution evidence is the author's published gate receipts plus this round's focused runs.
- **Hosted evidence:** in progress at the snapshot. No hosted verdict is claimed.
- **Hardware:** physical calibration NOT RUN. Bench acceptance 4 is not exercised, and field skips are not hardware proof.
- **Toolchain:** host python3 3.14 and the local make, not the hosted 3.12 image.

## 9. Pending manager duties

- Build and gate the current-dev merge candidate at the merge turn, with builder and native banks. The source base and live dev are both `09c7231e`. Link the receipts on the PR.
- **Merge-bank resource comparison** under `AREA_BUDGET.md`'s bank rule. Dev's delta since the record's measured revision `e8454e27` touches RTL: M2, M6, and F-INT's `KL_mbx.sv`. Decide re-record versus D7 retention, with the ledger separating predecessor movement.
- Accept the hosted contexts (several still running at the snapshot) and the act replica at this head.
- Carry RESIDUE R558-10-R1, R558-2-R1 / R559-2-R1, R558-5-R1 and R559-7-R1 on the residue checklist.
- Obtain the external verdict for this head (R559-8 is in flight). Route acceptance 4 to the post-merge bench lane, then run post-merge containment.

## 10. Packet

Paths are relative to this packet, listed with SHA-256 in `MANIFEST.sha256`. Host paths in receipts are written as `$PACKET`, `$SCRATCH`, `$CLONE`, `$PINNED_VERILATOR`, `$MD_VENV` and `$HOME`.

- **Scripts:**
  - `composition_check.sh <repo> <head> <merge> <source-head> <dev> <lane-base>`;
  - `record_vs_lane_routes.py <repo> <old-record-rev> <head>`;
  - `datapath_wiring_probes.py <checkout> <verilator> <jobs> [probe ...]`;
  - `run_docs_gates.sh <checkout> <base>`;
  - `verify_tree_state.sh <clone> <head> <tree>`.
- **Receipts:** `receipts/composition.txt`, `record_vs_lane_routes.log`, `maap_target.{log,rc}`, `datapath_wiring_probes.log`, `milan_dp_dp.{log,rc}`, `milan_dp_dp2.{log,rc}`, `maap_differential.log`, `lint_rtl_check.log`, `docs_gates.log`, `docs_markdown_gates.log`, `check_doc_paths.log`, `code_quality_gates.log`, `hosted_check_runs.txt`, `verilator_identity.txt` and `tree_state_final.txt`.

R558-10 FINISHED
