[R220] NEGATIVE - exact head ad62493186576144f9fa1568babad012bc9ad8ca

Cold external re-review R220-2 of PR #505 / issue #407 by the Opus reviewer, cleared context.

- **Base:** `b17580b91deb11f3441dfc5d7f9fafe539d929b8`.
- **Head:** tree `6b279253aa7d3edd6d9b5e9adc1ed9caf6f13d75`. Its sole parent is round-1 head `6af65a15`, whose sole parent is the base. Live `dev` was still `b17580b9` at 06:34 UTC, so the head tree is the candidate merge tree.
- **Diff:** base to head and round-1 head to head both change only `scripts/ci_events.py` and `docs/testing/CI_WORKFLOWS.md`.
- **Public sources read, in order:**
  - AGENTS.md, CONTRIBUTING.md and docs/README.md;
  - the #407 body, the AC5 correction 5770808527, and the A155, A10 and A159 issue comments;
  - REQUIREMENTS.md section 8;
  - CI_WORKFLOWS.md items 1-12, the `--selftest` coverage list, and the Elaboration and One authoritative SHA sections;
  - the PR #505 thread through 5772174202, including R219-1 5771593926, R220-1 5771705156, decision 5771705480, response 5771927279 and REVIEW READY 5771927468;
  - the #439 body (for F3) and the state of scratch PR #506;
  - the diff, the history and the executable checker;
  - the factual AC5 and round-2 manager/builder receipts at evidence commit `b7380181`.
- **Not read:** R219's receipt files, the author's narrative handoff files, and any private transcript.
- **Attribution:** "measured" means reproduced by R220, in the review clone or in a disposable scratch copy. All other results are attributed to their owner.

**Why the verdict is NEGATIVE:**

- F1 is resolved at this head. It was R219 F1 and R220 F1, MINOR Docs.
- F2 is resolved at this head. It was R220 F2, MINOR Tests and Conformance.
- A new MINOR, F3, is open under Docs. This PR wrote the item-12 sentence "The remaining content gap belongs to the seven RTL jobs (#439)". But the SHA pin step of `full-ci-gate` is outside those jobs, and it still accepts content edits with `--check` green.
- Conformance, RTL, Robustness and Tests are covered clean at this head. Docs was applied and is not clean.
- There is no BLOCKER and no MAJOR. The verdict is NEGATIVE only because AGENTS section 7 cannot bank Docs while F3 is open.

## Disposition of prior findings

| Prior item | Lens | State at ad624931 | Evidence |
|---|---|---|---|
| F1: the shape-gate paragraph said the commands were "not pinned yet (#407)" | Docs | Resolved | CI_WORKFLOWS.md:1051-1055 now states name, position and canonical script, the named first-line refusal and the item-11 remedy. `git grep "pinned yet"` finds nothing. The drop-flag arms of steps 41-43 bite the real checker (p2). The docs gates exit 0 (logs/gates). |
| F2: only the last line of a body had a swallowing arm | Tests, Conformance | Resolved | ci_events.py:7443-7446 adds `or-true-line-N` for every non-last line. All 173 normalized lines now carry a swallowing arm, including every bounded `--check` call and the AC5 line (p2). Under mutant M5b, the real CLI `--selftest` goes from PASS (931 arms) at 6af65a15 to 117 failures at ad624931, and names `docs-check step 34 or-true-line-1` (p3). |
| SUGGESTION: no append or reorder lever | Tests | Adopted | There are 56 `append-command` arms and 40 `reorder-lines` arms. A prefix-only comparator (M4) and an order-insensitive one (M1) both pass at 6af65a15, and fail 56 and 40 arms at ad624931 (p3). |
| SUGGESTION: coverage list, whitespace count, RTL comments | Docs | Adopted, accurate | CI_WORKFLOWS.md:895-906; ci_events.py:1981-1992 and 2016-2018. |
| SUGGESTION: maintenance wording | Docs | Adopted, accurate | CI_WORKFLOWS.md:653-656; ci_events.py:865-869. In a scratch maintenance run, a workflow edit plus a matching record update passes `--check` and `--selftest`, with 1145 arms derived automatically (p5 S2). |

