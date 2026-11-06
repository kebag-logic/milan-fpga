# HANDOFF: #665 lane S5, round 3, [A702d]

STATUS: REVIEW READY. Head `3f8caae5eca7e681c3452eacdd818d1033a89f8d`, one commit on `26ba56e1`, no rebase, no force, nothing pushed.

Repository: origin is `kebag-logic/milan-fpga`, verified; `protocol-processor` verified as its own top level with the processor repository as origin. Target `dev-soft-core`.
Receipt paths below are under `receipts/`, indexed by `receipts/INDEX.md`, generated from the files present.
TAKEN posted: issuecomment-6692914323. REVIEW READY posted: issuecomment-6693645158; text in `REVIEW-READY-COMMENT.md`. PR body: `PR-BODY.md`, from the live body, which equalled the round 2 file byte for byte.

## Authority

- Assignment: [A10] issuecomment-6692737899 (round 3), on R783-2 (issuecomment-6692731463) and R784-2 (issuecomment-6692599602). Copies: `issue-6692737899.md`, `review-6692731463.md`, `review-6692599602.md`.
- Grading unchanged, as ruled in issuecomment-6682851386 (`issue-6682851386.md`).

## No re-measurement

`run.py`, `hooks.py`, `hooks_build.py` and `hooks_soc.py` have the same blobs at `26ba56e1` and the head, so run.py's graded output does not change, and the 732-path measurement was not rerun, as the assignment allows. At the head's code all four published `table.md` re-render byte for byte (`probes/doc_checks.txt`, `probes/verdict_independence.txt`). Scope: `probes/scope.txt`.

## Commit

| Commit | What |
|---|---|
| `3f8caae5` | `hooks_selftest.py` and `README.md`: the mutants on their rules, the grading rules pinned, the amended-bounds wording. |

## Changes (file:line at the head, reason)

| File:line | Change | Reason |
|---|---|---|
| `tb/verilator/ctrl_service_hooks/hooks_selftest.py:42`, `:45` | `GRADE_ALL`, `AGING_GROUP` | what the reshaped mutants wrap, as written |
| `hooks_selftest.py:63-64` | `HELD_FIELDS`, `HELD_LABELS` | item 2: one statement of the held rows' labels, for both branches |
| `hooks_selftest.py:451` | the held row's `ms` | item 2: `hp-row-ms-zero`, `hp-ms` |
| `hooks_selftest.py:457` | the held margin at a non-integer value | item 2: `hp-margin-round`, so the README's sentence holds for the margin |
| `hooks_selftest.py:458-459` | labels by `HELD_FIELDS`, `probe` added | item 2: a table reads `probe` |
| `hooks_selftest.py:479-482` | a push never sent: cycles, W, margin and labels | item 2: `hm-cycles`, `hm-wait`, `hm-margin`, `hm-group`, `hm-path`, `hm-interface`, `hm-family` |
| `hooks_selftest.py:495-496`, `:501-502`, `:510` | rows at a slack of 6,490 and 6,489 in place of `near`, the two slacks asserted, 7 paths | item 2: `s-narrow-le`, the boundary at the swing and one below it |
| `hooks_selftest.py:686` | `narrow_under` | the two boundary mutants |
| `hooks_selftest.py:726` | `graded_by_amended` leaves `bound_ms`, reads the column at one interface | item 1, R784-2 F-1; also R783-2 S4 |
| `hooks_selftest.py:733` | `findings_by_amended` | item 1: a mutant that reaches the `LATE` rule |
| `hooks_selftest.py:741` | `superseded_by_any_row` | the audit's third mutant, below |
| `hooks_selftest.py:747` | `window_before_arm` | item 1: the real group, only the marks moved |
| `hooks_selftest.py`, `MUTANTS` | 15 new names, one the old `supersede` edit renamed, and 3 reshaped: 94 in all | items 1, 2 |
| `README.md:206` | says what is pinned, and no more | item 2: "every rule" narrowed; the labels pinned as well |
| `README.md` mutant table | regenerated from `MUTANTS` by `scripts/readme_mutants.py` | 94 rows |
| `README.md:459` | R783-2's sentence, then the difference between the two readings | item 3 |
| `README.md:469` | "leaves" is "is committed", and a clause on the first notice | R784-2 RESIDUE-1; R783-2 S5's first half = R784-2 S-3, the same edit |

