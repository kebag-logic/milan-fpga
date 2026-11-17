[R843] POSITIVE - exact head e1ecce20d52c3ca1c34c50722f4a0fb607964bc9

# R843-7: internal independent review of PR #914 (issue #894, lane 894b), round 14 delta

- **Head:** `e1ecce20d52c3ca1c34c50722f4a0fb607964bc9`, tree `35952b321f7e3fca20db5260cf76ab99b0cadaaa`.
- **Delta reviewed:** `d0a2a1605d7a..e1ecce20`, two commits.
  - `60389719`: docs and comments only.
  - `e1ecce20`: a flip self-test control, `CHECK_HELD_CONTROL`, and a harness mutant.
- **Prior heads:** R843-6 was NEGATIVE and R844-5 POSITIVE at `d0a2a160`. Under the round's brief, code this delta does not touch keeps its prior lens verdict.
- **Source base:** `7398ec0aeea468d92ff642a03a06e291a0cd58d1`.

## Verdict

**POSITIVE.** R843-6-F1 is closed at its cause. R843-6-S1 is closed: I removed the `tx_held` call from `--check` in a disposable copy, and the flip self-test now fails, by name.

Nothing open in this delta is MINOR, MAJOR or BLOCKER. I record two wording residues (R843-7-R1 and R2) and two optional suggestions about the evidence packet (S1 and S2). None of them changes a figure, a gate, code or an image.

## What I checked, and how

### (1) R843-6-F1: closed

- **The fix:** `docs/reference/FR_NFR.md:420` now reads "2,027 at 8x8/1if, whose `CTRL_LOOP_TX_MS` is its own tx row's 74.26 ms rounded up, 75 ms, held to that row by `flip_grade.py --check` (`tx_held`; 2,026 at 70 ms before the row reached 74.26)".
  - That is R843-6-F1's suggested text, word for word.
  - The old figure appears only in the historical parenthesis.
- **Against the code:**
  - `ctrl_loop.h:355` gives `CTRL_LOOP_TX_MS 75u`, and `ctrl_loop.h:436` gives `CTRL_LOOP_JOIN_CS 19u`.
  - `srp_mbx.c:36` computes `SRP_REDECLARE_CS = 2000 + 19 + (75+9)/10 = 2,027` cs.
  - The same formula gives 2,023 at 34 ms, 2,030 at 105, 2,029 at 99 and 2,026 at 70. All of these match the row.
  - So the sentence "IEEE 802.1Q-2018 35.2.2.8 sets only the least, 2,000 cs, and the terms above it cover the Leave's latest departure" is true again for the figures the row gives.
- **The gate holds it:** my `flip_grade.py --check --point 8x8/1if` at the head prints `HELD 8x8/1if: ... CTRL_LOOP_TX_MS 75 ms against its tx row by every source 74.26 ms` and `RESULT: PASS`, rc 0 (`receipts/H-flip-check-8x8-1if.txt`).
- **My own sweep** (`receipts/sweep-r843-7.txt`) searched the tree with `git grep` for:
  - `69.84`, `2,026`, `2026 cs`, `2026u`, `li a3,2026` and `20,260` anywhere;
  - `70 ms` or `70u` on any line that also names 8x8/1if, `TX_MS`, THE TRANSMIT, the hold-off or a tx row.
- **Every hit is historical, a plant, or unrelated:**
  - `SPLIT_CONTROL_MEMORY.md:2814` ("It was 70 ms for 69.84 at the costs restated on the composed image"), `:2815` ("2,027 cs there (2,026 at 70 ms)"), `:2820` ("(historical; 75 ms for 74.26 at the head's costs, above)"), `:2821` ("(`d1c9023b`'s, historical)") and `:2824` ("on that image (historical; ...)") are all scoped to an earlier image.
  - `:2816` is a refusal ("A 70 ms figure is refused against the head's tx row, 74.26 ms").
  - `:2829` describes the `li a3,2026` to `li a3,2027` change.
  - `FR_NFR.md:420` is the historical parenthesis above.
  - `ctrl_service_budget/README.md:205` and `:1236`, and `flip_grade.py:72`, `:102` and `:111`, are the new control's 70 ms plant.
  - `ctrl_service_budget/README.md:1004` (369.84) is an unrelated figure.
