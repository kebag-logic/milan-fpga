[A773] REVIEW READY
Commit: `867faf1e` (PR #902, `894-tiers` -> `dev-soft-core`; two commits on round 13's `234bc149`; the manager pushes)

Round 14 changes documents and comments only. It answers round 13's delta reviews:
- R837-7 (PR #902 issuecomment-6890948441): NEGATIVE, on one MINOR;
- R838-7 (issuecomment-6890766701): NEGATIVE, on one MINOR;
- R838-8 (issuecomment-6890858159): POSITIVE.

Changed:
- **R837-7-F1** (`b25530f6`): every current-tense figure the round-12 and round-13 moves touched now gives the head's figure, or is stated as history.
  - The moves: a build of one 725 to 735 us, a TICK 50 to 55, AECP's timer slot 65 to 70, a LINK 150 to 155, the SRP drain 250 to 280, the slice 900 to 950 us, the load 0.515 and 0.511 to 0.516 and 0.512, and every row.
  - Section 13: `SPLIT_CONTROL_MEMORY.md:2197` reads 735. Also `:2342`, `:2373`, `:2380`, `:2443` to `:2445`, `:2459`, `:2467`, `:2477`, `:2479`, `:2480`, `:2489` and `:2509`.
  - `FR_NFR.md:383` (3.4.1). `sw/firmware/ctrl/srp/README.md:238` reads 33.38 ms at the 950 us slice, with 33.01 at 900 us as history.
  - `poll_grade.py:70`, a comment the sweep found: 280 and 365 us (it said 250 and 365).
  - The grep receipt has 64 hits of the eleven tokens: 36 historical and 28 another quantity, none current with an old value (`receipts/stale-figures-grep.txt`).
- **R837-7-R1** (`b25530f6`): the comment at `ctrl_loop.h:321` reads as the review gives it.
- **R837-7-S1, taken** (`b25530f6`): item 5's precondition is now stated. `cd_milan` is a clock output of the PLL that makes `cd_sys` (`milan_soc.py:282`, `:288`), and LiteX makes each such domain's reset the PLL's lock, so both leave and enter reset together. A datapath clock or reset of its own would reopen the late path. It is stated in section 13 where item 5 is, and in `receipts/item5-no-late-completion.md`.
- **R838-7-R1** (`867faf1e`): `edit_rows.py:3`'s docstring names "its SET_CONFIGURATION ruling, item 3", not the comment ID. It is rewrapped within its nine lines.
- **The PR body** (the packet's `PR-BODY.md`) gains a Round 14 section and rows for R837-7 and R838-7/8. The two sites corrected before round 14 are kept as corrected.
- **R837-7-S3, taken** (the packet): no file in it carries a host path, scripts included, so its INDEX hashes are the published bytes. INDEX states that the outer manifest is authoritative for an earlier packet's redacted scripts.

Validation (no leg, no sweep):
- **Images:** 332 of 332 image files (8 ELFs, 8 binaries, 316 objects) are byte-identical to `234bc149`'s at `b25530f6` and at `867faf1e`, on one clone path.
- **Harness ELFs:** the 14 harness legs' ELFs were linked again at both heads, each from its leg's own build parameters and flash map. All 14 are identical, and equal to round 13's own leg builds.
- **Sources:** `ctrl_loop.h`'s token stream is identical. `poll_grade.py`'s AST is identical, positions included. `edit_rows.py`'s AST is identical but for its docstring, which nothing reads.
- **Gates,** on a clean clone of `867faf1e`, 28 commands, each rc 0:
  - `docs_check.py`;
  - `check_em_dash.py` from `66adb9a9`, `cec88385` and `234bc149`;
  - doc style and gPTP docs, each with its self-test; `DOC_MAP.gen.py --check`;
  - both idiom gates with their self-tests; `git diff --check`;
  - the solution, submodule, feature-status, TODO-ownership, hygiene, doc-path and archive gates;
  - the stale-figure grep.

Acceptance criteria (round 14):
- **Item 1** met: the sweep and its grep receipt.
- **Item 2** met: the comment, with no token changed.
- **Item 3** met: the precondition, in the receipt and in section 13.
- **Item 4** met: identity by sha256, token stream and AST, then the documentation gates. Nothing was rerun.
- **Item 5** met: the PR body's round-14 section and finding rows.
- **The head's figures are round 13's,** since every input is identical:
  - R4 13.10, R4L 188.48, ACMP 28.95, ADP 27.30 and MAAP 27.42;
  - the first queued notice 14.66, R5 74.07, R6 69.86 and the last queued notice 127.21;
  - tx 33.38 and txL 48.43 ms;
  - the load 0.516 and 0.512, the pace 8 ms, and the slice rule choosing the built 950 us.

Open risks/questions:
- **R837-7-S2 is not taken.** Holding an unanswered over-cost record in arm B's `aecp-fanout` needs an executable change, so the PR body lists it under Known limitations.
- **R838-8-S1 is not taken.** The corrected R838-6-F2 row is kept as it stands.
- **The packet:** `894-a773/round14/` (PR body, receipts, INDEX).
