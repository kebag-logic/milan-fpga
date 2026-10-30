[R739] NEGATIVE - exact head db9ab2215ba18aec4c1828090b3611b001dbf2b8

# Independent delta review R739-4: Mister-M-alt/FPGA-gPTP PR #97 (issue #96)

- Head `db9ab2215ba18aec4c1828090b3611b001dbf2b8`, tree `df0a399476813ccfda8d3bb03fa9d7a272b5fd0c`. Base main `135afd04`. Previously reviewed head `411b35fc`.
- Delta `411b35fc..db9ab22` has two commits and four files: `docs/INTEGRATION.md`, `docs/MANAGER.md`, `docs/README.md` and `scripts/check_docs.py`. It has no mode change, no gitlink, and no RTL, generator, generated, test-bench or Makefile path.
- Scope: the delta, the manager's round-4 ruling (issue comment linked in the brief; copy in `receipts/manager_ruling_6521925963.txt`), and every named prior finding at its cause. Code the delta does not touch keeps its round-3 lens verdict.

## Order of work and isolation

- PR data came only from `gh pr view` with the permitted fields (`receipts/pr_view.json`). Source came from git. I read the manager's ruling comment and my own round-3 report.
- I wrote my verdict and ledger to disk (`receipts/verdict_before_prior_findings.txt`, 12:33 UTC) before reading the other reviewer's round-3 report. I read that report afterwards, only to resolve its findings. I did not read the PR comment thread, the author handoff file, or any other reviewer's round-4 material.
- Every probe, mutant and gate ran in an archive copy under the packet's `scratch/`. The clone was never modified.

## Verdict basis

The ruling is carried out on the pages and in the PR body. No prose statement of the gate's accepted or rejected forms remains. Each round-3 case is now a self-test arm and passes, and all gates pass at the head.

The manager's check (3) is not met. Real constant copies, planted on a Current page, pass the gate in two ways:
- **F1** is a regression in this delta. Commit `c6bca77` added tilde-fence handling. Text after a long tilde fence, or after a tilde line with text after its marker, is now treated as fenced. A copy there escapes. The round-3 head caught both plants. The backtick versions of the same constructs escape at both heads.
- **F2** is a pre-existing escape inside this PR's copy rule. A copy wrapped in underscore emphasis passes: `_375 ms_`, `_5 minutes_` and `_five minutes_` all give rc 0, at both heads.

Under the ruling, a finding in this class is RESIDUE unless it shows the gate passing a real stale copy. Both findings show that, so both are MINOR, and the verdict is NEGATIVE. Each has a small fix, tested in scratch, that keeps the head gate and the 53-arm self-test passing. The other option the ruling allows is to record the cases as expected-failure self-test arms.

## The manager's four checks

| Check | Result | Evidence |
|---|---|---|
| (1) No prose statement of the gate's accepted or rejected forms on any page or in the PR body | **Met.** The only gate sentences left are the ruled pointer, at `docs/INTEGRATION.md:856`, `docs/MANAGER.md:59` and `docs/README.md:48`. The pages and the PR body name no matched, rejected, passing or exempt form. Two other edits are not matching rules: the deleted sentence "`make docs` does not check them" (cadence table), and the rewording at `MANAGER.md:57`, "The seeded row counts the `--seq-seed 0x200000` image". That second sentence is correct: the checker runs that seed (`check_docs.py:129`). See RES-1 for a scope wording point in the pointer sentence. | `receipts/prose_gate_statements.txt`, PR body in `receipts/pr_view.json` |
| (2) Each round-3 case is a self-test case that passes or is an expected failure | **Met.**<br>- Decimal minutes: "A 2.5 min hold." and "Wait 0.5 minutes." are pass arms (`check_docs.py:760-761`).<br>- Unit inference without a comma: "syncReceiptTimeout ms", "in ms" and "(ms)" are must-fail arms (`:780-786`).<br>- The rejected-set examples: "A 5min countdown." and "A five min countdown." are must-fail arms (`:771-772`).<br>- Fences: a tilde-fence pass arm (`:764`) and a copy-after-tilde-fence arm (`:773`).<br>- The round-3 suggestion examples "twenty-five minutes" and "5 minimum" are pass arms (`:762-763`).<br><br>The self-test passes with 53 arms. Each of 10 single reversions of the round-4 checker changes fails at its own arm. | `receipts/head_docs.log`, `receipts/checker_mutants_r4.txt` |
| (3) The c6bca77 checker changes let no real stale copy through | **Not met: F1.** Of 43 real copies and drifted rows planted at the head, 35 fail as they must and 8 pass:<br>- 2 are new in this delta and form F1: `c_after_long_tilde_fence` and `c_after_tilde_info_close`. Both gave rc 1 at `411b35fc` and give rc 0 at the head.<br>- 4 were already passing at `411b35fc`: `c_after_long_backtick_fence` (part of F1) and the three underscore copies (F2).<br>- 2 are the decimal and unit-word forms that round 3 accepted as passes (S-1).<br><br>The delta also fixes 6 escapes and 6 false failures that the round-3 head had. | `receipts/copy_probes_head.txt`, `receipts/copy_probes_r3head.txt`, `receipts/fence_cases.txt` |
| (4) All docs and CI-hygiene gates pass at the head | **Met.** All rc 0:<br>- `make -j16 docs`: 14 Current and 18 historical pages; docs self-test 53 arms; diagram self-test 10 arms; source evidence 20 exact, self-test 7 arms.<br>- `make diagrams-check` and `make contract`.<br>- `make lint`, with the pinned Verilator 5.050 first on `PATH`.<br>- `git diff --check` from `135afd04` and from `411b35fc`.<br><br>The repository has no workflow directory, so these targets are its gates. | `receipts/head_gates.txt`, `receipts/head_*.log`, `receipts/verilator_identity.txt` |

