[R220] NEGATIVE - exact head 6af65a151663e1301f1983a6c9d22650a0b35da9

This is a cold external review of PR #505 for issue #407, by the Opus reviewer with a cleared context.

- **Base:** `b17580b91deb11f3441dfc5d7f9fafe539d929b8`. The head is its only child, and the head tree is `9983ea19387ff054aa5baf7bd881cd24e46176bc`.
- **Diff:** `scripts/ci_events.py` and `docs/testing/CI_WORKFLOWS.md` only.
- **Public sources read:**
  - the #407 body, the AC5 correction (issuecomment-5770808527), and the [A155] TAKEN and IMPLEMENTATION DECISIONS comments;
  - the PR #505 thread and scratch PR #506;
  - CONTRIBUTING.md, AGENTS.md, REQUIREMENTS.md section 8 and CI_WORKFLOWS.md;
  - the public evidence at `6fdc390c`. Its AC5 directories are byte-identical to `1fa64a45`.
- **Attribution:** author and manager evidence is marked as theirs. Anything I call "measured" I reproduced myself, in an isolated clone or in scratch copies outside the tracked tree.

**Why the verdict is NEGATIVE:**

- Two MINOR findings are open: F1 (Docs) and F2 (Tests and Conformance). There is no BLOCKER and no MAJOR.
- RTL and Robustness are covered clean at this head.
- The production refusal is exact, and the AC5 raw receipts show every expected observation.
- The verdict is NEGATIVE only because AGENTS section 7 cannot be met at this head while a MINOR stays open.

## Findings

[R220] MINOR Docs - docs/testing/CI_WORKFLOWS.md:1040-1043 - the policy page still says the three docs-check shape-gate commands are "not pinned yet (#407)"

- **Requirement/evidence:**
  - AGENTS section 6, Docs: "Changed contracts are reflected in authoritative docs".
  - The docs-check section still reads: "`CARRIER_STEP_LISTS` records all three steps by name and position ... like the other recognised steps, their commands are not pinned yet (#407)".
  - At this head those commands are pinned. Their records are at scripts/ci_events.py:1064-1075, and item 11 (CI_WORKFLOWS.md:635) says every recognized carrier `run` body is pinned.
  - Measured: I dropped `--self-test` from `Deploy shape gate`. The head checker refuses it with "job `docs-check` step 42 (`Deploy shape gate`) script is not the canonical form: line 1 ...". The base checker accepts the same edit (logs/shape-gate-pin-probe.log).
  - Commit 5251942a (2026-09-19) wrote the sentence as a forward reference to this issue, and this diff leaves it untouched.
  - I did not also file this under Conformance. AC4 names items 11 and 12 only, and both are updated.
- **Impact:** once `Closes #407` merges, the authoritative CI policy contradicts itself. A cold reader of the docs-check section would conclude that the sweep, deploy and entity gate commands can still be rewritten under their recorded names.
- **Required change:** the sentence states the current contract, or is removed. No text on the page may still name the carriers' non-gate script content as open.
- **Verification:**
  - `git grep -n "pinned yet (#407)"` returns nothing.
  - These all pass at the corrected head: docs_check, gen_toc --check, check_doc_paths, check_em_dash against the merge base, and ci_events --check/--selftest.

[R220] MINOR Tests, Conformance - scripts/ci_events.py:7435-7437 (`_carrier_script_edits`, `or-true`) - the swallowed-call lever swallows only each body's last command, so `--selftest` cannot fail for a comparison that ignores a swallowed non-last call, including the exact AC5 mutation

- **Requirement/evidence:**
  - AGENTS section 6, Tests: "Each new test can fail for the defect it claims to detect".
  - The `or-true` edit appends ` || true` to `lines[-1]` only.
  - This PR adds the claim "A swallowed Python idiom call therefore leaves that step green, but both jobs' contract steps refuse it by name" (CI_WORKFLOWS.md:770-771). That call is line 1 of 2 in docs-check step 34, and no arm swallows it.