- **Nothing states 2,026, 70 ms or 69.84 as 8x8/1if's current figure.**
  - My hit set equals the author's `receipts/sweep-e1ecce20.txt`.
  - That set also has `milan_dp/README.md:1637` ("LeaveAll's 50 and 70 ms"), an unrelated measurement. My narrower regex leaves it out.
- **`docs_check`:** 0 findings across 219 md files, rc 0 (`receipts/H-docs_check.txt`).

### (2) R843-6-S1: closed, falsified with my own source mutation

- **How the control works:** `flip_grade.check_held_control` (`flip_grade.py:100-111`) runs `main` in-process with argv `--check --point 8x8/1if`.
  - It wraps the module-global `tx_held` so that a call without texts gets ctrl_loop.h with 8x8/1if's figure planted at 70 ms.
  - It requires rc != 0 and the line `OVER 8x8/1if: CTRL_LOOP_TX_MS states 70 ms`.
  - `main` (`:472-473`) calls `tx_held(ROOT, points)` by its global name, so the wrapper is what the CLI path reaches.
  - It runs when the script is `__main__` (my `--selftest` run below) and when the module is imported as `flip_grade` (the harness, below).
- **Source mutation (clone M):** I deleted `+ tx_held(ROOT, points)` from `main`'s findings (`receipts/probe-edits.diff`).
  - `flip_grade.py --selftest` then prints `ESCAPED --check --point 8x8/1if with 8x8/1if's CTRL_LOOP_TX_MS planted at 70 ms` and `flip check: 615 of 616 planted controls refused`, rc 1 (`receipts/M-flip-selftest-no-tx_held-in-check.txt`).
  - That is exactly what R843-6-S1 asked for. At d0a2a160 the same removal left the self-test green.
- **At the head (clone H):** `--selftest` gives `616 of 616`, rc 0 (`receipts/H-flip-selftest.txt`).
- **The control's premise, through the real CLI:** I planted `CTRL_LOOP_TX_MS 70u` in the file itself.
  - With `main` wired (clone P), `--check --point 8x8/1if` gives `OVER 8x8/1if: CTRL_LOOP_TX_MS states 70 ms, under the built design's tx row 74.26 ms` and `RESULT: FAIL`, rc 1 (`receipts/P-plant70-check-8x8-1if-wired.txt`).
  - With the call removed (clone M), it gives `RESULT: PASS`, rc 0: the gap the control now closes (`receipts/M-plant70-check-8x8-1if-unwired.txt`).
- **The harness mutant, by name:** I wrote my own probe, `scripts/mutant_by_name.py`, run with `-I` on clone H (`receipts/H-mutant-by-name.txt`).
  - `selftest_mutants.MUTANTS` has 260 entries, and the new mutant is among them.
  - All flip checks pass at the wiring.
  - Under the mutant, exactly one check fails: `the flip check refuses --check --point 8x8/1if with 8x8/1if's CTRL_LOOP_TX_MS planted at 70 ms (escaped)`.
  - All pass again after it.
  - This agrees with the author's `receipts/gates/check-held-mutant-e1ecce20.txt`.
- **The mutant's scope:** it wraps `flip_grade.main` and blanks `tx_held` only while `main` runs, so the direct `TX_HELD_CONTROLS` still see the real `tx_held`. It does not mask the three earlier controls.

### (3) The residues took their exact fixes

