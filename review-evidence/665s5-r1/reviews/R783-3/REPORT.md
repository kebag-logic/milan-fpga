[R783] NEGATIVE - exact head 3f8caae5eca7e681c3452eacdd818d1033a89f8d

# R783-3: issue #665 lane S5 / PR #844, round 3, internal cleared-context review

- **Head:** `3f8caae5eca7e681c3452eacdd818d1033a89f8d`, tree `54c36ee7cccf492d1800bca8da915c6e55c2feef`. `665-s5-hooks` -> `dev-soft-core`, source base `5b5f4336`.
- **Delta judged:** `26ba56e1..3f8caae5`, one commit, `hooks_selftest.py` and `README.md` only, against the ruling issuecomment-6692737899.
- **Verdict:** NEGATIVE, on one MINOR finding. **No measurement, figure or verdict in the tree is wrong, and no RTL or firmware moved.**
  - F1 (Tests, Conformance, Docs): the supersede mutant does not hold the rule it names. Deleting the path term from the supersede rule leaves 28 of 28 checks and 94 of 94 mutants green, while the PR says each mutant fails on the rule it names and REVIEW READY says this one "now reaches that rule".
- **Everything else asked of this round holds:** the aging and amended mutants, both deletion probes, all six source mutants, the narrow boundary, the amended-bounds sentence, and the departure from the D2 shape.
- **Also here:** one RESIDUE and four SUGGESTIONs. "Each hook within its bound" stays open as ruled and is not a finding.

## Reconstruction

Read in the assigned order: AGENTS.md; the #665 body; the ruling 6692737899, the takeover 6692914323 and REVIEW READY 6693645158; the PR body; then `git diff 26ba56e1..3f8caae5`, `run.py`, and the self-test's checks. CONTRIBUTING.md and REQUIREMENTS.md were searched by section (`REQUIREMENTS.md:51` for NFR-SCOUT-03), not re-read in full: the delta touches a test and its README, so the prior rounds' reading stands. My own pass and probes came first. R783-2 and R784-2 were read after it, and are resolved below.

## Focus checks

| Check | Result | Evidence |
|---|---|---|
| Aging mutant fails on its rule; deletion makes it escape | **Holds.** It fires `armed < mark` at `hooks_selftest.py:618`. With that assertion deleted, it alone escapes, 93 of 94. | `receipts/deletion_probe.txt`, `receipts/author_audit_rerun.txt` |
| Amended mutants fail on their rule; deletion makes them escape | **Holds.** `the column grades a path` fires `:572`, `a finding reads the column` fires `:575`. With both deleted, both escape, 92 of 94. With `:575` alone deleted the finding mutant escapes. With `:572` alone deleted the verdict mutant is still caught by `:575`, as a finding follows from its verdict, which the PR says. | `receipts/deletion_probe.txt` |
| Supersede mutants fail on the rules they name | **Does not hold for one: F1.** `the table names another group` is sound: it holds `:594`, and it also holds the group term of the rule. `any later group supersedes a refusal` does not hold its rule. | `receipts/source_probe.txt`, `receipts/supersede_demo.txt` |
| All six source mutants killed | **Confirmed in my own spelling, not by rerunning the prior script.** `hp-row-ms-zero`, `hp-ms`, `s-narrow-le`, `hm-cycles`, `hm-wait` and `hm-margin` each fail the named check on the expected assertion. | `receipts/source_probe.txt` |
| Narrow boundary at the swing and one below | **Confirmed.** `check_summary` asserts slacks of exactly 6,490 and 6,489 at `:502`. `<=` gives 2 fits, the swing less 1 gives 0, and the swing plus 2 gives 2. Moving either row one cycle off its boundary, with the slack pin off, lets exactly its own mutant escape, so both rows are live. | `receipts/source_probe.txt`, `receipts/deletion_probe.txt` |
| The held row's fields | **Confirmed.** 33 field edits across both branches of `held_row`: 28 killed. The 5 left are `row` and `ahead` in each branch, which no harness code reads (`run.py:79` only copies `row`, and nothing reads `ahead`), and dropping a rounding that is exact on the check's input. `README.md:206` limits itself to fields a verdict, count or table reads, so it is true. | `receipts/source_probe.txt` |
| Amended-bounds sentence, README and PR body | **Confirmed, word for word.** `README.md:459` and the PR's Grading row carry R783-2's sentence. Read from the four published `table.md`: 756 rows, 4 move (`t5.i1` 21.699, `t5.i2` 33.434, `t5.i3` 44.890, `t5.i4` 57.150), all on the 8x8 answering run; no H-SRP path in the band; H-COUNTERS' 20 misses become 16, and no other hook's count moves. | `receipts/amended_rows.txt` |
| Author's rule table | **93 of 94 accepted, 1 disputed (F1).** The audit reproduces line for line at this head. I read each first-fired assertion against its mutant's name. Eight mutants fire a positive control (`:192`, `:211`, `:236`, `:258`, `:273`, `:318` twice, `:333`). I read each of those implementations: each defect is non-recognition or, for the AAF_CTRL one, over-recognition, which is what `ok.applied == 1` detects. | `receipts/author_audit_rerun.txt` |
| Departure from the D2 shape | **Keeps the property.** The D2 shape added as an extra mutant is caught. With `:572` and `:575` deleted the `NO` pin at `:580` still catches it, and it escapes only with all three gone, so the author's account of probe C is exact. A verdict reading only the 60 ms ceiling is killed by two checks. Loosening the pin would have weakened a test, so keeping it was right. See S1. | `receipts/deletion_probe.txt`, `receipts/source_probe.txt` |

