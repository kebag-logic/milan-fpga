[R580] NEGATIVE - exact head bc89f84e6757f8fcddf21958e99f40f17bc0ee1e

# R580-1: internal cleared-context review of PR #702 (Relates to #640, lane M0s step 2)

- Head `bc89f84e6757f8fcddf21958e99f40f17bc0ee1e`, tree `b498495714ea3ca8e3ab8e38781cc7ff54b68967`. It is one commit on dev `7c1b52bee26b497080ee22b1c1986109f80a5ee7`.
- The diff touches 9 files: `syn/ooc/` (2 new, 4 changed) and 3 pages under `docs/`.
- There is no RTL, firmware, workflow, baseline JSON or submodule-pin change. Pins are `external efeb541a`, `gptp-processor 5dce647a`, `protocol-processor 2ad2f845`, `lwSRP 9197193e` and `verilog-axis 48ff7a7e`, identical at base and head.
- Reconstruction order: AGENTS.md and CONTRIBUTING.md, then docs/README. Next, the #640 body and all manager and owner comments, including assignment 6086604096 and STOP 6087021702. Then the plan, AREA_BUDGET and the recipe page. Then the diff and history. Last, the published evidence at `6aae6d5f.../review-evidence/640-m0s-r1`.
- The PR had no prior review findings. Its only other review is the concurrent external R581-1, which was not consulted before this verdict and ledger were written.

## Verdict summary

The step-2 tooling does what the author's evidence says:
- The all-fabric and standalone paths are byte-identical to the base.
- Selected f0-f4 and full-split recipes and gate comparisons work.
- The named census refuses each role reversal.
- No policy, schema, threshold or record moves.
- The STOP diagnosis is correct.

Two MINOR findings remain open:
- **F1:** The default (all-fabric) selection checks no engine population. A wrapper-retaining F0-F4 image is accepted as all-fabric, and `record --write` writes it into the acceptance baseline. The new documentation states the contrary.
- **F2:** The recipe's placement marker is the only discriminator between a split route and all-fabric acceptance (probe P3). Removing the marker from the recipe, or the present-binding geometry check, survives every self-test and both mutation campaigns.

Conformance, Robustness, Tests and Docs are therefore UNCLEAN; RTL is CLEAN.

## Findings

### F1 - MINOR - Conformance, Robustness, Tests, Docs - default selection performs no population check

- **Where:**
  - `syn/ooc/pp_placement.py:56` (`selection()` returns False for an unmarked all-fabric request, so `validate()` reads nothing).
  - `syn/ooc/pp_baseline.py:205-226`: the all-fabric `prepare()` emits only `PP_REPORTS`, which checks wrapper count = 1 and no engine.
  - `syn/ooc/pp_placement.py:38-40` defines the all-fabric population, but no all-fabric recipe or gate path applies it.
  - Docs: `docs/design/AREA_BUDGET.md:370` "Missing or wrong-placement engines fail by name".
  - Docs: `docs/design/MARK_II_AREA_PLAN.md:659` "The gate refuses mismatched placement or incomplete population evidence".
  - Docs: `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:191`, where the all-fabric row says it "requires" the "existing shipping wrapper and protocol engines".
- **Authority:** assignment 6086604096 item 2: "Controls: a planted wrong-placement or missing-wrapper case fails by name". It also requires named population checks for a selected placement and "no re-record. Only M9 re-records acceptance". `limits()` explicitly permits F0-F4 to keep one wrapper (`pp_placement.py:44-45`).
- **Evidence (probe P3, `receipts/probe_marker.tsv`):** the fixture is the gate self-test's synthetic route, used as an F0-F4 candidate that keeps one wrapper. Without the marker that the default recipe never writes:
  - `check` as all-fabric gives exit 0 `RESULT: PASS`.
  - `record --write` gives exit 0 and the acceptance baseline changes.
  - With SRP removed from the hierarchy, the default check still gives exit 0 `RESULT: PASS`. The removal appears only as the ungated line `u_pp/u_srp: LUT -896, FF -50 (instance added or removed)`.
  - The legacy recipe refuses such an export only incidentally: `inventory()` refuses when `PP_TROM_HEX_P` is no longer bound. A wrapper-retaining export that still binds it passes, and the recipe's own f0-f4 path anticipates both cases (`pp_baseline.py:179-182`).