- **Measured** in memory with a weakened comparison, mutant M5b, which ignores a trailing `|| true` on every non-last line:
  - `--check` stays green and the complete `--selftest` still passes, with 931 arms.
  - M5b accepts the AC5 tamper with 0 findings. The real checker reports 1 (logs/full-selftest-under-checker-mutants.log).
  - The 40 multi-command bodies have 117 non-last lines between them. The real checker refuses an appended `|| true` on every one; M5b accepts 54 (logs/m5b-exposure.log).
  - Those 54 include the bounded `--check` call of four ratchets (docs-check steps 26, 28, 30 and 31, line 1) and the Python idiom call (step 34, line 1).
- **Precedent:** the #303 pin arms swallow each command of its two-command body (scripts/ci_events.py:6657-6666; CI_WORKFLOWS.md:892-893).
- **Conformance attribution:**
  - AC2 requires "`|| true` appended to the call" for "a ratchet with a bound".
  - Every ratchet body is `<ratchet> --check` followed by `<ratchet> --selftest`, and only the self-test line has a swallowing arm.
  - Read literally ("a call in the body"), AC2 is met. Read as "the ratchet's bounded call", AC2 is not met.
  - Per AGENTS section 6, I record this under both lenses and publish the ambiguity here.
  - The required change below satisfies both readings, so no separate decision is needed if the lane adopts it.
- **Impact:**
  - Production behaviour is correct today: the real comparison is exact.
  - What is missing is regression proof. A later relaxation that tolerates a non-last `|| true` would re-open the hole #407 closes, with `--check` and `--selftest` both green.
  - CI_WORKFLOWS.md:770-771 would then become false without any gate noticing.
- **Required change:** the #407 lever population swallows every command of a multi-command body, or at minimum every non-last line that invokes a gate or tool. Each such arm is reason-pinned to that line.
- **Verification:**
  - Under M5b, the complete `--selftest` fails and names docs-check step 34 line 1 (probes/nonlast_mutants.py, probes/m5b_exposure.py).
  - The real `--selftest` still passes.

[R220] SUGGESTION Tests - scripts/ci_events.py:7428-7471 - no lever appends a command or reorders two lines

- The real checker refuses both edits (logs/robustness-probes.log):
  - an appended line that overwrites a later gate's script is refused at docs-check step 4, line 2;
  - a reordering is refused at step 34, line 1.
- Neither edit is armed, though. A prefix-only comparator (M4) and an order-insensitive comparator (M1) each pass the complete `--selftest` (logs/full-selftest-under-checker-mutants.log).
- Precedent arms an "extra line" and a "hostile line" for other pinned scripts (CI_WORKFLOWS.md:778, 838-839).
- AC2 does not require these levers.

[R220] SUGGESTION Docs - docs/testing/CI_WORKFLOWS.md:774-896; scripts/ci_events.py:1980-1983, 2014-2015 - the coverage list and two comments were not extended for the new script pins

- The "`--selftest` covers, one at a time" list gained no #407 entries, although #406 extended it (:866-876).
- Its phrase "all ten canonical scripts" now under-describes the whitespace control, which reformats all 56 bodies (scripts/ci_events.py:7897-7899).
- Two comments on the RTL step lists still say they are held "exactly as" CARRIER_STEP_LISTS holds the carriers, and "in the shape CARRIER_STEP_LISTS records" them. The carrier lists now also record scripts.

[R220] SUGGESTION Docs - docs/testing/CI_WORKFLOWS.md:651-652; scripts/ci_events.py:867 - "beside a mutation entry/arm" names nothing a maintainer has to edit

- The arms derive from the live step (scripts/ci_events.py:7451-7471).
- Measured (logs/maintenance-sim.log):
  - updating a legitimate script edit's canonical record alone restores `--check` OK and `--selftest` PASS, with 933 arms, the new ones derived automatically;
  - a workflow-only edit is refused naming the step and the line.
- The phrase mirrors AC4's parenthetical "(update the canonical script beside a mutation entry)", which assumed hand-written arms. This is a wording note on AC4, not a behaviour gap.
- Consider saying that the arms follow the live step automatically.

## Clean lenses

[R220] PASS RTL - `git diff --stat b17580b9..6af65a15`, scripts/ci_events.py:3649, logs/arm-and-check-preservation.log - no RTL applies, and the checker's interfaces are intact

- The diff touches no file under hdl/, tb/, syn/, sw/ or .github/workflows/, and no gitlink.
- These equal base exactly:
  - RTL_STEP_LISTS, RTL_SIBLING_STEP_LISTS and ENV_FILE_WRITERS;
  - SV2V_INSTALL, BUILDER_RUNS and BUILDER_COMMAND;
  - the six canonical gate scripts and CANONICAL_CONTRACT_SCRIPT.
