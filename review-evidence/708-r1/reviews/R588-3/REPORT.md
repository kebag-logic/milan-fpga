[R588] POSITIVE - exact head e9f2ea8e1d256f709f206518cf402d77914c5e3f

# R588-3: composition review of issue #708 / PR #754

- **Candidate:** `e9f2ea8e1d256f709f206518cf402d77914c5e3f`, tree `268289918a958a682bc98146fe62b8a484ab3351`.
- **Parents:** live dev `1f6f2f57177f1dd904654c317009461b43423989` and PR head `b2460b79b399a2c383d8d912c8d017b78e5e4072` (tree `4cc342899bae1253e7e4f63435c4ba2550f1d020`).
- **Scope:** composition acceptance only. The verdict says the composed tree introduces no defect beyond the reviewed sources.
- **Source reviews this round builds on:**
  - R588-2 POSITIVE at `b2460b79`, PR comment 6220532638;
  - R589-1 POSITIVE at `5c6f50ee`, PR comment 6219051857.

**Summary.** The candidate is exactly the clean three-way merge of dev and the PR head.

- One file is changed on both sides: `docs/design/MAILBOX_SPLIT.md`. The two sides' hunks are disjoint.
- Every other path is taken whole from one side.
- The one program that reads the merged page passes on the candidate. So do every documentation, inventory and workflow gate that reads files from both sides.
- The signed local-CI packet verifies with the required key, and names this candidate and head.
- Its `execution.coverage` field is `null` (S1 below). No lens in this report relies on that field.
- There is no open BLOCKER, MAJOR or MINOR.

## 1. Reconstruction

- **Order read:**
  1. AGENTS.md (sections 5 to 8);
  2. the issue #708 body: scope, owed adaptations, acceptance 1 to 5;
  3. the manager's issue comments: the assignment, the hold ruling, the flow decision and the resume;
  4. the PR #754 round-2 assignment (6219696478);
  5. the diff `1f6f2f57..e9f2ea8e`;
  6. the history `734eb780..{1f6f2f57, b2460b79}`;
  7. the signed packet at `63a243a9:review-evidence/708-r1/local-ci/b2460b79`;
  8. hosted checks at the PR head.
- I read prior review findings only after my own composition pass (section 6).
- **Composition question.** The predecessor set named for this train is empty. Live dev equals the source base `1f6f2f57`.
  - The PR's last dev merge is `734eb780` (merge commit `a1dfbfad`).
  - So the composition is dev `734eb780..1f6f2f57` against PR `734eb780..b2460b79`.
  - The dev side holds PRs #745 (slot OOM and census memory bound), #753 (board deployment guide, pinned LiteX) and #751 (bench lane B19 records).

## 2. Composition evidence