## Resolution of named prior findings

| Prior finding | Resolution at this head | Evidence |
|---|---|---|
| R739-3 F1: unit source stated wider than the checker; "5min" and "five min" escape | **Resolved at its cause.** The checker now matches the wider rule:<br>- `UNIT_CELL_RE` accepts a comma, whitespace or a parenthesis before the unit (`check_docs.py:123`).<br>- The digit minute pattern makes the separator optional, and the word pattern accepts "min" (`:456-457`).<br><br>All of these are self-test arms, and the prose is gone. The widening gives the 17 current rows the same unit set as before, so no row gains or loses copy checking. | `receipts/row_units.txt`; probes `c_meaning_*`, `c_cease_5min`, `c_cease_five_min` |
| R739-3 F2: "2.5 min" falsely failed; `~~~` fences not exempt | **Resolved as stated.** The digit minute pattern has the `(?<![\d.,])` lookbehind. `~~~` is a fence marker, and a fence closes only on its own marker. Both are self-test arms. The tilde support brings the new escape F1. | probes `n_decimal_*`, `n_fenced_tilde*` |
| R739-3 S-1: minute patterns matched inside "twenty-five minutes" and "5 minimum" | **Resolved.** Both are pass arms. | `check_docs.py:762-763` |
| R740-3 F1: decimal minutes ("Wait 0.5 minutes.", "1.5 min") falsely failed, against the stated rule | **Resolved.** Both pass at the head (my `n_decimal_minutes`; author probe `decimal_min_1_5`). "Wait 0.5 minutes." is a self-test arm. The universal "decimals pass" prose is removed. `5 min`, `five minutes` and `five-minute` still fail. | `receipts/copy_probes_head.txt` |
| R740-3 F2: unit inference needed a comma the PR body omitted | **Resolved by extension.** The comma-less cell now gives the unit, with self-test arms. The comma control still fails. The claim is removed. | `receipts/checker_mutants_r4.txt` (`unit_comma_only`, `unit_no_space`, `unit_no_paren`) |
| R740-3 S1 to S5 (= R739-2 S-1 to S-5) | S2, a unit label that silently disables the check, is resolved: the label forms are now arms. S1 (coincident values), S3 (unitless rows) and S5 (lint `PATH`) are unchanged and carried below. S4 (one seeded image) is unchanged. It is disclosed at `MANAGER.md:57` and needs nothing more. | — |
| Rounds 1 and 2, both reviewers | Resolved at round 3 by both reviewers. The delta does not touch their causes, so they stay resolved. | round-3 reports |

## Findings

### F1 - MINOR - Robustness, Tests

- **Where:** `scripts/check_docs.py:124` (`FENCE_MARKERS`) and `:479-481`:
  ```
  marker = line.lstrip()[:3]
  if marker in FENCE_MARKERS and fence in ("", marker):
      fence = "" if fence else marker
  ```
- **Authority:**
  - The manager's check (3) and the round-4 ruling. A gate-class finding is not RESIDUE when it shows the gate passing a real stale copy.
  - The fence rule comes from the CommonMark spec §4.5 (fenced code blocks), which GFM follows: "The closing code fence must be at least as long as the opening fence", and "Closing fences cannot have info strings". Under that rule, a `~~~` line inside a `~~~~` fence is code content, and so is a "``` x" line inside a backtick fence.