No prior finding was relabeled or moved to another issue.

## Findings

[R220] MINOR Docs - docs/testing/CI_WORKFLOWS.md:768 - the item-12 residue sentence assigns the whole remaining content gap to the seven RTL jobs, but `full-ci-gate`'s SHA pin step is outside them and its script is unpinned (F3)

- **Requirement/evidence:**
  - AGENTS section 6, Docs: "Changed contracts are reflected in authoritative docs".
  - The base text said that "every RTL step no rule above holds by script can still be rewritten or swallowed under the recorded name". This PR replaced it with: "The remaining content gap belongs to the seven RTL jobs (#439). Their recognized steps remain rewritable where no specialized script pin applies. The four non-RTL carriers now pin every recognized script (#407)." That text is at CI_WORKFLOWS.md:768-770. It was written at 6af65a15 and this revision did not change it.
  - Item 4 (CI_WORKFLOWS.md:342-348) names the other jobs in these files: the gate job, the physical leg, the fast selector and the fast verdict. `RTL_SIBLING_STEP_LISTS` records their steps (ci_events.py:2152).
  - **Measured, p11.** Those jobs have 12 run steps. Eleven refuse a `true` replacement and a `|| true` on every line. The twelfth is `full-ci-gate` step 2, "Print the event and pin the one SHA this run validates" (rtl.yml:54-64). It accepts `|| true` on each of its 8 normalized lines, and `check()` stays clean. The base checker gives the same result.
  - **Measured, p7, through the real CLI.** Two edits to that step leave `ci_events.py --check` at `OK (1505 contract item(s))` at ad624931, and at `OK (1393)` at base:
    - deleting its `if [ "$head" != "$GITHUB_SHA" ]; then ... exit 1; fi` block;
    - replacing its `exit 1` with `true`.
  - #439 covers only "every recognised step of the seven RTL jobs". Neither #407 nor #439 therefore covers this step.
- **Impact:**
  - The authoritative policy now tells a maintainer that, once #439 lands, no recognized step in the four workflow files can change what it runs unseen.
  - That is false for the gate's checkout-HEAD assertion, which can be swallowed with every context green.
  - The base text disclosed this gap in general terms, and the rewrite removed the disclosure. Runtime behaviour does not change, and the gap itself predates this PR.
- **Required change:**
  - The residue statement names every recognized step whose script no rule pins. At this head that is the seven RTL jobs' steps that no specialized pin holds, plus `full-ci-gate`'s pin step. Alternatively, the statement stops claiming that the seven RTL jobs hold the whole remaining gap.
  - The pin-step gap gets a public tracker: a new issue, or a recorded decision to widen #439. Closing the gap itself is not required in this lane.
- **Verification:**
  - Re-read item 12 against logs/p11-sibling-residue.log.
  - Rerun docs_check, gen_toc --check, check_doc_paths, and check_em_dash against the merge base.
  - Rerun ci_events --check and --selftest, because the checker reads this page.
- **Context (not a finding against this diff):** the pre-existing "One authoritative SHA" section (CI_WORKFLOWS.md:915-920) calls the gate's refusal of a checkout whose HEAD is not `GITHUB_SHA` "machine-checked". p7 shows that `--check` does not hold that script. This belongs with the new tracker.

[R220] SUGGESTION Robustness - scripts/ci_events.py:7439, :7476 - the #407 arm generator raises on a malformed pristine tree instead of naming it

- **Measured (p8, p9):**
  - With docs-check step 34's body replaced by whitespace, `--check` names the defect and exits 1. `--selftest` also exits 1, but with an `IndexError` traceback from `lines[-1]` at :7439.
  - A run step without a `name` raises `KeyError` at :7476.
