[R333] POSITIVE - exact head ae729bbfd90934f4d56d3b02f1ffc652496b414d

Round R333-5 is an external independent re-cover of PR #572 (issue #231). It runs at the same head as my R333-4 round. No commit was added. The only matter judged is whether my R333-4 finding F1 is closed. F1 was about PR body text, not about a file in the tree.

- Head: `ae729bbfd90934f4d56d3b02f1ffc652496b414d`
- Tree: `c2c692fb14fe731e46ff03873c11a45a77adc4e8`
- Source base: `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`
- Live `dev` when this round was written: `831f94f4146cc45ec476f8c8dcf5afac7cd8eacf` (`receipts/ls_remote.txt`)

## Head identity (carry-over basis)

- **The live PR head is unchanged.**
  - `gh pr view 572 --json headRefOid` returns `ae729bbfd90934f4d56d3b02f1ffc652496b414d` (`receipts/pr572_view.json`). GraphQL returns the same value (`receipts/pr572_graphql_edits.json`).
  - `git ls-remote` shows that both `refs/pull/572/head` and `refs/heads/231-pp-shadow-baseline` equal `ae729bbf` (`receipts/ls_remote.txt`).
  - The PR is open, not a draft, and based on `dev` at `7eb3b0d4`.
- **The tree is the one R333-4 reviewed.**
  - The clone's `HEAD` is `ae729bbf`, with tree `c2c692fb` (`receipts/head_identity.txt`).
  - The history `7eb3b0d4..HEAD` has the same four commits as before, and `3a1477c5..HEAD` still changes only the two documentation pages.
  - The full diff still touches the same 13 paths (`receipts/diff_scope.txt`).
  - The four gitlinks are unchanged from base: `external` efeb541a, `gptp-processor` 5dce647a, `protocol-processor` 990f9652, `third_party/verilog-axis` 48ff7a7e.
- **Result.** A commit ID fixes its tree, so every artifact R333-4 covered under Conformance, RTL, Robustness and Tests is byte-identical here. Those results carry over.
- **Smoke check.** I re-ran the three fast-CI baseline self-tests at this head (`scripts/smoke.sh`, `receipts/smoke_selftests.txt`). All three return rc 0:
  - the preparation self-test: 40 inventory refusals with the restored control, 9 endpoint refusals, and export/CLI containment;
  - the maintained mutant campaign: control passes and all 28 named mutants are killed;
  - the reports self-test.
- **The clone was left clean.** After the runs, `git status --porcelain` is empty. The `git ls-files -s` digest is unchanged: `14ddf5bb…` before and after.

## F1 (R333-4, shared with R332-5 F1): CLOSED

**The requirement (R333-4 F1, `receipts/prior_R333-4_comment.md`):**

- The PR body must carry no status sentence that is false for the live PR.
- Verification: run `gh pr view 572 --json body,headRefOid`, confirm that no such sentence remains, and confirm that the head is still `ae729bbf`.

**The evidence at this round:**

- **The false paragraph is gone.** It read "This commit is local and unpushed. This body is a prepared replacement; the live PR has not been edited. Independent re-review, publication and final-head acceptance remain pending." That text no longer appears in the live body (`receipts/pr572_body.md`, sha256 `117191fc…`).
- **The new closing line is true.** Line 59 now reads: "`ae729bbfd90934f4d56d3b02f1ffc652496b414d` is the published PR head and is under independent re-review at this exact head." It matches the live `headRefOid`.
- **No other line claims a local, unpushed or unedited state.**
  - A case-insensitive scan for local/unpushed/pushed/unedited/edited/draft/pending/"will be"/awaiting/head found four lines (`receipts/body_state_terms.txt`).
  - Lines 11 and 35 use "local gate" in the CONTRIBUTING sense of locally executed gates. They say nothing about where the head is.
  - Line 49 is the Round 3 historical record, scoped to `3a1477c5`.
  - Line 59 is the corrected line.
- **Every commit ID in the body is consistent with the live PR** (`receipts/body_shas.txt`).
  - `ae729bbf` appears three times, at lines 5, 57 and 59, and each time it is the live head.
  - `7eb3b0d4` appears twice, at lines 47 and 57. Both times it is the em-dash gate base, which equals the live `baseRefOid`.
  - `3a1477c5` appears once, at line 49, as Round 3 history. It is the head's parent (`receipts/head_identity.txt`).
  - The numbers 5847401184 and 5847557806 are issue comment IDs.
- **The edit history matches the manager's account.**
  - GraphQL `lastEditedAt` is 2026-09-26T15:57:16Z, the latest `userContentEdits` entry (`receipts/pr572_graphql_edits.json`). The GraphQL body is byte-identical to the REST body.
  - That time is consistent with the manager's correction comment, issuecomment-5847675182, posted at 15:57:24Z (`receipts/manager_F1_correction_comment.md`). The comment says: body-only correction, no commit, and Rounds 1-3 unchanged as round-scoped history.
- **The Round 1-3 sections are historical records of their own rounds.** Each current-state statement in them is either round-scoped (for example, Round 3 "reviewed at `3a1477c5`") or still true at this head. The Round 3 counts (40, nine, five, nine, 28) match this round's smoke output.

**Conclusion.** F1's required outcome is met, and it was verified as its own Verification line prescribes. F1 is closed. R332-5 F1 is the same body line, per the manager's comment 5847675182, which answers both findings. This round has no evidence that it remains open.

## Findings

No new BLOCKER, MAJOR or MINOR finding.

## Lens results (per-lens evidence)

