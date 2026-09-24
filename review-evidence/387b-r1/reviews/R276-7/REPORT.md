[R276] POSITIVE - exact head 00db64eb1e6e0c9bdb9f35ec5e37ebe6e00d550b

Round R276-7 is the internal cleared-context delta re-review of issue #387 / PR #555, round 4 of the lane (assignment 5821889812).

- Head `00db64eb1e6e0c9bdb9f35ec5e37ebe6e00d550b`, tree `5523c0bcc1383f6392fa3c1269d1e5e08223bdbb`. It is one commit on `0f003fab`, which my round 3 (R276-6) reviewed.
- Delta `0f003fab..00db64eb`: 4 files, +7/-5, all prose. Three are Markdown pages. The fourth is the docstring of `tb/verilator/milan_dp/render_mutants.py`. Nothing under `hdl/`, `sw/`, `scripts/` or `.github/`, and no gitlink, changes (`receipts/verify_f1_delta.txt`).
- All five lenses were applied at this head.

**Verdict.** R276-6 F1 (MINOR, Docs) is closed: every current statement of the `milan_dp` deadline now says 3600 s under decision 5820240308. The delta touches only the four files the assignment named. The history lines and the self-test mutation string are unchanged, as intended. No finding is open. One new SUGGESTION (S3) and the four round-3 suggestions are optional and do not affect coverage.

## Reconstruction

The sources were read in this order:
1. AGENTS.md, CONTRIBUTING.md and docs/README.md. These stand as I read them in R276-6.
2. The issue #387 acceptance and decisions, as reconstructed in R276-6. For this round I re-read decision 5820240308 (`receipts/decision_5820240308.txt`).
3. Assignment 5821889812 (`receipts/assignment_5821889812.txt`) and review start 5822075260.
4. `git diff 0f003fab..00db64eb`, its history, and a scan of the whole tree at the head.
5. The public evidence tree `9028ea6d` (`review-evidence/387b-r1/author-r4`). I used it only to confirm that `round-4.patch` has the same changed lines as the delta, and that `gate-results.json` names head `00db64eb`.
6. Exact-head hosted check runs.

Prior public review findings (R276-6 and R277-5) were read after this round's verdict, findings and ledger were fixed in a draft of this file. See "Prior public findings".

## F1 closure (R276-6 F1, MINOR, Docs)

| Site | At `0f003fab` | At `00db64eb` |
|---|---|---|
| `docs/testing/TESTING.md:166-167` | 2700 s; basis "#444 measured worst case plus margin" | "3600 seconds for `milan_dp`". Basis: "Decision 5820240308 sets this deadline from recorded hosted samples". The next line points to the table and measurements in `CI_WORKFLOWS.md`. This meets the assignment's requirement to cite the decision and the recorded samples, not #444 alone |
| `docs/testing/RUNNING_TESTS.md:79-80` | "2700 seconds (#444)" | "3600 seconds under decision 5820240308", linked |
| `tb/verilator/milan_dp_gptp/README.md:31-32` | "2700-second budget (#444)" | "3600-second budget", with a linked sentence naming decision 5820240308 |
| `tb/verilator/milan_dp/render_mutants.py:37` | "suite_timeout = 2700 s (#444)" | "suite_timeout = 3600 s (decision 5820240308)". It is a docstring only and compiles (`py_compile` exit 0) |

Every link targets `issues/387#issuecomment-5820240308`, the decision that raised the deadline to 3,600 s. It agrees with the executable surface:
- `scripts/run_all_suites.sh:39,245` (`${SUITE_TIMEOUT:-3600}`);
- the pin at `scripts/measure_test_evidence.py:718`;
- `CI_WORKFLOWS.md:159`;
- `tb/verilator/milan_dp/README.md:244`;
- `.github/workflows/rtl.yml:152`, where `timeout-minutes: 120` on `verilator-shards` holds the 3600 s deadline.

