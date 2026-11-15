[A773] REVIEW READY
Commit: `4ae887a1` (PR #902, `894-tiers` -> `dev-soft-core`; two commits on round 17's `478ff78c`, `6ef3be3b` and `4ae887a1`; the manager pushes)

Round 18 answers R837-11 (PR #902 issuecomment-6892594920), NEGATIVE on three MINORs at `478ff78c`. It changes one Markdown file, plus the PR body.

Changed:
- **R837-11-F1** (`6ef3be3b`): section 13's queued-notice table (`:2204-2205`) gives the head's rows, with `12180198`'s at the 1,200 us slice beside them:
  - 1x1/1if: 14.66 ms held to 20, and 127.21 ms held to 130;
  - 8x8/2if: 20.93 ms (stated 22) and 806.60 ms (stated 62, ceiling 70), reported.
  `:2207` names decision D's 20 ms for the first notice and the amendment's 130 ms for the last (`AECP_QUEUED_MS`; decision D's 125 before it). The cells equal `flip_grade.py --check` at both points.
- **R837-11-F2** (`6ef3be3b`): `:2477` gives `EDIT_RECORD_US`'s 260 and 325 us as round 11's, and the head's 300 and 595, the paced class's dearest member's, beside them.
- **R837-11-F3:** the reviewer's mechanical method is adopted and credited.
  - `scripts/constant_history.py` is copied unchanged: 125 snapshots from `66f71326`, 73 constants moved.
  - `scripts/figure_sweep.py` keeps the reviewer's rules, ROW and LOAD, and adds one AUTO rule per moved constant: the constant's own name beside any number its history held and the head does not.
  - ROW holds every two-decimal ms figure against the head's rows (`flip_grade.py --check` at both points); LOAD does the same for the head's loads.
  - `scripts/figure_classify.py` classes every hit and exits 1 on any it does not class.
  - The completeness claims in the PR body (Status, 14.1, 15.1, 16.5, 17.2, and the R837-8-F1 row) are now stated of their own sweeps' hits, and say what each missed.
- **Found by reading the sweep's hits,** each now history with the head's figure beside it (`4ae887a1`):
  - `:2284`: the "#32 moves" table's `item.acmp` row, now 55/55 and 70/70 us at the head;
  - `:2287`: round 30's ACMP owed frame, 125 us;
  - `:2379`: the long record's states, beside the head's 87,895 and 146,678 cycles;
  - `:2476-2477`: the one-row edit cut's measurements;
  - `:2520`: THE RETRY's pre-tiers 20 ms bound, beside the head's first queued notice.
- **R837-11-R1 to R4,** as the report gives them: `:2427`, `:2432`, `:2244`, and the PR body's round-12 narrative.
- **The PR body** (the packet's `PR-BODY.md`) gains a Round 18 section and rows.

Validation (clean clone of `4ae887a1`, 0 changed paths before and after):
- **The sweep at the head:** 824 hits.
  - **By class:** 457 historical, 75 beside the head's figure, 15 the head's own, 269 another quantity, and 8 that name #916.
  - **Unmarked hits:** 541 carry no history marker. Each is classed by its own line, or by a region whose every hit was read.
  - **The claim, exactly:** every hit of this sweep is classified, and none states a superseded figure as current. A figure stated beside no moved constant's name or subject, that is neither a two-decimal row figure nor a three-decimal load figure, is outside its reach.
- **What changed:** `git diff --name-only 478ff78c 4ae887a1` lists `docs/design/SPLIT_CONTROL_MEMORY.md` alone. Round 16's image, ELF and statement proofs carry unchanged.
- **Gates,** 24 commands, rc 0 but the two that exit 1 by design (the flip check over both points and at 8x8/2if, whose rows are reported):
  - `docs_check.py`;
  - `check_em_dash.py` from `66adb9a9`, `cec88385` and `478ff78c`;
  - doc style, gPTP docs and `DOC_MAP`;
  - both idiom gates and `git diff --check`;
  - the solution, submodule, feature-status, TODO-ownership, hygiene, doc-path and archive gates;
  - `flip_grade.py --check` at 1x1/1if (rc 0) and `load_grade.py --check` (rc 0);
  - `constant_history.py`, and the sweep and its classifier.

Acceptance criteria (round 18):
- **Item 1** met: the table, at the head's rows.
- **Item 2** met: `EDIT_RECORD_US`.
- **Item 3** met: the mechanical sweep, every hit classified, and each completeness claim exact.
- **Item 4** met: R1 to R4.
- **Item 5** met: the documentation gates on a clean clone.
- **Every row, the load, the pace and the slice are round 13's,** and every image and ELF round 16's.

Open risks/questions:
- **#916** (`milan_dp`'s `kJoinCs = 20`) stays open, outside this lane.
- **R837-10-S1 and S3, and R837-7-S2,** remain optional and untaken; each needs a code change.
- **The packet:** `894-a773/round18/` (PR body, receipts, INDEX).