- CARRIER_STEP_LISTS equals base once the new `run` records are removed.
- Ignoring docstrings, only check_carrier_steps, _mutations, _selftest_whitespace and selftest changed.
- The `path in (DOCS, ELABORATE)` guard leaves the seven RTL jobs to #439, as CI_WORKFLOWS.md:765-766 states.
- No other tool imports these tables.

[R220] PASS Robustness - scripts/ci_events.py:3572-3589, 3630-3650 at 6af65a15; logs/robustness-probes.log - all 15 probes behave as specified: 14 malformed, reordered or bad-record cases are refused or fail closed, and 1 whitespace equivalence is accepted by design

- Each of these is refused, naming the job, step and line:
  - an appended line that overwrites a later gate's script;
  - reordered lines;
  - a command moved into the `command -v tclsh || {` block;
  - a swallowed middle command;
  - an NBSP;
  - CRLF line endings;
  - an empty body;
  - an appended comment.
- A non-string `run` is refused by the step-identity check.
- A malformed production record fails closed: a list, an empty tuple, a non-string element, or a raw string.
- A deleted production record fails closed, and its arms are still derived from the live step.
- Extra blanks inside a quoted word are accepted. That is the shared item-7 normalization, which #407 adopts explicitly ("item 1: verbatim after whitespace normalisation").

## Acceptance and required checks

This table is the Conformance evidence. F2 carries the one open Conformance attribution.

