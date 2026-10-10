[R558] POSITIVE - exact head f909d6c460344527f102f24b8e7a77f09959e755

Round R558-2. Internal cleared-context review of issue #696 / PR #706.
Head `f909d6c460344527f102f24b8e7a77f09959e755`, tree `9d6acafcd88efe041dfed3f008f0d70941c16e5e`.
Delta reviewed: `030eb98a..f909d6c4`, three commits (`eb2cac84`, `f03e254e`, `f909d6c4`), answering round-2 assignment 6093171536.
Source base `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`; merged dev `8b61b70902f3ebf118e56967277e2686731081bd`; live dev `aef7ac66605c4404900ce04cbaaeff88e41bb880` (not built here).

All five lenses were applied at this head and all five are CLEAN.
There is no BLOCKER, MAJOR or MINOR finding.
One RESIDUE (wording only) is carried to the manager: R558-2-R1.
Every round-1 finding (R558-1-F1, R559-1-F1, F2, F3) is resolved at this head, and the round-1 residue R1-R3 and R558-1-S1 are applied.

## 1. Reconstruction

Read in this order:

1. AGENTS.md; CONTRIBUTING.md sections 3 and 6.
2. docs/README.md.
3. Issue #696 body (acceptance 1-4), assignment 6076750392, rulings 6076940309, 6079087547, 6079463350, 6080332335, 6089712293, the author STOP and REVIEW READY comments, and round-2 assignment 6093171536.
4. Authorities: `docs/design/MAAP_FABRIC.md`, `hdl/ieee1722/maap/KL_maap.sv`, `syn/ooc/pp_resource_baseline.json`, `docs/design/MARK_II_AREA_PLAN.md`.
5. `git diff 030eb98a..f909d6c4` (5 files) and the commit history; `git diff 6aa25dec..f909d6c4` for context.
6. Public evidence: the author REVIEW READY 6093452983; R559-1's plant `review-evidence/696-r1/reviews/R559-1/receipts/plants/r_restart_on_link_loss.patch` on branch `696-review-evidence` at `b96793c3` (blob `cac1017e`, sha256 `f9e8de81...`). Only the patch was read.

The round-1 reports R558-1 (6093137183) and R559-1 (6093167069) were read only after my own pass over the diff.

## 2. Round-1 findings: resolution at this head

| Finding | Required outcome | State at `f909d6c4` | Evidence |
|---|---|---|---|
| R559-1-F1 (Tests) | An M5 check holds the port down longer than a walk; the drop causes no restart or PROBE; the fresh walk starts after the rise; the falling-edge plant fails that named check in the default campaign | **Resolved** | See note 1 below the table. |
| R558-1-F1 (Docs) | `MAAP_FABRIC.md` states the merge-result figure and attributes 441/340 | **Resolved** | See note 2 below the table. |
| R559-1-F2 (Docs) | Plan "current record" figures and the gate row follow the re-record | **Resolved** | See note 3 below the table. The remaining baseline wording is R558-2-R1. |
| R559-1-F3 (Docs, Tests) | Both texts name `02:00:00:00:00:00` with clock 0 | **Resolved** | See note 4 below the table. |
| R559-1 residue R1-R3 | Wording | Applied | `MAAP_FABRIC.md:143`, `:36` and `:137-138`; `docs/findings/README.md:25` |
| R558-1-S1 (suggestion) | Optional | Applied | `MARK_II_AREA_PLAN.md:56` |
| R559-1-S1..S4 (suggestions) | Optional | Not applied; the reasons are in REVIEW READY | No lens effect |

Notes on the four resolved findings:

1. **R559-1-F1.** The new check is at `sim_main.cpp:68-71,763-803,974` and the campaign row at `mutants.py:70-72`.
   - R559-1's patch, applied verbatim, gives 172 checks and 1 failure: only `M5 B.3.5.9 link loss is no event; return reprobes`. The harness exits 1.
   - The same plant against the `030eb98a` harness gives 171 checks and 0 failures. So the new check is what closes the gap.
   - The default campaign row `m5_restart_on_link_loss` exits 1 at that check.
2. **R558-1-F1.** `MAAP_FABRIC.md:143-148` now gives:
   - 441/340 at `39571196`;
   - 445/340 at merge result `0df48637`, which is +6/+60 against `6aa25dec`;
   - dev `8b61b709` at 443/280, so the lane share is +2/+60.

   I checked the arithmetic. The figures equal the round-1 receipts that R558-1 quoted.
