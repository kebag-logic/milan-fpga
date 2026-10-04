[R460] NEGATIVE - exact head a8669732b30436c641d51829950c204defd57a30

# R460-1: internal independent review of issue #85 / PR #152 (GAP-16, ADP MTXW walk)

- Exact head `a8669732b30436c641d51829950c204defd57a30`, tree `0bb0763a562807b53ecaed11a4109473139aa982`; source base `5c71928ad2bf1a854a5538d69b77214dfdf1697f`.
- Scope: tests and the documents they cite. `git diff 5c71928a..a8669732 -- hdl syn scripts .github Makefile` is empty. The diff covers 14 files: `docs/00`, `docs/architecture/04`, `docs/architecture/09`, `tb/adp_engine/{README.md, mutants.py, sim_main.cpp}` and eight new `tb/adp_engine/mutations/arc-*.patch` files (all mode 100644).
- Reconstruction order:
  1. This repository has no AGENTS.md or CONTRIBUTING.md, so the conventions came from `README.md` and `docs/README.md`.
  2. Issue #85: its body (frozen acceptance 1 to 4) and the manager's lane comment (scope, items 1 to 4, gates).
  3. 04 §5, §6.1 and §6.2, and F04.2, F04.3, F04.7 and F04.8.
  4. The diff and its 6 commits.
  5. The published `review-evidence/pp85-r1` packet.
  6. The parent's B6, B7 and B8 enumeration records, read-only.
- Prior public review findings on PR #152: none existed when this review started. The PR then carried only the two review-start comments; no review objects existed.
- Simulator: pinned Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`; wrapper sha256 in `receipts/simulator-identity.txt`).
- Everything ran in disposable copies under the packet's scratch directory. The review clone was never written; its integrity was checked afterwards (`receipts/clone-integrity.txt`).

## Verdict

NEGATIVE. One MINOR finding is open (F-1, Tests lens).

The F04.2 and F04.3 walk is complete:
- It is driven by an independent table and ends with its cell counts.
- Each cell's citations agree with 04 F04.7 and F04.8.
- The five cells issue #85 named are graded.
- 38 of 38 arms are KILLED, with both controls passing.
- Each `arc-` arm fails its own arc's check.
- The available_index adjudication matches the published records.

The gap is one action of the F04.3 fresh-index arc: "note the index" (F04.8 arc 4; Milan §5.6.4.5.2 step 3). Neither the walk nor any directed phase grades it. A one-line RTL fault that drops it passes both `tb/adp_engine` (1330 of 1330) and `tb/pp_top` (10416 of 10416). With that action unnoted, the restart detector (REQ-ADP-013) compares against a stale last index.

## Findings

### F-1: MINOR. The fresh-index arc's "note the index" action is graded nowhere; a fault that drops it survives every suite

- **Lens:** Tests.
- **Where:**
  - `tb/adp_engine/sim_main.cpp:1515-1576` (`walk_discovery_cell`) and the arc table `:327-336` (arc "DISCOVERED -> DISCOVERED (index > last)", cell `V_FRESH x D_DISC`).
  - The directed P9b (`:975-981`) and P9e (`:1015-1033`) phases.
  - The action is listed in `docs/architecture/04_adp_engine.md` F04.8, row "TK_DISCOVERED to itself, fresh": "note the index, restart T-ADP-NOADP". The RTL that implements it is `hdl/adp/KL_adp_engine.sv:358-360`.
- **Authority:**
  - Milan v1.2 §5.6.4.5.2 step 3, as 04 F04.8 derives it: the fresh-index arc notes the received `available_index` and restarts T-ADP-NOADP.
  - REQ-ADP-013 (00 §6): an index at or below the last one means talker-restart handling, which only works if the last one is kept current.
  - Issue #85 acceptance 3 and the lane's item 3: every F04.3 arc in the walk, the restart detector named.
  - README `:62-64` and F04.8's preamble state that every cell's observables are compared with the cell and that each arc's check is the arc's.
- **Evidence** (`receipts/probes/probes-summary.txt` and `receipts/suites/probe-r6-pp_top-run.log`; reproduced by `scripts/probes.py`):
  - **`r6-fresh-no-store`:** removes `rec_wr_en_w = 1'b1;` from the fresh branch (`KL_adp_engine.sv:359`) and keeps the T-ADP-NOADP re-arm. Result: rc 0, 1330 checks, 1330 PASS. Under the same fault, `make -C tb/pp_top run` gives rc 0, 10416 checks, 10416 PASS.
    - The arc 4 cell grades the bound and discovered bits, the event sequence, the timer arm and the absence of any frame. It does not grade the noted index, which only a following ADPDU can expose.
    - P9e2 grades the index noted by the restart arc (probe `r7-restart-no-store` is caught by P9e2). Nothing grades the index noted by the fresh arc.
    - For comparison, `r8-discover-no-store` (arc 2 notes nothing) is caught only incidentally, by arcs 5 and 6. Arc 2's own check stays green.
  - **`x1-fresh-noted-check`:** adds one follow-up to the walk. Discover at index 700, send a fresh 701, then repeat 701, and require the restart pair (DEPARTED then DISCOVERED). It passes on the head RTL (1334 of 1334).
  - **`x2-fresh-noted-check-vs-r6`:** the same check under the r6 fault fails exactly that check: `got 0 events`.
