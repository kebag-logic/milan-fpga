[R693] POSITIVE - exact head 41f4a53cc0b12f143fa3e61a5339a11e79806ce9

# R693-2: internal cleared-context round-2 review of PR #782 (issue #781)

Head `41f4a53cc0b12f143fa3e61a5339a11e79806ce9`, tree `51524679ffb3046c28887b4c112fd1bf5a6ddfe4`, one commit on
`8a4fa2f9` (no rebase or amend). Source base and live dev: `a032c6d6e3775f145349d5a495c1e1ad12294936`. This is a delta
review. Code the delta does not touch keeps its round-1 lens verdict unless the delta changes something that code depends on.

## Verdict basis

- No BLOCKER, MAJOR or MINOR finding is open. Three RESIDUE items (wording only) and three SUGGESTIONs follow.
- The one prior blocking finding, R694-1-F1 (MAJOR, the hosted calibration had not been measured), is **resolved** at this head.
  See "Prior findings".
- The brief asked me to confirm that the run's cancellation was external. **It was not purely external.** The run was
  cancelled because rtl-fast's `yosys-elaboration` job at `8a4fa2f9` hit its own 30-minute job timeout. No test failed, and
  the measurement is unaffected. Details are under check (1). This feeds RESIDUE R1 and SUGGESTION S1.

## Checks against the focus list

### (1) The measurement

- **Run and job:** run 40131149135, `rtl-full`, `pull_request`, head_sha `8a4fa2f9…`. Job 120983200812, "Verilator shard
  4/17", conclusion `success`. Its step 23, "Run this exhaustive suite shard", ran from 2026-10-24T20:50:36Z to 21:01:31Z,
  which is **655 s**. Receipts: `receipts/run40131149135*.json`, `receipts/job120983200812.log` (REST format) and
  `receipts/job120983200812.ghrunview.log` (`gh run view --log` format).
- **Suites:** the log shows `shard: 4/17   selected suites: 4`. All four passed: `controller_rate`, `datapath`,
  `fw_service_budget`, and `media_phase` at 21:01:31.71Z. The summary reads
  `suites: 4   passed: 4   failed: 0   timed out: 0`, with 24996 checks and 0 in-suite failures.
- **Measured window:** `python3 scripts/suite_shards.py --measure` on the `gh run view --log` file prints
  `"media_phase": 582` (`receipts/measure-job120983200812.txt`). The window runs from fw_service_budget's PASS line at
  20:51:49.97Z to 21:01:31.71Z, 581.7 s, rounded up to 582.
- **Tree validated:** the run validated merge commit `e9df8b0a`. Its parents are `a032c6d6` and `8a4fa2f9`, and its tree
  `57cbe969…` equals `8a4fa2f9`'s own tree (dev is an ancestor), so "at `8a4fa2f9`" is accurate. Receipt:
  `receipts/target-e9df8b0a.json`.
- **Artifact:** `suite-logs-4` (id 12576025045). The zip's sha256 equals the API digest, `2d5ad7de…`. `TARGET_SHA` is
  `e9df8b0a`. `media_phase.log` ends `RESULT: PASS` and holds 28 case summaries, all with `failures: 0`, for 386 checks.
  The 28 are pins, render, blend and ofs, the 11 `DET_CASES`, and the 13 `CASES`. That is exactly the
  `tb/verilator/media_phase/Makefile:92` default target `run: pins render blend ofs det cases`, so the whole target ran and
  no case was skipped. Receipt: `receipts/artifact-suite-logs-4-summary.txt`.
- **Against the ruling's condition:** 582 s and 655 s are both well inside 1400/1.1 = 1272 s.
  1400 − 582 = 818 s, which is 58.4 % of 1400.
