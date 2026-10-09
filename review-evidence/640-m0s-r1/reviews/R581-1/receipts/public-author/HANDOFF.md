[A581]

Relates to #640.

# Handoff

**Disposition: STOP for the selected route; authorized tooling step complete.**
The assignment explicitly permits step 2 when integration is absent.
No implementation route or new resource measurement was performed.

Branch: `640-m0s`.
Base: `7c1b52bee26b497080ee22b1c1986109f80a5ee7`.
Head: `bc89f84e6757f8fcddf21958e99f40f17bc0ee1e`.
Tree: `b498495714ea3ca8e3ab8e38781cc7ff54b68967`.
Commit: `Support selected placement resource measurements for M0s`.
The commit has one subject, no body or trailers, using the configured identity.
The worktree and all three initialized public dependencies are clean.

Executor: [A581]. Internal reviewer: [R580]. External reviewer: [R581].
Independent review and review-lens coverage remain pending.
No executor verdict counts as approval.

## Assignment and authority

Assignment: #640, comment 6086604096.
Takeover comment: #640, comment 6086625198.
The parent remains Backlog; the explicit lane assignment authorizes this step.
The requirements, approved #664 text, #665 foundations, complete Mark II plan,
area budget and measurement recipes were read before implementation.
The remote was verified against the repository URL supplied in the assignment.
The initial clean HEAD matched the specified base.

## Integration STOP

| Evidence at the assigned base | Missing behavior |
|---|---|
| `sw/litex/milan_soc.py:2505` | The mailbox class explicitly leaves its datapath disconnected |
| `sw/litex/milan_soc.py:2549` | Link, GM and RX inputs are idle; outgoing packets are discarded |
| `sw/litex/milan_soc.py:3612` | The switch adds a mailbox skeleton, without selecting protocol ownership |
| `hdl/milan/milan_datapath.sv:8003` | The processor wrapper is instantiated unconditionally |
| `hdl/milan/milan_datapath.sv:7167` | MAAP pruning alone supplies no replacement firmware owner |
| `sw/firmware/milan_baremetal/Makefile:6` | The shipping library retains its existing entry object |
| `sw/firmware/ctrl/maap/README.md:85` | Placement integration and the shipping entry point remain outside that foundation |

Parent integration must connect mailbox ingress, egress and events, remove
ADP, ACMP, MAAP and SRP from fabric, invoke the F0-F4 application, and retain
AECP, media controls, counters and coherent saved-state ownership. Firmware
source presence alone is insufficient. This lane changes none of that RTL.

## Changes

Every path and line below belongs to the committed head above.

| File:line | Change and purpose |
|---|---|
| `syn/ooc/pp_baseline.py:22` | Preserve absolute-file imports used by checkpoint-report recipes. |
| `syn/ooc/pp_baseline.py:154` | Omit only removed protocols' absent ROM bindings; retain geometry checks for present bindings. |
| `syn/ooc/pp_baseline.py:259` | Generate selected integrated measurements; validate population before implementation and after it. |
| `syn/ooc/pp_baseline.py:580` | Expose explicit selection while preserving default all-fabric and standalone behavior. |
| `syn/ooc/pp_placement.py:14` | Define the three selections and expected one-interface engine populations. |
| `syn/ooc/pp_placement.py:51` | Require recipe/selection agreement and complete, unique, valid census rows. |
| `syn/ooc/pp_placement.py:88` | Query retained module identities and emit their measured counts; report image-internal timing. |
| `syn/ooc/pp_resource_gate.py:169` | Accept wrapper-free source provenance through the datapath; preserve legacy normalization. |
| `syn/ooc/pp_resource_gate.py:191` | Bind split selection into input identity without changing the record shape. |
| `syn/ooc/pp_resource_gate.py:250` | Measure selected image hierarchy without a wrapper; avoid false cross-root removal deltas. |
| `syn/ooc/pp_resource_gate.py:278` | Validate selected census before reading the candidate resources. |
| `syn/ooc/pp_resource_gate.py:698` | Compare selected routes under existing policy; refuse intermediate acceptance writes. |
| `syn/ooc/pp_placement_selftest.py:55` | Execute both Tcl census stages against independent populations, reversing every required presence/absence. |
| `syn/ooc/pp_placement_selftest.py:73` | Exercise real recipe preparation, retained ROM checks, worker identity and filename imports. |
| `syn/ooc/pp_placement_selftest.py:156` | Judge wrapper-free partial/full fixtures and plant metadata, resource, route and identity defects. |
| `syn/ooc/pp_baseline_mutants.py:13` | Extend recipe enforcement-removal controls; retain all existing detectors. |
| `syn/ooc/pp_resource_gate_mutants.py:283` | Add six placement enforcement removals; adapt existing mutation locations without dropping controls. |
| `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:183` | Document selected recipes, census limits, unchanged comparisons and the integration STOP. |
| `docs/design/MARK_II_AREA_PLAN.md:634` | Record intermediate STOP, missing figures, parent integration work and unchanged memory obligations. |
| `docs/design/AREA_BUDGET.md:358` | Record missing selected measurement and preserve the accepted route and reserve. |