- Both fail closed, so no false pass is possible. Both lines were already present at 6af65a15.
- Optional: skip or name such a step, so that `--selftest` prints its "pristine tree is not clean" problem rather than a traceback. This does not affect coverage.

## Lens results at ad624931

[R220] PASS Conformance - issue #407 AC1-AC5 and decision 5770808527; scripts/ci_events.py:870-1188, :3574-3591, :3651-3652; CI_WORKFLOWS.md:635-656, :768-775; logs/p1, p2, p5, p12, logs/gates; receipts/public-evidence - every acceptance criterion holds at this head, and F2's Conformance attribution is resolved

- **AC1.** I enumerated the live YAML with my own parser and my own shell normalization (p1). It holds 56 run bodies: docs-check 41, wire-accountability 2, docs-check-no-git 1 and elaborate 12. They have 173 normalized lines, and every body equals its record. A refusal names the job, the step number and name, and the first differing line (p5 S1, S3 and S6; p8).
- **AC2.**
  - Every carrier, and every docs-check gate class, carries these levers:
    - replacement by `true`;
    - `|| true` on every line, including the bounded `--check` call and the AC5 call;
    - a dropped command, where the body has several;
    - a dropped flag, where a `--self-test`, `--selftest` or `--check` flag exists;
    - `continue-on-error`.
  - The gate classes are the Python gate (step 34), the bounded ratchets (steps 26, 28, 30 and 31), the builder gate (step 21) and the reference build (step 2).
  - Each arm's reason names its step. The stub vacuity control fails all 1046 workflow arms (logs/03-selftest-head.log).
  - Among the named classes, the docs builder body (`python3 sw/builder/test_builder.py`) carries no such flag, and neither does the no-git body, so no flag arm applies to them. A155 recorded this publicly in 5770873818.
  - Both readings of "`|| true` appended to the call" are now met for a bounded ratchet.
- **AC3.** `--check` is OK over 1505 items, and `--selftest` passes with 1144 arms (logs/02 and logs/03).
- **AC4.**
  - Item 12 no longer names the carriers' non-gate content as open.
  - Item 11 states the pins and the cost, and names the remedy: update the canonical entry in the same commit, while the arms derive automatically.
  - The issue's parenthetical "beside a mutation entry" assumed hand-written arms, and this implementation has none to update. The wording was proposed publicly in R220-1 and accepted in 5771705480. I read AC4 as met, not as a conflict that needs a decision.
  - docs_check, gen_toc --check and check_doc_paths exit 0. F3 concerns a different sentence and is filed under Docs only.
- **AC5.** Met by the measurement at 6af65a15, retained for ad624931 on unchanged execution artifacts. See the AC5 section.

[R220] PASS RTL - `git diff --stat b17580b9..ad624931`; workflow and act_ci.py blob ids at b17580b9, 6af65a15 and ad624931; logs/p6-scope-equality.json, logs/p10-records-structure.json - no RTL, workflow or gitlink change, and the checker's interfaces and every table outside the carrier records are unchanged

- **Blobs:** only the two named files change. These are identical at all three revisions: docs.yml `f5a45401`, elaborate.yml `54c71a04`, rtl.yml `8510159e`, rtl-fast.yml `f7c502c9` and act_ci.py `794794b1`. No gitlink changes.
- **Round-1 head to head,** compared by AST with docstrings removed:
  - 331 functions are identical.
  - Only `_carrier_script_edits` and `_carrier_script_arms` differ, and both are reachable only from `--selftest`.
  - All 176 module constants are equal by value.
- **Base to head:**
  - 324 functions are identical.
  - Added: `check_carrier_script` and four self-test helpers.
  - Changed: `check_carrier_steps` (one call, at :3651-3652), `_mutations`, `_selftest_whitespace` and `selftest`.
  - CARRIER_STEP_LISTS without its new `run` records equals base.
  - These equal base: RTL_STEP_LISTS, RTL_SEQUENCE_PINS, RTL_SIBLING_STEP_LISTS, ENV_FILE_WRITERS, and every canonical specialized script.
