[R764] NEGATIVE - exact head e803d94b3a11921a293cf036a8eda333d23828f9

External independent review of issue #833 / PR #834, round R764-9. Tree `e10d752b67f6b8a1b726c60f1889e61ff60bbb1b`, source base `1f29f189279f9fc0132f4918e47342b87d22f33a`. The round 9 delta is `5b6d38a3..e803d94b`. I reconstructed it from public state in a cleared context: AGENTS.md / CONTRIBUTING.md, the issue body and acceptance, the manager's round 9 ruling (issuecomment-6590477473), the READY post (issuecomment-6592237814), the PR body, the diff, and the published packet at `ce4b2da6:review-evidence/833-r1`. I read the round 8 reports (issuecomment-6590465323 and -6590467902) only after my own pass over the diff and my own sweep.

## Summary

- **Verdict NEGATIVE, on one MINOR finding: R764-9-F1.** It is the item 5 question. The `owner_report` control, which this PR adds to the sweep preflight, fails by chance under load. I reproduced it at this head: 10 of 5760 runs red. The exact fix is one line, and with it 0 of 4480 runs are red. Lenses: Conformance, Tests, Robustness.
- **Round 9's own items are met** (items 1 to 4):
  - every liveness listing the ruling names is present and asserts its row;
  - all 13 round 8 reviewer mutants are in `MUTANTS` byte for byte, and each is red with its words and named in its row;
  - each of the ten edge mutants is red on its own cell and no other;
  - the RESIDUE fixes are applied exactly.
- **My sweep found no survivor inside a stated domain.** It ran 99 of my own mutants over all 35 listings of `owner_stated_seconds`, one family per row and behaviour, crossed with resume class, liveness and shell. Survivors were then run on every owner control and the whole test.
  - 33 survive everything.
  - 6 of the 33 are equivalent mutants.
  - 27 are outside the listed domains. Each is listed below with its row and the domain words that leave it out. By the bar they are residue. SUGGESTION S1 says which three cheap listings would close most of them.
- **`scripts/owned_process.py` is byte-identical to the round 8 head.** No probe showed the product wrong.

## Item checks (Focus 1 to 5)

### 1. The liveness listings, and the reading of "late in grace"

The listings are in `stated_liveness`, `scripts/test_suite_cancellation.py:830-860`. A real `cat` process stands for a live descendant. The product's `_live` (`owned_process.py:104-106`) reads `/proc` for real, so it sees that process as live.

- **R763-8-F1, beside a stopped shell before any resume** (`:845-848`).
  - The live descendant is listed from pass 2 until 3 s.
  - The shell's `SIGCONT` is stated at 3 s. It comes in the first pass in which nothing else lives (`owned_process.py:304`).
- **R764-8-F1, with no cancelled shell** (`:850-853`).
  - A survivor's trap starts the live descendant.
  - It gets no `SIGTERM`, and gets `SIGKILL` at 2 s.
  - Its parent, the survivor, is spared to 4 s by `owned_process.py:329`. The verdict is at 14 s.
- **R764-8-F1, the trap's command after an in-grace resume, in pass 1 and pass 2** (`:842-843`).
  - The live column of `RESUME_MATRIX` (`process_test_support.py:267`) covers every class of resume, beyond the ruling.
  - Each cell asserts no `SIGTERM`, and `SIGKILL` and the verdict at 10 s and 20 s after the resume.
- **R763-8-F2, "late in grace"** (`:854-860`). The author reads it as the command first listed in the last pass before 2 s, after a resume one pass earlier at 2 s less two ticks. I checked that reading against the product:
  - Inside grace, whether a new descendant gets `SIGTERM` depends on just two things (`owned_process.py:313,319-323`): whether that pass's clock is below `deadline`, and whether the descendant is in the first census.
  - So the latest point at which a trap's command can face that branch is the last pass before 2 s.
  - A live command cannot be listed in its resume pass, because it would hold the resume (`:304`). So "after a resume a pass earlier" is the only way to list one there.
  - The other reading, a resume *in* the last in-grace pass, is the matrix cell "a last in-grace resume and its live trap command". There the command is first listed past grace.
  - **Both readings are listed.** The zombie that sets the pace is from the first census and is not live. It is `SIGTERM`ed at 0 s and `SIGKILL`ed at 2 s, and it holds nothing. I checked the starved clock's `pause` by hand: the passes fall at 1.5 s, 2 s less three ticks, 2 s less two ticks (the resume), 2 s less a tick (the command) and 2 s.
- **The reading is consistent with the product.**

