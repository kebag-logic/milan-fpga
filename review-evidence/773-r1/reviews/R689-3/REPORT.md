[R689] POSITIVE - exact head e658682ed451ba46885225e5b3fc16841f61a5ca

Internal cleared-context independent review R689-3, issue #773 / PR #779.

- Head `e658682ed451ba46885225e5b3fc16841f61a5ca`, tree `5023d9f2e8c37399701a6afc62f39e3054dd0f15`.
- Source base and live dev `a032c6d6e3775f145349d5a495c1e1ad12294936`.
- Previously reviewed head `1b47a3dcff0cb65cb5cebe1f86327429a76f775d`, in R689-2 (issuecomment-6384874659) and R690-2 (issuecomment-6384993033).

This round re-covers the delta and the round-2 findings. The delta is one manager documentation commit on `1b47a3dc`. R689-2-F1 and R690-2-F1 (MINOR, Docs) are resolved at this head. R689-2-S1 was taken and is correct. R689-2-RES1 / R690-2-R1 is fixed. No MINOR, MAJOR or BLOCKER is open. One new RESIDUE and one SUGGESTION follow, with the optional items carried from earlier rounds.

## Method

I reconstructed the task in this order:

1. AGENTS.md, CONTRIBUTING.md (sections 2, 6 and the commit rule), docs/README.
2. Issue #773's frozen scope and ruling (b), carried from R689-1 and R689-2. The issue state is unchanged: there is no new scope or decision comment since R689-2, only the [A664] REVIEW READY (`receipts/public_state.txt`).
3. `git diff 1b47a3dc..e658682e` and the commit metadata.
4. The published evidence tree `review-evidence/773-r1` at `1faf10a1`.
5. The manager's fix note (issuecomment-6384888081) and the current PR body.

I read the round-2 review findings only after my own pass over the diff.

## Delta at this head

`git diff --stat 1b47a3dc e658682e` touches one file, `docs/design/MEDIA_CLOCK_FOLLOWING.md`: +6/-2 in two hunks. Excluding that page, the diff has 0 lines (`receipts/public_state.txt`, `receipts/clone_integrity.txt`). The commit message is one line with no trailers (CONTRIBUTING "Commits: one line, no trailers"). The added lines contain no lane, round, reviewer or comment-ID label.

1. **The `[HOLD]` sentence, `MEDIA_CLOCK_FOLLOWING.md:1887-1890`.** It now reads: "`capture_coherence`'s datapath leg reaches that bound: its largest 2 ms `[HOLD]` maximum is 2,059,807 ns, in 9 of its 23 runs; the other 14 reach 2,059,787 ns, where the five tick spacings take one cycle more."
   - I checked this against the published excerpt `author-r2/receipts/round2/sweep/excerpts/capture_coherence.txt`. Its git blob `c8c9d838`, sha256 `f4c5863a...`, equals its `published_sha256` in the evidence `MANIFEST.json` (481 entries).
   - The excerpt has 31 runs: 23 at 2 ms and 8 at 125 us.
   - The 2 ms maxima are 9 x 2,059,807 and 14 x 2,059,787 ns. The 125 us maxima are 5 x 184,807 and 3 x 184,787 ns.
   - The 20 ns gap is one 50 MHz cycle. The five tick spacings are 5 Ps = 5,208.33 cycles, so they fall at 5,208 or 5,209 cycles. That matches the page's "5,208 cycles at least".
   - The page does not claim every run at 125 us.
2. **The 8x8 CRF corner, `MEDIA_CLOCK_FOLLOWING.md:1857-1860`.** It now reads: "leaves up to 2,714 ns after its timestamp less the applied offset. That is after the hand-over, which is Equation (1)'s TT, so it is transit that the stream's latency budget carries."
   - The figure checks: 18,040 ns, the store-and-forward egress shift, less 15,326 ns, the 8x8 TC spare, is 2,714 ns.
   - The reference is the one `[WIRE]` grades (`:1906-1907`). For a CRF PDU, the timestamp less the applied offset is the instant plus TC (`:1909`), and that is where the spare is measured from.
   - The boundary agrees with the ruled hand-over (`:1820-1821`: the MAC transmit port with the MAC ready and no other frame ahead) and with "The MAC's own backpressure is outside the datapath" (`:1846`). So the corner is transit after TT. It is not a breach of Equation (1)'s upper bound.

