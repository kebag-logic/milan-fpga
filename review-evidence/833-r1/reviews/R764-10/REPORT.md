[R764] POSITIVE - exact head fce77f0efc1425ef7732a8d70c02addc108f7afe

External independent review of issue #833 / PR #834, round R764-10. Tree `5c37f78dadab8c4624d1b84d966d44accda975f1`, source base `1f29f189279f9fc0132f4918e47342b87d22f33a`. The round 10 delta is `e803d94b..fce77f0e`: six one-line commits in `scripts/test_suite_cancellation.py`, `scripts/process_test_support.py` and `docs/testing/TESTING.md`. `scripts/owned_process.py` is byte-identical to the previous head (`git diff --quiet e803d94b HEAD -- scripts/owned_process.py`).

I reconstructed the round from public state in a cleared context, in this order:
- AGENTS.md / CONTRIBUTING.md;
- the manager's round 10 ruling (issuecomment-6592794168);
- the diff and its six commits;
- the live PR body;
- the published packet at `66b6f829:review-evidence/833-r1`.

I read the prior round 9 findings (R763-9, issuecomment-6592787571, and my own R764-9) only after my own pass over the diff. My only inputs from my own earlier round were my round 9 driver scripts, which I re-ran unchanged.

## Summary

- **Verdict POSITIVE.** No BLOCKER, MAJOR or MINOR is open. All six ruling items are met at this head.
- **Item 1, `owner_report`.** The child now waits in `signal.pause()` with no timer (`scripts/test_suite_cancellation.py:441-442`). `STUBBORN` is unchanged and still used by the other controls (`:376-384`, `:508`, `:533`, `:578-579`, `:628-629`).
  - My round 9 driver, 8 at once, gave **0 red in 6000 runs**:
    - 3000 at mean load 25.8;
    - 3000 more with every run at load 40 or more, mean 53.5.
  - All 6 `owner_report` mutants are red with their words.
- **Items 2 to 4.**
  - Every listing the ruling names is present and asserts its events.
  - Each new mutant is red with its words, and the per-listing map shows where each is red.
  - Six of the seven new mutants match R763-9's published edits byte for byte; the seventh is the author's edge mutant.
- **Item 5.** One added guide line (`TESTING.md:262`), and no row changed in that commit.
- **Item 6.** R763-9-R1's exact text is applied (`test_suite_cancellation.py:831-832`).
- **My round 9 sweep at this head.** It has 99 mutants over 46 listings (35 at round 9).
  - 24 survive every owner control and the whole test (33 at round 9). One more is red only on `owner_shell_window`.
  - The 9 killed since round 9 are exactly the classes R764-9-S1 targeted, plus `E/C2`, which an early listing kills.
  - No survivor is new, and none lies inside a stated domain as item 5 defines it.
  - The remaining 24 are recorded once as RESIDUE (R764-10-R3), per the ruling.
- **Two wording RESIDUEs in the delta's prose (R1, R2) and one SUGGESTION (S1).** None blocks.

## Item checks

### 1. `owner_report` (R763-9-F3 = R764-9-F1)

- **The fix is R763-9-F3's, exactly.** `:441-442` reads `"import os, signal, sys; from pathlib import Path; " "Path(sys.argv[1]).write_text(str(os.getpid())); signal.pause()"`.
  - The child now has no timer, so after `eventually(... == "S")` (`:447`) nothing wakes it before `_describe` (`:449`).
  - The report now shows `wchan __do_sys_pause` (`receipts/author-campaign.log`, the `report-*` lines), so the non-empty-wchan assertion still has teeth.
- **`STUBBORN` is unchanged.** The only `STUBBORN` line in the delta is the removed use at `:441`.
- **Stress, with my round 9 `scripts/repeat_control.sh`, unchanged, on a `git archive` copy of the head, 8 at once:**

  | Batch | Runs | Red | Load |
  |---|---|---|---|
  | `receipts/owner-report-head-1*` | 3000 | 0 | mean 25.8 |
  | `receipts/owner-report-head-2*` | 3000 | 0 | every run at load1 >= 40, mean 53.5 |

  The round 9 head under the same driver gave 10 of 5760 (R764-9-F1).