- **Cancellation, which was not external:**
  - rtl-fast run 40131149068, job 120983101989 (`yosys-elaboration`, `timeout-minutes: 30` at
    `.github/workflows/rtl-fast.yml:258`), started 20:45:23Z and was cancelled at 21:15:35Z.
  - Its check-run annotation reads **"The job has exceeded the maximum execution time of 30m0s"**
    (`receipts/annotations.txt`).
  - Its Yosys cache missed (`Cache not found for input keys: yosys-v0.66-…-8f83907f…-Linux`), so it built Yosys from source
    from 20:45:45Z to 21:02:15Z, about 16.5 min. It was still inside a passing gate step when the limit hit; every gate
    line before the cut reads PASS.
  - The cache key at `rtl-fast.yml:288` includes `hashFiles('.github/workflows/*.yml')`, and this PR changes `rtl.yml`. So
    the miss follows from the PR's own required workflow change.
  - rtl-fast's fail-fast observer (job 120982936824) then printed `{"first_failure": "yosys-elaboration", "conclusion":
    "cancelled"}` and ran `ci_fail_fast.py cancel`.
  - rtl-full's observer (job 120982936960) and its twelve in-flight shards carry the annotation "The run was canceled by
    @github-actions[bot]". The rtl-full observer's own "Cancel this run" step was skipped, so rtl-full itself detected no
    failure.
  - No test failed anywhere, and shard 4/17 had finished at 21:01:37Z, before any cancellation.
  - For comparison, dev's own push run at `a032c6d6` hit the cache and took 13 min 10 s for the same job
    (`receipts/dev-a032c6d6-yosys-elab.tsv`).

### (2) PROVISIONAL_SUITES, SUITE_SECONDS, comments and docs

- `scripts/suite_shards.py:147` reads `PROVISIONAL_SUITES: frozenset[str] = frozenset()`.
- `:116` reads `"media_phase": 1400`.
- `scripts/run_all_suites.sh:258` reads `media_phase) … ${SUITE_TIMEOUT:-1400}`, unchanged. The runner-contract copy at
  `scripts/measure_test_evidence.py:675` is also 1400.
- The sources comment at `suite_shards.py:71-75` states run 40131149135, job 120983200812, worker 4/17, 655 s, 582 s, and
  the three earlier windows over 900 s. The note at `:143-146` states "None is pending". The head arm at `:865-870` prints
  `ok   head no provisional figure is pending`, which my selftest receipt shows at line 15.
- `run_all_suites.sh:249-251` states the 582 s pass and the kept 1400 s.
- `docs/testing/CI_WORKFLOWS.md:438`, the #781 row, records the job, the worker, the run, the head, the step times, 655 s,
  582 s, 818 s (58.4 %), and why 1400 s is kept. The load paragraph at `:2950-2951` reads "`media_phase`'s kept
  1400-second budget at 1539 seconds: 81 inside its bound" (1620 − 1539 = 81, matching selftest worker 4/17).
- Every figure was rechecked against the hosted log and the selftest.
- **Comment rule:** the delta's new source comments name only issue IDs, run and job IDs, and worker indices. They show no
  bench lane label, lane name, review round, reviewer ID or issue-comment ID. There is no new comment-rule residue.
- The commit message is one line with no trailer.
- No stale "provisional media_phase" wording remains. `git grep -i provisional` over docs, scripts, .github and tests finds
  only unrelated uses and the generic new-suite rule in `TESTING.md:540`.

### (3) The open risk: nothing ties a measured suite's figure to suite_timeout

**Judgement: acceptable, and not a finding.** It is recorded as SUGGESTION S3. My evidence:

- **m1:** `"media_phase": 582` with PROVISIONAL empty passes the selftest. This is the expected escape, and it reproduces
  the author's statement.
- **m2:** `"media_phase": 1401`, one second above the suite's own deadline, also passes the selftest. No check refuses an
  estimate that is larger than the deadline.
- **The deadline is independently pinned.** Planting the driver arm at 582 s (m9) or 900 s (m10) is refused by the
  runner contract `measure_test_evidence.py --check` (rc 2, "the declared 1400/1800/…-second suite budgets changed").
- **The downside is bounded** (`receipts/worst-case-582.txt`). With the figure lowered to 582 s, the balancer moves
  `media_phase` to worker 1/17, predicted at 1473 s. If the suite then ran its full 1400 s deadline, that worker would take
  2291 s, 409 s inside its 45-minute (2700 s) job limit. A wrong lowering would therefore break the #727 60 % planning
  bound silently, but it cannot turn into a job timeout.
- **Every other measured suite works the same way.** Under the module rule, a figure equal to a fresh measurement is
  legitimate for those suites. The kept 1400 s is a ruled exception, and its reason sits beside the entry
  (`suite_shards.py:71-75`). Treating this as a defect of this PR would demand a new mechanism the issue does not require.

### (4) Gates, all run at the exact head in this clone

| Gate | Result | Receipt |
|---|---|---|
| `python3 scripts/suite_shards.py --selftest` | rc 0, `selftest: PASS`. Workers 0..15 are at most 1605 s of 1620 s. Worker 16/17 is 2032 s of 2160 s. | `receipts/gates/selftest.log` |
| `python3 scripts/ci_gate_workflows.py --check` | rc 0 | `receipts/gates/ci_gate_workflows.*` |
| `python3 scripts/ci_events.py --check` | rc 0, OK, 2199 contract items | `receipts/gates/ci_events.*` |
| Ownership listings: `--list`, `--ci-pieces --list`, `--ci-pieces --shard k/17 --list` for k = 0..16, at head and at a `git archive` of `8a4fa2f9` | 19/19 byte-identical. 64 suites and 81 units. The union of the 17 shards equals the piece list, with 0 duplicates. Shard 4 lists the four suites above. Shard 16 lists only `milan_dp_mclk__0`. | `receipts/gates/{head,base}-*.txt` |
| `lint_rtl.py --check`, pinned Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`) | rc 0, `LINT GATE: PASS (89 <= 89)` | `receipts/gates/lint.*` |
| `docs_check.py` | rc 0, 0 findings across 210 md files | `receipts/gates/docs_check.*` |
| `check_feature_status.py`, `check_doc_style.py` (and `--selftest`), `check_solution_docs.py`, `check_submodule_docs.py`, `check_gptp_docs.py` | each rc 0 | `receipts/gates/*` |
| `check_em_dash.py --base a032c6d6` | **not judged** locally: rc 2, the pinned Markdown renderer is not installed. The delta adds no non-ASCII character. The hosted docs run at this head passed. | `receipts/gates/em_dash.*` |
| `cd tests && behave --no-capture -f plain` | rc 0, 406 scenarios passed, 0 failed | `receipts/gates/behave.log` |
| `measure_test_evidence.py --check` (runner contract) | rc 0 at head | used as the oracle for m9 and m10 |

