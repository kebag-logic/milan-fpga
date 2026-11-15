[R837] NEGATIVE - exact head 867faf1e7321e1260f86701f01d7de0c94e67490

Round R837-8. Internal independent delta review of PR #902 (issue #894), round 14. Tree `639655730d2a898d963e195cfb95d35fef5ca715`. Delta: `234bc149..867faf1e`, two commits (`b25530f6`, `867faf1e`), six files, 21 insertions and 21 deletions. The delta changes only documents, comments and one docstring.

## Verdict summary

- **NEGATIVE, on one MINOR finding: R837-8-F1 (Docs).** R837-7-F1 is closed at every site it named, but not at its cause. One present-tense txL/R4L row figure that the round-12 and round-13 moves superseded is still stated as current in FR_NFR 3.4.1. A second sits in section 13. The author's grep tokens included no row figure for txL or R4L, so the sweep could not find either.
  - `FR_NFR.md:383` says "8 ms holds it, txL 48.09 ms and R4L 188.39 ms". The head's figures are 48.43 and 188.48. FR_NFR never gives the head's R4L.
  - This delta fixed the identical sentence in section 13 (`:2380`, "at the head it finds 8 ms, txL 48.43 ms and R4L 188.48"). The FR_NFR twin was left as it was.
- **Everything else in the focus list checks out at this head:**
  - the named R837-7-F1 sites;
  - R837-7-R1 and R838-7-R1, applied word for word;
  - R837-7-S1's precondition, true against `milan_soc.py` and the pinned LiteX;
  - the no-code-change proof;
  - the documentation gates;
  - the PR body's round-14 section and finding rows.
- **Wording residue:** three RESIDUE items and two suggestions are recorded below. None of them changes the verdict.
- **Prior verdicts:** round 13's verdicts on the code, tests and measurements carry. No compiled or executed input changed (Tests, below).

## Method

1. I read the AGENTS.md contract and the round's assignment. I fetched the REVIEW READY comment (issuecomment-6891277821), the review-start comment, the live PR #902 body and the signed author-r14 packet at archive `1a095573`.
2. I made my own pass over the raw delta (`receipts/delta.diff`, `receipts/delta_log.txt`).
3. I ran my own stale-figure greps (`stale_grep_r837.sh`, `stale_rows_r837.sh`) and my own token/AST identity probe (`identity_r837.py`).
4. I re-ran the slice model (`tier_grid.py`) for the one new current figure the delta adds, and a sample of the documentation gates.
5. I checked item 5's precondition against `milan_soc.py` and the pinned LiteX source.
6. Only after that did I read the round-13 reviews (R837-7, R838-7, R838-8) to resolve their findings.
7. I ran nothing heavy: no leg, campaign, build, Docker or act. The clone was restored and verified (`receipts/restore_check.txt`).

## Findings

### R837-8-F1 - MINOR - Docs - a superseded txL/R4L pace figure is still stated as current in FR_NFR 3.4.1 (R837-7-F1's cause, the rows)

- **Artifacts** (`receipts/f1_sites.txt`):
  - `docs/reference/FR_NFR.md:383` reads: "and with AMAP_LIVE_WRITE's cost re-measured at 30 us (... item 4), 8 ms holds it, txL 48.09 ms and R4L 188.39 ms (#894, #908)".
    - Those are the direct index's figures. The head gives txL 48.43 and R4L 188.48 (section 13 `:2371`; this delta's own `:2380`).
    - The next sentence, which this delta changed to past tense, says "8 ms then held txL, 48.23 ms, and R4L, 188.41 ms". So the line now gives an earlier state in present tense and a later state in past tense.
    - The head's R4L, 188.48, appears nowhere in FR_NFR.md (0 hits).
  - `docs/design/SPLIT_CONTROL_MEMORY.md:2467` (*The direct index*, item 4) reads: "Then txL is 49.69 ms at 7 ms, and 8 ms is the smallest pace that holds: txL 48.09 ms within 49 and R4L 188.39 within 238". This delta put the rest of that line into past tense, but this clause still gives the old figures in present tense. It is the lesser site, because "Then" and the subsection heading date it.
