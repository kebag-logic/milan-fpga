[R558] NEGATIVE - exact head 1ceada05ff6384af12233eac8ea405b3bdfc6fae

# R558-11 - issue #696 / PR #706 - composition review of the merge-train candidate

- **Candidate:** `1ceada05ff6384af12233eac8ea405b3bdfc6fae`, tree `4650fd5d9d5c940bc6788491229dc808cf866962`.
  - First parent: live dev `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc` (merge of PR #707, #621), which carries `c20c85bd` (merge of PR #722, Mark II M5, #640).
  - Second parent: PR source head `aa980479aafd1d72c72015707fa6618b5aa47cb1`, last merged with dev `09c7231e`.
- **Role:** cleared-context internal reviewer, composition acceptance only. The source head has two POSITIVE source reviews: R558-10 (comment 6114159517) and R559-8 (comment 6114178642).
- **Verdict:** NEGATIVE on one composition MINOR (R558-11-F1, Docs). It is the same class of defect as R558-9-F1, which the PR fixed for M2 and M6 at `aa980479`.
  - M5's newly merged section of `MARK_II_AREA_PLAN.md` says its 50,267-LUT base route "equals the `route-1x1` record". In the composed tree, that record is #696's 50,013-LUT record.
  - Every RTL, test and gate result on the composed tree is clean. The M5 pass verdict and the partial-central figure are both correct.

## 1. Scope reconstructed from public state

- **Read in order:**
  1. AGENTS.md, CONTRIBUTING.md and docs/README.md.
  2. The #696 issue body and every assignment and ruling comment: 6076750392, 6076940309, 6079087547, 6079463350, 6080332335, 6089712293, 6093171536, 6097504752 and 6102832618.
  3. The round's start comment, 6117947877.
  4. `docs/design/AREA_BUDGET.md`: the resource-gate policy, D7 and the merge-bank rule at `:444-449` and `:512-527`.
  5. `docs/design/MARK_II_AREA_PLAN.md` and `syn/ooc/pp_resource_baseline.json`.
  6. The diff `c6bd08c6..1ceada05` and the history.
  7. The public evidence index at `97f433d6:review-evidence/696-r1` (the author's source-head receipts).
- **Composition question:** does the composed tree add any defect beyond the two reviewed sources, dev `c6bd08c6` and PR `aa980479`?

## 2. Composition facts (`receipts/composition_overlap.txt`, `receipts/pr_delta_over_dev.diff`, `receipts/pr_source_delta.diff`)

- **The candidate is the mechanical merge.**
  - `git merge-tree --write-tree c6bd08c6 aa980479` gives `4650fd5d`, the candidate's tree, with no conflict.
  - The merge base is `09c7231e`.
- **Both deltas are carried unchanged.**
  - `c6bd08c6..1ceada05` and `09c7231e..aa980479` have the same stable patch-id (`d5ad5e91...`): 17 files, +1,619/-267.
  - The dev side `aa980479..1ceada05` equals `09c7231e..c6bd08c6` apart from hunk offsets: 49 files.
- **Files changed on both sides:** exactly one, `docs/design/MARK_II_AREA_PLAN.md`, as the manager named it.
  - The dev side (M5, `c20c85bd`) adds `:536` and the new section "M5 intermediate measurement", `:1075-1111`.
  - The PR side changes `:56`, `:110-147`, `:656-657`, `:696-697`, `:707`, `:948` and `:969`.
  - There is no textual overlap. A semantic interaction is found and reported as R558-11-F1 / R1.
- **Other shared surfaces checked:**
  - **RTL.** The dev side does not change `milan_datapath.sv` or `KL_maap.sv`. Its RTL changes are `hdl/common/csr/milan_csr.sv` (M5, read path only) and the `gptp-processor` pin `7dda9c3b` (#621).
    - The PR's datapath edits are one comment and the `.port_operational_i(eff_link_w)` / `.realtime_ns_i(ptp_now_w[31:0])` connections.
    - So the composed `milan_datapath` elaborates the PR's `KL_maap` with dev's CSR block and gPTP pin. That composition is exercised in section 4.
  - **Test plumbing.**
    - `tb/verilator/maap/integration.mk` derives its sources and flags from `milan_dp`'s `print-srcs` / `print-dp-vflags`. Dev's #621 changed `tb/verilator/milan_dp/Makefile`, moving the `gmstep` leg to the new `milan_dp_gm_steps` suite. The derivation still works on the candidate: the integration build gives rc 0.
    - `scripts/suite_shards.py` gained a `milan_dp_gm_steps` landmark. `scripts/measure_test_evidence_readers.py` gained the `phc_step.py`, `gmstep_mutants.py` and `lock_mutants.py` dispositions. Neither touches the MAAP suite.
  - **Docs tables and registries.**
    - The PR changes no row of `docs/testing/TESTING.md` or `tb/verilator/README.md`. Dev's edits there are the gm-steps split only.
    - `docs/traceability/MODULE_MATRIX.md` is generated, and `gen_module_matrix.py --check` passes.
    - `docs/findings/README.md` is changed by the PR only.
  - **Record citations.** I searched for every `50,267`, `50,013`, `+0.299` and `0.233 ns` citation in the tree. Only `MARK_II_AREA_PLAN.md:1095-1096,1111` are new, unqualified references to the record in the composed tree. Every other citation is in PR-source text that the source reviews already judged.

## 3. Findings of this round

### R558-11-F1 - MINOR - Docs - `docs/design/MARK_II_AREA_PLAN.md:1088`, `:1095-1096` - after the merge, M5's 50,267-LUT base route is said to equal the `route-1x1` record, which is now #696's

- **Authority/evidence:**
  - At the candidate, `syn/ooc/pp_resource_baseline.json` records `route-1x1` as follows: LUT 50013, FF 54306, SLICE 15753, WNS 0.233, WHS 0.017. Its `measured` note names #696's lane head `bee1b0d7`.
  - The same page states this twice:
    - `:110`: "the gate's current record, #696's first-draw re-baseline";
    - `:657`: "now at 50,013 LUTs ... that record is the comparison anchor".
  - Dev's M5 section (`c20c85bd`, PR #722) tabulates "Base route at dev `e8454e27` | 50,267 | 54,413 | 15,779 | 74 / 27 | +0.299 / +0.031" at `:1088`. It then states:
    - `:1095`: "The base route equals the `route-1x1` record in every gated figure."
    - `:1096`: "Against that record, the M5 route passes with no failing endpoint."
  - At dev `c6bd08c6` that sentence was true. The PR head `aa980479` has no M5 section. So neither source carries the defect, and the merge alone makes `:1095` false: LUT, FF, slice, WNS and WHS all differ from the current record.
  - The same composed page already names the record correctly for the sibling sections: M2 at `:696-697` and M6 at `:948`, which read "#645/#647's `route-1x1` record ... #696's 50,013-LUT re-record has since replaced it".
  - Within one page, the record that M2 and M6 compare against and the record that M5 compares against therefore read as two different records, although all three base rows are identical.
  - `scripts/check_plan_composition.py` (`receipts/plan_composition.log`) lists the unqualified references at `:1095`, `:1096` and `:1111`.
- **Why MINOR and not RESIDUE:**
  - `:1095` states the identity and figures of the gate record ("equals the `route-1x1` record in every gated figure"), and that statement is false of the current record.
  - This is the class that R558-9-F1 (MINOR, M2/M6) and R558-5-F1 (MINOR, M0s) on this PR established. Both were fixed with the record named.
  - The manager's acceptance criterion for this round is "no sentence implying the current route-1x1 record is 50,267", and this sentence does exactly that.
- **Impact:**
  - The merged authoritative plan names two different records as "the `route-1x1` record".
  - D7 lanes take their comparison anchor from these intermediate-measurement sections. A later lane modelled on M5, the newest section, would anchor on 50,267, which is no longer the gate's record.
  - No gate detects it: all 38 documentation, static and record gates pass on the candidate.
- **No measurement or verdict is wrong.** Against #696's record, the M5 route stays within every tolerance and floor (`receipts/plan_composition.log`):
  - LUT -436 (tolerance 500), FF -80 (600), slices +38 (80);
  - RAMB36/RAMB18 equal;
  - WNS falls 0.136 ns (limit 0.25) to +0.097 (floor 0.030); WHS rises.
- **Required outcome:** at the merged head, `:1095-1096` name the record the M5 base row was compared against: #645/#647's `route-1x1` record, the gate record at dev `e8454e27`. They either say that #696's record has since replaced it or name both, and nothing implies that the current `route-1x1` record is 50,267. One fix that keeps every figure, in the PR's own wording for M2:
  - `:1095`: "The base route equals #645/#647's `route-1x1` record, the gate record at dev `e8454e27`, in every gated figure; [#696](https://github.com/kebag-logic/milan-fpga/issues/696)'s 50,013-LUT re-record has since replaced it."
  - `:1096`: "Against that record, the M5 route passes with no failing endpoint; it also passes against #696's record."
- **Verification:**
  - `python3 -I scripts/check_plan_composition.py <checkout>` must show no unqualified `:1095` reference. `receipts/f1_fix_probe.log` shows this wording applied in a scratch copy, with `docs_check.py`, `check_em_dash.py --base c6bd08c6`, `gen_toc.py --verify-anchors` / `--check` and `check_doc_style.py` all rc 0. The copy was then restored.
  - `pp_resource_gate.py check-baseline` must still pass.

### R558-11-R1 - RESIDUE - Docs - `docs/design/MARK_II_AREA_PLAN.md:1111` - M5's lane-scoped "The gate record stays unchanged under D7." now sits beside #696's re-record

- The sentence is true of M5, and the paragraph makes M5 its subject. On the composed page, though, the gate record did change, through #696.
- It is wording only: it states no figure or record identity and changes no verdict. It is the same class as R558-9-R1, which the PR resolved for M2 and M6 with this exact pattern.
- **Exact fix:** `:1111` "M5 does not re-record the gate under D7."

No BLOCKER or MAJOR.

### What the manager asked to confirm

- **Each record named where it is the comparison anchor:** M0s `:656-657`, M2 `:696-697` and M6 `:948` do. M5 `:1095-1096` does not (F1).
- **The partial-central figure is computed from the rows:**
  - The arithmetic is `37,957` (`:1052`, Partial F5-unqualified, Central) + (200 - 34) + (600 - 121) + (600 - 418) = 38,784.
  - 38,784 - 38,040 = 744, matching `:1110` exactly (`receipts/plan_composition.log`).
  - It is consistent with `:113`: the levers and ledger keep the baseline's route figures.
- **No sentence implying the current route-1x1 record is 50,267:** violated only at `:1095` (F1).
- **Every gate reading the plan passes on the candidate:** yes, see section 4.
- **Nothing else interacts:** see section 2.

## 4. Executed evidence on the candidate (this round)

Every run used a scratch git checkout of `1ceada05` with the three submodules at their gitlinks. The receipts are in `receipts/`.

- **Toolchain** (`receipts/toolchain.txt`):
  - Verilator 5.050 through the scoped wrapper (`Verilator 5.050 2026-07-01 rev v5.050`; binary sha256 `fb2cc573...`), and GNU make 4.4.1.
  - Host python3 3.14.7, with pyyaml.
  - The pinned Markdown renderer is a pre-existing private environment. Its `pip freeze` equals `tools/markdown/requirements.txt`: cmarkgfm 2025.10.22, html5lib 1.1, cffi 2.1.1, pycparser 3.0, six 1.17.0, webencodings 0.6.1.
- **MAAP target** `make -C tb/verilator/maap all VERILATOR_JOBS=4`, rc 0 (`c_maap_all.log`, `.rc`):
  - unit `KL_maap: 186 checks, 0 failures`;
  - campaign `checks: 65 failures: 0`: the unit clean control and the real-datapath clean control `m4_datapath_clean` pass, and 63 planted defects fail their named checks;
  - the five datapath plants (`m4_reset_time_sampling`, `m5_datapath_ignores_link`, `m3_datapath_ignores_clock`, `m4_datapath_first_offset_ignores_seed`, `m3_datapath_first_offset_ignores_clock`) are each rejected by name on the composed `milan_datapath`.
- **MAAP real-datapath arm alone** (`c_maap_integration_build.log`, `c_maap_integration_run.log`): build rc 0; `MAAP integration: 5 checks, 0 failures`, run rc 0.
  - The arm elaborates the composed `milan_datapath`, with M5's `milan_csr` and the #621 gPTP pin, from `milan_dp`'s derived source list.
- **Datapath suite** `make -C tb/verilator/milan_dp run VERILATOR_JOBS=4`, rc 0, 31 min (`c_milan_dp.log`, `.rc`):
  - 11,955 checks, 0 failures: gptp 182, gptp-lat 182, 1x1 236, notify 421, crflic 417, dynmap 162, nxn 1,967, divergent 1,969, nxn8 3,751, nxn4c 1,967, nolpf 236, prune 33 (MAAP_P = 0), ax1x1 233, aclk 193, and the render-law controls 6/6.
  - The crflic leg has KL_maap probing, reaching ANNOUNCE and opening the DA gate (log `:6682-6704`). The nxn legs check "MAAP unclaimed/off" talker holds (`:9132-9134` and others).
  - The `gmstep` leg is no longer in this suite (#621).
- **GM-steps suite** `make -C tb/verilator/milan_dp_gm_steps run`, rc 0 (`c_gm_steps.log`, `.rc`):
  - `gmstep: checks: 190 failures: 0`;
  - controls `6 checks: 6 PASS, 0 FAIL` (clean control plus five acceptance controls).
  - This is dev's new suite, running for the first time on a datapath carrying the PR's PHC-seeded `KL_maap`.
- **Documentation, registry and record gates** (`scripts/run_doc_gates.sh`; `receipts/doc_gates/`, `receipts/doc_gates2/`, `receipts/doc_gates_union.tsv`): 38 commands, all rc 0 under an interpreter that has the module they need.
  - The em-dash gate passes against both bases:
    - `check_em_dash.py --base c6bd08c6`: 0 findings over 344 added lines in 7 pages;
    - `--base 09c7231e`: 0 findings over 690 added lines in 25 pages.
  - Documentation and generated pages: `docs_check.py`, `check_doc_style.py` (also `--selftest`), `check_gptp_docs.py` (also `--with-submodule`), `DOC_MAP.gen.py --check`, `check_solution_docs.py`, `check_submodule_docs.py`, `check_diagram_pngs.py`, `check_feature_status.py --self-test`, `gen_module_matrix.py --check`, `check_doc_paths.py` and `check_archive.py`.
  - TOC: `gen_toc.py --selftest`, `--verify-anchors` (487 links) and `--check` (144 pages).
  - Registries and scope: `check_baremetal_only.py --check`, `check_rtl_source_lists.py`, `ci_events.py --check` / `--selftest`, `check_sweep_shape.py --self-test`, `suite_shards.py --selftest` and `check_wire_accountability.py --self-test`.
  - Code-quality scans: `measure_naming.py --check`, `check_port_contracts.py`, `measure_fail_fast.py --check`, `check_todo_ownership.py`, `measure_test_evidence.py --check` / `--selftest`, `check_hygiene.py --check`, and `check_{sv,cpp,py,sh}_idiom.py`.
  - Record and lint: `pp_resource_gate.py check-baseline` gives "baseline PASS: 3 endpoints"; `lint_rtl.py --check` passes.
  - Every non-zero entry in either run is an environment refusal (`receipts/doc_gates_env_refusals.txt`). The first run had no html5lib and the submodules were not yet registered in the scratch checkout. The second run, in the renderer environment, had no pyyaml. Every command passes in the run that has its dependency.
- **Plan composition check** (`scripts/check_plan_composition.py`, `receipts/plan_composition.log`, rc 0):
  - inventory: 22 rows and 66 figures equal the recorded `route-1x1` / `ooc-1x1` / `ooc-8x8` scopes, with 0 differences;
  - partial-central: 38,784 / 744 reproduced;
  - M5 route against the current record: PASS on every tabled figure;
  - unqualified record references listed.
- **F1 wording probe** (`scripts/probe_f1_fix.py`, `receipts/f1_fix_probe.log`): see F1's verification. The scratch copy was restored to HEAD with 0 tracked changes.
- **Clone integrity** (`receipts/head_integrity.txt`):
  - the review clone is at `1ceada05` with tree `4650fd5d`, and the index tree is `4650fd5d`;
  - porcelain status is empty, and both worktree-to-index and index-to-HEAD are clean;
  - the submodules `gptp-processor` `7dda9c3b`, `protocol-processor` `2ad2f845` and `third_party/verilog-axis` `48ff7a7e` equal their gitlinks and are clean.
  - No probe touched the review clone. All builds and probes ran in scratch checkouts.

## 5. Lens results (artifact-specific)

```text
[R558] PASS Conformance - hdl/ieee1722/maap/KL_maap.sv and hdl/milan/milan_datapath.sv:7184-7185 at 1ceada05 (patch-ids equal to aa980479); receipts/c_maap_all.log (186/0, campaign 65/0), receipts/c_maap_integration_run.log (5/0) - the Annex B behaviour reviewed at the source is carried byte-for-byte, and its unit, campaign and real-datapath checks pass on the composed datapath with M5's CSR block and the #621 gPTP pin
[R558] PASS RTL - the composed milan_datapath (PR's KL_maap + port_operational_i/realtime_ns_i wiring, dev's milan_csr.sv M5 read path, gptp-processor 7dda9c3b); receipts/c_milan_dp.log (11,955/0, rc 0), receipts/c_gm_steps.log (190/0, 6/6), receipts/c_maap_integration_build.log, receipts/doc_gates2 lint_rtl --check - no textual RTL overlap, the merge is mechanical, and every datapath elaboration and leg passes, including MAAP_P=0 prune
[R558] PASS Robustness - tb/verilator/maap/mutants.py campaign on the candidate (m5_restart_on_link_loss, the m5/m3/m4 datapath link/clock/seed plants, the M8 truncation plants m8_early_last_accepted and m8_missing_bytes_accepted); receipts/c_maap_all.log - link-loss, link-return, clock and seed paths through the composed eff_link_w / ptp_now_w wiring are rejected by name; the dev side changes neither signal's driver in milan_datapath.sv
[R558] PASS Tests - tb/verilator/maap/{Makefile,integration.mk,mutants.py,sim_main.cpp,sim_integration.cpp} against dev's tb/verilator/milan_dp/Makefile (print-srcs/print-dp-vflags) and the new milan_dp_gm_steps suite; scripts/suite_shards.py --selftest, check_sweep_shape.py --self-test, measure_test_evidence.py --check/--selftest; receipts/c_maap_all.log, receipts/doc_gates_union.tsv - the integration arm's derived source list still resolves after #621's Makefile split, every plant fails its named check, and the suite inventory gates pass
[R558] MINOR Docs - docs/design/MARK_II_AREA_PLAN.md:1095-1096 - R558-11-F1 (open); R558-11-R1 RESIDUE at :1111. Otherwise clean: :56, :110-147, :656-657, :696-707, :948-969, :1110 partial-central, docs gates 38/38, check-baseline PASS
```

## 6. Prior public findings on this PR, at this head (read after my own pass and draft verdict)

| Finding | State at `1ceada05` | Evidence |
|---|---|---|
| R558-9-F1 (MINOR, Docs; M2 `:695-696`, M6 `:947` at `eb86b843`) | **Still resolved** at `:696-697` and `:948` | `receipts/plan_composition.log`. F1 here is the same class, newly introduced by M5's section |
| R558-9-R1 (RESIDUE; M2/M6 "gate record stays unchanged") | **Still resolved** at `:707` and `:969` | R558-11-R1 is the M5 analogue |
| R558-5-F1 (MINOR, Docs; M0s anchor) | **Still resolved** | `MARK_II_AREA_PLAN.md:656-657` and `AREA_BUDGET.md:379` name #696's 50,013 record |
| R558-6-F1, R558-7-F1, R559-6-F1/F2 (MINOR; first draw, every-seed checks, echo check) | **Still resolved** | `KL_maap.sv`, `sim_main.cpp`, `mutants.py` and `MAAP_FABRIC.md` are carried unchanged (same patch-id). The campaign rejects every plant by name (`c_maap_all.log`) |
| R558-3-F1 = R559-3-F1 (BLOCKER; `integration.mk` capture) | **Still resolved** | Unchanged file. The derived source list builds against dev's #621 `milan_dp/Makefile`; 5/0 |
| R558-1-F1, R559-1-F1/F2/F3 (MINOR) | **Still resolved** | Inventory 66/66 equal to the record. The M5 loss check passes in the campaign |
| R558-2-R1 / R559-2-R1 (RESIDUE) | **Retained** | Still applies at `MARK_II_AREA_PLAN.md:66-67`, `:317` and `:1125` (the former `:1086`, shifted 39 lines by M5's section). Wording only |
| R558-5-R1 (RESIDUE) | **Retained** | `AREA_BUDGET.md:370`, `:387` and `MARK_II_AREA_PLAN.md:669` are unchanged |
| R558-10-R1 / R559-7-R1 (RESIDUE, PR body; supersedes R558-4-R1) | **Retained** | The PR body still says "review ready at `32582421...`" (`:16`), `# 32582421...` (`:175`) and "Hosted checks and the local workflow replica need the pushed head." (`:252`) |
| R558-8-S1, R559-7-S1, R558-7-S2, R559-6-S2/S3, R558-6-S1/S2, R559-5-S1, R558-3-S1/S2, R559-3-S1, R558-4-S1/S2, R559-4-S1/S2, R559-1-S1..S4 (SUGGESTION) | **Retained, optional, no lens effect** | Their sources are unchanged by the composition |

The source-positive reviews R558-10 and R559-8 raise no new MINOR or higher.

## 7. Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Composed `KL_maap` / datapath wiring; MAAP unit, campaign and real-datapath arm on the candidate. Source conformance: R558-10, R559-8 | R558-11 (composition); R558-10, R559-8 (source) | `1ceada05ff6384af12233eac8ea405b3bdfc6fae`; source `aa980479aafd1d72c72015707fa6618b5aa47cb1` |
| RTL | CLEAN | Composed `milan_datapath` with M5 `milan_csr` and gPTP `7dda9c3b`; `milan_dp` (11,955/0), `milan_dp_gm_steps` (190/0, 6/6), integration build; lint | R558-11 | `1ceada05ff6384af12233eac8ea405b3bdfc6fae` |
| Robustness | CLEAN | Link-loss/return, clock and seed plants through the composed wiring; M8 truncation plants | R558-11 (composition); R558-10, R559-8 (source) | `1ceada05ff6384af12233eac8ea405b3bdfc6fae`; source `aa980479aafd1d72c72015707fa6618b5aa47cb1` |
| Tests | CLEAN (SUGGESTIONs retained) | MAAP harnesses and campaign on the candidate; `integration.mk` derivation against #621's `milan_dp/Makefile`; suite-shard, sweep-shape and test-evidence gates | R558-11 | `1ceada05ff6384af12233eac8ea405b3bdfc6fae` |
| Docs | **UNCLEAN** (R558-11-F1 open; RESIDUE R558-11-R1, R558-2-R1 / R559-2-R1, R558-5-R1, R558-10-R1 / R559-7-R1 retained) | `MARK_II_AREA_PLAN.md` both sides and the record sweep; `AREA_BUDGET.md`; findings index; record file; 38 documentation, registry and record gates | R558-11 | `1ceada05ff6384af12233eac8ea405b3bdfc6fae` |

Docs becomes clean only at a head that resolves F1 and is re-reviewed. A fix commit touching only `MARK_II_AREA_PLAN.md` leaves Conformance, RTL, Robustness and Tests covered at that head, because no artifact in their scope changes. That must be confirmed against the new head's diff.

## 8. Real limits

- **Not run:** the full parent sweep, PP/gPTP/Yosys/builder banks, the firmware differential (no firmware or `ctrl` file changed on the dev side), Vivado, act/hosted, hardware and bench.
- **Not rerun at the composition:** `KL_maap` line coverage. Its inputs, `KL_maap.sv` and `sim_main.cpp`, are PR-only and byte-equal to the source.
- **No wiring-drop probes this round.** Dev changes no line of `milan_datapath.sv`, so the merge cannot drop a MAAP connection. The datapath plants in the campaign still reject link, clock and seed defects by name.
- **The route record does not describe the candidate image.** The `route-1x1` record's inputs are #696's `bee1b0d7` (dev `e8454e27`). The candidate also carries M5's `milan_csr.sv` and the #621 gPTP pin. I did not measure the route, which needs Vivado.
- **Physical calibration NOT RUN.** Field-campaign skips are not hardware proof.
- **Invalid first attempt, not evidence.** An attempt from an archive extraction without git metadata stopped at `pp_srcs.py`'s `git ls-files` refusal before any simulation. Its logs are in `receipts/` (`maap_all.log`, `gm_steps.log`, `milan_dp.log`) but are not in the manifest.
- **Redaction.** Host home-directory paths of the Verilator root in the published logs are replaced with `<pinned-verilator-root>`. Nothing else in the logs was edited.

## 9. Pending manager duties

- **F1 resolution.** It needs a new PR commit, for example a dev merge plus the wording fix. A re-review of that head must confirm F1 (and R1) and the unchanged other lenses.
- **AREA_BUDGET.md:516-525 merge-bank rule.** The dev delta since the record's measured revision touches RTL (`milan_csr.sv`) and the gPTP pin, so the bank runs the route comparison on the merge candidate. D7 keeps the record for M5. Whether the #621 pin movement needs attribution is for the manager's merge bank.
- **Candidate banks** (`$VALIDATION_STORAGE/696-candidate-0923`), act and hosted acceptance at the exact candidate head.
- **Residue checklist.** Carry R558-11-R1, R558-2-R1 / R559-2-R1, R558-5-R1 and R558-10-R1 / R559-7-R1.
- **Bench interop (acceptance 4)** stays with the post-merge bench lane.

## 10. Packet

`REPORT.md`, `scripts/` (`run_doc_gates.sh`, `check_plan_composition.py`, `probe_f1_fix.py`), and `receipts/` as listed in `MANIFEST.sha256`. Scratch checkouts under `scratch/` are not published.

R558-11 FINISHED