**Mutation campaign** (`scripts/mutants.py`, `receipts/mutants/SUMMARY.txt`): 11 runs, each on a disposable `git archive`
copy.

- The control passes.
- Caught as expected:
  - m3: 582 s left provisional;
  - m5: a misspelt provisional name;
  - m6: the provisional comparison disabled while nothing is pending;
  - m8: 1499 s;
  - m9: the driver arm at 582 s;
  - m10: the driver arm at 900 s.
- Escaped as expected:
  - m1: 582 s, not provisional;
  - m2: 1401 s;
  - m4: `media_phase` still provisional at 1400 s. This is the round-1 state, which is self-consistent.
- One escape I had not predicted, **m7**: `if problems or provisional:` changed to `if problems:` in the head arm, combined
  with a planted provisional mismatch. The head arm prints `FAIL head: media_phase: provisional figure 582 s …`, yet the
  run ends `selftest: PASS`. That line is unchanged since dev `a032c6d6`, so the delta did not cause it. With
  PROVISIONAL now empty it has no effect at this head. See SUGGESTION S2.
- The receipt's `as expected: 10` reflects that one wrong prediction of mine. It does not mean a check regressed.

### (5) The new head's own hosted run

Snapshot taken at 2026-10-24T23:09Z (`receipts/hosted-41f4a53c-snapshot.txt`):

- **Finished:** `rtl-fast` 40139678153 **success**, `docs` 40139677909 **success**, `elaborate` 40139677908 **success**.
  rtl-fast's `yosys-elaboration` hit the Yosys cache this time and finished in 16.5 min.
- **Still running:** `rtl-full` 40139678015 was `in_progress`, with no job failed or cancelled and 42 jobs successful so far.
- **The `media_phase` worker:** job 121008732969, "Verilator shard 4/17", **success**. Its suite step ran 22:47:47Z to
  22:58:30Z. `TARGET_SHA` is `f059e1c5`, whose parents are `a032c6d6` and `41f4a53c`, and whose tree **`51524679…` equals
  this head's tree** (`receipts/target-f059e1c5.json`).