The `ARM`, `GRADES` and `LATE` assertion lines are byte-identical to `26ba56e1`, so R784-2's probe text matches unedited. `MUTANTS` stays a list of 3-tuples, which both packets' scripts unpack.

No firmware, RTL or shared harness file is edited. No file outside `tb/verilator/ctrl_service_hooks/` differs from the base.

## New and reshaped mutants, each with what it fires

No new check: 28 in all. Five new assertions in three checks, the held labels widened to `probe`, and 94 mutants: 15 new names, one of them the old `supersede` edit renamed, and 3 reshaped, the 18 rows below. Lines are in `hooks_selftest.py` at the head.

| Mutant | Check | Fires | Failing words |
|---|---|---:|---|
| supersede: the table names another group | a refusal is superseded only by its own path | `:594` | `superseded: {'rows': [{'hook': 'H-DISC', 'group': 'hooks-disc-aging'...` |
| supersede: any later group supersedes a refusal | a refusal is superseded only by its own path | `:596` | `other interface: {'rows': [{'hook': 'H-DISC', ...` |
| aging: the window opens before the arm (the earlier rule) | the aging window opens after the arm | `:618` | `interface 0: the window opens before the arm (25 > 23)` |
| held: its row reports no time | the held push's grade | `:451` | `the held row reports 0.0 ms, not its service` |
| held: its row reports a millisecond more | the held push's grade | `:451` | `the held row reports 21.0 ms, not its service` |
| held: its margin is rounded to the millisecond | the held push's grade | `:457` | `the held margin is 80, not 1000 - 900 - 20.00002` |
| held: it names another probe | the held push's grade | `:459` | `held row ('H-COUNTERS', 'hooks-counters', 'counters.first.if0', ...` |
| held missing: it records CPU cycles | a held push never sent | `:479` | `a push never sent records a service: {...` |
| held missing: it records a W | a held push never sent | `:479` | `a push never sent records a service: {...` |
| held missing: it records a margin | a held push never sent | `:479` | `a push never sent records a service: {...` |
| held missing: it is another group's | a held push never sent | `:482` | `missing row ('H-COUNTERS', 'hooks-x', ...` |
| held missing: it is another path's | a held push never sent | `:482` | `missing row (..., 'counters.x', 'notify', 0)` |
| held missing: it is another interface's | a held push never sent | `:482` | `missing row (..., 'notify', 1)` |
| held missing: it is another family's | a held push never sent | `:482` | `missing row (..., 'aecp', 0)` |
| summary: a fit by the swing itself is narrow | the worst path and the counts | `:512` | `2 narrow fits, not 1` |
| summary: a fit one cycle under the swing is not narrow | the worst path and the counts | `:512` | `0 narrow fits, not 1` |
| amended: the column grades a path | the amended column grades nothing | `:572` | `the amended bounds graded a path` |
| amended: a finding reads the column | the amended column grades nothing | `:575` | `findings []` |

## The audit

`scripts/mutant_audit.py`, receipt `probes/mutant_audit.txt`. For each mutant it records the assertion fired, its line and its failing words, then deletes that assertion in memory and reruns until the mutant escapes, so the chain lists everything holding it. A mutant counts as `own rule` only when its first assertion carries the text in `scripts/mutant_rules.py`, and it fails by an assertion, not an exception.

