[R277] POSITIVE - exact head 00db64eb1e6e0c9bdb9f35ec5e37ebe6e00d550b

Round R277-6: an external, independent delta review of PR #555 (issue #387), the executor's round 4, commissioned by assignment 5821889812. The tree is `5523c0bcc1383f6392fa3c1269d1e5e08223bdbb`. The source base is `57456af96b3127b9d309a995bbbd35a6113ce52d`. The previous head, covered by this reviewer in R277-5, is `0f003fab3303858ba4db955ad3c0512e67a8018b`.

## Verdict

- R277-5 was NEGATIVE on a single Docs MINOR, F1: four current statements still gave 2700 s as the `milan_dp` budget.
- F1 is **closed** at this head. Commit `00db64eb` touches only those four files. Its changes are text only.
- No BLOCKER, MAJOR or MINOR is open under any lens.
- The R277-5 ledger stands for every artifact this delta does not touch. Docs and Tests were re-applied at this head, because files in their scope changed. Conformance was re-checked against decision 5820240308.
- The verdict and ledger were drafted before any other reviewer's report was read.

## Findings

No new BLOCKER, MAJOR or MINOR findings.

### S3 SUGGESTION - Docs - `tb/verilator/milan_dp/render_mutants.py:37`

- The corrected docstring line is 96 characters wide. The lines around it wrap at about 78.
- No gate enforces a width. The file already has lines of 80 to 89 characters, and `py_compile` and the docs gates pass.
- Re-wrapping the line is optional.

## F1 (R277-5, Docs MINOR): closed

| Required outcome (R277-5) | Evidence at `00db64eb` |
|---|---|
| No current page or runner docstring states 2700 s as the `milan_dp` budget | All four statements now give 3600 s:<br>`TESTING.md:166` "1800 seconds per suite, and 3600 seconds for `milan_dp`".<br>`RUNNING_TESTS.md:79-80` "3600 seconds under decision 5820240308".<br>`milan_dp_gptp/README.md:31-32` "its own 3600-second budget", which decision 5820240308 sets.<br>`render_mutants.py:37` "suite_timeout = 3600 s (decision 5820240308)". |
| Each statement gives 3600 s under decision 5820240308, or points to `CI_WORKFLOWS.md` | All four link to or name decision 5820240308.<br>`TESTING.md:167-168` replaces the #444 basis ("measured hosted worst case plus a stated margin") with "sets this deadline from recorded hosted samples". It keeps the pointer to the table in `CI_WORKFLOWS.md`.<br>The basis matches the decision's own terms: 3600 s, a 32% margin at the worst sample, and the samples recorded in `CI_WORKFLOWS.md`. |
| Historical sentences stay marked as history | `CI_WORKFLOWS.md:167` reads "That 1800 s deadline became 2700 s under #444."<br>`CI_WORKFLOWS.md:185` reads "The `a21cd358` sample left 240.1 s of 2700 s: 8.9%."<br>Both are past-tense records of the sample that triggered the decision. They are intentionally unchanged, and the file is not in the delta. |
| The selftest's planted mutation keeps the old value | `measure_test_evidence_selftest.py:294` `("SUITE_TIMEOUT:-3600", "SUITE_TIMEOUT:-2700")` is intentionally unchanged: it proves that a reversion to 2700 s is rejected.<br>`budget_pin_probe.py` confirms the live runner is accepted and the 2700 s reversion is rejected with "the declared 1800/3600/5400-second suite budgets changed" (`receipts/budget_pin_probe.log`). |
| `git grep 2700` returns only the history lines and the planted mutation | `receipts/residual_2700.log` lists `CI_WORKFLOWS.md:167`, `:185` and `measure_test_evidence_selftest.py:294`.<br>The other two hits are unrelated: the literal `12700` at `mmcm_servo/sim_rails.cpp:154` and a SHA-256 substring at `act_ci.py:7660`.<br>A wider search finds no other current `milan_dp` budget statement. It covered `2,700`, "forty-five", "45 min", `#444` and `issues/444`, and the `timeout-minutes` values in `.github/`. The `#444` comment at `rtl.yml:137` concerns the fifth shard, not the deadline.<br>The PR body (`receipts/pr555_head_and_body.txt`) states 3600 s and calls 2700 s "the former" budget. |
| The docs gates still pass | `docs_check.py` reports 0 findings across 165 md files. `check_doc_style.py`, `check_gptp_docs.py`, `DOC_MAP.gen.py --check` and `check_solution_docs.py` all report OK (`receipts/*.log`).<br>`check_em_dash.py` could not judge on this host (see Real limits). The delta's added lines contain no em dash (`receipts/delta_scope.log`, count 0). |