- **Interface:** the CLI modes, exit codes and finding format are unchanged. `--check` takes 0.17 s and `--selftest` takes 7 s.

[R220] PASS Robustness - scripts/ci_events.py:3026-3045, :3574-3591, :3594-3684; logs/p8-robustness.json, logs/p5-maintenance-ac5.json - malformed bodies and records fail closed at this head, and whitespace-only reformatting is accepted

All 21 cases behave as specified (p8):

- NBSP, CRLF and U+2028 are refused by name.
- Each of these is refused, naming the job, the step and the first differing line:
  - an empty or whitespace-only body;
  - an appended comment;
  - a prepended `set +e`;
  - a duplicated line;
  - a swallowed middle command;
  - a command moved into the `tclsh` block;
  - a swallowed elaborate call.
- A non-string `run`, or a removed `run`, is refused by the identity check.
- Each of these records fails closed by name: a list, an empty tuple, a tuple holding a non-string, a raw string, a missing record, and a record that is not normalized.
- Tabs, continuations and blank lines are accepted.

Further, a record-only edit is refused (p5 S3). A workflow-only edit is refused at step 34 line 3, with `--selftest` red beside it (p5 S1). The generator's behaviour on a malformed pristine tree fails closed; see the SUGGESTION above.

[R220] PASS Tests - scripts/ci_events.py:7421-7487, :7531-7567, :7820-7853, :7856-7925; logs/p2-arms.json, logs/p3-cli-mutants.json and logs/p3-cli/, logs/p4-masking.json, logs/p5-maintenance-ac5.json - the arms are line-complete and reason-pinned, they fail for their named defects, and every prior control is retained

- **Derivation (p2).** The 213 new arms equal a population I computed independently:
  - 117 `or-true-line-N` arms, one per non-last line;
  - 56 `append-command` arms;
  - 40 `reorder-lines` arms, one adjacent distinct pair per multi-command body.
- Each new arm edits only its own step's `run`. Each reason names the job, the step number and name, the line number, and the expected text (`None` for an appended line).
- The AC5 arm makes exactly the edit `python3 scripts/check_py_idiom.py || true` on line 1.
- All 1046 workflow arms bite the real checker, and every label is unique.
- **Preservation (p2).** All 590 base arms and all 833 round-1 arms are present, with identical reasons and identical edits. The record stage still holds 56 missing-record controls and one matching-update positive. The whitespace stage reformats all 56 carrier bodies plus the specialized scripts.
- **Each lever fails for its named defect (p3).** Every mutant was run through the real CLI on scratch copies, and `--check` exits 0 under every one:

| Comparator mutant | 6af65a15 `--selftest` | ad624931 `--selftest` |
|---|---|---|
| M5b: a trailing `\|\| true` on a non-last line is ignored | PASS (931) | 117 failures, AC5 arm named |
| M4: prefix-only comparison | PASS (931) | 56 failures (append arms) |
| M1: order-insensitive comparison | PASS (931) | 40 failures (reorder arms) |
| `\|\| true` ignored on lines carrying `--check` | 3 failures | 14 failures |
| `\|\| true` ignored on any line | 54 failures | 171 failures |
| comparison removed | 187 failures | 400 failures (every body arm) |
| missing-record enforcement removed | 56 failures | 56 failures |
| elaborate comparison skipped | 46 failures | 111 failures |

  More mutants that fail at the head:
  - `|| true` ignored on the last line: 54 failures;
  - a truncated body accepted: 40;
  - only the first line compared: 229;
  - only the line count compared: 264;
  - flags ignored: 56;
  - `true` accepted as any body: 56.
- **Specialized controls stay reason-pinned (p4):**
  - no earlier arm is satisfied only by a #407 finding;
  - stubbing each of 8 specialized checks drops the same number of base arms at the head as at base (13, 15, 8, 34, 5, 14, 2 and 16);
  - with the #407 comparison removed, exactly the 400 body arms miss (p3).