- **Mutants.** All 6 are red on `owner_report` with their words: `report-without-state`, `-wchan`, `-state-or-wchan`, `-current-parent`, `report-age-in-ticks` and `report-parent-is-first-parent` (`receipts/author-campaign.log`).
- **Published receipts agree.** The hashes match `MANIFEST.json`:
  - `author-r10/receipts/final/r763-9-stress-final-head.log`: 3000 runs, 0 red;
  - `r764-9-repeat-final-head.log`: 3200 runs, 0 red, mean 44.2.

### 2. The early-in-grace listings (R763-9-F1)

- **Mechanism.**
  - `kept` (`test_suite_cancellation.py:776-787`) keeps a listing again as "an early ..." when its census at `TICK` lists something its census at 0 does not.
  - That copy has `(TICK, "census")` inserted after the first event.
  - `starved_cleanup`'s `pause` (`process_test_support.py:300-307`) lands a pass exactly on that time and notes it. So the listing's own equality assertion proves the pass was placed.
- **The eight early listings** (`receipts/reviewer-sweep.json`, `none` cells) are exactly the guide's table (`TESTING.md:302-309`):
  - after a first-pass resume, not live and live;
  - with no shell, not live and live;
  - beside a stopped shell, not live and live;
  - beside a shell never resumed, under it and beside it.
- **The four early mutants** are byte-identical to R763-9's `natural.py`. That file's sha256 `9b111b07…` matches `MANIFEST.json` (`receipts/byte-match-r9.log`). Each is red on `owner_stated_seconds` with its words (`receipts/author-campaign.log`). The per-listing map (`receipts/author-cellmap-new.txt`) shows where:

  | Mutant | Red on |
  |---|---|
  | `early-new-sigtermed-0.25` and `-0.5` | all 8 early listings |
  | `early-trap-command-sigtermed` | the 2 early first-pass listings |
  | `early-live-new-sigtermed` | the 5 early live listings |

- **Named in rows 2 and 6.** All four are in row 2 (`TESTING.md:314`) and row 6 (`:318`).
  - Row 2's domain adds "first listed a tick after the first pass, live or not, in the early listings: with no shell, beside a stopped one, and after a first-pass resume".
  - Row 6's adds "and a tick after a first-pass resume, in its early listings".
  - Both are true of the listings.

### 3. A live new descendant beside a shell never resumed (R763-9-F2)

- **The listing is R763-9-F2's preferred listing with its stated event list.**
  - Listing `:867-872`, under-shell case: `{shell, child: (shell), live: (child) from pass 2}`.
  - Events: `SIGTERM` child at 0; `SIGKILL` trap command at 2; `SIGKILL` child at 4; at 14, `SIGKILL` shell, child and trap command, then the verdict.
- **Named in rows 3 and 4 and the liveness table.**
  - Row 3 (`:315`): "with no cancelled shell, and under or beside one never resumed".
  - Row 4 (`:316`): "with or without a new descendant, live or not".
  - Liveness table: `:291`.
- **Both F2 mutants are byte-identical to R763-9's.** `parent-of-live-new-unspared-beside-shell` and `verdict-early-live-new-beside-stopped-shell` are red with "a live new descendant beside a shell never resumed's …". Each is red on 4 listings: both never-resumed listings and their early copies.
- **The edge mutant** `parent-under-unresumed-shell-unspared` is red only on the under-shell listing and its early copy. That is the one cell that tells under from beside.
- **Row placement.** Both parent mutants are in row 3 and the verdict mutant is in row 4.

### 4. R764-9-S1's three listings