### 2. The 13 round 8 reviewer mutants

- **Byte for byte.** I evaluated only the literal edit tables of the published probe sources at `ce4b2da6` (`reviews/R763-8/r8_mutants.py`, `reviews/R764-8/probes/r764_8_live_probes.py`, `r764_8_probes.py`). Their hashes match their packets' `MANIFEST.sha256`. All 13 edits are byte-identical to `MUTANTS` (`receipts/byte-match.log`).
- **Red with their words.** The default campaign is PASS, 142 mutants with 139 controls (`receipts/author-campaign.log`). Each of the 13 is red on `owner_stated_seconds` with its words.
- **Named in their rows.** Every mutant with a control is named in the guide's tables (`receipts/table-names.log`). The 3 not named have no control, and each says why: `sigterm-checks-parent`, `no-sigcont-after-send`, `no-leaf-first`.

### 3. Domain notes and the ten edge mutants

- **The domain notes name the liveness cells.** Rows 2 to 8 (`docs/testing/TESTING.md:295-301`) name them, and the liveness table is at `:284-290`.
- **Each edge mutant is red on its own cell alone.** I put the control in record mode in a copy, so that every listing reports instead of stopping at the first failure (`scripts/cell_sweep.py --author`, `receipts/author-cellmap.txt/.json`). Each of the ten is red on exactly one listing, its own.
  - Example: `next-to-last-in-grace-trap-command-sigtermed` is red only on "a next-to-last in-grace resume and its trap command".
  - Example: `live-new-sigtermed-with-no-shell` is red only on "a live new descendant".

### 4. Residues

- **R763-8-R1** is applied as published (`TESTING.md:263`).
- **R763-8-R2, the same as R764-8-R1**, is applied (`test_suite_cancellation.py:752-753`).
- **R763-8-R3** is applied (`:814-815`).
- **R764-8-S1** is taken (`TESTING.md:262`).
- **The comment rule.** The delta's added source lines carry no lane label, round, reviewer ID or comment ID; the only reference is `#833`.
- **Whitespace.** `git diff --check 1f29f189 e803d94b` is silent.

### 4b. The sweep: every cell of every row

**Method.** `scripts/cell_sweep.py` applies each mutant to a copy of `scripts/`. It runs `owner_stated_seconds` in record mode, which prints each of the 35 listings as `CELL` or `FAILCELL`. The unmutated tree passes all 35. Every mutant red on no listing is then run, with the test unmodified, on all ten owner controls and the whole test (`receipts/reviewer-sweep.txt/.json`).

**The families**, at each site of `owned_process.py:256-339`:

| Family | What it breaks | Cells |
|---|---|---|
| A | `SIGTERM` to a new descendant in grace | live or not, × no shell / shell unresumed / resumed in each in-grace class |
| B | the trap command's window | live or not, × 8 resume classes |
| C | a new descendant spared past 2 s with no resume | live or not, × shell or none |
| D | parent sparing by a new child | live or not, × shell or none |
| E | a live new descendant ignored for the resume | × 8 pass classes |
| F | a not-live descendant holding the resume | new or from the first census, × 8 pass classes |
| G | the verdict postponed or hastened while a live new descendant is listed | no shell / unresumed / 8 resume classes |
| H | the shell's own window lost beside its trap command | live or not, × 8 resume classes |
| X | 3 deliberately contrived edges | |

The classes are: the first pass; early in grace (under 0.25 s); the interior of grace; late in grace (1.75 s to 2 s); the first pass past grace; early past grace; the interior past grace; and late past grace (13.75 s or more).

**Result:** 99 mutants. 65 are red on at least one listing, and 1 more is red on `owner_shell_window` and the whole test (`B/live/R7`). **33 survive every control and the whole test.**

**Equivalent mutants (6):**

| Mutants | Why they are equivalent |
|---|---|
| `E/C1`, `F-new/C1` | No descendant is new in the first pass: `initial` is that pass's census (`owned_process.py:286-287`). |
| `H/live/R5`, `R6`, `R7`, `R8` | Past grace and before `kill_all`, a shell whose live trap command is its child is spared by the parent rule (`owned_process.py:329`) whether or not the shell's own skip (`:317`) applies. They would differ only for a re-parented trap command, which no row states. |

**Outside the listed domains (27), so residue by the bar:**

