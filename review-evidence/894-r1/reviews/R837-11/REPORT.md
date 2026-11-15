[R837] NEGATIVE - exact head 478ff78cc7752635147511490b06a0aa9ec1f25c

# R837-11: delta re-review of PR #902 (issue #894), rounds 15 to 17

- **Head:** `478ff78cc7752635147511490b06a0aa9ec1f25c`, tree `16bb0a6cf86e27811d3f8ac3c3ff733cd7ae54bb`, checked in the detached review clone and in a clean clone.
- **Delta reviewed whole:** `867faf1e..478ff78c`, four one-line commits with no trailers, seven files (`receipts/delta_changed_paths.txt`).
  - Round 15, `6b759b30`: section 13 and FR_NFR 3.4.1.
  - Round 16, `eed2e40d` and `b6f5c638`: the `aecp_mbx.h` comment, `ctrl_loop.h` `CTRL_LOOP_TX_MS` 98 to 99 at two interfaces, the two self-test controls and the budget README.
  - Round 17, `478ff78c`: `SPLIT_CONTROL_MEMORY.md` alone (`receipts/round17_changed_paths.txt`).
- **Ancestor:** R838-9 POSITIVE at `867faf1e`. It counts as the ancestor only because this round covers the whole delta at the exact head.
- **Verdict: NEGATIVE, on three MINOR findings.**
  - R837-10-F1 and round 17's four extra sites are closed at their cause.
  - My own sweep, derived from the history of every stated constant rather than a hand list, finds two superseded figures still stated as current in section 13, inside the author's declared sweep scope. That makes the PR's "none current" claims false.
  - Nothing compiled, executed or measured is wrong. Every row, bound, image and self-test the delta touches holds at this head.

## Findings

### R837-11-F1 - MINOR - Docs, Conformance - `docs/design/SPLIT_CONTROL_MEMORY.md:2204-2205`, `:2207` - the queued-notice table states superseded rows and the superseded 1x1/1if bound as current

- **Artifact:** section 13, "The queued notices at stated costs, and the first notice". The table and the sentence after it are present tense, with no head label. The paragraph above introduces them as THE TIERS' rows "solved by every source at the built design's slice".
  > | the first notice of a queue ... | 14.60 ms by every source, held to 20 | 20.25 ms by every source, stated 22 |
  > | every notice queued behind it (`AECP_QUEUED_MS`) | 91.59 ms by every source, held to 125 | 647.23 ms by every source, stated 62, ceiling 70 |
  >
  > At 1x1/1if both are decision D's tier bounds
- **Evidence:**
  - At the head, `flip_grade.py --check` gives the first and last queued notice as 14.66 and 127.21 ms at 1x1/1if, within 20 and 130 (`receipts/gates/flip_1x1.log`), and as 20.93 and 806.60 ms at 8x8/2if (`receipts/gates/flip_8x8.log`).
  - `AECP_QUEUED_MS` is `(MBX_N_IF == 1u ? 130u : 62u)` (`aecp_mbx.h:70`). By #894's amendment (issuecomment-6862465874), the 1x1/1if last-notice bound is 130 ms, not decision D's 125. FR_NFR 3.4.1 says so (`FR_NFR.md:386-387`), as `aecp_mbx.h:62-64` and the budget README (`:172`) do.
  - The table's figures are those of `12180198` (2026-11-12, the 1,200 us slice). Line history: `git log -L2204,2205` over the PR shows that commit as the last edit. Section 13 itself gives 91.59 as the first sweep's 1,200 us figure (`:2342`).
- **Impact:**
  - A reader of section 13 takes the last queued notice at 1x1/1if to be held to decision D's 125 ms with 33 ms of margin.
  - The head holds it to the amendment's 130 ms with 2.79 ms of margin. The 8x8/2if row is 806.60 ms, not 647.23.
  - The bound statement is the requirement's interpretation (FR_NFR 3.4.1), so this is not wording alone. It is the same class as R837-8-F1, whose cause this retains at a site round 15's row sweep did not reach: 14.60, 20.25, 91.59 and 647.23 are not cells of the rows-history table its tokens came from.