1. **The live trap command after the 1 s resume.** `("one-second", 1)` joins the live loop (`:847-848`), and the liveness table has it (`:293`).
2. **The live new descendant beside a shell never resumed.** This is item 3's listing.
3. **A non-shell parent with a live child beside a stopped shell.** This is the beside case of `:867-872`: the child under the owner, killed at 4 s. The liveness table has it (`:292`).

Rows 2 (`:314`), 6 (`:318`) and 8 (`:320`) now read "live or not … at 1 s". Row 8 keeps "not live" only at 3 s, 5.5 s and a tick before 14 s, which matches the listings.

My sweep confirms the target classes are killed (below).

### 5. The listing-time domain (R763-9-S1)

- **Commit `500b0f618c` adds one line and changes nothing else** (`TESTING.md:262`): "Between stated times the starved owner's passes are half a second apart; a listing's domain is its listed passes."
- **It matches `pause`** (`process_test_support.py:300-307`):
  - with no stated time within half a second, a pass counts 0.5 s;
  - otherwise it lands a tick short and then on the time, which `:260` already states.
- **No row's claim changes.** I applied it as the ruling defines it: a survivor is in-domain only if a row's domain words claim a configuration at one of a listing's listed passes where the mutant differs.

### 6. R763-9-R1

The printed summary carries `next_to_last=2 - 2 * TICK, lone=[1, 10], live_new_descendant=True` (`:831-832`), byte for byte R763-9-R1's text. This also takes R764-9-S2.

### Module moves

- **`BLOCKING` moved byte-identical** into `process_test_support.py:264-270`. It is no longer defined in the test file, and its one use (`test_suite_cancellation.py:886`) imports it (`:25`).
- **Every one of the 143 round 9 `MUTANTS` entries has an identical value, in the same order.** 7 entries are appended (`receipts/module-moves.log`, `scripts/module_moves.py`, AST literal evaluation of both heads).
- **The ratchet.** The re-laid words are string-literal continuations only. The modules are 999 and 996 lines. `scripts/check_py_idiom.py` is rc 0 at this head, with `long module: 10 <= 10` (`receipts/py-idiom-check.log`).
- **`git diff --check 1f29f189 HEAD` is silent.**

## The sweep at this head (my round 9 `scripts/cell_sweep.py`, unchanged)

- **The unmutated tree** passes all 46 listings.
- **74 of 99 mutants** are red on at least one listing; 25 are red on none.
- **The launcher artifact.** Phase 2 of the script ran under a launcher that ignored SIGHUP. There every whole-test run timed out in the hard-HUP stop. That is the retained R764-6-S1 condition, not a mutant effect.
- **Re-run with SIGHUP at its default** (`scripts/whole_rerun.py`, `receipts/whole-rerun.log`):
  - the head is PASS, in 62 s;
  - 24 of the 25 are PASS;
  - `B/live/R7` is red on `owner_shell_window` and the whole test, as at round 9.
- **Killed since round 9 (9):**
  - `A`, `B`, `H/live/R3`, `G-postponed/R3` and `G-hastened/R3`, by the 1 s live listing;
  - `G-postponed/shell-unresumed`, `G-hastened/shell-unresumed` and `D-live-new-child-spares-nothing/shell`, by the never-resumed listings;
  - `E/C2`, by the early listings.
- **No new survivor.** The 24 that survive everything are a subset of round 9's 33.

**Classification under item 5** (each checked against the row's domain words and the listings' passes):