**No current statement of the old budget remains.** Every `2700` / `2,700` in tracked text at the head (`receipts/verify_f1_delta.txt`):
- `CI_WORKFLOWS.md:167` "That 1800 s deadline became 2700 s under #444." This is history, unchanged by the delta.
- `CI_WORKFLOWS.md:185` "The `a21cd358` sample left 240.1 s of 2700 s: 8.9%." This is history, and it is the trigger that decision 5820240308 cites. It is unchanged.
- `scripts/measure_test_evidence_selftest.py:294` `("SUITE_TIMEOUT:-3600", "SUITE_TIMEOUT:-2700")` is a planted mutation that the self-test must reject. It is unchanged. `--selftest` gives 101/101, including `[PASS] a changed suite budget is rejected: SUITE_TIMEOUT:-3600` (`receipts/measure_test_evidence--selftest.log`).
- The remaining matches are unrelated: a hash in `scripts/act_ci.py:7660`, a vendor build number in a tcl header, and the range `12700` in `sim_rails.cpp`.

A search for the deadline in other words also finds no stale statement:
- "2,700", "45 minutes" and `#444` beside a budget;
- `milan_dp` next to "budget", "deadline" or "seconds" in `*.md`, `*.py`, `*.sh` and `*.yml`;
- the submodules `gptp-processor`, `protocol-processor` and `verilog-axis`, which contain no `milan_dp` budget statement.

**Fault probe.** Changing only `run_all_suites.sh:245` back to `SUITE_TIMEOUT:-2700` makes `measure_test_evidence.py --check` report `runner evidence contract: FAIL`, exit 1. The file was then restored and the tree checked clean (`receipts/probe_driver_2700.log`). So the 3600 s that the prose now states is the value the contract enforces.

**The part of my F1 required outcome about `TESTING.md:259`.** I wrote that `:259` should give the decision's basis; the assignment did not list it and said "change nothing else". I re-judged the line against the decision's own text:
- The line reads "The `milan_dp` budget is no exception to it: it covers the unchanged suite on the slower hosted runner." It dates from `06055a04`, before this PR, and states no figure.
- Decision 5820240308 bases the raise on runner noise over "near-identical content". It declines to move the controls, which would save about 180 s, because that is smaller than the noise.
- The #367 rule `:257` states is kept: the eight additional gmstep controls stay in the explicit `gmstep-mutants` target (`CI_WORKFLOWS.md:189-190`).
- So the sentence is consistent with the decision and does not misstate a current contract. I withdraw that part of the required outcome and keep only a suggestion (S3).

## Findings

None open at MINOR or above.

### S3 - SUGGESTION - Docs - `docs/testing/TESTING.md:259`

- The sentence explains why the `milan_dp` budget is not a raised deadline for a campaign, with no citation. Since this PR, the budget's authority is decision 5820240308, and the suite has gained the three gmstep controls and the RENDER-SETTIME checks. It is not literally "unchanged".
- A link to decision 5820240308 ("runner noise over near-identical content; controls kept") would make the rationale traceable. This is optional. It is not a current-contract error.

## Lens results at this head (clean lines carry their evidence)

