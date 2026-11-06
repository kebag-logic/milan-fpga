[R787] POSITIVE - exact head 171fd56b2c50a44ed75a32c1b9bbd7ae818f2c22

Round R787-3, issue #848, PR #849. Tree `9d8daa835aa16f477d3af405fa2bb1b1ec0d5883`, live dev `3f6bef88bd8a78cb2833a12572b9c4a9013f9bdf`, previously reviewed head `91c115b576601139c53038440f0987412d5172e8`.

## Verdict

Both items of the round 3 ruling (issuecomment-6694897633) are met at their cause. No BLOCKER, MAJOR or MINOR is open, so every lens is clean at this head.

**One required gate is still unproved: `gate_25_0`.** This verdict does not count it as passed. It rests on the act replay the assignment names, which I have not seen, so it stays a manager duty (see "`gate_25_0`" below).

| ID | Severity | Lenses | Title |
|---|---|---|---|
| R787-3-S1 | SUGGESTION | Tests | The archive copy's lane needle is not anchored, so an archive-only misfile passes the selftest |
| R787-3-S2 | SUGGESTION | Tests | A lane needle has no end anchor, and lane file names are not pinned |
| R787-3-S3 | SUGGESTION | Tests | The audience line's use of the window has no edge control |
| R787-3-S4 | SUGGESTION | Tests | The rejoined opening lines leave mixed indentation |
| R787-3-R1 | RESIDUE | Docs | The PR body's lane sentence reads wider than the control |
| R787-3-R2 | RESIDUE | Docs | `W8` means two different mutants in the PR body |

**S1 is the one judgement call, and the manager may want to read it.** Taken literally, the ruling's sentence is broken by that one mutant. I rate it SUGGESTION for the reasons given under S1. If it were promoted to MINOR, `Tests` would be unclean and this verdict would become NEGATIVE.

## The ruling, item by item

**Lane control: met.** A control fails when an entry leaves its page's lane or when lanes merge into one file.

| Named mutant | Source | `91c115b5` | This head |
|---|---|---|---|
| W8, every lane in one file | R788-2 | survived | killed |
| W9, copy filed in its origin's lane | R788-2 | survived | killed |
| W11, every finding under one lane | R787-2 | survived | killed |
| W12, copy filed under its origin's lane | R787-2 | survived | killed |

R787's own `W08` and `W09` (only the first or last lane written) are killed too, so the ruling's list holds under either numbering.

My own campaign agrees. All 4 merge mutants (LM1-LM4) are killed, including one file that keeps each lane's titled section. So are 7 of the 9 misfile mutants (LF1-LF7), both dropped-lane mutants and both title mutants. At `91c115b5` the 7 misfile mutants and LM1-LM3 survive, which shows the campaign is live (`receipts/own-mutants-prior-91c115b5.txt`).

**Banner window: met.** A banner on line 15 is read and one on line 16 is not.

- The two arms put their banner on lines 15 and 16, measured on the fixture rather than derived (`receipts/delta-checks.txt`). They are `scripts/docs_inventory.py:945` and `:947`.
- `status()` directly gives `superseded` for lines 1, 14 and 15, and `current` for 16 and 17.
- On a real page, `docs/AAF_LATENCY_TAPS.md`, a banner inserted on line 15 gives `--check` rc 1, and on line 16 gives rc 0 (`receipts/real-tree-probe.txt`).
- N14, N16, N19 and B01-B03 are killed. So are my windows of 12, 14, 16, 17, 19 and 1000, and the slice mutants on `:438` alone (BH14, BH16, BO).

**Module limit, ratchet, digest: met.**

- `scripts/docs_inventory.py` is 1000 lines, none over 120 columns.
- `long module` reads 10 <= 10, and `scripts/py_idiom.budget` is unchanged.
- The file's sha256 is `092505ae2b979e6bd599028051c72e861fd1081a5ff70186de4d3c05953d8754`, which appears once in `ci/image/command-table.json`.
- The old digest appears nowhere in the tree.

**Merge of dev `3f6bef88`: correct.**