The added census is an observation report, not a changed acceptance schema.
The existing acceptance record shape and all policy values remain unchanged.
No workflow, threshold, RTL, firmware behavior or shipping default changed.
No source or generated artifact outside the assigned scope changed.

## Tests and planted defects

| Test entry | Planted defect and observation |
|---|---|
| `pp_placement_selftest.py:55` | Every role reversed independently under both Tcl census stages; the intended placement/role must be named |
| `pp_placement_selftest.py:73` | Missing retained AECP/gPTP ROM, invalid endpoint, lost worker cap, missing ROM promotion, wrapper-only timing, or broken absolute-file import must fail |
| `pp_placement_selftest.py:156` | Absent/duplicate/wrong recipe selection, mislabelled census, missing header/role/file, duplicate role, invalid count and wrong retained population must exit 2 by name |
| Same selected fixtures | Extra LUT/RAMB36, exceeded tile ceiling, negative hold slack and incomplete routing must exit 1; changed implementation identity must exit 2 |
| Same selected fixtures | Removing the wrapper source and hierarchy must still permit a valid split comparison; all-fabric must refuse that population |
| Same selected fixtures | A requested acceptance write must fail without altering the baseline; scope-root changes cannot count as removal savings |
| Recipe mutation campaign | Positive control passes; all 41 individual enforcement removals fail |
| Resource mutation campaign | Positive control passes; all 180 individual enforcement removals fail, including six placement guards |
| Existing resource self-test | 260 existing arms and 500 seeded generated cases remain green |
| Existing OOC recipes | All 58 pre-synthesis refusal arms remain green |
| Added-line documentation gate | All 339 planted controls pass; zero findings over 165 added Markdown lines |

These are synthetic, executable controls. They establish measurement-tooling
behavior, not integrated firmware ownership or a completed implementation run.
Expected nonzero child verdicts in negative tests are caught by their harness;
every final gate command below exits zero.

## Coverage table

This table records executor evidence only. It banks no independent review lens.

| Lens | Evidence at the head above | Independent covering round/head |
|---|---|---|
| Conformance | Assignment step-1 prerequisite checked; only step 2 completed; unchanged D7 record/policy and reserve | Pending [R580]/[R581] |
| RTL | No RTL or dependency-pin delta; unconditional wrapper and idle mailbox establish route STOP; lint remains green | Pending [R580]/[R581] |
| Robustness | Named placement, census, ROM, route, identity, primitive and malformed-input refusals | Pending [R580]/[R581] |
| Tests | 41 recipe mutations, 180 resource mutations, 58 OOC controls, retained 260 arms and 500 seeded cases | Pending [R580]/[R581] |
| Docs | Recipe and both ledgers reflect the STOP and proof limits; documentation and generated Contents gates pass | Pending [R580]/[R581] |