| Survivors | Status | Why |
|---|---|---|
| `E/C1`, `F-new/C1` | equivalent | No descendant is new in the first pass (`owned_process.py:286-287`). |
| `H/live/R5`, `R6`, `R7`, `R8` | equivalent | Past grace, a shell whose live trap command is its child is spared by the parent rule (`owned_process.py:329`), whether or not its own skip applies. The product is unchanged, so the round 9 argument stands. |
| `E/C6`, `E/C8` | outside | No listing has a live new descendant alone holding a pending resume at a pass in 2 s to 2.25 s or at 13.75 s or later. The 3 s listing's passes are 0.5, 1, 1.5, 2 less a tick, 2, 2.5 and 3 less a tick, and its early copy's are a tick in, then plus 0.5 s steps. In the never-resumed listings the first-census child, which is live, also holds the resume, so the mutant does not differ at 14 s less a tick. |
| `F-new/C2`, `C4`, `C5`, `C6` | outside | A not-live new descendant at the resume pass is listed only at 1 s, 3 s, 5.5 s and a tick before 14 s (guide `:280`). In the early not-live listing beside a stopped shell, the live child holds the resume anyway. |
| `F-initial/C1`, `C2`, `C3`, `C5`, `C6`, `C7`, `C8` | outside | A not-live first-census entry beside a pending resume is listed only as the next-to-last cell's zombie, at 2 s less two ticks (C4, killed). |
| `G-postponed/R7`, `G-hastened/R7` | outside | No listing resumed between 2.25 s and 13.75 s has a live new descendant at its verdict. Rows 6 and 8 say "not live" at 3 s and 5.5 s. |
| 3 `X-*` | outside | Contrived thresholds of a microsecond, or "no zombie", inside the next-to-last cell. At its listed passes they behave as the product does. |

So by item 5 none is a finding. All 18 non-equivalent ones are RESIDUE R764-10-R3.

## Findings

### R764-10-R1 - RESIDUE - Docs - `docs/testing/TESTING.md:295` - "The last cell" now points at the wrong row

- **Evidence:** at the previous head the next-to-last cell was the liveness table's last row. Round 10 appended three rows after it (`:291-293`), so "The last cell" now reads as the 1 s row. The sentence's own words still name the right listing.
- **Impact:** wording only. It changes no listing, mutant, row domain or claim.
- **Exact fix:** replace "The last cell is listed with a command that is not live as well:" with "The next-to-last in-grace cell is listed with a command that is not live as well:".
- **Verification:** read `:286-295`.

### R764-10-R2 - RESIDUE - Docs - `docs/testing/TESTING.md:297`, `scripts/test_suite_cancellation.py:778-779` (docstring) - "whose census grows after the first pass" is wider than the rule

- **Evidence:** the rule (`:786`) keeps a listing early only if its census at a tick in lists something its first census does not.
  - "an in-grace resume", "a second-stage resume" and the matrix cells with a trap command all grow after the first pass, at their resume, and get no early copy.
  - The guide's early table (`:302-309`) lists exactly the eight that do. The row domains cite "the early listings". The PR body already states the rule exactly.
- **Impact:** wording only. No row domain or claim depends on the sentence.
- **Exact fix:**
  - At `TESTING.md:297`, replace "Each listing whose census grows after the first pass is kept again, early:" with "Each listing whose census, a tick after the first pass, lists a descendant its first census did not is kept again, early:".
  - In the docstring at `:778-779`, replace "one whose census grows after the first pass does so again early" with "one whose census a tick in lists a descendant its first did not does so again early".
- **Verification:** read both lines.

### R764-10-R3 - RESIDUE - Tests - `receipts/reviewer-sweep-summary.txt`, `receipts/whole-rerun.log` - the sweep's 18 non-equivalent out-of-domain survivors, listed once

- **Survivors:** `E/C6`, `E/C8`, `F-new/C2`, `C4`, `C5`, `C6`, `F-initial/C1`, `C2`, `C3`, `C5`, `C6`, `C7`, `C8`, `G-postponed/R7`, `G-hastened/R7`, and the 3 `X-*`.
- **Evidence:** each falls outside every listed pass and domain, as tabled above.
- **Impact:** none on any stated claim. Per the round 10 ruling, a survivor outside a stated domain is residue.
- **Exact fix:** none required. The manager carries it to the residue checklist.
- **Verification:** `python3 -I scripts/cell_sweep.py <tree> <scratch> <out.json> --jobs N`, then `scripts/whole_rerun.py` with SIGHUP at its default.