- `d8a6cfb3` has parents `91c115b5` and `3f6bef88`.
- Replaying the merge in a disposable clone reports exactly one conflict, `docs/DOCUMENTATION_AUDIT.md` (`receipts/merge-replay.txt`).
- Dev to head differs in only this PR's four files, with no change under `hdl`, `tb` or `syn` and no gitlink change.
- The audit page is byte-identical to `91c115b5` and `--check` gives rc 0, so a real dev merge that moved page lengths left the page fresh. That is #848's acceptance on real data.

**The delta changes what it says.** Top-level syntax differs only in `control`, `copy_controls` and `selftest`. The other 99 names are identical: 81 definitions and assignments, plus 18 import names. The layout-free diff shows only the intended changes, and no needle was weakened: the two removed `## D0-002` needles are subsumed by the stronger anchored ones (`receipts/delta-checks.txt`).

## Prior findings, at their cause

Read after my own pass over the diff. Both published campaigns were replayed at this head, using the author's copies. I diffed those against the originals: only the grader string differs.

| Prior finding | State | Evidence at this head |
|---|---|---|
| R787-2-F1 = R788-2 F1, lane control | RESOLVED | `:762` marks each file's start, `:764` grades NUL needles on lane text only, and `:854-858` anchor each lane's title, baselines and own entries. W8, W9, W11 and W12 are killed. |
| R787-2-F2 = R788-2 F2, banner window | RESOLVED | See the banner item above. |
| R787-2-S1 = R788-2 S5, Evidence cell moves | RETAINED SUGGESTION | Product code unchanged, disclosed in the PR body. |
| R787-2-S2 = R788-2 S1, route needles | RETAINED SUGGESTION | P04-P07, L07 and T4 survive. Left out by the ruling. |
| R787-2-S3 | RETAINED IN PART | W13, W14, W15, W18 and W19 are killed. W20 survives (also my LR1). |
| R788-2 S3 | RESOLVED | W13, W15, W16 and W17 are killed. |
| R788-2 S2, swapped baselines | RETAINED SUGGESTION | B1 survives. The page's baselines are unpinned, though the lane files' are now pinned (my LB1 is killed). |
| R787-2-S4 = R788-2 S4, reused `DIR` | RETAINED SUGGESTION | `write_findings` unchanged. |
| R788-2 R1, R2 | RESOLVED | R1 is true now that F2 is fixed. The PR body carries R2's exact wording. |
| S9 / C03, equivalent | ANSWERED | Survives, as expected, and unchanged. |

Campaign totals match the author's: R787's 62 give 52 killed and 10 survivors, and R788's 60 give 54 killed and 6 survivors. The survivors are exactly the ones named in the REVIEW READY comment (`receipts/r787-2-campaign-head.txt`, `receipts/r788-2-campaign-head.tsv`).

## `gate_25_0`

I read the HANDOFF, the attempt receipt, the log and the rc file.

- The step gave rc 124 at the author's 585 s limit. The log holds only its header and two pip notices, with no verdict. So this is a time limit, not a gate failure, and it is not proof either.
- `scripts/ci_builder_legs.py:30` records 945.182 s for this gate, which supports the author's account.
- Nothing under `sw/builder` names any of the four changed files. This is a text search, not a trace of what the gate reads, and the author says the same.
- I saw no act replay receipt. Hosted `docs-gates-1` was still queued at 2026-11-06T21:48:03Z.

## Findings

No finding here is BLOCKER, MAJOR or MINOR.

### R787-3-S1 - SUGGESTION - Tests

**Title:** The archive copy's lane needle is not anchored, so an archive-only misfile passes the selftest.

**Where:** `scripts/docs_inventory.py:876`, with the filing at `:620`.

**Evidence:** The needle `"## D0-001: docs/history/v1/OLD.md:8\n"` is graded on all lane text joined. Mutant LF8 files archive entries in `overview and guides` and survives. On the real tree it moves 9 of 76 entries, the `archive` lane file disappears, and `--check` stays rc 0 (`receipts/real-tree-probe.txt`). Five other lanes have no fixture finding, so they have no such control either.

**Why SUGGESTION and not MINOR:**

- The ruling's named mutants are all killed.
- `:620` has no per-lane branch. Every lane-generic mutant I tried is killed, so LF8 needs a special case keyed on one lane.
- R787-2-S3 used the same reasoning to accept sampling across a loop with no branch.
- The natural table form, LF9, is seen by `--check` on the real tree (rc 1, 510 lines differ), so review would see it.