## Executed checks at this head

All of these ran in this clone, which was untouched before and after (`receipts/clone_integrity.txt`).

- **`scripts/check_bounds.py <checkout> <capture_coherence excerpt>`: 59 PASS, ALL PASS, rc 0** (`receipts/check_bounds.txt`).
  - It recomputes every #773 figure in exact arithmetic, and requires each one to appear verbatim on the page or in the matrix.
  - Its sentence check now rebuilds the stated sentence from the log: the largest maximum, its run count, the other value and its count. It also requires that the largest maximum equals the derived bound, that the gap is one cycle, and that the earlier "in every 2 ms run" claim is absent.
  - It also checks the new 8x8 CRF wording.
- **Planted control: the same script on the pages as they stood at `1b47a3dc` gives 4 FAIL, rc 1** (`receipts/check_bounds_prior_head_control.txt`). The four failures are the old universal claim present, the new sentence missing, and the two CRF sentences missing. So the check can fail for the defect it was written to detect.
- **Docs gates under the hash-pinned renderer**, installed from `tools/markdown/requirements.txt` (sha256 `40cdefe0...`) into a disposable venv: cmarkgfm 2025.10.22, html5lib 1.1 (`receipts/renderer_install.txt`). Each gate gave rc 0 (`receipts/gates/*.log`):
  - `docs_check.py`: 0 findings over 210 md files and 1,418 scrubbed text files; scrub self-test 23/23.
  - `check_doc_style.py`: OK.
  - `check_doc_paths.py`: OK, 1,062 cited paths resolve.
  - `check_em_dash.py --base a032c6d6`: 0 findings over 202 added lines, arms 339/339.
  - `gen_toc.py --check`: OK, 149 pages.
  - `gen_toc.py --verify-anchors`: 537 cross-page fragment links reproduced.
  - `check_feature_status.py`: 0 findings.
  - `check_solution_docs.py`: OK.
  - `check_hygiene.py --check`: PASS.
  - `check_todo_ownership.py`: OK.

  These agree with the gates the manager's fix note reports at this head.
- **Hosted contexts at the exact head** (`receipts/hosted_check_runs.tsv`, snapshotted while the runs were live):
  - 14 completed success, including `docs-gates-0/1/2`, `docs-check-no-git`, `verilator-lint`, `bdd-conformance` and `full-ci-gate`;
  - 1 skipped (`Physical gPTP (nightly and manual)`);
  - 20 in progress and 11 queued, including `docs-check` and `elaborate-gates-*`.

  I claim none of the pending contexts. The manager owns hosted and act acceptance.

## Prior findings at this head

| Finding | Status at e658682e | Evidence |
|---|---|---|
| R689-2-F1 / R690-2-F1, MINOR, Docs: "in every 2 ms run" | **Resolved.** The page states the measured distribution. The PR body's Round 2 bullet (`receipts/pr_body_snapshot.md:40`) states the same: "largest 2 ms `[HOLD]` maximum 2,059,807 ns in 9 of 23 runs, 2,059,787 ns in the other 14". The REVIEW READY's restatement (issue comment 6384707314) is corrected by the public PR comment 6384888081, which names it. That is the correcting comment R689-2 required. See SUG1 for its placement. | `receipts/check_bounds.txt`, `receipts/check_bounds_prior_head_control.txt`, `receipts/public_state.txt` |
| R689-2-S1, SUGGESTION, Conformance and Docs: name the 8x8 CRF corner's reference and boundary | **Taken, correct**, in the page (`:1857-1860`) and the PR body's Known limitations (`pr_body_snapshot.md:132`). | Delta item 2 above |
| R689-2-RES1 / R690-2-R1, RESIDUE: stale reviewer placeholders | **Fixed.** The body reads "Internal cleared-context reviewer: [R689]" and "External reviewer: [R690]". | `pr_body_snapshot.md:59-60` |
| R689-2-S2, SUGGESTION, Tests: name the files behind the shard tracked-change count | Not taken. Still optional; no effect on coverage. | — |
| R689-1-S3 / R689-2-S3, SUGGESTION, Tests: a measured contended dp case | Not taken. Still optional. | — |
| R689-1-S1, SUGGESTION, RTL and Robustness: guard or state the arbitration-spare condition | Not taken. Still optional. | — |
| R689-1-F1, R690-1-F1, R690-1-F2, R689-1-R1, R689-1-S2 | Resolved at `1b47a3dc` (R689-2). Nothing in the delta reopens them. | R689-2 ledger |