## Gate table

**28 commands, all final rc 0.** No gate output was piped.
Logs are retained under the assigned external scratch directory, denoted `WORK`.
`RECEIPTS.tsv` binds each raw log's exact size and SHA-256.
The checks ran against the committed file contents; the added-line gate and
integrity check additionally ran after commit. The OOC source set is unchanged.

Use the pinned environments, including the assigned lint executable.
The interpreter used here supports `-X cpu_count=4`; its reported count was 4.
No campaign exceeded four workers; no RTL simulation build was launched.
The existing OOC refusal suite completed in 449.72 seconds.

```sh
export TMPDIR="$WORK"
export PYTHONDONTWRITEBYTECODE=1
export VERILATOR_JOBS=2
BASE="$(git rev-parse HEAD^)"
```

| Command | rc | Raw evidence under WORK | Defect class detected |
|---|---:|---|---|
| `python3 syn/ooc/pp_baseline.py --selftest` | 0 | `recipe.log` | Malformed/missing ROMs, wrong parameter block, wrong placement, removed checks, wrong worker setting, broken absolute-file import |
| `python3 syn/ooc/pp_baseline_mutants.py` | 0 | `recipe-mutants.log` | 41 single enforcement removals; control passes and each removal fails |
| `python3 syn/ooc/pp_resource_gate.py --selftest` | 0 | `resource.log` | 260 existing arms and 500 seeded cases; selected census, ROM-independent source provenance, identity, resources, timing and route plants |
| `python3 syn/ooc/pp_resource_gate.py check-baseline` | 0 | `baseline.log` | Policy table drift, malformed acceptance record or a record that violates its policy |
| `python3 syn/ooc/pp_baseline_reports_selftest.py` | 0 | `reports.log` | Missing hierarchy child, double-counted shared LUTs, blackbox contents and wrong residual attribution |
| `python3 scripts/pp_srcs.py --check --selftest` | 0 | `sources.log` | Hand-maintained or stale processor source populations; planted source-list controls |
| `python3 scripts/docs_check.py` | 0 | `docs.log` | Broken documentation links, forbidden wording and privacy leaks |
| `python3 scripts/check_doc_style.py` | 0 | `style.log` | Documentation style violations |
| `python3 scripts/check_doc_paths.py` | 0 | `paths.log` | Nonportable documentation paths |
| `python3 scripts/check_solution_docs.py` | 0 | `solutions.log` | Missing or inconsistent solution documentation |
| `python3 scripts/check_archive.py` | 0 | `archive.log` | Historical/current documentation boundary drift |
| `python3 scripts/gen_toc.py --check` | 0 | `toc.log` | Generated Contents drift |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 | `anchors.log` | Generated anchors diverging from renderer rules |
| `python3 scripts/check_feature_status.py` | 0 | `status.log` | Documentation status claims disagreeing with the authoritative ledger |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 | `traceability.log` | Generated module/requirement/test matrix drift |
| `python3 scripts/check_py_idiom.py` | 0 | `py-idiom.log` | New annotation, public-docstring, function/module-size or Python idiom debt |
| `python3 scripts/check_hygiene.py --check` | 0 | `hygiene.log` | Whitespace, newline and tracked text hygiene regressions |
| `python3 scripts/check_todo_ownership.py` | 0 | `todo.log` | Unowned work markers |
| `python3 scripts/measure_naming.py --check` | 0 | `naming.log` | New unqualified-unit naming debt |
| `python3 scripts/measure_fail_fast.py --check` | 0 | `fail-fast.log` | New paths masking failed operations |
| `python3 scripts/measure_test_evidence.py --check` | 0 | `test-evidence.log` | Loss of executable negative controls or seed accounting |
| `python3 scripts/ci_events.py --check` | 0 | `ci-events.log` | Workflow event/command contract drift |
| `python3 scripts/ci_scope.py --selftest` | 0 | `ci-scope.log` | Planted classifier changes that suppress required validation |
| `git diff --check "$BASE" HEAD` | 0 | `diff.log` | Whitespace errors in the complete committed delta |
| `python3 syn/ooc/ooc_tcl_selftest.py` | 0 | `ooc.log` | 58 pre-synthesis refusal arms: missing/stale/truncated images, wrong generics, geometry, source order and diagnostics |
| `python3 scripts/lint_rtl.py --check --self-test` | 0 | `lint.log` | New lint violations or incomplete pinned source populations; self-test controls |
| `python3 -X cpu_count=4 syn/ooc/pp_resource_gate_mutants.py` | 0 | `gate-mutants.log` | 180 enforcement removals; six target placement census guards |
| `python3 scripts/check_em_dash.py --base "$BASE"` | 0 | `em-dash.log` | Forbidden added characters and false generated-label exemptions; 339 planted arms |