**Impact:** Only a change that special-cases one lane could lose that lane's work list with the selftest green.

**Optional outcome:** Anchor this needle: `f"\0# D0 findings: archive{lead}## D0-001: docs/history/v1/OLD.md:8\n"`.

**Verification:** In a disposable sketch the selftest stays green with 56 controls and LF8 is killed (`receipts/fix-feasibility.txt`). That line reaches 143 columns, so it needs one more line, and the module has no headroom. Any such change also needs a re-pin.

### R787-3-S2 - SUGGESTION - Tests

**Title:** A lane needle has no end anchor, and lane file names are not pinned.

**Where:** `scripts/docs_inventory.py:854-858`, `:622`, `:629`.

**Evidence:** Three mutants that append another lane's entries after a file's own entries survive (LD1-LD3). The natural form, a copy filed in both lanes in `located` order, is killed (LD4, LD5), because it breaks the needle's adjacency. Swapped file names (LN1) and a slug that keeps spaces (LN2) also survive, because the grader reads files by content.

**Impact:** Low. The own entries stay in the right file, so no lane loses work.

**Optional outcome:** End-mark each file as well as start-marking it, and pin one file name.

### R787-3-S3 - SUGGESTION - Tests

**Title:** The audience line's use of the window has no edge control.

**Where:** `scripts/docs_inventory.py:265`.

**Evidence:** `BANNER_SCAN_LINES` also bounds the audience line. Changing the constant is now killed, but changing only that slice is not: AU14, AU16 and a window of three lines (AU3) survive. A window of two is killed. This code is outside the delta and the ruling.

**Impact:** A page's audience could be misread at the edge of the window. `--check` and the review diff would show the change on the committed page.

**Optional outcome:** One arm with an `Audience:` line on line 15, if the module ever has room.

### R787-3-S4 - SUGGESTION - Tests

**Title:** The rejoined opening lines leave mixed indentation.

**Where:** `scripts/docs_inventory.py:852-853`, `:907-908`.

**Evidence:** The first arm's continuation sits at 9 columns and the arms after it at 8. It is layout only and was the price of staying at 1000 lines.

**Optional outcome:** Tidy it when the module is next split or shortened.

### R787-3-R1 - RESIDUE - Docs

**Where:** PR #849 body, "Added controls".

"An entry filed outside its lane, or lanes merged into one file, fails it." reads wider than the control, per S1.

**Exact fix:** "An entry of either lane that arm exercises filed outside it, or lanes merged into one file, fails it."

### R787-3-R2 - RESIDUE - Docs

**Where:** PR #849 body, "Review round 2" table.

`W7` and `W8` there are R787-1's names, while `W8` in the round 3 table is R788-2's name for a different mutant.

**Exact fix:** Label the round 2 rows "R787-1 W7" and "R787-1 W8".

## Other checks

**Real tree** (`receipts/real-tree-probe.txt`): 5 lane files, 76 entries and 0 outside their lane. One line appended to all 212 tracked pages gives `--check` rc 0.

**Gates run directly at this head** (`receipts/independent-gates.txt`, `receipts/hygiene.txt`), all rc 0:

- `docs_inventory.py --check` and `--selftest` (56 controls)
- `check_py_idiom.py` and `check_doc_style.py`
- `docs_check.py`, `check_doc_paths.py` and `check_hygiene.py`
- `ci_gate_workflows.py --check` and `ci_events.py --check`
- `git diff --check` from dev to head

**Author evidence** (`receipts/evidence-check.txt`):

- All 1008 manifest rows match their published digests, including 196 author round 3 rows.
- All 72 `docs.yml` logs name the exact head on their first line.
- The rc files read 71 at 0 and 1 at 124, as the author states.
- 8 tree-after records exist.