- **Required outcome:**
  - The table states the head's rows: 14.66 within 20 and 127.21 within 130 at 1x1/1if; 20.93 (stated 22) and 806.60 (stated 62, ceiling 70) at 8x8/2if, reported.
  - Alternatively, it is labelled as `12180198`'s at the 1,200 us slice, with the head's beside it.
  - `:2207` says the first notice's bound at 1x1/1if is decision D's 20 ms, and the last's is the amendment's 130 ms (`AECP_QUEUED_MS`).
- **Verification:** the table's cells equal `flip_grade.py --check` at both points at the new head. A grep of `91.59|14.60|20.25|647.23` returns only history. The docs gates stay rc 0.

### R837-11-F2 - MINOR - Docs, Tests - `docs/design/SPLIT_CONTROL_MEMORY.md:2477` - `EDIT_RECORD_US` stated as 260 and 325 us

- **Artifact:** "The one-row edit" section, bullet "The edits a class of their own". It reads, in the present tense:
  > each is charged a one-row edit's record, `EDIT_RECORD_US`, 260 us at 1x1/1if (24,360 cycles ...) and 325 us at 8x8/2if (30,563)
- **Evidence:**
  - At the head, `edit_rows.EDIT_RECORD_US` is `{'1x1/1if': 300, '8x8/2if': 595}`, the dearest of `edit_rows.PACED`'s members (`edit_rows.py:38-41`). Since round 12 an accepted SET_CONFIGURATION is a paced member (300 and 595 us).
  - The tier model charges each paced record that, not 260 or 325 (`edit_rows.py:59`, `:72`).
  - The head's figures appear only later, at `:2491` and `FR_NFR.md:383`, not beside this sentence.
  - The line was last edited at `b25530f6` (round 14).
  - The constant is absent from every token list the author's four sweeps used (`author-r17/receipts/statement-sweep.txt`; PR body 17.2's list). `receipts/constant_history.txt` shows it moved 240 to 260 within the PR, and then to the class's dearest member.
- **Impact:** a reader takes the paced class's charge as 260 us at 1x1/1if, so the rows' paced term looks 40 us a record cheaper than the model charges, and 270 us cheaper at 8x8/2if. The figure is a stated cost of the grader the acceptance rests on, so this is not wording alone.
- **Required outcome:** the sentence gives the class's charge as the head states it, or states 260 and 325 as round 11's, with the head's 300 and 595 beside them. For example: "each is charged the paced class's record, `EDIT_RECORD_US`, then a one-row edit's 260 us at 1x1/1if (...) and 325 at 8x8/2if, 300 and 595 since SET_CONFIGURATION joined the class ([below](#set_configurations-record))".
- **Verification:** no present-tense sentence pairs `EDIT_RECORD_US` with 240, 260 or 325. The paced class's figure everywhere equals `edit_rows.EDIT_RECORD_US`.

### R837-11-F3 - MINOR - Docs, Tests - PR body Status round 15 (`:27`), sections 15.1 (`:389`) and 17.2 (`:502`); REVIEW READY issuecomment-6892298990 - the sweeps' "none current" claims are false at the head

- **Artifact:**
  - Status round 15: "Every superseded 1x1/1if row figure (R4, R4L, ACMP, ADP, MAAP, the first and last queued notice, ...) is stated as history or beside the head's."
  - 15.1: "None states a superseded f[igure]".
  - 17.2 (`:502`): "None states a superseded figure as current". The REVIEW READY says "None is current".