- **Authority and evidence:**
  - R837-7-F1's required outcome: sweep every current-tense figure the round-12 and round-13 moves touch, "and the rows", in section 13, FR_NFR 3.4.1, the READMEs and the PR body. Make each either the head's figure or explicitly historical.
  - PR body 14.1 claims: "Every row moved too. Each current-tense site now gives the head's figure, or says that the figure was then."
  - This delta's own fix of the twin sentence at `:2380` shows the standard the author applied.
  - The grep receipt's tokens (`receipts/stale-figures-grep.txt:2-3`) cover the cost and slice figures but no txL or R4L row figure. That is why neither site was classified.
  - My grep of every superseded 1x1/1if row figure outside table lines (`receipts/stale_rows_r837.tsv`) finds these two sites as the only present-tense uses. Every other hit is past tense or sits beside the head's figure.
- **Impact:**
  - A reader of the requirement clause takes txL 48.09 ms and R4L 188.39 ms as the pace's current result. The clause never states the head's R4L.
  - No bound is broken: 188.48 is within 238 and 48.43 within 49. The code, the tables and the checks carry the right figures.
  - This is a stale figure stated as current, not wording only, so it is MINOR, as R837-7-F1 and R838-6-F2 were.
- **Required outcome:**
  - `FR_NFR.md:383`: state the direct-index figures as history ("8 ms held it, txL 48.09 ms and R4L 188.39 ms"). Give the head's pace result (8 ms, txL 48.43 ms, R4L 188.48 ms) where the line states the head, as `:2380` does.
  - `SPLIT_CONTROL_MEMORY.md:2467`: make the clause past tense ("txL was 49.69 ms at 7 ms, and 8 ms was the smallest pace that held: txL 48.09 ms ... R4L 188.39"), or give the head's figures beside it.
  - Add the superseded row figures to the stale-figure grep's tokens and classify every hit.
- **Verification:** run `stale_rows_r837.sh` from the repository root. Every hit must be past tense or sit beside the head's figure. Compare with `flip_grade.py --check --point 1x1/1if` or section 13's 950 us row. The token stream and AST identity must stay intact.
- **Lens attribution:** Docs. It is not Conformance: no clause, bound, state transition or acceptance claim of the requirement is wrong, only a prose figure in its evidence. It is not Tests: no test, receipt or executable claim is wrong.

### R837-8-R1 - RESIDUE - Docs - the PR body's R838-6-F2 row cites `:2524` for the current summary

- **Artifact:** live PR #902 body, the Findings row "R838-6-F2 (MINOR)" (line 371 of `receipts/pr902_body_live.md`): "`SPLIT_CONTROL_MEMORY.md:2346`, `:2370`, `:2524`".
- **Evidence:** at the head, `:2524` is the hot-list bullet. The current summary (R4 13.10) is `:2525`. R837-7-F1's required outcome asked for the row to cite `:2525`.
- **Impact:** a pointer in PR text only. No figure or verdict changes.
- **Exact fix:** replace `:2524` with `:2525` in that row.

### R837-8-R2 - RESIDUE - Docs - one present-tense sentence inside the past-tense 900 us paragraph

- **Artifact:** `SPLIT_CONTROL_MEMORY.md:2509`: "Every other 1x1/1if row holds by every source, the load is 0.516 and 0.512, and the pace stays 8 ms."
- **Evidence:** this sentence sits between "the slice rule ... chose 950 us" and the ruling. It describes the 900 us state, which the rest of the paragraph now gives as past.
  - The figures are the same in both states: 0.516 and 0.512 were set at `99626ee4` and hold at the head, as `tier_grid.py` shows in `receipts/tier_grid_1x1.txt`.
  - The pace is 8 ms in both states.
- **Impact:** tense only. No figure is wrong.
- **Exact fix:** "Every other 1x1/1if row held by every source, the load was 0.516 and 0.512, and the pace stayed 8 ms."

### R837-8-R3 - RESIDUE - Docs - the PR body's 14.1 claims a head figure "beside" every moved past-tense site

- **Artifact:** PR body 14.1: "`:2373`, `:2443` to `:2445`, `:2459`, `:2467`, `:2477` and `:2509` are past tense. Where a figure moved, each gives the head's beside it".
- **Evidence:** `:2373` ("choosing the built design at 900 us") and `:2467` ("the slice rule still gave 900 us") give no head figure beside the old one. They are past tense, which is enough, and `:2342` gives 950 us.
- **Impact:** an overstated description in PR text. No figure is wrong apart from F1's clause at `:2467`, which F1 carries.
- **Exact fix:** "are past tense; `:2443`, `:2444` and `:2509` give the head's figure beside the old one."

### R837-8-S1 - SUGGESTION - Docs, Tests - generate the stale-figure tokens from the rows-history table

The receipt's tokens were chosen by hand and missed the rows. Taking every non-head cell of section 13's rows-history table (`:2359` to `:2370`) as a token would make the next sweep complete by construction, as `stale_rows_r837.sh` does.

