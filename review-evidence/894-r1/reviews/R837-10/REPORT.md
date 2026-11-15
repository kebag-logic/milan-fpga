[R837] NEGATIVE - exact head b6f5c638eb08973420109439c718a2c05766a374

# R837-10: delta re-review of PR #902 (issue #894), rounds 15 and 16

- **Head:** `b6f5c638eb08973420109439c718a2c05766a374`, tree `84201f66ba328bbdabb5774264f80d425bac3fa2`. I checked both in the isolated clone.
- **Delta:** `867faf1e..b6f5c638`, three commits (`6b759b30`, `eed2e40d`, `b6f5c638`), seven files.
- **Ancestor review:** R838-9 POSITIVE at `867faf1e` (issuecomment-6891425121). This round covers the whole delta at the exact head, so that ancestor applies to code the delta does not touch.
- **Verdict: NEGATIVE, on one MINOR finding (R837-10-F1, Docs).**
  - R837-9-F1 and R837-9-F2 are closed at their causes.
  - R837-8-F1 is closed for every row figure and pace figure.
  - One extra site the author found and reported as closed, `SPLIT_CONTROL_MEMORY.md:2004`, is closed only in part. It still states, in the present tense, a JoinTime consequence derived from the pre-tiers 44 ms: "within 2 x `MBX_N_IF` x 44 = 176 ms at two interfaces, inside the 200 ms JoinTime". That claim does not hold at this head.
  - Everything else checked holds: the identity claim, the controls, the self-tests, the statement checks and the replay of round 13's tables.

## Findings

### R837-10-F1 - MINOR - Docs - `:2004` still states the pre-tiers 176 ms JoinTime consequence as current