- **Evidence:**
  - F1 (first and last queued notice, inside section 13) and F2 (a statement constant, inside section 13) are both in the declared scope. The two published claims assert their absence.
  - Cause: each sweep's tokens are a hand list.
    - Round 15's are the rows-history table's cells, so a row figure never entered in that table escapes.
    - Round 17's are named constants' old values, so `EDIT_RECORD_US`, `AECP_QUEUED_MS`'s 125 and the other moved stated costs escape.
  - `receipts/constant_history.txt` lists 73 constants that moved over the PR's 125 snapshots, many outside round 17's list: `EDIT_RECORD_US`, `AECP_OWED_BYTES`, `CTRL_LOOP_BUILD_PASS_US`, `LONG_RECORD_US`, `DATAPATH_US`, and the load gate's per-item costs.
  - My classified sweep over those values, the head's rows at both points and the head's loads is `receipts/figure_sweep.tsv`, `receipts/weak_marker_hits.txt` and `receipts/sweep_triage.md`. It finds F1 and F2, and no other present-tense superseded figure.
- **Impact:** the evidence a cold reviewer is told to rely on overstates its own completeness. That is how F1 (stale since the rows moved after `12180198`) and F2 (stale since `e4d80a8a` made SET_CONFIGURATION a paced member) survived several reviewed rounds. Under the maintainer's ruling, a verdict-bearing claim that is false is not residue.
- **Required outcome:**
  - The PR body's and the next REVIEW READY's completeness claims are true at their head.
  - The sweep's superseded values are derived mechanically from the history of every stated constant and stated row, not listed by hand. Examples: the definitions' values over the PR's commits, as `scripts/constant_history.py` does, and every row and bound cell against `flip_grade.py --check` at both points.
- **Verification:** a rerun of that sweep at the new head classifies every hit, with no present-tense superseded figure. The claims cite it.

### Residue (wording only around figures correct at their own head; no lens made unclean)