| Residue | Where at the head | Status |
|---|---|---|
| R843-6-R1 | `flip_grade.py:67-68` | Verbatim exact fix |
| R843-6-R2 | `srp_mbx.c:34-35` | Verbatim exact fix; see R843-7-R1 below for a scope nit in that same prescribed text |
| R843-6-R3 | `srp_talker.cpp:53-54` | Verbatim ("20,230 ms at 1x1/1if, 20,270 at 8x8/1if and 20,300 at two interfaces"). `kHoldOffMs` = 20000 + 10 x (19 + 8) = 20,270 at 75 ms, as stated |
| R843-6-R4 | `SPLIT_CONTROL_MEMORY.md:2816` | Verbatim |
| R843-6-R5 and R844-5-R1 (PR text) | Live PR #914 body | The status now reads "Published source head: `e1ecce20`. The manager owns composition, merge and the base synchronization for PR #914 (`894-8x8-1if` -> `dev-soft-core`)". The live PR base is `dev-soft-core`, and the prerequisite sentence is gone. This is equivalent in substance to the exact fix. Accepted |

- The `srp_mbx.c` hunk is +2 / -2 lines, all of them `//` comments, so line numbers and object code are unchanged.
- The `srp_talker.cpp` hunk is a host-test comment, which is in no image.

### (4) Images, self-tests and docs jobs

- **Images:** the delta changes no compiled byte.
  - Its only firmware hunks are the comment lines above. `srp_mbx.c` keeps its line count, so even `__LINE__` is unaffected.
  - The author's `receipts/images/img-identity-e1ecce20.txt` lists all eight images (fixture and platform x 1x1/8x8 x 1if/2if) as identical to d0a2a160's by ELF and loadable sha256: `RESULT: PASS: all 8 identical`.
  - The two `qimg-*.txt` receipts differ only in the commit id.
  - I did not rebuild images. I judged this from the delta itself, and the author's receipt agrees.
- **Flip self-test:** 616 of 616, reproduced by me (above).
- **Flip check:** passes at 1x1/1if (`receipts/H-flip-check-1x1-1if.txt`) and at 8x8/1if, both rc 0.
- **Harness self-test, 932 checks and 260 mutants:**
  - I reproduced the 260 mutants and the new mutant's catch by name.
  - My own full `run.py --self-test` did not finish: it was stopped at the session's time limit after 3,310 of about 5,236 lines, with 146 mutants caught and 0 escapes or failures (`receipts/H-harness-selftest-partial.txt`).
  - The author's receipt ends `self-test: 0 failures` and `harness self-test rc=0`. Its middle 4,036 lines are cut, so the "932 checks" total cannot be read from it (S2).
  - The figure rests on the author's run, and nothing I ran contradicts it.
- **Docs jobs:**
  - The author's `verify-docs-yml-e1ecce20.txt`: 61 steps rc 0, 34 not run with a stated reason (hosted-only orchestration, cancellation or upload), 0 bad.
  - Mine: `docs_check` rc 0, and `check_py_idiom.py` rc 0 in the review clone (`receipts/clone-py_idiom.txt`).
  - An earlier attempt of the idiom gate in scratch clone H failed with rc 1, only because that clone's copied submodules have no git metadata (`receipts/H-py_idiom.txt`; not a tree defect).
- **The author's packet** (archive `ae64c917`, `review-evidence/894b-r1/author-r14`):
  - 158 of the 168 INDEX entries match their published bytes.
  - All the receipts this report relies on match.
  - The 10 that differ are two workflow logs and eight scripts. At least eight of them carry host-path scrub markers, so the index predates publication scrubbing (`receipts/packet-index-verify.txt`; S1).
- **Hosted:** no check-runs and no workflow runs exist at this exact head (`receipts/hosted-e1ecce20.txt`). I claim no hosted evidence, and that acceptance belongs to the manager.

## Findings

### R843-7-R1: RESIDUE. Lenses: Docs.

- **Where:** `sw/firmware/ctrl/srp/srp_mbx.c:34-35`: "held at or over its tx row at every shape by flip_grade.py --check: rows_tiers.tx_statements, and tx_held at 8x8/1if".
  - This is R843-6-R2's own prescribed text, taken verbatim.
- **Evidence:**
  - `ctrl_loop.h:338-373` lists four shapes. `flip_grade.POINTS` is `('1x1/1if', '8x8/2if', '8x8/1if')` (`rows_grade.py:89`, `flip_grade.py:65`).
  - 1x1/2if is not graded as its own point. It takes 8x8/2if's 105 ms (`ctrl_loop.h:328`, "both two-interface shapes 8x8/2if's"), and that figure is held at the heavier 8x8/2if point.
  - So "at every shape" says slightly more than the gate does.