- **Artifact:** `docs/design/SPLIT_CONTROL_MEMORY.md:2004`, changed by this delta. The sentence reads:
  > Its bound, `CTRL_LOOP_TX_MS`, ... 30 + 7 x 2 = 44 ms (before THE TIERS; under them it is the tx row's statement, 34 and 99 ms at the head, [below](#the-tiers)); every participant's owed MRPDU, one a call, within 2 x `MBX_N_IF` x 44 = 176 ms at two interfaces, inside the 200 ms JoinTime (IEEE 802.1Q Table 10-7).
- **Authority and evidence:**
  - R837-8-F1's cause is any superseded figure stated as current. The PR body's round-16 section says: "`:2004` and `:2521` gave the pre-tiers 44 ms as current. They now mark it as before THE TIERS, with the head's statement beside it."
  - At `:2521` the author also moved the consequence into the past tense: "so every participant's MRPDU was sent within the 200 ms JoinTime (under THE TIERS ...)".
  - At `:2004` only the 44 ms got its parenthesis. The derived clause in the same sentence is still present tense, and it still multiplies the 44 ms that the sentence itself calls pre-tiers.
  - The same formula at the head's statement gives 2 x 2 x 99 = 396 ms at two interfaces (`ctrl_loop.h:371`; tx row 98.49 ms, `receipts/tx_row_figures.log`). That is not inside 200 ms.
  - The author's sweep could not find this hit. Its tokens (`author-r16/receipts/sweep-tokens.txt`) are two-decimal row figures only, with no statement figure such as 44, 176, 98 or 30, so `comment_sweep`/`stale_rows` "current with a superseded figure: 0" is true only of those tokens.
  - My spot sweep (`receipts/spot_sweep.txt`, `spot_sweep.py`, plus a grep for 44/176/JoinTime) finds no other such site.
- **Impact:**
  - A reader of section 13's THE TRANSMIT paragraph takes the current design to deliver every participant's MRPDU inside JoinTime at two interfaces. The head does not claim that: 8x8/2if rows are reported by decision (#890).
  - No code, bound, image, test or acceptance figure is wrong.
  - Acceptance 1 is at 1x1/1if, where the same formula gives 2 x 34 = 68 ms, so that point is unaffected.
- **Why MINOR, not RESIDUE:** the fix withdraws a current IEEE 802.1Q Table 10-7 timing claim. The owner's rule keeps a defect that touches a conformance or clause claim out of RESIDUE. This also matches the grading of R837-8-F1 and R837-9-F1, the same class of finding.
- **Lens:** Docs.
  - I did not attribute it to Conformance. The implementation, the frozen acceptance (1x1/1if) and every bound the tree holds are unchanged, and the two-interface timing is reported by decision.
  - If the manager reads the sentence as a clause claim of the PR, Conformance is attributable too.
- **Required outcome:**
  - State the clause as history at `:2004`, as `:2521` now does. For example: "every participant's owed MRPDU, one a call, was within 2 x `MBX_N_IF` x 44 = 176 ms at two interfaces, inside the 200 ms JoinTime".
  - Then either say what governs under THE TIERS, or drop the consequence. Under THE TIERS, the MRP timer budget `CTRL_LOOP_TX_BOUND_MS` is held at 1x1/1if, and 8x8/2if is reported.
  - Correct the PR body's round-16 claim about `:2004` to match.
- **Verification:**
  - At `:2004`, no present-tense clause rests on 44 or 176.
  - A grep of `docs/ sw/ tb/` and the PR body for `176 ms`, `x 44` and `44 ms` returns only history or unrelated hits.
  - The docs gates stay rc 0.

### R837-10-R1 - RESIDUE - the author packet's RC line for record-classes

- **Artifact:** `author-r16/receipts/statements/RC.txt`, line "record-classes ... equal to round 13's output".
- **Evidence:** `receipts/r13_vs_r16_compare.txt`. The two outputs are not byte-equal: two `results: 8x8/2if none` listing lines are swapped (the 16- and 0-record result sets). Sorted, they are identical, and every verdict line and the RESULT are identical.
- **Exact fix:** "equal to round 13's output up to the order of two result-set listing lines".

### Suggestions

- **R837-10-S1 (SUGGESTION, Tests, Robustness)**
  - **What:** `rows_tiers.tx_statements` (`rows_tiers.py:565`) refuses only a figure under the row. `ctrl_loop.h:366-367` describes the figure as the row "in ms rounded up".
  - **Evidence:** `receipts/tx_row_figures.log`. A planted `100u` at two interfaces passes, because the check holds the figure at or over the row, not at its ceiling.
  - **Option:** hold `tx_stated == ceil(row)`, or say "at or over" in the header comment, as `:2351` already does.
- **R837-10-S2 (SUGGESTION, Docs, Tests)**
  - **What:** add the statement history to the stale-figure tokens (`CTRL_LOOP_TX_MS` 30/98/44, 176, the 20 ms hold), not only the row cells. Derived consequences like F1's are then swept.
- **R837-10-S3 (SUGGESTION, Docs)**
  - **What:** R837-9-F1 offered two options. `aecp_mbx.h:50` now states 49.69 ms as history with "and 8 ms did", which is acceptable. It could also give the head's result at 8 ms (txL 48.43, R4L 188.48), as `FR_NFR.md:383` and `:2467` do.

## Prior findings at this head

| Prior finding | Status at `b6f5c638` | Evidence |
|---|---|---|
| R837-9-F1 (MINOR, Docs): `aecp_mbx.h:50` states "txL is 49.69 ms at 7 ms" as current | **Closed** at its site and cause | (1) `aecp_mbx.h:50` now reads "txL was 49.69 ms at 7 ms, and 8 ms did". (2) The token stream is identical at `867faf1e`, `234bc149` and the head, sha256 `9a09ccc4...` (`receipts/token_streams.txt`), which equals the author's `identity/tokens.txt`. (3) The non-built-pace figures F1 asked for (47.96, 45.67, 43.57, 47.29, 44.51, 42.96, 49.69, 53.86, 248.26) are all in `author-r16/receipts/sweep-tokens.txt`. (4) My sweep of `aecp_mbx.h` finds 49.69 only as history. |
| R837-9-F2 (MINOR, Docs, Tests): `CTRL_LOOP_TX_MS` states 98 at two interfaces, under the 98.49 row; no control plants the two-interface leg | **Closed**, option 1 | (1) `ctrl_loop.h:371` is `34u : 99u`, and 99 = ceil(98.49). (2) `tx_statements(root)` returns `[]` at both points, and the prior `98u` is refused at 8x8/2if (`receipts/tx_row_figures.log`). (3) Both controls refuse a `tx_statements` that skips 8x8/2if, and also one that skips 1x1/1if, and pass at the head (`receipts/probe_tx_controls.log`, my own in-process mutation `probe_tx_controls.py`). (4) `:2351` is history plus the head's ("stated as 30 and 98 ms. At the head it states 34 and 99 ms"). (5) The literal control strings were updated (`rows_tiers.py:932/934`, `flip_grade.py:174-183`). |
| R837-9 wording ("states as 30" at `:2351`) | Closed | `:2351` now reads "stated as 30 and 98 ms" |
| R837-9-S1 / S2 (SUGGESTION) | S1 applied for the pace figures (tokens above); S2 effectively answered by the per-point controls | the statement figures are still untokenised, which is how F1 survived (R837-10-S2) |
| R837-8-F1 (MINOR, Docs): superseded txL/R4L row and pace figures stated as current | **Closed for row and pace figures; its cause remains at one derived statement site (R837-10-F1)** | (1) My spot sweep of 27 superseded tokens over tracked `docs/ sw/ tb/` (`receipts/spot_sweep.txt`, 69 hits) finds every row and pace hit to be history, beside the head's figure, or an unrelated quantity (`ts_modular_ring.svg` coordinates, the budget README's 0.513 ms, SAVED_STATE 44 ms). (2) FR_NFR `:383` "8 ms held it, txL 48.09 ms and R4L 188.39 ms" is past tense. (3) The SRP README `:238` gives 33.01/29.78 beside the head's 33.38. (4) The one exception is `:2004`'s 176 ms (F1). |
| Round-15 reset precondition (`:2509`) | Holds against the tree | Section 13 `:2509` says `cd_milan` is a `create_clkout` of the same S7PLL as `cd_sys` (`milan_soc.py:265,282-288`, no `with_reset=False`, no CRG soft reset into the PLL besides `cpu_reset_n`, `:251-252`). "Both are held in reset until the PLL locks ... each released through its own synchronizer" matches each `create_clkout`'s default lock-driven reset. The LiteX source is not available on this host, so the per-domain synchronizer is taken from LiteX's documented `create_clkout` behaviour (limit below). |

## What I checked

1. **The delta, read in full.**
   - `git diff 867faf1e..b6f5c638` in word mode (`scratch`, unpublished). Code changes:
     - `ctrl_loop.h:371`, `98u` to `99u`;
     - `aecp_mbx.h:50`, two tense words in a `//` comment;
     - `rows_tiers.py:929-935`: the control now plants `33u : 98u` and requires one refusal per point;
     - `flip_grade.py:171-185`: each leg is planted alone (`33u : 99u` at 1x1/1if, `34u : 98u` at 8x8/2if) and its own point's refusal is required;
     - the README `:187`.
   - Docs changes: section 13 `:2004`, `:2351`, `:2380`, `:2402`, `:2466-2467`, `:2509`, `:2521`, and FR_NFR `:383`, `:387`.
   - **Comment rule:** the new comment at `flip_grade.py:176-177` and the changed source comments carry no lane label, review round, reviewer ID or comment ID. There is no new instance.
2. **The identity claim.**
   - `git grep CTRL_LOOP_TX_MS` across the tree: the only compiled reader is `ctrl_loop.c:203`, `_Static_assert(MBX_N_IF != 1u || CTRL_LOOP_TX_MS <= CTRL_LOOP_TX_BOUND_MS, ...)`. It is vacuous at two interfaces, and a static assertion emits no code.
   - The other readers are the Python model (`rows_tiers.py:167`) and the `ctrl_configs.py:241` description.
   - No build flag emits macro debug info (`-g3`, `-gdwarf` and `debug_macro` absent from `sw/ tb/ scripts/`).
   - Since `234bc149` the only token change in any `.c`/`.h` is that `#define`. `aecp_mbx.h`'s preprocessed token stream is identical (`receipts/token_streams.txt`, equal to the author's `tokens.txt` hashes).
   - The author's `image-compare.txt` reports 332/332 files, 0 differ. `harness-elf-sha256.txt` lists the harness ELFs, which I did not rebuild.
   - So the claim holds by construction and by the author's published hashes. I did not re-link the images or ELFs myself.
