[R763] POSITIVE - exact head 5843d1af1d3a892fdc0fbb766ba2058ec44c26ea

# R763-11: internal cleared-context review of PR #834 (issue #833)

- **Head:** `5843d1af1d3a892fdc0fbb766ba2058ec44c26ea`, tree `bfbcbc98c2d0cd6944e7f7948f4d5f60621db52c`, isolated detached clone. The PR's `headRefOid` is the same and the PR is not a draft.
- **Scope:** delta only, per the round 11 ruling (issue #833, issuecomment-6595078798). The delta is `fce77f0e..5843d1af`: two commits, three files (`docs/testing/TESTING.md` +4/-3, `scripts/process_test_support.py` +4, `scripts/test_suite_cancellation.py` +10/-9).
- **Unchanged:** `scripts/owned_process.py` is byte-identical to round 10 (`git diff --quiet fce77f0e..5843d1af -- scripts/owned_process.py`). The delta touches no HDL, no `tb/` and no workflow.
- **Order of work:** I applied all five lenses to the diff before reading any prior review's findings. I read the round 10 reports (R763-10, R764-10) only afterwards, to settle item 2 and the prior findings.
- **Result:** no BLOCKER, MAJOR or MINOR. There is one RESIDUE and one SUGGESTION.

## Item 1: R763-10-F1 pinned

| Check | Result | Evidence |
|---|---|---|
| Listing "a stubborn parent beside a stopped shell": shell `(owner_pid,"2")`, parent `(owner_pid,"5")`, child `(parent,"4")` with the child a real live process, cancelled shell `shell` | present | `scripts/test_suite_cancellation.py:827-829` |
| Listing "a stubborn parent under a stopped shell": the same, with the parent `(shell,"5")` | present | same loop, `entry=(shell,"5")` |
| Stated events match the ruling: `SIGTERM` to parent and child at 0; `SIGKILL` to the child at 2 and to the parent at 4; at 14 `SIGKILL` to shell, parent and child; verdict | match | `[*stubborn[:4], (14,"SIGKILL","shell"), *stubborn[4:]]`, with `stubborn` at `:791-792` |
| The shell is never resumed in either listing | holds | The child is live in every census, so `live - {root_pid}` is never empty (`owned_process.py:302`) |
| `first-census-parent-unspared-beside-shell` is in `MUTANTS` with R763-10's edit, byte for byte | match | `scripts/process_test_support.py:913-916`, compared against R763-10-F1's published code line |
| That mutant is red on a named control with its words | red | `owner_stated_seconds`, words "a stubborn parent beside a stopped shell's". The parent gets `SIGKILL` at 3.0 s. See `receipts/head-mutants.log` |
| The mutant is named in row 3 | yes | `TESTING.md:316`, data row 3 of the stated-behaviour table, and no other row (`receipts/table-vs-mutants.txt`) |
| The guide lists both listings with their words | yes | `TESTING.md:283` |
| Re-layout changes no behaviour | AST-equal | See the AST check below |

**AST check** (`scripts/ast_relayout.py`, `receipts/ast_relayout.log`, rc 0):
- I took `test_suite_cancellation.py` at head, inlined `stubborn` at its one use, removed the added beside/under loop, and restored `kept`'s round 10 docstring.
- The module AST then equals `fce77f0e`'s.
- In `process_test_support.py`, the only AST difference is the added `MUTANTS` key. No entry changed value or order (`receipts/ast_support.log`).
- The shared `stubborn` list is only read (sliced and compared), never mutated, so sharing it changes nothing.

## Item 2: RESIDUE exact fixes

| Prior item | Status at this head | Evidence |
|---|---|---|
| R764-10-R1 ("The last cell" → "The next-to-last in-grace cell is listed with a command that is not live as well:") | applied verbatim | `TESTING.md:296` |
| R763-10-R1 (guide: "Each listing whose census has grown by the second pass is kept again, early: ..."; docstring: "one whose census has grown by the second pass does so again early, with a census stated a tick after the first pass.") | applied verbatim in both places | `TESTING.md:298`, `scripts/test_suite_cancellation.py:778-779` |
| R764-10-R2 (the same two lines, different text) | taken through R763-10-R1, as the ruling allows | The author's reason, published in the REVIEW READY comment, is that R764-10-R2's docstring text needs a third line and the module is at its 1000-line limit. The limit holds: `check_py_idiom.py` rc 0. One residual imprecision remains; see R763-11-R1 |
| R764-10-S1 (assert or split on `words[2:]`) | not taken, reason given | The reason given is that neither fits on the line under the limit, and every growing listing's words start with "a ". Checked: all eight early names in `TESTING.md:303-310` come from words beginning "a " |

## Own sweep over row 3's cells

Row 3's domain is a parent whose live child, from the first census or new since it, outlives its own `SIGKILL`:
- with no cancelled shell;
- under or beside a cancelled shell that is never resumed.

In every case the parent is killed at 4 s and not a tick before.

At this head the four child-origin × shell-condition cells are each listed:
- first census, no shell: "a stubborn parent";
- new, no shell: "a live new descendant";
- new, beside or under a shell: the round 10 liveness listings;
- first census, beside or under a shell: the two new listings.

I wrote seven disposable probe mutants of `owned_process.py` aimed at the cells this round added. Each was run with `owner_stated_seconds` in a copy under scratch (`scripts/probe_row3.py`, `receipts/probe_row3.log`, rc 0). All seven are red and none survives:

| Probe | Red on | Parent's `SIGKILL` |
|---|---|---|
| under-only-first-census-unspared | "a stubborn parent under a stopped shell" | 3.0 s |
| beside-only-first-census-unspared | "a stubborn parent beside a stopped shell" | 3.0 s |
| shell-first-census-parent-a-tick-early | beside | 4 − tick |
| under-first-census-parent-a-tick-early | under | 4 − tick |
| shell-first-census-parent-a-pass-late | beside | 4.5 s |
| shell-first-census-parent-never-killed | beside | 14 s only |
| under-first-census-parent-killed-at-grace | under | 2.0 s |

Notes on the probes:
- The under-only probe shows that the "under" listing discriminates on its own. It does not rely on the "beside" listing failing first.
- My first draft of "never-killed" put its edit inside the `clock < kill_all` branch. That made it equivalent to the head code, and it stayed green. The published probe puts the edit on the branch condition, and it is red. I record the draft here as a probe error, not as a survivor.

Full `--mutants` at head (`receipts/head-mutants.log`, rc 0): `owned-process mutants: PASS (150 mutants, 147 with a control that must fail)`. All 147 controlled mutants are red with their words, and `none` is green on all ten owner controls.

**Result: no survivor inside a stated domain.** I did not re-open the out-of-domain survivor classes from round 10 (R763-10-R2, R764-10-R3). They stay residue for #495.

## Findings

### R763-11-R1 - RESIDUE - Docs, Tests (docstring)

**Location:** `docs/testing/TESTING.md:298`, `scripts/test_suite_cancellation.py:779`. **Issue:** "has grown" does not describe one early listing.

- **Evidence:**
  - The rule is `set(listing(TICK)) - set(listing(0))` (`:786`). It keeps a listing early when its census at a tick lists a descendant its first census did not.
  - Take "a live new descendant beside a stopped shell" (`:852-854`). Its census is {shell, child} at 0 and {shell, live} at a tick: one entry is swapped for another, and the count does not grow. It is still kept early, and the early table names it (`:308`).
  - Read as a count, "has grown" leaves this listing out. The clause after it in the guide ("the first to list what is new since it") states the rule correctly.
- **Impact:** wording only. No listing, mutant, row domain or claim changes.
- **Exact fix:**
  - `TESTING.md:298`: replace "Each listing whose census has grown by the second pass is kept again, early:" with "Each listing whose census by the second pass lists a descendant its first census did not is kept again, early:".
  - Docstring `:779`: replace "census has grown by the second pass" with "census gains a pid by the second pass". The line becomes 119 columns, within the 120 limit, with no new line.
- **Verification:** read both lines; `python3 -I scripts/check_py_idiom.py` rc 0.

### R763-11-S1 - SUGGESTION - Tests

**Location:** `scripts/test_suite_cancellation.py:830-834`. **Issue:** the stated-seconds summary does not show the new axis.

- The `owner-stated-seconds:` summary line shows the matrix, the lone resumes and the liveness axis. It does not show the first-census stubborn parent beside or under a shell.
- A key such as `stubborn_parent_beside_under_shell=True` would make the round's addition visible in the log.
- This is optional. The module is at its line limit, and this round's ruling did not ask for it.

### Comment rule

- The added source lines carry no lane label, round, reviewer ID or comment ID. I scanned the `+` lines of the delta and found none.
- The new `MUTANTS` entry has no comment.

## Prior findings at this head

- **R763-10-F1 (MINOR):** resolved at its cause. The cell is now listed, the mutant is in `MUTANTS`, and it is red with its words. Both sub-cells (beside and under) discriminate independently, by the probes above.
- **R763-10-R1:** applied. One residual imprecision is recorded as R763-11-R1.
- **R763-10-R2:** retained as residue for #495. No action is needed in this PR.
- **R764-10-R1:** applied.
- **R764-10-R2:** taken through R763-10-R1.
- **R764-10-R3:** retained as residue.
- **R764-10-S1:** not taken, with the reason above.

## Evidence

**Executed by this round at the exact head.** Each has a log and an rc file under `receipts/`:

| Command | rc | Result |
|---|---|---|
| `python3 -B scripts/test_suite_cancellation.py --control owner_stated_seconds` | 0 | PASS |
| `python3 -B scripts/test_suite_cancellation.py --mutants --jobs 16` | 0 | PASS, 150 mutants, 147 with a control that must fail; 157 runs |
| `python3 -B scripts/test_suite_cancellation.py` | 0 | `suite cancellation: PASS`, 59.4 s |
| `python3 -I scripts/check_py_idiom.py` | 0 | Both changed modules are at 1000 lines, within `LONG_MODULE_LINES = 1000`. No line is over 120 columns |
| `scripts/probe_row3.py` | 0 | 7 probes, 0 survivors |
| `scripts/ast_relayout.py` | 0 | Module AST equal after the stated edits |

**Spot-checks of published evidence** (`receipts/evidence-spotcheck.txt`):
- I fetched `review-evidence/833-r1` at `a0ae7348`.
- The `published_sha256` values in `MANIFEST.json` match my fetched copies of `author-r11/HANDOFF.md` and `author-r11/receipts/gates/lane/{mutants.log,mutants.rc,test_suite_cancellation.rc}`.
- The author's lane `--mutants` log ends with the same PASS line, and its rc files are 0.
- I examined no detached signature artifact; the hash match is the check made.

**Hosted contexts** (`receipts/hosted-check-runs.tsv`, a snapshot taken during this round): 5 completed with success, 1 skipped (Physical gPTP, nightly or manual), 10 in progress and 28 queued. Hosted and act acceptance belong to the manager.

**State after probes:**
- All probe and mutant trees were under scratch or a temporary directory, and the clone was never edited.
- `git status --porcelain` is empty, and the HEAD and tree are unchanged.
- The gitlinks are recorded in `receipts/gitlinks.txt`: external efeb541a, gptp-processor 135afd04, protocol-processor a9e84b66, lwSRP 08ee86e8, tsn-c-stack 70936b77, verilog-axis 48ff7a7e.

## Lens results

| Lens | Result | Artifact and what was checked |
|---|---|---|
| Conformance | PASS | `scripts/test_suite_cancellation.py:791-792,827-829`, `TESTING.md:283,316`. Ruling items 1 and 2 met. Row 3's claimed domain now has a listing in each cell, with the stated events |
| RTL | PASS | `git diff --stat fce77f0e..5843d1af` touches no `hdl/`, no `tb/` and no workflow. `scripts/owned_process.py` is byte-identical. The prior RTL verdict stands, because the delta changes nothing it depends on |
| Robustness | PASS | `receipts/probe_row3.log`. Kills too early (3.0 s, 2.0 s, a tick before 4 s), too late (4.5 s), never, and beside-only or under-only are each red |
| Tests | PASS | `receipts/head-mutants.log` (150/147 red, `none` green 10/10), `receipts/ast_relayout.log`, `receipts/head-whole.log`, `receipts/check_py_idiom.log` |
| Docs | PASS (RESIDUE R763-11-R1 carried) | `TESTING.md:283,296,298,316`. Item 2 wording applied verbatim. R763-11-R1 is wording only |

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | round 11 ruling; `TESTING.md:283,316`; `test_suite_cancellation.py:788-834`; `process_test_support.py:913-916` | R763-11 | 5843d1af1d3a892fdc0fbb766ba2058ec44c26ea |
| RTL | CLEAN | delta stat (no HDL, `tb/` or workflow); `owned_process.py` byte-identical to fce77f0e; prior verdict carried | R763-11 | 5843d1af1d3a892fdc0fbb766ba2058ec44c26ea |
| Robustness | CLEAN | 7 probe mutants over the beside and under cells, all red | R763-11 | 5843d1af1d3a892fdc0fbb766ba2058ec44c26ea |
| Tests | CLEAN | full `--mutants`; named mutant red with its words; AST re-layout check; whole test; idiom gate | R763-11 | 5843d1af1d3a892fdc0fbb766ba2058ec44c26ea |
| Docs | CLEAN | `TESTING.md:283,296,298,316`; docstring `:778-779`; R763-11-R1 is RESIDUE | R763-11 | 5843d1af1d3a892fdc0fbb766ba2058ec44c26ea |

## Limits of this round

- **Delta only.** Code the delta does not touch keeps its prior lens verdicts.
- **Not re-run by me:**
  - the `docs.yml` steps;
  - `behave`;
  - the gptp_shadow lifecycle test;
  - `--matrix`;
  - the round 10 reviewers' full sweeps.
  
  For these I rely on the author's published receipts, which I spot-checked by hash.
- **No full banks.** I ran no parent, PP, gPTP, Yosys or builder bank, no Docker or act, and no host `act_ci`.
- **No manager source bank** exists at this head, and I infer none.
- **No hardware proof.** Physical calibration was NOT RUN, and the skipped field contexts are not hardware proof.
- **Hosted contexts** were still running when the snapshot was taken.

## Pending manager duties

- Validate the current-dev merge candidate (source base `1f29f189`, live dev `e61a4afa`) with the builder and native banks, and link the receipts.
- Accept the hosted and act exact-head contexts.
- Carry R763-11-R1, R763-10-R2 and R764-10-R3 to the residue checklist.
- Merge only with explicit maintainer authorization.

R763-11 FINISHED
