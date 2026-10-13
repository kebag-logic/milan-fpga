[R632] POSITIVE - exact head d8f0108803ffc2c85f398ba3d56e858ffffc72ee

R632-8, cleared-context composition review of issue #730 / PR #731 on the merge-train candidate. Tree `d68712a36ddd5df521863c79514c7cfed07db5fe`. Parents: train candidate `6758fe0216955c96f37b52d7129509586c9c0a8c` (live dev `49da9fd974e8805d56c90e29dcfcb67994c2c430` plus #726, B16 and 697c) and PR source head `b341e875d87c6aa2be355bad17f373782517f723` (base `dc4d06cbfec209cc2ff76806f4b49c51f46639ae`). All five lenses were applied to the composition. No BLOCKER, MAJOR or MINOR finding is open. The one carried RESIDUE is PR-body wording that was already open at the source head. The composed tree introduces no defect beyond the reviewed sources. This review is not merge authorization.

## 1. What the composition is

- **Clean merge.** `git merge-tree --write-tree 6758fe02 b341e875` gives `d68712a3`, which is the candidate's tree. The merge needed no resolution work (`receipts/merge_tree.txt`).
- **PR delta on the candidate.** `6758fe02..d8f01088` changes only `docs/testing/CI_WORKFLOWS.md` (+152/-5 in this view) and `scripts/act_ci.py`. Its hunk bodies match `dc4d06cb..b341e875` byte for byte; only the line offsets differ. The PR changes no workflow, gitlink, RTL, firmware or suite.
- **Overlapping files.** This PR and its predecessors both change two files (`receipts/predecessor_overlap.txt`):
  - `docs/testing/CI_WORKFLOWS.md`: changed by #721 (M8a, +18/-1), #727 (PR #728, +36/-19) and 697c (+71/-6). #726 and B16 leave it unchanged.
  - `scripts/act_ci.py`: changed by **697c** (`fea74c5c8`, +39/-4). That commit adds `third_party/tsn-c-stack` to `TRUSTED_SUBMODULES`, adds `selftest_stack_manifest`, and updates the manifest arms. The scope note named only CI_WORKFLOWS.md, so I reviewed this second overlap as well. dev, #726 and B16 leave this file unchanged.
- **Semantic interactions checked:**
  - the workflow inventory that the PR's concurrency derivation reads. 697c changes `rtl-fast.yml`, which goes from 10 to 12 jobs, and one `run:` line in `rtl.yml`;
  - the trusted submodule registry, now six entries and six gitlinks;
  - the derived CPU-range plan;
  - the docs gate inventories, TOC and anchors, the em-dash gate and the CI event contract;
  - the Python idiom and bare-metal ratchets that read `act_ci.py`.

## 2. Evidence produced in this round (composed tree)

All gates ran in the foreground on the candidate clone. The interpreter was CPython 3.14.7 with PyYAML 6.0.3. The Markdown-renderer gates used a disposable venv holding exactly `tools/markdown/requirements.txt` (`receipts/gates_md/renderer_freeze.txt`).

| Gate | rc | Receipt |
|---|---|---|
| `docs_check.py` | 0 (0 findings, 206 md files) | `receipts/gates/docs_check.log` |
| `check_doc_style.py`, `--selftest` | 0, 0 | `receipts/gates/check_doc_style*.log` |
| `gen_toc.py --check` / `--verify-anchors` / `--selftest` | 0 / 0 (488 fragments) / 0 (1501 arms) | `receipts/gates_md/gen_toc_*.log` |
| `check_em_dash.py --base 6758fe02` (composed parent) | 0 (0 of 167 added lines) | `receipts/gates_md/em_dash_parent.log` |
| `check_em_dash.py --base 49da9fd9` (live dev) / `--base dc4d06cb` (PR base) / `--selftest` | 0 / 0 / 0 | `receipts/gates_md/em_dash_*.log` |
| `check_doc_paths.py`, `docs/DOC_MAP.gen.py --check`, `check_archive.py` | 0, 0, 0 | `receipts/gates/` |
| `ci_events.py --check` / `--selftest` | 0 (2169 items) / 0 (3064 arms) | `receipts/gates/ci_events_*.log` |
| `check_py_idiom.py` / `--selftest` | 0 (long function 9<=9, long module 10<=10) / 0 | `receipts/gates/check_py_idiom*.log` |
| `check_baremetal_only.py --check` / `--selftest` | 0 / 0 | `receipts/gates/check_baremetal_only*.log` |
| `measure_naming.py --check`, `measure_fail_fast.py --check`, `measure_test_evidence.py --check`, `check_hygiene.py --check`, `check_todo_ownership.py` | all 0 | `receipts/gates/` |
| `git diff --check 6758fe02 HEAD` | 0 | `receipts/gates/git_diff_check.log` |