3. **Controls and self-tests at the head**, run in this clone (`receipts/`):
   - `rows_tiers --selftest`: 1033 of 1033, rc 0;
   - `flip_grade --selftest`: 585 of 585, rc 0;
   - `load_grade --selftest`: 26 of 26, rc 0;
   - `flip_grade --check --point 1x1/1if`: rc 0, RESULT PASS (tx 33.38/49, txL 48.43/49);
   - the mutation probe: PASS (item 1, row R837-9-F2).
4. **Sweeps.**
   - My own spot sweep: 27 superseded tokens, including the integer statement figures 44 ms, 176 ms and "30 and 98", plus a separate grep for `98 ms`/`98u`/`and 98` and for 44/176/JoinTime.
   - Result: exactly one superseded figure is still stated as current: `:2004`'s 176 ms (F1).
   - I accept the author's 766-file comment sweep for its 144 row and pace tokens. My sweep found no counterexample among those tokens.
5. **Round 13's legs.**
   - The round-16 re-runs `compare-1x1.txt` and `compare-8x8.txt` are byte-identical to `author-r13/receipts/compare/compare-{1x1,8x8}.txt`.
   - `record-classes.txt` equals `author-r13/receipts/classes/record-classes-ed0df35b.txt` up to the order of two listing lines (R837-10-R1), with RESULT PASS in both (`receipts/r13_vs_r16_compare.txt`).