### R764-10-S1 - SUGGESTION - Tests - `scripts/test_suite_cancellation.py:787` - `f"an early {words[2:]}"` assumes the words start with "a "

- No growing listing starts with "an " today, so every early name is right.
- A future one would print "an early  …".
- An `assert words.startswith("a ")` beside it, or a split on the first word, would hold the convention.
- This is optional.

No new comment-rule instance: the delta's added source lines carry no lane label, round, reviewer ID or comment ID. The only issue reference is the existing `#833`.

## Prior findings at this head

| ID | Severity | Status at fce77f0e | Evidence |
|---|---|---|---|
| R764-9-F1 = R763-9-F3 | MINOR / MAJOR as ruled | **RESOLVED** | `:441-442`; 0 of 6000 red, 3000 of them at load >= 40; 6 of 6 `owner_report` mutants red with their words |
| R763-9-F1 | MINOR | **RESOLVED** | 8 early listings; 4 byte-identical mutants red with their words on the early listings; rows 2 and 6 |
| R763-9-F2 | MINOR | **RESOLVED** | the preferred listing and event list (`:867-872`); both mutants byte-identical and red; edge mutant red on its cell alone; rows 3 and 4 and liveness table `:291` |
| R764-9-S1 | SUGGESTION | **Taken** | three listings; the 9 targeted survivor classes are killed; rows 2, 6 and 8 drop "not live" at 1 s |
| R763-9-S1 | SUGGESTION | **Taken** | `TESTING.md:262` |
| R763-9-R1 = R764-9-S2 | RESIDUE / SUGGESTION | **RESOLVED**, exact text | `:831-832` |
| R764-6-S1 | SUGGESTION | Retained, not taken | It is outside #833. My sweep's phase 2 hit exactly this launcher condition; the campaign driver resets SIGHUP (`process_test_support.py:965-981`). |

## Lens results

```text
[R764] PASS Conformance — docs/testing/TESTING.md:262,291-293,297-320; scripts/test_suite_cancellation.py:441-442,776-787,831-832,847-872 — ruling items 1 to 6 checked against the listings, the per-listing map of all 149 mutants and 6000 owner_report runs; #833 acceptance 2 (no chance failure) holds for owner_report at load >= 40
[R764] PASS RTL — scripts/owned_process.py byte-identical since e803d94b (git diff --quiet) and the delta stat (no hdl/, no product code) — the cleanup state machine's transitions re-probed by 99 reviewer mutants over 46 listings; no interface or contract change
[R764] PASS Robustness — receipts/owner-report-head-1*, -2* (6000 runs, 8 at once, mean load 25.8 and 53.5); receipts/whole-rerun.log (head and 24 survivors, whole test) — the control is now race-free under load; feature/launcher dependence is the retained R764-6-S1 only
[R764] PASS Tests — scripts/test_suite_cancellation.py:776-872; scripts/process_test_support.py:264-307 and the MUTANTS tail; receipts/author-campaign.log (PASS, 149 mutants, 146 with a control), author-cellmap-new.txt, byte-match-r9.log, module-moves.log, reviewer-sweep.json, whole-rerun.log — every new listing has a mutant red on it; no in-domain survivor; R3 is residue by the ruling
[R764] PASS Docs — docs/testing/TESTING.md:255-325; live PR body (Round 10), equal to the packet's author-r10/PR-BODY.md apart from its trailing newline — the rows, liveness and early tables match the listings; R1 and R2 are wording RESIDUE only
```

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | round 10 ruling; `TESTING.md:255-325`; `test_suite_cancellation.py:435-470, 740-872`; `owned_process.py` (unchanged) | R764-10 | fce77f0efc1425ef7732a8d70c02addc108f7afe |
| RTL | CLEAN | `owned_process.py`, byte-identical since `e803d94b`; delta stat with no HDL; 99-mutant sweep | R764-10 | fce77f0efc1425ef7732a8d70c02addc108f7afe |
| Robustness | CLEAN | `owner_report` stress, 6000 runs; whole test at the head and on 24 survivors with SIGHUP at its default | R764-10 | fce77f0efc1425ef7732a8d70c02addc108f7afe |
| Tests | CLEAN | author campaign; per-listing map of 149 mutants; reviewer sweep; byte match against R763-9 `natural.py`; module-move check; idiom ratchet | R764-10 | fce77f0efc1425ef7732a8d70c02addc108f7afe |
| Docs | CLEAN (RESIDUE R1, R2 carried) | `TESTING.md:255-325`; PR body Round 10; delta docstrings and comments | R764-10 | fce77f0efc1425ef7732a8d70c02addc108f7afe |