The first pass ran the TOC and em-dash gates without the pinned renderer, and they refused with rc 2 ("renderer not installed"). They were re-run with the renderer and passed; the table shows those re-runs.

**Independent derivation.** `scripts/derive_concurrency.py` parses the four replayed workflows with YAML's base loader. It does not import the runner (`receipts/derive_concurrency.txt`). On the composed tree, on the source head and on the train candidate the derived concurrency is the same: `rtl-full` 4 (`verilator-shards` and `yosys-shards`, with no `max-parallel`); `docs`, `elaborate` and `rtl-fast` 1. The composed `rtl-fast` has 12 jobs, none with a matrix.

**Parse-only composition proof for `scripts/act_ci.py`.** `scripts/compose_independence.py` parses each file with `ast` and does not execute it (`receipts/compose_independence.txt`):
- The PR changes 77 top-level names. 697c changes 4: `TRUSTED_SUBMODULES`, `selftest_submodule_manifest`, `selftest_lwsrp_manifest` and `selftest_stack_manifest`. The two sets do not overlap.
- Every composed top-level definition equals the side that changed it.
- No 697c definition names anything the PR changed.
- The only PR definition that names a 697c change is `selftest`, through the call `selftest_submodule_manifest(tally, git_fixture)`. That call is byte-identical to the one at the base.
- `initialize_required_submodules`, the only consumer of `REQUIRED_SUBMODULES`, is identical at base, source and composed.
- A line-level diff gives the same result: the composed file equals the source file plus exactly the 697c delta.

## 3. Lens results (exact head d8f0108803ffc2c85f398ba3d56e858ffffc72ee)

[R632] PASS Conformance - `scripts/act_ci.py:2095-2146` (`job_container_width`, `replay_container_concurrency`), `.github/workflows/rtl.yml:153-157,455-459`, `.github/workflows/rtl-fast.yml` (12 jobs, none with a matrix), `receipts/derive_concurrency.txt` - Acceptance 2 (derived, not mirrored) gives the same plan on the composed workflows as on the source: rtl-full 4, the others 1. Ranges and slot blocks (`act_ci.py:4676-4682,4724-4738`) are unchanged. Acceptance 3 (no workflow, step or job change) still holds: `6758fe02..d8f01088` touches no `.github` file. 697c's workflow edits are its own and add no matrix. Acceptances 4 and 5, and the live part of 3, stay deferred under ruling 6131815815.

[R632] PASS RTL - `receipts/merge_tree.txt`, `receipts/compose_independence.txt`, `scripts/act_ci.py:227-262` (six-entry `TRUSTED_SUBMODULES`, `REQUIRED_SUBMODULES`), `:1807` (`initialize_required_submodules`) - The composition touches no HDL. In the runner, the 697c registry change and the PR's CPU-range and monitor architecture share no definition, and neither side's code depends on the other's. The interface contract is unchanged: six gitlinks in the index match six `.gitmodules` stanzas.

[R632] PASS Robustness - `receipts/compose_independence.txt`, `scripts/act_ci.py:12946-13116` (`selftest_submodule_manifest`, `selftest_lwsrp_manifest`, `selftest_stack_manifest`), `:4724-4738` - The PR's refusals (concurrency above the slot ranges, a host without CPUs, an unreadable `max-parallel`), its signal-mask and cleanup paths, and 697c's manifest refusals (omitted, redirected, dropped or extra tsn-c-stack) are disjoint definitions. Neither side's failure path reads state the other side changed. The `selftest` order around the manifest arms is unchanged.