- `[R276] PASS Conformance - docs/testing/TESTING.md:166-167, RUNNING_TESTS.md:79-80, tb/verilator/milan_dp_gptp/README.md:31-32, tb/verilator/milan_dp/render_mutants.py:37 against decision 5820240308 and assignment 5821889812; run_all_suites.sh:39,245; measure_test_evidence.py:718; rtl.yml:152 - the four sites and only those changed, each states 3600 s and cites the decision, matching the enforced value and the 120-minute shard; the round-3 conformance of the #387 RTL (R276-6 at 0f003fab) is untouched because the delta changes no hdl/ or tb logic.`
- `[R276] PASS RTL - git diff --raw 0f003fab..00db64eb (receipts/verify_f1_delta.txt) - no file under hdl/, no gitlink and no build or source list changed; the RTL reviewed clean in R276-6 at 0f003fab is byte-identical at this head. Hosted verilator-lint and Yosys shards 0-3/4 succeeded at this head; yosys-elaboration and elaborate were still in progress when sampled (receipts/hosted_checkruns_head.tsv).`
- `[R276] PASS Robustness - receipts/verify_f1_delta.txt, receipts/probe_driver_2700.log - the only behaviour-bearing value the delta describes (the milan_dp deadline and its TIMEOUT = exit 92 handling, render_mutants.py:36-40) is unchanged in code; the docstring still describes the real kill path. Reverting the deadline fails the runner contract. No input, reset or timeout path changed; the R276-6 robustness evidence at 0f003fab stands.`
- `[R276] PASS Tests - tb/verilator/milan_dp/render_mutants.py (docstring-only change, py_compile exit 0), scripts/measure_test_evidence.py --check exit 0 and --selftest 101/101, check_py_idiom exit 0, and the 2700 fault probe that the contract rejects - no test logic changed, and the budget pin still has teeth.`
- `[R276] PASS Docs - the four changed sites plus CI_WORKFLOWS.md:156-192 (history lines :167 and :185 kept), TESTING.md:257-259, tb/verilator/milan_dp/README.md:244 - consistent with decision 5820240308. Gates at this head: docs_check (git and no-git tree) 0 findings; check_em_dash --base 57456af9 0 findings over 181 added lines, arms 339/339; gen_toc --check OK; check_doc_style OK; check_doc_paths OK (841 paths); git diff --check for the delta and the whole PR clean. The em-dash and TOC checks ran with the pinned renderer from tools/markdown/requirements.txt in an unpublished scratch environment. S3 is optional.`

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Delta against decision 5820240308 and assignment 5821889812; the runner, the contract pin and the shard timeout. The #387 RTL and decision conformance was applied in R276-6 at ancestor `0f003fab`, and the delta changes nothing in its scope | R276-7 | 00db64eb1e6e0c9bdb9f35ec5e37ebe6e00d550b |
| RTL | CLEAN | `git diff --raw` of the delta, which contains no `hdl/`, gitlink or source-list change; the R276-6 RTL review at `0f003fab` carries over byte-identically; hosted lint and Yosys shards at this head | R276-7 | 00db64eb1e6e0c9bdb9f35ec5e37ebe6e00d550b |
| Robustness | CLEAN | Deadline and timeout path unchanged in code; `render_mutants.py` docstring against the real kill path; 2700 reversion probe; R276-6 robustness evidence at ancestor `0f003fab` untouched | R276-7 | 00db64eb1e6e0c9bdb9f35ec5e37ebe6e00d550b |
| Tests | CLEAN | `render_mutants.py` (docstring only, compiles); `measure_test_evidence.py --check` and `--selftest` 101/101; `check_py_idiom`; 2700 fault probe; R276-6 test evidence at ancestor `0f003fab`, whose test logic is unchanged | R276-7 | 00db64eb1e6e0c9bdb9f35ec5e37ebe6e00d550b |
| Docs | CLEAN | `TESTING.md`, `RUNNING_TESTS.md`, `milan_dp_gptp/README.md`, `render_mutants.py` docstring, `CI_WORKFLOWS.md` history lines, `milan_dp/README.md:244`; a tree-wide and submodule scan for the old budget; docs_check (both modes), em-dash, TOC, style, paths and `diff --check` | R276-7 | 00db64eb1e6e0c9bdb9f35ec5e37ebe6e00d550b |

## Prior public findings (read after this round's verdict, findings and ledger were drafted)

| Finding | Status at `00db64eb` | Evidence |
|---|---|---|
| R276-6 F1 = R277-5 F1 (MINOR, Docs): 2700 s stated as current | **Resolved** | See "F1 closure". R277-5 F1 asked that `git grep -n 2700 -- docs scripts tb` show only the `CI_WORKFLOWS.md` history and `measure_test_evidence_selftest.py:294`. It also shows the unrelated `scripts/act_ci.py` hash, the tcl build number and the `sim_rails.cpp` range. None of those is a budget. The `TESTING.md:259` part of R276-6 F1 is withdrawn, with the reasons given above, and replaced by S3 |
| R276-6 S1 (Docs, `milan_dp/README.md:763`, `obj_aclk` 139/0 vs 143/0) | Retained, optional | Unchanged at this head |
| R276-6 S2 (Tests, `gmstep_mutants.py:186-188` docstring vs inputs read) | Retained, optional | Unchanged at this head |
| R277-5 S1 (Docs, `CI_WORKFLOWS.md:166` "timed out 1 s and 13 s early") | Retained, optional | Unchanged at this head. I agree the wording is ambiguous; it is not a contract error |
| R277-5 S2 (Tests, RENDER-SETTIME omission control not committed to a runner) | Retained, optional | Unchanged at this head |
| All earlier findings (R276-4/5, R277-3/4) | Remain resolved | Resolved by `0f003fab` per R276-6 and R277-5. The delta touches none of their artifacts |