PR #779 has 0 PR reviews and 0 inline threads.

## Findings

### R689-3-RES1 - RESIDUE - Docs - PR body Status still names `1b47a3dc` as the ready head

- **Where:** PR body Status (`receipts/pr_body_snapshot.md:16` and `:32`), and the Contents line "what round 2 changed" (`:5`).
  - `:16` reads "READY FOR REVIEW at `1b47a3dc` (eight commits on dev `a032c6d6`)".
  - `:32` reads "From `13d8f1e8` to `1b47a3dc` only two documentation pages and a comment changed". Nothing in the body names `e658682e` or its commit.
- **Evidence:** the PR head is `e658682e` (nine commits on `a032c6d6`). Every gate row names the head it ran at and claims nothing else, and the docs gates at `e658682e` are public in the fix note and in this report. So no measurement, figure or verdict is wrong. Only the head the status line points to is stale.
- **Exact fix:**
  - At `:16`: "READY FOR REVIEW at `e658682e` (nine commits on dev `a032c6d6`) ... Round 2 adds two commits on `13d8f1e8`: documentation and one comment, no RTL line. A manager commit on `1b47a3dc` changes `MEDIA_CLOCK_FOLLOWING.md` only."
  - Add one gate row: "`docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, `check_em_dash.py --base a032c6d6`, `gen_toc.py --check` / `--verify-anchors` | `e658682e` | rc 0 each".
  - At `:32`, append: "From `1b47a3dc` to `e658682e` only `MEDIA_CLOCK_FOLLOWING.md` changed."
- **Verification:** compare the Status line with `headRefOid`. It is wording only and does not affect coverage.

### R689-3-SUG1 - SUGGESTION - Docs - put a pointer to the correction on the issue thread

- **Where:** issue #773, REVIEW READY 6384707314, line 7: "2,059,807 ns is the `[HOLD]` maximum in every 2 ms run." It is unedited, and was created and last updated at 13:19:40Z.
- **Point:** the correction exists publicly, as PR comment 6384888081. A reader who stays on the issue thread does not see it.
- **Suggestion:** a one-line issue comment pointing to it. Optional, because the required correcting comment exists.

## Clean-lens results

- `[R689] PASS Conformance — MEDIA_CLOCK_FOLLOWING.md:1820-1821,1846,1857-1860,1866-1872,1906-1910 at e658682e; receipts/check_bounds.txt`
  - Checked against IEEE 1722-2016 4.3.3 Equation (1) and ruling (b)'s hand-over.
  - The 8x8 CRF corner is measured from the stamp less the applied offset that `[WIRE]` grades. It falls after the ruled hand-over (TT), so it is transit and not an upper-bound breach.
  - The start-up bound of 2,059,807 ns is inside Milan v1.2 4.4.2.1's 2.126 ms.
  - Every other Conformance artifact is unchanged since R689-2 covered it at `1b47a3dc`; the diff outside this page is 0 lines.
- `[R689] PASS RTL — git diff 1b47a3dc..e658682e -- . ':!docs/design/MEDIA_CLOCK_FOLLOWING.md' (0 lines); receipts/clone_integrity.txt`
  - No HDL, testbench, script or config byte changed, and the gitlinks equal those R689-2 recorded.
  - R689-1's RTL coverage at `13d8f1e8` and R689-2's at `1b47a3dc` stand unchanged. Neither depends on the changed prose.