- **R837-11-R1:** `SPLIT_CONTROL_MEMORY.md:2427`, lever c's placement table. The row label "None (the head)" names lever c's head, not this one (`bbeb9299`, 2026-11-13). Exact fix: "None (the head lever c measured)".
- **R837-11-R2:** `SPLIT_CONTROL_MEMORY.md:2432`. "At an AECP item of 230 us the last queued notice is 125.87 ms even at a base of 155 us" is lever c's counterfactual at that head's costs. Exact fix: "was 125.87 ms then".
- **R837-11-R3:** `SPLIT_CONTROL_MEMORY.md:2244`. "before #894, at 1x1/1if, R4 is 73.02 ms ...; R5 is 37.19 ms ...; the first queued notice is held at 20 ms ...; At 8x8/2if R4 is 489.97 ms" is anchored "before #894" but in the present tense. Exact fix: "was" and "were" throughout those three sentences.
- **R837-11-R4:** PR body `:67`, the round-12 narrative. "Round 11's cut, its class split (...) and its TICK stand": the TICK is 55 us at the head (round 12's final pass), and the class is charged at its dearer member's record. Exact fix: "stood at round 12's start (its TICK restated to 55 us by the final pass, below)".

### Suggestions

- **R837-11-S1 (SUGGESTION, Docs):** derive future sweeps' tokens from `git log -L` (or an equivalent) on each stated constant's definition, as `scripts/constant_history.py` does. This is folded into F3's required outcome and is optional beyond it.
- **Retained, unchanged causes, optional:**
  - R837-10-S1 (Tests, Robustness): `tx_statements` holds the figure at or over the row, and the header says "rounded up". A planted `100u` still passes, since the code is unchanged since `b6f5c638`.
  - R837-10-S3 (Docs): `aecp_mbx.h:50` could give the head's result at 8 ms.
  - R837-7-S2 (Tests, Robustness): an unanswered over-cost record in arm B's `aecp-fanout` is reported, not held.
  - R838-8-S1 (Docs): the R838-6-F2 row's receipt label.

### Known, not a finding of this PR

- `tb/verilator/milan_dp/srptx.hpp:82-83` (`kJoinCs = 20`, against the firmware's 19 cs) and `tb/verilator/milan_dp/README.md:1610`, `:1639` (the adapter's 200 ms).
- They are filed as #916, whose acceptance covers both the harness and the README, and listed under the PR's Known limitations. My sweep found no other site of that defect.

## Prior findings at this head (read after my own pass)

| Finding | Status at `478ff78c` | Evidence |
|---|---|---|
| R837-10-F1 (MINOR, Docs): `:2004` stated the pre-tiers 176 ms JoinTime product as current | **Closed** at site and cause | `:2004` now says the product "was then within 2 x `MBX_N_IF` x 44 = 176 ms", and "Under THE TIERS no such product is claimed". `CTRL_LOOP_TX_BOUND_MS` (49 ms) holds the tx row at 1x1/1if, and 8x8/2if is reported. The IEEE 802.1Q Table 10-7 citation is now only beside the history. The R837-10 verification grep (`176 ms`, `x 44`, `44 ms`) returns only history or unrelated hits (`receipts/f1_verification_grep.txt`). |
| Round 17's four extra sites: `:2260`, `:2357`, `:2377`, `:2442` | **Closed** | `:2260`: `SRP_JOIN_CS` "200 ms then; 190 ms at 19 cs". `:2357`: "then at the slice ruling's 800 us (950 us at the head)". `:2377`: "held ... picked 800 us". `:2442`: "was ... 50 ms (... 49 ms since `T_egress` is counted)", and "the pace stayed ... then 6 ms (8 ms at the head)". Each matches `ctrl_loop.h:339`, `:365`, `:279` and `aecp_mbx.h:54`. |
| R837-10-R1 (RESIDUE): the RC line for record-classes | **Closed** | `author-r17/receipts/statements/RC.txt` carries the corrected line, and so does PR body 16.3. |
| R837-10-S2 (SUGGESTION): sweep statement figures and their products | Taken; **its cause is retained in part** | See F2 and F3: the statement tokens are still a hand list. |
| R837-10-S1, S3 (SUGGESTION) | Retained, optional | Not taken. Round 17 is documents only. |
| R837-9-F1 (MINOR): `aecp_mbx.h:50` gave txL 49.69 ms at 7 ms as current | **Closed** | It reads "txL was 49.69 ms at 7 ms, and 8 ms did". The head's 8 ms holds txL at 48.43 within 49 (`receipts/gates/flip_1x1.log`). |
| R837-9-F2 (MINOR): `CTRL_LOOP_TX_MS` 98 at two interfaces under the 98.49 row; no control planted that leg | **Closed** | `ctrl_loop.h:371` is `34u : 99u`. `tx_statements` is `[]` at both points, and each leg planted one under its row is refused at its own point only (`receipts/tx_probe.txt`). A `tx_statements` blind to either point is reported by both self-test controls (`receipts/tx_mutation_probe.txt`, RESULT PASS). |
| R837-8-F1 (MINOR): superseded row figures stated as current | Closed at its named sites; **cause retained at a new site** | See F1. |
| R838-9-R1 (RESIDUE): the R838-6-F2 row cited `:2524` | **Closed** | It cites `:2525`, which gives R4 13.10 ms at 950 us. |
| R837-7-S2, R838-8-S1 (SUGGESTION) | Retained, optional | Not taken, as the PR's Findings table states. |

## What I checked

1. **Packet integrity.**
   - The round-15 to 17 author packets are in `894-review-evidence` at `2db39123`, which descends from the named `6356449c`. That named tree holds only r7 to r16, and `author-r17` first appears at `2db39123`.
   - Every INDEX row (40, 67 and 40 rows) matches its file's bytes and length. Every outer `MANIFEST.json` entry for the three packets matches its `published_sha256`, and none is redacted (`receipts/packet_r17_verify.txt`).
   - The packet's `PR-BODY.md` equals the live PR body byte for byte, up to the trailing newline the fetch adds.
   - The evidence commit and the head are not GPG-signed. "Signed" here means hash-indexed.
2. **Round 17 at its cause.** The diff matches the REVIEW READY's claim: one file and 12 lines. The rows above check each changed sentence against the head's constants and rows.
3. **My own sweep.**
   - Scope: every Markdown file the PR changes (28), every first-party README, every first-party `sw/` and `tb/` source line, and the PR body. That is 797 files and 720 hits.
   - Values: every superseded value of every stated constant the PR moved (`scripts/constant_history.py`), plus every two-decimal ms figure and three-decimal load not among the head's rows and loads (`scripts/figure_sweep.py`).
   - Each unmarked hit (470) and each weak-marker hit (32) was read and classified (`receipts/sweep_triage.md`).
   - Result: F1, F2 and R1 to R4. Every other hit is history anchored to a named head, a clause figure, another quantity, or #916's known sites.
   - The PR body's current-status block was checked against exact-head execution:
     - every 1x1/1if and 8x8/2if row;
     - the load, 0.516 / 0.512 and 0.794 / 0.754;
     - the slice rule, 10 of 420 designs holding at a least margin of +0.0116;
     - 0.695 with every notice the largest legal one (`receipts/tier_grid_1x1.log`).
   - The block is correct.
4. **R837-10's round-15 and 16 checks still hold.**
   - `git diff --name-only b6f5c638 478ff78c` is `docs/design/SPLIT_CONTROL_MEMORY.md` alone.
   - No build, firmware or harness input reads it: every non-Markdown reference is a comment or `ci_scope.py`'s path list.
   - So round 16's identity receipts carry to this head: 332 of 332 image files and 14 of 14 harness ELFs identical to `234bc149`'s (`author-r16/receipts/identity/`; 332 and 14 rows counted).
   - The model outputs at this head, `flip_grade.py --check` at 1x1/1if, at 8x8/2if and at both, and `load_grade.py --check`, are byte-identical to round 16's receipts.
   - `tx_statements` is `[]` at both points.
   - `flip_grade.py --selftest`: 585 of 585 controls refused. `rows_tiers.py --selftest`: 1,033 of 1,033.
5. **Documentation gates** on a clean clone, 0 changed paths before and after (`receipts/gates/SUMMARY.txt`, `COMMANDS.txt`). All rc 0:
   - `docs_check`; em-dash from `66f71326`, `867faf1e` and `b6f5c638`;
   - doc style and gPTP docs, each with its self-test;
   - solution docs, submodule docs, feature status, TODO ownership, hygiene, both idiom gates, archive and doc paths;
   - the TOC anchors and check; `git diff --check`.
6. **Comment rule.** The delta's new source-comment text (`aecp_mbx.h:50`, `flip_grade.py:176-177`, `rows_tiers.py:929`) names no lane, round, reviewer or comment ID. No new residue.
7. **Restore.** Both checkouts' worktree and index equal the head (bytes and modes), with 0 porcelain lines and the six gitlinks as pinned (`receipts/restore_check.txt`). No probe wrote a file in either checkout: the mutation probe patches in-process.

## Lens results

```text
[R837] MINOR Conformance - docs/design/SPLIT_CONTROL_MEMORY.md:2204-2207 - R837-11-F1: 1x1/1if's last queued notice stated as held to decision D's 125 ms; the head and FR_NFR 3.4.1 hold it to 130 (AECP_QUEUED_MS)
[R837] PASS RTL - receipts/delta_changed_paths.txt; sw/firmware/ctrl/loop/ctrl_loop.h:371, ctrl_loop.c:203 - no HDL or interface in the delta; the one firmware edit (99u at two interfaces) enters only a static assertion scoped to MBX_N_IF == 1, and every image and harness ELF is byte-identical (author-r16 identity receipts, carried by the one-Markdown-file round-17 diff)
[R837] PASS Robustness - rows_tiers.py:555-569, :929-935; flip_grade.py:171-184; receipts/tx_probe.txt, tx_mutation_probe.txt - each interface leg planted one under its row is refused at its own point only, the at-ceiling head passes, and a check blind to either point is caught by both controls; R837-10-S1 (over-statement) retained as a suggestion
[R837] MINOR Tests - docs/design/SPLIT_CONTROL_MEMORY.md:2477; PR body :27, :389, :502 - R837-11-F2 and F3: the paced class's charge misstated, and the sweeps' completeness claims, the evidence the tests' scope is judged by, false at the head
[R837] MINOR Docs - docs/design/SPLIT_CONTROL_MEMORY.md:2204-2207, :2477; PR body :27, :389, :502 - R837-11-F1, F2 and F3
```

Clean results for the delta's executable parts, applied within the lenses above: the self-tests (585 of 585, 1,033 of 1,033), the flip check at 1x1/1if (rc 0) and at 8x8/2if (rc 1 by the owner's decision of 2026-11-12, reported), and the load gate (rc 0). All are byte-identical to round 16's receipts.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | issue #894 acceptance and scope decision; FR_NFR 3.4.1 (`:366-392`); section 13 `:2004`, `:2204-2207`, `:2260`, `:2348`, `:2442`; `ctrl_loop.h:334-371`; `aecp_mbx.h:38-70`; flip, load and tier-grid outputs | R837-11 | `478ff78cc7752635147511490b06a0aa9ec1f25c` |
| RTL | CLEAN | delta paths (no `hdl/`); `ctrl_loop.h:371`; `ctrl_loop.c:198-205`; author-r16 identity receipts plus the round-17 one-file diff | R837-11 | `478ff78cc7752635147511490b06a0aa9ec1f25c` |
| Robustness | CLEAN | `rows_tiers.tx_statements` and both controls; per-point plants; blind-check mutation probe | R837-11 | `478ff78cc7752635147511490b06a0aa9ec1f25c` |
| Tests | UNCLEAN (F2, F3) | `flip_grade.py --selftest`, `rows_tiers.py --selftest`; probes; `edit_rows.py`; the author's four sweeps and their claims; my sweep | R837-11 | `478ff78cc7752635147511490b06a0aa9ec1f25c` |
| Docs | UNCLEAN (F1, F2, F3) | the 28 changed Markdown files, every README, `sw/` and `tb/` comments, PR body, REVIEW READY; docs gates | R837-11 | `478ff78cc7752635147511490b06a0aa9ec1f25c` |

