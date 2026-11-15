[R837] NEGATIVE - exact head 41ca9f876b01e4af84d872b8bdbd751cc09debe0

# R837-14: delta re-review of PR #902 (issue #894), rounds 15 to 20

- **Reviewed:** the delta from `867faf1e` (round 14; R838-9 POSITIVE there) to `41ca9f87`, tree `297dcb32`, and every present-tense bound or figure statement in section 13, FR_NFR 3.4.1 and the live PR body.
- **Verdict:** NEGATIVE, on two MINORs.
  - **F1:** a superseded image size is stated as current in section 13.
  - **F2:** the sweeps' reach is not stated exactly as their patterns are.
- **Not affected:** the rows, the load, the pace, the slice, the code delta and its controls. They are correct at this head.
- **Prior findings:** R837-13-F1 to F5, R1 to R4 and the author's five extra sites are closed at their cause. R837-13-F6 is closed for the two limits it named, and its class comes back in a narrower form as F2.
- **Also recorded:** eight residues and three suggestions.

## How the task was reconstructed

I read the following, in this order:
1. AGENTS.md and CONTRIBUTING.md (the review and lens rules).
2. Issue #894: its frozen acceptance, the delegated scope rulings, the amendment's 130 ms and the owner's decision that 8x8/2if rows are reported (#890).
3. FR_NFR 3.4.1, and section 13 of `docs/design/SPLIT_CONTROL_MEMORY.md`.
4. `git diff 867faf1e..41ca9f87` and its nine commits. I checked the whole lane diff from `66f71326` only where the delta depends on it.
5. The author's round-20 packet (`review-evidence/894-r1/author-r20` at `f6582308`), and the round-12, round-13 and round-16 receipts the carries cite.
6. REVIEW READY issuecomment-6893619187.

I wrote my verdict and ledger draft before reading R837-13's public report (issuecomment-6893393934). I used that report only to resolve its findings below. I did not read the R838 reports.

## Findings

### R837-14-F1: MINOR (Docs)

- **Where:** `docs/design/SPLIT_CONTROL_MEMORY.md:2382`. The 1x1/1if size fixture's rom is stated at a superseded figure, as current.
- **Evidence:**
  - `:2382` reads: "At 1x1/1if the size fixture's image is 110,800 B of rom and 55,152 B of sram, 41.0 RAMB36, its 552 B slots included, since the one-row edit's cut (...; 110,576 B and 40.5 RAMB36 before it)."
  - The same section, at `:2494`, gives the SET_CONFIGURATION cut that followed: "224 B there (111,024 B, 41.0 RAMB36)".
  - The author's round-12 receipt `author-r12/receipts/images/rom-per-image.txt` has `fixture-1x1-1if 110576 110800 111024`.
  - Round 13's slice change kept every image at equal sizes (`:2509`), and every later round is comment or constant only, with identical images (round 16's `receipts/identity/image-compare.txt`).
  - So the head's fixture is 111,024 B. The PR body's Status says so too.
  - No sweep can reach this sentence. Its figure is a byte count, which is neither a moved constant nor a row or load. The author's section-13 read skipped it because "before it" in the parenthesis counts as a history marker.
- **Impact:** the subsection describing the tiers' fit gives a reader the round-11 image as the head's.
- **Required outcome:** `:2382` gives 111,024 B as the head's, with 110,800 B (after the one-row edit's cut) and 110,576 B (40.5 RAMB36, before it) as history. The sram and RAMB36 figures are unchanged.
- **Verification:** `:2382` equals `:2494` and the Status line.

### R837-14-F2: MINOR (Tests, Docs)

