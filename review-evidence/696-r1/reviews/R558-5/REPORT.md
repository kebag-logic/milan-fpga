[R558] NEGATIVE - exact head 87d51e76972de36be477844a39182da8a122a5eb

# R558-5 - issue #696 / PR #706 - composition review of the merge-train candidate

- Candidate: `87d51e76972de36be477844a39182da8a122a5eb`, tree `03143567d700df74f208ff16f547f5023f485d62`.
- Parents: train base `c64a9b66` and PR head `30073ee9`.
- Review start: https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6097083162
- Scope: composition acceptance only. The source head `30073ee9` has two POSITIVE source reviews, R558-4 ([6095865153](https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6095865153)) and R559-4 ([6095881954](https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6095881954)).

## Verdict in one paragraph

The composition is mechanically clean and loses nothing. The train base tree equals live dev `e8454e27`, tree `b90bf2ca`. Both `merge-tree(e8454e27, 30073ee9)` and `merge-tree(c64a9b66, 30073ee9)` reproduce the candidate tree `03143567`. Only two files are changed on both sides: `docs/design/AREA_BUDGET.md` and `docs/design/MARK_II_AREA_PLAN.md`. Every other file is byte-equal to exactly one side. In both shared pages, every changed line from each side survives unchanged. All 32 gates that read the composed files pass at the candidate. These include `docs_check.py`, `gen_toc.py` (check, anchors, self-test), `check_em_dash.py` against the parent and against dev, `ci_events.py`, and the M0s resource gate's `check-baseline` and self-tests run over #696's record. All 76 current-record figures on the two pages match `pp_resource_baseline.json` at the candidate. The MAAP suite (172/0 unit, 3/0 real datapath) and the TDM8 render suite that dev changed (266/0, 71/0, 5/5 leg defects) pass on the composed tree.

**One composition defect is open, so the verdict is NEGATIVE.** M0s wrote its step-1 status against the #645 record. Two of its sentences say the current comparison record is still that record's 50,267-LUT route. At the candidate, #696 has re-recorded that route at 50,230 LUTs, so the same pages now name two different routes as the current record (F1, MINOR, Docs). Neither source is wrong alone; the merge creates the contradiction, and no documentation gate catches it.

## Reconstruction (public state only)

1. `AGENTS.md`, `CONTRIBUTING.md` (precedence), `docs/README.md`.
2. Issue #696: the body (acceptance 1-4) and the public rulings in its comments: 6076750392, 6076940309, 6079087547, 6079463350, 6080332335, 6089712293 and 6093171536. Acceptance 3 asks for resource records re-recorded through the recipe, with no floor exception.
3. Interface authorities read for the overlap: `docs/design/AREA_BUDGET.md` (record table, re-baselines, M0s sections, resource gate), `docs/design/MARK_II_AREA_PLAN.md` (gate row, current inventory, ledger, M0s step-1 status), `docs/testing/PP_SHADOW_BASELINE_RECIPE.md#selected-placement-measurements`, `syn/ooc/pp_resource_baseline.json`, `syn/ooc/pp_placement.py`, `syn/ooc/pp_resource_gate.py`.
4. `git diff c64a9b66..87d51e76` (17 files) and history. The dev side is `8b61b709..e8454e27`: 52 files, from PR #701, the F5 AECP firmware lane and M0s #702. The PR side is `8b61b709..30073ee9`: 17 files.
5. Public evidence: `review-evidence/696-r1` at `97f433d6` (tree listing, `merge-receipts/check-route-1x1.log`) and the manager's evidence comments. Prior review findings on the PR were read only after this round's own pass and its F1 evidence (`receipts/f1_evidence.txt`) were written.

## Composition map

| Item | Result | Receipt |
|---|---|---|
| Base equals live dev | tree `c64a9b66` = tree `e8454e27` = `b90bf2ca` | `receipts/provenance.txt` |
| Candidate reproducible | both merge-trees give `03143567`, no conflict | `receipts/provenance.txt` |
| Files changed by both sides | `docs/design/AREA_BUDGET.md`, `docs/design/MARK_II_AREA_PLAN.md` only | `receipts/pr_files_since_8b61b709.txt`, `receipts/dev_files_8b61b709_e8454e27.txt` |
| Every other file | 15 PR files equal to `30073ee9`; 50 dev files equal to `e8454e27` | `receipts/blob_provenance.txt` |
| Shared pages lossless | dev->candidate changed lines = PR's changed lines, and source->candidate changed lines = dev's changed lines, on both pages | `receipts/overlap_hunks.txt` |
| Gitlinks | `protocol-processor 2ad2f845`, `gptp-processor 5dce647a`, `third_party/verilog-axis 48ff7a7e`, `lwSRP 9197193e`, `external efeb541a`, same on both sides | `receipts/provenance.txt` |