| Survivors | Row | Why it is outside |
|---|---|---|
| `A/live/R3`, `B/live/R3`, `H/live/R3`, `G-postponed/R3`, `G-hastened/R3` | 2, 6, 7, 8 | A live trap command after an interior in-grace resume (1 s). Rows 2 and 6 say "not live, after a resume at 1 s", and row 8 says "and, not live, after resumes at 1 s, 3 s, 5.5 s". |
| `G-postponed/R7`, `G-hastened/R7` | 6 | The verdict with a live trap command after 3 s or 5.5 s. Those listings' commands are not live (the guide's liveness table, `:284-290`, lists every live cell). |
| `E/C2`, `E/C6`, `E/C8` | 5 | Whether a live new descendant holds the resume, at passes the 3 s listing does not have: under 0.25 s, 2 s to 2.25 s, and 13.75 s or more. Its passes are 0.5 s, 1 s, 1.5 s, 2 s less a tick, 2 s, 2.5 s and 3 s less a tick. The guide says "A cell's domain is its listed resume". |
| `F-new/C2`, `C4`, `C5`, `C6` | 5 | Whether a not-live new descendant fails to hold the resume. It is pinned only at 1 s, 3 s, 5.5 s and a tick before 14 s, by the listings that list the command in the resume pass. The ruling's axis is the live one. |
| `F-initial/C1`, `C2`, `C3`, `C5`, `C6`, `C7`, `C8` | 5 | Whether a first-census zombie fails to hold the resume. It is listed only at 2 s less two ticks. |
| `G-postponed/shell-unresumed`, `G-hastened/shell-unresumed` | 3 | A live new descendant beside a shell never resumed. Row 3 says "beside a shell never resumed, with or without a new descendant", and gives "live or not" only to the no-shell clause. That listing (`:809-812`) is not live. |
| `D-live-new-child-spares-nothing/shell` | 2nd row | Parent sparing beside a cancelled shell. The row's parent listings ("a stubborn parent", "a live new descendant") have no shell. |
| 3 `X-*` | 2 | Thresholds of a microsecond, or "no zombie listed", inside the next-to-last cell. That cell's own resume and listing pass behave correctly under them. |

**No survivor falls inside a row's stated domain.** So by the bar the sweep raises no finding.

### 5. The `owner_report` race: a finding, R764-9-F1

## Findings

### R764-9-F1 - MINOR - Conformance, Tests, Robustness - `owner_report` fails the sweep preflight by chance under load

- **Locations:**
  - `scripts/test_suite_cancellation.py:441`: the sleeper is `STUBBORN`, which wakes every 20 ms (`:382-383`);
  - `:446`: `eventually(... == "S")`;
  - `:448`: a second, separate `_describe` read;
  - `:451-452`: `assert "state S" in asleep`;
  - preflight: `scripts/run_all_suites.sh:288-292`, where a red aborts the sweep with exit 2.
  - `owner_report` was added by this PR (`58c8a367d7`), in a file this PR changes.
- **Authority:**
  - Issue #833 acceptance 2: "... with no suite left to fail by chance".
  - The issue body: a sweep failure is "not accepted as a flake by default".
  - AGENTS.md section 6, Tests lens: a test must fail only for the defect it claims to detect.
- **Evidence, measured at this head** (`scripts/repeat_control.sh`, `receipts/owner-report-*`):
  - The unmodified control is red in **10 of 5760** runs at host load 5 to 40, 16 at once:
    - 2 of 1280 at load about 5;
    - 0 of 1280 at about 30;
    - 8 of 3200 at about 40.
  - Every red is `AssertionError: ('state S', '... state R wchan hrtimer_nanosleep ...')` (one has `wchan 0`). The control saw the child asleep, and the child then woke for its next 20 ms tick before the report's own read.
  - That agrees with the author's 4 of 1152.
  - The other nine owner controls had 0 reds in 192 runs each, at load 42 to 50 (`receipts/repeat-*`).
- **Impact:**
  - The preflight runs in every sweep and act shard under full host load, and a red aborts it with exit 2.
  - At about 0.2 % to 0.35 % per run, a sweep of k shards fails by chance with probability about k times that.
  - That is the failure class this issue exists to remove, now coming from its own control. The product's report was right every time.
- **Required outcome:** the child that `owner_report` observes stays in state S from the control's wait through the report's read, and the `state S` assertion is kept. This is not RESIDUE: it changes a test.
- **Exact fix, verified in a scratch copy** (`receipts/owner-report-fix.diff`). At `:441`:

  ```python
  sleeper = subprocess.Popen([sys.executable, "-c", STUBBORN.replace("time.sleep(0.02)", "time.sleep(3600)"), str(ready)])
  ```

  A dedicated constant with one long sleep is equivalent. The shared `STUBBORN` stays unchanged for the other controls.
