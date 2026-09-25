[R306] POSITIVE - exact head 9d66cfe0dc87ffe4a5f45691d5c86b041b050b38

Round R306-3. This is an internal, independent, cleared-context delta review of PR #560 (issue #508).

- Scope: the round-4 fix commit `9d66cfe0` over `224ec0e9`, which R306-2 reviewed.
- Tree: `5424e3e661916f1fd38c8a198400dfc0ec6baded`.
- Source base: `573f0052a0e4412e81f0845438fcec2086ce5d55`.

Summary:

- Both round-3 findings are closed at this head.
- The delta is exactly the scoped 5 files and 6 lines.
- Every assigned gate is rc 0.
- No new finding.
- All five lenses are covered clean at this exact head.

## Reconstruction

- **Authorities.**
  - AGENTS.md sections 6-7 and CONTRIBUTING.md (required docs contexts).
  - `.github/workflows/docs.yml`: the documentation gates run before any submodule checkout (`:12-20`), and `docs-check-no-git` strips `.git` (`:482-490`).
- **Assignment.** The amended assignment on issue 508 (comment 5826348330) is the frozen round-4 scope. It asks for three things:
  1. Commit-pinned GitHub blob URLs at `990f9652` for `README.md:488`. They keep `#fig-06-lineage` and `#fig-05-settled` and name F06.13 and F05.5.
  2. Eight arms, eight elaborations and nine runs, stated everywhere the campaign size appears.
  3. No other change, plus the named gate list.
- **Start.** The public review start is PR comment 5826437183.
- **Prior findings.** I read the prior public findings (R306-2 5826344643 and R307-2 5826345263) only after my own pass over the delta.

## Delta scope (`receipts/delta.raw`, `receipts/delta.diff`, `receipts/delta.stat`)

`git diff --raw 224ec0e9 9d66cfe0` lists 5 modified files. All are mode 100644, and there are 6 insertions and 6 deletions:

- `CHANGELOG.md:57`
- `docs/testing/TESTING.md:267`
- `scripts/measure_test_evidence.py:620` (a string literal inside `DUT_READER_DISPOSITIONS`)
- `tb/verilator/milan_dp/Makefile:451-452` (`#` comment lines only)
- `tb/verilator/milan_dp/README.md:488`

Nothing else changed:

- No gitlink moved: `external` is `efeb541a`, `gptp-processor` is `e5dcea6e`, `protocol-processor` is `990f9652` and `third_party/verilog-axis` is `48ff7a7e`.
- No `hdl/`, testbench source or processor file is touched.
- The commit is one line with no trailers.

## Findings

None at this head.

## Prior public findings: disposition at this head

| Finding | Disposition | Evidence |
|---|---|---|
| R306-2 F1 (BLOCKER; Docs, Tests) = R307-2 F1 (MAJOR; Docs, Tests): relative links into the processor submodule at `README.md:488` | **CLOSED** | See the F1 evidence below the table. |
| R306-2 F2 (MINOR; Docs) = R307-2 F2 (MINOR; Docs): campaign still described as seven | **CLOSED** | See the F2 evidence below the table. |
| R306-2 S1 (G8 count taken before the solicited read) and S2 (Failed-to-Advertise step) | **RETAINED** as SUGGESTION | Not touched by this delta; optional. |
| R307-2 S1 (ordinal G8 push labels) and S2 (`README.md:849` dated 345/0 row) | **RETAINED** as SUGGESTION | Not touched by this delta; optional. |
| R306-1 S1 (= R307-1 S2), S2, S3 | **RETAINED** as SUGGESTION | Not touched by this delta; optional. |
| R306-2 observation: pre-existing stale processor citations outside this PR (`sw/litex/*`, `sim_main.cpp:2297`) | **Unchanged**, out of scope | Separate-issue material under AGENTS.md section 4; not a finding against this lane. |

**F1 evidence.**

- `README.md:488` now links `https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/990f96526bb89356c963a260ebbdcf2a77e6623a/docs/architecture/{06_aecp_engine.md#fig-06-lineage,05_acmp_engine.md#fig-05-settled}`. The link texts are "F06.13, field lineage" and "F05.5, settlement detail".
- The host and repository are the `.gitmodules` URL of `protocol-processor`. The commit is the gitlink `990f9652`. This is the same form as the same README's `:728`.
- At the pin, the anchors are `06_aecp_engine.md:295` `<a id="fig-06-lineage">` **F06.13 - Field lineage** and `05_acmp_engine.md:316` `<a id="fig-05-settled">` **F05.5 - Settlement detail**. The figure names in the link text match.
- The hosted blobs exist at that commit. Their SHAs equal the local pin's blobs (`77720a15...`, `56afbfdd...`), and both URLs return HTTP 200 (`receipts/hosted_blob_check.txt`).
- `docs_check.py` in a `git archive` of `9d66cfe0` (empty `protocol-processor/`) reports 0 findings, rc 0 (`receipts/docs_check_git_archive.txt`).
- The same procedure at `224ec0e9` still gives the 2 original findings, rc 1 (`receipts/docs_check_git_archive_prior_head_control.txt`). So the check can fail for this defect, and the fix is what turned it green.
- Hosted results at this head:
  - `docs-check-no-git` is **success**.
  - In `docs-check`, step 9 "Link health, wording, dead-reference and local-info gate" (the step that failed at `224ec0e9`) is **success**. Steps 10-25 are also success. The job was still running at 04:02:19Z (`receipts/hosted_snapshot_final.txt`).