## Real limits

- No manager source bank runs at this head, and I claim none. Source-head execution here is the author's published receipts plus my own model runs, self-tests and docs gates on a clean clone.
- No firmware, harness or ELF was rebuilt. Image and ELF identity is carried from round 16's receipts by the one-Markdown-file round-17 diff. No Verilator or Yosys was run, since the delta holds no HDL.
- Hosted evidence at the exact head, snapshotted at about 10:45 CET (`receipts/hosted_check_runs.tsv`): 13 jobs completed with success, among them `docs-check-no-git`, `docs-gates-1` and `docs-gates-2`; 1 skipped (Physical gPTP, nightly and manual); 36 queued or in progress, including the Verilator and Yosys shards and `docs-gates-0`. That is not a hosted verdict; the manager owns hosted and act acceptance.
- Physical calibration was not run, and field skips are not hardware proof. 8x8/2if rows are reported by decision (#890), not held.
- The sweep is regex-driven and hand-classified. Integer row figures with no unit beside them, and figures in images, are outside it.

## Pending manager duties

- Carry F1 to F3 (MINOR) and R1 to R4 (RESIDUE) to the author; the residues also go to the residue checklist. Carry the retained suggestions.
- Re-review at the corrected head: all five lenses re-banked against that commit (Docs, Tests and Conformance re-covered; RTL and Robustness re-covered if anything in their scope moves).
- Decide whether #916's open sites need anything under AGENTS.md section 7 ("a finding moved to another Issue is not resolved"). The brief classes them as known, not a finding of this PR.
- Hosted and act acceptance at the exact head, and the current-dev merge candidate (source base `66f713267f201d1a00d7f711e04b3a996d804dee`, live dev `6b66f66d89cf25d2717687bcc2c3bf617685a99a`) with builder and native banks at the merge turn.
- A second positive review and the full completion bar before any merge, with explicit maintainer authorization.

R837-11 FINISHED
