[R837] NEGATIVE - exact head 9606b3a915de284c71d3063c2e8d94b097f18241

R837-6: the internal, cleared-context delta review of PR #902 (issue #894, Mark II split tier rows), round 11. The delta runs from `7398ec0a`, which R837-5 and R838-5 both reviewed POSITIVE, to `9606b3a9`: ten one-line commits by the author over 17 files, tree `29bfeabee4a8a4e2b61dfa06c137b1588d3d7d8c`.

## Verdict

- **NEGATIVE, on one MINOR finding: R837-6-F1.** The 1x1/1if survey of every stated table ran over arm A alone. The final pass's one held 1x1/1if leg outside arm A was not surveyed by the rule. That is H-L1N, the answering-every-port arm's `notice-every-0`. The head's own 1x1/1if table names that arm in its scope, and its 8x8/2if counterpart (H-L8N) forced a restatement this round. F1 leaves Conformance, RTL, Tests and Docs unclean.
- **The rest of round 11 holds at this head.**
  - The cut keeps behaviour: all 37 map-edit campaign rows are caught, my three behavioural plants are caught, and the unchanged definition test passes.
  - The class split matches the amendment.
  - Every restatement is at or above its measurement by the rule.
  - Every 1x1/1if row is within its bound by every source.
  - The identity proof supports the carry.
- **Residue and suggestions:** 3 RESIDUE items (two new, one carried) and 2 SUGGESTIONs. None of them affects the verdict.

## Method and scope