- **Positive controls (p5):** two edits, each with its matching record update, pass `--check` and `--selftest`: one to a docs.yml script and one to an elaborate script. A whitespace-only reformat passes `--check`.

**Docs (applied, not clean).** Applied at ad624931 to every changed line of both files, and to #407 references across the tree. These all match the measured behaviour:

- F1 and the three Docs suggestions (see the disposition table);
- item 11 (CI_WORKFLOWS.md:635-656);
- the coverage list (:895-906);
- the shape-gate paragraph (:1051-1055);
- the code comments at ci_events.py:865-869, 1981-1992, 2016-2018, 3576-3601 and 7431-7436.

No page copies an arm count. F3 remains open, so Docs is not covered.

## AC5, and retaining the 6af65a15 measurement

**Receipts.** The measurement is A10's; R220 re-read it.

- I downloaded 18 files from evidence commit `b7380181`, and each matches its git blob id. The AC5 blobs are identical at `1fa64a45`, `6fdc390c` and `b7380181`.
- The published verifier, `ac5/verify_receipts.py`, exits 0 on them.

**Scratch commit** `66ba2106`, read through the GitHub commits API:

- Its sole parent is `6af65a15`. It changes one file: docs.yml:323 becomes `python3 scripts/check_py_idiom.py || true`.
- #506 is closed and was never merged.

**Raw lines** (`grep -n` on the verified blobs):

| Receipt lines | Observation |
|---|---|
| ac5-act/01.log:1837 | The Python idiom gate step succeeds. |
| ac5-act/01.log:1902-1904 | The contract step fails with one finding: "job `docs-check` step 34 (`Python idiom gate`) ... line 1", over 1505 items. |
| ac5-act/01.log:1909 | The docs-check job fails. All 35 earlier docs-check steps succeeded. |
| ac5-act/02.log:37-39, :44 | `full-ci-gate`'s contract step reports the same finding and fails; the job fails. |
| ac5-act/02.log:88, :99, :105 | verilator-suites finds 0 of 5 shards and sees skipped workers; the job fails. |
| ac5-act/02.log:149, :161, :167 | yosys-portability finds 0 of 4 shards and sees skipped workers; the job fails. |
| act-draft-fast/01.log:3679 | The normal 6af65a15 docs workflow passes. |

**Retention judgment.** Retaining this measurement for ad624931 is justified by unchanged execution artifacts:

- All workflow blobs and act_ci.py are identical at 6af65a15 and ad624931.
- Every production function and constant of ci_events.py is identical. That includes the records, the normalization and the comparator.
- The only executable changes are reachable only from `--selftest`. The AC5 path never reaches `--selftest`, because line 1 of both contract scripts is `--check`.
- The only changed input on the path is CI_WORKFLOWS.md, which `--check` reads as POLICY. It leaves the diagnostic unchanged. The finding the head checker reports natively for the same edit is byte-identical to the finding recorded in both act logs, over the same 1505 items (p12). The base checker accepts the edit.
- The normal docs-check at this head passes every step before the contract step. Hosted docs-check succeeded at 06:10:52 UTC (GitHub state), and A10's 40 commands exited 0. Both are attributed.

This remains a measurement at 6af65a15. It is not an act run at the exact new head, and this report does not present it as one.

## Gates run by R220 at ad624931

These exit 0 (logs/02, logs/03, logs/gates):

- `ci_events.py --check`, over 1505 items;
- `ci_events.py --selftest`, with 1144 arms;
- `docs_check.py`: 0 findings over 163 md files and 826 scrubbed files;
- `gen_toc.py --check` and `gen_toc.py --verify-anchors`;
- `check_doc_paths.py`: 824 cited paths resolve;
- `check_em_dash.py --base b17580b9`: 0 findings over 47 added lines;
- `check_doc_style.py`;
- `git diff --check b17580b9 ad624931`.