```text
[R333] PASS Conformance — issue #231 acceptance; assignment 5847557806; receipts/head_identity.txt; receipts/diff_scope.txt; receipts/smoke_selftests.txt — Head and tree are byte-identical to R333-4's clean coverage at ae729bbf. The body's Round 4 claims (two pages changed, gates rc 0, mutant control passes and all maintained mutants fail) are consistent with the tree and with the smoke re-run.
[R333] PASS RTL — receipts/head_identity.txt (gitlinks, tree c2c692fb); receipts/diff_scope.txt (no hdl/ path, no gitlink change vs 7eb3b0d4) — There are no RTL, gitlink, constraint or synthesis-input changes relative to R333-4's clean coverage at the same head.
[R333] PASS Robustness — syn/ooc/pp_baseline.py at tree c2c692fb; receipts/smoke_selftests.txt — Every named refusal family (inventory 40, endpoint 9, export/CLI containment) still passes at this head. Bytes are unchanged from R333-4.
[R333] PASS Tests — syn/ooc/pp_baseline_mutants.py, syn/ooc/pp_baseline_reports_selftest.py, .github/workflows/rtl-fast.yml:209-211; receipts/smoke_selftests.txt — The control passes, all 28 maintained mutants are killed, the reports self-test passes, and fast CI still wires all three.
[R333] PASS Docs — PR #572 live body (receipts/pr572_body.md, lines 5, 49, 57, 59); receipts/body_state_terms.txt; receipts/body_shas.txt; receipts/pr572_graphql_edits.json; docs/findings/PP_SHADOW_BASELINE.md and docs/testing/PP_SHADOW_BASELINE_RECIPE.md at tree c2c692fb (unchanged since R333-4's clean page check) — F1 is closed. No line claims a local or unpushed head or an unedited PR, and every current-state commit reference matches the live headRefOid and baseRefOid.
```

## Completion ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #231 acceptance and assignment 5847557806 (R333-4); head/tree identity; smoke self-tests; live body Round 4 claims | R333-5 (carries R333-4 tree coverage at same head) | ae729bbfd90934f4d56d3b02f1ffc652496b414d |
| RTL | CLEAN | tree c2c692fb; gitlinks equal base 7eb3b0d4; 13-path diff scope with no hdl/ path | R333-5 (carries R333-4 at same head) | ae729bbfd90934f4d56d3b02f1ffc652496b414d |
| Robustness | CLEAN | syn/ooc/pp_baseline.py self-test refusal families, re-run | R333-5 (carries R333-4 at same head) | ae729bbfd90934f4d56d3b02f1ffc652496b414d |
| Tests | CLEAN | pp_baseline_mutants.py (28/28 killed, control PASS); reports self-test; rtl-fast.yml:209-211 wiring | R333-5 (carries R333-4 at same head) | ae729bbfd90934f4d56d3b02f1ffc652496b414d |
| Docs | CLEAN | live PR body (F1 closed); PP_SHADOW_BASELINE.md; PP_SHADOW_BASELINE_RECIPE.md (unchanged since R333-4) | R333-5 | ae729bbfd90934f4d56d3b02f1ffc652496b414d |

## Residue checklist (non-blocking, carried from R333-4)

These are optional. They do not affect lens coverage.

- **S1 (SUGGESTION, Docs), `docs/findings/PP_SHADOW_BASELINE.md:282-283`.** The single-synthesis-command template refusals are exercised but not named in the category list.
- **S2 (SUGGESTION, Docs), `docs/findings/PP_SHADOW_BASELINE.md:281`.** One fixed count remains ("nine original refusal cases"). It is accurate at this head.

## Real limits

- **The tree lenses were not re-derived in full.** This round re-covers them at the same head by byte identity with R333-4 plus a smoke re-run of the three fast-CI self-tests. I did not repeat R333-4's delta review or documentation gate runs.
- **No builder, synthesis, place-and-route, full Verilator/Yosys or parent/PP/gPTP bank was run.** That was out of scope. The measured area and timing figures rest on the manager's public evidence (review-evidence/231-r1 at c8a1a9a2) and earlier rounds.
- **No hardware proof exists.** Physical calibration was NOT RUN. Hosted "Physical gPTP" is SKIPPED, and skipped contexts are not hardware proof.
- **Hosted checks were still running.** At my snapshot (`receipts/hosted_checks.tsv`), `docs-check`, `elaborate` and Verilator shards 0, 1, 2 and 4 were IN_PROGRESS. rtl-fast, full-ci-gate, all Yosys shards, Verilator shard 3, docs-check-no-git and wire-accountability were SUCCESS. I do not judge hosted acceptance.
- **I did not read R332-5's report before writing this verdict.** I checked it only afterwards (issuecomment-5847672858). Its F1 names the same body line (line 59) and the same quoted text, and prescribes the same verification. The evidence above therefore closes it too.
- **No candidate merge was built or validated.** This round validated the source at `ae729bbf` against base `7eb3b0d4` only. That is not the current-dev candidate.

## Pending manager duties

- Build and validate the final current-dev candidate merge (source base `7eb3b0d4`, live `dev` `831f94f4`), and record post-merge containment.
- Accept the hosted exact-head contexts once the in-progress Verilator shards, `docs-check` and `elaborate` finish, and the local act replica.
- Confirm that the internal review lane ([R332]) re-covers Docs at `ae729bbf`, so the two-positive bar in CONTRIBUTING is met.
- Obtain explicit maintainer merge authorization. Close #231 and move it to Done.

R333-5 FINISHED