Reading them changed no finding and no ledger row.

## Hosted evidence at the exact head (inspected, not owned)

Snapshot at 2026-09-24T20:57:08Z (`receipts/hosted_checkruns_head.tsv`):
- **Executed and succeeded:** `changes`, `full-ci-gate`, `bdd-conformance`, `verilator-lint`, `wire-accountability`, `docs-check-no-git`, and Yosys shards 0-3/4.
- **Still in progress:** `docs-check`, `elaborate`, `yosys-elaboration`, and Verilator shards 0-4/5.
- **Skipped context:** "Physical gPTP (nightly and manual)". It is the scheduled suite, and a skip is not physical-rate or hardware evidence.

The manager owns hosted and act acceptance. This review does not depend on the in-progress contexts: the delta is prose only, and the local docs gates above pass.

## Receipts and scripts (all listed in MANIFEST.sha256)

- `scripts/verify_f1_delta.sh <clone> [prev] [head]` is portable. It prints the delta's raw file list, the delta, every `2700` in tracked text, the current deadline statements, and whether the history and self-test lines are unchanged.
- Receipts:
  - `receipts/verify_f1_delta.txt`: the script's output at this head;
  - `receipts/probe_driver_2700.log`: the fault probe and its restoration;
  - gate logs:
    - `receipts/check_doc_paths.log`, `check_doc_style.log`, `docs_check.log`, `docs_check_nogit.log`;
    - `receipts/check_em_dash.log`, `gen_toc.log`;
    - `receipts/check_py_idiom.log`, `measure_test_evidence--check.log`, `measure_test_evidence--selftest.log`;
    - the file-named logs `scripts_check_doc_paths_py.log`, `scripts_check_doc_style_py.log`, `scripts_docs_check_py.log`, `scripts_measure_test_evidence_py.log`, `tb_verilator_milan_dp_render_mutants_py.log`;
    - `receipts/diff_check_0f003fab.log` and `diff_check_57456af9.log`;
  - `receipts/decision_5820240308.txt` and `assignment_5821889812.txt`: public comment bodies;
  - `receipts/hosted_checkruns_head.tsv`;
  - `receipts/review_clone_integrity.txt`.

## Real limits

- **Delta review.** I did not re-run the RTL simulations, the property probe or the gmstep, aclk and option-off legs at this head. The delta changes no code that they exercise. My R276-6 evidence at `0f003fab` covers them, and the RTL, `tb` logic, scripts and workflows are byte-identical between the two heads.
- **Not run here:** the full parent, PP and gPTP banks, the builder, Yosys, `run_all_suites.sh`, act, and the pinned Verilator (not needed for a prose delta). The manager's source static, builder and native banks at this head were not re-run by me.
- **Not claimed.** Physical calibration and the #117 two-board handover (acceptance 4) were NOT RUN and are not claimed. Field skips are not hardware proof.
- **Hosted contexts.** Several were still in progress when sampled. Nothing in this verdict relies on them.
- **Clone integrity.** The review clone is byte-exact at the head (`receipts/review_clone_integrity.txt`):
  - HEAD `00db64eb`, and `write-tree` equals `5523c0bc`;
  - empty `status --ignored`, after I removed the bytecode caches my gate runs created;
  - no assume-unchanged or skip-worktree flags;
  - 883 tracked blobs with 0 byte or mode mismatches;
  - gitlinks `gptp-processor` e5dcea6e, `protocol-processor` 09f9bf38 and `third_party/verilog-axis` 48ff7a7e are clean at their pins, with `external` uninitialised as at the start.

## Pending manager duties

- Build and validate the final current-dev candidate: source base `57456af9`, live dev `573f0052`.
- Own hosted and act acceptance at this head, including the Verilator shards and `yosys-elaboration` that were in progress when sampled. Check the shard 4/5 `milan_dp` window against the 10% level of decision 5820240308.
- Obtain the other reviewer's round-4 verdict. Merge needs two independent positive reviews and the full completion bar, and a maintainer's explicit merge authorization.
- Run the #117 bench step (acceptance 4) after merge.

R276-7 FINISHED
