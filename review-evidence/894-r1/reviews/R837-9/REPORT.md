[R837] NEGATIVE - exact head 6b759b30d08cecf8be0141bae36a9917a41da819

# R837-9: internal independent review of PR #902 (issue #894), round 15 delta

- **Head:** `6b759b30d08cecf8be0141bae36a9917a41da819`, tree `3f36cf22a5e8042c2512229a00aa60f58ed171ff`. Verified in the detached review clone before and after every probe (`restore.txt`).
- **Delta:** `867faf1e..6b759b30` is one commit. It changes only `docs/design/SPLIT_CONTROL_MEMORY.md` and `docs/reference/FR_NFR.md`, 8 lines replaced (`delta_names.txt`, `delta.diff`). No file under `sw/`, `tb/`, `hw/`, `syn/` or `scripts/` changed.
- **Ancestor review:** R838-9 POSITIVE at `867faf1e` (PR #902 issuecomment-6891425121). R837-8 NEGATIVE at `867faf1e` (issuecomment-6891424100), on R837-8-F1.
- **Verdict: NEGATIVE, on two MINOR findings.**
  - **R837-9-F1 (Docs).** R837-8-F1's cause is not fully closed. Its FR_NFR:383 twin in a source comment still states a superseded txL figure as current: `aecp_mbx.h:50`, "txL is 49.69 ms at 7 ms". The tree's model gives 52.09 ms at the head.
  - **R837-9-F2 (Docs, Tests).** The delta newly states the head's 8x8/2if tx row, 98.49 ms, at `SPLIT_CONTROL_MEMORY.md:2351`, next to "`CTRL_LOOP_TX_MS` states ... 98 ms". `ctrl_loop.h:366-371` says that figure is the row rounded up, which would be 99.
    - The tree's own `rows_tiers.tx_statements` refuses this tree. The author's receipts have printed the refusal since round 12, but only inside the 8x8/2if invocation, which is expected to exit 1 anyway. So no gate ever failed on it.
- **Resolved:** every other part of R837-8-F1 is closed at this head:
  - both named sites;
  - the five further sites;
  - every superseded 1x1/1if **row** figure. My own sweep, built from the rows-history table, finds none stated as current anywhere in the tree or the PR body.
- **Also resolved:** R837-8-R1, R2 and R3 and R838-9-R1 are applied.
- **Item-5 reset wording:** the new wording at `:2509` is true against `milan_soc.py` and the pinned LiteX.
- **Docs gates:** the gates I ran are rc 0 on the clean clone.

## Findings

### R837-9-F1 - MINOR - Docs - a superseded txL figure is stated as current in THE PACE's source comment (the remainder of R837-8-F1's cause)

- **Artifact:** `sw/firmware/ctrl/aecp/aecp_mbx.h:49-50` (unchanged since `fe0cef5b`): "with each map key at its position in the build's key domain (...) and AMAP_LIVE_WRITE's cost re-measured at 30 us, txL is 49.69 ms at 7 ms, and 8 ms does (#894, #908)."
- **Authority and evidence:**
  - 49.69 ms at 7 ms is the direct index's figure. This delta made the same clause past tense at `SPLIT_CONTROL_MEMORY.md:2467` ("Then txL was 49.69 ms at 7 ms"). It also made the comment's prose twin past tense at `FR_NFR.md:383` ("8 ms held it, txL 48.09 ms and R4L 188.39 ms").
  - At the head, the tree's own tier model (`rows_tiers.solve('txL', ..., BUILT)` at `pace_ms=7`) gives **txL 52.09 ms at 7 ms**. At 8 ms it gives 48.43 ms and R4L 188.48 ms, which equal section 13's `:2371` (`pace_probe.txt`, `scripts/pace_probe.py`).
  - R837-8-F1 required every superseded figure "stated as current anywhere in the docs, READMEs, comments or the PR body" to be made historical or the head's. The author's sweep (`author-r15/scripts/stale_rows.py`) takes its tokens from the rows-history table's cells and the load figures. That is complete for row figures, as my own sweep agrees. But it holds no txL figure at a pace other than the built one, so this hit was never classified. `stale_rows.log`'s "current with a superseded figure: 0" is true of its tokens only.
- **Impact:**
  - A reader of the constant's own comment takes 49.69 ms as txL's current margin at 7 ms. In fact 7 ms misses txL's 49 ms bound by 3.09 ms at the head, not by 0.69.
  - No bound, code or image is wrong: `AECP_PACE_MS` is 8 and `paced_rows.choice` returns 8.
  - The same class was graded MINOR in R837-8-F1 (a stale figure stated as current), so it is graded MINOR here.
- **Required outcome:**
  - In `aecp_mbx.h`, state 49.69 as history, for example: "txL was 49.69 ms at 7 ms, and 8 ms did".
  - Then either give the head's result ("at the head 8 ms holds txL, 48.43 ms, and R4L, 188.48 ms"), as `FR_NFR.md:383` now does, or drop the figure.
  - Add the txL and R4L figures at non-built paces to the stale-figure tokens. Section 13's `:2380`, `:2402`, `:2436`, `:2457` and `:2467` give them: 47.96, 45.67, 43.57, 47.29, 44.51, 42.96, 49.69, 53.86 and 248.26. Then re-classify every hit.
- **Verification:**
  - `scripts/sweep.sh <repo> tokens_sweep.txt`: every hit must be history, beside the head's figure, or unrelated.
  - The comment-only change must leave every preprocessed source and image byte-identical, as round 14's identity proof does.

### R837-9-F2 - MINOR - Docs, Tests - `CTRL_LOOP_TX_MS` states 98 ms at two interfaces under the head's 8x8/2if tx row, 98.49 ms, and the delta now states both side by side

- **Artifacts:**
  - `docs/design/SPLIT_CONTROL_MEMORY.md:2351`, changed by this delta: "...28.00 and 89.01 ms before it; **33.38 and 98.49 ms at the head**), which `CTRL_LOOP_TX_MS` states as 30 and 98 ms (34 at 1x1/1if since #894's round 11...)".
  - `sw/firmware/ctrl/loop/ctrl_loop.h:366-371`: "THE TRANSMIT's MRPDU by every source at the built design, in ms rounded up (...rows_tiers.py, the tx row, which refuses a tree whose row passes this)", with `#define CTRL_LOOP_TX_MS (MBX_N_IF == 1u ? 34u : 98u)`.
- **Authority and evidence:**
  - At the head, the tree's model gives the 8x8/2if tx row as 98.49 ms (`tx_probe.txt`), whose ceiling is 99. `rows_tiers.tx_statements(root)` at the head returns `["8x8/2if: CTRL_LOOP_TX_MS states 98 ms, under the built design's tx row 98.49 ms"]` (`txstmt_probe.txt`).
  - Replaying the model over the PR's history (`tx_history.txt`): the row was 88.92 ms at `6ec12ad7` and 98.49 ms from `e4d80a8a` on, while the statement stayed 98.
  - The author's own receipts print the same line as `OVER` from round 12 to round 13:
    - `author-r12/receipts/model/flip-8x8-21aeb997.txt:32` and `flip-8x8-3909588f.txt:32`;
    - `author-r13/receipts/model/flip-8x8-ed0df35b.txt:32`;
    - `author-r13/receipts/lane/*/flip_check_8x8_exits_1.log:33`.
  - In those receipts the line is listed among the 8x8/2if rows that are reported and not held. But it is not a row over its bound. It is a stated figure below its own row, which `ctrl_loop.h:366-368` says the tree refuses.
  - The PR body states "tx 98.49" for 8x8/2if and "The two-interface images and statements are unchanged by round 13". Both are true. Neither notes that the statement is now under its row.
  - Tests: the controls that plant this statement (`rows_tiers.py:932-935`, `flip_grade.py:174-178`) plant only the 1x1/1if leg. The only invocation that reaches the 8x8/2if statement, `flip_grade.py --check --point 8x8/2if` or the default `--check`, exits 1 by design (issue #894's 2026-11-12 decision: 8x8/2if rows are reported). A stale two-interface statement therefore passes every gate. That is how this one survived three rounds.
- **Impact:**
  - **No runtime effect.** `ctrl_loop.c:203` asserts the figure at one interface only. Issue #894's frozen acceptance 1 (`--point 1x1/1if`) is unaffected: 33.38 ms is within the stated 34.
  - **What is wrong:** the documented contract of the constant, the delta's own sentence, and the tree's own statement check disagree at 8x8/2if. A reader of `:2351` sees a "rounded up" statement under its row.
  - **Why MINOR, not RESIDUE:** this is a stated figure against a measured row, not wording only.
- **Required outcome (either is acceptable, publicly):**
  1. Restate `CTRL_LOOP_TX_MS` at two interfaces to 99 ms. Also update the literal control strings in `rows_tiers.py:932/934` and `flip_grade.py:174/175`, and `:2351`. The planted control should then cover the two-interface leg too, or the 8x8/2if statement check should be surfaced separately from the expected exit 1, for example as a gated statement-only check.
  2. Or record a decision that the two-interface statement is not held. Then say so in `ctrl_loop.h:366-370` and at `:2351`, and make `tx_statements` stop reporting it as a refusal.
  - Either way, `:2351` should no longer read "states as 30 and 98" in the present tense. The 1x1/1if figure is 34 (wording, folded in here).
- **Verification:** `rows_tiers.tx_statements(root)` returns `[]` at both points (`scripts/txstmt_probe.py`), or the recorded decision is cited at both sites. `flip_grade.py --check --point 1x1/1if` stays rc 0, and `--selftest` refuses every control.

### Wording residue

None new in the delta. The present-tense "states as 30" at `:2351` is folded into F2's required outcome.

### Suggestions

- **R837-9-S1 (SUGGESTION, Docs, Tests).** Generate the stale-figure tokens from every figure section 13 gives for a superseded state, not only the rows-history table. That means the pace-by-pace txL/R4L figures and the 8x8/2if rows too. Also sweep the C/H comments of the constants those figures justify (`AECP_PACE_MS`, `CTRL_LOOP_TX_MS`, `AECP_QUEUED_MS`, `CTRL_LOOP_SLICE_US`). F1 is exactly the gap between the two scopes.
- **R837-9-S2 (SUGGESTION, Tests).** In the 8x8/2if flip receipts, separate "row over its bound (reported by decision)" from "statement under its row". Then an expected exit 1 cannot hide a statement error. F2 is the instance.

## Focus items

1. **R837-8-F1 at its cause:**
   - **Named sites:**
     - `FR_NFR.md:383` now reads "8 ms held it, txL 48.09 ms and R4L 188.39 ms". Where it states the head, it reads "there 8 ms holds txL, 48.43 ms, and R4L, 188.48 ms".
     - `SPLIT_CONTROL_MEMORY.md:2467` now reads "Then txL was 49.69 ms at 7 ms, and 8 ms was the smallest pace that held: ... (`AECP_PACE_MS`; 48.43 and 188.48 at the head)".
     - Both are resolved.
   - **Five further sites:** `:2351` (beside the head's 33.38), `:2380` ("held", "did"), `:2402` ("was" ×3), `:2466` ("would be", "would move") and `FR_NFR.md:387` ("was 125.84 ms (127.21 at the head)"). All resolved.
   - **My sweep (`sweep_classified.txt`):**
     - Tokens: 123. They are every non-head cell of the rows-history table (93, built by `scripts/tokens.py`), plus the 8x8/2if earlier rows, the earlier tx and load figures, the 900 us state's figures, and txL/R4L at non-built paces.
     - Scope: every tracked text file, tables included (226 path:line:token hits), and the live PR body (equal to the packet's `PR-BODY.md` but for a trailing newline).
     - Result: every hit is history, beside the head's figure, or an unrelated quantity, except `aecp_mbx.h:50`, which is **F1**.
     - The 1x1/1if row figures at the head reproduce from the tree's model: txL 48.43, R4L 188.48, tx 33.38 (`pace_probe.txt`, `tx_probe.txt`).
   - **Author's packet:** 141 hits, "current with a superseded figure: 0". This is correct for its tokens, as stated in F1.
2. **Prior residues:**
   - **R837-8-R1 / R838-9-R1:** the PR body's R838-6-F2 row now cites `:2525`. At the head, `:2525` holds the load and the "R4 13.10 ms" summary. Resolved.
   - **R837-8-R2:** `:2509` reads "Every other 1x1/1if row held by every source, the load was 0.516 and 0.512, and the pace stayed 8 ms." Resolved.
   - **R837-8-R3:** PR body 14.1 reads "are past tense. `:2443`, `:2444` and `:2509` give the head's figure beside the old one". Resolved.
   - **R837-8-S1:** taken for row figures. Its extension is S1 above.
   - **R837-8-S2:** optional, not taken. That is acceptable.
   - **Item-5 reset wording (`:2509`):** "each output's domain takes the PLL's lock as its reset, so both are held in reset until the PLL locks and enter it when it loses lock, each released through its own synchronizer." This is true.
     - `milan_soc.py:238/265` (`cd_sys`) and `:282/288` (`cd_milan`) are `pll.create_clkout` outputs of one S7PLL, with the default `with_reset=True`. No `cd_sys.rst`/`cd_milan.rst` override or CRG `rst` exists in `sw/litex`.
     - The pinned LiteX (`litex_pins.txt:53`, `a1e1c365`) `xilinx_common.py:58-60` adds `AsyncResetSynchronizer(cd, ~self.locked)` per output: asynchronous assertion on loss of lock, release synchronised in each domain.
     - The PLL's own reset is the board button (`:251-252`), which drops lock.
3. **Delta scope and gates:**
   - `git diff --name-only 867faf1e 6b759b30` lists two docs files. So round 14's identity proof and round 13's measurements carry for all code.
   - Gates I ran on the clean clone are all rc 0 (`gates/SUMMARY.txt`, status empty before and after):
     - `docs_check.py`: 0 findings, 219 md + 1598 files;
     - `check_feature_status.py`;
     - `check_em_dash.py --base 867faf1e` (8 added lines) and `--base 66f71326` (2357 added lines), with the pinned renderer in a private venv;
     - `check_doc_style.py`;
     - `check_doc_paths.py`;
     - `check_archive.py`;
     - `git diff --check`.
   - **Author packet:** `author-r15` in archive `a5a6e2be` matches all 41 `MANIFEST.json` published hashes and all 40 `INDEX.md` rows (`packet_verify.txt`). Its `receipts/gates/SUMMARY.txt` shows 28 gates rc 0 on a clean clone, and its `delta.diff` body is this delta.

## Lenses

```text
[R837] PASS Conformance - FR_NFR.md:380-387 at 6b759b30 against the tree's tier model (pace_probe.txt, tx_probe.txt) and issue #894 acceptance 1-2 - every 1x1/1if clause figure the delta changed is the head's or history; the bounds 49, 238 and 130 ms and acceptance 1 (1x1/1if) are unaffected by a docs-only delta; F2 is not a clause or acceptance defect (8x8/2if reported by the 2026-11-12 decision)
[R837] PASS RTL - delta_names.txt (no HDL, firmware or build file) and SPLIT_CONTROL_MEMORY.md:2509 against milan_soc.py:238,251-252,265,282,288 and pinned LiteX xilinx_common.py:58-60 - no logic delta; the reset/clock precondition is the shared PLL's per-domain synchronised lock reset
[R837] PASS Robustness - SPLIT_CONTROL_MEMORY.md:2509 (item 5's clock and reset precondition, the late path it reopens) and delta.diff - the precondition is explicit and true, the independent-clock/reset case is named as reopening the proof; no failure-path claim added
[R837] MINOR Tests - rows_tiers.py:932-935, flip_grade.py:174-178, author-r13 flip_check_8x8_exits_1.log:33 - R837-9-F2: the two-interface TX statement is planted nowhere and reported only inside an expected exit 1
[R837] MINOR Docs - aecp_mbx.h:50; SPLIT_CONTROL_MEMORY.md:2351 with ctrl_loop.h:366-371 - R837-9-F1 and R837-9-F2
```

### Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `FR_NFR.md:380-387`; the tree's tier model at the head (txL/R4L by pace, tx at both points); issue #894's acceptance | R837-9 (delta), carrying R838-9's code coverage | `6b759b30d08cecf8be0141bae36a9917a41da819` |
| RTL | CLEAN | `delta_names.txt`; `:2509` against `milan_soc.py` and the pinned LiteX source | R837-9 (delta), carrying R838-9's code coverage | `6b759b30d08cecf8be0141bae36a9917a41da819` |
| Robustness | CLEAN | `:2509` item-5 precondition; `delta.diff` | R837-9 (delta), carrying R838-9's code coverage | `6b759b30d08cecf8be0141bae36a9917a41da819` |
| Tests | UNCLEAN (F2) | `rows_tiers.tx_statements`, its controls `rows_tiers.py:932-935` and `flip_grade.py:174-178`; author flip receipts r12/r13 | R837-9 | `6b759b30d08cecf8be0141bae36a9917a41da819` |
| Docs | UNCLEAN (F1, F2) | both delta files; my sweep of 123 tokens over every tracked file and the PR body; `aecp_mbx.h:50`; `ctrl_loop.h:366-371`; gates | R837-9 | `6b759b30d08cecf8be0141bae36a9917a41da819` |

F2's Tests part sits in code unchanged since `e4d80a8a`, which R838-9's ancestor POSITIVE carried as clean. I record it because this delta's `:2351` sentence depends on that statement, and because AGENTS.md section 6 records a finding under every lens it is attributable to. The manager may weigh that a re-attribution of carried coverage needs the reviewer's own re-filing; I make that re-filing here.

## Real limits

- **No code review:** I did not re-review code the delta leaves untouched. Code identity is carried from round 14's published proof, not re-proved by a rebuild.
- **Model probes:** the probes run the tree's own Python tier model read-only. The history replay (`tx_history.txt`) used the head's `third_party/tsn-c-stack/include` for every commit, and that gitlink moves once in the PR range. So it dates F2's onset only approximately; the head's figures are exact.
- **Gates:** I ran 8 documentation gates myself. The other 20 of the author's 28 are carried from its hash-verified receipts.
- **Hosted checks:** at the time I looked (`hosted_checks.tsv`), 3 had completed successfully (`changes`, `wire-accountability`, `docs-check-no-git`), 4 were in progress and 12 queued. This is not acceptance evidence.
- **No manager bank:** no manager source bank runs at this head, and none is claimed or inferred.
- **No hardware:** physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Hosted and act acceptance at the exact head.
- The current-dev merge candidate (source base `66f71326`, live dev `6b66f66d`): builder and native banks at the merge turn, with receipts linked on the PR.
- Carry F1 and F2 to the author. After the fix, a delta re-review must cover Docs and Tests at the new head. If F2 option 1 changes `ctrl_loop.h`, it must also confirm that images stay byte-identical (the figure is asserted at one interface only).

R837-9 FINISHED
