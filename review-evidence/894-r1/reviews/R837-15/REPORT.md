[R837] NEGATIVE - exact head fe1fd5413afca1352b6990a732ac84512b874ab6

# R837-15: delta re-review of PR #902 (issue #894), rounds 15 to 20 and the R837-14 fix

- **Head:** `fe1fd5413afca1352b6990a732ac84512b874ab6`, tree `5454838dad6c954e2e2376440655a7e83a13b982`. Ten commits on `867faf1e` (round 14, R838-9 POSITIVE). This round covers the whole delta `867faf1e..fe1fd541`: 8 files, +112 / -107.
- **Role:** internal, cleared-context, independent reviewer. I read no private author material and no other reviewer's report before my own pass. I read R837-14's findings (PR #902 issuecomment-6894240714) only afterwards, to resolve them.
- **Verdict:** NEGATIVE on two MINORs, both Docs.
  - F1: section 5's tier paragraph, the one `fe1fd541` edited, still gives the 8x8/2if platform's ruling-head rom as the head's.
  - F2: the live PR body and the issue's REVIEW READY describe `41ca9f87`. The PR body still says the F1 fix is "not pushed", with "This head is unchanged".
  - Every other lens is clean. Everything else checked holds:
    - every prior finding is closed at its cause;
    - every row, load, slice and image figure in the delta is the head's;
    - the four sweeps reproduce byte-for-byte;
    - the stated sweep reaches equal their patterns;
    - the carries hold;
    - the documentation gates are rc 0.

## How the task was reconstructed

1. AGENTS.md and CONTRIBUTING.md: the lenses, the severities, the completion ledger, and the rule that a REVIEW READY names its full SHA.
2. The issue #894 body (acceptance, and the maintainer-delegated scope of 2026-11-12) and its rulings:
   - the round-13 ruling issuecomment-6888782796 (the slice rule's choice);
   - the amendment issuecomment-6862465874 (the last queued notice's 130 ms at 1x1/1if);
   - #890 (8x8/2if reported).
3. The round-20 REVIEW READY (issuecomment-6893619187, edited in place), the evidence tree `6be20b98` (`review-evidence/894-r1/author-r20/`, `HANDOFF-r20.md` included) and the `local-fe1fd541/` receipts.
4. `git diff 867faf1e..fe1fd541`, word by word for `41ca9f87..fe1fd541`, and its history.
5. Then the head's graders, the image receipts, and my own probes.

## Findings

### R837-15-F1: MINOR (Docs)

- **Where:** `docs/design/SPLIT_CONTROL_MEMORY.md:370`, second sentence. It reads: "The platform's image there holds 130,328 B of `rom` in 131,072, 744 B before the granule its ledger's 60.0 holds."
- **Evidence:**
  - The same paragraph's table row `:368` gives the head's figure as "130,920 (130,328)", with the ruling's head in parentheses.
  - `:2494` says "the 8x8/2if platform holds 130,920 B of 131,072, 60.0 RAMB36, 152 B spare", and so does the PR body's Status (`:57`).
  - The author's `author-r12/receipts/images/rom-per-image.txt` gives `platform-8x8-2if 130496 130704 130920`.
  - No compiled change since then alters sizes. Round 13's slice change kept equal sizes (`:2498`, `:2509`). Rounds 14 and 16 had 0 of 332 image files differing from `234bc149`. Since `b6f5c638` the delta is comment, docstring and Markdown only, and the header's preprocessed token stream is identical (below).
  - The sentence was introduced in this PR (`4c7e3350`). `fe1fd541` gave the head's figure to the same paragraph's first sentence (S2), but left this one as it was.
  - No sweep can reach it: it is a byte count beside no moved constant. The author's byte read was scoped to section 13, FR_NFR 3.4.1 and the PR body (`HANDOFF-r20.md`, item 3), so it never read section 5.
- **Impact:** the fit paragraph gives the platform's ruling-head image and its 744 B of headroom as current. At the head the image is 592 B larger and has 152 B before the 60.0 granule. That headroom is what any further growth at the ledgered point is judged against.
- **Required outcome:** `:370` gives the head's figure with the ruling's head's as history. For example: "The platform's image there holds 130,920 B of `rom` in 131,072 at the head, 152 B before the granule its ledger's 60.0 holds (130,328 B and 744 B at the ruling's head)."
- **Verification:** `:370` agrees with `:368`, `:2494` and the PR Status. A byte/RAMB36 read extended to section 5's tier paragraph (`:361-372`) finds no other stale figure there. My own probe of that range (`receipts/s5-byte-sentences.tsv`) finds only this one.

### R837-15-F2: MINOR (Docs)

- **Where:** the live PR #902 body (sha256 `8b061b6a…`, identical to the packet's `author-r20/PR-BODY.md`) and issue #894's REVIEW READY record:
  - Status `:25`: "Head `41ca9f87`: twenty-six commits on round 11's `9606b3a9`, rounds 12 to 20".
  - The Findings row for R837-14-F1, `:788`: "Prepared as one local commit on this head, not pushed: the manager routes it to this PR or the next of the train. This head is unchanged".
  - How to get into the same state, `:812`: `git rev-parse --short=8 HEAD   # 41ca9f87`.
  - `:839`: "The final head is `41ca9f87`". The gate table has no row for `fe1fd541`.
  - No REVIEW READY names `fe1fd541`. The issue's last one for this lane is round 20's, for `41ca9f87`, and `HANDOFF-r20.md` says "no REVIEW READY names it".
- **Authority:** AGENTS.md section 5 (REVIEW READY with the full SHA and its validation) and the Docs lens ("The PR and Issue contain enough evidence for another cold reviewer").
- **Impact:**
  - A cold reviewer of the PR reads R837-14-F1 as still open at the head.
  - The PR names no head-specific evidence for the commit under review. That evidence exists, `author-r20/receipts/local-fe1fd541/` (26 commands, rc 0), but nothing in the PR links it.
  - The Definition of Done's "Required local verification bar passes" points at gates recorded for `41ca9f87`.
  - This is not wording only: it misstates a finding's resolution and the head that the evidence covers.
- **Required outcome:**
  - The PR body's Status, How-to, final-pass text and gate table name `fe1fd541`, 27 commits on `9606b3a9`.
  - They state that commit's change: R837-14-F1, R1 to R6, S1, S2, and the eight further sites.
  - They link `receipts/local-fe1fd541/`.
  - The R837-14-F1 row records it as fixed in the tree at `fe1fd541`.
  - A REVIEW READY (new, or edited in place as round 20's was) names the full SHA of the head handed to review.
- **Verification:** grep the live body for `41ca9f87` as the current head, and for "not pushed". Read the issue for a REVIEW READY naming the head's full SHA.

## Residue (wording only; no lens made unclean; for the residue checklist)

- **R837-15-R1** (PR body 20.6, `:654`): "ROW's exact follow-context,, and name the limits". Exact fix: "ROW's exact follow-context, and name the limits".
- **R837-15-R2** (PR body 18.3, `:552`): "Its 824 hits at the head" is round 18's count. The sweep has 828 at `fe1fd541`, reproduced below. Exact fix: "Its 824 hits at `4ae887a1`".
- **R837-15-R3** (`SPLIT_CONTROL_MEMORY.md:2006`): "Three of the head's behaviours were kept by where the work then stood, each found against the head's own trace". Inside the now past-tense 2026-11-05 record, "the head" reads as the PR's head. Exact fix: "Three of that head's behaviours were kept by where the work then stood, each found against its own trace". The mechanism the sentence goes on to give still holds at the head (`srp_mbx.c:1062`, "The poll reclaims, so a record the next pass takes finds the room").

## Suggestions (optional)

- **R837-15-S1 (Docs, outside the delta):** `SPLIT_CONTROL_MEMORY.md:2275` says "With #32 the 8x8/2if `answering-every-port` arm does not fit its ledger". This is base text from `66f71326`, unchanged by this PR. It is superseded since the pin move: section 5 `:357` gives 123,420 B, 1,508 B under 124,928, and the entry is 59.0 at the head. A later documentation pass or a new Issue, not this lane.
- **R837-15-S2 (Docs, outside the delta):** section 5 `:483` says "plans 58.5 ... its entry ledgers 58.5 ... The cap is now fully used: any further growth at that point ... is a STOP". This is #810's merged text under `:472`'s lead "At this branch's head ... (round 30)", and the tiers ruling's 59.0 supersedes it (`:273`). It could be labelled with its head or put in the past tense.
- **R837-15-S3 (Tests):** widen the author's byte/RAMB36 read (`read13.py`'s extraction) to the section-5 paragraphs this PR writes (`:265-273`, `:335-348`, `:361-372`). F1 sat outside its scope. My `scripts/byte_sentences.py` is one way to list them.
- **R837-15-S4 (Docs):** the stated ROW and LOAD reach are exact but leave case-sensitivity implicit. The keywords are matched as written, so a sentence opening with "Load" does not match `load`. One clause in 19.2 item 3 would make that explicit.
- **Retained, causes unchanged:**
  - R837-14-S1's `:2300` "**no stated cost moves**" (base text; `:2214` was taken);
  - R837-14-S3;
  - R837-10-S1, R837-10-S3, R837-7-S2 and R838-8-S1. Each needs a code change, and the delta makes none.
- **Known, not this PR's:** #916.

## Prior findings at this head (resolved after my own pass)

| Finding | State at `fe1fd541` | Evidence |
|---|---|---|
| R837-14-F1 (`:2382` gave 110,800 B as the head's) | **Closed at cause** | `:2382` reads "111,024 B of rom and 55,152 B of sram, 41.0 RAMB36 ... since SET_CONFIGURATION's cut; 110,800 B after the one-row edit's cut, and 110,576 B and 40.5 RAMB36 before it". This equals `:2494`, the Status `:57`, section 5's table `:365`, and `rom-per-image.txt`'s `fixture-1x1-1if ... 111024`. The RAMB36 arithmetic holds: 55 + 27 half-tiles = 41.0. |
| R837-14-F2 (stated sweep reach wider than the patterns) | **Closed at cause** | PR body 19.2 items 1 and 3, 18.3, and the edited REVIEW READY state AUTO's 0/1/2 drop (`figure_sweep.py` `auto_rules`), the thousands-separator rule (`f'{int(v):,}'` for values of 1,000 or more), and ROW's exact follow-context (`(?= ?ms\b\| and \d\| within\| over\|,\| ms\| \()`). The text equals the patterns. R8's " and " with a digit is fixed. |
| R837-14-R1 to R6 | **Closed** | R1 `:1999-2007` is in the past tense (one tail is R837-15-R3). R2 `:2197` ("were ... the build of one restated since"). R3 `:2246` ("At #810's head's 1x1/1if R4"). R4 `:2304` ("was 123,112 B ... ledgered 58.0 (59.0 at the head)"). R5 `:2382` ("was 125,200 B ... (125,792 B at the head)"). R6 `:2520-2521` ("was taken", "was a pass class of its own"). |
| R837-14-R7, R8 | **Closed** | The Status round-20 bullet reads "Nothing compiled changed, and what executes reads identically". 19.2 item 3 has " and " then a digit. |
| R837-14-S1, S2 | Taken for `:2214` and for section 5's table and `:370`'s first sentence | `:370`'s second sentence is R837-15-F1. `:2300` is retained as optional. |
| R837-13-F1 to F6, R1 to R4 (closed at R837-14) | **Still closed** | No delta since `41ca9f87` touches them. The sweeps reproduce identically at this head (below). |

## What I checked

### The delta and the eight further sites

- `fe1fd541` changes only `docs/design/SPLIT_CONTROL_MEMORY.md`: 27 lines, line count 2,676 both sides.
- I read every changed sentence of `:363-370`, `:1999-2007`, `:2197`, `:2214`, `:2246`, `:2302`, `:2304`, `:2310`, `:2382`, `:2419`, `:2466`, `:2469`, `:2475-2476` and `:2520-2521` against the head's figures.
- **The eight further sites are closed.** Each figure is either now history, or the head's figure with history beside it:
  - `:2302`: "added ... took ... then (122,936 B in 122,880) ... would not have built";
  - `:2304`: "grew by 112 to 120 B";
  - `:2310`: "(59.0 at the head)";
  - `:2419`: "At lever c's head those lines held";
  - `:2466`: "moved 192 B";
  - `:2469`: "was then ... (each image at the head: section 5)";
  - `:2475`: "split";
  - `:2476`: "moved".
- New anchors resolve, including `#the-contingent-moves-908` (the heading at `:2438`), and `doc_paths` passes.
- **Section 5's table `:363-368`:** every head figure equals the `fe0cef5b` column of `rom-per-image.txt`. Each RAMB36 figure follows from rom and sram rounded up to 2,048 B half-tiles:
  - fixture 41.0, 41.5, 54.0, 59.0;
  - platform 42.5, 43.5, 56.0, 60.0.
- `ctrl_plat`'s 17,536, 19,008, 18,176 and 20,288 B (`:370`) equal `ctrl_memory_ledger.py`'s `PLAT_*`.

### Every present-tense byte and RAMB36 statement

- `scripts/byte_sentences.py` lists every sentence with a byte count, KiB, RAMB36, tiles, a granule, a spare or a ledger:
  - section 13 `:1098-2527` (53 sentences, `receipts/s13-byte-sentences.tsv`);
  - section 5 (103, `receipts/s5-byte-sentences.tsv`);
  - FR_NFR 3.4.1 (5);
  - the PR body (9).
- I read every flagged sentence. Results:
  - Section 13: no byte or RAMB36 figure is stated as the head's when it is not the head's, inside this PR's text. `:2494`'s present-tense images are the head's. The pre-existing `:2275` is S1, and `:1549` is base text, KLJ2-labelled by context.
  - FR_NFR 3.4.1: only clause values and the rings' 6,144 / 21,504 B.
  - The PR body: its image figures (`:57`, `:123`) are the head's: 130,920 B, 152 B spare, 129,624 B, 111,024 B, 41.0.
  - Section 5, inside the delta: `:370`'s second sentence (F1).

### Rows, loads, bounds and the FR_NFR delta

These were run at the head:
- `flip_grade.py --check --point 1x1/1if` rc 0, byte-identical to the author's `local-fe1fd541/flip_check_1x1.log`: R4 13.10 within 20, R5 74.07 and R6 69.86 within 90, first 14.66 within 20, last 127.21 within 130, R4L 188.48 within 238, ACMP 28.95, ADP 27.30, MAAP 27.42 within 30, tx 33.38 and txL 48.43 within 49.
- These exit 1 by design (8x8/2if reported, #890) and are byte-identical to round 20's receipts: the check over both points, `--point 8x8/2if`, and `--design as-built`.
- `load_grade.py --check` rc 0: 0.516 and 0.512 at 1x1/1if, 0.794 and 0.754 at 8x8/2if, 32x32/2if 2.175 and 1.684 (2.41x).
- `tier_grid.py --point 1x1/1if` chooses "slice 950 us, tier 1 aecp-first, tier 2 srp-first, AECP queue, cap 2, least margin +0.0116".
- Every figure the delta states matches the head's: `:2520` and FR_NFR `:390-393`, the PR Status table, and the 8x8/2if line (`:59`). The figures are 14.66, 20.93 stated 22, 33.38 within 49 at `CTRL_LOOP_TX_MS` 34 and 99, 127.21 beside 125.84, and 975, 1,010, 735, 1,030, 1,995 and 1,215 us (`ctrl_loop.h:326-328`).

### The four sweeps' completeness claims

- I reran the author's published scripts (`author-r20/scripts/`, run with `-I`, outputs under my packet) on this clone at the head.
- Results:
  - `constant_history.py`: 126 snapshots, 73 moved.
  - `figure_sweep.py`: 797 files, 828 hits, 543 without a history marker.
  - `figure_classify.py` rc 0: another 267, beside 86, head 15, historical 452, reported 8, unclassified 0. The receipt is **byte-identical** to `local-fe1fd541/figure-classes.txt` (sha256 `b039a100…`).
  - `removed_constants.py`: 10 gone, 8 lines (`:1970`, `:2010`, `:2519`, `:2522` and body `:585`, `:586`, `:612`, `:773`), all history.
  - `retired_artifacts.py`: 1 file, 15 lines, 8 in documents/header/docstring and 7 in the body, all history.
- These equal every count the body and REVIEW READY state. At `41ca9f87`, sweeps 1 and 3 had 261 + 567 = 828 hits, and their per-class sums equal the head's.
- **The stated reach equals the patterns** (F2 above). The limits are stated, and F1 sits inside a stated limit ("a figure beside neither a name nor a listed subject"). So the sweep claims are exactly true. The failure is the read's scope (S3), not a sweep claim.
- One note: `figure_classify.py` prints "current with a superseded figure: 0" as a literal, not a count. Its real guard is "unclassified 0" and exit 1 on any unclassed hit, and the body's claim rests on that guard.

### The carries

- **Images:** round 16's `image-compare.txt` gives 0 of 332 files differing at `b6f5c638` from `234bc149` (round 14: 0 of 332, 14 of 14 ELFs). From `b6f5c638` to the head, `sw/` and `tb/` change only:
  - the `aecp_mbx.h` comment, whose preprocessed token stream (`-fpreprocessed -dD -E`) is identical at `b6f5c638` and HEAD (sha256 `2b5d8a6e…`);
  - the harness README;
  - `rows_grade.py`'s docstring. Its AST without the docstring is identical to `26898c05`'s, positions included, at 428 lines (`receipts/probes/head_probes.log`).
- **Self-tests** at the head, all rc 0: `flip_grade.py --selftest` 585 of 585, `rows_tiers.py --selftest` 1,033 of 1,033, `load_grade.py --selftest` 26 of 26, `record_classes.py --selftest` 11 of 11.
- **`tx_statements`** returns `[]` over both points and at each point alone.
- **Probe (Tests, Robustness):** `CTRL_LOOP_TX_MS` planted in memory (no file written):
  - `34u : 98u` is refused at 8x8/2if alone ("states 98 ms, under the built design's tx row 98.49");
  - `33u : 99u` is refused at 1x1/1if alone (33.38);
  - the head's `34u : 99u` and an over-statement `35u : 100u` are accepted, as the rule is "at or over its row".
- **`CTRL_LOOP_TX_MS`** is compiled only into `ctrl_loop.c:203`'s one-interface `_Static_assert`, so round 16's 98 → 99 changes no image.
- **Comment rule:** the delta's added source comments and docstrings (`aecp_mbx.h`, `rows_grade.py`, `rows_tiers.py`, `flip_grade.py`) name no lane, round, reviewer or comment ID.

### Documentation gates on a clean clone

- I made a clean clone of the head: `git clone --no-checkout`, then `git checkout --detach fe1fd541`, with 0 changed paths before and after. These were all rc 0:
  - `docs_check` (0 findings, 219 md files);
  - `check_em_dash` against `66adb9a9`, `cec88385`, `867faf1e` and `41ca9f87`, with the pinned renderer (339 of 339 arms, 0 findings);
  - `doc_style`, `gptp_docs` and `DOC_MAP.gen.py --check`;
  - `solution_docs`, `submodule_docs` (6 exact gitlinks) and `feature_status`;
  - `doc_paths` (1,166 paths resolve) and `archive`;
  - `git diff --check 66f71326 HEAD`.
- Four code-quality gates refuse to run without initialised submodules: `cpp_idiom`, `py_idiom`, `todo_ownership` and `hygiene --check`. I ran them in the review clone, which is clean, at the exact head, with its pinned submodules. All were rc 0. The receipts are in `receipts/docs-gates/`.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `flip_grade.py --check --point 1x1/1if` rc 0, byte-identical to the author's receipt (every row within its tier bound, the last notice within the amendment's 130 ms). `load_grade.py --check` 0.516 / 0.512 ≤ 0.70. `tier_grid.py` 950 us. FR_NFR `:390-393` delta against those outputs. 8x8/2if reported by decision (#890). Every image within its cap (`rom-per-image.txt`, section 5 `:365-368`) | R837-15 | `fe1fd5413afca1352b6990a732ac84512b874ab6` |
| RTL | CLEAN | `git diff --stat 867faf1e..fe1fd541`: no HDL, constraint or synthesis file. Firmware delta: an `aecp_mbx.h` comment (token stream identical) and `ctrl_loop.h:371` `CTRL_LOOP_TX_MS` (compiled only into `ctrl_loop.c:203`'s one-interface assert). Image identity 0 of 332 (round 16's receipt) | R837-15 | `fe1fd5413afca1352b6990a732ac84512b874ab6` |
| Robustness | CLEAN | The delta changes no executable behaviour. `rows_tiers.tx_statements` refuses an under-statement at each interface count, at its own point, and accepts the head's and an over-statement (`receipts/probes/head_probes.log`). `[]` at both points | R837-15 | `fe1fd5413afca1352b6990a732ac84512b874ab6` |
| Tests | CLEAN | Self-tests 585, 1,033, 26 and 11 of as many, rc 0. `flip_grade.py:180` plants each leg under its row. The four sweeps rerun with every count and the class receipt byte-identical. The stated reach equals `figure_sweep.py`'s patterns. The `rows_grade.py` AST is identical | R837-15 | `fe1fd5413afca1352b6990a732ac84512b874ab6` |
| Docs | **UNCLEAN** | `SPLIT_CONTROL_MEMORY.md:370` (F1). Live PR body `:25`, `:788`, `:812`, `:839`, and no REVIEW READY for the head (F2). Otherwise every delta sentence and every byte/RAMB36 sentence listed above. Docs gates rc 0 | R837-15 | `fe1fd5413afca1352b6990a732ac84512b874ab6` |

- R838-9's POSITIVE at `867faf1e` counts as the ancestor review for the code before the delta.
- This round covered the whole delta `867faf1e..fe1fd541`, so the four clean lenses are banked at this head.
- Docs re-opens at the commit and PR edit that answer F1 and F2.

## Real limits

- **I did not rebuild the images.** The author's build needs their private flash maps and runtimes, and the published receipts give hashes, not sizes, for rounds 13 to 16. The head's rom figures rest on this chain of receipts and identity:
  - round 12's `rom-per-image.txt` (`fe0cef5b`);
  - round 13's equal-size statement for the slice change (`:2498`, `:2509`; the one-interface `ctrl_loop.o` differs at equal sizes);
  - rounds 14 and 16's 0-of-332 identity;
  - my token, AST and diff checks since `b6f5c638`.
- **Not rerun by me:** the harness self-test (`ctrl_service_budget/run.py --self-test`), the firmware campaigns, the CPU budget harness legs, and every bank. The author's receipts are at `41ca9f87` and `234bc149`. The delta since then changes no compiled output, and the only change to what executes is `rows_grade.py`'s docstring, whose parse I verified.
- **Hosted evidence:** at review time the exact head's hosted checks were still running. `rtl-fast`'s firmware jobs and `full-ci-gate` were complete and successful. Verilator shards 0 to 18 and Yosys shards 0 to 3 were mostly queued or in progress, `firmware-unit` and `elaborate-gates-1` were in progress, and Physical gPTP was skipped. I claim no hosted or act result.
- **No manager source bank** runs at this head, and I infer none. Physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- The current-dev merge candidate (source base `66f71326`, live dev `6b66f66d`): the builder and native banks at the merge turn.
- Hosted and act acceptance at the exact head.
- Routing F1 and F2: one documentation commit and a PR-body / REVIEW READY update. Then a re-review of Docs at the resulting head.
- Carrying R837-15-R1 to R3 to the residue checklist.
- #916 stays open, outside this lane.

## Receipts (this packet)

- `scripts/byte_sentences.py` and `scripts/head_probes.py`.
- `receipts/s13-byte-sentences.tsv`, `receipts/s5-byte-sentences.tsv`, `receipts/frnfr341-byte-sentences.tsv` and `receipts/prbody-byte-sentences.tsv`.
- `receipts/gates/` (the flip, load and model self-tests and checks, and `tx_statements`).
- `receipts/docs-gates/`.
- `receipts/probes/`.
- `receipts/sweeps/` (the reruns of the author's four sweeps and classifiers).

R837-15 FINISHED