## Evidence checked

- **The packet.** Commit `66b6f829` ("Archive #834 round 10 author packet") is **unsigned**; GitHub reports `unsigned`. Its integrity record is `MANIFEST.json`, with 8882 entries. 12 of 12 sampled files match `published_sha256` (`receipts/packet-hash-check.log`):
  - `PR-BODY.md` and `cost.txt`;
  - `matrix-part1..4.rc`, all 0, and `matrix-part4.log`;
  - both reviewer-driver stress logs;
  - `gates/docs_all.out`: every docs.yml shard "failed 0";
  - `row-mutants.log`;
  - R763-9's `natural.py`.
- **Own runs at this head**, all on a `git archive` copy:
  - `--mutants --jobs 8`: PASS, 149 mutants, 146 with a control;
  - the whole test: PASS;
  - `check_py_idiom.py`: rc 0, run in the clone read-only.
- **Hosted contexts at this head, read-only, at the time of reading.**
  - Executed and passed (15): `changes`, `full-ci-gate`, `docs-gates-0/2`, `docs-check-no-git`, `wire-accountability`, `elaborate-gates-0`, `bdd-conformance`, `verilator-lint`, `firmware-unit`, `firmware-verilator`, `firmware-aecp-mutants`, `firmware-srp-mutants`, and the two `Prepare pinned Yosys` jobs.
  - In progress or queued (33): the Verilator and Yosys shards, `docs-gates-1`, `elaborate-gates-1`, `yosys-elaboration`, `publication-census`, and the firmware boundary and control-mutant jobs.
  - Skipped: `Physical gPTP (nightly and manual)`.
  - I infer nothing from pending contexts (`receipts/hosted-success.txt`).
- **Restored state.** The clone was never edited. HEAD and tree are exact, and `git status` is empty. Index and worktree equal HEAD, and blob ids and modes from `ls-files -s` equal `ls-tree -r HEAD`. The six submodule gitlinks are unchanged since `e803d94b` (`receipts/restore-check.log`).

## Real limits

- No manager source bank ran at this head, and I claim none. The source-head gates are the author's published receipts, which I spot-checked by hash.
- I ran no full parent, PP, gPTP, Yosys or builder bank, and no docs.yml replay.
- Physical calibration was NOT RUN, and the field skips are not hardware proof.
- The sweep is a reviewer sample at class granularity, not an exhaustive proof. The equivalence claims rest on reading the cited lines.
- The load figures are from a shared 16-CPU host whose load moved between about 8 and 57. The `owner_report` result is a measurement, not a bound.
- My sweep's phase 2 ran under a SIGHUP-ignoring launcher. Its whole-test column in `reviewer-sweep.json` is superseded by `whole-rerun.json`.
- Some receipts (`reviewer-sweep.json`, `author-cellmap.json`, `author-campaign.log`) contain this host's scratch and `/tmp` paths. The manager may redact them.

## Pending manager duties

- Validate the current-dev merge candidate at the merge turn: source base `1f29f189`, live dev `e61a4afaa54a598ceec08b7b5879285256cc60b6`. That covers the builder and native banks, and hosted and act acceptance at the final head.
- Carry RESIDUE R764-10-R1, R2 and R3 to the residue checklist. Carry SUGGESTION S1 and the retained R764-6-S1 at your discretion.

R764-10 FINISHED