- **Where:** PR body 20.6, 19.2 items 1 and 3, and the REVIEW READY's "Reach" lines. The round-20 claim "Each sweep's reach is stated exactly as its patterns are" is not exactly true.
- **Evidence, sweep 1** (`figure_sweep.py`'s `auto_rules`):
  - It drops every old value 0, 1 or 2 (`:79`).
  - It matches an old value of 1,000 or more only when written with a thousands separator (`:89`).
  - Neither restriction is in the stated reach ("a number its history held and the head does not") or the limits, in the PR body or the REVIEW READY.
- **Evidence, sweep 3:**
  - The REVIEW READY states the reach as "a two-decimal ms figure in a sentence naming a row".
  - The ROW pattern (`:129`) needs the figure to be followed by `ms`, ` and <digit>`, ` within`, ` over`, `,` or ` (`.
  - So the REVIEW READY's line is wider than the pattern. My probe (`receipts/reach_probe.tsv`, `scripts/reach_probe.py`) finds 1,236 non-head two-decimal figures outside that follow-context in section 13, FR_NFR 3.4.1 and the body. They include 52 non-head cells of the rows-history table at `:2361-2371`.
  - PR body 19.2 item 3 does state the follow-context, but it gives one alternative as "a space and a digit", where the pattern is " and " followed by a digit.
- **Not affected:** what the sweeps actually found. The dropped 0/1/2 values are expression literals (`receipts/sweeps/constant_history.txt`: `AECP_MBX_COMPLETIONS`' `+ 1u`, `MAP_SLOTS`, `SRP_MBX_POLL_MAX`). A grep finds no in-scope sentence stating an old value of 1,000 or more without a separator beside its subject. Every out-of-context row cell I read at `:2189` onward is labelled with its head.
- **Impact:** a reader is told that the uncovered region is smaller than it is. This is the class of R837-13-F6, now without a hidden instance.
- **Required outcome:** either state each sweep's reach exactly as its patterns are, in the PR body and the REVIEW READY (the 0/1/2 drop, the separator rule, the exact follow-context list), or widen the patterns, rerun and classify every new hit.
- **Verification:** the stated reach and limits equal `figure_sweep.py:79`, `:89` and `:129-133`, or the widened sweep reruns with every hit classified.

## Residue (wording only around figures correct at their own head; no lens made unclean)

- **R837-14-R1** (`SPLIT_CONTROL_MEMORY.md:1999-2007`, the 2026-11-05 record, sibling of R837-13-R1). Present tense remains around R1's fixes.
  - The present-tense sentences:
    - `:1999` "SRP's MRPDU build is now deferrable work";
    - `:2001` "builds nothing ... makes";
    - `:2002` "holds a build ... reports";
    - `:2003` "no two passes given whole run back to back";
    - `:2005` "stays the poll's";
    - `:2006` "are kept by where the work now stands";
    - `:2007` "... hold the rule, with 43 planted defects ... each failing".
  - `CTRL_LOOP_TX_AGE`, `CTRL_LOOP_TX_EVENTS`, `tx_pass`, `Loop.L19TheTransmitOnlyInAPassThatTakesNoRecord`, `Loop.L20AnAgedTransmitIsAPassOfItsOwn` and `Srp.AHeldBuildTakesAPassOfItsOwnPastItsAge` do not exist at the base or at the head.
  - Exact fix:
    - `:1999`: "was then deferrable work";
    - `:2001`: "built nothing and declared nothing; the build's call made ... and then built";
    - `:2002`: "held a build, and the poll reported";
    - `:2003`: "no two passes given whole ran back to back";
    - `:2005`: "stayed the poll's";
    - `:2006`: "were kept by where the work then stood";
    - `:2007`: "held the rule at that head, with 43 planted defects ... each failing its named test then".
- **R837-14-R2** (`:2197`). "the two builds are restated by the rule on the image that merged `dev-soft-core` `0fb66211`, whose heaviest are 96,033 and 40,700 CPU cycles": the build of one has since been restated twice (725, then 735 us).
  - Exact fix: "were restated ... whose heaviest were 96,033 and 40,700 CPU cycles (the build of one restated since, `:2444` and `:2506`)".
- **R837-14-R3** (`:2246`). "At 1x1/1if's R4, 74.83 ms, W less one record and W less two both hold 37 refills" is #810's head's as-built R4. `flip_grade.py --design as-built` gives 77.96 ms at this head (`receipts/head-gates/flip_check_1x1_asbuilt_exits_1.log`).
  - Exact fix: "At #810's head's 1x1/1if R4, 74.83 ms, W less one record and W less two both held 37 refills".
- **R837-14-R4** (`:2304`). "At this branch's merge of the pin move ... arm A's 8x8/2if image is 123,112 B ... and the size fixture's entry ledgers 58.0".
  - Exact fix: "was 123,112 B ... ledgered 58.0 (59.0 at the head, [section 5](#5-fit))".
- **R837-14-R5** (`:2382`, first sentence). "At 8x8/2if the size fixture's image, at the merge of #810's `084cf7a8`, is 125,200 B".
  - Exact fix: "was 125,200 B ... (125,792 B at the head)", per round 12's `rom-per-image.txt`. RAMB36 is unchanged.
- **R837-14-R6** (`:2520-2521`). "A change-notice retry is taken only in a pass that took no input ... once held 4 ms past its time" and "SRP's MRPDU build is a pass class of its own ... taken only in a pass that took no record ... or once held past its age". These are pre-tiers rules, framed by `:2519`'s "The three bullets below record the loop before them", but in the present tense. At the head, `ctrl_loop.h:144-181` gives THE RETRY's three passes and THE TRANSMIT's slice of tier 2.
  - Exact fix: "was taken only ...", "was a pass class of its own ..., taken only ...".
- **R837-14-R7** (PR body Status, round 20 bullet). "Nothing compiled or executed changed": `rows_grade.py`'s docstring is read at run time by `documented()`. The same bullet says its parser reads it identically.
  - Exact fix: "Nothing compiled changed, and what executes reads identically".
- **R837-14-R8** (PR body 19.2 item 3). "then ms, a space and a digit, within, ...".
  - Exact fix: "then ms, ' and ' with a digit, within, over, a comma or ' ('". This is part of F2's outcome if F2 is answered by restating.

## Suggestions

- **R837-14-S1 (Docs):** `:2214` "the arm holds 122,556 bytes, 324 under the granule" and `:2300` "under the AECP record's stated 265 and 205 us, and **no stated cost moves**". Both are base text from `66f71326`, dated by their paragraphs (round 25 and round 27), in the present tense.
  - Optional: put them in the past tense in a later documents pass. The PR does not change either line.
- **R837-14-S2 (Docs):** section 5's "With the control loop's tiers" table (`:365`, 1x1/1if fixture 110,400 B, 40.5) is outside this round's read scope.
  - Optional: reconcile it with 111,024 B or label its head.
- **R837-14-S3 (Tests):** to make F1's class reachable, give the section-13 read (`read13.py`) a rule that ignores history markers inside parentheses when they sit beside an unlabelled figure.
- **Retained, optional, causes unchanged** (no executable change in the delta): R837-10-S1, R837-10-S3, R837-7-S2 and R838-8-S1.

## Prior findings at this head (resolved after my own pass)

| Finding | State | Evidence at `41ca9f87` |
|---|---|---|
| R837-13-F1 (retired search's verdict as current) | **Closed at cause** | `:2194` past tense with the 20.93 ms tier row beside it. `FR_NFR.md:390` and `:393` are past tense. The `aecp_mbx.h:21-27` comment, whose token stream is identical (gcc `-fpreprocessed` and a tokenizer, `receipts/identity*.txt`). `rows_grade.py:5`, `:19-21`. The retired-artifact sweep reproduces 15 lines, all history. |
| R837-13-F2 (polls table) | **Closed** | Every cell at `:2219-2227` equals `poll_grade.STATED_US` (1x1/1if: 205/90/290/35/25/280/735/55/210; 8x8/2if: 325/245/690/60/35/365/1,215/70/275), with round 22's in parentheses. |
| R837-13-F3 (save bounds) | **Closed** | `:2518` gives 12,470/22,870 ms (8x8) and 4,070/6,070 ms (1x1), equal to harness README `:108`, `:112`. The KLJ2 and datasheet figures are labelled. |
| R837-13-F4 (32x32 load) | **Closed** | `:2525` gives 1.684 (2.175) and 2.41x, equal to `load_grade.py --check` at the head. |
| R837-13-F5 (125 vs 130 at 1x1) | **Closed** | `:2244` agrees with `flip_grade.py --check` (last 127.21 vs 130) and `--design as-built` (130 vs 125). |
| R837-13-F6 (stated sweep reach wider than patterns) | **Closed for its two named limits** (table cell with the unit in the header; load of 1 or more), both now stated in 19.2. | The class recurs as **R837-14-F2**. |
| R837-13-R1 to R4 | **Closed** | `:1974-1975`, `:2000`, `:2003` ("was the build's alone"), `:2330`, `:2340`, `:1970` read as the exact fixes. R1's siblings are R837-14-R1. |
| R837-13-S1, S2 | **Taken** | `retired_artifacts.py` reproduced byte-identically. The "What is left" figures are traced (`:2514`, `:2518`, `:2525` checked against the graders). |
| Author's five extra sites (`:2393-2395`, `:2429`, `:2466`, `:2490`, `:2493`) | **Closed** | 55/70 us equal `poll_grade.STATED_US`. 87,895 and 146,678 cycles are round 13's `record-classes-ed0df35b.txt`, on images identical to the head's. 28,376/56,474 and 300/595 us equal `edit_rows.PACED`. SET_STREAM_INFO is labelled round 12's. |
| R837-9-F1, F2; R837-10-F1; R837-11-F1, F2; R837-12-F1 | **Still closed** | `aecp_mbx.h:50` "txL was 49.69 ms at 7 ms, and 8 ms did". `ctrl_loop.h:371` `34u : 99u`. `tx_statements` is `[]` at both points. `:2004`, `:2204-2207`, `:2477`, `:1970`, `:2010`. |

## What I checked, by brief item

### (1) and (2): the delta's code

- **The change:** `ctrl_loop.h:371` moves the two-interface `CTRL_LOOP_TX_MS` from 98 to 99, over the head's 8x8/2if tx row of 98.49 ms.
  - Its only compiled reader is `_Static_assert(MBX_N_IF != 1u || ...)` (`ctrl_loop.c:203`), which is vacuous at two interfaces.
  - Round 16's receipts show 332 of 332 image files and 14 of 14 harness ELFs identical to `234bc149`'s.
  - Since `b6f5c638`, `sw/` changed only the `aecp_mbx.h` comment, and the preprocessor output is byte-identical (`receipts/identity-from-b6f5c638.txt`).
- **The controls:**
  - `flip_grade.channel_controls` now plants each interface count's leg (`33u : 99u` at 1x1/1if, `34u : 98u` at 8x8/2if) and requires the refusal at its own point. Its lambda binds `under` as a default argument, so there is no late binding.
  - `rows_tiers.channel_controls` requires `tx_statements` to be empty at the head and to have one finding per point under the plant.
- **Mutation probes** (disposable, in my clean clone, restored; `receipts/probes/`):
  - With `tx_statements` blind to 8x8/2if, both self-tests escape exactly "THE TRANSMIT's stated figure under its row" (584/585 and 1032/1033).
  - With the 8x8/2if leg reverted to 98, the 8x8/2if check reports "CTRL_LOOP_TX_MS states 98 ms, under the built design's tx row 98.49 ms", the 1x1/1if check still passes, and the flip self-test escapes the same control.
  - So each new control can fail for the defect it claims.
- **`rows_grade.py`:**
  - The AST without the module docstring is identical, positions included, against `26898c05`, `867faf1e` and `b6f5c638`.
  - The part `documented()` parses (`:325`, 4,508 characters) is identical, with the same ten sources.
  - The line count is 428 both ways, and nothing else reads `rows_grade.__doc__`.
- **Every importer at the head, all rc 0:** `flip_grade --selftest` 585/585, `rows_tiers --selftest` 1,033/1,033, `load_grade --selftest` 26/26, `record_classes --selftest` 11/11.
- **The flip outputs:**
  - `flip_grade --check --point 1x1/1if` is rc 0.
  - Over both points, at 8x8/2if, and `--design as-built` each exit 1 by design.
  - All four outputs and `rows_tiers --terms` are byte-identical to the author's round-20 receipts.
- **Not rerun:** the harness self-test (about 12 minutes and a heavy unit). I rely on the author's receipt (0 failures, 246 mutants).
- **Comment rule:** the delta's new source comments (`aecp_mbx.h:21-27` and `:50`, `flip_grade.py:176-177`, `rows_tiers.py:929`, the `rows_grade.py` docstring) name no lane, round, reviewer or comment ID. No residue.

### (3): the sweeps and the read

- **The four sweeps:** I reran the author's scripts (inspected first: read-only git plus their own output files, run with `python3 -I`) on my clean clone with the live PR body. The live body equals the packet's `PR-BODY.md` plus a trailing newline.
  - `constant_history.txt`, `figure_sweep.tsv` (sha256 `5e1538ac620d2c45…`, equal to the author's two parts concatenated; not republished, as it is over 200 KB), `figure-classes.txt`, `removed_constants.tsv` and `retired.tsv` are byte-identical to the author's.
  - `read-section13.txt` is identical apart from the author's header line.
- **The classified totals:** sweeps 1 and 3 have 828 hits, 0 unclassified and 0 current with a superseded figure. Sweep 2 has 10 removed constants and 8 lines, all history. Sweep 4 has 1 deleted file (the PR has no renames) and 15 lines, all history.
- **The read:** I read every present-tense bound or figure statement in section 13 from `:1967` to `:2527` in full against the head's graders. These were:
  - `flip_grade --check` at both points and as-built, `load_grade --check`, and `tier_grid --point 1x1/1if` (10 of 420, +0.0116, 0.695; `receipts/head-gates/tier_grid_1x1.log`);
  - the stated tables `poll_grade.STATED_US`, `load_grade.STATED_US` and `STATED_US_DONOR`, `rows_tiers.DATAPATH_US` and `LONG_RECORD_US`, and `edit_rows.PACED`;
  - the `ctrl_loop.h`, `aecp_mbx.h` and `aecp.h` constants.
  
  I also read FR_NFR 3.4.1 in full, and the PR body's Status, Round 20, How to validate, Known limitations and Definition of Done.
- **Every instance found:**
  - one MINOR (F1);
  - eight residues (R1 to R8; R1, R4, R5 and R6 are tense in framed records, R7 and R8 are PR-body wording);
  - two pre-existing base-text sites (S1).
- **Correct at the head:**
  - every row figure: 13.10 / 188.48 / 28.95 / 27.30 / 27.42 / 14.66 / 74.07 / 69.86 / 127.21 / 33.38 / 48.43, and the 8x8/2if set 44.24 to 459.40;
  - the loads 0.516 / 0.512, 0.794 / 0.754, 2.175 / 1.684 and 2.41x;
  - the pace (8 ms), the slice (950 / 1,300 us) and `CTRL_LOOP_SRP_UNIT_US` 280 / 365;
  - the "#32 moves" table (`:2281-2285`), equal to both columns of `load_grade`;
  - FR_NFR 3.4.1's figures.
- **Covered only by framing and the sweeps:** `:1098-:1966` are dated records, each opening "This subsection is the record of …". Their "this head" sentences refer to the record's head, and none names THE TIERS or #894.

### (4): the completeness claims

- Sweeps 2 and 4: their stated reach and limits match their code.
- Sweeps 1 and 3: their stated reach does not match their patterns. See F2.

### (5): the carries and the docs gates

- **The carries:** 332 images and 14 ELFs identical to `234bc149`'s (round 16's `image-compare.txt` and `harness-elf-sha256.txt`, after `b6f5c638`'s constant), and since then only the comment. `tx_statements` is `[]` at both points (`receipts/tx_statements-head.txt`).
- **Docs gates on a clean clone, every one rc 0** (`receipts/head-gates/SUMMARY.txt`): `docs_check`; `check_em_dash` over `867faf1e..` and `66f71326..`, run with the pinned renderer whose requirements are byte-identical to `tools/markdown/requirements.txt`; its self-test; doc_style, doc_paths, archive, feature_status, gptp_docs, solution_docs, submodule_docs, todo_ownership, hygiene and py_idiom.

### Packet integrity

All 105 rows of the author's round-20 INDEX match their files, by bytes and sha256. All 106 entries of the archive MANIFEST for `author-r20` match, none redacted. The archive commits are unsigned, so integrity rests on these hashes.

### Restore

The review clone and my probe clone are both at `41ca9f87`:
- tree and index tree `297dcb32`;
- worktree equal to HEAD in content and mode;
- `git ls-files -s` hash `a990bf3d…` in both;
- submodule gitlinks equal to the head's (`receipts/restore-check.txt`).

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `flip_grade --check --point 1x1/1if` rc 0, every 1x1/1if row within its bound (`receipts/head-gates/flip_check_1x1.log`); FR_NFR 3.4.1 `:331-458` against the `rows_tiers`, `paced_rows` and `ctrl_loop.h` bounds (20/30/90/130/238/49 ms); acceptance 2 (585/585) and 3 (0.516 ≤ 0.70; 8x8/2if reported by the owner's decision, #890) | R837-14 | `41ca9f876b01e4af84d872b8bdbd751cc09debe0` |
| RTL | CLEAN | `git diff --stat 867faf1e..41ca9f87` touches no HDL; `ctrl_loop.h:371` read only by `ctrl_loop.c:203`'s assertion, vacuous at two interfaces; image and ELF identity (round 16 receipts) and `aecp_mbx.h` preprocessed identity | R837-14 | `41ca9f876b01e4af84d872b8bdbd751cc09debe0` |
| Robustness | CLEAN | `flip_grade.py:171-184` and `rows_tiers.py:926-936` controls at each point, falsified by two mutation probes (`receipts/probes/`); `rows_grade.documented()` parse unchanged; the 8x8/2if leg at or over its row (98.49 → 99) | R837-14 | `41ca9f876b01e4af84d872b8bdbd751cc09debe0` |
| Tests | UNCLEAN (F2) | model self-tests 585/1,033/26/11 rc 0; mutation probes; sweeps reproduced byte-identically; `figure_sweep.py:79`, `:89`, `:129-133` against the stated reach | R837-14 | `41ca9f876b01e4af84d872b8bdbd751cc09debe0` |
| Docs | UNCLEAN (F1, F2) | section 13 `:1967-2527` in full and `:1098-1966` by framing and sweeps; FR_NFR 3.4.1; the live PR body; docs gates rc 0 on a clean clone | R837-14 | `41ca9f876b01e4af84d872b8bdbd751cc09debe0` |

## Real limits

- **No firmware, image, ELF or harness build was run.** Image and ELF identity rests on round 16's published receipts, plus my token and preprocessor identity of the only later `sw/` change.
- **The harness self-test was not rerun.** That result is the author's receipt.
- **No full parent, protocol-processor, gPTP, Yosys or builder bank was run, and no Docker, act or hosted acceptance.** I inspected no hosted run. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Not read sentence by sentence:** section 13 `:1098-:1966` (dated records, covered by framing and the mechanical sweeps), section 5, and the PR body's round-12 Description and Findings table (covered by the sweeps and spot reads).
- **First docs-gate attempt:** my first attempt ran without submodules and without the pinned renderer. Its logs, under `receipts/gates/`, are not listed in the manifest and are not evidence. The rerun under `receipts/head-gates/` is.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `66f71326`, live dev `6b66f66d`) with the builder and native banks, and link their receipts on the PR.
- Own hosted and act acceptance at the exact head.
- Carry R837-14-R1 to R8 to the residue checklist.
- Route F1 and F2 to the author, and publish this report.

R837-14 FINISHED