- **Impact:**
  - A regression in the restart detector's state update, the behaviour REQ-ADP-013 and Milan §5.6.4.5.2 step 2 rely on, can merge with every processor suite green.
  - In the field, a listener would keep the index of its first discovery as "last". After a talker restart whose first heard index is above that value, the listener would not raise the DEPARTED/DISCOVERED pair, so ACMP would not re-probe.
  - The RTL at this head is correct. The defect is the missing verification of an action this PR's own F04.8 assigns to the arc.
- **Required outcome:**
  1. Grade the noted index inside the arc 4 cell, or as a follow-up step of it whose failure clears `cell_ok` for that cell. Example: after the fresh AVAILABLE at last + 1, an AVAILABLE repeating that index must produce the restart pair. Apply the same treatment to the other step-3 cell (`V_GMF x D_DISC`), if its index is also meant to be noted.
  2. Plant an `arc-fresh-no-store` arm (the r6 edit) that must fail `P13 F04.3 arc DISCOVERED -> DISCOVERED (index > last)`.
  3. Update the README mutation record and its check count.
- **Verification:** `make -C tb/adp_engine run` passes. `python3 tb/adp_engine/mutants.py --jobs N` shows both controls PASS and 39 of 39 arms KILLED, with the new arm naming arc 4's check. This review's `x1` and `x2` probes show that four added checks are enough.

### R-1: RESIDUE. The PR body suggests `make mutants` takes `--jobs N`

- **Lens:** Docs (PR body wording only).
- **Where:** PR #152 body, item 3: "the campaign (`make -C tb/adp_engine mutants`, `--jobs N`) kills 38 of 38 arms".
- **Evidence:** `tb/adp_engine/Makefile`'s `mutants` target runs `python3 mutants.py --output "$(MUTANT_OUTPUT)"`, so it always uses the default of 4. `--jobs N` belongs to `mutants.py`. The README (`:226-229`) states this correctly.
- **Exact fix:** replace that parenthesis with "(`make -C tb/adp_engine mutants` at the default 4 jobs, or `python3 tb/adp_engine/mutants.py --output DIR --jobs N`)".
- **Effect:** none on any measurement, test, verdict or claim. The verdict stays as given and no lens is left unclean.

### S-1: SUGGESTION. The engine's comments still carry the pre-adjudication warning

`hdl/adp/KL_adp_engine.sv:703-707` (and the banner the PR body mentions) still says the rule "diverges from the reference platform's every-ADPDU increment; adjudication against live controllers is required before cutover". The README now reads it the other way: the former rule diverged from IEEE §6.2.2.15, and only the live-controller handling of an ENTITY_DEPARTING remains open. This lane may not touch `hdl/`, so carry the restatement to the next lane that edits `hdl/adp`.

### S-2: SUGGESTION. `make mutants` cannot set the campaign's job count

Add `MUTANT_JOBS ?= 4` and pass `--jobs $(MUTANT_JOBS)` in `tb/adp_engine/Makefile`, so that the manager's concurrency rule applies through `make` as well.

## Concurrent public review (read only after this verdict and ledger were written)

The external reviewer posted R461-1 (POSITIVE) on PR #152 at 2026-10-04T01:09:30Z, after this review started. It is not a prior review. Each of its items, at this head:

| Item | Disposition |
|---|---|
| R461-1-R1, RESIDUE (`tb/adp_engine/README.md:100`) | Concur and retain as RESIDUE with its stated fix. The README table at `:88-98` gives a clause only for the N cells and for WAITING × ENTITY_DISCOVER (another entity_id). |
| R461-1-S1, SUGGESTION (citation checks test prefixes only) | Concur. This review's `t3` likewise shows that the count reacts to a missing clause; a wrong clause would pass. |
| R461-1-S2, SUGGESTION (the restart-store and NOADP-value actions are caught only by directed phases) | Consistent with this review's `r7` (caught only by P9e2). It does not cover F-1: the fresh-index store (`r6`) is caught by no phase at all, in `tb/adp_engine` or in `tb/pp_top`. F-1 therefore stays MINOR. |
| R461-1-S3, SUGGESTION (`make mutants` jobs) | Same observation as R-1 and S-2 here. |

## Lens ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | F04.7 compared cell by cell with the C++ `ADV` table: 45 cells, next state, draws, arms, cancel, frame and both citations. F04.8 compared arc by arc with `DISC` and `F043_ARCS`: 33 cells, 8 arcs. README walk tables against both. 04 §5 and 00 §6 REQ-ADP-011 changed from §6.2.2.9 to §6.2.2.15, consistent with 04's own IEEE §6.2.2 field numbering (§6.2.2.5, .15, .16, .17, .18, .20). The seven re-cited cells the PR body lists. The adjudication's reasoning: DEPARTING is the only ADPDU where the two rules differ; `r4-departing-increments` confirms the walk tells them apart. The five cells, by arms and by probes `r1`, `r2` and `r3` | R460-1 | a8669732b30436c641d51829950c204defd57a30 |
| RTL | CLEAN | No `hdl/`, `syn/` or `scripts/` change (empty diff). All 16 RTL patches the campaign plants applied with `git apply --check` to the head `hdl/` (40 units ran). The eight `arc-` patches touch the lines F04.8 names (`KL_adp_engine.sv:350`, `:354`, `:358`, `:359-360`, `:361`, `:375`, `:415`, `:1070`) | R460-1 | a8669732b30436c641d51829950c204defd57a30 |
| Robustness | CLEAN | Campaign at `--jobs 10` (40 of 40) and the eight `arc-` arms again at `--jobs 1`: identical verdicts, counts and FAIL lines. Every unit ran in a scratch copy of its own. The `arc-` expected labels are unique prefixes. Each `arc-` arm fails a post-stimulus grading line inside its own arc's cell, not only the setup's `reached` check. The cited-cell, cell-count and arc-count checks have teeth (probes `t1`, `t2` and `t3`) | R460-1 | a8669732b30436c641d51829950c204defd57a30 |
| Tests | UNCLEAN (F-1) | `tb/adp_engine` at the head (rc 0, 1330 of 1330) and at the base (rc 0, 1328 of 1328): the two new citation checks are the whole delta. Campaign: 2 controls PASS, 38 of 38 KILLED, every count equal to its README row. Eleven reviewer fault probes (`r1` to `r8`, `t1` to `t3`) plus `x1`/`x2`: `r6` survives `tb/adp_engine` and `tb/pp_top` | R460-1 | a8669732b30436c641d51829950c204defd57a30 |
| Docs | CLEAN | `make check` rc 0 (wavedrom, links 1120, matrix 115 REQ / 17 GAP, 94 rows, params). `gen_matrix.py --check` rc 0 (94 rows, 0 untested). README check count, class counts (12/20/6/7 and 13/15/2/3) and mutation record. 09 §3 sentence. PR body against the published `PR-BODY.md` (identical but for one trailing newline). B6, B7 and B8 figures recomputed (`receipts/aidx_rates.txt`): peer 6.000 / 6.004 / 5.992 / 5.983 s per increment; processor 6.988 and 6.965 s; restarts at 85 and 19. The parent register-map sentence is quoted correctly. Privacy sweep: no device name, entity id or model id from the records appears in the diff, the commit messages or the PR body. R-1 is RESIDUE only | R460-1 | a8669732b30436c641d51829950c204defd57a30 |

## Acceptance (issue #85, with the lane's items)