Semantic interactions examined beyond the shared pages:

- **The M0s resource gate reads #696's record.** `check-baseline` gives `baseline PASS: 3 endpoints`. M0s's placement self-test confirms the acceptance schema, record and policy are unchanged. The gate self-test passes. The all-fabric recipe path (`prepare`, `inventory` default) is unchanged by M0s, so #696's record identity and flow remain the comparison identity.
- **The M0s all-fabric population census.** It expects exactly one `KL_maap` and zero `KL_pp_maap` and `KL_mbx`. #696 keeps one `KL_maap` module (`KL_maap.sv:75`) and one instance (`milan_datapath.sv:7168`). It adds no module and renames none.
- **#701's TDM8 render harness meets #696's datapath RTL for the first time.** The default suite passes on the composed tree.
- **Other dev firmware and test changes do not reach the MAAP suite or differential.** The MAAP differential compiles `maap/maap.c`, `KL_maap.sv` and its own test, and none of these is touched by dev. `integration.mk` derives its inputs from `tb/verilator/milan_dp`, `hdl` and the processor pin, which dev also leaves untouched.
- **Docs registries.** `docs/README.md` (dev, one row), `TESTING.md` (dev) and the new M0s anchors were checked. The TOC, anchors, DOC_MAP, doc paths and em-dash checks pass.

## Findings

### R558-5-F1 - MINOR - Docs - `docs/design/AREA_BUDGET.md:368`, `docs/design/MARK_II_AREA_PLAN.md:653-654` - after the merge, M0s's step-1 status still names the #645 50,267-LUT route as the accepted comparison record