- **Result:** `suites: 4   passed: 4   failed: 0   timed out: 0`. `--measure` gives **`"media_phase": 559`**
  (`receipts/measure-job121008732969.txt`; the REST log was given `gh run view` column prefixes because the run was still
  in progress).
- **Artifact:** `suite-logs-4` (id 12579170725, zip sha256 equal to the API digest `140b9b9a…`). 28 case summaries, 28
  with `failures: 0`, 386 checks, ending `RESULT: PASS` (`receipts/artifact-new-suite-logs-4-summary.txt`).
- The rest of `rtl-full`, the unions, the `verilator-suites` aggregate and `yosys-portability` had not concluded at my
  verdict. Accepting those hosted results is the manager's job.

## Findings

**R1 RESIDUE — Docs — PR #782 body, "Round 2: the hosted measurement", fourth bullet**
- Evidence: the bullet says "Twelve other Verilator shards and the fail-fast observer were cancelled from outside at 21:16Z
  to 21:18Z". The cause was rtl-fast `yosys-elaboration` (job 120983101989) exceeding its 30-minute job limit, after a Yosys
  cache miss that the PR's `rtl.yml` change caused through the workflow-hash key. The fail-fast cancel then reached rtl-full.
  Check (1) has the evidence.
- Impact: wording only. The measurement, the figure and this head's hosted results are unaffected. A cold reader is told
  that an external event cut the run short, when it was this head's own required fast job.
- Exact fix: replace the bullet with: "The run as a whole ended cancelled, but no test failed. rtl-fast's
  `yosys-elaboration` (job 120983101989) exceeded its 30-minute job limit: the PR's `rtl.yml` change re-keys the Yosys
  cache, so Yosys was built from source (about 16.5 min). Its fail-fast observer then cancelled this run's twelve
  in-flight Verilator shards and observer at 21:16Z to 21:18Z, after shard 4/17 had finished. At `41f4a53c` the cache hit
  and rtl-fast passed."
- The manager's round-2 assignment carries the same wording ("cancelled from outside"). It is manager text, so this is
  noted for the residue checklist and is not an author fix.
- Verification: the PR body text.

**R2 RESIDUE — Docs — `docs/testing/CI_WORKFLOWS.md:438` ("`scripts/suite_shards.py --measure` on the job log") and the
PR body "How to validate" (`--measure job-120983200812.log` "downloaded from run 40131149135")**
- Evidence: `--measure` reads only the `gh run view --log` layout (job, step and timestamp columns; `suite_shards.py:442`).
  The REST job-log download, which is also what the web UI's raw log serves, is refused:
  `cannot measure …: no 'shard: I/N   selected suites: K' line`, rc 2 (`receipts/measure-rest-format.txt`). It does fail
  closed.
- Impact: wording only, with no figure change. A reviewer who follows the text with the obvious download gets a refusal
  instead of 582.
- Exact fix: in the PR body, write
  `gh run view 40131149135 --log --job 120983200812 > job-120983200812.log` before the `--measure` line. In the row, write
  "(`scripts/suite_shards.py --measure` on the job's `gh run view --log` output)".
- Verification: text. Running the stated command reproduces 582.

**R3 RESIDUE — Docs — `docs/testing/CI_WORKFLOWS.md:438`, the local-measurement clause carried from dev (`dd2563439`, #632)**
- Evidence: the row calls the locally timed run "its whole default target (the pins, the blend, the offsets, eleven
  detector cases and thirteen loop cases, its five builds included)". The default target is
  `run: pins render blend ofs det cases` (`tb/verilator/media_phase/Makefile:92`). That adds `render`, and there are six
  builds: `build`, `pins-build`, `render-build`, `blend-build`, `ofs-build` and `det-build`. The hosted log also shows a
  `render` summary.
- Impact: wording only. The 787.5 s and 769.3 s figures measured the whole target and do not change. This clause predates
  this PR, and this PR re-wrote the row around it.
- Exact fix: "(the pins, the render, the blend, the offsets, eleven detector cases and thirteen loop cases, its six builds
  included)".
- Verification: text against `Makefile:87-160`.