6. **Author packets.**
   - `author-r15` (40 rows) and `author-r16` (67 rows) verify against their `INDEX.md`: 0 bad and 0 unlisted (`receipts/verify_index.log`).
   - All 109 rows verify against the archive's outer `MANIFEST.json`: 0 bad and none redacted (`receipts/verify_outer_manifest.log`). Archive commit `6356449c`.
   - The live PR body equals the packet's `PR-BODY.md` apart from the trailing newline the API adds.
7. **Docs gates at the head**, run myself:
   - `docs_check.py`: rc 0, 0 findings over 219 md files;
   - `check_doc_paths.py`: rc 0, 1166 paths;
   - `check_em_dash.py --base 867faf1e`: rc 0, 11 added lines;
   - `check_em_dash.py --base 66f71326`: rc 0, 2359 added lines, with the pinned renderer environment.

## Lens results

```text
[R837] PASS Conformance - docs/reference/FR_NFR.md:383,387; ctrl_loop.h:371; flip_grade --check --point 1x1/1if (receipts/flip_grade_--check_--point_1x1_1if.log) - the delta's clause text only changes tense or adds the head's figure; acceptance 1 (1x1/1if) rc 0 with tx 33.38 within 49 and txL 48.43 within 49; the bounds 49/238/130 ms and the 8x8/2if reported-by-decision status (#890) are unchanged; 99 = ceil(98.49) by the stated-figure rule
[R837] PASS RTL - no HDL in 867faf1e..b6f5c638; ctrl_loop.c:203 (sole compiled reader of CTRL_LOOP_TX_MS, vacuous at 2if); receipts/token_streams.txt; milan_soc.py:251-252,265,282-288 against SPLIT_CONTROL_MEMORY.md:2509's clock and reset precondition - no object code or interface contract changes; the reset wording matches the CRG
[R837] PASS Robustness - rows_tiers.py:929-935, flip_grade.py:171-185; receipts/probe_tx_controls.log, receipts/tx_row_figures.log - each control fails when the check skips either point, and both fail safe if a row later drops below a planted figure; over-statement is not refused (S1, a suggestion, unchanged design)
[R837] PASS Tests - rows_tiers --selftest 1033/1033, flip_grade --selftest 585/585, load_grade --selftest 26/26 (receipts/*selftest*.log); probe_tx_controls.py mutations at both points - the new controls fail for the defect they claim to detect and pass at the head
[R837] MINOR Docs - docs/design/SPLIT_CONTROL_MEMORY.md:2004 - R837-10-F1: the pre-tiers 176 ms JoinTime consequence is still stated as current
```

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | FR_NFR 3.4.1 `:383`, `:387`; `ctrl_loop.h:366-371`; flip check at 1x1/1if; tx row figures at both points | R837-10 | `b6f5c638eb08973420109439c718a2c05766a374` |
| RTL | CLEAN | delta (no HDL); `ctrl_loop.c:203`; token streams of `aecp_mbx.h`/`ctrl_loop.h` at `867faf1e`, `234bc149`, head; `milan_soc.py` CRG against `:2509` | R837-10 | `b6f5c638eb08973420109439c718a2c05766a374` |
| Robustness | CLEAN | `rows_tiers.py:929-935`, `flip_grade.py:171-185`; mutation probe at both points; over-statement probe | R837-10 | `b6f5c638eb08973420109439c718a2c05766a374` |
| Tests | CLEAN | three self-tests; `probe_tx_controls.py`; author `controls-probe.txt` | R837-10 | `b6f5c638eb08973420109439c718a2c05766a374` |
| Docs | UNCLEAN (R837-10-F1) | section 13 and FR_NFR delta lines; README `:187`; `aecp_mbx.h:50`; spot sweep; docs gates; PR body | R837-10 | `b6f5c638eb08973420109439c718a2c05766a374` |