- **Read first, before any prior review:** AGENTS.md; the round-11 assignment (#894 `6878230332`) and its amendment (`6878532871`); the AECP check (`6876349104`); the measurement (`6878200592`); the direct-index ruling (`6870437042`); the stated-table rule (`6881287231`); REVIEW READY (`6883768027`). Then the full delta diff and its per-commit file lists (`receipts/packet/delta-files-per-commit.txt`), then the author packet at archive `f3320c19`, `review-evidence/894-r1/author-r11`.
- **Read only after my own pass:** the round-10 reviews on the PR, R838-5 (`6874731724`) and R837-5 (`6874821615`).
- **Not read:** private author material, lane scratchpads and other reviewers' reports for this round.
- **My own execution, all at the exact head in this clone**, restored afterwards (see Real limits):
  - the AECP map-edit campaign rows and reviewer plants;
  - an unplanted baseline of the AECP Core and Mailbox suites;
  - the graders' checks and self-tests;
  - the author's what-if script.

## Evidence verification

- **Packet integrity** (`receipts/packet/index-verify.txt`): 420 of the 424 `INDEX.md` rows match. The 4 that differ are `HANDOFF-r11.md`, `scripts/final_receipts.sh`, `scripts/index.py` and `scripts/sanitize.py`, each rewritten by the host-path sanitizer after indexing. Every measurement receipt matches. See S1.
- **Grader outputs** (`receipts/model/`), each byte-identical to the author's final receipt:

| Check | Result at the head |
|---|---|
| `flip_grade.py --check --point 1x1/1if` | rc 0, RESULT: PASS |
| `flip_grade.py --check --point 8x8/2if` | rc 1, the reported point, as before |
| `load_grade.py --check` | 0.515 / 0.511 at 1x1/1if, PASS |
| `tier_grid.py --point 1x1/1if` | chooses slice 900, aecp-first, srp-first, queue, cap 2 (18 of 420 hold) |
| the author's `whatif.py` | the same rows as the author's receipt |

- **Self-tests:** flip 585/585, load 25/25, rows_tiers 1032/1032 (which includes `edit_rows`' unpaced-edit control) and record_classes 6/6. Each refused every planted control.
- **Firmware** (`receipts/maprows/`, `receipts/maprows2/`, `receipts/baseline/`):
  - The full 286-row AECP table passes its own drift check at the head.
  - All 37 rows of `aecp_map_mutants.ROWS` are caught by name, the 12 new ones included.
  - The unplanted app arm passes 87 tests, among them `Core.MapEditsAreTheirDefinitionRowForRow` (unchanged by the delta), `Core.MapCommandsEchoTheirDescriptorAndPage` and `Core.OutputMappingsHaveOneGlobalOwner`. The work arm passes 2, including `Core.MapEditWorkReadsOnlyWhatItCleared`.
- **The author's 286-of-286 campaign** ran at `6ec12ad7` (`wf/6ec12ad7/step-rcs.txt`, `firmware-aecp-mutants` step 9 rc 0). That is after the last `aecp_maps.c` change (`3e0ca737`). firmware-unit is rc 0 at `2d579e89`, with `fw_coverage --check` PASS.

## Checks against the assignment

### (1) The cut (`bc971054`, then `3e0ca737`, which only re-lays declarations)

- **I read `aecp_maps.c:178-504` against the pre-cut code. Behaviour is preserved:**
  - **Clearing:** `memset(e.slot, 0, MAP_DOMAIN)` covers every index `place()` can return below `MAP_SLOTS` (first × `MAP_CHANNELS` + channel < `MAP_DOMAIN`). Each mapping's `next`, `flags` and `copies` are cleared at its turn.
  - **No uncleared read:** the table ends at `steps`, and every chain reaches only entries below `steps`. The add loop reads up to `count`, but runs only when `steps == count`, because any early break is refused in the check loop first.
  - **The reach:**
    - The FOUND pass records the first and last rows equal to a held mapping. Rows outside that reach equal none, so the REMOVE pass would keep them anyway. The rows before the reach stay in place and the tail is moved down.
    - `e->from`/`e->to` are written only when `match == FOUND`. The BARRED pass over other output ports' maps always runs from 0 to `count`.
  - **Refusals:** every refusal keeps its status and order. Range and geometry come before the slot, BAD_ARGUMENTS before NO_RESOURCES, and the lock and length checks before the pace stamp, all as before.
  - **Byte order:** the composed words match the `union held` layout under the new little-endian `#error` guard.
  - The direct index and the 2(n+R) bound are untouched. The new `stale()` exists only under `AECP_MAP_WORK`.
- **Reviewer plants** (`scripts/run_rows.py`, `scripts/run_rows2.py`):

| Plant | Result |
|---|---|
| The foreign BARRED pass ending at the own reach | caught by `Core.OutputMappingsHaveOneGlobalOwner` |
| The foreign pass starting at the own reach | caught by the definition test |
| The reach overwritten by a foreign pass (`match != 0`) | caught by the definition test |
| Two semantics-neutral controls (reach from 0; reach to `count`) | pass, as expected |

  The foreign-start plant also passes the owner test alone: that test's own map is empty, so the reach starts at 0 there. The definition test is what holds it.
- **Cycles:** REMOVE 22,728 (`armA/records-A.txt:4`); ADD 20,595 (`cut/spans-by-variant.txt:298`, exp7, the `bc971054` image per `images/identity.txt`).

### (2) The class split

- **`edit_rows.py` matches the amendment:**
  - `min(k, ceil((w+1)/P))` edits per window, through `paced_rows.edits`; unpaced, all k.
  - Each edit is charged at `EDIT_RECORD_US`: 260 us at 1x1/1if, from 24,360 cycles (255.8 by the rule, so 260); 325 us at 8x8/2if, from 30,563 (320.9, so 325). Every other record is charged at `record.aecp`.
- **`LONG_ROWS` are untouched:** `rows_tiers.py:465` passes `None` for `LONG_ROWS`, so R4L and txL take no edit term.
- **The term is a source:** the `tier1_records` restructuring (`tier1_rows.py:191-220`) keeps the sum of each row's AECP and other records, and `edits` joins `SOURCES['records']`.
- **The planted control:** an unpaced edit charged at the non-edit record is refused by name, and must shorten a held row.
- **`record_classes.py`:**
  - Its 6 controls are refused.
  - It refuses a pass with no 1x1/1if arm A leg, or one missing a group.
  - A group log with no RESULT is dropped and then refused as missing.
  - The author's run over every leg gives RESULT PASS (`classes/record-classes-9606b3a9.txt`). The held dearest records are: edit 24,360 (260/260), other 21,908 (235/235), long 86,978 (915/975) at 1x1/1if, and 30,563 (325/325), 23,715 (250/265) and 145,770 (1,535/1,650) at 8x8/2if.
- **Pacing in the spans:** in `arm-b/spans-aecp-fanout.txt` the edits are followed by their next records 7.78 and 8.12 ms later, over the 7 ms window.

### (3) The restatements, by the rule (cycles / 100 × 1.05, rounded up to 5 us)

| Restatement | Measured | By the rule | Stated |
|---|---|---|---|
| TICK at 1x1/1if | 4,617 (48.5) | 50 | 50 |
| ACMP owed frame at 1x1/1if | 4,890 (51.3) | 55 | 55 |
| `CTRL_LOOP_TX_MS` at 1x1/1if | tx row 33.01 ms | | 34 ms (the row rounded up, ≤ 49) |
| A pass's events' fixed part at 8x8/2if | 2,859 (30.02) | 35 | 35 |
| ACMP owed frame at 8x8/2if | 6,193 (65.03) | 70 | 70 |

- **The survey at 8x8/2if** (`armA/compare-8x8-at-final-statements.txt`): within, apart from `build_one` 146,376 (#910's build of one, named, as before) and `item.aecp.notice` 61,637, which is the largest legal notice, held instead to `LONG_NOTICE_US` 655 (650 by the rule).
- **The survey at 1x1/1if** (`armA/compare-A-at-6ec12ad7-statements.txt`): within over arm A, apart from the two class lines. **It reads no 1x1/1if leg outside arm A: R837-6-F1.**

### (4) The 1x1/1if rows (`flip_grade.py --check` at the head)

| Row | W, ms | Bound, ms |
|---|---:|---:|
| R4 | 12.93 | 20 |
| R4L | 188.41 | 238 |
| ACMP | 28.64 | 30 |
| ADP | 27.01 | 30 |
| MAAP | 27.13 | 30 |
| first queued notice | 14.56 | 20 |
| R5 | 73.39 | 90 |
| R6 | 69.24 | 90 |
| last queued notice | 127.22 | 130 |
| tx | 33.01 | 49 |
| txL | 48.23 | 49 |

- **Load:** 0.515 and 0.511, against 0.70.
- **Joins:** 186.492 to 190.044 ms over every published leg, within 181 to 239.
- **Pace:** 8 ms.
- **Slice rule:** the grid chooses the built design.

### (5) The carry by identity

- **Commits after `9fda93a1`** (`receipts/packet/delta-files-per-commit.txt`):
  - Only two touch a compiled file: `3e0ca737` (`aecp_maps.c`) and `6ec12ad7` (`ctrl_loop.h`).
  - `images/identity.txt` and its three 332-line lists show 0 of 332 files differing between `9fda93a1`, `3e0ca737` and `6ec12ad7`. The lists cover all eight fixture and platform images, every object, ELF and binary. A one-constant control differs in 24 files.
  - Nothing after `6ec12ad7` touches a compiled file: `9106a980` changes `flip_grade.py`, `2d579e89` a README, `9606b3a9` graders and docs.
  - The delta touches no RTL.
  - **The identity supports carrying the sweep and RTL jobs from `9fda93a1`.** Everything else was re-run at later heads: firmware-unit at `2d579e89`, the campaigns at `6ec12ad7`, the docs jobs and graders at the head.
- **Between `bc971054` and `9fda93a1`,** only `tb/` graders, READMEs and docs changed. So the harness image (`ctrl_app.elf` `df8dec1a`) is the head's image.

### KNOWN, sent to a decision

The answering-ports arm's SET_CONFIGURATION is 33,724 cycles at 1x1/1if (355 us by the rule) and 78,332 at 8x8/2if (825). It is reported by `record_classes.py` and not held. The PR states this correctly (`SPLIT_CONTROL_MEMORY.md:2478`, REVIEW READY open risks, and the what-if row "non-edit 355"). It is not a finding.

## Findings

### R837-6-F1 - MINOR - Conformance, RTL, Tests, Docs - the 1x1/1if stated-table survey omits the held answering-every-port leg

- **Artifacts:**
  - author-r11 `receipts/final/armA/compare-A-at-6ec12ad7-statements.txt` and `compare-A-at-9fda93a1-statements.txt`: every line reads an `A/` leg (214 and 216 lines);
  - `HANDOFF-r11.md:162`, "compare (1x1 arm A, 8x8 legs)";
  - REVIEW READY: "Every stated table by the rule, at both points ... Within at 1x1/1if but for the two class lines";
  - `receipts/packet/survey-scope.txt` (mine) collects these.
- **Authority:**
  - #894 `6881287231` requires every stated table the rows read to be checked against this head's measurements by the rule.
  - The head's 1x1/1if table states its own scope as "every group of arm A and of the answering-every-port arm ... each cost the larger of that and this table's" (`tb/verilator/ctrl_service_budget/load_grade.py:106-121`).
  - `record_classes.py:16-19` holds the answering-every-port arm as formal measurement.
- **Evidence:**
  - H-L1N (`--variant answering-every-port --groups notice-every-0`, 1x1/1if, on `bc971054`'s firmware, rc 0) is part of round 11's final pass. Its costs were compared by the rule only for AECP records, through `record_classes`. There, its SET_NAME of 21,908 cycles is the 1x1/1if dearest ordinary record, at exactly 235 of 235.
  - The same arm's group at 8x8/2if, H-L8N, gave this round's events' fixed part of 2,859 cycles and forced 30 to 35 us there.
  - At 1x1/1if no measurement of that group's polls' base, events' fixed part, TICK, step pass or owed frames is compared with any table. The cut moved costs by layout alone (`SPLIT_CONTROL_MEMORY.md:2473`).
  - The harness holds per-pass costs raw, not by the rule. Its rc 0 therefore cannot show that a statement is at or above its measurement + 5 %.
- **Impact:** a 1x1/1if statement below its measurement by the rule can stand unseen. The polls' base is the slice rule's input: R835-3-F1 found 20,456 cycles, 215 by the rule, taking the slice to 950 against the built 900. So the rows, the load, the pace and the slice choice at 1x1/1if are verified only against arm A's figures.
- **Required outcome:** one of these two.
  - Publish the stated-table comparison over H-L1N's measurements at the head's statements: both `load_grade` columns, `poll_grade.STATED_US[1]`, `whole_grade.stated_us(1)`, `rows_grade.ROW_COSTS`, `rows_tiers.DATAPATH_US`, `LONG_NOTICE_US` and `LONG_RECORD_US`. Restate anything over by the rule, recompute every row and the pace, and rerun the slice rule.
  - Or obtain a public decision that the 1x1/1if statements' scope is arm A alone, and correct the table's scope comment and the PR's claim to match.
- **Verification:** a published compare receipt that reads H-L1N, with 0 lines over (apart from the class lines), or restatements with refreshed `flip_grade --check`, `load_grade --check` and `tier_grid` receipts. A reviewer checks the receipt's leg prefixes, as here.

### R837-6-R1 - RESIDUE - Docs - review rounds and a lane name in new source comments (owner comment rule; #746 tracks the earlier instances)

- **Instances:**
  - `tb/verilator/ctrl_service_budget/edit_rows.py:3`, "#894's round-11 amendment";
  - `edit_rows.py:29`, "under the cut of #894's round 11";
  - `load_grade.py:126`, "on #894's round 11";
  - `load_grade.py:130`, "2,093 at round 9's head";
  - `poll_grade.py:86`, "On #894's round 11";
  - `poll_grade.py:89`, "(6,239 at round 9's head)";
  - `record_classes.py:4-5`, "(#894's round 11: ... which no pass had run since round 4)";
  - `record_classes.py:72`, "(lane 894b's, reported)".
- **Exact fix:** name the issue, ruling or commit instead. Use "#894's class-split decision of 2026-11-14" for the amendment, "under #894's one-row edit cut (`bc971054`)" for the cut, and "at `<commit>`" in place of "round 9's head" or "since round 4". Make the docstring "8x8/1if (#894's follow-up point, reported)".
- **Optional, docs and not source:** the same wording in `sw/firmware/gtest/README.md:319`, "(#894's round 11)".
- No figure, test or behaviour changes.

### R837-6-R2 - RESIDUE - Docs - "adds 220 B of rom to every image"

- **Artifact:** `docs/design/SPLIT_CONTROL_MEMORY.md:2479`.
- **Evidence:** section 13's own figures give the 1x1/1if size fixture 110,576 B before the cut and 110,800 after, which is +224 B. Earlier rounds reconciled `.text` against rom growth by alignment (R838-3-F3).
- **Exact fix:** "The cut adds 220 B of code to every image (224 B of rom in the 1x1/1if size fixture, by alignment)", or the per-image rom deltas measured.
- Every stated total stays as written.

### R837-5-R1 - RESIDUE (carried, unfixed at this head) - Docs

- **Artifact:** `SPLIT_CONTROL_MEMORY.md:2493` (line 2479 at `7398ec0a`) still reads "**The margins at this head** (round 30's legs, ...".
- **Exact fix:** unchanged from R837-5: "**The margins at round 30's legs** (".

### R837-6-S1 - SUGGESTION - Docs - packet INDEX generated before sanitizing

- **Artifact:** author-r11 `INDEX.md`, rows `HANDOFF-r11.md`, `scripts/final_receipts.sh`, `scripts/index.py` and `scripts/sanitize.py` (`receipts/packet/index-verify.txt`).
- **Evidence:** the 4 rows' bytes and hashes do not match the files. `sanitize.py`'s own substitutions show the files were rewritten after indexing. This is the same pattern as R837-5-S1 / R838-5-S7, now in four files. No measurement receipt is affected.
- **Suggested outcome:** sanitize, then index, and fail the indexer on a mismatch.

### R837-6-S2 - SUGGESTION - Tests, Robustness - `record_classes.py` names a record by the next response after its start

- **Artifact:** `tb/verilator/ctrl_service_budget/record_classes.py:102-107`.
- **Evidence:** a record that commits no solicited response takes the command of a later record's response. If that response is an edit's and the next record is more than 7 ms away, an ordinary record would be held to 260 rather than 235. Nothing in the published spans shows this happening.
- **Suggested outcome:** take a response only within the record's own span (start to start + cycles, on the bus clock), else "unanswered". Add a synthetic control.

## Prior public findings at this head

- **Round 10 left no open MINOR or above.** R838-5 and R837-5 resolved every round-4 MINOR and earlier residue.
- **R837-5-R1:** carried above, unfixed.
- **R837-5-S1:** recurs as R837-6-S1.
- **R837-5-S2:** the compile-time row runs at one geometry. It is retained, since `aecp_map_mutants.py`'s build rows are unchanged.
- **R838-5-S1 to S15:** retained as optional. The delta does not touch the code they name, with one exception.
  - **R838-5-S14 (`struct edit`'s frame):** the cut adds two `size_t` fields, 8 B on RV32. The suggestion's integration limit and call-chain measurement stay advisable.
  - **R838-5-S11 (`place()`'s first-coordinate guard):** `place()` is unchanged.
- **Every earlier retained resolution** that R838-5 lists still holds: the direct index, the range guards, the 49/238 bounds, the pace rule and the image reconciliation. The delta changes none of the code they rest on, and the campaign and definition tests pass.

## Lens results

| Lens | Result | Evidence |
|---|---|---|
| Conformance | UNCLEAN (F1) | The class split, the restatements and the rows match the amendment and the rule (items 2 to 4). The 1x1/1if survey's scope does not meet `6881287231`. |
| RTL | UNCLEAN (F1) | `aecp_maps.c:178-504`: the cut is behaviour-preserving, with clearing, reach, refusal order and the byte-order guard all as above. The cut's timing effect is not shown for the held 1x1/1if answering-every-port leg. |
| Robustness | CLEAN | `aecp_maps.c:359-504`: truncated length, count over page, out-of-domain keys, stale-table reads under `stale()`, an empty map, a REMOVE with no match, repeated rows and the foreign pass's full range. All are held by the campaign rows and my plants. `record_classes` handles a missing arm, a missing group and a truncated log. |
| Tests | UNCLEAN (F1) | The 12 new rows and my plants are caught, the tests pass unplanted and the definition test is unchanged. The stated-table validation is incomplete at 1x1/1if. |
| Docs | UNCLEAN (F1; R1, R2 and R837-5-R1 are residue) | `SPLIT_CONTROL_MEMORY.md:2470-2479`, FR_NFR 3.4.1, the harness, AECP and SRP READMEs and `ctrl_loop.h:360-366` match the tools. The PR and REVIEW READY overstate the 1x1/1if survey. |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | assignment and amendment; `edit_rows.py`; `tier1_rows.py:134-220`; `rows_tiers.py:465`; `load_grade.py:106-185`; `poll_grade.py:83-93`; `ctrl_loop.h:360-366`; flip, load and tier_grid receipts; compare-A and compare-8x8 | R837-6 (F1 open) | 9606b3a915de284c71d3063c2e8d94b097f18241 |
| RTL | UNCLEAN | `aecp_maps.c:150-504` diff and full read; `images/identity.txt` and the three 332-line lists; per-commit file lists | R837-6 (F1 open) | 9606b3a915de284c71d3063c2e8d94b097f18241 |
| Robustness | CLEAN | `aecp_maps.c:359-504`; `record_classes.py:87-162`; `receipts/maprows*/`; `receipts/baseline/` | R837-6 | 9606b3a915de284c71d3063c2e8d94b097f18241 |
| Tests | UNCLEAN | `test_aecp.cpp:2330-2342,2802-2841`; `aecp_map_mutants.py:107-160`; 37 rows plus 6 reviewer plants; baseline 87+2; self-tests 585, 25, 1032 and 6 | R837-6 (F1 open) | 9606b3a915de284c71d3063c2e8d94b097f18241 |
| Docs | UNCLEAN | `SPLIT_CONTROL_MEMORY.md:2351,2470-2493`; `FR_NFR.md` 3.4.1 diff; `ctrl_service_budget/README.md`; `aecp/README.md`; `srp/README.md:238`; `gtest/README.md:319`; REVIEW READY; packet INDEX | R837-6 (F1 open) | 9606b3a915de284c71d3063c2e8d94b097f18241 |

## Real limits

- **No harness leg was run by me.** F1 rests on the published receipts' scope. I could not survey H-L1N myself: its log is not published, and the cost parsers the survey uses are not in the tree or the packet.
- **Not run by me:** the full 286-row campaign (only its 37 map rows), the control and SRP campaigns, the docs jobs, the Verilator and Yosys banks, and any hardware.
- **Physical calibration is NOT RUN,** and field skips are not hardware proof. Hosted CI does not run on split PRs, so source-head execution evidence is the author's published local receipts plus mine. No manager source bank exists at this head, and none is claimed.
- **Clone state:** the clone was restored and verified afterwards (`receipts/state/clone-after.txt`). HEAD is `9606b3a9`, with tree `29bfeabe`. The index and tree blob and mode digests are equal, with 0 status entries including ignored files. All six gitlinks are at their recorded commits, and the five initialised submodules are clean. I removed the bytecode caches my runs created.

## Pending manager duties

- Route F1 to the author: either publish the H-L1N survey with any restatement, or record a scope decision.
- Carry R837-6-R1, R837-6-R2 and R837-5-R1 to the residue checklist.
- **Owner decision:** the answering-ports SET_CONFIGURATION (KNOWN).
- **Open duties outside this PR:** #910 (8x8/2if build of one) and #872 (8x8/2if rows); #908, #909 and the 8x8/1if follow-up, as before.
- **At the merge turn:** the current-dev candidate (source base `66f71326`, live dev `b7d69295`), with builder and native banks and post-merge containment, and hosted or replica acceptance.
- Publish this report and the files listed in `MANIFEST.sha256`.

R837-6 FINISHED
