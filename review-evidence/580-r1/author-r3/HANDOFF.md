# [A372] Merge with dev handoff

Status: local merge and assigned validation complete. All 40 gate invocations returned rc 0 at the recorded head. Worktree clean; REVIEW READY posted; executor round stopped.

Assignment: https://github.com/kebag-logic/milan-fpga/issues/580#issuecomment-5857846388
Issue: #580. PR: #591. Executor: [A372]. Independent review remains required.
Branch: `580-pp-pin-16be6768`.
Physical worktree: `$LANES/580-pp-pin-16be6768`.
Origin: `https://github.com/kebag-logic/milan-fpga.git` (verified).
Starting head: `d02db63c367daf9adc7d709840bd81077e781d80` (verified).
Required dev: `2a2a7bb655e528edc3087c88033cd3a47546feb4` (fetched and verified).
Required processor gitlink: `16be6768f710e79450aace277abacd6c2c3336e5` (gitlink and checkout verified).
Before any processor Git inspection, its top-level resolved to the physical submodule directory.

## Scope and stop conditions

Merge dev with subject `Merge dev into 580-pp-pin-16be6768`, no body or trailers.
Resolve only `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` per the assignment:
retain the original-measurements framing, F1-F4 enforcement and historical audit
pin distinction; use dev F1-F4 follow-up rows, lane F5 disposition, unchanged F6-F8.
Keep every fact from both sides and add no new claim.
Report other disagreements rather than rewriting them unless caused by the merge.
Stop for any other conflicted file or a failed capture-receipt check.
No push, PR change, merge to dev, rebase, additional checkout, firmware or RTL edit.

## Merge identity

Merge head: `01e18f6c4d01a545e8d927ac119187c9514dc40c`.
Merge tree: `17de168ce12a5af81ba8a0f9d795290e071e7948`.
Parents, in order: `d02db63c367daf9adc7d709840bd81077e781d80`, `2a2a7bb655e528edc3087c88033cd3a47546feb4`.
Subject verified: one line, no body or trailers.
Processor gitlink after merge: `16be6768f710e79450aace277abacd6c2c3336e5` (verified).
No change against the first parent in `hdl/`, `sw/firmware/`, the processor gitlink,
or the capture harness/receipt. The worktree is clean.

## Resolved hunks, verbatim

### Hunk 1: before (conflict as produced by Git)

```text
<<<<<<< HEAD
It records measurements at `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`.
The audit's processor pin was `990f96526bb89356c963a260ebbdcf2a77e6623a`.
=======
Original measurements were recorded at `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`.
The original processor pin was `990f96526bb89356c963a260ebbdcf2a77e6623a`.
F1-F4 enforcement now reflects the assigned parent follow-ups.
>>>>>>> origin/dev
```

### Hunk 1: after

```text
Original measurements were recorded at `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`.
The audit's processor pin was `990f96526bb89356c963a260ebbdcf2a77e6623a`.
F1-F4 enforcement now reflects the assigned parent follow-ups.
```

### Hunk 2: before (conflict as produced by Git)