- `[R689] PASS Robustness — MEDIA_CLOCK_FOLLOWING.md:1881-1890 against the excerpt's 23 2 ms and 8 125 us [HOLD] maxima; diff outside the page 0 lines`
  - The start-up path is graded at both values the five tick spacings can take: 5,208 cycles (9 runs) and 5,209 cycles (14 runs).
  - The derived bound is the largest maximum observed and is not exceeded at either offset.
  - The reset and re-entry conditions and the MAC-level limits are unchanged from R689-2.
- `[R689] PASS Tests — receipts/check_bounds.txt (59/59), receipts/check_bounds_prior_head_control.txt (4 FAIL at 1b47a3dc); evidence MANIFEST.json binding of capture_coherence.txt`
  - The evidence the page cites is bound by digest to the published sweep at `1b47a3dc`. Its tests and RTL are byte-identical at `e658682e`, so that sweep is exact for this head's tests.
  - The sentence check is data-driven and fails on the prior head's text.
  - The dp leg (847/0) and the mutation arm (42/42) were verified in R689-2 and are untouched.
- `[R689] PASS Docs — MEDIA_CLOCK_FOLLOWING.md:1857-1860,1887-1890; MILAN_COMPLIANCE_MATRIX.md:191; receipts/gates/*.log (10 gates rc 0, pinned renderer); receipts/pr_body_snapshot.md:40,59-60,132`
  - The page, the PR body and the matrix ("the `[HOLD]` maximum measured at 1x1") all agree with the log.
  - No tracked doc still carries "in every 2 ms run" or "2,714 ns late" (`git grep`).
  - The only open item is wording residue, RES1.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | MEDIA_CLOCK_FOLLOWING.md:1820-1910 (the delta and the clauses it relies on); matrix:191; check_bounds 59/59 | R689-3 | e658682ed451ba46885225e5b3fc16841f61a5ca |
| RTL | CLEAN | zero-line non-page diff 1b47a3dc..e658682e; gitlinks; carried from R689-2 (1b47a3dc) and R689-1 (13d8f1e8), whose scope is unchanged | R689-3 (delta), with R689-2 for unchanged scope | e658682ed451ba46885225e5b3fc16841f61a5ca |
| Robustness | CLEAN | MEDIA_CLOCK_FOLLOWING.md:1881-1890 against all 31 runs' [HOLD] maxima; zero-line non-page diff | R689-3 | e658682ed451ba46885225e5b3fc16841f61a5ca |
| Tests | CLEAN | check_bounds 59/59 plus the 4-FAIL prior-head control; MANIFEST-bound capture_coherence excerpt; tests unchanged since the sweep head | R689-3 | e658682ed451ba46885225e5b3fc16841f61a5ca |
| Docs | CLEAN (RESIDUE RES1 carried to the checklist) | page delta; matrix; PR body; 10 docs gates under the pinned renderer, rc 0 | R689-3 | e658682ed451ba46885225e5b3fc16841f61a5ca |

## Real limits

- I ran no source bank at this head. Execution evidence for the RTL and tests is the author's published round-2 sweep at `1b47a3dc`, whose code is byte-identical here. I did not run Verilator, Yosys, Vivado, behave or lint this round.
- That five tick spacings take 5,209 cycles in the 14 runs is inferred from the arithmetic and the 20 ns gap. The log does not attribute the cycle, and I added no instrumentation.
- The 8x8 TDM32 figures and the MAC-level figures are derived only. No harness runs that shape at its clocks.
- Physical calibration was NOT RUN. Field and hosted skips are not hardware proof.
- 31 hosted contexts were still queued or in progress when I took the snapshot.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base and live dev `a032c6d6`) with the builder and native banks, and link the receipts on the PR.
- Accept the hosted and act contexts at this exact head once they complete, including `docs-check` and `elaborate-gates-*`.
- Carry R689-3-RES1 to the residue checklist. Optionally act on R689-3-SUG1.
- Obtain the external reviewer's verdict at this head, and the maintainer's explicit merge authorization.

R689-3 FINISHED