## Findings

### F1: MINOR (Tests, Conformance, Docs). The supersede mutant does not hold the rule it names, and the path term of that rule has no holder

- **Where:** `tb/verilator/ctrl_service_hooks/hooks_selftest.py:597-598` (`check_superseded`), `:741-744` and `:802` (the mutant), `run.py:141` (the rule), `README.md:199,235`; the rule table entry `"supersede: any later group supersedes a refusal": "other interface"`; the PR body's status line ("each failing on the rule it names"), its "A third mutant" paragraph, and REVIEW READY 6693645158 ("It now reaches that rule").
- **Authority:** ruling 6692737899 item 1: "the PR sentence must be true of all of them". AGENTS.md section 6 Tests: each test can fail for the defect it claims to detect. `README.md:199`: a refusal is superseded only where the aging group "measured the same path on the same interface".
- **Evidence:**
  - The rule at `run.py:141` has three terms: group, path and interface. Its guard, `by`, comes first.
  - The `another path` case at `:597` uses `acmp.bind_rx`, which has no entry in `hooks.SUPERSEDED` (`hooks.py:446`). So `by` is `None` and the comparison is never evaluated. That assertion cannot fail for the defect it is labelled with.
  - Deleting the path term from `run.py:141` leaves the whole self-test green: 28 of 28 checks, 94 of 94 mutants (`sup-no-path`, `receipts/source_probe.txt`).
  - The group term is held, but by the sibling: dropping it makes `the table names another group` escape, so the self-test exits 1 (`sup-no-group`). The interface term is held by `:596`.
  - The mutant is a wrapper over `grade_all`'s output (`:741`) that clears every refusal, so it skips the `by` guard. That is the only reason it fires `:596` and then `:598`, and neither firing says anything about the path term. It replaces no rule.
  - Its name says *group*, its first fire is the *interface* assertion, and the check's name says *path*. Deleting `:596` alone lets nothing escape, and deleting `:598` alone lets nothing escape (`receipts/deletion_probe.txt`).
- **Impact:** the term is load-bearing, not equivalent. `hooks-disc-aging` also measures `acmp.entity_available` on the same interface (`hooks.py`, `aging_group`). With the term gone, a run where that group loses TMR_NO_ADP but measures ENTITY_AVAILABLE has its refusal silently superseded (head: 1 refusal, 0 superseded; term dropped: 0 refusals, 1 superseded; `receipts/supersede_demo.txt`). A refusal fails the run, so the gate could lose a fail-closed path while reporting full marks. At this head the code is right, and no run of Results supersedes anything (`README.md:200`). This is the class R784-2 F-1 named, in the mutant the author added to close it, so the audit sentence is not yet true of all 94.
- **Why MINOR and not RESIDUE or SUGGESTION:** the fix changes a test, not only words, and the sentence it falsifies is the one the ruling requires to be true. Neither prior report raises it, and R783-2's 58 source mutants include none on this rule.
- **Required outcome:**
  1. A check fails when the path term is dropped from the rule.
  2. A mutant fails on that assertion and escapes when it is deleted.
  3. The mutant's name, its rule table entry and the PR sentence agree on what it fires.