- **Impact:** none on code, figures, gates or images. This is a source-comment scope word only.
- **Exact fix:** "(hold, CTRL_LOOP_TX_MS, the built design's, held at or over its tx row at each point flip_grade.py --check grades: rows_tiers.tx_statements at 1x1/1if and 8x8/2if, whose figure 1x1/2if takes, and tx_held at 8x8/1if), so it adds both."
- **Verification:** a comment diff at those lines.

### R843-7-R2: RESIDUE. Lenses: Docs.

- **Where:** `tb/verilator/ctrl_service_budget/flip_grade.py:71`: "#: The control that --check itself reports tx_held's refusal (check_held_control): main run as the CLI runs it."
- **Why:** the sentence is missing its verb ("the control that [holds that] --check ...").
- **Exact fix:** "#: The control that holds --check itself to reporting tx_held's refusal (check_held_control): main run as the CLI runs it."
- **Verification:** a comment diff.

### R843-7-S1: SUGGESTION. Lenses: Docs. Packet tooling only.

- **Where:** `author-r14/INDEX.md` in archive `ae64c917`.
- **What:** 10 of its 168 hashes do not match the published bytes, because the index was generated before host-path scrubbing (`receipts/packet-index-verify.txt`).
- **Optional:** regenerate INDEX after scrubbing, so that a cold reviewer can verify every file.

### R843-7-S2: SUGGESTION. Lenses: Tests. Packet tooling only.