The whole RTL simulation/portability bank, hosted checks, physical qualification,
candidate merge validation and containment are not claimed. They remain later
review/merge obligations. This assignment prohibited pushing and PR operations.
No hosted run was inspected or used as local evidence.

## Accepted record and measurement ledger

The accepted baseline is byte-identical to the base:
`cf2eec5ce8e41d50f5308264a8608d7341ba142d6d3a04058e5572e1a8a29e41`, 27995 bytes.
No actual resource record was created or replaced.
Fixture-local writes exercise existing refusal behavior only.

| Endpoint | LUT | FF | Slices | RAMB36 / RAMB18 | WNS / WHS ns | Provenance |
|---|---:|---:|---:|---|---|---|
| Accepted all-fabric route | 50,267 | 54,413 | 15,779 | 74 / 27 | +0.299 / +0.031 | Existing record, unchanged |
| Accepted standalone 1x1 | 23,179 | 19,779 | Not recorded | 16 / 3 | -3.562 / +0.159 | Existing synthesis reference |
| Accepted standalone 8x8 | 30,135 | 27,380 | Not recorded | 21 / 5 | -2.278 / +0.159 | Existing synthesis reference |
| M0s F0-F4 route | Not measured | Not measured | Not measured | Not measured | Not measured | STOP: missing integration |

The baseline anchors above are not measurements of this lane.
No delta from a selected image can be calculated.
Firmware text, rodata, data, BSS, stack, pools, staging, usable RAM and actual
primitive allocation remain unmeasured for an integrated selected image.
About 50 firmware tiles is a budget only; the complete allocation includes
reused CPU memory, and partial placement retains AECP and used wrapper stores.
The 121.5-tile ceiling preserves 13.5 tiles, the 10 percent reserve.
The later route must reconcile actual counts without borrowing full-split credits.

## Environment and artifact integrity

The recorded service memory peak was 2,285,273,088 bytes, below 9 GB.
No memory-limit or out-of-memory event occurred.
Disk space remained above the 30 GB floor; the final observation had 83 GiB free.
No synthesis or route, hardware access, flashing, push, PR operation,
merge, rebase or delegated work was used. No existing public comment was edited.
No route was started, so no implementation lock was taken.
Every output artifact is smaller than 200 KB. Environments, packages and
scratch/generated trees remain outside the output directory and repository.
All long-running work has completed before the final public comment.

## Remaining work

1. Independent review of this exact tooling head by the assigned reviewers.
2. Parent integration to connect the datapath and establish selected ownership.
3. Repeat placement qualification; only then run the selected route exclusively.
4. Publish actual image figures, accepted-record comparison and memory reconciliation.
5. Follow the existing later checkpoint and M9 obligations; no acceptance re-record here.

The final issue disposition is STOP, carrying the committed head.
It reports completed step-2 support and the unchanged route prerequisite.