| Item | Result at 6af65a15 | Evidence |
|---|---|---|
| AC1 | Met. All 56 recognized run bodies have a record equal to an independent re-normalization of the live YAML: docs-check 41, wire-accountability 2, docs-check-no-git 1, elaborate 12. A refusal names the job, the step number and name, and the first differing line. | logs/independent-census.log, logs/native-ac5-analogue.log |
| AC2 | All levers are present. There are 243 arms: no-op 56, or-true 56, drop-command 40, drop-flag 35, continue-on-error 56. Every carrier and every gate class gets each lever that can apply to it. Flag-drop cannot apply to docs-check-no-git step 2 or to the builder call, because neither carries such a flag, and adding one is out of scope ("changing what any gate runs"). [A155] recorded this publicly. The stub vacuity control fails 833/833 arms, but it is tautological by construction; see the "Actual vacuity" row. For the reading of "the call", see F2. | logs/ci_events-selftest.log, probes/tally_selftest.py |
| AC3 | Met. `--check` is OK over 1505 items. `--selftest` passes with 931 arms, which includes the 243 new arms and 57 new record controls. | logs/ci_events-check.log, logs/ci_events-selftest.log |
| AC4 | Met as worded. The item 12 residue now names only the RTL jobs (#439). Item 11 states the pins and the cost. docs_check, gen_toc --check and check_doc_paths exit 0. See also F1 and the third SUGGESTION. | CI_WORKFLOWS.md:635-653 and 765-772, logs/gate-*.log |
| AC5 | Met; see the AC5 section below. | public receipts, re-read |
| Specialized gates preserved | All 590 base mutation arms are still present, each with an identical expected fragment. The specialized check functions are unchanged. | logs/arm-and-check-preservation.log |
| Workflow semantics unchanged | All four workflow files are byte-identical to base. | same log |
| Actual vacuity | With the new comparison removed, all 187 body arms miss, and the complete `--selftest` reports 243 failures: the 187 arms plus the 56 missing-record controls. The continue-on-error arms are caught by the pre-existing key check. | logs/vacuity-and-checker-mutants.log, logs/full-selftest-under-checker-mutants.log |
| Missing/deleted records | All 56 missing-record controls pass. A deleted production record is refused and keeps its arms. | logs/ci_events-selftest.log, logs/robustness-probes.log |
| Maintenance positive controls | A whitespace reformat of all 56 bodies is accepted. A script and its record updated together are accepted. The full maintenance simulation is described in the third SUGGESTION. | logs/maintenance-sim.log |
| Local gates rerun | All exit 0: docs_check, gen_toc --check, check_doc_paths, check_em_dash --base b17580b9, check_doc_style, check_py_idiom and its --selftest (54/54), check_hygiene --check, check_todo_ownership, measure_fail_fast --check, check_feature_status, check_baremetal_only --check. | logs/gate-*.log |

## AC5 (A10 measurement; raw receipts re-read by R220)

- The SHA-256 values published in MANIFEST match all five files I read.
- I fetched both commits and diffed them. Scratch head `66ba2106` is exactly `6af65a15` plus one line, `python3 scripts/check_py_idiom.py || true`.
- #506 is closed and was never merged.

| Observation | Scratch 66ba2106 (meant to fail) | Normal 6af65a15 |
|---|---|---|
| Python idiom gate step | Success (ac5-act/01.log:1837). | Success (act-draft-fast/01.log:1947). |
| docs-check contract step | Failure, with one finding: job `docs-check` step 34 (`Python idiom gate`) line 1 (01.log:1902-1904). | Success (act-draft-fast/01.log:2946). |
| docs-check job | Failed (01.log:1909). No later docs-check step ran. | Succeeded (`docs: PASS`). |
| full-ci-gate contract step | Failure with the same finding (02.log:37-39). The job failed (02.log:44). | Hosted full-ci-gate succeeded on the ready run (05:07 UTC). The exhaustive act replica is still pending. |
| verilator-suites | Ran and failed at the download, the SHA verifier ("expected 5 ... found 0"), the tally and the worker-result check (02.log:84-105). | The hosted ready run was in progress at 05:19 UTC. |
| yosys-portability | Ran and failed: "expected 4 ... found 0", inventory expected=54 observed=0, and the worker-result check (02.log:145-167). | All 4 hosted shards succeeded; the aggregate was still pending. |
| Runner exit | Both invocations exited 1, a workflow failure rather than a setup refusal. | Exit 0 for docs, rtl-fast and elaborate. |

- Only the scratch head's failures are the expected refusal path. At the normal head, the required contexts must pass on their own.
- The idiom gate reports 0 findings on this tree, so the green step here does not show a real finding being swallowed. AC5 does not ask for that, and I have not added it as a requirement.
- Native analogue (logs/native-ac5-analogue.log): the base checker accepts the same tamper (1393 items, exit 0), and the head checker refuses it naming step 34 line 1.

## Completion ledger (reviewer-owned, round R220-1)

| Lens | Covering round | Head | State |
|---|---|---|---|
| Conformance | none (R220-1 applied it) | 6af65a151663e1301f1983a6c9d22650a0b35da9 | not covered: F2 open (MINOR) |
| RTL | R220-1 | 6af65a151663e1301f1983a6c9d22650a0b35da9 | covered clean |
| Robustness | R220-1 | 6af65a151663e1301f1983a6c9d22650a0b35da9 | covered clean |
| Tests | none (R220-1 applied it) | 6af65a151663e1301f1983a6c9d22650a0b35da9 | not covered: F2 open (MINOR) |
| Docs | none (R220-1 applied it) | 6af65a151663e1301f1983a6c9d22650a0b35da9 | not covered: F1 open (MINOR) |

- **Open findings, not moved to other issues:** F1 (MINOR, Docs) and F2 (MINOR, Tests and Conformance).
- **What un-covers the clean lenses:**
  - a commit that changes the checking path of `scripts/ci_events.py` un-covers Robustness;
  - a change under hdl/, tb/, syn/, the workflows or the gitlinks un-covers RTL.
- The F1 fix edits the policy page that `ci_events.py --check` reads, so `--check` and `--selftest` must be rerun at the corrected head.
- Section 7 items outside review remain the lane's to do:
  - the ready exhaustive act replica;
  - hosted verilator-suites and yosys-portability at the ready head;
  - the candidate-merge and post-merge checks.

## Scope and limits

- **Not run by R220:** Docker/act, hardware, a full RTL sweep, dependency installation, commits, pushes and public writes. The AC5 act results are the manager's; I re-read them here.
- **Probe hygiene:** probes changed only in-memory worlds or scratch copies outside the tracked tree.
- **Final state:** the review checkout is still at 6af65a15, clean, with submodules at their gitlinks.
- **Evidence:** logs/, probes/ and public-state/ sit beside this report, and the README.md there gives the reproduction commands.

R220-1 FINISHED