- **Verification:** `sup-no-path` reports killed. One shape that works, tried in memory: give `:597` the row `dict(again, path=['acmp.entity_available', 1])` beside `lost`. It passes on the head rule and fails on `another path` with the term dropped (`receipts/supersede_fix_check.txt`). Then rerun the audit and the deletion probes.

### R1: RESIDUE (Docs). The Grading row cites a check for more than it holds

- **Where:** the PR body's Round 2 table, row "Grading".
- **Evidence:** "no verdict, finding or count reads it" is true of the code: the readers are `run.py:192,206,215`, and the blob is unchanged since R783-2 and R784-2 confirmed that. But its evidence cell cites `the amended column grades nothing`, which holds verdicts and `LATE` findings only (S2). `README.md:206` already says this correctly.
- **Exact fix:** after "eight mutants", add "which hold verdicts and `LATE` findings; the column's only readers are `table` and `amended_cell`".

### Suggestions (optional, none affects the verdict)

- **S1 (Tests):** `hooks_selftest.py:726`. The listed verdict mutant moves SRP only, so no listed mutant exercises the 60 ms half of the rule, though assertions do. The two-interface shape could stand as a ninth mutant under its own name.
- **S2 (Tests), retained from R783-2 S2 and R784-2 S-1, with a correction:** `am-slack-reads-column`, `am-misses-read-column` and `am-cell-reads-column` survive. R783-2 S2 said `check_amended` covers the misses count. My two-interface shape shows it does not, and `:582-583` pin neither the count nor the cell's `over its bound`. One expect on that line covers two of the three.
- **S3 (Docs):** with F1's fix, a name such as `supersede: any row supersedes a refusal` would say what the wrapper does.
- **S4 (Tests):** `mutant_audit.py`, receipts only. `fires[chain[0][1]] = ...` raises `IndexError` on an escaped mutant instead of printing `ESCAPED`. It fails closed, so nothing is hidden, but the audit could not report the verdict it has a branch for.

## Prior findings at this head

| Finding | Status | Evidence at this head |
|---|---|---|
| R783-2 F1, grading rules unpinned | **RESOLVED** | Six source mutants killed, boundary at 6,490 and 6,489, labels pinned in both branches, `README.md:206` true as narrowed. |
| R783-2 F2 = R784-2 F-2, amended-bounds wording | **RESOLVED** | Sentence verbatim in both places; 4 rows from the published tables; "the whole difference" sentence follows at `README.md:459` and in the PR's Round 3 table. |
| R784-2 F-1, mutants off their rule | **RESOLVED for `aging` and `amended`. Its audit-sentence half is RETAINED as F1**, on the third mutant the author added. | `receipts/deletion_probe.txt` |
| R784-2 RESIDUE-1, "leaves" | **RESOLVED** | `README.md:469`: "is committed". |
| R783-2 S4 | **Taken** | The mutant leaves `bound_ms` as written. |
| R783-2 S5 first half = R784-2 S-3 | **Taken** | `README.md:469` adds the first-notice clause, in the same edit as RESIDUE-1, which the ruling allows. |
| R783-2 S1, S2, S3, S5 second half; R784-2 S-1, S-2, S-4 | **Retained, optional** | Out of the ruling. The 10 survivors of the published `source_mutants.txt` are the ones R783-2 listed. |

## Lens results