3. **R559-1-F2.** `MARK_II_AREA_PLAN.md:110-141` has 22 rows and 66 figures, with 0 differences against the `pp_resource_baseline.json` scopes at this head. At `030eb98a` the route column differed in 18 rows. For the gate row at `:56`:
   - 0.114 - 0.030 = 0.084, which is less than 0.25, so the floor binds first;
   - the floor (0.03) and the tolerance (0.25) were read from the record.
4. **R559-1-F3.** The fixture is named correctly at `MAAP_FABRIC.md:227-229` and `sim_main.cpp:9,58-59,645-646`.
   - With `realtime_ns_i=0` (`sim_main.cpp:228`) the low 32 bits sum to 0, so the fallback is exercised.
   - Both `zero_seed_freezes_*` defects are still caught.

## 3. Findings

### R558-2-R1 - RESIDUE - Docs - `docs/design/MARK_II_AREA_PLAN.md:66-67`, `:317`, `:970` - baseline sentences still point at the live record file as if it held the #645/#647 record

- **Evidence:**
  - `:66-67` says "Source: `pp_resource_baseline.json`, all three `record` objects. Each `measured` note identifies `a5ca6e51...`". The link resolves to the file at this head. There, every `measured` note now identifies `0df48637`, and the route figures are #696's.
  - `:317` says "The current ledger starts from the committed 50,267 record".
  - `:970` names "current three-endpoint record".
- **Why this is residue and not a finding:**
  - Every figure in those sections is correct for the baseline they describe.
  - `:110-111` says explicitly that only the route figures changed, and that the levers and ledger keep the baseline's figures.
  - Correcting the sentences changes no figure, verdict, test or clause claim.
- **Exact fix:**
  - `:66`: "Source: the three `record` objects of [`pp_resource_baseline.json`](../../syn/ooc/pp_resource_baseline.json) as stored at dev `5603c353`; #696's record has since replaced them (see [Current processor inventory](#current-processor-inventory))."
  - `:317`: "The [current ledger](#ledger) starts from the 50,267 route figure of the #645/#647 record."
  - `:970`: "Adopted processor pin and the #645/#647 three-endpoint record".
- **Verification:** reread the three lines, then run `docs_check.py`, `gen_toc.py --check` and `check_em_dash.py`.

## 4. Lens results

### Conformance - CLEAN

[R558] PASS Conformance - `hdl/ieee1722/maap/KL_maap.sv:155-157,431-441` (unchanged since `030eb98a`), `docs/design/MAAP_FABRIC.md:104-111`, `tb/verilator/maap/sim_main.cpp:763-803` - the M5 contract against B.3.5.9 and Table B.7 as the issue and assignment 6093171536 cite them:

- **Rising edge only.** The restart fires on `port_operational_i && !port_operational_r`. It re-draws the offset, sets four PROBEs with the first at once, and does not count a conflict.
- **Falling level.** A falling level changes no state, so the walk in progress continues. This matches the documented contract ("no event for leaving the operational state") and the harness expectation.
- **Round-2 assignment.** Items 1-5 are met:
  - the new check;
  - the plant in the default campaign;
  - the merge-result figure with its attribution;
  - the plan's current inventory and gate row;
  - the fixture MAC and the applied residue.
- **Acceptance.** Acceptance 1-3 stand as evidenced in round 1; this delta changes no RTL. Acceptance 4 belongs to the post-merge bench lane.

### RTL - CLEAN

[R558] PASS RTL - `receipts/design_inputs_unchanged.txt` - `git diff 0df48637..f909d6c4` touches no `hdl/`, `sw/`, recipe Tcl or gitlink path:

- The `hdl` tree is `d0bcd6ad` at both commits, and the `sw` tree is `710738e1` at both.
- `syn` differs only by `pp_resource_baseline.json`.
- The gitlinks are unchanged: `protocol-processor` at `2ad2f845`, `gptp-processor` at `5dce647a`.

So the recorded measurement inputs (merge result `0df48637`) equal this head's design inputs, and the record stands.

- `receipts/record_delta_8b61b709_head.txt`: for all three endpoints, tolerance, floor, ceiling and identity are unchanged. Only the route figures and scopes changed; the standalone figures did not.
- The record itself is unchanged across `030eb98a..f909d6c4`.
- Earlier rounds stand for `KL_maap.sv` and its datapath integration, since neither file changed.

