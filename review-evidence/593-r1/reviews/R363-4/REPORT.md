[R363] POSITIVE - exact head e79f23347f754f99d8312c19995431557c896404

# R363-4: composition review of the #593 merge-train candidate (PR #601)

- **Candidate:** `e79f23347f754f99d8312c19995431557c896404`, tree `1403e0eec59a844918b537f26c164e32ec58ddb8`.
  Parents: train candidate C_582 `1304205cfc9fa4c9e69a32130fb366895c5f883b` and PR #601 head `7a051e618677ecd907ed04b086afbdfe374b4336`.
- **Scope:** composition acceptance only. The source head already carries two POSITIVE source reviews:
  [R362-3](https://github.com/kebag-logic/milan-fpga/pull/601#issuecomment-5859780858) and [R363-3](https://github.com/kebag-logic/milan-fpga/pull/601#issuecomment-5859790981), both at `7a051e61`.
- **Verdict basis:** all five lenses were applied to the composed tree. No BLOCKER, MAJOR or MINOR finding is open. One SUGGESTION follows, routed to #602; it does not affect coverage.
  The composed tree introduces no defect beyond the reviewed sources.

## 1. Reconstruction (public state only)

- AGENTS.md sections 3 and 5-7 and CONTRIBUTING.md section 3 give the verification bar. Release campaigns point to REQ-VER-06 and TESTING 6d (`CONTRIBUTING.md:418-423`).
- Issue #593 body (items 1-2) and the manager comments on #593 set the scope and the gates. They cover the assignment, scope note, and round-2 and round-3 assignments.
- The #602 ruling (issue comment 5859297355) supersedes only the PHC-step-to-`mr` obligation of #387. It assigns the RTL change and the remaining design-document rows to #602's deliverable 2.
- PR #601 is OPEN, based on `dev`, head `7a051e61`.

## 2. Composition analysis

**Effective PR delta.** The PR branch was cut from `6d5ebd7357c1e468e446f18a61527c5be6118a04`, the #586 merge. The train carries #586 as C_396 (`10a5bf59a`, second parent `07f72ad6`).

- The PR's own work is therefore `6d5ebd73..7a051e61`: 3 commits, 7 files.
- The naive merge-base overlap with the train is 8 files, including CONTRIBUTING.md and `tests/steps/torture_plan_steps.py`. That overlap is #586 content present on both sides, not a second edit.

**Candidate delta == PR delta.** `git diff --name-only 1304205c e79f2334` equals `git diff --name-only 6d5ebd73 7a051e61` (`receipts/candidate_delta_paths.txt`). The two patches differ only in hunk offsets (+4 lines in TESTING.md).

**Blob fidelity** (`check_blob_fidelity.sh`, `receipts/blob_fidelity.log`):

- Six of the seven PR files are byte-identical to the PR head at the candidate. They are REQUIREMENTS.md, `docs/design/GM_LOSS_RECOVERY.md`, `tb/tools/torture_campaign.py`, `tb/tools/torture_release_mutants.py`, `tests/features/torture_campaign_plan.feature` and `tests/steps/torture_release_steps.py`.
- `docs/testing/TESTING.md` is the only file both sides changed after #586. The candidate blob `d3117723` equals the PR head blob `7ed8cc33` plus exactly the train's own 4-line insert. The residual diff is identical to the train's delta since the PR base.

**The train's edit to the shared file.** Commit `7f997b60d` ("Measure firmware service budgets on the product CPU"), merged by C_397 `3ef7ed1b2`, adds `TESTING.md:401-404`, the firmware service-budget sibling. It sits in section 1.1 (suite index, heading at `:396`). Section 6d spans `:828-1162`, and the PR's hunks sit at `:916-1072`. There is no textual or semantic interaction:

- Section 1.1's new lines say nothing about the soak, `mr`, `tu`, release campaigns or REQ-VER-06.
- Section 6d says nothing about the suite inventory or `fw_service_budget`.
- The heading set and numbering are unchanged: `## 6c` `:729`, `## 6b` `:811`, `## 6d` `:828`, `## 7` `:1163`.
- The TOC entry `:101` and every inbound 6d anchor still resolve. The inbound links are `REQUIREMENTS.md:368`, `CONTRIBUTING.md:423` and `tests/README.md:108`.
- Outside 6d, the page's other `mr`/`tu` mentions are simulation-suite rows (`:273`, `:495`, `:498`, `:536`). The PR does not touch them, and they do not conflict with the release rule.

**Other train documents read against the composed rule:**

- **REQ-VER-06 ↔ TESTING 6d, composed.** Both state the same chain.
  - `mr`: the cause window is `[toggle - R, toggle + R]` with limit `1 s / 2` (`TESTING.md:951-963`; `REQUIREMENTS.md:259-283`).
  - `tu`: `h + R >= 0.25 s`, `2R < 0.25 s`, limit 0.125 s with equality refused, upper `h <= 0.5 s` (`TESTING.md:1028-1040`; `REQUIREMENTS.md:299-315`).
  - Both cite the #602 ruling (`TESTING.md:940-943`, `REQUIREMENTS.md:280-283`).
  - The code agrees: `torture_campaign.py:3327-3328` (`0.25 / 2`), `:3764` (`MILAN_MAX_OBSERVATION_INTERVAL_S / 2`), `:3833-3834`.
- **"Current image still toggles `mr` on PHC steps"** (`REQUIREMENTS.md:281`, `TESTING.md:941`, `GM_LOSS_RECOVERY.md:155`) remains true on the composed tree.
  - `hdl/milan/milan_datapath.sv:3134-3137` still ORs `media_rebase_p_w` into `mcr_restart_p_w`.
  - The train's only datapath change since the PR base (`f8a52f919`, the `N_CONTROL_P` binding at `:7424-7429`) does not touch the restart path.
  - #602 is still OPEN.
- **TIME_SYNC.md.** Neither the train nor the PR changed it since the PR base. `TIME_SYNC.md:345` ("a step is also one `mr` toggle") describes the current image, which is consistent with the PR's current-image statement. Its rewrite belongs to #602 deliverable 2 by the ruling.
- **#387 re-base text as merged** (`docs/findings/394_387_E1_SWITCH_CYCLES.md`, train-added). It says three times that it does not grade #593 (`:15`, `:233`, `:343`).
  - Its per-cycle `mr` and MEDIA_RESET observations (`:235-245`, `:317-331`) show MEDIA_RESET falling to 0 at STREAM_START. That agrees with the composed 6d rule that a decrease is a Table 5.4 reset which fails the soak (`TESTING.md:973-978`, `REQUIREMENTS.md:278`).
  - Its summary of the #387 contract (`:165-173`) predates the #602 ruling (committed 19:29Z; ruling 19:54Z). See S1.
  - Its link targets resolve: `GM_LOSS_RECOVERY.md#media-re-base-on-a-phc-step` (heading `:142`, unchanged) and `TESTING.md#6b-bench-evidence-retention`.
- **Gate inventories.**
  - The train's `scripts/ci_scope.py` change adds `docs/AAF_LATENCY_TAPS.md` to `GATE_READ_DOCS`. The PR's Python names doc pages only in strings and opens none, so no entry is owed.
  - `ci_scope.py --selftest` passes on the candidate, and the delta paths classify as relevant (`true`, `receipts/ci_scope_delta.log`).
  - `ci_events.py --check` passes (1655 contract items).
  - The PR adds no workflow, record pin or new file.

## 3. Findings

No BLOCKER, MAJOR or MINOR finding.

**S1 - SUGGESTION - Docs, Conformance - `docs/findings/394_387_E1_SWITCH_CYCLES.md:165-173` (train-added, not changed by PR #601) - pre-ruling contract summary coexists with the #602 ruling**

- **Evidence:** the page says "The contract requires one counted event per step … One `mr` toggle and one MEDIA_RESET record that event." It links to the GM_LOSS_RECOVERY section whose "Outgoing `mr`" row (`:155`, from this PR) now states that PHC-only re-bases are no cause.
- **Why it is not a defect:**
  - The page is a dated record of the #387 contract as decided. It was written before the ruling and explicitly declines to grade #593.
  - The ruling (comment 5859297355) supersedes exactly that obligation and assigns the design documents to #602 deliverable 2.
  - It is the same class as R362-3 S3 (`GM_LOSS_RECOVERY.md:156`). The other pre-ruling rows of the same page are `:156-157`, `:183` and `:196`.
- **Impact:** a reader who starts from the findings page may take the pre-ruling contract as current.
- **Optional outcome:** #602's documentation deliverable also annotates this findings summary, or links the ruling next to it, when the RTL change lands. No change in PR #601.
- **Verification:** at #602's merge, a search of `docs/` for "One `mr` toggle and one MEDIA_RESET" shows either no hit or a hit that cites the ruling.

## 4. Prior public findings on this PR at this head

I read these after my own pass. The candidate carries the PR head's blobs for every file except TESTING.md, where only the unrelated 4-line insert differs. Each source-head disposition therefore carries over unchanged.

| Prior finding | Status at `e79f2334` | Evidence |
|---|---|---|
| R362-1 F1 = R363-1 F1 (MAJOR), `tu` rise before first discontinuity | Resolved (carried) | `TESTING.md:1055-1058`; planner self-test 78 OK on candidate |
| R362-1 F2 = R363-1 F2 (MAJOR), GM change never graded | Resolved (carried) | `TESTING.md:1014-1019`, `:1061-1064`; `check_release_tu_history` byte-identical |
| R362-1 F3 = R363-1 F4 (MINOR), coarse resolution PASS | Resolved (carried) | Limits `torture_campaign.py:3328`, `:3764`; 132/132 mutants killed on candidate |
| R362-1 F4 = R363-1 S3, PHC-step conflict | Resolved: #602 ruled and cited | `REQUIREMENTS.md:280-283`, `TESTING.md:940-943`, `GM_LOSS_RECOVERY.md:155`; claim re-verified against `milan_datapath.sv:3137` on candidate |
| R362-1 F5, R363-1 F5, R362-2 F2, R363-2 F1 (MINOR), mutation pins | Resolved (carried) | `receipts/release_mutants.log` 132 killed, source unchanged |
| R363-1 F3 (MINOR), one cause, many toggles | Resolved (carried) | `TESTING.md:944-945` |
| R362-2 F1 (MINOR), `tu` limit did not decide minimum | Resolved (carried) | `TESTING.md:1028-1033`, `REQUIREMENTS.md:305-310` |
| R362-2 F3 = R363-2 F2 (MINOR), #602 text stale | Resolved (carried) | Same lines as the #602 row above |
| Round-1/2 suggestions (R362-1 S1-S4, R363-1 S1-S2, R362-2 S1, R363-2 S1-S2) | Taken or resolved as the round-2/3 re-reviews record; unchanged by composition | Blob fidelity |
| R362-3 S1-S3, R363-3 S1-S4 (SUGGESTION) | Retained as optional; none affects coverage; composition neither fixes nor worsens them | Blob fidelity. R362-3 S3's class is extended by this round's S1 |
| R363-3 limit: `check_em_dash.py`, `gen_toc.py --check/--verify-anchors` could not run (renderer absent) | **Closed on the candidate** | Run here with the hash-pinned `tools/markdown/requirements.txt` renderer: all rc 0 (`receipts/r_*.log`) |

## 5. Commands run on the candidate (foreground; receipts under `receipts/`)

`run_gates.sh` (summary: `receipts/summary.tsv`):

- rc 0: `docs_check.py` (0 findings, 172 md files), `check_doc_style.py`, `check_doc_paths.py`, `check_archive.py`, `check_feature_status.py --self-test`, `check_gptp_docs.py`, `check_solution_docs.py`, `check_submodule_docs.py`, `check_py_idiom.py`, `check_hygiene.py`, `check_todo_ownership.py`, `ci_scope.py --selftest`, `check_baremetal_only.py --check`, `ci_events.py --check` and `git diff --check 1304205c HEAD`.
- `torture_campaign.py --self-test`: 78 tests OK.
- `torture_release_mutants.py`: 132 killed, source unchanged.
- `behave tests/features/torture_campaign_plan.feature`: 87 scenarios and 356 steps passed.
- The six renderer-dependent entries returned rc 2 under the system interpreter: "the pinned Markdown renderer is not installed". That is an environment limit, not a verdict. They were re-run as follows.

`run_render_gates.sh` used a disposable interpreter under `scratch/`, with `tools/markdown/requirements.txt` installed `--require-hashes` (`receipts/r_freeze.log`). Summary: `receipts/summary_render.tsv`. All rc 0:

- `gen_toc.py --check`: 114 pages OK.
- `gen_toc.py --verify-anchors`: 195 cross-page fragments reproduced.
- `gen_toc.py --selftest`: 1501/1501.
- `check_em_dash.py --base 1304205c`: 0 findings over 154 added lines, 339/339 arms.
- `check_em_dash.py --base 6d5ebd73`: 0 findings over 1482 added lines.
- `check_em_dash.py --selftest` and `docs_check.py`.

Other checks:

- `check_blob_fidelity.sh`: composition proof (section 2).
- `ci_scope.py <candidate delta paths>`: `true` (relevant).
- `check_clone_integrity.sh`: clean. See section 8.
- Hosted check runs, read-only (`receipts/hosted_checks.txt`). At the source head `7a051e61`:
  - `rtl-fast`, `docs-check`, `docs-check-no-git`, `bdd-conformance`, `full-ci-gate`, `verilator-lint`, `yosys-elaboration` and Yosys shards 0-3 succeeded.
  - Verilator shards 0/5 and 3/5 succeeded; shards 1/5, 2/5 and 4/5 were `in_progress` when read.
  - `Physical gPTP` was skipped, which is not hardware evidence.
- The candidate commit is not on the remote (HTTP 422), so no hosted evidence exists for it.

## 6. Reviewer-owned completion ledger

| Lens | Result | Does the composition touch this lens's scope? | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|---|
| Conformance | CLEAN | Yes, by adjacency. The PR's rule text is byte-identical, but it now coexists with the train's #387 findings page and shares TESTING.md | `REQUIREMENTS.md:250-316`; `TESTING.md:914-1072`; `GM_LOSS_RECOVERY.md:142-200`; `TIME_SYNC.md:345`; `394_387_E1_SWITCH_CYCLES.md:15,165-173,233-245,317-343`; #602 ruling 5859297355; `torture_campaign.py:3327-3328,3764,3824-3834` | R363-4 (this round). Source behaviour: R362-3, R363-3 | `e79f2334` (source: `7a051e61`) |
| RTL | CLEAN | No PR RTL. The train changed `milan_datapath.sv`/`KL_pp_shadow.sv` (`f8a52f919`), which bears on the PR's current-image claim | `hdl/milan/milan_datapath.sv:3134-3137,7424-7429`; `git diff 6d5ebd73 1304205c -- hdl/`; gitlinks (`receipts/clone_integrity_final.log`) | R363-4 (this round). PR no-RTL claim: R362-3, R363-3 | `e79f2334` |
| Robustness | CLEAN | No: planner/oracle blobs are byte-identical to the PR head | `receipts/blob_fidelity.log`; `receipts/planner_selftest.log` (78 OK), `receipts/release_mutants.log` (132 killed) on the candidate | R362-3, R363-3 (source); re-executed here | `7a051e61`, an ancestor of `e79f2334`; no Robustness-scope artifact changed since (blob fidelity) |
| Tests | CLEAN | No: test and step files are byte-identical. The train's test changes are disjoint (`sw/builder/`, `sw/litex/`, `tb/verilator/fw_service_budget/`) | `receipts/planner_selftest.log`, `release_mutants.log`, `behave_plan.log` (87/356), `ci_scope_selftest.log`, `ci_events_check.log` | R362-3, R363-3 (source), with execution re-confirmed on the candidate by R363-4 | `7a051e61` → `e79f2334` |
| Docs | CLEAN (S1 is a SUGGESTION) | Yes: TESTING.md was merged with the train's `:401-404` insert | `TESTING.md` headings `:88-1305`, TOC `:101`, the `:401-404` insert, 6d `:828-1162`; inbound anchors `REQUIREMENTS.md:368`, `CONTRIBUTING.md:423`, `tests/README.md:108`; `receipts/r_gen_toc_*.log`, `r_em_dash_*.log`, `r_docs_check.log`, `docs_check.log`, `doc_style.log`, `doc_paths.log`, `archive.log` | R363-4 (this round) | `e79f2334` |

## 7. Real limits

- This round did not run the full parent, PP, gPTP, Yosys or builder banks, or Verilator suites. Per scope, the composition changes no RTL in the PR delta, and the train's RTL was validated in its own lanes.
- No physical calibration, bench run or hardware evidence was examined. Desk gates do not discharge REQ-VER-06's physical campaigns (`CONTRIBUTING.md:428`). Skipped hosted contexts are not hardware proof.
- The renderer-dependent documentation gates ran with a disposable, hash-pinned interpreter outside the repository (Python 3.14 wheels). Their rc 2 under the system interpreter is recorded as an environment limit.
- No hosted or local-replica evidence exists for `e79f2334`. The source-head hosted Verilator shards 1/5, 2/5 and 4/5 were still running when read.
- The final current-dev candidate (live dev `8bc97021`) was not examined. This verdict covers `e79f2334` only.
- The public source evidence tree (`review-evidence/593-r1` at `59efc9fa`) was listed but not re-executed. Source bank acceptance remains the manager's.

## 8. Clone restoration

No source file was edited. `scripts/__pycache__/`, an ignored artifact created by a gate child process, was removed. `receipts/clone_integrity_final.log` records the final state:

- HEAD `e79f2334`, tree `1403e0ee`; the index `write-tree` equals `1403e0ee`.
- Index and worktree are clean, with no untracked or ignored files.
- Gitlinks match HEAD: `external` `efeb541a`, `gptp-processor` `5dce647a`, `protocol-processor` `16be6768`, `third_party/verilog-axis` `48ff7a7e`.

## 9. Pending manager duties

- Publish the candidate's manager bank receipts; none had landed on #593 or #601 when this round finished.
- Hosted/local-replica acceptance at the merge head.
- Build and validate the final current-dev candidate (source base `1304205c`, live dev `8bc97021`), and re-run the TESTING.md and REQUIREMENTS.md composition gates there if dev moved either file.
- Obtain any further review the bar requires, then get maintainer merge authorization.
- Post-merge containment. Route S1 to #602's documentation deliverable if adopted.

R363-4 FINISHED
