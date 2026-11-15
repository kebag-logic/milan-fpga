[R837] POSITIVE - exact head 07ed787ee0448be2360f97e8af01194a499003ee

# R837-18: narrow re-review of the live PR #902 body (issue #894), same head as R837-16 and R837-17

This is an internal, cleared-context, independent review. Head `07ed787ee0448be2360f97e8af01194a499003ee`, tree `697298a1c8a5552b7ecd7f5790ccfbfeaa16cf13`. The review start is PR #902 issuecomment-6897710678. No commit has been made since R837-16 (issuecomment-6897523873) or R837-17 (issuecomment-6897687921). The only artifact that changed is the live PR body, edited at 2026-11-15T16:33:14Z.

**Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR is open.

- **R837-17-F1 is closed at its cause.** Body line 894 now carries R837-17's combined (a)+(b) fix, word for word. I checked each clause against the tree and against a run of my own at this head.
- **R837-17-S1 is taken** at all three sites: `:35`, `:468` and `:511`.
- **The live body differs from the body R837-17 reviewed in only those four lines,** plus one trailing blank line.
- **The whole-body scan found three wording-only items** (R837-18-R1 to R3). Each states a true carry, but names its basis loosely. None of them changes a measurement, verdict or test result, so each is RESIDUE with an exact fix.

## Method

1. **Order followed:** AGENTS.md sections 6 and 7 and the review brief, then R837-17's report (PR #902 issuecomment-6897687921, `receipts/c6897687921.md`), which holds the findings under check. Then the live PR body and its edit history, the tree at this head, and the published evidence: branch `894-review-evidence` at `9c4290b841` and evidence tree `471b48a4`.
2. **The tree** was not re-reviewed, as the brief directs. It is byte-identical to R837-16's and R837-17's head (index hash `2b9aa980…`, `receipts/clone-verify.txt`).
3. **Probes,** all on a disposable clone under `scratch/`, which is not published:
   - the hooks self-test at this head, under a file-read audit hook (`scripts/trace_reads.py`);
   - the import and read closure, intersected with every file changed since `234bc149`;
   - token streams of the two firmware headers at `b6f5c638` and at the head;
   - a reconstruction of the prior body by undoing the four edits (`scripts/reverse_edits.py`).
4. **No GitHub write,** no commit and no Docker. The review clone was left untouched (`receipts/clone-verify.txt`).

## (1) R837-17-F1 at its cause

The live body line 894 now reads: "…its one reader is lane part a's `hooks_selftest`, which ran at round 13's final head, `234bc149`; no later commit touches `tb/verilator/ctrl_service_hooks/` (`git log 234bc149..HEAD -- tb/verilator/ctrl_service_hooks` is empty), and of the files it imports or reads outside that directory, later commits change `poll_grade.py` and `aecp_mbx.h` in comments only and `ctrl_loop.h` in comments and in `CTRL_LOOP_TX_MS`, which none of them reads, so its result carries to the head; run at `07ed787e` it prints the same 28 of 28 checks and 96 of 96 mutants (R837-17's `receipts/hooks_selftest_07ed787e.log`)."

**It is exactly the report's fix.**
- `scripts/reverse_edits.py` finds R837-17's fix text once in the live body.
- The old phrase "identity of its inputs" appears 0 times.
- The word diff against the body R837-17 reviewed (`receipts/body_worddiff_r837-17_to_live.txt`) is that replacement and nothing else on line 894.

**Each clause is true at this head:**

- **"no later commit touches `tb/verilator/ctrl_service_hooks/`":** `git log 234bc149..HEAD -- tb/verilator/ctrl_service_hooks` is empty.
- **"the files it imports or reads outside that directory":**
  - **At run time:** the self-test, run under an audit hook, loaded or opened 37 repository files (`receipts/hooks_selftest_reads.txt`). Intersected with the 11 files changed since `234bc149` (`receipts/name_only_234bc149.txt`), that leaves `ctrl_loop.h` and `poll_grade.py` (`receipts/hooks_reads_changed.txt`).
  - **Conditional reads:** `aecp_mbx.h` is read by `notice_window.py:63,71` and `round_grade.py:28` on paths this run did not take, so naming it is correct and conservative.
  - **Changed files read nowhere in the closure:** the model graders (`rows_tiers.py`, `flip_grade.py`, `rows_grade.py`, `edit_rows.py`) and the changed Markdown files are not loaded. They appear in the closure only inside comments (`receipts/hooks_static_refs.txt`, `receipts/model_grader_importers.txt`).