- **Result at the head:** 94 of 94 on their own rule, rc 0.
- **The rule table is a judgement.** I wrote it by reading each mutant beside its check, not from the audit's output. A reviewer can dispute any row.
- **Positive control:** on a clean clone of `26ba56e1` it flags exactly three, rc 1, the required result (`probes/mutant_audit_previous_head.txt`): `supersede: any later group...`, the `aging` window mutant and `amended: the column grades a path`.
- **Chains:** 91 escape, 59 after one deletion and 32 after more. Three end in an exception once their rule is gone: `aging: the sink still waits...` (IndexError), `summary: alone and under load are not apart` (KeyError), `ALL: no descriptor has a row` (AttributeError). Each is downstream of the deletion, and each one's first assertion is its rule.

## Reviewers' verification, re-run at the head on a clean clone

| Reviewer's check | Result | Receipt |
|---|---|---|
| R784-2 `rule_probes.py`, unedited | A 94 of 94; B escapes the aging mutant; C escapes both amended mutants; D1 fires the arm rule, D2 `the amended bounds graded a path`, D3 `findings []`; D4 and D5 unchanged (suggestions) | `probes/rule_probes.txt` |
| R783-2 `source_mutants.py`, unedited | 48 of 58 killed, up from 37; the six, the four labels and `hp-margin-round` killed, every kill on a `FAIL` line; 10 survivors, none claimed | `probes/source_mutants.txt` |
| R784-2 `assert_sites.py`, `mutant_audit.py` | 94 by assertion, 0 raised, 0 escaped | `probes/assert_sites.txt`, `probes/r784_mutant_audit.txt` |
| R783-2 `mutant_audit.py` | rule 94, crash 0, escaped 0 | `probes/r783_mutant_audit.txt` |
| R783-2 `amended_audit.py`, R784-2 `amended_table.py` | exactly `counters.all.t5.i1` to `t5.i4` on 8x8 answering, 0 H-SRP paths between 18 and 20 ms | `probes/amended_audit.txt`, `probes/amended_table.txt` |
| R784-2 `verdict_independence.py` | 0 verdicts unlike the base rule; summaries and tables equal the published ones | `probes/verdict_independence.txt` |
| R783-2 `doc_checks.py`, R784-2 `doc_figures.py` | 16 of 16 plants, tables byte-equal, 94 README rows, no mismatch | `probes/doc_checks.txt`, `probes/doc_figures.txt` |
| R783-2 `vacuity_probe.py` | 0 unplanted matches as written; S1's moved-path case unchanged, not taken | `probes/vacuity_probe.txt` |
| R783-2 `comment_scan.py` | 0 label matches and 0 U+2014, over this round's and the whole lane's added lines | `probes/comment_scan.txt` |
| R783-2 `verify_clone.py` | head, tree and index exact; 1,496 files rehashed, 0 differ; 0 status lines | `probes/verify_clone.txt` |

`compare_rounds.py`, `compare_runs.py` and the simulations were not run: they compare measurements, and none changed.

## Disclosures

- **A third mutant, found by the audit.** `supersede: any later group supersedes a refusal` failed the positive control and never reached `only by its own path`: with `:575` deleted it escaped at `26ba56e1`. Neither review named it. Item 1 requires the audit sentence to be true of all of them, so it is fixed, and the old edit stays as `supersede: the table names another group`.
- **A departure from D2's shape.** R784-2 gave D2 as the grading mutant, but D2 reads the column at two interfaces and does not escape probe C: `:580`, the table's `NO`, is a third assertion that catches it. Measured before editing. Loosening that pin would weaken a test, so it stays, and the mutant reads the column at one interface, where only SRP's verdict moves. With `:572` alone deleted it still fails on `:575`, because a finding follows from its verdict; with both deleted, as probe C does, it escapes.
- **A false pass, not cited.** My first `source_mutants.py` run reported 58 of 58 killed. Every kill was a `FileNotFoundError`: the script builds symlinks from its root argument, and I gave it a relative path. The cited run has an absolute path, 0 setup crashes, and every kill on a `FAIL` line.
- **The privacy gate's reach.** `push-privacy-check.py` does not catch `/data/...` or `/srv/...` paths, found by its positive control. `scripts/text_privacy.py` adds that scan for the PR body and the comment, with planted lines of its own.
- **`README.md:206`** was narrowed beyond the ruling's "every rule": it also now says no path's verdict and no `LATE` finding reads the column, rather than that the column grades nothing, because `a-slack-reads-column` and `a-exit-reads-column` still survive.
- **The PR's round 2 rows** that R783-2 and R784-2 showed overstated are corrected in place, and one says that its audit of 79 was wrong about three.

