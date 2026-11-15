[R837] NEGATIVE - exact head 26898c05cfe530137b4aa7389bcc1b0b75de0ebb

Round R837-13 is an internal, cleared-context delta review of PR #902 (issue #894). It covers rounds 15 to 19, `867faf1e..26898c05`: seven commits and seven files. The head is `26898c05cfe530137b4aa7389bcc1b0b75de0ebb`, tree `7577c52f94bca3b0e17411213a479a82d0a35130`.

All five lenses were applied. The verdict is NEGATIVE on six MINOR findings:

- Five (F1 to F5) are sentences in section 13, FR_NFR 3.4.1 and one header comment that state a superseded figure or verdict as current. Under the maintainer's ruling each of these is MINOR.
- One (F6) is a completeness claim: the PR body and the REVIEW READY state the reach of sweeps 1 and 3 more widely than their patterns actually reach. F2 and F4 are the instances that prove it.

Round 19's own changes are correct:

- R837-12-F1 is closed at `:1970` and `:2010-2016`.
- R837-12-R1 to R5 are closed.
- All three sweeps reproduce the author's receipts byte for byte.
- The rows equal `flip_grade.py --check` at both points.
- The documentation gates are rc 0 on a clean clone.

Everything below is recorded in this one report so the author can absorb it in a single pass: the six findings, four residues and two suggestions.

## How the task was reconstructed

I read these in order:

1. AGENTS.md and CONTRIBUTING.md.
2. #894's body and frozen acceptance, plus the maintainer and manager comments, up to the round-19 REVIEW READY (issuecomment-6893105270).
3. FR_NFR 3.4.1.
4. Section 13 of `docs/design/SPLIT_CONTROL_MEMORY.md`.
5. The diff `867faf1e..26898c05`, commit by commit.
6. The published packet `review-evidence/894-r1` at `8d79dc79`.

Prior reviewers' reports (R837-12 and earlier) were read only after my own pass over the delta and section 13 was finished.

## Findings

### R837-13-F1 - MINOR - Docs, Conformance - `docs/design/SPLIT_CONTROL_MEMORY.md:2194`; `docs/reference/FR_NFR.md:390`, `:393`; `sw/firmware/ctrl/aecp/aecp_mbx.h:21-27` (comment) - the retired retry search's verdict is stated as current

- **Evidence.**
  - `:2194` reads: "185 us is the most THE RETRY's search holds the first notice to 22 ms at (`AECP_QUEUED_FIRST_MS`). At 186 us its binding pass ... is over THE SHARE".
  - `FR_NFR.md:390` reads: "185 us is the most THE RETRY's search holds the first notice of a queue to 22 ms at; 186 us already fails it."
  - `FR_NFR.md:393` reads: "Both bounds hold with other ports still refusing: each refused attempt is charged to its round". This is the search's model. It sits right after `:392`, which says the 8x8/2if rows "do not fit under the tiers".
  - `aecp_mbx.h:21-27` makes the same statement in a header comment.
  - The search, `sw/firmware/ctrl/test/ctrl_retry_search.py`, was deleted by this PR in `3f469cef` (THE TIERS). Section 13 itself says so six lines later: "the search is retired" (`:2200`).
  - The statement came in with `6c284a97`, a #665-lane commit on which the search still existed. It reached this branch through the merges after `3f469cef`.
  - Probe at the head: I planted `AECP_ROUND_COLD_US` at 186 us at two interfaces in a disposable copy.
    - The 8x8/2if first-queued-notice row stays 20.93 ms, within the stated 22 ms.
    - Every other row moves by at most 0.02 ms.
    - The load is unchanged.
    - Nothing at the head refuses 186 us. Receipts: `receipts/probe-cold186-flip-8x8.log` and `-1x1.log`.
