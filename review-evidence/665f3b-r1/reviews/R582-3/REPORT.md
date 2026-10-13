[R582] NEGATIVE - exact head 532ab871272597d83fa08506bcb05298fbe87806

# R582-3: internal independent delta review of PR #736 (issue #665, F3b round 3)

- Head under review: `532ab871272597d83fa08506bcb05298fbe87806`, tree `c298ac5e6a61242d1de452ec24c9991b78881148`.
- Delta reviewed: `651ccb5aea1bc4d99f356503c188947d39e0c9e4..532ab871`, one commit, three files (`receipts/delta-stat.txt`, `receipts/delta.diff`).
- Scope: the round-3 assignment, [issue #665 comment 6155487551](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6155487551). It answers R582-2 (BLOCKER) and R583-2 (MAJOR).
- Context was rebuilt from public state only, in this order: AGENTS.md, the issue's F3b assignments and rulings (6151273346, 6151422598, 6153927545, 6155487551), the author's REVIEW READY (6155670224), `docs/testing/CI_WORKFLOWS.md`, then the diff, then exact-head hosted evidence. The prior review findings were read only after the independent pass over the diff.

## Verdict

The verdict is NEGATIVE for one MINOR finding in the Docs lens.

- The delta does what round 3 asked:
  - `docs/design/MAILBOX_SPLIT.md` is registered as gate-read, and its reader is named.
  - The classifier self-test passes locally and on the hosted runner.
  - No other unregistered gate-read page exists.
  - Every hosted context at the exact head executed and is green.
- R582-2-F1 (BLOCKER), R583-2-F1 (MAJOR) and R582-1-F1 (MAJOR) are resolved.
- One defect remains. The policy page's gate-read paragraph still opens "Seven pages under `docs/`…". The registered table now holds eight, and the new paragraph this commit added is the eighth.
- Fixing that changes a count in the authoritative policy page, so it is a figure, not pure wording. It is filed as MINOR.

## Findings

### R582-3-F1 - MINOR - Docs - `docs/testing/CI_WORKFLOWS.md:179`

**Authority and evidence**

- `scripts/ci_scope.py:69-78` `GATE_READ_DOCS` now has eight entries.
- The self-test prints eight `ok gate-read page` lines (`receipts/ci_scope_selftest.log`).
- The author's REVIEW READY also counts "eight registered/relevant pages".
- `CI_WORKFLOWS.md:179` still reads "Seven pages under `docs/` are relevant because Python in a classifier-gated job names them". That count was correct at the source base `a0f39ad4` and at `651ccb5a`, which both had seven.
- The commit appended the eighth reader's paragraph at `:201-204` beneath that sentence but left the count unchanged.
- No gate reads the count. `ci_events.py --check` passes with it (`receipts/scripts_ci_events_py_check.log`).
- AGENTS.md section 6, Docs lens: "Changed contracts are reflected in authoritative docs".

**Impact**

- The authoritative CI policy page misstates the size of the gate-read set that this commit changed.
- A maintainer auditing the docs-only classification against the prose would count one page fewer than the classifier enforces.
- No gate or classification is affected.

**Required outcome:** `CI_WORKFLOWS.md:179` states the number of pages in `GATE_READ_DOCS`, which is eight. Alternatively, it drops the number.

**Verification:**

- Count the pages listed in the paragraph and compare with `GATE_READ_DOCS` and the self-test's `gate-read page` lines.
- `scripts/ci_events.py --check`, `scripts/check_doc_style.py` and `scripts/docs_check.py` stay rc 0.

### R582-3-R1 - RESIDUE - Docs (PR body only) - PR #736 body, "Status"

**Evidence**

- The body (`receipts/pr736-body.md:23-24`) reads: "Round 2 resumes `db29bdd0…`; `651ccb5aea1bc4d99f356503c188947d39e0c9e4` is the published head of PR #736."
- The published head is now `532ab871272597d83fa08506bcb05298fbe87806`. The same section already names it as "Candidate".
- This is wording only. It changes no figure, test, code, verdict or conformance claim.

**Exact fix:** replace "`651ccb5aea1bc4d99f356503c188947d39e0c9e4` is the published head of PR #736." with "`532ab871272597d83fa08506bcb05298fbe87806` is the published head of PR #736."

## Prior public findings at this head

| Finding | Status at `532ab871` | Evidence |
|---|---|---|
| R582-2-F1 (BLOCKER): `MAILBOX_SPLIT.md` read by a gate but missing from `GATE_READ_DOCS` | **Resolved** | See "Assignment items" 1 and 4 below. |
| R583-2-F1 (MAJOR): the same omission, failing the hosted selector | **Resolved** | As R582-2-F1 |
| R582-1-F1 (MAJOR): hosted `firmware-boundary` and `firmware-verilator`, with their exact-head proof outstanding | **Resolved** | See below. |
| R582-2-S1 (SUGGESTION): RX and link refresh plants escape | **Addressed by its documentation option** | See below. |
| R582-2-R1 (RESIDUE): stale PR body "Status" and limitation bullets | **Resolved** | See below. |
| R582-1-S2 (SUGGESTION): funded clock-read worst case not driven | Retained, optional | The delta touches no test. |
| R582-1-S3 (SUGGESTION): latency stated in words | Unchanged, optional | — |
| R582-1-S4 (SUGGESTION): #23 not named in the PR body | **Resolved** | The body now says "The range also includes #23, integrating the old pin's publication code; it adds no newly adopted behavior." |
| R583-1-F1, R583-1-F2, R582-1-F2, R582-1-R1, R583-1-R1 | Resolved in round 2; still resolved | The delta touches no firmware, test, `MAILBOX_SPLIT.md` or `SUBMODULES.md` (`receipts/delta-stat.txt`). |

**R582-1-F1, resolved.** At this exact head, `firmware-boundary` (job 115552196013) and `firmware-verilator` (job 115552196052) executed every gate step and concluded `success`. This includes "Hold the TSN stack boundary over the firmware/Verilator builders' compiles" (`receipts/hosted-job-steps.txt`). The `rtl-fast` aggregate reports `FIRMWARE_BOUNDARY_RESULT: success` and `FIRMWARE_VERILATOR_RESULT: success` (`receipts/rtl-fast-aggregate-115559598623.log:69-70`).

**R582-2-S1, addressed by its documentation option.**

- `sw/firmware/ctrl/maap/README.md:135-137` now states that the RX and link refreshes provide freshness within the pass, and that the same pass's MAAP poll refreshes and republishes changed gates.
- Checked against `sw/firmware/ctrl/maap/maap_mbx.c`:
  - `receive` refreshes at `:127`;
  - the link event refreshes at `:157`;
  - `poll` refreshes at `:167`;
  - `poll` then writes `mbx_pub_da_gate` only when the gate changed (`:169-175`).
- The statement is accurate. The README does not name the timer-event refresh (`:145`), but it does not claim the list is exhaustive. The earlier sentence at README `:127`, "The dispatch path caches each `acmp_declaring` answer before entering MAAP", already covers it.
- No killing control was added. That was optional.

**R582-2-R1, resolved.**

- The body's "Status" carries the exact replacement text from R582-2-R1.
- Neither removed limitation bullet remains: a grep for "cannot be proven", "prepared for later publication" and "still the published head" returns 0.
- Its new head reference has since gone stale; see R582-3-R1.

## Assignment items (round 3)

1. **Register the page.**
   - `scripts/ci_scope.py:72` adds `docs/design/MAILBOX_SPLIT.md`.
   - The rule comment at `:67-68` names `ctrl_service_bounds.py (firmware-unit)`.
   - `:292-293` adds the classification case.
   - `CI_WORKFLOWS.md:201-204` states the reader, its job, what it checks, and that no `docs-check` step runs it. Each claim is verified:
     - `.github/workflows/rtl-fast.yml:356` runs `test_ctrl_firmware.py … --shard 0/4`. That is the "suites" phase (`test_ctrl_firmware.py:155-162`), whose first arm is `arm_service_bounds`.
     - `.github/workflows/docs.yml` invokes neither `test_ctrl_firmware.py` nor `ctrl_service_bounds.py`.
     - `ctrl_service_bounds.py:61-77` plants a stale value into every figure and conclusion.
   - Local result: `python3 -I scripts/ci_scope.py --selftest` returns rc 0 with 109 `ok` lines. These include the case, the derived `gate-read page docs/design/MAILBOX_SPLIT.md (named at sw/firmware/ctrl/test/ctrl_service_bounds.py:13)`, and both of its mutation arms (`receipts/ci_scope_selftest.log`).
2. **No other unregistered page.**
   - The self-test's derivation equals the table: eight pages, all `ok`.
   - An independent inventory (`scripts/gate_read_inventory.py`, `receipts/gate_read_inventory.log`) looked beyond what the scan covers. It took all 177 documentation-class tracked files and searched every non-documentation file the branch changed since `a0f39ad4`: 78 files, including workflow YAML, `scripts/`, C/C++ and YAML, which the scan does not read.
   - The only programmatic reads of documentation-class pages are:
     - `scripts/check_submodule_docs.py` reading `docs/reference/SUBMODULES.md` and the `submodule_boundaries` diagram;
     - `docs/diagrams/submodule_boundaries.gen.py`;
     - `scripts/ci_events.py` reading `CI_WORKFLOWS.md`.
   - All of those run in `docs.yml` (`:111-124`), which always runs, or are already tabled as documentation only. None is in a classifier-gated job.
   - No gated code imports `check_submodule_docs`. The references in `ctrl_configs.py:160-161` and `syn/yosys/ooc_selftest.py:71` are mentions, not reads.
   - Everything else found was a Markdown link or a comment.
3. **Suggestion and residue.** S1 accurate (above); R1 applied (above).
4. **Hosted CI at the exact head** (`receipts/hosted-summary.txt`, `receipts/check-runs-532ab871.json`).
   - All four workflow runs are attempt 1, `pull_request`, and concluded `success`: `rtl-fast` 38471631742, `rtl-full` 38471631680, `elaborate` 38471632015 and `docs` 38471631560.
   - The following check runs are `success` at head `532ab871…`: `changes`, `elaborate`, `firmware-unit`, `firmware-control-mutants`, `firmware-aecp-mutants`, `firmware-srp-mutants`, `firmware-boundary`, `firmware-verilator`, `publication-census`, `verilator-lint`, `bdd-conformance`, `yosys-elaboration`, `rtl-fast`, `full-ci-gate`, Verilator shards 0-4/5, Yosys shards 0-3/4, `verilator-suites`, `yosys-portability`, `docs-check`, `docs-check-no-git` and `wire-accountability`.
   - Only "Physical gPTP (nightly and manual)" is `skipped`. It is a scheduled/manual context, so it is not hardware proof.
   - The hosted `changes` log prints `selftest: PASS` with the `MAILBOX_SPLIT.md` lines (`receipts/changes-job-115551904745.log:614,656,699-700,711`).
   - Hosted `firmware-unit` prints `[ok] arm service_bounds`, `checks: 47 failures: 0` (`receipts/firmware-unit-115552196216-service-bounds-excerpt.log`).
5. **Nothing else changed.**
   - `git diff --raw 651ccb5a..532ab871` lists exactly three blob modifications, all mode 100644: `CI_WORKFLOWS.md`, `ci_scope.py` and `maap/README.md`.
   - There is no gitlink, firmware, test, generated or workflow change.

## Probes and local runs

| Run | Result | Receipt |
|---|---|---|
| `python3 -I scripts/ci_scope.py --selftest` at head | rc 0, 109 ok, `selftest: PASS` | `receipts/ci_scope_selftest.{log,rc}` |
| Mutation M0: unmodified copy (control) | rc 0, 0 FAIL | `receipts/ci_scope_mutants.tsv`, `receipts/mutant_M0_control.log` |
| M1: drop `MAILBOX_SPLIT.md` from `GATE_READ_DOCS` | rc 1. Both the case and the derivation arm FAIL. | `receipts/mutant_M1_drop_table_entry.log` |
| M2: drop the new classification case only | rc 1. The arm "gate-read … filed as docs-only is rejected" FAILs, so the case is removal-sensitive. | `receipts/mutant_M2_drop_case.log` |
| M3: `651ccb5a`'s `ci_scope.py` in the head tree | rc 1. The R582-2-F1 FAIL line reproduces. | `receipts/mutant_M3_parent_ci_scope.log` |
| `arm_service_bounds` alone at head (`scripts/run_service_bounds.py`) | rc 0, 47 checks, 38/38 planted controls caught | `receipts/service_bounds_head.{log,rc}` |
| `scripts/ci_events.py --check` / `--selftest` | rc 0 / rc 0 (2169 items, 3064 arms) | `receipts/scripts_ci_events_py_check.log`, `receipts/scripts_ci_events_py_selftest.log` |
| `scripts/check_doc_style.py`; `scripts/docs_check.py` | rc 0; rc 0 | `receipts/scripts_check_doc_style_py.log`, `receipts/scripts_docs_check_py.log` |
| `scripts/check_em_dash.py --base 651ccb5a` | rc 2, **not run**: the pinned renderer was not installed locally. A direct search of the delta's added lines finds no U+2014. Hosted `docs-check` is green. | `receipts/doc_gates.tsv` |
| Gate-read inventory over branch changes | No unregistered gate-read page | `receipts/gate_read_inventory.log` |
| Clone integrity after probes | rc 0. HEAD, tree, index, 1311/1311 tracked blob bytes and modes, and five required gitlinks clean. No untracked or ignored residue: bytecode caches created by the runs were removed. | `receipts/integrity.log` |

Probes ran on `git archive` copies under the packet's `scratch/`. The local interpreter was CPython 3.14.7; the author recorded 3.12.3.

## Lens results (R582-3)

- `[R582] PASS Conformance` — `scripts/ci_scope.py:67-72,292-293`; `CI_WORKFLOWS.md:201-204`; hosted check runs at `532ab871`. Checked against round-3 items 1-5, R582-2-F1/R583-2-F1 required outcomes, and AGENTS.md section 7 exact-head `rtl-fast`/`verilator-suites`/`yosys-portability`.
- `[R582] PASS RTL` — `receipts/delta-stat.txt`. The delta changes no `hdl/`, `tb/`, firmware C or generated file, so RTL scope is inapplicable. The exact-head hosted `verilator-suites`, `yosys-portability`, `elaborate`, `verilator-lint` and `yosys-elaboration` are green.
- `[R582] PASS Robustness` — `ci_scope.py` `is_doc_only_path`/`GATE_READ_DOCS`. A docs-only edit or rename of `MAILBOX_SPLIT.md` is now classified relevant: the case at `:293`, plus `--no-renames` as stated at `CI_WORKFLOWS.md:231-233`. The no-git fallback path was exercised by the hosted `docs-check-no-git` (green).
- `[R582] PASS Tests` — mutation probes M0-M3. The new case and table entry each fail the self-test when removed, and the parent classifier reproduces the original failure. The hosted `firmware-unit` ran `service_bounds` (47/0).
- `[R582] MINOR Docs` — `CI_WORKFLOWS.md:179`. See R582-3-F1. The other Docs artifacts are accurate: `CI_WORKFLOWS.md:201-204`, `ci_scope.py:67-68` comment, and `maap/README.md:135-137` against `maap_mbx.c:127,145,157,167-175`.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round-3 items 1-5; `ci_scope.py:67-72,292-293`; `CI_WORKFLOWS.md:201-204`; PR body; hosted runs 38471631742/38471631680/38471632015/38471631560 | R582-3 | `532ab871272597d83fa08506bcb05298fbe87806` |
| RTL | CLEAN | `git diff --raw 651ccb5a..532ab871` (no RTL/firmware/generated change); hosted `verilator-suites`, `yosys-portability`, `elaborate`, `verilator-lint`, `yosys-elaboration` | R582-3 | `532ab871272597d83fa08506bcb05298fbe87806` |
| Robustness | CLEAN | `ci_scope.py` classification and gate-read derivation, rename and no-git paths; `maap_mbx.c` refresh sites against `maap/README.md:135-137` | R582-3 | `532ab871272597d83fa08506bcb05298fbe87806` |
| Tests | CLEAN | `ci_scope.py --selftest` (local and hosted); mutants M0-M3; `arm_service_bounds` local and hosted | R582-3 | `532ab871272597d83fa08506bcb05298fbe87806` |
| Docs | UNCLEAN (R582-3-F1 MINOR open; R582-3-R1 RESIDUE carried) | `CI_WORKFLOWS.md:179,201-204`; `ci_scope.py:57-68`; `maap/README.md:127-137`; PR #736 body | R582-3 | `532ab871272597d83fa08506bcb05298fbe87806` |

Lens scope untouched by this delta stays covered by the earlier rounds, as the brief directs. This includes the firmware predicate, the stack pin and the image hashes, covered by R582-2 and R583-2 at `651ccb5a`. Nothing in those lenses' firmware, test or pin scope changed between `651ccb5a` and `532ab871`.

## Limits

- This is a delta review. Firmware behaviour, the pin and the images were not re-run beyond `arm_service_bounds`. Earlier rounds' coverage of those artifacts stands because the delta does not touch them.
- No manager source bank exists or is claimed at this head. Source-head execution evidence is the author's published receipts plus the exact-head hosted runs read here.
- `check_em_dash.py` was not run locally (missing pinned renderer); the hosted `docs-check` covers it.
- Physical calibration NOT RUN. The skipped "Physical gPTP" context is not hardware proof.
- No act or Docker replica was run, by instruction. Hosted and act acceptance belongs to the manager.

## Pending manager duties

- Carry R582-3-F1 to the executor. A one-word fix at `CI_WORKFLOWS.md:179` un-covers only Docs; re-review is needed at the new head.
- Carry R582-3-R1 to the residue checklist.
- Build and validate the current-dev merge candidate (source base `a0f39ad4`, live dev `0136de16`) with the builder and native banks, and link the receipts.
- Obtain the external review at the final head.
- Hosted and act acceptance at the final head.
- Merge only with explicit maintainer authorization.

R582-3 FINISHED