## Suggestions

Taken, the same edit covering them: R783-2 S4; R783-2 S5's first half = R784-2 S-3.
Not taken, as ruled: R783-2 S1, S2, S3, S5's `KeyError`; R784-2 S-1, S-2, S-4.

## Open questions

- **For the maintainer, unchanged:** the amended column's scope, and the one-path or per-descriptor decision. The four rows are where the two readings differ.
- S5's acceptance "each hook within its bound" stays open on #665, by the ruling.
- **For the manager:** hosted and local acceptance at the exact head, and the current merge candidate. Not re-merged this round.

No STOP condition was met: no firmware, RTL or shared-harness change was needed.

## Gate table

At `3f8caae5`, each on a clean clone. Every receipt ends with its rc.

| Gate | Command (from the clone's root) | Result | Receipt |
|---|---|---|---|
| Hook self-test | `python3 -B tb/verilator/ctrl_service_hooks/run.py --self-test` | rc 0; 28 of 28 checks, 94 of 94 mutants | `probes/hooks_selftest.txt` |
| Hook self-test, direct | `python3 -B tb/verilator/ctrl_service_hooks/hooks_selftest.py` | rc 0; the same | `probes/hooks_selftest_direct.txt` |
| The audit | `python3 -B mutant_audit.py <clone> mutant_rules.json` | rc 0; 94 of 94 on their own rule | `probes/mutant_audit.txt` |
| The audit's positive control | the same, on a clone of `26ba56e1` | **rc 1 is the required result**; flags exactly three | `probes/mutant_audit_previous_head.txt` |
| R784-2's deletion probes | `python3 -B rule_probes.py <clone>` | rc 0; B and C escape as required | `probes/rule_probes.txt` |
| R783-2's source mutants | `python3 -B source_mutants.py <absolute clone> <scratch> 8` | rc 0; the six killed | `probes/source_mutants.txt` |
| Other probes of both packets | as listed above | each rc 0 | `probes/` |
| Docs, scope, idiom, CI and behave gates (`gates_s5.py`), with the hook and CPU budget self-tests | see each log's first line | 0 of 98 nonzero or left the tree dirty; behave 1977 steps passed; 1718 s | `docs/summary.md` |
| `git diff --check` | `git diff --check 5b5f4336 HEAD` | rc 0, also as a docs gate | `probes/scope.txt`, `docs/git_diff_check.log` |
| Privacy, the lane's diff | `python3 -B push-privacy-check.py <lane> 5b5f4336` | rc 0; 0 private lines | `probes/privacy_tree.txt` |
| Privacy, the public text | `python3 -B text_privacy.py PR-BODY.md REVIEW-READY-COMMENT.md` | rc 0; 0 findings, 7 of 7 planted lines found | `probes/privacy_text.txt` |

Not run again, and not in this round's gate set: the four runs, the 16 plants and the no-op control, the firmware self-test, the CPU budget harness, the builder, the boundary gate and the candidate merge. Their receipts stand in `665s5-a702b` at `78415f7a`, `d5add6f9` and `26ba56e1`. The full sweep and Vivado did not run, as no RTL changed. No hardware or bench access. Nothing pushed.