### Robustness - CLEAN

[R558] PASS Robustness - `sim_main.cpp:763-803` with reviewer probes `receipts/probes.log` - the link-loss path is now graded: invalid ordering and a long outage, in both PROBE and ANNOUNCE.

Four alternative link-loss behaviours each fail the new named check, with harness rc 1:

- a restart on both edges;
- timers frozen while the link is down;
- a loss that releases to IDLE;
- TX gated while the link is down.

These existing checks still pass (172/0):

- the short-outage return;
- the steady-level check;
- the cancellation of a pending DEFEND on link return.

### Tests - CLEAN

[R558] PASS Tests - `tb/verilator/maap/{sim_main.cpp,mutants.py}` at `f909d6c4`, with the pinned Verilator `5.050 rev v5.050` (identity checked):

| Gate | Result | Receipt |
|---|---|---|
| Default target `make -C tb/verilator/maap` (harness, then campaign) | rc 0. Harness: 172 checks, 0 failures. Campaign: 52 rows, 2 clean controls, 50 defects at their named checks, 0 escapes. Includes `m5_restart_on_link_loss`, the zero-seed defects and the M4/M5/M3 datapath rows. | `receipts/default_campaign.log`, `campaign_rows.txt` |
| R559-1 `r_restart_on_link_loss.patch`, verbatim | 172 checks, 1 failure (only the new M5 check); harness rc 1, make rc 2 | `receipts/r559_plant_direct.log`, `r559_plant.log`, `r559_plant_applied.diff` |
| Same plant, `030eb98a` harness | 171 checks, 0 failures, rc 0 | `receipts/r559_plant_vs_030eb98a_harness.log` |
| Line coverage | `KL_maap.sv` 215/215, gate PASS | `receipts/coverage.log` |
| Reviewer probes | 4/4 fail the named check | `receipts/probes.log` |

The new check is not a restatement of the RTL. Its outage length comes from the B.3.4.2 bound: 4 x 600 ms = 2.4 s, while a walk takes less than 3 x 600 ms plus the at-once frames. It requires all of the following:

- the frames sent during the outage keep the range that was in use at the loss;
- none of them starts within the at-once bound of the loss;
- the walk count is 3+1 from PROBE and 0 from ANNOUNCE;
- validity is revoked one cycle after the rise;
- four fresh PROBEs follow, the first at once, then the ANNOUNCE;
- the conflict count is unchanged.

### Docs - CLEAN (R558-2-R1 is residue)

[R558] PASS Docs - `docs/design/MAAP_FABRIC.md:36,104-111,137-149,222-232`, `docs/design/MARK_II_AREA_PLAN.md:56,107-147`, `docs/findings/README.md:25` - checked against `syn/ooc/pp_resource_baseline.json`, the round-1 figures and the harness.

- **Plan against the record.** `receipts/plan_vs_record_head.txt`: 22 rows, 66 figures, 0 differences.
- **Route-only claim.** `MARK_II_AREA_PLAN.md:112` ("only the route figures changed") is confirmed by `receipts/record_delta_8b61b709_head.txt`.
- **Documentation gates** (`receipts/docs/`). Each returned rc 0:
  - `docs_check.py`;
  - `check_em_dash.py --base 8b61b709`: 212 added lines, 0 findings;
  - `check_em_dash.py --base 030eb98a`: 40 added lines, 0 findings;
  - `check_em_dash.py --selftest`: 339 arms;
  - `gen_toc.py --check`;
  - `check_doc_style.py`;
  - `DOC_MAP.gen.py --check`;
  - `check_feature_status.py --self-test`;
  - `gen_module_matrix.py --check`;
  - `check_solution_docs.py`.
- **Renderer.** The pinned Markdown renderer was installed into a private scratch environment. The first `check_em_dash` and `gen_toc` attempts returned 2 because the renderer was absent. The rc 0 reruns are `02v`, `03v`, `08v` and `10v`.
- **Commits.** Each of the three is one line with no trailers, and they sit on `030eb98a` with no rebase.