| Item | Status at this head |
|---|---|
| 1. F04.2 walk from an independent table, ending with a cell count | Met. `ADV[9][5]` is transcribed from Milan, never from RTL. The walk ends with `CHECK(adv_cells == 45)` and `CHECK(disc_cells == 33)`, and its teeth were proven by `t2`. Each cell carries its Milan and IEEE clauses (45 of 45 and 33 of 33, proven by `t3`), and the table drives the expectations (`t1`) |
| 2. The five cells | Met. DOWN × DISCOVER, GM_CHANGE and SHUTDOWN are inert (arms `walk-down-*`). DELAY × LINK_DOWN cancels the timer and sends no DEPARTING (`walk-delay-ignores-link-down`, `walk-link-down-keeps-timer`, probe `r2`). DELAY × SHUTDOWN departs and resets the index in both phases from a non-zero index (1 and 2) (`walk-delay-shutdown-silent`, `walk-departing-keeps-index`, `r1`, `r4`) |
| 3. F04.3 arcs in the same walk, with the named mutants and one per arc | Met to the letter: 8 `arc-` arms, each killed through its own arc's check, plus the two named arms. F-1 leaves one arc action (the fresh index's "note the index") unverified |
| 4. available_index interop | Adjudicated as the lane allows. §6.2.2.15 stands, and the limit is restated and narrowed to how a live controller handles an ENTITY_DEPARTING. The cited records support every figure |

## Receipts (all listed in MANIFEST.sha256)

- `receipts/suites/`: head and base `tb/adp_engine`, head `make check`, `gen_matrix --check`, and the `tb/pp_top` run under the r6 fault (each with an `.rc`).
- `receipts/campaign-j10/`: the full campaign at `--jobs 10`, with one log per unit.
- `receipts/campaign-arc-j1/`: the eight `arc-` arms at `--jobs 1`.
- `receipts/probes/`: reviewer fault probes, with `probes-summary.txt` and one log per probe.
- `receipts/aidx_rates.txt`: B6, B7 and B8 index readings by role, with no identities.
- `receipts/evidence-read.txt`: hashes of the evidence read.
- `receipts/hosted-check-runs.txt`, `receipts/simulator-identity.txt`, `receipts/clone-integrity.txt`.
- `scripts/probes.py`, `scripts/aidx_rates.py`, `scripts/verify_clone.sh`: portable, path-parameterised.
- Host paths in the logs are redacted to `<SIM_ROOT>`, `<SCRATCH>`, `<PACKET>` and `<CLONE>`.

## Real limits

- The Milan v1.2 and IEEE 1722.1-2021 texts were not available to this review. Clause numbers and quotations were checked for consistency between 04 F04.7/F04.8, the C++ tables, the README and 04's own field numbering, and against the reviewer's reading of the standards' structure, not against the documents. The §6.2.2.15 quotation in the README was not checked word for word.
- No full processor, parent, Yosys or builder bank was run (not allowed). `scripts/run_suites.sh`, `lint_hdl.sh`, `syn/yosys/run.sh` and the parent consumer set of 17 were not re-executed here. They are the manager's.
- The published `review-evidence/pp85-r1` packet at `4b05825f` holds only the author's HANDOFF, PR bodies and adoption patches. No manager evidence comment was on issue #85 or PR #152 when this review read them, so this review relied on its own runs for every figure it grades.
- Hosted runs at the exact head, when last read: `docs-gates` success (2 runs), `portability` success (2 runs), `suites` in progress (2 runs, no conclusion). Only these three contexts exist, and none was skipped. Hosted and act acceptance belong to the manager.
- The live-controller handling of an ENTITY_DEPARTING remains unrecorded, as the README states. Physical calibration was NOT RUN, and field skips are not hardware proof.
- The final current-dev candidate (live dev `241f91845230ae410506dffb16b71937127fd175`) was not built; that is the manager's merge-turn duty.

## Pending manager duties

- Carry F-1 back to the author lane. Re-review is needed after the fix (a new head).
- Carry R-1 (the exact PR-body fix above) to the residue checklist, and S-1/S-2 as suggestions.
- Confirm the hosted `suites` conclusion at the exact head, and own hosted/act acceptance.
- At the merge turn: the source-base versus live-dev candidate build, the parent consumer set at dev `5fabb46e` + c8 + p2-p1 + c10, with gate 16's T30 failures attributed to #643 / PR #648 as the lane records them.
- #39, #40 and #41 are closed and cited as "Relates to". Their acceptance still holds at this head (`cfg-*`, `gate-enable-dropped*` KILLED; P11 and P12 PASS).

R460-1 FINISHED
