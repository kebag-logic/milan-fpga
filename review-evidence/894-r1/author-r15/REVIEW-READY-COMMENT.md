[A773] REVIEW READY
Commit: `6b759b30` (PR #902, `894-tiers` -> `dev-soft-core`; one commit on round 14's `867faf1e`; the manager pushes)

Round 15 changes two Markdown files and the PR body. It answers round 14's delta reviews:
- R837-8 (PR #902 issuecomment-6891424100): NEGATIVE, on one MINOR;
- R838-9 (issuecomment-6891425121): POSITIVE.

Changed:
- **R837-8-F1** (`6b759b30`):
  - `FR_NFR.md:383` now reads "8 ms held it, txL 48.09 ms and R4L 188.39 ms", and where it states the head, "8 ms holds txL, 48.43 ms, and R4L, 188.48 ms".
  - `SPLIT_CONTROL_MEMORY.md:2467` is past tense, with "48.43 and 188.48 at the head" beside the old figures.
  - The sweep used tokens from every row of section 13's rows-history table, not only the last four. It found more present-tense superseded figures, now past tense or beside the head's: `:2351`, `:2380`, `:2402`, `:2466` (a counterfactual, now conditional) and `FR_NFR.md:387`.
  - **The grep receipt** (`receipts/stale-rows-grep.txt`):
    - 123 tokens: every figure of every earlier row (R4, R4L, ACMP, ADP, MAAP, the first and last queued notice, R5, R6, tx and txL), and every earlier load figure.
    - The scope is section 13, FR_NFR 3.4.1, MAILBOX_SPLIT, the READMEs and the code files outside table lines, plus every line of the PR body.
    - 141 hits: 96 historical, 30 beside the head's figure, 15 another quantity. None is current with a superseded figure.
- **The residues:**
  - R837-8-R1 and R838-9-R1: the R838-6-F2 row cites `:2525`.
  - R837-8-R2: the `:2509` sentence is past tense.
  - R837-8-R3: PR body 14.1 now names exactly the sites with the head's figure beside the old one, and says that round 14's tokens held no row figure.
  - R838-9's note on item 5: `:2509` now says both domains are held in reset until the PLL locks, each released through its own synchronizer.
- **R837-8-S1, taken:** the row tokens are generated from the rows-history table (`scripts/stale_rows.py`).
- **The PR body** (the packet's `PR-BODY.md`) gains a Round 15 section and finding rows.

Validation:
- **What changed:** `git diff --name-only 867faf1e 6b759b30` lists `docs/design/SPLIT_CONTROL_MEMORY.md` and `docs/reference/FR_NFR.md` only. No file under `sw/`, `tb/`, `hw/`, `syn/` or `scripts/` changes, so round 14's identity proof and round 13's measurements carry.
- **Gates,** on a clean clone of `6b759b30`, 29 commands, each rc 0:
  - `docs_check.py`;
  - `check_em_dash.py` from `66adb9a9`, `cec88385` and `867faf1e`;
  - doc style and gPTP docs, each with its self-test; `DOC_MAP.gen.py --check`;
  - both idiom gates with their self-tests; `git diff --check`;
  - the solution, submodule, feature-status, TODO-ownership, hygiene, doc-path and archive gates;
  - round 14's cost-figure grep (64 hits, each classified as before) and the row sweep.

Acceptance criteria (round 15):
- **Item 1** met: both sites, the full row sweep, and every hit classified. PR body 14.1 is now literally true.
- **Item 2** met: R1, R2 and R3.
- **Item 3** met: documentation and PR body only, and the documentation gates on a clean clone.
- **The head's figures are round 13's:** R4 13.10, R4L 188.48, ACMP 28.95, ADP 27.30, MAAP 27.42, the first queued notice 14.66, R5 74.07, R6 69.86, the last queued notice 127.21, tx 33.38 and txL 48.43 ms. The load is 0.516 and 0.512, and the pace 8 ms.

Open risks/questions:
- **R837-8-S2 is not taken.** The precondition is stated in section 13 and the receipt, which the review finds sufficient.
- **The packet:** `894-a773/round15/` (PR body, receipts, INDEX).