- **Cause:** the checker toggles on any line whose first three characters after indentation are a marker of the open kind. It ignores run length and trailing text. So a fence can close early, and the real closing line then reopens it. Everything after that is treated as fenced, up to the next marker or the end of the file. A copy in that rendered prose is skipped.
- **Evidence:** each plant below is followed by "The Sync watch is 375 ms." as prose on `docs/HDL_DEVELOPER.md` (Current). Results are rc from the full checker at both heads, with the same probe list (`receipts/copy_probes_head.txt`, `receipts/copy_probes_r3head.txt`):

  | Plant | `411b35fc` | `db9ab22` |
  |---|---|---|
  | `c_after_long_tilde_fence`: a `~~~~` line, a `~~~` line, a `~~~~` line, then the copy | rc 1, caught | **rc 0, escapes** |
  | `c_after_tilde_info_close`: lines `~~~text`, `literal`, `~~~ not a close`, `more`, `~~~`, then the copy | rc 1, caught | **rc 0, escapes** |
  | `c_after_long_backtick_fence`: a four-backtick line, a three-backtick line, a four-backtick line, then the copy | rc 0, escapes | rc 0, escapes |

  `receipts/fence_cases.txt` runs eight cases through the head's `copy_findings` and compares each with the spec rule. There are five disagreements:
  - four real copies escape: the two tilde cases and their two backtick versions;
  - one copy inside a long tilde fence is falsely reported (loud, not a pass).
- **Impact:** a stale copy of a unit-bearing constant can sit on a Current page and pass `make docs`. This needs a long fence, or a fence line with text after its marker. The tilde versions are new in this delta; the backtick versions predate it. No tracked Markdown file has a `~~~` or four-backtick fence today (`receipts/markup_usage.txt`), so no present page is affected.
- **Required outcome:** do one of the following.
  - (a) Track the fence as CommonMark does:
    - The opening run is three or more of one character, indented at most three spaces. A backtick info string has no backtick.
    - The closing run uses the same character, is at least as long, and has only spaces after it.

    Add must-fail self-test arms for a copy after the `~~~~`/`~~~`/`~~~~` lines, a copy after a `~~~ x` inner line, and their backtick versions. Add a pass arm for a copy inside a long fence. `receipts/fence_fix_candidate.diff` is one illustrative form. In a scratch tree it clears all five disagreements, and the docs check and the 53-arm self-test still pass.
  - (b) Record those cases as expected-failure self-test arms, as the ruling allows, with no prose.
- **Verification:**
  - Under (a), `python3 -I scripts/fence_cases.py <check_docs.py> <repo-root>` reports 0 disagreements.
  - Rerun `scripts/copy_probes_r4.sh`. Under (a), `c_after_long_tilde_fence`, `c_after_tilde_info_close` and `c_after_long_backtick_fence` give rc 1.
  - The self-test and `make docs` pass.

### F2 - MINOR - Robustness, Tests

- **Where:** `scripts/check_docs.py:448` (`...{suffix}\b`), `:456` (`(?<![\d.,])\b{minutes}...s?\b`), `:457` (`(?<![\w-]){word}...s?\b`).
- **Authority:** as for F1. The copy rule already catches the same value in inline code, in `**bold**` and in `*italic*` markup (probes `c_sync_inline_code`, `c_cease_bold_word`). Underscore emphasis is the same markup in GFM, and the checker does not catch it.
- **Cause:** `\b` treats `_` as a word character. So there is no boundary between `ms` and a closing `_`, or between an opening `_` and `5` or `five`. The lookbehind `(?<![\w-])` also rejects `_`.
- **Evidence:**
  - Three plants give rc 0 at both heads: `c_sync_underscore` ("The Sync watch is _375 ms_."), `c_cease_underscore_digit` ("After _5 minutes_ it ceases.") and `c_cease_underscore_word` ("After _five minutes_ it ceases."). Each renders as emphasised "375 ms" or "5 minutes" on a Current page.
  - `receipts/underscore_boundary.txt` tries a boundary that excludes `_` but keeps letters and digits. It catches all three copies. It still passes all six non-copies: "2.5 min", "twenty-five minutes", "5 minimum", "375 msec", "1375 ms" and "snake_5_min".