- **Verification:**
  - With the fix: **0 of 4480** red at load about 19 to 49 (`receipts/owner-report-fix-*`). Against the head's 10 of 5760, one-sided Fisher p = 0.003.
  - The whole test is PASS with the fix (`receipts/whole-fix.log`).
  - All six `owner_report` mutants are still red on it with their words (`receipts/fix-owner-report-mutants.log`).
  - Re-run: `scripts/repeat_control.sh <tree> owner_report 16 200 <out>`, expecting 0 red.

### R764-9-S1 - SUGGESTION - Tests, Docs - three listings would close most of the sweep's out-of-domain survivors

These are optional. Each is one `kept` call on the existing helpers.

1. **A live trap command after the 1 s resume**, `cell(1, live)` with `window(1)`. It closes `A`, `B`, `G` and `H/live/R3`. Then rows 2, 6 and 8 can drop "not live" at 1 s.
2. **A live new descendant beside a shell never resumed**, the child outliving 14 s, with the verdict at 14 s. It closes `G/shell-unresumed`, so row 3's "with or without a new descendant" holds live or not.
3. **A non-shell parent with a live child beside a stopped shell**, killed at 4 s. It closes `D/shell`.

### R764-9-S2 - SUGGESTION - Tests - `scripts/test_suite_cancellation.py:824-827`

The printed `owner-stated-seconds:` summary still lists `resumes=[0, 1, 3, 5.5, last]`. It does not show the resume at 2 s less two ticks, the lone resumes at 1 s and 10 s, or the liveness cells. Adding them, for example `next_to_last=2 - 2 * TICK, lone=[1, 10], live=True`, would make the receipt line match the listings. It is optional, since no row cites the line.

No RESIDUE is raised in the round 9 delta.

## Prior findings at this head

| ID | Severity | Status | Evidence |
|---|---|---|---|
| R763-8-F1 | MINOR | **RESOLVED** | Listing `:845-848`. `resume-beside-new-live` is red on it alone, and so is the edge mutant `resume-beside-live-new-past-grace`. Row 5 names it (`TESTING.md:298`). |
| R763-8-F2 | MINOR | **RESOLVED** | Listings `:854-860`. `sigterm-trap-command-after-resume-from-1.5s` is red on both next-to-last cells. Rows 2 and 6 name them. My `A/notlive` and `A/live/R4` mutants are red there too. |
| R764-8-F1 | MINOR | **RESOLVED as ruled** | All three places are pinned: with no shell (`:850`), beside a stopped shell (`:845`), and as the trap's command in pass 1, pass 2 and late in grace (`:843`, `:856-860`). Both survivors are red. The round 8 required outcome also named a live command after the 1 s resume. The ruling's list replaced that with pass 1, pass 2 and late in grace. The guide now says "not live, after a resume at 1 s", so nothing is over-claimed there. The survivors at 1 s are out-of-domain residue, and S1.1 would pin it. |
| R763-8-R1, R2 (= R764-8-R1), R3 | RESIDUE | **RESOLVED**, exact fixes applied | `TESTING.md:263`; `test_suite_cancellation.py:752-753, 814-815` |
| R764-8-S1 | SUGGESTION | **Taken** | `TESTING.md:262` |
| R764-6-S1 | SUGGESTION | Retained, not taken, as the author states | It is outside #833; no change. |

## Lens results