- **Impact:** a split image measured without `--placement` (operator omission at recipe time) is judged, and can be recorded, as the all-fabric acceptance endpoint. The wrong-placement control the assignment asks for exists only for images already labelled as split. The three documentation sentences above claim more than the code enforces.
- **Required outcome:** under the default selection, a measurement whose control-engine population is not the all-fabric one must be refused (exit 2) by role name. Alternatively, the manager may rule that the default stays wrapper-only. In that case the recipe, plan and budget pages must state that the default verifies only the wrapper, and must name this case as a known limit with that ruling referenced.
  - Either way, the recorded endpoints must stay comparable: the same identity, record shape, policy, tolerances and existing check results.
- **Verification:**
  - A planted control: a wrapper-retaining F0-F4 measurement with no selection marker, judged under the default, exits 2 naming the missing role(s). Or, under the ruling, the corrected doc lines.
  - Probe P2's legacy parity stays IDENTICAL.
  - `check-baseline` still passes.

### F2 - MINOR - Tests - the recipe's load-bearing split guards are untested

- **Where:**
  - `syn/ooc/pp_baseline.py:265` writes the `# baseline placement: <name>` marker, which the gate's `selection()` requires.
  - `syn/ooc/pp_baseline.py:181` keeps geometry checks for a removed protocol's ROM binding that is still present, a behaviour documented at `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:242`.
  - Tests: `syn/ooc/pp_placement_selftest.py:73-127` (`recipe_selftest`) and `syn/ooc/pp_baseline_mutants.py:13-25`.
- **Evidence (probe P1, `receipts/probe_mutants.tsv`):**
  - Mutant B5 deletes the marker from the emitted split script. Recipe and gate self-tests both give rc 0, so it SURVIVES.
  - Mutant B4 skips a removed-protocol ROM binding even when present. Both give rc 0, so it SURVIVES.
  - Neither is in the author's 41-mutant table.
  - Probe P3 shows why B5 matters: a split directory without the marker is accepted by `check` and `record --write` as all-fabric, while the same directory with the marker is refused as `wrong placement`.
  - The gate fixtures write the marker themselves (`pp_placement_selftest.py:139`), so no test connects the recipe's emission to the gate's refusal.
- **Impact:** a later edit that drops the marker or the present-binding check passes every hosted and local gate. The f0-f4/full-split measurements then lose the refusal that keeps them out of all-fabric acceptance, and the documented geometry claim becomes false, with no failing test.
- **Required outcome:**
  - The recipe self-test asserts that each selected script carries exactly one marker naming the requested selection.
  - An f0-f4 export that still binds `PP_TROM_HEX_P` with bad geometry is refused by name.
  - Both enforcement removals are detected, by the campaign or an equivalent control.
- **Verification:** re-run `scripts/probe_mutants.py`. B5 and B4 must report DETECTED, with the control passing.

### S1 - SUGGESTION - Tests - remaining undetected mutants and self-test hooks

Probe P1 surviving mutants:
- **B1:** the split synthesis-command count check removed.
- **B6:** the split `--synthesis-only` endpoint swapped to the full flow.
- **G1:** the ooc refusal for a selected placement removed. Behaviour is partly equivalent, because an unmarked ooc script is still refused by `selection()`.
- **G3:** the M9 refusal for `check-baseline`. This is equivalent: check-baseline does not read the placement.
- **G8:** datapath provenance accepted for all-fabric. Equivalent on the current fixtures.
- **G10:** the `--fuzz` split refusal removed.
- **G13 and B9:** disabling the one-line hooks that run `gate_selftest`/`recipe_selftest`. This silently removes all 59 placement gate controls and the recipe controls while CI stays green.