### R837-8-S2 - SUGGESTION - Docs - R837-7-S1's face contract note

R837-7-S1 also suggested naming the precondition in the face's contract note. It is now stated in section 13 and in the receipt, which is sufficient. A one-line pointer where the face's commit/acknowledge contract is documented is optional.

## Focus items

1. **R837-7-F1** is **closed at every named site but not at its cause** (R837-8-F1). The named sites:
   - `SPLIT_CONTROL_MEMORY.md:2197` reads 735 (`ctrl_loop.h:328`: 735u).
   - `srp/README.md:238` reads "33.38 ms there at the 950 us slice", with 33.01 at 900 us as history.
   - `poll_grade.py:70` reads 280 and 365, which match `poll_grade.STATED_US` retained 280/365 (`:90`, `:92`) and `load_grade` `record.srp` 280/365.
   - PR body section 8 gives 0.516 and 0.512.
   - The R838-6-F2 row gives R4 13.10 and 127.21 at 950 us (but see R1).
   - The new current figures this delta adds are the head's: 0.516 and 0.695 at `:2380`, and 10 of 420 with 950 us chosen at `:2509` (`tier_grid.py --point 1x1/1if`, rc 0, `receipts/tier_grid_1x1.txt`).
   - The author's 64-hit classification is correct for the hits it lists: I spot-read every hit in section 13, FR_NFR, the READMEs and `load_grade.py`. My own token grep (`receipts/stale_grep_r837.tsv`) adds only past-tense or unrelated hits for 0.513 (`:2447`, `:2459`, the budget README's 0.513 ms). But the receipt's tokens omit the rows, which is F1.
2. **R837-7-R1 and R838-7-R1** are applied word for word. **R837-7-S1** is taken and its statement is true:
   - `cd_milan` and `cd_sys` are both `create_clkout` outputs of one `S7PLL` (`milan_soc.py:247`/`:250`, `:265`, `:288`).
   - Pinned LiteX `a1e1c365` `xilinx_common.py:42`, `:58-60` defaults `with_reset=True` to `AsyncResetSynchronizer(cd, ~self.locked)`.
   - No other driver of either domain's reset exists in `milan_soc.py`, and the CRG defines no `rst` (`receipts/item5_litex_check.txt`).
3. **The no-code-change proof holds:**
   - My probe (`receipts/identity_r837.txt`) gives `ctrl_loop.h`'s comment-stripped token stream identical at 516 lines (sha256 prefix `13d2df1e0b8efa83`, as the author's). `poll_grade.py`'s AST is identical with positions. `edit_rows.py`'s AST is identical once its docstring is blanked.
   - Nothing reads `edit_rows.__doc__`.
   - No executable reads section 13, FR_NFR or the SRP README. `test_ctrl_memory.py` reads section 3 only, and `ctrl_service_bounds.py` reads `MAILBOX_SPLIT.md`, which is unchanged.
   - So the author's 332/332 image and 14/14 ELF identity follows from the inputs. I spot-checked their receipts and rebuilt nothing.
   - Documentation gates I re-ran at the head (`receipts/gates_r837.txt`): `docs_check`, doc style, doc paths, archive, hygiene, feature status, solution docs, `git diff --check`, and `check_em_dash` from `234bc149` and from the source base `66f71326` (with the pinned renderer, `receipts/md_venv_freeze.txt`). Each was rc 0.
   - The author's packet INDEX is 45 of 45 rows byte- and hash-exact (`receipts/packet_verify.txt`).
