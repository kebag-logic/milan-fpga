[R332] POSITIVE - exact head ae729bbfd90934f4d56d3b02f1ffc652496b414d

Round R332-6 is an internal, cleared-context re-cover of PR #572 for issue #231 at the same head as R332-5. There is no new commit. The only question in this round is whether the PR-body correction closes R332-5 F1. It does, and the verdict is POSITIVE.

- Head: `ae729bbfd90934f4d56d3b02f1ffc652496b414d`, tree `c2c692fb14fe731e46ff03873c11a45a77adc4e8`.
- Source base: `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`. Live `dev` at review time: `831f94f4146cc45ec476f8c8dcf5afac7cd8eacf`.

## Verdict summary

- **R332-5 F1 (MINOR, Docs, live PR body line 59): CLOSED.**
  - The body was edited at 2026-09-26T15:57:16Z. The edit replaced only that paragraph.
  - The body no longer says the head is local or unpushed, or that the PR is unedited.
  - The one current-state line names the live `headRefOid`.
- **R333-4 F1** is the same defect in the same paragraph. The same evidence closes it.
- **The head and tree are unchanged.** The local clone, `refs/heads/231-pp-shadow-baseline`, `refs/pull/572/head` and the API all give `ae729bbf`, tree `c2c692fb`. So the R332-5 coverage of Conformance, RTL, Robustness and Tests carries over.
- **Those four lenses were re-applied at this head** with the focused self-tests and mutant campaign (see the lens results below).
- **All five lenses are CLEAN.** No BLOCKER, MAJOR or MINOR finding is open.

## Evidence for the F1 decision

| Check | Result | Receipt |
|---|---|---|
| Live `headRefOid` | `ae729bbfd90934f4d56d3b02f1ffc652496b414d`. PR is open and not a draft; base is `dev` | `receipts/pr572.json` |
| Remote refs | Branch and `refs/pull/572/head` both at `ae729bbf` | `receipts/ls_remote.txt` |
| Remote commit tree | `c2c692fb14fe731e46ff03873c11a45a77adc4e8`, parent `3a1477c5` | `receipts/remote_commit.json` |
| PR commit list | 4 commits, last `ae729bbf`; no commit added since R332-5 | `receipts/pr_commits.txt` |
| Body edit history | The last edit changes line 59 only. It removes "This commit is local and unpushed. This body is a prepared replacement; the live PR has not been edited. Independent re-review, publication and final-head acceptance remain pending." It adds "`ae729bbf…` is the published PR head and is under independent re-review at this exact head." The latest edit equals the live body | `receipts/pr_edits.json`, `receipts/body_last_edit.diff` |
| Forbidden-claim scan | No local, unpushed, unedited, prepared-replacement or publication-pending claim. The only hits for "local" are "local gate(s)" on lines 11 and 35, which are gate names | `receipts/body_scan.txt`, `receipts/check_pr_body.txt` |
| Negative control | The same pattern finds the pre-correction line 59, so the scan can fail | `receipts/negative_control.txt` |
| Full SHAs in body | See the SHA list below | `receipts/check_pr_body.txt` |
| Status truth | "Under independent re-review at this exact head" is true: R332-6 and R333-5 were publicly started at `ae729bbf` | `receipts/recent_pr_comments.txt` |
| Scripted re-check | `scripts/check_pr_body.sh` returns `result=PASS`, rc 0 | `receipts/check_pr_body.txt` |

Full SHAs named in the body:

- Current head `ae729bbf`: lines 5, 57 and 59.
- Source base `7eb3b0d4`: lines 47 and 57, as the em-dash reference.
- Round-3 head `3a1477c5`: line 49, as round-scoped history.

No current-state line names any other commit.

Round-scoped history in Rounds 1-3 was left in place, as allowed. It is still true at this head:

- Round 3 says "40 inventory refusals". The self-test at this head prints 40 `baseline inventory refusal … PASS` lines (`receipts/selftest_counts.txt`).
- Round 3 says "all 28 named mutants". The mutant campaign at this head reports 28 `PASS` lines and no other lines (`receipts/run_syn_ooc_pp_baseline_mutants.py.log`).
- Round 2's "ten" mutants refers to that round's head.

## Lens results at this head

[R332] PASS Conformance — `receipts/round4_diffstat.txt`, `receipts/full_diffstat.txt`, `receipts/remote_commit.json` — The tree is identical to the one R332-5 covered against the #231 acceptance and the round-four text-only assignment. The body correction states the true head, and the round-scoped claims match what executes at this head.

[R332] PASS RTL — `receipts/full_diffstat.txt`, `receipts/integrity_after.txt` — The full diff from `7eb3b0d4` has no `hdl/` path and no gitlink change. Gitlinks at this head: `external` `efeb541a`, `gptp-processor` `5dce647a`, `protocol-processor` `990f9652`, `third_party/verilog-axis` `48ff7a7e`. R332-5's RTL coverage carries over unchanged.

[R332] PASS Robustness — `receipts/run_syn_ooc_pp_baseline.py_--selftest.log`, `receipts/integrity_after.txt` — Every refusal arm passes. After the runs, the clone has zero tracked, untracked or ignored residue once the reviewer-created `__pycache__` is removed. The code is byte-identical to R332-5's head.

[R332] PASS Tests — `receipts/exact_head_runs.txt`, `receipts/run_*.log` — Results of the three commands that `.github/workflows/rtl-fast.yml` runs:
- `pp_baseline.py --selftest`: rc 0.
- `pp_baseline_mutants.py`: rc 0; the control passes and 28 of 28 mutants are killed.
- `pp_baseline_reports_selftest.py`: rc 0.