- **"in comments only … in comments and in `CTRL_LOOP_TX_MS`":** `receipts/closure_changed_diff.txt` holds the `234bc149..HEAD` diff of the three files.
  - `poll_grade.py` changes one `#:` comment line.
  - `aecp_mbx.h` changes comment lines.
  - `ctrl_loop.h` changes comment lines and `#define CTRL_LOOP_TX_MS (… 98u)` to `99u`.
- **"which none of them reads":** the only closure file that names `CTRL_LOOP_TX_MS` is `ctrl_loop.h`, which defines it (`receipts/tx_ms_readers.txt`).
  - The closure's header parsers read `CTRL_LOOP_T_EGRESS_MS` and the join constant instead (`tier1_rows.py:229-257`, `join_grade.py:29-30`), and neither changed.
  - No closure file spells the name any other way.
- **"run at `07ed787e` it prints the same 28 of 28 checks and 96 of 96 mutants":**
  - My run gives rc 0 and "28 of 28 checks pass; 96 of 96 mutants caught" (`receipts/hooks_selftest_07ed787e.log`, `.rc`).
  - Its output is byte-identical to round 13's published receipt minus that receipt's header line (`receipts/hooks_selftest_compare.txt`, empty). Round 13's receipt is `author-r13/receipts/lane/lane-234bc149/hooks_selftest.log`, blob `8f5fe3fd`, re-hashed here (`receipts/r13_hooks_selftest_234bc149.log`).
- **"R837-17's `receipts/hooks_selftest_07ed787e.log`":** it is published at `894-review-evidence` `9c4290b841`, `review-evidence/894-r1/reviews/R837-17/receipts/hooks_selftest_07ed787e.log`. It is byte-equal to my run's log (`receipts/r837-17_hooks_selftest_07ed787e.log`).

**F1: CLOSED.**

## (2) R837-17-S1's three sites

| Site | R837-17 body | Live body | Correct head |
|---|---|---|---|
| `:35` (Status, round 19) | "Three sweeps run at the head" | "Three sweeps run at `26898c05`" | yes: the round-19 gate row names `26898c05` |
| `:468` (16.5) | "run again at the head" | "run again at `b6f5c638`" | yes: 16.6 and the round-16 gate row name `b6f5c638` |
| `:511` (17.2) | "run again at the head," | "run again at `478ff78c`," | yes: the round-17 gate row names `478ff78c` |

**S1: TAKEN, all three sites.**

The body delta since R837-17 is lines 35, 468, 511 and 894, plus a trailing blank line (`receipts/body_diff_r837-17_to_live.txt`).
- **The body R837-17 reviewed:** the edit-history entry at 16:20:36Z, sha256 `4d54a675…`. That is the hash R837-17 recorded (`receipts/body-edit-history.txt`, `receipts/pr902_body_r837-17.md`).
- **The live body:** sha256 `bbcf851a…` (`receipts/pr902_body_live.md`).
- **The reconstruction:** undoing the four edits gives a byte prefix of the prior body. The two differ only by the one trailing newline (`receipts/reverse_edits.txt`).

## (3) Whole-body scan: evidence-at-a-head and carry-basis claims

The pattern "ran at|run at|at the head|final head|carries|carry|carried|identical" gives 86 hits (`receipts/head_phrase_scan.txt`). I read every hit that places a run at a head or carries evidence to one. Hits that only give a figure "at the head" were reviewed by R837-16 against the tree, and no commit has been made since.