## Delta scope

- `git diff --name-status 0f003fab..00db64eb` lists exactly four modified files (`receipts/delta_scope.log`):

  | File | Lines added / removed |
  |---|---|
  | `docs/testing/RUNNING_TESTS.md` | +2 / -1 |
  | `docs/testing/TESTING.md` | +2 / -2 |
  | `tb/verilator/milan_dp/render_mutants.py` | +1 / -1 |
  | `tb/verilator/milan_dp_gptp/README.md` | +2 / -1 |

- In `render_mutants.py`, only the module docstring changed. The AST after the docstring is identical at both heads (`receipts/ast_probe.log`).
- The delta changes no RTL, testbench code, runner, workflow or submodule gitlink.
- `57456af9` is an ancestor of the head.

## What was checked, per lens (artifact at this head)

- **Conformance.**
  - Decision 5820240308 (issue #387) sets the budget to 3600 s, with a 32% margin at the worst sample, and records the samples in `CI_WORKFLOWS.md`.
  - These all agree with it:
    - `run_all_suites.sh:240-248` (`${SUITE_TIMEOUT:-3600}`);
    - `measure_test_evidence.py:716-724`;
    - `CI_WORKFLOWS.md:159,171-190`;
    - the four corrected statements;
    - `milan_dp/README.md:244,864`;
    - the PR body.
  - The hosted shards allow 120 minutes (`rtl.yml:152`).
  - At this head, the hosted `milan_dp` window is 2435.2 s. That leaves 1164.8 s, or 32.4% of 3600 s, above the decision's 10% re-split trigger (`receipts/milan_dp_window_head.txt`).
  - Frozen acceptance and the other rulings: R277-5 stands, and the delta does not touch them.
- **RTL.** The delta contains no path under `hdl/` and no build input, and the code in `render_mutants.py` is AST-identical. R277-5 stands.
- **Robustness.** No behavior changed. The runner's timeout path (exit 92) and the budget contract are unchanged, and the contract still rejects the reverted budget (`receipts/budget_pin_probe.log`). R277-5 stands.
- **Tests.** Re-applied, because a file under `tb/` changed.
  - The change is to a docstring only (`receipts/ast_probe.log`), and `py_compile` passes.
  - `measure_test_evidence_selftest.py` exits 0, and its planted-mutation arm is intact and fires.
  - Hosted runs at this head (`receipts/hosted_checks_00db64eb.tsv`, `receipts/milan_dp_window_head.txt`):
    - Every executed context read so far succeeded. That includes Verilator shards 0-4/5, Yosys shards 0-3/4, `rtl-fast`, `docs-check`, `elaborate`, `verilator-lint` and `bdd-conformance`.
    - Shard 4/5 ran `milan_dp` to PASS: 9785 checks, 0 in-suite failures, 0 timed out. The count is the same as at `0f003fab`, as expected for a docs-only delta.
    - The `verilator-suites` aggregate was still in progress when read.
    - The Physical gPTP context was skipped by design (nightly and manual). A skip is not evidence.
- **Docs.** Re-applied. Evidence: the four corrected statements and their paragraphs, the history lines in `CI_WORKFLOWS.md`, the residual search, the PR body and the docs gates, all listed above.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Decision 5820240308 against `run_all_suites.sh:240-248`, `measure_test_evidence.py:716-724`, `CI_WORKFLOWS.md:159,171-190`, `TESTING.md:166-168`, `RUNNING_TESTS.md:78-80`, `milan_dp_gptp/README.md:31-32`, `render_mutants.py:37`, the PR body, and the hosted window (32.4%). Also R277-5's artifacts, which the delta does not touch: the datapath, `KL_media_clock_restart.sv`, gmstep, the option-off/ax1x1 legs and `RENDER-SETTIME` | R277-6 (budget and decision); R277-5 (the rest) | `00db64eb1e6e0c9bdb9f35ec5e37ebe6e00d550b`; R277-5 at ancestor `0f003fab3303858ba4db955ad3c0512e67a8018b`, with no in-scope artifact changed since |
| RTL | CLEAN | R277-5: `KL_media_clock_restart.sv:196-259`, the datapath re-base, restart and render wiring, `lint_rtl --check`, `check_rtl_source_lists`. This round: the delta has no RTL or build input (`receipts/delta_scope.log`) | R277-5 | `0f003fab3303858ba4db955ad3c0512e67a8018b`, an ancestor of `00db64eb`, with no RTL-scope change since |
| Robustness | CLEAN | R277-5: property probe 36/36 with 6/6 kills; the option-off, ax1x1 and true-ratio legs; `render_mutants.py` 6/6. This round: the timeout/exit-92 contract is unchanged, and the budget pin rejects 2700 s (`receipts/budget_pin_probe.log`) | R277-5; R277-6 (budget pin) | `0f003fab3303858ba4db955ad3c0512e67a8018b` (ancestor, no behavior change since); `00db64eb1e6e0c9bdb9f35ec5e37ebe6e00d550b` |
| Tests | CLEAN | `render_mutants.py` changed in its docstring only (`receipts/ast_probe.log`); `py_compile`; `measure_test_evidence_selftest.py` exit 0 with the planted 2700 s arm; hosted contexts and shard 4/5 at 9785/0 (`receipts/hosted_checks_00db64eb.tsv`, `receipts/milan_dp_window_head.txt`). R277-5's test artifacts are unchanged | R277-6 | `00db64eb1e6e0c9bdb9f35ec5e37ebe6e00d550b` |
| Docs | CLEAN | `TESTING.md:163-172,257-267`, `RUNNING_TESTS.md:76-84`, `milan_dp_gptp/README.md:24-36`, `render_mutants.py:28-42`, `CI_WORKFLOWS.md:150-190` (history kept), `milan_dp/README.md:244,864`, the PR body, the residual search (`receipts/residual_2700.log`) and the docs gates (`receipts/docs_check.log`, `doc_style.log`, `gptp_docs.log`, `doc_map.log`, `solution_docs.log`). R277-5's other Docs artifacts are unchanged | R277-6 | `00db64eb1e6e0c9bdb9f35ec5e37ebe6e00d550b` |

## Prior findings from this reviewer (R277-5, at `0f003fab`)

| Finding | Disposition at `00db64eb` | Evidence |
|---|---|---|
| F1 MINOR Docs: 2700 s stated as the current budget | **Closed** | The F1 table above. |
| S1 SUGGESTION Docs: `CI_WORKFLOWS.md:166` "timed out 1 s and 13 s early" | Retained; optional | The file is unchanged. A SUGGESTION does not affect coverage. |
| S2 SUGGESTION Tests: the settime omission control is not committed | Retained; optional | Unchanged. R277-5 showed that the committed `RENDER-SETTIME` checks can fail. |

## Prior public findings from the other reviewer

This section was written after the verdict, findings and ledger above were drafted.

| Finding | Disposition at `00db64eb` | Evidence |
|---|---|---|
| R276-6 F1 MINOR Docs: the same four statements as R277-5 F1 | **Closed** | The F1 table above. |
| R276-6 F1, additional clause: `TESTING.md:259` should give the decision's basis | **Not a defect, in this reviewer's own judgment.** The sentence is unchanged and optional wording is retained (the other reviewer's R276-7 withdrew this clause and filed it as S3) | `:259` reads "The `milan_dp` budget is no exception to it: it covers the unchanged suite on the slower hosted runner." "It" is the #367 rule that a long mutation campaign is an explicit target, never a raised deadline. The sentence dates from #444 (`06055a04c`). It states no number, and it stays true under decision 5820240308: the decision kept the suite whole rather than moving the three acceptance-named controls out, and it raised the deadline for runner noise. The explicit `gmstep-mutants` campaign stays a separate target (`TESTING.md:267`, `CI_WORKFLOWS.md:190`). |
| R276-6 S1 SUGGESTION Docs: the `obj_aclk` census row still shows 139 / 0 at `milan_dp/README.md:763` | Retained; optional | The row is unchanged and undated. The table says undated rows come from the earlier broad run. |
| R276-6 S2 SUGGESTION Tests: the `gmstep_mutants.py` freshness docstring names more inputs than the check reads | Retained; optional | Unchanged. The point is moot in the sweep, because `run` rebuilds `obj_gmstep` first. |
| R276-7 (at this head): POSITIVE, with suggestions only | No open finding to resolve | Read after this round's verdict and ledger were drafted. |

## Real limits

- **Hardware.** Physical calibration was NOT RUN. Acceptance 4, the #117 two-board handover, has no evidence, and field skips are not hardware proof.
- **Not run here, by the round's rules:** the full `milan_dp` `run` sweep, `run_all_suites.sh`, the builder, PP, gPTP and Yosys banks, act/Docker, and hardware. This delta is text-only. The other legs rest on R277-5, the manager's source banks at this head, and the hosted exact-head shard 4/5.
- **Hosted merge base.** The hosted `pull_request` runs built GitHub's merge `66972b69` of this head onto dev `573f0052`. That is neither the source base `57456af9` nor the current live dev `ffcbd33d`. Those runs are evidence for that merge, not for the manager's own candidate. The `milan_dp` window is one hosted sample.
- **Em-dash gate.** `check_em_dash.py` could not judge on this host: its pinned renderer is not installed, and shared installs are out of bounds. The substitute check is a count of em dashes in the delta's added lines, which is 0. The delta has no other dash-bearing prose.
- **Standards.** No standards document was available. IEEE and Milan clauses were read as quoted in the tree and the decisions.

## Pending manager duties

- Accept the hosted and act results. At this head, the `verilator-suites` aggregate was still in progress when read, and `yosys-portability` had not yet been reported.
- Build and validate the final current-dev candidate at the merge turn: source base `57456af9`, live dev `ffcbd33d`.
- Obtain the required independent positives and a reviewer-owned five-lens ledger for the merge candidate. Obtain explicit maintainer authorization before any merge.
- After merge: acceptance 4 on the #117 bench, and post-merge containment.

## Clone integrity

- The review clone is at `00db64eb1e6e0c9bdb9f35ec5e37ebe6e00d550b`, tree `5523c0bcc1383f6392fa3c1269d1e5e08223bdbb`.
- All 883 tracked blobs were re-hashed with `--no-filters` and match HEAD, modes included. The index equals HEAD.
- There are no untracked, ignored or modified entries. The bytecode caches created by this round's checks were removed.
- The gitlinks are `gptp-processor` `e5dcea6e`, `protocol-processor` `09f9bf38` and `third_party/verilog-axis` `48ff7a7e`, all checked out clean. `external` `efeb541a` is uninitialized. See `receipts/integrity.log`.

## Receipts and scripts (listed in MANIFEST.sha256)

- `ast_probe.py`: shows that a commit changes only a Python module docstring.
- `budget_pin_probe.py`: shows that the runner contract accepts 3600 s and rejects 2700 s.
- `shard_window.py`: computes the hosted `milan_dp` window and its margin.
- `integrity.sh`: checks the clone's bytes, modes, index and gitlinks.
- `receipts/`: delta scope, residual search, docs gate logs, selftest, probes, hosted checks, `milan_dp` window, PR head and body, integrity.

R277-6 FINISHED