**S1 SUGGESTION — Robustness, Tests — `.github/workflows/rtl-fast.yml:258` (`timeout-minutes: 30`) with `:288`
(`hashFiles('.github/workflows/*.yml')` in the Yosys cache key); this is pre-existing and is not in the delta**
- Evidence:
  - A cold Yosys build took about 16.5 min (20:45:45Z to 21:02:15Z), and the job was still inside a passing gate step when
    it hit the 30-minute limit. Dev's warm run of the same job took 13 min 10 s.
  - Any change to any workflow file re-keys the cache. A run in a scope where the new key has not been saved yet therefore
    starts cold.
  - This PR's `rtl.yml` change makes that true for the first push run on `dev` after merge. Dev's cache scope cannot see
    the key saved under `refs/pull/782/merge`, and rtl.yml's "Prepare pinned Yosys" job saves the key only about 17 min
    into the same run.
  - So dev's first post-merge rtl-fast is likely to time out in `yosys-elaboration` and fail-fast-cancel that push's
    rtl-full, exactly as at `8a4fa2f9`.
- Impact: post-merge containment noise, and possibly a red required context on dev, with no test failure. Every future
  workflow-changing PR hits the same thing on its first run.
- Optional outcome: a new Issue, since this PR's ruling forbids changing `timeout-minutes`. Options include keying on the
  Yosys recipe rather than every workflow file, restoring by prefix, or giving the cold path its own budget. Until then the
  manager should expect a cold-cache cancel on the first dev push and re-run once rtl-full's "Prepare pinned Yosys" has
  saved the key.
- Verification: the next workflow-changing head's first run, or the dev push run after this merge.

**S2 SUGGESTION — Tests — `scripts/suite_shards.py:879` (`if problems or provisional:`); pre-existing since `a032c6d6`**
- Evidence: m7 above. The planted arms in `provisional_selftest` (`:810-836`) exercise `provisional_problems` directly. No
  arm checks that `head_selftest` counts a head provisional mismatch into the failure total, so dropping `or provisional`
  prints FAIL but ends `selftest: PASS`.
- Impact: none at this head, because PROVISIONAL is empty. It matters again the next time a new suite is registered
  provisionally.
- Optional outcome: return the failure count from a helper and plant it, or fold the head comparison into the counted
  `bad` total.
- Verification: m7 turns the selftest nonzero.

**S3 SUGGESTION — Robustness, Tests — `scripts/suite_shards.py:76-141` against `run_all_suites.sh:252-261`**
- Evidence: m1 and m2, and the worst-case probe in check (3). A measured or kept figure is not tied to the driver deadline
  in either direction. 1401 s, above `media_phase`'s own 1400 s deadline, passes. 582 s also passes, while the ruling keeps
  1400 s.
- Impact: bounded, as computed above: no job timeout, only a silently broken 60 % planning bound.
- Optional outcome: refuse any `SUITE_SECONDS[s] > suite_timeout(s)`, since no passing window can exceed its deadline. Pin
  ruled kept-above-measured figures, such as `media_phase` at 1400 s, in a small table checked against `suite_timeout`.
- Verification: m1 and m2 turn the selftest nonzero.

## Prior findings at this head

My own pass came first. These are the prior rounds' findings, resolved or retained at this head:

| Finding | Status at `41f4a53c` | Evidence |
|---|---|---|
| R694-1-F1 MAJOR (Conformance, Robustness, Tests): the hosted calibration had not been measured | **RESOLVED** | Job 120983200812 completed with `success`, 582 s for the whole default target (28/28 cases), within 1272 s. This PR's own run at the new head gives 559 s. The figure and receipt are recorded at `suite_shards.py:71-75` and `CI_WORKFLOWS.md:438`, and PROVISIONAL is emptied at `:147`. 1400 s is kept per the round-2 assignment. The ruling's "only if the measurement fits 1400 s with 10 %" condition holds. No predicate was changed and no case was omitted. |
| R693-1 S1 SUGGESTION: `--expect` prose and the load table are not gated | Retained, optional | The delta does not touch either. The values at head are correct: the load paragraph's worker 4 figure, 1539 s, matches the selftest. |
| R693-1 S2 SUGGESTION: an over-provisioned worker count is not refused | Retained, optional | Untouched by the delta. |
| R693-1 S3 SUGGESTION: keep 1400 s and say 582 s is the dev-tree window | Largely adopted | 1400 s is kept, and the row records 582 s beside the earlier over-900 s windows. The row does not say that those windows came from heads changing `media_phase` inputs (#778, #779). Optional. |
| R693-1 S4 SUGGESTION: link the ruling comment from the row | Not adopted, optional | `CI_WORKFLOWS.md:438-441` still links only #673's ruling. |

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #781 body items 1-4; ruling (b) issuecomment-6388150329 and its measurement condition; round-2 assignment issuecomment-6390031279; `suite_shards.py:71-76,116,143-147`; `run_all_suites.sh:249-258`; `measure_test_evidence.py:675`; hosted job 120983200812 (582 s, 655 s) and job 121008732969 (559 s), each binding to the reviewed tree; 28/28 cases (no skip); PR body `Closes #781` | R693-2 | `41f4a53cc0b12f143fa3e61a5339a11e79806ce9` |
| RTL | CLEAN | `git diff a032c6d6..41f4a53c` touches no `hdl/`, `tb/` or gitlink, and the delta touches three non-RTL files; gitlinks match the HEAD tree (`receipts/submodule-status.txt`); `lint_rtl.py --check` PASS 89 <= 89 on pinned 5.050; the round-1 CI-architecture verdict holds, because the delta changes no workflow, generator or consumer | R693-2 | `41f4a53cc0b12f143fa3e61a5339a11e79806ce9` |
| Robustness | CLEAN | `provisional_problems` and `head_selftest` (`suite_shards.py:383-400,839-880`) with the empty set; m3, m5, m6 and m8 refused; driver-deadline pin (m9, m10 refused); the worst case of an unpinned figure (2291 s against 2700 s); `--measure` fails closed on a wrong log format (rc 2); the hosted cancellation chain traced to its cause (S1, which is pre-existing) | R693-2 | `41f4a53cc0b12f143fa3e61a5339a11e79806ce9` |
| Tests | CLEAN | selftest PASS; `ci_gate_workflows --check` and `ci_events --check` rc 0; 19/19 listings byte-identical to `8a4fa2f9`, 81 units each owned once; behave 406/406; 11-run mutation campaign (m7 is pre-existing, S2); hosted artifacts `suite-logs-4` at both heads verified against their API digests | R693-2 | `41f4a53cc0b12f143fa3e61a5339a11e79806ce9` |
| Docs | CLEAN (RESIDUE R1-R3 do not unclean) | `CI_WORKFLOWS.md:438,2950-2951`; `run_all_suites.sh:249-251`; `suite_shards.py:71-75,143-146`; the delta's comment-rule check; `git grep` for stale provisional wording; docs_check, doc_style (and selftest), solution, submodule, gPTP and feature-status gates rc 0; em-dash gate not run locally (delta all ASCII; hosted docs success at this head); PR body | R693-2 | `41f4a53cc0b12f143fa3e61a5339a11e79806ce9` |

## Real limits

- I ran no full suite sweep at this head. The delta changes only comments, prose, one printed message and the empty set, and
  the sweep reads these files only through its preflight selftest, which passes. The author's 64/64 sweep at `6f7b70ed` and
  the hosted shards are the suite execution evidence.
- No manager source bank ran at this exact head, and I claim none. I ran no act runner and no host `act_ci.py` or its
  selftest. The author reports that the trusted-dev `act_ci.py --selftest` passed; I did not reproduce it.
- `check_em_dash.py` was not judged locally, because the pinned Markdown renderer is not installed here and installing it
  was out of bounds.
- At the verdict, the new head's `rtl-full` was still running: the remaining shards, unions, `verilator-suites` and
  `yosys-portability`. Its `media_phase` worker had passed.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- The current-dev merge candidate is not validated by this review.

## Pending manager duties

- Accept or refuse the new head's complete hosted run 40139678015 and the rtl-fast, docs and elaborate runs, which had
  succeeded at the snapshot.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts.
- Expect the dev push after merge to start with a cold Yosys cache (S1). If rtl-fast's `yosys-elaboration` times out
  there, re-run once rtl-full's "Prepare pinned Yosys" has saved the key, and consider opening the S1 Issue.
- Carry R1, R2 and R3 to the residue checklist, including the "cancelled from outside" wording in the round-2 assignment.
- Post-merge containment and Issue closure per CONTRIBUTING.

R693-2 FINISHED
