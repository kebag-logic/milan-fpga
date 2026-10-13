[R626] POSITIVE - exact head b89a1ded1596030c4e0baf45a8509a20cbe04933

Round R626-4, independent composition acceptance for issue #727 / PR #728. All five lenses were applied. The composed tree introduces no defect beyond the reviewed sources. No open BLOCKER, MAJOR or MINOR was found. One inherited wording RESIDUE and two inherited optional SUGGESTIONs remain below. This verdict does not authorize merge or replace the manager's final candidate validation.

Candidate tree: `7aa454c189276935ebf891dc9deb5250a35aaa24`. Ordered parents: live dev `d5858bbee328cf8d2c39a99ec14203f5d0ddd123` and reviewed source `2c2f336979e4fdb1da444f041f37551e2c9175df`. Source base: `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`. Dev contains predecessor PR #724 (#716) and PR #721 (M8a).

The contract was reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the [frozen issue](https://github.com/kebag-logic/milan-fpga/issues/727), its [assignment](https://github.com/kebag-logic/milan-fpga/issues/727#issuecomment-6121794007), [round-2 ruling](https://github.com/kebag-logic/milan-fpga/issues/727#issuecomment-6126048117), [round-3 ruling](https://github.com/kebag-logic/milan-fpga/issues/727#issuecomment-6126613714), REQUIREMENTS.md section 8, workflow/driver interfaces, then diff/history and public evidence. Manager scope rulings were treated as public contract. The independent diff pass preceded reading the original review reports. [The independent verdict and ledger](receipts/independent-verdict.md) were written before those reports were opened. No private author material, management files or other checkout was read. [Public review start](https://github.com/kebag-logic/milan-fpga/pull/728#issuecomment-6134963179).

**Composition evidence.**

The intersection is exactly:

| Shared file | Predecessor contribution retained | PR #728 contribution retained |
|---|---|---|
| `docs/testing/CI_WORKFLOWS.md` | Four firmware jobs, their budgets and census; M8a's seventh gate-read page and elaboration prerequisites | Measured-time split, 60% bound, separate `maap` provenance, new-suite steps and corrected historical ownership description |
| `docs/testing/TESTING.md` | M8a memory, link, simulation, rule-table and mutation coverage description | The duration table as a prerequisite of both serial preflight and hosted workers |

Both shared documents equal an independent three-way text merge of their source versions. Every nonoverlapping changed entry retains its owning source's mode and blob. Semantic reading found no lost statement, contradictory table or changed anchor. In particular, four firmware jobs and five Verilator workers describe separate workflows and retain their separate deadlines. M8a's linker/memory checks run through the LiteX aggregate; they add no default Verilator suite.

The selector is byte-identical to the reviewed source. The exhaustive workflow, suite driver, tally reader and processor/axis gitlinks are identical across source base, source head, dev and candidate. All four trees have the same 63 suite Makefiles: 62 default suites and the separately scheduled physical suite. No predecessor creates an unmeasured suite. See [composition-audit.log](receipts/composition-audit.log), the four published diff receipts, and [composition_audit.py](scripts/composition_audit.py).

The actual candidate driver lists contain every default suite once. Independent summation of their recorded durations and overheads gives:

| Worker | Suites | Predicted seconds | 60% bound in seconds |
|---|---:|---:|---:|
| 0/5 | 15 | 4204 | 4320 |
| 1/5 | 16 | 4205 | 4320 |
| 2/5 | 14 | 4203 | 4320 |
| 3/5 | 16 | 4205 | 4320 |
| 4/5 | 1 | 2877 | 4320 |

The bound is independently computed as the workflow's 120 minutes times 36 seconds. Worker 4 owns only `milan_dp`; `tsn_fuzz` stays on 1 and `chmap_capture` on 3. The inventory exactly equals `SUITE_SECONDS`, with no provisional entry.

**Focused candidate validation.**

| Command or check | Result and receipt |
|---|---|
| `python3 scripts/suite_shards.py --selftest` | PASS; inventory, bounds, boundary controls, setup owners, provisional figures and process-seed comparisons; [log](receipts/suite-shards-selftest.log) |
| `bash scripts/run_all_suites.sh --shard I/5 --list`, I=0..4 | All rc 0; 62-suite disjoint union; `receipts/shard-0.log` through `shard-4.log` |
| `python3 scripts/ci_events.py --check` | 2016 contract items pass; [log](receipts/ci-events-check.log) |
| `python3 scripts/ci_events.py --selftest` | 2828 arms pass, including workflow records, worker counts, ownership and firmware budgets; [log](receipts/ci-events-selftest.log) |
| `python3 scripts/ci_events.py --firmware-census` | `preserved: true`; [census](receipts/firmware-census.log) |
| `python3 scripts/ci_scope.py --selftest` | PASS, including the M8a reader population; [log](receipts/ci-scope-selftest.log) |
| `python3 scripts/docs_check.py` | Zero findings; 205 Markdown files and 1278 scrubbed text files; [log](receipts/docs-check.log) |
| `python3 scripts/gen_toc.py --check` and `--verify-anchors` | PASS; 145 annotated contents lists and 485 cross-page links; [TOC](receipts/toc-check.log), [anchors](receipts/toc-anchors.log) |
| `python3 scripts/check_em_dash.py --base d5858bbee328cf8d2c39a99ec14203f5d0ddd123` | Zero findings over 43 added lines; 339 controls pass; [log](receipts/em-dash.log) |
| `python3 scripts/check_doc_paths.py`; `check_doc_style.py`; `check_py_idiom.py` | All rc 0; corresponding receipts record their scope |
| `git diff --check d5858bbee328cf8d2c39a99ec14203f5d0ddd123 HEAD` | rc 0; [receipt](receipts/diff-check.rc) |

The first TOC/anchor/em-dash attempts exited 2 because the pinned Markdown dependency was absent. A hash-locked installation under packet scratch supplied it; all three then passed. Initial refusal receipts are retained. No shared installation was modified. Independent commands ran concurrently under a foreground supervisor that joined every child, never exceeding eight concurrent checks.

The documented new-suite procedure was also replayed on a disposable archive of this exact candidate, using the inspected [published author helper](https://github.com/kebag-logic/milan-fpga/blob/dfdd39ff0eb50992be0cca34797ddd41e556dc01/review-evidence/727-r1/author-r3/r3-new-suite-steps.py). A suite without a duration fails self-test with rc 1 and sharded selection with rc 2. Its provisional 1800 seconds is accepted as a figure but fails the five-worker bound. Applying the documented sixth-worker edits makes selector self-test, workflow check and workflow self-test pass: 2017 contract items and 2828 arms. The firmware census still reports preservation. Six real driver lists cover 63 suites exactly once and retain the specialized owners. [Probe receipt](receipts/new-suite-probe.log), [portable probe](scripts/probe_new_suite.py). This probe ran no suite, build or full serial preflight.

**Public source evidence and prior findings.**

The source reviews are [R626-3](https://github.com/kebag-logic/milan-fpga/pull/728#issuecomment-6130305824) and [R627-3](https://github.com/kebag-logic/milan-fpga/pull/728#issuecomment-6130308095), both POSITIVE at `2c2f336979e4fdb1da444f041f37551e2c9175df`. The [published author evidence](https://github.com/kebag-logic/milan-fpga/tree/dfdd39ff0eb50992be0cca34797ddd41e556dc01/review-evidence/727-r1/author-r3) includes the new-suite replay and mutation receipts inspected here. These are source evidence, not executions of the full banks at this candidate.

The [manager's acceptance-3 comment](https://github.com/kebag-logic/milan-fpga/pull/728#issuecomment-6130352848) is corroborated by source run 38283356358 job metadata. Workers 0..4 executed successfully in 4200, 2726, 4195, 4182 and 2845 seconds, all below 4320. The metadata names source head `2c2f3369`, not candidate `b89a1ded`. The physical gPTP job was skipped. See [source-hosted-jobs.json](receipts/source-hosted-jobs.json). No manager source bank is claimed or inferred, and no hosted execution at the composition head is claimed.

Every prior public finding was resolved or retained as follows. Original reviewer lens labels are preserved. The PR has no additional submitted-review or inline-comment findings; [channel receipt](receipts/public-review-channels.json).

| Prior finding | Disposition at this candidate | Evidence |
|---|---|---|
| R626-1/F1 = R627-1-F1; MINOR, Tests | RESOLVED | `scripts/suite_shards.py:723-730` independently requires 36 seconds per timeout minute. Candidate self-test passes; the unchanged source's published mutations detect all three required bound-loosening cases. |
| R626-2/F1; MINOR, Docs and Robustness | RESOLVED | `suite_shards.py:54-87,239-244,336-382`; `TESTING.md:513-519`. Candidate disposable replay confirms the missing-duration, provisional-bound and expanded-worker stages work alongside the new firmware census. |
| R626-1/R1 = R627-1-R1; RESIDUE, Docs | RESOLVED | `CI_WORKFLOWS.md:238-241` retains the explicit `maap` pull-request provenance exception. |
| R627-1-R2; RESIDUE, Docs | RESOLVED | Current PR body distinguishes warm caches from worker 1's packet-generator build. |
| R626-2/R2; RESIDUE, Docs | RESOLVED | Current PR body distinguishes table-free serial selection from table-dependent preflight. |
| R626-1/S1 = R626-2/S2; SUGGESTION, Robustness and Tests | RESOLVED | `suite_shards.py:800-808` refuses head-arm skipping when any checkout input exists. Implementation is source-identical; source mutation/cancellation evidence remains applicable. |
| R626-1/S2; SUGGESTION, Tests | RESOLVED | `suite_shards.py:704-707,732-739`; candidate zero-duration and extra-worker controls pass. |
| R626-2/S1; SUGGESTION, Tests | RESOLVED | `suite_shards.py:857-881`; candidate separate-process seed comparisons pass; the source's hash-tie mutation remains detected. |
| R626-1/R2 = R626-2/R1 = R626-3/R1 = R627-3-R1; RESIDUE, Docs | RETAINED as R626-4-R1 | Workflow comment remains unchanged, as directed by the public rulings. |
| R626-3/S1; SUGGESTION, Docs | RETAINED as R626-4-S1 | New-suite steps still omit an explicit list of prose worker-count updates. |
| R626-3/S2; SUGGESTION, Tests | RETAINED as R626-4-S2 | The head-level provisional-check call is unchanged; the present provisional set is empty. |

R627-2 and R627-3 introduce no additional unresolved blocking finding. No source-only mutation campaign was repeated merely to replace existing source coverage.

**Retained findings.**

R626-4-R1 - RESIDUE - Docs - `.github/workflows/rtl.yml:136-137`.
Authority/evidence: the comment says “four hashed workers”; the selector uses measured durations. Acceptance 2 and the round-2/3 rulings preserve workflow bytes and route this wording to #495. Impact: comment wording only; no executed command, measurement, generated artifact, verdict, clause claim or privacy rule changes. Exact required fix: replace `four hashed workers` with `four workers balanced by measured hosted time (#727)`. Verification: a comment-only diff and a passing `ci_events.py --check`. The manager must retain it on the residue checklist; moving the paperwork does not resolve the wording.

R626-4-S1 - SUGGESTION - Docs - `scripts/suite_shards.py:63-82`.
Authority/evidence: the new-worker steps name code pins, while `CI_WORKFLOWS.md:229`, `TESTING.md:518` and `tb/verilator/milan_dp/README.md:442` also state worker counts. Impact: a future worker expansion can leave prose stale; no present count is wrong, and AGENTS.md already requires documentation updates. Optional outcome: add a bullet naming the affected documentation. Verification: a future expansion updates all such counts and passes the documentation checks. Retained from R626-3/S1.

R626-4-S2 - SUGGESTION - Tests - `scripts/suite_shards.py:817,821-826`.
Authority/evidence: the public R626-3 mutation deletes the head's `provisional_problems` call without failing; the function's four planted controls are independent of that call. The candidate retains the exact source code and an empty provisional set. Impact: future provisional figures depend on retaining the head call. Optional outcome: exercise the head invocation through the same helper used by planted controls. Verification: deleting that invocation must fail a named control while the clean head passes. This mutation was not rerun in composition review. Retained from R626-3/S2.

**Reviewer-owned ledger.**

“Yes” identifies composition interactions examined in this round. “No” preserves named source coverage after checking the composition boundary; it does not claim a new source review.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Yes: frozen #727 acceptance and rulings; shared policy text; `suite_shards.py:129-203,387-408`; actual inventory/lists; independent load sums; source-hosted evidence distinguished from candidate | R626-4, retaining R626-3/R627-3 source coverage | b89a1ded1596030c4e0baf45a8509a20cbe04933 |
| RTL | CLEAN | No interaction: candidate diff adds no HDL, interface, suite recipe or gitlink change; `composition-audit.log` proves selector/source identity and unchanged exhaustive workflow, driver, tally and pins. M8a code retains dev's exact entries | R626-3 and R627-3 source reviews; boundary verified by R626-4 at b89a1ded | 2c2f336979e4fdb1da444f041f37551e2c9175df |
| Robustness | CLEAN | Yes: live inventory/duration agreement; selector refusal/boundary/owner controls; predecessor classifier and workflow contracts; disposable six-worker/new-suite replay | R626-4 | b89a1ded1596030c4e0baf45a8509a20cbe04933 |
| Tests | CLEAN | Yes: `ci_events.py` record/ownership/count pins and 2828 controls; firmware census; 62-suite union; M8a gate-read registry; new-suite replay and preserved firmware population | R626-4 | b89a1ded1596030c4e0baf45a8509a20cbe04933 |
| Docs | CLEAN | Yes: `CI_WORKFLOWS.md:44-150,229-264,371-381,1265-1277`; `TESTING.md:513-525,704-726`; two-sided merge comparison; documentation, paths, TOCs and anchor receipts. R1 is RESIDUE; S1 optional | R626-4 | b89a1ded1596030c4e0baf45a8509a20cbe04933 |

**Integrity, limits and manager duties.**

[Final integrity](receipts/final-integrity.log) verifies the detached exact head/tree, all 1302 candidate tracked blobs by raw byte hash and mode, the exact stage-zero index and absence of hidden index flags. Registered required submodules match their gitlinks and every tracked byte/mode/index: protocol processor `2ad2f845dd583f8310075fa2380cb60a04fd091a` (562 blobs), gPTP processor `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9` (104), and axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce` (214). All are clean. The uninitialized external and lwSRP gitlinks were unchanged and unused by these focused checks. Candidate source bytes were never edited; only packet scratch contained probe edits.

No full parent, processor, synthesis or builder bank, hardware operation, local workflow replica, or host orchestration self-test ran here. No commits, pushes, GitHub writes, merges, author contact or delegated review occurred. Physical calibration: NOT RUN. Field skips and desk checks are not hardware proof. Recorded duration headroom remains a prediction with runner/cache variance; it is not a timing guarantee for every future run.

The manager still owns final current-dev candidate construction and builder/native-bank validation at the merge turn, publishing those receipts, hosted and local-replica acceptance, review completion, authorized merge, post-merge containment, and issue/project closure. The supplied validation base is `d5858bbee328cf8d2c39a99ec14203f5d0ddd123`; a changed dev tip requires renewed candidate assessment. This report supplies composition acceptance only and must not be described as a manager source bank or a full candidate-bank pass.

Portable scripts are under `scripts/`; their raw outputs and return codes are under `receipts/`. Reproduction entry points are `run_checks.py`, `composition_audit.py`, `probe_new_suite.py` and `verify_integrity.py`, using `--repo` and, where applicable, `--packet`. `run_checks.py --python` selects an isolated interpreter with the hash-locked Markdown requirements. The new-suite probe requires a fresh scratch destination. `MANIFEST.sha256` lists every publishable receipt and script; scratch is excluded.

R626-4 FINISHED