**F2 evidence.**

- `gsi_mutants.py` `MUTATIONS` has 8 entries (`receipts/arm_count.txt`). The selector refuses `0` and `9` with "use 1..8" (`receipts/gsi_mutants_selector_bound.txt`).
- Every campaign-size statement now agrees (`receipts/gsi_mentions.txt`):
  - `CHANGELOG.md:57`: eight failing arms.
  - `Makefile:451-452`: eight more elaborations and nine runs.
  - `measure_test_evidence.py:620`: one of eight defects.
  - `TESTING.md:267`: "eight field and notification mutants". That is seven field mutants plus the G8 push-count mutant.
- These match README `:496-517`.
- Nine runs means the clean re-run (`gsi_mutants.py:250-253`) plus eight mutants. "More" in the Makefile comment excludes the `notify` prerequisite's own elaboration and run. That is the sibling `crflic-mutants` convention (`Makefile:439-440`: "three more elaborations and four runs", 3 arms).
- No statement of the campaign still says seven.

## Per-lens coverage lines

[R306] PASS Conformance - `tb/verilator/milan_dp/README.md:488` against processor `docs/architecture/06_aecp_engine.md:295` (F06.13) and `05_acmp_engine.md:316` (F05.5) at `990f9652`, and assignment 5826348330 items 1-3, at 9d66cfe0 - the cited figures are the ones named, the delta changes no behaviour, and no acceptance criterion's evidence moved. The full-scope Conformance result is R306-2 at ancestor `224ec0e9`, and nothing in its scope changed since (`receipts/delta.raw`).

[R306] PASS RTL - `receipts/delta.raw` and `tb/verilator/milan_dp/Makefile:451-452` at 9d66cfe0 - no `hdl/` file, testbench source, recipe line or gitlink changed. The two Makefile lines are `#` comments, and `protocol-processor` is still `990f9652`. The R306-2 RTL result at ancestor `224ec0e9` stands unchanged in scope.

[R306] PASS Robustness - `tb/verilator/milan_dp/gsi_mutants.py:222-233` (selector bound) and `receipts/delta.raw` at 9d66cfe0 - the stated campaign size equals the executable table: `1..8` accepted, `0`/`9` refused rc 2. No executable path changed. The R306-2 Robustness result (G8 bounds, P1/P4, the duplicate mutant) at ancestor `224ec0e9` stands unchanged in scope.

[R306] PASS Tests - `receipts/verify_delta_run.txt` and `receipts/gate_*.txt` at 9d66cfe0 - every assigned gate is rc 0:
- `docs_check.py` (git mode, 0 findings) and in a `git archive` with no git and no submodule (0 findings);
- `gen_toc.py --verify-anchors` (168 fragments) and `--check`;
- `gen_toc.py --selftest` (1501/1501);
- `check_doc_paths.py` (842 paths);
- `check_em_dash.py --base c266432d` (0 findings, 339/339 arms);
- `measure_test_evidence.py --check` (ratchet PASS; runner contract OK) and `--selftest` (101/101);
- `check_py_idiom.py` and `--selftest` (54/54);
- `git diff --check` on the full PR range and on the delta.

The archive gate's negative control at `224ec0e9` fails with the original 2 findings. So the gate that went red is shown to detect the defect, and it is green now.