```text
[R764] MINOR Conformance — scripts/test_suite_cancellation.py:441-452, scripts/run_all_suites.sh:288-292 — R764-9-F1: the PR's owner_report control fails the preflight by chance (10/5760), against #833 acceptance 2
[R764] PASS RTL — scripts/owned_process.py:256-339 (byte-identical since 5b6d38a3; git diff --quiet) and the delta's stat (scripts and docs only, no hdl/) — the cleanup state machine, its clocks and the transitions every guide row names, checked by 99 reviewer mutants over all 35 listings; no interface or contract change
[R764] MINOR Robustness — scripts/test_suite_cancellation.py:441-452 — R764-9-F1: the control's red depends on host load (2/1280 at about 5, 8/3200 at about 40); robustness of the cleanup itself is unchanged and probed by the sweep
[R764] MINOR Tests — scripts/test_suite_cancellation.py:441-452 — R764-9-F1. The round 9 test delta itself (:741-860, process_test_support.py:263-275, 763-886) is clean: 13 byte-identical reviewer mutants red, 10 edge mutants each red on its own listing alone, and no in-domain survivor among 99 reviewer mutants
[R764] PASS Docs — docs/testing/TESTING.md:255-302, PR body "Round 9", READY post — the liveness table and the domain notes of rows 2 to 8 checked against stated_liveness and the per-listing map; the RESIDUE fixes applied; no comment-rule residue in the delta; the owner_report race is disclosed accurately
```

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R764-9-F1) | Issue #833 acceptance; round 9 ruling; `TESTING.md:255-302`; `test_suite_cancellation.py:435-470, 741-860`; `run_all_suites.sh:268-292`; `owned_process.py:256-339` | R764-9 | e803d94b3a11921a293cf036a8eda333d23828f9 |
| RTL | CLEAN | `owned_process.py:256-339`, byte-identical since round 8; delta stat with no HDL; the 99-mutant sweep | R764-9 | e803d94b3a11921a293cf036a8eda333d23828f9 |
| Robustness | UNCLEAN (R764-9-F1) | `owner_report` repeats: 5760 at the head and 4480 with the fix; the other nine controls, 192 each; sweep families C to G over pass classes | R764-9 | e803d94b3a11921a293cf036a8eda333d23828f9 |
| Tests | UNCLEAN (R764-9-F1) | `test_suite_cancellation.py:741-860`; `process_test_support.py:263-275, 763-886`; author campaign; per-listing map of all 142 mutants; reviewer sweep; byte match | R764-9 | e803d94b3a11921a293cf036a8eda333d23828f9 |
| Docs | CLEAN | `TESTING.md:255-325`; PR body Round 9; READY post; delta comments and docstrings | R764-9 | e803d94b3a11921a293cf036a8eda333d23828f9 |

## Evidence checked

- **Signed packet.** Commit `ce4b2da6` is not signed with a GPG signature; GitHub reports `unsigned`. Its integrity record is `MANIFEST.json`, with 7923 entries. 12 of 12 sampled round 9 receipts match `published_sha256` (`receipts/packet-hash-check.log`). The sample covers:
  - `docsyml-verify.rc` = 0 and the docs.yml table;
  - matrix parts 1 to 4, rc 0;
  - `r8-mutants`, rc 0;
  - `cost.txt`;
  - `ready.md`;
  - `PR-BODY.md`, which equals the live PR body apart from the trailing newline.
- **Own runs at this head:**
  - the whole test: rc 0, `suite cancellation: PASS` (`receipts/whole-head.log`);
  - `--mutants`: PASS, 142 mutants with 139 controls, in 38 s at 16 jobs.
- **Hosted contexts at this head, read-only.**
  - Executed and passed: `changes`, `full-ci-gate`, `docs-gates-0/1/2`, `elaborate-gates-0`, `bdd-conformance`, `firmware-aecp-mutants`, and Verilator shards 13 and 15 among others.
  - Still queued or in progress: most Verilator shards, `docs-check`, the firmware jobs, `verilator-lint`, the Yosys jobs and `publication-census`.
  - Skipped: `Physical gPTP`.
  - The manager owns hosted and act acceptance. I infer nothing from contexts that are still pending.
- **Restored state.** The clone was never edited. All probes ran on copies under the packet's `scratch/`. HEAD and tree are exact. The index and worktree match HEAD, `git status` is empty, and the six submodule gitlinks are unchanged (`receipts/restore-check.log`).

## Real limits

- No manager source bank ran at this head. I claim none.
- I ran no full parent, PP, gPTP, Yosys or builder bank, and no docs.yml replay. The source-head gates are the author's published receipts, which I spot-checked by hash.
- Physical calibration was NOT RUN, and the field skips are not hardware proof.
- The sweep's mutants work at class granularity: the thresholds are 0.25 s and 1.75 s, half a tick, and 13.75 s. They are a reviewer sample, not an exhaustive proof.
- The equivalence claims for the 6 equivalent mutants rest on reading the code at the cited lines.
- The load figures are from a shared 16-CPU host whose load moved from 5 to 50 during the runs.
- The F1 rate is a measurement, not a bound.
- The receipts in `receipts/owner-report-*/red.*` and the sweep JSON contain this host's scratch paths. The manager may redact them.

## Pending manager duties

- **Rule on R764-9-F1.** Its exact fix is above, and the PR will need a new head and re-review of the Tests lens there.
- **Validate the current-dev merge candidate**: source base `1f29f189`, live dev `e61a4afaa54a598ceec08b7b5879285256cc60b6`. That covers the builder and native banks, and the hosted and act acceptance at the final head.
- **Carry SUGGESTIONS S1 and S2**, and the retained R764-6-S1, at the manager's discretion. There is no RESIDUE for the checklist this round.

R764-9 FINISHED