Code the delta does not touch keeps R838-9's verdicts at `867faf1e`. Nothing those verdicts depend on changed, except the two controls and the define, which I re-covered here.

## Limits

- **Images and ELFs not rebuilt.** I did not re-link the 332 image files or the harness ELFs. The identity rests on the author's hash receipts plus my structural argument: the only token change is a `#define` read only by a static assertion that is vacuous at two interfaces, and no macro debug info is emitted.
- **The packets are hash-indexed, not cryptographically signed.** The archive commit is unsigned (`%G?` = N). I verified integrity against `INDEX.md` and the outer manifest only.
- **LiteX source not available locally.** The per-domain lock synchronizer behind `create_clkout` is not re-read from the pinned LiteX on this host.
- **No source bank run by me.** No manager source bank runs at this head, and I neither claim nor infer one. I did not inspect hosted or act runs; the manager owns hosted/act acceptance.
- **Not hardware proof.** Physical calibration NOT RUN; field skips are not hardware proof.

## Pending manager duties

- Carry R837-10-F1 (MINOR), R837-10-R1 (RESIDUE) and S1 to S3 to the author.
- After the `:2004` fix, a Docs delta re-review at the new head is required. If the fix is docs-only, the other four lenses carry from this round.
- At the merge turn: the current-dev candidate (source base `66f713267f201d1a00d7f711e04b3a996d804dee`, live dev `6b66f66d89cf25d2717687bcc2c3bf617685a99a`), the builder and native banks, and hosted/act acceptance on the exact head.

R837-10 FINISHED
