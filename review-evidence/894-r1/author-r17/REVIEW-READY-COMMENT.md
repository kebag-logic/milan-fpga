[A773] REVIEW READY
Commit: `478ff78c` (PR #902, `894-tiers` -> `dev-soft-core`; one commit on round 16's `b6f5c638`; the manager pushes)

Round 17 answers R837-10 (PR #902 issuecomment-6892175293), NEGATIVE on one MINOR at `b6f5c638`. It changes one Markdown file, plus the PR body.

Changed:
- **R837-10-F1:** `SPLIT_CONTROL_MEMORY.md:2004` now reads "every participant's owed MRPDU, one a call, was then within 2 x `MBX_N_IF` x 44 = 176 ms at two interfaces, inside the 200 ms JoinTime". Then it says what governs under THE TIERS:
  - no such product is claimed;
  - `CTRL_LOOP_TX_BOUND_MS`, 49 ms at the 19 cs join timer, holds the tx row at 1x1/1if;
  - at 8x8/2if the rows are reported, not held (#890).
  It makes no two-interface JoinTime claim. The PR body's round-16 claim about `:2004` is corrected.
- **R837-10-S2, taken:** a sweep of every superseded statement figure (`statement_sweep.py`).
  - **Tokens:** each constant's old value, where the sentence names what it states:
    - `CTRL_LOOP_TX_MS` 44/30/98;
    - `CTRL_LOOP_TX_BOUND_MS` 40/50;
    - the join timer's 20 cs and 200 ms;
    - the build of one's 725/430;
    - a TICK's 45/50, AECP's timer slot's 60/65, a LINK's 150, and the SRP drain's 250;
    - the slice's 800/900/1,200 us, the pace's 6/7 ms, and the load's 0.515/0.511.
  - **Derivations:** every derivation one of those figures enters, such as 30 + 7 x 2 = 44 and 2 x `MBX_N_IF` x 44 = 176, and each result wherever it appears.
  - **Clause flags:** every sentence citing a clause or table is flagged.
  - **Scope:** section 13, FR_NFR 3.4.1, MAILBOX_SPLIT, every README, every comment and docstring under `sw/` and `tb/`, and the PR body; tables included.
  - **It found four more present-tense sites,** now history with the head's figure beside them:
    - `:2260`: `SRP_JOIN_CS` 200 ms, now 190 ms at 19 cs;
    - `:2357`: the built design at 800 us, now 950;
    - `:2377`: "picks 800 us";
    - `:2442`: the bound "is ... 50 ms", now 49, and the pace "now 6 ms", now 8.
  - **Result:** 178 hits, every one classified: 114 historical, 41 beside the head's figure, 17 another quantity, 6 reported (below). None is current.
- **R837-10-R1:** the RC line now reads "equal to round 13's output up to the order of two result-set listing lines" (this packet's `receipts/statements/RC.txt`), and so does PR body 16.3.

Validation (clean clone of `478ff78c`, 0 changed paths before and after):
- **What changed:** `git diff --name-only b6f5c638 478ff78c` lists `docs/design/SPLIT_CONTROL_MEMORY.md` alone. Round 16's image, ELF and statement proofs carry unchanged.
- **Gates,** 23 commands, each rc 0:
  - `docs_check.py`;
  - `check_em_dash.py` from `66adb9a9`, `cec88385` and `b6f5c638`;
  - doc style, gPTP docs and `DOC_MAP`;
  - both idiom gates and `git diff --check`;
  - the solution, submodule, feature-status, TODO-ownership, hygiene, doc-path and archive gates;
  - **the four sweeps,** every hit classified: round 14's cost grep (64), round 15's row sweep (143), round 16's comment sweep (15) and the statement sweep (178).

Acceptance criteria (round 17):
- **Item 1** met: `:2004`, and the PR body's round-16 claim.
- **Item 2** met: the statement sweep, and every hit classified.
- **Item 3** met: the RC line.
- **Item 4** met: one Markdown file, and the documentation gates on a clean clone.
- **Every row, the load, the pace and the slice are round 13's,** and every image and ELF round 16's.

Open risks/questions:
- **Found by the sweep and not fixed here** (harness code, outside a documents round): `tb/verilator/milan_dp/srptx.hpp:83`.
  - The SRP transmit check (#867) mirrors the adapter's JoinTime as `kJoinCs = 20`, and its README (`:1610`, `:1639`) says the adapter configures 200 ms.
  - `srp_mbx.c:29` configures `CTRL_LOOP_JOIN_CS`, 19 cs since #908's contingent moves.
  - So the check's Join-arm layout test (`srptx.hpp:591`) matches no arm, and its record's `timers_cs.join` reads 20.
  - It is listed under the PR body's Known limitations, for an Issue of its own.
- **R837-10-S1 and S3 are not taken,** since this round changes documents only.
- **The packet:** `894-a773/round17/` (PR body, receipts, INDEX).