[R306] PASS Docs - `CHANGELOG.md:57`, `docs/testing/TESTING.md:267`, `scripts/measure_test_evidence.py:620`, `tb/verilator/milan_dp/Makefile:451-452` and `tb/verilator/milan_dp/README.md:488,496-517` at 9d66cfe0:
- The campaign size is consistent everywhere (8 arms, 8 elaborations, 9 runs).
- The processor references are commit-pinned, resolvable without the submodule, and keep their fragments and figure names.
- No obsolete text was restored.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | README `:488` figure citations vs processor F06.13/F05.5 at `990f9652`; assignment 5826348330; delta scope. The full acceptance mapping is R306-2, and it is untouched in scope. | R306-3 (delta), on R306-2 full scope at ancestor `224ec0e9a9fa129924bf8f0433cf70b4140f7bd2` | `9d66cfe0dc87ffe4a5f45691d5c86b041b050b38` |
| RTL | CLEAN | Delta raw diff (no `hdl/`, recipe or gitlink change); Makefile `:451-452` comment lines; gitlinks. The full RTL is R306-2, and it is untouched in scope. | R306-3 (delta), on R306-2 full scope at ancestor `224ec0e9a9fa129924bf8f0433cf70b4140f7bd2` | `9d66cfe0dc87ffe4a5f45691d5c86b041b050b38` |
| Robustness | CLEAN | `gsi_mutants.py` `MUTATIONS` (8) and selector bound probe; delta raw diff. G8 bounds, probes and the duplicate mutant are R306-2, and they are untouched in scope. | R306-3 (delta), on R306-2 full scope at ancestor `224ec0e9a9fa129924bf8f0433cf70b4140f7bd2` | `9d66cfe0dc87ffe4a5f45691d5c86b041b050b38` |
| Tests | CLEAN | Full assigned gate list (in clone and in a submodule-free `git archive`); negative control at `224ec0e9`; hosted `docs-check-no-git` success and `docs-check` step 9 success. The `obj_notify` 380/0 and `gsi-mutants` 9/9 results are R306-2, and they are untouched in scope. | R306-3 | `9d66cfe0dc87ffe4a5f45691d5c86b041b050b38` |
| Docs | CLEAN | CHANGELOG `:57`; TESTING `:267`; `measure_test_evidence.py:620`; Makefile `:451-452`; milan_dp README `:488,496-517`; pinned blob existence and hashes; anchors at the pin | R306-3 | `9d66cfe0dc87ffe4a5f45691d5c86b041b050b38` |

No `BLOCKER`, `MAJOR` or `MINOR` is open under any lens. Open SUGGESTIONs (R306-2 S1/S2, R307-2 S1/S2, R306-1 S1-S3) do not affect coverage.

## Real limits

- **Not run.** I did not run the full parent, processor, gPTP, Yosys or builder banks, the `milan_dp` sweep, `obj_notify` or `gsi-mutants`, Docker/act, `act_ci` or its selftest, hardware, or physical calibration. The delta changes no executable path, so the R306-2 executable results carry unchanged in scope. The manager's source banks are the public evidence for the rest.
- **Hosted snapshot** (`receipts/hosted_snapshot_final.txt`, 2026-09-25T04:02:19Z):
  - Success: `docs-check-no-git`, `bdd-conformance`, `changes`, `full-ci-gate`, `verilator-lint`, `wire-accountability`, and `Yosys shard 0/4`-`2/4`.
  - `docs-check` was in progress. Steps 1-25, including the step that failed at `224ec0e9`, were success, and steps 26-50 were pending.
  - Still in progress or queued: `elaborate`, `yosys-elaboration`, `Verilator shard 0/5`-`4/5` and `Yosys shard 3/4`.
  - `Physical gPTP` was **skipped**. A skipped context is not hardware proof.
- **Renderer dependencies.** The Markdown-renderer gates ran under a disposable environment in `scratch/`. It was installed from `tools/markdown/requirements.txt` with `--require-hashes` and binary wheels only, plus `pyyaml`.
- **Advisory output.** `measure_test_evidence.py --check` prints the advisory "the mutation ratchet can be lowered to 76". It is rc 0, and the delta cannot change that count, since it edits only a disposition string.
- **Clause text.** The Milan clause reading rests on the processor architecture pages at `990f9652`. The standard's own text is not in this clone.
- **Redaction.** Host path prefixes in receipts are replaced with `<clone>` and `<packet>`.
- **Clone restored** (`receipts/restore_verification.txt`):
  - HEAD and the index tree are both `5424e3e6...`, and there are 0 status entries, ignored files included. A `scripts/__pycache__/` left by the gates was removed.
  - Worktree and index diffs are empty.
  - All 885 tracked blobs re-hash and have the right modes.
  - The gitlinks are `efeb541a`, `e5dcea6e`, `990f9652` and `48ff7a7e`, and all three required submodules are checked out at them with 0 dirty entries.

## Pending manager duties

- Confirm that hosted `docs-check` concludes **success** at `9d66cfe0` (steps 26-50 were pending). This closes the last hosted half of R306-2 F1's verification.
- Confirm the remaining in-flight contexts at this exact head: `elaborate`, `yosys-elaboration`, `Verilator shard 0/5`-`4/5` and `Yosys shard 3/4`. Own hosted and act acceptance.
- Build and validate the final current-dev candidate at the merge turn, from source base `573f0052` and live dev `c533b4818df8b3f581df76aa0d1c6d5f55d20449`. It is distinct from this source-head review.
- Physical calibration is NOT RUN. Field skips are not hardware proof.
- Optionally, open an issue for the out-of-scope stale processor citations noted in R306-2.

## Receipts

- Portable reproduction: `verify_delta.sh <clone> <python> <scratch>` produces `receipts/verify_delta_run.txt`.
- Every published file is listed in `MANIFEST.sha256`.

R306-3 FINISHED
