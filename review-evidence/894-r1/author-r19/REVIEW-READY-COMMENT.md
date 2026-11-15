[A773] REVIEW READY
Commit: `26898c05` (PR #902, `894-tiers` -> `dev-soft-core`; one commit on round 18's `4ae887a1`; the manager pushes)

Round 19 answers R837-12 (PR #902 issuecomment-6893024482), NEGATIVE on one MINOR at `4ae887a1`. It changes `SPLIT_CONTROL_MEMORY.md` and `tb/verilator/ctrl_service_budget/README.md`, plus the PR body.

Changed:
- **R837-12-F1:** section 13's `:1970` and `:2010` to `:2016` now read as the 2026-11-05 record's, in the past tense, with what governs under THE TIERS beside them:
  - `CTRL_LOOP_SRP_MS` is removed;
  - SRP's R5 and R6 are tier rows held to decision D's 90 ms, 74.07 and 69.86 ms at 1x1/1if;
  - the first queued notice is a tier row, 14.66 ms within 20 at 1x1/1if, and 20.93 ms at 8x8/2if, stated 22 and reported.
  These equal `flip_grade.py --check` at both points.
- **R837-12-R1 to R5,** as the report gives them:
  - R1, `:2522`;
  - R2, the harness README's `:1490`, "past its 130 ms bound (at 1,250 ms)";
  - R3, the PR body's Contents, Status Round 14 and 14.1, which now name round 14's miss;
  - R4, "copied unchanged but for a one-line provenance comment";
  - R5, the classifier's reason at `ctrl_service_budget/README.md:172`.
- **R837-12-S1, taken:** the removed-constant sweep (`scripts/removed_constants.py`, the reviewer's, credited) and the "by construction" grep.
- **The PR body** (the packet's `PR-BODY.md`) gains a Round 19 section and rows.

Validation (clean clone of `26898c05`, 0 changed paths before and after). Three sweeps, each with its limit:
1. **The moved constants** (`constant_history.py`: 73 constants moved over 125 snapshots from `66f71326`; `figure_sweep.py`'s rules and AUTO rules).
   - **Result:** 256 hits: 133 historical, 56 beside the head's figure, 8 the head's own, 51 another quantity, 8 naming #916.
   - **Limit:** a superseded figure stated beside neither the constant's name nor its prose subject, and any removed constant.
2. **The removed constants** (`removed_constants.py`): 10 constants removed, and 8 lines name one, every one history-framed.
   - **Limit:** a removed constant's bound stated without its name.
3. **The rows and loads** against `flip_grade.py --check` at both points (ROW and LOAD).
   - **Result:** 566 hits: 324 historical, 19 beside, 7 the head's own, 216 another quantity.
   - **Limit:** a row or load figure in another precision, or in a sentence naming neither a row nor the load.
- **"by construction"** in section 13 appears at `:1970`, `:2351` and `:2519`, each history.
- **The claim, exactly:** every hit of the three sweeps at `26898c05` is classified, and none states a superseded figure or a removed constant as current. Each sweep's limit is as stated.
- **What changed:** `git diff --name-only 4ae887a1 26898c05` lists the two Markdown files alone. Round 16's image, ELF and statement proofs carry unchanged.
- **Gates,** 27 commands, rc 0 but the two that exit 1 by design (the flip check over both points and at 8x8/2if):
  - the documentation and idiom gates;
  - `flip_grade.py --check --point 1x1/1if` (rc 0) and `load_grade.py --check` (rc 0);
  - the three sweeps, their classifiers, and the grep.

Acceptance criteria (round 19):
- **Item 1** met: F1.
- **Item 2** met: the removed-constant sweep and the grep.
- **Item 3** met: R1 to R5.
- **Item 4** met: each completeness claim is stated of its sweep, with its limit.
- **Item 5** met: the documentation gates on a clean clone.
- **Every row, the load, the pace and the slice are round 13's,** and every image and ELF round 16's.

Open risks/questions:
- **#916** stays open, outside this lane.
- **R837-10-S1 and S3, and R837-7-S2,** remain optional and untaken; each needs a code change.
- **The packet:** `894-a773/round19/` (PR body, receipts, INDEX).