Consider controls for B1/B6/G10, and a count assertion in the mutation drivers, or the CI step, that the placement controls ran.

### S2 - SUGGESTION - Conformance - census breadth

The f0-f4 census names ADP, both ACMP engines, SRP and both MAAPs. The plan's removal table (`MARK_II_AREA_PLAN.md:680-690`) also assigns:
- the originator (F3/F5);
- the ACMP binding store (F1/F3);
- the NVM port and the wrapper NVM backend (F1).

An image that keeps those blocks would still pass as `f0-f4`. The measurement itself stays honest (whole-image), so this is not a defect. Consider naming the F1/F3-owned blocks once the integration lane fixes their placement, or stating the census's scope in the recipe table.

## Assignment items (judged at this head)

1. **Recipe and gate name and measure a selected placement without the single-wrapper assumption.** Met for labelled selections:
   - `--placement {all-fabric,f0-f4,full-split}` on both tools.
   - `prepare_split` has a census after synthesis and after the endpoint. It writes `baseline_placement.tsv`, has no `PP_REPORTS`, and uses image-rooted timing (`pp_placement.py:110-120`).
   - The gate reads wrapper-free provenance through `milan_datapath.sv` and image-rooted scopes, and binds the placement into the input digest.
   - The default selection is the gap in F1.
2. **All-fabric endpoint and 1x1/8x8 references unchanged and comparable.** Reproduced in probe P2 (`receipts/probe_parity.tsv`). Base and head `pp_baseline.py` produce byte-identical outputs (14 to 17 files each) for these variants:
   - integrated route;
   - synthesis-only;
   - attribution-only;
   - single-thread;
   - standalone;
   - standalone single-thread;
   - standalone integrated clock.

   Each variant is IDENTICAL both with and without explicit `--placement all-fabric`. Base and head `pp_resource_gate.py` produce identical output for:
   - `check-baseline` on the real record: rc 0/0, `baseline PASS: 3 endpoints`;
   - `record` of the legacy route and ooc fixtures;
   - `check` of the legacy fixture against the real record: rc 2/2, the same refusal;
   - `--fuzz 3000 --seed 234`.

   The head self-test's first 310 lines equal the base self-test's, and 59 placement lines follow. The recorded endpoints are unchanged: route-1x1 is 50,267 LUT, 74 RAMB36 / 27 RAMB18, 87.5 tiles, WNS/WHS +0.299/+0.031, identity Build 6511674 with the recorded flow. No real Vivado measurement directory is published, so re-checking the endpoints' own run directories is a limit (below).
3. **Controls.**
   - Recipe mutants: 41 of 41 detected with the control passing. Resource mutants: 180 of 180 detected. Both reproduced, and the log digests equal the author's `RECEIPTS.tsv` (`recipe-mutants`, `gate-mutants`).
   - The Tcl census refuses every role reversal by `placement: role (module)` in all three selections and at both stages.
   - The gate refuses absent, duplicate and wrong markers, missing census, wrong header, wrong row placement, missing wrapper row, duplicate rows, invalid counts and each role reversal by name.
   - My probe adds 24 of 34 further mutants detected; the survivors are F2 and S1.
   - The wrong-placement-under-default case does not fail (F1).
4. **No gate policy, schema, threshold or baseline change and no re-record.** Met:
   - `pp_resource_baseline.json` is untouched.
   - The constants ROWS, GATED, POLICY, RECORD, IDENTITY and SCOPE are unchanged.
   - The `check-baseline` policy table is equal.
   - Selected `record --write` and `check-baseline` are refused ("belongs to M9"), and the gate self-test proves the baseline bytes are unchanged.
5. **Ledgers marked intermediate and claim no split figure.** Met:
   - `MARK_II_AREA_PLAN.md:634-669` has "Not measured" in every column and STOP.
   - `AREA_BUDGET.md:358-380` gives the accepted 50,267-LUT record as a stored anchor. Its 74 + 27/2 = 87.5 tiles is checked against the JSON.
   - The 121.5-tile ceiling and 10 % reserve are retained.