- **Impact:** a real copy passes in a common Markdown form. No Current page uses underscore emphasis today (`receipts/markup_usage.txt`), so no present page is affected. This predates the delta: the copy rule was added in this PR, and earlier rounds, mine included, did not plant this form. It is raised now because the ruling makes a real-copy pass the one gate defect that is not RESIDUE.
- **Required outcome:** do one of the following.
  - Use letter-and-digit boundaries in place of `\b` and `\w` around the value and unit in the three patterns. Add must-fail arms for `_375 ms_` and `_five minutes_`.
  - Record them as expected-failure arms.
- **Verification:** rerun `scripts/copy_probes_r4.sh`. The three `c_*underscore*` probes give rc 1, and every `n_*` probe still gives rc 0.

### RESIDUE (wording only; does not change the verdict)

- **RES-1:** the pointer sentence reads "`make docs` rules are `scripts/check_docs.py`".
  - **Where:** `docs/INTEGRATION.md:856`, `docs/MANAGER.md:59`, `docs/README.md:48`, and once in the PR body.
  - **Why:** `make docs` also runs `scripts/check_source_evidence.py` and `scripts/generate_diagrams.py --check` (`Makefile:28-36`). Beside each table the sentence means the rules for that table, so this is only a scope wording point.
  - **Exact fix (pages):** "The `make docs` rules for this table are `scripts/check_docs.py`; its [`selftest()`](../scripts/check_docs.py) cases are the specification."
  - **Exact fix (PR body):** "The `make docs` rules for these tables are ...".

### SUGGESTION (non-blocking)

- **S-1:** "0.375 s" and "375 milliseconds" still pass as copies (`c_decimal_s`, `c_word_ms`).
  - They were named in round 2 and accepted as passes in round 3. Their only disclosure was the prose "Decimals and other unit words ... pass. Review keeps those forms out.", which the ruling removed.
  - The self-test, which is now the specification, has no arm for them, nor for unitless rows (`248`, `1,024 words`).
  - Suggest pass arms labelled as known escapes, so the specification keeps the limit the prose recorded.
- **S-2:** `check_docs.py:787` reads `usage ={"Shipping": ...`. Commit `c6bca77` dropped a space from `usage = {` on a line the ruling did not ask to change. Restore the space.
- **S-3:** `without_fences` (`check_docs.py:164-174`) is used by the other page rules. It still recognises only backtick fences, with the same toggle logic as F1. One shared fence helper for the copy rule and `without_fences` would keep the rules consistent.
- **S-4 (carried from round 3 S-2):** a coincident unrelated figure is reported as a copy. For example, a "125 ms" cadence would be reported as `FU_RTO_MS_C`; the cadence table is safe only because it sits inside the home section. Consider naming the possible coincidence in the finding text.
- **S-5 (carried from round 3 S-3):** `make lint` uses the `verilator` on `PATH`. A `VERILATOR ?=` variable would make the pinned identity explicit.
- **S-6 (carried from round 3 S-4):** `docs/history/v1/RESOURCE_DELTAS_2026_10.md:30` says WNS "moves from +2.249 ns" but does not give the value it moves to. The linked candidate report gives +1.773 ns.

## Other statements checked

- **PR body, "53 arms, up from 10 at the base" and "This revision adds 11 arms": confirmed.** That is 42 + 5 pass + 3 copy + 3 unit-cell arms (`receipts/head_docs.log`).
- **PR body, "Nine changes to the checker were each reverted on their own ... Each reversion makes the self-test fail at the arm for its case": confirmed.**
  - My 10 reversions split the unit regex change three ways and add the digit trailing boundary (`receipts/checker_mutants_r4.txt`).
  - Each reversion gives rc 1 at its own arm, and the control gives rc 0.
  - The author's `checker_mutants.log` shows 9 planted, 0 unexpected.
- **PR body, "At the previous head 13 of the 25 probes differ ...; at this head none does": consistent.** The author's `tree_probes_db9ab22.log` shows 25 probes, 0 differing. My own wider set agrees on every overlapping probe. The author's set does not include the F1 or F2 constructs.
- **PR body, "This revision changes only three Markdown pages and the docs checker": confirmed** (`git diff --raw 411b35fc..HEAD`).
- **PR body, "The eleventh checks that a fence closes only on its own marker": confirmed.** The arm is `check_docs.py:773`, and the `any_marker_close` mutant fails it. F1 concerns run length and trailing text, which that arm does not cover.
- **Source comment `check_docs.py:121-122`, "A Meaning cell ending in ms, ns or ppm gives the row's unit": consistent** with the widened `UNIT_CELL_RE`.