```text
[R783] MINOR Conformance - hooks_selftest.py:597-598,802, PR status line, against ruling 6692737899 item 1 - the audit sentence is not true of all 94 (F1). Items 2 and 3 of the ruling are met.
[R783] PASS RTL - git diff --stat 26ba56e1..3f8caae5; receipts/verify_clone.txt - no hdl/, firmware or gateware file in the delta, six gitlinks unchanged, hooks_soc.py and hooks_build.py blobs equal to 26ba56e1, so nothing the prior RTL verdict depends on moved
[R783] PASS Robustness - run.py:87-110,139-144 at this head; receipts/supersede_demo.txt, source_probe.txt - run.py and hooks.py blobs equal to 26ba56e1; a held push never sent stays a never-fitting row and a finding; both unreached supersede cases stay refusals at head, so the code fails closed (the gap is in the gate, F1)
[R783] MINOR Tests - hooks_selftest.py:597-598,741-744,802 - the path term of the supersede rule has no holder (F1)
[R783] MINOR Docs - PR status line and "A third mutant" paragraph; README.md:235 - the claim that the mutant reaches its rule (F1)
```

Otherwise clean in Docs: all 94 mutants are in the README with the right check, eight `amended:` mutants as the PR says, and the delta's 105 added lines carry no lane label, round, reviewer ID, comment ID or em dash, with a positive control (`receipts/doc_parity.txt`). Otherwise clean in Tests: my run of the self-test equals the published receipt line for line.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Ruling 6692737899; PR body; REVIEW READY 6693645158; 756 published rows; `receipts/amended_rows.txt` | R783-3 | `3f8caae5eca7e681c3452eacdd818d1033a89f8d` |
| RTL | CLEAN | Delta file list; blobs of `hooks_soc.py`, `hooks_build.py`; six gitlinks; `receipts/verify_clone.txt` | R783-3 | `3f8caae5eca7e681c3452eacdd818d1033a89f8d` |
| Robustness | CLEAN | `run.py:87-110,139-144`; `hooks.py:92-103,446`; `receipts/supersede_demo.txt`, `source_probe.txt` | R783-3 | `3f8caae5eca7e681c3452eacdd818d1033a89f8d` |
| Tests | UNCLEAN (F1) | `hooks_selftest.py` (28 of 28, 94 of 94 reproduced); 51 source mutants; 20 deletion probes; audit rerun; 94-row rule table | R783-3 | `3f8caae5eca7e681c3452eacdd818d1033a89f8d` |
| Docs | UNCLEAN (F1) | `README.md` delta, 94-row table against `MUTANTS`; PR body; `receipts/doc_parity.txt`; published docs gate summary | R783-3 | `3f8caae5eca7e681c3452eacdd818d1033a89f8d` |

## Real limits

- **Signature:** the brief says a signed packet. Evidence commit `700a07e6` reads `unsigned` on the hosting service and I found no signature file, so no signature was verified. Integrity here rests on `MANIFEST.json` (26 fetched `author-r3` files, 0 differ) and `INDEX.md` (23 digests, 0 differ) (`receipts/evidence_integrity.txt`).
- **Not rerun:** the four runs, the plants, the builder, any simulation. `run.py` and `hooks.py` are unchanged, so the figures rest on the published tables and the prior rounds' reproduction.
- **Prior scripts:** I did not rerun `rule_probes.py` or `source_mutants.py`. I wrote my own equivalents, and read the published receipts for those two.
- **Docs gates:** not rerun. The published summary lists 98 gates, each rc 0 with a clean tree, at this head.
- **Scope:** code outside the delta keeps its prior lens verdict, except where this report says it was read again.
- **Hosted evidence:** when last read, 12 check runs at this head were queued and 2 in progress, none concluded. Nothing is claimed from them.
- **Physical calibration** NOT RUN, and field skips are not hardware proof. No manager source bank is claimed or inferred at this head.

## Pending manager duties

- Carry F1 to the author, and R1 to the residue checklist.
- Hosted and act acceptance at the final head; the current-dev merge candidate (source base `5b5f4336`, live dev `87e9d03aa2a4797957ac0124d0c7851a2eec234c`), builder and native banks, with receipts linked on the PR.
- The maintainer's open questions stay open: the column's scope, and the one-path or per-descriptor decision.
- "Each hook within its bound" stays open on #665, as ruled.

The clone was left at exact head: 1,502 tracked entries rehashed, 0 differ, index and six gitlinks equal, status clean (`receipts/verify_clone.txt`).

R783-3 FINISHED