[R632] PASS Tests - `receipts/compose_independence.txt`, `receipts/gates/ci_events_selftest.log`, `receipts/gates/check_py_idiom*.log`, `receipts/gates/check_baremetal_only*.log`, `scripts/act_ci.py:7176-7252` (`selftest_job_concurrency` shipping arm), `:14940-14995` (shipping dry-run arm) - The PR's shipping-workflow arms read only matrix and `max-parallel` shapes, and these give the same derivation on the composed workflows. The dry-run arm stubs out `initialize_required_submodules` and `validate_checkout`, so 697c's registry cannot reach it. The 697c arms reach no PR-changed definition. Every other gate that reads either file passes on the composed tree. I did not execute `act_ci.py --selftest` on the composed tree, because the round's rules forbid running it on the host. See the limits below.

[R632] PASS Docs - `docs/testing/CI_WORKFLOWS.md:285-305` (#727 split), `:320-325` and `:60-150` (697c firmware and TSN stack jobs), `:1342-1355` (M8a SDK member), `:1720-1729` (six gitlinks, five public pins), `:1838-1841`, `:1844-1856`, `:1872-1889`, `:1910-1943`, `:1948-1991`, `:2277-2287`, `:2497`, `:2630`; `receipts/gates*/` - The merged page states both sides correctly:
- The PR's "five Verilator workers, four Yosys workers" matches #727's five-worker split and the composed `rtl.yml`.
- "`docs`, `elaborate` and `rtl-fast` derive 1" holds with 697c's two added non-matrix jobs.
- The per-container ranges, the reservation until destroy, the signal-mask and closing-precedence text, and the 20N slot blocks are unchanged from the reviewed source and agree with the code.
- 697c's "four at once, the hosted runner's CPU count" and its four-CPU replica figures stay true, because every leg still has four CPUs.
- M8a's text and 697c's six-gitlink and five-pin text sit in sections the PR does not touch.
- The doc, TOC, anchor, em-dash, doc-map and CI-event gates are green. Nothing became false in combination.

## 4. Findings

No new finding at this head.

Prior public findings, re-checked at this head:

| ID | Severity, lens | Disposition at d8f01088 |
|---|---|---|
| R632-7-R1 = R633-7-R1 | RESIDUE, Docs | **RETAINED.** The PR body's Status section still says the PR head is `73b8dcd6` and that Round 7 is "local and unpushed", but the published head is `b341e875` (`receipts/pr731-body-snapshot.md`). This is wording only. Exact fix: replace the three Status lines, from the branch/head line through "The manager owns its publication and re-review.", with "`730-act-cpusets` -> `dev`, published PR head `b341e875d87c6aa2be355bad17f373782517f723`. The manager owns publication of the reviews and the merge-candidate validation." It goes to the residue checklist. It does not affect the verdict. |
| R632-7-S1, R632-7-S2, R632-7-S3; R632-6-S1, R632-6-S2, R632-6-S3 (and their earlier aliases) | SUGGESTION, Tests or Robustness | **RETAINED, optional.** The definitions they name are byte-identical in the composed file (AST proof), so the composition changes none of them. |
| All earlier F-series findings (R632-1..6, R633-1..5) | BLOCKER/MAJOR/MINOR, various | **RESOLVED** at the source head per R632-7 and R633-7. The composed file carries the source definitions unchanged, so they stay resolved. |

I read the prior findings only after finishing my own pass over the diff and gates.

## 5. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #730 acceptance and rulings; `act_ci.py:2095-2146,4676-4738`; composed workflows; `receipts/derive_concurrency.txt` | R632-8 (composition); source: R632-7, R633-7 | d8f0108803ffc2c85f398ba3d56e858ffffc72ee (source rounds at b341e875d87c6aa2be355bad17f373782517f723) |
| RTL | CLEAN | `receipts/merge_tree.txt`; `receipts/compose_independence.txt`; `act_ci.py:227-262,1807`; gitlinks and `.gitmodules` | R632-8 (composition); source: R632-7, R633-7 | d8f0108803ffc2c85f398ba3d56e858ffffc72ee (source rounds at b341e875d87c6aa2be355bad17f373782517f723) |
| Robustness | CLEAN | `receipts/compose_independence.txt`; manifest refusal arms; PR refusal and cleanup definitions (byte-identical to source) | R632-8 (composition); source: R632-7, R633-7 | d8f0108803ffc2c85f398ba3d56e858ffffc72ee (source rounds at b341e875d87c6aa2be355bad17f373782517f723) |
| Tests | CLEAN | `receipts/compose_independence.txt`; `act_ci.py:7176-7252,14940-14995`; `receipts/gates/` (ci_events, idiom and ratchet gates) | R632-8 (composition); source: R632-7, R633-7 | d8f0108803ffc2c85f398ba3d56e858ffffc72ee (source rounds at b341e875d87c6aa2be355bad17f373782517f723) |
| Docs | CLEAN (RESIDUE R632-7-R1 carried) | composed `CI_WORKFLOWS.md` at the lines cited above; `receipts/gates/`, `receipts/gates_md/`; PR body snapshot | R632-8 (composition); source: R632-7, R633-7 | d8f0108803ffc2c85f398ba3d56e858ffffc72ee (source rounds at b341e875d87c6aa2be355bad17f373782517f723) |

The composition touches the scope of all five lenses: both overlapping files sit under Conformance, Tests and Docs, and the runner module sits under RTL and Robustness. Each lens was therefore applied in this round rather than inherited.

## 6. Real limits

- **`act_ci.py --selftest` was not run on the composed tree.** This round's rules forbid running the runner or its self-test on the host. My judgment that it passes on the composed tree rests on three things: the parse-level and line-level proof that the two sides are independent; the source head's hosted `docs-check` step "Local act runner contract gate" concluding success (`receipts/hosted_source_docs_check_steps.json`, job 115136282389); and the published Round 7 author receipts (531 ok at the source head). That job runs a pull-request event's checkout, which does not include the 697c delta. **I have not seen an executed self-test on this tree.** I expect the composed self-test to run 4 arms more than the source's 531, from 697c's tsn-c-stack arms.
- One interpreter only, CPython 3.14.7. The hosted documentation runner uses 3.12.
- The candidate `d8f01088` and the train candidate `6758fe02` are not on GitHub, so no hosted run exists at this head. At the time of the snapshot, the source head's Verilator shards were still in progress; `docs-check`, `rtl-fast`, `elaborate`, `wire-accountability` and the Yosys shards had succeeded. The manager owns hosted and act acceptance.
- No Docker, act, replay, live dry-run, hardware, builder bank or native bank was run. Physical calibration NOT RUN. Field skips are not hardware proof. No mutation campaign was needed: the composition changes no PR-owned definition.
- Restoration: no tracked file was modified. HEAD, index and tree are `d68712a3`, and the six gitlinks match HEAD. The bytecode caches the gates wrote were removed (`receipts/restore_check.txt`).

## 7. Pending manager duties

1. Execute `scripts/act_ci.py --selftest` on the composed tree or on the final current-dev candidate, inside the disposable CI job boundary (the hosted `docs-check` "Local act runner contract gate" or the manager's bank), and link the receipt.
2. Run current-dev merge-candidate validation with the builder and native banks, plus exact-head hosted acceptance, including the `verilator-suites` and `yosys-portability` evidence.
3. Carry RESIDUE R632-7-R1 / R633-7-R1 (the exact PR-body fix in section 4) to the residue checklist.
4. After the merge: issue #730 acceptance 3 (live `nproc` and same-head verdict), acceptance 4 (before/after wall clock and slot memory peak), and optional acceptance 5, under ruling 6131815815; then post-merge containment. The issue stays open for these (`Relates to #730`).
5. Publish this packet: REPORT.md and the files listed in MANIFEST.sha256.

R632-8 FINISHED