6. **STOP diagnosis.** Confirmed:
   - `sw/litex/milan_soc.py:2505` (CtrlMailbox docstring: "THE DATAPATH SIDE IS NOT CONNECTED IN F0") and `:2549-2552`: link, GM, RX and gPTP domain are tied to 0, `o_tx_valid_o=Signal()`, and `i_tx_ready_i=1`.
   - `hdl/milan/milan_datapath.sv:8003`: `KL_pp_shadow` is instantiated at module scope, after `end : pp_ctr_event_queue`, with no enclosing generate.
   - No build switch removes it; `--ctrl-mailbox` (`milan_soc.py:3612`) adds only the mailbox skeleton.
   - The census module names exist with one shipping instance each: `protocol_processor_top.sv` lines 1918/2100/2231/2341/2494/3733/3957, `KL_maap` in `milan_datapath.sv` g_maap, `KL_gptp_shadow` in g_gptp_plane, and `KL_mbx` only under `--ctrl-mailbox`.
   - The all-fabric oracle's processor-MAAP = 0 matches the current route record, whose scopes have no `u_pp/u_maap`, while the ooc records do.

## Executed evidence (this round, exact head, local)

All jobs ran concurrently with their own log and rc under `receipts/gates/`. The environment was:
- `TMPDIR` inside the packet scratch, with bytecode writing disabled;
- the pinned Markdown venv;
- Verilator 5.050 on PATH (identity verified);
- the pinned RV32 SDK (archive sha256 `d42680e9...b78f` verified, extracted to scratch).

| Job | rc | Result |
|---|---:|---|
| `pp_baseline.py --selftest` | 0 | includes 3 placement Tcl lines and the recipe placement line |
| `pp_baseline_mutants.py` | 0 | control + 41 detected; log digest = author's |
| `pp_resource_gate.py --selftest` | 0 | legacy arms + 59 placement gate controls |
| `-X cpu_count=4 pp_resource_gate_mutants.py` | 0 | 180 mutants fail; log digest = author's |
| `pp_resource_gate.py check-baseline` | 0 | `baseline PASS: 3 endpoints` |
| `pp_baseline_reports_selftest.py` | 0 | digest = author's |
| `ooc_tcl_selftest.py` | 0 | 58 arms (485 s) |
| `dp_srcs.py --selftest` + both tops | 0 | 35 arms |
| `scripts/pp_srcs.py --check --selftest` | 0 | digest = author's |
| builder bank `sw/builder/test_builder.py --require-rv32` | 0 | 1128 s; "ALL GATES PASS EXCEPT 14 NOT RUN" (no LiteX interpreter here; one calibration report absent) |
| `docs_check.py` | 0 | 0 findings / 201 md |
| doc style + selftest, doc paths, DOC_MAP, feature status, module matrix | 0 | |
| `check_em_dash.py --base 7c1b52be` | 0 | 165 added lines, 339/339 arms |
| `gen_toc.py --check` and `--verify-anchors` | 0 | |
| `check_py_idiom.py` | 0 | ratchets at budget |
| `git diff --check 7c1b52be HEAD` | 0 | |

The builder bank was first started with the other jobs and stopped at the 590 s wrapper limit (`receipts/gates_summary.txt`). It was re-run alone and completed rc 0 (`scripts/run_builder_bank.sh`, `receipts/gates/builder_bank.time`).

Reviewer probes (scripts in `scripts/`):
- **P1** `probe_mutants.py`: 34 extra mutants plus a control, 12 workers.
- **P2** `probe_parity.py`: base-vs-head legacy parity.
- **P3** `probe_marker.py`: marker and default-selection acceptance.

After the probes:
- HEAD and tree are as stated, `git write-tree` = `b4984957...`, and the index and HEAD tree entry digests are equal.
- The worktree and the three initialised dependencies are clean.
- The builder bank's ignored `sw/builder/out/` output, created by this run, was removed (`receipts/tree_integrity.txt`).

