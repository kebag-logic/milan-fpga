[R460] POSITIVE - exact head 4298ed2595d98ec98592bea4e05c4d1744663c34

# R460-2: internal independent review of issue #85 / PR #152 (GAP-16, ADP MTXW walk), round 2

- Exact head `4298ed2595d98ec98592bea4e05c4d1744663c34`, tree `7704889e1e07e546d6d155470800e7387f477e62`. Round-1 head `a8669732b30436c641d51829950c204defd57a30`; source base `5c71928ad2bf1a854a5538d69b77214dfdf1697f`.
- Scope: the round-2 delta `a8669732..4298ed25`, in three commits (`e634a6e`, `f3f6c90`, `4298ed2`) over six files:
  - `tb/adp_engine/{sim_main.cpp, mutants.py, Makefile, README.md}`;
  - the new `tb/adp_engine/mutations/arc-fresh-no-store.patch` (mode 100644);
  - `hdl/adp/KL_adp_engine.sv`, comments only.
- Reconstruction:
  - The repository has no AGENTS.md or CONTRIBUTING.md; conventions come from `README.md` and `docs/README.md`, as in round 1.
  - Issue #85's frozen acceptance and the lane comment, as reconstructed in R460-1.
  - The round-2 assignment (issue #85 comment 5975300666), the REVIEW READY comment (5975528337) and the review start (PR #152 comment 5975536722).
  - 04 F04.8.
  - The delta and its history, then the PR body at this head.
  - The pinned evidence packet.
- Simulator: pinned Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`; wrapper sha256 in `receipts/simulator-identity.txt`).
- Every run used a disposable copy under the packet's scratch directory. The review clone was never written; its integrity was verified at the end (`receipts/clone-integrity.txt`).

## Verdict

POSITIVE. No MINOR, MAJOR or BLOCKER finding is open at this head. R460-1's one MINOR (F-1) is resolved. One new RESIDUE (R2-1, wording only) and one SUGGESTION (S2-1) are recorded.

- **F-1 resolved.**
  - Both index > last cells of TK_DISCOVERED (`V_FRESH x D_DISC`, arc 4's cell, and `V_GMF x D_DISC`) are now followed by an AVAILABLE that repeats the noted index 701, with grandmaster and domain matching. That AVAILABLE must give the restart pair (`sim_main.cpp:1582-1596`).
  - The step's failures count inside `walk_discovery_cell`, so they clear `cell_ok` for that cell (`:1634-1636`), and in the match cell they fail arc 4's check. Probe `y4` proves it.
  - F04.8's fresh-arc guard reads no grandmaster, so treating the GM-mismatch cell the same way is what F04.8 says. Probe `y1` (the store gated on a GM match) is caught only by that cell's follow-up, and `y3` shows it would survive without that follow-up.
- **`arc-fresh-no-store`:**
  - It fails exactly 4 checks: both follow-ups (`got 0 events`), `P13 F04.3 arc DISCOVERED -> DISCOVERED (index > last): walked and graded`, and the arc count 7 of 8.
  - The full campaign, run through `make mutants JOBS=8`, gives 2 controls PASS and 39 of 39 KILLED (41 of 41).
  - Every count equals its README row. Only the three rows the README names changed (3 to 4, 4 to 7, 10 to 13).
  - The new and changed arms gave identical verdicts, counts and FAIL lines at `--jobs 1`.
- **R460-1's `probes.py`, rerun unchanged** (sha256 identical to the round-1 packet's copy):
  - `r6-fresh-no-store` was green at `a8669732` (1330 of 1330). It is now red, with the 4 lines above.
  - `x2` went from 1 to 5 failures. Every other probe's rc and failure count is unchanged.
- **`make mutants JOBS=N`:** the Makefile passes `--jobs $(JOBS)`, default 4 (`make -n` shows `--jobs 7` and `--jobs 4`). It was exercised for real at `JOBS=8`.
- **Engine change is comments only.** At the base, at `a8669732` and at this head, the source with comments stripped hashes the same (`b228a031…`). The simulator's own preprocessor output is byte-identical (`0c16b9e1…`), and the line count is the same (1098). `lint_hdl.sh` gives rc 0 with 41 of 41 modules OK.
- **R-1 resolved.** The PR body's item 3 now reads exactly as R460-1 required.

## Round-1 items at this head

| Round-1 item | Disposition at `4298ed25` | Evidence |
|---|---|---|
| F-1 (MINOR, Tests): the fresh arc's "note the index" was graded nowhere | **Resolved** | `sim_main.cpp:1582-1596`; probes `r6` (now 4 failures, arc 4's check among them), `y1` to `y4`; campaign arm `arc-fresh-no-store` KILLED at `JOBS=8` and at `--jobs 1`; README `:147-152`, `:252-256`, row `:294`; check count 1334 at `:6` and in the run |
| R-1 (RESIDUE, Docs): PR body item 3 suggested `make mutants` takes `--jobs N` | **Resolved** | PR body item 3 now reads "(`make -C tb/adp_engine mutants` at the default 4 jobs, or `python3 tb/adp_engine/mutants.py --output DIR --jobs N`)" (body sha256 in `receipts/evidence-read.txt`) |
| S-1 (SUGGESTION): engine comments carried the pre-adjudication warning | **Taken** | `KL_adp_engine.sv:38-42` and `:705-707` now match the README verdict (`README.md:205-212`); comment-only proof in `receipts/static/engine-comment-only.txt` |
| S-2 (SUGGESTION): `make mutants` could not set the job count | **Taken** | `tb/adp_engine/Makefile:5` and `:25`; README `:237` |

No round-1 item is retained or worsened.

## Findings

### R2-1: RESIDUE. "and so arc 4's check" overstates the GM-mismatch cell's follow-up

- **Lens:** Docs (prose in the README and the PR body only).
- **Where:**
  - `tb/adp_engine/README.md:151-152`: "A failure there fails the cell, and so arc 4's check."
  - PR #152 body, "Round 2", item 1: "A failure clears the cell, and so arc 4's check."
- **Evidence:** arc 4's walk cell is the match cell only (F04.8 and `F043_ARCS`, `sim_main.cpp:331`). Probe `y1` breaks only the GM-mismatch cell's follow-up. Result: 1 failure, that cell's follow-up line, and arc 4's check stays green. The test is correct and matches F04.8; only the sentence generalises from the match cell to both cells.
- **Exact fix:**
  - README: "A failure there fails its cell; in the match cell, arc 4's walk cell, it also fails arc 4's check."
  - PR body: "A failure clears that cell; in the match cell it also fails arc 4's check."
- **Effect:** none on any measurement, figure, verdict, test, code or clause claim. Every count and FAIL list in the README and the PR body is correct as measured.

### S2-1: SUGGESTION. The follow-up's index is a literal copied from `apply_disc`

`sim_main.cpp:1585` writes `const uint32_t noted = 700 + 1;  // apply_disc's last + 1`. The 700 duplicates `apply_disc`'s `last` (`:1487`) rather than sharing it.

Probes `y5` and `y6` change the literal to 700. With that change the follow-up passes on the head RTL, and it also passes under the r6 fault (rc 0, 1334 of 1334): the check loses its teeth without going red. At this head the literal is right, and `arc-fresh-no-store` would turn UNPROVEN in the campaign if it drifted, so this is not a defect.

Suggestion: name the TK_DISCOVERED last index once, for example `constexpr uint32_t DISC_LAST = 700;`, and use it in both places.

## Lens ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | F04.8 "TK_DISCOVERED to itself, fresh" (guard: interface equal and index > last, no grandmaster; action: note the index, restart T-ADP-NOADP; Milan §5.6.4.5.2 steps 1, 3) against `notes_fresh_index` (`sim_main.cpp:338-343`): both index > last cells, as the guard says. The follow-up's expectation, the restart pair for an index at or below the last one with GM and domain matching, is F04.8's restart arc (step 2). The engine comments (`KL_adp_engine.sv:38-42`, `:705-707`) agree with the README's adjudication (`:205-212`) and cite §6.2.2.15 as 04 §5 does. No conformance claim changed elsewhere | R460-2 (delta) over R460-1 | 4298ed2595d98ec98592bea4e05c4d1744663c34 |
| RTL | CLEAN | `hdl/` delta is 8 comment lines in `KL_adp_engine.sv`. With comments stripped the source is identical to `a8669732` and `5c71928a`. The preprocessor output is byte-identical, with 1098 lines in all three. `lint_hdl.sh` rc 0, 41 of 41. `arc-fresh-no-store.patch` removes exactly the fresh branch's `rec_wr_en_w = 1'b1;` (`:359`), applies with `git apply --check` to the head (campaign) and keeps the re-arm (`:360`). The record write data is shared by all branches (`:345`), so a value fault confined to the fresh branch is not a one-line edit | R460-2 (delta) over R460-1 | 4298ed2595d98ec98592bea4e05c4d1744663c34 |
| Robustness | CLEAN | Campaign at `JOBS=8` through make, and the five new or changed arms plus the control at `--jobs 1`: identical verdicts, tallies and FAIL lines (`receipts/static/j8-vs-j1.txt`). Each unit ran in a private copy. The follow-up feeds `cell_ok` (`y4`). The GM-mismatch follow-up has teeth of its own (`y1`, `y3`). Without the follow-up, r6 survives (`y2`), so the step is what kills it. No out-of-memory event in the unit (peak at the 12 GiB cap from page cache, `oom_kill 0`) | R460-2 | 4298ed2595d98ec98592bea4e05c4d1744663c34 |
| Tests | CLEAN | `tb/adp_engine` rc 0, 1334 of 1334. Campaign 41 of 41 (2 controls, 39 KILLED), every count equal to its README row (`receipts/static/campaign-vs-readme.txt`; two older pp_top rows state their current count in their text, unchanged since round 1). R460-1's `probes.py` unchanged: r6 now red, the rest as before (`receipts/static/probes-r1-vs-round1.txt`). Round-2 probes `y1` to `y6`. S2-1 is a suggestion only | R460-2 | 4298ed2595d98ec98592bea4e05c4d1744663c34 |
| Docs | CLEAN (R2-1 is RESIDUE) | `make check` rc 0 in a disposable clone at the head: lint 41 mermaid and 18 wavedrom blocks, links 1120, matrix 115 REQ / 17 GAP, `gen_matrix` 94 rows with 0 untested, parameters 28. README: check count 1334, the follow-up paragraph, the arc paragraph, the round-2 campaign sentence, three changed rows and the new row against their FAIL lines, and the `JOBS=N` sentence. No stale 1330 or "38 of 38" claim remains outside the dated round-1 sentence. PR body round-2 section: every figure checked against this review's runs; R-1 wording now exact. Privacy sweep of the delta, the commit messages and the PR body: no entity id, MAC address, host path or e-mail | R460-2 | 4298ed2595d98ec98592bea4e05c4d1744663c34 |

## Prior public review findings (read only after the verdict and ledger above were written)

The prior public reviews on PR #152 are R460-1 (comment 5975297523; its items are resolved in the table above) and R461-1 (comment 5975267550, POSITIVE at `a8669732`). PR #152 has no review objects and no review comments. R461-2 had only its start notice when read. Each R461-1 item, at this head:

| Item | Disposition at `4298ed25` | Evidence |
|---|---|---|
| R461-1-R1, RESIDUE (`tb/adp_engine/README.md:100`: "The table above gives each cell's class and Milan clause") | **Retained** as RESIDUE with its stated fix. Round 2 did not touch the line, as the PR body says, and the table at `:88-98` still gives a clause only for the N cells and WAITING × ENTITY_DISCOVER | `README.md:98-101` at the head; round-2 hunks start at `:6`, then `:147` and later |
| R461-1-S1, SUGGESTION (citation counts test a prefix only) | **Retained** as SUGGESTION; not taken (PR body, round 2 item 4) | R460-1's `t3` gives the same result at this head (42 of 45 on a dropped clause) |
| R461-1-S2, SUGGESTION (the restart arc's noted index and the NOADP value are caught by directed phases only) | **Retained** as SUGGESTION; not taken. The round-2 follow-up exercises the restart pair after a fresh index, but it does not grade the index the restart arc itself notes | R460-1's `r7-restart-no-store` at this head: rc 2, its one failure is `P9e2 restart stored the new index`, as at `a8669732` |
| R461-1-S3, SUGGESTION (`make mutants` jobs) | **Resolved** by `JOBS ?= 4` and `--jobs $(JOBS)` (the same as R460-1 S-2) | `Makefile:5`, `:25`; `make -n` and the `JOBS=8` campaign |

None of these changes the verdict.

## Receipts (all listed in MANIFEST.sha256)

- `receipts/suites/`:
  - head `tb/adp_engine` run, 1334 of 1334;
  - head `make check`, which includes `gen_matrix --check`;
  - head `lint_hdl.sh`;
  - each with an `.rc`.
- `receipts/campaign-make-j8/`: the full campaign through `make mutants JOBS=8`, with one log per unit.
- `receipts/campaign-arc-j1/`: the five new or changed arms and the control at `--jobs 1`.
- `receipts/probes-r1/`: R460-1's `probes.py`, rerun unchanged, with a summary and one log per probe.
- `receipts/probes-r2/`: round-2 probes `y1` to `y6`.
- `receipts/static/`:
  - comment-only proof;
  - campaign counts against the README and round 1;
  - round-1 against round-2 probe outcomes;
  - `JOBS=8` against `--jobs 1`.
- `receipts/hosted-check-runs.txt`, `receipts/evidence-read.txt`, `receipts/simulator-identity.txt`, `receipts/clone-integrity.txt`.
- `scripts/`:
  - `probes.py` (R460-1's, byte-identical) and `probes2.py`;
  - `strip_compare.py`, `compare_counts.py`, `launch.sh` and `verify_clone.sh`.

  All are path-parameterised.
- Host paths in the logs are redacted to `<SIM_ROOT>`, `<SCRATCH>`, `<PACKET>` and `<CLONE>`.

## Real limits

- The Milan v1.2 and IEEE 1722.1-2021 texts were not available. Clause references were checked for consistency between 04 F04.8, the C++ tables, the README and the engine comments, not against the documents.
- Banks that were not allowed here were not run: `scripts/run_suites.sh`, Yosys, the parent consumer set and the builder. The PR body's figures for them (33 suites, 1,021,455 checks, which is round 1's 1,021,451 + 4; Yosys 42 tops; parent gates 1 to 9s, 11, 13, 14, 17 re-run) are the author's and the manager's. The manager's banks at this head are reported passed.
- The pinned evidence packet (`milan-fpga` `4b05825f`, `review-evidence/pp85-r1`) is round 1's archive (committed 2026-10-04T00:50:25Z). It holds the author HANDOFF, PR bodies and adoption patches only. When read, issue #85 and PR #152 carried no manager evidence comment. This review relied on its own runs for every figure it grades.
- Hosted runs at the exact head, read 2026-10-04T01:58Z: `docs-gates` success (2 runs) and `portability` success (2 runs). `suites` was in progress (2 runs, no conclusion). Those were the only contexts, and none was skipped. Hosted and act acceptance belong to the manager.
- This repository has no submodules (0 gitlinks at the head and at the base), so there was no gitlink to verify.
- Physical calibration NOT RUN. Field skips are not hardware proof. How a live controller handles an ENTITY_DEPARTING remains unrecorded, as the README states.
- The final current-dev candidate (source base `5c71928a`, live dev `241f91845230ae410506dffb16b71937127fd175`) was not built.

## Pending manager duties

- Carry R2-1 (the exact README and PR-body sentences above) to the residue checklist, and S2-1 as a suggestion.
- Confirm the hosted `suites` conclusion at the exact head, and own hosted/act acceptance.
- At the merge turn, build the current-dev candidate (source base `5c71928a` against live dev `241f9184`). Run the parent consumer set, with gate 16's T30 failures attributed to milan-fpga #643 as the lane records them. Gates 10, 12, 15, 16 and 16b were not re-run at `4298ed2`; that rests on the preprocessed-identical RTL, which this review confirmed for `KL_adp_engine.sv`, the only `hdl/` file changed since `a866973`.
- Two independent positive reviews and the full completion bar are still required before merge.

R460-2 FINISHED