**Comment rule:** no new instance. The 14 added lines in `scripts/docs_inventory.py` carry no bench lane label, review round, reviewer ID, comment ID or em dash. "Lane" in that code is the product's own area lane. Both new commits are one line with no trailers.

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #848 acceptance and the ruling against `scripts/docs_inventory.py:136`, `:438`, `:620`, `:762-764`, `:854-858`, `:945-947`, `ci/image/command-table.json`, `receipts/real-tree-probe.txt`, `receipts/merge-replay.txt`. "The docs gates pass" depends on the pending `gate_25_0` duty. | R787-3 | `171fd56b2c50a44ed75a32c1b9bbd7ae818f2c22` |
| RTL | CLEAN | Inapplicable by artifact: `git diff 3f6bef88..171fd56b` names four files, none under `hdl`, `tb` or `syn`, with no gitlink change (`receipts/hygiene.txt`). Dev's own RTL arrives byte-identical through the merge. | R787-3 | `171fd56b2c50a44ed75a32c1b9bbd7ae818f2c22` |
| Robustness | CLEAN | Product code identical to `91c115b5` (`receipts/delta-checks.txt`), so the prior verdict on `:612-631` and `:665-684` stands. Rechecked: banner edges, 212-page append, lane routing and the audit page after a real merge. Retained items are SUGGESTIONs. | R787-3 | `171fd56b2c50a44ed75a32c1b9bbd7ae818f2c22` |
| Tests | CLEAN | `scripts/docs_inventory.py:731-771`, `:843-901`, `:904-972`, `receipts/own-mutants-head.txt` (41 rows), `receipts/own-mutants-prior-91c115b5.txt`, `receipts/r787-2-campaign-head.txt` (62), `receipts/r788-2-campaign-head.tsv` (60), `receipts/delta-checks.txt`. S1-S4 are SUGGESTIONs. | R787-3 | `171fd56b2c50a44ed75a32c1b9bbd7ae818f2c22` |
| Docs | CLEAN | Docstring `scripts/docs_inventory.py:738`, arm names `:945` and `:947`, `.github/ci-templates/docs.yml:423-433`, `docs/DOCUMENTATION_AUDIT.md` (unchanged since `91c115b5`), PR #849 body and `[A739c] REVIEW READY` against these receipts. R1 and R2 are RESIDUE. | R787-3 | `171fd56b2c50a44ed75a32c1b9bbd7ae818f2c22` |

## Real limits

- **`gate_25_0` is not proved** by anything I examined. I did not run it, and I did not run `gate_25_1`.
- **Packet signature:** the evidence commit `9014f7e7` is unsigned, and I found no signature file. I checked digests against `MANIFEST.json`, which shows the files match the manifest but not who produced them.
- **Hosted state:** six checks on this head, all queued, none executed (`receipts/hosted-snapshot.txt`). This is not acceptance evidence.
- **`ci_tool_inventory.py --check` was not run**, because the pinned parser is not available here. I compared the digest directly.
- **Command table, outside this delta:** 36 of 151 rows for tracked files do not match their file's digest. The set is identical on dev, and `scripts/docs_inventory.py` matches on both (`receipts/table-digests.txt`). `scripts/ci_python_walk.py:347` enforces a digest for scripts it finds a capability in. I did not establish whether any of the 36 is enforced, or whether #838 covers them.
- **Mutants are a chosen set.** My 41 rows give 29 killed and 12 survivors: the IDENTITY control, the 2 under S1, the 5 under S2, W20's twin LR1 and the 3 under S3.
- **Real-tree probes** ran in a disposable clone with no submodules initialised, and `--check` gave rc 0 there unmodified.
- **Not run, by assignment:** full banks, Docker or act, the host runner and hardware. No manager source bank exists at this head and I infer none. Physical calibration NOT RUN, and field skips are not hardware proof.
- **Review clone:** at the exact head and tree, with a clean index and worktree. All 1470 tracked blobs and modes verified and all 6 gitlinks present (`receipts/clone-integrity.txt`). Bytecode my gate runs generated was removed afterwards.

## Pending manager duties

- Confirm `gate_25_0` from the act replay and the hosted run on this exact head.
- Rule on S1's severity if the literal reading of the ruling is preferred.
- Carry R787-3-R1 and R787-3-R2 to the residue checklist.
- Decide whether the 36 mismatched table rows need an Issue, or confirm that #838 covers them. The `ci/image/tool-inventory.json` drift also stays with #838.
- Build the current-dev merge candidate and own hosted and act acceptance at the merge turn. Dev was still `3f6bef88` at my last check.
- Publish this report with its receipts.

R787-3 FINISHED
