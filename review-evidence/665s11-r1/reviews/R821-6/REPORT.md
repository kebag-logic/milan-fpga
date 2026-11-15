[R821] NEGATIVE - exact head 33b0d03a4ac899ed1601cd2cd97efbf66e293c9e

# R821-6: internal cleared-context delta review of PR #881 (issue #871, S11 AECP REBOOT), round 6

- **Head:** `33b0d03a4ac899ed1601cd2cd97efbf66e293c9e`, tree `caae1d031c84bb0813647c4901c9565769626d06`. The live PR head equals it; the PR is not a draft; base `dev-soft-core`.
- **Delta:** `d3566d44..33b0d03a`, one commit, seven files (+23/-19).
- **Prior state:** R821-5 NEGATIVE at `d3566d44` on F1 (MINOR), plus RS-1 and RS-2 (RESIDUE). R822-5 POSITIVE at `d3566d44` with three residues.
- **Verdict: NEGATIVE, on one MINOR (F1-R6, Docs).**
  - F1's executable part is resolved. `poll_grade.STATED_US[1]['retained']` is 285, equal to both load columns' `item.retained` and `record.srp`, and the docstring's figures are right.
  - But the design doc's polls row now reads `285 (280)` under a legend that says "Each figure in parentheses was round 22's". Round 22's retained figure was 250. The edit replaced a correct historical figure with a wrong one.
  - The fix is one cell: `285 (250)`.
  - The `285 (280)` text was prescribed by this reviewer's own R821-5 F1 option (a), and the author applied it as written. The error is in that prescription, not in the author's execution.
  - It changes a stated figure, so under the residue rule it is not wording-only.
- **Everything else holds:**
  - RS-1, RS-2 and R822-5's R1 to R3 are applied as written.
  - The `ctrl_plat.h` edit is comment-only.
  - No firmware image input changed.
  - The statement survey finds no conflict.
  - All 11 two-valued figures are the donor column's and are identical at `41ca9f87`.
  - Every rerun gate is rc 0 on a clean clone.
- **Scope:** this verdict and ledger were written from an independent pass over the delta. Prior findings were read only to check their resolution (section "Prior findings").

## Inputs, in order

1. AGENTS.md and CONTRIBUTING.md (review contract, lens and severity rules), docs/README.
2. Issue #871 scope and the manager's ruling on R821-5 (F1 option (a)), as carried by the round-6 review start (PR #881 issuecomment-6901308293) and REVIEW READY (#871 issuecomment-6901282063).
3. Interface authorities for the delta:
   - `tb/verilator/ctrl_service_budget/{poll_grade,load_grade,rows_grade}.py`;
   - `docs/design/SPLIT_CONTROL_MEMORY.md` "The polls by source";
   - `sw/firmware/ctrl/plat/ctrl_plat.c` `quiet()`/`depart()`/`ctrl_plat_step()`;
   - `docs/design/REBOOT_RESET.md` section 8.