```text
<<<<<<< HEAD
| F1 | Parent validity follow-up; coordinate [PP38][pp38]. Refuse zero/all-ones literal and pinned model IDs. Keep model evolution with #495. | Legal ID accepted; both endpoint values refused on both input forms; generated ENTITY/ADP equality retained. |
| F2 | Parent buffer-floor follow-up; coordinate [PP60][pp60] L4. Validate every declared listener buffer. | 2126000 accepted, 2125999 refused; all five images unchanged. |
| F3 | Parent stream-format follow-up; coordinate [PP60][pp60] L3/L4. Bound format count and validate AAF/CRF family and Milan CRF word. | Legal family controls; independently refuse 48 entries, mixed family and altered CRF word; test inputs and outputs. |
| F4 | Parent source-construction follow-up; coordinate [PP60][pp60] L6. Outputs must have INTERNAL available. | INTERNAL+CRF accepted; outputs with only CRF refused; preserve applicable input-only behavior. |
| F5 | [Processor #122][cluster-decision] retains F07.2's Milan 5.3.3.8 minimum. Parent [#584][cluster-fix] owns correcting D8's non-conforming zero-cluster 8x8 input pools. | Every input port must own at least one cluster. Product meaning, refusal tests and image changes remain #584's work; successful packing grants no waiver. |
=======
| F1 (#573) | Enforced by `B._model_id` for literal, pinned and resolved hash IDs. Evolution remains with #495 and [PP38][pp38]. | Declaration tests accept legal IDs, refuse both endpoints on both inputs, and compare packed ENTITY/ADP identity. Removing the endpoint guard fails the tests. |
| F2 (#574) | Enforced by `B._stream_buffer_ns` on every listener declaration. Coordinates [PP60][pp60] L4. | Declaration tests pack 2126000 and 0xFFFFFFFF unchanged at every listener index. They refuse 2125999, 2^32 and 2^32+2125999. Removing either bound fails. All five images remain unchanged. |
| F3 (#575) | Enforced by `B._validate_stream_formats` and `_crf_format`. Coordinates [PP60][pp60] L3/L4. | Both directions accept legal families and 46 final entries. Declaration tests independently refuse count overflow, mixed families and altered CRF words. Removed-check mutants fail. |
| F4 (#576) | Enforced by `B._validate_output_clock_sources` for every AAF/CRF output. Coordinates [PP60][pp60] L6. | Declaration tests accept INTERNAL+CRF with either selected. CRF-only outputs refuse; removed-check mutants fail. Input-only clock loading remains supported; full YAML still requires both AAF directions. |
| F5 | Processor contract follow-up under [PP60][pp60]. Reconcile F07.2's minimum with parent D8 zero-cluster input pools. | Public clause-backed disposition; do not infer a requirement waiver from successful packing. |
>>>>>>> origin/dev
```

### Hunk 2: after

```text
| F1 (#573) | Enforced by `B._model_id` for literal, pinned and resolved hash IDs. Evolution remains with #495 and [PP38][pp38]. | Declaration tests accept legal IDs, refuse both endpoints on both inputs, and compare packed ENTITY/ADP identity. Removing the endpoint guard fails the tests. |
| F2 (#574) | Enforced by `B._stream_buffer_ns` on every listener declaration. Coordinates [PP60][pp60] L4. | Declaration tests pack 2126000 and 0xFFFFFFFF unchanged at every listener index. They refuse 2125999, 2^32 and 2^32+2125999. Removing either bound fails. All five images remain unchanged. |
| F3 (#575) | Enforced by `B._validate_stream_formats` and `_crf_format`. Coordinates [PP60][pp60] L3/L4. | Both directions accept legal families and 46 final entries. Declaration tests independently refuse count overflow, mixed families and altered CRF words. Removed-check mutants fail. |
| F4 (#576) | Enforced by `B._validate_output_clock_sources` for every AAF/CRF output. Coordinates [PP60][pp60] L6. | Declaration tests accept INTERNAL+CRF with either selected. CRF-only outputs refuse; removed-check mutants fail. Input-only clock loading remains supported; full YAML still requires both AAF directions. |
| F5 | [Processor #122][cluster-decision] retains F07.2's Milan 5.3.3.8 minimum. Parent [#584][cluster-fix] owns correcting D8's non-conforming zero-cluster 8x8 input pools. | Every input port must own at least one cluster. Product meaning, refusal tests and image changes remain #584's work; successful packing grants no waiver. |
```

## Gate summary

Every gate ran in the foreground, without a pipeline, from the physical worktree.
Each command used a 3600-second timeout; no command timed out.
The complete command table and per-command receipts appear below.

| Gate group | Invocations | rc | Result |
|---|---:|---:|---|
| Documentation | 33 | 0 each | All assigned checks and self-tests passed |
| Capture receipt | 1 | 0 | Existing receipt accepted without remeasurement |
| ROM digests | 1 | 0 | Normal OOC path checked all three ledger-keyed ROMs |
| Builder declarations | 1 | 0 | F1-F4 controls, shipping rows, refusals and binding mutants passed |
| Whitespace | 4 | 0 each | Both parent comparisons, worktree and index passed |

## Findings and limitations