- **Authority/evidence:**
  - At the candidate, `pp_resource_baseline.json` records `route-1x1` LUT = 50230 (#696, merge result `0df48637`).
  - `AREA_BUDGET.md:129` says "The table is the gate's record", and its table at `:122` gives 50,230.
  - `MARK_II_AREA_PLAN.md:110` names #696's re-baseline as "the gate's current record".
  - On the same pages, the M0s text reads:
    - `AREA_BUDGET.md:368`: "The accepted 50,267-LUT route remains the comparison record."
    - `MARK_II_AREA_PLAN.md:653-654`: "The last accepted gate record remains unchanged. Its 50,267 LUTs and 74/27 RAM primitives remain comparison anchors."
  - `AREA_BUDGET.md:354` and the recipe page require D7 and the selected routes to compare against "the last accepted gate record" and "the accepted `route-1x1` record". At the candidate, the gate compares against 50,230.
  - Both sentences come from dev `e8454e27`, where they were true. They are absent at source `30073ee9` (`receipts/f1_evidence.txt`). The merge alone makes them false.
  - The manager's composition criterion asks that every figure and record identity on both pages match the recorded file at the candidate.
- **Why MINOR and not RESIDUE:** both sentences make a claim about a figure and a record's identity: which record is the gate's comparison anchor, and its LUT count. They are not baseline-scoped sentences. That differs from R558-2-R1 / R559-2-R1, where every figure was correct for a baseline the page explicitly retains (`MARK_II_AREA_PLAN.md:110-113`). Here the sentences name the *gate* record. A later M0s or D7 lane following them would report its delta against 50,267 while the gate judges against 50,230, a 37-LUT and 105-FF difference.
- **Impact:** the merged pages contradict themselves about the current acceptance record, and the text that steers the next measurement lane points at a superseded record. No gate detects this; all 32 documentation and resource gates pass.
- **Required outcome:** at the merged head, each sentence either names #696's record as the comparison record (50,230 LUTs, 74/27, 87.5 tiles unchanged) or is explicitly dated to the `7c1b52be` base. Neither may claim the gate record is unchanged or is 50,267. One fix that keeps every other M0s claim:
  - `AREA_BUDGET.md:368`: "At base `7c1b52be` the comparison record was #645's 50,267-LUT route; [#696](https://github.com/kebag-logic/milan-fpga/issues/696)'s 50,230-LUT route has since replaced it."
  - `MARK_II_AREA_PLAN.md:653-654`: "At that base the last accepted gate record was #645/#647's 50,267 LUTs and 74/27 RAM primitives. [#696](https://github.com/kebag-logic/milan-fpga/issues/696) has since re-recorded it at 50,230 LUTs with 74/27 unchanged; that record is the comparison anchor, and the ledger keeps the baseline figures."
- **Verification:**
  - `git grep -n "50,267" -- docs/design/AREA_BUDGET.md docs/design/MARK_II_AREA_PLAN.md` shows no sentence that calls 50,267 the current, last accepted or comparison gate record.
  - `python3 -I check_figures.py <tree>` exits 0 (this packet).
  - `docs_check.py`, `gen_toc.py --check`/`--verify-anchors` and `check_em_dash.py --base <parent>` exit 0, plus `pp_resource_gate.py check-baseline`.

### R558-5-R1 - RESIDUE - Docs - `docs/design/AREA_BUDGET.md:359,376`, `docs/design/MARK_II_AREA_PLAN.md:666` - lane-scoped "records are unchanged" lines now sit beside #696's re-record

These three M0s sentences ("Acceptance records and policy values remain unchanged." / "Acceptance records, schema and policy are unchanged." / "The acceptance schema, thresholds and records are unchanged.") are true of the M0s change, and their paragraphs make that the subject. On the composed pages, a reader could take them as page-wide. This is wording only: no figure or record identity is stated. Exact fix: prefix each with "M0s changes no", e.g. "M0s changes no acceptance record, schema or policy value." Verification: reread the lines, then run `check_em_dash.py --base <parent>` and `docs_check.py`.

## Prior public findings on this PR, at this head

| Finding | State at `87d51e76` | Evidence |
|---|---|---|
| R558-3-F1 = R559-3-F1 (BLOCKER; GNU make 4.3 capture leak in `integration.mk`) | Resolved; unchanged by composition | `tb/verilator/maap/integration.mk` blob equal to `30073ee9` (`receipts/blob_provenance.txt`). On the composed tree the integration build and run gives 3/0 (`receipts/suites/maap.log:700-713`), under make 4.4.1 only |
| R558-1-F1, R559-1-F1/F2/F3 (MINOR) | Still resolved | the MAAP_FABRIC, sim_main, sim_integration and mutants blobs equal source. The MARK_II inventory and gate row equal the record (`receipts/check_figures.log`, 76/76) |
| R558-2-R1 / R559-2-R1 (RESIDUE, `MARK_II_AREA_PLAN.md:66-67`, `:317`, `:970`) | Retained on the residue checklist; the residue still applies at the candidate, unaffected by dev's additions (which start at `:638`) | `sed -n 64,68p` at the candidate |
| R558-4-R1 (RESIDUE, PR body stale head) | Retained; the PR body still states `f909d6c4` | PR body as read during this round |
| R558-3-S1/S2, R558-4-S1/S2, R559-4-S1/S2, R558-1-S1, R559-1-S1..S4 (SUGGESTION) | Retained, optional | unchanged sources |

## Lens results (artifact-specific)

- [R558] UNCLEAN Docs - `docs/design/AREA_BUDGET.md:368`, `docs/design/MARK_II_AREA_PLAN.md:653-654` - open MINOR R558-5-F1. Also examined, and clean apart from RESIDUE R558-5-R1:
  - the record table `AREA_BUDGET.md:120-138`, the stack and wrapper figures `:143-149`, the gate comparison `:407` and the seventh re-baseline `:460-463`;
  - `MARK_II_AREA_PLAN.md:56` and `:110-147` (76/76 figures equal the record);
  - the M0s selection, placement-marker, population-check and split-recipe text, which is present and unmodified on both pages;
  - `docs/README.md` and `TESTING.md`;
  - 32/32 gates (`receipts/gates/`).
- [R558] PASS Conformance - the 15 PR blobs equal source (`receipts/blob_provenance.txt`); `syn/ooc/pp_resource_baseline.json` equals `30073ee9`; `receipts/gates/resource_check_baseline.log` - the composition changes no MAAP RTL, test or record byte, so acceptance 1-3 stand as the source reviews established them. The re-record is still accepted by the M0s gate at the candidate (`baseline PASS: 3 endpoints`). The only composed artifacts are the two prose pages (Docs).
- [R558] PASS RTL - `hdl/ieee1722/maap/KL_maap.sv`, `hdl/milan/milan_datapath.sv` blobs equal `30073ee9`; dev `8b61b709..e8454e27` changes no `hdl/` file; `KL_maap.sv:75`, `milan_datapath.sv:7168` against `syn/ooc/pp_placement.py:19-31,40-43` - the composed RTL is the source-reviewed RTL. M0s's all-fabric census expects exactly one `KL_maap`; #696 keeps one module and one instance. The render datapath build elaborates and passes on the composed tree.
- [R558] PASS Robustness - `syn/ooc/pp_resource_gate.py` and `pp_placement.py` (dev) over `pp_resource_baseline.json` (#696): `check-baseline` 0, gate self-test 0, placement self-test 0 (`receipts/gates/`) - the M0s refusal paths still work with #696's record in place (wrong placement, incomplete census, tool or recipe change, record --write refused for selections, baseline bytes unchanged). The MAAP robustness behaviour is byte-identical to source.
- [R558] PASS Tests - `receipts/suites/maap.log` (unit 172/0; datapath 3/0: M4 MAC diversity, M5 link return, M3 clock seed), `receipts/suites/render.log` (shipping 266/0, multi-stream 71/0, `--leg-defects` 5/5; rc 0), `receipts/check_figures_probe.log` - these suites are the ones whose inputs come from both sides. The render harness (dev #701) runs over #696's datapath for the first time and passes. The figure comparator used for this round fails on a planted one-figure change (rc 1), so its 76/76 result can fail.

## Reviewer-owned ledger (this round)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN (the composition does not touch its scope; source coverage R558-4 and R559-4 at `30073ee9`) | blob provenance of the 15 PR files, the record file, `check-baseline` under the M0s gate | R558-5 | 87d51e76972de36be477844a39182da8a122a5eb |
| RTL | CLEAN (the composition does not touch its scope; source coverage R558-4 and R559-4 at `30073ee9`) | `KL_maap.sv`, `milan_datapath.sv` blobs; no dev `hdl/` change; M0s census against the instance count; render build | R558-5 | 87d51e76972de36be477844a39182da8a122a5eb |
| Robustness | CLEAN (composition touches it only through the M0s gate reading #696's record) | `check-baseline`, gate self-test, placement self-test | R558-5 | 87d51e76972de36be477844a39182da8a122a5eb |
| Tests | CLEAN | MAAP unit and datapath, TDM8 render default suite, comparator probe | R558-5 | 87d51e76972de36be477844a39182da8a122a5eb |
| Docs | **UNCLEAN** (R558-5-F1 MINOR open; R558-5-R1 RESIDUE) | both shared pages in full at the overlap, 76 record figures, 32 doc and resource gates | R558-5 | 87d51e76972de36be477844a39182da8a122a5eb |

## Executed evidence (this packet)

| Command | Result |
|---|---|
| `run_gates.sh <candidate> <venv-python> receipts/gates` (32 gates, at most 16 at once, locked Markdown renderer from `tools/markdown/requirements.txt`) | 32/32 rc 0. `docs_check: 0 finding(s) across 202 md files`; `TOC gate: OK`; `anchor check: 462 ... reproduced`; `check_em_dash ... [c64a9b66..HEAD]` 0 findings over 212 added lines in 7 pages, and 0 against `e8454e27`; `ci_events: OK (1749 contract items)`; `baseline PASS: 3 endpoints` |
| `run_suites.sh <scratch clone> <pinned 5.050> receipts/suites maap` | rc 0; `KL_maap: 172 checks, 0 failures`; `MAAP integration: 3 checks, 0 failures` |
| `run_suites.sh ... render` | rc 0; `tdm8_render: checks: 266 failures: 0`, `checks: 71 failures: 0`, leg defects 5/5 |
| `python3 -I check_figures.py <candidate>` | rc 0; 76 figures compared, 0 differences |
| same over a copy with one planted figure (`u_pp/u_talker` 664 -> 641) | rc 1; names the planted row |
| `receipts/provenance.txt`, `blob_provenance.txt`, `overlap_hunks.txt`, `f1_evidence.txt` | the composition map above |

The suites ran in a scratch clone at the exact head. Its submodules were populated from this clone's own module store; the gitlinks were verified against `HEAD`. The host-private toolchain path prefix in the two suite logs is redacted as `<pinned-verilator-root>`. After the gate runs, the review clone was verified clean: no tracked or untracked change, index and worktree equal to `HEAD`. This round's interpreter caches were removed from it.

## Real limits

- The resource gate's `check` and M0s's all-fabric census were not re-run on #696's routed measurement directory. Its hierarchy report is not in the public evidence, and no Vivado run was in scope. The census expectation is checked by instance count against RTL, not against the routed report.
- The MAAP mutation campaign (52 rows), coverage, the firmware differential, the parent sweep, Yosys and the processor banks were not re-run. None of their inputs changes between source and candidate (blob provenance); source receipts and source reviews cover them.
- The make-4.3 hosted shape of `integration.mk` was not reproduced here; only make 4.4.1 was run.
- No hosted or act evidence for this candidate was inspected; the manager owns it. Physical calibration and bench interop (acceptance 4) were not run. Field skips are not hardware proof.
- No manager source bank exists at this head, and none is claimed.

## Pending manager duties

- Route R558-5-F1 to a fix at the merge candidate (a Docs-only change to the two sentences), then re-review the Docs lens at the new head.
- Carry R558-5-R1, R558-4-R1 and R558-2-R1 / R559-2-R1 on the residue checklist.
- At the merge turn: the current-dev candidate builder and native banks. Run the resource gate `check` on the routed directory if the merge turn produces one, which exercises M0s's census on a real all-fabric route. Then hosted and act acceptance, and the bench lane for acceptance 4.

R558-5 FINISHED