4. `git diff d3566d44..33b0d03a` and its history (`git log -S` on the polls row back to round 22's `8684993388`, and `a0c25e5c`).
5. The author packet `review-evidence/665s11-r1/author-r6` at archive `5c2e4ba6`.
   - All 259 files match `MANIFEST.json`'s `published_sha256`, with 6 publisher-redacted or rewritten, 0 missing and 0 unlisted (`receipts/packet-audit.txt`).
   - The archive commit is unsigned (verification false). This shows hash consistency, not an independent signer.
6. Prior public findings: R821-5 (issuecomment-6900325190) and R822-5 (issuecomment-6900286461), read after the independent pass.

## What was executed

Scripts are under `scripts/`, receipts under `receipts/`.

| What | Result | Receipt |
|---|---|---|
| Packet audit (`audit_packet.py`) | 259/259 match, rc 0 | `packet-audit.txt` |
| Clean clone of `33b0d03a` (submodules at their gitlinks) and a worktree at `41ca9f87`; `gates.sh` ran 16 gates concurrently | all rc 0 | `gates/summary.txt` |
| `flip_grade.py --check --point 1x1/1if` | PASS; last queued notice 134.74 of 135 (-0.26), txL 48.75 of 49 | `gates/flip_check_1x1.log` |
| `load_grade.py --check` | PASS; 1x1/1if at the pin 0.520, with tsn-c-stack#32 0.516, ceiling 0.70 | `gates/load_check.log` |
| `load_grade.py --selftest`, `flip_grade.py --selftest` | rc 0, rc 0 | `gates/load_selftest.log`, `gates/flip_selftest.log` |
| `selftest_polls.polls_checks` (the polls gate's checks, which read `poll_grade.STATED_US`) | 33 of 33 | `gates/polls_checks.log` |
| The author's `statement_survey.py` at the head and at `41ca9f87` | head: PASS, 0 conflicts, every derivation holds; the 11 TWO VALUES lines are identical at both heads | `gates/survey_head.log`, `gates/survey_41ca9f87.log` |
| Reviewer `figures_probe.py` (pin vs donor vs polls; the donor-at-or-above-pin rule outside `load_grade.WALK`) at the head and `41ca9f87` | PASS at both; same 10 load/polls pairs; the retained chain is (285 ×5) at the head and (280 ×5) at `41ca9f87` | `gates/figures_*.log` |
| `check_py_idiom.py`, `check_cpp_idiom.py`, `docs_check.py`, `check_doc_paths.py`, `check_doc_style.py`, `git diff --check d3566d44 HEAD` | all rc 0 | `gates/*.log` |
| Non-comment lines changed in `*.c *.h *.cpp *.py` | one: `poll_grade.py` `retained=280` → `285` | `gates/delta_noncomment.log` |
| Fault probe: `retained` planted back to 280 in the clean clone, then restored | survey FAILS (`280 (its source 285)`); `load_grade --check`/`--selftest`, flip check and polls checks all still rc 0 | `probe-retained-280/` |
| History of the polls row | round 22's 1x1/1if retained was 250 (`poll_grade` `retained=250`); `a0c25e5c` wrote `280 (250)`; the head writes `285 (280)` | `f1r6-round22-row.txt` |
| Hosted snapshot at the head (read-only) | 9 success, 1 skipped, 20 in progress, 20 queued. Not a verdict; the manager owns hosted acceptance | `hosted-snapshot.tsv` |

After the probe, the clean clone was restored: `git status --porcelain` is empty and HEAD is `33b0d03a`.

The review clone was not edited. It is at `33b0d03a` / `caae1d03`, its index and work tree are clean, and its gitlinks are unchanged (`gitlinks.txt`):
- gptp-processor `135afd04`;
- protocol-processor `a9e84b66`;
- lwSRP `08ee86e8`;
- tsn-c-stack `715589c1`.

## The assignment's items

### (1) F1: the retained retry at its rule

- **Gate value:** `poll_grade.py:91` `STATED_US[1]['retained'] = 285`.
- **Its rule:** `poll_grade.py:67-71` says the retained retry is "stated at the SRP record's cost".
- **The source the rule reads:** `load_grade.STATED_US['1x1/1if']['record.srp']` and `STATED_US_DONOR['1x1/1if']['record.srp']` are both 285 (`load_grade.py:146,179`). Both columns' `item.retained` are 285 (`:148,182`).
- **8x8/2if** stays 365 throughout.
- **Docstring:** "285 and 365 us; 280 at 1x1/1if before AECP's REBOOT, #871". Correct: every member of the chain is 280 at `41ca9f87` (`figures_41ca9f87.log`).
- **Rows unchanged:** `rows_grade.costs` already charged `max(item.retained, record.srp)` = 285 (`rows_grade.py:157`).
- **Polls gate:** the gate's limit and its `RECORD` limit (`poll_grade.py:246`) rise from 280 to 285, equal to the stated rule.
  - The apply measured 280 by the rule at round 5 (26,363 cycles), so the gate still binds the measurement.
  - The edit is a restatement to the rule, not a loosening to obtain a pass: it passed at 280 too.
- **Gates:** `selftest_polls` 33/33, `flip_grade.py --check --point 1x1/1if` and `load_grade.py --check` rc 0.
- **The design doc's row** is F1-R6 below.

### (2) RS-1, RS-2 and R822-5's residues

- **RS-1:** `test_plat_boot.cpp:187` reads `(ADepartingTheRingRefusedHoldsTheReset)`. That is `TEST_F(Boot, B18ADepartingTheRingRefusedHoldsTheReset)` at `:908`, named descriptively. Resolved.
- **RS-2:** resolved. Each of these reads "aecp_reboot_mutants.py" (the doc rows add "which `aecp_mutants.py` plants"):
  - `REBOOT_RESET.md:315,316`;
  - `test_plat_boot.cpp:76` and `:982` (B20's comment);
  - `plat_mutants.py:265`.

  `aecp_reboot_mutants.ROWS` has 15 rows, matching "fifteen", and `aecp_mutants.py:18,873` plants them. All three named defects are there (`aecp_reboot_mutants.py:65,69,73`).
- **R822-5-R1:** resolved.
  - `(B18)` is gone.
  - The `plat_mutants.py:259-265` comment names `NoOtherChannelTransmitsAfterTheDeparting`, `NoFrameOfAnyChannelIsTakenFromTheSuccess` and `TheGateHoldsWhileTheResponseCannotBeHandedOver` (`TEST_F` at `test_plat_boot.cpp:983,945,1090`).
  - The `B19`/`B20` left at `:254-268` are diagnostic strings and `m(...)` arguments, which R1 said to leave.
- **R822-5-R2:** `REBOOT_RESET.md:316` reads "after its SUCCESS. Its three layers each carry one: the loop's stop (...)". Every layer and defect name is kept. Resolved.
- **R822-5-R3:** resolved.
  - `REBOOT_RESET.md:297` and `plat/README.md:89` carry the given sentence.
  - `ctrl_plat.h:38` reads "and, from ADP's shutdown, ADP until the port".
  - Checked against `ctrl_plat.c`:
    - `quiet()` services the store on its own centisecond and the F_NVM face from the first `depart()` pass;
    - `adp_poll` runs only at `reboot == 2u`, after every other ring has drained and `adp_mbx_set_enable(..., false)`;
    - the port is written once ADP owes nothing and its ring has drained.

    The prose now matches.
  - The header edit is a one-line, comment-only replacement (+1/-1, so no `__LINE__` shift).
- **Comment rule:** every added source-comment line in the delta was grepped for bench labels, review rounds, reviewer IDs and comment IDs. There are none. The `B11 to B23` in `REBOOT_RESET.md:316` is a design-doc test-range name that predates the delta.

### (3) No firmware image changed

- **Author's receipt:** `identity/{d3566d44,33b0d03a}/sha256.txt` are identical. They hash 8 files: the size fixture and the platform at 1x1/1if and 8x8/1if, each ELF and loadable binary. Copies are in `author-identity-*.sha256.txt`.
- **Independent structural check:** the delta changes one non-comment line in `*.c *.h *.cpp *.py`, and it is in `poll_grade.py`, a harness grader that is not an image input. `ctrl_plat.h` is the only firmware header touched, with comment text only and an unchanged line count.
- So round 5's legs and full pass carry. The images were not rebuilt.

### (4) The statement survey

- **At the head:** 0 conflicts, and all six derivations hold at both points.
- **The 11 two-valued figures** are each `load_grade.STATED_US_DONOR` against the pin's tables:
  - 1x1/1if: `event.ACMP` 185/170, `event.MAAP` 165/170, `record.acmp` 280/265, `record.adp` 105/100;
  - 8x8/2if: `build` 1,995 (`ctrl_loop.h` and `whole_grade`)/2,035, `event.ACMP` 350/210, `event.AECP` 105/110, `event.TICK` 40/85, `item.reclaim` 35 (polls)/40, `record.acmp` 440/305, `record.adp` 240/125.
- **At `41ca9f87`:** the same 11 lines are byte-identical (`survey_41ca9f87.log`), and the reviewer probe gives the same 10 load/polls pairs.
- **None is a superseded figure stated as current:**
  - The donor column is documented as measured on tsn-c-stack#32's image (`load_grade.py:161-177`) and is graded as its own column (`COLUMNS`, `BOUND`).
  - The costs where the donor is below the pin (`record.acmp`, `record.adp`, `event.ACMP`) are all in `load_grade.WALK`, which the docstring allows (`:200-203`).
  - Every other difference has the donor at or above the pin, which is the column's "larger of" rule. The probe found no donor below the pin outside WALK.
- **Limit:** the survey is the author's out-of-tree script. No in-tree gate binds `poll_grade`'s retained to `load_grade`'s (see S-R6-1).

### (5) Reruns

All rc 0 on a clean clone (table above). The harness self-test (246 mutants), `firmware-unit`, `docs.yml` and the TOC gates were not rerun. For those this review relies on the author's round-6 receipts: the delta reaches them only through comments, the doc table and the one `poll_grade` constant, which the rerun polls checks cover.

## Findings

### F1-R6 MINOR - Docs - the polls row's parenthesized figure is no longer round 22's

- **Where:** `docs/design/SPLIT_CONTROL_MEMORY.md:2238`, the `retained` row reads `285 (280) | 365 (395)`. The PR body's round-6 row (`PR-BODY.md` line 39) repeats `285 (280)`.
- **Authority/evidence:**
  - The column header (`:2231`) is "1x1/1if, us, at the head (round 22's)". The legend (`:2243`) says "Each figure in parentheses was round 22's, the most measured ... plus 5 %".
  - At round 22's `8684993388`, the row was `250 | 395` and `poll_grade.STATED_US[1]['retained'] = 250`.
  - `a0c25e5c` wrote `280 (250)`, which was correct.
  - Every other parenthesis in the table still equals round 22's, including this row's own 8x8/2if `(395)` (`receipts/f1r6-round22-row.txt`).
  - The 280 in the cell is the pre-REBOOT head figure, which the `poll_grade.py:70` docstring states correctly. In this table's convention it is wrong.
- **Origin:** R821-5 F1 option (a) prescribed "the polls row to `285 (280)`", and the author applied it verbatim. The defect is in this reviewer's prescription.
- **Impact:** the doc states a false round-22 figure for the retained item at 1x1/1if (280 instead of 250). Someone reconstructing the round-22 baseline from the table gets a wrong value. No gate, row, load or measurement verdict changes. It is a stated figure, so it is not wording-only.
- **Required outcome:** the cell reads `285 (250)`. Optionally, the PR body's F1 row names `285 (250)` as well.
- **Verification:** inspect the row against `git show 8684993388:docs/design/SPLIT_CONTROL_MEMORY.md` (row `retained | 250 | 395`). `docs_check.py` and `check_doc_style.py` rc 0.

### RESIDUE

- **RS-R6-1 (Docs, layout only):** the reflows left short or long lines among wrapped neighbours.
  - `test_plat_boot.cpp:187-189`: "... reads the tail only when / the room it last read is short / (mbx.c), reads it at each send; else the model's". Exact fix: join the last two lines, "the room it last read is short (mbx.c), reads it at each send; else the model's".
  - `poll_grade.py:72`: "#: built once and addressed per recipient and whose". Exact fix: refill it with the next line.
  - `ctrl_plat.h:38`: 99 columns among about 80-column neighbours. Exact fix: rewrap the paragraph to its neighbours' width.

  No text changes in any of these.

### SUGGESTIONS

- **S-R6-1 (Tests):** the round-6 fault probe shows that no in-tree gate catches the F1 class.
  - With `poll_grade.STATED_US[1]['retained']` planted back to 280, `load_grade.py --check`, `load_grade.py --selftest`, `flip_grade.py --check` and the polls checks all stay rc 0. Only the author's out-of-tree `statement_survey.py` fails (`receipts/probe-retained-280/`).
  - Optional: bring the survey's derivation checks into the tree. That is new work for its own Issue, not this lane.
- **Optional suggestions from earlier rounds** remain optional and untaken: R821-5 S1 and S2, R822-5 S1 to S13, and those they consolidate.

## Prior findings, resolved or retained at this head

| Finding | State at `33b0d03a` | Evidence |
|---|---|---|
| R821-5 F1 (MINOR, Tests, Docs) | **Tests part resolved.** `poll_grade` retained is 285 by its rule, equal to the load gate's, and the docstring is right. **Docs part superseded by F1-R6:** the row's figure moved to 285, but its round-22 parenthesis was changed to 280 | item (1) and F1-R6 |
| R821-5 RS-1 (RESIDUE) | Resolved | `test_plat_boot.cpp:187` |
| R821-5 RS-2 (RESIDUE) | Resolved | `REBOOT_RESET.md:315,316`, `test_plat_boot.cpp:76,982`, `plat_mutants.py:265` |
| R821-4 RS-A / R822-4 RES-A (RESIDUE), consolidated into R822-5-R1 | Resolved | `plat_mutants.py:259-265` |
| R822-5-R1, R2, R3 (RESIDUE) | Resolved | item (2) |
| R821-5 S1, S2; R822-5 S1 to S13 (SUGGESTION) | Retained, optional | not taken by the ruling |

No BLOCKER or MAJOR from earlier rounds is open.

## Lens results (each at `33b0d03a`)

```text
[R821] PASS Conformance - poll_grade.py:67-71,91,246; load_grade.py:146-148,179-182; rows_grade.py:157; ctrl_plat.c quiet()/depart()/ctrl_plat_step(); REBOOT_RESET.md:297,315-316 - the restated gate value follows its documented rule (SRP record cost 285 in both load columns); the REBOOT sequence prose (journal from the last pass, ADP polled only after the other rings drain and ADP's shutdown, the port once ADP's ring drains) matches the code; the delta changes no protocol behaviour (IEEE 1722.1-2021 7.4.43, Milan v1.2 5.6.3.3 paths unchanged)
[R821] PASS RTL - git diff --name-only d3566d44..33b0d03a (no hdl/, sw/litex/, CSR, census or SoC file); receipts/gates/delta_noncomment.log; author identity/{d3566d44,33b0d03a}/sha256.txt - no RTL, SoC or image input changed; the 8 split image files are byte-identical by the author's receipt, consistent with the structural check that only comments and one harness constant changed
[R821] PASS Robustness - ctrl_plat.h:30-41 (comment only, line count unchanged); test_plat_boot.cpp:184-189,976-983 and plat_mutants.py:259-265 (comments only); poll_grade.py:91,246 - no executable firmware or test path changed; the polls gate's RECORD/retained limit moves to its stated rule (280 to 285) while the measured apply is 280 by the rule, so the gate still binds and no limit was relaxed to obtain a pass
[R821] PASS Tests - receipts/gates/{polls_checks,load_check,load_selftest,flip_check_1x1,flip_selftest,survey_head,figures_head}.log; receipts/probe-retained-280/ - polls checks 33/33, load and flip checks and self-tests rc 0 on a clean clone; the planted-back 280 is caught only by the out-of-tree survey (S-R6-1, optional)
[R821] UNCLEAN Docs - SPLIT_CONTROL_MEMORY.md:2238 - F1-R6 (MINOR): round 22's retained figure stated as 280, not 250. Otherwise poll_grade.py:67-71 docstring, REBOOT_RESET.md:297,315-316, plat/README.md:89, ctrl_plat.h:38, test_plat_boot.cpp:76,187,982, plat_mutants.py:259-265 state the head's behaviour and figures; docs_check, doc_paths, doc_style rc 0; RS-R6-1 is RESIDUE
```

## Reviewer-owned ledger

Coverage for the rest of the PR outside the delta carries from R821-5 at `d3566d44`. The delta touches only the artifacts named below.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `poll_grade.py`, `load_grade.py`, `rows_grade.py`, `ctrl_plat.c`/`ctrl_plat.h`, `REBOOT_RESET.md` section 8, statement survey at the head and `41ca9f87` | R821-6 | `33b0d03a4ac899ed1601cd2cd97efbf66e293c9e` |
| RTL | CLEAN | delta file list (no RTL/SoC/image input), non-comment delta scan, author image identity receipts | R821-6 | `33b0d03a4ac899ed1601cd2cd97efbf66e293c9e` |
| Robustness | CLEAN | `ctrl_plat.h`, `test_plat_boot.cpp`, `plat_mutants.py` (comment-only edits), `poll_grade.py` limits | R821-6 | `33b0d03a4ac899ed1601cd2cd97efbf66e293c9e` |
| Tests | CLEAN | polls checks, load and flip check/self-test, survey, figures probe, retained-280 fault probe | R821-6 | `33b0d03a4ac899ed1601cd2cd97efbf66e293c9e` |
| Docs | UNCLEAN (F1-R6) | `SPLIT_CONTROL_MEMORY.md` polls table, `poll_grade.py` docstring, `REBOOT_RESET.md`, `plat/README.md`, source comments in the delta, PR body (the live body equals the packet's but for the manager's packet-link line) | R821-6 | `33b0d03a4ac899ed1601cd2cd97efbf66e293c9e` |

## Real limits

- The firmware images were not rebuilt. Image identity rests on the author's receipt plus the structural check of the delta.
- The harness self-test (246 mutants), `firmware-unit`, `docs.yml`, the TOC and em-dash gates, and any campaign were not rerun. This review relies on the author's round-6 receipts for those.
- The archive commit is unsigned. The packet is hash-consistent with its manifest, not independently signed.
- No manager source bank runs at this head, and none is claimed. The hosted run was in progress at the snapshot, and that snapshot is not acceptance.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- Acceptance item 1 stays partial by public ruling (Relates to #871), as in prior rounds.

## Pending manager duties

- Rule on F1-R6. Its fix is the one-cell `285 (250)`; a reviewer then re-checks Docs at the new head.
- Carry RS-R6-1 to the residue checklist.
- Build and validate the current-dev merge candidate (source base `1d6bf555`, live dev `6b66f66d`) with the builder and native banks, and link the receipts.
- Accept the hosted and act evidence at the exact merge head.
- Merge only with explicit maintainer authorization.

R821-6 FINISHED