Reported without changing source: `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:186`
names the reachable YAML probe as 47 AAF output entries, while
`scripts/audit_pp_descriptors.py:263-264` constructs 48 entries.
Both exact lines already exist on dev `2a2a7bb6`; the merge did not create this
mismatch. The assignment directs reporting inherited disagreements, not rewriting them.
No other conflict occurred and neither mandatory stop condition was triggered.

Git emitted `warning: unable to find all commit-graph files` on some inspections.
Object identity, tree-entry comparisons and every assigned gate succeeded.
No repository metadata repair was attempted.


Capture receipt passed without remeasurement. The ROM ledger was checked, not rewritten.
Documentation checks use the existing locked environment under `/tmp`; no dependency installation was needed.
The 33-command documentation inventory is `docs-plan.json`, matching the prior round's documentation bank and the generation guide's required checks.

## Public activity

TAKEN: https://github.com/kebag-logic/milan-fpga/issues/580#issuecomment-5857856811
REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/580#issuecomment-5857908975

## Completed gate receipts

Each command used `rtk proxy timeout 3600`; stdout/stderr went directly to a regular log file, never a pipeline. Logs stay under `/tmp/580-a372`; JSON receipts record size and SHA256.

| Gate | Command | rc | Evidence |
|---|---|---:|---|
| capture-check | `python3 scripts/check_nvm_capture.py` | 0 | `capture-check.json`; 324 log bytes |
| rom-check | `syn/yosys/ooc.sh KL_chan_map_render` | 0 | `rom-check.json`; 299 log bytes |
| builder-declarations | `python3 sw/builder/test_declarations.py` | 0 | `builder-declarations.json`; 1131 log bytes |
| docs_check | `python3 scripts/docs_check.py` | 0 | `docs_check.json`; 127 log bytes |
| docs_check-selftest | `python3 scripts/docs_check.py --selftest` | 0 | `docs_check-selftest.json`; 56 log bytes |
| check_doc_style | `python3 scripts/check_doc_style.py` | 0 | `check_doc_style.json`; 47 log bytes |
| check_doc_style-selftest | `python3 scripts/check_doc_style.py --selftest` | 0 | `check_doc_style-selftest.json`; 33 log bytes |
| check_gptp_docs | `python3 scripts/check_gptp_docs.py` | 0 | `check_gptp_docs.json`; 41 log bytes |
| check_gptp_docs-selftest | `python3 scripts/check_gptp_docs.py --selftest` | 0 | `check_gptp_docs-selftest.json`; 46 log bytes |
| check_solution_docs | `python3 scripts/check_solution_docs.py` | 0 | `check_solution_docs.json`; 87 log bytes |
| check_solution_docs-selftest | `python3 scripts/check_solution_docs.py --selftest` | 0 | `check_solution_docs-selftest.json`; 59 log bytes |
| check_submodule_docs | `python3 scripts/check_submodule_docs.py` | 0 | `check_submodule_docs.json`; 47 log bytes |
| check_submodule_docs-selftest | `python3 scripts/check_submodule_docs.py --selftest` | 0 | `check_submodule_docs-selftest.json`; 66 log bytes |
| check_diagram_pngs | `python3 scripts/check_diagram_pngs.py` | 0 | `check_diagram_pngs.json`; 66 log bytes |
| check_diagram_pngs-selftest | `python3 scripts/check_diagram_pngs.py --selftest` | 0 | `check_diagram_pngs-selftest.json`; 59 log bytes |
| check_archive | `python3 scripts/check_archive.py` | 0 | `check_archive.json`; 93 log bytes |
| check_archive-selftest | `python3 scripts/check_archive.py --selftest` | 0 | `check_archive-selftest.json`; 35 log bytes |
| check_em_dash-base | `/tmp/580-a366-docs-env/bin/python3 scripts/check_em_dash.py --base 2a2a7bb655e528edc3087c88033cd3a47546feb4` | 0 | `check_em_dash-base.json`; 139 log bytes |
| check_em_dash-selftest | `/tmp/580-a366-docs-env/bin/python3 scripts/check_em_dash.py --selftest` | 0 | `check_em_dash-selftest.json`; 42 log bytes |
| doc-paths | `python3 scripts/check_doc_paths.py` | 0 | `doc-paths.json`; 84 log bytes |
| feature-status | `python3 scripts/check_feature_status.py` | 0 | `feature-status.json`; 29 log bytes |
| feature-status-selftest | `python3 scripts/check_feature_status.py --self-test` | 0 | `feature-status-selftest.json`; 1500 log bytes |
| module-matrix | `python3 docs/traceability/gen_module_matrix.py --check` | 0 | `module-matrix.json`; 118 log bytes |
| gen-hdl-reference-selftest | `/tmp/580-a366-docs-env/bin/python3 scripts/gen_hdl_reference.py --selftest` | 0 | `gen-hdl-reference-selftest.json`; 385 log bytes |
| baremetal-only | `python3 scripts/check_baremetal_only.py --check` | 0 | `baremetal-only.json`; 71 log bytes |
| rtl-source-lists | `python3 scripts/check_rtl_source_lists.py` | 0 | `rtl-source-lists.json`; 390 log bytes |
| timesync-check | `python3 docs/diagrams/timesync_chain.gen.py --check` | 0 | `timesync-check.json`; 60 log bytes |
| timesync-selftest | `python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 | `timesync-selftest.json`; 61 log bytes |
| doc-map-check | `python3 docs/DOC_MAP.gen.py --check` | 0 | `doc-map-check.json`; 61 log bytes |
| doc-map-selftest | `python3 docs/DOC_MAP.gen.py --selftest` | 0 | `doc-map-selftest.json`; 60 log bytes |
| submodule-boundaries-check | `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 | `submodule-boundaries-check.json`; 54 log bytes |
| submodule-boundaries-selftest | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 | `submodule-boundaries-selftest.json`; 60 log bytes |
| gen-toc-selftest | `/tmp/580-a366-docs-env/bin/python3 scripts/gen_toc.py --selftest` | 0 | `gen-toc-selftest.json`; 38 log bytes |
| gen-toc-verify-anchors | `/tmp/580-a366-docs-env/bin/python3 scripts/gen_toc.py --verify-anchors` | 0 | `gen-toc-verify-anchors.json`; 64 log bytes |
| gen-toc-check | `/tmp/580-a366-docs-env/bin/python3 scripts/gen_toc.py --check` | 0 | `gen-toc-check.json`; 94 log bytes |
| py-idiom | `python3 scripts/check_py_idiom.py` | 0 | `py-idiom.json`; 461 log bytes |
| diff-dev | `git diff --check 2a2a7bb655e528edc3087c88033cd3a47546feb4 HEAD` | 0 | `diff-dev.json`; 47 log bytes |
| diff-lane | `git diff --check d02db63c367daf9adc7d709840bd81077e781d80 HEAD` | 0 | `diff-lane.json`; 47 log bytes |
| diff-worktree | `git diff --check` | 0 | `diff-worktree.json`; 0 log bytes |
| diff-index | `git diff --cached --check` | 0 | `diff-index.json`; 47 log bytes |
<!-- completed-gates -->

## Integrity and deliverables

`merge-integrity.json` records a complete parent-selection check: all 931 paths
outside the ownership page equal the appropriate unchanged or changed parent
entry. Only the two recorded ownership-page hunks were manually resolved.
F1-F4 equal dev verbatim; F5-F8 equal the lane verbatim.
The final raw commit message is exactly the requested subject plus one newline.
The committed processor gitlink and initialized checkout still equal
`16be6768f710e79450aace277abacd6c2c3336e5`.
The final parent worktree and index are clean.

`PR-BODY.md` preserves its original bytes and role labels and appends only the
short `Merge with dev` section. Original body: 3039 bytes,
SHA256 `eb53c4c2b0b800315463389fb9a59fdbcda1903c6daa63a931482e8a15ff0298`.
No PR edit or push was made. No existing public comment was edited or deleted.
The merge head needs independent review and authorized publication; this round
makes no review verdict, merge-to-dev claim, or physical timing claim.

The output directory contains only small text evidence, not installed dependencies,
build trees or exported source trees. Logs remain under `/tmp/580-a372`; each JSON
receipt records its exact command, return code, size and SHA256.