## 5. Reviewer ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_maap.sv:155-157,431-441`, `MAAP_FABRIC.md:104-111`, the M5 check, assignment 6093171536 items 1-5, acceptance 1-4 | R558-2 | f909d6c460344527f102f24b8e7a77f09959e755 |
| RTL | CLEAN | design-input diff `0df48637..f909d6c4` (hdl and sw trees, gitlinks), record policy delta; unchanged RTL was covered in round 1 | R558-2 | f909d6c460344527f102f24b8e7a77f09959e755 |
| Robustness | CLEAN | `sim_main.cpp:763-803`, 4 reviewer link-loss probes, the existing M5/M6 cancellation checks | R558-2 | f909d6c460344527f102f24b8e7a77f09959e755 |
| Tests | CLEAN | `sim_main.cpp`, `mutants.py`, default target (172/0; 52 rows), R559-1 plant verbatim, the same plant against the old harness, coverage 215/215 | R558-2 | f909d6c460344527f102f24b8e7a77f09959e755 |
| Docs | CLEAN (R558-2-R1 residue) | `MAAP_FABRIC.md`, `MARK_II_AREA_PLAN.md`, `docs/findings/README.md`, plan against record (0 of 66 differ), 13 docs-gate runs | R558-2 | f909d6c460344527f102f24b8e7a77f09959e755 |

## 6. Real limits

- **Standard text.** The IEEE 1722-2016 text is not available in this environment.
  - The new prose cites "Table B.3" for the absence of a leave event, where the assignment cites Table B.7. I could not check that table number.
  - The behavioural claim, that B.3.5.9 is an enter-only event, agrees with the issue, the assignment and round 1's reading of the standard.
- **No Vivado run.** The 445/340 and 443/280 MAAP figures and the record figures are the author's round-1 measurements. I checked them by design-input equality and arithmetic, not by re-measuring.
- **Not rerun here:**
  - the parent suite sweep;
  - Yosys;
  - the xvlog parser gate;
  - lint;
  - behave;
  - the firmware banks and the differential;
  - the processor banks;
  - the full 94-command docs bank (a focused 13-run subset was run).

  The delta changes none of their inputs except the MAAP harness and campaign, which were rerun.
- **Datapath M5 check.** It keeps its 8-cycle outage. R559-1-F1 allows the long outage in the unit harness, the datapath harness or both, so this is acceptable.
- **No manager source bank at this head.** None ran and none is claimed. The current-dev candidate against live dev `aef7ac66` was not built.
- **Hosted checks.** At the exact-head snapshot (2026-10-10T04:04:22Z, `receipts/hosted_snapshot.tsv`):
  - 12 completed with success;
  - 1 was skipped (Physical gPTP, nightly/manual);
  - 7 were in progress: `docs-check`, `elaborate`, `firmware-unit` and Verilator shards 0, 1, 2 and 4.

  No hosted verdict is claimed.
- **No hardware evidence.** Physical calibration was NOT RUN. The field skips are not hardware proof. Bench interop (acceptance 4) is not evidenced.
- **Redaction.** In `receipts/default_campaign.log` and `receipts/coverage.log`, the home-directory prefix in compiler command lines was replaced by `$HOME`.

## 7. Pending manager duties

- Carry R558-2-R1 to the residue checklist.
- Build and validate the current-dev merge candidate on live dev `aef7ac66` (builder and native banks), and link its receipts.
- Accept the hosted and replica contexts on the final head. At the snapshot, the Verilator shards, `firmware-unit`, `elaborate` and `docs-check` were still running.
- Hand acceptance 4 to the post-merge bench lane, then run post-merge containment.
- Obtain R559's round-2 verdict, which the merge also needs.

## 8. Receipts and reproduction

Paths are relative to this packet and listed in `MANIFEST.sha256`.

**Scripts**

- `scripts/plan_vs_record.py <repo> [rev]`
- `scripts/record_delta.py <repo> <old> <new>`
- `scripts/run_jobs.sh <packet> <bin>` runs the default target, the verbatim plant, then coverage and the probes, on disposable copies. It expects `<bin>/verilator` and `<bin>/verilator_coverage` to select the pinned 5.050.
- `scripts/probe_mutants.sh <tree>`
- `scripts/docs_subset.sh <tree> <out>`
- `scripts/clone_integrity.sh <repo> <head> <tree>`

**Clone integrity** (`receipts/clone_integrity.log`):

- HEAD and the tree are exact.
- The index tree equals the HEAD tree, the worktree equals the index, and there are no index flags.
- There are no untracked or ignored files.
- All 1,238 tracked files rehash equal, with their modes.
- The gitlinks are at their pins, and the submodule worktrees are clean.

Reading the gate's help text created one ignored `syn/ooc/__pycache__`; I removed it before that check. Every probe ran on scratch copies.

R558-2 FINISHED