These refused with exit 2, by design, because protocol-processor and gptp-processor are not initialized in this clone, and were not reproduced: `check_py_idiom.py`, `check_hygiene.py --check`, `measure_fail_fast.py --check`, `check_todo_ownership.py` and `measure_control_flow.py --selftest`.

## Completion ledger (reviewer-owned, R220-2)

| Lens | Covering round | Head | State |
|---|---|---|---|
| Conformance | R220-2 | ad62493186576144f9fa1568babad012bc9ad8ca | covered clean |
| RTL | R220-2 | ad62493186576144f9fa1568babad012bc9ad8ca | covered clean |
| Robustness | R220-2 | ad62493186576144f9fa1568babad012bc9ad8ca | covered clean (one SUGGESTION) |
| Tests | R220-2 | ad62493186576144f9fa1568babad012bc9ad8ca | covered clean |
| Docs | none (R220-2 applied it) | ad62493186576144f9fa1568babad012bc9ad8ca | not covered: F3 open (MINOR) |

- All five lenses were applied at this head. None was carried forward from R220-1.
- **What a fix for F3 un-covers:**
  - Any F3 fix edits item 12, which AC4 names, and the page the checker reads. Docs and Conformance must therefore be applied again at that head, and `--check` and `--selftest` rerun there.
  - If the fix changes only that prose and the self-test arm set is unchanged, RTL, Robustness and Tests remain banked at ad624931.
  - Any change to the checker or the workflows un-covers them.

## Execution gates not judged here

A10 comment 5772174202 lists the gates still in flight or pending. None is called PASS here, and nothing in this report says the PR is merge-ready:

- the exhaustive native checks for ad624931;
- the trusted draft act replica for ad624931;
- the ready-head act replicas;
- hosted `verilator-suites` and `yosys-portability` at a ready head. At 06:04 UTC both were skipped on the draft no-op path, which is not exhaustive evidence;
- candidate-merge validation;
- post-merge containment.

## Evidence limits

- **Not run by R220:** act or Docker, hosted runs, the full parent RTL sweep, Yosys, the processor suites, gPTP make, behave, the builder, lint, xvlog, and the five code-quality scans listed above.
- **Submodules:** all four were uninitialized (`-`) in this clone at entry and at exit, and R220 did not initialize them. The checker and the doc gates R220 ran do not read submodule trees.
- **Attributed, not reproduced:**
  - A10's act receipts at 6af65a15;
  - A10's 40 manager/builder commands at ad624931;
  - A159's author evidence;
  - GitHub's hosted check-run state, read at 06:48 UTC.
- **F3 runtime effect:** p7 and p11 show that `--check` accepts the pin-step edits. R220 did not run a workflow to observe their effect at run time.
- **Probe hygiene:** probes mutated only in-memory worlds, or disposable `git archive` scratch copies in the system temporary directory, which have since been removed.
- **Independence:** R220 did not contact the author or R219.

## Integrity

At exit, the clone is unchanged:

- HEAD is `ad62493186576144f9fa1568babad012bc9ad8ca`, with tree `6b279253`.
- `git status --porcelain=v2 --untracked-files=all --ignored` is empty.
- The hash of `git ls-files -s` equals its entry value, `d062a5e4...`.
- All 850 tracked non-gitlink files re-hash to their index blob ids, and the index equals HEAD.
- No assume-unchanged or skip-worktree flag is set, and there is no `__pycache__`.
- `git submodule status` is unchanged from entry: `external`, `gptp-processor`, `protocol-processor` and `third_party/verilog-axis` are all uninitialized (`-`), at their recorded gitlinks.

No commit, push, public write, merge, install, privileged action, hardware access or subagent was made.

## Receipts

`README.md` beside this report lists the layout and the commands:

- `logs/`: entry and exit state, the CLI runs, the probe outputs, and every mutant's complete self-test output under `logs/p3-cli/`;
- `probes/`: p1 to p12, plus `common.py`;
- `receipts/`: snapshots of the public state and the public evidence.

R220-2 FINISHED