- **Impact.** The requirement document and the design note justify the maintainer's 2.7 % exception by a tool and a verdict that the head does not have. "186 us already fails it" is false under the head's graders.
- **Required outcome.**
  - State the 185 us rationale as the 2026-11-13 decision's, made under the loop search before THE TIERS retired it, in the past tense.
  - Beside it, state what governs now: under THE TIERS the 8x8/2if first queued notice is a tier row, 20.93 ms by every source, stated 22 ms, reported (#890).
  - Do the same for FR_NFR `:393`'s "Both bounds hold", and make the same change to the header comment. That is a comment-only change: the token stream stays the same.
  - The decision and the 185 us figure themselves stand.
- **Verification.**
  - Section 13, FR_NFR 3.4.1 and `sw/firmware/ctrl` carry no present-tense "search holds" or "already fails".
  - `gcc -fpreprocessed -dD -E -P` token streams of `aecp_mbx.h` are identical before and after the change.
  - The documentation gates stay rc 0.

### R837-13-F2 - MINOR - Docs - `docs/design/SPLIT_CONTROL_MEMORY.md:2215-2229` - the polls-by-source table gives superseded stated costs as current

- **Evidence.**
  - `:2215` reads "`poll_grade.py` holds each pass's base and each item to its stated cost". The table under it carries no head label.
  - `:2229` reads "Each figure is the most measured ... plus 5 %".
  - 11 of the table's 18 cells differ from `poll_grade.STATED_US` at the head (`poll_grade.py:90-93`):

    | Item | 1x1/1if: table, head | 8x8/2if: table, head |
    |---|---|---|
    | base | 155, 205 | 280, 325 |
    | rebuild | 290, 290 | 630, 690 |
    | walk | 20, 35 | 60, 60 |
    | retained | 250, 280 | 395, 365 |
    | mrpdu | 405, 735 | 1,215, 1,215 |
    | acmp | 65, 55 | 185, 70 |
    | aecp | 225, 210 | 340, 275 |

  - Eight of those cells were moved by this PR's commits (`receipts/sweeps/constant_history.txt` rows 53-63). At `66f71326` the table equalled `poll_grade.py` in every one of those eight.
  - The other three cells (`retained` at 8x8/2if, and `aecp`) already differed at the base.
  - Section 13 itself gives the moves elsewhere. `:2340` gives "a pass's polls' base to 205 (155) ... the walk to 35 (20)", and `:2284-2285` gives "205, 205 | 325, 325".
- **Impact.** The section that states the model's costs gives a reader the pre-PR poll items as the head's.
- **Required outcome.** Do one of these:
  - give the head's `poll_grade.STATED_US` in every cell, with the earlier figures beside as history, as `:2284` does;
  - label the table and `:2229`'s measurement with the head they were taken at, and give the head's figures beside.
- **Verification.** Every cell equals `poll_grade.STATED_US` at the new head, or is labelled with its head. The F6 extension finds no unlabelled cell.

### R837-13-F3 - MINOR - Docs - `docs/design/SPLIT_CONTROL_MEMORY.md:2518` - the save's durability bounds give KLJ2's 8x8/2if figures as current

- **Evidence.**
  - `:2518`, under "What is left", reads: "A SET_NAME of the entity is durable at most 12,110 ms after it at 8x8/2if ... and 22,150 ms ... when marked just after another's save in flight".
  - This PR moved both figures to KLJ3's container: 12,470 ms and 22,870 ms, at 382 steps.
    - Section 13 gives the new figures at `:1624-1625` and `:1837`.
    - The harness README at the head gives them at `tb/verilator/ctrl_service_budget/README.md:108` and `:112`.
  - The same sentence's "datasheet maximum" figures, 15,370 and 28,670 ms at 8x8/2if, are the 2026-11-04 record's, derived at 370 steps (`:1854`).
- **Impact.** The section's summary of what is left states superseded worst-case durability figures as the head's.
- **Required outcome.**
  - `:2518` gives 12,470 and 22,870 ms at 8x8/2if, or gives 12,110 and 22,150 ms labelled as KLJ2's with the head's beside.
  - The datasheet-maximum figures are re-derived at 382 steps or labelled as KLJ2's.
- **Verification.** `:2518`'s figures equal the harness README's `save_window.bound_ms` figures at the new head, or carry their head.

### R837-13-F4 - MINOR - Docs - `docs/design/SPLIT_CONTROL_MEMORY.md:2525` - 32x32/2if's load gives round 30's figures as the head's

- **Evidence.**
  - The `:2525` bullet is set at the head: "`load_grade.py --check` at this head", "fails at this head".
  - It states "32x32/2if is reported, not held: ... 1.660 with #32 (2.151), 2.37x the compute for 0.70".
  - `load_grade.py --check` at the head prints 2.175 at the pin and 1.684 with #32, and 2.41x (`receipts/gates/load_check.log`). That is identical to the author's `author-r19/receipts/gates/load_check.log`.
  - 1.660, 2.151 and 2.37x are round 30's row at `:2320`.
- **Impact.** The head-set summary states a superseded load as current. The F6 pattern gap is why no sweep saw it.
- **Required outcome.** `:2525` gives 1.684 (2.175) and 2.41x, or labels round 30's figures with their head.
- **Verification.** `:2525` equals `load_grade.py --check` at the new head.

### R837-13-F5 - MINOR - Docs, Conformance - `docs/design/SPLIT_CONTROL_MEMORY.md:2244` - the flip check is said to hold the last queued notice to decision D's 125 ms at both points

- **Evidence.**
  - `:2244` reads: "Decision D's tier bounds bind each point's flip ... and the flip check holds them: since #894 the rows by every source of the built design ...; before it, and still with `flip_grade.py --design as-built` ..., at 1x1/1if and at 8x8/2if, R4 at tier 1's 20 ms, R5 and R6 at SRP's 90 ms, the first queued notice at 20 ms and the last at 125 ms."
  - At the head, `flip_grade.py --check --point 1x1/1if` holds the built design's last queued notice to 130 ms (`receipts/gates/flip_1x1.log`: "last | 127.21 | 130"). 127.21 ms would fail 125.
  - Only the as-built comparison model still uses 125 there.
  - The harness README's matching sentence (`README.md:172`) carries the 130 ms qualifier, and so do `:2207` and `:2344` in this section. `:2244` does not.
- **Impact.** It states a bound that the amendment superseded at 1x1/1if as the flip check's current bound.
- **Required outcome.** `:2244` says that at 1x1/1if the built design's last queued notice is held to the amendment's 130 ms (`AECP_QUEUED_MS`, [above]), with decision D's 125 ms as the as-built model's and 8x8/2if's.
- **Verification.** `:2244` agrees with `flip_grade.py --check` and `--design as-built` at both points at the new head.

### R837-13-F6 - MINOR - Docs, Tests - PR body 19.2 items 1 and 3, `:606`'s "Each sweep's limit is as stated above", and the REVIEW READY's Limit lines - two sweeps' stated reach is wider than their patterns

- **Evidence.**
  - **Sweep 1** states its reach as "a superseded value beside the moved constant's name, or beside the reviewer's prose subject for it".
    - Its AUTO rule counts a stated table key's value only when the value carries a unit (`figure_sweep.py:68`: "a table key's, only with a unit").
    - So a table cell whose unit is in the column header is unreachable even when the key names the row.
    - `:2219-2227` name `base`, `walk`, `rebuild`, `retained`, `mrpdu` and `acmp`, each listed as moved in `constant_history.txt`, beside superseded values. The sweep has zero hits in `:2211-2232` (F2).
  - **Sweep 3** states its reach as "every three-decimal figure in a sentence naming the load".
    - Its pattern is `(?<![\d.])(0\.\d{3})` (`figure_sweep.py:132`), so no load of 1 or more is reachable.
    - Yet its own `HEAD_LOADS` (`:101`) lists 2.175 and 1.684.
    - A probe with only that pattern widened to `[1-9]\d*\.\d{3}` finds 19 new LOAD-rule hits. Exactly two are load figures, and both are F4's at `:2525`. The rest are millisecond figures in sentences that mention a load (`receipts/sweeps/probe-load-ge1.tsv`, script `scripts/probe_figure_sweep_wideload.py`).
  - The claim "every hit ... is classified, and none states a superseded figure ... as current" is true of the hits. The limits around it are not exactly true.
- **Impact.** A reader is told that the uncovered region is smaller than it is. This is the same class as R837-11-F3.
- **Required outcome.** Do one of these:
  - extend the two rules (a table row whose first cell is a moved key, with the unit read from the header; a load pattern of `\d+\.\d{3}`), rerun, and classify every new hit;
  - state each limit exactly (table cells with the unit in the header; loads of 1 or more).
- **Verification.** Rerun the sweeps at the new head. The F2 and F4 sites appear as hits and are classified, or the PR body and the REVIEW READY state those limits.

## Residue (wording only around figures correct at their own head; no lens made unclean)

- **R837-13-R1:** `SPLIT_CONTROL_MEMORY.md:1974-1975`, `:2000`, `:2003`.
  - Round 19 put `:2010-2016` of the 2026-11-05 record into the past tense. The same record's present tense remains above them: "now takes the next pass whole", "a retry's round is committed within `CTRL_LOOP_RETRY_MS` ... `aecp_mbx.c` holds the sum to `AECP_NOTICE_MS` at compile time", "The loop marks a pass ... (`tx_pass`)", "Once SRP's tick has counted more than `CTRL_LOOP_TX_AGE`".
  - None of `CTRL_LOOP_RETRY_MS`, `CTRL_LOOP_RETRY_AGE_MS`, `CTRL_LOOP_TX_AGE`, `CTRL_LOOP_TX_EVENTS` or `tx_pass` exists at the base or at the head. Nothing holds `AECP_NOTICE_MS` at compile time.
  - The figures are correct for the record's head, and `:1969-1970` frame them.
  - Exact fix:
    - `:1974`: "now takes" becomes "then took".
    - `:1975`: "is committed" becomes "was committed", and "holds the sum" becomes "held the sum".
    - `:2000`: "marks ... calls" becomes "marked ... called".
    - `:2003`: "is the build's alone" becomes "was the build's alone".
- **R837-13-R2:** `:2330`. "**32x32/2if is 0.960 over**" sits in round 30's framed paragraph ("there"). Exact fix: "was 0.960 over there (0.984 at the head)".
- **R837-13-R3:** `:2340`. "every row below is at those costs" is followed by a table whose later rows are at later costs, each labelled. Exact fix: "the table's first row below is at those costs; each later row names its own".
- **R837-13-R4:** `:1970`. "Two of its statements no longer held when this note was written. A retried notice was then inside its 20 ms ..." The second sentence is the change the note records, not one of the statements that no longer held. Exact fix: "Two of its statements no longer held when this note was written: a retried notice was then inside its 20 ms under any input, by construction, and the least margin it states ...".

## Suggestions

- **R837-13-S1 (SUGGESTION, Tests, Docs):** add a retired-artifact sweep. List every file the PR deletes (`git log --diff-filter=D --name-only 66f71326..HEAD`) and the prose names of those files ("THE RETRY's search", "the loop search"). Grep the sweep's scope for each, and class every hit. That would have found F1 mechanically.
- **R837-13-S2 (SUGGESTION, Docs):** trace every figure in section 13's "What is left" bullets (`:2513-2526`) to a named grader or harness output at the head. F3 and F4 are both there.
- **Retained, optional, causes unchanged:** R837-10-S1 (`tx_statements` holds "at or over"), R837-10-S3, R837-7-S2, R838-8-S1.

## What I checked

### (1) Prior findings at this head (read after my own pass)

| Finding | State at `26898c05` | Evidence |
|---|---|---|
| R837-12-F1 (MINOR): `:1970` and `:2010-2014` stated THE RETRY's by-construction 20 ms and the removed `CTRL_LOOP_SRP_MS`'s 18 ms as current | **Closed at its sites.** Its cause class, a pre-tiers retry bound or verdict stated as current, has one sibling outside the named sites, kept open as R837-13-F1 | `:1970` reads "no longer held when this note was written" and names THE TIERS' rows: 14.66 within 20 at 1x1/1if, 20.93 at 8x8/2if stated 22. `:2010` reads "stated", with "Under THE TIERS it is removed" and R5 and R6 at 74.07 and 69.86 ms. `:2011-2016` are past tense. All equal `flip_grade.py --check` at both points. Tense residue in the same record above is R837-13-R1 |
| R837-12-R1 | Closed | `:2522` reads "(removed under THE TIERS), was ... took ... fitted ... held" |
| R837-12-R2 | Closed | Harness README `:1490` reads "past its 130 ms bound (at 1,250 ms)" |
| R837-12-R3 | Closed | PR body `:9` "(completed in 18.2)", `:10` "(completed in 18.1)", `:307` "Round 14's tokens named no `EDIT_RECORD_US`, which round 18 found (18.2)" |
| R837-12-R4 | Closed | PR body `:541` and `:613` read "copied unchanged but for a one-line provenance comment", as the REVIEW READY does |
| R837-12-R5 | Closed | `figure_classify.py` classes README `:172` as "decision D's bound, the 1x1/1if 130 ms beside it" |
| R837-12-S1 | Taken | `removed_constants.py` (10 removed, 8 lines, all history) and the "by construction" grep (`:1970`, `:2351`, `:2519`), reproduced |
| R837-11-F1 and F2 | Closed, sites unchanged since `4ae887a1` | `:2204-2207` and `:2477` |
| R837-11-F3 | Closed as recorded. The class recurs in a new form as R837-13-F6 | See F6 |
| R837-10-F1 | Closed, unchanged | `:2004` gives the 176 ms product as history, with `CTRL_LOOP_TX_BOUND_MS` and #890 beside it |
| R837-9-F1 and F2 | Closed | `aecp_mbx.h:50` reads "txL was 49.69 ms at 7 ms, and 8 ms did". `ctrl_loop.h:371` reads `34u : 99u`. `tx_statements` is `[]` at both points. Each planted leg is refused at its own point only (`receipts/tx_statements.txt`) |
| R837-8-F1, R837-10-R1, R838-9-R1 | Closed, unchanged | Rounds 17 to 19 do not touch them |

### (2) The three sweeps, rerun, and section 13 read against the graders

I copied the packet's scripts into this packet's `scripts/author_*.py` and ran them on a clean clone of the head, against `66f71326` and the live PR body. The live body is the packet's `PR-BODY.md` plus one trailing newline.

- `constant_history.py` reports 125 snapshots and 73 constants moved.
- `figure_sweep.py` reports 797 files, 822 hits and 539 without a history marker.
- `removed_constants.py` reports 10 gone and 8 lines.
- Both classifiers are rc 0, with nothing unclassified.
- Every output equals the author's receipt byte for byte (`receipts/sweeps/`).
- The split per sweep matches the REVIEW READY. Sweep 1 has 256 hits: 133 historical, 56 beside, 8 head, 51 another, 8 #916. Sweep 3 has 566 hits: 324 historical, 19 beside, 7 head, 216 another.

The by-hand read covered every present-tense bound and figure statement from `:2189` to `:2527`, against `flip_grade.py --check` at both points, `load_grade.py --check`, `poll_grade.STATED_US`, the headers' constants and the harness README. That read found F1 to F5 and R2 to R3.

Each subsection from `:1098` to `:2188` is framed as a dated record ("This subsection is the record of ..."). There I read the framing, the lines this PR changed (`:1149-1150`, `:1624-1625`, `:1837`, `:1970`, `:2004`, `:2010-2016`) and the bound statements of the 2026-11-05 record (`:1967-2060`). That read found R1 and R4.

Rows confirmed at the head:

- At 1x1/1if: 13.10, 74.07, 69.86, 14.66, 127.21, 188.48, 28.95, 27.30, 27.42, 33.38 and 48.43 ms.
- At 8x8/2if, reported by decision (#890): 44.24, 206.45, 196.31, 20.93, 806.60, 195.76, 67.94, 68.08, 69.13, 98.49 and 459.40 ms.
- `:2204-2207`, `:2344-2347`, `:2351`, `:2371`, `:2380`, `:2509`, `:2520-2521` and FR_NFR `:383` and `:386-387` equal them.
- `:2197`'s 975, 1,010 and 735 us, and 1,030, 1,995 and 1,215 us, equal `ctrl_loop.h:326-328`.

### (3) The completeness claims

- **True as stated:**
  - The claim that every hit is classified with none current.
  - Sweep 2's reach and limit.
  - The "by construction" result.
  - "`git diff --name-only 4ae887a1 26898c05` lists the two Markdown files alone".
- **Not exactly true:** sweep 1's and sweep 3's stated reach and limit (F6).

### (4) The rounds 15-16 carry-over and the gates

- `git diff --name-only b6f5c638 26898c05` lists `SPLIT_CONTROL_MEMORY.md` and the harness README only. No compiled or linked input changed after R837-10's head.
- R837-10's identity evidence is the author-r16 packet. Its INDEX and archive manifest are re-verified, with 0 mismatches (`receipts/packet-verify-r16.txt`):
  - 332 image files at `b6f5c638`, the same set as `234bc149`'s, 0 differing;
  - 14 harness ELFs identical;
  - the token streams differ only at `CTRL_LOOP_TX_MS`.
- `CTRL_LOOP_TX_MS` is read only by `ctrl_loop.c:203`'s `_Static_assert` under `MBX_N_IF == 1`.
- Self-tests at the head:
  - `flip_grade.py --selftest`: 585 of 585 controls refused;
  - `rows_tiers.py --selftest`: 1,033 of 1,033;
  - `load_grade.py --selftest`: 26 of 26.
- `tx_statements` is `[]` at both points.
- Documentation and idiom gates on a clean clone, 0 changed paths after (`receipts/gates-SUMMARY.txt`), all rc 0:
  - docs_check;
  - check_em_dash from `66f71326`, `867faf1e` and `4ae887a1`, plus its self-test, run with the pinned renderer, cmarkgfm 2025.10.22 and html5lib 1.1;
  - doc style, gPTP docs, DOC_MAP;
  - cpp and py idiom;
  - `git diff --check 66f71326 HEAD`;
  - solution docs, submodule docs, feature status, TODO ownership, hygiene, doc paths, archive.
- Graders on the same clone:
  - `flip_grade.py --check --point 1x1/1if` rc 0;
  - `load_grade.py --check` rc 0;
  - `--check` over both points, and at 8x8/2if, rc 1 by design.
  - Each output is identical to the author's receipt.
- The author-r19 packet verifies: 48 INDEX rows and 49 manifest rows, 0 mismatches (`receipts/packet-verify-r19.txt`).

### Clean-lens lines

```text
[R837] PASS RTL - sw/firmware/ctrl/loop/ctrl_loop.h:371, sw/firmware/ctrl/loop/ctrl_loop.c:203, sw/firmware/ctrl/aecp/aecp_mbx.h:50; git diff --name-only 867faf1e..26898c05 - the delta has no HDL; its only compiled changes are CTRL_LOOP_TX_MS's two-interface 98->99 (read only by a one-interface _Static_assert) and a comment (token stream identical); author-r16 identity receipts (332 images, 14 ELFs identical to 234bc149's) re-verified, and nothing compiled changed after b6f5c638
[R837] PASS Robustness - tb/verilator/ctrl_service_budget/flip_grade.py:171-184, rows_tiers.py:926-936; receipts/tx_statements.txt - each interface count's TX_MS leg planted under its row is refused at its own point only, the unplanted head gives [] at both points, and self-tests refuse 585/585, 1033/1033 and 26/26 at the head; rounds 17-19 change no behaviour, input path or configuration
```

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F5) | FR_NFR 3.4.1 `:372-394`, `:415`; section 13 `:2189-2527`; `flip_grade.py --check` at both points; `--design as-built` at 1x1/1if; the 186 us probe | R837-13 | `26898c05cfe530137b4aa7389bcc1b0b75de0ebb` |
| RTL | CLEAN | `ctrl_loop.h:371`, `ctrl_loop.c:203`, `aecp_mbx.h:50`; author-r16 identity receipts; `git diff --name-only b6f5c638..26898c05` | R837-13 | `26898c05cfe530137b4aa7389bcc1b0b75de0ebb` |
| Robustness | CLEAN | `flip_grade.py:171-184`, `rows_tiers.py:926-936`; `receipts/tx_statements.txt`; the three self-tests | R837-13 | `26898c05cfe530137b4aa7389bcc1b0b75de0ebb` |
| Tests | UNCLEAN (F6) | `figure_sweep.py:68`, `:101`, `:132`; the three sweeps rerun; the widened-pattern probe; the self-tests | R837-13 | `26898c05cfe530137b4aa7389bcc1b0b75de0ebb` |
| Docs | UNCLEAN (F1 to F6) | section 13 `:1967-2527`; FR_NFR 3.4.1; harness README `:108`, `:112`, `:172`, `:185`, `:1490`; the live PR body (19.2, the Findings rows); the REVIEW READY; the docs gates | R837-13 | `26898c05cfe530137b4aa7389bcc1b0b75de0ebb` |

R838-9 (POSITIVE at `867faf1e`) does not cover the delta's lenses, because this round leaves three of them unclean.

## Real limits

- **No source bank.** No manager source bank runs at this head. Source-head execution evidence is the author's published gate receipts plus the gates and graders I reran here.
- **Physical calibration NOT RUN.** Field skips are not hardware proof.
- **Images not rebuilt.** I did not rebuild images or ELFs. Identity rests on the re-verified r16 receipts and on the fact that nothing compiled changed after `b6f5c638`.
- **Unsigned evidence commit.** The commit `8d79dc79` is unsigned. Packet integrity rests on its INDEX and archive manifest hashes, which I re-verified.
- **Save model not run.** I did not run `save_window.py` directly; it imports harness modules outside a harness run. F3's head figures are the harness README's and section 13's own `:1624` and `:1837`. I did not re-derive the datasheet-maximum figures at 382 steps.
- **Early subsections spot-read.** In section 13's dated records (`:1098-1966`) I read the framing, the PR-changed lines and the 2026-11-05 record's bound statements, not every sentence.
- **Hosted checks.** At the time of reading, the exact-head hosted checks were partly complete. Docs, lint, CDC and several firmware jobs had succeeded; Verilator shards, the elaborate gates and the remaining firmware jobs were queued or in progress; physical gPTP was skipped (`receipts/hosted-checks-26898c05.txt`). I make no hosted claim.
- **Out of scope.** #916 is known and not this PR's. 8x8/2if rows are reported only, by decision (#890). The PR #914 ruling does not apply here.

## Pending manager duties

- Hosted and act acceptance at the exact head.
- The current-dev merge candidate at the merge turn, on source base `66f71326` and live dev `6b66f66d`, with builder and native banks.
- Publishing this report and its receipts.
- Carrying R837-13-R1 to R4 to the residue checklist.

## Receipts (listed in MANIFEST.sha256)

- `receipts/gates-SUMMARY.txt` and `receipts/gates/*`: the gates and graders on the clean clone.
- `receipts/sweeps/*`: the reruns, and the widened LOAD probe's hits.
- `receipts/findings-evidence.txt`: each finding's cited lines beside the head's figure.
- `receipts/probe-cold186-flip-*.log`, `receipts/tx_statements.txt`, `receipts/packet-verify-r16.txt`, `receipts/packet-verify-r19.txt`, `receipts/hosted-checks-26898c05.txt` and `receipts/restore-verify.txt`.
- `restore-verify.txt` shows both clones at the exact head, tree, index and submodule gitlinks after the probes. The probe copy was deleted.
- `scripts/*`: `run_gates.sh`, `verify_packet.py`, `findings_evidence.sh`, the probe sweep, and the author's sweep scripts as run.

R837-13 FINISHED
