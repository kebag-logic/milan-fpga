[A773] REVIEW READY
Commit: 07ed787ee0448be2360f97e8af01194a499003ee

PR #902, `894-tiers` -> `dev-soft-core`, head `07ed787e`: twenty-eight commits on round 11's `9606b3a9`. The manager pushes.

Round 21 answers R837-14 (PR #902 issuecomment-6894240714) at `41ca9f87` and R837-15 (issuecomment-6896987271) at `fe1fd541`, each NEGATIVE on two MINORs. Since round 20's REVIEW READY (issuecomment-6893619187, `41ca9f87`) there are two commits, both changing `docs/design/SPLIT_CONTROL_MEMORY.md` alone.

Changed:
- **`fe1fd541`,** round 20's local commit, which the owner landed in #902:
  - R837-14-F1: `:2382` gives the head's 1x1/1if fixture image, 111,024 B, with 110,800 and 110,576 B (40.5 RAMB36) as history;
  - R837-14-R1 to R6, S1 and S2;
  - eight further image, ledger and record-era sites, each now history: `:2302`, `:2304`, `:2310`, `:2419`, `:2466`, `:2469`, `:2475`, `:2476`.
  - Its gates and sweeps on a clean clone: 26 commands, rc 0 (round 20's packet, `receipts/local-fe1fd541/`).
- **`07ed787e`:**
  - R837-15-F1: section 5's `:370` gives the head's 8x8/2if platform image, 130,920 B in 131,072, 152 B before the 60.0 granule, with the ruling's head's 130,328 B and 744 B as history.
  - S3, taken: a byte and RAMB36 read of the section-5 paragraphs this PR writes (`:265-273`, `:335-348`, `:361-372`, the reviewer's `byte_sentences.py`). It found three more sites, now history beside the head's:
    - `:335`: the pin move's `ctrl_plat` sizes; the head's, from the platform images' symbol tables, are 17,536, 19,008, 18,176 and 20,288 B;
    - `:346-347`: round 29's fixture and platform images;
    - `:348`: the round-25 arm's 58.0 and 58.5 ledger.
  - R3: `:2006`.
- **The PR body** (the packet's `PR-BODY.md`):
  - R837-15-F2: it names `07ed787e` in the Status, the How-to, the final-pass text and the gate table, records R837-14-F1 as fixed in the tree at `fe1fd541` and links its receipts;
  - R1 and R2;
  - S4: the ROW and LOAD keywords are matched case-sensitively, as written.

Validation (clean clone of `07ed787e`, 0 changed paths before and after):
- **What changed:** `git diff --name-only 41ca9f87 HEAD` lists `docs/design/SPLIT_CONTROL_MEMORY.md` alone. Round 20's image, ELF, statement, token-stream and parse proofs carry unchanged, and so do round 13's measurements.
- **Gates,** 29 commands, rc 0 but the flip check at 8x8/2if, which exits 1 by design:
  - the documentation and idiom gates;
  - `flip_grade.py --check` at both points and `load_grade.py --check`;
  - the section-5 byte read.
- **The four sweeps,** over the final PR body, each with its reach and limit as 19.2 states them:
  - moved constants: 261 hits;
  - rows and loads: 567 hits;
  - removed constants: 8 lines;
  - retired artifacts: 15 lines.
  Every hit is classified, and none states a superseded figure, a removed constant or a retired file as current.

Acceptance criteria (round 21):
- **Item 1** met: F1, and S3 with its three further sites.
- **Item 2** met: F2; the head is named throughout, and this REVIEW READY gives its full SHA.
- **Item 3** met: R1 to R3, and S4.
- **Item 4** met: the docs gates and the four sweeps on a clean clone.
- **Every row, the load, the pace and the slice are round 13's,** and every image and ELF round 16's.

Open risks/questions:
- **R837-15-S1 and S2** (`:2275`, `:483`) are base text outside this PR's delta, and optional; they are not taken.
- **#916** stays open, outside this lane.
- **The packet:** `894-a773/round21/` (PR body, receipts, INDEX).