**These hold exactly:**
- `:26` and `:37` (Status): "Head `07ed787e`"; "Nothing compiled or executed changed after `41ca9f87`". `git diff --name-only 41ca9f87 HEAD` lists `SPLIT_CONTROL_MEMORY.md` alone (`receipts/compiled_inputs_after_b6f5c638.txt`).
- `:30`, `:32` (rounds 14 and 16: "byte-identical to `234bc149`'s, so round 13's measurements carry"): the identity receipts are at those heads, as R837-16 verified.
- `:35`, `:468`, `:511`: named SHAs (section 2).
- `:265`: "round 13's final head `234bc149`" … "The two differ only in `hooks.py`" … "ran at that head". Confirmed: `git diff --name-only ed0df35b 234bc149` is `hooks.py` alone.
- `:409`, `:524`, `:575`, `:622`, `:702`: each round's `git diff --name-only` claim, and that round 16's (or round 14's) proofs carry.
- `:716`: "Every gate that imports `rows_grade` ran at `41ca9f87`", backed by round 20's packet.
- `:879`: "28 of 28; 96 of 96 mutants caught", reproduced at this head.
- `:894`: "The final head is `07ed787e`", the round-by-round chain, and F1's sentence (section 1). Also "After `c274b9f5` only five Markdown files changed before it": `git diff --name-only c274b9f5 ed0df35b` lists exactly five Markdown files.
- The gate table `:896-923`: each row's head is the head its packet ran at. The round-21 row is `07ed787e`.
- `:925`: "None of the commits after `c274b9f5` changes the compiled firmware output". This is true:
  - Images and ELFs are identical through `b6f5c638`.
  - After `b6f5c638` the only compiled input changed is `aecp_mbx.h`. Its token stream (`gcc -fpreprocessed -dD -E -P`) and its 108-line count are identical to `b6f5c638`'s, and so are `ctrl_loop.h`'s (`receipts/compiled_inputs_after_b6f5c638.txt`).
  - Its stated basis is loose; see R3.

**These carry correctly but name their basis loosely.** All three are RESIDUE, reported together here:

### R837-18-R1: RESIDUE (Docs)

- **Where:** body `:894`: "After `c274b9f5` only five Markdown files changed before it, so the legs' firmware and graders are the head's."
- **Evidence:**
  - Read in its paragraph, "the head" here is round 13's `234bc149`, and the claim is true there.
  - The same paragraph has just said "The final head is `07ed787e`". Read as `07ed787e`, "graders" would be false: `rows_tiers.py` and `flip_grade.py` changed executably in round 16, and `rows_grade.py`, `edit_rows.py` and `poll_grade.py` changed in comments or docstrings after `234bc149`.
  - The paragraph's own round-16 and round-20 links carry those changes correctly. This is the same round-scoped "the head" as R837-17-S1.
- **Why RESIDUE:** the true carry chain is stated beside it. The fix changes no claim.
- **Exact fix:** "so the legs' firmware and graders are `234bc149`'s."

### R837-18-R2: RESIDUE (Docs)

- **Where:** body `:760` (21.5): "Round 20's image, ELF, statement, token-stream and parse proofs, and round 13's measurements, carry to `07ed787e`."
- **Evidence:**
  - Round 20 made no image, ELF or statement proof. Its packet's identity receipts are `identity/tokens.txt`, `identity/rows_grade.txt` and the token and parse gate logs; the evidence tree at `9c4290b841` holds no image or ELF receipt for rounds 17 to 21.
  - 20.11 (`:702`) itself says that "round 16's image, ELF and statement proofs" carry to `41ca9f87`.
  - The carry is true, since `41ca9f87..07ed787e` changes `SPLIT_CONTROL_MEMORY.md` alone.
- **Why RESIDUE:** the proofs exist and the chain is recorded at `:702`. Only the round that owns them is misnamed.
- **Exact fix:** "Round 16's image, ELF and statement proofs, round 20's token-stream and parse proofs, and round 13's measurements, carry to `07ed787e`."

### R837-18-R3: RESIDUE (Docs)

- **Where:** body `:925`: "None of the commits after `c274b9f5` changes the compiled firmware output, as the image and object identity receipts show, round 14's included."
- **Evidence:**
  - The image and object receipts end at `b6f5c638`.
  - For `41ca9f87`'s `aecp_mbx.h` comment, the basis is round 20's token-stream receipt (`:634`, `:702`), reproduced here.
  - The conclusion is true.
- **Why RESIDUE:** the basis exists in the body and the result is unaffected. The sentence just doesn't name the receipt for the last compiled-input change.
- **Exact fix:** "…as the image and object identity receipts show through `b6f5c638`, round 14's included, and after it round 20's token-stream receipt for its one header comment (`receipts/identity/tokens.txt`)."

**No other instance.** No sentence in the live body says evidence ran at a head where it did not run. No other carry basis is untrue.

## (4) R837-16's and R837-17's verdicts at this head

- **No commit, and the tree is byte-identical:** `receipts/clone-verify.txt`, index hash `2b9aa980…`, as both rounds recorded.
- **Conformance, RTL and Robustness:** R837-16's CLEAN verdicts depend on the tree, not on the body, and **stand**.
- **Tests:** R837-17's CLEAN **stands**. Its exact-head hooks self-test is reproduced here.
- **Docs:** re-applied here to the changed body. It is **CLEAN**: F1 is closed, and R1 to R3 are residue.
- **Prior findings:**

| Finding | Status at this head | Evidence |
|---|---|---|
| R837-17-F1 (MINOR, Docs: false carry basis for the hooks self-test) | **Closed** at its cause, by the report's exact fix | body `:894`; `receipts/hooks_selftest_*`, `receipts/hooks_reads_changed.txt`, `receipts/tx_ms_readers.txt` |
| R837-17-S1 (round-scoped "the head" at `:35`, `:468`, `:511`) | **Taken** at all three sites | `receipts/body_worddiff_r837-17_to_live.txt` |
| R837-16-F1, R3 | Still closed; the delta does not touch them | body `:265`, `:894` |
| R837-16-R1, R2 (tree wording, `SPLIT_CONTROL_MEMORY.md:361-370`, `:2003`) | Carried on the residue checklist; the tree is unchanged | `receipts/clone-verify.txt` |
| R837-16-S1, S2 and the older suggestions it retains | Retained, optional; the causes are unchanged | no commit |
| R837-15 and earlier, as R837-16's table records | Still closed | tree byte-identical; the body delta touches none of them |

## Findings

**BLOCKER / MAJOR / MINOR: none.**

**RESIDUE** (wording only; no lens made unclean; for the residue checklist):
- **R837-18-R1 (Docs):** `:894` "are the head's" → "are `234bc149`'s".
- **R837-18-R2 (Docs):** `:760` names round 16's proofs as round 20's; exact fix above.
- **R837-18-R3 (Docs):** `:925` names image and object receipts only; exact fix above.
- **Verification for all three:** read the three lines in the live body.

**SUGGESTION:**
- **R837-18-S1 (Docs):** `:894` cites "R837-17's `receipts/hooks_selftest_07ed787e.log`" with no location. Add the published path (`894-review-evidence`, `review-evidence/894-r1/reviews/R837-17/receipts/hooks_selftest_07ed787e.log`) so a cold reader can open it.

**Comment rule:** there is no source delta in this round, so there is no new instance.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | R837-16's artifacts (`ctrl_loop.h:371`, `FR_NFR.md` 3.4.1 `:380-394`, `aecp_mbx.h:22-27,50`, section 5). Tree byte-identical (`receipts/clone-verify.txt`). The body delta (`receipts/body_diff_r837-17_to_live.txt`) changes no conformance or clause claim | R837-16, carried by R837-17 and R837-18 (no commit) | `07ed787ee0448be2360f97e8af01194a499003ee` |
| RTL | CLEAN | R837-16's artifacts (no HDL, constraint or SoC file in `867faf1e..07ed787e`). Tree byte-identical; the gitlinks are unchanged (`receipts/clone-verify.txt`) | R837-16, carried by R837-17 and R837-18 | `07ed787ee0448be2360f97e8af01194a499003ee` |
| Robustness | CLEAN | R837-16's artifacts (`ctrl_loop.c:203`, `flip_grade.py:172-184`, `rows_tiers.py:929-936`). Tree byte-identical | R837-16, carried by R837-17 and R837-18 | `07ed787ee0448be2360f97e8af01194a499003ee` |
| Tests | CLEAN | `tb/verilator/ctrl_service_hooks/run.py --self-test` at this head: rc 0, 28/28, 96/96, output identical to round 13's (`receipts/hooks_selftest_07ed787e.log`, `receipts/hooks_selftest_compare.txt`). Its traced closure (`receipts/hooks_selftest_reads.txt`). R837-16's tree artifacts | R837-17, re-confirmed by R837-18 | `07ed787ee0448be2360f97e8af01194a499003ee` |
| Docs | CLEAN (residue R1 to R3 only) | Live PR body sha256 `bbcf851a…`: `:35`, `:468`, `:511`, `:760`, `:879`, `:894`, `:896-925`, and every head or carry phrase (`receipts/head_phrase_scan.txt`). The body R837-17 reviewed (`4d54a675…`) and the edit history. Tree docs unchanged (R837-16-R1, R2 are residue) | R837-18 | `07ed787ee0448be2360f97e8af01194a499003ee` |

## Real limits

- **Not re-reviewed:** the tree, as directed. Conformance, RTL, Robustness and the tree artifacts under Tests are carried from R837-16 at this same head, with no commit in between.
- **Not run here:** no source bank, campaign, sweep, Verilator or Yosys suite. The only execution was the hooks self-test, on a disposable clone. No manager source bank is claimed or implied.
- **The read trace's reach:** it records files opened or loaded in the self-test's own process, and does not follow child processes. The run took 4 s and `hooks_selftest.py` itself calls no subprocess. A file read only on a path this run did not take is not listed; `aecp_mbx.h` is such a file, found statically and covered by the sentence. The exact-head output, identical to round 13's, covers the remaining gap for this gate.
- **The scan's reach:** it reads claims that place a run at a head or carry evidence to one. Figures "at the head" were reviewed by R837-16 against the unchanged tree.
- **Hosted state:** read at 2026-11-15T16:41:50Z. 25 completed success, 1 completed skipped, 16 in progress, 14 queued, no completed failure (`receipts/hosted-check-runs.tsv`). This was inspected, not accepted.
- **Hardware:** physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Carry R837-18-R1, R2 and R3 to the residue checklist with their exact fixes, together with R837-16-R1 and R2.
- Hosted and act acceptance at this exact head, and the current-dev merge-candidate validation: builder and native banks, on source base `66f713267f20…` against live dev `6b66f66d89cf…`. Then link their receipts on the PR.
- Publish this packet.

## Receipts

Every receipt is listed in `MANIFEST.sha256`.

| Receipt | What |
|---|---|
| `receipts/pr902_body_live.md`, `receipts/pr902_body_r837-17.md`, `receipts/body-edit-history.txt` | The live body (16:33:14Z, `bbcf851a…`), the body R837-17 reviewed (16:20:36Z, `4d54a675…`), and the edit history |
| `receipts/body_diff_r837-17_to_live.txt`, `receipts/body_worddiff_r837-17_to_live.txt`, `receipts/reverse_edits.txt` | The body delta (lines 35, 468, 511, 894, and a trailing blank line) and the reconstruction |
| `receipts/head_phrase_scan.txt` | 86 head and carry phrase hits |
| `receipts/name_only_234bc149.txt`, `receipts/closure_changed_diff.txt` | The 11 files changed since `234bc149`, and the diffs of the three closure files |
| `receipts/hooks_selftest_reads.txt`, `receipts/hooks_reads_changed.txt`, `receipts/tx_ms_readers.txt`, `receipts/hooks_static_refs.txt`, `receipts/model_grader_importers.txt` | The self-test's traced closure, its changed members, the `CTRL_LOOP_TX_MS` readers, and the static references |
| `receipts/hooks_selftest_07ed787e.log`, `.rc`, `receipts/hooks_selftest_compare.txt`, `receipts/r13_hooks_selftest_234bc149.log`, `receipts/r837-17_hooks_selftest_07ed787e.log` | The exact-head self-test, its comparison with round 13's receipt (blob `8f5fe3fd`), and R837-17's published log |
| `receipts/compiled_inputs_after_b6f5c638.txt` | The compiled inputs changed after `b6f5c638`, with token-stream and line-count identity |
| `receipts/hosted-check-runs.tsv`, `.readtime` | Hosted check runs at the head (inspected, not accepted) |
| `receipts/clone-verify.txt` | The review clone after the probes: HEAD, tree, clean status, index equal to the tree (`2b9aa980…`), gitlinks |
| `receipts/c6897687921.md` | R837-17's report, as read |
| `scripts/trace_reads.py`, `scripts/reverse_edits.py` | The probe scripts |

R837-18 FINISHED