[R332] PASS Docs — live PR #572 body (`receipts/pr572_body.md`, sha256 `cffa50ce…`), `receipts/body_last_edit.diff`, `receipts/check_pr_body.txt` — F1 is closed and no current-state line is false. The committed `docs/findings/PP_SHADOW_BASELINE.md:278-288` and `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:379-391` are byte-identical to R332-5's head (same tree), where the seven documentation gates were covered clean.

## Findings

None open at this head.

## Prior public findings at this head

| Prior finding | Status | Evidence |
|---|---|---|
| R332-5 F1 (MINOR, Docs): live PR body line 59 claims the head is local and unpushed and the PR unedited | **CLOSED** | `receipts/body_last_edit.diff`, `receipts/check_pr_body.txt`, `receipts/negative_control.txt` |
| R333-4 F1 (MINOR, Docs): the same paragraph | **CLOSED** (same evidence) | as above |
| R332-4 F1 = R333-3 F1 (fixed counts in page and recipe) | Remains **CLOSED** | Same tree as at the round that closed it (`receipts/remote_commit.json`) |
| R332-3 F1 and F2; R333-2 F1 and F4; R333-1 F1-F4; R332-1 F1-F3 | Remain **CLOSED** | Closed at earlier heads; the tree is unchanged since R332-5 |

## Residue checklist (suggestions; they do not affect coverage)

- **R332-5 S1 / R333-4 S2:** `docs/findings/PP_SHADOW_BASELINE.md:281` still says "nine original refusal cases". This is true at this head (the self-test prints `9 refusals PASS`). The optional change is to describe that arm by category.
- **R333-4 S1:** the two template refusals (`syn/ooc/pp_baseline.py:386-394`) are not named among the categories on `PP_SHADOW_BASELINE.md:282-283`. The optional change is to add "template".
- **R332-5 S2:** `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:382` calls every maintained mutant "enforcement-removal", but three of them alter an enforcement point rather than remove it. No action is needed.
- **Invocation note (new, no finding):** `python3 -I syn/ooc/pp_baseline_reports_selftest.py` fails with `ModuleNotFoundError: pp_baseline_mapping` (`receipts/run_syn_ooc_pp_baseline_reports_selftest.py.log`). Isolated mode drops the script directory from `sys.path`.
  - The workflow, `scripts/ci_events.py` and the recipe all invoke it without `-I`, and that form passes (`receipts/run_reports_selftest_noI.log`).
  - Recorded only so that a future isolated-mode runner is not surprised.

## Completion ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #231 acceptance and round-four assignment (via R332-5 at the same tree); `receipts/round4_diffstat.txt`, `receipts/full_diffstat.txt`, `receipts/selftest_counts.txt` | R332-6 (R332-5 same head) | ae729bbfd90934f4d56d3b02f1ffc652496b414d |
| RTL | CLEAN | `receipts/full_diffstat.txt` (no `hdl/`); gitlinks in `receipts/integrity_after.txt` | R332-6 (R332-5 same head) | ae729bbfd90934f4d56d3b02f1ffc652496b414d |
| Robustness | CLEAN | `receipts/run_syn_ooc_pp_baseline.py_--selftest.log`; `receipts/integrity_after.txt` | R332-6 (R332-5 same head) | ae729bbfd90934f4d56d3b02f1ffc652496b414d |
| Tests | CLEAN | `receipts/exact_head_runs.txt`; `receipts/run_syn_ooc_pp_baseline_mutants.py.log`; `receipts/run_reports_selftest_noI.log` | R332-6 (R332-5 same head) | ae729bbfd90934f4d56d3b02f1ffc652496b414d |
| Docs | CLEAN | live PR body `receipts/pr572_body.md`; `receipts/body_last_edit.diff`; `receipts/check_pr_body.txt`; `receipts/negative_control.txt`; committed pages at the same tree | R332-6 | ae729bbfd90934f4d56d3b02f1ffc652496b414d |

## Integrity after probes

- No source edit was made, and no probe mutated the tree. The mutant harness restores its own fixtures.
- After the runs, HEAD is `ae729bbf` and the tree is `c2c692fb`.
- `git status --porcelain --ignored` is empty.
- The worktree and index match HEAD.
- The `git ls-files -s` digest equals the HEAD `ls-tree` digest (`14ddf5bb…`), so blob bytes and modes match.
- The four gitlinks match the listing above (`receipts/integrity_after.txt`).

## Real limits

- **Earlier-round coverage is reused, not re-run.** This round did not re-run the builder, synthesis, placement, parent, PP, gPTP or Yosys banks, or the documentation CI gates. Those were covered at this same tree by R332-5 and earlier rounds, and by the manager's source banks. The reported area and timing figures are not re-measured here.
- **Hosted checks were only partly finished when fetched.** At 15:59Z (`receipts/hosted_checks.tsv`):
  - completed with success: `rtl-fast`, `verilator-lint`, `yosys-elaboration`, all four Yosys shards, Verilator shard 3/5, `docs-check-no-git`, `bdd-conformance`, `wire-accountability`, `full-ci-gate`;
  - still in progress: `docs-check`, `elaborate`, and Verilator shards 0, 1, 2 and 4;
  - skipped, which is not evidence: `Physical gPTP`.
- **No physical evidence.** Physical calibration was NOT RUN, and the field skips are not hardware proof.
- **Scoped Verilator was not used.** No probe needed it.

## Pending manager duties

- Accept the exact-head hosted and act evidence once the in-progress contexts above finish.
- Build and validate the current-`dev` candidate merge result: source base `7eb3b0d4…`, live `dev` `831f94f4…`.
- Obtain explicit maintainer merge authorization.
- Confirm the second independent positive review at this exact head (R333-5).
- Carry out post-merge containment. Update the #229 merge-commit link, as retained from earlier rounds.
- Close #231 and move it to Done.

R332-6 FINISHED
