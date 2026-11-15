[A773] REVIEW READY
Commit: `b6f5c638` (PR #902, `894-tiers` -> `dev-soft-core`; two commits on round 15's `6b759b30`; the manager pushes)

Round 16 answers R837-9 (PR #902 issuecomment-6891685454), NEGATIVE on two MINORs at `6b759b30`, under the manager's maintainer-delegated ruling.

Changed:
- **R837-9-F1** (`eed2e40d`): `aecp_mbx.h:50` now reads "txL was 49.69 ms at 7 ms, and 8 ms did". It is a comment only: the token stream is identical and the line count unchanged.
- **R837-9-F2, outcome 1** (`b6f5c638`):
  - `CTRL_LOOP_TX_MS` is now `(MBX_N_IF == 1u ? 34u : 99u)`: 99 ms at two interfaces, the 8x8/2if tx row's 98.49 rounded up.
  - The literal control strings are updated at `rows_tiers.py:932/934` and `flip_grade.py:174-184`. Both controls now plant the two-interface leg:
    - `rows_tiers` plants both legs under their rows and requires a refusal at each point;
    - `flip_grade` plants each leg alone and requires the refusal by name at its own point, since 8x8/2if's flip check exits 1 by design.
    - `rows_tiers.py` stays at its 1,000 lines.
  - **Documents:** `:2351` now reads "stated as 30 and 98 ms. At the head it states 34 and 99 ms". `:2004` and `:2521`, which gave the pre-tiers 44 ms as current, now mark it as before THE TIERS. The harness README names both points.
- **The PR body** (the packet's `PR-BODY.md`) gains a Round 16 section and rows for R837-9-F1, F2, S1 and S2.

Validation (clean clone of `b6f5c638`, 0 changed paths before and after):
- **Item 2:**
  - `rows_tiers.tx_statements(root)` returns `[]` at both points. At `6b759b30` it returned the 8x8/2if line.
  - `flip_grade.py --check --point 1x1/1if`: rc 0.
  - The self-tests refuse 1,033 of 1,033 and 585 of 585.
  - With `tx_statements` made blind to 8x8/2if, both controls escape by name (`receipts/statements/controls-probe.txt`).
- **Item 3:**
  - 332 of 332 image files are byte-identical to `234bc149`'s, on one clone path.
  - All 14 harness legs' ELFs are identical to `234bc149`'s.
  - The objects carry no debug or macro sections. `ctrl_loop.h`'s token stream differs only by `98u` -> `99u`. No STOP.
- **Item 4, statement checks:** every statement check at both points, published in `receipts/statements/`.
  - These return `[]` at both points: `tx_statements`, `unrowed`, `edit_rows.findings`, `queued_bound.statements`, `paced_rows.statements` and `count_findings`, and `load_grade.srp_unit` and `findings`.
  - `rows_tiers.findings` lists only 8x8/2if's reported rows.
  - `load_grade --check`: rc 0. `flip_grade --check --point 8x8/2if` now lists rows alone.
  - Every stated table against round 13's measured costs equals round 13's output: the class lines only.
  - `record_classes.py` over round 13's legs: RESULT PASS, equal to round 13's output.
- **Item 4, comment sweep:**
  - It covers every comment and docstring under `sw/` and `tb/`, 766 files.
  - It used 144 tokens: rows, loads, and txL and R4L at every pace at either point, plus the cost figures in context.
  - 15 hits: 4 historical, 3 beside the head's figure, 8 another quantity. None is current.
  - The same sweep finds F1 at `6b759b30`.
- **Item 5, 35 commands, each rc 0:**
  - the model self-tests;
  - the firmware unit gate's AECP and loop arms (18 arms, PASS);
  - the documentation and idiom gates;
  - round 14's cost grep and round 15's row sweep (every hit classified);
  - the comment sweep and the controls probe.

Acceptance criteria (round 16):
- **Item 1** met.
- **Item 2** met, by outcome 1.
- **Item 3** met: identical images and ELFs.
- **Item 4** met: every statement check at both points, and the sweep.
- **Item 5** met.
- **The head's figures are round 13's:** R4 13.10, R4L 188.48, ACMP 28.95, ADP 27.30, MAAP 27.42, the first queued notice 14.66, R5 74.07, R6 69.86, the last queued notice 127.21, tx 33.38 and txL 48.43 ms. The load is 0.516 and 0.512, and the pace 8 ms. At 8x8/2if tx is 98.49 ms, within the stated 99.

Open risks/questions:
- **The 8x8/2if rows** stay reported (#894's decision of 2026-11-12). Only the statement controls hold that point's statement.
- **The packet:** `894-a773/round16/` (PR body, receipts, INDEX).