- **Where:** `author-r14/receipts/gates/harness-selftest-e1ecce20.txt`.
- **What:** the receipt keeps the first and last 600 of 5,236 lines. The REVIEW READY's "932 checks pass and 260 mutants are caught" totals appear in neither part.
- **Optional:** append a one-line count (checks passed, mutants caught, and the round's mutant by name) to the kept tail.

### Prior findings at this head

| Finding | Status at e1ecce20 | Evidence |
|---|---|---|
| R843-6-F1, MINOR (Conformance, Docs) | **RESOLVED** | `FR_NFR.md:420` exact text; sweep clean; `--check` HELD 75/74.26 |
| R843-6-S1, SUGGESTION (Tests) | **RESOLVED** | Source mutation gives 615/616 with the named escape; harness mutant caught by that check alone |
| R843-6-R1 to R4, RESIDUE | **RESOLVED** | Verbatim at `flip_grade.py:67-68`, `srp_mbx.c:34-35`, `srp_talker.cpp:53-54` and `SPLIT_CONTROL_MEMORY.md:2816` |
| R843-6-R5 and R844-5-R1, RESIDUE (PR text) | **RESOLVED** | Live body status and base `dev-soft-core` |
| R843-5-S1 and S2, R843-4-S1, R843-2-S2 and R843-3-S2, SUGGESTION | Retained, optional | Not touched by this delta |

## Lens results

```text
[R843] PASS Conformance - docs/reference/FR_NFR.md:420 against ctrl_loop.h:355,436, srp_mbx.c:36 and IEEE 802.1Q-2018 35.2.2.8 - 2,027 cs at 75 ms for the 74.26 ms row (2,023/2,030/2,029/2,026 by the same formula); flip --check HELD 75 vs 74.26 at 8x8/1if, RESULT PASS; sweep finds no current-tense 2,026/70/69.84
[R843] PASS RTL - git diff d0a2a160..e1ecce20 -- sw/ hdl/ - no HDL in the delta; srp_mbx.c +2/-2 comment-only (line count kept), srp_talker.cpp host-test comment; 8 images identical by the author's img-identity receipt; firmware behaviour keeps R844-5's verdict at d0a2a160
[R843] PASS Robustness - flip_grade.py:100-111, selftest_mutants.py:236-246, :500 - the control plants only what tx_held reads and requires rc and the named OVER line; the mutant blanks tx_held only while main runs, leaving the direct TX_HELD_CONTROLS intact; a real 70 ms plant is refused through the CLI (P) and escapes only with the call removed (M)
[R843] PASS Tests - receipts/M-flip-selftest-no-tx_held-in-check.txt, H-flip-selftest.txt, H-mutant-by-name.txt - removing tx_held from --check fails the self-test by name (615/616, rc 1); head 616/616; harness mutant listed (260) and caught by that check alone; harness full self-test per the author's receipt (0 failures), mine partial with 0 escapes
[R843] PASS Docs - FR_NFR.md:420, SPLIT_CONTROL_MEMORY.md:2814-2829, ctrl_service_budget/README.md:205,1236, srp_mbx.c:31-35, srp_talker.cpp:50-54, flip_grade.py:67-72, PR #914 body - every prior residue taken; docs_check 0 findings; no new source-comment lane, round, reviewer or comment ID in the delta; residues R843-7-R1 and R2 (wording) recorded with exact fixes
```

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `FR_NFR.md:420`; `ctrl_loop.h:355,436`; `srp_mbx.c:36`; the hold-off arithmetic against 802.1Q-2018 35.2.2.8; `flip_grade --check` at 1x1/1if and 8x8/1if | R843-7 | `e1ecce20d52c3ca1c34c50722f4a0fb607964bc9` |
| RTL | CLEAN | The delta's `sw/` hunks (comment-only, line count kept); no `hdl/` change; the author's 8-image identity receipt | R843-7 (delta); firmware and RTL otherwise from R844-5 at `d0a2a160`, which this delta leaves untouched | `e1ecce20d52c3ca1c34c50722f4a0fb607964bc9` |
| Robustness | CLEAN | `flip_grade.py:100-111,192,407`; `selftest_mutants.py:236-246,500`; plant probes P and M | R843-7 | `e1ecce20d52c3ca1c34c50722f4a0fb607964bc9` |
| Tests | CLEAN | Flip `--selftest` (head and source mutant); the harness mutant by name; `--check` at two points; the harness receipt (author) and my partial run | R843-7 | `e1ecce20d52c3ca1c34c50722f4a0fb607964bc9` |
| Docs | CLEAN (two residues, non-blocking) | `FR_NFR.md:420`; `SPLIT_CONTROL_MEMORY.md:2814-2829`; `ctrl_service_budget/README.md:205,1236`; the delta's comments; the PR body; the packet INDEX | R843-7 | `e1ecce20d52c3ca1c34c50722f4a0fb607964bc9` |

## Real limits

- **The harness self-test:** my full `run.py --self-test` did not complete in the session's wall budget (partial, 0 escapes). The 932-check total is the author's figure, and the published receipt cannot show it.
- **Images:** I did not rebuild them. Identity rests on a comment-only delta that keeps line counts, and on the author's receipt.
- **Not re-run, by the round's brief:** campaigns, legs and full banks. No manager source bank was run or inferred at this head.
- **Hosted:** no hosted runs exist at this exact head. Act and hosted acceptance belong to the manager.
- **Hardware:** physical calibration was NOT RUN, and field skips are not hardware proof.
- **Owed elsewhere:** the 8x8/1if every-source rows (R4 21.39 against 20, tx 74.26 against the MRPDU's 49) stay reported and owed to #872, as ruled. They are not a finding of this delta.

## Pending manager duties

- Validate the current-dev merge candidate (source base `7398ec0aeea4`, live dev `6b66f66d89cf`) with the builder and native banks at the merge turn, and link the receipts on the PR.
- Hosted and act acceptance at the exact head or candidate.
- Carry R843-7-R1 and R2 (wording) to the residue checklist, together with any open items of earlier rounds.
- Note S1 and S2 for packet tooling (optional).
- The merge needs explicit maintainer authorization. This report merges nothing.

## Probe hygiene

- The review clone ends at `e1ecce20`, tree `35952b32`, with 0 status lines, its worktree equal to HEAD, and all six gitlinks unchanged (`receipts/clone-integrity.txt`).
- Every edit was made in disposable clones under `scratch/` (H clean, M source mutant plus plant, P plant only). Those clones are not published.

R843-7 FINISHED