Hosted checks at the exact head (`receipts/hosted_checks.tsv`, fetched 19:16Z), executed and successful:
- bdd-conformance, changes, docs-check-no-git, elaborate, full-ci-gate, verilator-lint, wire-accountability;
- Verilator shard 3/5 and Yosys shards 0-3/4;
- yosys-elaboration, whose "Prove the OOC read sets..." step runs the recipe and resource self-tests and both mutation campaigns: success.

Still in progress at fetch time: docs-check, firmware-unit, Verilator shards 0, 1, 2 and 4. Skipped context, not executed: Physical gPTP (nightly and manual). The manager owns hosted and act acceptance.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Assignment 6086604096 items 1-3 against `pp_baseline.py:259-276,612-618`, `pp_placement.py:34-107`, `pp_resource_gate.py:169-295,381-386,701-760`; P2 parity; P3; STOP lines `milan_soc.py:2505,2549`, `milan_datapath.sv:8003` | R580-1 | bc89f84e6757f8fcddf21958e99f40f17bc0ee1e |
| RTL | CLEAN | No hdl/ or pin delta (`git diff --raw`, gitlinks equal); census identities against `protocol_processor_top.sv`, `milan_datapath.sv` g_maap/g_gptp_plane, `KL_mbx.sv`; Tcl census and image timing executed under tclsh (`pp_placement_selftest.py:35-70`); recorded route scopes for dark processor MAAP | R580-1 | bc89f84e6757f8fcddf21958e99f40f17bc0ee1e |
| Robustness | UNCLEAN (F1) | Malformed census, wrong header, row, duplicate and invalid counts, missing census/role, ooc selection, endpoint options, ROM absence and geometry (gate and recipe self-test logs, P1); default-selection mislabelled split (P3) | R580-1 | bc89f84e6757f8fcddf21958e99f40f17bc0ee1e |
| Tests | UNCLEAN (F1, F2) | `pp_placement_selftest.py`, both mutation drivers; 41 + 180 campaigns reproduced; P1 34 mutants (10 survivors); P3 | R580-1 | bc89f84e6757f8fcddf21958e99f40f17bc0ee1e |
| Docs | UNCLEAN (F1) | `PP_SHADOW_BASELINE_RECIPE.md:183-277`, `MARK_II_AREA_PLAN.md:634-669,1056-1065`, `AREA_BUDGET.md:346-380` against code, JSON record and STOP; docs gates rc 0 | R580-1 | bc89f84e6757f8fcddf21958e99f40f17bc0ee1e |

## Real limits

- No Vivado run was made. The Tcl census was executed only under tclsh against a stubbed `get_cells`. Whether `ORIG_REF_NAME`/`REF_NAME` survive synthesis and route for every role is shown only for the wrapper (existing recipe) and for the engines' hierarchy names in recorded routes. The dark processor MAAP's presence after synthesis, as opposed to after route, is not established; a retained cell would make a wrapper-retaining f0-f4 census fail closed.
- No integrated split export exists, so no selected route can be measured. This is consistent with the STOP.
- The recorded endpoints' own measurement directories are not published. Their check results were reproduced only as `check-baseline` and as base/head parity on synthetic fixtures.
- The builder bank was run with 14 arms NOT RUN, because no LiteX interpreter is available here. Physical calibration was NOT RUN; field skips are not hardware proof.
- Hosted contexts listed as in progress were not awaited.

## Pending manager duties

- Rule on F1's alternative: a default population check, or a documented limit by ruling.
- Re-review after the fixes for F1 and F2.
- Validate the current-dev merge candidate (builder and native banks) at the merge turn.
- Accept the hosted exact-head contexts still running (docs-check, firmware-unit, Verilator shards 0/1/2/4) and the act replica.
- Collect the second positive review.
- Merge only with maintainer authorization.

R580-1 FINISHED