4. **The PR body** (live, which equals the packet's `PR-BODY.md` but for one blank line):
   - It has the round 14 section.
   - It has the R837-7, R838-7 and R838-8 rows (F1, R1, S1 to S3, R838-7-F1/R1, R838-8-S1).
   - It keeps the round-13 rows.
   - Section 7's sentence now reads "In round 12, nothing under `sw/` changed after `a47cd3f2`".
   - Residue: R1 and R3.

## Prior findings at this head

| Prior ID | Disposition at `867faf1e` |
|---|---|
| R837-7-F1 (MINOR) | Named sites fixed. Cause not closed: retained as **R837-8-F1** |
| R837-7-R1 (RESIDUE) | Resolved exactly (`ctrl_loop.h:321-322`) |
| R837-7-S1 (SUGGESTION) | Taken; verified true (focus item 2); the optional contract-note part is S2 |
| R837-7-S2 (SUGGESTION) | Not taken; listed under Known limitations; carries as optional |
| R837-7-S3 (SUGGESTION) | Taken; INDEX rows are the published bytes, 45 of 45 |
| R838-7-F1 (MINOR) | Resolved before round 14 (R838-8 POSITIVE), kept; its line cite is R837-8-R1 |
| R838-7-R1 (RESIDUE) | Resolved exactly (`edit_rows.py:3`) |
| R838-8-S1 (SUGGESTION) | Not taken; optional |
| Round 13's other dispositions | Carry: the delta touches no artifact they depend on |

No new comment-rule instance is in the delta's source comments. `ctrl_loop.h` names a commit SHA. `edit_rows.py` drops the comment ID.

## Lens results

```text
[R837] PASS Conformance - docs/reference/FR_NFR.md:383 (234bc149..867faf1e, "still holds" -> "then held" only); SPLIT_CONTROL_MEMORY.md:2509 item-5 text; tier_grid.py --point 1x1/1if at head (receipts/tier_grid_1x1.txt) - no clause, bound, pace rule or slice rule changed; the new current figures (0.516, 0.695, 10 of 420, 950 us) are the model's at the head
[R837] PASS RTL - receipts/identity_r837.txt (ctrl_loop.h token stream identical); sw/litex/milan_soc.py:247-288 and pinned LiteX xilinx_common.py:42-60 (receipts/item5_litex_check.txt) - no source token changed; the stated clock/reset precondition matches the CRG and the pinned create_clkout
[R837] PASS Robustness - SPLIT_CONTROL_MEMORY.md:2509 ("A datapath clock or reset of its own would reopen the late path"); receipts/item5_litex_check.txt - the late-completion path's precondition is named and true, and no fault or refusal path changed
[R837] PASS Tests - receipts/identity_r837.txt; poll_grade.py and edit_rows.py ASTs; author receipts/identity/*.txt (INDEX-verified); git grep of doc readers (test_ctrl_memory.py:866 section 3 only, ctrl_service_bounds.py:13 MAILBOX_SPLIT) - no test, harness input or doc-read check changed, so round 13's test evidence carries
[R837] MINOR Docs - docs/reference/FR_NFR.md:383; SPLIT_CONTROL_MEMORY.md:2467 - R837-8-F1 (plus RESIDUE R1 to R3)
```

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | FR_NFR 3.4.1 delta; section 13 item-5 text; `tier_grid.py` at head | R837-8 | `867faf1e7321e1260f86701f01d7de0c94e67490` |
| RTL | CLEAN | `ctrl_loop.h` token stream; `milan_soc.py:247-288`; pinned LiteX `xilinx_common.py:42-60` | R837-8 | `867faf1e7321e1260f86701f01d7de0c94e67490` |
| Robustness | CLEAN | item-5 precondition, `receipts/item5_litex_check.txt` | R837-8 | `867faf1e7321e1260f86701f01d7de0c94e67490` |
| Tests | CLEAN | identity probe; ASTs; doc-reader grep; author identity receipts | R837-8 | `867faf1e7321e1260f86701f01d7de0c94e67490` |
| Docs | UNCLEAN (R837-8-F1 open) | section 13 (`:2197` to `:2509`), FR_NFR 3.4.1, SRP README, budget README, `poll_grade.py:70`, `edit_rows.py:3`, live PR body, author grep receipt | R837-8 | `867faf1e7321e1260f86701f01d7de0c94e67490` |

Code-lens coverage for round 13's code (`ctrl_loop.c`, the AECP face and commands, `record_classes.py`, the hooks harness) carries from round 13's reviews at `234bc149`. No compiled or executed input changed after it.

## Limits

- No leg, campaign, image build or ELF relink was run. Image and ELF identity is the author's receipt, which my token/AST probe and doc-reader search back.
- Hosted checks at `867faf1e` were inspected, not judged (`receipts/hosted_checks_867faf1e.tsv`): 9 success; 1 skipped (Physical gPTP, nightly/manual, which is not proof); 40 queued or in progress (Verilator and Yosys shards). The manager owns hosted and act acceptance.
- No manager source bank ran at this head, and none is inferred.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- The em-dash gate used an existing pinned-renderer environment, read-only.

## Pending manager duties

- Carry R1 to R3 to the residue checklist.
- Re-review after F1's fix.
- Build the current-dev merge candidate at the merge turn: source base `66f713267f201d1a00d7f711e04b3a996d804dee`, live dev `6b66f66d89cf25d2717687bcc2c3bf617685a99a`.
- Accept the exact-head hosted Verilator and Yosys results once they complete.

R837-8 FINISHED