| Check | Result | Receipt |
|---|---|---|
| `git merge-tree --write-tree 1f6f2f57 b2460b79` | `268289918a95...`, equal to the candidate tree; parents are dev then the PR head | `receipts/merge_composition.txt` |
| Files changed on both sides | one: `docs/design/MAILBOX_SPLIT.md`. Dev hunk `@@ -1033,3` (census worker sentence, #744). PR hunks `@@ -32`, `@@ -779,27`, `@@ -807`, `@@ -1112` (contents line, differences section, history). Disjoint | `receipts/merge_composition.txt` |
| Per-path origin | the 16 dev-side paths are taken whole from dev, and the 17 other PR-side paths whole from the PR head. Only `MAILBOX_SPLIT.md` is merged, and it differs from each parent by exactly the other side's hunk | `receipts/composition_check.txt`, `scripts/composition_check.sh` |
| Submodule gitlinks | `protocol-processor` is `2cbed0a987c1` in the candidate and the PR head; dev has `2ad2f845`. The other four gitlinks are unchanged. Checkouts match and are clean | `receipts/restore_check.txt` |
| Programs that read the merged page | `scripts/ci_scope.py` (path list only) and `sw/firmware/ctrl/test/ctrl_service_bounds.py` (exact service-bound lines) | `git grep MAILBOX_SPLIT` |
| `ctrl_service_bounds` on the candidate | `[ok] arm service_bounds`, 47 checks, 0 failures. Whole `test_ctrl_firmware.py --jobs 4`: PASS, rc 0, in 4 min 20 s | `receipts/firmware_unit_candidate.{log,rc}` |
| Workflow delta between candidate and head | only `rtl-fast.yml` and its template, both byte-equal to dev. The census `--jobs` now comes from `CI_CENSUS_JOBS` (#744). `publication_census.py:598-607` uses jobs only to elaborate shapes in parallel, and its results are sorted. So the census verdict does not depend on the job count, and its RTL inputs equal the head's | `receipts/manifest_checks.txt`, `git diff b2460b79 e9f2ea8e -- .github/` |
| Dev-side pages that mention the processor or its records | `117_GPTP_SILICON_EVIDENCE.md:580` cites AREA_BUDGET for a historical lane-base diff. The B19 rows in 117 and 387 are bound to the dev `9ef71772` image. `BOARD_DEPLOYMENT.md:114` and README/QUICKSTART only initialise submodules. None quotes a figure, digest or ACMP behaviour that this pin move changes | `git grep` and diff reads |
| Resource record against the composed inputs | dev changes no `hdl/`, `syn/`, `sw/` source or memory image. `pp_resource_gate.py check-baseline`: `baseline PASS: 3 endpoints` | `receipts/gates/pp_check_baseline.*` |
| Comments added by the composition | none: the merge took every source file whole. The added code and record lines from the PR side (`hdl`, `acmp_walk.cpp`, `scripts`, `syn`) carry no lane label, reviewer ID, round or comment ID. The `measured` strings in `pp_resource_baseline.json` are record provenance, not source comments | `git diff -U0 1f6f2f57 e9f2ea8e` grep |

**Gates run on the candidate.** The script is `scripts/run_gates.sh`. There are 37 receipts in `receipts/gates/`, every one rc 0:

- **Documentation:**
  - `docs_check.py`: 0 findings over 209 md files;
  - `check_feature_status.py` and its `--self-test`;
  - `check_em_dash.py --base 1f6f2f57`: 0 findings over 201 added lines on 7 pages, arms 339/339;
  - `check_doc_style.py` and its `--selftest`;
  - `check_gptp_docs.py`;
  - `check_solution_docs.py`;
  - `check_submodule_docs.py` (6 exact gitlinks) and its `--selftest`;
  - `check_diagram_pngs.py`;
  - `gen_module_matrix.py --check`;
  - `gen_toc.py --verify-anchors`: 527 cross-page fragment links reproduced;
  - `gen_toc.py --check`: 148 pages;
  - `gen_toc.py --selftest`: 1501/1501;
  - `check_doc_paths.py`;
  - `check_archive.py`.
- **Inventories and ratchets:**
  - `check_baremetal_only.py --check` (0 findings over 1346 files) and its `--selftest`;
  - `check_port_contracts.py`;
  - `measure_naming.py --check`;
  - `measure_test_evidence.py --check` and its `--selftest`;
  - `measure_fail_fast.py --check`;
  - `check_todo_ownership.py`;
  - `check_hygiene.py --check`;
  - `check_py_idiom.py`, `check_sv_idiom.py` and `check_cpp_idiom.py`;
  - `pp_srcs.py --check`.
- **Workflow contract:**
  - `ci_events.py --check` (2199 contract items) and its `--selftest`;
  - `ci_gate_workflows.py --check`;
  - `ci_gate_workflows_selftest.py`;
  - `ci_scope.py --selftest`.
- **Other:** `git diff --check 1f6f2f57 HEAD`.

The first attempt at `check_em_dash` and the three `gen_toc` runs stopped with rc 2, because the pinned Markdown renderer was not installed on this host. They were rerun with `tools/markdown/requirements.txt`, installed `--require-hashes` into a private environment under the packet's scratch directory. The receipts are those reruns.

## 3. Signed local-CI packet

The packet is `63a243a9:review-evidence/708-r1/local-ci/b2460b79`. Receipts are in `receipts/signed/`, `receipts/signature_verify.txt` and `receipts/manifest_checks.txt`.

1. **Key.** `allowed_signers` has one line, principal `milan-local-ci`, `namespaces="milan-local-ci"`. Its key fingerprint is `SHA256:dRI12tvJkhueTEGqsRutn2L+dT/5qqOCsCVzBU5CI7k`, the required one. **PASS.**
2. **Signature.** `ssh-keygen -Y verify -f allowed_signers -I milan-local-ci -n milan-local-ci -s manifest.json.sig < manifest.json` reports `Good "milan-local-ci" signature`, rc 0. `manifest.json` has sha256 `440e6db51fdf5965f9cb7da163d380f27859d0eea741024a1b60976d75938ce5`, as stated. **PASS.**
3. **Subject.** `subject` names this candidate, the candidate parent `1f6f2f57`, the candidate tree `26828991`, the head `b2460b79`, the head tree `4cc34289` and PR 754. All match. `definitions.candidate.*` and `definitions.head.*` equal the sha256 of each workflow at the named commit (8/8). The head and candidate differ only in `rtl-fast.yml`. `result` is `success`.
4. **Execution.** act exit 0. Of 64 act jobs, 63 are `success` and one is `skipped`: `rtl-full/Physical gPTP (nightly and manual)`, whose `if:` (`rtl.yml:414`) runs it only on schedule or manual dispatch. Bank `manager-builder` has 48 commands and bank `full-native` has 5, every one exit 0. Commands are recorded only as `argv_sha256`.
5. **Coverage.** `execution.coverage` is `null`. The packet holds no per-job mapping to act, a bank or a named not-run reason. This round therefore does not rely on such a mapping. See S1.

Hosted checks at the PR head `b2460b79` show 63 pass and 1 skipping (the same Physical gPTP job). They cover the head, not this candidate. The manager owns hosted and act acceptance.

## 4. Findings

### R588-3-S1 - SUGGESTION - Tests - the signed manifest's `execution.coverage` is `null`

- **Artifact:** `review-evidence/708-r1/local-ci/b2460b79/manifest.json` (sha256 `440e6db5...`), key `execution.coverage`.
- **Evidence:** the round brief says every workflow job is mapped in the manifest's coverage by act, by bank or by a named not-run reason. The signed bytes carry `"coverage":null`.
  - act replayed the head's workflows: `definitions.head.rtl-fast.yml` is `93da483b`, while the candidate's is `5758f0dd`.
  - Bank commands appear only as argv hashes, so nothing signed says which bank step ran the candidate-only `rtl-fast` definition.
  - Nothing signed gives the Physical gPTP skip a reason.
- **Why this is not graded MINOR:**
  - The manifest is outside the composed tree.
  - No repository document defines its schema: `act_ci.py`, CI_WORKFLOWS.md and CONTRIBUTING.md have no `coverage` or `milan-local-ci` key.
  - The gap it would close is closed here by direct evidence. The candidate-only workflow bytes are dev's (#744). The census verdict is independent of its job count, and its inputs equal the head's. The skip follows the job's event condition, as it does on the hosted run.
- **Impact:** a later reader of the packet cannot reproduce the coverage statement from the signed bytes.
- **Outcome:** the manager either republishes the manifest with `execution.coverage` populated, or corrects the statement that describes it.
- **Verification:** for the republished packet, `python3 -c 'import json;print(json.load(open("manifest.json"))["execution"]["coverage"])'` shows one entry per act job. The signature must still verify against the same key.

### Prior findings, retained or resolved at this head

The PR-side files are byte-equal to `b2460b79`, so every source-side resolution carries over unchanged.

| Finding | Status at `e9f2ea8e` | Evidence |
|---|---|---|
| R588-1-F1 (MINOR, Docs): pin page omitted the #168 16-bit VLAN | **Resolved** | `docs/reference/SUBMODULES.md:199,208` state that GET_STREAM_INFO selector 6 and GET_RX_STATE carry 16 bits. `hdl/milan/milan_datapath.sv:5190-5191` carry the selector-6 note. Both are taken from the PR whole |
| R588-1-R1 and R589-1-R1 (RESIDUE): comment ID in `acmp_walk.cpp` | **Resolved** | `git grep "comment [0-9]{6,}" acmp_walk.cpp` finds nothing |
| R588-1-R2 (RESIDUE): LD3 history wording | **Resolved** | `acmp_walk.cpp:43-44` reads "normalised LD1 and LD2 in the walk, and LD3's status byte in its scenario" |
| R588-1-S1 (SUGGESTION, Tests): two more #168 convergences are not walked | **Retained, optional** | unchanged |
| R588-1-S2 (SUGGESTION, Tests): sv2v 0.0.12 nvm_port guard | **Resolved** | filed as issue #755 (open) |
| R588-2-R1 (RESIDUE, Docs): the PR body calls the selector-6 note "a one-line comment" | **Retained** | PR body, round-2 F1 bullet: "now has a one-line comment like those on selectors 4 and 7". The note is two lines (`milan_datapath.sv:5190-5191`). **Exact fix:** replace "a one-line comment" with "a two-line comment". This changes no code, test or claim |
| R588-2-S1 (SUGGESTION, Docs): the selector-6 note omits the unsettled case | **Retained, optional** | `milan_datapath.sv:5190-5191` |

### Observation, not a finding against this PR

`.github/ci-templates/rtl-fast.yml` keeps `(#665, comment 6100024293)` in a workflow comment. That comment ID predates this train; #744 only reflowed it on dev. Issue #746 tracks this class of comment. The PR adds no new instance.

## 5. Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | **The composition does not touch this lens's scope.** `receipts/composition_check.txt` shows no RTL, firmware, test expectation, gitlink or clause citation that differs from `b2460b79`. The dev side is CI, deployment and bench-record text, and the B19 rows are bound to dev `9ef71772`. Source coverage comes from R588-2 at `b2460b79` and R589-1 at `5c6f50ee` | R588-2 (source), R588-3 (composition) | `b2460b79` (source); `e9f2ea8e` (composition) |
| RTL | CLEAN | **The composition does not touch this lens's scope.** Dev changes no `hdl/`, `syn/` or submodule path. The `protocol-processor` gitlink is `2cbed0a9` in both the candidate and the PR head. Candidate gates: `pp_resource_gate.py check-baseline` (3 endpoints), `pp_srcs.py --check`, `check_sv_idiom.py`, `check_port_contracts.py` and `measure_naming.py --check`, all rc 0 | R588-2 (source), R588-3 (composition) | `b2460b79`; `e9f2ea8e` |
| Robustness | CLEAN | **The composition does not touch this lens's scope** for PR code. The dev-side scripts (`act_ci.py`, `check_baremetal_only.py`, `ci_events.py`, `ci_runtime_workflows.py`) are dev's bytes. Their checks and self-tests pass over the PR's files on the candidate: `check_baremetal_only --check/--selftest`, `ci_events --check/--selftest` and `ci_gate_workflows_selftest`. `publication_census.py:598-607` gives the same verdict for any job count | R588-2 (source), R588-3 (composition) | `b2460b79`; `e9f2ea8e` |
| Tests | CLEAN (S1 suggestion) | **The composition touches this lens's scope** through the merged page's reader and the workflow definitions. `test_ctrl_firmware.py --jobs 4` passes on the candidate, including `service_bounds` (47/0). Candidate gates: `measure_test_evidence --check/--selftest`, `ci_gate_workflows --check`, `ci_scope --selftest` and `measure_fail_fast --check`. The signed packet verifies: subject and definitions match, act has 63 success and 1 event-gated skip, and both banks exit 0 | R588-3 | `e9f2ea8e1d256f709f206518cf402d77914c5e3f` |
| Docs | CLEAN (retained RESIDUE R588-2-R1; suggestion R588-2-S1) | **The composition touches this lens's scope** through the merged `MAILBOX_SPLIT.md` (disjoint hunks at 32, 779-807, 1033 and 1112). Dev's `CI_WORKFLOWS.md`, README, QUICKSTART, guides and findings pages sit beside the PR's AREA_BUDGET, SUBMODULES and 234 pages. Candidate gates: `docs_check`, `check_em_dash --base 1f6f2f57`, `gen_toc --check/--verify-anchors/--selftest`, `check_doc_style --selftest`, `check_submodule_docs --selftest`, `check_doc_paths` and `check_diagram_pngs`, all rc 0 | R588-3 | `e9f2ea8e1d256f709f206518cf402d77914c5e3f` |

## 6. Limits and pending manager duties

**Limits:**

- **Not run by this round:**
  - act or Docker;
  - the host act runner and its selftest;
  - the builder, native, Vivado, Yosys, gPTP or full parent bank;
  - the hosted gates on the candidate.
- **Execution evidence for the candidate** is:
  - the signed packet (banks on the candidate, act on the head);
  - the focused runs listed here.
- **Not performed:** physical calibration and the field or Physical gPTP runs. They are not hardware proof. The Physical gPTP job is skipped on PR events by design.
- **Hosted evidence** at `b2460b79` (63 pass, 1 skip) is head evidence, not candidate evidence.
- **Clone state:** after the runs, the clone is at the exact head. HEAD, index tree and worktree all equal `268289918a95...`, and there are no tracked modifications. Five submodule checkouts sit at their gitlinks and are clean. The ignored `__pycache__` directories the runs created were removed (`receipts/restore_check.txt`).

**Pending manager duties:**

1. S1: republish the manifest with `execution.coverage` populated, or correct the statement that describes it.
2. Carry R588-2-R1 to the residue checklist, with its exact fix.
3. Confirm the two-positive bar from the public record:
   - R589-1 (external) is POSITIVE at `5c6f50ee`;
   - R588-2 is POSITIVE at `b2460b79`;
   - the round-2 assignment (6219696478) ruled that one re-reviewer covers the `5c6f50ee..b2460b79` delta;
   - that delta also includes comment-only edits in `acmp_walk.cpp` and `milan_datapath.sv`.
4. Build and validate the final current-dev candidate at the merge turn if dev moves past `1f6f2f57`.
5. Hosted and act acceptance.
6. After the merge (issue #708 acceptance 5), flash the image and run the soak.
7. Post-merge containment, then issue closure and the move to Done.
8. A merge requires explicit maintainer authorization.

R588-3 FINISHED