## Published author evidence (milan-fpga `b71327c6`, `review-evidence/gptp96-r1/author-r4`)

- The evidence commit reports `unsigned` (`receipts/evidence_commit_verification.txt`). Its integrity rests on `MANIFEST.json`, not a signature.
- All 62 `author-r4/` files match their `published_sha256`. No manifest entry is missing from the tree, and no file is unlisted (`receipts/evidence_manifest_check.txt`).
- Spot checks:
  - `gates-head-db9ab22/rc.txt`: docs, diagrams-check, contract, lint, both diff checks and status are all rc 0.
  - `identity.txt` names head `db9ab22` and Verilator 5.050.
  - The mutant and tree-probe logs agree with my receipts.
- The parent-consumer gate logs for `411b35fc`, `db9ab221` and `f97c1803` are present and hash-verified. I did not re-execute them; that is outside this brief.

## Comments and privacy

- The delta's added lines have no lane, round, reviewer or comment-ID label, no host name and no private path (`receipts/delta_added_lines.txt`).
- The one edited source comment states behaviour and ends "(#96)".

## Clone integrity (`receipts/clone_integrity.txt`)

- HEAD, the index tree and the worktree match `db9ab22` / `df0a3994`.
- `git status --ignored` is empty, and there is no `__pycache__`.
- `ls-files -s` equals `ls-tree -r HEAD` in modes, blobs and paths.
- The tree has no gitlinks and no `.gitmodules`, and none are required.

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | The delta has no clause, Milan or 802.1AS citation change. The round-3 clause verdicts are unaffected. | R739-4 delta; earlier rounds for unchanged citations | db9ab2215ba18aec4c1828090b3611b001dbf2b8 |
| RTL | CLEAN | No RTL, generator or generated path in the delta (`git diff --raw`). The round-3 publication-timing verdicts (`KL_gptp_engine.sv`, `KL_gptp_ucpu.sv`) stand. `make lint` passes with the pinned 5.050. | R739-3, re-confirmed by R739-4 lint | db9ab2215ba18aec4c1828090b3611b001dbf2b8 |
| Robustness | UNCLEAN (F1, F2) | `check_docs.py:121-124,441-500`: unit cell, minute patterns, fence logic. 55 planted probes at both heads; 8 CommonMark fence cases; underscore boundary variant; row-unit comparison. | R739-4 | db9ab2215ba18aec4c1828090b3611b001dbf2b8 |
| Tests | UNCLEAN (F1, F2) | Self-test arms `check_docs.py:756-786` (53 arms); 10 single-change reversions; author mutant and tree-probe receipts (hash-verified); head gates. The F1 and F2 constructs have no arm. | R739-4 | db9ab2215ba18aec4c1828090b3611b001dbf2b8 |
| Docs | CLEAN (RES-1 recorded) | `docs/INTEGRATION.md:848-890`, `docs/MANAGER.md:52-66`, `docs/README.md:42-50`, the PR body. No gate-rule prose remains. The new and remaining sentences are correct, apart from the wording point RES-1. | R739-4 delta; R739-3 for unchanged pages | db9ab2215ba18aec4c1828090b3611b001dbf2b8 |

## Real limits

- This was a delta review. Pages, code and suites the delta does not touch keep their round-3 verdicts. I re-ran no engine, microCPU, parser, gasket or decode suites, because the delta changes none of their inputs.
- The rendering behaviour behind F1 and F2 rests on the CommonMark §4.5 rule and GFM emphasis. I ran no local renderer, and I sent nothing to a rendering service.
- The fence and boundary fixes are illustrative scratch patches. They are not a required form.
- The author's parent-consumer gate results are hash-verified receipts only. The author evidence commit is unsigned.
- Physical calibration was NOT RUN. No hardware or field result is claimed, and field skips are not hardware proof.
- No manager source bank ran at this exact head, and none is claimed or inferred.

## Pending manager duties

- Rule on F1 and F2. Both are real-copy passes, so the RESIDUE carve-out does not cover them. Choose the fix or expected-failure arms.
- Build and validate the current-dev merge candidate (source base `135afd04`, live dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`) with the builder and native banks at the merge turn, and link the receipts on the PR.
- Hosted and act acceptance at the exact head.
- Carry RES-1 to the residue checklist.
- The parent gitlink bump and the parent page pins, which the PR body says any bump needs.

R739-4 FINISHED
